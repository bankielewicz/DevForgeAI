"""
MigrationRunner service for executing migration scripts (STORY-078).

Implements:
- SVC-011: Execute migration scripts in order
- SVC-012: Capture script output for logging
- SVC-013: Stop on first failure
- SVC-014: Track successfully applied migrations

Follows clean architecture with dependency injection.
"""

import subprocess
import sys
import logging
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple
from abc import ABC, abstractmethod
from dataclasses import dataclass

from installer.models import MigrationScript, MigrationError


logger = logging.getLogger(__name__)

# Subprocess constants
DEFAULT_MIGRATION_TIMEOUT = 300
SUBPROCESS_ENCODING = "utf-8"


@dataclass
class MigrationResult:
    """Result of executing a single migration."""

    script: MigrationScript
    success: bool
    exit_code: int
    stdout: str
    stderr: str
    error_message: Optional[str] = None


@dataclass
class MigrationRunResult:
    """Result of running all migrations."""

    all_success: bool
    applied_count: int
    failed_at_migration: Optional[MigrationScript] = None
    failed_migration_result: Optional[MigrationResult] = None
    results: List[MigrationResult] = None

    def __post_init__(self) -> None:
        """Initialize results list if not provided."""
        if self.results is None:
            self.results = []


class IMigrationRunner(ABC):
    """Interface for migration execution."""

    @abstractmethod
    def run(
        self, migrations: List[MigrationScript], timeout_seconds: int = 300
    ) -> MigrationRunResult:
        """Execute migration scripts."""
        pass


class MigrationRunner(IMigrationRunner):
    """Executes migration scripts in sequence."""

    def __init__(self, python_executable: Optional[str] = None) -> None:
        """
        Initialize MigrationRunner.

        Args:
            python_executable: Path to Python executable.
                Defaults to sys.executable
        """
        if python_executable is None:
            python_executable = sys.executable
        self.python_executable = python_executable

    def _run_subprocess(
        self, cmd: List[str], timeout_seconds: int
    ) -> Tuple[int, str, str]:
        """
        Execute a subprocess with timeout handling.

        Args:
            cmd: Command and arguments to execute
            timeout_seconds: Timeout duration

        Returns:
            Tuple of (exit_code, stdout, stderr)
        """
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            try:
                stdout, stderr = process.communicate(timeout=timeout_seconds)
                return process.returncode, stdout, stderr
            except subprocess.TimeoutExpired:
                process.kill()
                stdout, stderr = process.communicate()
                stderr += f"\nMigration timeout after {timeout_seconds} seconds"
                return -1, stdout, stderr

        except Exception as e:
            raise MigrationError(f"Subprocess execution failed: {e}")

    def run(
        self, migrations: List[MigrationScript], timeout_seconds: int = 300
    ) -> MigrationRunResult:
        """
        Execute migration scripts in order.

        Each migration script is executed as a subprocess using Python.
        Output is captured for logging. Execution stops on first failure.

        Args:
            migrations: List of migration scripts in order
            timeout_seconds: Timeout per migration script (default 300 seconds)

        Returns:
            MigrationRunResult with execution details
        """
        if not migrations:
            return MigrationRunResult(all_success=True, applied_count=0)

        results: List[MigrationResult] = []
        total_migrations = len(migrations)

        for index, migration in enumerate(migrations):
            position = index + 1
            logger.info(
                f"Running migration {position} of {total_migrations}: "
                f"{migration.from_version} → {migration.to_version}"
            )

            try:
                result = self._execute_migration(
                    migration, position, total_migrations, timeout_seconds
                )
                results.append(result)

                if not result.success:
                    logger.error(
                        f"Migration failed at {position} of {total_migrations}: "
                        f"{result.error_message}"
                    )
                    return MigrationRunResult(
                        all_success=False,
                        applied_count=index,  # Number successfully applied before failure
                        failed_at_migration=migration,
                        failed_migration_result=result,
                        results=results,
                    )

                logger.info(
                    f"Migration {position} of {total_migrations} completed successfully"
                )

            except MigrationError as e:
                logger.error(f"Migration execution error: {e}")
                return MigrationRunResult(
                    all_success=False,
                    applied_count=index,
                    failed_at_migration=migration,
                    failed_migration_result=None,
                    results=results,
                )

        # All migrations succeeded
        return MigrationRunResult(
            all_success=True,
            applied_count=len(migrations),
            results=results,
        )

    def _execute_migration(
        self,
        migration: MigrationScript,
        position: int,
        total: int,
        timeout_seconds: int,
    ) -> MigrationResult:
        """
        Execute a single migration script.

        Args:
            migration: MigrationScript to execute
            position: Current position in sequence
            total: Total number of migrations
            timeout_seconds: Execution timeout

        Returns:
            MigrationResult with execution details

        Raises:
            MigrationError: If execution fails
        """
        try:
            # Prepare command
            script_path = Path(migration.path)
            if not script_path.exists():
                raise MigrationError(f"Migration script not found: {migration.path}")

            # Make script executable (Unix)
            try:
                import os
                import stat
                st = os.stat(script_path)
                os.chmod(script_path, st.st_mode | stat.S_IEXEC)
            except (OSError, AttributeError):
                pass  # May fail on Windows, that's OK

            # Execute with Python
            cmd = [self.python_executable, str(script_path)]

            logger.debug(f"Executing: {' '.join(cmd)}")

            # Execute subprocess
            exit_code, stdout, stderr = self._run_subprocess(cmd, timeout_seconds)

            # Determine success
            success = exit_code == 0

            if success:
                logger.info(
                    f"Migration output:\n{stdout}" if stdout else "Migration completed"
                )
            else:
                logger.error(
                    f"Migration stderr:\n{stderr}" if stderr else "Unknown error"
                )

            return MigrationResult(
                script=migration,
                success=success,
                exit_code=exit_code,
                stdout=stdout,
                stderr=stderr,
                error_message=None if success else (stderr or f"Exit code: {exit_code}"),
            )

        except Exception as e:
            raise MigrationError(f"Failed to execute migration: {e}")

    def get_applied_migrations(self, run_result: MigrationRunResult) -> List[str]:
        """
        Get list of successfully applied migrations.

        Args:
            run_result: Result from run()

        Returns:
            List of migration script paths that succeeded
        """
        applied = []
        for result in run_result.results:
            if result.success:
                applied.append(result.script.path)
            else:
                break  # Stop at first failure

        return applied

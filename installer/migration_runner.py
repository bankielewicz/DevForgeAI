"""
STORY-078: Migration Runner Service.

Executes migration scripts in sequence with output capture and error handling.

AC Mapping:
- AC#4: Migration Script Execution
  - Scripts run in version order (oldest to newest)
  - Each script's progress displayed to user
  - Script output (stdout/stderr) captured in logs
  - Script failure triggers immediate rollback
  - Successful migrations recorded for rollback reference

Technical Specification:
- SVC-011: Execute migration scripts in order
- SVC-012: Capture script output for logging
- SVC-013: Stop on first failure
- SVC-014: Track successfully applied migrations
"""

import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Any


@dataclass
class MigrationScript:
    """
    Data model for a migration script to execute.

    Attributes:
        path: Absolute path to the Python migration script.
        from_version: Source version this migration upgrades from.
        to_version: Target version this migration upgrades to.
    """
    path: Path
    from_version: str
    to_version: str


@dataclass
class AppliedMigration:
    """
    Record of a successfully applied migration.

    Captures execution details including output and timing for audit purposes.

    Attributes:
        path: Path to the executed script.
        from_version: Source version.
        to_version: Target version.
        stdout: Captured standard output.
        stderr: Captured standard error.
        exit_code: Process exit code (0 for success).
        executed_at: Timestamp when execution started.
        duration_seconds: Total execution time.
    """
    path: Path
    from_version: str
    to_version: str
    stdout: str = ""
    stderr: str = ""
    exit_code: int = 0
    executed_at: Optional[datetime] = None
    duration_seconds: float = 0.0


@dataclass
class FailedMigration:
    """
    Record of a failed migration.

    Captures failure details for error reporting and rollback decisions.

    Attributes:
        path: Path to the failed script.
        from_version: Source version.
        to_version: Target version (not reached).
        stdout: Captured standard output before failure.
        stderr: Captured standard error.
        exit_code: Non-zero process exit code.
        error_message: Human-readable error description.
    """
    path: Path
    from_version: str
    to_version: str
    stdout: str = ""
    stderr: str = ""
    exit_code: int = 1
    error_message: str = ""


@dataclass
class MigrationRunResult:
    """
    Result of running a migration sequence.

    Attributes:
        success: True if all migrations completed successfully.
        applied_migrations: List of successfully executed migrations.
        failed_migration: Details of the first failed migration, if any.
        should_rollback: True if failure requires rollback to backup.
    """
    success: bool
    applied_migrations: List[AppliedMigration] = field(default_factory=list)
    failed_migration: Optional[FailedMigration] = None
    should_rollback: bool = False


class MigrationRunner:
    """
    Executes migration scripts in sequence (AC#4).

    Runs Python migration scripts in order, capturing output and stopping
    on the first failure. Each migration's progress is logged, and
    successful migrations are tracked for potential rollback.
    """

    DEFAULT_TIMEOUT = 300  # 5 minutes default

    def __init__(self, logger: Any = None, timeout_seconds: Optional[int] = None) -> None:
        """
        Initialize migration runner.

        Args:
            logger: Optional logger for progress and output messages.
            timeout_seconds: Timeout per migration script in seconds (default 300).
        """
        self._logger = logger
        self._timeout_seconds = timeout_seconds or self.DEFAULT_TIMEOUT

    @property
    def logger(self) -> Any:
        """Return the logger instance (for backward compatibility)."""
        return self._logger

    @property
    def timeout_seconds(self) -> int:
        """Return the timeout setting in seconds."""
        return self._timeout_seconds

    def run(self, migrations: List[MigrationScript], project_root: Path) -> MigrationRunResult:
        """
        Execute migration scripts in order (SVC-011).

        Runs each migration script sequentially, stopping on the first failure.
        Output from each script is captured and logged.

        Args:
            migrations: List of MigrationScript objects to execute in order.
            project_root: Path to project root (passed to scripts as argument).

        Returns:
            MigrationRunResult with success status and applied/failed migrations.

        Raises:
            FileNotFoundError: If project_root doesn't exist.
        """
        if not project_root.exists():
            raise FileNotFoundError(f"Project root not found: {project_root}")

        result = MigrationRunResult(success=True)

        if not migrations:
            return result

        for migration in migrations:
            self._log_migration_start(migration)

            execution_result = self._execute_migration(migration, project_root)

            if execution_result.exit_code == 0:
                result.applied_migrations.append(execution_result)
                self._log_migration_success(migration, execution_result.duration_seconds)
            else:
                self._record_failure(result, migration, execution_result)
                break  # Stop on first failure (SVC-013)

        return result

    def _log_migration_start(self, migration: MigrationScript) -> None:
        """Log the start of a migration execution."""
        if self._logger:
            self._logger.log_info(
                f"Starting migration: {migration.from_version} -> {migration.to_version}"
            )

    def _log_migration_success(self, migration: MigrationScript, duration: float) -> None:
        """Log successful completion of a migration."""
        if self._logger:
            self._logger.log_info(
                f"Completed migration: {migration.from_version} -> {migration.to_version} "
                f"(duration: {duration:.2f}s)"
            )

    def _record_failure(
        self,
        result: MigrationRunResult,
        migration: MigrationScript,
        execution: AppliedMigration
    ) -> None:
        """Record a migration failure in the result and log the error."""
        result.success = False
        result.should_rollback = True
        result.failed_migration = FailedMigration(
            path=migration.path,
            from_version=migration.from_version,
            to_version=migration.to_version,
            stdout=execution.stdout,
            stderr=execution.stderr,
            exit_code=execution.exit_code,
            error_message=execution.stderr or f"Migration failed with exit code {execution.exit_code}"
        )

        if self._logger:
            self._logger.log_error(
                message=f"Migration failed: {migration.from_version} -> {migration.to_version}",
                source_path=str(migration.path)
            )

    def _execute_migration(self, migration: MigrationScript, project_root: Path) -> AppliedMigration:
        """
        Execute a single migration script (SVC-012).

        Runs the migration script as a subprocess, capturing stdout/stderr
        and enforcing a timeout.

        Args:
            migration: MigrationScript to execute.
            project_root: Path to pass to migration script as argument.

        Returns:
            AppliedMigration with captured stdout/stderr and exit code.
        """
        result = AppliedMigration(
            path=migration.path,
            from_version=migration.from_version,
            to_version=migration.to_version,
            executed_at=datetime.now()
        )

        # Validate script exists before attempting execution
        if not migration.path.exists():
            return self._create_not_found_result(result, migration.path)

        start_time = time.time()
        self._run_subprocess(result, migration.path, project_root)
        result.duration_seconds = time.time() - start_time

        return result

    def _create_not_found_result(
        self, result: AppliedMigration, script_path: Path
    ) -> AppliedMigration:
        """Create a failed result for a missing script file."""
        result.exit_code = 1
        error_msg = f"Migration script not found: {script_path}"
        result.stderr = error_msg
        return result

    def _run_subprocess(
        self, result: AppliedMigration, script_path: Path, project_root: Path
    ) -> None:
        """
        Run the migration script as a subprocess.

        Updates the result object in place with stdout, stderr, and exit code.

        Args:
            result: AppliedMigration object to update.
            script_path: Path to the migration script.
            project_root: Working directory for the subprocess.
        """
        try:
            process = subprocess.run(
                [sys.executable, str(script_path), str(project_root)],
                capture_output=True,
                text=True,
                timeout=self._timeout_seconds,
                cwd=str(project_root)
            )

            result.stdout = process.stdout
            result.stderr = process.stderr
            result.exit_code = process.returncode

            # Log captured output (SVC-012)
            if self._logger and process.stdout:
                self._logger.log_info(f"Migration output:\n{process.stdout}")

        except subprocess.TimeoutExpired as e:
            result.exit_code = 1
            result.stderr = f"Migration timeout after {self._timeout_seconds} seconds"
            result.stdout = e.stdout.decode() if e.stdout else ""

        except Exception as e:
            result.exit_code = 1
            result.stderr = str(e)

"""
STORY-078: Upgrade Orchestrator Service.

Orchestrates the full upgrade workflow including detection, backup,
migration, validation, and rollback.

AC Mapping:
- AC#1: Upgrade Detection
- AC#2: Pre-Upgrade Backup Creation
- AC#6: Version Metadata Update
- AC#7: Automatic Rollback on Failure
- AC#8: Upgrade Summary Display

Technical Specification:
- SVC-001: Detect upgrade scenario by comparing versions
- SVC-002: Orchestrate upgrade workflow (backup -> migrate -> validate -> update)
- SVC-003: Trigger rollback on any failure
"""

import json
import shutil
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Any

from installer.version import (
    get_installed_version,
    get_source_version,
    compare_versions,
    MODE_FRESH_INSTALL,
    MODE_PATCH_UPGRADE,
    MODE_MINOR_UPGRADE,
    MODE_MAJOR_UPGRADE,
    MODE_REINSTALL,
    MODE_DOWNGRADE
)


@dataclass
class UpgradeSummary:
    """
    Summary of upgrade operation (AC#8).

    Attributes:
        files_added: Number of new files created.
        files_updated: Number of existing files modified.
        files_removed: Number of files deleted.
        migrations_executed: List of migration script names that ran.
        duration_seconds: Total upgrade duration.
    """
    files_added: int = 0
    files_updated: int = 0
    files_removed: int = 0
    migrations_executed: List[str] = field(default_factory=list)
    duration_seconds: float = 0.0


@dataclass
class DetectionResult:
    """
    Result of upgrade detection (AC#1).

    Attributes:
        is_upgrade: True if source version is newer.
        is_fresh_install: True if no existing installation.
        is_reinstall: True if same version.
        is_downgrade: True if source version is older.
        from_version: Currently installed version.
        to_version: Source package version.
        upgrade_type: "major", "minor", or "patch" for upgrades.
    """
    is_upgrade: bool = False
    is_fresh_install: bool = False
    is_reinstall: bool = False
    is_downgrade: bool = False
    from_version: Optional[str] = None
    to_version: Optional[str] = None
    upgrade_type: Optional[str] = None


@dataclass
class UpgradeResult:
    """
    Result of upgrade execution.

    Attributes:
        success: True if upgrade completed successfully.
        status: "completed", "rolled_back", or "failed".
        from_version: Previous version before upgrade.
        to_version: New version after upgrade.
        migrations_applied: List of applied migration records.
        backup_path: Path to backup created before upgrade.
        rolled_back: True if rollback was triggered.
        error_message: Description of failure, if any.
        duration_seconds: Total upgrade duration.
        summary: Detailed upgrade summary.
        log_file: Path to upgrade log file.
    """
    success: bool
    status: str = "completed"
    from_version: Optional[str] = None
    to_version: Optional[str] = None
    migrations_applied: List[Any] = field(default_factory=list)
    backup_path: Optional[Path] = None
    rolled_back: bool = False
    error_message: Optional[str] = None
    duration_seconds: float = 0.0
    summary: Optional[UpgradeSummary] = None
    log_file: Optional[Path] = None


class UpgradeOrchestrator:
    """
    Orchestrates upgrade workflow (SVC-002).

    Coordinates the full upgrade lifecycle:
    1. Detection - determine upgrade type
    2. Backup - preserve current state
    3. Migration - run upgrade scripts
    4. Validation - verify new state
    5. Update - write new version metadata
    6. Rollback - restore on failure (if needed)
    """

    def __init__(
        self,
        logger: Any = None,
        backup_service: Any = None,
        migration_discovery: Any = None,
        migration_runner: Any = None,
        migration_validator: Any = None
    ) -> None:
        """
        Initialize upgrade orchestrator with dependencies.

        All dependencies are optional for flexibility in testing and production.
        If not provided, orchestrator creates instances as needed.

        Args:
            logger: Logger for progress messages.
            backup_service: BackupService for creating/restoring backups.
            migration_discovery: MigrationDiscovery for finding scripts.
            migration_runner: MigrationRunner for executing scripts.
            migration_validator: MigrationValidator for post-migration checks.
        """
        self._logger = logger
        self._backup_service = backup_service
        self._migration_discovery = migration_discovery
        self._migration_runner = migration_runner
        self._migration_validator = migration_validator

    @property
    def logger(self) -> Any:
        """Return the logger instance (for backward compatibility)."""
        return self._logger

    @property
    def backup_service(self) -> Any:
        """Return the backup service instance."""
        return self._backup_service

    @property
    def migration_discovery(self) -> Any:
        """Return the migration discovery instance."""
        return self._migration_discovery

    @property
    def migration_runner(self) -> Any:
        """Return the migration runner instance."""
        return self._migration_runner

    @property
    def migration_validator(self) -> Any:
        """Return the migration validator instance."""
        return self._migration_validator

    def detect(self, project_root: Path, source_root: Path) -> DetectionResult:
        """
        Detect upgrade scenario (AC#1, SVC-001).

        Compares installed version with source package version to determine
        the installation mode (fresh install, upgrade, reinstall, or downgrade).

        Args:
            project_root: Path to target project.
            source_root: Path to source package.

        Returns:
            DetectionResult with version info and upgrade type.
        """
        result = DetectionResult()

        installed = self._get_installed_version_safe(project_root)
        source = get_source_version(source_root / "devforgeai")
        result.to_version = source.get("version")

        if installed is None:
            return self._detect_fresh_install(result)

        result.from_version = installed.get("version")
        mode = compare_versions(result.from_version, result.to_version)

        return self._classify_installation_mode(result, mode)

    def _get_installed_version_safe(self, project_root: Path) -> Optional[dict]:
        """
        Get installed version, handling corrupted files gracefully.

        Args:
            project_root: Path to target project.

        Returns:
            Version dict, or None if not installed or corrupted.
        """
        devforgeai_path = project_root / ".devforgeai"
        if not devforgeai_path.exists():
            return None

        try:
            return get_installed_version(devforgeai_path)
        except json.JSONDecodeError:
            if self._logger:
                self._logger.log_warning(
                    "Corrupted version file detected, treating as fresh install"
                )
            return None

    def _detect_fresh_install(self, result: DetectionResult) -> DetectionResult:
        """Handle fresh install detection."""
        result.is_fresh_install = True
        result.from_version = None
        if self._logger:
            self._logger.log_info(f"Fresh install detected: v{result.to_version}")
        return result

    def _classify_installation_mode(
        self, result: DetectionResult, mode: str
    ) -> DetectionResult:
        """
        Classify installation mode based on version comparison.

        Args:
            result: DetectionResult to populate.
            mode: Mode from compare_versions().

        Returns:
            Populated DetectionResult.
        """
        if mode == MODE_FRESH_INSTALL:
            result.is_fresh_install = True
        elif mode == MODE_REINSTALL:
            result.is_reinstall = True
            self._log_info(f"Reinstall detected: v{result.from_version}")
        elif mode == MODE_DOWNGRADE:
            result.is_downgrade = True
            self._log_info(
                f"Downgrade detected: v{result.from_version} -> v{result.to_version}"
            )
        elif mode in (MODE_PATCH_UPGRADE, MODE_MINOR_UPGRADE, MODE_MAJOR_UPGRADE):
            self._populate_upgrade_result(result, mode)

        return result

    def _populate_upgrade_result(self, result: DetectionResult, mode: str) -> None:
        """Populate upgrade detection result."""
        result.is_upgrade = True
        result.upgrade_type = self._get_upgrade_type(mode)
        self._log_info(
            f"Upgrade detected: v{result.from_version} -> v{result.to_version} "
            f"({result.upgrade_type})"
        )

    def _get_upgrade_type(self, mode: str) -> str:
        """Map version comparison mode to upgrade type string."""
        return {
            MODE_MAJOR_UPGRADE: "major",
            MODE_MINOR_UPGRADE: "minor",
            MODE_PATCH_UPGRADE: "patch"
        }.get(mode, "patch")

    def _log_info(self, message: str) -> None:
        """Log an info message if logger available."""
        if self._logger:
            self._logger.log_info(message)

    def execute(self, project_root: Path, source_root: Path) -> UpgradeResult:
        """
        Execute upgrade workflow (SVC-002).

        Orchestrates the complete upgrade lifecycle:
        detect -> backup -> migrate -> validate -> update version

        Args:
            project_root: Path to target project.
            source_root: Path to source package.

        Returns:
            UpgradeResult with status and details.
        """
        start_time = time.time()
        result = UpgradeResult(success=True)

        # Check for concurrent upgrade lock
        if self._is_upgrade_locked(project_root):
            result.success = False
            result.error_message = "Upgrade already in progress (lock file exists)"
            return result

        # Phase 1: Detect upgrade scenario
        detection = self.detect(project_root, source_root)
        result.from_version = detection.from_version
        result.to_version = detection.to_version

        # Early exit for non-migration scenarios
        if detection.is_fresh_install or detection.is_reinstall or detection.is_downgrade:
            return self._finalize_simple_result(result, start_time)

        # Phase 2: Create backup (AC#2)
        backup_result = self._execute_backup_phase(result, project_root, detection)
        if not backup_result:
            result.duration_seconds = time.time() - start_time
            return result

        # Phase 3: Discover and run migrations (AC#4)
        migration_result = self._execute_migration_phase(
            result, project_root, source_root, detection
        )
        if not migration_result:
            result.duration_seconds = time.time() - start_time
            return result

        # Phase 4: Validate migration (AC#5)
        validation_result = self._execute_validation_phase(result, project_root)
        if not validation_result:
            result.duration_seconds = time.time() - start_time
            return result

        # Phase 5: Update metadata and finalize (AC#6, AC#8)
        return self._finalize_successful_upgrade(result, project_root, detection, start_time)

    def _is_upgrade_locked(self, project_root: Path) -> bool:
        """Check if an upgrade is already in progress."""
        lock_file = project_root / ".devforgeai" / ".upgrade.lock"
        return lock_file.exists()

    def _finalize_simple_result(
        self, result: UpgradeResult, start_time: float
    ) -> UpgradeResult:
        """Finalize result for non-migration scenarios (fresh/reinstall/downgrade)."""
        result.success = True
        result.duration_seconds = time.time() - start_time
        result.summary = UpgradeSummary(duration_seconds=result.duration_seconds)
        return result

    def _execute_backup_phase(
        self,
        result: UpgradeResult,
        project_root: Path,
        detection: DetectionResult
    ) -> bool:
        """
        Execute backup creation phase.

        Returns:
            True if backup succeeded, False if failed.
        """
        try:
            if self._backup_service:
                result.backup_path = self._backup_service.create_backup(
                    target_dir=project_root,
                    from_version=detection.from_version
                )
            else:
                result.backup_path = self._create_backup(
                    project_root=project_root,
                    from_version=detection.from_version
                )
            return True
        except Exception as e:
            result.success = False
            result.error_message = f"Backup creation failed: {e}"
            return False

    def _execute_migration_phase(
        self,
        result: UpgradeResult,
        project_root: Path,
        source_root: Path,
        detection: DetectionResult
    ) -> bool:
        """
        Execute migration discovery and execution phase.

        Returns:
            True if migrations succeeded, False if failed (rollback triggered).
        """
        migrations = self._discover_migrations(source_root, detection)
        run_result = self._run_migrations(migrations, project_root)

        if run_result:
            result.migrations_applied = run_result.applied_migrations

            if not run_result.success:
                self._handle_migration_failure(result, run_result, project_root)
                return False

        return True

    def _discover_migrations(
        self, source_root: Path, detection: DetectionResult
    ) -> List[Any]:
        """Discover applicable migrations for the upgrade path."""
        if self._migration_discovery:
            return self._migration_discovery.discover(
                from_version=detection.from_version,
                to_version=detection.to_version
            )

        migrations_dir = source_root / "migrations"
        if migrations_dir.exists():
            from installer.migration_discovery import MigrationDiscovery
            discovery = MigrationDiscovery(migrations_dir=migrations_dir, logger=self._logger)
            return discovery.discover(
                from_version=detection.from_version,
                to_version=detection.to_version
            )

        return []

    def _run_migrations(
        self, migrations: List[Any], project_root: Path
    ) -> Optional[Any]:
        """Run discovered migrations."""
        if self._migration_runner:
            return self._migration_runner.run(
                migrations=migrations,
                project_root=project_root
            )

        if migrations:
            from installer.migration_runner import MigrationRunner
            runner = MigrationRunner(logger=self._logger)
            return runner.run(migrations=migrations, project_root=project_root)

        return None

    def _handle_migration_failure(
        self,
        result: UpgradeResult,
        run_result: Any,
        project_root: Path
    ) -> None:
        """Handle migration failure with rollback (AC#7)."""
        result.success = False
        result.rolled_back = True
        result.status = "rolled_back"

        if run_result.failed_migration:
            fm = run_result.failed_migration
            result.error_message = (
                f"Migration failed: {fm.from_version} -> {fm.to_version}: "
                f"{fm.error_message}"
            )

        self._perform_rollback(result.backup_path, project_root)

    def _execute_validation_phase(
        self, result: UpgradeResult, project_root: Path
    ) -> bool:
        """
        Execute post-migration validation phase.

        Returns:
            True if validation passed, False if failed (rollback triggered).
        """
        validator = self._migration_validator
        if validator is None:
            from installer.migration_validator import MigrationValidator
            validator = MigrationValidator(logger=self._logger)

        validation = validator.validate(
            project_root=project_root,
            expected_files=[".devforgeai/.version.json"]
        )

        if not validation.overall_passed:
            self._handle_validation_failure(result, project_root)
            return False

        return True

    def _handle_validation_failure(
        self, result: UpgradeResult, project_root: Path
    ) -> None:
        """Handle validation failure with rollback (AC#7)."""
        result.success = False
        result.rolled_back = True
        result.status = "rolled_back"
        result.error_message = "Post-migration validation failed"
        self._perform_rollback(result.backup_path, project_root)

    def _perform_rollback(self, backup_path: Path, project_root: Path) -> None:
        """Perform rollback using backup service or internal method."""
        if self._backup_service:
            self._backup_service.restore(backup_path, project_root)
        else:
            self._rollback(backup_path=backup_path, project_root=project_root)

    def _finalize_successful_upgrade(
        self,
        result: UpgradeResult,
        project_root: Path,
        detection: DetectionResult,
        start_time: float
    ) -> UpgradeResult:
        """Finalize a successful upgrade with metadata update and summary."""
        self._update_version_metadata(
            project_root=project_root,
            from_version=detection.from_version,
            to_version=detection.to_version,
            migrations_applied=result.migrations_applied
        )

        result.duration_seconds = time.time() - start_time
        result.summary = UpgradeSummary(
            migrations_executed=self._get_migration_paths(result.migrations_applied),
            duration_seconds=result.duration_seconds
        )

        result.log_file = self._save_upgrade_log(project_root=project_root, result=result)

        return result

    def _get_migration_paths(self, migrations: List[Any]) -> List[str]:
        """Extract path strings from migration objects."""
        if not migrations:
            return []
        return [str(m.path) for m in migrations]

    def _create_backup(self, project_root: Path, from_version: str) -> Path:
        """
        Create backup of current installation (AC#2).

        Copies all DevForgeAI components (.devforgeai, .claude, CLAUDE.md)
        to a timestamped backup directory.

        Args:
            project_root: Path to project root.
            from_version: Current version being backed up.

        Returns:
            Path to backup directory.
        """
        backup_path = self._create_backup_directory(project_root, from_version)

        # Backup DevForgeAI components
        self._backup_devforgeai(project_root, backup_path)
        self._backup_claude_directory(project_root, backup_path)
        self._backup_claude_md(project_root, backup_path)

        self._log_info(f"Backup created: {backup_path}")
        return backup_path

    def _create_backup_directory(self, project_root: Path, version: str) -> Path:
        """Create and return the backup directory path."""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        backup_name = f"v{version}-{timestamp}"
        backup_path = project_root / ".devforgeai" / "backups" / backup_name
        backup_path.mkdir(parents=True, exist_ok=True)
        return backup_path

    def _backup_devforgeai(self, project_root: Path, backup_path: Path) -> None:
        """Backup .devforgeai directory (excluding backups and logs)."""
        devforgeai_src = project_root / ".devforgeai"
        if devforgeai_src.exists():
            devforgeai_dest = backup_path / ".devforgeai"
            shutil.copytree(
                devforgeai_src,
                devforgeai_dest,
                ignore=shutil.ignore_patterns('backups', 'logs'),
                dirs_exist_ok=True
            )

    def _backup_claude_directory(self, project_root: Path, backup_path: Path) -> None:
        """Backup .claude directory."""
        claude_src = project_root / ".claude"
        if claude_src.exists():
            claude_dest = backup_path / ".claude"
            shutil.copytree(claude_src, claude_dest, dirs_exist_ok=True)

    def _backup_claude_md(self, project_root: Path, backup_path: Path) -> None:
        """Backup CLAUDE.md file."""
        claude_md = project_root / "CLAUDE.md"
        if claude_md.exists():
            shutil.copy2(claude_md, backup_path / "CLAUDE.md")

    def _rollback(self, backup_path: Path, project_root: Path) -> bool:
        """
        Rollback to backup state (AC#7).

        Restores all backed up components to their original state.

        Args:
            backup_path: Path to backup directory.
            project_root: Path to project root.

        Returns:
            True if rollback successful.
        """
        if not backup_path or not backup_path.exists():
            return False

        # Restore each component
        self._restore_devforgeai(backup_path, project_root)
        self._restore_claude_directory(backup_path, project_root)
        self._restore_claude_md(backup_path, project_root)

        self._log_info(f"Rollback completed from: {backup_path}")
        return True

    def _restore_devforgeai(self, backup_path: Path, project_root: Path) -> None:
        """Restore .devforgeai directory from backup."""
        backup_devforgeai = backup_path / ".devforgeai"
        if not backup_devforgeai.exists():
            return

        target_devforgeai = project_root / ".devforgeai"

        # Restore version file first
        backup_version = backup_devforgeai / ".version.json"
        if backup_version.exists():
            shutil.copy2(backup_version, target_devforgeai / ".version.json")

        # Restore other files (excluding system directories and version file)
        skip_items = {'backups', 'logs', '.version.json'}
        for item in backup_devforgeai.iterdir():
            if item.name in skip_items:
                continue
            target = target_devforgeai / item.name
            self._restore_item(item, target)

    def _restore_claude_directory(self, backup_path: Path, project_root: Path) -> None:
        """Restore .claude directory from backup."""
        backup_claude = backup_path / ".claude"
        if backup_claude.exists():
            target_claude = project_root / ".claude"
            self._restore_item(backup_claude, target_claude)

    def _restore_claude_md(self, backup_path: Path, project_root: Path) -> None:
        """Restore CLAUDE.md file from backup."""
        backup_claude_md = backup_path / "CLAUDE.md"
        if backup_claude_md.exists():
            shutil.copy2(backup_claude_md, project_root / "CLAUDE.md")

    def _restore_item(self, source: Path, target: Path) -> None:
        """Restore a single file or directory."""
        if target.exists():
            if target.is_dir():
                shutil.rmtree(target)
            else:
                target.unlink()

        if source.is_dir():
            shutil.copytree(source, target)
        else:
            shutil.copy2(source, target)

    def _update_version_metadata(
        self,
        project_root: Path,
        from_version: str,
        to_version: str,
        migrations_applied: List[Any]
    ) -> None:
        """
        Update version metadata after successful upgrade (AC#6).

        Updates the .version.json file with new version information
        and migration history.

        Args:
            project_root: Path to project root.
            from_version: Previous version.
            to_version: New version.
            migrations_applied: List of applied migrations.
        """
        version_file = project_root / ".devforgeai" / ".version.json"
        data = self._read_version_data(version_file)

        # Update version metadata
        data["version"] = to_version
        data["upgraded_from"] = from_version
        data["upgrade_timestamp"] = datetime.now(timezone.utc).isoformat()
        data["mode"] = "upgrade"
        data["migrations_applied"] = self._extract_migration_names(migrations_applied)

        # Write updated version file
        version_file.parent.mkdir(parents=True, exist_ok=True)
        version_file.write_text(json.dumps(data, indent=2))

        self._log_info(f"Version metadata updated: v{from_version} -> v{to_version}")

    def _read_version_data(self, version_file: Path) -> dict:
        """Read existing version data or return empty dict."""
        if not version_file.exists():
            return {}
        try:
            return json.loads(version_file.read_text())
        except json.JSONDecodeError:
            return {}

    def _extract_migration_names(self, migrations: List[Any]) -> List[str]:
        """Extract migration script names from migration objects."""
        if not migrations:
            return []
        return [
            str(m.path.name) if hasattr(m, 'path') else str(m)
            for m in migrations
        ]

    def _save_upgrade_log(self, project_root: Path, result: UpgradeResult) -> Path:
        """
        Save upgrade summary to log file (AC#8).

        Creates a timestamped JSON log file with complete upgrade details
        for audit and troubleshooting purposes.

        Args:
            project_root: Path to project root.
            result: UpgradeResult to log.

        Returns:
            Path to log file.
        """
        log_file = self._create_log_file_path(project_root)
        log_content = self._build_log_content(result)

        log_file.write_text(json.dumps(log_content, indent=2))
        self._log_info(f"Upgrade log saved: {log_file}")

        return log_file

    def _create_log_file_path(self, project_root: Path) -> Path:
        """Create the log file path and ensure directory exists."""
        logs_dir = project_root / ".devforgeai" / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return logs_dir / f"upgrade-{timestamp}.log"

    def _build_log_content(self, result: UpgradeResult) -> dict:
        """Build the log content dictionary from upgrade result."""
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": result.status,
            "success": result.success,
            "from_version": result.from_version,
            "to_version": result.to_version,
            "duration_seconds": result.duration_seconds,
            "backup_path": str(result.backup_path) if result.backup_path else None,
            "rolled_back": result.rolled_back,
            "error_message": result.error_message,
            "migrations_applied": self._extract_migration_names(result.migrations_applied or [])
        }

"""STORY-078: Upgrade Orchestrator - orchestrates detection, backup, migration, validation, rollback."""

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
    """Summary of upgrade operation (AC#8)."""
    files_added: int = 0
    files_updated: int = 0
    files_removed: int = 0
    migrations_executed: List[str] = field(default_factory=list)
    duration_seconds: float = 0.0


@dataclass
class DetectionResult:
    """Result of upgrade detection (AC#1)."""
    is_upgrade: bool = False
    is_fresh_install: bool = False
    is_reinstall: bool = False
    is_downgrade: bool = False
    from_version: Optional[str] = None
    to_version: Optional[str] = None
    upgrade_type: Optional[str] = None


@dataclass
class UpgradeResult:
    """Result of upgrade execution."""
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
    """Orchestrates upgrade workflow: detect -> backup -> migrate -> validate -> update."""

    def __init__(self, logger: Any = None, backup_service: Any = None,
                 migration_discovery: Any = None, migration_runner: Any = None,
                 migration_validator: Any = None) -> None:
        """Initialize with optional dependencies for testing flexibility."""
        self._logger = logger
        self._backup_service = backup_service
        self._migration_discovery = migration_discovery
        self._migration_runner = migration_runner
        self._migration_validator = migration_validator

    @property
    def logger(self) -> Any:
        return self._logger

    @property
    def backup_service(self) -> Any:
        return self._backup_service

    @property
    def migration_discovery(self) -> Any:
        return self._migration_discovery

    @property
    def migration_runner(self) -> Any:
        return self._migration_runner

    @property
    def migration_validator(self) -> Any:
        return self._migration_validator

    def detect(self, project_root: Path, source_root: Path) -> DetectionResult:
        """Detect upgrade scenario (AC#1, SVC-001)."""
        result = DetectionResult()
        installed = self._get_installed_version_safe(project_root)
        source = get_source_version(source_root / "devforgeai")
        result.to_version = source.get("version")

        if installed is None:
            return self._detect_fresh_install(result)

        result.from_version = installed.get("version")
        return self._classify_installation_mode(result, compare_versions(result.from_version, result.to_version))

    def _get_installed_version_safe(self, project_root: Path) -> Optional[dict]:
        devforgeai_path = project_root / ".devforgeai"
        if not devforgeai_path.exists(): return None
        try: return get_installed_version(devforgeai_path)
        except json.JSONDecodeError:
            self._log_warning("Corrupted version file detected, treating as fresh install")
            return None

    def _detect_fresh_install(self, result: DetectionResult) -> DetectionResult:
        result.is_fresh_install, result.from_version = True, None
        self._log_info(f"Fresh install detected: v{result.to_version}")
        return result

    def _classify_installation_mode(self, result: DetectionResult, mode: str) -> DetectionResult:
        if mode == MODE_FRESH_INSTALL:
            result.is_fresh_install = True
        elif mode == MODE_REINSTALL:
            result.is_reinstall = True
            self._log_info(f"Reinstall detected: v{result.from_version}")
        elif mode == MODE_DOWNGRADE:
            result.is_downgrade = True
            self._log_info(f"Downgrade detected: v{result.from_version} -> v{result.to_version}")
        elif mode in (MODE_PATCH_UPGRADE, MODE_MINOR_UPGRADE, MODE_MAJOR_UPGRADE):
            result.is_upgrade = True
            result.upgrade_type = {MODE_MAJOR_UPGRADE: "major", MODE_MINOR_UPGRADE: "minor", MODE_PATCH_UPGRADE: "patch"}.get(mode, "patch")
            self._log_info(f"Upgrade detected: v{result.from_version} -> v{result.to_version} ({result.upgrade_type})")
        return result

    def _log_info(self, msg: str) -> None:
        if self._logger: self._logger.log_info(msg)

    def _log_warning(self, msg: str) -> None:
        if self._logger: self._logger.log_warning(msg)

    def execute(self, project_root: Path, source_root: Path) -> UpgradeResult:
        """Execute upgrade workflow (SVC-002)."""
        start_time = time.time()
        result = UpgradeResult(success=True)

        if self._is_upgrade_locked(project_root):
            result.success, result.error_message = False, "Upgrade already in progress (lock file exists)"
            return result

        detection = self.detect(project_root, source_root)
        result.from_version, result.to_version = detection.from_version, detection.to_version

        if detection.is_fresh_install or detection.is_reinstall or detection.is_downgrade:
            return self._finalize_simple_result(result, start_time)

        for phase in [
            lambda: self._execute_backup_phase(result, project_root, detection),
            lambda: self._execute_migration_phase(result, project_root, source_root, detection),
            lambda: self._execute_validation_phase(result, project_root)
        ]:
            if not phase():
                result.duration_seconds = time.time() - start_time
                return result

        return self._finalize_successful_upgrade(result, project_root, detection, start_time)

    def _is_upgrade_locked(self, project_root: Path) -> bool:
        return (project_root / ".devforgeai" / ".upgrade.lock").exists()

    def _finalize_simple_result(self, result: UpgradeResult, start_time: float) -> UpgradeResult:
        result.success, result.duration_seconds = True, time.time() - start_time
        result.summary = UpgradeSummary(duration_seconds=result.duration_seconds)
        return result

    def _execute_backup_phase(self, result: UpgradeResult, project_root: Path, detection: DetectionResult) -> bool:
        try:
            result.backup_path = (self._backup_service.create_backup(target_dir=project_root, from_version=detection.from_version) if self._backup_service else self._create_backup(project_root=project_root, from_version=detection.from_version))
            return True
        except Exception as e: result.success, result.error_message = False, f"Backup creation failed: {e}"; return False

    def _execute_migration_phase(self, result: UpgradeResult, project_root: Path, source_root: Path, detection: DetectionResult) -> bool:
        migrations = self._discover_migrations(source_root, detection)
        run_result = self._run_migrations(migrations, project_root)
        if run_result:
            result.migrations_applied = run_result.applied_migrations
            if not run_result.success:
                self._handle_migration_failure(result, run_result, project_root)
                return False
        return True

    def _discover_migrations(self, source_root: Path, detection: DetectionResult) -> List[Any]:
        if self._migration_discovery:
            return self._migration_discovery.discover(from_version=detection.from_version, to_version=detection.to_version)
        migrations_dir = source_root / "migrations"
        if not migrations_dir.exists(): return []
        from installer.migration_discovery import MigrationDiscovery
        return MigrationDiscovery(migrations_dir=migrations_dir, logger=self._logger).discover(from_version=detection.from_version, to_version=detection.to_version)

    def _run_migrations(self, migrations: List[Any], project_root: Path) -> Optional[Any]:
        if self._migration_runner: return self._migration_runner.run(migrations=migrations, project_root=project_root)
        if not migrations: return None
        from installer.migration_runner import MigrationRunner
        return MigrationRunner(logger=self._logger).run(migrations=migrations, project_root=project_root)

    def _handle_migration_failure(self, result: UpgradeResult, run_result: Any, project_root: Path) -> None:
        result.success, result.rolled_back, result.status = False, True, "rolled_back"
        if run_result.failed_migration:
            fm = run_result.failed_migration
            result.error_message = f"Migration failed: {fm.from_version} -> {fm.to_version}: {fm.error_message}"
        self._perform_rollback(result.backup_path, project_root)

    def _execute_validation_phase(self, result: UpgradeResult, project_root: Path) -> bool:
        validator = self._migration_validator or __import__('installer.migration_validator', fromlist=['MigrationValidator']).MigrationValidator(logger=self._logger)
        if not validator.validate(project_root=project_root, expected_files=[".devforgeai/.version.json"]).overall_passed:
            result.success, result.rolled_back, result.status = False, True, "rolled_back"
            result.error_message = "Post-migration validation failed"
            self._perform_rollback(result.backup_path, project_root)
            return False
        return True

    def _perform_rollback(self, backup_path: Path, project_root: Path) -> None:
        (self._backup_service.restore(backup_path, project_root) if self._backup_service
         else self._rollback(backup_path=backup_path, project_root=project_root))

    def _finalize_successful_upgrade(self, result: UpgradeResult, project_root: Path, detection: DetectionResult, start_time: float) -> UpgradeResult:
        self._update_version_metadata(project_root, detection.from_version, detection.to_version, result.migrations_applied)
        result.duration_seconds = time.time() - start_time
        result.summary = UpgradeSummary(
            migrations_executed=[str(m.path) for m in result.migrations_applied] if result.migrations_applied else [],
            duration_seconds=result.duration_seconds)
        result.log_file = self._save_upgrade_log(project_root=project_root, result=result)
        return result

    def _create_backup(self, project_root: Path, from_version: str) -> Path:
        """Create backup of current installation (AC#2)."""
        backup_path = project_root / ".devforgeai" / "backups" / f"v{from_version}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        backup_path.mkdir(parents=True, exist_ok=True)
        devforgeai_src = project_root / ".devforgeai"
        if devforgeai_src.exists():
            shutil.copytree(devforgeai_src, backup_path / ".devforgeai", ignore=shutil.ignore_patterns('backups', 'logs'), dirs_exist_ok=True)
        claude_src = project_root / ".claude"
        if claude_src.exists():
            shutil.copytree(claude_src, backup_path / ".claude", dirs_exist_ok=True)
        if (project_root / "CLAUDE.md").exists():
            shutil.copy2(project_root / "CLAUDE.md", backup_path / "CLAUDE.md")
        self._log_info(f"Backup created: {backup_path}")
        return backup_path

    def _rollback(self, backup_path: Path, project_root: Path) -> bool:
        """Rollback to backup state (AC#7)."""
        if not backup_path or not backup_path.exists():
            return False
        backup_devforgeai = backup_path / ".devforgeai"
        if backup_devforgeai.exists():
            target_devforgeai = project_root / ".devforgeai"
            if (backup_devforgeai / ".version.json").exists():
                shutil.copy2(backup_devforgeai / ".version.json", target_devforgeai / ".version.json")
            for item in backup_devforgeai.iterdir():
                if item.name not in {'backups', 'logs', '.version.json'}:
                    self._restore_item(item, target_devforgeai / item.name)
        if (backup_path / ".claude").exists():
            self._restore_item(backup_path / ".claude", project_root / ".claude")
        if (backup_path / "CLAUDE.md").exists():
            shutil.copy2(backup_path / "CLAUDE.md", project_root / "CLAUDE.md")
        self._log_info(f"Rollback completed from: {backup_path}")
        return True

    def _restore_item(self, source: Path, target: Path) -> None:
        if target.exists():
            shutil.rmtree(target) if target.is_dir() else target.unlink()
        (shutil.copytree if source.is_dir() else shutil.copy2)(source, target)

    def _update_version_metadata(self, project_root: Path, from_version: str, to_version: str, migrations_applied: List[Any]) -> None:
        """Update version metadata after successful upgrade (AC#6)."""
        version_file = project_root / ".devforgeai" / ".version.json"
        try: data = json.loads(version_file.read_text()) if version_file.exists() else {}
        except json.JSONDecodeError: data = {}
        data.update({"version": to_version, "upgraded_from": from_version,
            "upgrade_timestamp": datetime.now(timezone.utc).isoformat(), "mode": "upgrade",
            "migrations_applied": [str(m.path.name) if hasattr(m, 'path') else str(m) for m in migrations_applied] if migrations_applied else []})
        version_file.parent.mkdir(parents=True, exist_ok=True)
        version_file.write_text(json.dumps(data, indent=2))
        self._log_info(f"Version metadata updated: v{from_version} -> v{to_version}")

    def _save_upgrade_log(self, project_root: Path, result: UpgradeResult) -> Path:
        """Save upgrade summary to log file (AC#8)."""
        logs_dir = project_root / ".devforgeai" / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)
        log_file = logs_dir / f"upgrade-{datetime.now().strftime('%Y%m%d%H%M%S')}.log"
        migrations = result.migrations_applied or []
        log_file.write_text(json.dumps({"timestamp": datetime.now(timezone.utc).isoformat(), "status": result.status,
            "success": result.success, "from_version": result.from_version, "to_version": result.to_version,
            "duration_seconds": result.duration_seconds, "backup_path": str(result.backup_path) if result.backup_path else None,
            "rolled_back": result.rolled_back, "error_message": result.error_message,
            "migrations_applied": [str(m.path.name) if hasattr(m, 'path') else str(m) for m in migrations]}, indent=2))
        self._log_info(f"Upgrade log saved: {log_file}")
        return log_file

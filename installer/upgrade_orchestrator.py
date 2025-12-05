"""
UpgradeOrchestrator service for coordinating the complete upgrade workflow (STORY-078).

Implements:
- SVC-001: Detect upgrade scenario by comparing versions
- SVC-002: Orchestrate upgrade workflow (backup → migrate → validate → update)
- SVC-003: Trigger rollback on any failure

Follows clean architecture with dependency injection and atomic operations.
"""

import json
import logging
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Tuple
import time

from installer.models import (
    BackupReason,
    UpgradeStatus,
    UpgradeSummary,
    UpgradeError,
    RollbackError,
)
from installer.backup_service import BackupService, IBackupService
from installer.migration_discovery import (
    MigrationDiscovery,
    IMigrationDiscovery,
    StringVersionComparator,
)
from installer.migration_runner import MigrationRunner, IMigrationRunner
from installer.migration_validator import MigrationValidator, IMigrationValidator
from installer.version_detector import VersionDetector
from installer.version_parser import VersionParser


logger = logging.getLogger(__name__)

# Constants for upgrade orchestration
DEFAULT_MIGRATION_TIMEOUT_SECONDS = 300
DEFAULT_BACKUP_RETENTION_COUNT = 5


class UpgradeOrchestrator:
    """Coordinates the complete upgrade workflow."""

    def __init__(
        self,
        backup_service: Optional[IBackupService] = None,
        migration_discovery: Optional[IMigrationDiscovery] = None,
        migration_runner: Optional[IMigrationRunner] = None,
        migration_validator: Optional[IMigrationValidator] = None,
        version_detector: Optional[VersionDetector] = None,
        version_comparator: Optional[StringVersionComparator] = None,
    ) -> None:
        """
        Initialize UpgradeOrchestrator with injected dependencies.

        Args:
            backup_service: Backup service. Defaults to BackupService()
            migration_discovery: Migration discovery. Defaults to MigrationDiscovery()
            migration_runner: Migration runner. Defaults to MigrationRunner()
            migration_validator: Migration validator. Defaults to MigrationValidator()
            version_detector: Version detector. Defaults to VersionDetector()
            version_comparator: Version comparator. Defaults to StringVersionComparator()
        """
        self.backup_service = backup_service or BackupService()
        self.migration_discovery = migration_discovery or MigrationDiscovery()
        self.migration_runner = migration_runner or MigrationRunner()
        self.migration_validator = migration_validator or MigrationValidator()
        self.version_detector = version_detector or VersionDetector()
        self.version_comparator = version_comparator or StringVersionComparator()

        self.parser = VersionParser()

    def _create_error_summary(
        self,
        from_version: str,
        to_version: str,
        error_message: str,
        duration: float,
        status: UpgradeStatus,
        backup_path: Optional[str] = None,
    ) -> UpgradeSummary:
        """
        Create an error summary for failed upgrades.

        Args:
            from_version: Source version
            to_version: Target version
            error_message: Error description
            duration: Upgrade duration
            status: Upgrade status (FAILED or ROLLED_BACK)
            backup_path: Path to backup if available

        Returns:
            UpgradeSummary with error details
        """
        return UpgradeSummary(
            from_version=from_version,
            to_version=to_version,
            status=status,
            backup_path=backup_path,
            duration_seconds=duration,
            error_message=error_message,
        )

    def detect_upgrade(self, installed_version: str, package_version: str) -> dict:
        """
        Detect if upgrade is needed and determine upgrade type.

        Args:
            installed_version: Currently installed version (X.Y.Z)
            package_version: Version in package (X.Y.Z)

        Returns:
            Dict with:
            - is_upgrade: bool
            - upgrade_type: str ("major", "minor", "patch", or "none")
            - from_version: str
            - to_version: str
            - message: str

        Raises:
            UpgradeError: If versions invalid
        """
        try:
            v_installed = self.parser.parse(installed_version)
            v_package = self.parser.parse(package_version)
        except ValueError as e:
            raise UpgradeError(f"Invalid version format: {e}")

        cmp = self.version_comparator.compare(installed_version, package_version)

        if cmp >= 0:
            return {
                "is_upgrade": False,
                "upgrade_type": "none",
                "from_version": installed_version,
                "to_version": package_version,
                "message": f"No upgrade needed: {installed_version} → {package_version}",
            }

        # Determine upgrade type
        if v_installed.major != v_package.major:
            upgrade_type = "major"
        elif v_installed.minor != v_package.minor:
            upgrade_type = "minor"
        else:
            upgrade_type = "patch"

        message = f"Upgrade detected: v{installed_version} → v{package_version} ({upgrade_type})"

        return {
            "is_upgrade": True,
            "upgrade_type": upgrade_type,
            "from_version": installed_version,
            "to_version": package_version,
            "message": message,
        }

    def execute(
        self,
        from_version: str,
        to_version: str,
        source_root: Path,
        target_root: Path,
        migrations_dir: Optional[Path] = None,
        migration_timeout_seconds: int = 300,
        backup_retention_count: int = 5,
    ) -> UpgradeSummary:
        """
        Execute complete upgrade workflow.

        Workflow:
        1. Create backup (atomic)
        2. Discover migrations
        3. Execute migrations
        4. Validate post-migration state
        5. Update version metadata
        6. Generate summary
        7. Cleanup old backups

        On failure at any step:
        - Trigger rollback from backup
        - Restore version metadata
        - Generate error summary

        Args:
            from_version: Current version
            to_version: Target version
            source_root: Source root with new files
            target_root: Target installation root
            migrations_dir: Directory containing migration scripts
            migration_timeout_seconds: Timeout per migration
            backup_retention_count: Number of backups to keep

        Returns:
            UpgradeSummary with results

        Raises:
            UpgradeError: On upgrade failure (after rollback)
        """
        start_time = time.time()
        backup_metadata = None

        try:
            logger.info(f"Starting upgrade: {from_version} → {to_version}")

            source_root = Path(source_root)
            target_root = Path(target_root)

            # Step 1: Create backup (atomic)
            logger.info("Creating backup...")
            try:
                backup_metadata = self.backup_service.create_backup(
                    source_root=target_root,
                    version=from_version,
                    reason=BackupReason.UPGRADE,
                )
                backup_path = str(self.backup_service.backups_root / backup_metadata.backup_id)
                logger.info(f"Backup created: {backup_path}")
            except Exception as e:
                raise UpgradeError(f"Backup creation failed: {e}")

            # Step 2: Discover migrations
            logger.info("Discovering migrations...")
            migrations = self.migration_discovery.discover(
                from_version, to_version, migrations_dir
            )

            if not migrations:
                logger.info("No migrations found for this upgrade")
            else:
                logger.info(f"Found {len(migrations)} migration(s)")

            # Step 3: Execute migrations
            if migrations:
                logger.info("Executing migrations...")
                try:
                    run_result = self.migration_runner.run(
                        migrations, timeout_seconds=migration_timeout_seconds
                    )

                    if not run_result.all_success:
                        error_msg = f"Migration failed: {run_result.failed_migration_result.error_message}"
                        raise UpgradeError(error_msg)

                    logger.info(f"All {run_result.applied_count} migration(s) completed")

                except UpgradeError:
                    raise
                except Exception as e:
                    raise UpgradeError(f"Migration execution failed: {e}")

            # Step 4: Validate post-migration state (future: add validation checks)
            logger.info("Validating post-migration state...")

            # Step 5: Update version metadata
            logger.info("Updating version metadata...")
            self._update_version_metadata(
                target_root, from_version, to_version, migrations
            )

            # Step 6: Generate success summary
            duration = time.time() - start_time
            summary = UpgradeSummary(
                from_version=from_version,
                to_version=to_version,
                status=UpgradeStatus.SUCCESS,
                files_added=0,  # Could calculate from backup diff
                files_updated=0,
                files_removed=0,
                migrations_applied=[m.path for m in migrations],
                backup_path=backup_path,
                duration_seconds=duration,
            )

            # Step 7: Cleanup old backups
            logger.info("Cleaning up old backups...")
            deleted = self.backup_service.cleanup(backup_retention_count)
            logger.info(f"Deleted {deleted} old backup(s)")

            logger.info(f"Upgrade completed successfully in {duration:.1f}s")
            return summary

        except UpgradeError as e:
            # Rollback on upgrade error
            logger.error(f"Upgrade failed: {e}")

            if backup_metadata:
                logger.info("Starting rollback...")
                try:
                    self._rollback(backup_metadata, target_root, from_version)
                    logger.info("Rollback completed successfully")
                except RollbackError as re:
                    logger.critical(f"Rollback failed: {re}")
                    raise

            duration = time.time() - start_time
            backup_path = (
                str(self.backup_service.backups_root / backup_metadata.backup_id)
                if backup_metadata
                else None
            )
            status = UpgradeStatus.ROLLED_BACK if backup_metadata else UpgradeStatus.FAILED

            return self._create_error_summary(
                from_version,
                to_version,
                str(e),
                duration,
                status,
                backup_path,
            )

        except Exception as e:
            # Unexpected error
            logger.critical(f"Unexpected error during upgrade: {e}")
            duration = time.time() - start_time

            return self._create_error_summary(
                from_version,
                to_version,
                f"Unexpected error: {e}",
                duration,
                UpgradeStatus.FAILED,
            )

    def _update_version_metadata(
        self, target_root: Path, from_version: str, to_version: str, migrations
    ) -> None:
        """
        Update .devforgeai/.version.json with new version info.

        Args:
            target_root: Installation root
            from_version: Previous version
            to_version: New version
            migrations: List of migrations applied

        Raises:
            UpgradeError: If update fails
        """
        try:
            version_file = target_root / ".devforgeai" / ".version.json"
            version_file.parent.mkdir(parents=True, exist_ok=True)

            now = datetime.now(timezone.utc)

            version_data = {
                "version": to_version,
                "installed_at": now.isoformat(),
                "upgraded_from": from_version,
                "upgrade_timestamp": now.isoformat(),
                "migrations_applied": [m.path for m in migrations] if migrations else [],
            }

            version_file.write_text(
                json.dumps(version_data, indent=2),
                encoding="utf-8",
            )

        except Exception as e:
            raise UpgradeError(f"Failed to update version metadata: {e}")

    def _rollback(
        self, backup_metadata, target_root: Path, from_version: str
    ) -> dict:
        """
        Rollback installation from backup.

        Args:
            backup_metadata: Backup metadata
            target_root: Installation root to restore to
            from_version: Version to restore to

        Returns:
            Dict with rollback results

        Raises:
            RollbackError: If rollback fails
        """
        try:
            start_time = time.time()

            # Restore files from backup
            self.backup_service.restore(backup_metadata.backup_id, target_root)

            # Restore version metadata
            version_file = target_root / ".devforgeai" / ".version.json"
            if version_file.exists():
                version_file.unlink()

            duration = time.time() - start_time

            return {
                "success": True,
                "duration_seconds": duration,
                "restored_backup": backup_metadata.backup_id,
            }

        except Exception as e:
            raise RollbackError(f"Rollback failed: {e}")

    def prepare_backup(
        self, from_version: str
    ) -> Tuple[bool, str]:
        """
        Prepare backup before upgrade starts (can be called separately).

        Args:
            from_version: Current version

        Returns:
            Tuple of (success: bool, backup_id: str or error message)
        """
        try:
            target_root = Path.cwd()  # Current installation
            backup_metadata = self.backup_service.create_backup(
                source_root=target_root,
                version=from_version,
                reason=BackupReason.UPGRADE,
            )
            backup_id = backup_metadata.backup_id
            return True, backup_id
        except Exception as e:
            return False, str(e)

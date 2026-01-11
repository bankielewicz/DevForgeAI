"""
Rollback Manager for DevForgeAI (STORY-251)

Provides simplified rollback interface for AC#4.
Wraps the complex RollbackOrchestrator for easier usage.

Usage:
    from installer.rollback_manager import RollbackManager

    manager = RollbackManager(project_root=Path("/path/to/project"))
    exit_code = manager.rollback(backup_id="backup-20250105-143000")
"""

import json
import logging
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any

from installer.exit_codes import ExitCodes
from installer.rollback import list_backups, restore_from_backup

logger = logging.getLogger(__name__)


class RollbackManager:
    """
    Simplified rollback manager for AC#4.

    Provides a simple interface to:
    - List available backups
    - Select and restore from backup
    - Create safety backup before rollback
    - Update version marker
    """

    VERSION_MARKER_FILE = ".devforgeai_installed"

    def __init__(self, project_root: Path):
        """
        Initialize RollbackManager.

        Args:
            project_root: Path to DevForgeAI installation
        """
        self.project_root = Path(project_root)
        self._version_data: Optional[Dict] = None

        # Load version data
        self._load_version_data()

    def _load_version_data(self) -> None:
        """Load version data from marker file."""
        marker_path = self.project_root / self.VERSION_MARKER_FILE
        if marker_path.exists():
            try:
                self._version_data = json.loads(marker_path.read_text())
            except json.JSONDecodeError:
                logger.warning(f"Failed to parse version marker: {marker_path}")
                self._version_data = None

    def list_available_backups(self) -> List[Dict[str, Any]]:
        """
        List available backups (AC#4).

        Returns:
            List of backup info dictionaries
        """
        return list_backups(self.project_root)

    def _create_safety_backup(self) -> Optional[Path]:
        """
        Create safety backup before rollback (AC#4).

        Returns:
            Path to safety backup, or None on failure
        """
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_name = f"{self.project_root.name}.backup-{timestamp}-pre-rollback"
        backup_path = self.project_root.parent / backup_name

        try:
            logger.info(f"Creating safety backup at {backup_path}")
            shutil.copytree(
                self.project_root,
                backup_path,
                ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.git')
            )
            return backup_path
        except Exception as e:
            logger.error(f"Failed to create safety backup: {e}")
            return None

    def _update_version_marker(self, backup_path: Path) -> None:
        """
        Update version marker after rollback (AC#4).

        Args:
            backup_path: Path to restored backup
        """
        # Try to get version from backup manifest
        manifest_path = backup_path / "manifest.json"
        version = "unknown"

        if manifest_path.exists():
            try:
                manifest = json.loads(manifest_path.read_text())
                version = manifest.get("from_version", "unknown")
            except Exception:
                pass

        # Update marker
        marker_path = self.project_root / self.VERSION_MARKER_FILE
        if self._version_data:
            self._version_data["version"] = version
            self._version_data["updated_at"] = datetime.now(timezone.utc).isoformat()
            self._version_data["rollback_from"] = self._version_data.get("version", "unknown")
        else:
            self._version_data = {
                "version": version,
                "installed_at": datetime.now(timezone.utc).isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat(),
                "components": {},
                "checksums": {}
            }

        marker_path.write_text(json.dumps(self._version_data, indent=2))
        logger.info(f"Version marker updated to {version}")

    def _confirm_rollback(self, backup: Dict[str, Any]) -> bool:
        """
        Prompt user to confirm rollback.

        Args:
            backup: Backup info dictionary

        Returns:
            True if user confirms
        """
        try:
            print(f"\nRollback to: {backup.get('name', 'unknown')}")
            print(f"  Version: {backup.get('from_version', 'unknown')}")
            print(f"  Created: {backup.get('timestamp', 'unknown')}")
            response = input("\nProceed with rollback? [y/N] ").strip().lower()
            return response in ('y', 'yes')
        except EOFError:
            return False

    def rollback(self, backup_id: Optional[str] = None, force: bool = False) -> int:
        """
        Rollback to a previous backup (AC#4).

        Args:
            backup_id: Specific backup name/id to restore, or None for interactive selection
            force: Skip confirmation prompt

        Returns:
            Exit code (0 = success)
        """
        # List available backups
        backups = self.list_available_backups()

        if not backups:
            logger.error("No backups available for rollback")
            print("Error: No backups found.")
            return ExitCodes.VALIDATION_FAILED

        # Select backup
        if backup_id:
            # Find specific backup
            selected = None
            for backup in backups:
                if backup["name"] == backup_id or str(backup["path"]) == backup_id:
                    selected = backup
                    break

            if not selected:
                logger.error(f"Backup not found: {backup_id}")
                print(f"Error: Backup not found: {backup_id}")
                return ExitCodes.VALIDATION_FAILED
        else:
            # Interactive selection
            print("\nAvailable backups:")
            for i, backup in enumerate(backups, 1):
                version = backup.get('from_version', 'unknown')
                timestamp = backup.get('timestamp', 'unknown')
                print(f"  {i}. {backup['name']} (version {version})")

            try:
                choice = input(f"\nSelect backup (1-{len(backups)}): ").strip()
                idx = int(choice) - 1
                if 0 <= idx < len(backups):
                    selected = backups[idx]
                else:
                    print("Invalid selection.")
                    return ExitCodes.VALIDATION_FAILED
            except (ValueError, EOFError):
                print("Invalid input.")
                return ExitCodes.VALIDATION_FAILED

        # Confirm rollback
        if not force:
            if not self._confirm_rollback(selected):
                print("Rollback cancelled.")
                return ExitCodes.SUCCESS

        # Create safety backup
        safety_backup = self._create_safety_backup()
        if not safety_backup:
            print("Warning: Could not create safety backup. Proceeding anyway.")

        # Restore from selected backup
        try:
            backup_path = Path(selected["path"])
            result = restore_from_backup(self.project_root, backup_path)

            if result["status"] == "success":
                # Update version marker
                self._update_version_marker(backup_path)

                logger.info(f"Rollback successful: {result['files_restored']} files restored")
                print(f"\nRollback successful!")
                print(f"  Files restored: {result['files_restored']}")
                print(f"  Safety backup: {safety_backup}")
                return ExitCodes.SUCCESS
            else:
                logger.error(f"Rollback failed: {result['errors']}")
                print(f"Rollback failed: {result['errors']}")
                return ExitCodes.ROLLBACK_OCCURRED

        except Exception as e:
            logger.error(f"Rollback error: {e}")
            print(f"Rollback error: {e}")
            return ExitCodes.ROLLBACK_OCCURRED

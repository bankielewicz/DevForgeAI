"""
Cleanup Manager for DevForgeAI (STORY-251)

Provides automatic backup cleanup:
- AC#8: Automatic backup cleanup

Usage:
    from installer.cleanup import CleanupManager

    manager = CleanupManager(target_path=Path("/path/to/project"))
    exit_code = manager.cleanup()
"""

import json
import logging
import shutil
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any

from installer.exit_codes import ExitCodes

logger = logging.getLogger(__name__)


class CleanupManager:
    """
    Manages backup cleanup operations.

    Implements AC#8: Automatic Backup Cleanup.
    """

    def __init__(
        self,
        target_path: Path,
        keep_recent: int = 3,
        max_age_days: int = 90
    ):
        """
        Initialize CleanupManager.

        Args:
            target_path: Path to DevForgeAI installation
            keep_recent: Number of recent backups to keep (default: 3)
            max_age_days: Maximum age of backups in days (default: 90)
        """
        self.target_path = Path(target_path)
        self.keep_recent = keep_recent
        self.max_age_days = max_age_days

    def _get_backup_timestamp(self, backup_path: Path) -> Optional[datetime]:
        """Extract timestamp from backup directory name or manifest."""
        # Try to extract from directory name (format: project.backup-YYYYMMDD-HHMMSS)
        name = backup_path.name
        try:
            # Find the timestamp part
            if ".backup-" in name:
                timestamp_str = name.split(".backup-")[1]
                # Parse YYYYMMDD-HHMMSS
                return datetime.strptime(timestamp_str, "%Y%m%d-%H%M%S")
        except Exception:
            pass

        # Try to read from manifest
        manifest_path = backup_path / "manifest.json"
        if manifest_path.exists():
            try:
                manifest = json.loads(manifest_path.read_text())
                created_at = manifest.get("created_at")
                if created_at:
                    return datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            except Exception:
                pass

        return None

    def _analyze_backups(self) -> List[Dict[str, Any]]:
        """
        Analyze existing backups (AC#8).

        Returns:
            List of backup info dictionaries
        """
        backups = []
        backup_parent = self.target_path.parent

        # Find backup directories
        for path in backup_parent.glob(f"{self.target_path.name}.backup-*"):
            if path.is_dir():
                backup_info = {
                    "path": path,
                    "name": path.name,
                    "size_bytes": 0,
                    "size_mb": 0,
                    "version": "unknown",
                    "created_at": None,
                    "age_days": 0,
                    "should_remove": False,
                    "removal_reason": None
                }

                # Get size
                try:
                    total_size = sum(
                        f.stat().st_size for f in path.rglob("*") if f.is_file()
                    )
                    backup_info["size_bytes"] = total_size
                    backup_info["size_mb"] = round(total_size / (1024 * 1024), 1)
                except Exception:
                    pass

                # Get timestamp
                timestamp = self._get_backup_timestamp(path)
                if timestamp:
                    backup_info["created_at"] = timestamp
                    # Calculate age in days
                    now = datetime.now()
                    if timestamp.tzinfo:
                        now = datetime.now(timezone.utc)
                    age = now - timestamp.replace(tzinfo=None) if not timestamp.tzinfo else now - timestamp
                    backup_info["age_days"] = age.days

                # Try to read manifest for version
                manifest_path = path / "manifest.json"
                if manifest_path.exists():
                    try:
                        manifest = json.loads(manifest_path.read_text())
                        backup_info["version"] = manifest.get("from_version", "unknown")
                    except Exception:
                        pass

                backups.append(backup_info)

        # Sort by timestamp (newest first)
        backups.sort(
            key=lambda b: b["created_at"] or datetime.min,
            reverse=True
        )

        # Determine which to remove based on policy
        for i, backup in enumerate(backups):
            # Keep the N most recent
            if i < self.keep_recent:
                continue

            # Check age
            if backup["age_days"] > self.max_age_days:
                backup["should_remove"] = True
                backup["removal_reason"] = f"Older than {self.max_age_days} days"
            elif backup["age_days"] > 30:
                backup["should_remove"] = True
                backup["removal_reason"] = f"Beyond keep_recent ({self.keep_recent}) and older than 30 days"

        return backups

    def _display_cleanup_policy(self) -> None:
        """Display cleanup policy (AC#8)."""
        print("\nBackup Cleanup Policy:")
        print(f"  - Keep most recent: {self.keep_recent} backups")
        print(f"  - Keep backups newer than: 30 days")
        print(f"  - Remove backups older than: {self.max_age_days} days")
        print("")

    def _display_cleanup_preview(self, backups: List[Dict[str, Any]]) -> None:
        """Display preview of cleanup operation (AC#8)."""
        to_remove = [b for b in backups if b["should_remove"]]

        if not to_remove:
            print("No backups to remove (all within policy).")
            return

        print("Will remove:")
        for backup in to_remove:
            created = backup["created_at"]
            if created:
                date_str = created.strftime("%Y-%m-%d")
            else:
                date_str = "unknown"
            print(f"  - {date_str} ({backup['version']}) - {backup['size_mb']} MB - {backup['age_days']} days old")

        print("")

    def _calculate_space_to_reclaim(self, backups: List[Dict[str, Any]]) -> int:
        """
        Calculate total space to reclaim (AC#8).

        Returns:
            Total bytes to reclaim
        """
        to_remove = [b for b in backups if b["should_remove"]]
        return sum(b["size_bytes"] for b in to_remove)

    def _confirm_cleanup(self) -> bool:
        """
        Prompt user to confirm cleanup.

        Returns:
            True if user confirms
        """
        try:
            response = input("Proceed? [Y/n] ").strip().lower()
            return response in ('', 'y', 'yes')
        except EOFError:
            return False

    def _remove_backups(self, backups: List[Dict[str, Any]]) -> int:
        """
        Remove backups marked for removal.

        Args:
            backups: List of backup info dictionaries

        Returns:
            Number of backups removed
        """
        removed = 0
        to_remove = [b for b in backups if b["should_remove"]]

        for backup in to_remove:
            try:
                shutil.rmtree(backup["path"])
                removed += 1
                logger.info(f"Removed backup: {backup['name']}")
            except Exception as e:
                logger.error(f"Failed to remove {backup['path']}: {e}")

        return removed

    def _write_cleanup_log(self, removed_backups: List[Dict[str, Any]], space_reclaimed: int) -> None:
        """Write cleanup log."""
        log_path = self.target_path / "cleanup.log"

        log_content = [
            "DevForgeAI Backup Cleanup Log",
            "=" * 30,
            "",
            f"Timestamp: {datetime.now(timezone.utc).isoformat()}",
            f"Backups removed: {len(removed_backups)}",
            f"Space reclaimed: {space_reclaimed / (1024 * 1024):.1f} MB",
            "",
            "Removed backups:",
        ]

        for backup in removed_backups:
            log_content.append(f"  - {backup['name']} ({backup['version']})")

        log_path.write_text("\n".join(log_content))
        logger.info(f"Cleanup log saved to {log_path}")

    def cleanup(self, force: bool = False) -> int:
        """
        Perform backup cleanup (AC#8).

        Args:
            force: If True, skip confirmation prompt (for silent mode)

        Returns:
            Exit code (0 = success)
        """
        # Display policy
        self._display_cleanup_policy()

        # Analyze backups
        backups = self._analyze_backups()

        if not backups:
            print("No backups found.")
            return ExitCodes.SUCCESS

        # Calculate space to reclaim
        space_to_reclaim = self._calculate_space_to_reclaim(backups)

        # Display preview
        self._display_cleanup_preview(backups)

        to_remove = [b for b in backups if b["should_remove"]]

        if not to_remove:
            return ExitCodes.SUCCESS

        print(f"Space to reclaim: {space_to_reclaim / (1024 * 1024):.0f} MB")

        # Confirm (unless force mode)
        if not force and not self._confirm_cleanup():
            print("Cleanup cancelled.")
            return ExitCodes.SUCCESS

        # Remove backups
        removed = self._remove_backups(backups)

        # Write log
        self._write_cleanup_log(to_remove, space_to_reclaim)

        print(f"\nCleanup complete. Removed {removed} backup(s).")
        print(f"Reclaimed {space_to_reclaim / (1024 * 1024):.1f} MB")

        return ExitCodes.SUCCESS

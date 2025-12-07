"""
BackupCleaner for retention-based backup cleanup and deletion (STORY-080).

Enforces retention policy:
- Deletes oldest backups beyond retention_count
- Preserves cleanup_excluded_backup_id (backup being restored)
- Skips cleanup if condition not met

Implements AC#8: Backup cleanup with retention policy
"""

import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional, List
from abc import ABC, abstractmethod

from installer.models import CleanupResult


class ILogger(ABC):
    """Logger interface for dependency injection."""

    @abstractmethod
    def info(self, message: str) -> None:
        """Log info level message."""
        pass

    @abstractmethod
    def error(self, message: str) -> None:
        """Log error level message."""
        pass


class BackupCleaner:
    """Deletes old backups based on retention policy."""

    def __init__(
        self,
        backup_dir: Path,
        retention_count: int = 5,
        cleanup_excluded_backup_id: Optional[str] = None,
        logger: Optional[ILogger] = None,
    ):
        """
        Initialize cleaner with retention policy.

        Args:
            backup_dir: Path to backups directory
            retention_count: Number of backups to keep (delete older ones)
            cleanup_excluded_backup_id: Backup ID to never delete
            logger: Optional logger
        """
        self.backup_dir = Path(backup_dir)
        self.retention_count = retention_count
        self.cleanup_excluded_backup_id = cleanup_excluded_backup_id
        self.logger = logger

    def cleanup(
        self,
        skip_if_condition_met: bool = False,
        condition_met: Optional[bool] = None,
    ) -> CleanupResult:
        """
        Delete old backups to enforce retention policy.

        Args:
            skip_if_condition_met: If True, skip cleanup if condition_met is False
            condition_met: Condition to check (e.g., rollback successful)

        Returns:
            CleanupResult with deleted backup count and IDs
        """
        try:
            # Skip cleanup if condition not met
            if skip_if_condition_met and condition_met is False:
                if self.logger:
                    self.logger.info("Skipping cleanup - condition not met")
                return CleanupResult(
                    deleted_count=0,
                    deleted_backup_ids=[],
                )

            # List all backups
            backups = self._list_backups()

            if len(backups) <= self.retention_count:
                # No cleanup needed
                return CleanupResult(
                    deleted_count=0,
                    deleted_backup_ids=[],
                )

            # Sort by timestamp (oldest first)
            backups.sort(key=lambda b: b["timestamp"])

            # Calculate how many to delete
            num_to_delete = len(backups) - self.retention_count
            deleted_ids = []

            # Delete oldest backups
            for i in range(num_to_delete):
                backup = backups[i]
                backup_id = backup["id"]

                # Never delete excluded backup
                if backup_id == self.cleanup_excluded_backup_id:
                    if self.logger:
                        self.logger.info(f"Preserving excluded backup: {backup_id}")
                    continue

                # Delete backup
                try:
                    backup_path = self.backup_dir / backup_id
                    if backup_path.exists():
                        shutil.rmtree(backup_path)
                        deleted_ids.append(backup_id)
                        if self.logger:
                            self.logger.info(f"Deleted backup: {backup_id}")
                except Exception as e:
                    if self.logger:
                        self.logger.error(f"Failed to delete {backup_id}: {e}")

            return CleanupResult(
                deleted_count=len(deleted_ids),
                deleted_backup_ids=deleted_ids,
            )

        except Exception as e:
            if self.logger:
                self.logger.error(f"Cleanup error: {str(e)}")
            return CleanupResult(
                deleted_count=0,
                deleted_backup_ids=[],
            )

    def _list_backups(self) -> List[dict]:
        """
        List all backups with metadata.

        Returns:
            List of backup dicts with id, timestamp, path
        """
        backups = []

        if not self.backup_dir.exists():
            return backups

        for backup_path in self.backup_dir.iterdir():
            if not backup_path.is_dir():
                continue

            # Read metadata.json
            metadata_path = backup_path / "metadata.json"
            if not metadata_path.exists():
                continue

            try:
                with open(metadata_path, "r") as f:
                    metadata = json.load(f)

                # Parse timestamp
                timestamp_str = metadata.get("timestamp", "")
                timestamp = datetime.fromisoformat(timestamp_str)

                backup_info = {
                    "id": metadata.get("id", backup_path.name),
                    "timestamp": timestamp,
                    "path": backup_path,
                }
                backups.append(backup_info)
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Error reading backup metadata: {e}")
                continue

        return backups

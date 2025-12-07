"""
BackupSelector for listing and selecting available backups (STORY-080).

Lists all available backups, formats them for display, and selects by ID.

Implements:
- AC#2: List available backups
- AC#3: Format backups for display with version, date, size, reason
- AC#3: Sort by timestamp (newest first)
"""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Optional
from abc import ABC, abstractmethod

from installer.models import BackupInfo


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


class BackupSelector:
    """Lists, formats, and selects available backups."""

    def __init__(self, backup_dir: Path, logger: Optional[ILogger] = None):
        """
        Initialize selector.

        Args:
            backup_dir: Path to backups directory
            logger: Optional logger for info/error messages
        """
        self.backup_dir = Path(backup_dir)
        self.logger = logger

    def list(self) -> List[BackupInfo]:
        """
        List all available backups sorted by timestamp (newest first).

        Returns:
            List of BackupInfo objects sorted by timestamp (newest first)
        """
        backups = []

        # List all backup directories
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

                # Create BackupInfo
                backup_info = BackupInfo(
                    id=metadata.get("id", backup_path.name),
                    version=metadata.get("version", "unknown"),
                    timestamp=timestamp,
                    size_bytes=metadata.get("size_bytes", 0),
                    reason=metadata.get("reason", "UNKNOWN"),
                    path=str(backup_path),
                )
                backups.append(backup_info)
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Error reading backup metadata from {backup_path}: {e}")
                continue

        # Sort by timestamp (newest first)
        backups.sort(key=lambda b: b.timestamp, reverse=True)

        return backups

    def format_for_display(self, backup_info: BackupInfo) -> str:
        """
        Format backup info for display.

        Args:
            backup_info: BackupInfo object

        Returns:
            Formatted string with version, date, size, reason
        """
        # Format timestamp
        timestamp_str = backup_info.timestamp.strftime("%Y-%m-%d %H:%M:%S")

        # Format size
        size_mb = backup_info.size_bytes / (1024 * 1024)

        # Format output
        formatted = (
            f"ID: {backup_info.id} | "
            f"Version: {backup_info.version} | "
            f"Date: {timestamp_str} | "
            f"Size: {size_mb:.1f} MB | "
            f"Reason: {backup_info.reason}"
        )

        return formatted

    def select(self, backup_id: str) -> Optional[BackupInfo]:
        """
        Select a backup by ID.

        Args:
            backup_id: ID of backup to select

        Returns:
            BackupInfo if found, None otherwise
        """
        backups = self.list()

        for backup in backups:
            if backup.id == backup_id:
                return backup

        if self.logger:
            self.logger.error(f"Backup not found: {backup_id}")

        return None

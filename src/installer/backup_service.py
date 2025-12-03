"""Backup service (AC#7).

Creates timestamped backups before file operations, with structure preservation.
"""
from datetime import datetime
from pathlib import Path
import shutil
from typing import List, Optional


class BackupService:
    """Creates and manages installation backups."""

    def __init__(self, backup_base: str = ".devforgeai"):
        """Initialize backup service."""
        self.backup_base = Path(backup_base)
        self.backup_base.mkdir(parents=True, exist_ok=True)
        self.backup_dir: Optional[Path] = None

    def _get_timestamp(self) -> str:
        """Return ISO 8601 timestamp for backup directory name."""
        return datetime.now().strftime("%Y-%m-%dT%H-%M-%S")

    def create_backup(self, source_paths: List[str]) -> str:
        """Create timestamped backup directory and copy files.

        Args:
            source_paths: List of file paths to backup

        Returns:
            Path to created backup directory

        Raises:
            OSError: If backup creation fails
        """
        timestamp = self._get_timestamp()
        self.backup_dir = self.backup_base / f"install-backup-{timestamp}"

        try:
            self.backup_dir.mkdir(parents=True, exist_ok=True)

            for source_path in source_paths:
                source = Path(source_path)
                if source.exists():
                    # Preserve directory structure
                    rel_path = source.relative_to(source.parent.parent) if source.parent.parent.exists() else source.name
                    dest = self.backup_dir / rel_path

                    if source.is_file():
                        dest.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(source, dest)
                    elif source.is_dir():
                        dest.mkdir(parents=True, exist_ok=True)
                        shutil.copytree(source, dest, dirs_exist_ok=True)

            # Set permissions (0700 - owner access only)
            self.backup_dir.chmod(0o700)

            return str(self.backup_dir)

        except Exception as e:
            # Clean up partial backup on failure
            if self.backup_dir and self.backup_dir.exists():
                shutil.rmtree(self.backup_dir)
            raise

    def restore_from_backup(self, backup_path: str, target_paths: dict) -> None:
        """Restore files from backup to target location.

        Args:
            backup_path: Path to backup directory
            target_paths: Dict mapping backup file paths to target paths
        """
        backup_root = Path(backup_path)

        for backup_file, target_file in target_paths.items():
            backup_file_path = backup_root / backup_file
            target_file_path = Path(target_file)

            if backup_file_path.exists():
                target_file_path.parent.mkdir(parents=True, exist_ok=True)
                if backup_file_path.is_file():
                    shutil.copy2(backup_file_path, target_file_path)
                elif backup_file_path.is_dir():
                    if target_file_path.exists():
                        shutil.rmtree(target_file_path)
                    shutil.copytree(backup_file_path, target_file_path)

    def cleanup_old_backups(self, keep_count: int = 5, max_age_days: int = 7) -> None:
        """Clean up old backups (>7 days, keep last 5).

        Args:
            keep_count: Number of recent backups to keep
            max_age_days: Delete backups older than this many days
        """
        backup_dirs = sorted([d for d in self.backup_base.iterdir()
                            if d.is_dir() and d.name.startswith('install-backup-')],
                           key=lambda x: x.name, reverse=True)

        # Remove by age
        from time import time
        now = time()
        max_age_seconds = max_age_days * 24 * 60 * 60

        for backup_dir in backup_dirs[keep_count:]:
            if now - backup_dir.stat().st_mtime > max_age_seconds:
                shutil.rmtree(backup_dir, ignore_errors=True)

    def get_backup_dir(self) -> Optional[Path]:
        """Return current backup directory path."""
        return self.backup_dir

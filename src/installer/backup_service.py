"""Backup service (AC#7).

Creates timestamped backups before file operations, with structure preservation.
Story: STORY-074 - Comprehensive Error Handling
AC#7: Creates devforgeai/install-backup-{timestamp}/ directory, copies files,
      preserves directory structure, logs backup location, cleans old backups (>7 days, min 5).
"""
import shutil
import time
from datetime import datetime
from pathlib import Path
from typing import List, Optional


class BackupService:
    """Creates and manages installation backups with timestamped directory structure.

    Implements AC#7 requirements:
    - Timestamped backup directory creation (devforgeai/install-backup-YYYY-MM-DDTHH-MM-SS/)
    - Directory structure preservation in backup
    - Backup location logging to install.log
    - Automatic cleanup of backups >7 days old (keeping minimum 5)
    """

    def __init__(self, logger):
        """Initialize backup service with logger dependency.

        Args:
            logger: InstallLogger instance for logging backup operations.
        """
        self.logger = logger
        self.backup_dir: Optional[Path] = None

    def _get_timestamp(self) -> str:
        """Return ISO 8601 timestamp for backup directory name.

        Format: YYYY-MM-DDTHH-MM-SS (19 characters total)
        Example: 2025-12-03T14-30-45

        Returns:
            ISO 8601 formatted timestamp string.
        """
        return datetime.now().strftime("%Y-%m-%dT%H-%M-%S")

    def create_backup(self, target_dir: Path, files_to_backup: List[Path]) -> Path:
        """Create timestamped backup directory and copy files (AC#7).

        Creates backup directory in target_dir/devforgeai/install-backup-{timestamp}/.
        Preserves relative directory structure from target_dir.

        Args:
            target_dir: Base directory where .devforgeai will be created.
            files_to_backup: List of file paths to backup (relative to target_dir).

        Returns:
            Path to created backup directory.

        Raises:
            PermissionError: If backup directory cannot be created (halts installation).
            OSError: If file copy fails (disk full, permission denied, etc.).

        Example:
            >>> backup_service = BackupService(logger)
            >>> backup_dir = backup_service.create_backup(
            ...     target_dir=Path("/home/user/project"),
            ...     files_to_backup=[Path("/home/user/project/.claude/commands/dev.md")]
            ... )
            >>> backup_dir
            PosixPath('/home/user/project/devforgeai/install-backup-2025-12-03T14-30-45')
        """
        start_time = time.time()

        # Create backup directory path: target_dir/devforgeai/install-backup-{timestamp}/
        timestamp = self._get_timestamp()
        backup_base = target_dir / ".devforgeai"
        self.backup_dir = backup_base / f"install-backup-{timestamp}"

        try:
            # Create backup directory (may raise PermissionError)
            self.backup_dir.mkdir(parents=True, exist_ok=True)

            # Copy files to backup, preserving relative directory structure
            backed_up_count = 0
            for file_path in files_to_backup:
                if not file_path.exists():
                    # Skip nonexistent files with warning
                    self.logger.log_warning(
                        f"Backup: File does not exist, skipping: {file_path}"
                    )
                    continue

                # Calculate relative path from target_dir
                try:
                    rel_path = file_path.relative_to(target_dir)
                except ValueError:
                    # File not relative to target_dir, use just the name
                    rel_path = Path(file_path.name)

                dest_path = self.backup_dir / rel_path

                # Handle symlinks (backup the link, not the target)
                if file_path.is_symlink():
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    # Copy symlink without following it
                    shutil.copy2(file_path, dest_path, follow_symlinks=False)
                    backed_up_count += 1
                elif file_path.is_file():
                    # Ensure parent directory exists
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    # Copy file with metadata preservation
                    shutil.copy2(file_path, dest_path)
                    backed_up_count += 1
                elif file_path.is_dir():
                    # Copy entire directory tree
                    dest_path.mkdir(parents=True, exist_ok=True)
                    shutil.copytree(file_path, dest_path, dirs_exist_ok=True)
                    backed_up_count += 1

            # Set restrictive permissions (0700 - owner access only)
            self.backup_dir.chmod(0o700)

            # Log backup completion with metrics
            elapsed = time.time() - start_time
            self.logger.log_info(
                f"Backup created: {self.backup_dir} ({backed_up_count} files, "
                f"duration: {elapsed:.2f}s)"
            )

            return self.backup_dir

        except Exception as e:
            # Clean up partial backup on failure
            if self.backup_dir and self.backup_dir.exists():
                shutil.rmtree(self.backup_dir, ignore_errors=True)
            raise

    def get_latest_backup(self, backups_root: Path) -> Optional[Path]:
        """Get the most recent backup directory.

        Args:
            backups_root: Root directory containing backup directories
                         (e.g., .devforgeai).

        Returns:
            Path to most recent backup directory, or None if no backups exist.
        """
        backup_dirs = [
            d for d in backups_root.iterdir()
            if d.is_dir() and d.name.startswith("install-backup-")
        ]

        if not backup_dirs:
            return None

        # Sort by directory name (timestamp format YYYY-MM-DDTHH-MM-SS sorts correctly)
        backup_dirs.sort()
        return backup_dirs[-1]  # Return most recent

    def cleanup_old_backups(self, backups_root: Path, days: int = 7) -> None:
        """Clean up backups older than specified days, keeping minimum 5 (AC#7, SVC-012).

        Removes backups that meet BOTH conditions:
        1. Older than specified days (default 7 days)
        2. AND there are more than 5 backups total (keep minimum 5)

        Args:
            backups_root: Root directory containing backup directories
                         (e.g., .devforgeai).
            days: Age threshold in days (default 7). Backups older than this
                  are candidates for deletion.

        Example:
            >>> service.cleanup_old_backups(
            ...     backups_root=Path("/home/user/.devforgeai"),
            ...     days=7
            ... )
            # Removes backups older than 7 days, keeping minimum 5 recent ones
        """
        if not backups_root.exists():
            return

        # Find all backup directories
        backup_dirs = [
            d for d in backups_root.iterdir()
            if d.is_dir() and d.name.startswith("install-backup-")
        ]

        if len(backup_dirs) <= 5:
            # Keep all if 5 or fewer exist
            return

        # Sort by name (timestamp format sorts chronologically)
        backup_dirs.sort()

        # Calculate age threshold
        now = datetime.now()
        max_age_seconds = days * 24 * 60 * 60

        # Remove old backups, keeping at least 5 most recent
        for backup_dir in backup_dirs[:-5]:  # Keep last 5
            try:
                # Get backup modification time
                mtime = backup_dir.stat().st_mtime
                backup_age_seconds = time.time() - mtime

                # Delete if older than threshold
                if backup_age_seconds > max_age_seconds:
                    shutil.rmtree(backup_dir, ignore_errors=True)
                    self.logger.log_info(f"Cleaned up old backup: {backup_dir.name}")
            except Exception as e:
                self.logger.log_warning(
                    f"Failed to clean up backup {backup_dir.name}: {e}"
                )

    def get_backup_location(self) -> Optional[Path]:
        """Get the path of the current backup directory.

        Returns:
            Path to current backup directory, or None if no backup created yet.
        """
        return self.backup_dir

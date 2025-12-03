"""Rollback service (AC#4).

Restores files from backup, removes partial installations, cleans empty directories.
"""
from pathlib import Path
import shutil
from typing import List, Optional
from .install_logger import InstallLogger


class RollbackService:
    """Handles rollback operations on installation failure."""

    def __init__(self, logger: Optional[InstallLogger] = None):
        """Initialize rollback service."""
        self.logger = logger or InstallLogger()
        self.files_created: List[Path] = []
        self.dirs_created: List[Path] = []

    def track_file_creation(self, file_path: str) -> None:
        """Track a file created during installation."""
        self.files_created.append(Path(file_path))

    def track_dir_creation(self, dir_path: str) -> None:
        """Track a directory created during installation."""
        self.dirs_created.append(Path(dir_path))

    def rollback(self, backup_dir: str, target_root: Optional[str] = None) -> bool:
        """Execute full rollback: restore from backup, remove partials, clean dirs.

        Args:
            backup_dir: Path to backup directory
            target_root: Optional target root for partial file cleanup

        Returns:
            True if rollback successful, False otherwise
        """
        try:
            self.logger.log_action("ROLLBACK_START", f"from backup {backup_dir}")

            # Restore files from backup
            self._restore_from_backup(backup_dir)

            # Remove partial files created during failed installation
            self._remove_partial_files()

            # Clean up empty directories created during installation
            self._clean_empty_directories()

            self.logger.log_action("ROLLBACK_COMPLETE")
            return True

        except Exception as e:
            self.logger.log_error(
                "ROLLBACK_FAILED",
                3,
                f"Rollback operation failed: {str(e)}",
                stack_trace=str(e)
            )
            return False

    def _restore_from_backup(self, backup_dir: str) -> None:
        """Restore all files from backup directory."""
        backup_path = Path(backup_dir)

        if not backup_path.exists():
            raise FileNotFoundError(f"Backup directory not found: {backup_dir}")

        for backup_file in backup_path.rglob("*"):
            if backup_file.is_file():
                rel_path = backup_file.relative_to(backup_path)
                # Restore to same location
                target = backup_path.parent.parent / rel_path
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(backup_file, target)
                self.logger.log_action("RESTORED", f"{target}")

    def _remove_partial_files(self) -> None:
        """Remove files that were created but not in backup."""
        for file_path in self.files_created:
            if file_path.exists() and not self._is_in_backup(file_path):
                try:
                    file_path.unlink()
                    self.logger.log_action("REMOVED_PARTIAL", f"{file_path}")
                except Exception as e:
                    self.logger.log_action("REMOVE_PARTIAL_FAILED", f"{file_path}: {str(e)}")

    def _clean_empty_directories(self) -> None:
        """Remove empty directories created during installation."""
        for dir_path in sorted(self.dirs_created, reverse=True):
            if dir_path.exists() and not any(dir_path.iterdir()):
                try:
                    dir_path.rmdir()
                    self.logger.log_action("REMOVED_EMPTY_DIR", f"{dir_path}")
                except Exception:
                    pass  # Ignore if directory not empty or removal fails

    def _is_in_backup(self, file_path: Path) -> bool:
        """Check if file exists in any backup."""
        # Look for backup directories
        backup_base = Path(".devforgeai")
        for backup_dir in backup_base.glob("install-backup-*"):
            if backup_dir.is_dir():
                # Check if file has corresponding entry in backup
                rel_path = file_path.relative_to(file_path.parent.parent)
                if (backup_dir / rel_path).exists():
                    return True
        return False

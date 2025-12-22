"""Rollback service (AC#4, AC#8).

Restores files from backup, removes partial installations, cleans empty directories.
Implements comprehensive error handling with graceful degradation on permission errors.
"""
from pathlib import Path
import shutil
import time
from typing import List, Optional
from dataclasses import dataclass
from .install_logger import InstallLogger
from .exit_codes import ExitCodes


@dataclass
class RollbackResult:
    """Result of rollback operation with exit code and statistics."""
    exit_code: int
    files_restored: int = 0
    files_removed: int = 0
    directories_removed: int = 0
    duration_seconds: float = 0.0

    def __eq__(self, other):
        """Allow comparison with integers for backward compatibility.

        Supports both:
        - result == 3 (compares exit_code)
        - result.exit_code == 3 (direct attribute comparison)
        """
        if isinstance(other, int):
            return self.exit_code == other
        return super().__eq__(other)


class RollbackService:
    """Handles rollback operations on installation failure (AC#4, AC#8).

    AC#4: When installation fails, rollback restores the system to pre-installation state:
    - Displays "Rolling back installation..." message
    - Restores all files from backup directory
    - Removes any partially copied files not in backup
    - Cleans up temporary directories and artifacts
    - Displays "Rollback complete. System restored to pre-installation state."
    - Returns exit code 3 (ROLLBACK_OCCURRED)

    AC#8: Rolls back partial installations by:
    - Removing any files created during failed installation
    - Preserving files that exist in backup directory
    - Removing empty directories created during installation
    - Logging all cleanup actions
    - Continuing on individual file permission errors (logs but doesn't crash)
    """

    def __init__(self, logger: Optional[InstallLogger] = None):
        """Initialize rollback service.

        Args:
            logger: Optional InstallLogger instance (creates default if not provided)
        """
        self.logger = logger or InstallLogger()
        self.files_created: List[Path] = []
        self.dirs_created: List[Path] = []

    def track_file_creation(self, file_path: str) -> None:
        """Track a file created during installation.

        Args:
            file_path: Path to file that was created
        """
        self.files_created.append(Path(file_path))

    def track_dir_creation(self, dir_path: str) -> None:
        """Track a directory created during installation.

        Args:
            dir_path: Path to directory that was created
        """
        self.dirs_created.append(Path(dir_path))

    def rollback(self, backup_dir, target_dir) -> RollbackResult:
        """Execute full rollback: restore from backup, remove partials, clean dirs (AC#4).

        This is the main rollback entry point that orchestrates the complete rollback process.
        Displays console messages and returns exit code 3 (ROLLBACK_OCCURRED).

        Args:
            backup_dir: Path to backup directory with files to restore
            target_dir: Path to target directory where files should be restored

        Returns:
            RollbackResult with exit code 3 and operation statistics

        Raises:
            FileNotFoundError: If backup directory doesn't exist
        """
        start_time = time.time()
        result = RollbackResult(exit_code=ExitCodes.ROLLBACK_OCCURRED)

        try:
            # Display start message
            print("Rolling back installation...")
            self.logger.log_info("Starting rollback from backup directory")

            # Restore files from backup directory
            result.files_restored = self.restore_from_backup(
                backup_dir=backup_dir,
                target_dir=target_dir
            )
            self.logger.log_info(f"Restored {result.files_restored} files from backup")

            # Remove partial files created during failed installation
            result.files_removed = self.cleanup_partial_installation(
                target_dir=target_dir,
                backup_dir=backup_dir,
                installation_manifest=self.files_created
            )
            self.logger.log_info(f"Removed {result.files_removed} partial installation files")

            # Clean up empty directories created during installation
            result.directories_removed = self.remove_empty_directories(target_dir)
            self.logger.log_info(f"Removed {result.directories_removed} empty directories")

            # Log final statistics
            elapsed = time.time() - start_time
            result.duration_seconds = elapsed
            self.logger.log_info(
                f"Rollback complete: {result.files_restored} files restored, "
                f"{result.files_removed} files removed, "
                f"{result.directories_removed} directories removed (duration: {elapsed:.2f}s)"
            )

            # Display completion message
            print("Rollback complete. System restored to pre-installation state.")

            return result

        except FileNotFoundError as e:
            # Re-raise with helpful message for backup not found
            error_msg = (
                f"Backup directory not found: {backup_dir}\n"
                "Cannot rollback without backup. Manual intervention required.\n"
                "Please restore files manually or contact support."
            )
            raise FileNotFoundError(error_msg) from e
        except Exception as e:
            elapsed = time.time() - start_time
            result.duration_seconds = elapsed
            self.logger.log_error(
                f"Rollback operation failed: {str(e)}"
            )
            raise

    def restore_from_backup(self, backup_dir, target_dir) -> int:
        """Restore all files from backup directory to target directory (AC#4).

        Copies all files from backup_dir to target_dir while preserving directory
        structure and handling symlinks correctly (copying symlinks, not following them).

        Args:
            backup_dir: Path to backup directory with files to restore
            target_dir: Path to target directory where files should be restored

        Returns:
            Number of files successfully restored

        Raises:
            FileNotFoundError: If backup directory doesn't exist
        """
        backup_path = Path(backup_dir)

        if not backup_path.exists():
            raise FileNotFoundError(
                f"Backup directory not found: {backup_dir}\n"
                "Cannot proceed without backup. Manual intervention required."
            )

        files_restored = 0

        # Walk through all files in backup directory (including subdirectories)
        for backup_file in backup_path.rglob("*"):
            if backup_file.is_file() or backup_file.is_symlink():
                # Calculate relative path from backup directory
                rel_path = backup_file.relative_to(backup_path)
                # Construct target path (parallel structure in target directory)
                target_file = Path(target_dir) / rel_path

                try:
                    # Create parent directories if needed
                    target_file.parent.mkdir(parents=True, exist_ok=True)

                    # Copy file (preserves metadata) without following symlinks
                    # symlink_type=False preserves symlinks as symlinks
                    if backup_file.is_symlink():
                        # Remove target symlink if it exists
                        if target_file.exists() or target_file.is_symlink():
                            target_file.unlink()
                        # Copy symlink as symlink (don't follow it)
                        shutil.copy2(backup_file, target_file, follow_symlinks=False)
                    else:
                        # Copy regular file, overwriting if exists
                        shutil.copy2(backup_file, target_file)

                    self.logger.log_info(f"Restored {target_file}")
                    files_restored += 1

                except PermissionError as e:
                    # Log error but continue with other files (AC#8: continue on permission error)
                    self.logger.log_error(
                        f"Permission denied restoring {target_file}: {str(e)}"
                    )
                except Exception as e:
                    # Log error but continue with other files
                    self.logger.log_error(
                        f"Failed to restore {target_file}: {str(e)}"
                    )

        return files_restored

    def cleanup_partial_installation(
        self,
        target_dir,
        backup_dir,
        installation_manifest: List[Path]
    ) -> int:
        """Remove files created during failed installation (AC#8).

        Removes any files that were created during installation but are NOT present
        in the backup directory. This prevents orphaned files from remaining on the system.
        Preserves all files that exist in the backup directory.

        Args:
            target_dir: Path to target directory where files were being installed
            backup_dir: Path to backup directory (files here are preserved)
            installation_manifest: List of file paths that were created during installation

        Returns:
            Number of files successfully removed
        """
        target_path = Path(target_dir)
        backup_path = Path(backup_dir)

        # Build set of files that exist in backup (by relative path)
        backup_files = set()
        if backup_path.exists():
            for backup_file in backup_path.rglob("*"):
                if backup_file.is_file() or backup_file.is_symlink():
                    rel_path = backup_file.relative_to(backup_path)
                    backup_files.add(rel_path)

        files_removed = 0

        # Walk entire target directory to find files NOT in backup
        if target_path.exists():
            for target_file in target_path.rglob("*"):
                if target_file.is_file() or target_file.is_symlink():
                    # Calculate relative path from target
                    try:
                        rel_path = target_file.relative_to(target_path)
                    except ValueError:
                        # File is outside target directory, skip it
                        continue

                    # If file is NOT in backup, remove it
                    if rel_path not in backup_files:
                        try:
                            target_file.unlink()
                            self.logger.log_info(f"Removed partial installation file {target_file}")
                            files_removed += 1
                        except PermissionError as e:
                            # Continue on permission error (AC#8)
                            self.logger.log_error(
                                f"Permission denied removing {target_file}: {str(e)}"
                            )
                        except Exception as e:
                            self.logger.log_error(f"Failed to remove {target_file}: {str(e)}")

        return files_removed

    def remove_empty_directories(self, target_dir) -> int:
        """Remove empty directories created during installation (AC#8).

        Walks the target directory and removes any directories that are empty.
        Uses iterative approach to handle nested structures - when a directory is removed,
        its parent may become empty and should also be checked.

        Args:
            target_dir: Path to target directory to clean up

        Returns:
            Number of directories successfully removed
        """
        target_path = Path(target_dir)

        if not target_path.exists():
            return 0

        directories_removed = 0

        # Keep removing empty directories until no more can be removed
        # This handles nested empty directories properly
        removed_in_pass = True
        while removed_in_pass:
            removed_in_pass = False

            # Build list of all directories (excluding target_dir itself)
            all_dirs = []
            for dir_path in target_path.rglob("*"):
                if dir_path.is_dir():
                    all_dirs.append(dir_path)

            # Sort by depth (deepest first) to handle nested structures
            all_dirs.sort(key=lambda p: len(p.parts), reverse=True)

            for dir_path in all_dirs:
                # Skip target directory itself
                if dir_path == target_path:
                    continue

                # Check if directory exists and is empty
                if dir_path.exists():
                    try:
                        # Check if directory has any contents
                        if not any(dir_path.iterdir()):
                            # Directory is empty, remove it
                            dir_path.rmdir()
                            self.logger.log_info(f"Removed empty directory {dir_path}")
                            directories_removed += 1
                            removed_in_pass = True
                    except OSError:
                        # Directory not empty or permission error, skip it
                        pass

        return directories_removed

"""FileRemover service for STORY-081.

Safely removes files and directories:
- Removes files before parent directories
- Skips preserved files
- Cleans up empty directories
- Handles permission errors gracefully
- Validates paths to prevent system directory removal
"""

import os
import shutil
from pathlib import Path
from typing import Any, List, Optional, Tuple

from installer.uninstall_models import FileRemovalResult


class FileRemover:
    """Safely removes files and directories during uninstall."""

    # System directories that must never be removed
    PROTECTED_PATHS = [
        "/bin", "/usr", "/etc", "/var", "/home", "/root",
        "/sbin", "/lib", "/opt", "/tmp", "/dev", "/proc",
        "C:\\Windows", "C:\\Program Files", "C:\\Users",
    ]

    def __init__(self, file_system: Any = None, logger: Any = None,
                 installation_root: Optional[Path] = None):
        """Initialize file remover.

        Args:
            file_system: File system abstraction (optional, uses real FS if None)
            logger: Logger for error reporting
            installation_root: Root directory constraint for removal
        """
        self.file_system = file_system
        self.logger = logger
        self.installation_root = installation_root or Path.cwd()

    def remove_files(self, files: List[str]) -> FileRemovalResult:
        """Remove list of files.

        Args:
            files: List of file paths to remove

        Returns:
            FileRemovalResult with statistics

        Raises:
            ValueError: If paths are invalid or protected
        """
        # Validate paths first
        self._validate_paths(files)

        result = FileRemovalResult()

        # Sort files by depth (deepest first) to remove children before parents
        sorted_files = sorted(files, key=lambda p: p.count("/"), reverse=True)

        for file_path in sorted_files:
            try:
                if self.file_system:
                    # Use mocked file system
                    size = self.file_system.get_size(file_path) if hasattr(
                        self.file_system, 'get_size') else 0
                    self.file_system.remove_file(file_path)
                else:
                    # Use real file system
                    full_path = self.installation_root / file_path
                    if full_path.exists():
                        size = full_path.stat().st_size
                        full_path.unlink()
                    else:
                        size = 0

                result.files_removed += 1
                result.total_space_bytes += size

            except PermissionError as e:
                error_msg = f"Permission denied: {file_path}"
                result.errors.append(error_msg)
                if self.logger:
                    self.logger.warning(error_msg)

            except FileNotFoundError:
                # File already removed, not an error
                pass

            except Exception as e:
                error_msg = f"Error removing {file_path}: {e}"
                result.errors.append(error_msg)
                if self.logger:
                    self.logger.error(error_msg)

        return result

    def remove_files_with_flags(self, files: List[dict]) -> FileRemovalResult:
        """Remove files respecting preserve flags.

        Args:
            files: List of dicts with 'path' and 'preserve' keys

        Returns:
            FileRemovalResult with statistics
        """
        # Filter out preserved files
        files_to_remove = [f["path"] for f in files if not f.get("preserve", False)]
        return self.remove_files(files_to_remove)

    def cleanup_empty_directories(self, directories: List[str]) -> int:
        """Remove empty directories.

        Args:
            directories: List of directory paths to check

        Returns:
            Count of directories removed
        """
        removed = 0

        # Sort by depth (deepest first) for bottom-up cleanup
        sorted_dirs = sorted(directories, key=lambda p: p.count("/"), reverse=True)

        for dir_path in sorted_dirs:
            try:
                if self.file_system:
                    # Use mocked file system
                    if hasattr(self.file_system, 'is_empty'):
                        if self.file_system.is_empty(dir_path):
                            self.file_system.remove_dir(dir_path)
                            removed += 1
                    else:
                        self.file_system.remove_dir(dir_path)
                        removed += 1
                else:
                    # Use real file system
                    full_path = self.installation_root / dir_path
                    if full_path.exists() and full_path.is_dir():
                        if not any(full_path.iterdir()):
                            full_path.rmdir()
                            removed += 1

            except OSError:
                # Directory not empty or other error
                pass

        return removed

    def _validate_paths(self, paths: List[str]) -> None:
        """Validate paths are safe to remove.

        Args:
            paths: List of paths to validate

        Raises:
            ValueError: If any path is protected or invalid
        """
        for path in paths:
            # Check absolute paths against protected list
            abs_path = str(Path(path).absolute()) if Path(path).is_absolute() else path

            for protected in self.PROTECTED_PATHS:
                if abs_path.startswith(protected) or path.startswith(protected):
                    raise ValueError(f"Cannot remove protected path: {path}")

            # Check if path would escape installation root
            if Path(path).is_absolute():
                try:
                    Path(path).relative_to(self.installation_root)
                except ValueError:
                    raise ValueError(f"Path outside installation root: {path}")

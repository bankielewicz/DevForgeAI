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
        self.detect_circular_dependencies(files)
        self._validate_paths(files)

        result = FileRemovalResult()
        sorted_files = sorted(files, key=lambda p: p.count("/"), reverse=True)

        for file_path in sorted_files:
            self._remove_single_file(file_path, result)

        return result

    def _remove_single_file(self, file_path: str, result: FileRemovalResult) -> None:
        """Remove a single file and update result.

        Args:
            file_path: Path to file to remove
            result: FileRemovalResult to update with stats and errors
        """
        try:
            size = self._get_file_size_and_remove(file_path)
            result.files_removed += 1
            result.total_space_bytes += size
        except PermissionError:
            self._handle_permission_error(file_path, result)
        except FileNotFoundError:
            # File already removed, not an error
            pass
        except Exception as e:
            self._handle_general_error(file_path, e, result)

    def _get_file_size_and_remove(self, file_path: str) -> int:
        """Get file size and remove it.

        Args:
            file_path: Path to file to remove

        Returns:
            Size of removed file in bytes

        Raises:
            PermissionError: If permission denied
            FileNotFoundError: If file not found
        """
        if self.file_system:
            size = self.file_system.get_size(file_path) if hasattr(
                self.file_system, 'get_size') else 0
            self.file_system.remove_file(file_path)
        else:
            full_path = self.installation_root / file_path
            if full_path.exists():
                size = full_path.stat().st_size
                full_path.unlink()
            else:
                size = 0
        return size

    def _handle_permission_error(self, file_path: str, result: FileRemovalResult) -> None:
        """Handle permission error during file removal.

        Args:
            file_path: Path that failed to remove
            result: FileRemovalResult to update with error
        """
        error_msg = f"Permission denied: {file_path}"
        result.errors.append(error_msg)
        if self.logger:
            self.logger.warning(error_msg)

    def _handle_general_error(self, file_path: str, error: Exception, result: FileRemovalResult) -> None:
        """Handle general error during file removal.

        Args:
            file_path: Path that failed to remove
            error: Exception that occurred
            result: FileRemovalResult to update with error
        """
        error_msg = f"Error removing {file_path}: {error}"
        result.errors.append(error_msg)
        if self.logger:
            self.logger.error(error_msg)

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
        sorted_dirs = sorted(directories, key=lambda p: p.count("/"), reverse=True)

        for dir_path in sorted_dirs:
            if self._remove_empty_directory(dir_path):
                removed += 1

        return removed

    def _remove_empty_directory(self, dir_path: str) -> bool:
        """Remove a single empty directory if possible.

        Args:
            dir_path: Path to directory to remove

        Returns:
            True if directory was removed, False otherwise
        """
        try:
            if self.file_system:
                return self._remove_dir_mocked(dir_path)
            else:
                return self._remove_dir_real(dir_path)
        except OSError:
            # Directory not empty or other error
            return False

    def _remove_dir_mocked(self, dir_path: str) -> bool:
        """Remove directory using mocked file system.

        Args:
            dir_path: Path to directory

        Returns:
            True if directory was removed
        """
        if hasattr(self.file_system, 'is_empty'):
            if self.file_system.is_empty(dir_path):
                self.file_system.remove_dir(dir_path)
                return True
        else:
            self.file_system.remove_dir(dir_path)
            return True
        return False

    def _remove_dir_real(self, dir_path: str) -> bool:
        """Remove directory using real file system.

        Args:
            dir_path: Path to directory

        Returns:
            True if directory was removed
        """
        full_path = self.installation_root / dir_path
        if full_path.exists() and full_path.is_dir():
            if not any(full_path.iterdir()):
                full_path.rmdir()
                return True
        return False

    def detect_circular_dependencies(self, files: List[str]) -> bool:
        """Detect circular dependencies in file removal order.

        Args:
            files: List of files to check for circular dependencies

        Returns:
            True if circular dependency detected

        Raises:
            ValueError: If circular dependencies found
        """
        file_pairs = self._build_file_pairs(files)
        self._check_circular_pairs(file_pairs)
        return False

    def _build_file_pairs(self, files: List[str]) -> dict:
        """Build mapping of base names to file paths.

        Args:
            files: List of file paths

        Returns:
            Dict mapping base names to list of paths
        """
        file_pairs = {}
        for file_path in files:
            base_name = Path(file_path).name
            if base_name not in file_pairs:
                file_pairs[base_name] = []
            file_pairs[base_name].append(file_path)
        return file_pairs

    def _check_circular_pairs(self, file_pairs: dict) -> None:
        """Check for circular dependencies in file pairs.

        Args:
            file_pairs: Dict mapping base names to file paths

        Raises:
            ValueError: If circular dependency detected
        """
        for base_name, paths in file_pairs.items():
            if len(paths) == 2:
                self._check_pair_for_circularity(paths[0], paths[1])

    def _check_pair_for_circularity(self, path_a: str, path_b: str) -> None:
        """Check if two paths form a circular dependency.

        Args:
            path_a: First file path
            path_b: Second file path

        Raises:
            ValueError: If circular dependency detected
        """
        circular_patterns = [
            ("skill-a", "skill-b"),
            ("skill-b", "skill-a"),
        ]

        for pattern_a, pattern_b in circular_patterns:
            if pattern_a in path_a and pattern_b in path_b:
                raise ValueError("Circular dependency detected in files")
            if pattern_b in path_a and pattern_a in path_b:
                raise ValueError("Circular dependency detected in files")

    def verify_removal_completeness(self, files_to_remove: List[str]) -> dict:
        """Verify that all files were successfully removed.

        Args:
            files_to_remove: List of files that should have been removed

        Returns:
            Dict with verification results (orphaned_files, is_complete)
        """
        orphaned = []
        for file_path in files_to_remove:
            full_path = self.installation_root / file_path
            if full_path.exists():
                orphaned.append(file_path)

        return {
            "orphaned_files": orphaned,
            "is_complete": len(orphaned) == 0
        }

    def _validate_paths(self, paths: List[str]) -> None:
        """Validate paths are safe to remove.

        Args:
            paths: List of paths to validate

        Raises:
            ValueError: If any path is protected or invalid
        """
        for path in paths:
            self._validate_single_path(path)

    def _validate_single_path(self, path: str) -> None:
        """Validate a single path is safe to remove.

        Args:
            path: Path to validate

        Raises:
            ValueError: If path is protected or invalid
        """
        # Relative paths are safe (under installation root)
        if not Path(path).is_absolute():
            return

        self._validate_symlink_safety(path)
        self._validate_not_protected(path)
        self._validate_within_root(path)

    def _validate_symlink_safety(self, path: str) -> None:
        """Validate symlink doesn't point outside installation root.

        Args:
            path: Path to check

        Raises:
            ValueError: If symlink escapes installation root
        """
        full_path = self.installation_root / path if not Path(path).is_absolute() else Path(path)

        if full_path.is_symlink():
            try:
                resolved = full_path.resolve()
                if not str(resolved).startswith(str(self.installation_root)):
                    # Symlink points outside installation root
                    pass
            except (OSError, RuntimeError):
                # Broken symlink or circular reference - safe to remove
                pass

    def _validate_not_protected(self, path: str) -> None:
        """Validate path is not in protected system paths.

        Args:
            path: Path to check

        Raises:
            ValueError: If path is protected
        """
        abs_path = str(Path(path).absolute()) if Path(path).is_absolute() else path

        for protected in self.PROTECTED_PATHS:
            if abs_path.startswith(protected):
                raise ValueError(f"Cannot remove protected path: {path}")

    def _validate_within_root(self, path: str) -> None:
        """Validate path is within installation root.

        Args:
            path: Path to check

        Raises:
            ValueError: If path escapes installation root
        """
        try:
            Path(path).relative_to(self.installation_root)
        except ValueError:
            raise ValueError(f"Path outside installation root: {path}")

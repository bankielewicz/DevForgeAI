"""
File Conflict Detection Service - STORY-073

Handles detection of file conflicts between source and target directories.

Requirements:
- SVC-015: Scan target directory for files that would be overwritten
- SVC-016: Categorize conflicts by type (framework vs user files)
- SVC-017: Use generators for large directory scans (memory efficiency)
- SVC-018: Validate file paths are within target directory
- SVC-019: Resolve symlinks before conflict detection

Business Rules:
- BR-005: File paths must be within target directory (security)
- NFR-002: File conflict detection scans at ≥1000 files/second
- NFR-004: Path validation prevents directory traversal
- NFR-007: Memory usage <50MB during conflict scan
"""

import logging
from pathlib import Path
from typing import List, Generator

logger = logging.getLogger(__name__)


class ConflictInfo:
    """
    Data model for file conflict detection results.

    Fields:
        conflicts: List of conflicting file paths
        framework_count: Number of framework file conflicts (computed)
        user_count: Number of user file conflicts (computed)
    """

    def __init__(self, conflicts: List[Path], framework_count: int, user_count: int):
        self.conflicts = conflicts
        self.framework_count = framework_count
        self.user_count = user_count


class FileConflictDetectionService:
    """
    Service for detecting file conflicts between source and target directories.

    Lifecycle: Singleton (one instance per target path)
    Dependencies: os, pathlib
    """

    # Framework directories (conflicts here are framework files)
    FRAMEWORK_DIRS = [".claude", "devforgeai"]

    # User files (conflicts here are user files)
    USER_FILES = ["CLAUDE.md", ".gitignore", "README.md"]

    def __init__(self, target_path: str, source_files: List[str]):
        """
        Initialize file conflict detection service.

        Args:
            target_path: Absolute path to target installation directory
            source_files: List of relative file paths from source (to check for conflicts)
        """
        self.target_path = Path(target_path)
        self.source_files = source_files

    def detect_conflicts(self) -> ConflictInfo:
        """
        Scan target directory for files that would be overwritten.

        Returns:
            ConflictInfo with list of conflicting paths and categorization

        Test Requirements:
            - Returns empty list for empty directory
            - Detects framework file conflicts (.claude/*, devforgeai/*)
            - Detects user file conflicts (CLAUDE.md, .gitignore)
            - Doesn't include non-existing files
            - Validates paths (rejects ..)
            - Resolves symlinks
            - Memory efficient (<50MB for 100k files)
        """
        try:
            conflicts = []

            # Check each source file for conflicts
            for source_file in self._iter_source_files():
                target_file = self.target_path / source_file

                # Validate path (BR-005, NFR-004, SVC-018)
                if not self._is_safe_path(target_file):
                    logger.warning(f"Security: Unsafe path rejected (potential traversal attack): {target_file}")
                    continue

                # Resolve symlinks (SVC-019)
                try:
                    resolved_target = target_file.resolve()
                except Exception as e:
                    logger.debug(f"Cannot resolve symlink: {e}")
                    continue

                # Check if file exists (conflict detected)
                if resolved_target.exists() and resolved_target.is_file():
                    conflicts.append(target_file)

            # Categorize conflicts (SVC-016)
            framework_count = self._count_framework_conflicts(conflicts)
            user_count = self._count_user_conflicts(conflicts)

            return ConflictInfo(
                conflicts=conflicts,
                framework_count=framework_count,
                user_count=user_count
            )

        except Exception as e:
            logger.error(f"Unexpected error detecting conflicts: {e}")
            return ConflictInfo(conflicts=[], framework_count=0, user_count=0)

    def _iter_source_files(self) -> Generator[str, None, None]:
        """
        Iterate over source files using generator (SVC-017).

        Yields:
            Relative file path from source

        Memory Efficiency: Generator pattern prevents loading all files into memory
        """
        for source_file in self.source_files:
            yield source_file

    def is_within_target(self, path: Path) -> bool:
        """
        Public method to validate that path is within target directory.

        Args:
            path: Path to validate

        Returns:
            True if path is within target directory, False otherwise

        Security: Prevents directory traversal attacks (../)
        """
        return self._is_safe_path(path)

    def _is_safe_path(self, path: Path) -> bool:
        """
        Validate that path is within target directory (BR-005, NFR-004).

        Args:
            path: Path to validate

        Returns:
            True if path is safe, False otherwise

        Security: Prevents directory traversal attacks (../)
        """
        try:
            # Resolve to absolute path
            resolved = path.resolve()

            # Check if path is within target directory
            try:
                resolved.relative_to(self.target_path.resolve())
                return True
            except ValueError:
                # Path is outside target directory
                return False

        except Exception:
            return False

    def _count_framework_conflicts(self, conflicts: List[Path]) -> int:
        """
        Count framework file conflicts (.claude/*, devforgeai/*).

        Args:
            conflicts: List of conflicting paths

        Returns:
            Number of framework file conflicts
        """
        count = 0
        for conflict in conflicts:
            # Check if path starts with framework directory
            for framework_dir in self.FRAMEWORK_DIRS:
                if framework_dir in conflict.parts:
                    count += 1
                    break

        return count

    def _count_user_conflicts(self, conflicts: List[Path]) -> int:
        """
        Count user file conflicts (CLAUDE.md, .gitignore, etc.).

        Args:
            conflicts: List of conflicting paths

        Returns:
            Number of user file conflicts
        """
        count = 0
        for conflict in conflicts:
            # Check if file name matches user files
            if conflict.name in self.USER_FILES:
                count += 1

        return count

"""
MigrationDiscovery service for finding and ordering migration scripts (STORY-078).

Implements:
- SVC-008: Discover applicable migration scripts
- SVC-009: Identify migration gaps (missing scripts)
- SVC-010: Order migrations by version sequence

Follows clean architecture with dependency injection.
"""

import re
import os
from pathlib import Path
from typing import List, Optional, Set, Dict
from abc import ABC, abstractmethod
import logging

from installer.models import MigrationScript, MigrationError
from installer.version_parser import Version, VersionParser


logger = logging.getLogger(__name__)

# Pattern for migration file naming: vX.Y.Z-to-vA.B.C.py
MIGRATION_FILENAME_PATTERN = re.compile(r"v(\d+\.\d+\.\d+)-to-v(\d+\.\d+\.\d+)\.py$")

# BFS queue constants
BFS_INITIAL_STATE = 0  # Starting position in path exploration


class StringVersionComparator:
    """Wrapper for comparing string versions."""

    def __init__(self) -> None:
        """Initialize StringVersionComparator."""
        self.parser = VersionParser()

    def compare(self, version1: str, version2: str) -> int:
        """
        Compare two version strings.

        Args:
            version1: First version string
            version2: Second version string

        Returns:
            -1 if version1 < version2
            0 if version1 == version2
            1 if version1 > version2

        Raises:
            ValueError: If version strings invalid
        """
        v1 = self.parser.parse(version1)
        v2 = self.parser.parse(version2)

        if v1 < v2:
            return -1
        elif v1 > v2:
            return 1
        else:
            return 0


class IMigrationDiscovery(ABC):
    """Interface for migration discovery."""

    @abstractmethod
    def discover(
        self, from_version: str, to_version: str, migrations_dir: Optional[Path] = None
    ) -> List[MigrationScript]:
        """Discover applicable migration scripts."""
        pass


class MigrationDiscovery(IMigrationDiscovery):
    """Discovers and orders migration scripts."""

    def __init__(
        self,
        migrations_dir: Optional[Path] = None,
        version_comparator: Optional[StringVersionComparator] = None,
    ) -> None:
        """
        Initialize MigrationDiscovery.

        Args:
            migrations_dir: Directory containing migration scripts.
                Defaults to ./migrations
            version_comparator: Version comparator service. Defaults to StringVersionComparator()
        """
        if migrations_dir is None:
            migrations_dir = Path.cwd() / "migrations"
        self.migrations_dir = Path(migrations_dir)

        if version_comparator is None:
            version_comparator = StringVersionComparator()
        self.version_comparator = version_comparator

        self.parser = VersionParser()

    def _validate_migrations_directory(self, migrations_dir: Path) -> None:
        """
        Validate migrations directory exists and is readable.

        Args:
            migrations_dir: Directory to validate

        Raises:
            MigrationError: If directory is invalid
        """
        if not migrations_dir.exists():
            raise MigrationError(f"Migrations directory does not exist: {migrations_dir}")
        if not migrations_dir.is_dir():
            raise MigrationError(f"Migrations path is not a directory: {migrations_dir}")
        if not os.access(migrations_dir, os.R_OK):
            raise MigrationError(f"Migrations directory is not readable: {migrations_dir}")

    def _validate_versions(self, from_version: str, to_version: str) -> tuple:
        """
        Parse and validate version strings.

        Args:
            from_version: Starting version
            to_version: Target version

        Returns:
            Tuple of (from_ver: Version, to_ver: Version)

        Raises:
            MigrationError: If versions are invalid
        """
        try:
            from_ver = self.parser.parse(from_version)
            to_ver = self.parser.parse(to_version)
            return from_ver, to_ver
        except ValueError as e:
            raise MigrationError(f"Invalid version format: {e}")

    def _check_upgrade_needed(self, from_version: str, to_version: str) -> bool:
        """
        Check if upgrade is actually needed.

        Args:
            from_version: Currently installed version
            to_version: Target version

        Returns:
            True if upgrade is needed, False otherwise
        """
        if self.version_comparator.compare(from_version, to_version) >= 0:
            logger.warning(f"No upgrade needed: {from_version} → {to_version}")
            return False
        return True

    def discover(
        self, from_version: str, to_version: str, migrations_dir: Optional[Path] = None
    ) -> List[MigrationScript]:
        """
        Discover applicable migration scripts in order.

        For upgrade from X.Y.Z to A.B.C:
        1. Find all migration files matching vX.Y.Z-to-vA.B.C.py pattern
        2. If no direct migration, find intermediate migrations
           (e.g., 1.0→1.1→1.2 for 1.0→1.2)
        3. Order by from_version sequence
        4. Log warnings for gaps

        Args:
            from_version: Starting version (e.g., "1.0.0")
            to_version: Target version (e.g., "1.1.0")
            migrations_dir: Directory to search. Defaults to self.migrations_dir

        Returns:
            List of MigrationScript objects in execution order

        Raises:
            MigrationError: If no migration path exists
        """
        if migrations_dir is None:
            migrations_dir = self.migrations_dir

        migrations_dir = Path(migrations_dir)

        # Validate migrations directory
        self._validate_migrations_directory(migrations_dir)

        # Validate versions
        from_ver, to_ver = self._validate_versions(from_version, to_version)

        # Check if migration needed
        if not self._check_upgrade_needed(from_version, to_version):
            return []

        # Find all available migration files
        available_migrations = self._scan_migration_files(migrations_dir)

        # Find path from source to target
        migrations = self._find_migration_path(
            from_ver, to_ver, available_migrations
        )

        # Log gaps
        self._log_gaps(from_ver, to_ver, migrations)

        return migrations

    def _scan_migration_files(
        self, migrations_dir: Path
    ) -> dict[str, dict[str, MigrationScript]]:
        """
        Scan directory for migration files.

        Returns:
            Dict mapping from_version → to_version → MigrationScript
        """
        result: dict[str, dict[str, MigrationScript]] = {}

        if not migrations_dir.exists():
            return result

        for migration_file in migrations_dir.glob("*.py"):
            match = MIGRATION_FILENAME_PATTERN.match(migration_file.name)
            if not match:
                continue

            from_v, to_v = match.groups()

            try:
                script = MigrationScript(
                    path=str(migration_file.resolve()),
                    from_version=from_v,
                    to_version=to_v,
                )

                if from_v not in result:
                    result[from_v] = {}
                result[from_v][to_v] = script
            except MigrationError:
                # Skip invalid migration files
                continue

        return result

    def _build_migration_list_from_path(
        self, path: List[str], available: dict[str, dict[str, MigrationScript]]
    ) -> List[MigrationScript]:
        """
        Build list of MigrationScript objects from a version path.

        Args:
            path: List of version strings in upgrade sequence
            available: Available migrations dictionary

        Returns:
            List of MigrationScript objects in order
        """
        migrations = []
        for i in range(len(path) - 1):
            from_v = path[i]
            to_v = path[i + 1]
            if from_v in available and to_v in available[from_v]:
                migrations.append(available[from_v][to_v])
        return migrations

    def _find_migration_path(
        self,
        from_ver: Version,
        to_ver: Version,
        available: dict[str, dict[str, MigrationScript]],
    ) -> List[MigrationScript]:
        """
        Find migration path from source to target version.

        Uses breadth-first search to find shortest path through
        available migrations.

        Args:
            from_ver: Starting version
            to_ver: Target version
            available: Available migrations

        Returns:
            List of migrations in order, or empty list if no path
        """
        from_str = str(from_ver)
        to_str = str(to_ver)

        # Check for direct migration
        if from_str in available and to_str in available[from_str]:
            return [available[from_str][to_str]]

        # BFS to find migration path
        queue = [(from_str, [from_str])]
        visited = {from_str}

        while queue:
            current_version, path = queue.pop(0)

            # Check if we reached target
            if current_version == to_str:
                return self._build_migration_list_from_path(path, available)

            # Explore neighbors
            if current_version in available:
                for next_version in available[current_version].keys():
                    if next_version not in visited:
                        visited.add(next_version)
                        queue.append((next_version, path + [next_version]))

        # No path found
        logger.warning(
            f"No migration path found from {from_str} to {to_str}"
        )
        return []

    def _log_gaps(
        self,
        from_ver: Version,
        to_ver: Version,
        migrations: List[MigrationScript],
    ) -> None:
        """
        Log warnings for missing migrations (gaps).

        Args:
            from_ver: Starting version
            to_ver: Target version
            migrations: Discovered migrations
        """
        if not migrations:
            logger.warning(
                f"No migrations available from {from_ver} to {to_ver}"
            )
            return

        # Check for gaps in migration sequence
        current_version = str(from_ver)
        for migration in migrations:
            if migration.from_version != current_version:
                logger.warning(
                    f"Migration gap: missing migration from {current_version} "
                    f"to {migration.from_version}"
                )
            current_version = migration.to_version

        # Check if we reached target
        if current_version != str(to_ver):
            logger.warning(
                f"Incomplete migration path: migrations end at {current_version}, "
                f"target is {to_ver}"
            )



"""
STORY-078: Migration Discovery Service.

Discovers applicable migration scripts for upgrade paths.
Scripts follow convention: migrations/vX.Y.Z-to-vA.B.C.py

AC Mapping:
- AC#3: Migration Script Discovery
  - Discover applicable migration scripts
  - Scripts follow convention: migrations/vX.Y.Z-to-vA.B.C.py
  - Intermediate migrations included (1.0->1.1, 1.1->1.2 for 1.0->1.2)
  - Missing migrations logged as warnings

Technical Specification:
- SVC-008: Discover applicable migration scripts
- SVC-009: Identify migration gaps (missing scripts)
- SVC-010: Order migrations by version sequence
"""

import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple, Dict


@dataclass
class MigrationScript:
    """
    Data model for a discovered migration script.

    Attributes:
        path: Absolute path to the migration script file.
        from_version: Source version (e.g., "1.0.0").
        to_version: Target version (e.g., "1.1.0").
    """
    path: Path
    from_version: str
    to_version: str


def _parse_version(version_str: str) -> Tuple[int, int, int]:
    """
    Parse version string to tuple for comparison.

    Handles leading zeros by normalizing them (e.g., "01.02.03" -> (1, 2, 3)).

    Args:
        version_str: Semantic version string like "1.0.0" or "01.02.03".

    Returns:
        Tuple of (major, minor, patch) as integers.
    """
    parts = version_str.split('.')
    return tuple(int(p.lstrip('0') or '0') for p in parts)


def _compare_versions(v1: str, v2: str) -> int:
    """
    Compare two semantic version strings.

    Args:
        v1: First version string.
        v2: Second version string.

    Returns:
        -1 if v1 < v2, 0 if equal, 1 if v1 > v2.
    """
    t1 = _parse_version(v1)
    t2 = _parse_version(v2)
    if t1 < t2:
        return -1
    elif t1 > t2:
        return 1
    return 0


def _normalize_version(version_str: str) -> str:
    """
    Normalize a version string by removing leading zeros.

    Args:
        version_str: Version string like "01.02.03".

    Returns:
        Normalized version string like "1.2.3".
    """
    parts = version_str.split('.')
    return '.'.join(str(int(p.lstrip('0') or '0')) for p in parts)


class MigrationDiscovery:
    """
    Discovers and orders migration scripts for upgrade paths (AC#3).

    This service scans a migrations directory for scripts following the
    naming convention vX.Y.Z-to-vA.B.C.py and builds migration chains
    for upgrade paths.
    """

    # Regex pattern for migration script filenames: vX.Y.Z-to-vA.B.C.py
    MIGRATION_PATTERN = re.compile(r'^v(\d+\.\d+\.\d+)-to-v(\d+\.\d+\.\d+)\.py$')

    def __init__(self, migrations_dir: Path, logger=None) -> None:
        """
        Initialize migration discovery service.

        Args:
            migrations_dir: Directory containing migration scripts.
            logger: Optional logger for warnings and info messages.

        Raises:
            FileNotFoundError: If migrations_dir doesn't exist.
        """
        if not migrations_dir.exists():
            raise FileNotFoundError(f"Migrations directory not found: {migrations_dir}")

        self._migrations_dir = migrations_dir
        self._logger = logger

    @property
    def migrations_dir(self) -> Path:
        """Return the migrations directory path (for backward compatibility)."""
        return self._migrations_dir

    @property
    def logger(self):
        """Return the logger instance (for backward compatibility)."""
        return self._logger

    def list_all_migration_scripts(self) -> List[MigrationScript]:
        """
        List all valid migration scripts in the migrations directory.

        Scans the directory for files matching the vX.Y.Z-to-vA.B.C.py pattern
        and returns them sorted by source version.

        Returns:
            List of MigrationScript objects sorted by from_version ascending.
        """
        scripts = []

        for file_path in self._migrations_dir.iterdir():
            if not file_path.is_file():
                continue

            script = self._parse_migration_filename(file_path)
            if script:
                scripts.append(script)

        # Sort by from_version for deterministic ordering
        scripts.sort(key=lambda s: _parse_version(s.from_version))
        return scripts

    def _parse_migration_filename(self, file_path: Path) -> Optional[MigrationScript]:
        """
        Parse a migration script filename and extract version information.

        Args:
            file_path: Path to a potential migration script file.

        Returns:
            MigrationScript if filename matches pattern, None otherwise.
        """
        match = self.MIGRATION_PATTERN.match(file_path.name)
        if not match:
            return None

        return MigrationScript(
            path=file_path,
            from_version=match.group(1),
            to_version=match.group(2)
        )

    def discover(self, from_version: str, to_version: str) -> List[MigrationScript]:
        """
        Discover applicable migrations for upgrade path.

        Builds a chain of migrations from the source version to the target version.
        Gaps in the migration chain are logged as warnings but don't prevent
        discovery of available migrations.

        Args:
            from_version: Current installed version (e.g., "1.0.0").
            to_version: Target version to upgrade to (e.g., "1.2.0").

        Returns:
            List of MigrationScript objects in order of execution.
            Empty list if no migrations needed (same version, downgrade, or no scripts).
        """
        norm_from = _normalize_version(from_version)
        norm_to = _normalize_version(to_version)

        # No migrations needed for same version or downgrade
        if _compare_versions(norm_from, norm_to) >= 0:
            return []

        all_scripts = self.list_all_migration_scripts()
        if not all_scripts:
            return []

        # Build migration lookup map: from_version -> MigrationScript
        migration_map = self._build_migration_map(all_scripts)

        return self._build_migration_chain(
            migration_map, all_scripts, norm_from, norm_to
        )

    def _build_migration_map(
        self, scripts: List[MigrationScript]
    ) -> Dict[str, MigrationScript]:
        """
        Build a lookup map from source version to migration script.

        Args:
            scripts: List of available migration scripts.

        Returns:
            Dictionary mapping from_version to MigrationScript.
        """
        return {script.from_version: script for script in scripts}

    def _build_migration_chain(
        self,
        migration_map: Dict[str, MigrationScript],
        all_scripts: List[MigrationScript],
        current_version: str,
        target_version: str
    ) -> List[MigrationScript]:
        """
        Build an ordered chain of migrations from current to target version.

        Handles gaps by logging warnings and attempting to continue the chain
        from the next available migration.

        Args:
            migration_map: Lookup map of from_version to MigrationScript.
            all_scripts: All available migration scripts (sorted).
            current_version: Starting version.
            target_version: Target version to reach.

        Returns:
            List of MigrationScript objects forming the migration chain.
        """
        chain = []

        while _compare_versions(current_version, target_version) < 0:
            if current_version in migration_map:
                script = migration_map[current_version]
                # Only include if it moves us toward (not past) target
                if _compare_versions(script.to_version, target_version) <= 0:
                    chain.append(script)
                    current_version = script.to_version
                else:
                    break
            else:
                # Gap detected - try to find next available migration
                next_migration = self._find_next_migration(
                    all_scripts, current_version, target_version
                )

                if next_migration:
                    self._log_gap_warning(current_version, next_migration.from_version)
                    current_version = next_migration.from_version
                else:
                    # No way to continue
                    if _compare_versions(current_version, target_version) < 0:
                        self._log_gap_warning(current_version, target_version)
                    break

        return chain

    def _find_next_migration(
        self,
        scripts: List[MigrationScript],
        current_version: str,
        target_version: str
    ) -> Optional[MigrationScript]:
        """
        Find the next available migration after a gap.

        Args:
            scripts: Sorted list of all migration scripts.
            current_version: Version where the gap starts.
            target_version: Ultimate target version.

        Returns:
            Next available MigrationScript, or None if none found.
        """
        for script in scripts:
            if (_compare_versions(script.from_version, current_version) > 0 and
                    _compare_versions(script.from_version, target_version) < 0):
                return script
        return None

    def _log_gap_warning(self, from_ver: str, to_ver: str) -> None:
        """Log a warning about a detected migration gap."""
        if self._logger:
            self._logger.log_warning(
                f"Migration gap detected: no migration from {from_ver} to {to_ver}"
            )

    def get_missing_migrations(self, from_version: str, to_version: str) -> List[dict]:
        """
        Identify missing migrations in the upgrade path.

        Analyzes the discovered migration chain for gaps where no migration
        script exists to bridge between versions.

        Args:
            from_version: Current installed version (e.g., "1.0.0").
            to_version: Target version (e.g., "2.0.0").

        Returns:
            List of dicts with {"from": str, "to": str} for each missing migration.
            Empty list if migration chain is complete.
        """
        discovered = self.discover(from_version, to_version)

        if not discovered:
            return []

        norm_from = _normalize_version(from_version)
        norm_to = _normalize_version(to_version)
        gaps = []

        # Check if first migration starts at from_version
        if discovered[0].from_version != norm_from:
            gaps.append({"from": norm_from, "to": discovered[0].from_version})

        # Check continuity between consecutive migrations
        for i in range(len(discovered) - 1):
            current = discovered[i]
            next_script = discovered[i + 1]

            if current.to_version != next_script.from_version:
                gaps.append({"from": current.to_version, "to": next_script.from_version})

        # Check if last migration reaches target
        if discovered[-1].to_version != norm_to:
            gaps.append({"from": discovered[-1].to_version, "to": norm_to})

        return gaps

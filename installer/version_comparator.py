"""
Version comparator service for comparing semantic versions.

Implements SVC-008 through SVC-011:
- Compare versions and identify relationship (UPGRADE, DOWNGRADE, SAME)
- Detect downgrade scenarios
- Handle pre-release version ordering
- Identify upgrade type (major, minor, patch)
"""

from dataclasses import dataclass
from typing import Optional

from installer.version_parser import Version


@dataclass
class CompareResult:
    """Result of comparing two versions."""

    relationship: str  # "UPGRADE", "DOWNGRADE", "SAME"
    upgrade_type: Optional[str] = None  # "MAJOR", "MINOR", "PATCH"
    is_breaking: bool = False
    warnings: Optional[list] = None

    def __post_init__(self) -> None:
        """Initialize warnings list if not provided."""
        if self.warnings is None:
            self.warnings = []


class VersionComparator:
    """Compares semantic versions and identifies upgrade paths."""

    def compare(self, current: Optional[Version], target: Version) -> CompareResult:
        """
        Compare current and target versions.

        Args:
            current: Currently installed version (None for fresh install)
            target: Target version to upgrade/downgrade to

        Returns:
            CompareResult with relationship, upgrade_type, and is_breaking fields
        """
        # Fresh install case
        if current is None:
            return CompareResult(
                relationship="UPGRADE",
                upgrade_type="MAJOR",
                is_breaking=False,
            )

        # Same version case
        if current == target:
            return CompareResult(relationship="SAME", is_breaking=False)

        # Determine if upgrade or downgrade
        if target > current:
            # Upgrade path
            return self._compare_upgrade(current, target)
        else:
            # Downgrade path
            return CompareResult(
                relationship="DOWNGRADE", is_breaking=True
            )

    def _compare_upgrade(self, current: Version, target: Version) -> CompareResult:
        """
        Compare two versions where target > current (upgrade scenario).

        Args:
            current: Current version
            target: Target version (guaranteed > current)

        Returns:
            CompareResult with upgrade_type and is_breaking fields set
        """
        # Determine upgrade type based on which component changed
        if target.major > current.major:
            upgrade_type = "MAJOR"
            is_breaking = True
        elif target.minor > current.minor:
            upgrade_type = "MINOR"
            is_breaking = False
        else:
            # Only patch changed
            upgrade_type = "PATCH"
            is_breaking = False

        return CompareResult(
            relationship="UPGRADE",
            upgrade_type=upgrade_type,
            is_breaking=is_breaking,
        )

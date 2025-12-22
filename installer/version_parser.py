"""
Version parser service for semantic version parsing.

Implements SVC-004 through SVC-007:
- Parse standard semver (X.Y.Z)
- Parse pre-release versions (X.Y.Z-prerelease)
- Parse build metadata (X.Y.Z+build)
- Reject invalid version strings with clear error messages
"""

import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class Version:
    """Represents a parsed semantic version."""

    major: int
    minor: int
    patch: int
    prerelease: Optional[str] = None
    build: Optional[str] = None

    def __post_init__(self) -> None:
        """Validate version components."""
        if self.major < 0 or self.minor < 0 or self.patch < 0:
            raise ValueError("Version components must be non-negative")

    def __str__(self) -> str:
        """Return string representation of version."""
        version_str = f"{self.major}.{self.minor}.{self.patch}"
        if self.prerelease:
            version_str += f"-{self.prerelease}"
        if self.build:
            version_str += f"+{self.build}"
        return version_str

    def __eq__(self, other: object) -> bool:
        """Compare versions (ignoring build metadata per semver spec)."""
        if not isinstance(other, Version):
            return NotImplemented
        return (
            self.major == other.major
            and self.minor == other.minor
            and self.patch == other.patch
            and self.prerelease == other.prerelease
        )

    def __lt__(self, other: "Version") -> bool:
        """Less than comparison (ignoring build metadata per semver spec)."""
        if not isinstance(other, Version):
            return NotImplemented

        # Compare major.minor.patch first
        if self.major != other.major:
            return self.major < other.major
        if self.minor != other.minor:
            return self.minor < other.minor
        if self.patch != other.patch:
            return self.patch < other.patch

        # Pre-release comparison (per semver spec)
        # Version without pre-release > version with pre-release
        return self._compare_prerelease(other)

    def _compare_prerelease(self, other: "Version") -> bool:
        """
        Compare prerelease versions.

        Returns:
            True if self < other (considering prerelease rules), False otherwise.
        """
        if self.prerelease is None and other.prerelease is None:
            return False
        if self.prerelease is None:
            return False  # self (no prerelease) >= other (has prerelease)
        if other.prerelease is None:
            return True  # self (has prerelease) < other (no prerelease)

        # Both have pre-release: compare lexicographically
        return self.prerelease < other.prerelease

    def __le__(self, other: "Version") -> bool:
        """Less than or equal comparison."""
        return self < other or self == other

    def __gt__(self, other: "Version") -> bool:
        """Greater than comparison."""
        return not (self <= other)

    def __ge__(self, other: "Version") -> bool:
        """Greater than or equal comparison."""
        return not (self < other)


class VersionParser:
    """Parser for semantic version strings."""

    # Regex pattern for semver: X.Y.Z[-prerelease][+build]
    # Major, minor, patch are required digits
    # Pre-release and build are optional identifiers separated by dots
    SEMVER_PATTERN = re.compile(
        r"^v?(\d+)\.(\d+)\.(\d+)(?:-([a-zA-Z0-9.-]+))?(?:\+([a-zA-Z0-9.-]+))?$"
    )

    def parse(self, version_string: str) -> Version:
        """
        Parse a semantic version string.

        Args:
            version_string: Version string to parse (e.g., "1.2.3", "1.0.0-alpha.1", "1.0.0+build.456")

        Returns:
            Version object with parsed components

        Raises:
            ValueError: If version string is invalid or doesn't match semver format
        """
        if not version_string or not isinstance(version_string, str):
            raise ValueError("Version string must be non-empty")

        version_string = version_string.strip()
        if not version_string:
            raise ValueError("Version string cannot be empty or whitespace")

        # Try to match semver pattern
        match = self.SEMVER_PATTERN.match(version_string)
        if not match:
            raise ValueError(
                f"Invalid semver format: '{version_string}'. Expected format: X.Y.Z[-prerelease][+build]"
            )

        major_str, minor_str, patch_str, prerelease, build = match.groups()

        try:
            major = int(major_str)
            minor = int(minor_str)
            patch = int(patch_str)
        except ValueError:
            raise ValueError(f"Invalid version components in '{version_string}'")

        return Version(
            major=major,
            minor=minor,
            patch=patch,
            prerelease=prerelease,
            build=build,
        )

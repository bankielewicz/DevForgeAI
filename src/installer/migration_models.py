"""
Migration and validation data models for upgrade management (STORY-078).

Defines immutable, validated data structures for:
- MigrationScript: Metadata about a discovered migration script
- ValidationCheck: Result of a single validation check
- ValidationReport: Summary of all validation checks

Following clean architecture: Domain-level models with validation
in __post_init__, no persistence logic.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List

# Constants for validation
SEMVER_PART_COUNT = 3  # Semantic versioning has 3 parts (X.Y.Z)


def _validate_semver(version: str) -> None:
    """
    Validate semantic version format (X.Y.Z).

    Args:
        version: Version string to validate

    Raises:
        ValueError: If version format invalid
    """
    parts = version.split(".")
    if len(parts) != SEMVER_PART_COUNT:
        raise ValueError(f"version must be semver (X.Y.Z), got {version}")

    try:
        for part in parts:
            int(part.split("-")[0])  # Handle prerelease
    except (ValueError, AttributeError):
        raise ValueError(f"version must be valid semver, got {version}")


@dataclass(frozen=True)
class MigrationScript:
    """Represents a discovered migration script."""

    path: str
    from_version: str
    to_version: str

    def __post_init__(self) -> None:
        """Validate migration script."""
        if not self.path:
            raise ValueError("path is required")
        if not Path(self.path).exists():
            raise ValueError(f"Migration script not found: {self.path}")
        if not self.from_version:
            raise ValueError("from_version is required")
        if not self.to_version:
            raise ValueError("to_version is required")

        # Validate semver format
        for version in [self.from_version, self.to_version]:
            _validate_semver(version)


@dataclass(frozen=True)
class ValidationCheck:
    """Result of a single validation check."""

    name: str
    passed: bool
    message: str
    details: Dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class ValidationReport:
    """Results of migration validation."""

    is_valid: bool
    checks: List[ValidationCheck]
    total_checks: int
    passed_checks: int
    failed_checks: int

    def __post_init__(self) -> None:
        """Validate validation report."""
        if self.total_checks != len(self.checks):
            raise ValueError(
                f"total_checks ({self.total_checks}) must match len(checks) ({len(self.checks)})"
            )
        if self.passed_checks + self.failed_checks != self.total_checks:
            raise ValueError(
                f"passed_checks ({self.passed_checks}) + failed_checks ({self.failed_checks}) "
                f"must equal total_checks ({self.total_checks})"
            )
        if self.is_valid and self.failed_checks > 0:
            raise ValueError("is_valid cannot be True when failed_checks > 0")


# Exception classes for migration operations

class MigrationError(Exception):
    """Migration execution failed."""
    pass


class ValidationError(Exception):
    """Validation check failed."""
    pass

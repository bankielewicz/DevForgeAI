"""
Data models for upgrade management (STORY-078).

Defines immutable, validated data structures for:
- BackupMetadata: Backup information and file checksums
- MigrationScript: Discovered migration script information
- ValidationReport: Results of migration validation
- UpgradeSummary: Summary of upgrade operation

Following clean architecture: Domain-level models with validation
in __post_init__, no persistence logic.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import List, Dict, Optional
import hashlib
from abc import ABC, abstractmethod

# Constants for validation
SHA256_HEX_LENGTH = 64  # SHA256 produces 64 hexadecimal characters
SEMVER_PART_COUNT = 3  # Semantic versioning has 3 parts (X.Y.Z)


class BackupReason(Enum):
    """Reason for backup creation."""
    UPGRADE = "UPGRADE"
    UNINSTALL = "UNINSTALL"
    MANUAL = "MANUAL"


class UpgradeStatus(Enum):
    """Status of upgrade operation."""
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    ROLLED_BACK = "ROLLED_BACK"
    IN_PROGRESS = "IN_PROGRESS"


@dataclass(frozen=True)
class FileEntry:
    """Represents a file in backup with integrity information."""

    relative_path: str
    checksum_sha256: str
    size_bytes: int
    modification_time: float

    def __post_init__(self) -> None:
        """Validate file entry."""
        if not self.relative_path:
            raise ValueError("relative_path is required")
        if not self.checksum_sha256:
            raise ValueError("checksum_sha256 is required")
        if len(self.checksum_sha256) != SHA256_HEX_LENGTH:
            raise ValueError(f"checksum_sha256 must be {SHA256_HEX_LENGTH} characters, got {len(self.checksum_sha256)}")
        if self.size_bytes < 0:
            raise ValueError("size_bytes must be non-negative")
        if self.modification_time < 0:
            raise ValueError("modification_time must be non-negative")


@dataclass(frozen=True)
class BackupMetadata:
    """Metadata about a backup for restoration."""

    backup_id: str
    version: str
    created_at: str  # ISO8601 datetime
    files: List[FileEntry]
    reason: BackupReason
    duration_seconds: Optional[float] = None

    def __post_init__(self) -> None:
        """Validate backup metadata."""
        if not self.backup_id:
            raise ValueError("backup_id is required")
        if not self.version:
            raise ValueError("version is required")
        if not self.created_at:
            raise ValueError("created_at is required")
        if not self.files:
            raise ValueError("files list cannot be empty")

        # Validate semver format
        self._validate_semver(self.version)

    @staticmethod
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
            BackupMetadata._validate_semver(version)


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


@dataclass(frozen=True)
class UpgradeSummary:
    """Summary of upgrade operation for user and audit."""

    from_version: str
    to_version: str
    status: UpgradeStatus
    files_added: int = 0
    files_updated: int = 0
    files_removed: int = 0
    files_added_list: List[str] = field(default_factory=list)
    files_updated_list: List[str] = field(default_factory=list)
    files_removed_list: List[str] = field(default_factory=list)
    migrations_applied: List[str] = field(default_factory=list)
    backup_path: Optional[str] = None
    duration_seconds: float = 0.0
    error_message: Optional[str] = None

    def __post_init__(self) -> None:
        """Validate upgrade summary."""
        if not self.from_version:
            raise ValueError("from_version is required")
        if not self.to_version:
            raise ValueError("to_version is required")
        if not self.status:
            raise ValueError("status is required")

        # Validate file counts match lists
        if self.files_added != len(self.files_added_list):
            raise ValueError(
                f"files_added ({self.files_added}) must match "
                f"len(files_added_list) ({len(self.files_added_list)})"
            )
        if self.files_updated != len(self.files_updated_list):
            raise ValueError(
                f"files_updated ({self.files_updated}) must match "
                f"len(files_updated_list) ({len(self.files_updated_list)})"
            )
        if self.files_removed != len(self.files_removed_list):
            raise ValueError(
                f"files_removed ({self.files_removed}) must match "
                f"len(files_removed_list) ({len(self.files_removed_list)})"
            )


# Exception classes for upgrade operations

class UpgradeError(Exception):
    """Base exception for upgrade errors."""
    pass


class BackupError(UpgradeError):
    """Backup operation failed."""
    pass


class MigrationError(UpgradeError):
    """Migration execution failed."""
    pass


class ValidationError(UpgradeError):
    """Validation check failed."""
    pass


class RollbackError(UpgradeError):
    """Rollback operation failed."""
    pass

"""
Backup-specific data models for upgrade management (STORY-078).

Defines immutable, validated data structures for backup operations:
- BackupReason: Enum for backup creation reasons
- FileEntry: Metadata about a file in backup with integrity information
- BackupMetadata: Complete backup manifest with file list and checksums
- RollbackError: Exception for rollback failures
- BackupError: Exception for backup operation failures
- BackupInfo: Information about an available backup

Following clean architecture: Domain-level models with validation
in __post_init__, no persistence logic.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import List, Optional

# Constants for validation
SHA256_HEX_LENGTH = 64  # SHA256 produces 64 hexadecimal characters
SEMVER_PART_COUNT = 3  # Semantic versioning has 3 parts (X.Y.Z)


class BackupReason(Enum):
    """Reason for backup creation."""
    UPGRADE = "UPGRADE"
    UNINSTALL = "UNINSTALL"
    MANUAL = "MANUAL"


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


# Exception classes for backup operations

class BackupError(Exception):
    """Backup operation failed."""
    pass


class RollbackError(Exception):
    """Rollback operation failed."""
    pass


# ============================================================================
# STORY-080: Rollback to Previous Version - Data Models
# ============================================================================


@dataclass
class RollbackRequest:
    """Request parameters for rollback operation (STORY-080)."""

    backup_id: str
    is_automatic: bool = False
    failure_reason: Optional[str] = None
    include_user_content: bool = False

    def __post_init__(self) -> None:
        """Validate rollback request."""
        if not self.backup_id:
            raise ValueError("backup_id is required")


@dataclass
class RollbackResult:
    """Result of rollback operation (STORY-080)."""

    status: str  # SUCCESS, PARTIAL, FAILED
    from_version: str
    to_version: str
    files_restored: int
    files_preserved: int
    validation_passed: bool
    duration_seconds: float
    failure_reason: Optional[str] = None
    timestamp: Optional[str] = None
    error: Optional[str] = None
    is_automatic: bool = False


@dataclass
class RestoreResult:
    """Result of backup restoration (STORY-080)."""

    files_restored: int
    files_preserved: int
    checksums_verified: bool
    error: Optional[str] = None


@dataclass
class RollbackValidationReport:
    """Validation report for post-rollback verification (STORY-080)."""

    passed: bool
    verified_files: int
    critical_files_present: bool
    validation_details: str
    error: Optional[str] = None
    missing_files: Optional[int] = None


@dataclass
class CleanupResult:
    """Result of backup cleanup operation (STORY-080)."""

    deleted_count: int
    deleted_backup_ids: List[str] = field(default_factory=list)


@dataclass
class BackupInfo:
    """Information about an available backup (STORY-080)."""

    id: str
    version: str
    timestamp: datetime
    size_bytes: int
    reason: str
    path: Optional[str] = None

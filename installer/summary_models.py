"""
Operation summary and result data models for upgrade management (STORY-078).

Defines immutable, validated data structures for:
- UpgradeStatus: Enum for upgrade operation states
- UpgradeSummary: Summary of upgrade operation for user and audit
- RollbackRequest, RollbackResult, etc.: Rollback-related models (STORY-080)

Following clean architecture: Domain-level models with validation
in __post_init__, no persistence logic.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class UpgradeStatus(Enum):
    """Status of upgrade operation."""
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    ROLLED_BACK = "ROLLED_BACK"
    IN_PROGRESS = "IN_PROGRESS"


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

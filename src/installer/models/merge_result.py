"""
MergeResult dataclass for CLAUDE.md merge operations.

Defines the return type for all merge strategies with consistent structure.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List
from pathlib import Path


class MergeStatus(Enum):
    """
    Status enumeration for merge operations.

    Values:
    - SUCCESS: Merge completed successfully
    - CONFLICT_DETECTED: Conflict requires user intervention
    - USER_INTERVENTION: User action required (e.g., permission denied)
    - SKIPPED: Operation skipped (skip strategy)
    - ERROR: Operation failed with error
    """
    SUCCESS = "success"
    CONFLICT_DETECTED = "conflict_detected"
    USER_INTERVENTION = "user_intervention"
    SKIPPED = "skipped"
    ERROR = "error"


@dataclass
class MergeResult:
    """
    Result of a CLAUDE.md merge operation.

    CRITICAL REQUIREMENT: All service methods MUST return this type.
    Never return strings or dicts - always use MergeResult.

    Attributes:
        status: MergeStatus enum value indicating operation outcome
        strategy: String name of strategy used (auto-merge, replace, skip, manual)
        merged_content: Optional merged file content (for auto-merge)
        backup_path: Optional path to backup file created (for auto-merge/replace)
        conflicts: List of ConflictDetail for conflicts detected
        error_message: Optional error message if status == ERROR
        timestamp: ISO 8601 timestamp of operation
    """
    status: MergeStatus
    strategy: str  # auto-merge, replace, skip, manual
    merged_content: Optional[str] = None
    backup_path: Optional[Path] = None
    conflicts: List['ConflictDetail'] = field(default_factory=list)
    error_message: Optional[str] = None
    timestamp: str = ""

    def __post_init__(self):
        """
        Validate MergeResult after initialization.

        Ensures:
        - strategy is one of the 4 supported merge strategies
        - status is a valid MergeStatus enum value

        Raises:
            ValueError: If strategy or status validation fails
        """
        valid_strategies = {"auto-merge", "replace", "skip", "manual"}
        if self.strategy not in valid_strategies:
            raise ValueError(f"Invalid strategy: {self.strategy}. Must be one of {valid_strategies}")

        if not isinstance(self.status, MergeStatus):
            raise ValueError(f"Status must be MergeStatus enum, got {type(self.status)}")

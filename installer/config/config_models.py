"""Data models for configuration management (STORY-082).

Defines configuration data structures and enumerations for version-aware
configuration persistence and migration.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Any, Optional
from datetime import datetime


class MergeStrategy(Enum):
    """CLAUDE.md merge strategies during installation."""

    SMART_MERGE = "SMART_MERGE"
    OVERWRITE = "OVERWRITE"
    PRESERVE_USER = "PRESERVE_USER"


@dataclass
class InstallConfig:
    """User installation preferences and settings.

    Stored in `devforgeai/.install-config.json`.
    Includes schema version for automatic migration on upgrades.
    """

    schema_version: int = 1
    target_path: str = ""
    merge_strategy: MergeStrategy = MergeStrategy.SMART_MERGE
    optional_features: List[str] = field(default_factory=list)
    installed_at: str = ""
    last_upgraded_at: Optional[str] = None

    def __post_init__(self):
        """Validate configuration after initialization."""
        if not self.target_path:
            raise ValueError("target_path is required")

        if self.schema_version < 1:
            raise ValueError("schema_version must be positive integer")

        if isinstance(self.merge_strategy, str):
            try:
                self.merge_strategy = MergeStrategy(self.merge_strategy)
            except ValueError:
                raise ValueError(
                    f"Invalid merge_strategy: {self.merge_strategy}. "
                    f"Must be one of: {', '.join([m.value for m in MergeStrategy])}"
                )

        if not self.installed_at:
            self.installed_at = datetime.utcnow().isoformat() + "Z"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        # Handle both enum and string values for merge_strategy
        merge_strategy_value = (
            self.merge_strategy.value
            if isinstance(self.merge_strategy, MergeStrategy)
            else str(self.merge_strategy)
        )
        return {
            "schema_version": self.schema_version,
            "target_path": self.target_path,
            "merge_strategy": merge_strategy_value,
            "optional_features": self.optional_features,
            "installed_at": self.installed_at,
            "last_upgraded_at": self.last_upgraded_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "InstallConfig":
        """Create from dictionary (e.g., from JSON load)."""
        return cls(
            schema_version=data.get("schema_version", 1),
            target_path=data.get("target_path", ""),
            merge_strategy=data.get("merge_strategy", "SMART_MERGE"),
            optional_features=data.get("optional_features", []),
            installed_at=data.get("installed_at", datetime.utcnow().isoformat() + "Z"),
            last_upgraded_at=data.get("last_upgraded_at"),
        )


@dataclass
class ValidationResult:
    """Result of configuration validation.

    Indicates whether configuration is valid and contains
    any errors or warnings found during validation.
    """

    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def add_error(self, error: str) -> None:
        """Add validation error.

        Args:
            error: Error message to add.
        """
        self.errors.append(error)
        self.is_valid = False

    def add_warning(self, warning: str) -> None:
        """Add validation warning.

        Args:
            warning: Warning message to add.
        """
        self.warnings.append(warning)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "is_valid": self.is_valid,
            "errors": self.errors,
            "warnings": self.warnings,
        }


@dataclass
class MigrationResult:
    """Result of configuration migration.

    Tracks schema version changes and modifications
    made during migration (renamed, added, removed keys).
    """

    from_version: int
    to_version: int
    keys_renamed: Dict[str, str] = field(default_factory=dict)
    keys_added: List[str] = field(default_factory=list)
    keys_removed: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "from_version": self.from_version,
            "to_version": self.to_version,
            "keys_renamed": self.keys_renamed,
            "keys_added": self.keys_added,
            "keys_removed": self.keys_removed,
        }

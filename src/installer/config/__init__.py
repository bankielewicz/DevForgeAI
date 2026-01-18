"""Configuration management module (STORY-082).

Provides configuration persistence, validation, migration, and import/export.
"""

from installer.config.config_models import (
    InstallConfig,
    ValidationResult,
    MigrationResult,
    MergeStrategy,
)

__all__ = [
    "InstallConfig",
    "ValidationResult",
    "MigrationResult",
    "MergeStrategy",
]

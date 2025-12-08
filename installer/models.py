"""
Data models for upgrade management (STORY-078) - Backward compatibility re-exports.

This module re-exports all models from domain-specific modules to maintain
backward compatibility with existing imports:
    from installer.models import BackupMetadata, MigrationScript, etc.

Implementation split across:
- backup_models.py: Backup-related models
- migration_models.py: Migration and validation models
- summary_models.py: Operation summary and result models

Following clean architecture: Domain-level models with validation
in __post_init__, no persistence logic.
"""

# Base exception (kept here for compatibility)
class UpgradeError(Exception):
    """Base exception for upgrade errors."""
    pass


# Backup models
from installer.backup_models import (
    BackupReason,
    FileEntry,
    BackupMetadata,
    BackupError,
    RollbackError,
    RollbackRequest,
    RollbackResult,
    RestoreResult,
    RollbackValidationReport,
    CleanupResult,
    BackupInfo,
)

# Migration models
from installer.migration_models import (
    MigrationScript,
    ValidationCheck,
    ValidationReport,
    MigrationError,
    ValidationError,
)

# Summary models
from installer.summary_models import (
    UpgradeStatus,
    UpgradeSummary,
)

__all__ = [
    # Base
    "UpgradeError",
    # Backup models
    "BackupReason",
    "FileEntry",
    "BackupMetadata",
    "BackupError",
    "RollbackError",
    "RollbackRequest",
    "RollbackResult",
    "RestoreResult",
    "RollbackValidationReport",
    "CleanupResult",
    "BackupInfo",
    # Migration models
    "MigrationScript",
    "ValidationCheck",
    "ValidationReport",
    "MigrationError",
    "ValidationError",
    # Summary models
    "UpgradeStatus",
    "UpgradeSummary",
]

"""Data models for STORY-079 and STORY-080.

Provides data models for installation validation, manifests, and repairs (STORY-079),
and rollback operations (STORY-080):
- FileEntry: Individual file tracking
- InstallManifest: Complete manifest structure
- ValidationIssue: Detected integrity problems
- RepairReport: Summary of repair operations
- FixResult: Result of fix command execution
- RollbackRequest: Request parameters for rollback
- RollbackResult: Result of rollback operation
- RestoreResult: Result of backup restoration
- RollbackValidationReport: Validation report for post-rollback verification
- CleanupResult: Result of backup cleanup
- BackupInfo: Information about available backup
"""

from .fix_models import (
    IssueType,
    IssueSeverity,
    UserChoice,
    FileEntry,
    InstallManifest,
    ValidationIssue,
    RepairReport,
    FixResult,
)

# Import STORY-080 models from parent models.py
# Note: We import from the parent module to get classes defined in installer/models.py
import sys
from pathlib import Path

# Get the models.py module (not this package)
# Add parent to path temporarily to import models.py directly
installer_path = str(Path(__file__).parent.parent)
if installer_path not in sys.path:
    sys.path.insert(0, installer_path)

try:
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "installer_models_py",
        str(Path(__file__).parent.parent / "models.py")
    )
    models_py = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(models_py)

    # Import STORY-078 classes (for compatibility)
    BackupMetadata = models_py.BackupMetadata
    FileEntry = models_py.FileEntry
    BackupReason = models_py.BackupReason
    UpgradeStatus = models_py.UpgradeStatus
    MigrationScript = models_py.MigrationScript
    ValidationCheck = models_py.ValidationCheck
    ValidationReport = models_py.ValidationReport
    UpgradeSummary = models_py.UpgradeSummary
    UpgradeError = models_py.UpgradeError
    BackupError = models_py.BackupError
    MigrationError = models_py.MigrationError
    ValidationError = models_py.ValidationError
    RollbackError = models_py.RollbackError

    # Import STORY-080 classes
    RollbackRequest = models_py.RollbackRequest
    RollbackResult = models_py.RollbackResult
    RestoreResult = models_py.RestoreResult
    RollbackValidationReport = models_py.RollbackValidationReport
    CleanupResult = models_py.CleanupResult
    BackupInfo = models_py.BackupInfo
except Exception:
    # Fallback: define stub classes if import fails
    pass

__all__ = [
    # STORY-079 classes
    "IssueType",
    "IssueSeverity",
    "UserChoice",
    "FileEntry",
    "InstallManifest",
    "ValidationIssue",
    "RepairReport",
    "FixResult",
    # STORY-078 classes (re-exported from models.py for backward compatibility)
    "BackupMetadata",
    "BackupReason",
    "UpgradeStatus",
    "MigrationScript",
    "ValidationCheck",
    "ValidationReport",
    "UpgradeSummary",
    "UpgradeError",
    "BackupError",
    "MigrationError",
    "ValidationError",
    "RollbackError",
    # STORY-080 classes
    "RollbackRequest",
    "RollbackResult",
    "RestoreResult",
    "RollbackValidationReport",
    "CleanupResult",
    "BackupInfo",
]

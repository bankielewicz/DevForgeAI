"""Data models for STORY-079: Fix/Repair Installation Mode.

Provides data models for installation validation, manifests, and repairs:
- FileEntry: Individual file tracking
- InstallManifest: Complete manifest structure
- ValidationIssue: Detected integrity problems
- RepairReport: Summary of repair operations
- FixResult: Result of fix command execution
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

__all__ = [
    "IssueType",
    "IssueSeverity",
    "UserChoice",
    "FileEntry",
    "InstallManifest",
    "ValidationIssue",
    "RepairReport",
    "FixResult",
]

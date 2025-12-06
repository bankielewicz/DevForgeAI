"""Data models for STORY-079: Fix/Repair Installation Mode (120 lines).

Enums and dataclasses for installation validation, manifest management, and repair operations.
All fields required by tests in test_installation_validator.py, test_manifest_manager.py,
test_repair_service.py, and test_fix_workflow.py.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional


class IssueType(str, Enum):
    """Types of installation issues detected."""
    MISSING = "MISSING"          # File in manifest but not on disk
    CORRUPTED = "CORRUPTED"      # File checksum doesn't match
    WRONG_VERSION = "WRONG_VERSION"  # File version doesn't match
    EXTRA = "EXTRA"              # File on disk not in manifest


class IssueSeverity(str, Enum):
    """Severity levels for detected issues."""
    CRITICAL = "CRITICAL"  # Breaks installation, must repair
    HIGH = "HIGH"          # May cause problems
    MEDIUM = "MEDIUM"      # Warning, non-critical
    LOW = "LOW"            # Information only


class UserChoice(str, Enum):
    """User choices for handling modified files."""
    KEEP = "keep"                          # Keep user's version
    RESTORE = "restore"                    # Use original from source
    SHOW_DIFF = "show_diff"                # Display differences
    BACKUP_AND_RESTORE = "backup_and_restore"  # Backup user version, restore original


@dataclass
class FileEntry:
    """Individual file entry in manifest (SVC-011, SVC-012, SVC-013)."""
    path: str                   # Relative path from installation root
    checksum: str               # SHA256 hash (64-character hex string)
    size: int                   # File size in bytes
    is_user_modifiable: bool    # Whether user is expected to modify


@dataclass
class InstallManifest:
    """Complete installation manifest (AC#1, AC#8, SVC-011, SVC-012)."""
    version: str                # DevForgeAI version (semver)
    created_at: str             # ISO8601 timestamp when created
    files: List[dict]           # List of FileEntry dicts
    schema_version: int = 1     # Manifest schema version


@dataclass
class ValidationIssue:
    """Detected integrity issue (AC#2, AC#3, SVC-001 to SVC-004)."""
    path: str                   # File path with issue
    issue_type: str             # IssueType: MISSING, CORRUPTED, WRONG_VERSION, EXTRA
    expected: Optional[str] = None      # Expected value (checksum, size, version)
    actual: Optional[str] = None        # Actual value found
    severity: Optional[str] = None      # IssueSeverity: CRITICAL, HIGH, MEDIUM, LOW
    is_user_modified: bool = False      # Whether appears to be user-modified


@dataclass
class RepairReport:
    """Summary of repair operation (AC#6, SVC-005 to SVC-008)."""
    timestamp: str              # When repair was run (ISO8601)
    total_files_checked: int    # Total files validated
    issues_found: int           # Number of issues detected
    issues_fixed: int           # Number of issues repaired
    issues_skipped: int         # Issues skipped by user choice
    issues_remaining: int = 0   # Issues requiring manual intervention
    exit_code: int = 0          # Exit code for command
    duration_seconds: float = 0.0  # Time taken
    repaired_files: List[str] = field(default_factory=list)  # Files that were repaired
    skipped_files: List[str] = field(default_factory=list)   # Files that were skipped

    def __str__(self) -> str:
        """String representation includes file details."""
        parts = [
            f"timestamp={self.timestamp}",
            f"total_files_checked={self.total_files_checked}",
            f"issues_found={self.issues_found}",
            f"issues_fixed={self.issues_fixed}",
            f"issues_skipped={self.issues_skipped}",
        ]
        if self.repaired_files:
            parts.append(f"repaired={self.repaired_files}")
        if self.skipped_files:
            parts.append(f"skipped={self.skipped_files}")
        return f"RepairReport({', '.join(parts)})"


@dataclass
class FixResult:
    """Result of fix command execution (AC#7)."""
    success: bool               # Whether fix succeeded
    exit_code: int              # Exit code (0=success, 1=missing source, 2=permission, 3=partial, 4=post-validate failed, 5=manual merge)
    report: Optional[RepairReport] = None  # Repair report if applicable
    error: Optional[str] = None            # Error message if failed
    issues_fixed: List[dict] = field(default_factory=list)  # List of fixed issues

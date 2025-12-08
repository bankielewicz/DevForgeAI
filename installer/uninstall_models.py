"""Uninstall data models for STORY-081.

Provides enums and dataclasses for uninstall operations:
- UninstallMode: COMPLETE or PRESERVE_USER_CONTENT
- ContentType: Classification of files
- UninstallStatus: Operation result status
- UninstallRequest: Input parameters
- UninstallPlan: Files to remove/preserve
- UninstallResult: Operation outcome
- ClassifiedFile: File with classification metadata
- CLICleanupResult: CLI cleanup outcome
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class UninstallMode(str, Enum):
    """Uninstall operation mode."""
    COMPLETE = "COMPLETE"
    PRESERVE_USER_CONTENT = "PRESERVE_USER_CONTENT"


class ContentType(str, Enum):
    """Classification of file content."""
    FRAMEWORK = "FRAMEWORK"
    USER_CONTENT = "USER_CONTENT"
    MODIFIED_FRAMEWORK = "MODIFIED_FRAMEWORK"
    USER_CREATED = "USER_CREATED"


class UninstallStatus(str, Enum):
    """Status of uninstall operation."""
    SUCCESS = "SUCCESS"
    PARTIAL = "PARTIAL"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


@dataclass
class ClassifiedFile:
    """File with classification metadata."""
    path: str
    content_type: ContentType
    size_bytes: int = 0
    checksum: Optional[str] = None
    original_checksum: Optional[str] = None
    is_modified: bool = False


@dataclass
class UninstallRequest:
    """Parameters for uninstall operation."""
    mode: str = "PRESERVE_USER_CONTENT"
    dry_run: bool = False
    skip_backup: bool = False
    skip_confirmation: bool = False


@dataclass
class UninstallPlan:
    """Plan of files to remove and preserve."""
    files_to_remove: List = field(default_factory=list)
    files_to_preserve: List = field(default_factory=list)
    directories_to_remove: List[str] = field(default_factory=list)
    total_size_bytes: int = 0
    preserved_size_bytes: int = 0


@dataclass
class UninstallResult:
    """Result of uninstall operation."""
    status: UninstallStatus
    files_removed: int = 0
    files_preserved: int = 0
    directories_removed: int = 0
    space_freed_mb: float = 0.0
    backup_path: Optional[str] = None
    duration_seconds: float = 0.0
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


@dataclass
class CLICleanupResult:
    """Result of CLI cleanup operation."""
    removed: bool = False
    binaries_removed: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    requires_manual_cleanup: bool = False
    manual_cleanup_instructions: Optional[str] = None


@dataclass
class FileRemovalResult:
    """Result of file removal operation."""
    files_removed: int = 0
    total_space_bytes: int = 0
    errors: List[str] = field(default_factory=list)

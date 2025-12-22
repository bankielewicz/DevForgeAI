"""
Services for DevForgeAI installer.

Provides:
- Auto-detection services (installations, CLAUDE.md, Git, conflicts)
- CLAUDE.md merge services (markdown parsing, backup, conflict detection)
- Formatted summaries (color-coded output)
"""

from .version_detection_service import VersionDetectionService, VersionInfo, VersionComparisonResult
from .claudemd_detection_service import ClaudeMdDetectionService, ClaudeMdInfo
from .git_detection_service import GitDetectionService, GitInfo
from .file_conflict_detection_service import FileConflictDetectionService, ConflictInfo
from .summary_formatter_service import SummaryFormatterService
from .auto_detection_service import AutoDetectionService, DetectionResult
from .markdown_parser import MarkdownParser
from .merge_backup_service import MergeBackupService
from .merge_conflict_detection_service import MergeConflictDetectionService
from .claudemd_merge_service import ClaudeMdMergeService

__all__ = [
    'VersionDetectionService',
    'VersionInfo',
    'VersionComparisonResult',
    'ClaudeMdDetectionService',
    'ClaudeMdInfo',
    'GitDetectionService',
    'GitInfo',
    'FileConflictDetectionService',
    'ConflictInfo',
    'SummaryFormatterService',
    'AutoDetectionService',
    'DetectionResult',
    'MarkdownParser',
    'MergeBackupService',
    'MergeConflictDetectionService',
    'ClaudeMdMergeService',
]

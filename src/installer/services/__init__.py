"""
Auto-detection services for DevForgeAI installer.

Provides automated detection of:
- Existing installations (version comparison)
- CLAUDE.md files (backup recommendations)
- Git repositories (root path detection)
- File conflicts (framework vs user files)
- Formatted summaries (color-coded output)
"""

from .version_detection_service import VersionDetectionService, VersionInfo, VersionComparisonResult
from .claudemd_detection_service import ClaudeMdDetectionService, ClaudeMdInfo
from .git_detection_service import GitDetectionService, GitInfo
from .file_conflict_detection_service import FileConflictDetectionService, ConflictInfo
from .summary_formatter_service import SummaryFormatterService
from .auto_detection_service import AutoDetectionService, DetectionResult

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
]

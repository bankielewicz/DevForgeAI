"""
Auto Detection Service (Orchestrator) - STORY-073

Orchestrates all auto-detection checks and returns unified results.

Requirements:
- SVC-001: Orchestrate all auto-detection checks and return DetectionResult
- SVC-002: Execute checks concurrently where possible
- SVC-003: Handle partial failures gracefully

Business Rules:
- BR-001: Auto-detection failures are non-fatal (continue with other checks)
- BR-002: Summary displays before any user prompts
- NFR-001: Auto-detection completes in <500ms for typical projects
"""

import logging
from typing import Optional, List
from concurrent.futures import ThreadPoolExecutor, as_completed

from .version_detection_service import VersionDetectionService, VersionInfo
from .claudemd_detection_service import ClaudeMdDetectionService, ClaudeMdInfo
from .git_detection_service import GitDetectionService, GitInfo
from .file_conflict_detection_service import FileConflictDetectionService, ConflictInfo
from .summary_formatter_service import SummaryFormatterService

logger = logging.getLogger(__name__)


class DetectionResult:
    """
    Data model aggregating all auto-detection results.

    Fields:
        version_info: Detected version information (None if not found)
        claudemd_info: CLAUDE.md detection results (None if not found)
        git_info: Git repository detection results (None if not found)
        conflicts: File conflict detection results (always present)
    """

    def __init__(
        self,
        version_info: Optional[VersionInfo] = None,
        claudemd_info: Optional[ClaudeMdInfo] = None,
        git_info: Optional[GitInfo] = None,
        conflicts: Optional[ConflictInfo] = None
    ):
        self.version_info = version_info
        self.claudemd_info = claudemd_info
        self.git_info = git_info
        self.conflicts = conflicts if conflicts is not None else ConflictInfo([], 0, 0)


class AutoDetectionService:
    """
    Service orchestrating all auto-detection checks.

    Lifecycle: Singleton (one instance per target path)
    Dependencies: All detection services + summary formatter
    """

    def __init__(
        self,
        target_path: str,
        source_version: str,
        source_files: List[str],
        version_service: Optional[VersionDetectionService] = None,
        claudemd_service: Optional[ClaudeMdDetectionService] = None,
        git_service: Optional[GitDetectionService] = None,
        conflict_service: Optional[FileConflictDetectionService] = None,
        formatter_service: Optional[SummaryFormatterService] = None
    ):
        """
        Initialize auto detection service.

        Args:
            target_path: Absolute path to target installation directory
            source_version: Version string from source installer
            source_files: List of relative file paths from source
            version_service: Optional VersionDetectionService instance (for testing)
            claudemd_service: Optional ClaudeMdDetectionService instance (for testing)
            git_service: Optional GitDetectionService instance (for testing)
            conflict_service: Optional FileConflictDetectionService instance (for testing)
            formatter_service: Optional SummaryFormatterService instance (for testing)
        """
        self.target_path = target_path
        self.source_version = source_version
        self.source_files = source_files

        # Initialize individual detection services (allow injection for testing)
        self.version_service = version_service or VersionDetectionService(target_path)
        self.claudemd_service = claudemd_service or ClaudeMdDetectionService(target_path)
        self.git_service = git_service or GitDetectionService(target_path)
        self.conflict_service = conflict_service or FileConflictDetectionService(target_path, source_files)
        self.formatter_service = formatter_service or SummaryFormatterService()

    def detect_all(self) -> DetectionResult:
        """
        Orchestrate all auto-detection checks and return unified results.

        Returns:
            DetectionResult with all detection results

        Test Requirements:
            - Returns DetectionResult with all fields
            - Invokes all 5 detection services
            - Handles partial failures gracefully (SVC-003, BR-001)
            - Completes in <500ms for typical projects (NFR-001)
            - Can execute checks concurrently (SVC-002)
        """
        try:
            # Execute detection checks
            # Note: For simplicity, running sequentially first
            # Can be optimized with concurrent.futures for SVC-002

            # Check 1: Version detection
            version_info = self._detect_version()

            # Check 2: CLAUDE.md detection
            claudemd_info = self._detect_claudemd()

            # Check 3: Git repository detection
            git_info = self._detect_git()

            # Check 4: File conflict detection
            conflicts = self._detect_conflicts()

            # Return unified results
            return DetectionResult(
                version_info=version_info,
                claudemd_info=claudemd_info,
                git_info=git_info,
                conflicts=conflicts
            )

        except Exception as e:
            logger.error(f"Unexpected error in auto-detection orchestration: {e}")
            # Return partial results (BR-001: failures are non-fatal)
            return DetectionResult()

    def detect_all_concurrent(self) -> DetectionResult:
        """
        Execute detection checks concurrently using ThreadPoolExecutor.

        Returns:
            DetectionResult with all detection results

        Performance: Faster than sequential for independent checks (SVC-002)
        """
        results = {
            'version_info': None,
            'claudemd_info': None,
            'git_info': None,
            'conflicts': None
        }

        # Define detection tasks
        tasks = {
            'version_info': self._detect_version,
            'claudemd_info': self._detect_claudemd,
            'git_info': self._detect_git,
            'conflicts': self._detect_conflicts
        }

        # Execute tasks concurrently
        with ThreadPoolExecutor(max_workers=4) as executor:
            # Submit all tasks
            future_to_key = {
                executor.submit(task): key
                for key, task in tasks.items()
            }

            # Collect results as they complete
            for future in as_completed(future_to_key):
                key = future_to_key[future]
                try:
                    results[key] = future.result()
                except Exception as e:
                    logger.error(f"Detection task {key} failed: {e}")
                    # Continue with other checks (BR-001)

        # Return unified results
        return DetectionResult(
            version_info=results['version_info'],
            claudemd_info=results['claudemd_info'],
            git_info=results['git_info'],
            conflicts=results['conflicts']
        )

    def format_summary(self, detection_result: DetectionResult) -> str:
        """
        Format detection results into human-readable summary.

        Args:
            detection_result: Complete detection results

        Returns:
            Formatted summary string

        Test Requirements:
            - Delegates to SummaryFormatterService
            - Returns multi-line string with 4 sections
        """
        return self.formatter_service.format_summary(detection_result)

    # Private helper methods

    def _detect_version(self) -> Optional[VersionInfo]:
        """
        Execute version detection check.

        Returns:
            VersionInfo or None if detection failed

        Error Handling: Failures are non-fatal (BR-001)
        """
        try:
            return self.version_service.read_version()
        except Exception as e:
            logger.error(f"Version detection failed: {e}")
            return None

    def _detect_claudemd(self) -> Optional[ClaudeMdInfo]:
        """
        Execute CLAUDE.md detection check.

        Returns:
            ClaudeMdInfo or None if detection failed

        Error Handling: Failures are non-fatal (BR-001)
        """
        try:
            return self.claudemd_service.detect()
        except Exception as e:
            logger.error(f"CLAUDE.md detection failed: {e}")
            return None

    def _detect_git(self) -> Optional[GitInfo]:
        """
        Execute Git repository detection check.

        Returns:
            GitInfo or None if detection failed

        Error Handling: Failures are non-fatal (BR-001)
        """
        try:
            git_root = self.git_service.detect_git_root()
            is_submodule = self.git_service.is_submodule()

            if git_root is not None:
                return GitInfo(
                    repository_root=git_root,
                    is_submodule=is_submodule
                )
            return None

        except Exception as e:
            logger.error(f"Git detection failed: {e}")
            return None

    def _detect_conflicts(self) -> ConflictInfo:
        """
        Execute file conflict detection check.

        Returns:
            ConflictInfo (always returns results, empty list if no conflicts)

        Error Handling: Failures return empty ConflictInfo (BR-001)
        """
        try:
            return self.conflict_service.detect_conflicts()
        except Exception as e:
            logger.error(f"Conflict detection failed: {e}")
            return ConflictInfo(conflicts=[], framework_count=0, user_count=0)

"""
Unit tests for SummaryFormatterService.

Tests AC#6:
- Format DetectionResult into human-readable summary
- Apply color coding for terminal output
- Paginate conflict lists (show first 10)
- Display 4 sections: Installation Status, Project Context, Conflicts, Recommendations

Component Requirements:
- SVC-020: Format DetectionResult into human-readable summary
- SVC-021: Apply color coding for terminal output
- SVC-022: Paginate conflict lists (show first 10)

Business Rules:
- BR-002: Summary displays before any user prompts
- NFR-008: Summary uses color coding when supported
"""

import pytest
from unittest.mock import Mock, patch
from pathlib import Path
from datetime import datetime


# Story: STORY-073
class TestSummaryFormatterService:
    """Test suite for SummaryFormatterService - DetectionResult formatting and display."""

    # AC#6: Format summary with 4 sections (SVC-020)

    # AC marker removed
    def test_should_format_summary_with_all_four_sections(self):
        """
        Test: Summary contains 4 required sections (SVC-020, AC#6)

        Given: Complete DetectionResult
        When: format_summary() is called
        Then: Returns string with Installation Status, Project Context, Conflicts, Recommendations
        """
        # Arrange
        from src.installer.services.summary_formatter_service import SummaryFormatterService
        from src.installer.services.auto_detection_service import DetectionResult
        from src.installer.services.version_detection_service import VersionInfo
        from src.installer.services.git_detection_service import GitInfo
        from src.installer.services.file_conflict_detection_service import ConflictInfo

        version_info = VersionInfo(
            installed_version="1.0.0",
            installed_at="2025-11-25T10:30:00Z",
            installation_source="installer"
        )

        git_info = GitInfo(
            repository_root=Path("/tmp/project"),
            is_submodule=False
        )

        conflict_info = ConflictInfo(
            conflicts=[Path("/tmp/project/CLAUDE.md")],
            framework_count=0,
            user_count=1
        )

        detection_result = DetectionResult(
            version_info=version_info,
            claudemd_info=None,
            git_info=git_info,
            conflicts=conflict_info
        )

        service = SummaryFormatterService()

        # Act
        summary = service.format_summary(detection_result)

        # Assert
        assert "Installation Status" in summary or "installation" in summary.lower()
        assert "Project Context" in summary or "git" in summary.lower()
        assert "Conflicts" in summary or "conflict" in summary.lower()
        assert "Recommendations" in summary or "recommend" in summary.lower()

    # AC marker removed
    def test_should_display_clean_install_when_no_version(self):
        """
        Test: Clean install shown when version_info is None (AC#6)

        Given: DetectionResult with version_info=None
        When: format_summary() is called
        Then: Installation Status shows "Clean install"
        """
        # Arrange
        from src.installer.services.summary_formatter_service import SummaryFormatterService
        from src.installer.services.auto_detection_service import DetectionResult
        from src.installer.services.file_conflict_detection_service import ConflictInfo

        detection_result = DetectionResult(
            version_info=None,
            claudemd_info=None,
            git_info=None,
            conflicts=ConflictInfo(conflicts=[], framework_count=0, user_count=0)
        )

        service = SummaryFormatterService()

        # Act
        summary = service.format_summary(detection_result)

        # Assert
        assert "clean install" in summary.lower() or "no existing installation" in summary.lower()

    # AC marker removed
    def test_should_display_existing_version_when_present(self):
        """
        Test: Existing version displayed in summary (AC#6)

        Given: DetectionResult with version_info
        When: format_summary() is called
        Then: Shows "Found existing DevForgeAI installation: v{version}"
        """
        # Arrange
        from src.installer.services.summary_formatter_service import SummaryFormatterService
        from src.installer.services.auto_detection_service import DetectionResult
        from src.installer.services.version_detection_service import VersionInfo
        from src.installer.services.file_conflict_detection_service import ConflictInfo

        version_info = VersionInfo(
            installed_version="1.2.3",
            installed_at="2025-11-25T10:30:00Z",
            installation_source="installer"
        )

        detection_result = DetectionResult(
            version_info=version_info,
            claudemd_info=None,
            git_info=None,
            conflicts=ConflictInfo(conflicts=[], framework_count=0, user_count=0)
        )

        service = SummaryFormatterService()

        # Act
        summary = service.format_summary(detection_result)

        # Assert
        assert "1.2.3" in summary
        assert "existing" in summary.lower() or "found" in summary.lower()

    # AC marker removed
    def test_should_display_git_root_path(self):
        """
        Test: Git repository root displayed (AC#6)

        Given: DetectionResult with git_info
        When: format_summary() is called
        Then: Project Context shows git root path
        """
        # Arrange
        from src.installer.services.summary_formatter_service import SummaryFormatterService
        from src.installer.services.auto_detection_service import DetectionResult
        from src.installer.services.git_detection_service import GitInfo
        from src.installer.services.file_conflict_detection_service import ConflictInfo

        git_info = GitInfo(
            repository_root=Path("/home/user/projects/myrepo"),
            is_submodule=False
        )

        detection_result = DetectionResult(
            version_info=None,
            claudemd_info=None,
            git_info=git_info,
            conflicts=ConflictInfo(conflicts=[], framework_count=0, user_count=0)
        )

        service = SummaryFormatterService()

        # Act
        summary = service.format_summary(detection_result)

        # Assert
        assert "myrepo" in summary or "/home/user/projects" in summary

    # AC marker removed
    def test_should_display_no_git_repository_when_missing(self):
        """
        Test: No git repository message when git_info is None (AC#6)

        Given: DetectionResult with git_info=None
        When: format_summary() is called
        Then: Shows "No git repository detected"
        """
        # Arrange
        from src.installer.services.summary_formatter_service import SummaryFormatterService
        from src.installer.services.auto_detection_service import DetectionResult
        from src.installer.services.file_conflict_detection_service import ConflictInfo

        detection_result = DetectionResult(
            version_info=None,
            claudemd_info=None,
            git_info=None,
            conflicts=ConflictInfo(conflicts=[], framework_count=0, user_count=0)
        )

        service = SummaryFormatterService()

        # Act
        summary = service.format_summary(detection_result)

        # Assert
        assert "no git" in summary.lower() or "not a git repository" in summary.lower()

    # AC#6: Conflict display (SVC-022)

    # AC marker removed
    def test_should_display_conflict_count_by_category(self):
        """
        Test: Conflict counts shown by category (AC#6)

        Given: DetectionResult with framework and user conflicts
        When: format_summary() is called
        Then: Shows "{count} framework files, {count} user files"
        """
        # Arrange
        from src.installer.services.summary_formatter_service import SummaryFormatterService
        from src.installer.services.auto_detection_service import DetectionResult
        from src.installer.services.file_conflict_detection_service import ConflictInfo

        conflict_info = ConflictInfo(
            conflicts=[
                Path(".claude/skills/skill.md"),
                Path(".devforgeai/context/tech-stack.md"),
                Path("CLAUDE.md")
            ],
            framework_count=2,
            user_count=1
        )

        detection_result = DetectionResult(
            version_info=None,
            claudemd_info=None,
            git_info=None,
            conflicts=conflict_info
        )

        service = SummaryFormatterService()

        # Act
        summary = service.format_summary(detection_result)

        # Assert
        assert "2" in summary and "framework" in summary.lower()
        assert "1" in summary and "user" in summary.lower()

    # AC marker removed
    def test_should_paginate_conflicts_show_first_10(self):
        """
        Test: Conflict list paginated to first 10 (SVC-022, AC#6)

        Given: 50 conflicts in DetectionResult
        When: format_summary() is called
        Then: Shows first 10 conflicts with "...and 40 more"
        """
        # Arrange
        from src.installer.services.summary_formatter_service import SummaryFormatterService
        from src.installer.services.auto_detection_service import DetectionResult
        from src.installer.services.file_conflict_detection_service import ConflictInfo

        conflicts = [Path(f"file_{i}.txt") for i in range(50)]
        conflict_info = ConflictInfo(
            conflicts=conflicts,
            framework_count=50,
            user_count=0
        )

        detection_result = DetectionResult(
            version_info=None,
            claudemd_info=None,
            git_info=None,
            conflicts=conflict_info
        )

        service = SummaryFormatterService()

        # Act
        summary = service.format_summary(detection_result)

        # Assert
        assert "40 more" in summary or "40 additional" in summary.lower()
        # Should show file_0 through file_9
        assert "file_0" in summary
        assert "file_9" in summary
        # Should NOT show file_10 or beyond
        assert "file_10" not in summary

    # AC marker removed
    def test_should_show_all_conflicts_when_less_than_10(self):
        """
        Test: All conflicts shown when <10 total (SVC-022)

        Given: 5 conflicts in DetectionResult
        When: format_summary() is called
        Then: Shows all 5 conflicts without "...more" message
        """
        # Arrange
        from src.installer.services.summary_formatter_service import SummaryFormatterService
        from src.installer.services.auto_detection_service import DetectionResult
        from src.installer.services.file_conflict_detection_service import ConflictInfo

        conflicts = [Path(f"file_{i}.txt") for i in range(5)]
        conflict_info = ConflictInfo(
            conflicts=conflicts,
            framework_count=5,
            user_count=0
        )

        detection_result = DetectionResult(
            version_info=None,
            claudemd_info=None,
            git_info=None,
            conflicts=conflict_info
        )

        service = SummaryFormatterService()

        # Act
        summary = service.format_summary(detection_result)

        # Assert
        for i in range(5):
            assert f"file_{i}.txt" in summary
        assert "more" not in summary.lower()

    # AC marker removed
    def test_should_display_no_conflicts_when_empty(self):
        """
        Test: No conflicts message when empty list (AC#6)

        Given: DetectionResult with empty conflicts list
        When: format_summary() is called
        Then: Shows "No conflicts detected"
        """
        # Arrange
        from src.installer.services.summary_formatter_service import SummaryFormatterService
        from src.installer.services.auto_detection_service import DetectionResult
        from src.installer.services.file_conflict_detection_service import ConflictInfo

        detection_result = DetectionResult(
            version_info=None,
            claudemd_info=None,
            git_info=None,
            conflicts=ConflictInfo(conflicts=[], framework_count=0, user_count=0)
        )

        service = SummaryFormatterService()

        # Act
        summary = service.format_summary(detection_result)

        # Assert
        assert "no file conflicts detected" in summary.lower() or "0 conflicts" in summary

    # SVC-021: Color coding (NFR-008)

    # AC marker removed
    def test_should_apply_ansi_color_codes_when_supported(self):
        """
        Test: ANSI color codes applied when terminal supports it (SVC-021, NFR-008)

        Given: Terminal supports colors (sys.stdout.isatty() == True)
        When: format_summary() is called
        Then: Output includes ANSI escape codes
        """
        # Arrange
        from src.installer.services.summary_formatter_service import SummaryFormatterService
        from src.installer.services.auto_detection_service import DetectionResult
        from src.installer.services.file_conflict_detection_service import ConflictInfo

        detection_result = DetectionResult(
            version_info=None,
            claudemd_info=None,
            git_info=None,
            conflicts=ConflictInfo(conflicts=[], framework_count=0, user_count=0)
        )

        service = SummaryFormatterService(use_colors=True)

        # Act
        summary = service.format_summary(detection_result)

        # Assert
        # Check for ANSI escape sequences (e.g., \033[32m for green)
        assert "\033[" in summary or summary != summary  # Has ANSI codes

    # AC marker removed
    def test_should_omit_colors_when_not_supported(self):
        """
        Test: No color codes when terminal doesn't support colors (SVC-021)

        Given: Terminal doesn't support colors (sys.stdout.isatty() == False)
        When: format_summary() is called
        Then: Output has no ANSI escape codes
        """
        # Arrange
        from src.installer.services.summary_formatter_service import SummaryFormatterService
        from src.installer.services.auto_detection_service import DetectionResult
        from src.installer.services.file_conflict_detection_service import ConflictInfo

        detection_result = DetectionResult(
            version_info=None,
            claudemd_info=None,
            git_info=None,
            conflicts=ConflictInfo(conflicts=[], framework_count=0, user_count=0)
        )

        service = SummaryFormatterService(use_colors=False)

        # Act
        summary = service.format_summary(detection_result)

        # Assert
        assert "\033[" not in summary

    # Recommendations section

    # AC marker removed
    def test_should_recommend_upgrade_when_newer_version_available(self):
        """
        Test: Upgrade recommendation shown (AC#6)

        Given: Source version > installed version
        When: format_summary() is called
        Then: Recommendations section shows "Upgrade recommended"
        """
        # Arrange
        from src.installer.services.summary_formatter_service import SummaryFormatterService
        from src.installer.services.auto_detection_service import DetectionResult
        from src.installer.services.version_detection_service import VersionInfo
        from src.installer.services.file_conflict_detection_service import ConflictInfo

        version_info = VersionInfo(
            installed_version="1.0.0",
            installed_at="2025-11-25T10:30:00Z",
            installation_source="installer"
        )

        detection_result = DetectionResult(
            version_info=version_info,
            claudemd_info=None,
            git_info=None,
            conflicts=ConflictInfo(conflicts=[], framework_count=0, user_count=0)
        )

        service = SummaryFormatterService(source_version="1.1.0")

        # Act
        summary = service.format_summary(detection_result)

        # Assert
        assert "upgrade" in summary.lower()

    # AC marker removed
    def test_should_recommend_clean_install_when_no_version(self):
        """
        Test: Clean install recommendation shown (AC#6)

        Given: version_info is None
        When: format_summary() is called
        Then: Recommendations section shows "Clean install"
        """
        # Arrange
        from src.installer.services.summary_formatter_service import SummaryFormatterService
        from src.installer.services.auto_detection_service import DetectionResult
        from src.installer.services.file_conflict_detection_service import ConflictInfo

        detection_result = DetectionResult(
            version_info=None,
            claudemd_info=None,
            git_info=None,
            conflicts=ConflictInfo(conflicts=[], framework_count=0, user_count=0)
        )

        service = SummaryFormatterService()

        # Act
        summary = service.format_summary(detection_result)

        # Assert
        assert "clean install" in summary.lower()

    # Performance

    def test_should_complete_summary_generation_within_50ms(self):
        """
        Test: Summary generation < 50ms (NFR)

        Given: DetectionResult with data
        When: format_summary() is called
        Then: Completes in <50ms
        """
        # Arrange
        import time
        from src.installer.services.summary_formatter_service import SummaryFormatterService
        from src.installer.services.auto_detection_service import DetectionResult
        from src.installer.services.file_conflict_detection_service import ConflictInfo

        conflicts = [Path(f"file_{i}.txt") for i in range(100)]
        conflict_info = ConflictInfo(
            conflicts=conflicts,
            framework_count=100,
            user_count=0
        )

        detection_result = DetectionResult(
            version_info=None,
            claudemd_info=None,
            git_info=None,
            conflicts=conflict_info
        )

        service = SummaryFormatterService()

        # Act
        start = time.time()
        summary = service.format_summary(detection_result)
        duration_ms = (time.time() - start) * 1000

        # Assert
        assert duration_ms < 50, f"Summary took {duration_ms}ms (expected <50ms)"

    # Edge Cases

    def test_should_handle_very_long_file_paths(self):
        """
        Test: Very long file paths handled gracefully

        Given: Conflicts with 500-character file paths
        When: format_summary() is called
        Then: Paths truncated or wrapped appropriately
        """
        # Arrange
        from src.installer.services.summary_formatter_service import SummaryFormatterService
        from src.installer.services.auto_detection_service import DetectionResult
        from src.installer.services.file_conflict_detection_service import ConflictInfo

        long_path = "a" * 500 + ".txt"
        conflict_info = ConflictInfo(
            conflicts=[Path(long_path)],
            framework_count=0,
            user_count=1
        )

        detection_result = DetectionResult(
            version_info=None,
            claudemd_info=None,
            git_info=None,
            conflicts=conflict_info
        )

        service = SummaryFormatterService()

        # Act
        summary = service.format_summary(detection_result)

        # Assert - should not crash
        assert summary is not None

    def test_should_handle_unicode_characters_in_paths(self):
        """
        Test: Unicode characters in file paths handled

        Given: Conflicts with Unicode file names
        When: format_summary() is called
        Then: Displays correctly without encoding errors
        """
        # Arrange
        from src.installer.services.summary_formatter_service import SummaryFormatterService
        from src.installer.services.auto_detection_service import DetectionResult
        from src.installer.services.file_conflict_detection_service import ConflictInfo

        unicode_path = "файл_测试_🚀.txt"
        conflict_info = ConflictInfo(
            conflicts=[Path(unicode_path)],
            framework_count=0,
            user_count=1
        )

        detection_result = DetectionResult(
            version_info=None,
            claudemd_info=None,
            git_info=None,
            conflicts=conflict_info
        )

        service = SummaryFormatterService()

        # Act
        summary = service.format_summary(detection_result)

        # Assert
        assert unicode_path in summary

    # Business Rule BR-002: Summary before prompts

    def test_summary_returns_string_for_immediate_display(self):
        """
        Test: Summary returns string for immediate display (BR-002)

        Given: DetectionResult
        When: format_summary() is called
        Then: Returns string (not None, not async)
        """
        # Arrange
        from src.installer.services.summary_formatter_service import SummaryFormatterService
        from src.installer.services.auto_detection_service import DetectionResult
        from src.installer.services.file_conflict_detection_service import ConflictInfo

        detection_result = DetectionResult(
            version_info=None,
            claudemd_info=None,
            git_info=None,
            conflicts=ConflictInfo(conflicts=[], framework_count=0, user_count=0)
        )

        service = SummaryFormatterService()

        # Act
        summary = service.format_summary(detection_result)

        # Assert
        assert isinstance(summary, str)
        assert len(summary) > 0

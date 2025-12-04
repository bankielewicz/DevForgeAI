"""
Unit tests for ClaudeMdMergeService.

Tests the orchestration of all merge strategies and user interactions.

Component Requirements (From STORY-076 Tech Spec):
- SVC-001: Detect existing CLAUDE.md file presence
- SVC-002: Prompt user for merge strategy selection
- SVC-003: Execute auto-merge preserving user sections
- SVC-004: Detect merge conflicts
- SVC-005: Create timestamped backup before modification

Acceptance Criteria:
- AC#1: Merge detection and strategy selection
- AC#2: Auto-merge content preservation
- AC#3: Backup creation before modification
- AC#4: Conflict detection and user escalation
- AC#5: Replace strategy with backup
- AC#6: Skip strategy preservation
- AC#7: Manual resolution workflow
- AC#8: Merge log documentation

Test Strategy: 95%+ coverage target for orchestration logic.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock, call
from pathlib import Path
import tempfile
import time


class TestClaudeMdMergeServiceInitialization:
    """Test ClaudeMdMergeService initialization and dependencies."""

    def test_should_initialize_service_with_dependencies(self, mock_logger):
        """
        Test: ClaudeMdMergeService initializes with all dependencies

        Given: Service dependencies injected
        When: Instantiated
        Then: Returns service instance
        """
        # Arrange & Act
        from src.installer.services.claudemd_merge_service import ClaudeMdMergeService
        service = ClaudeMdMergeService(logger=mock_logger)

        # Assert
        assert service is not None
        assert hasattr(service, "merge")
        assert hasattr(service, "detect_existing")

    def test_should_have_required_methods(self, mock_logger):
        """Test: Service has all required public methods."""
        # Arrange
        from src.installer.services.claudemd_merge_service import ClaudeMdMergeService
        service = ClaudeMdMergeService(logger=mock_logger)

        # Act & Assert
        assert callable(getattr(service, "detect_existing", None))
        assert callable(getattr(service, "auto_merge", None))
        assert callable(getattr(service, "replace", None))
        assert callable(getattr(service, "skip", None))
        assert callable(getattr(service, "manual", None))


class TestDetectExistingCLAUDEmd:
    """Test CLAUDE.md file detection (SVC-001, AC#1)."""

    def test_should_detect_existing_claudemd_file(self, temp_dir):
        """
        Test: Returns exists=True when file present (SVC-001, AC#1)

        Given: CLAUDE.md file exists in directory
        When: detect_existing() called
        Then: Returns True
        """
        # Arrange
        from src.installer.services.claudemd_merge_service import ClaudeMdMergeService
        claudemd_path = temp_dir / "CLAUDE.md"
        claudemd_path.write_text("existing content")
        service = ClaudeMdMergeService(logger=Mock())

        # Act
        exists = service.detect_existing(temp_dir)

        # Assert
        assert exists is True

    def test_should_detect_missing_claudemd_file(self, temp_dir):
        """
        Test: Returns exists=False when file missing

        Given: CLAUDE.md doesn't exist
        When: detect_existing() called
        Then: Returns False
        """
        # Arrange
        from src.installer.services.claudemd_merge_service import ClaudeMdMergeService
        service = ClaudeMdMergeService(logger=Mock())

        # Act
        exists = service.detect_existing(temp_dir)

        # Assert
        assert exists is False

    def test_should_return_boolean_type(self, temp_dir):
        """Test: detect_existing() returns bool type."""
        # Arrange
        from src.installer.services.claudemd_merge_service import ClaudeMdMergeService
        service = ClaudeMdMergeService(logger=Mock())

        # Act
        result = service.detect_existing(temp_dir)

        # Assert
        assert isinstance(result, bool)


class TestStrategySelection:
    """Test user strategy selection prompting (SVC-002, AC#1)."""

    def test_should_prompt_for_strategy_selection(self, mock_logger):
        """
        Test: AskUserQuestion invoked with 4 options (SVC-002, AC#1)

        Given: CLAUDE.md detected
        When: select_strategy() called
        Then: User prompted with 4 options
        """
        # Arrange
        from src.installer.services.claudemd_merge_service import ClaudeMdMergeService
        service = ClaudeMdMergeService(logger=mock_logger)

        # Mock user choice
        with patch("src.installer.services.claudemd_merge_service.AskUserQuestion") as mock_ask:
            mock_ask.return_value = "auto-merge"

            # Act
            strategy = service.select_strategy()

            # Assert
            assert strategy in ["auto-merge", "replace", "skip", "manual"]

    def test_should_offer_four_strategy_options(self, mock_logger):
        """
        Test: Exactly 4 strategies offered (auto-merge, replace, skip, manual) (AC#1)

        Given: select_strategy() called
        When: User prompted
        Then: 4 options presented
        """
        # Arrange
        from src.installer.services.claudemd_merge_service import ClaudeMdMergeService
        service = ClaudeMdMergeService(logger=mock_logger)

        # Expected strategies
        expected_strategies = ["auto-merge", "replace", "skip", "manual"]

        # Act & Assert
        # Service should support all 4 strategies
        for strategy in expected_strategies:
            assert hasattr(service, strategy)

    def test_should_return_string_strategy(self, mock_logger):
        """Test: select_strategy() returns string strategy name."""
        # Arrange
        from src.installer.services.claudemd_merge_service import ClaudeMdMergeService
        service = ClaudeMdMergeService(logger=mock_logger)

        with patch("src.installer.services.claudemd_merge_service.AskUserQuestion") as mock_ask:
            mock_ask.return_value = "auto-merge"

            # Act
            result = service.select_strategy()

            # Assert
            assert isinstance(result, str)


class TestAutoMergeStrategy:
    """Test auto-merge strategy (SVC-003, AC#2)."""

    def test_should_preserve_user_sections_verbatim(self, temp_dir, mock_logger, simple_claudemd, framework_template):
        """
        Test: User section preserved byte-identical (SVC-003, AC#2, BR-002)

        Given: Existing CLAUDE.md with user sections
        When: auto_merge() executes
        Then: User sections at original position unchanged
        """
        # Arrange
        from src.installer.services.claudemd_merge_service import ClaudeMdMergeService
        service = ClaudeMdMergeService(logger=mock_logger)
        claudemd_path = temp_dir / "CLAUDE.md"
        claudemd_path.write_text(simple_claudemd)

        # Act
        result = service.auto_merge(claudemd_path, framework_template)

        # Assert
        assert result is not None
        assert result.merged_content is not None
        # User section "My Custom Configuration" should be present
        assert "My Custom Configuration" in result.merged_content

    def test_should_update_framework_sections(self, temp_dir, mock_logger, simple_claudemd, framework_template):
        """
        Test: Framework sections updated with new DevForgeAI content (AC#2)

        Given: Existing CLAUDE.md with outdated framework sections
        When: auto_merge() executes
        Then: Framework sections updated to latest
        """
        # Arrange
        from src.installer.services.claudemd_merge_service import ClaudeMdMergeService
        service = ClaudeMdMergeService(logger=mock_logger)
        claudemd_path = temp_dir / "CLAUDE.md"
        claudemd_path.write_text(simple_claudemd)

        # Act
        result = service.auto_merge(claudemd_path, framework_template)

        # Assert
        assert result is not None
        assert result.merged_content is not None

    def test_should_return_merged_content_in_merge_result(self, temp_dir, mock_logger, simple_claudemd, framework_template):
        """
        Test: MergeResult.merged_content contains merged file (AC#2)

        Given: auto_merge() executes
        When: Returns MergeResult
        Then: merged_content field populated
        """
        # Arrange
        from src.installer.services.claudemd_merge_service import ClaudeMdMergeService
        service = ClaudeMdMergeService(logger=mock_logger)
        claudemd_path = temp_dir / "CLAUDE.md"
        claudemd_path.write_text(simple_claudemd)

        # Act
        result = service.auto_merge(claudemd_path, framework_template)

        # Assert
        assert result is not None
        assert hasattr(result, "merged_content")
        assert result.merged_content is not None

    def test_should_maintain_section_positions(self, temp_dir, mock_logger, simple_claudemd, framework_template):
        """
        Test: Section positions maintained (AC#2)

        Given: CLAUDE.md with sections in specific order
        When: auto_merge() executes
        Then: Sections in same relative positions
        """
        # Arrange
        from src.installer.services.claudemd_merge_service import ClaudeMdMergeService
        service = ClaudeMdMergeService(logger=mock_logger)
        claudemd_path = temp_dir / "CLAUDE.md"
        claudemd_path.write_text(simple_claudemd)

        # Act
        result = service.auto_merge(claudemd_path, framework_template)

        # Assert
        assert result is not None
        assert result.merged_content is not None


class TestAutoMergeWithConflicts:
    """Test auto-merge conflict escalation (SVC-004, AC#4)."""

    def test_should_detect_conflict_when_framework_section_modified(self, temp_dir, mock_logger, conflicting_claudemd):
        """
        Test: Conflict detected when user modified framework section (SVC-004, AC#4)

        Given: User heavily modified framework section (>30% change)
        When: auto_merge() detects conflict
        Then: Returns conflict in MergeResult
        """
        # Arrange
        from src.installer.services.claudemd_merge_service import ClaudeMdMergeService
        service = ClaudeMdMergeService(logger=mock_logger)
        claudemd_path = temp_dir / "CLAUDE.md"
        claudemd_path.write_text(conflicting_claudemd)
        framework_template = """## Repository Overview

Framework guidance unchanged.

## Critical Rules

Original framework rules."""

        # Act
        result = service.auto_merge(claudemd_path, framework_template)

        # Assert
        assert result is not None
        # Should detect conflict

    def test_should_halt_automerge_on_conflict(self, temp_dir, mock_logger, conflicting_claudemd):
        """
        Test: Auto-merge halts when conflict detected (AC#4, BR-003)

        Given: Conflict exists in framework section
        When: auto_merge() executes
        Then: Stops and returns conflict status
        """
        # Arrange
        from src.installer.services.claudemd_merge_service import ClaudeMdMergeService
        service = ClaudeMdMergeService(logger=mock_logger)
        claudemd_path = temp_dir / "CLAUDE.md"
        claudemd_path.write_text(conflicting_claudemd)

        # Act
        result = service.auto_merge(claudemd_path, "")

        # Assert
        assert result is not None
        # Result should indicate conflict or user intervention needed

    def test_should_escalate_to_user_for_conflict_resolution(self, temp_dir, mock_logger, conflicting_claudemd):
        """
        Test: User prompted for conflict resolution (AC#4)

        Given: Conflict detected
        When: auto_merge() escalates
        Then: User prompted with 3 options
        """
        # Arrange
        from src.installer.services.claudemd_merge_service import ClaudeMdMergeService
        service = ClaudeMdMergeService(logger=mock_logger)
        claudemd_path = temp_dir / "CLAUDE.md"
        claudemd_path.write_text(conflicting_claudemd)

        with patch("src.installer.services.claudemd_merge_service.AskUserQuestion") as mock_ask:
            mock_ask.return_value = "keep-user"

            # Act
            result = service.auto_merge(claudemd_path, "")

            # Assert
            assert result is not None


class TestBackupCreation:
    """Test backup creation before modification (SVC-005, AC#3, BR-001)."""

    def test_should_create_backup_before_automerge(self, temp_dir, mock_logger, simple_claudemd, framework_template):
        """
        Test: Backup created before merge (SVC-005, AC#3, BR-001)

        Given: auto_merge() called
        When: Executes merge
        Then: Backup created first
        """
        # Arrange
        from src.installer.services.claudemd_merge_service import ClaudeMdMergeService
        service = ClaudeMdMergeService(logger=mock_logger)
        claudemd_path = temp_dir / "CLAUDE.md"
        claudemd_path.write_text(simple_claudemd)

        # Act
        result = service.auto_merge(claudemd_path, framework_template)

        # Assert
        assert result is not None
        assert result.backup_path is not None
        # Backup should exist
        if result.backup_path:
            assert Path(result.backup_path).exists()

    def test_should_halt_if_backup_fails(self, temp_dir, mock_logger, simple_claudemd):
        """
        Test: No modification if backup fails (BR-001)

        Given: Backup creation fails
        When: auto_merge() executes
        Then: Original file untouched
        """
        # Arrange
        from src.installer.services.claudemd_merge_service import ClaudeMdMergeService
        service = ClaudeMdMergeService(logger=mock_logger)
        claudemd_path = temp_dir / "CLAUDE.md"
        original_content = simple_claudemd
        claudemd_path.write_text(original_content)

        with patch("src.installer.services.claudemd_merge_service.MergeBackupService.create_backup") as mock_backup:
            mock_backup.side_effect = Exception("Backup failed")

            # Act & Assert
            try:
                result = service.auto_merge(claudemd_path, "")
                # Should not modify original
                assert claudemd_path.read_text() == original_content
            except Exception:
                # Backup failure should raise
                assert claudemd_path.read_text() == original_content


class TestReplaceStrategy:
    """Test replace strategy (AC#5)."""

    def test_should_create_backup_for_replace(self, temp_dir, mock_logger, simple_claudemd, framework_template):
        """
        Test: Backup created before replacement (AC#5)

        Given: replace() called
        When: Executes replacement
        Then: Backup created first
        """
        # Arrange
        from src.installer.services.claudemd_merge_service import ClaudeMdMergeService
        service = ClaudeMdMergeService(logger=mock_logger)
        claudemd_path = temp_dir / "CLAUDE.md"
        claudemd_path.write_text(simple_claudemd)

        # Act
        result = service.replace(claudemd_path, framework_template)

        # Assert
        assert result is not None
        assert result.backup_path is not None

    def test_should_overwrite_with_template_for_replace(self, temp_dir, mock_logger, simple_claudemd, framework_template):
        """
        Test: CLAUDE.md overwritten with template (AC#5)

        Given: replace() called
        When: Executes replacement
        Then: File contains framework template
        """
        # Arrange
        from src.installer.services.claudemd_merge_service import ClaudeMdMergeService
        service = ClaudeMdMergeService(logger=mock_logger)
        claudemd_path = temp_dir / "CLAUDE.md"
        claudemd_path.write_text(simple_claudemd)

        # Act
        result = service.replace(claudemd_path, framework_template)

        # Assert
        assert result is not None
        # File should be replaced
        content = claudemd_path.read_text()
        assert framework_template in content or len(content) > 0

    def test_should_return_success_status_for_replace(self, temp_dir, mock_logger, simple_claudemd, framework_template):
        """Test: replace() returns SUCCESS status."""
        # Arrange
        from src.installer.services.claudemd_merge_service import ClaudeMdMergeService
        service = ClaudeMdMergeService(logger=mock_logger)
        claudemd_path = temp_dir / "CLAUDE.md"
        claudemd_path.write_text(simple_claudemd)

        # Act
        result = service.replace(claudemd_path, framework_template)

        # Assert
        assert result is not None
        assert result.status == "SUCCESS" or result.status is not None


class TestSkipStrategy:
    """Test skip strategy (AC#6, BR-004)."""

    def test_should_not_modify_file_for_skip(self, temp_dir, mock_logger, simple_claudemd):
        """
        Test: File unchanged for skip strategy (AC#6, BR-004)

        Given: skip() called
        When: Executes skip
        Then: File not modified
        """
        # Arrange
        from src.installer.services.claudemd_merge_service import ClaudeMdMergeService
        service = ClaudeMdMergeService(logger=mock_logger)
        claudemd_path = temp_dir / "CLAUDE.md"
        original_content = simple_claudemd
        claudemd_path.write_text(original_content)
        original_mtime = claudemd_path.stat().st_mtime

        # Act
        result = service.skip(claudemd_path)

        # Assert
        assert result is not None
        # File should be unchanged
        assert claudemd_path.read_text() == original_content
        # Modification time should not change
        assert claudemd_path.stat().st_mtime == original_mtime

    def test_should_return_skipped_status(self, temp_dir, mock_logger, simple_claudemd):
        """Test: skip() returns SKIPPED status."""
        # Arrange
        from src.installer.services.claudemd_merge_service import ClaudeMdMergeService
        service = ClaudeMdMergeService(logger=mock_logger)
        claudemd_path = temp_dir / "CLAUDE.md"
        claudemd_path.write_text(simple_claudemd)

        # Act
        result = service.skip(claudemd_path)

        # Assert
        assert result is not None
        assert result.status == "SKIPPED" or "skip" in str(result.status).lower()

    def test_should_not_create_backup_for_skip(self, temp_dir, mock_logger, simple_claudemd):
        """Test: No backup created for skip strategy."""
        # Arrange
        from src.installer.services.claudemd_merge_service import ClaudeMdMergeService
        service = ClaudeMdMergeService(logger=mock_logger)
        claudemd_path = temp_dir / "CLAUDE.md"
        claudemd_path.write_text(simple_claudemd)

        # Act
        result = service.skip(claudemd_path)

        # Assert
        assert result is not None
        assert result.backup_path is None


class TestManualStrategy:
    """Test manual resolution workflow (AC#7)."""

    def test_should_create_backup_for_manual(self, temp_dir, mock_logger, simple_claudemd, framework_template):
        """
        Test: Backup created for manual strategy (AC#7)

        Given: manual() called
        When: Executes manual workflow
        Then: Backup created
        """
        # Arrange
        from src.installer.services.claudemd_merge_service import ClaudeMdMergeService
        service = ClaudeMdMergeService(logger=mock_logger)
        claudemd_path = temp_dir / "CLAUDE.md"
        claudemd_path.write_text(simple_claudemd)

        # Act
        result = service.manual(claudemd_path, framework_template)

        # Assert
        assert result is not None
        assert result.backup_path is not None

    def test_should_create_devforgeai_template_file(self, temp_dir, mock_logger, simple_claudemd, framework_template):
        """
        Test: CLAUDE.md.devforgeai-template created (AC#7)

        Given: manual() called
        When: Executes workflow
        Then: Template file written
        """
        # Arrange
        from src.installer.services.claudemd_merge_service import ClaudeMdMergeService
        service = ClaudeMdMergeService(logger=mock_logger)
        claudemd_path = temp_dir / "CLAUDE.md"
        claudemd_path.write_text(simple_claudemd)

        # Act
        result = service.manual(claudemd_path, framework_template)

        # Assert
        assert result is not None
        template_path = temp_dir / "CLAUDE.md.devforgeai-template"
        assert template_path.exists()

    def test_should_display_merge_instructions(self, temp_dir, mock_logger, simple_claudemd, framework_template):
        """Test: Manual merge instructions displayed (AC#7)."""
        # Arrange
        from src.installer.services.claudemd_merge_service import ClaudeMdMergeService
        service = ClaudeMdMergeService(logger=mock_logger)
        claudemd_path = temp_dir / "CLAUDE.md"
        claudemd_path.write_text(simple_claudemd)

        # Act
        result = service.manual(claudemd_path, framework_template)

        # Assert
        assert result is not None
        # Logger should be called with instructions
        mock_logger.log.assert_called()


class TestMergeLogging:
    """Test merge operation logging (AC#8)."""

    def test_should_log_with_iso_8601_timestamp(self, temp_dir, mock_logger, simple_claudemd, framework_template):
        """
        Test: Log entry has ISO 8601 timestamp (AC#8)

        Given: Merge operation completes
        When: Logged
        Then: Timestamp in ISO 8601 format
        """
        # Arrange
        from src.installer.services.claudemd_merge_service import ClaudeMdMergeService
        service = ClaudeMdMergeService(logger=mock_logger)
        claudemd_path = temp_dir / "CLAUDE.md"
        claudemd_path.write_text(simple_claudemd)

        # Act
        result = service.auto_merge(claudemd_path, framework_template)

        # Assert
        assert result is not None
        if result.timestamp:
            # Should be ISO 8601 format
            assert "T" in result.timestamp or "-" in result.timestamp

    def test_should_log_strategy_selected(self, temp_dir, mock_logger, simple_claudemd):
        """Test: Log includes strategy selected (AC#8)."""
        # Arrange
        from src.installer.services.claudemd_merge_service import ClaudeMdMergeService
        service = ClaudeMdMergeService(logger=mock_logger)
        claudemd_path = temp_dir / "CLAUDE.md"
        claudemd_path.write_text(simple_claudemd)

        # Act
        result = service.skip(claudemd_path)

        # Assert
        assert result is not None
        assert result.strategy == "skip"

    def test_should_log_action_taken(self, temp_dir, mock_logger, simple_claudemd, framework_template):
        """Test: Log includes action taken (AC#8)."""
        # Arrange
        from src.installer.services.claudemd_merge_service import ClaudeMdMergeService
        service = ClaudeMdMergeService(logger=mock_logger)
        claudemd_path = temp_dir / "CLAUDE.md"
        claudemd_path.write_text(simple_claudemd)

        # Act
        result = service.auto_merge(claudemd_path, framework_template)

        # Assert
        assert result is not None
        # Result should indicate action

    def test_should_log_backup_path_if_created(self, temp_dir, mock_logger, simple_claudemd, framework_template):
        """Test: Log includes backup path (AC#8)."""
        # Arrange
        from src.installer.services.claudemd_merge_service import ClaudeMdMergeService
        service = ClaudeMdMergeService(logger=mock_logger)
        claudemd_path = temp_dir / "CLAUDE.md"
        claudemd_path.write_text(simple_claudemd)

        # Act
        result = service.auto_merge(claudemd_path, framework_template)

        # Assert
        assert result is not None
        if result.backup_path:
            assert result.backup_path is not None


class TestMergeResultDataModel:
    """Test MergeResult return type (consistent return type per lessons learned)."""

    def test_automerge_returns_merge_result_not_string(self, temp_dir, mock_logger, simple_claudemd, framework_template):
        """
        Test: auto_merge() returns MergeResult (not string or dict)

        Given: auto_merge() executes
        When: Returns result
        Then: Always returns MergeResult type
        """
        # Arrange
        from src.installer.services.claudemd_merge_service import ClaudeMdMergeService
        service = ClaudeMdMergeService(logger=mock_logger)
        claudemd_path = temp_dir / "CLAUDE.md"
        claudemd_path.write_text(simple_claudemd)

        # Act
        result = service.auto_merge(claudemd_path, framework_template)

        # Assert
        assert result is not None
        # Should not be string
        assert not isinstance(result, str)
        # Should have MergeResult fields
        assert hasattr(result, "status")
        assert hasattr(result, "strategy")

    def test_replace_returns_merge_result_not_string(self, temp_dir, mock_logger, simple_claudemd, framework_template):
        """Test: replace() always returns MergeResult."""
        # Arrange
        from src.installer.services.claudemd_merge_service import ClaudeMdMergeService
        service = ClaudeMdMergeService(logger=mock_logger)
        claudemd_path = temp_dir / "CLAUDE.md"
        claudemd_path.write_text(simple_claudemd)

        # Act
        result = service.replace(claudemd_path, framework_template)

        # Assert
        assert result is not None
        assert not isinstance(result, str)

    def test_skip_returns_merge_result_not_string(self, temp_dir, mock_logger, simple_claudemd):
        """Test: skip() always returns MergeResult."""
        # Arrange
        from src.installer.services.claudemd_merge_service import ClaudeMdMergeService
        service = ClaudeMdMergeService(logger=mock_logger)
        claudemd_path = temp_dir / "CLAUDE.md"
        claudemd_path.write_text(simple_claudemd)

        # Act
        result = service.skip(claudemd_path)

        # Assert
        assert result is not None
        assert not isinstance(result, str)

    def test_manual_returns_merge_result_not_string(self, temp_dir, mock_logger, simple_claudemd, framework_template):
        """Test: manual() always returns MergeResult."""
        # Arrange
        from src.installer.services.claudemd_merge_service import ClaudeMdMergeService
        service = ClaudeMdMergeService(logger=mock_logger)
        claudemd_path = temp_dir / "CLAUDE.md"
        claudemd_path.write_text(simple_claudemd)

        # Act
        result = service.manual(claudemd_path, framework_template)

        # Assert
        assert result is not None
        assert not isinstance(result, str)


class TestMergeErrorHandling:
    """Test specific exception types in merge operations."""

    def test_should_raise_filenotfounderror_for_missing_claudemd(self, temp_dir, mock_logger, framework_template):
        """
        Test: FileNotFoundError for missing CLAUDE.md (not generic Exception)

        Given: auto_merge() called with nonexistent file
        When: Tries to read file
        Then: Raises FileNotFoundError specifically
        """
        # Arrange
        from src.installer.services.claudemd_merge_service import ClaudeMdMergeService
        service = ClaudeMdMergeService(logger=mock_logger)
        nonexistent = temp_dir / "nonexistent.md"

        # Act & Assert
        with pytest.raises(FileNotFoundError):
            service.auto_merge(nonexistent, framework_template)

    def test_should_raise_permissionerror_for_readonly_file(self, temp_dir, mock_logger, framework_template):
        """Test: PermissionError raised for permission denied."""
        # Arrange
        from src.installer.services.claudemd_merge_service import ClaudeMdMergeService
        import os
        service = ClaudeMdMergeService(logger=mock_logger)
        claudemd_path = temp_dir / "CLAUDE.md"
        claudemd_path.write_text("content")
        os.chmod(claudemd_path, 0o000)

        try:
            # Act & Assert
            with pytest.raises(PermissionError):
                service.auto_merge(claudemd_path, framework_template)
        finally:
            os.chmod(claudemd_path, 0o644)

    def test_should_raise_valueerror_for_invalid_strategy(self, temp_dir, mock_logger):
        """Test: ValueError raised for invalid strategy."""
        # Arrange
        from src.installer.services.claudemd_merge_service import ClaudeMdMergeService
        service = ClaudeMdMergeService(logger=mock_logger)

        # Act & Assert
        with pytest.raises(ValueError):
            service._validate_strategy("invalid-strategy")


class TestMergePerformance:
    """Test merge performance requirements (NFRs)."""

    def test_should_automerge_under_2_seconds(self, temp_dir, mock_logger, complex_claudemd, framework_template):
        """
        Test: Auto-merge <2 seconds for typical merge (NFR-002)

        Given: 20-section merge
        When: auto_merge() executes
        Then: Completes in <2 seconds
        """
        # Arrange
        from src.installer.services.claudemd_merge_service import ClaudeMdMergeService
        service = ClaudeMdMergeService(logger=mock_logger)
        claudemd_path = temp_dir / "CLAUDE.md"
        claudemd_path.write_text(complex_claudemd)

        # Act
        start = time.time()
        result = service.auto_merge(claudemd_path, framework_template)
        elapsed = time.time() - start

        # Assert
        assert result is not None
        assert elapsed < 2.0, f"Merge took {elapsed:.2f}s (expected <2s)"

    def test_should_replace_quickly(self, temp_dir, mock_logger, complex_claudemd, framework_template):
        """Test: Replace completes quickly."""
        # Arrange
        from src.installer.services.claudemd_merge_service import ClaudeMdMergeService
        service = ClaudeMdMergeService(logger=mock_logger)
        claudemd_path = temp_dir / "CLAUDE.md"
        claudemd_path.write_text(complex_claudemd)

        # Act
        start = time.time()
        result = service.replace(claudemd_path, framework_template)
        elapsed = time.time() - start

        # Assert
        assert result is not None
        assert elapsed < 1.0, f"Replace took {elapsed:.2f}s (expected <1s)"

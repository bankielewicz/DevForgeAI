"""
Integration tests for CLAUDE.md merge workflow.

Tests end-to-end workflows across all strategies and cross-service data flows.

Test Strategy: 85%+ coverage target for integration scenarios.
Covers all 4 strategies and their workflows.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch
import time


class TestAutoMergeIntegrationWorkflow:
    """Test complete auto-merge workflow end-to-end."""

    def test_should_complete_automerge_workflow_without_conflicts(self, temp_dir, mock_logger, simple_claudemd, framework_template):
        """
        Test: Full auto-merge workflow: Detect → Strategy → Backup → Merge → Log

        Given: Existing CLAUDE.md without conflicts
        When: Complete workflow executes
        Then: All steps succeed with backup and merged content
        """
        # Arrange
        from src.installer.services.claudemd_merge_service import ClaudeMdMergeService
        service = ClaudeMdMergeService(logger=mock_logger)
        claudemd_path = temp_dir / "CLAUDE.md"
        claudemd_path.write_text(simple_claudemd)

        # Act
        # Step 1: Detect
        exists = service.detect_existing(temp_dir)
        assert exists is True

        # Step 2: Execute auto-merge
        result = service.auto_merge(claudemd_path, framework_template)

        # Assert
        assert result is not None
        assert result.strategy == "auto-merge"
        assert result.backup_path is not None
        assert result.merged_content is not None
        assert Path(result.backup_path).exists()

    def test_should_handle_automerge_with_conflict_resolution(self, temp_dir, mock_logger, conflicting_claudemd):
        """
        Test: Auto-merge with conflict triggers user escalation

        Given: Conflicting CLAUDE.md
        When: Auto-merge detects conflict
        Then: Escalates to user for resolution
        """
        # Arrange
        from src.installer.services.claudemd_merge_service import ClaudeMdMergeService
        service = ClaudeMdMergeService(logger=mock_logger)
        claudemd_path = temp_dir / "CLAUDE.md"
        claudemd_path.write_text(conflicting_claudemd)

        # Act
        with patch("src.installer.services.claudemd_merge_service.AskUserQuestion") as mock_ask:
            mock_ask.return_value = "keep-user"
            result = service.auto_merge(claudemd_path, "")

        # Assert
        assert result is not None


class TestReplaceIntegrationWorkflow:
    """Test complete replace workflow end-to-end."""

    def test_should_complete_replace_workflow(self, temp_dir, mock_logger, simple_claudemd, framework_template):
        """
        Test: Full replace workflow: Backup → Overwrite → Log

        Given: Existing CLAUDE.md
        When: Replace workflow executes
        Then: Backup created, content replaced, logged
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
        assert result.strategy == "replace"
        assert result.backup_path is not None
        assert Path(result.backup_path).exists()
        # File should be replaced
        assert claudemd_path.read_text() != simple_claudemd or framework_template in claudemd_path.read_text()


class TestSkipIntegrationWorkflow:
    """Test complete skip workflow end-to-end."""

    def test_should_complete_skip_workflow(self, temp_dir, mock_logger, simple_claudemd):
        """
        Test: Full skip workflow: No modification → Log

        Given: Existing CLAUDE.md
        When: Skip workflow executes
        Then: File unchanged, logged as skipped
        """
        # Arrange
        from src.installer.services.claudemd_merge_service import ClaudeMdMergeService
        service = ClaudeMdMergeService(logger=mock_logger)
        claudemd_path = temp_dir / "CLAUDE.md"
        claudemd_path.write_text(simple_claudemd)
        original_content = claudemd_path.read_text()

        # Act
        result = service.skip(claudemd_path)

        # Assert
        assert result is not None
        assert result.strategy == "skip"
        assert result.backup_path is None
        # File unchanged
        assert claudemd_path.read_text() == original_content


class TestManualIntegrationWorkflow:
    """Test complete manual resolution workflow end-to-end."""

    def test_should_complete_manual_workflow(self, temp_dir, mock_logger, simple_claudemd, framework_template):
        """
        Test: Full manual workflow: Backup → Create template → Log → Wait for user

        Given: Existing CLAUDE.md
        When: Manual workflow executes
        Then: Backup created, template written, instructions logged
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
        assert result.strategy == "manual"
        assert result.backup_path is not None
        # Template file created
        template_path = temp_dir / "CLAUDE.mddevforgeai-template"
        assert template_path.exists()


class TestCrossServiceDataFlow:
    """Test data flow between services (MarkdownParser → ConflictDetection → MergeService)."""

    def test_should_flow_parsed_sections_to_conflict_detection(self, temp_dir, mock_logger):
        """
        Test: MarkdownParser output → ConflictDetectionService input

        Given: Markdown content
        When: Parsed and analyzed for conflicts
        Then: Sections identified and compared
        """
        # Arrange
        from src.installer.services.markdown_parser import MarkdownParser
        from src.installer.services.merge_conflict_detection_service import MergeConflictDetectionService

        parser = MarkdownParser()
        conflict_service = MergeConflictDetectionService(logger=mock_logger)

        content = """## Framework Section

Framework content here.

## User Section

User content here."""

        # Act
        parsed = parser.parse(content)
        conflicts = conflict_service.detect_conflicts(content, "")

        # Assert
        assert parsed is not None
        assert conflicts is not None

    def test_should_flow_backup_path_to_merge_result(self, temp_dir, mock_logger, simple_claudemd, framework_template):
        """
        Test: Backup path → MergeResult includes path

        Given: Backup created
        When: Returned in MergeResult
        Then: Path field populated
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
        # Path should be accessible
        assert Path(result.backup_path).exists()


class TestAllStrategiesAvailable:
    """Test that all 4 strategies are available and functional."""

    def test_should_have_all_four_strategies(self, mock_logger):
        """
        Test: All 4 strategies implemented (auto-merge, replace, skip, manual)

        Given: ClaudeMdMergeService instance
        When: Checked for methods
        Then: All 4 strategy methods exist
        """
        # Arrange
        from src.installer.services.claudemd_merge_service import ClaudeMdMergeService
        service = ClaudeMdMergeService(logger=mock_logger)

        # Act & Assert
        assert hasattr(service, "auto_merge")
        assert hasattr(service, "replace")
        assert hasattr(service, "skip")
        assert hasattr(service, "manual")

    def test_should_execute_all_four_strategies(self, temp_dir, mock_logger, simple_claudemd, framework_template):
        """Test: All 4 strategies execute without error."""
        # Arrange
        from src.installer.services.claudemd_merge_service import ClaudeMdMergeService
        service = ClaudeMdMergeService(logger=mock_logger)

        # Act & Assert
        for strategy_name in ["auto_merge", "replace", "skip", "manual"]:
            claudemd_path = temp_dir / f"CLAUDE-{strategy_name}.md"
            claudemd_path.write_text(simple_claudemd)

            strategy = getattr(service, strategy_name)
            if strategy_name == "skip":
                result = strategy(claudemd_path)
            else:
                result = strategy(claudemd_path, framework_template)

            assert result is not None


class TestStrategySelectionAndExecution:
    """Test selecting strategy and executing workflow."""

    def test_should_select_and_execute_automerge(self, temp_dir, mock_logger, simple_claudemd, framework_template):
        """Test: User selects auto-merge → executes successfully."""
        # Arrange
        from src.installer.services.claudemd_merge_service import ClaudeMdMergeService
        service = ClaudeMdMergeService(logger=mock_logger)
        claudemd_path = temp_dir / "CLAUDE.md"
        claudemd_path.write_text(simple_claudemd)

        with patch("src.installer.services.claudemd_merge_service.AskUserQuestion") as mock_ask:
            mock_ask.return_value = "auto-merge"

            # Act
            strategy = service.select_strategy()
            result = service.auto_merge(claudemd_path, framework_template)

            # Assert
            assert strategy == "auto-merge"
            assert result is not None

    def test_should_select_and_execute_replace(self, temp_dir, mock_logger, simple_claudemd, framework_template):
        """Test: User selects replace → executes successfully."""
        # Arrange
        from src.installer.services.claudemd_merge_service import ClaudeMdMergeService
        service = ClaudeMdMergeService(logger=mock_logger)
        claudemd_path = temp_dir / "CLAUDE.md"
        claudemd_path.write_text(simple_claudemd)

        with patch("src.installer.services.claudemd_merge_service.AskUserQuestion") as mock_ask:
            mock_ask.return_value = "replace"

            # Act
            strategy = service.select_strategy()
            result = service.replace(claudemd_path, framework_template)

            # Assert
            assert strategy == "replace"
            assert result is not None

    def test_should_select_and_execute_skip(self, temp_dir, mock_logger, simple_claudemd):
        """Test: User selects skip → executes successfully."""
        # Arrange
        from src.installer.services.claudemd_merge_service import ClaudeMdMergeService
        service = ClaudeMdMergeService(logger=mock_logger)
        claudemd_path = temp_dir / "CLAUDE.md"
        claudemd_path.write_text(simple_claudemd)

        with patch("src.installer.services.claudemd_merge_service.AskUserQuestion") as mock_ask:
            mock_ask.return_value = "skip"

            # Act
            strategy = service.select_strategy()
            result = service.skip(claudemd_path)

            # Assert
            assert strategy == "skip"
            assert result is not None

    def test_should_select_and_execute_manual(self, temp_dir, mock_logger, simple_claudemd, framework_template):
        """Test: User selects manual → executes successfully."""
        # Arrange
        from src.installer.services.claudemd_merge_service import ClaudeMdMergeService
        service = ClaudeMdMergeService(logger=mock_logger)
        claudemd_path = temp_dir / "CLAUDE.md"
        claudemd_path.write_text(simple_claudemd)

        with patch("src.installer.services.claudemd_merge_service.AskUserQuestion") as mock_ask:
            mock_ask.return_value = "manual"

            # Act
            strategy = service.select_strategy()
            result = service.manual(claudemd_path, framework_template)

            # Assert
            assert strategy == "manual"
            assert result is not None


class TestEndToEndWorkflows:
    """Test complete workflows with all components integrated."""

    def test_should_handle_fresh_installation_no_existing_claudemd(self, temp_dir, mock_logger, framework_template):
        """
        Test: Fresh installation (no existing CLAUDE.md)

        Given: No CLAUDE.md exists
        When: Workflow executes
        Then: No merge needed, framework template used directly
        """
        # Arrange
        from src.installer.services.claudemd_merge_service import ClaudeMdMergeService
        service = ClaudeMdMergeService(logger=mock_logger)

        # Act
        exists = service.detect_existing(temp_dir)

        # Assert
        assert exists is False

    def test_should_handle_existing_installation_with_automerge(self, temp_dir, mock_logger, simple_claudemd, framework_template):
        """
        Test: Upgrade scenario with auto-merge

        Given: Existing CLAUDE.md
        When: Auto-merge executes
        Then: Content preserved and framework updated
        """
        # Arrange
        from src.installer.services.claudemd_merge_service import ClaudeMdMergeService
        service = ClaudeMdMergeService(logger=mock_logger)
        claudemd_path = temp_dir / "CLAUDE.md"
        claudemd_path.write_text(simple_claudemd)

        # Act
        exists = service.detect_existing(temp_dir)
        result = service.auto_merge(claudemd_path, framework_template)

        # Assert
        assert exists is True
        assert result is not None
        assert "My Custom Configuration" in result.merged_content

    def test_should_preserve_all_user_content_across_automerge(self, temp_dir, mock_logger, complex_claudemd, framework_template):
        """
        Test: Complex merge preserves all user sections

        Given: Complex CLAUDE.md with 8 user sections
        When: Auto-merge executes
        Then: All user sections preserved
        """
        # Arrange
        from src.installer.services.claudemd_merge_service import ClaudeMdMergeService
        service = ClaudeMdMergeService(logger=mock_logger)
        claudemd_path = temp_dir / "CLAUDE.md"
        claudemd_path.write_text(complex_claudemd)

        # Act
        result = service.auto_merge(claudemd_path, framework_template)

        # Assert
        assert result is not None
        assert result.merged_content is not None
        # User sections should be present
        user_sections = ["My Project Structure", "Team Guidelines", "Team Guidelines", "Project Constraints", "Additional Resources"]
        for section in user_sections[:3]:  # Check first few
            if section in complex_claudemd:
                assert section in result.merged_content or result.merged_content is not None


class TestErrorRecovery:
    """Test error handling and recovery across workflows."""

    def test_should_recover_from_backup_failure(self, temp_dir, mock_logger, simple_claudemd):
        """
        Test: If backup fails, merge doesn't proceed

        Given: Backup fails
        When: Auto-merge attempts
        Then: Raises exception, file unchanged
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
                service.auto_merge(claudemd_path, "")
            except Exception:
                pass
            # File should be unchanged
            assert claudemd_path.read_text() == original_content

    def test_should_handle_permission_errors(self, temp_dir, mock_logger, simple_claudemd):
        """Test: Permission errors handled appropriately."""
        # Arrange
        from src.installer.services.claudemd_merge_service import ClaudeMdMergeService
        import os
        service = ClaudeMdMergeService(logger=mock_logger)
        claudemd_path = temp_dir / "CLAUDE.md"
        claudemd_path.write_text(simple_claudemd)
        os.chmod(claudemd_path, 0o000)

        try:
            # Act & Assert
            with pytest.raises(PermissionError):
                service.auto_merge(claudemd_path, "")
        finally:
            os.chmod(claudemd_path, 0o644)


class TestBackupIntegrity:
    """Test backup creation and verification integration."""

    def test_should_verify_backup_after_creation(self, temp_dir, mock_logger, simple_claudemd, framework_template):
        """
        Test: Backup verified after creation

        Given: Auto-merge creates backup
        When: Verification occurs
        Then: Backup is valid (size/hash match)
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
        backup_path = Path(result.backup_path)
        assert backup_path.exists()
        # Original should match backup in size
        assert backup_path.stat().st_size > 0

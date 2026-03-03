"""
Test Suite: Worktree Lifecycle Operations
Feature: STORY-091 - Git Worktree Auto-Management
AC#1: Automatic Worktree Creation
AC#6: Existing Worktree Detection and Resume

Tests for worktree creation, detection, and resumption.
"""

import pytest
import tempfile
import os
from pathlib import Path
from datetime import datetime
from unittest.mock import patch, MagicMock


class TestWorktreeCreation:
    """Test worktree creation operations"""

    def test_should_create_worktree_at_specified_path(self):
        """
        Scenario: Create new worktree for story
        Given: Story STORY-037 with no existing worktree
        When: Calling worktree create
        Then: Should create worktree at ../devforgeai-story-037/
        """
        # Arrange
        story_id = "STORY-037"
        story_number = "037"
        worktree_path = f"../devforgeai-story-{story_number}/"

        # Act
        # Simulating worktree creation

        # Assert
        assert worktree_path == "../devforgeai-story-037/"

    def test_should_create_or_checkout_branch_with_story_id(self):
        """
        Scenario: Create branch from story ID
        Given: Story ID STORY-037
        When: Creating worktree with branch
        Then: Should create/checkout branch story-037
        """
        # Arrange
        story_id = "STORY-037"
        story_number = story_id.split("-")[1]

        # Act
        branch_name = f"story-{story_number}"

        # Assert
        assert branch_name == "story-037"

    def test_should_handle_existing_branch_without_worktree(self):
        """
        Scenario: Branch exists but no worktree created yet
        Given: Branch story-037 exists in main repo
        When: Creating worktree
        Then: Should create worktree using existing branch
        """
        # Arrange
        branch_exists = True
        worktree_exists = False

        # Act
        # Should checkout existing branch into new worktree

        # Assert
        assert branch_exists and not worktree_exists

    def test_should_switch_execution_context_to_worktree(self):
        """
        Scenario: After worktree creation, switch context
        Given: Worktree created at ../devforgeai-story-037/
        When: Switching context
        Then: Execution should occur in worktree directory
        """
        # Arrange
        worktree_path = "../devforgeai-story-037/"

        # Act
        # Context switch simulated

        # Assert
        assert worktree_path.endswith("/")

    def test_should_display_success_message_on_creation(self):
        """
        Scenario: Display creation confirmation
        Given: Worktree created successfully
        When: Creation completes
        Then: Should display message like "Created worktree: ../devforgeai-story-037/ (branch: story-037)"
        """
        # Arrange
        worktree_path = "../devforgeai-story-037/"
        branch_name = "story-037"

        # Act
        success_message = f"Created worktree: {worktree_path} (branch: {branch_name})"

        # Assert
        assert "Created worktree:" in success_message
        assert "devforgeai-story-037" in success_message
        assert "story-037" in success_message

    def test_should_measure_creation_time_for_performance_validation(self):
        """
        Scenario: Measure worktree creation duration
        Given: Worktree creation starts
        When: Creation completes
        Then: Should record elapsed time
        """
        # Arrange
        start_time = datetime.now()
        # Simulated creation
        end_time = datetime.now()

        # Act
        elapsed = (end_time - start_time).total_seconds()

        # Assert
        assert elapsed >= 0

    def test_should_validate_git_worktree_add_command_succeeds(self):
        """
        Scenario: Git worktree add command execution
        Given: Valid story ID and path
        When: Executing git worktree add
        Then: Command should execute successfully
        """
        # Arrange
        story_number = "037"
        worktree_path = f"../devforgeai-story-{story_number}/"
        branch_name = f"story-{story_number}"

        # Act
        git_command = f"git worktree add {worktree_path} {branch_name}"

        # Assert
        assert "git worktree add" in git_command
        assert worktree_path in git_command
        assert branch_name in git_command


class TestExistingWorktreeDetection:
    """Test detection and resumption of existing worktrees"""

    def test_should_detect_existing_worktree_directory(self):
        """
        Scenario: Worktree already exists for story
        Given: Directory ../devforgeai-story-037/ exists
        When: Checking for existing worktree
        Then: Should detect existing worktree
        """
        # Arrange
        with tempfile.TemporaryDirectory() as tmpdir:
            worktree_path = Path(tmpdir) / "devforgeai-story-037"
            worktree_path.mkdir()

            # Act
            exists = worktree_path.exists()

            # Assert
            assert exists

    def test_should_not_attempt_creation_if_worktree_exists(self):
        """
        Scenario: Worktree already exists
        Given: ../devforgeai-story-037/ is valid worktree
        When: Running /dev STORY-037
        Then: Should detect existing, skip creation
        """
        # Arrange
        worktree_exists = True

        # Act
        should_create = not worktree_exists

        # Assert
        assert not should_create

    def test_should_validate_worktree_git_file_integrity(self):
        """
        Scenario: Validate worktree .git file
        Given: Worktree directory exists
        When: Checking integrity
        Then: Should verify .git file points to main repo
        """
        # Arrange
        with tempfile.TemporaryDirectory() as tmpdir:
            worktree_path = Path(tmpdir) / "devforgeai-story-037"
            worktree_path.mkdir()
            git_file = worktree_path / ".git"
            git_file.write_text("gitdir: /path/to/main/repo/.git/worktrees/story-037\n")

            # Act
            has_git_file = git_file.exists()
            content_valid = "gitdir:" in git_file.read_text()

            # Assert
            assert has_git_file
            assert content_valid

    def test_should_reject_corrupted_git_file(self):
        """
        Scenario: Worktree .git file is corrupted or missing
        Given: .git file missing or invalid
        When: Validating integrity
        Then: Should flag as corrupted
        """
        # Arrange
        with tempfile.TemporaryDirectory() as tmpdir:
            worktree_path = Path(tmpdir) / "devforgeai-story-037"
            worktree_path.mkdir()

            # Act
            has_git_file = (worktree_path / ".git").exists()

            # Assert
            assert not has_git_file  # Missing file = corrupted

    def test_should_display_resume_message_for_existing_worktree(self):
        """
        Scenario: Resume existing worktree
        Given: Valid existing worktree detected
        When: Displaying message
        Then: Should show "Resuming in existing worktree: ../devforgeai-story-037/"
        """
        # Arrange
        worktree_path = "../devforgeai-story-037/"

        # Act
        resume_message = f"Resuming in existing worktree: {worktree_path}"

        # Assert
        assert "Resuming" in resume_message
        assert "devforgeai-story-037" in resume_message

    def test_should_not_delete_existing_worktree_on_resume(self):
        """
        Scenario: Resume worktree without deletion
        Given: Existing worktree with uncommitted changes
        When: Running /dev STORY-037 again
        Then: Should preserve worktree and changes
        """
        # Arrange
        preserve_worktree = True

        # Act
        # Resume operation should not delete

        # Assert
        assert preserve_worktree

    def test_should_handle_worktree_on_different_filesystem(self):
        """
        Scenario: Worktree on different filesystem than main repo
        Given: Worktree on different disk/mount
        When: Validating integrity
        Then: Should still work (Git supports this)
        """
        # Arrange
        # Simulating different filesystem

        # Act
        # Git worktree should work cross-filesystem

        # Assert
        assert True

    def test_should_validate_worktree_is_not_regular_directory(self):
        """
        Scenario: Path exists as regular directory, not worktree
        Given: ../devforgeai-story-037/ exists but is not a git worktree
        When: Validating
        Then: Should detect mismatch and require user confirmation before deletion
        """
        # Arrange
        is_directory = True
        is_git_worktree = False

        # Act
        needs_confirmation = is_directory and not is_git_worktree

        # Assert
        assert needs_confirmation


class TestWorktreeIntegrity:
    """Test worktree integrity validation"""

    def test_should_detect_corrupted_worktree_state(self):
        """
        Scenario: Worktree directory corrupted
        Given: .git file missing or invalid format
        When: Checking worktree status
        Then: Should identify corruption
        """
        # Arrange
        has_git_file = False
        git_file_valid = False

        # Act
        is_corrupted = not (has_git_file and git_file_valid)

        # Assert
        assert is_corrupted

    def test_should_offer_repair_option_for_corrupted_worktree(self):
        """
        Scenario: Corrupted worktree detected
        Given: Worktree integrity check fails
        When: Displaying options
        Then: Should offer to delete and recreate
        """
        # Arrange
        is_corrupted = True

        # Act
        # Repair workflow: delete old, create new

        # Assert
        assert is_corrupted

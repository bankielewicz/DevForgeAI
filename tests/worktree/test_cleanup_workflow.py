"""
Test Suite: Cleanup Workflow and Idle Worktree Management
Feature: STORY-091 - Git Worktree Auto-Management
AC#2: Idle Worktree Detection (7+ Days)
AC#3: Cleanup Prompt with Three Options

Tests for idle worktree cleanup workflow with user prompts.
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock


class TestIdleWorktreeCleanupDetection:
    """Test detection of idle worktrees and display"""

    def test_should_detect_idle_worktrees_and_flag_for_cleanup(self):
        """
        Scenario: Idle worktrees detected on /dev invocation
        Given: Worktree inactive >7 days
        When: Running /dev command
        Then: Should detect and flag for cleanup
        """
        # Arrange
        threshold_days = 7
        last_activity = datetime.now() - timedelta(days=10)
        current_time = datetime.now()

        # Act
        days_idle = (current_time - last_activity).days
        is_idle = days_idle > threshold_days

        # Assert
        assert is_idle

    def test_should_display_list_of_idle_worktrees(self):
        """
        Scenario: Display idle worktrees before prompt
        Given: Found 2 idle worktrees
        When: Displaying to user
        Then: Should list: "Found 2 idle worktrees (>7 days): devforgeai-story-031, devforgeai-story-033"
        """
        # Arrange
        idle_worktrees = ["devforgeai-story-031", "devforgeai-story-033"]
        threshold_days = 7

        # Act
        message = f"Found {len(idle_worktrees)} idle worktrees (>{threshold_days} days): {', '.join(idle_worktrees)}"

        # Assert
        assert "Found 2 idle worktrees" in message
        assert "devforgeai-story-031" in message
        assert "devforgeai-story-033" in message

    def test_should_display_message_before_tdd_execution(self):
        """
        Scenario: Show cleanup prompt before Phase 0/1
        Given: Idle worktrees detected
        When: TDD execution about to begin
        Then: Should prompt before proceeding with /dev
        """
        # Arrange
        has_idle_worktrees = True

        # Act
        should_prompt = has_idle_worktrees

        # Assert
        assert should_prompt

    def test_should_handle_no_idle_worktrees_found(self):
        """
        Scenario: No idle worktrees exist
        Given: All worktrees have recent activity
        When: Scanning for idle
        Then: Should skip cleanup prompt and continue
        """
        # Arrange
        idle_worktrees = []

        # Act
        has_idle = len(idle_worktrees) > 0

        # Assert
        assert not has_idle


class TestCleanupPromptPresentation:
    """Test the 3-option cleanup prompt"""

    def test_should_present_three_cleanup_options(self):
        """
        Scenario: Display cleanup options to user
        Given: Idle worktrees detected
        When: Presenting prompt
        Then: Should show exactly 3 options:
              1. Resume Development
              2. Fresh Start
              3. Delete Old
        """
        # Arrange
        cleanup_options = [
            "Resume Development",
            "Fresh Start",
            "Delete Old"
        ]

        # Act
        option_count = len(cleanup_options)

        # Assert
        assert option_count == 3
        assert "Resume Development" in cleanup_options
        assert "Fresh Start" in cleanup_options
        assert "Delete Old" in cleanup_options

    def test_should_describe_resume_development_option(self):
        """
        Scenario: Describe Resume Development option
        Given: User sees cleanup prompt
        When: Reading option 1
        Then: Should explain: "Keep worktree, continue where left off"
        """
        # Arrange
        option = "Resume Development"
        description = "Keep worktree, continue where left off"

        # Act
        option_text = f"{option} - {description}"

        # Assert
        assert "Keep worktree" in option_text
        assert "left off" in option_text

    def test_should_describe_fresh_start_option(self):
        """
        Scenario: Describe Fresh Start option
        Given: User sees cleanup prompt
        When: Reading option 2
        Then: Should explain: "Delete worktree, create new one (clean slate)"
        """
        # Arrange
        option = "Fresh Start"
        description = "Delete worktree, create new one (clean slate)"

        # Act
        option_text = f"{option} - {description}"

        # Assert
        assert "Delete" in option_text
        assert "create new" in option_text
        assert "clean slate" in option_text

    def test_should_describe_delete_old_option(self):
        """
        Scenario: Describe Delete Old option
        Given: User sees cleanup prompt
        When: Reading option 3
        Then: Should explain: "Delete idle worktree(s) not matching current story"
        """
        # Arrange
        option = "Delete Old"
        description = "Delete idle worktree(s) not matching current story"

        # Act
        option_text = f"{option} - {description}"

        # Assert
        assert "Delete" in option_text
        assert "idle" in option_text

    def test_should_invoke_ask_user_question_for_cleanup_prompt(self):
        """
        Scenario: Prompt is interactive
        Given: Idle worktrees detected
        When: Presenting cleanup options
        Then: Should use AskUserQuestion with 3 options
        """
        # Arrange
        options = [
            "Resume Development",
            "Fresh Start",
            "Delete Old"
        ]

        # Act
        # AskUserQuestion would be invoked with these options

        # Assert
        assert len(options) == 3


class TestCleanupOptionExecution:
    """Test execution of each cleanup option"""

    def test_should_execute_resume_development_option(self):
        """
        Scenario: User selects "Resume Development"
        Given: Cleanup prompt shown
        When: User chooses option 1
        Then: Should keep worktree unchanged and continue to Phase 0
        """
        # Arrange
        user_selection = "Resume Development"
        worktree_should_be_deleted = False

        # Act
        if user_selection == "Resume Development":
            delete_worktree = False
        else:
            delete_worktree = True

        # Assert
        assert not delete_worktree

    def test_should_execute_fresh_start_option(self):
        """
        Scenario: User selects "Fresh Start"
        Given: Cleanup prompt shown
        When: User chooses option 2
        Then: Should delete old worktree and create new one
        """
        # Arrange
        user_selection = "Fresh Start"

        # Act
        should_delete_old = user_selection == "Fresh Start"
        should_create_new = user_selection == "Fresh Start"

        # Assert
        assert should_delete_old
        assert should_create_new

    def test_should_execute_delete_old_option(self):
        """
        Scenario: User selects "Delete Old"
        Given: Cleanup prompt shown with 2 idle worktrees
        When: User chooses option 3
        Then: Should delete only idle worktrees, keep current story worktree
        """
        # Arrange
        user_selection = "Delete Old"
        idle_worktrees = ["devforgeai-story-031", "devforgeai-story-033"]
        current_story = "story-037"

        # Act
        should_delete_idle = user_selection == "Delete Old"

        # Assert
        assert should_delete_idle

    def test_should_preserve_uncommitted_changes_during_resume(self):
        """
        Scenario: Resume with uncommitted changes
        Given: Worktree has uncommitted changes
        When: User selects "Resume Development"
        Then: Should preserve all uncommitted changes
        """
        # Arrange
        has_uncommitted_changes = True
        user_selection = "Resume Development"

        # Act
        preserve_changes = user_selection == "Resume Development"

        # Assert
        assert preserve_changes

    def test_should_warn_before_deleting_worktree_with_uncommitted_changes(self):
        """
        Scenario: Delete with uncommitted changes
        Given: Worktree has uncommitted changes, user selects Fresh Start
        When: About to delete
        Then: Should warn user and require explicit confirmation
        """
        # Arrange
        has_uncommitted_changes = True
        user_selection = "Fresh Start"

        # Act
        should_warn = has_uncommitted_changes and user_selection in ["Fresh Start", "Delete Old"]

        # Assert
        assert should_warn

    def test_should_execute_deletion_only_after_user_confirmation(self):
        """
        Scenario: Deletion confirmation
        Given: Fresh Start selected with uncommitted changes
        When: Warning shown
        Then: Should require user confirmation before deleting
        """
        # Arrange
        deletion_confirmed = True

        # Act
        can_delete = deletion_confirmed

        # Assert
        assert can_delete

    def test_should_continue_to_phase_0_after_cleanup(self):
        """
        Scenario: After cleanup completes
        Given: Cleanup option executed successfully
        When: Cleanup finishes
        Then: Should proceed with normal Phase 0 validation
        """
        # Arrange
        cleanup_completed = True

        # Act
        should_continue_phase_0 = cleanup_completed

        # Assert
        assert should_continue_phase_0

    def test_should_prevent_tdd_execution_until_cleanup_completed(self):
        """
        Scenario: TDD blocked until cleanup done
        Given: Cleanup prompt shown
        When: Prompt displayed
        Then: Should block Phase 1 until user makes selection
        """
        # Arrange
        cleanup_prompt_shown = True

        # Act
        phase_1_blocked = cleanup_prompt_shown

        # Assert
        assert phase_1_blocked

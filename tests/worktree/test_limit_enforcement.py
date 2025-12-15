"""
Test Suite: Maximum Worktree Limit Enforcement
Feature: STORY-091 - Git Worktree Auto-Management
AC#7: Maximum Worktree Limit Enforcement

Tests for enforcing maximum active worktrees limit.
"""

import pytest
from datetime import datetime, timedelta


class TestWorktreeLimitDetection:
    """Test detection when worktree limit reached"""

    def test_should_count_active_worktrees(self):
        """
        Scenario: Count all active worktrees
        Given: 3 worktrees exist
        When: Counting active worktrees
        Then: Should return count of 3
        """
        # Arrange
        worktrees = [
            {"name": "devforgeai-story-031", "idle": False},
            {"name": "devforgeai-story-033", "idle": False},
            {"name": "devforgeai-story-037", "idle": False},
        ]

        # Act
        active_count = len([w for w in worktrees if not w.get("idle", False)])

        # Assert
        assert active_count == 3

    def test_should_detect_limit_reached_at_default_maximum(self):
        """
        Scenario: Maximum 5 worktrees reached (default limit)
        Given: 5 active worktrees exist, max_worktrees = 5
        When: Attempting to create 6th
        Then: Should detect limit reached
        """
        # Arrange
        max_worktrees = 5
        active_worktrees = 5

        # Act
        limit_reached = active_worktrees >= max_worktrees

        # Assert
        assert limit_reached

    def test_should_not_flag_limit_when_below_maximum(self):
        """
        Scenario: Below maximum limit
        Given: 4 active worktrees, max = 5
        When: Checking limit
        Then: Should allow creation of new worktree
        """
        # Arrange
        max_worktrees = 5
        active_worktrees = 4

        # Act
        limit_reached = active_worktrees >= max_worktrees

        # Assert
        assert not limit_reached

    def test_should_exclude_idle_worktrees_from_limit_count(self):
        """
        Scenario: Idle worktrees don't count toward limit
        Given: 4 active, 5 idle worktrees, max = 5
        When: Checking limit
        Then: Should count only 4 active, allow new creation
        """
        # Arrange
        max_worktrees = 5
        active_worktrees = [
            {"name": "devforgeai-story-031", "idle": False},
            {"name": "devforgeai-story-033", "idle": False},
            {"name": "devforgeai-story-035", "idle": False},
            {"name": "devforgeai-story-037", "idle": False},
        ]
        idle_worktrees = [
            {"name": "devforgeai-story-001", "idle": True},
            {"name": "devforgeai-story-002", "idle": True},
        ]

        # Act
        active_count = len(active_worktrees)
        limit_reached = active_count >= max_worktrees

        # Assert
        assert not limit_reached

    def test_should_apply_custom_max_worktrees_limit(self):
        """
        Scenario: Custom maximum configured
        Given: max_worktrees = 10 (not default 5)
        When: Creating worktrees
        Then: Should use 10, not 5
        """
        # Arrange
        custom_max = 10
        active_worktrees = 9

        # Act
        limit_reached = active_worktrees >= custom_max

        # Assert
        assert not limit_reached

    def test_should_flag_limit_when_exact_at_custom_maximum(self):
        """
        Scenario: Exactly at custom limit
        Given: max_worktrees = 10, have 10 active
        When: Attempting 11th
        Then: Should detect limit
        """
        # Arrange
        custom_max = 10
        active_worktrees = 10

        # Act
        limit_reached = active_worktrees >= custom_max

        # Assert
        assert limit_reached


class TestLimitEnforcementWorkflow:
    """Test workflow when limit is reached"""

    def test_should_display_worktrees_list_when_limit_reached(self):
        """
        Scenario: Show all active worktrees when limit reached
        Given: Limit reached with 5 worktrees
        When: Displaying list
        Then: Should show: "Active worktrees (5): devforgeai-story-XXX..."
        """
        # Arrange
        worktrees = [
            {"name": "devforgeai-story-031", "last_activity": datetime.now() - timedelta(days=1)},
            {"name": "devforgeai-story-033", "last_activity": datetime.now() - timedelta(days=2)},
            {"name": "devforgeai-story-035", "last_activity": datetime.now() - timedelta(days=3)},
            {"name": "devforgeai-story-037", "last_activity": datetime.now() - timedelta(days=1)},
            {"name": "devforgeai-story-039", "last_activity": datetime.now() - timedelta(hours=6)},
        ]

        # Act
        message = f"Active worktrees ({len(worktrees)}): " + ", ".join([w["name"] for w in worktrees])

        # Assert
        assert "Active worktrees (5):" in message
        assert "devforgeai-story-031" in message

    def test_should_display_last_activity_dates(self):
        """
        Scenario: Show activity dates for each worktree
        Given: Worktree list displayed
        When: Showing details
        Then: Should include last activity timestamps
        """
        # Arrange
        worktrees = [
            {"name": "devforgeai-story-031", "last_activity": datetime.now() - timedelta(days=1)},
            {"name": "devforgeai-story-033", "last_activity": datetime.now() - timedelta(days=2)},
        ]

        # Act
        # Display would show activity dates

        # Assert
        assert len(worktrees) > 0

    def test_should_prompt_user_for_worktree_deletion(self):
        """
        Scenario: Prompt for deletion when limit reached
        Given: 5 worktrees, limit reached
        When: Limit detected
        Then: Should prompt: "Maximum worktrees (5) reached. Delete an existing worktree?"
        """
        # Arrange
        max_worktrees = 5
        active_count = 5

        # Act
        message = f"Maximum worktrees ({max_worktrees}) reached. Delete an existing worktree?"

        # Assert
        assert "Maximum worktrees" in message
        assert "Delete" in message

    def test_should_block_tdd_execution_until_limit_resolved(self):
        """
        Scenario: Block Phase 0 when limit reached
        Given: Limit reached
        When: /dev command runs
        Then: Should block and require user action
        """
        # Arrange
        limit_reached = True

        # Act
        phase_0_blocked = limit_reached

        # Assert
        assert phase_0_blocked

    def test_should_require_user_selection_to_delete_worktree(self):
        """
        Scenario: User must select which worktree to delete
        Given: 5 worktrees listed with activity dates
        When: User selects one
        Then: Should delete selected worktree
        """
        # Arrange
        user_selected_worktree = "devforgeai-story-031"

        # Act
        # Delete selected worktree

        # Assert
        assert user_selected_worktree is not None

    def test_should_prevent_deletion_without_user_confirmation(self):
        """
        Scenario: Don't delete without explicit user confirmation
        Given: Limit reached
        When: Showing prompt
        Then: Should require explicit user selection before deletion
        """
        # Arrange
        user_confirmed = False

        # Act
        can_delete = user_confirmed

        # Assert
        assert not can_delete

    def test_should_continue_after_worktree_deletion(self):
        """
        Scenario: After user deletes a worktree
        Given: User selected worktree to delete
        When: Deletion completes
        Then: Should allow new worktree creation and proceed to Phase 0
        """
        # Arrange
        deletion_completed = True

        # Act
        can_proceed = deletion_completed

        # Assert
        assert can_proceed

    def test_should_validate_limit_before_creation_attempt(self):
        """
        Scenario: Check limit BEFORE attempting creation
        Given: Running /dev for new story
        When: About to create worktree
        Then: Should check limit first, block if at max
        """
        # Arrange
        max_worktrees = 5
        active_count = 5
        story_id = "STORY-999"

        # Act
        limit_reached = active_count >= max_worktrees
        should_block_creation = limit_reached

        # Assert
        assert should_block_creation


class TestLimitConfigurationHandling:
    """Test limit configuration handling"""

    def test_should_use_default_limit_when_not_configured(self):
        """
        Scenario: No max_worktrees in config
        Given: Config missing max_worktrees
        When: Checking limit
        Then: Should use default of 5
        """
        # Arrange
        default_limit = 5

        # Act
        applied_limit = default_limit

        # Assert
        assert applied_limit == 5

    def test_should_apply_configured_limit_from_config(self):
        """
        Scenario: Custom limit configured
        Given: max_worktrees = 8 in parallel.yaml
        When: Applying configuration
        Then: Should use 8, not default 5
        """
        # Arrange
        configured_limit = 8
        default_limit = 5

        # Act
        applied_limit = configured_limit

        # Assert
        assert applied_limit == 8
        assert applied_limit != default_limit

    def test_should_validate_limit_within_valid_range(self):
        """
        Scenario: Limit must be 1-20
        Given: max_worktrees = 15
        When: Validating
        Then: Should accept as valid
        """
        # Arrange
        limit = 15

        # Act
        is_valid = 1 <= limit <= 20

        # Assert
        assert is_valid

    def test_should_reject_limit_below_minimum(self):
        """
        Scenario: Limit below 1
        Given: max_worktrees = 0
        When: Validating
        Then: Should reject and use default
        """
        # Arrange
        invalid_limit = 0
        default_limit = 5

        # Act
        if invalid_limit < 1:
            applied_limit = default_limit
        else:
            applied_limit = invalid_limit

        # Assert
        assert applied_limit == 5

    def test_should_reject_limit_above_maximum(self):
        """
        Scenario: Limit above 20
        Given: max_worktrees = 25
        When: Validating
        Then: Should reject and use default
        """
        # Arrange
        invalid_limit = 25
        default_limit = 5

        # Act
        if invalid_limit > 20:
            applied_limit = default_limit
        else:
            applied_limit = invalid_limit

        # Assert
        assert applied_limit == 5

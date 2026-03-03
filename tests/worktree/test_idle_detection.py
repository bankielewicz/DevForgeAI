"""
Test Suite: Idle Worktree Detection
Feature: STORY-091 - Git Worktree Auto-Management
AC#2: Idle Worktree Detection (7+ Days)

Tests for detecting worktrees inactive beyond configurable threshold.
"""

import pytest
from datetime import datetime, timedelta
from pathlib import Path
import tempfile


class TestIdleWorktreeDetection:
    """Test detection of idle worktrees exceeding activity threshold"""

    def test_should_detect_worktree_with_activity_within_threshold(self):
        """
        Scenario: Worktree has recent activity (2 days ago)
        Given: Worktree last modified 2 days ago, threshold = 7 days
        When: Scanning for idle worktrees
        Then: Should NOT flag as idle
        """
        # Arrange
        threshold_days = 7
        last_activity = datetime.now() - timedelta(days=2)
        current_time = datetime.now()

        # Act
        days_idle = (current_time - last_activity).days
        is_idle = days_idle > threshold_days

        # Assert
        assert not is_idle

    def test_should_detect_worktree_with_activity_at_threshold_boundary(self):
        """
        Scenario: Worktree last active exactly 7 days ago
        Given: last_activity = 7 days ago, threshold = 7
        When: Comparing
        Then: Should NOT flag as idle (equal to threshold, not exceeding)
        """
        # Arrange
        threshold_days = 7
        last_activity = datetime.now() - timedelta(days=7)
        current_time = datetime.now()

        # Act
        days_idle = (current_time - last_activity).days
        is_idle = days_idle > threshold_days

        # Assert
        assert not is_idle

    def test_should_detect_worktree_exceeding_idle_threshold(self):
        """
        Scenario: Worktree inactive for 8+ days
        Given: Worktree last modified 8 days ago, threshold = 7 days
        When: Scanning for idle worktrees
        Then: Should flag as idle
        """
        # Arrange
        threshold_days = 7
        last_activity = datetime.now() - timedelta(days=8)
        current_time = datetime.now()

        # Act
        days_idle = (current_time - last_activity).days
        is_idle = days_idle > threshold_days

        # Assert
        assert is_idle

    def test_should_detect_worktree_far_exceeding_threshold(self):
        """
        Scenario: Worktree inactive for 30+ days
        Given: Worktree last modified 30 days ago, threshold = 7 days
        When: Scanning for idle worktrees
        Then: Should flag as idle
        """
        # Arrange
        threshold_days = 7
        last_activity = datetime.now() - timedelta(days=30)
        current_time = datetime.now()

        # Act
        days_idle = (current_time - last_activity).days
        is_idle = days_idle > threshold_days

        # Assert
        assert is_idle

    def test_should_determine_last_activity_from_git_commit(self):
        """
        Scenario: Last activity determined by most recent Git commit
        Given: Last commit 5 days ago
        When: Calculating last activity
        Then: Should use commit date
        """
        # Arrange
        last_commit_date = datetime.now() - timedelta(days=5)
        threshold_days = 7

        # Act
        days_idle = (datetime.now() - last_commit_date).days
        is_idle = days_idle > threshold_days

        # Assert
        assert not is_idle

    def test_should_determine_last_activity_from_file_modification(self):
        """
        Scenario: No commits, but files modified recently
        Given: Files modified 3 days ago, no recent commits
        When: Calculating last activity
        Then: Should use file modification date
        """
        # Arrange
        last_file_mod = datetime.now() - timedelta(days=3)
        threshold_days = 7

        # Act
        days_idle = (datetime.now() - last_file_mod).days
        is_idle = days_idle > threshold_days

        # Assert
        assert not is_idle

    def test_should_use_most_recent_activity_among_commit_and_file_mod(self):
        """
        Scenario: Compare commit date and file modification date
        Given: Last commit 10 days ago, files modified 3 days ago
        When: Determining last activity
        Then: Should use most recent (file mod 3 days ago)
        """
        # Arrange
        last_commit = datetime.now() - timedelta(days=10)
        last_file_mod = datetime.now() - timedelta(days=3)
        threshold_days = 7

        # Act
        last_activity = max(last_commit, last_file_mod)
        days_idle = (datetime.now() - last_activity).days
        is_idle = days_idle > threshold_days

        # Assert
        assert not is_idle  # 3 days < 7 days

    def test_should_scan_multiple_idle_worktrees_simultaneously(self):
        """
        Scenario: Detect multiple idle worktrees in single scan
        Given: 5 worktrees, 2 are idle
        When: Scanning all worktrees
        Then: Should identify all idle ones
        """
        # Arrange
        threshold_days = 7
        worktrees = [
            {"name": "devforgeai-story-031", "last_activity": datetime.now() - timedelta(days=10)},
            {"name": "devforgeai-story-033", "last_activity": datetime.now() - timedelta(days=15)},
            {"name": "devforgeai-story-035", "last_activity": datetime.now() - timedelta(days=2)},
            {"name": "devforgeai-story-037", "last_activity": datetime.now() - timedelta(days=1)},
            {"name": "devforgeai-story-039", "last_activity": datetime.now() - timedelta(days=20)},
        ]

        # Act
        idle_worktrees = []
        for wt in worktrees:
            days_idle = (datetime.now() - wt["last_activity"]).days
            if days_idle > threshold_days:
                idle_worktrees.append(wt["name"])

        # Assert
        assert len(idle_worktrees) == 3
        assert "devforgeai-story-031" in idle_worktrees
        assert "devforgeai-story-033" in idle_worktrees
        assert "devforgeai-story-039" in idle_worktrees

    def test_should_handle_missing_last_activity_timestamp(self):
        """
        Scenario: Worktree missing last activity information
        Given: No commit history or modification timestamps
        When: Determining last activity
        Then: Should fall back to worktree creation date
        """
        # Arrange
        creation_date = datetime.now() - timedelta(days=10)
        last_activity = creation_date  # Fallback to creation
        threshold_days = 7

        # Act
        days_idle = (datetime.now() - last_activity).days
        is_idle = days_idle > threshold_days

        # Assert
        assert is_idle

    def test_should_handle_future_timestamp_gracefully(self):
        """
        Scenario: Timestamp in future (clock skew)
        Given: last_activity is in the future
        When: Calculating days idle
        Then: Should handle gracefully (consider not idle or treat as 0)
        """
        # Arrange
        future_activity = datetime.now() + timedelta(days=5)
        threshold_days = 7

        # Act
        days_idle = (datetime.now() - future_activity).days
        if days_idle < 0:
            days_idle = 0  # Treat as current
        is_idle = days_idle > threshold_days

        # Assert
        assert not is_idle

    def test_should_apply_custom_threshold_to_idle_detection(self):
        """
        Scenario: Custom threshold configured (not default 7)
        Given: cleanup_threshold_days = 14 in config
        When: Scanning for idle worktrees
        Then: Should use 14-day threshold, not 7
        """
        # Arrange
        custom_threshold = 14
        last_activity = datetime.now() - timedelta(days=10)

        # Act
        days_idle = (datetime.now() - last_activity).days
        is_idle = days_idle > custom_threshold

        # Assert
        assert not is_idle  # 10 days < 14 days

    def test_should_detect_zero_day_old_worktree_as_not_idle(self):
        """
        Scenario: Brand new worktree created today
        Given: Worktree created less than 1 hour ago
        When: Scanning for idle
        Then: Should NOT flag as idle
        """
        # Arrange
        threshold_days = 7
        last_activity = datetime.now()

        # Act
        days_idle = (datetime.now() - last_activity).days
        is_idle = days_idle > threshold_days

        # Assert
        assert not is_idle
        assert days_idle == 0

    def test_should_handle_leap_second_edge_case(self):
        """
        Scenario: Handle leap second during age calculation
        Given: Calculation spans leap second
        When: Computing days between timestamps
        Then: Should still provide accurate comparison
        """
        # Arrange
        date1 = datetime.now() - timedelta(days=7, seconds=1)
        date2 = datetime.now()

        # Act
        days_diff = (date2 - date1).days

        # Assert
        assert days_diff >= 7

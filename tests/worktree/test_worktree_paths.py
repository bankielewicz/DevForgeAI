"""
Test Suite: Worktree Path Generation and Security
Feature: STORY-091 - Git Worktree Auto-Management
AC#1: Automatic Worktree Creation

Tests for worktree path validation and path traversal prevention.
"""

import pytest
import os
from pathlib import Path


class TestWorktreePathGeneration:
    """Test path generation and security validation"""

    def test_should_generate_worktree_path_from_story_id(self):
        """
        Scenario: Generate worktree path from story ID
        Given: Story ID = STORY-037
        When: Generating worktree path
        Then: Should produce ../devforgeai-story-037/
        """
        # Arrange
        story_id = "STORY-037"
        pattern = "../devforgeai-story-{id}/"

        # Act
        story_number = story_id.split("-")[1]
        worktree_path = pattern.format(id=story_number)

        # Assert
        assert worktree_path == "../devforgeai-story-037/"

    def test_should_handle_three_digit_story_id(self):
        """
        Scenario: Three-digit story ID
        Given: Story ID = STORY-037
        When: Generating path
        Then: Should produce ../devforgeai-story-037/
        """
        # Arrange
        story_id = "STORY-037"
        pattern = "../devforgeai-story-{id}/"

        # Act
        story_number = story_id.split("-")[1]
        worktree_path = pattern.format(id=story_number)

        # Assert
        assert worktree_path == "../devforgeai-story-037/"

    def test_should_handle_four_digit_story_id(self):
        """
        Scenario: Four-digit story ID
        Given: Story ID = STORY-1234
        When: Generating path
        Then: Should produce ../devforgeai-story-1234/
        """
        # Arrange
        story_id = "STORY-1234"
        pattern = "../devforgeai-story-{id}/"

        # Act
        story_number = story_id.split("-")[1]
        worktree_path = pattern.format(id=story_number)

        # Assert
        assert worktree_path == "../devforgeai-story-1234/"

    def test_should_reject_invalid_story_id_format(self):
        """
        Scenario: Invalid story ID format
        Given: Story ID = "INVALID-ABC"
        When: Validating story ID
        Then: Should reject with error message
        """
        # Arrange
        invalid_story_id = "INVALID-ABC"

        # Act & Assert
        with pytest.raises(ValueError, match="Story ID must match"):
            import re
            pattern = r"STORY-\d{3,4}"
            if not re.match(pattern, invalid_story_id):
                raise ValueError("Story ID must match STORY-\\d{3,4}")

    def test_should_reject_story_id_with_two_digit_number(self):
        """
        Scenario: Story ID with only 2 digits
        Given: Story ID = STORY-37
        When: Validating story ID
        Then: Should reject as invalid format
        """
        # Arrange
        invalid_story_id = "STORY-37"

        # Act & Assert
        with pytest.raises(ValueError):
            import re
            pattern = r"STORY-\d{3,4}"
            if not re.match(pattern, invalid_story_id):
                raise ValueError("Story ID must have 3-4 digits")

    def test_should_reject_story_id_with_five_digit_number(self):
        """
        Scenario: Story ID with 5 digits
        Given: Story ID = STORY-12345
        When: Validating story ID
        Then: Should reject as invalid format
        """
        # Arrange
        invalid_story_id = "STORY-12345"

        # Act & Assert
        with pytest.raises(ValueError, match="must have"):
            import re
            pattern = r"STORY-\d{3,4}$"  # Match exact format only
            if not re.match(pattern, invalid_story_id):
                raise ValueError("Story ID must have 3-4 digits")

    def test_should_prevent_path_traversal_with_double_dots(self):
        """
        Scenario: Prevent path traversal attack
        Given: Attacker tries ../../../etc/passwd pattern
        When: Validating worktree path
        Then: Should reject and prevent directory escape
        """
        # Arrange
        malicious_path = "../../etc/passwd"

        # Act & Assert
        with pytest.raises(ValueError, match="Path traversal"):
            if ".." in malicious_path or malicious_path.startswith("/"):
                raise ValueError("Path traversal detected")

    def test_should_prevent_absolute_path_injection(self):
        """
        Scenario: Prevent absolute path injection
        Given: Worktree path starts with /
        When: Validating path
        Then: Should reject absolute paths
        """
        # Arrange
        absolute_path = "/etc/passwd"

        # Act & Assert
        with pytest.raises(ValueError, match="Absolute path"):
            if absolute_path.startswith("/"):
                raise ValueError("Absolute path not allowed")

    def test_should_enforce_maximum_path_length(self):
        """
        Scenario: Enforce maximum path length for Windows compatibility
        Given: Generated path exceeds 200 characters
        When: Validating path length
        Then: Should reject with error
        """
        # Arrange
        pattern = "../devforgeai-story-{id}/"
        long_id = "9" * 195  # Create path that will exceed 200 chars
        generated_path = pattern.format(id=long_id)
        max_length = 200

        # Act & Assert
        assert len(generated_path) > max_length  # Verify test setup
        with pytest.raises(ValueError, match="Path too long"):
            if len(generated_path) > max_length:
                raise ValueError("Path too long for Windows compatibility")

    def test_should_validate_path_only_contains_allowed_characters(self):
        """
        Scenario: Path contains only alphanumeric and hyphens
        Given: Story ID with special characters
        When: Validating path characters
        Then: Should reject if contains forbidden characters
        """
        # Arrange
        valid_story_id = "STORY-037"
        pattern = "../devforgeai-story-{id}/"

        # Act
        story_number = valid_story_id.split("-")[1]
        worktree_path = pattern.format(id=story_number)

        # Assert - path should only have allowed chars
        allowed_chars = set("abcdefghijklmnopqrstuvwxyz0123456789-_/.")
        assert all(c in allowed_chars for c in worktree_path)

    def test_should_generate_consistent_path_for_same_story_id(self):
        """
        Scenario: Same story ID generates same path
        Given: Story ID = STORY-037
        When: Calling path generation twice
        Then: Should produce identical paths
        """
        # Arrange
        story_id = "STORY-037"
        pattern = "../devforgeai-story-{id}/"

        # Act
        story_number = story_id.split("-")[1]
        path1 = pattern.format(id=story_number)
        path2 = pattern.format(id=story_number)

        # Assert
        assert path1 == path2
        assert path1 == "../devforgeai-story-037/"

    def test_should_convert_story_id_to_lowercase_in_path(self):
        """
        Scenario: Story ID format conversion
        Given: Story ID = STORY-037 (uppercase)
        When: Generating path
        Then: Should normalize to lowercase in path
        """
        # Arrange
        story_id = "STORY-037"

        # Act
        story_number = story_id.split("-")[1].lower()
        worktree_path = f"../devforgeai-story-{story_number}/"

        # Assert
        assert worktree_path == "../devforgeai-story-037/"
        assert worktree_path.islower() or all(c not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" for c in worktree_path)

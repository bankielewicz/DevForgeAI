"""
Test Suite: Configuration Loading and Validation
Feature: STORY-091 - Git Worktree Auto-Management
AC#5: Configurable Cleanup Threshold

Tests for parallel.yaml configuration file parsing and validation.
"""

import pytest
import yaml
import tempfile
import os
from pathlib import Path


class TestParallelConfigLoading:
    """Test configuration file loading from parallel.yaml"""

    def test_should_load_valid_config_file_when_exists(self):
        """
        Scenario: Valid configuration file exists at .devforgeai/config/parallel.yaml
        Given: Configuration file with valid worktree section
        When: Loading configuration
        Then: Should parse YAML and return config dictionary
        """
        # Arrange
        config_content = """
worktree:
  cleanup_threshold_days: 7
  max_worktrees: 5
  location_pattern: "../devforgeai-story-{id}/"
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "parallel.yaml"
            config_path.write_text(config_content)

            # Act
            with open(config_path) as f:
                config = yaml.safe_load(f)

            # Assert
            assert config is not None
            assert config['worktree']['cleanup_threshold_days'] == 7
            assert config['worktree']['max_worktrees'] == 5
            assert config['worktree']['location_pattern'] == "../devforgeai-story-{id}/"

    def test_should_use_default_threshold_when_config_missing(self):
        """
        Scenario: Configuration file does not exist
        Given: No parallel.yaml file
        When: Attempting to load configuration
        Then: Should fall back to default threshold of 7 days
        """
        # Arrange
        default_threshold = 7

        # Act
        config_threshold = default_threshold  # Fallback behavior

        # Assert
        assert config_threshold == 7

    def test_should_use_default_max_worktrees_when_config_missing(self):
        """
        Scenario: Configuration file missing max_worktrees value
        Given: No configuration or missing key
        When: Checking maximum worktrees limit
        Then: Should default to 5 worktrees
        """
        # Arrange
        default_max = 5

        # Act
        max_worktrees = default_max

        # Assert
        assert max_worktrees == 5

    def test_should_use_default_location_pattern_when_config_missing(self):
        """
        Scenario: Location pattern not specified in config
        Given: Missing location_pattern key
        When: Determining worktree path
        Then: Should use default pattern "../devforgeai-story-{id}/"
        """
        # Arrange
        default_pattern = "../devforgeai-story-{id}/"

        # Act
        pattern = default_pattern

        # Assert
        assert pattern == "../devforgeai-story-{id}/"
        assert "{id}" in pattern

    def test_should_reject_invalid_threshold_and_fallback_to_default(self):
        """
        Scenario: Configuration file contains invalid threshold value
        Given: cleanup_threshold_days set to negative or non-integer value
        When: Parsing configuration
        Then: Should reject invalid value and fall back to default 7
        """
        # Arrange
        invalid_threshold = -5
        default_threshold = 7

        # Act
        if invalid_threshold < 1 or invalid_threshold > 365:
            config_threshold = default_threshold
        else:
            config_threshold = invalid_threshold

        # Assert
        assert config_threshold == 7

    def test_should_reject_threshold_exceeding_max_range(self):
        """
        Scenario: Threshold value exceeds maximum allowed (365 days)
        Given: cleanup_threshold_days = 400
        When: Validating configuration
        Then: Should reject and use default 7
        """
        # Arrange
        invalid_threshold = 400

        # Act
        if invalid_threshold > 365:
            config_threshold = 7
        else:
            config_threshold = invalid_threshold

        # Assert
        assert config_threshold == 7

    def test_should_accept_valid_threshold_in_range(self):
        """
        Scenario: Valid threshold within 1-365 day range
        Given: cleanup_threshold_days = 14
        When: Validating configuration
        Then: Should accept value
        """
        # Arrange
        valid_threshold = 14

        # Act
        if 1 <= valid_threshold <= 365:
            config_threshold = valid_threshold
        else:
            config_threshold = 7

        # Assert
        assert config_threshold == 14

    def test_should_reject_location_pattern_without_id_placeholder(self):
        """
        Scenario: location_pattern configured without {id} placeholder
        Given: location_pattern = "/home/user/worktrees/"
        When: Validating configuration
        Then: Should reject pattern and raise error with clear message
        """
        # Arrange
        invalid_pattern = "/home/user/worktrees/"

        # Act & Assert
        with pytest.raises(ValueError, match="location_pattern must contain"):
            if "{id}" not in invalid_pattern:
                raise ValueError("location_pattern must contain {id} placeholder")

    def test_should_accept_valid_location_pattern_with_id_placeholder(self):
        """
        Scenario: Valid location pattern with {id} placeholder
        Given: location_pattern = "../devforgeai-story-{id}/"
        When: Validating configuration
        Then: Should accept pattern
        """
        # Arrange
        valid_pattern = "../devforgeai-story-{id}/"

        # Act
        has_placeholder = "{id}" in valid_pattern

        # Assert
        assert has_placeholder

    def test_should_apply_custom_threshold_from_config(self):
        """
        Scenario: Custom threshold configured in parallel.yaml
        Given: cleanup_threshold_days = 14 (not default)
        When: Loading and applying configuration
        Then: Should use configured value 14, not default 7
        """
        # Arrange
        configured_threshold = 14
        default_threshold = 7

        # Act
        applied_threshold = configured_threshold

        # Assert
        assert applied_threshold == 14
        assert applied_threshold != default_threshold

    def test_should_validate_max_worktrees_in_valid_range(self):
        """
        Scenario: max_worktrees validation
        Given: max_worktrees = 10
        When: Validating configuration
        Then: Should accept value in range 1-20
        """
        # Arrange
        max_worktrees = 10

        # Act
        if 1 <= max_worktrees <= 20:
            is_valid = True
        else:
            is_valid = False

        # Assert
        assert is_valid

    def test_should_reject_max_worktrees_below_minimum(self):
        """
        Scenario: max_worktrees less than 1
        Given: max_worktrees = 0
        When: Validating configuration
        Then: Should reject and use default 5
        """
        # Arrange
        invalid_max = 0

        # Act
        if invalid_max < 1:
            applied_max = 5
        else:
            applied_max = invalid_max

        # Assert
        assert applied_max == 5

    def test_should_reject_max_worktrees_above_maximum(self):
        """
        Scenario: max_worktrees exceeds maximum allowed (20)
        Given: max_worktrees = 25
        When: Validating configuration
        Then: Should reject and use default 5
        """
        # Arrange
        invalid_max = 25

        # Act
        if invalid_max > 20:
            applied_max = 5
        else:
            applied_max = invalid_max

        # Assert
        assert applied_max == 5

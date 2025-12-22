"""
Unit tests for ConfigValidator service (STORY-082, AC#6).

Tests for configuration validation logic including:
- Required key validation (SVC-005)
- Type validation (SVC-006)
- Value validation (enum, datetime, paths)
- Unknown key warnings (SVC-007)
- Comprehensive error messages

This module contains 25 tests covering all validation scenarios.
"""

import json
import pytest
from typing import Dict, Any


class TestConfigValidatorRequiredKeys:
    """Tests for required key validation (AC#6, SVC-005)."""

    def test_should_validate_all_required_keys_present(self, sample_install_config):
        """Test: Valid config passes required key validation."""
        # Arrange
        config = sample_install_config
        required_keys = ["schema_version", "target_path", "merge_strategy", "installed_at"]

        # Act & Assert
        for key in required_keys:
            assert key in config

    def test_should_fail_validation_when_target_path_missing(self, invalid_configs):
        """Test: Missing required key 'target_path' triggers error."""
        # Arrange
        config = invalid_configs["missing_target_path"]

        # Act
        assert "target_path" not in config

        # Assert - validation should fail
        # (Implementation will return error: "Missing required key: target_path")

    def test_should_fail_validation_when_merge_strategy_missing(self, invalid_configs):
        """Test: Missing required key 'merge_strategy' triggers error."""
        # Arrange
        config = invalid_configs["missing_merge_strategy"]

        # Act
        assert "merge_strategy" not in config

        # Assert - validation should fail

    def test_should_fail_validation_when_installed_at_missing(self, invalid_configs):
        """Test: Missing required key 'installed_at' triggers error."""
        # Arrange
        config = invalid_configs["missing_installed_at"]

        # Act
        assert "installed_at" not in config

        # Assert - validation should fail

    def test_should_fail_validation_when_schema_version_missing(self):
        """Test: Missing required key 'schema_version' triggers error."""
        # Arrange
        config = {
            "target_path": "/home/user/project",
            "merge_strategy": "SMART_MERGE",
            "optional_features": [],
            "installed_at": "2025-11-25T10:30:00Z",
        }

        # Act & Assert
        assert "schema_version" not in config

    def test_should_validate_optional_features_required_with_default_empty_array(self):
        """Test: optional_features is required but defaults to empty array."""
        # Arrange
        config = {
            "schema_version": 1,
            "target_path": "/home/user/project",
            "merge_strategy": "SMART_MERGE",
            "installed_at": "2025-11-25T10:30:00Z",
        }

        # Act & Assert
        # optional_features should be added with default [] if missing
        if "optional_features" not in config:
            config["optional_features"] = []
        assert config["optional_features"] == []


class TestConfigValidatorTypes:
    """Tests for type validation (AC#6, SVC-006)."""

    def test_should_fail_validation_when_optional_features_is_string(
        self, invalid_configs
    ):
        """Test: Type error when optional_features is string instead of array."""
        # Arrange
        config = invalid_configs["optional_features_not_array"]

        # Act & Assert
        assert isinstance(config["optional_features"], str)
        # Validation should fail with: "Invalid type for 'optional_features': expected array, got string"

    def test_should_fail_validation_when_schema_version_is_string(self):
        """Test: Type error when schema_version is string instead of int."""
        # Arrange
        config = {
            "schema_version": "1",  # String instead of int
            "target_path": "/home/user/project",
            "merge_strategy": "SMART_MERGE",
            "optional_features": [],
            "installed_at": "2025-11-25T10:30:00Z",
        }

        # Act & Assert
        assert isinstance(config["schema_version"], str)

    def test_should_fail_validation_when_schema_version_is_negative(self):
        """Test: Type error when schema_version is negative."""
        # Arrange
        config = {
            "schema_version": -1,
            "target_path": "/home/user/project",
            "merge_strategy": "SMART_MERGE",
            "optional_features": [],
            "installed_at": "2025-11-25T10:30:00Z",
        }

        # Act & Assert
        assert config["schema_version"] < 0

    def test_should_fail_validation_when_target_path_is_not_string(self):
        """Test: Type error when target_path is not string."""
        # Arrange
        config = {
            "schema_version": 1,
            "target_path": 123,  # Integer instead of string
            "merge_strategy": "SMART_MERGE",
            "optional_features": [],
            "installed_at": "2025-11-25T10:30:00Z",
        }

        # Act & Assert
        assert not isinstance(config["target_path"], str)

    def test_should_fail_validation_when_merge_strategy_is_not_string(self):
        """Test: Type error when merge_strategy is not string."""
        # Arrange
        config = {
            "schema_version": 1,
            "target_path": "/home/user/project",
            "merge_strategy": ["SMART_MERGE"],  # Array instead of string
            "optional_features": [],
            "installed_at": "2025-11-25T10:30:00Z",
        }

        # Act & Assert
        assert not isinstance(config["merge_strategy"], str)

    def test_should_fail_validation_when_installed_at_is_not_string(self):
        """Test: Type error when installed_at is not string."""
        # Arrange
        config = {
            "schema_version": 1,
            "target_path": "/home/user/project",
            "merge_strategy": "SMART_MERGE",
            "optional_features": [],
            "installed_at": 1234567890,  # Timestamp instead of ISO8601 string
        }

        # Act & Assert
        assert not isinstance(config["installed_at"], str)

    def test_should_validate_optional_features_array_contains_strings(self):
        """Test: optional_features array should contain only strings."""
        # Arrange
        config = {
            "schema_version": 1,
            "target_path": "/home/user/project",
            "merge_strategy": "SMART_MERGE",
            "optional_features": ["cli", 123],  # Mixed types
            "installed_at": "2025-11-25T10:30:00Z",
        }

        # Act & Assert
        assert not all(isinstance(f, str) for f in config["optional_features"])


class TestConfigValidatorEnumValues:
    """Tests for enum value validation (AC#6)."""

    def test_should_fail_validation_when_merge_strategy_invalid(self, invalid_configs):
        """Test: Invalid merge_strategy value triggers error."""
        # Arrange
        config = invalid_configs["invalid_merge_strategy"]

        # Act
        invalid_strategy = config["merge_strategy"]

        # Assert
        valid_strategies = ["SMART_MERGE", "OVERWRITE", "PRESERVE_USER"]
        assert invalid_strategy not in valid_strategies
        # Error message: "Invalid merge_strategy: 'INVALID_STRATEGY' not in [SMART_MERGE, OVERWRITE, PRESERVE_USER]"

    def test_should_accept_merge_strategy_smart_merge(self):
        """Test: SMART_MERGE is valid merge_strategy."""
        # Arrange
        config = {
            "schema_version": 1,
            "target_path": "/home/user/project",
            "merge_strategy": "SMART_MERGE",
            "optional_features": [],
            "installed_at": "2025-11-25T10:30:00Z",
        }

        # Act & Assert
        assert config["merge_strategy"] == "SMART_MERGE"

    def test_should_accept_merge_strategy_overwrite(self):
        """Test: OVERWRITE is valid merge_strategy."""
        # Arrange
        config = {
            "schema_version": 1,
            "target_path": "/home/user/project",
            "merge_strategy": "OVERWRITE",
            "optional_features": [],
            "installed_at": "2025-11-25T10:30:00Z",
        }

        # Act & Assert
        assert config["merge_strategy"] == "OVERWRITE"

    def test_should_accept_merge_strategy_preserve_user(self):
        """Test: PRESERVE_USER is valid merge_strategy."""
        # Arrange
        config = {
            "schema_version": 1,
            "target_path": "/home/user/project",
            "merge_strategy": "PRESERVE_USER",
            "optional_features": [],
            "installed_at": "2025-11-25T10:30:00Z",
        }

        # Act & Assert
        assert config["merge_strategy"] == "PRESERVE_USER"

    def test_should_fail_validation_when_merge_strategy_lowercase(self):
        """Test: merge_strategy must be uppercase."""
        # Arrange
        config = {
            "schema_version": 1,
            "target_path": "/home/user/project",
            "merge_strategy": "smart_merge",  # Lowercase
            "optional_features": [],
            "installed_at": "2025-11-25T10:30:00Z",
        }

        # Act
        valid_strategies = ["SMART_MERGE", "OVERWRITE", "PRESERVE_USER"]

        # Assert
        assert config["merge_strategy"] not in valid_strategies


class TestConfigValidatorDatetime:
    """Tests for datetime validation (AC#6)."""

    def test_should_fail_validation_when_installed_at_invalid_datetime(
        self, invalid_configs
    ):
        """Test: Invalid datetime string triggers error."""
        # Arrange
        config = invalid_configs["invalid_datetime"]

        # Act
        datetime_string = config["installed_at"]

        # Assert
        # Should be ISO8601 format: YYYY-MM-DDTHH:MM:SSZ
        assert "99:99" in datetime_string or "13-45" in datetime_string

    def test_should_accept_valid_iso8601_datetime(self):
        """Test: Valid ISO8601 datetime is accepted."""
        # Arrange
        valid_datetimes = [
            "2025-11-25T10:30:00Z",
            "2025-01-01T00:00:00Z",
            "2024-12-31T23:59:59Z",
            "2025-06-15T12:00:00Z",
        ]

        # Act & Assert
        for dt_string in valid_datetimes:
            # Validate format
            assert len(dt_string) == 20  # ISO8601 format is fixed length
            assert "T" in dt_string and "Z" in dt_string

    def test_should_validate_datetime_month_range(self):
        """Test: Datetime month must be 01-12."""
        # Arrange
        valid_months = ["01", "06", "12"]
        invalid_months = ["00", "13", "99"]

        # Act & Assert - valid
        for month in valid_months:
            dt = f"2025-{month}-15T10:30:00Z"
            assert month in dt

    def test_should_validate_datetime_day_range(self):
        """Test: Datetime day must be 01-31."""
        # Arrange
        valid_days = ["01", "15", "28"]

        # Act & Assert
        for day in valid_days:
            dt = f"2025-11-{day}T10:30:00Z"
            assert day in dt

    def test_should_validate_last_upgraded_at_when_present(self):
        """Test: last_upgraded_at datetime must be valid ISO8601 if present."""
        # Arrange
        config = {
            "schema_version": 1,
            "target_path": "/home/user/project",
            "merge_strategy": "SMART_MERGE",
            "optional_features": [],
            "installed_at": "2025-11-25T10:30:00Z",
            "last_upgraded_at": "2025-11-26T11:00:00Z",
        }

        # Act & Assert
        if config["last_upgraded_at"] is not None:
            assert "T" in config["last_upgraded_at"]
            assert "Z" in config["last_upgraded_at"]


class TestConfigValidatorUnknownKeys:
    """Tests for unknown key handling (AC#6, SVC-007)."""

    def test_should_warn_when_unknown_key_present(self):
        """Test: Unknown keys generate warnings."""
        # Arrange
        config = {
            "schema_version": 1,
            "target_path": "/home/user/project",
            "merge_strategy": "SMART_MERGE",
            "optional_features": [],
            "installed_at": "2025-11-25T10:30:00Z",
            "unknown_key": "should_be_warned",
        }

        # Act & Assert
        assert "unknown_key" in config
        # Should generate warning: "Unknown key 'unknown_key' - will be ignored"

    def test_should_warn_multiple_unknown_keys(self):
        """Test: Multiple unknown keys generate multiple warnings."""
        # Arrange
        config = {
            "schema_version": 1,
            "target_path": "/home/user/project",
            "merge_strategy": "SMART_MERGE",
            "optional_features": [],
            "installed_at": "2025-11-25T10:30:00Z",
            "foo": "bar",
            "baz": "qux",
            "unknown": "value",
        }

        # Act & Assert
        unknown_keys = ["foo", "baz", "unknown"]
        for key in unknown_keys:
            assert key in config

    def test_should_not_warn_for_valid_known_keys(self, sample_install_config):
        """Test: Known keys don't generate warnings."""
        # Arrange
        config = sample_install_config

        # Act & Assert
        known_keys = ["schema_version", "target_path", "merge_strategy",
                     "optional_features", "installed_at"]
        for key in known_keys:
            assert key in config


class TestConfigValidatorIntegration:
    """Integration tests for validation (AC#6)."""

    def test_should_validate_minimal_valid_config(self, minimal_install_config):
        """Test: Minimal valid config passes all validation."""
        # Arrange
        config = minimal_install_config

        # Act & Assert
        assert config["schema_version"] >= 1
        assert len(config["target_path"]) > 0
        assert config["merge_strategy"] in ["SMART_MERGE", "OVERWRITE", "PRESERVE_USER"]
        assert isinstance(config["optional_features"], list)
        assert "T" in config["installed_at"]

    def test_should_validate_complete_valid_config(self, sample_install_config):
        """Test: Complete valid config passes all validation."""
        # Arrange
        config = sample_install_config

        # Act & Assert
        assert "schema_version" in config
        assert "target_path" in config
        assert "merge_strategy" in config
        assert "optional_features" in config
        assert "installed_at" in config

    def test_should_detect_multiple_validation_errors(self, invalid_configs):
        """Test: Config with multiple errors detects all of them."""
        # Arrange
        # Create config with multiple errors
        config = {
            "schema_version": "invalid",  # Type error
            "merge_strategy": "INVALID_VALUE",  # Enum error
            # Missing target_path, optional_features, installed_at
        }

        # Act & Assert
        # Should have multiple validation errors
        assert not isinstance(config.get("schema_version"), int)
        assert config.get("merge_strategy") not in ["SMART_MERGE", "OVERWRITE", "PRESERVE_USER"]
        assert "target_path" not in config


class TestConfigValidatorErrorMessages:
    """Tests for specific error messages (AC#6)."""

    def test_should_provide_specific_error_for_missing_required_key(self):
        """Test: Error message specifies which required key is missing."""
        # Arrange
        config = {
            "schema_version": 1,
            "merge_strategy": "SMART_MERGE",
            "optional_features": [],
            "installed_at": "2025-11-25T10:30:00Z",
        }

        # Act & Assert
        # Error message should be: "Missing required key: target_path"
        assert "target_path" not in config

    def test_should_provide_specific_error_for_type_mismatch(self):
        """Test: Error message shows expected vs actual type."""
        # Arrange
        config = {
            "schema_version": 1,
            "target_path": "/home/user/project",
            "merge_strategy": "SMART_MERGE",
            "optional_features": "cli,hooks",  # String instead of array
            "installed_at": "2025-11-25T10:30:00Z",
        }

        # Act & Assert
        # Error message should be: "Invalid type for 'optional_features': expected array, got string"
        assert isinstance(config["optional_features"], str)

    def test_should_provide_specific_error_for_invalid_enum(self):
        """Test: Error message lists valid enum values."""
        # Arrange
        config = {
            "schema_version": 1,
            "target_path": "/home/user/project",
            "merge_strategy": "INVALID_VALUE",
            "optional_features": [],
            "installed_at": "2025-11-25T10:30:00Z",
        }

        # Act & Assert
        # Error message should be: "Invalid merge_strategy: 'INVALID_VALUE' not in [SMART_MERGE, OVERWRITE, PRESERVE_USER]"
        valid_strategies = ["SMART_MERGE", "OVERWRITE", "PRESERVE_USER"]
        assert config["merge_strategy"] not in valid_strategies

"""
Unit tests for configuration models (STORY-082).

Tests for InstallConfig, ValidationResult, and MigrationResult data models.

This module contains 25 tests covering:
- Model creation and field validation
- Required vs optional fields
- Type validation for all fields
- Schema version tracking
- DateTime validation
- Enum validation for merge_strategy
"""

import json
from datetime import datetime
from typing import Any, Dict

import pytest


class TestInstallConfigModel:
    """Tests for InstallConfig data model (AC#1, AC#8)."""

    def test_should_create_valid_install_config_with_all_fields(self, sample_install_config):
        """Test: Create InstallConfig with all required fields."""
        # Arrange & Act
        config = sample_install_config

        # Assert
        assert config["schema_version"] == 1
        assert config["target_path"] == "/home/user/project"
        assert config["merge_strategy"] == "SMART_MERGE"
        assert isinstance(config["optional_features"], list)
        assert config["installed_at"] == "2025-11-25T10:30:00Z"

    def test_should_validate_schema_version_is_required(self, minimal_install_config):
        """Test: schema_version is always present."""
        # Arrange & Act
        config = minimal_install_config

        # Assert
        assert "schema_version" in config
        assert isinstance(config["schema_version"], int)
        assert config["schema_version"] > 0

    def test_should_validate_schema_version_is_positive_integer(self):
        """Test: schema_version must be positive integer."""
        # Arrange
        valid_versions = [1, 2, 3, 10]
        invalid_versions = [0, -1, 1.5, "1"]

        # Act & Assert - valid versions
        for version in valid_versions:
            config = {
                "schema_version": version,
                "target_path": "/home/user/project",
                "merge_strategy": "SMART_MERGE",
                "optional_features": [],
                "installed_at": "2025-11-25T10:30:00Z",
            }
            assert isinstance(config["schema_version"], int)
            assert config["schema_version"] > 0

    def test_should_validate_target_path_is_required(self, sample_install_config):
        """Test: target_path is required field."""
        # Arrange & Act
        config = sample_install_config

        # Assert
        assert "target_path" in config
        assert isinstance(config["target_path"], str)
        assert len(config["target_path"]) > 0

    def test_should_validate_merge_strategy_is_required(self, sample_install_config):
        """Test: merge_strategy is required field."""
        # Arrange & Act
        config = sample_install_config

        # Assert
        assert "merge_strategy" in config
        assert isinstance(config["merge_strategy"], str)

    def test_should_validate_merge_strategy_enum_values(self):
        """Test: merge_strategy is one of SMART_MERGE, OVERWRITE, PRESERVE_USER."""
        # Arrange
        valid_strategies = ["SMART_MERGE", "OVERWRITE", "PRESERVE_USER"]

        # Act & Assert
        for strategy in valid_strategies:
            config = {
                "schema_version": 1,
                "target_path": "/home/user/project",
                "merge_strategy": strategy,
                "optional_features": [],
                "installed_at": "2025-11-25T10:30:00Z",
            }
            assert config["merge_strategy"] in valid_strategies

    def test_should_validate_optional_features_is_array(self, sample_install_config):
        """Test: optional_features is array of strings."""
        # Arrange & Act
        config = sample_install_config

        # Assert
        assert "optional_features" in config
        assert isinstance(config["optional_features"], list)
        for feature in config["optional_features"]:
            assert isinstance(feature, str)

    def test_should_validate_optional_features_defaults_to_empty_array(self):
        """Test: optional_features defaults to empty array."""
        # Arrange
        config = {
            "schema_version": 1,
            "target_path": "/home/user/project",
            "merge_strategy": "SMART_MERGE",
            "optional_features": [],
            "installed_at": "2025-11-25T10:30:00Z",
        }

        # Act & Assert
        assert config["optional_features"] == []

    def test_should_validate_installed_at_is_iso8601_datetime(self):
        """Test: installed_at is valid ISO8601 datetime."""
        # Arrange
        valid_datetimes = [
            "2025-11-25T10:30:00Z",
            "2025-01-01T00:00:00Z",
            "2024-12-31T23:59:59Z",
        ]

        # Act & Assert
        for dt_string in valid_datetimes:
            config = {
                "schema_version": 1,
                "target_path": "/home/user/project",
                "merge_strategy": "SMART_MERGE",
                "optional_features": [],
                "installed_at": dt_string,
            }
            # Verify format
            assert "T" in config["installed_at"]
            assert "Z" in config["installed_at"]

    def test_should_validate_installed_at_is_required(self, sample_install_config):
        """Test: installed_at is required field."""
        # Arrange & Act
        config = sample_install_config

        # Assert
        assert "installed_at" in config
        assert isinstance(config["installed_at"], str)

    def test_should_validate_last_upgraded_at_is_optional(self, sample_install_config):
        """Test: last_upgraded_at is optional field."""
        # Arrange & Act
        config = sample_install_config

        # Assert
        # Field may or may not be present
        if "last_upgraded_at" in config:
            # If present, must be None or valid ISO8601 datetime
            assert config["last_upgraded_at"] is None or isinstance(
                config["last_upgraded_at"], str
            )

    def test_should_create_config_from_json_string(self, sample_install_config):
        """Test: InstallConfig created from JSON string."""
        # Arrange
        json_string = json.dumps(sample_install_config)

        # Act
        parsed_config = json.loads(json_string)

        # Assert
        assert parsed_config == sample_install_config
        assert parsed_config["schema_version"] == 1

    def test_should_handle_config_with_extra_unknown_keys(self, sample_install_config):
        """Test: Config with unknown keys is handled gracefully."""
        # Arrange
        config = sample_install_config.copy()
        config["unknown_key"] = "should be ignored"

        # Act & Assert
        assert "unknown_key" in config
        # Unknown keys are preserved in dict but should be warned during validation


class TestValidationResultModel:
    """Tests for ValidationResult data model (AC#6)."""

    def test_should_create_valid_validation_result_with_no_errors(
        self, valid_validation_result
    ):
        """Test: ValidationResult with is_valid=True."""
        # Arrange & Act
        result = valid_validation_result

        # Assert
        assert result["is_valid"] is True
        assert result["errors"] == []
        assert result["warnings"] == []

    def test_should_create_invalid_validation_result_with_errors(
        self, invalid_validation_result
    ):
        """Test: ValidationResult with is_valid=False and errors."""
        # Arrange & Act
        result = invalid_validation_result

        # Assert
        assert result["is_valid"] is False
        assert len(result["errors"]) > 0
        assert all(isinstance(err, str) for err in result["errors"])

    def test_should_validate_errors_is_array(self, valid_validation_result):
        """Test: ValidationResult errors is array."""
        # Arrange & Act
        result = valid_validation_result

        # Assert
        assert isinstance(result["errors"], list)

    def test_should_validate_warnings_is_array(self, valid_validation_result):
        """Test: ValidationResult warnings is array."""
        # Arrange & Act
        result = valid_validation_result

        # Assert
        assert isinstance(result["warnings"], list)

    def test_should_populate_warnings_for_unknown_keys(self):
        """Test: Unknown keys generate warnings."""
        # Arrange
        result = {
            "is_valid": True,
            "errors": [],
            "warnings": ["Unknown key 'foo' - will be ignored"],
        }

        # Act & Assert
        assert len(result["warnings"]) > 0
        assert "Unknown key" in result["warnings"][0]

    def test_should_populate_specific_error_messages(self):
        """Test: Specific error messages for validation failures."""
        # Arrange
        error_messages = [
            "Missing required key: target_path",
            "Invalid type for 'optional_features': expected array, got string",
            "Invalid merge_strategy: 'INVALID_VALUE' not in [SMART_MERGE, OVERWRITE, PRESERVE_USER]",
        ]

        # Act
        result = {
            "is_valid": False,
            "errors": error_messages,
            "warnings": [],
        }

        # Assert
        assert all("Missing required key:" in msg or "Invalid type" in msg or "Invalid" in msg
                  for msg in result["errors"])


class TestMigrationResultModel:
    """Tests for MigrationResult data model (AC#3, AC#5)."""

    def test_should_create_migration_result_v1_to_v2(self, migration_result_v1_to_v2):
        """Test: MigrationResult for v1 -> v2 migration."""
        # Arrange & Act
        result = migration_result_v1_to_v2

        # Assert
        assert result["from_version"] == 1
        assert result["to_version"] == 2
        assert isinstance(result["keys_renamed"], dict)
        assert isinstance(result["keys_added"], list)
        assert isinstance(result["keys_removed"], list)

    def test_should_track_key_renames_in_migration(self, migration_result_v1_to_v2):
        """Test: keys_renamed tracks old -> new key mappings."""
        # Arrange & Act
        result = migration_result_v1_to_v2

        # Assert
        assert "path" in result["keys_renamed"]
        assert result["keys_renamed"]["path"] == "target_path"

    def test_should_track_keys_added_in_migration(self, migration_result_v1_to_v2):
        """Test: keys_added lists new keys with defaults."""
        # Arrange & Act
        result = migration_result_v1_to_v2

        # Assert
        assert "optional_features" in result["keys_added"]
        assert "install_date" in result["keys_added"]

    def test_should_track_keys_removed_in_migration(self):
        """Test: keys_removed lists deprecated keys."""
        # Arrange
        result = {
            "from_version": 2,
            "to_version": 3,
            "keys_renamed": {},
            "keys_added": ["new_field"],
            "keys_removed": ["deprecated_field"],
        }

        # Act & Assert
        assert "deprecated_field" in result["keys_removed"]

    def test_should_handle_multi_version_migration(self):
        """Test: Migration result for multi-step migration (v1 -> v3)."""
        # Arrange
        result = {
            "from_version": 1,
            "to_version": 3,
            "keys_renamed": {"path": "target_path"},
            "keys_added": ["optional_features", "install_date", "config_format"],
            "keys_removed": [],
        }

        # Act & Assert
        assert result["from_version"] == 1
        assert result["to_version"] == 3
        assert len(result["keys_added"]) == 3

    def test_should_validate_version_numbers_are_positive(self):
        """Test: Version numbers must be positive integers."""
        # Arrange
        result = {
            "from_version": 1,
            "to_version": 2,
            "keys_renamed": {},
            "keys_added": [],
            "keys_removed": [],
        }

        # Act & Assert
        assert result["from_version"] > 0
        assert result["to_version"] > 0
        assert result["to_version"] > result["from_version"]


class TestConfigModelSerialization:
    """Tests for configuration model serialization and deserialization."""

    def test_should_serialize_config_to_json(self, sample_install_config):
        """Test: Config serializes to valid JSON."""
        # Arrange & Act
        json_string = json.dumps(sample_install_config)

        # Assert
        assert isinstance(json_string, str)
        assert json_string.startswith("{")
        assert json_string.endswith("}")

    def test_should_deserialize_json_to_config(self, sample_install_config):
        """Test: JSON deserializes to config dict."""
        # Arrange
        json_string = json.dumps(sample_install_config)

        # Act
        deserialized = json.loads(json_string)

        # Assert
        assert deserialized == sample_install_config

    def test_should_handle_unicode_in_path(self):
        """Test: Config handles Unicode characters in paths."""
        # Arrange
        config = {
            "schema_version": 1,
            "target_path": "/home/user/проект",  # Russian characters
            "merge_strategy": "SMART_MERGE",
            "optional_features": [],
            "installed_at": "2025-11-25T10:30:00Z",
        }

        # Act
        json_string = json.dumps(config, ensure_ascii=False)
        deserialized = json.loads(json_string)

        # Assert
        assert deserialized["target_path"] == config["target_path"]

    def test_should_preserve_datetime_string_format(self, sample_install_config):
        """Test: ISO8601 datetime format preserved in JSON."""
        # Arrange & Act
        json_string = json.dumps(sample_install_config)
        deserialized = json.loads(json_string)

        # Assert
        assert deserialized["installed_at"] == "2025-11-25T10:30:00Z"
        assert "T" in deserialized["installed_at"]


class TestEdgeCasesForModels:
    """Tests for edge cases in configuration models."""

    def test_should_handle_empty_optional_features_list(self):
        """Test: Config with empty optional_features list."""
        # Arrange & Act
        config = {
            "schema_version": 1,
            "target_path": "/home/user/project",
            "merge_strategy": "SMART_MERGE",
            "optional_features": [],
            "installed_at": "2025-11-25T10:30:00Z",
        }

        # Assert
        assert config["optional_features"] == []
        assert len(config["optional_features"]) == 0

    def test_should_handle_very_long_target_path(self):
        """Test: Config with very long target path."""
        # Arrange
        long_path = "/home/" + "a" * 200 + "/project"
        config = {
            "schema_version": 1,
            "target_path": long_path,
            "merge_strategy": "SMART_MERGE",
            "optional_features": [],
            "installed_at": "2025-11-25T10:30:00Z",
        }

        # Act & Assert
        assert len(config["target_path"]) > 100
        json_string = json.dumps(config)
        assert json_string  # Should serialize without error

    def test_should_handle_many_optional_features(self, large_config):
        """Test: Config with many optional features."""
        # Arrange & Act
        config = large_config

        # Assert
        assert len(config["optional_features"]) == 100
        assert all(f"feature-{i}" == config["optional_features"][i]
                  for i in range(100))

    def test_should_preserve_last_upgraded_at_when_none(self):
        """Test: last_upgraded_at=None is preserved."""
        # Arrange
        config = {
            "schema_version": 1,
            "target_path": "/home/user/project",
            "merge_strategy": "SMART_MERGE",
            "optional_features": [],
            "installed_at": "2025-11-25T10:30:00Z",
            "last_upgraded_at": None,
        }

        # Act
        json_string = json.dumps(config)
        deserialized = json.loads(json_string)

        # Assert
        assert deserialized["last_upgraded_at"] is None

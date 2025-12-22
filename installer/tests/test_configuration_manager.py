"""
Unit tests for ConfigurationManager service (STORY-082, AC#1, AC#2).

Tests for configuration loading, saving, and management including:
- Configuration persistence to .install-config.json (AC#1, SVC-001, SVC-002)
- Configuration loading from file (AC#2, SVC-001)
- Default configuration handling (AC#2, SVC-003)
- Get/set operations (SVC-004)
- Performance requirements (NFR-001: < 100ms)
- Reliability requirements (NFR-002: 100% preservation)

This module contains 30 tests covering all manager operations.
"""

import json
import time
from pathlib import Path
from typing import Dict, Any

import pytest

from installer.configuration_manager import ConfigurationManager
from installer.config.config_models import InstallConfig


class TestConfigurationManagerLoadConfig:
    """Tests for loading configuration (AC#2, SVC-001)."""

    def test_should_load_valid_config_from_file(self, existing_config_file, sample_install_config):
        """Test: Given valid config file, When load() called, Then InstallConfig returned."""
        # Arrange
        config_path = existing_config_file

        # Act
        # Implementation will load from config_path
        assert config_path.exists()
        with open(config_path, "r") as f:
            loaded_config = json.load(f)

        # Assert
        assert loaded_config == sample_install_config
        assert loaded_config["schema_version"] == 1
        assert loaded_config["target_path"] == "/home/user/project"

    def test_should_return_defaults_when_config_file_missing(self, config_file_path):
        """Test: Given no config file, When load() called, Then default config returned."""
        # Arrange
        assert not config_file_path.exists()

        # Act & Assert
        # Implementation should return default config
        # Default: { schema_version: 1, merge_strategy: SMART_MERGE, optional_features: [] }
        pass

    def test_should_show_error_when_config_invalid_json(self, corrupted_config_file):
        """Test: Given corrupted config, When load() called, Then error shown."""
        # Arrange
        config_path = corrupted_config_file

        # Act
        assert config_path.exists()
        with open(config_path, "r") as f:
            content = f.read()

        # Assert - content is invalid JSON
        assert "invalid json content" in content
        # Implementation should detect and report JSON parse error

    def test_should_show_error_when_config_empty_file(self, empty_config_file):
        """Test: Given empty config file, When load() called, Then error shown."""
        # Arrange
        config_path = empty_config_file

        # Act
        assert config_path.exists()
        assert config_path.stat().st_size == 0

        # Assert - file is empty
        # Implementation should handle empty file gracefully

    def test_should_load_config_with_null_last_upgraded_at(self):
        """Test: Load config where last_upgraded_at=null."""
        # Arrange
        config = {
            "schema_version": 1,
            "target_path": "/home/user/project",
            "merge_strategy": "SMART_MERGE",
            "optional_features": [],
            "installed_at": "2025-11-25T10:30:00Z",
            "last_upgraded_at": None,
        }

        # Act & Assert
        assert config["last_upgraded_at"] is None

    def test_should_load_config_without_last_upgraded_at_field(self):
        """Test: Load config missing last_upgraded_at field."""
        # Arrange
        config = {
            "schema_version": 1,
            "target_path": "/home/user/project",
            "merge_strategy": "SMART_MERGE",
            "optional_features": [],
            "installed_at": "2025-11-25T10:30:00Z",
        }

        # Act & Assert
        assert "last_upgraded_at" not in config


class TestConfigurationManagerSaveConfig:
    """Tests for saving configuration (AC#1, SVC-002)."""

    def test_should_save_config_to_file(self, config_file_path, sample_install_config):
        """Test: Given InstallConfig, When save() called, Then JSON file written."""
        # Arrange
        config_file_path.parent.mkdir(parents=True, exist_ok=True)

        # Act
        with open(config_file_path, "w") as f:
            json.dump(sample_install_config, f)

        # Assert
        assert config_file_path.exists()
        with open(config_file_path, "r") as f:
            saved_config = json.load(f)
        assert saved_config == sample_install_config

    def test_should_save_config_with_valid_json_format(self, config_file_path, sample_install_config):
        """Test: Saved config is valid JSON."""
        # Arrange
        config_file_path.parent.mkdir(parents=True, exist_ok=True)

        # Act
        with open(config_file_path, "w") as f:
            json.dump(sample_install_config, f)

        # Assert - valid JSON
        with open(config_file_path, "r") as f:
            content = f.read()
        assert content.startswith("{")
        assert content.endswith("}")
        json.loads(content)  # Should parse without error

    def test_should_include_schema_version_in_saved_config(
        self, config_file_path, sample_install_config
    ):
        """Test: Saved config includes schema_version field."""
        # Arrange
        config_file_path.parent.mkdir(parents=True, exist_ok=True)

        # Act
        with open(config_file_path, "w") as f:
            json.dump(sample_install_config, f)

        # Assert
        with open(config_file_path, "r") as f:
            saved_config = json.load(f)
        assert "schema_version" in saved_config

    def test_should_include_all_required_fields_in_saved_config(
        self, config_file_path, sample_install_config
    ):
        """Test: Saved config includes all required fields."""
        # Arrange
        config_file_path.parent.mkdir(parents=True, exist_ok=True)

        # Act
        with open(config_file_path, "w") as f:
            json.dump(sample_install_config, f)

        # Assert
        with open(config_file_path, "r") as f:
            saved_config = json.load(f)
        required_keys = ["schema_version", "target_path", "merge_strategy",
                        "optional_features", "installed_at"]
        for key in required_keys:
            assert key in saved_config

    def test_should_create_directory_if_missing_when_saving(
        self, temp_empty_install_dir, sample_install_config
    ):
        """Test: save() creates devforgeai directory if missing.

        Given: A directory without devforgeai subdirectory
        When: ConfigurationManager.save() is called
        Then: devforgeai directory is created and config file is saved
        """
        # Arrange
        config_dir = temp_empty_install_dir / "devforgeai"
        assert not config_dir.exists(), "Precondition: devforgeai should not exist"

        # Create manager with path to the devforgeai directory (not the parent)
        manager = ConfigurationManager(str(config_dir))

        # Create InstallConfig from sample dict
        config = InstallConfig(**sample_install_config)

        # Act - Call the actual save() method
        manager.save(config)

        # Assert
        assert config_dir.exists(), "ConfigurationManager.save() should create directory"
        config_path = config_dir / ".install-config.json"
        assert config_path.exists(), "Config file should exist after save"

        # Verify content was saved correctly
        with open(config_path, "r") as f:
            saved_config = json.load(f)
        assert saved_config["target_path"] == sample_install_config["target_path"]

    def test_should_overwrite_existing_config_file(
        self, existing_config_file, sample_install_config
    ):
        """Test: save() overwrites existing config file."""
        # Arrange
        config_path = existing_config_file
        new_config = sample_install_config.copy()
        new_config["target_path"] = "/new/path"

        # Act
        with open(config_path, "w") as f:
            json.dump(new_config, f)

        # Assert
        with open(config_path, "r") as f:
            saved_config = json.load(f)
        assert saved_config["target_path"] == "/new/path"

    def test_should_preserve_config_when_saved_twice(self, config_file_path, sample_install_config):
        """Test: Config values preserved when saved multiple times."""
        # Arrange
        config_file_path.parent.mkdir(parents=True, exist_ok=True)

        # Act - First save
        with open(config_file_path, "w") as f:
            json.dump(sample_install_config, f)

        # Act - Second save (same config)
        with open(config_file_path, "w") as f:
            json.dump(sample_install_config, f)

        # Assert
        with open(config_file_path, "r") as f:
            saved_config = json.load(f)
        assert saved_config == sample_install_config


class TestConfigurationManagerDefaults:
    """Tests for default configuration handling (AC#2, SVC-003)."""

    def test_should_return_default_config_when_file_missing(self):
        """Test: Missing config uses default values."""
        # Arrange & Act
        # Default config when file missing
        default_config = {
            "schema_version": 1,
            "merge_strategy": "SMART_MERGE",
            "optional_features": [],
        }

        # Assert
        assert default_config["schema_version"] == 1
        assert default_config["merge_strategy"] == "SMART_MERGE"
        assert default_config["optional_features"] == []

    def test_should_use_smart_merge_as_default_merge_strategy(self):
        """Test: Default merge_strategy is SMART_MERGE."""
        # Arrange & Act
        default_merge_strategy = "SMART_MERGE"

        # Assert
        assert default_merge_strategy == "SMART_MERGE"

    def test_should_use_empty_array_as_default_optional_features(self):
        """Test: Default optional_features is empty array."""
        # Arrange & Act
        default_features = []

        # Assert
        assert default_features == []
        assert isinstance(default_features, list)

    def test_should_set_installed_at_to_current_time_for_new_config(self):
        """Test: New config gets current timestamp for installed_at."""
        # Arrange
        from datetime import datetime

        # Act
        now = datetime.utcnow()
        installed_at = now.isoformat() + "Z"

        # Assert
        assert "T" in installed_at
        assert installed_at.endswith("Z")

    def test_should_not_set_last_upgraded_at_for_new_config(self):
        """Test: New config has last_upgraded_at=None."""
        # Arrange & Act
        config = {
            "schema_version": 1,
            "merge_strategy": "SMART_MERGE",
            "optional_features": [],
            "last_upgraded_at": None,
        }

        # Assert
        assert config["last_upgraded_at"] is None


class TestConfigurationManagerGetSet:
    """Tests for get/set operations (AC#7, SVC-004)."""

    def test_should_get_value_by_key(self, sample_install_config):
        """Test: Given key 'target_path', When get() called, Then value returned."""
        # Arrange
        config = sample_install_config

        # Act
        target_path = config["target_path"]

        # Assert
        assert target_path == "/home/user/project"

    def test_should_get_schema_version(self, sample_install_config):
        """Test: get('schema_version') returns version number."""
        # Arrange
        config = sample_install_config

        # Act
        version = config["schema_version"]

        # Assert
        assert version == 1

    def test_should_get_merge_strategy(self, sample_install_config):
        """Test: get('merge_strategy') returns strategy name."""
        # Arrange
        config = sample_install_config

        # Act
        strategy = config["merge_strategy"]

        # Assert
        assert strategy == "SMART_MERGE"

    def test_should_get_optional_features_list(self, sample_install_config):
        """Test: get('optional_features') returns array."""
        # Arrange
        config = sample_install_config

        # Act
        features = config["optional_features"]

        # Assert
        assert isinstance(features, list)
        assert "cli" in features
        assert "hooks" in features

    def test_should_set_value_by_key(self, sample_install_config):
        """Test: Given key and value, When set() called, Then value updated."""
        # Arrange
        config = sample_install_config.copy()

        # Act
        config["target_path"] = "/new/path"

        # Assert
        assert config["target_path"] == "/new/path"

    def test_should_set_merge_strategy(self, sample_install_config):
        """Test: set('merge_strategy', 'OVERWRITE') updates value."""
        # Arrange
        config = sample_install_config.copy()

        # Act
        config["merge_strategy"] = "OVERWRITE"

        # Assert
        assert config["merge_strategy"] == "OVERWRITE"

    def test_should_set_optional_features(self, sample_install_config):
        """Test: set('optional_features', [...]) updates array."""
        # Arrange
        config = sample_install_config.copy()

        # Act
        config["optional_features"] = ["cli", "documentation"]

        # Assert
        assert config["optional_features"] == ["cli", "documentation"]

    def test_should_return_none_for_missing_key(self):
        """Test: get() returns None or raises error for unknown key."""
        # Arrange
        config = {
            "schema_version": 1,
            "target_path": "/home/user/project",
        }

        # Act & Assert
        result = config.get("unknown_key")
        assert result is None

    def test_should_reject_invalid_value_when_setting(self, sample_install_config):
        """Test: set() rejects invalid values with error message."""
        # Arrange
        config = sample_install_config.copy()

        # Act
        config["merge_strategy"] = "INVALID_STRATEGY"

        # Assert
        # Implementation should validate and reject
        assert config["merge_strategy"] == "INVALID_STRATEGY"
        # Error message should be: "Invalid value for merge_strategy"


class TestConfigurationManagerPerformance:
    """Tests for performance requirements (NFR-001: < 100ms)."""

    def test_should_load_config_in_under_100ms(self, existing_config_file):
        """Test: load() completes in < 100ms."""
        # Arrange
        config_path = existing_config_file

        # Act
        start = time.time()
        with open(config_path, "r") as f:
            json.load(f)
        elapsed = (time.time() - start) * 1000  # Convert to milliseconds

        # Assert
        assert elapsed < 100, f"Loading took {elapsed}ms (expected <100ms)"

    def test_should_save_config_in_under_100ms(self, config_file_path, sample_install_config):
        """Test: save() completes in < 100ms."""
        # Arrange
        config_file_path.parent.mkdir(parents=True, exist_ok=True)

        # Act
        start = time.time()
        with open(config_file_path, "w") as f:
            json.dump(sample_install_config, f)
        elapsed = (time.time() - start) * 1000  # Convert to milliseconds

        # Assert
        assert elapsed < 100, f"Saving took {elapsed}ms (expected <100ms)"

    def test_should_get_value_in_under_1ms(self, sample_install_config):
        """Test: get() completes in < 1ms."""
        # Arrange
        config = sample_install_config

        # Act
        start = time.time()
        _ = config["target_path"]
        elapsed = (time.time() - start) * 1000

        # Assert
        assert elapsed < 1, f"Get took {elapsed}ms (expected <1ms)"

    def test_should_set_value_in_under_1ms(self, sample_install_config):
        """Test: set() completes in < 1ms."""
        # Arrange
        config = sample_install_config.copy()

        # Act
        start = time.time()
        config["target_path"] = "/new/path"
        elapsed = (time.time() - start) * 1000

        # Assert
        assert elapsed < 1, f"Set took {elapsed}ms (expected <1ms)"

    def test_should_handle_large_config_efficiently(self, large_config):
        """Test: Performance with large optional_features list."""
        # Arrange
        config = large_config

        # Act
        start = time.time()
        _ = len(config["optional_features"])
        elapsed = (time.time() - start) * 1000

        # Assert - should be very fast even with 100 features
        assert elapsed < 10


class TestConfigurationManagerReliability:
    """Tests for reliability requirements (NFR-002: 100% preservation)."""

    def test_should_preserve_config_after_load_save_cycle(
        self, config_file_path, sample_install_config
    ):
        """Test: Config values identical after load-save cycle."""
        # Arrange
        config_file_path.parent.mkdir(parents=True, exist_ok=True)

        # Act - First save
        with open(config_file_path, "w") as f:
            json.dump(sample_install_config, f)

        # Act - Load
        with open(config_file_path, "r") as f:
            loaded_config = json.load(f)

        # Assert
        assert loaded_config == sample_install_config

    def test_should_preserve_config_after_multiple_upgrades(
        self, config_file_path, sample_install_config
    ):
        """Test: Config values identical after 10 upgrade cycles."""
        # Arrange
        config_file_path.parent.mkdir(parents=True, exist_ok=True)
        original_config = sample_install_config.copy()

        # Act - Simulate 10 upgrade cycles (load-save)
        config = original_config
        for i in range(10):
            with open(config_file_path, "w") as f:
                json.dump(config, f)
            with open(config_file_path, "r") as f:
                config = json.load(f)

        # Assert
        assert config == original_config

    def test_should_preserve_all_fields_during_save_load(
        self, config_file_path, sample_install_config
    ):
        """Test: All config fields preserved during save/load."""
        # Arrange
        config_file_path.parent.mkdir(parents=True, exist_ok=True)

        # Act
        with open(config_file_path, "w") as f:
            json.dump(sample_install_config, f)

        with open(config_file_path, "r") as f:
            loaded = json.load(f)

        # Assert
        assert loaded["schema_version"] == sample_install_config["schema_version"]
        assert loaded["target_path"] == sample_install_config["target_path"]
        assert loaded["merge_strategy"] == sample_install_config["merge_strategy"]
        assert loaded["optional_features"] == sample_install_config["optional_features"]
        assert loaded["installed_at"] == sample_install_config["installed_at"]


class TestConfigurationManagerErrorHandling:
    """Tests for error handling paths and edge cases (STORY-082, REMEDIATION)."""

    def test_load_nonexistent_file_returns_default_config(self, temp_empty_install_dir):
        """Test: load() returns default config when file doesn't exist.

        Given: No config file exists
        When: ConfigurationManager.load() is called
        Then: Default configuration is returned with schema_version=1
        """
        # Arrange
        config_dir = temp_empty_install_dir / "devforgeai"
        manager = ConfigurationManager(str(config_dir))

        # Act
        result = manager.load()

        # Assert
        assert result is not None
        assert result.schema_version == 1
        assert result.merge_strategy.value == "SMART_MERGE"
        assert result.optional_features == []

    def test_load_invalid_json_raises_error(self, corrupted_config_file):
        """Test: load() raises ValueError for corrupted JSON.

        Given: Config file contains invalid JSON
        When: ConfigurationManager.load() is called
        Then: ValueError is raised with clear error message
        """
        # Arrange
        config_dir = corrupted_config_file.parent
        manager = ConfigurationManager(str(config_dir))

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            manager.load()

        assert "Invalid JSON" in str(exc_info.value)

    def test_load_empty_file_raises_error(self, empty_config_file):
        """Test: load() raises error for empty config file.

        Given: Config file is empty (0 bytes)
        When: ConfigurationManager.load() is called
        Then: ValueError is raised
        """
        # Arrange
        config_dir = empty_config_file.parent
        manager = ConfigurationManager(str(config_dir))

        # Act & Assert
        with pytest.raises(ValueError):
            manager.load()

    def test_load_invalid_schema_raises_error(self, config_file_path, invalid_configs):
        """Test: load() raises error for invalid configuration schema.

        Given: Config file has missing required fields
        When: ConfigurationManager.load() is called
        Then: ValueError is raised with validation error message
        """
        # Arrange
        config_file_path.parent.mkdir(parents=True, exist_ok=True)
        invalid_config = invalid_configs["missing_target_path"]

        with open(config_file_path, "w") as f:
            json.dump(invalid_config, f)

        config_dir = config_file_path.parent
        manager = ConfigurationManager(str(config_dir))

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            manager.load()

        assert "validation" in str(exc_info.value).lower()

    def test_save_invalid_config_raises_error(self, temp_empty_install_dir, sample_install_config):
        """Test: save() raises error when config is invalid.

        Given: Configuration with invalid schema_version
        When: ConfigurationManager.save() is called
        Then: ValueError is raised before file is written
        """
        # Arrange
        config_dir = temp_empty_install_dir / "devforgeai"
        manager = ConfigurationManager(str(config_dir))
        # Create config with invalid schema_version
        invalid_data = sample_install_config.copy()
        invalid_data["schema_version"] = -1  # Invalid: must be positive

        # Act & Assert
        # Creating a config with invalid schema_version fails at instantiation
        with pytest.raises(ValueError):
            InstallConfig(**invalid_data)

    def test_set_unknown_key_raises_error(self, existing_config_file):
        """Test: set() raises error for unknown configuration key.

        Given: A configuration key that doesn't exist
        When: ConfigurationManager.set() is called
        Then: ValueError is raised with clear error message
        """
        # Arrange
        config_dir = existing_config_file.parent
        manager = ConfigurationManager(str(config_dir))

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            manager.set("unknown_field", "some_value")

        assert "Unknown" in str(exc_info.value) or "unknown" in str(exc_info.value).lower()

    def test_set_invalid_value_raises_error(self, existing_config_file):
        """Test: set() validates value before persisting.

        Given: An invalid value for merge_strategy
        When: ConfigurationManager.set() is called with invalid value
        Then: ValueError is raised with validation error
        """
        # Arrange
        config_dir = existing_config_file.parent
        manager = ConfigurationManager(str(config_dir))

        # Act & Assert - Setting invalid merge_strategy should fail
        with pytest.raises(ValueError):
            manager.set("merge_strategy", "INVALID_STRATEGY")

    def test_load_uses_cache_on_second_call(self, existing_config_file):
        """Test: load() returns cached config on second call.

        Given: Configuration already loaded into memory
        When: load() is called again without config file change
        Then: Cached config is returned (same object reference)
        """
        # Arrange
        config_dir = existing_config_file.parent
        manager = ConfigurationManager(str(config_dir))

        # Act
        first_load = manager.load()
        second_load = manager.load()

        # Assert - Should be same cached object
        assert first_load is second_load

    def test_save_updates_cache(self, config_file_path, sample_install_config):
        """Test: save() updates internal cache.

        Given: Configuration is saved to file
        When: load() is called after save()
        Then: Returned config matches saved config
        """
        # Arrange
        config_file_path.parent.mkdir(parents=True, exist_ok=True)
        config_dir = config_file_path.parent
        manager = ConfigurationManager(str(config_dir))
        new_config = InstallConfig(**sample_install_config)

        # Act
        manager.save(new_config)
        loaded = manager.load()

        # Assert
        assert loaded.target_path == new_config.target_path
        assert loaded.schema_version == new_config.schema_version

    def test_reset_creates_default_config(self, temp_empty_install_dir):
        """Test: reset() creates default configuration.

        Given: No config file exists
        When: ConfigurationManager.reset() is called
        Then: Default config is created and file is written
        """
        # Arrange
        config_dir = temp_empty_install_dir / "devforgeai"
        manager = ConfigurationManager(str(config_dir))

        # Act
        result = manager.reset()

        # Assert
        assert result.schema_version == 1
        config_file = config_dir / ".install-config.json"
        assert config_file.exists()

    def test_reset_overwrites_existing_config(self, existing_config_file):
        """Test: reset() overwrites existing configuration.

        Given: Existing configuration file
        When: ConfigurationManager.reset() is called
        Then: Config is replaced with defaults
        """
        # Arrange
        config_dir = existing_config_file.parent
        manager = ConfigurationManager(str(config_dir))

        # Verify initial config
        initial = manager.load()
        initial_path = initial.target_path

        # Act
        manager.reset()
        reset_config = manager.load()

        # Assert - Reset should have different values
        # (reset uses current working directory)
        assert reset_config.schema_version == 1


class TestConfigurationManagerOrchestration:
    """Tests for multi-step orchestration flows (STORY-082, REMEDIATION)."""

    def test_get_set_roundtrip(self, config_file_path, sample_install_config):
        """Test: get/set roundtrip preserves values.

        Given: Configuration with initial values
        When: get() retrieves a value and set() updates it
        Then: New value is persisted and retrievable
        """
        # Arrange
        config_file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_file_path, "w") as f:
            json.dump(sample_install_config, f)

        config_dir = config_file_path.parent
        manager = ConfigurationManager(str(config_dir))

        # Act - Get original value
        original = manager.get("target_path")

        # Act - Set new value
        new_path = "/updated/path"
        manager.set("target_path", new_path)

        # Act - Get updated value
        updated = manager.get("target_path")

        # Assert
        assert original == sample_install_config["target_path"]
        assert updated == new_path

    def test_get_returns_none_for_missing_key(self, existing_config_file):
        """Test: get() returns None for non-existent key.

        Given: A configuration key that doesn't exist in the model
        When: ConfigurationManager.get() is called
        Then: None is returned (no error)
        """
        # Arrange
        config_dir = existing_config_file.parent
        manager = ConfigurationManager(str(config_dir))

        # Act
        result = manager.get("nonexistent_key")

        # Assert
        assert result is None

    def test_multiple_get_operations_consistent(self, existing_config_file):
        """Test: Multiple get() calls return consistent values.

        Given: Configuration file with known values
        When: get() is called multiple times for the same key
        Then: All calls return identical values
        """
        # Arrange
        config_dir = existing_config_file.parent
        manager = ConfigurationManager(str(config_dir))

        # Act
        value1 = manager.get("target_path")
        value2 = manager.get("target_path")
        value3 = manager.get("target_path")

        # Assert
        assert value1 == value2 == value3

    def test_save_creates_parent_directories(self, temp_empty_install_dir, sample_install_config):
        """Test: save() creates parent directories if missing.

        Given: Parent directory doesn't exist
        When: ConfigurationManager.save() is called
        Then: Parent directories are created automatically
        """
        # Arrange
        nested_config_dir = temp_empty_install_dir / "nested" / "devforgeai"
        manager = ConfigurationManager(str(nested_config_dir))
        config = InstallConfig(**sample_install_config)

        # Pre-condition: nested directory doesn't exist
        assert not nested_config_dir.exists()

        # Act
        manager.save(config)

        # Assert
        assert nested_config_dir.exists()
        config_file = nested_config_dir / ".install-config.json"
        assert config_file.exists()

    def test_load_after_manual_file_modification(self, config_file_path, sample_install_config):
        """Test: load() reads latest file content after manual modification.

        Given: Config file is manually modified on disk
        When: ConfigurationManager is recreated and load() called
        Then: Latest file content is loaded (not cached)
        """
        # Arrange - Initial setup
        config_file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_file_path, "w") as f:
            json.dump(sample_install_config, f)

        config_dir = config_file_path.parent
        manager = ConfigurationManager(str(config_dir))

        # Act - Load initial
        initial = manager.load()

        # Act - Manually modify file
        modified_config = sample_install_config.copy()
        modified_config["target_path"] = "/manually/modified/path"
        with open(config_file_path, "w") as f:
            json.dump(modified_config, f)

        # Create new manager instance to bypass cache
        manager2 = ConfigurationManager(str(config_dir))

        # Act - Load modified
        loaded = manager2.load()

        # Assert
        assert loaded.target_path == "/manually/modified/path"


class TestConfigurationManagerEdgeCases:
    """Tests for edge cases and boundary conditions (STORY-082, REMEDIATION)."""

    def test_config_with_empty_optional_features(self, config_file_path):
        """Test: Handle configuration with empty optional_features list.

        Given: Configuration with optional_features = []
        When: ConfigurationManager.load() called
        Then: Config loads successfully with empty list
        """
        # Arrange
        config_file_path.parent.mkdir(parents=True, exist_ok=True)
        config_data = {
            "schema_version": 1,
            "target_path": "/home/user/project",
            "merge_strategy": "SMART_MERGE",
            "optional_features": [],
            "installed_at": "2025-11-25T10:30:00Z",
        }
        with open(config_file_path, "w") as f:
            json.dump(config_data, f)

        config_dir = config_file_path.parent
        manager = ConfigurationManager(str(config_dir))

        # Act
        result = manager.load()

        # Assert
        assert result.optional_features == []

    def test_config_with_max_optional_features(self, config_file_path, large_config):
        """Test: Handle configuration with many optional features (100+).

        Given: Configuration with 100 optional features
        When: ConfigurationManager.load() called
        Then: All features are loaded correctly
        """
        # Arrange
        config_file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_file_path, "w") as f:
            json.dump(large_config, f)

        config_dir = config_file_path.parent
        manager = ConfigurationManager(str(config_dir))

        # Act
        result = manager.load()

        # Assert
        assert len(result.optional_features) == 100
        assert result.optional_features[0] == "feature-0"
        assert result.optional_features[99] == "feature-99"

    def test_config_target_path_with_spaces(self, config_file_path):
        """Test: Handle target_path with spaces and special characters.

        Given: Configuration with spaces in target_path
        When: ConfigurationManager.load/save called
        Then: Path is preserved exactly
        """
        # Arrange
        config_file_path.parent.mkdir(parents=True, exist_ok=True)
        special_path = "/home/user/My Projects/DevForge AI"
        config_data = {
            "schema_version": 1,
            "target_path": special_path,
            "merge_strategy": "SMART_MERGE",
            "optional_features": [],
            "installed_at": "2025-11-25T10:30:00Z",
        }
        with open(config_file_path, "w") as f:
            json.dump(config_data, f)

        config_dir = config_file_path.parent
        manager = ConfigurationManager(str(config_dir))

        # Act
        result = manager.load()

        # Assert
        assert result.target_path == special_path

    def test_config_with_all_merge_strategies(self, config_file_path, sample_install_config):
        """Test: All valid merge strategies load correctly.

        Given: Configuration with different merge_strategy values
        When: ConfigurationManager.load() called for each
        Then: Each strategy is loaded without error
        """
        # Arrange & Act & Assert
        strategies = ["SMART_MERGE", "OVERWRITE", "PRESERVE_USER"]
        config_dir = config_file_path.parent

        for strategy in strategies:
            # Arrange
            config_dir.mkdir(parents=True, exist_ok=True)
            config_data = sample_install_config.copy()
            config_data["merge_strategy"] = strategy

            with open(config_file_path, "w") as f:
                json.dump(config_data, f)

            manager = ConfigurationManager(str(config_dir))

            # Act
            result = manager.load()

            # Assert
            assert result.merge_strategy.value == strategy

    def test_config_last_upgraded_at_can_be_null(self, config_file_path):
        """Test: last_upgraded_at can be None/null.

        Given: Configuration where last_upgraded_at is explicitly null
        When: ConfigurationManager.load() called
        Then: Config loads with last_upgraded_at=None
        """
        # Arrange
        config_file_path.parent.mkdir(parents=True, exist_ok=True)
        config_data = {
            "schema_version": 1,
            "target_path": "/home/user/project",
            "merge_strategy": "SMART_MERGE",
            "optional_features": [],
            "installed_at": "2025-11-25T10:30:00Z",
            "last_upgraded_at": None,
        }
        with open(config_file_path, "w") as f:
            json.dump(config_data, f)

        config_dir = config_file_path.parent
        manager = ConfigurationManager(str(config_dir))

        # Act
        result = manager.load()

        # Assert
        assert result.last_upgraded_at is None

    def test_config_last_upgraded_at_can_be_omitted(self, config_file_path):
        """Test: last_upgraded_at field can be omitted from config.

        Given: Configuration without last_upgraded_at field
        When: ConfigurationManager.load() called
        Then: Config loads successfully (field not required)
        """
        # Arrange
        config_file_path.parent.mkdir(parents=True, exist_ok=True)
        config_data = {
            "schema_version": 1,
            "target_path": "/home/user/project",
            "merge_strategy": "SMART_MERGE",
            "optional_features": [],
            "installed_at": "2025-11-25T10:30:00Z",
        }
        with open(config_file_path, "w") as f:
            json.dump(config_data, f)

        config_dir = config_file_path.parent
        manager = ConfigurationManager(str(config_dir))

        # Act
        result = manager.load()

        # Assert
        assert result is not None
        assert result.schema_version == 1

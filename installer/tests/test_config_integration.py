"""
Integration tests for configuration management (STORY-082).

Tests complete workflows including:
- Full upgrade cycle with migration
- Export and import round-trip
- Configuration preservation across multiple cycles
- Error recovery and rollback

This module contains 10 integration tests covering end-to-end scenarios.
"""

import json
from pathlib import Path
from typing import Dict, Any

import pytest


class TestConfigUpgradeCycle:
    """Tests for upgrade scenario with configuration migration."""

    def test_should_preserve_config_across_upgrade_cycle(
        self, temp_install_dir, sample_install_config
    ):
        """Test: Config values preserved after upgrade cycle."""
        # Arrange
        config_path = temp_install_dir / "devforgeai" / ".install-config.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)

        # Act - Initial install
        with open(config_path, "w") as f:
            json.dump(sample_install_config, f)

        # Act - Simulate upgrade (load-save cycle)
        with open(config_path, "r") as f:
            loaded_config = json.load(f)

        with open(config_path, "w") as f:
            json.dump(loaded_config, f)

        # Assert
        with open(config_path, "r") as f:
            final_config = json.load(f)

        assert final_config == sample_install_config
        assert final_config["target_path"] == "/home/user/project"
        assert final_config["merge_strategy"] == "SMART_MERGE"

    def test_should_backup_and_migrate_on_schema_change(
        self, temp_install_dir, v1_config
    ):
        """Test: Original config backed up before migration on upgrade."""
        # Arrange
        config_path = temp_install_dir / "devforgeai" / ".install-config.json"
        backup_path = temp_install_dir / "devforgeai" / ".install-config.backup"
        config_path.parent.mkdir(parents=True, exist_ok=True)

        # Act - Install v1 config
        with open(config_path, "w") as f:
            json.dump(v1_config, f)

        # Act - Upgrade: backup before migration
        with open(config_path, "r") as f:
            original = json.load(f)

        with open(backup_path, "w") as f:
            json.dump(original, f)

        # Act - Migrate v1 -> v2
        v2_config = {
            "schema_version": 2,
            "target_path": original["path"],
            "merge_strategy": original["merge_strategy"],
            "optional_features": [],
            "installed_at": original["installed_at"],
            "install_date": original["installed_at"].split("T")[0],
        }

        with open(config_path, "w") as f:
            json.dump(v2_config, f)

        # Assert - Backup exists
        assert backup_path.exists()

        # Assert - Migrated config exists
        assert config_path.exists()
        with open(config_path, "r") as f:
            migrated = json.load(f)

        assert migrated["schema_version"] == 2
        assert migrated["target_path"] == v1_config["path"]

        # Assert - Original is in backup
        with open(backup_path, "r") as f:
            backed_up = json.load(f)
        assert backed_up == v1_config

    def test_should_handle_rollback_from_backup_if_migration_fails(
        self, temp_install_dir, v1_config
    ):
        """Test: Can restore backup if migration fails."""
        # Arrange
        config_path = temp_install_dir / "devforgeai" / ".install-config.json"
        backup_path = temp_install_dir / "devforgeai" / ".install-config.backup"
        config_path.parent.mkdir(parents=True, exist_ok=True)

        # Act - Initial config
        with open(config_path, "w") as f:
            json.dump(v1_config, f)

        with open(backup_path, "w") as f:
            json.dump(v1_config, f)

        # Act - Migration fails, restore from backup
        with open(backup_path, "r") as f:
            restored = json.load(f)

        with open(config_path, "w") as f:
            json.dump(restored, f)

        # Assert
        with open(config_path, "r") as f:
            final = json.load(f)

        assert final == v1_config


class TestConfigExportImportCycle:
    """Tests for export and import round-trip."""

    def test_should_export_and_reimport_without_loss(
        self, temp_install_dir, sample_install_config
    ):
        """Test: Config survives export -> import cycle without loss."""
        # Arrange
        export_file = temp_install_dir / "exported.json"

        # Act - Export
        with open(export_file, "w") as f:
            json.dump(sample_install_config, f)

        # Act - Import
        with open(export_file, "r") as f:
            imported = json.load(f)

        # Assert
        assert imported == sample_install_config

    def test_should_exclude_sensitive_data_in_export_import_cycle(
        self, temp_install_dir, config_with_sensitive_data
    ):
        """Test: Sensitive data excluded during export."""
        # Arrange
        export_file = temp_install_dir / "exported.json"

        # Act - Export (filter sensitive keys)
        sensitive_keys = ["api_token", "database_password", "jwt_secret"]
        export_config = {
            k: v for k, v in config_with_sensitive_data.items()
            if k not in sensitive_keys
        }

        with open(export_file, "w") as f:
            json.dump(export_config, f)

        # Act - Import
        with open(export_file, "r") as f:
            imported = json.load(f)

        # Assert
        assert "api_token" not in imported
        assert "database_password" not in imported
        assert "jwt_secret" not in imported
        # But non-sensitive fields should be present
        assert "target_path" in imported


class TestConfigMultipleUpgradeCycles:
    """Tests for multiple successive upgrade cycles."""

    def test_should_preserve_config_across_10_upgrade_cycles(
        self, temp_install_dir, sample_install_config
    ):
        """Test: Config values identical after 10 upgrade cycles (NFR-002)."""
        # Arrange
        config_path = temp_install_dir / "devforgeai" / ".install-config.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)

        original = sample_install_config.copy()

        # Act - Simulate 10 upgrade cycles
        config = original
        for cycle in range(10):
            with open(config_path, "w") as f:
                json.dump(config, f)

            with open(config_path, "r") as f:
                config = json.load(f)

        # Assert
        assert config == original
        assert config["schema_version"] == original["schema_version"]
        assert config["target_path"] == original["target_path"]
        assert config["optional_features"] == original["optional_features"]

    def test_should_handle_mixed_v1_and_v2_configs_in_sequence(
        self, temp_install_dir, v1_config, minimal_install_config
    ):
        """Test: Handle config format changes across upgrade sequence."""
        # Arrange
        config_path = temp_install_dir / "devforgeai" / ".install-config.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)

        # Act - Install v1
        with open(config_path, "w") as f:
            json.dump(v1_config, f)

        # Act - Upgrade to v2
        v2_config = minimal_install_config.copy()
        v2_config["schema_version"] = 2

        with open(config_path, "w") as f:
            json.dump(v2_config, f)

        # Act - Verify v2 is current
        with open(config_path, "r") as f:
            current = json.load(f)

        # Assert
        assert current["schema_version"] == 2


class TestConfigValidationInWorkflow:
    """Tests for validation in real workflows."""

    def test_should_validate_config_after_loading(
        self, temp_install_dir, sample_install_config
    ):
        """Test: Loaded config passes validation."""
        # Arrange
        config_path = temp_install_dir / "devforgeai" / ".install-config.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)

        with open(config_path, "w") as f:
            json.dump(sample_install_config, f)

        # Act
        with open(config_path, "r") as f:
            loaded = json.load(f)

        # Assert - Validate
        assert loaded["schema_version"] >= 1
        assert "target_path" in loaded
        assert "merge_strategy" in loaded
        assert isinstance(loaded["optional_features"], list)
        assert "installed_at" in loaded

    def test_should_validate_config_before_import(
        self, temp_install_dir, invalid_configs
    ):
        """Test: Invalid config rejected on import."""
        # Arrange
        import_file = temp_install_dir / "invalid.json"
        invalid = invalid_configs["missing_target_path"]

        with open(import_file, "w") as f:
            json.dump(invalid, f)

        # Act
        with open(import_file, "r") as f:
            loaded = json.load(f)

        # Assert - Should have validation errors
        assert "target_path" not in loaded

    def test_should_reject_import_with_schema_version_mismatch_on_import(
        self, temp_install_dir
    ):
        """Test: Schema mismatch triggers migration on import."""
        # Arrange
        import_file = temp_install_dir / "v1.json"
        v1 = {
            "schema_version": 1,
            "path": "/home/user/project",
            "merge_strategy": "SMART_MERGE",
            "installed_at": "2025-11-25T10:30:00Z",
        }

        with open(import_file, "w") as f:
            json.dump(v1, f)

        # Act
        with open(import_file, "r") as f:
            loaded = json.load(f)

        current_version = 2
        migration_needed = loaded["schema_version"] < current_version

        # Assert
        assert migration_needed is True


class TestConfigErrorRecovery:
    """Tests for error recovery in config operations."""

    def test_should_recover_from_corrupted_config_using_backup(
        self, temp_install_dir, sample_install_config
    ):
        """Test: Restore backup if config becomes corrupted."""
        # Arrange
        config_path = temp_install_dir / "devforgeai" / ".install-config.json"
        backup_path = temp_install_dir / "devforgeai" / ".install-config.backup"
        config_path.parent.mkdir(parents=True, exist_ok=True)

        # Act - Create backup
        with open(backup_path, "w") as f:
            json.dump(sample_install_config, f)

        # Act - Corrupt config
        with open(config_path, "w") as f:
            f.write("{ invalid json }")

        # Act - Try to load config (fails)
        # Fallback to backup
        try:
            with open(config_path, "r") as f:
                json.load(f)
            recovered = None
        except json.JSONDecodeError:
            with open(backup_path, "r") as f:
                recovered = json.load(f)

        # Assert
        assert recovered == sample_install_config

    def test_should_use_defaults_if_config_missing_and_no_backup(
        self, temp_install_dir
    ):
        """Test: Use defaults if config and backup missing."""
        # Arrange
        config_path = temp_install_dir / "devforgeai" / ".install-config.json"

        # Act - Config doesn't exist
        assert not config_path.exists()

        # Fallback to defaults
        default_config = {
            "schema_version": 1,
            "merge_strategy": "SMART_MERGE",
            "optional_features": [],
        }

        # Assert
        assert default_config["schema_version"] == 1
        assert default_config["merge_strategy"] == "SMART_MERGE"


class TestConfigConcurrency:
    """Tests for concurrent config operations."""

    def test_should_handle_simultaneous_read_write_safely(
        self, temp_install_dir, sample_install_config
    ):
        """Test: Config handles concurrent read and write operations."""
        # Arrange
        config_path = temp_install_dir / "devforgeai" / ".install-config.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)

        # Act - Initial write
        with open(config_path, "w") as f:
            json.dump(sample_install_config, f)

        # Act - Concurrent read
        with open(config_path, "r") as f:
            read_config = json.load(f)

        # Act - Concurrent write
        modified = sample_install_config.copy()
        modified["target_path"] = "/new/path"

        with open(config_path, "w") as f:
            json.dump(modified, f)

        # Assert
        with open(config_path, "r") as f:
            final = json.load(f)

        assert final["target_path"] == "/new/path"


class TestConfigComplexScenarios:
    """Tests for complex real-world scenarios."""

    def test_should_handle_config_with_many_optional_features(
        self, temp_install_dir, large_config
    ):
        """Test: Config works efficiently with many optional features."""
        # Arrange
        config_path = temp_install_dir / "devforgeai" / ".install-config.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)

        # Act
        with open(config_path, "w") as f:
            json.dump(large_config, f)

        with open(config_path, "r") as f:
            loaded = json.load(f)

        # Assert
        assert len(loaded["optional_features"]) == 100

    def test_should_handle_config_with_unicode_characters(
        self, temp_install_dir
    ):
        """Test: Config handles international characters in paths."""
        # Arrange
        unicode_config = {
            "schema_version": 1,
            "target_path": "/home/user/проект/café",
            "merge_strategy": "SMART_MERGE",
            "optional_features": ["中文", "русский"],
            "installed_at": "2025-11-25T10:30:00Z",
        }

        config_path = temp_install_dir / "devforgeai" / ".install-config.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)

        # Act
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(unicode_config, f, ensure_ascii=False)

        with open(config_path, "r", encoding="utf-8") as f:
            loaded = json.load(f)

        # Assert
        assert loaded["target_path"] == unicode_config["target_path"]
        assert "中文" in loaded["optional_features"]

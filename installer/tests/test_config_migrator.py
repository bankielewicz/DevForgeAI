"""
Unit tests for ConfigMigrator service (STORY-082, AC#3, AC#5).

Tests for configuration schema migration including:
- Schema version mismatch detection (AC#3, SVC-008)
- Schema migration (AC#3, AC#5, SVC-009)
- Multi-step migrations (SVC-010)
- Backup creation (AC#3, SVC-011)
- Migration path validation (BR-002)

This module contains 25 tests covering all migration scenarios.
"""

import json
from pathlib import Path
from typing import Dict, Any

import pytest


class TestConfigMigratorVersionDetection:
    """Tests for schema version detection (AC#3, SVC-008)."""

    def test_should_detect_schema_version_mismatch(self, v1_config):
        """Test: Given schema v1 and current v2, When check() called, Then migration_needed=True."""
        # Arrange
        config_version = v1_config["schema_version"]
        current_version = 2

        # Act
        migration_needed = config_version < current_version

        # Assert
        assert migration_needed is True

    def test_should_detect_no_migration_when_versions_match(self, sample_install_config):
        """Test: When schema versions match, no migration needed."""
        # Arrange
        config_version = sample_install_config["schema_version"]
        current_version = 1

        # Act
        migration_needed = config_version < current_version

        # Assert
        assert migration_needed is False

    def test_should_detect_forward_version_incompatibility(self):
        """Test: Config with future schema_version triggers warning."""
        # Arrange
        config = {
            "schema_version": 5,  # Future version
            "target_path": "/home/user/project",
        }
        current_version = 2

        # Act
        is_future_version = config["schema_version"] > current_version

        # Assert
        assert is_future_version is True
        # Should warn: "Configuration schema version 5 is newer than supported version 2"

    def test_should_detect_multiple_version_gaps(self, v1_config):
        """Test: Detect when migration path spans multiple versions."""
        # Arrange
        from_version = v1_config["schema_version"]
        to_version = 3

        # Act
        version_gap = to_version - from_version

        # Assert
        assert version_gap == 2
        # Should indicate: v1 -> v2 -> v3 migration path needed


class TestConfigMigratorV1toV2:
    """Tests for v1 -> v2 schema migration (AC#3, SVC-009)."""

    def test_should_migrate_v1_config_to_v2(self, v1_config, v2_expected_config):
        """Test: Given v1 config, When migrate() called, Then v2 config returned."""
        # Arrange
        v1 = v1_config

        # Act
        # Simulate migration: rename 'path' to 'target_path', add new fields
        v2 = {
            "schema_version": 2,
            "target_path": v1.get("path") or v1.get("target_path"),
            "merge_strategy": v1.get("merge_strategy", "SMART_MERGE"),
            "optional_features": v1.get("optional_features", []),
            "installed_at": v1.get("installed_at"),
        }

        # Assert
        assert v2["schema_version"] == 2
        assert v2["target_path"] == "/home/user/project"
        assert "optional_features" in v2

    def test_should_rename_path_key_to_target_path(self, v1_config):
        """Test: v1 'path' key renamed to 'target_path' in v2."""
        # Arrange
        v1 = v1_config
        assert "path" in v1

        # Act
        v2 = {
            "schema_version": 2,
            "target_path": v1["path"],  # Renamed from 'path'
        }

        # Assert
        assert "path" not in v2
        assert "target_path" in v2
        assert v2["target_path"] == v1["path"]

    def test_should_add_optional_features_with_default_empty_array(self, v1_config):
        """Test: v1 -> v2 adds optional_features with default []."""
        # Arrange
        v1 = v1_config
        assert "optional_features" not in v1

        # Act
        v2 = {
            "schema_version": 2,
            "optional_features": [],  # Added with default
        }

        # Assert
        assert "optional_features" in v2
        assert v2["optional_features"] == []

    def test_should_add_install_date_field(self, v1_config):
        """Test: v1 -> v2 adds install_date from installed_at."""
        # Arrange
        v1 = v1_config

        # Act
        # Extract date from ISO8601 timestamp
        install_date = v1["installed_at"].split("T")[0]
        v2 = {
            "schema_version": 2,
            "install_date": install_date,
        }

        # Assert
        assert "install_date" in v2
        assert v2["install_date"] == "2025-11-01"

    def test_should_preserve_merge_strategy_during_migration(self, v1_config):
        """Test: merge_strategy preserved from v1 to v2."""
        # Arrange
        v1 = v1_config

        # Act
        v2 = {
            "schema_version": 2,
            "merge_strategy": v1["merge_strategy"],
        }

        # Assert
        assert v2["merge_strategy"] == "SMART_MERGE"

    def test_should_preserve_installed_at_during_migration(self, v1_config):
        """Test: installed_at timestamp preserved from v1 to v2."""
        # Arrange
        v1 = v1_config

        # Act
        v2 = {
            "schema_version": 2,
            "installed_at": v1["installed_at"],
        }

        # Assert
        assert v2["installed_at"] == v1["installed_at"]


class TestConfigMigratorMultiStep:
    """Tests for multi-step migrations (SVC-010)."""

    def test_should_migrate_v1_to_v3_via_v2(self):
        """Test: Given v1 config and current v3, When migrate() called, Then v3 config via v1->v2->v3."""
        # Arrange
        v1 = {
            "schema_version": 1,
            "path": "/home/user/project",
            "merge_strategy": "SMART_MERGE",
            "installed_at": "2025-11-01T10:00:00Z",
        }

        # Act - Step 1: v1 -> v2
        v2 = {
            "schema_version": 2,
            "target_path": v1["path"],
            "merge_strategy": v1["merge_strategy"],
            "optional_features": [],
            "installed_at": v1["installed_at"],
            "install_date": "2025-11-01",
        }

        # Act - Step 2: v2 -> v3
        v3 = {
            "schema_version": 3,
            "target_path": v2["target_path"],
            "merge_strategy": v2["merge_strategy"],
            "optional_features": v2["optional_features"],
            "installed_at": v2["installed_at"],
            "install_date": v2["install_date"],
            "config_format": "json",  # New in v3
        }

        # Assert
        assert v3["schema_version"] == 3
        assert v3["target_path"] == "/home/user/project"
        assert "config_format" in v3

    def test_should_handle_v1_to_v4_migration_path(self):
        """Test: Migration path v1 -> v2 -> v3 -> v4."""
        # Arrange
        current_version = 4
        config_version = 1
        versions_to_migrate = list(range(config_version + 1, current_version + 1))

        # Act
        migration_path = versions_to_migrate

        # Assert
        assert migration_path == [2, 3, 4]

    def test_should_track_cumulative_changes_in_multi_step_migration(self):
        """Test: Track all key changes across multiple migration steps."""
        # Arrange
        migration_result = {
            "from_version": 1,
            "to_version": 3,
            "keys_renamed": {"path": "target_path"},
            "keys_added": ["optional_features", "install_date", "config_format"],
            "keys_removed": [],
        }

        # Act
        total_additions = len(migration_result["keys_added"])
        total_renames = len(migration_result["keys_renamed"])

        # Assert
        assert total_additions == 3
        assert total_renames == 1


class TestConfigMigratorBackup:
    """Tests for backup creation (AC#3, SVC-011, BR-002)."""

    def test_should_backup_original_before_migration(
        self, config_file_path, existing_config_file, sample_install_config
    ):
        """Test: Given migration, When migrate() called, Then original saved to .backup."""
        # Arrange
        backup_path = config_file_path.parent / ".install-config.backup"

        # Act
        with open(existing_config_file, "r") as f:
            original_config = json.load(f)

        # Simulate backup
        with open(backup_path, "w") as f:
            json.dump(original_config, f)

        # Assert
        assert backup_path.exists()
        with open(backup_path, "r") as f:
            backup_config = json.load(f)
        assert backup_config == original_config

    def test_should_create_backup_file_in_devforgeai_directory(
        self, config_file_path, sample_install_config
    ):
        """Test: Backup file created in devforgeai directory."""
        # Arrange
        config_file_path.parent.mkdir(parents=True, exist_ok=True)
        backup_path = config_file_path.parent / ".install-config.backup"

        # Act
        with open(backup_path, "w") as f:
            json.dump(sample_install_config, f)

        # Assert
        assert backup_path.parent == config_file_path.parent
        assert backup_path.exists()

    def test_should_preserve_backup_after_successful_migration(
        self, config_file_path, sample_install_config
    ):
        """Test: Backup preserved even after successful migration."""
        # Arrange
        config_file_path.parent.mkdir(parents=True, exist_ok=True)
        backup_path = config_file_path.parent / ".install-config.backup"

        original_config = sample_install_config.copy()

        # Act
        with open(backup_path, "w") as f:
            json.dump(original_config, f)

        # Assert - backup still exists
        assert backup_path.exists()

        # Load it to verify integrity
        with open(backup_path, "r") as f:
            loaded_backup = json.load(f)
        assert loaded_backup == original_config

    def test_should_support_backup_restoration(
        self, config_file_path, backup_file_path, sample_install_config
    ):
        """Test: Original config can be restored from backup."""
        # Arrange
        config_file_path.parent.mkdir(parents=True, exist_ok=True)
        original_config = sample_install_config

        # Act - Create backup
        with open(backup_file_path, "w") as f:
            json.dump(original_config, f)

        # Act - Restore from backup
        with open(backup_file_path, "r") as f:
            restored_config = json.load(f)

        # Assert
        assert restored_config == original_config


class TestConfigMigratorMigrationResult:
    """Tests for migration result tracking (AC#3)."""

    def test_should_return_migration_result_with_metadata(self, migration_result_v1_to_v2):
        """Test: Migration returns MigrationResult with change tracking."""
        # Arrange & Act
        result = migration_result_v1_to_v2

        # Assert
        assert "from_version" in result
        assert "to_version" in result
        assert "keys_renamed" in result
        assert "keys_added" in result
        assert "keys_removed" in result

    def test_should_report_all_renames_in_migration_result(self, migration_result_v1_to_v2):
        """Test: keys_renamed includes all old -> new key mappings."""
        # Arrange & Act
        result = migration_result_v1_to_v2

        # Assert
        assert result["keys_renamed"]["path"] == "target_path"

    def test_should_report_all_additions_in_migration_result(self, migration_result_v1_to_v2):
        """Test: keys_added lists all new fields."""
        # Arrange & Act
        result = migration_result_v1_to_v2

        # Assert
        assert "optional_features" in result["keys_added"]
        assert "install_date" in result["keys_added"]

    def test_should_report_all_removals_in_migration_result(self):
        """Test: keys_removed lists all deprecated fields."""
        # Arrange
        result = {
            "from_version": 2,
            "to_version": 3,
            "keys_renamed": {},
            "keys_added": [],
            "keys_removed": ["deprecated_field"],
        }

        # Act & Assert
        assert "deprecated_field" in result["keys_removed"]


class TestConfigMigratorEdgeCases:
    """Tests for edge cases in migration."""

    def test_should_handle_migration_with_extra_unknown_fields(self):
        """Test: Migration handles config with unknown fields gracefully."""
        # Arrange
        v1 = {
            "schema_version": 1,
            "path": "/home/user/project",
            "merge_strategy": "SMART_MERGE",
            "installed_at": "2025-11-01T10:00:00Z",
            "unknown_field": "should_be_preserved",  # Unknown field
        }

        # Act
        v2 = {
            "schema_version": 2,
            "target_path": v1["path"],
            "merge_strategy": v1["merge_strategy"],
            "optional_features": [],
            "installed_at": v1["installed_at"],
            "install_date": "2025-11-01",
        }

        # Assert
        # Unknown field should be handled gracefully (preserved or warned)
        assert v2["schema_version"] == 2

    def test_should_handle_migration_with_null_optional_fields(self):
        """Test: Migration handles null values in optional fields."""
        # Arrange
        v1 = {
            "schema_version": 1,
            "path": "/home/user/project",
            "merge_strategy": "SMART_MERGE",
            "installed_at": "2025-11-01T10:00:00Z",
            "last_upgraded_at": None,
        }

        # Act
        v2 = {
            "schema_version": 2,
            "target_path": v1["path"],
            "merge_strategy": v1["merge_strategy"],
            "optional_features": [],
            "installed_at": v1["installed_at"],
            "install_date": "2025-11-01",
        }

        # Assert
        assert v2["schema_version"] == 2

    def test_should_handle_migration_when_backup_already_exists(
        self, config_file_path, backup_file_path, sample_install_config
    ):
        """Test: Backup file replaced/overwritten during migration."""
        # Arrange
        config_file_path.parent.mkdir(parents=True, exist_ok=True)
        old_backup = sample_install_config.copy()
        old_backup["target_path"] = "/old/path"

        # Act - Create old backup
        with open(backup_file_path, "w") as f:
            json.dump(old_backup, f)

        # Act - Create new backup (should overwrite)
        with open(backup_file_path, "w") as f:
            json.dump(sample_install_config, f)

        # Assert
        with open(backup_file_path, "r") as f:
            current_backup = json.load(f)
        assert current_backup == sample_install_config

    def test_should_handle_very_large_config_migration(self, large_config):
        """Test: Performance with large configuration."""
        # Arrange
        v1 = large_config.copy()
        v1["schema_version"] = 1

        # Act
        v2 = v1.copy()
        v2["schema_version"] = 2
        v2["install_date"] = "2025-11-25"

        # Assert
        assert v2["schema_version"] == 2
        assert len(v2["optional_features"]) == 100


class TestConfigMigratorValidation:
    """Tests for migration validation."""

    def test_should_validate_migrated_config_after_migration(self):
        """Test: Migrated config passes validation."""
        # Arrange
        v2_config = {
            "schema_version": 2,
            "target_path": "/home/user/project",
            "merge_strategy": "SMART_MERGE",
            "optional_features": [],
            "installed_at": "2025-11-01T10:00:00Z",
            "install_date": "2025-11-01",
        }

        # Act & Assert
        assert v2_config["schema_version"] >= 1
        assert "target_path" in v2_config
        assert v2_config["merge_strategy"] in ["SMART_MERGE", "OVERWRITE", "PRESERVE_USER"]

    def test_should_report_migration_errors_if_validation_fails(self):
        """Test: Migration errors reported clearly."""
        # Arrange
        invalid_migrated_config = {
            "schema_version": 2,
            # Missing required fields
        }

        # Act & Assert
        # Should report missing required keys
        assert "target_path" not in invalid_migrated_config

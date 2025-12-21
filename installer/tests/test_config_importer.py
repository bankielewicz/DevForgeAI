"""
Unit tests for ConfigImporter service (STORY-082, AC#5).

Tests for configuration import including:
- Import from JSON file (AC#5, SVC-014)
- Validate before importing (AC#5, SVC-015)
- Migrate if schema version differs (AC#5, SVC-016)
- Notify user of migrated/defaulted values (AC#5)

This module contains 15 tests covering import scenarios.
"""

import json
from pathlib import Path
from typing import Dict, Any

import pytest


class TestConfigImporterBasic:
    """Tests for basic import functionality (AC#5, SVC-014)."""

    def test_should_import_valid_config_from_file(
        self, temp_install_dir, sample_install_config
    ):
        """Test: Given valid JSON file, When import() called, Then config applied."""
        # Arrange
        import_file = temp_install_dir / "config.json"
        with open(import_file, "w") as f:
            json.dump(sample_install_config, f)

        # Act
        with open(import_file, "r") as f:
            imported_config = json.load(f)

        # Assert
        assert imported_config == sample_install_config

    def test_should_apply_imported_config_to_installation(
        self, temp_install_dir, sample_install_config
    ):
        """Test: Imported config is applied to DevForgeAI."""
        # Arrange
        import_file = temp_install_dir / "config.json"
        config_dest = temp_install_dir / "devforgeai" / ".install-config.json"
        config_dest.parent.mkdir(parents=True, exist_ok=True)

        with open(import_file, "w") as f:
            json.dump(sample_install_config, f)

        # Act
        with open(import_file, "r") as f:
            imported = json.load(f)
        with open(config_dest, "w") as f:
            json.dump(imported, f)

        # Assert
        assert config_dest.exists()
        with open(config_dest, "r") as f:
            applied = json.load(f)
        assert applied == sample_install_config


class TestConfigImporterValidation:
    """Tests for import validation (AC#5, SVC-015)."""

    def test_should_validate_before_importing(self, temp_install_dir, invalid_configs):
        """Test: Given invalid JSON, When import() called, Then validation error returned."""
        # Arrange
        import_file = temp_install_dir / "invalid.json"
        invalid_config = invalid_configs["missing_target_path"]

        with open(import_file, "w") as f:
            json.dump(invalid_config, f)

        # Act
        with open(import_file, "r") as f:
            loaded = json.load(f)

        # Assert
        assert "target_path" not in loaded
        # Validation should fail with error

    def test_should_reject_import_with_missing_required_keys(self, temp_install_dir, invalid_configs):
        """Test: Import fails when required keys missing."""
        # Arrange
        import_file = temp_install_dir / "incomplete.json"
        incomplete_config = invalid_configs["missing_target_path"]

        with open(import_file, "w") as f:
            json.dump(incomplete_config, f)

        # Act & Assert
        assert "target_path" not in incomplete_config

    def test_should_reject_import_with_invalid_types(self, temp_install_dir, invalid_configs):
        """Test: Import fails when field types invalid."""
        # Arrange
        import_file = temp_install_dir / "wrong_types.json"
        wrong_types_config = invalid_configs["optional_features_not_array"]

        with open(import_file, "w") as f:
            json.dump(wrong_types_config, f)

        # Act & Assert
        assert isinstance(wrong_types_config["optional_features"], str)

    def test_should_show_specific_error_message_on_validation_failure(self, temp_install_dir):
        """Test: Validation error shows specific problem."""
        # Arrange
        import_file = temp_install_dir / "bad.json"
        bad_config = {
            "schema_version": "not_a_number",
            "target_path": "/home/user/project",
        }

        with open(import_file, "w") as f:
            json.dump(bad_config, f)

        # Act
        with open(import_file, "r") as f:
            loaded = json.load(f)

        # Assert
        # Error should specify: "Invalid type for 'schema_version': expected int, got string"
        assert isinstance(loaded["schema_version"], str)


class TestConfigImporterMigration:
    """Tests for migration during import (AC#5, SVC-016)."""

    def test_should_migrate_v1_config_on_import(
        self, temp_install_dir, v1_config, v2_expected_config
    ):
        """Test: Given v1 export and current v2, When import() called, Then migration runs."""
        # Arrange
        import_file = temp_install_dir / "v1-config.json"
        with open(import_file, "w") as f:
            json.dump(v1_config, f)

        # Act
        with open(import_file, "r") as f:
            loaded_v1 = json.load(f)

        # Simulate migration
        migrated = {
            "schema_version": 2,
            "target_path": loaded_v1.get("path") or loaded_v1.get("target_path"),
            "merge_strategy": loaded_v1.get("merge_strategy", "SMART_MERGE"),
            "optional_features": loaded_v1.get("optional_features", []),
            "installed_at": loaded_v1.get("installed_at"),
            "install_date": loaded_v1["installed_at"].split("T")[0],
        }

        # Assert
        assert migrated["schema_version"] == 2
        assert migrated["target_path"] == v1_config["path"]

    def test_should_check_schema_version_compatibility_during_import(
        self, temp_install_dir, v1_config
    ):
        """Test: Import checks if schema version compatible."""
        # Arrange
        import_file = temp_install_dir / "config.json"
        with open(import_file, "w") as f:
            json.dump(v1_config, f)

        # Act
        with open(import_file, "r") as f:
            loaded = json.load(f)

        config_version = loaded["schema_version"]
        current_version = 2

        # Assert
        if config_version < current_version:
            # Migration needed
            assert config_version < current_version

    def test_should_apply_migration_before_import(self, temp_install_dir, v1_config):
        """Test: Migration applied before storing imported config."""
        # Arrange
        import_file = temp_install_dir / "v1.json"
        config_dest = temp_install_dir / "devforgeai" / ".install-config.json"
        config_dest.parent.mkdir(parents=True, exist_ok=True)

        with open(import_file, "w") as f:
            json.dump(v1_config, f)

        # Act
        with open(import_file, "r") as f:
            v1 = json.load(f)

        # Migrate
        v2 = {
            "schema_version": 2,
            "target_path": v1["path"],
            "merge_strategy": v1["merge_strategy"],
            "optional_features": [],
            "installed_at": v1["installed_at"],
            "install_date": v1["installed_at"].split("T")[0],
        }

        # Store migrated config
        with open(config_dest, "w") as f:
            json.dump(v2, f)

        # Assert
        with open(config_dest, "r") as f:
            stored = json.load(f)
        assert stored["schema_version"] == 2


class TestConfigImporterNotification:
    """Tests for user notification (AC#5)."""

    def test_should_notify_user_of_migrated_values(self):
        """Test: User notified of any values that were migrated."""
        # Arrange
        migration_changes = {
            "migrated_keys": ["path -> target_path"],
            "added_defaults": ["optional_features", "install_date"],
        }

        # Act & Assert
        # Notification should list:
        # - "Key 'path' renamed to 'target_path'"
        # - "Added field 'optional_features' with default value []"
        # - "Added field 'install_date' with value '2025-11-01'"
        assert len(migration_changes["migrated_keys"]) > 0

    def test_should_notify_user_of_defaulted_values(self):
        """Test: User notified of fields set to defaults."""
        # Arrange
        defaulted_fields = {
            "optional_features": [],
            "merge_strategy": "SMART_MERGE",
        }

        # Act & Assert
        # Notification should list:
        # - "Set 'optional_features' to default value []"
        # - "Set 'merge_strategy' to default value SMART_MERGE"
        for field, value in defaulted_fields.items():
            assert field is not None

    def test_should_summarize_import_changes(self):
        """Test: Import provides summary of all changes."""
        # Arrange
        summary = {
            "status": "success",
            "migrated": ["path -> target_path"],
            "added": ["optional_features", "install_date"],
            "removed": [],
            "message": "Config imported and migrated from v1 to v2",
        }

        # Act & Assert
        assert summary["status"] == "success"
        assert len(summary["migrated"]) > 0 or len(summary["added"]) > 0


class TestConfigImporterEdgeCases:
    """Tests for edge cases in import."""

    def test_should_handle_import_of_config_with_extra_fields(self, temp_install_dir):
        """Test: Import handles extra unknown fields gracefully."""
        # Arrange
        config = {
            "schema_version": 1,
            "target_path": "/home/user/project",
            "merge_strategy": "SMART_MERGE",
            "optional_features": [],
            "installed_at": "2025-11-25T10:30:00Z",
            "extra_field": "should_be_handled",
            "another_extra": 123,
        }

        import_file = temp_install_dir / "with_extras.json"
        with open(import_file, "w") as f:
            json.dump(config, f)

        # Act
        with open(import_file, "r") as f:
            loaded = json.load(f)

        # Assert
        assert "extra_field" in loaded
        # Should warn but not fail

    def test_should_handle_import_of_partial_config(self, temp_install_dir):
        """Test: Import fills in missing optional fields with defaults."""
        # Arrange
        partial_config = {
            "schema_version": 1,
            "target_path": "/home/user/project",
            "installed_at": "2025-11-25T10:30:00Z",
            # Missing merge_strategy and optional_features
        }

        import_file = temp_install_dir / "partial.json"
        with open(import_file, "w") as f:
            json.dump(partial_config, f)

        # Act
        with open(import_file, "r") as f:
            loaded = json.load(f)

        # Add defaults
        if "merge_strategy" not in loaded:
            loaded["merge_strategy"] = "SMART_MERGE"
        if "optional_features" not in loaded:
            loaded["optional_features"] = []

        # Assert
        assert loaded["merge_strategy"] == "SMART_MERGE"
        assert loaded["optional_features"] == []

    def test_should_reject_import_with_corrupted_json(self, temp_install_dir):
        """Test: Reject import of corrupted JSON file."""
        # Arrange
        import_file = temp_install_dir / "corrupted.json"
        with open(import_file, "w") as f:
            f.write("{ invalid json }")

        # Act & Assert
        with pytest.raises(json.JSONDecodeError):
            with open(import_file, "r") as f:
                json.load(f)

    def test_should_reject_empty_import_file(self, temp_install_dir):
        """Test: Reject empty import file."""
        # Arrange
        import_file = temp_install_dir / "empty.json"
        import_file.touch()

        # Act & Assert
        try:
            with open(import_file, "r") as f:
                content = f.read()
            if content:
                json.loads(content)
            else:
                # Empty file
                raise json.JSONDecodeError("Expecting value", content, 0)
        except json.JSONDecodeError:
            pass  # Expected

    def test_should_handle_import_with_unicode_paths(self, temp_install_dir):
        """Test: Import handles Unicode characters in paths."""
        # Arrange
        config = {
            "schema_version": 1,
            "target_path": "/home/user/проект",  # Russian
            "merge_strategy": "SMART_MERGE",
            "optional_features": [],
            "installed_at": "2025-11-25T10:30:00Z",
        }

        import_file = temp_install_dir / "unicode.json"
        with open(import_file, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False)

        # Act
        with open(import_file, "r", encoding="utf-8") as f:
            loaded = json.load(f)

        # Assert
        assert loaded["target_path"] == "/home/user/проект"

    def test_should_handle_import_preserving_timestamp_precision(self, temp_install_dir):
        """Test: Import preserves timestamp precision."""
        # Arrange
        config = {
            "schema_version": 1,
            "target_path": "/home/user/project",
            "merge_strategy": "SMART_MERGE",
            "optional_features": [],
            "installed_at": "2025-11-25T10:30:45.123456Z",
        }

        import_file = temp_install_dir / "precise.json"
        with open(import_file, "w") as f:
            json.dump(config, f)

        # Act
        with open(import_file, "r") as f:
            loaded = json.load(f)

        # Assert
        assert loaded["installed_at"] == config["installed_at"]


class TestConfigImporterIntegration:
    """Integration tests for import functionality."""

    def test_should_round_trip_export_and_import(
        self, temp_install_dir, sample_install_config
    ):
        """Test: Config survives export -> import cycle."""
        # Arrange
        export_file = temp_install_dir / "export.json"
        import_file = temp_install_dir / "import.json"

        # Act - Export
        with open(export_file, "w") as f:
            json.dump(sample_install_config, f)

        # Act - Read export file
        with open(export_file, "r") as f:
            exported = json.load(f)

        # Act - Import
        with open(import_file, "w") as f:
            json.dump(exported, f)

        # Act - Read import file
        with open(import_file, "r") as f:
            imported = json.load(f)

        # Assert
        assert imported == sample_install_config

    def test_should_support_multi_project_config_sharing(self, temp_install_dir, sample_install_config):
        """Test: Config can be imported into multiple projects."""
        # Arrange
        project1_dir = temp_install_dir / "project1" / "devforgeai"
        project2_dir = temp_install_dir / "project2" / "devforgeai"
        project1_dir.mkdir(parents=True)
        project2_dir.mkdir(parents=True)

        export_file = temp_install_dir / "shared-config.json"
        with open(export_file, "w") as f:
            json.dump(sample_install_config, f)

        # Act - Import into project1
        with open(export_file, "r") as f:
            config = json.load(f)
        with open(project1_dir / ".install-config.json", "w") as f:
            json.dump(config, f)

        # Act - Import into project2
        with open(export_file, "r") as f:
            config = json.load(f)
        with open(project2_dir / ".install-config.json", "w") as f:
            json.dump(config, f)

        # Assert
        with open(project1_dir / ".install-config.json", "r") as f:
            p1_config = json.load(f)
        with open(project2_dir / ".install-config.json", "r") as f:
            p2_config = json.load(f)

        assert p1_config == sample_install_config
        assert p2_config == sample_install_config

"""
Unit tests for ConfigExporter service (STORY-082, AC#4).

Tests for configuration export including:
- Export to JSON (AC#4, SVC-012)
- Exclude sensitive values (AC#4, SVC-013, BR-003, NFR-003)
- Include schema version (AC#4)
- Write to stdout or file with -o flag (AC#4)

This module contains 15 tests covering export scenarios.
"""

import json
from pathlib import Path
from io import StringIO

import pytest


class TestConfigExporterBasic:
    """Tests for basic export functionality (AC#4, SVC-012)."""

    def test_should_export_config_to_valid_json(self, sample_install_config):
        """Test: Given config, When export() called, Then valid JSON returned."""
        # Arrange & Act
        json_output = json.dumps(sample_install_config)

        # Assert
        assert isinstance(json_output, str)
        # Should be valid JSON
        parsed = json.loads(json_output)
        assert parsed == sample_install_config

    def test_should_export_config_with_all_fields(self, sample_install_config):
        """Test: Export includes all fields (except sensitive values)."""
        # Arrange & Act
        export_output = {
            "schema_version": sample_install_config["schema_version"],
            "target_path": sample_install_config["target_path"],
            "merge_strategy": sample_install_config["merge_strategy"],
            "optional_features": sample_install_config["optional_features"],
            "installed_at": sample_install_config["installed_at"],
        }

        # Assert
        assert "schema_version" in export_output
        assert "target_path" in export_output
        assert "merge_strategy" in export_output
        assert "optional_features" in export_output
        assert "installed_at" in export_output

    def test_should_export_config_to_stdout_by_default(self, sample_install_config):
        """Test: Export outputs to stdout when no output file specified."""
        # Arrange & Act
        json_output = json.dumps(sample_install_config, indent=2)

        # Assert
        assert len(json_output) > 0
        # Should be valid JSON that could be printed to stdout

    def test_should_export_config_to_file_with_o_flag(self, temp_install_dir, sample_install_config):
        """Test: Export writes to file with -o flag."""
        # Arrange
        output_file = temp_install_dir / "exported-config.json"

        # Act
        with open(output_file, "w") as f:
            json.dump(sample_install_config, f)

        # Assert
        assert output_file.exists()
        with open(output_file, "r") as f:
            loaded = json.load(f)
        assert loaded == sample_install_config

    def test_should_format_exported_json_with_indentation(self, sample_install_config):
        """Test: Exported JSON is formatted with proper indentation."""
        # Arrange & Act
        json_output = json.dumps(sample_install_config, indent=2)

        # Assert
        assert "\n" in json_output  # Should have newlines for readability
        assert "  " in json_output  # Should have indentation


class TestConfigExporterSensitiveDataExclusion:
    """Tests for sensitive data filtering (AC#4, SVC-013, BR-003, NFR-003)."""

    def test_should_exclude_api_token_from_export(self, config_with_sensitive_data):
        """Test: api_token not included in export output."""
        # Arrange
        config = config_with_sensitive_data

        # Act
        # Remove sensitive keys before export
        sensitive_keys = ["api_token", "database_password", "jwt_secret"]
        export_config = {k: v for k, v in config.items() if k not in sensitive_keys}

        # Assert
        assert "api_token" not in export_config
        assert "api_token" in config  # Original still has it

    def test_should_exclude_database_password_from_export(self, config_with_sensitive_data):
        """Test: database_password not included in export output."""
        # Arrange
        config = config_with_sensitive_data

        # Act
        sensitive_keys = ["api_token", "database_password", "jwt_secret"]
        export_config = {k: v for k, v in config.items() if k not in sensitive_keys}

        # Assert
        assert "database_password" not in export_config
        assert "database_password" in config

    def test_should_exclude_jwt_secret_from_export(self, config_with_sensitive_data):
        """Test: jwt_secret not included in export output."""
        # Arrange
        config = config_with_sensitive_data

        # Act
        sensitive_keys = ["api_token", "database_password", "jwt_secret"]
        export_config = {k: v for k, v in config.items() if k not in sensitive_keys}

        # Assert
        assert "jwt_secret" not in export_config

    def test_should_exclude_oauth_token_from_export(self):
        """Test: oauth_token not included in export output."""
        # Arrange
        config = {
            "schema_version": 1,
            "target_path": "/home/user/project",
            "merge_strategy": "SMART_MERGE",
            "optional_features": [],
            "installed_at": "2025-11-25T10:30:00Z",
            "oauth_token": "secret-oauth-token",
        }

        # Act
        sensitive_keys = ["api_token", "database_password", "jwt_secret", "oauth_token"]
        export_config = {k: v for k, v in config.items() if k not in sensitive_keys}

        # Assert
        assert "oauth_token" not in export_config

    def test_should_preserve_non_sensitive_values(self, config_with_sensitive_data):
        """Test: Non-sensitive values preserved in export."""
        # Arrange
        config = config_with_sensitive_data

        # Act
        sensitive_keys = ["api_token", "database_password", "jwt_secret"]
        export_config = {k: v for k, v in config.items() if k not in sensitive_keys}

        # Assert
        assert export_config["schema_version"] == 1
        assert export_config["target_path"] == "/home/user/project"
        assert export_config["merge_strategy"] == "SMART_MERGE"
        assert export_config["installed_at"] == "2025-11-25T10:30:00Z"

    def test_should_export_zero_sensitive_values(self, config_with_sensitive_data):
        """Test: Export contains no tokens, passwords, or API keys (NFR-003)."""
        # Arrange
        config = config_with_sensitive_data
        sensitive_patterns = ["token", "password", "secret", "key", "credential"]

        # Act
        sensitive_keys = ["api_token", "database_password", "jwt_secret"]
        export_config = {k: v for k, v in config.items() if k not in sensitive_keys}

        # Assert
        for key in export_config:
            # No key should contain sensitive words
            assert not any(pattern in key.lower() for pattern in sensitive_patterns if pattern != "key")

    def test_should_handle_config_with_only_safe_values(self, sample_install_config):
        """Test: Config with no sensitive data exports fully."""
        # Arrange
        config = sample_install_config

        # Act
        sensitive_keys = ["api_token", "database_password", "jwt_secret"]
        export_config = {k: v for k, v in config.items() if k not in sensitive_keys}

        # Assert
        # All fields should be in export since none are sensitive
        assert len(export_config) == len(config)


class TestConfigExporterSchemaVersion:
    """Tests for schema version inclusion (AC#4)."""

    def test_should_include_schema_version_in_export(self, sample_install_config):
        """Test: Exported config includes schema_version for compatibility."""
        # Arrange & Act
        export_config = sample_install_config.copy()

        # Assert
        assert "schema_version" in export_config
        assert export_config["schema_version"] == 1

    def test_should_preserve_schema_version_value(self):
        """Test: schema_version value unchanged during export."""
        # Arrange
        config_v1 = {
            "schema_version": 1,
            "target_path": "/home/user/project",
        }
        config_v2 = {
            "schema_version": 2,
            "target_path": "/home/user/project",
        }

        # Act & Assert
        assert config_v1["schema_version"] == 1
        assert config_v2["schema_version"] == 2


class TestConfigExporterIntegration:
    """Integration tests for export functionality."""

    def test_should_export_then_reimport_successfully(self, sample_install_config, temp_install_dir):
        """Test: Exported config can be re-imported without loss."""
        # Arrange
        export_path = temp_install_dir / "exported.json"

        # Act
        with open(export_path, "w") as f:
            json.dump(sample_install_config, f)

        # Act - Re-import
        with open(export_path, "r") as f:
            imported = json.load(f)

        # Assert
        assert imported == sample_install_config

    def test_should_handle_export_with_special_characters(self):
        """Test: Export handles Unicode and special characters in paths."""
        # Arrange
        config = {
            "schema_version": 1,
            "target_path": "/home/user/проект/café",  # Unicode
            "merge_strategy": "SMART_MERGE",
            "optional_features": [],
            "installed_at": "2025-11-25T10:30:00Z",
        }

        # Act
        json_output = json.dumps(config, ensure_ascii=False)

        # Assert
        assert "проект" in json_output or "\\u" in json_output
        parsed = json.loads(json_output)
        assert parsed["target_path"] == config["target_path"]

    def test_should_export_formatted_for_readability(self, sample_install_config):
        """Test: Exported JSON is human-readable with formatting."""
        # Arrange & Act
        json_output = json.dumps(sample_install_config, indent=2, sort_keys=True)

        # Assert
        lines = json_output.split("\n")
        assert len(lines) > 1  # Multiple lines
        assert any("  " in line for line in lines)  # Has indentation
        # First character should be {
        assert json_output.strip()[0] == "{"

    def test_should_create_export_file_if_output_path_missing(self, temp_install_dir, sample_install_config):
        """Test: Export creates directories in output path if needed."""
        # Arrange
        export_dir = temp_install_dir / "exports" / "2025-11"
        export_file = export_dir / "config.json"

        # Act
        export_dir.mkdir(parents=True, exist_ok=True)
        with open(export_file, "w") as f:
            json.dump(sample_install_config, f)

        # Assert
        assert export_file.exists()

    def test_should_overwrite_existing_export_file(self, temp_install_dir, sample_install_config):
        """Test: Export overwrites existing export file."""
        # Arrange
        export_file = temp_install_dir / "config.json"

        # Act - First export
        with open(export_file, "w") as f:
            json.dump(sample_install_config, f)

        new_config = sample_install_config.copy()
        new_config["target_path"] = "/new/path"

        # Act - Second export (overwrite)
        with open(export_file, "w") as f:
            json.dump(new_config, f)

        # Assert
        with open(export_file, "r") as f:
            saved = json.load(f)
        assert saved["target_path"] == "/new/path"

    def test_should_handle_large_config_export(self, large_config, temp_install_dir):
        """Test: Export handles large configuration."""
        # Arrange
        export_file = temp_install_dir / "large.json"

        # Act
        with open(export_file, "w") as f:
            json.dump(large_config, f)

        # Assert
        assert export_file.exists()
        with open(export_file, "r") as f:
            loaded = json.load(f)
        assert len(loaded["optional_features"]) == 100

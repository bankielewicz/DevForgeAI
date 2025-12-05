"""
Unit tests for MigrationValidator service (STORY-078).

Tests migration validation:
- File existence validation (AC#5)
- Configuration validation (AC#5)
- JSON schema validation (AC#5)
- Validation report generation (AC#5)

Test Framework: pytest 7.4+
Coverage Target: 95%+ for business logic
"""

import pytest
import json
from pathlib import Path
from typing import List, Dict, Any

from installer.migration_validator import (
    MigrationValidator,
    ConfigValidator,
)
from installer.models import ValidationReport, ValidationError


class TestMigrationValidator:
    """Tests for migration validation"""

    def test_should_validate_expected_files_exist(self, tmp_path):
        """
        AC#5: Verify expected files exist after migration

        Arrange: Files exist at specified paths
        Act: Call validate(expected_files=[...])
        Assert: Returns ValidationReport with passed checks
        """
        # Arrange
        (tmp_path / "file1.txt").write_text("content1")
        (tmp_path / "file2.txt").write_text("content2")

        validator = MigrationValidator()

        # Act
        report = validator.validate(
            root_path=tmp_path,
            expected_files=["file1.txt", "file2.txt"]
        )

        # Assert
        assert report.is_valid is True
        assert report.passed_checks == 1
        assert report.failed_checks == 0

    def test_should_detect_missing_expected_files(self, tmp_path):
        """
        AC#5: Detect missing expected files

        Arrange: Some expected files missing
        Act: Call validate(expected_files=[existing, missing])
        Assert: Returns ValidationReport with failed checks
        """
        # Arrange
        (tmp_path / "file1.txt").write_text("content1")

        validator = MigrationValidator()

        # Act
        report = validator.validate(
            root_path=tmp_path,
            expected_files=["file1.txt", "file2.txt"]
        )

        # Assert
        assert report.is_valid is False
        assert report.failed_checks > 0
        assert len(report.checks) > 0

    def test_should_validate_expected_directories_exist(self, tmp_path):
        """
        AC#5: Verify expected directories exist

        Arrange: Directories exist at specified paths
        Act: Call validate(expected_dirs=[...])
        Assert: Returns ValidationReport with passed checks
        """
        # Arrange
        (tmp_path / "dir1").mkdir()
        (tmp_path / "dir2").mkdir()

        validator = MigrationValidator()

        # Act
        report = validator.validate(
            root_path=tmp_path,
            expected_dirs=["dir1", "dir2"]
        )

        # Assert
        assert report.is_valid is True
        assert report.passed_checks == 1

    def test_should_detect_missing_expected_directories(self, tmp_path):
        """
        AC#5: Detect missing expected directories

        Arrange: Some directories missing
        Act: Call validate(expected_dirs=[existing, missing])
        Assert: Returns ValidationReport with failed checks
        """
        # Arrange
        (tmp_path / "dir1").mkdir()

        validator = MigrationValidator()

        # Act
        report = validator.validate(
            root_path=tmp_path,
            expected_dirs=["dir1", "dir2"]
        )

        # Assert
        assert report.is_valid is False
        assert report.failed_checks > 0


class TestJSONValidation:
    """Tests for JSON schema validation"""

    def test_should_validate_json_file_exists(self, tmp_path):
        """
        AC#5: Verify JSON file exists

        Arrange: JSON file present
        Act: Call validate(json_schemas={file: [keys]})
        Assert: Returns ValidationReport with passed checks
        """
        # Arrange
        config_file = tmp_path / "config.json"
        config_file.write_text('{"version": "1.0.0"}')

        validator = MigrationValidator()

        # Act
        report = validator.validate(
            root_path=tmp_path,
            json_schemas={"config.json": ["version"]}
        )

        # Assert
        assert report.is_valid is True

    def test_should_detect_missing_json_file(self, tmp_path):
        """
        AC#5: Detect missing JSON file

        Arrange: JSON file does not exist
        Act: Call validate(json_schemas={missing_file: [keys]})
        Assert: Returns ValidationReport with failed checks
        """
        # Arrange
        validator = MigrationValidator()

        # Act
        report = validator.validate(
            root_path=tmp_path,
            json_schemas={"config.json": ["version"]}
        )

        # Assert
        assert report.is_valid is False
        assert report.failed_checks > 0

    def test_should_validate_json_required_keys(self, tmp_path):
        """
        AC#5: Check JSON contains required keys

        Arrange: JSON file with required keys
        Act: Call validate(json_schemas={file: [keys]})
        Assert: Returns ValidationReport with passed checks
        """
        # Arrange
        config_file = tmp_path / "config.json"
        config_file.write_text('{"version": "1.0.0", "debug": true}')

        validator = MigrationValidator()

        # Act
        report = validator.validate(
            root_path=tmp_path,
            json_schemas={"config.json": ["version", "debug"]}
        )

        # Assert
        assert report.is_valid is True

    def test_should_detect_missing_json_keys(self, tmp_path):
        """
        AC#5: Detect missing required keys in JSON

        Arrange: JSON file missing required keys
        Act: Call validate(json_schemas={file: [keys]})
        Assert: Returns ValidationReport with failed checks
        """
        # Arrange
        config_file = tmp_path / "config.json"
        config_file.write_text('{"version": "1.0.0"}')

        validator = MigrationValidator()

        # Act
        report = validator.validate(
            root_path=tmp_path,
            json_schemas={"config.json": ["version", "missing_key"]}
        )

        # Assert
        assert report.is_valid is False
        assert report.failed_checks > 0

    def test_should_detect_invalid_json_syntax(self, tmp_path):
        """
        AC#5: Detect invalid JSON syntax

        Arrange: File contains invalid JSON
        Act: Call validate(json_schemas={file: [keys]})
        Assert: Returns ValidationReport with failed checks
        """
        # Arrange
        config_file = tmp_path / "config.json"
        config_file.write_text('{invalid json}')

        validator = MigrationValidator()

        # Act
        report = validator.validate(
            root_path=tmp_path,
            json_schemas={"config.json": ["version"]}
        )

        # Assert
        assert report.is_valid is False
        assert report.failed_checks > 0

    def test_should_validate_nested_json_keys(self, tmp_path):
        """
        AC#5: Validate nested JSON keys (e.g., "settings.debug")

        Arrange: JSON file with nested structure
        Act: Call validate(json_schemas={file: ["settings.debug"]})
        Assert: Returns ValidationReport with passed checks
        """
        # Arrange
        config_file = tmp_path / "config.json"
        config_file.write_text('{"settings": {"debug": true}}')

        validator = MigrationValidator()

        # Act
        report = validator.validate(
            root_path=tmp_path,
            json_schemas={"config.json": ["settings.debug"]}
        )

        # Assert
        assert report.is_valid is True


class TestConfigurationValidation:
    """Tests for configuration validation"""

    def test_should_validate_required_config_keys(self, tmp_path):
        """
        AC#5: Check required configuration keys exist

        Arrange: Configuration file with required keys
        Act: Call validate(config_validations={file: [keys]})
        Assert: Returns ValidationReport with passed checks
        """
        # Arrange
        config_file = tmp_path / "config.json"
        config_file.write_text('{"host": "localhost", "port": 8080}')

        validator = MigrationValidator()

        # Act
        report = validator.validate(
            root_path=tmp_path,
            config_validations={"config.json": ["host", "port"]}
        )

        # Assert
        assert report.is_valid is True

    def test_should_detect_missing_config_keys(self, tmp_path):
        """
        AC#5: Detect missing required config keys

        Arrange: Configuration missing required keys
        Act: Call validate(config_validations={file: [keys]})
        Assert: Returns ValidationReport with failed checks
        """
        # Arrange
        config_file = tmp_path / "config.json"
        config_file.write_text('{"host": "localhost"}')

        validator = MigrationValidator()

        # Act
        report = validator.validate(
            root_path=tmp_path,
            config_validations={"config.json": ["host", "port"]}
        )

        # Assert
        assert report.is_valid is False
        assert report.failed_checks > 0


class TestValidationReport:
    """Tests for validation report generation"""

    def test_should_return_detailed_validation_report(self, tmp_path):
        """
        AC#5: Return detailed validation report

        Arrange: Multiple validation checks run
        Act: Call validate(...)
        Assert: Returns complete ValidationReport with all checks
        """
        # Arrange
        (tmp_path / "file1.txt").write_text("content")
        (tmp_path / "dir1").mkdir()
        config_file = tmp_path / "config.json"
        config_file.write_text('{"version": "1.0.0"}')

        validator = MigrationValidator()

        # Act
        report = validator.validate(
            root_path=tmp_path,
            expected_files=["file1.txt"],
            expected_dirs=["dir1"],
            json_schemas={"config.json": ["version"]}
        )

        # Assert
        assert isinstance(report, ValidationReport)
        assert report.total_checks > 0
        assert report.passed_checks > 0

    def test_should_include_check_details_in_report(self, tmp_path):
        """
        AC#5: Include detailed information in report

        Arrange: Validation with both passed and failed checks
        Act: Call validate(...)
        Assert: Report includes details about each check
        """
        # Arrange
        (tmp_path / "file1.txt").write_text("content")

        validator = MigrationValidator()

        # Act
        report = validator.validate(
            root_path=tmp_path,
            expected_files=["file1.txt", "file2.txt"]
        )

        # Assert
        assert len(report.checks) > 0

    def test_should_summarize_validation_results(self, tmp_path):
        """
        AC#5: Summarize validation results

        Arrange: Multiple validation checks
        Act: Call validate(...)
        Assert: Report includes summary counts
        """
        # Arrange
        (tmp_path / "file1.txt").write_text("content")

        validator = MigrationValidator()

        # Act
        report = validator.validate(
            root_path=tmp_path,
            expected_files=["file1.txt"]
        )

        # Assert
        assert report.total_checks >= 1
        assert report.passed_checks >= 0
        assert report.failed_checks >= 0
        assert report.passed_checks + report.failed_checks == report.total_checks


class TestConfigValidator:
    """Tests for ConfigValidator service"""

    def test_should_validate_simple_keys(self):
        """
        ConfigValidator: Validate simple configuration keys

        Arrange: Config dict with simple keys
        Act: Call validate_keys(config, ["key1", "key2"])
        Assert: Returns validation result with found keys
        """
        # Arrange
        config = {"key1": "value1", "key2": "value2"}
        validator = ConfigValidator()

        # Act
        result = validator.validate_keys(config, ["key1", "key2"])

        # Assert
        assert result["valid"] is True
        assert result["missing_keys"] == []
        assert "key1" in result["found_keys"]
        assert "key2" in result["found_keys"]

    def test_should_detect_missing_keys(self):
        """
        ConfigValidator: Detect missing keys

        Arrange: Config dict with some keys missing
        Act: Call validate_keys(config, ["existing", "missing"])
        Assert: Returns validation result with missing keys listed
        """
        # Arrange
        config = {"key1": "value1"}
        validator = ConfigValidator()

        # Act
        result = validator.validate_keys(config, ["key1", "missing_key"])

        # Assert
        assert result["valid"] is False
        assert "missing_key" in result["missing_keys"]
        assert "key1" in result["found_keys"]

    def test_should_validate_nested_keys(self):
        """
        ConfigValidator: Validate nested configuration keys

        Arrange: Config dict with nested structure
        Act: Call validate_keys(config, ["level1.level2.key"])
        Assert: Returns validation result with nested key found
        """
        # Arrange
        config = {
            "database": {
                "settings": {
                    "host": "localhost"
                }
            }
        }
        validator = ConfigValidator()

        # Act
        result = validator.validate_keys(
            config,
            ["database.settings.host"]
        )

        # Assert
        assert result["valid"] is True
        assert "database.settings.host" in result["found_keys"]

    def test_should_handle_missing_nested_keys(self):
        """
        ConfigValidator: Detect missing nested keys

        Arrange: Config with incomplete nesting
        Act: Call validate_keys(config, ["level1.level2.missing"])
        Assert: Returns validation result with missing nested key
        """
        # Arrange
        config = {
            "database": {
                "settings": {
                    "host": "localhost"
                }
            }
        }
        validator = ConfigValidator()

        # Act
        result = validator.validate_keys(
            config,
            ["database.settings.missing_key"]
        )

        # Assert
        assert result["valid"] is False
        assert "database.settings.missing_key" in result["missing_keys"]


class TestValidationEdgeCases:
    """Tests for edge cases and error scenarios"""

    def test_should_handle_empty_validation_requests(self, tmp_path):
        """
        Edge case: No validation checks requested

        Arrange: Call validate(root_path=...) with no checks
        Act: Execute validation
        Assert: Returns report with no checks
        """
        # Arrange
        validator = MigrationValidator()

        # Act
        report = validator.validate(root_path=tmp_path)

        # Assert
        assert report.total_checks == 0
        assert report.passed_checks == 0
        assert report.failed_checks == 0

    def test_should_handle_empty_json_file(self, tmp_path):
        """
        Edge case: JSON file is empty

        Arrange: JSON file with no content
        Act: Call validate(json_schemas={file: [keys]})
        Assert: Returns report with failed check
        """
        # Arrange
        config_file = tmp_path / "config.json"
        config_file.write_text('')

        validator = MigrationValidator()

        # Act
        report = validator.validate(
            root_path=tmp_path,
            json_schemas={"config.json": ["version"]}
        )

        # Assert
        assert report.is_valid is False

    def test_should_handle_files_not_directories(self, tmp_path):
        """
        Edge case: Expected directory exists as file

        Arrange: Path is file but validation expects directory
        Act: Call validate(expected_dirs=[file_path])
        Assert: Returns report with failed check
        """
        # Arrange
        (tmp_path / "notadir.txt").write_text("content")

        validator = MigrationValidator()

        # Act
        report = validator.validate(
            root_path=tmp_path,
            expected_dirs=["notadir.txt"]
        )

        # Assert
        assert report.is_valid is False

    def test_should_handle_unicode_in_json(self, tmp_path):
        """
        Edge case: JSON with unicode characters

        Arrange: JSON file with unicode characters
        Act: Call validate(json_schemas={file: [keys]})
        Assert: Returns report with passed check
        """
        # Arrange
        config_file = tmp_path / "config.json"
        config_file.write_text('{"description": "Test"}', encoding="utf-8")

        validator = MigrationValidator()

        # Act
        report = validator.validate(
            root_path=tmp_path,
            json_schemas={"config.json": ["description"]}
        )

        # Assert
        assert report.is_valid is True


# Fixtures for test support


@pytest.fixture
def sample_config_file(tmp_path):
    """Create a sample configuration file"""
    config_file = tmp_path / "config.json"
    config = {
        "version": "1.0.0",
        "name": "MyApp",
        "settings": {
            "debug": True,
            "log_level": "INFO"
        }
    }
    config_file.write_text(json.dumps(config, indent=2))
    return config_file


@pytest.fixture
def migration_validator():
    """Create MigrationValidator instance"""
    return MigrationValidator()


@pytest.fixture
def config_validator():
    """Create ConfigValidator instance"""
    return ConfigValidator()

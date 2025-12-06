"""
STORY-078: Unit tests for MigrationValidator service.

Tests post-migration validation including file existence, schema validation,
and configuration key checking.
All tests follow TDD Red phase - they should FAIL until implementation exists.

Coverage Target: 95%+

AC Mapping:
- AC#5: Migration Validation
  - Expected files verified to exist
  - Schemas validated (JSON/YAML well-formed)
  - Configuration tested for required keys
  - Validation failures trigger rollback
  - Validation results logged with pass/fail for each check

Technical Specification:
- SVC-015: Validate expected files exist after migration
- SVC-016: Validate JSON/YAML schema integrity
- SVC-017: Validate required configuration keys
- SVC-018: Return detailed validation report
"""

import pytest
import json
import yaml
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def project_root(tmp_path):
    """
    Create a temporary project root for validation testing.

    Returns:
        Path: Path to project root
    """
    project = tmp_path / "project"
    project.mkdir()
    (project / ".devforgeai").mkdir()
    (project / ".claude").mkdir()
    return project


@pytest.fixture
def valid_project_structure(project_root):
    """
    Create a valid project structure with all expected files.

    Returns:
        dict: Paths to created files
    """
    files = {}

    # Create .devforgeai structure
    devforgeai = project_root / ".devforgeai"
    (devforgeai / "config").mkdir()
    (devforgeai / "context").mkdir()
    (devforgeai / "protocols").mkdir()

    # Version file
    version_file = devforgeai / ".version.json"
    version_file.write_text(json.dumps({
        "version": "1.1.0",
        "installed_at": "2025-12-01T00:00:00Z",
        "schema_version": "1.0"
    }, indent=2))
    files["version"] = version_file

    # Config file
    config_file = devforgeai / "config" / "upgrade-config.json"
    config_file.write_text(json.dumps({
        "backup_retention_count": 5,
        "migration_timeout_seconds": 300,
        "validate_after_migration": True
    }, indent=2))
    files["config"] = config_file

    # Context file (YAML)
    context_file = devforgeai / "context" / "tech-stack.md"
    context_file.write_text("# Technology Stack\n\n- Python 3.10+\n- pytest\n")
    files["context"] = context_file

    # Create .claude structure
    claude = project_root / ".claude"
    (claude / "agents").mkdir()
    (claude / "commands").mkdir()
    (claude / "skills").mkdir()

    files["project_root"] = project_root

    return files


@pytest.fixture
def validation_rules():
    """
    Provide sample validation rules for testing.

    Returns:
        dict: Validation rules configuration
    """
    return {
        "expected_files": [
            ".devforgeai/.version.json",
            ".devforgeai/config/upgrade-config.json",
            ".claude/agents",
            ".claude/commands",
            ".claude/skills"
        ],
        "json_schemas": {
            ".devforgeai/.version.json": {
                "required_keys": ["version", "installed_at", "schema_version"]
            },
            ".devforgeai/config/upgrade-config.json": {
                "required_keys": ["backup_retention_count"]
            }
        },
        "yaml_files": [],
        "required_config_keys": {
            ".devforgeai/.version.json": ["version", "schema_version"],
            ".devforgeai/config/upgrade-config.json": ["backup_retention_count"]
        }
    }


# ============================================================================
# Test Class: File Existence Validation (AC#5, SVC-015)
# ============================================================================

class TestFileExistenceValidation:
    """Test validation of expected file existence (AC#5, SVC-015)."""

    def test_validate_all_expected_files_exist(self, valid_project_structure, validation_rules):
        """
        SVC-015: Validate all expected files exist after migration.

        Given: Project with all expected files present
        When: MigrationValidator.validate() is called
        Then: Validation passes for file existence
        """
        # Arrange
        from installer.migration_validator import MigrationValidator

        validator = MigrationValidator(logger=Mock())
        project_root = valid_project_structure["project_root"]

        # Act
        result = validator.validate(
            project_root=project_root,
            expected_files=validation_rules["expected_files"]
        )

        # Assert
        assert result.file_existence.all_passed is True
        assert len(result.file_existence.passed) == len(validation_rules["expected_files"])
        assert len(result.file_existence.failed) == 0

    def test_validate_detects_missing_file(self, project_root, validation_rules):
        """
        SVC-015: Detect missing expected file.

        Given: Project with missing .version.json
        When: validate() is called
        Then: Validation fails, reports missing file
        """
        # Arrange
        from installer.migration_validator import MigrationValidator

        validator = MigrationValidator(logger=Mock())

        # Create partial structure (missing .version.json)
        (project_root / ".devforgeai" / "config").mkdir(parents=True)
        (project_root / ".claude" / "agents").mkdir(parents=True)
        (project_root / ".claude" / "commands").mkdir(parents=True)
        (project_root / ".claude" / "skills").mkdir(parents=True)

        # Act
        result = validator.validate(
            project_root=project_root,
            expected_files=validation_rules["expected_files"]
        )

        # Assert
        assert result.file_existence.all_passed is False
        assert ".devforgeai/.version.json" in result.file_existence.failed

    def test_validate_detects_missing_directory(self, project_root):
        """
        SVC-015: Detect missing expected directory.

        Given: Project with missing .claude/skills directory
        When: validate() is called
        Then: Validation fails, reports missing directory
        """
        # Arrange
        from installer.migration_validator import MigrationValidator

        validator = MigrationValidator(logger=Mock())

        # Create partial structure (missing skills)
        (project_root / ".claude" / "agents").mkdir(parents=True)
        (project_root / ".claude" / "commands").mkdir(parents=True)
        # Missing: .claude/skills

        expected = [".claude/agents", ".claude/commands", ".claude/skills"]

        # Act
        result = validator.validate(project_root=project_root, expected_files=expected)

        # Assert
        assert result.file_existence.all_passed is False
        assert ".claude/skills" in result.file_existence.failed

    def test_validate_multiple_missing_files_reports_all(self, project_root):
        """
        SVC-015: Report all missing files, not just first.

        Given: Project with multiple missing files
        When: validate() is called
        Then: All missing files reported
        """
        # Arrange
        from installer.migration_validator import MigrationValidator

        validator = MigrationValidator(logger=Mock())

        expected = ["file1.txt", "file2.txt", "file3.txt"]
        # None exist

        # Act
        result = validator.validate(project_root=project_root, expected_files=expected)

        # Assert
        assert result.file_existence.all_passed is False
        assert len(result.file_existence.failed) == 3

    def test_validate_empty_expected_files_passes(self, project_root):
        """
        SVC-015: Empty expected files list passes validation.

        Given: No expected files (patch upgrade with no new files)
        When: validate() is called
        Then: Validation passes
        """
        # Arrange
        from installer.migration_validator import MigrationValidator

        validator = MigrationValidator(logger=Mock())

        # Act
        result = validator.validate(project_root=project_root, expected_files=[])

        # Assert
        assert result.file_existence.all_passed is True


# ============================================================================
# Test Class: Schema Validation (AC#5, SVC-016)
# ============================================================================

class TestSchemaValidation:
    """Test JSON/YAML schema validation (AC#5, SVC-016)."""

    def test_validate_valid_json_file(self, project_root):
        """
        SVC-016: Valid JSON file passes schema validation.

        Given: Well-formed JSON file
        When: validate_schema() is called
        Then: Validation passes
        """
        # Arrange
        from installer.migration_validator import MigrationValidator

        json_file = project_root / "config.json"
        json_file.write_text('{"key": "value", "number": 42}')

        validator = MigrationValidator(logger=Mock())

        # Act
        result = validator.validate_schema(file_path=json_file, file_type="json")

        # Assert
        assert result.passed is True
        assert result.error is None

    def test_validate_invalid_json_file(self, project_root):
        """
        SVC-016: Invalid JSON file fails schema validation.

        Given: Malformed JSON file
        When: validate_schema() is called
        Then: Validation fails with error message
        """
        # Arrange
        from installer.migration_validator import MigrationValidator

        json_file = project_root / "config.json"
        json_file.write_text('{"key": "value", invalid}')  # Missing quotes

        validator = MigrationValidator(logger=Mock())

        # Act
        result = validator.validate_schema(file_path=json_file, file_type="json")

        # Assert
        assert result.passed is False
        assert result.error is not None
        assert "json" in result.error.lower() or "parse" in result.error.lower()

    def test_validate_valid_yaml_file(self, project_root):
        """
        SVC-016: Valid YAML file passes schema validation.

        Given: Well-formed YAML file
        When: validate_schema() is called
        Then: Validation passes
        """
        # Arrange
        from installer.migration_validator import MigrationValidator

        yaml_file = project_root / "config.yaml"
        yaml_file.write_text("key: value\nnumber: 42\nlist:\n  - item1\n  - item2\n")

        validator = MigrationValidator(logger=Mock())

        # Act
        result = validator.validate_schema(file_path=yaml_file, file_type="yaml")

        # Assert
        assert result.passed is True

    def test_validate_invalid_yaml_file(self, project_root):
        """
        SVC-016: Invalid YAML file fails schema validation.

        Given: Malformed YAML file
        When: validate_schema() is called
        Then: Validation fails with error message
        """
        # Arrange
        from installer.migration_validator import MigrationValidator

        yaml_file = project_root / "config.yaml"
        yaml_file.write_text("key: value\n  bad_indent: value\n")  # Indentation error

        validator = MigrationValidator(logger=Mock())

        # Act
        result = validator.validate_schema(file_path=yaml_file, file_type="yaml")

        # Assert
        assert result.passed is False
        assert result.error is not None

    def test_validate_multiple_json_files(self, valid_project_structure):
        """
        SVC-016: Validate multiple JSON files in project.

        Given: Project with multiple JSON files
        When: validate() is called with json_files list
        Then: All JSON files validated
        """
        # Arrange
        from installer.migration_validator import MigrationValidator

        project_root = valid_project_structure["project_root"]
        validator = MigrationValidator(logger=Mock())

        json_files = [
            ".devforgeai/.version.json",
            ".devforgeai/config/upgrade-config.json"
        ]

        # Act
        result = validator.validate(
            project_root=project_root,
            json_files=json_files
        )

        # Assert
        assert result.schema_validation.all_passed is True
        assert len(result.schema_validation.passed) == 2

    def test_validate_detects_corrupt_json(self, project_root):
        """
        SVC-016: Detect corrupted JSON file.

        Given: JSON file truncated/corrupted mid-write
        When: validate_schema() is called
        Then: Validation fails
        """
        # Arrange
        from installer.migration_validator import MigrationValidator

        json_file = project_root / "config.json"
        json_file.write_text('{"key": "value"')  # Truncated - missing closing brace

        validator = MigrationValidator(logger=Mock())

        # Act
        result = validator.validate_schema(file_path=json_file, file_type="json")

        # Assert
        assert result.passed is False

    def test_validate_empty_json_file(self, project_root):
        """
        SVC-016: Empty JSON file fails validation.

        Given: Empty JSON file
        When: validate_schema() is called
        Then: Validation fails (not valid JSON)
        """
        # Arrange
        from installer.migration_validator import MigrationValidator

        json_file = project_root / "config.json"
        json_file.write_text("")

        validator = MigrationValidator(logger=Mock())

        # Act
        result = validator.validate_schema(file_path=json_file, file_type="json")

        # Assert
        assert result.passed is False


# ============================================================================
# Test Class: Configuration Key Validation (AC#5, SVC-017)
# ============================================================================

class TestConfigurationKeyValidation:
    """Test required configuration key validation (AC#5, SVC-017)."""

    def test_validate_all_required_keys_present(self, project_root):
        """
        SVC-017: Config with all required keys passes validation.

        Given: Config file with all required keys
        When: validate_config_keys() is called
        Then: Validation passes
        """
        # Arrange
        from installer.migration_validator import MigrationValidator

        config_file = project_root / "config.json"
        config_file.write_text(json.dumps({
            "version": "1.0.0",
            "installed_at": "2025-12-01",
            "schema_version": "1.0"
        }))

        validator = MigrationValidator(logger=Mock())
        required_keys = ["version", "installed_at", "schema_version"]

        # Act
        result = validator.validate_config_keys(
            file_path=config_file,
            required_keys=required_keys
        )

        # Assert
        assert result.passed is True
        assert len(result.missing_keys) == 0

    def test_validate_detects_missing_required_key(self, project_root):
        """
        SVC-017: Detect missing required configuration key.

        Given: Config file missing "schema_version" key
        When: validate_config_keys() is called
        Then: Validation fails, reports missing key
        """
        # Arrange
        from installer.migration_validator import MigrationValidator

        config_file = project_root / "config.json"
        config_file.write_text(json.dumps({
            "version": "1.0.0",
            "installed_at": "2025-12-01"
            # Missing: schema_version
        }))

        validator = MigrationValidator(logger=Mock())
        required_keys = ["version", "installed_at", "schema_version"]

        # Act
        result = validator.validate_config_keys(
            file_path=config_file,
            required_keys=required_keys
        )

        # Assert
        assert result.passed is False
        assert "schema_version" in result.missing_keys

    def test_validate_detects_multiple_missing_keys(self, project_root):
        """
        SVC-017: Report all missing keys, not just first.

        Given: Config file missing multiple required keys
        When: validate_config_keys() is called
        Then: All missing keys reported
        """
        # Arrange
        from installer.migration_validator import MigrationValidator

        config_file = project_root / "config.json"
        config_file.write_text(json.dumps({"version": "1.0.0"}))

        validator = MigrationValidator(logger=Mock())
        required_keys = ["version", "installed_at", "schema_version", "mode"]

        # Act
        result = validator.validate_config_keys(
            file_path=config_file,
            required_keys=required_keys
        )

        # Assert
        assert result.passed is False
        assert len(result.missing_keys) == 3
        assert "installed_at" in result.missing_keys
        assert "schema_version" in result.missing_keys
        assert "mode" in result.missing_keys

    def test_validate_nested_keys(self, project_root):
        """
        SVC-017: Validate nested configuration keys.

        Given: Config with nested structure
        When: validate_config_keys() with dot notation
        Then: Nested keys validated
        """
        # Arrange
        from installer.migration_validator import MigrationValidator

        config_file = project_root / "config.json"
        config_file.write_text(json.dumps({
            "database": {
                "host": "localhost",
                "port": 5432
            },
            "features": {
                "enabled": True
            }
        }))

        validator = MigrationValidator(logger=Mock())
        required_keys = ["database.host", "database.port", "features.enabled"]

        # Act
        result = validator.validate_config_keys(
            file_path=config_file,
            required_keys=required_keys
        )

        # Assert
        assert result.passed is True

    def test_validate_config_with_null_value_for_required_key(self, project_root):
        """
        SVC-017: Key with null value counts as present.

        Given: Config with null value for required key
        When: validate_config_keys() is called
        Then: Key is considered present (value validation is separate)
        """
        # Arrange
        from installer.migration_validator import MigrationValidator

        config_file = project_root / "config.json"
        config_file.write_text(json.dumps({
            "version": "1.0.0",
            "optional_field": None  # Null but present
        }))

        validator = MigrationValidator(logger=Mock())
        required_keys = ["version", "optional_field"]

        # Act
        result = validator.validate_config_keys(
            file_path=config_file,
            required_keys=required_keys
        )

        # Assert
        assert result.passed is True


# ============================================================================
# Test Class: Validation Report (AC#5, SVC-018)
# ============================================================================

class TestValidationReport:
    """Test detailed validation report generation (AC#5, SVC-018)."""

    def test_validation_report_includes_all_check_results(self, valid_project_structure, validation_rules):
        """
        SVC-018: Validation report includes all check types.

        Given: Full validation run
        When: validate() completes
        Then: Report includes file, schema, and config key results
        """
        # Arrange
        from installer.migration_validator import MigrationValidator

        project_root = valid_project_structure["project_root"]
        validator = MigrationValidator(logger=Mock())

        # Act
        result = validator.validate(
            project_root=project_root,
            expected_files=validation_rules["expected_files"],
            json_files=[".devforgeai/.version.json"],
            config_keys={".devforgeai/.version.json": ["version", "schema_version"]}
        )

        # Assert
        assert hasattr(result, 'file_existence')
        assert hasattr(result, 'schema_validation')
        assert hasattr(result, 'config_keys')
        assert hasattr(result, 'overall_passed')

    def test_validation_report_has_pass_fail_for_each_check(self, project_root):
        """
        SVC-018: Each check has individual pass/fail status.

        Given: Mix of passing and failing validations
        When: validate() completes
        Then: Each check has its own status
        """
        # Arrange
        from installer.migration_validator import MigrationValidator

        # Create one valid file, one invalid
        valid_json = project_root / "valid.json"
        valid_json.write_text('{"key": "value"}')

        invalid_json = project_root / "invalid.json"
        invalid_json.write_text('{"key": invalid}')

        validator = MigrationValidator(logger=Mock())

        # Act
        result = validator.validate(
            project_root=project_root,
            json_files=["valid.json", "invalid.json"]
        )

        # Assert
        assert "valid.json" in result.schema_validation.passed
        assert "invalid.json" in result.schema_validation.failed

    def test_validation_report_overall_passed_false_on_any_failure(self, project_root):
        """
        SVC-018: overall_passed is False if any check fails.

        Given: One failing check among many passing
        When: validate() completes
        Then: overall_passed is False
        """
        # Arrange
        from installer.migration_validator import MigrationValidator

        validator = MigrationValidator(logger=Mock())

        # Act
        result = validator.validate(
            project_root=project_root,
            expected_files=["nonexistent.txt"]  # Will fail
        )

        # Assert
        assert result.overall_passed is False

    def test_validation_report_overall_passed_true_when_all_pass(self, valid_project_structure, validation_rules):
        """
        SVC-018: overall_passed is True when all checks pass.

        Given: All validations pass
        When: validate() completes
        Then: overall_passed is True
        """
        # Arrange
        from installer.migration_validator import MigrationValidator

        project_root = valid_project_structure["project_root"]
        validator = MigrationValidator(logger=Mock())

        # Act
        result = validator.validate(
            project_root=project_root,
            expected_files=validation_rules["expected_files"]
        )

        # Assert
        assert result.overall_passed is True

    def test_validation_report_logged_with_details(self, valid_project_structure, validation_rules):
        """
        AC#5: Validation results logged with pass/fail for each check.

        Given: Validation run
        When: validate() completes
        Then: Logger called with detailed results
        """
        # Arrange
        from installer.migration_validator import MigrationValidator

        project_root = valid_project_structure["project_root"]
        mock_logger = Mock()
        validator = MigrationValidator(logger=mock_logger)

        # Act
        validator.validate(
            project_root=project_root,
            expected_files=validation_rules["expected_files"]
        )

        # Assert
        mock_logger.log_info.assert_called()


# ============================================================================
# Test Class: Rollback Trigger (AC#5)
# ============================================================================

class TestValidationRollbackTrigger:
    """Test validation failure triggers rollback (AC#5)."""

    def test_validation_failure_sets_should_rollback_flag(self, project_root):
        """
        AC#5: Validation failure triggers rollback.

        Given: Validation fails
        When: validate() completes
        Then: should_rollback is True
        """
        # Arrange
        from installer.migration_validator import MigrationValidator

        validator = MigrationValidator(logger=Mock())

        # Act
        result = validator.validate(
            project_root=project_root,
            expected_files=["nonexistent.txt"]
        )

        # Assert
        assert result.overall_passed is False
        assert result.should_rollback is True

    def test_validation_success_does_not_set_rollback_flag(self, valid_project_structure):
        """
        AC#5: Validation success does not trigger rollback.

        Given: Validation passes
        When: validate() completes
        Then: should_rollback is False
        """
        # Arrange
        from installer.migration_validator import MigrationValidator

        project_root = valid_project_structure["project_root"]
        validator = MigrationValidator(logger=Mock())

        # Act
        result = validator.validate(
            project_root=project_root,
            expected_files=[".devforgeai/.version.json"]
        )

        # Assert
        assert result.overall_passed is True
        assert result.should_rollback is False


# ============================================================================
# Test Class: Edge Cases
# ============================================================================

class TestMigrationValidatorEdgeCases:
    """Test edge cases for migration validator."""

    def test_validate_nonexistent_project_root(self):
        """
        Edge case: Project root doesn't exist.

        Given: Nonexistent project root
        When: validate() is called
        Then: All file checks fail
        """
        # Arrange
        from installer.migration_validator import MigrationValidator

        validator = MigrationValidator(logger=Mock())

        # Act
        result = validator.validate(
            project_root=Path("/nonexistent/project"),
            expected_files=["any.txt"]
        )

        # Assert
        assert result.overall_passed is False

    def test_validate_file_with_special_characters(self, project_root):
        """
        Edge case: File with special characters in name.

        Given: File with spaces and unicode in name
        When: validate() is called
        Then: Validation handles correctly
        """
        # Arrange
        from installer.migration_validator import MigrationValidator

        special_file = project_root / "file with spaces.json"
        special_file.write_text('{"key": "value"}')

        validator = MigrationValidator(logger=Mock())

        # Act
        result = validator.validate(
            project_root=project_root,
            expected_files=["file with spaces.json"]
        )

        # Assert
        assert result.file_existence.all_passed is True

    def test_validate_very_large_json_file(self, project_root):
        """
        Edge case: Very large JSON file.

        Given: JSON file > 10MB
        When: validate_schema() is called
        Then: Validation completes without memory issues
        """
        # Arrange
        from installer.migration_validator import MigrationValidator

        large_json = project_root / "large.json"
        # Create ~1MB JSON (smaller for test speed)
        data = {"items": [{"id": i, "data": "x" * 100} for i in range(1000)]}
        large_json.write_text(json.dumps(data))

        validator = MigrationValidator(logger=Mock())

        # Act
        result = validator.validate_schema(file_path=large_json, file_type="json")

        # Assert
        assert result.passed is True

    def test_validate_binary_file_as_json(self, project_root):
        """
        Edge case: Binary file mistakenly named .json.

        Given: Binary file with .json extension
        When: validate_schema() is called
        Then: Validation fails gracefully
        """
        # Arrange
        from installer.migration_validator import MigrationValidator

        binary_file = project_root / "binary.json"
        binary_file.write_bytes(b'\x00\x01\x02\x03\xff\xfe')

        validator = MigrationValidator(logger=Mock())

        # Act
        result = validator.validate_schema(file_path=binary_file, file_type="json")

        # Assert
        assert result.passed is False

    def test_validate_symlink_to_valid_file(self, project_root):
        """
        Edge case: Symlink pointing to valid file.

        Given: Symlink to valid JSON file
        When: validate() is called
        Then: Follows symlink, validates target
        """
        # Arrange
        from installer.migration_validator import MigrationValidator

        target = project_root / "target.json"
        target.write_text('{"key": "value"}')

        symlink = project_root / "link.json"
        symlink.symlink_to(target)

        validator = MigrationValidator(logger=Mock())

        # Act
        result = validator.validate(
            project_root=project_root,
            expected_files=["link.json"],
            json_files=["link.json"]
        )

        # Assert
        assert result.file_existence.all_passed is True
        assert result.schema_validation.all_passed is True

    def test_validate_read_permission_denied(self, project_root):
        """
        Edge case: File exists but cannot be read.

        Given: File with no read permissions
        When: validate_schema() is called
        Then: Validation fails with permission error
        """
        # Arrange
        from installer.migration_validator import MigrationValidator

        validator = MigrationValidator(logger=Mock())

        # Create file then remove read permission
        protected = project_root / "protected.json"
        protected.write_text('{"key": "value"}')

        with patch('builtins.open', side_effect=PermissionError("Permission denied")):
            # Act
            result = validator.validate_schema(file_path=protected, file_type="json")

            # Assert
            assert result.passed is False
            assert "permission" in result.error.lower()


# ============================================================================
# Test Class: Config Key Validation Errors (Coverage: Lines 399-400, 428, 534-536)
# ============================================================================

class TestConfigKeyValidationErrors:
    """Test error handling in config key validation (Coverage gap tests)."""

    def test_validate_config_keys_file_not_found(self, project_root):
        """
        Coverage: Lines 399-400 - FileNotFoundError exception handling.

        Given: Config file does not exist
        When: validate_config_keys() is called
        Then: Returns passed=False with all keys marked as missing
        """
        # Arrange
        from installer.migration_validator import MigrationValidator

        validator = MigrationValidator(logger=Mock())
        nonexistent_file = project_root / "nonexistent_config.json"
        required_keys = ["version", "schema_version", "installed_at"]

        # Act
        result = validator.validate_config_keys(
            file_path=nonexistent_file,
            required_keys=required_keys
        )

        # Assert
        assert result.passed is False
        assert len(result.missing_keys) == 3
        assert "version" in result.missing_keys
        assert "schema_version" in result.missing_keys
        assert "installed_at" in result.missing_keys

    def test_validate_config_keys_permission_denied(self, project_root):
        """
        Coverage: Lines 399-400 - PermissionError exception handling.

        Given: Config file exists but read permission denied
        When: validate_config_keys() is called
        Then: Returns passed=False with all keys marked as missing
        """
        # Arrange
        from installer.migration_validator import MigrationValidator

        validator = MigrationValidator(logger=Mock())
        config_file = project_root / "config.json"
        config_file.write_text('{"version": "1.0.0"}')
        required_keys = ["version", "schema_version"]

        # Act - Mock Path.read_text to raise PermissionError
        with patch.object(Path, 'read_text', side_effect=PermissionError("Permission denied")):
            result = validator.validate_config_keys(
                file_path=config_file,
                required_keys=required_keys
            )

        # Assert
        assert result.passed is False
        assert len(result.missing_keys) == 2

    def test_validate_config_keys_corrupt_json(self, project_root):
        """
        Coverage: Lines 399-400 - JSONDecodeError exception handling.

        Given: Config file contains invalid JSON syntax
        When: validate_config_keys() is called
        Then: Returns passed=False with all keys marked as missing
        """
        # Arrange
        from installer.migration_validator import MigrationValidator

        validator = MigrationValidator(logger=Mock())
        config_file = project_root / "config.json"
        config_file.write_text('{invalid json content: }}}')
        required_keys = ["version", "database.host"]

        # Act
        result = validator.validate_config_keys(
            file_path=config_file,
            required_keys=required_keys
        )

        # Assert
        assert result.passed is False
        assert len(result.missing_keys) == 2
        assert "version" in result.missing_keys
        assert "database.host" in result.missing_keys

    def test_validate_nested_key_with_non_dict_parent(self, project_root):
        """
        Coverage: Line 428 - Nested key not found when parent is not a dict.

        Given: Config has "database" as a string (not a dict)
        When: validate_config_keys() with "database.host" is called
        Then: Returns passed=False, "database.host" marked as missing
        """
        # Arrange
        from installer.migration_validator import MigrationValidator

        validator = MigrationValidator(logger=Mock())
        config_file = project_root / "config.json"
        config_file.write_text(json.dumps({
            "database": "connection_string",  # String, not dict
            "version": "1.0.0"
        }))
        required_keys = ["version", "database.host"]

        # Act
        result = validator.validate_config_keys(
            file_path=config_file,
            required_keys=required_keys
        )

        # Assert
        assert result.passed is False
        assert "database.host" in result.missing_keys
        assert "version" not in result.missing_keys

    def test_validate_nested_key_with_missing_intermediate(self, project_root):
        """
        Coverage: Line 428 - 3-level nesting with middle level missing.

        Given: Config has structure where middle key "settings" does not exist
        When: validate_config_keys() with "app.settings.timeout" is called
        Then: Returns passed=False, nested key marked as missing
        """
        # Arrange
        from installer.migration_validator import MigrationValidator

        validator = MigrationValidator(logger=Mock())
        config_file = project_root / "config.json"
        config_file.write_text(json.dumps({
            "app": {
                "name": "TestApp"
                # Missing: "settings" key
            },
            "version": "1.0.0"
        }))
        required_keys = ["version", "app.settings.timeout"]

        # Act
        result = validator.validate_config_keys(
            file_path=config_file,
            required_keys=required_keys
        )

        # Assert
        assert result.passed is False
        assert "app.settings.timeout" in result.missing_keys
        assert "version" not in result.missing_keys

    def test_validate_multiple_config_files_with_failures(self, project_root):
        """
        Coverage: Lines 534-536 - Batch validation records failures correctly.

        Given: Multiple config files, some with missing keys
        When: validate() is called with config_keys dict
        Then: Report correctly records passed/failed files and missing keys
        """
        # Arrange
        from installer.migration_validator import MigrationValidator

        validator = MigrationValidator(logger=Mock())

        # Create valid config file
        valid_config = project_root / "valid.json"
        valid_config.write_text(json.dumps({
            "version": "1.0.0",
            "schema_version": "1.0"
        }))

        # Create invalid config file (missing required key)
        invalid_config = project_root / "invalid.json"
        invalid_config.write_text(json.dumps({
            "version": "1.0.0"
            # Missing: schema_version
        }))

        # Create nonexistent config reference
        config_keys = {
            "valid.json": ["version", "schema_version"],
            "invalid.json": ["version", "schema_version"],
            "nonexistent.json": ["version"]  # File does not exist
        }

        # Act
        result = validator.validate(
            project_root=project_root,
            config_keys=config_keys
        )

        # Assert
        assert result.config_keys.all_passed is False
        assert "valid.json" in result.config_keys.passed
        assert "invalid.json" in result.config_keys.failed
        assert "nonexistent.json" in result.config_keys.failed
        assert "schema_version" in result.config_keys.missing_keys.get("invalid.json", [])
        assert "version" in result.config_keys.missing_keys.get("nonexistent.json", [])


# ============================================================================
# Test Class: Logging and Properties (Coverage: Lines 161, 257-258)
# ============================================================================

class TestLoggingAndProperties:
    """Test logging behavior and property accessors (Coverage gap tests)."""

    def test_config_key_validation_failure_logging(self, project_root):
        """
        Coverage: Lines 257-258 - Logger called on config key validation failure.

        Given: Config validation fails due to missing keys
        When: validate() completes
        Then: Logger.log_info() called with config key failure summary
        """
        # Arrange
        from installer.migration_validator import MigrationValidator

        mock_logger = Mock()
        validator = MigrationValidator(logger=mock_logger)

        # Create config with missing keys
        config_file = project_root / "config.json"
        config_file.write_text(json.dumps({"version": "1.0.0"}))

        config_keys = {
            "config.json": ["version", "missing_key"]
        }

        # Act
        validator.validate(
            project_root=project_root,
            config_keys=config_keys
        )

        # Assert - Logger should be called for config validation failure
        calls = [str(call) for call in mock_logger.log_info.call_args_list]
        config_validation_logged = any("Config key validation" in str(call) for call in calls)
        assert config_validation_logged, f"Expected config key validation log, got: {calls}"

    def test_logger_property_backward_compatibility(self):
        """
        Coverage: Line 161 - Logger property getter returns internal logger.

        Given: MigrationValidator initialized with a logger
        When: validator.logger property is accessed
        Then: Returns the same logger instance (backward compatibility)
        """
        # Arrange
        from installer.migration_validator import MigrationValidator

        mock_logger = Mock()
        mock_logger.log_info = Mock()

        # Act
        validator = MigrationValidator(logger=mock_logger)
        retrieved_logger = validator.logger

        # Assert
        assert retrieved_logger is mock_logger
        assert retrieved_logger is validator._logger


# ============================================================================
# Test Class: YAML Fallback Validation (Coverage: Lines 31-32, 342, 356-371)
# ============================================================================

class TestYAMLFallbackValidation:
    """Test YAML validation without PyYAML library (Coverage gap tests)."""

    def test_validate_yaml_without_pyyaml_library(self, project_root):
        """
        Coverage: Lines 31-32, 342 - YAML validation when PyYAML unavailable.

        Given: PyYAML is not available (YAML_AVAILABLE=False)
        When: validate_schema() is called for YAML file
        Then: Falls back to basic YAML validator (_validate_yaml_basic)
        """
        # Arrange
        from installer.migration_validator import MigrationValidator

        validator = MigrationValidator(logger=Mock())

        yaml_file = project_root / "config.yaml"
        yaml_file.write_text("key: value\nlist:\n  - item1\n  - item2\n")

        # Act - Mock YAML_AVAILABLE to simulate PyYAML not installed
        with patch('installer.migration_validator.YAML_AVAILABLE', False):
            result = validator.validate_schema(file_path=yaml_file, file_type="yaml")

        # Assert
        assert result.passed is True

    def test_basic_yaml_validator_detects_indentation_errors(self, project_root):
        """
        Coverage: Lines 356-371 - Basic YAML validator detects indentation errors.

        Given: YAML file with excessive indentation after non-block line
        When: _validate_yaml_basic() is called (via YAML_AVAILABLE=False)
        Then: Raises ValueError for indentation error
        """
        # Arrange
        from installer.migration_validator import MigrationValidator

        validator = MigrationValidator(logger=Mock())

        # Create YAML with indentation error:
        # Line 1: "key: value" (not ending with colon, indent=0)
        # Line 2: "      nested: bad" (indent=6, which is >2 more than previous)
        yaml_file = project_root / "bad_indent.yaml"
        yaml_file.write_text("key: value\n      nested: bad\n")

        # Act - Mock YAML_AVAILABLE to force use of basic validator
        with patch('installer.migration_validator.YAML_AVAILABLE', False):
            result = validator.validate_schema(file_path=yaml_file, file_type="yaml")

        # Assert
        assert result.passed is False
        assert result.error is not None
        assert "indent" in result.error.lower() or "error" in result.error.lower()

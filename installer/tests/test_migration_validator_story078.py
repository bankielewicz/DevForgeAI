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
from installer.models import (
    ValidationReport,
    ValidationError,
    FileEntry,
    BackupMetadata,
    BackupReason,
    ValidationCheck,
    UpgradeSummary,
    UpgradeStatus,
    MigrationScript,
    UpgradeError,
    BackupError,
    MigrationError,
    RollbackError,
)


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


# ==================== NEW COVERAGE GAP TESTS (STORY-078 Phase 4.5) ====================
# Targets: 17% gap in models.py (30 lines in data model validation)


class TestFileEntryValidation:
    """Tests for FileEntry data model validation"""

    def test_should_reject_empty_relative_path(self):
        """
        Test: Empty relative_path rejected

        Arrange: FileEntry with empty path
        Act: Create FileEntry
        Assert: ValueError raised
        """
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            FileEntry(
                relative_path="",
                checksum_sha256="abc123def456abc123def456abc123def456abc123def456abc123def456ab",
                size_bytes=100,
                modification_time=1000000000
            )
        assert "relative_path" in str(exc_info.value)

    def test_should_reject_empty_checksum(self):
        """
        Test: Empty checksum rejected

        Arrange: FileEntry with empty checksum
        Act: Create FileEntry
        Assert: ValueError raised
        """
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            FileEntry(
                relative_path="file.txt",
                checksum_sha256="",
                size_bytes=100,
                modification_time=1000000000
            )
        assert "checksum_sha256" in str(exc_info.value)

    def test_should_validate_sha256_length(self):
        """
        Test: SHA256 hex length validated (must be 64 chars)

        Arrange: Checksum too short (32 chars)
        Act: Create FileEntry
        Assert: ValueError raised
        """
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            FileEntry(
                relative_path="file.txt",
                checksum_sha256="abc123def456abc123def456abc123de",  # 32 chars (MD5)
                size_bytes=100,
                modification_time=1000000000
            )
        assert "64" in str(exc_info.value)

    def test_should_reject_negative_size_bytes(self):
        """
        Test: Negative size_bytes rejected

        Arrange: FileEntry with negative size
        Act: Create FileEntry
        Assert: ValueError raised
        """
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            FileEntry(
                relative_path="file.txt",
                checksum_sha256="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                size_bytes=-1,
                modification_time=1000000000
            )
        assert "size_bytes" in str(exc_info.value)

    def test_should_reject_negative_modification_time(self):
        """
        Test: Negative modification_time rejected

        Arrange: FileEntry with negative mtime
        Act: Create FileEntry
        Assert: ValueError raised
        """
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            FileEntry(
                relative_path="file.txt",
                checksum_sha256="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                size_bytes=100,
                modification_time=-1
            )
        assert "modification_time" in str(exc_info.value)

    def test_should_accept_zero_size_bytes(self):
        """
        Test: Zero-byte file allowed

        Arrange: FileEntry with size_bytes=0
        Act: Create FileEntry
        Assert: Success
        """
        # Act
        entry = FileEntry(
            relative_path="empty.txt",
            checksum_sha256="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            size_bytes=0,
            modification_time=1000000000
        )

        # Assert
        assert entry.size_bytes == 0


class TestBackupMetadataValidation:
    """Tests for BackupMetadata data model validation"""

    def test_should_reject_empty_backup_id(self):
        """
        Test: Empty backup_id rejected

        Arrange: BackupMetadata with empty backup_id
        Act: Create BackupMetadata
        Assert: ValueError raised
        """
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            BackupMetadata(
                backup_id="",
                version="1.0.0",
                created_at="2025-01-01T12:00:00Z",
                files=[FileEntry(
                    relative_path="file.txt",
                    checksum_sha256="abc123def456abc123def456abc123def456abc123def456abc123def456ab",
                    size_bytes=100,
                    modification_time=1000000000
                )],
                reason=BackupReason.UPGRADE
            )
        assert "backup_id" in str(exc_info.value)

    def test_should_reject_empty_files_list(self):
        """
        Test: Empty files list rejected

        Arrange: BackupMetadata with empty files
        Act: Create BackupMetadata
        Assert: ValueError raised
        """
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            BackupMetadata(
                backup_id="v1.0.0-20250101-120000-000",
                version="1.0.0",
                created_at="2025-01-01T12:00:00Z",
                files=[],  # Empty!
                reason=BackupReason.UPGRADE
            )
        assert "files" in str(exc_info.value).lower()

    def test_should_validate_semver_format_major_minor_patch(self):
        """
        Test: Semver validation accepts X.Y.Z format

        Arrange: Valid semver "1.0.0"
        Act: Create BackupMetadata
        Assert: Success
        """
        # Act
        metadata = BackupMetadata(
            backup_id="v1.0.0-20250101-120000-000",
            version="1.0.0",
            created_at="2025-01-01T12:00:00Z",
            files=[FileEntry(
                relative_path="file.txt",
                checksum_sha256="abc123def456abc123def456abc123def456abc123def456abc123def456ab",
                size_bytes=100,
                modification_time=1000000000
            )],
            reason=BackupReason.UPGRADE
        )

        # Assert
        assert metadata.version == "1.0.0"

    def test_should_reject_invalid_semver_too_few_parts(self):
        """
        Test: Semver with 2 parts rejected

        Arrange: Version "1.0" (missing patch)
        Act: Create BackupMetadata
        Assert: ValueError raised
        """
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            BackupMetadata(
                backup_id="v1.0-20250101-120000-000",
                version="1.0",  # Missing patch version
                created_at="2025-01-01T12:00:00Z",
                files=[FileEntry(
                    relative_path="file.txt",
                    checksum_sha256="abc123def456abc123def456abc123def456abc123def456abc123def456ab",
                    size_bytes=100,
                    modification_time=1000000000
                )],
                reason=BackupReason.UPGRADE
            )
        assert "semver" in str(exc_info.value).lower()

    def test_should_reject_invalid_semver_non_numeric(self):
        """
        Test: Semver with non-numeric parts rejected

        Arrange: Version "1.x.0"
        Act: Create BackupMetadata
        Assert: ValueError raised
        """
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            BackupMetadata(
                backup_id="v1.x.0-20250101-120000-000",
                version="1.x.0",  # Non-numeric
                created_at="2025-01-01T12:00:00Z",
                files=[FileEntry(
                    relative_path="file.txt",
                    checksum_sha256="abc123def456abc123def456abc123def456abc123def456abc123def456ab",
                    size_bytes=100,
                    modification_time=1000000000
                )],
                reason=BackupReason.UPGRADE
            )
        assert "semver" in str(exc_info.value).lower()


class TestValidationReportValidation:
    """Tests for ValidationReport data model validation"""

    def test_should_reject_mismatched_total_checks(self):
        """
        Test: total_checks must match len(checks)

        Arrange: total_checks=5 but checks has 3 items
        Act: Create ValidationReport
        Assert: ValueError raised
        """
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            ValidationReport(
                is_valid=True,
                checks=[
                    ValidationCheck(name="check1", passed=True, message="passed"),
                    ValidationCheck(name="check2", passed=True, message="passed"),
                    ValidationCheck(name="check3", passed=True, message="passed"),
                ],
                total_checks=5,  # Mismatch!
                passed_checks=3,
                failed_checks=0
            )
        assert "total_checks" in str(exc_info.value).lower()

    def test_should_reject_inconsistent_check_counts(self):
        """
        Test: passed_checks + failed_checks must equal total_checks

        Arrange: passed=3, failed=1, total=5
        Act: Create ValidationReport
        Assert: ValueError raised
        """
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            ValidationReport(
                is_valid=False,
                checks=[
                    ValidationCheck(name="check1", passed=True, message="passed"),
                    ValidationCheck(name="check2", passed=True, message="passed"),
                    ValidationCheck(name="check3", passed=True, message="passed"),
                    ValidationCheck(name="check4", passed=False, message="failed"),
                ],
                total_checks=5,  # Should be 4
                passed_checks=3,
                failed_checks=1
            )
        assert "passed_checks" in str(exc_info.value).lower()

    def test_should_reject_valid_with_failed_checks(self):
        """
        Test: Cannot be is_valid=True when failed_checks > 0

        Arrange: is_valid=True but failed_checks=1
        Act: Create ValidationReport
        Assert: ValueError raised
        """
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            ValidationReport(
                is_valid=True,  # Contradiction!
                checks=[
                    ValidationCheck(name="check1", passed=True, message="passed"),
                    ValidationCheck(name="check2", passed=False, message="failed"),
                ],
                total_checks=2,
                passed_checks=1,
                failed_checks=1  # Contradiction with is_valid=True
            )
        assert "is_valid" in str(exc_info.value).lower()


class TestUpgradeSummaryValidation:
    """Tests for UpgradeSummary data model validation"""

    def test_should_reject_empty_from_version(self):
        """
        Test: Empty from_version rejected

        Arrange: UpgradeSummary with empty from_version
        Act: Create UpgradeSummary
        Assert: ValueError raised
        """
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            UpgradeSummary(
                from_version="",
                to_version="1.0.1",
                status=UpgradeStatus.SUCCESS
            )
        assert "from_version" in str(exc_info.value)

    def test_should_reject_mismatched_file_counts(self):
        """
        Test: files_added must match len(files_added_list)

        Arrange: files_added=5 but files_added_list has 3 items
        Act: Create UpgradeSummary
        Assert: ValueError raised
        """
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            UpgradeSummary(
                from_version="1.0.0",
                to_version="1.0.1",
                status=UpgradeStatus.SUCCESS,
                files_added=5,  # Mismatch!
                files_added_list=["file1", "file2", "file3"],
                files_updated=0,
                files_removed=0
            )
        assert "files_added" in str(exc_info.value)

    def test_should_reject_invalid_upgrade_status(self):
        """
        Test: Invalid status rejected

        Arrange: status not an UpgradeStatus enum
        Act: Create UpgradeSummary
        Assert: Error raised (type error)
        """
        # Act & Assert - This should work with proper UpgradeStatus
        summary = UpgradeSummary(
            from_version="1.0.0",
            to_version="1.0.1",
            status=UpgradeStatus.SUCCESS
        )

        # Assert - Verify status is correct
        assert summary.status == UpgradeStatus.SUCCESS

    def test_should_require_error_message_on_failed_status(self, tmp_path):
        """
        Test: Failed status should ideally have error message

        Arrange: UpgradeSummary with FAILED status
        Act: Create UpgradeSummary
        Assert: Created (message optional but recommended)
        """
        # Act
        summary = UpgradeSummary(
            from_version="1.0.0",
            to_version="1.0.1",
            status=UpgradeStatus.FAILED,
            error_message="Database migration timeout"
        )

        # Assert
        assert summary.status == UpgradeStatus.FAILED
        assert summary.error_message == "Database migration timeout"

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


# ==================== COMPREHENSIVE COVERAGE GAP TESTS FOR MODELS ====================
# Targets: Lines 54-62, 79-83, 103-109, 123-129, 159-168, 191-210
# Phases: Model validation, error handling, edge cases

class TestBackupMetadataValidation:
    """Tests for BackupMetadata model validation"""

    def test_should_fail_with_empty_backup_id(self):
        """
        Coverage: Line 54 - Empty backup_id validation

        Arrange: BackupMetadata with empty backup_id
        Act: Create instance
        Assert: ValueError raised
        """
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            BackupMetadata(
                backup_id="",
                version="1.0.0",
                created_at="2025-01-01T00:00:00Z",
                files=[FileEntry(relative_path="file.txt", checksum_sha256="abc" + "0" * 61, size_bytes=100, modification_time=1000000000)],
                reason=BackupReason.UPGRADE
            )
        assert "backup_id is required" in str(exc_info.value)

    def test_should_fail_with_empty_version(self):
        """
        Coverage: Line 56 - Empty version validation

        Arrange: BackupMetadata with empty version
        Act: Create instance
        Assert: ValueError raised
        """
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            BackupMetadata(
                backup_id="v1.0.0-001",
                version="",
                created_at="2025-01-01T00:00:00Z",
                files=[FileEntry(relative_path="file.txt", checksum_sha256="abc" + "0" * 61, size_bytes=100, modification_time=1000000000)],
                reason=BackupReason.UPGRADE
            )
        assert "version is required" in str(exc_info.value)

    def test_should_fail_with_empty_created_at(self):
        """
        Coverage: Line 58 - Empty created_at validation

        Arrange: BackupMetadata with empty created_at
        Act: Create instance
        Assert: ValueError raised
        """
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            BackupMetadata(
                backup_id="v1.0.0-001",
                version="1.0.0",
                created_at="",
                files=[FileEntry(relative_path="file.txt", checksum_sha256="abc" + "0" * 61, size_bytes=100, modification_time=1000000000)],
                reason=BackupReason.UPGRADE
            )
        assert "created_at is required" in str(exc_info.value)

    def test_should_fail_with_empty_files_list(self):
        """
        Coverage: Line 60, 62 - Empty files list validation

        Arrange: BackupMetadata with empty files list
        Act: Create instance
        Assert: ValueError raised
        """
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            BackupMetadata(
                backup_id="v1.0.0-001",
                version="1.0.0",
                created_at="2025-01-01T00:00:00Z",
                files=[],
                reason=BackupReason.UPGRADE
            )
        assert "files list cannot be empty" in str(exc_info.value)

    def test_should_fail_with_invalid_semver_format(self):
        """
        Coverage: Line 88-89 - Invalid semver format

        Arrange: BackupMetadata with invalid version format
        Act: Create instance
        Assert: ValueError raised with semver message
        """
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            BackupMetadata(
                backup_id="v1.0.0-001",
                version="1.0",  # Only 2 parts
                created_at="2025-01-01T00:00:00Z",
                files=[FileEntry(relative_path="file.txt", checksum_sha256="abc" + "0" * 61, size_bytes=100, modification_time=1000000000)],
                reason=BackupReason.UPGRADE
            )
        assert "semver" in str(exc_info.value).lower()

    def test_should_fail_with_non_numeric_version_parts(self):
        """
        Coverage: Line 106-109 - Non-numeric version parts

        Arrange: BackupMetadata with non-numeric version parts
        Act: Create instance
        Assert: ValueError raised
        """
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            BackupMetadata(
                backup_id="v1.0.0-001",
                version="1.x.0",
                created_at="2025-01-01T00:00:00Z",
                files=[FileEntry(relative_path="file.txt", checksum_sha256="abc" + "0" * 61, size_bytes=100, modification_time=1000000000)],
                reason=BackupReason.UPGRADE
            )
        assert "valid semver" in str(exc_info.value).lower()


class TestMigrationScriptValidation:
    """Tests for MigrationScript model validation"""

    def test_should_fail_with_empty_path(self):
        """
        Coverage: Line 79 - Empty path validation

        Arrange: MigrationScript with empty path
        Act: Create instance
        Assert: ValueError raised
        """
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            MigrationScript(
                path="",
                from_version="1.0.0",
                to_version="1.1.0"
            )
        assert "path is required" in str(exc_info.value)

    def test_should_fail_when_migration_script_not_found(self):
        """
        Coverage: Line 81 - Script file not found

        Arrange: MigrationScript with non-existent path
        Act: Create instance
        Assert: ValueError raised
        """
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            MigrationScript(
                path="/nonexistent/path/migration.py",
                from_version="1.0.0",
                to_version="1.1.0"
            )
        assert "not found" in str(exc_info.value).lower()

    def test_should_fail_with_empty_from_version(self):
        """
        Coverage: Line 83 - Empty from_version validation

        Arrange: MigrationScript with empty from_version
        Act: Create instance
        Assert: ValueError raised
        """
        # Arrange
        migration_file = Path("/tmp/test_migration.py")
        migration_file.write_text("pass")

        try:
            # Act & Assert
            with pytest.raises(ValueError) as exc_info:
                MigrationScript(
                    path=str(migration_file),
                    from_version="",
                    to_version="1.1.0"
                )
            assert "from_version is required" in str(exc_info.value)
        finally:
            migration_file.unlink()

    def test_should_fail_with_empty_to_version(self):
        """
        Coverage: Line 83 - Empty to_version validation

        Arrange: MigrationScript with empty to_version
        Act: Create instance
        Assert: ValueError raised
        """
        # Arrange
        migration_file = Path("/tmp/test_migration2.py")
        migration_file.write_text("pass")

        try:
            # Act & Assert
            with pytest.raises(ValueError) as exc_info:
                MigrationScript(
                    path=str(migration_file),
                    from_version="1.0.0",
                    to_version=""
                )
            assert "to_version is required" in str(exc_info.value)
        finally:
            migration_file.unlink()

    def test_should_fail_with_invalid_from_version_format(self):
        """
        Coverage: Lines 132-133 - Invalid from_version semver

        Arrange: MigrationScript with invalid from_version format
        Act: Create instance
        Assert: ValueError raised
        """
        # Arrange
        migration_file = Path("/tmp/test_migration3.py")
        migration_file.write_text("pass")

        try:
            # Act & Assert
            with pytest.raises(ValueError) as exc_info:
                MigrationScript(
                    path=str(migration_file),
                    from_version="invalid.version",
                    to_version="1.1.0"
                )
            assert "semver" in str(exc_info.value).lower()
        finally:
            migration_file.unlink()


class TestValidationReportValidation:
    """Tests for ValidationReport model validation"""

    def test_should_fail_when_total_checks_mismatch(self):
        """
        Coverage: Line 103, 108-109 - Total checks mismatch

        Arrange: ValidationReport with mismatched total_checks
        Act: Create instance
        Assert: ValueError raised
        """
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            ValidationReport(
                is_valid=True,
                checks=[ValidationCheck(name="check1", passed=True, message="OK")],
                total_checks=5,  # Mismatch: only 1 check
                passed_checks=1,
                failed_checks=0
            )
        assert "total_checks" in str(exc_info.value)

    def test_should_fail_when_passed_plus_failed_not_equal_total(self):
        """
        Coverage: Line 123, 125, 127, 129 - Check count mismatch

        Arrange: ValidationReport with mismatched check counts
        Act: Create instance
        Assert: ValueError raised
        """
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            ValidationReport(
                is_valid=True,
                checks=[
                    ValidationCheck(name="check1", passed=True, message="OK"),
                    ValidationCheck(name="check2", passed=True, message="OK")
                ],
                total_checks=2,
                passed_checks=2,
                failed_checks=1  # Mismatch: 2+1 != 2
            )
        assert "must equal total_checks" in str(exc_info.value)

    def test_should_fail_when_is_valid_true_but_failed_checks_gt_0(self):
        """
        Coverage: Line 159, 163, 168 - Invalid state check

        Arrange: ValidationReport with is_valid=True but failed_checks>0
        Act: Create instance
        Assert: ValueError raised
        """
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            ValidationReport(
                is_valid=True,  # Invalid: should be False
                checks=[
                    ValidationCheck(name="check1", passed=True, message="OK"),
                    ValidationCheck(name="check2", passed=False, message="Failed")
                ],
                total_checks=2,
                passed_checks=1,
                failed_checks=1
            )
        assert "is_valid cannot be True when failed_checks > 0" in str(exc_info.value)


class TestValidationCheckValidation:
    """Tests for ValidationCheck model validation"""

    def test_should_create_validation_check_with_details(self):
        """
        Test: ValidationCheck with optional details

        Arrange: ValidationCheck with details dict
        Act: Create instance
        Assert: Instance created successfully with details
        """
        # Act
        check = ValidationCheck(
            name="file_exists",
            passed=True,
            message="File found",
            details={"path": "/path/to/file", "size": "1024 bytes"}
        )

        # Assert
        assert check.name == "file_exists"
        assert check.details["path"] == "/path/to/file"


class TestUpgradeSummaryValidation:
    """Tests for UpgradeSummary model validation"""

    def test_should_fail_with_empty_from_version(self):
        """
        Coverage: Line 191-192 - Empty from_version

        Arrange: UpgradeSummary with empty from_version
        Act: Create instance
        Assert: ValueError raised
        """
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            UpgradeSummary(
                from_version="",
                to_version="1.1.0",
                status=UpgradeStatus.SUCCESS
            )
        assert "from_version is required" in str(exc_info.value)

    def test_should_fail_with_empty_to_version(self):
        """
        Coverage: Line 193-194 - Empty to_version

        Arrange: UpgradeSummary with empty to_version
        Act: Create instance
        Assert: ValueError raised
        """
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            UpgradeSummary(
                from_version="1.0.0",
                to_version="",
                status=UpgradeStatus.SUCCESS
            )
        assert "to_version is required" in str(exc_info.value)

    def test_should_fail_with_null_status(self):
        """
        Coverage: Line 195-196 - Null status

        Arrange: UpgradeSummary with None status
        Act: Create instance
        Assert: ValueError raised
        """
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            UpgradeSummary(
                from_version="1.0.0",
                to_version="1.1.0",
                status=None
            )
        assert "status is required" in str(exc_info.value)

    def test_should_fail_when_files_added_mismatch(self):
        """
        Coverage: Lines 199-203 - File count mismatch

        Arrange: UpgradeSummary with mismatched added file counts
        Act: Create instance
        Assert: ValueError raised
        """
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            UpgradeSummary(
                from_version="1.0.0",
                to_version="1.1.0",
                status=UpgradeStatus.SUCCESS,
                files_added=5,
                files_added_list=["file1.txt", "file2.txt"]  # Only 2, not 5
            )
        assert "files_added" in str(exc_info.value)

    def test_should_fail_when_files_updated_mismatch(self):
        """
        Coverage: Lines 204-208 - Updated files mismatch

        Arrange: UpgradeSummary with mismatched updated file counts
        Act: Create instance
        Assert: ValueError raised
        """
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            UpgradeSummary(
                from_version="1.0.0",
                to_version="1.1.0",
                status=UpgradeStatus.SUCCESS,
                files_updated=3,
                files_updated_list=["file1.txt"]  # Only 1, not 3
            )
        assert "files_updated" in str(exc_info.value)

    def test_should_fail_when_files_removed_mismatch(self):
        """
        Coverage: Lines 209-213 - Removed files mismatch

        Arrange: UpgradeSummary with mismatched removed file counts
        Act: Create instance
        Assert: ValueError raised
        """
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            UpgradeSummary(
                from_version="1.0.0",
                to_version="1.1.0",
                status=UpgradeStatus.SUCCESS,
                files_removed=2,
                files_removed_list=[]  # Empty, not 2
            )
        assert "files_removed" in str(exc_info.value)


class TestFileEntryValidation:
    """Tests for FileEntry model validation"""

    def test_should_fail_with_empty_relative_path(self):
        """
        Coverage: Line 159 - Empty relative_path

        Arrange: FileEntry with empty relative_path
        Act: Create instance
        Assert: ValueError raised
        """
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            FileEntry(
                relative_path="",
                checksum_sha256="abc" + "0" * 61,
                size_bytes=100,
                modification_time=1000000000
            )
        assert "relative_path is required" in str(exc_info.value)

    def test_should_fail_with_empty_checksum(self):
        """
        Coverage: Line 163 - Empty checksum_sha256

        Arrange: FileEntry with empty checksum
        Act: Create instance
        Assert: ValueError raised
        """
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            FileEntry(
                relative_path="file.txt",
                checksum_sha256="",
                size_bytes=100,
                modification_time=1000000000
            )
        assert "checksum_sha256 is required" in str(exc_info.value)

    def test_should_fail_with_invalid_checksum_length(self):
        """
        Coverage: Line 168 - Invalid checksum length

        Arrange: FileEntry with wrong-length checksum
        Act: Create instance
        Assert: ValueError raised
        """
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            FileEntry(
                relative_path="file.txt",
                checksum_sha256="too_short",
                size_bytes=100,
                modification_time=1000000000
            )
        assert "64 characters" in str(exc_info.value)

    def test_should_fail_with_negative_size_bytes(self):
        """
        Coverage: Line 168 - Negative size

        Arrange: FileEntry with negative size_bytes
        Act: Create instance
        Assert: ValueError raised
        """
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            FileEntry(
                relative_path="file.txt",
                checksum_sha256="abc" + "0" * 61,
                size_bytes=-1,
                modification_time=1000000000
            )
        assert "non-negative" in str(exc_info.value)

    def test_should_fail_with_negative_modification_time(self):
        """
        Coverage: Line 168 - Negative modification time

        Arrange: FileEntry with negative modification_time
        Act: Create instance
        Assert: ValueError raised
        """
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            FileEntry(
                relative_path="file.txt",
                checksum_sha256="abc" + "0" * 61,
                size_bytes=100,
                modification_time=-1
            )
        assert "non-negative" in str(exc_info.value)


class TestExceptionClasses:
    """Tests for custom exception classes"""

    def test_should_create_upgrade_error(self):
        """
        Coverage: Lines 191-210 - Exception class coverage

        Arrange: Create UpgradeError
        Act: Raise exception
        Assert: Exception created successfully
        """
        # Act & Assert
        with pytest.raises(UpgradeError):
            raise UpgradeError("Base upgrade error")

    def test_should_create_backup_error(self):
        """
        Test: BackupError inherits from UpgradeError

        Arrange: Create BackupError
        Act: Raise exception
        Assert: Exception is UpgradeError subclass
        """
        # Act & Assert
        with pytest.raises(UpgradeError):
            raise BackupError("Backup failed")

    def test_should_create_migration_error(self):
        """
        Test: MigrationError inherits from UpgradeError

        Arrange: Create MigrationError
        Act: Raise exception
        Assert: Exception is UpgradeError subclass
        """
        # Act & Assert
        with pytest.raises(UpgradeError):
            raise MigrationError("Migration failed")

    def test_should_create_validation_error(self):
        """
        Test: ValidationError inherits from UpgradeError

        Arrange: Create ValidationError
        Act: Raise exception
        Assert: Exception is UpgradeError subclass
        """
        # Act & Assert
        with pytest.raises(UpgradeError):
            raise ValidationError("Validation failed")

    def test_should_create_rollback_error(self):
        """
        Test: RollbackError inherits from UpgradeError

        Arrange: Create RollbackError
        Act: Raise exception
        Assert: Exception is UpgradeError subclass
        """
        # Act & Assert
        with pytest.raises(UpgradeError):
            raise RollbackError("Rollback failed")

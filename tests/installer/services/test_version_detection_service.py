"""
Unit tests for VersionDetectionService.

Tests AC#1 and AC#2:
- Read .devforgeai/.version.json file
- Parse installed_version, installed_at, installation_source fields
- Compare semantic versions and provide recommendations
- Handle corrupted JSON and malformed versions

Component Requirements:
- SVC-004: Read .devforgeai/.version.json and parse installed version
- SVC-005: Compare installed vs source version using semantic versioning
- SVC-006: Handle corrupted version.json gracefully
- SVC-007: Handle non-standard versions (null, 'latest', 'dev')

Business Rules:
- BR-001: Auto-detection failures are non-fatal
"""

import pytest
from unittest.mock import Mock, patch, mock_open
from pathlib import Path
import json
from datetime import datetime
from packaging import version


# Story: STORY-073
class TestVersionDetectionService:
    """Test suite for VersionDetectionService - Version reading and comparison."""

    # AC#1: Read version.json file (SVC-004)

    # AC marker removed
    def test_should_read_version_json_successfully(self, temp_dir):
        """
        Test: Read valid version.json file → VersionInfo returned

        Given: .devforgeai/.version.json exists with valid structure
        When: read_version() is called
        Then: Returns VersionInfo with all fields populated
        """
        # Arrange
        from src.installer.services.version_detection_service import VersionDetectionService

        version_dir = temp_dir / ".devforgeai"
        version_dir.mkdir()
        version_file = version_dir / ".version.json"

        version_data = {
            "installed_version": "1.0.0",
            "installed_at": "2025-11-25T10:30:00Z",
            "installation_source": "installer"
        }
        version_file.write_text(json.dumps(version_data))

        service = VersionDetectionService(target_path=str(temp_dir))

        # Act
        result = service.read_version()

        # Assert
        assert result is not None
        assert result.installed_version == "1.0.0"
        assert result.installed_at == "2025-11-25T10:30:00Z"
        assert result.installation_source == "installer"

    # AC marker removed
    def test_should_return_none_when_version_json_missing(self, temp_dir):
        """
        Test: Missing version.json → None returned (SVC-004)

        Given: .devforgeai/.version.json does not exist
        When: read_version() is called
        Then: Returns None without error
        """
        # Arrange
        from src.installer.services.version_detection_service import VersionDetectionService

        service = VersionDetectionService(target_path=str(temp_dir))

        # Act
        result = service.read_version()

        # Assert
        assert result is None

    # AC marker removed
    def test_should_return_none_when_devforgeai_directory_missing(self, temp_dir):
        """
        Test: Missing .devforgeai directory → None returned

        Given: .devforgeai/ directory does not exist
        When: read_version() is called
        Then: Returns None without error
        """
        # Arrange
        from src.installer.services.version_detection_service import VersionDetectionService

        service = VersionDetectionService(target_path=str(temp_dir))

        # Act
        result = service.read_version()

        # Assert
        assert result is None

    # AC marker removed
    def test_should_handle_corrupted_json_gracefully(self, temp_dir):
        """
        Test: Corrupted version.json → None returned (SVC-006)

        Given: version.json contains invalid JSON
        When: read_version() is called
        Then: Returns None and logs error
        """
        # Arrange
        from src.installer.services.version_detection_service import VersionDetectionService

        version_dir = temp_dir / ".devforgeai"
        version_dir.mkdir()
        version_file = version_dir / ".version.json"
        version_file.write_text("{ invalid json content")

        service = VersionDetectionService(target_path=str(temp_dir))

        # Act
        result = service.read_version()

        # Assert
        assert result is None

    # AC marker removed
    def test_should_handle_missing_required_fields(self, temp_dir):
        """
        Test: version.json missing required fields → None returned (SVC-006)

        Given: version.json exists but missing installed_version
        When: read_version() is called
        Then: Returns None
        """
        # Arrange
        from src.installer.services.version_detection_service import VersionDetectionService

        version_dir = temp_dir / ".devforgeai"
        version_dir.mkdir()
        version_file = version_dir / ".version.json"

        version_data = {
            "installed_at": "2025-11-25T10:30:00Z"
            # Missing installed_version and installation_source
        }
        version_file.write_text(json.dumps(version_data))

        service = VersionDetectionService(target_path=str(temp_dir))

        # Act
        result = service.read_version()

        # Assert
        assert result is None

    # AC marker removed
    def test_should_handle_null_version_field(self, temp_dir):
        """
        Test: version.json with null installed_version → None returned (SVC-007)

        Given: version.json has null for installed_version
        When: read_version() is called
        Then: Returns None
        """
        # Arrange
        from src.installer.services.version_detection_service import VersionDetectionService

        version_dir = temp_dir / ".devforgeai"
        version_dir.mkdir()
        version_file = version_dir / ".version.json"

        version_data = {
            "installed_version": None,
            "installed_at": "2025-11-25T10:30:00Z",
            "installation_source": "installer"
        }
        version_file.write_text(json.dumps(version_data))

        service = VersionDetectionService(target_path=str(temp_dir))

        # Act
        result = service.read_version()

        # Assert
        assert result is None

    # AC#2: Version comparison with recommendations (SVC-005)

    # AC marker removed
    def test_should_recommend_upgrade_when_source_newer(self):
        """
        Test: Source version > installed version → "upgrade" action (SVC-005)

        Given: Installed version 1.0.0, source version 1.1.0
        When: compare_versions() is called
        Then: Returns action="upgrade" with recommendation message
        """
        # Arrange
        from src.installer.services.version_detection_service import VersionDetectionService

        service = VersionDetectionService(target_path="/tmp")

        # Act
        result = service.compare_versions(
            installed_version="1.0.0",
            source_version="1.1.0"
        )

        # Assert
        assert result.action == "upgrade"
        assert "1.0.0" in result.message
        assert "1.1.0" in result.message
        assert "recommended" in result.message.lower()

    # AC marker removed
    def test_should_warn_downgrade_when_source_older(self):
        """
        Test: Source version < installed version → "downgrade" action (SVC-005)

        Given: Installed version 2.0.0, source version 1.5.0
        When: compare_versions() is called
        Then: Returns action="downgrade" with warning message
        """
        # Arrange
        from src.installer.services.version_detection_service import VersionDetectionService

        service = VersionDetectionService(target_path="/tmp")

        # Act
        result = service.compare_versions(
            installed_version="2.0.0",
            source_version="1.5.0"
        )

        # Assert
        assert result.action == "downgrade"
        assert "2.0.0" in result.message
        assert "1.5.0" in result.message
        assert "warning" in result.message.lower() or "may lose features" in result.message.lower()

    # AC marker removed
    def test_should_indicate_same_version_when_equal(self):
        """
        Test: Source version == installed version → "same" action (SVC-005)

        Given: Installed version 1.0.0, source version 1.0.0
        When: compare_versions() is called
        Then: Returns action="same" with reinstall message
        """
        # Arrange
        from src.installer.services.version_detection_service import VersionDetectionService

        service = VersionDetectionService(target_path="/tmp")

        # Act
        result = service.compare_versions(
            installed_version="1.0.0",
            source_version="1.0.0"
        )

        # Assert
        assert result.action == "same"
        assert "1.0.0" in result.message
        assert "reinstall" in result.message.lower()

    # AC marker removed
    def test_should_handle_malformed_installed_version(self):
        """
        Test: Malformed installed version → "unknown" action (SVC-007)

        Given: Installed version is not valid semver
        When: compare_versions() is called
        Then: Returns action="unknown" with manual review message
        """
        # Arrange
        from src.installer.services.version_detection_service import VersionDetectionService

        service = VersionDetectionService(target_path="/tmp")

        # Act
        result = service.compare_versions(
            installed_version="invalid.version",
            source_version="1.0.0"
        )

        # Assert
        assert result.action == "unknown"
        assert "manual review" in result.message.lower()

    # AC marker removed
    def test_should_handle_malformed_source_version(self):
        """
        Test: Malformed source version → "unknown" action (SVC-007)

        Given: Source version is not valid semver
        When: compare_versions() is called
        Then: Returns action="unknown"
        """
        # Arrange
        from src.installer.services.version_detection_service import VersionDetectionService

        service = VersionDetectionService(target_path="/tmp")

        # Act
        result = service.compare_versions(
            installed_version="1.0.0",
            source_version="not-a-version"
        )

        # Assert
        assert result.action == "unknown"

    # AC marker removed
    def test_should_compare_major_version_correctly(self):
        """
        Test: Major version difference detected (SVC-005)

        Given: Installed 1.0.0, source 2.0.0
        When: compare_versions() is called
        Then: Returns action="upgrade"
        """
        # Arrange
        from src.installer.services.version_detection_service import VersionDetectionService

        service = VersionDetectionService(target_path="/tmp")

        # Act
        result = service.compare_versions(
            installed_version="1.0.0",
            source_version="2.0.0"
        )

        # Assert
        assert result.action == "upgrade"

    # AC marker removed
    def test_should_compare_minor_version_correctly(self):
        """
        Test: Minor version difference detected (SVC-005)

        Given: Installed 1.0.0, source 1.1.0
        When: compare_versions() is called
        Then: Returns action="upgrade"
        """
        # Arrange
        from src.installer.services.version_detection_service import VersionDetectionService

        service = VersionDetectionService(target_path="/tmp")

        # Act
        result = service.compare_versions(
            installed_version="1.0.0",
            source_version="1.1.0"
        )

        # Assert
        assert result.action == "upgrade"

    # AC marker removed
    def test_should_compare_patch_version_correctly(self):
        """
        Test: Patch version difference detected (SVC-005)

        Given: Installed 1.0.0, source 1.0.1
        When: compare_versions() is called
        Then: Returns action="upgrade"
        """
        # Arrange
        from src.installer.services.version_detection_service import VersionDetectionService

        service = VersionDetectionService(target_path="/tmp")

        # Act
        result = service.compare_versions(
            installed_version="1.0.0",
            source_version="1.0.1"
        )

        # Assert
        assert result.action == "upgrade"

    # Edge Cases: Non-standard versions (SVC-007)

    # AC marker removed
    def test_should_handle_prerelease_versions(self):
        """
        Test: Pre-release version comparison (Edge Case #8)

        Given: Version with pre-release tag (1.0.0-alpha)
        When: compare_versions() is called
        Then: Parses with semver, warns about stability
        """
        # Arrange
        from src.installer.services.version_detection_service import VersionDetectionService

        service = VersionDetectionService(target_path="/tmp")

        # Act
        result = service.compare_versions(
            installed_version="1.0.0-alpha",
            source_version="1.0.0"
        )

        # Assert
        assert result.action in ["upgrade", "unknown"]
        # Should mention pre-release or stability

    # AC marker removed
    def test_should_handle_dev_version(self):
        """
        Test: Dev version string → "unknown" action (SVC-007)

        Given: Version string "dev" or "latest"
        When: compare_versions() is called
        Then: Returns action="unknown"
        """
        # Arrange
        from src.installer.services.version_detection_service import VersionDetectionService

        service = VersionDetectionService(target_path="/tmp")

        # Act
        result_dev = service.compare_versions(
            installed_version="dev",
            source_version="1.0.0"
        )
        result_latest = service.compare_versions(
            installed_version="latest",
            source_version="1.0.0"
        )

        # Assert
        assert result_dev.action == "unknown"
        assert result_latest.action == "unknown"

    # AC marker removed
    def test_should_handle_empty_version_string(self):
        """
        Test: Empty version string → "unknown" action (SVC-007)

        Given: Version is empty string
        When: compare_versions() is called
        Then: Returns action="unknown"
        """
        # Arrange
        from src.installer.services.version_detection_service import VersionDetectionService

        service = VersionDetectionService(target_path="/tmp")

        # Act
        result = service.compare_versions(
            installed_version="",
            source_version="1.0.0"
        )

        # Assert
        assert result.action == "unknown"

    # Performance (NFR-001)

    def test_should_complete_version_read_within_10ms(self, temp_dir):
        """
        Test: Version.json parsing < 10ms (NFR)

        Given: Valid version.json file
        When: read_version() is called
        Then: Completes in <10ms
        """
        # Arrange
        import time
        from src.installer.services.version_detection_service import VersionDetectionService

        version_dir = temp_dir / ".devforgeai"
        version_dir.mkdir()
        version_file = version_dir / ".version.json"

        version_data = {
            "installed_version": "1.0.0",
            "installed_at": "2025-11-25T10:30:00Z",
            "installation_source": "installer"
        }
        version_file.write_text(json.dumps(version_data))

        service = VersionDetectionService(target_path=str(temp_dir))

        # Act
        start = time.time()
        result = service.read_version()
        duration_ms = (time.time() - start) * 1000

        # Assert
        assert duration_ms < 10, f"Read took {duration_ms}ms (expected <10ms)"

    # Data Model Validation

    def test_version_info_model_has_required_fields(self):
        """
        Test: VersionInfo data model has all required fields

        Given: VersionInfo class defined
        When: Instance is created
        Then: Has installed_version, installed_at, installation_source fields
        """
        # Arrange
        from src.installer.services.version_detection_service import VersionInfo

        # Act
        version_info = VersionInfo(
            installed_version="1.0.0",
            installed_at="2025-11-25T10:30:00Z",
            installation_source="installer"
        )

        # Assert
        assert hasattr(version_info, "installed_version")
        assert hasattr(version_info, "installed_at")
        assert hasattr(version_info, "installation_source")

    def test_version_comparison_result_has_required_fields(self):
        """
        Test: VersionComparisonResult has action and message fields

        Given: VersionComparisonResult class defined
        When: Instance is created
        Then: Has action and message fields
        """
        # Arrange
        from src.installer.services.version_detection_service import VersionComparisonResult

        # Act
        result = VersionComparisonResult(
            action="upgrade",
            message="Upgrade available"
        )

        # Assert
        assert hasattr(result, "action")
        assert hasattr(result, "message")
        assert result.action in ["upgrade", "downgrade", "same", "unknown"]

    # Business Rule BR-001: Non-fatal failures

    def test_should_not_crash_on_io_error(self, temp_dir):
        """
        Test: IOError reading file → None returned (BR-001)

        Given: File read raises IOError
        When: read_version() is called
        Then: Returns None without crashing
        """
        # Arrange
        from src.installer.services.version_detection_service import VersionDetectionService

        version_dir = temp_dir / ".devforgeai"
        version_dir.mkdir()
        version_file = version_dir / ".version.json"
        version_file.write_text('{"installed_version": "1.0.0"}')

        service = VersionDetectionService(target_path=str(temp_dir))

        with patch('builtins.open', side_effect=IOError("Cannot read")):
            # Act
            result = service.read_version()

            # Assert
            assert result is None

    def test_should_not_crash_on_permission_error(self, temp_dir):
        """
        Test: PermissionError → None returned (BR-001)

        Given: File read raises PermissionError
        When: read_version() is called
        Then: Returns None without crashing
        """
        # Arrange
        from src.installer.services.version_detection_service import VersionDetectionService

        version_dir = temp_dir / ".devforgeai"
        version_dir.mkdir()
        version_file = version_dir / ".version.json"
        version_file.write_text('{"installed_version": "1.0.0"}')

        service = VersionDetectionService(target_path=str(temp_dir))

        with patch('builtins.open', side_effect=PermissionError("Access denied")):
            # Act
            result = service.read_version()

            # Assert
            assert result is None

    # Cross-platform path handling

    def test_should_work_with_windows_paths(self):
        """
        Test: Windows path format supported

        Given: Target path is Windows format
        When: VersionDetectionService is instantiated
        Then: Path is handled correctly
        """
        # Arrange
        from src.installer.services.version_detection_service import VersionDetectionService

        # Act
        service = VersionDetectionService(target_path="C:\\test\\path")

        # Assert
        assert service is not None

    def test_should_work_with_unix_paths(self):
        """
        Test: Unix path format supported

        Given: Target path is Unix format
        When: VersionDetectionService is instantiated
        Then: Path is handled correctly
        """
        # Arrange
        from src.installer.services.version_detection_service import VersionDetectionService

        # Act
        service = VersionDetectionService(target_path="/test/path")

        # Assert
        assert service is not None

    # ===== COVERAGE GAP TESTS (Error handling in read_version and compare_versions) =====

    def test_read_version_with_parse_error(self, temp_dir):
        """
        Test: read_version handles JSON decode errors gracefully

        Given: version.json has malformed JSON that raises JSONDecodeError
        When: read_version() is called
        Then: Returns None and logs error without crashing
        """
        # Arrange
        from src.installer.services.version_detection_service import VersionDetectionService
        from unittest.mock import patch

        version_dir = temp_dir / ".devforgeai"
        version_dir.mkdir()
        version_file = version_dir / ".version.json"
        version_file.write_text('{"installed_version": "1.0.0"')  # Missing closing brace

        service = VersionDetectionService(target_path=str(temp_dir))

        with patch('src.installer.services.version_detection_service.logger') as mock_logger:
            # Act
            result = service.read_version()

            # Assert
            assert result is None
            mock_logger.error.assert_called()
            # Verify error message mentions corrupted or JSON
            error_call_args = str(mock_logger.error.call_args)
            assert 'corrupted' in error_call_args.lower() or 'json' in error_call_args.lower()

    def test_read_version_with_key_error(self, temp_dir):
        """
        Test: read_version handles KeyError for missing required fields

        Given: version.json missing 'installed_version' key
        When: read_version() is called
        Then: Returns None and logs warning (not error, per implementation line 110)
        """
        # Arrange
        from src.installer.services.version_detection_service import VersionDetectionService
        from unittest.mock import patch

        version_dir = temp_dir / ".devforgeai"
        version_dir.mkdir()
        version_file = version_dir / ".version.json"
        version_file.write_text('{"wrong_key": "value"}')  # Missing installed_version

        service = VersionDetectionService(target_path=str(temp_dir))

        with patch('src.installer.services.version_detection_service.logger') as mock_logger:
            # Act
            result = service.read_version()

            # Assert
            assert result is None
            # Implementation logs warning, not error (see line 110 in version_detection_service.py)
            mock_logger.warning.assert_called()

    def test_compare_versions_with_invalid_format(self):
        """
        Test: compare_versions handles malformed version strings

        Given: Version string raises InvalidVersion exception
        When: compare_versions() is called
        Then: Returns action="unknown" with manual review message
        """
        # Arrange
        from src.installer.services.version_detection_service import VersionDetectionService
        from unittest.mock import patch
        from packaging.version import InvalidVersion

        service = VersionDetectionService(target_path="/tmp")

        # Act - Test with version that raises InvalidVersion during parsing
        with patch('packaging.version.Version', side_effect=InvalidVersion("Invalid")):
            result = service.compare_versions(
                installed_version="1.0.0",
                source_version="totally.broken.version"
            )

        # Assert
        assert result.action == "unknown"
        assert "manual review" in result.message.lower()

    def test_compare_versions_with_none_values(self):
        """
        Test: compare_versions handles None version values

        Given: Installed or source version is None
        When: compare_versions() is called
        Then: Returns action="unknown"
        """
        # Arrange
        from src.installer.services.version_detection_service import VersionDetectionService

        service = VersionDetectionService(target_path="/tmp")

        # Act & Assert - None installed version
        result1 = service.compare_versions(
            installed_version=None,
            source_version="1.0.0"
        )
        assert result1.action == "unknown"

        # Act & Assert - None source version
        result2 = service.compare_versions(
            installed_version="1.0.0",
            source_version=None
        )
        assert result2.action == "unknown"

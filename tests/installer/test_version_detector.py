"""
Unit tests for VersionDetector service (STORY-077).

Tests AC#1: Version File Detection
- Read version from .devforgeai/.version.json
- Display version to user
- Complete within 1 second

Tests AC#6: Missing Version File Handling
- Handle missing .version.json gracefully
- Provide clear error messages

Tests Technical Specification:
- SVC-001: Read version from .devforgeai/.version.json
- SVC-002: Handle missing version file gracefully
- SVC-003: Handle corrupted version file
- NFR-001: Version detection < 1 second
- NFR-003: Graceful error handling for malformed JSON
- NFR-004: Read-only operations (no file modification)
"""

import pytest
import json
import time
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timezone


class TestVersionDetectorFileDetection:
    """Test AC#1: Version File Detection - Read .version.json"""

    def test_should_read_version_from_valid_version_file(self, temp_dir):
        """Given: .version.json exists with valid JSON
        When: read_version() called
        Then: returns Version object with correct fields"""
        # Arrange
        version_file = temp_dir / ".devforgeai" / ".version.json"
        version_file.parent.mkdir(parents=True, exist_ok=True)
        version_data = {
            "version": "1.2.3",
            "installed_at": "2025-11-25T10:30:00Z",
            "upgraded_from": None,
            "schema_version": 1
        }
        version_file.write_text(json.dumps(version_data))

        # Import here to avoid import errors if module doesn't exist yet
        from installer.version_detector import VersionDetector

        detector = VersionDetector(devforgeai_path=version_file.parent.parent / ".devforgeai")

        # Act
        version = detector.read_version()

        # Assert
        assert version is not None
        assert version.major == 1
        assert version.minor == 2
        assert version.patch == 3
        assert version.prerelease is None
        assert version.build is None

    def test_should_display_version_to_user(self, temp_dir):
        """Given: .version.json exists
        When: display_version() called
        Then: returns user-friendly formatted version string"""
        # Arrange
        version_file = temp_dir / ".devforgeai" / ".version.json"
        version_file.parent.mkdir(parents=True, exist_ok=True)
        version_data = {
            "version": "1.2.3",
            "installed_at": "2025-11-25T10:30:00Z",
            "upgraded_from": None,
            "schema_version": 1
        }
        version_file.write_text(json.dumps(version_data))

        from installer.version_detector import VersionDetector

        detector = VersionDetector(devforgeai_path=version_file.parent.parent / ".devforgeai")

        # Act
        display_text = detector.display_version()

        # Assert
        assert "1.2.3" in display_text or "v1.2.3" in display_text
        assert isinstance(display_text, str)

    def test_should_complete_within_one_second(self, temp_dir):
        """Given: .version.json exists
        When: read_version() called
        Then: operation completes in < 1 second (NFR-001)"""
        # Arrange
        version_file = temp_dir / ".devforgeai" / ".version.json"
        version_file.parent.mkdir(parents=True, exist_ok=True)
        version_data = {
            "version": "1.2.3",
            "installed_at": "2025-11-25T10:30:00Z"
        }
        version_file.write_text(json.dumps(version_data))

        from installer.version_detector import VersionDetector

        detector = VersionDetector(devforgeai_path=version_file.parent.parent / ".devforgeai")

        # Act & Assert
        start = time.time()
        detector.read_version()
        elapsed = time.time() - start

        assert elapsed < 1.0, f"Version detection took {elapsed}s (expected < 1s)"

    def test_should_handle_version_with_upgraded_from_field(self, temp_dir):
        """Given: .version.json has upgraded_from field
        When: read_version() called
        Then: upgraded_from field is available in metadata"""
        # Arrange
        version_file = temp_dir / ".devforgeai" / ".version.json"
        version_file.parent.mkdir(parents=True, exist_ok=True)
        version_data = {
            "version": "1.2.3",
            "installed_at": "2025-11-25T10:30:00Z",
            "upgraded_from": "1.1.0",
            "schema_version": 1
        }
        version_file.write_text(json.dumps(version_data))

        from installer.version_detector import VersionDetector

        detector = VersionDetector(devforgeai_path=version_file.parent.parent / ".devforgeai")

        # Act
        metadata = detector.read_version_metadata()

        # Assert
        assert metadata is not None
        assert metadata.get("upgraded_from") == "1.1.0"


class TestVersionDetectorMissingFile:
    """Test AC#6: Missing Version File Handling"""

    def test_should_return_none_when_version_file_missing(self, temp_dir):
        """Given: .version.json does not exist
        When: read_version() called
        Then: returns None (not exception) - graceful handling"""
        # Arrange
        devforgeai_path = temp_dir / ".devforgeai"
        devforgeai_path.mkdir(parents=True, exist_ok=True)

        from installer.version_detector import VersionDetector

        detector = VersionDetector(devforgeai_path=devforgeai_path)

        # Act
        version = detector.read_version()

        # Assert
        assert version is None

    def test_should_provide_error_result_when_file_missing(self, temp_dir):
        """Given: .version.json does not exist
        When: get_version_status() called
        Then: returns error result with clear message"""
        # Arrange
        devforgeai_path = temp_dir / ".devforgeai"
        devforgeai_path.mkdir(parents=True, exist_ok=True)

        from installer.version_detector import VersionDetector

        detector = VersionDetector(devforgeai_path=devforgeai_path)

        # Act
        result = detector.get_version_status()

        # Assert
        assert result["status"] == "missing"
        assert "not found" in result["message"].lower() or "missing" in result["message"].lower()

    def test_should_support_fresh_install_path_when_missing(self, temp_dir):
        """Given: .version.json does not exist
        When: detector.treat_as_fresh_install() called
        Then: version is set to 0.0.0"""
        # Arrange
        devforgeai_path = temp_dir / ".devforgeai"
        devforgeai_path.mkdir(parents=True, exist_ok=True)

        from installer.version_detector import VersionDetector

        detector = VersionDetector(devforgeai_path=devforgeai_path)

        # Act
        version = detector.treat_as_fresh_install()

        # Assert
        assert version.major == 0
        assert version.minor == 0
        assert version.patch == 0


class TestVersionDetectorCorruptedFile:
    """Test corrupted version file handling (SVC-003, NFR-003)"""

    def test_should_handle_invalid_json(self, temp_dir):
        """Given: .version.json contains invalid JSON
        When: read_version() called
        Then: returns error result with clear message (not exception)"""
        # Arrange
        version_file = temp_dir / ".devforgeai" / ".version.json"
        version_file.parent.mkdir(parents=True, exist_ok=True)
        version_file.write_text("{invalid json content")

        from installer.version_detector import VersionDetector

        detector = VersionDetector(devforgeai_path=version_file.parent.parent / ".devforgeai")

        # Act
        result = detector.get_version_status()

        # Assert
        assert result["status"] in ["error", "corrupted"]
        assert "json" in result["message"].lower() or "invalid" in result["message"].lower()

    def test_should_handle_empty_file(self, temp_dir):
        """Given: .version.json is empty
        When: read_version() called
        Then: returns error result gracefully"""
        # Arrange
        version_file = temp_dir / ".devforgeai" / ".version.json"
        version_file.parent.mkdir(parents=True, exist_ok=True)
        version_file.write_text("")

        from installer.version_detector import VersionDetector

        detector = VersionDetector(devforgeai_path=version_file.parent.parent / ".devforgeai")

        # Act
        result = detector.get_version_status()

        # Assert
        assert result["status"] in ["error", "corrupted"]

    def test_should_handle_missing_version_field(self, temp_dir):
        """Given: .version.json missing 'version' field
        When: read_version() called
        Then: returns error with clear message about missing field"""
        # Arrange
        version_file = temp_dir / ".devforgeai" / ".version.json"
        version_file.parent.mkdir(parents=True, exist_ok=True)
        version_data = {
            "installed_at": "2025-11-25T10:30:00Z",
            "schema_version": 1
        }
        version_file.write_text(json.dumps(version_data))

        from installer.version_detector import VersionDetector

        detector = VersionDetector(devforgeai_path=version_file.parent.parent / ".devforgeai")

        # Act
        result = detector.get_version_status()

        # Assert
        assert result["status"] == "error"
        assert "version" in result["message"].lower()

    def test_should_not_modify_file_on_read(self, temp_dir):
        """Given: .version.json exists
        When: read_version() called
        Then: file is not modified (NFR-004)"""
        # Arrange
        version_file = temp_dir / ".devforgeai" / ".version.json"
        version_file.parent.mkdir(parents=True, exist_ok=True)
        version_data = {
            "version": "1.2.3",
            "installed_at": "2025-11-25T10:30:00Z"
        }
        version_file.write_text(json.dumps(version_data))
        original_mtime = version_file.stat().st_mtime

        from installer.version_detector import VersionDetector

        detector = VersionDetector(devforgeai_path=version_file.parent.parent / ".devforgeai")

        # Act
        time.sleep(0.1)  # Small delay to ensure mtime would change if modified
        detector.read_version()

        # Assert
        new_mtime = version_file.stat().st_mtime
        assert new_mtime == original_mtime, "File was modified during read operation"


class TestVersionDetectorEdgeCases:
    """Test edge cases for version file detection"""

    def test_should_handle_version_with_all_metadata_fields(self, temp_dir):
        """Given: .version.json has all optional fields
        When: read_version_metadata() called
        Then: all fields are correctly read"""
        # Arrange
        version_file = temp_dir / ".devforgeai" / ".version.json"
        version_file.parent.mkdir(parents=True, exist_ok=True)
        version_data = {
            "version": "1.2.3",
            "installed_at": "2025-11-25T10:30:00Z",
            "upgraded_from": "1.1.0",
            "schema_version": 1
        }
        version_file.write_text(json.dumps(version_data))

        from installer.version_detector import VersionDetector

        detector = VersionDetector(devforgeai_path=version_file.parent.parent / ".devforgeai")

        # Act
        metadata = detector.read_version_metadata()

        # Assert
        assert metadata["version"] == "1.2.3"
        assert metadata["installed_at"] == "2025-11-25T10:30:00Z"
        assert metadata["upgraded_from"] == "1.1.0"
        assert metadata["schema_version"] == 1

    def test_should_validate_iso8601_timestamp(self, temp_dir):
        """Given: .version.json with installed_at field
        When: validate_timestamp() called
        Then: ISO8601 format is validated"""
        # Arrange
        version_file = temp_dir / ".devforgeai" / ".version.json"
        version_file.parent.mkdir(parents=True, exist_ok=True)
        version_data = {
            "version": "1.2.3",
            "installed_at": "2025-11-25T10:30:00Z",
            "schema_version": 1
        }
        version_file.write_text(json.dumps(version_data))

        from installer.version_detector import VersionDetector

        detector = VersionDetector(devforgeai_path=version_file.parent.parent / ".devforgeai")

        # Act
        metadata = detector.read_version_metadata()

        # Assert
        assert "T" in metadata["installed_at"]
        assert "Z" in metadata["installed_at"]

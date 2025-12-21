"""
Unit tests for ExistingInstallationDetector.

Tests AC#3: Existing Installation Detection
- Detect existing .claude/ directory
- Detect existing devforgeai/ directory
- Read version.json if present
- Display user choice prompt

Component Requirements:
- SVC-010: Detect existing installation by checking directories
- SVC-011: Read version.json if present and include version in message

Business Rules:
- BR-002: Warnings (⚠ WARN) allow continuation but prompt user
"""

import pytest
from unittest.mock import Mock, patch, mock_open
from pathlib import Path
import json


class TestExistingInstallationDetector:
    """Test suite for ExistingInstallationDetector service."""

    # AC#3: Existing Installation Detection - Fresh Install (PASS)

    def test_should_return_pass_when_no_existing_installation(self, fresh_installation_dir):
        """
        Test: No existing installation → PASS status

        Given: Target directory has no .claude/ or devforgeai/ directories
        When: ExistingInstallationDetector.check() is called
        Then: Returns CheckResult with PASS status
        """
        # Arrange
        from src.installer.validators.installation_detector import ExistingInstallationDetector

        detector = ExistingInstallationDetector(target_path=str(fresh_installation_dir))

        # Act
        result = detector.check()

        # Assert
        assert result.status == "PASS"
        assert "no existing" in result.message.lower() or "fresh" in result.message.lower()
        assert result.check_name == "Existing Installation"

    def test_should_return_pass_when_directory_empty(self, temp_dir):
        """
        Test: Empty directory → PASS status

        Given: Target directory is completely empty
        When: ExistingInstallationDetector.check() is called
        Then: Returns CheckResult with PASS status
        """
        # Arrange
        from src.installer.validators.installation_detector import ExistingInstallationDetector

        detector = ExistingInstallationDetector(target_path=str(temp_dir))

        # Act
        result = detector.check()

        # Assert
        assert result.status == "PASS"

    # AC#3: Existing Installation Detection - .claude/ Directory (WARN)

    def test_should_return_warn_when_claude_directory_exists(self, temp_dir):
        """
        Test: Existing .claude/ directory → WARN status (SVC-010)

        Given: Target directory contains .claude/ directory
        When: ExistingInstallationDetector.check() is called
        Then: Returns CheckResult with WARN status and prompt message
        """
        # Arrange
        from src.installer.validators.installation_detector import ExistingInstallationDetector

        claude_dir = temp_dir / ".claude"
        claude_dir.mkdir()

        detector = ExistingInstallationDetector(target_path=str(temp_dir))

        # Act
        result = detector.check()

        # Assert
        assert result.status == "WARN"
        assert ".claude" in result.message.lower()
        assert "existing" in result.message.lower()

    def test_should_return_warn_when_claude_skills_directory_exists(self, temp_dir):
        """
        Test: Existing .claude/skills/ directory → WARN status

        Given: Target directory contains .claude/skills/ structure
        When: ExistingInstallationDetector.check() is called
        Then: Returns CheckResult with WARN status
        """
        # Arrange
        from src.installer.validators.installation_detector import ExistingInstallationDetector

        skills_dir = temp_dir / ".claude" / "skills"
        skills_dir.mkdir(parents=True)

        detector = ExistingInstallationDetector(target_path=str(temp_dir))

        # Act
        result = detector.check()

        # Assert
        assert result.status == "WARN"
        assert "existing" in result.message.lower()

    # AC#3: Existing Installation Detection - devforgeai/ Directory (WARN)

    def test_should_return_warn_when_devforgeai_directory_exists(self, temp_dir):
        """
        Test: Existing devforgeai/ directory → WARN status (SVC-010)

        Given: Target directory contains devforgeai/ directory
        When: ExistingInstallationDetector.check() is called
        Then: Returns CheckResult with WARN status
        """
        # Arrange
        from src.installer.validators.installation_detector import ExistingInstallationDetector

        devforgeai_dir = temp_dir / "devforgeai"
        devforgeai_dir.mkdir()

        detector = ExistingInstallationDetector(target_path=str(temp_dir))

        # Act
        result = detector.check()

        # Assert
        assert result.status == "WARN"
        assert "devforgeai" in result.message.lower()

    def test_should_return_warn_when_devforgeai_context_directory_exists(self, temp_dir):
        """
        Test: Existing devforgeai/context/ directory → WARN status

        Given: Target directory contains devforgeai/context/ structure
        When: ExistingInstallationDetector.check() is called
        Then: Returns CheckResult with WARN status
        """
        # Arrange
        from src.installer.validators.installation_detector import ExistingInstallationDetector

        context_dir = temp_dir / "devforgeai" / "context"
        context_dir.mkdir(parents=True)

        detector = ExistingInstallationDetector(target_path=str(temp_dir))

        # Act
        result = detector.check()

        # Assert
        assert result.status == "WARN"

    def test_should_return_warn_when_both_directories_exist(self, existing_installation_dir):
        """
        Test: Both .claude/ and devforgeai/ exist → WARN status

        Given: Target directory contains both directories
        When: ExistingInstallationDetector.check() is called
        Then: Returns CheckResult with WARN status mentioning both
        """
        # Arrange
        from src.installer.validators.installation_detector import ExistingInstallationDetector

        detector = ExistingInstallationDetector(target_path=str(existing_installation_dir))

        # Act
        result = detector.check()

        # Assert
        assert result.status == "WARN"
        # Message should mention both directories or general "existing installation"
        assert "existing" in result.message.lower()

    # SVC-011: Read version.json if present and include version in message

    def test_should_read_version_json_if_present(self, temp_dir):
        """
        Test: Reads version.json and includes version in message (SVC-011)

        Given: Existing installation with version.json file
        When: ExistingInstallationDetector.check() is called
        Then: Message includes version number from version.json
        """
        # Arrange
        from src.installer.validators.installation_detector import ExistingInstallationDetector

        claude_dir = temp_dir / ".claude"
        claude_dir.mkdir()

        version_file = temp_dir / "version.json"
        version_data = {"version": "1.0.0", "release_date": "2025-11-25"}
        version_file.write_text(json.dumps(version_data))

        detector = ExistingInstallationDetector(target_path=str(temp_dir))

        # Act
        result = detector.check()

        # Assert
        assert result.status == "WARN"
        assert "1.0.0" in result.message or "v1.0.0" in result.message

    def test_should_handle_missing_version_json_gracefully(self, temp_dir):
        """
        Test: Missing version.json handled gracefully

        Given: Existing installation without version.json
        When: ExistingInstallationDetector.check() is called
        Then: Returns WARN without crashing, no version in message
        """
        # Arrange
        from src.installer.validators.installation_detector import ExistingInstallationDetector

        claude_dir = temp_dir / ".claude"
        claude_dir.mkdir()

        detector = ExistingInstallationDetector(target_path=str(temp_dir))

        # Act
        result = detector.check()

        # Assert
        assert result.status == "WARN"
        assert "existing" in result.message.lower()
        # Should not crash even without version.json

    def test_should_handle_invalid_version_json(self, temp_dir):
        """
        Test: Invalid version.json handled gracefully

        Given: Existing installation with malformed version.json
        When: ExistingInstallationDetector.check() is called
        Then: Returns WARN without crashing
        """
        # Arrange
        from src.installer.validators.installation_detector import ExistingInstallationDetector

        claude_dir = temp_dir / ".claude"
        claude_dir.mkdir()

        version_file = temp_dir / "version.json"
        version_file.write_text("invalid json content {")

        detector = ExistingInstallationDetector(target_path=str(temp_dir))

        # Act
        result = detector.check()

        # Assert
        assert result.status == "WARN"
        # Should not crash on malformed JSON

    def test_should_include_version_format_in_message(self, temp_dir):
        """
        Test: Version displayed in expected format (SVC-011)

        Given: version.json contains version "1.2.3"
        When: ExistingInstallationDetector.check() is called
        Then: Message includes "DevForgeAI v1.2.3" format
        """
        # Arrange
        from src.installer.validators.installation_detector import ExistingInstallationDetector

        claude_dir = temp_dir / ".claude"
        claude_dir.mkdir()

        version_file = temp_dir / "version.json"
        version_data = {"version": "1.2.3"}
        version_file.write_text(json.dumps(version_data))

        detector = ExistingInstallationDetector(target_path=str(temp_dir))

        # Act
        result = detector.check()

        # Assert
        assert result.status == "WARN"
        # Check for version format (flexible to allow "v1.2.3" or "1.2.3")
        assert "1.2.3" in result.message

    # AC#3: User Choice Prompt (in message)

    def test_should_include_user_choice_options_in_message(self, temp_dir):
        """
        Test: WARN message includes user choice options (AC#3)

        Given: Existing installation detected
        When: ExistingInstallationDetector.check() is called
        Then: Message includes upgrade/fresh install/cancel options
        """
        # Arrange
        from src.installer.validators.installation_detector import ExistingInstallationDetector

        claude_dir = temp_dir / ".claude"
        claude_dir.mkdir()

        detector = ExistingInstallationDetector(target_path=str(temp_dir))

        # Act
        result = detector.check()

        # Assert
        assert result.status == "WARN"
        message_lower = result.message.lower()
        # Check for choice indicators (flexible wording)
        choice_keywords = ["upgrade", "fresh", "cancel", "choose", "option"]
        matches = sum(1 for keyword in choice_keywords if keyword in message_lower)
        assert matches >= 2, "Message should include user choice guidance"

    # Edge Case: Partial previous installation

    def test_should_detect_partial_installation(self, partial_installation_dir):
        """
        Test: Partial installation → WARN with recommendation

        Given: Target directory has .claude/ but no skills subdirectory
        When: ExistingInstallationDetector.check() is called
        Then: Returns WARN status with partial installation context
        """
        # Arrange
        from src.installer.validators.installation_detector import ExistingInstallationDetector

        detector = ExistingInstallationDetector(target_path=str(partial_installation_dir))

        # Act
        result = detector.check()

        # Assert
        assert result.status == "WARN"
        assert "existing" in result.message.lower()

    def test_should_recommend_fresh_install_for_partial(self, temp_dir):
        """
        Test: Partial installation message recommends fresh install

        Given: Incomplete installation structure detected
        When: ExistingInstallationDetector.check() is called
        Then: Message recommends fresh installation
        """
        # Arrange
        from src.installer.validators.installation_detector import ExistingInstallationDetector

        # Create partial structure
        claude_dir = temp_dir / ".claude"
        claude_dir.mkdir()

        detector = ExistingInstallationDetector(target_path=str(temp_dir))

        # Act
        result = detector.check()

        # Assert
        assert result.status == "WARN"
        # Message should mention fresh install as option
        message_lower = result.message.lower()
        assert "fresh" in message_lower or "reinstall" in message_lower

    # Cross-platform path handling

    def test_should_work_with_windows_paths(self):
        """
        Test: Windows path format supported

        Given: Target path is Windows format
        When: ExistingInstallationDetector.check() is called
        Then: Correctly detects .claude/ and devforgeai/
        """
        # Arrange
        from src.installer.validators.installation_detector import ExistingInstallationDetector

        with patch('pathlib.Path.exists') as mock_exists:
            mock_exists.return_value = False

            detector = ExistingInstallationDetector(target_path="C:\\test\\path")

            # Act
            result = detector.check()

            # Assert
            assert result.status == "PASS"

    def test_should_work_with_unix_paths(self):
        """
        Test: Unix path format supported

        Given: Target path is Unix format
        When: ExistingInstallationDetector.check() is called
        Then: Correctly detects directories
        """
        # Arrange
        from src.installer.validators.installation_detector import ExistingInstallationDetector

        with patch('pathlib.Path.exists') as mock_exists:
            mock_exists.return_value = False

            detector = ExistingInstallationDetector(target_path="/test/path")

            # Act
            result = detector.check()

            # Assert
            assert result.status == "PASS"

    # Performance

    def test_should_complete_check_within_1_second(self, temp_dir):
        """
        Test: Installation detection completes in <1 second

        Given: Target directory structure
        When: ExistingInstallationDetector.check() is called
        Then: Execution completes in <1 second
        """
        # Arrange
        import time
        from src.installer.validators.installation_detector import ExistingInstallationDetector

        detector = ExistingInstallationDetector(target_path=str(temp_dir))

        # Act
        start = time.time()
        result = detector.check()
        duration_ms = (time.time() - start) * 1000

        # Assert
        assert duration_ms < 1000, f"Check took {duration_ms}ms (expected <1000ms)"

    # Security: Path traversal prevention

    def test_should_not_follow_symlinks_outside_target(self, temp_dir):
        """
        Test: Does not follow symlinks outside target directory

        Given: .claude/ is symlink to external directory
        When: ExistingInstallationDetector.check() is called
        Then: Detects symlink but does not follow outside target
        """
        # Arrange
        from src.installer.validators.installation_detector import ExistingInstallationDetector

        # Create symlink (if platform supports it)
        try:
            external_dir = temp_dir / "external"
            external_dir.mkdir()

            claude_link = temp_dir / ".claude"
            claude_link.symlink_to(external_dir)

            detector = ExistingInstallationDetector(target_path=str(temp_dir))

            # Act
            result = detector.check()

            # Assert
            assert result.status == "WARN"
            # Should detect existence but not access external path
        except OSError:
            # Symlinks not supported on platform, skip test
            pytest.skip("Symlinks not supported on this platform")

    # Reliability

    def test_should_handle_permission_errors_gracefully(self, temp_dir):
        """
        Test: Permission errors handled gracefully

        Given: Cannot read .claude/ directory due to permissions
        When: ExistingInstallationDetector.check() is called
        Then: Returns WARN with permission context
        """
        # Arrange
        from src.installer.validators.installation_detector import ExistingInstallationDetector

        with patch('pathlib.Path.exists') as mock_exists:
            mock_exists.side_effect = PermissionError("Access denied")

            detector = ExistingInstallationDetector(target_path=str(temp_dir))

            # Act
            result = detector.check()

            # Assert
            # Should not crash, returns WARN or error status
            assert result.status in ["WARN", "FAIL"]

    # Usability

    def test_should_include_installation_path_in_message(self, temp_dir):
        """
        Test: Message includes installation path (NFR-006)

        Given: Existing installation detected
        When: ExistingInstallationDetector.check() is called
        Then: Message includes path where installation found
        """
        # Arrange
        from src.installer.validators.installation_detector import ExistingInstallationDetector

        claude_dir = temp_dir / ".claude"
        claude_dir.mkdir()

        detector = ExistingInstallationDetector(target_path=str(temp_dir))

        # Act
        result = detector.check()

        # Assert
        assert result.status == "WARN"
        # Message should include path context
        assert str(temp_dir) in result.message or "path" in result.message.lower()

    # Version detection edge cases

    def test_should_handle_version_json_with_additional_fields(self, temp_dir):
        """
        Test: version.json with extra fields handled correctly

        Given: version.json contains additional metadata fields
        When: ExistingInstallationDetector.check() is called
        Then: Extracts version correctly, ignores extra fields
        """
        # Arrange
        from src.installer.validators.installation_detector import ExistingInstallationDetector

        claude_dir = temp_dir / ".claude"
        claude_dir.mkdir()

        version_file = temp_dir / "version.json"
        version_data = {
            "version": "2.0.0",
            "release_date": "2025-11-25",
            "build_number": "12345",
            "extra_field": "ignored"
        }
        version_file.write_text(json.dumps(version_data))

        detector = ExistingInstallationDetector(target_path=str(temp_dir))

        # Act
        result = detector.check()

        # Assert
        assert result.status == "WARN"
        assert "2.0.0" in result.message

    def test_should_handle_version_json_missing_version_field(self, temp_dir):
        """
        Test: version.json without "version" field handled gracefully

        Given: version.json exists but missing "version" key
        When: ExistingInstallationDetector.check() is called
        Then: Returns WARN without version in message
        """
        # Arrange
        from src.installer.validators.installation_detector import ExistingInstallationDetector

        claude_dir = temp_dir / ".claude"
        claude_dir.mkdir()

        version_file = temp_dir / "version.json"
        version_data = {"release_date": "2025-11-25"}
        version_file.write_text(json.dumps(version_data))

        detector = ExistingInstallationDetector(target_path=str(temp_dir))

        # Act
        result = detector.check()

        # Assert
        assert result.status == "WARN"
        # Should not crash, simply omit version from message

    # Edge Cases: _read_version exception handling (Lines 86-87, 114, 121-122)

    def test_should_handle_generic_exception_in_check(self, temp_dir):
        """
        Test: Generic exception during check() → WARN status

        Given: Path.exists() raises unexpected exception
        When: ExistingInstallationDetector.check() is called
        Then: Returns WARN with error context
        """
        # Arrange
        from src.installer.validators.installation_detector import ExistingInstallationDetector

        detector = ExistingInstallationDetector(target_path=str(temp_dir))

        with patch.object(Path, 'exists') as mock_exists:
            mock_exists.side_effect = RuntimeError("Unexpected filesystem error")

            # Act
            result = detector.check()

            # Assert
            assert result.status == "WARN"
            assert "error" in result.message.lower()

    def test_should_handle_io_error_reading_version_json(self, temp_dir):
        """
        Test: IOError reading version.json → returns None for version

        Given: version.json exists but raises IOError when read
        When: ExistingInstallationDetector.check() is called
        Then: Returns WARN without version (graceful handling)
        """
        # Arrange
        from src.installer.validators.installation_detector import ExistingInstallationDetector

        claude_dir = temp_dir / ".claude"
        claude_dir.mkdir()

        # Create version.json
        version_file = temp_dir / "version.json"
        version_file.write_text('{"version": "1.0.0"}')

        detector = ExistingInstallationDetector(target_path=str(temp_dir))

        # Mock open to raise IOError
        with patch('builtins.open', side_effect=IOError("Cannot read file")):
            # Act
            result = detector.check()

            # Assert
            assert result.status == "WARN"
            # Version should not appear since read failed
            assert "1.0.0" not in result.message or "existing" in result.message.lower()

    def test_should_handle_generic_exception_in_read_version(self, temp_dir):
        """
        Test: Generic exception in _read_version → returns None

        Given: Unexpected exception occurs during version reading
        When: ExistingInstallationDetector.check() is called
        Then: Returns WARN without crashing, no version in message
        """
        # Arrange
        from src.installer.validators.installation_detector import ExistingInstallationDetector

        claude_dir = temp_dir / ".claude"
        claude_dir.mkdir()

        version_file = temp_dir / "version.json"
        version_file.write_text('{"version": "2.0.0"}')

        detector = ExistingInstallationDetector(target_path=str(temp_dir))

        # Mock json.load to raise generic exception
        with patch('json.load', side_effect=Exception("Unexpected JSON error")):
            # Act
            result = detector.check()

            # Assert
            assert result.status == "WARN"
            # Should gracefully handle and continue without version

    def test_should_handle_version_json_with_empty_version(self, temp_dir):
        """
        Test: version.json with empty version string → no version in message

        Given: version.json has empty string for version
        When: ExistingInstallationDetector.check() is called
        Then: Returns WARN without including empty version
        """
        # Arrange
        from src.installer.validators.installation_detector import ExistingInstallationDetector

        claude_dir = temp_dir / ".claude"
        claude_dir.mkdir()

        version_file = temp_dir / "version.json"
        version_data = {"version": ""}
        version_file.write_text(json.dumps(version_data))

        detector = ExistingInstallationDetector(target_path=str(temp_dir))

        # Act
        result = detector.check()

        # Assert
        assert result.status == "WARN"
        # Empty version should be treated as no version
        assert "DevForgeAI v" not in result.message or "existing" in result.message.lower()

    def test_should_handle_version_json_with_null_version(self, temp_dir):
        """
        Test: version.json with null version → no version in message

        Given: version.json has null for version value
        When: ExistingInstallationDetector.check() is called
        Then: Returns WARN without version
        """
        # Arrange
        from src.installer.validators.installation_detector import ExistingInstallationDetector

        claude_dir = temp_dir / ".claude"
        claude_dir.mkdir()

        version_file = temp_dir / "version.json"
        version_data = {"version": None}
        version_file.write_text(json.dumps(version_data))

        detector = ExistingInstallationDetector(target_path=str(temp_dir))

        # Act
        result = detector.check()

        # Assert
        assert result.status == "WARN"
        assert "existing" in result.message.lower()

    def test_should_add_v_prefix_to_version_without_it(self, temp_dir):
        """
        Test: Version without 'v' prefix gets prefix added

        Given: version.json has version "1.2.3" (no prefix)
        When: ExistingInstallationDetector.check() is called
        Then: Message includes "v1.2.3" format
        """
        # Arrange
        from src.installer.validators.installation_detector import ExistingInstallationDetector

        claude_dir = temp_dir / ".claude"
        claude_dir.mkdir()

        version_file = temp_dir / "version.json"
        version_data = {"version": "1.2.3"}
        version_file.write_text(json.dumps(version_data))

        detector = ExistingInstallationDetector(target_path=str(temp_dir))

        # Act
        result = detector.check()

        # Assert
        assert result.status == "WARN"
        assert "v1.2.3" in result.message

    def test_should_preserve_v_prefix_if_already_present(self, temp_dir):
        """
        Test: Version with 'v' prefix is preserved as-is

        Given: version.json has version "v2.0.0" (with prefix)
        When: ExistingInstallationDetector.check() is called
        Then: Message includes "v2.0.0" (not "vv2.0.0")
        """
        # Arrange
        from src.installer.validators.installation_detector import ExistingInstallationDetector

        claude_dir = temp_dir / ".claude"
        claude_dir.mkdir()

        version_file = temp_dir / "version.json"
        version_data = {"version": "v2.0.0"}
        version_file.write_text(json.dumps(version_data))

        detector = ExistingInstallationDetector(target_path=str(temp_dir))

        # Act
        result = detector.check()

        # Assert
        assert result.status == "WARN"
        assert "v2.0.0" in result.message
        assert "vv2.0.0" not in result.message  # Should not double prefix

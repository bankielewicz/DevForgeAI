"""
Integration tests for STORY-077 version detection and compatibility checking.

Tests end-to-end workflows combining multiple services:
- VersionDetector
- VersionParser
- VersionComparator
- CompatibilityChecker

Tests all acceptance criteria working together in realistic scenarios.
"""

import pytest
import json
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch


class TestVersionFlowFreshInstall:
    """Test E2E: Fresh installation (no version file exists)"""

    def test_fresh_install_should_detect_missing_version_and_use_0_0_0(self, temp_dir):
        """Given: No .version.json exists
        When: installer runs version detection
        Then: treats as fresh install with version 0.0.0"""
        # Arrange
        devforgeai_path = temp_dir / "devforgeai"
        devforgeai_path.mkdir(parents=True, exist_ok=True)

        from installer.version_detector import VersionDetector

        detector = VersionDetector(devforgeai_path=devforgeai_path)

        # Act
        current_version = detector.read_version()

        # Assert
        if current_version is None:
            # Verify fresh install path is available
            fresh_version = detector.treat_as_fresh_install()
            assert fresh_version.major == 0
            assert fresh_version.minor == 0
            assert fresh_version.patch == 0

    def test_fresh_install_upgrade_to_1_0_0_is_safe(self, temp_dir):
        """Given: Fresh install (0.0.0) -> 1.0.0
        When: compatibility check runs
        Then: returns safe=True (any upgrade from 0.0.0 is safe)"""
        # Arrange
        from installer.version_parser import VersionParser
        from installer.compatibility_checker import CompatibilityChecker

        parser = VersionParser()
        checker = CompatibilityChecker()
        current = parser.parse("0.0.0")
        target = parser.parse("1.0.0")

        # Act
        result = checker.check_compatibility(current, target, force=False)

        # Assert
        assert result["safe"] is True
        assert result["blocked"] is False


class TestVersionFlowMinorUpgrade:
    """Test E2E: Minor version upgrade (backward compatible)"""

    def test_minor_upgrade_flow_1_0_0_to_1_1_0(self, temp_dir):
        """Given: Installed 1.0.0, upgrading to 1.1.0
        When: full version flow executes
        Then: detects upgrade, identifies as MINOR, allows without warning"""
        # Arrange
        version_file = temp_dir / "devforgeai" / ".version.json"
        version_file.parent.mkdir(parents=True, exist_ok=True)
        version_data = {
            "version": "1.0.0",
            "installed_at": "2025-11-25T10:00:00Z",
            "schema_version": 1
        }
        version_file.write_text(json.dumps(version_data))

        from installer.version_detector import VersionDetector
        from installer.version_parser import VersionParser
        from installer.version_comparator import VersionComparator
        from installer.compatibility_checker import CompatibilityChecker

        # Act
        detector = VersionDetector(devforgeai_path=version_file.parent.parent / "devforgeai")
        parser = VersionParser()
        comparator = VersionComparator()
        checker = CompatibilityChecker()

        current = detector.read_version()
        target = parser.parse("1.1.0")
        compare_result = comparator.compare(current, target)
        compat_result = checker.check_compatibility(current, target, force=False)

        # Assert
        assert current.major == 1
        assert current.minor == 0
        assert compare_result.upgrade_type == "MINOR"
        assert compat_result["safe"] is True
        assert compat_result["warnings"] == []

    def test_minor_upgrade_displays_version_info_to_user(self, temp_dir):
        """Given: Minor upgrade scenario
        When: detector.display_version() called
        Then: returns user-friendly version string"""
        # Arrange
        version_file = temp_dir / "devforgeai" / ".version.json"
        version_file.parent.mkdir(parents=True, exist_ok=True)
        version_data = {
            "version": "1.0.0",
            "installed_at": "2025-11-25T10:00:00Z"
        }
        version_file.write_text(json.dumps(version_data))

        from installer.version_detector import VersionDetector

        detector = VersionDetector(devforgeai_path=version_file.parent.parent / "devforgeai")

        # Act
        display = detector.display_version()

        # Assert
        assert "1.0.0" in display or "v1.0.0" in display
        assert isinstance(display, str)


class TestVersionFlowMajorUpgrade:
    """Test E2E: Major version upgrade (breaking changes)"""

    def test_major_upgrade_flow_1_0_0_to_2_0_0_requires_confirmation(self, temp_dir):
        """Given: Installed 1.0.0, upgrading to 2.0.0
        When: full version flow executes
        Then: detects upgrade, identifies as MAJOR, shows warnings"""
        # Arrange
        version_file = temp_dir / "devforgeai" / ".version.json"
        version_file.parent.mkdir(parents=True, exist_ok=True)
        version_data = {
            "version": "1.0.0",
            "installed_at": "2025-11-25T10:00:00Z",
            "schema_version": 1
        }
        version_file.write_text(json.dumps(version_data))

        from installer.version_detector import VersionDetector
        from installer.version_parser import VersionParser
        from installer.version_comparator import VersionComparator
        from installer.compatibility_checker import CompatibilityChecker

        # Act
        detector = VersionDetector(devforgeai_path=version_file.parent.parent / "devforgeai")
        parser = VersionParser()
        comparator = VersionComparator()
        checker = CompatibilityChecker()

        current = detector.read_version()
        target = parser.parse("2.0.0")
        compare_result = comparator.compare(current, target)
        compat_result = checker.check_compatibility(current, target, force=False)

        # Assert
        assert compare_result.upgrade_type == "MAJOR"
        assert compare_result.is_breaking is True
        assert compat_result["safe"] is False
        assert len(compat_result["warnings"]) > 0
        assert compat_result["is_breaking"] is True

    def test_major_upgrade_warning_includes_breaking_changes(self, temp_dir):
        """Given: Major upgrade with warnings
        When: check_compatibility() called
        Then: warnings list includes breaking change indicators"""
        # Arrange
        from installer.version_parser import VersionParser
        from installer.compatibility_checker import CompatibilityChecker

        parser = VersionParser()
        checker = CompatibilityChecker()
        current = parser.parse("1.0.0")
        target = parser.parse("2.0.0")

        # Act
        result = checker.check_compatibility(current, target, force=False)

        # Assert
        warnings = result["warnings"]
        assert len(warnings) > 0
        warning_text = " ".join(warnings).lower()
        assert any(keyword in warning_text for keyword in [
            "major", "breaking", "caution", "warning", "change"
        ])

    def test_major_upgrade_can_be_forced_with_flag(self, temp_dir):
        """Given: Major upgrade with --force flag
        When: check_compatibility(force=True) called
        Then: allows upgrade despite breaking changes"""
        # Arrange
        from installer.version_parser import VersionParser
        from installer.compatibility_checker import CompatibilityChecker

        parser = VersionParser()
        checker = CompatibilityChecker()
        current = parser.parse("1.0.0")
        target = parser.parse("2.0.0")

        # Act
        result_with_force = checker.check_compatibility(current, target, force=True)
        result_without_force = checker.check_compatibility(current, target, force=False)

        # Assert
        assert result_without_force["safe"] is False
        assert result_with_force["blocked"] is False


class TestVersionFlowDowngrade:
    """Test E2E: Downgrade scenarios (blocked by default)"""

    def test_downgrade_flow_2_0_0_to_1_5_0_is_blocked(self, temp_dir):
        """Given: Installed 2.0.0, attempting downgrade to 1.5.0
        When: full version flow executes
        Then: detects downgrade, blocks operation, shows error"""
        # Arrange
        version_file = temp_dir / "devforgeai" / ".version.json"
        version_file.parent.mkdir(parents=True, exist_ok=True)
        version_data = {
            "version": "2.0.0",
            "installed_at": "2025-11-25T10:00:00Z",
            "schema_version": 1
        }
        version_file.write_text(json.dumps(version_data))

        from installer.version_detector import VersionDetector
        from installer.version_parser import VersionParser
        from installer.version_comparator import VersionComparator
        from installer.compatibility_checker import CompatibilityChecker

        # Act
        detector = VersionDetector(devforgeai_path=version_file.parent.parent / "devforgeai")
        parser = VersionParser()
        comparator = VersionComparator()
        checker = CompatibilityChecker()

        current = detector.read_version()
        target = parser.parse("1.5.0")
        compare_result = comparator.compare(current, target)
        compat_result = checker.check_compatibility(current, target, force=False)

        # Assert
        assert compare_result.relationship == "DOWNGRADE"
        assert compat_result["blocked"] is True
        assert "error_message" in compat_result or "message" in compat_result
        if "exit_code" in compat_result:
            assert compat_result["exit_code"] != 0

    def test_downgrade_error_message_mentions_force_flag(self, temp_dir):
        """Given: Blocked downgrade
        When: check_compatibility() returns
        Then: error message mentions --force flag as override"""
        # Arrange
        from installer.version_parser import VersionParser
        from installer.compatibility_checker import CompatibilityChecker

        parser = VersionParser()
        checker = CompatibilityChecker()
        current = parser.parse("2.0.0")
        target = parser.parse("1.5.0")

        # Act
        result = checker.check_compatibility(current, target, force=False)

        # Assert
        message = result.get("error_message", "").lower()
        assert "--force" in message or "force" in message

    def test_downgrade_can_be_forced_with_flag(self, temp_dir):
        """Given: Downgrade with --force flag
        When: check_compatibility(force=True) called
        Then: allows downgrade despite block"""
        # Arrange
        from installer.version_parser import VersionParser
        from installer.compatibility_checker import CompatibilityChecker

        parser = VersionParser()
        checker = CompatibilityChecker()
        current = parser.parse("2.0.0")
        target = parser.parse("1.5.0")

        # Act
        result_with_force = checker.check_compatibility(current, target, force=True)
        result_without_force = checker.check_compatibility(current, target, force=False)

        # Assert
        assert result_without_force["blocked"] is True
        assert result_with_force["blocked"] is False


class TestVersionFlowPrerelease:
    """Test E2E: Pre-release version workflows"""

    def test_prerelease_ordering_in_full_flow(self, temp_dir):
        """Given: Installed 1.0.0-alpha, upgrading to 1.0.0-beta
        When: full flow executes
        Then: correctly identifies as upgrade"""
        # Arrange
        from installer.version_parser import VersionParser
        from installer.version_comparator import VersionComparator

        parser = VersionParser()
        comparator = VersionComparator()

        current = parser.parse("1.0.0-alpha")
        target = parser.parse("1.0.0-beta")

        # Act
        result = comparator.compare(current, target)

        # Assert
        assert result.relationship == "UPGRADE"

    def test_stable_release_from_prerelease(self, temp_dir):
        """Given: Installed 1.0.0-rc.1, upgrading to 1.0.0
        When: full flow executes
        Then: identifies as upgrade, allows safely"""
        # Arrange
        from installer.version_parser import VersionParser
        from installer.version_comparator import VersionComparator
        from installer.compatibility_checker import CompatibilityChecker

        parser = VersionParser()
        comparator = VersionComparator()
        checker = CompatibilityChecker()

        current = parser.parse("1.0.0-rc.1")
        target = parser.parse("1.0.0")

        # Act
        compare_result = comparator.compare(current, target)
        compat_result = checker.check_compatibility(current, target, force=False)

        # Assert
        assert compare_result.relationship == "UPGRADE"
        assert compat_result["safe"] is True


class TestVersionFlowErrorHandling:
    """Test E2E: Error handling and edge cases"""

    def test_corrupted_version_file_provides_clear_error(self, temp_dir):
        """Given: Corrupted .version.json
        When: detector.read_version() called
        Then: returns clear error without crashing"""
        # Arrange
        version_file = temp_dir / "devforgeai" / ".version.json"
        version_file.parent.mkdir(parents=True, exist_ok=True)
        version_file.write_text("{invalid json")

        from installer.version_detector import VersionDetector

        detector = VersionDetector(devforgeai_path=version_file.parent.parent / "devforgeai")

        # Act
        result = detector.get_version_status()

        # Assert
        assert result["status"] in ["error", "corrupted"]
        assert "message" in result

    def test_invalid_version_string_in_file_handled_gracefully(self, temp_dir):
        """Given: Valid JSON but invalid version string
        When: read_version() called
        Then: returns error without crashing"""
        # Arrange
        version_file = temp_dir / "devforgeai" / ".version.json"
        version_file.parent.mkdir(parents=True, exist_ok=True)
        version_data = {
            "version": "not.a.valid.version",
            "installed_at": "2025-11-25T10:00:00Z"
        }
        version_file.write_text(json.dumps(version_data))

        from installer.version_detector import VersionDetector

        detector = VersionDetector(devforgeai_path=version_file.parent.parent / "devforgeai")

        # Act
        result = detector.get_version_status()

        # Assert
        assert result["status"] == "error"


class TestVersionFlowPerformance:
    """Test E2E: Performance requirements"""

    def test_complete_version_detection_flow_under_1_second(self, temp_dir):
        """Given: Version detection flow
        When: full flow executes
        Then: completes in < 1 second total"""
        # Arrange
        version_file = temp_dir / "devforgeai" / ".version.json"
        version_file.parent.mkdir(parents=True, exist_ok=True)
        version_data = {
            "version": "1.0.0",
            "installed_at": "2025-11-25T10:00:00Z"
        }
        version_file.write_text(json.dumps(version_data))

        import time
        from installer.version_detector import VersionDetector
        from installer.version_parser import VersionParser
        from installer.version_comparator import VersionComparator
        from installer.compatibility_checker import CompatibilityChecker

        # Act
        start = time.time()

        detector = VersionDetector(devforgeai_path=version_file.parent.parent / "devforgeai")
        parser = VersionParser()
        comparator = VersionComparator()
        checker = CompatibilityChecker()

        current = detector.read_version()
        target = parser.parse("1.1.0")
        comparator.compare(current, target)
        checker.check_compatibility(current, target, force=False)

        elapsed = time.time() - start

        # Assert
        assert elapsed < 1.0, f"Full flow took {elapsed}s (expected < 1s)"


class TestVersionFlowRegressions:
    """Test regression scenarios and boundary conditions"""

    def test_version_0_0_0_upgrade_paths(self, temp_dir):
        """Given: Version 0.0.0 (initial development)
        When: upgrade to any version
        Then: correctly identified as upgrade"""
        # Arrange
        from installer.version_parser import VersionParser
        from installer.version_comparator import VersionComparator

        parser = VersionParser()
        comparator = VersionComparator()

        test_cases = [
            ("0.0.0", "0.0.1"),
            ("0.0.0", "0.1.0"),
            ("0.0.0", "1.0.0"),
        ]

        # Act & Assert
        for current_str, target_str in test_cases:
            result = comparator.compare(
                parser.parse(current_str),
                parser.parse(target_str)
            )
            assert result.relationship == "UPGRADE", \
                f"{current_str} -> {target_str} should be UPGRADE"

    def test_large_version_numbers_handled_correctly(self, temp_dir):
        """Given: Large version numbers (10+)
        When: compared
        Then: correctly identified (numeric not string comparison)"""
        # Arrange
        from installer.version_parser import VersionParser
        from installer.version_comparator import VersionComparator

        parser = VersionParser()
        comparator = VersionComparator()

        # Act
        result = comparator.compare(
            parser.parse("1.9.0"),
            parser.parse("1.10.0")
        )

        # Assert (1.10.0 > 1.9.0)
        assert result.relationship == "UPGRADE"

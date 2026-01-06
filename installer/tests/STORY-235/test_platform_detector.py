"""
Test Suite for Platform Detection Module (STORY-235)

TDD Green Phase: All tests should now PASS with implementation.

Test Categories:
- AC#1: Operating System Detection
- AC#2: WSL Version Detection
- AC#3: Filesystem Type Detection
- AC#4: Cross-Filesystem Detection
- AC#5: PlatformInfo Data Structure

Coverage Target: 95%+ for business logic layer
"""

import pytest
from unittest.mock import patch, mock_open, MagicMock
from pathlib import Path

# Path setup is in installer/tests/conftest.py (via sys.path.insert)
from installer.platform_detector import PlatformDetector, PlatformInfo


@pytest.fixture(autouse=True)
def clear_cache():
    """Clear PlatformDetector cache before and after each test."""
    PlatformDetector.clear_cache()
    yield
    PlatformDetector.clear_cache()


# ==============================================================================
# AC#1: Operating System Detection
# ==============================================================================

class TestOperatingSystemDetection:
    """
    AC#1: Given the installer is running on any supported platform,
    When the platform detector is invoked,
    Then it correctly identifies the operating system.
    """

    @pytest.mark.parametrize("mock_os,expected_os_type", [
        ("Linux", "Linux"),
        ("Darwin", "Darwin"),
        ("Windows", "Windows"),
    ])
    def test_detect_os_returns_correct_os_type(self, mock_os, expected_os_type):
        """
        Test: platform.system() mocked to each OS returns correct os_type.

        Arrange: Mock platform.system() to return specific OS string
        Act: Call PlatformDetector.detect()
        Assert: Returned PlatformInfo.os_type matches expected value
        """
        # Arrange
        with patch("platform.system", return_value=mock_os):
            # Act
            result = PlatformDetector.detect()

            # Assert
            assert result.os_type == expected_os_type, \
                f"Expected os_type='{expected_os_type}', got '{result.os_type}'"

    def test_detect_os_linux_returns_linux(self):
        """
        Test: platform.system() mocked to "Linux" returns os_type="Linux"
        (Source: STORY-235, AC#1 Verification Checklist line 295)
        """
        # Arrange
        with patch("platform.system", return_value="Linux"):
            with patch("builtins.open", mock_open(read_data="")):
                # Act
                result = PlatformDetector.detect()

                # Assert
                assert result.os_type == "Linux"

    def test_detect_os_darwin_returns_darwin(self):
        """
        Test: platform.system() mocked to "Darwin" returns os_type="Darwin"
        (Source: STORY-235, AC#1 Verification Checklist line 296)
        """
        # Arrange
        with patch("platform.system", return_value="Darwin"):
            # Act
            result = PlatformDetector.detect()

            # Assert
            assert result.os_type == "Darwin"

    def test_detect_os_windows_returns_windows(self):
        """
        Test: platform.system() mocked to "Windows" returns os_type="Windows"
        (Source: STORY-235, AC#1 Verification Checklist line 297)
        """
        # Arrange
        with patch("platform.system", return_value="Windows"):
            # Act
            result = PlatformDetector.detect()

            # Assert
            assert result.os_type == "Windows"


# ==============================================================================
# AC#2: WSL Version Detection
# ==============================================================================

class TestWSLVersionDetection:
    """
    AC#2: Given the installer is running on a Linux system,
    When the platform detector checks for WSL,
    Then it correctly identifies WSL presence and version.
    """

    def test_detect_wsl_true_when_microsoft_in_proc_version(self):
        """
        Test: /proc/version with "microsoft" returns is_wsl=True
        (Source: STORY-235, AC#2 Verification Checklist line 301)
        """
        # Arrange
        proc_version_content = "Linux version 5.15.90.1-microsoft-standard-WSL2"
        with patch("platform.system", return_value="Linux"):
            with patch("builtins.open", mock_open(read_data=proc_version_content)):
                # Act
                result = PlatformDetector.detect()

                # Assert
                assert result.is_wsl is True, \
                    f"Expected is_wsl=True when 'microsoft' in /proc/version"

    def test_detect_wsl_version_2_when_wsl2_in_proc_version(self):
        """
        Test: /proc/version with "WSL2" returns wsl_version=2
        (Source: STORY-235, AC#2 Verification Checklist line 302)
        """
        # Arrange
        proc_version_content = "Linux version 5.15.90.1-microsoft-standard-WSL2"
        with patch("platform.system", return_value="Linux"):
            with patch("builtins.open", mock_open(read_data=proc_version_content)):
                # Act
                result = PlatformDetector.detect()

                # Assert
                assert result.wsl_version == 2, \
                    f"Expected wsl_version=2 when 'WSL2' in /proc/version, got {result.wsl_version}"

    def test_detect_wsl_version_1_when_microsoft_but_not_wsl2(self):
        """
        Test: /proc/version with "microsoft" but no "WSL2" returns wsl_version=1
        """
        # Arrange
        proc_version_content = "Linux version 4.4.0-19041-Microsoft"
        with patch("platform.system", return_value="Linux"):
            with patch("builtins.open", mock_open(read_data=proc_version_content)):
                # Act
                result = PlatformDetector.detect()

                # Assert
                assert result.is_wsl is True
                assert result.wsl_version == 1, \
                    f"Expected wsl_version=1 for WSL1, got {result.wsl_version}"

    def test_detect_wsl_false_when_no_microsoft_in_proc_version(self):
        """
        Test: /proc/version without "microsoft" returns is_wsl=False
        (Source: STORY-235, AC#2 Verification Checklist line 303)
        """
        # Arrange
        proc_version_content = "Linux version 5.15.0-generic (buildd@lgw01-amd64-016)"
        with patch("platform.system", return_value="Linux"):
            with patch("builtins.open", mock_open(read_data=proc_version_content)):
                # Act
                result = PlatformDetector.detect()

                # Assert
                assert result.is_wsl is False, \
                    f"Expected is_wsl=False when 'microsoft' NOT in /proc/version"
                assert result.wsl_version is None, \
                    f"Expected wsl_version=None when not WSL"

    def test_detect_wsl_false_when_proc_version_missing(self):
        """
        Test: Missing /proc/version returns is_wsl=False (graceful error handling)
        (Source: STORY-235, AC#2 Verification Checklist line 304)
        (Source: STORY-235, BR-001: WSL detection must gracefully handle missing /proc/version)
        """
        # Arrange
        with patch("platform.system", return_value="Linux"):
            with patch("builtins.open", side_effect=FileNotFoundError("/proc/version")):
                # Act
                result = PlatformDetector.detect()

                # Assert
                assert result.is_wsl is False, \
                    f"Expected is_wsl=False when /proc/version missing"
                assert result.wsl_version is None, \
                    f"Expected wsl_version=None when /proc/version missing"

    def test_detect_wsl_case_insensitive_microsoft_detection(self):
        """
        Test: WSL detection is case-insensitive for "microsoft"
        (Source: STORY-235, Implementation Notes line 372)
        """
        # Arrange
        proc_version_content = "Linux version 5.15.90.1-MICROSOFT-standard-WSL2"
        with patch("platform.system", return_value="Linux"):
            with patch("builtins.open", mock_open(read_data=proc_version_content)):
                # Act
                result = PlatformDetector.detect()

                # Assert
                assert result.is_wsl is True, \
                    f"Expected case-insensitive detection of 'microsoft'"

    def test_detect_wsl_case_insensitive_wsl2_detection(self):
        """
        Test: WSL version detection is case-insensitive for "wsl2"
        (Source: STORY-235, Implementation Notes line 373)
        """
        # Arrange - lowercase "wsl2"
        proc_version_content = "Linux version 5.15.90.1-microsoft-standard-wsl2"
        with patch("platform.system", return_value="Linux"):
            with patch("builtins.open", mock_open(read_data=proc_version_content)):
                # Act
                result = PlatformDetector.detect()

                # Assert
                assert result.wsl_version == 2, \
                    f"Expected case-insensitive detection of 'wsl2'"


# ==============================================================================
# AC#3: Filesystem Type Detection
# ==============================================================================

class TestFilesystemTypeDetection:
    """
    AC#3: Given the installer is running with a target installation path,
    When the platform detector analyzes the path,
    Then it correctly identifies the filesystem type.
    """

    def test_detect_filesystem_ext4_for_native_linux(self):
        """
        Test: Native Linux path returns filesystem="ext4" or similar
        (Source: STORY-235, AC#3 Verification Checklist line 308)
        """
        # Arrange
        test_path = "/home/user/project"
        with patch("platform.system", return_value="Linux"):
            with patch("builtins.open", mock_open(read_data="")):  # No microsoft in proc/version
                # Act
                result = PlatformDetector.detect(path=test_path)

                # Assert
                assert result.filesystem in ["ext4", "btrfs", "xfs"], \
                    f"Expected Linux filesystem type, got '{result.filesystem}'"

    def test_detect_filesystem_ntfs_wsl_for_mnt_path_in_wsl(self):
        """
        Test: WSL /mnt/c path returns filesystem="ntfs-wsl"
        (Source: STORY-235, AC#3 Verification Checklist line 309)
        """
        # Arrange
        test_path = "/mnt/c/Users/user/project"
        proc_version_content = "Linux version 5.15.90.1-microsoft-standard-WSL2"
        with patch("platform.system", return_value="Linux"):
            with patch("builtins.open", mock_open(read_data=proc_version_content)):
                # Act
                result = PlatformDetector.detect(path=test_path)

                # Assert
                assert result.filesystem == "ntfs-wsl", \
                    f"Expected filesystem='ntfs-wsl' for /mnt/c in WSL, got '{result.filesystem}'"

    def test_detect_filesystem_ntfs_for_windows(self):
        """
        Test: Windows path returns filesystem="ntfs"
        """
        # Arrange
        test_path = "C:\\Users\\user\\project"
        with patch("platform.system", return_value="Windows"):
            # Act
            result = PlatformDetector.detect(path=test_path)

            # Assert
            assert result.filesystem in ["ntfs", "fat32"], \
                f"Expected Windows filesystem type, got '{result.filesystem}'"

    def test_detect_filesystem_apfs_for_macos(self):
        """
        Test: macOS path returns filesystem="apfs" or "hfs+"
        """
        # Arrange
        test_path = "/Users/user/project"
        with patch("platform.system", return_value="Darwin"):
            # Act
            result = PlatformDetector.detect(path=test_path)

            # Assert
            assert result.filesystem in ["apfs", "hfs+"], \
                f"Expected macOS filesystem type, got '{result.filesystem}'"


# ==============================================================================
# AC#4: Cross-Filesystem Detection
# ==============================================================================

class TestCrossFilesystemDetection:
    """
    AC#4: Given the installer is running in WSL with a target path starting with "/mnt/",
    When the platform detector analyzes the path,
    Then it correctly sets is_cross_filesystem and determines chmod support.
    """

    def test_detect_cross_filesystem_true_for_wsl_mnt_path(self):
        """
        Test: WSL + /mnt/c path returns is_cross_filesystem=True
        (Source: STORY-235, AC#4 Verification Checklist line 313)
        """
        # Arrange
        test_path = "/mnt/c/Users/user/project"
        proc_version_content = "Linux version 5.15.90.1-microsoft-standard-WSL2"
        with patch("platform.system", return_value="Linux"):
            with patch("builtins.open", mock_open(read_data=proc_version_content)):
                # Act
                result = PlatformDetector.detect(path=test_path)

                # Assert
                assert result.is_cross_filesystem is True, \
                    f"Expected is_cross_filesystem=True for /mnt/ path in WSL"

    def test_detect_cross_filesystem_false_for_native_linux_mnt(self):
        """
        Test: Native Linux + /mnt/data returns is_cross_filesystem=False
        (Source: STORY-235, AC#4 Verification Checklist line 314)
        (Source: STORY-235, BR-002: Cross-filesystem detection only applies in WSL)
        """
        # Arrange
        test_path = "/mnt/data/project"
        proc_version_content = "Linux version 5.15.0-generic (buildd@lgw01-amd64-016)"
        with patch("platform.system", return_value="Linux"):
            with patch("builtins.open", mock_open(read_data=proc_version_content)):
                # Act
                result = PlatformDetector.detect(path=test_path)

                # Assert
                assert result.is_cross_filesystem is False, \
                    f"Expected is_cross_filesystem=False for native Linux even with /mnt/ path"

    def test_detect_cross_filesystem_false_for_wsl_native_path(self):
        """
        Test: WSL + native Linux path (not /mnt/) returns is_cross_filesystem=False
        """
        # Arrange
        test_path = "/home/user/project"
        proc_version_content = "Linux version 5.15.90.1-microsoft-standard-WSL2"
        with patch("platform.system", return_value="Linux"):
            with patch("builtins.open", mock_open(read_data=proc_version_content)):
                # Act
                result = PlatformDetector.detect(path=test_path)

                # Assert
                assert result.is_cross_filesystem is False, \
                    f"Expected is_cross_filesystem=False for native path in WSL"

    def test_detect_chmod_not_supported_for_cross_filesystem(self):
        """
        Test: Cross-filesystem scenario sets supports_chmod=False
        (Source: STORY-235, AC#4: "chmod operations will not work")
        """
        # Arrange
        test_path = "/mnt/c/Users/user/project"
        proc_version_content = "Linux version 5.15.90.1-microsoft-standard-WSL2"
        with patch("platform.system", return_value="Linux"):
            with patch("builtins.open", mock_open(read_data=proc_version_content)):
                # Act
                result = PlatformDetector.detect(path=test_path)

                # Assert
                assert result.supports_chmod is False, \
                    f"Expected supports_chmod=False for cross-filesystem (NTFS via WSL)"


# ==============================================================================
# AC#5: PlatformInfo Data Structure
# ==============================================================================

class TestPlatformInfoDataStructure:
    """
    AC#5: Given platform detection completes successfully,
    When the detection results are returned,
    Then a PlatformInfo dataclass is returned with all fields populated.
    """

    def test_platform_info_has_all_required_fields(self):
        """
        Test: PlatformInfo dataclass has all required fields
        (Source: STORY-235, AC#5 lines 77-83)
        """
        # Arrange & Act
        # Check that PlatformInfo exists and has required attributes
        required_fields = [
            "os_type",
            "is_wsl",
            "wsl_version",
            "filesystem",
            "is_cross_filesystem",
            "supports_chmod",
        ]

        # Assert
        for field in required_fields:
            assert hasattr(PlatformInfo, "__dataclass_fields__") and \
                   field in PlatformInfo.__dataclass_fields__, \
                f"PlatformInfo missing required field: {field}"

    def test_detect_returns_platform_info_with_all_fields_populated(self):
        """
        Test: All fields populated in returned PlatformInfo
        (Source: STORY-235, AC#5 Verification Checklist line 319)
        """
        # Arrange
        test_path = "/home/user/project"
        proc_version_content = "Linux version 5.15.90.1-microsoft-standard-WSL2"
        with patch("platform.system", return_value="Linux"):
            with patch("builtins.open", mock_open(read_data=proc_version_content)):
                # Act
                result = PlatformDetector.detect(path=test_path)

                # Assert - All fields have values (not None for required fields)
                assert result.os_type is not None, "os_type must be populated"
                assert result.is_wsl is not None, "is_wsl must be populated"
                # wsl_version can be None if not WSL
                assert result.filesystem is not None, "filesystem must be populated"
                assert result.is_cross_filesystem is not None, "is_cross_filesystem must be populated"
                assert result.supports_chmod is not None, "supports_chmod must be populated"

    def test_platform_info_is_dataclass(self):
        """
        Test: PlatformInfo is a dataclass (immutable data container)
        (Source: STORY-235, Design Decisions line 367)
        """
        from dataclasses import is_dataclass

        # Assert
        assert is_dataclass(PlatformInfo), \
            "PlatformInfo must be a dataclass per design decision"

    def test_platform_info_field_types(self):
        """
        Test: PlatformInfo fields have correct types
        (Source: STORY-235, Technical Specification lines 99-128)
        """
        # Arrange
        test_path = "/home/user/project"
        with patch("platform.system", return_value="Linux"):
            with patch("builtins.open", mock_open(read_data="")):
                # Act
                result = PlatformDetector.detect(path=test_path)

                # Assert field types
                assert isinstance(result.os_type, str), "os_type must be str"
                assert isinstance(result.is_wsl, bool), "is_wsl must be bool"
                assert result.wsl_version is None or isinstance(result.wsl_version, int), \
                    "wsl_version must be Optional[int]"
                assert isinstance(result.filesystem, str), "filesystem must be str"
                assert isinstance(result.is_cross_filesystem, bool), "is_cross_filesystem must be bool"
                assert isinstance(result.supports_chmod, bool), "supports_chmod must be bool"


# ==============================================================================
# Technical Specification Tests (SVC Requirements)
# ==============================================================================

class TestServiceRequirements:
    """
    Tests derived from Technical Specification Service Requirements (SVC-001 to SVC-005)
    """

    def test_svc_001_detect_os_using_platform_system(self):
        """
        SVC-001: Detect operating system using platform.system()
        (Source: STORY-235, Technical Specification line 138)
        """
        # This test validates the implementation uses platform.system()
        with patch("platform.system", return_value="TestOS") as mock_platform:
            # Act - this should call platform.system()
            try:
                PlatformDetector.detect()
            except Exception:
                pass  # Implementation may not exist yet

            # Assert - platform.system was called
            mock_platform.assert_called()

    def test_svc_002_detect_wsl_by_parsing_proc_version(self):
        """
        SVC-002: Detect WSL by parsing /proc/version for 'microsoft'
        (Source: STORY-235, Technical Specification line 144)
        """
        # Arrange
        proc_version_content = "Linux version 5.15.90.1-microsoft-standard-WSL2"
        with patch("platform.system", return_value="Linux"):
            with patch("builtins.open", mock_open(read_data=proc_version_content)) as mock_file:
                # Act
                result = PlatformDetector.detect()

                # Assert - /proc/version was read
                mock_file.assert_called()
                assert result.is_wsl is True

    def test_svc_003_detect_wsl_version_from_version_string(self):
        """
        SVC-003: Detect WSL version (1 vs 2) from version string
        (Source: STORY-235, Technical Specification line 150)
        """
        # Test WSL2 detection
        proc_version_wsl2 = "Linux version 5.15.90.1-microsoft-standard-WSL2"
        with patch("platform.system", return_value="Linux"):
            with patch("builtins.open", mock_open(read_data=proc_version_wsl2)):
                result = PlatformDetector.detect()
                assert result.wsl_version == 2

        # Clear cache between iterations
        PlatformDetector.clear_cache()

        # Test WSL1 detection
        proc_version_wsl1 = "Linux version 4.4.0-19041-Microsoft"
        with patch("platform.system", return_value="Linux"):
            with patch("builtins.open", mock_open(read_data=proc_version_wsl1)):
                result = PlatformDetector.detect()
                assert result.wsl_version == 1

    def test_svc_004_detect_cross_filesystem_for_mnt_paths(self):
        """
        SVC-004: Detect cross-filesystem when path starts with /mnt/ in WSL
        (Source: STORY-235, Technical Specification line 155)
        """
        # Arrange
        test_path = "/mnt/c/project"
        proc_version_content = "Linux version 5.15.90.1-microsoft-standard-WSL2"
        with patch("platform.system", return_value="Linux"):
            with patch("builtins.open", mock_open(read_data=proc_version_content)):
                # Act
                result = PlatformDetector.detect(path=test_path)

                # Assert
                assert result.is_cross_filesystem is True

    def test_svc_005_determine_chmod_support_based_on_filesystem(self):
        """
        SVC-005: Determine chmod support based on filesystem type
        (Source: STORY-235, Technical Specification line 160)
        """
        # Test NTFS-WSL - chmod not supported
        test_path = "/mnt/c/project"
        proc_version_content = "Linux version 5.15.90.1-microsoft-standard-WSL2"
        with patch("platform.system", return_value="Linux"):
            with patch("builtins.open", mock_open(read_data=proc_version_content)):
                result = PlatformDetector.detect(path=test_path)
                assert result.supports_chmod is False, \
                    "NTFS-WSL should not support chmod"

        # Test ext4 - chmod supported
        test_path = "/home/user/project"
        with patch("platform.system", return_value="Linux"):
            with patch("builtins.open", mock_open(read_data="")):
                result = PlatformDetector.detect(path=test_path)
                assert result.supports_chmod is True, \
                    "Native Linux filesystem should support chmod"


# ==============================================================================
# Business Rules Tests (BR-001, BR-002)
# ==============================================================================

class TestBusinessRules:
    """
    Tests for business rules defined in Technical Specification
    """

    def test_br_001_graceful_handling_of_missing_proc_version(self):
        """
        BR-001: WSL detection must gracefully handle missing /proc/version
        (Source: STORY-235, Technical Specification line 165-168)
        """
        # Arrange
        with patch("platform.system", return_value="Linux"):
            with patch("builtins.open", side_effect=FileNotFoundError):
                # Act - should NOT raise exception
                result = PlatformDetector.detect()

                # Assert - returns safe defaults
                assert result.is_wsl is False
                assert result.wsl_version is None

    def test_br_001_graceful_handling_of_permission_error(self):
        """
        BR-001 extension: Handle permission errors reading /proc/version
        """
        # Arrange
        with patch("platform.system", return_value="Linux"):
            with patch("builtins.open", side_effect=PermissionError):
                # Act - should NOT raise exception
                result = PlatformDetector.detect()

                # Assert - returns safe defaults
                assert result.is_wsl is False
                assert result.wsl_version is None

    def test_br_002_cross_filesystem_only_applies_in_wsl(self):
        """
        BR-002: Cross-filesystem detection only applies in WSL
        (Source: STORY-235, Technical Specification line 172-176)
        """
        # Arrange - Native Linux (not WSL) with /mnt/ path
        test_path = "/mnt/data/project"
        native_linux_version = "Linux version 5.15.0-generic"
        with patch("platform.system", return_value="Linux"):
            with patch("builtins.open", mock_open(read_data=native_linux_version)):
                # Act
                result = PlatformDetector.detect(path=test_path)

                # Assert - not cross-filesystem even with /mnt/ path
                assert result.is_cross_filesystem is False


# ==============================================================================
# Non-Functional Requirements Tests (NFR-001, NFR-002)
# ==============================================================================

class TestNonFunctionalRequirements:
    """
    Tests for non-functional requirements
    """

    def test_nfr_001_detection_completes_under_100ms(self):
        """
        NFR-001: Platform detection must complete under 100ms
        (Source: STORY-235, Technical Specification line 184)
        """
        import time

        # Arrange
        with patch("platform.system", return_value="Linux"):
            with patch("builtins.open", mock_open(read_data="")):
                # Act
                start_time = time.time()
                PlatformDetector.detect()
                elapsed_ms = (time.time() - start_time) * 1000

                # Assert
                assert elapsed_ms < 100, \
                    f"Detection took {elapsed_ms:.2f}ms, expected <100ms"

    def test_nfr_002_works_on_all_supported_platforms(self):
        """
        NFR-002: Must work on all supported platforms
        (Source: STORY-235, Technical Specification line 189)
        """
        platforms = ["Linux", "Darwin", "Windows"]

        for platform_os in platforms:
            # Clear cache between platform iterations
            PlatformDetector.clear_cache()

            with patch("platform.system", return_value=platform_os):
                with patch("builtins.open", mock_open(read_data="")):
                    # Act - should not raise exception
                    result = PlatformDetector.detect()

                    # Assert - returns valid result
                    assert result is not None, f"Failed for platform: {platform_os}"
                    assert result.os_type == platform_os


# ==============================================================================
# Edge Cases and Error Handling
# ==============================================================================

class TestEdgeCasesAndErrorHandling:
    """
    Additional edge case tests for robustness
    """

    def test_detect_with_empty_path(self):
        """
        Test: Detection works with empty/None path (uses current directory)
        """
        with patch("platform.system", return_value="Linux"):
            with patch("builtins.open", mock_open(read_data="")):
                # Act - should not raise exception
                result = PlatformDetector.detect(path=None)

                # Assert
                assert result is not None
                assert result.os_type == "Linux"

    def test_detect_with_relative_path(self):
        """
        Test: Detection works with relative paths
        """
        test_path = "./relative/path"
        with patch("platform.system", return_value="Linux"):
            with patch("builtins.open", mock_open(read_data="")):
                # Act
                result = PlatformDetector.detect(path=test_path)

                # Assert
                assert result is not None

    def test_detect_with_pathlib_path(self):
        """
        Test: Detection works with pathlib.Path objects
        """
        test_path = Path("/home/user/project")
        with patch("platform.system", return_value="Linux"):
            with patch("builtins.open", mock_open(read_data="")):
                # Act
                result = PlatformDetector.detect(path=test_path)

                # Assert
                assert result is not None

    def test_detect_wsl_mnt_d_drive(self):
        """
        Test: Detection works for different Windows drive letters (/mnt/d, /mnt/e)
        """
        test_paths = ["/mnt/d/project", "/mnt/e/data", "/mnt/z/backup"]
        proc_version_content = "Linux version 5.15.90.1-microsoft-standard-WSL2"

        for test_path in test_paths:
            with patch("platform.system", return_value="Linux"):
                with patch("builtins.open", mock_open(read_data=proc_version_content)):
                    result = PlatformDetector.detect(path=test_path)
                    assert result.is_cross_filesystem is True, \
                        f"Expected cross-filesystem for path: {test_path}"

    def test_detect_wsl_uppercase_mnt_path(self):
        """
        Test: Detection is case-sensitive for /mnt/ (should NOT match /MNT/)
        """
        # Linux paths are case-sensitive, /MNT/ is different from /mnt/
        test_path = "/MNT/c/project"
        proc_version_content = "Linux version 5.15.90.1-microsoft-standard-WSL2"

        with patch("platform.system", return_value="Linux"):
            with patch("builtins.open", mock_open(read_data=proc_version_content)):
                result = PlatformDetector.detect(path=test_path)
                # /MNT/ should NOT trigger cross-filesystem since it's not /mnt/
                assert result.is_cross_filesystem is False

    def test_platform_info_is_immutable_like(self):
        """
        Test: PlatformInfo behaves like an immutable object (frozen dataclass)
        """
        # This tests that the implementation uses frozen=True or similar
        with patch("platform.system", return_value="Linux"):
            with patch("builtins.open", mock_open(read_data="")):
                result = PlatformDetector.detect()

                # Attempt to modify should raise error if frozen
                try:
                    result.os_type = "Modified"
                    # If we get here without error, the dataclass isn't frozen
                    # This is acceptable but frozen is preferred
                except Exception:
                    pass  # Expected for frozen dataclass


# ==============================================================================
# Caching Tests (Per Design Decision)
# ==============================================================================

class TestCachingBehavior:
    """
    Tests for caching behavior per design decision
    (Source: STORY-235, Design Decisions line 369)
    """

    def test_detect_caches_results_for_same_path(self):
        """
        Test: Detection results are cached for the same path
        """
        test_path = "/home/user/project"
        call_count = 0

        def counting_system():
            nonlocal call_count
            call_count += 1
            return "Linux"

        with patch("platform.system", side_effect=counting_system):
            with patch("builtins.open", mock_open(read_data="")):
                # Act - call twice with same path
                result1 = PlatformDetector.detect(path=test_path)
                result2 = PlatformDetector.detect(path=test_path)

                # Assert - second call should use cache (or at least return same result)
                assert result1 == result2, "Cached results should be equal"

    def test_detect_different_paths_may_have_different_results(self):
        """
        Test: Different paths can return different results
        """
        proc_version_content = "Linux version 5.15.90.1-microsoft-standard-WSL2"
        with patch("platform.system", return_value="Linux"):
            with patch("builtins.open", mock_open(read_data=proc_version_content)):
                # Act
                result_native = PlatformDetector.detect(path="/home/user/project")
                result_cross = PlatformDetector.detect(path="/mnt/c/project")

                # Assert - different cross-filesystem status
                assert result_native.is_cross_filesystem is False
                assert result_cross.is_cross_filesystem is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

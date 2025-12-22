"""
Unit tests for DiskSpaceChecker.

Tests AC#2: Disk Space Validation
- Calculate free space in MB
- PASS if ≥100MB available
- FAIL if <100MB available

Component Requirements:
- SVC-008: Calculate free space using shutil.disk_usage, compare against 100MB
- SVC-009: Handle exceptions gracefully with WARN status

Business Rules:
- BR-001: Critical failures (✗ FAIL) block installation
"""

import pytest
from unittest.mock import Mock, patch
from pathlib import Path


class TestDiskSpaceChecker:
    """Test suite for DiskSpaceChecker service."""

    # AC#2: Disk Space Validation - Sufficient Space (PASS)

    def test_should_return_pass_when_100mb_available(self):
        """
        Test: 100MB free space → PASS status (exact threshold)

        Given: Target directory has exactly 100MB free
        When: DiskSpaceChecker.check() is called
        Then: Returns CheckResult with PASS status
        """
        # Arrange
        from src.installer.validators.disk_space_checker import DiskSpaceChecker

        checker = DiskSpaceChecker(target_path="/test/path")

        with patch('shutil.disk_usage') as mock_disk_usage:
            # 100MB = 100 * 1024 * 1024 bytes
            mock_disk_usage.return_value = Mock(free=100 * 1024 * 1024)

            # Act
            result = checker.check()

            # Assert
            assert result.status == "PASS"
            assert "100" in result.message or "MB" in result.message
            assert result.check_name == "Disk Space"

    def test_should_return_pass_when_500mb_available(self):
        """
        Test: 500MB free space → PASS status (well above threshold)

        Given: Target directory has 500MB free
        When: DiskSpaceChecker.check() is called
        Then: Returns CheckResult with PASS status and space amount
        """
        # Arrange
        from src.installer.validators.disk_space_checker import DiskSpaceChecker

        checker = DiskSpaceChecker(target_path="/test/path")

        with patch('shutil.disk_usage') as mock_disk_usage:
            mock_disk_usage.return_value = Mock(free=500 * 1024 * 1024)

            # Act
            result = checker.check()

            # Assert
            assert result.status == "PASS"
            assert "500" in result.message or "MB" in result.message

    def test_should_return_pass_when_1gb_available(self):
        """
        Test: 1GB free space → PASS status

        Given: Target directory has 1GB free
        When: DiskSpaceChecker.check() is called
        Then: Returns CheckResult with PASS status
        """
        # Arrange
        from src.installer.validators.disk_space_checker import DiskSpaceChecker

        checker = DiskSpaceChecker(target_path="/test/path")

        with patch('shutil.disk_usage') as mock_disk_usage:
            mock_disk_usage.return_value = Mock(free=1024 * 1024 * 1024)  # 1GB

            # Act
            result = checker.check()

            # Assert
            assert result.status == "PASS"

    # AC#2: Disk Space Validation - Insufficient Space (FAIL)

    def test_should_return_fail_when_99mb_available(self):
        """
        Test: 99MB free space → FAIL status (below threshold)

        Given: Target directory has only 99MB free (below 100MB requirement)
        When: DiskSpaceChecker.check() is called
        Then: Returns CheckResult with FAIL status and resolution message
        """
        # Arrange
        from src.installer.validators.disk_space_checker import DiskSpaceChecker

        checker = DiskSpaceChecker(target_path="/test/path")

        with patch('shutil.disk_usage') as mock_disk_usage:
            mock_disk_usage.return_value = Mock(free=99 * 1024 * 1024)

            # Act
            result = checker.check()

            # Assert
            assert result.status == "FAIL"
            assert "99" in result.message
            assert "100" in result.message  # Required amount
            assert "insufficient" in result.message.lower() or "not enough" in result.message.lower()

    def test_should_return_fail_when_50mb_available(self):
        """
        Test: 50MB free space → FAIL status

        Given: Target directory has only 50MB free
        When: DiskSpaceChecker.check() is called
        Then: Returns CheckResult with FAIL status
        """
        # Arrange
        from src.installer.validators.disk_space_checker import DiskSpaceChecker

        checker = DiskSpaceChecker(target_path="/test/path")

        with patch('shutil.disk_usage') as mock_disk_usage:
            mock_disk_usage.return_value = Mock(free=50 * 1024 * 1024)

            # Act
            result = checker.check()

            # Assert
            assert result.status == "FAIL"
            assert "50" in result.message

    def test_should_return_fail_when_10mb_available(self):
        """
        Test: 10MB free space → FAIL status

        Given: Target directory has only 10MB free (critically low)
        When: DiskSpaceChecker.check() is called
        Then: Returns CheckResult with FAIL status
        """
        # Arrange
        from src.installer.validators.disk_space_checker import DiskSpaceChecker

        checker = DiskSpaceChecker(target_path="/test/path")

        with patch('shutil.disk_usage') as mock_disk_usage:
            mock_disk_usage.return_value = Mock(free=10 * 1024 * 1024)

            # Act
            result = checker.check()

            # Assert
            assert result.status == "FAIL"

    # SVC-008: Calculate free space using shutil.disk_usage

    def test_should_calculate_space_in_mb(self):
        """
        Test: Converts bytes to MB correctly (SVC-008)

        Given: shutil.disk_usage returns bytes
        When: DiskSpaceChecker.check() is called
        Then: Converts to MB and displays in message
        """
        # Arrange
        from src.installer.validators.disk_space_checker import DiskSpaceChecker

        checker = DiskSpaceChecker(target_path="/test/path")

        with patch('shutil.disk_usage') as mock_disk_usage:
            # 150MB in bytes
            mock_disk_usage.return_value = Mock(free=150 * 1024 * 1024)

            # Act
            result = checker.check()

            # Assert
            assert result.status == "PASS"
            assert "150" in result.message or "MB" in result.message

    def test_should_call_disk_usage_with_target_path(self):
        """
        Test: Calls shutil.disk_usage with correct path (SVC-008)

        Given: Target path is specified
        When: DiskSpaceChecker.check() is called
        Then: shutil.disk_usage is called with target path
        """
        # Arrange
        from src.installer.validators.disk_space_checker import DiskSpaceChecker

        target_path = "/specific/test/path"
        checker = DiskSpaceChecker(target_path=target_path)

        with patch('shutil.disk_usage') as mock_disk_usage:
            mock_disk_usage.return_value = Mock(free=200 * 1024 * 1024)

            # Act
            result = checker.check()

            # Assert
            mock_disk_usage.assert_called_once()
            # Verify path argument
            call_args = mock_disk_usage.call_args[0]
            assert target_path in str(call_args[0])

    # SVC-009: Handle exceptions gracefully with WARN status

    def test_should_return_warn_when_disk_usage_raises_exception(self):
        """
        Test: Disk usage calculation fails → WARN status (SVC-009)

        Given: shutil.disk_usage raises OSError
        When: DiskSpaceChecker.check() is called
        Then: Returns WARN status with error context
        """
        # Arrange
        from src.installer.validators.disk_space_checker import DiskSpaceChecker

        checker = DiskSpaceChecker(target_path="/test/path")

        with patch('shutil.disk_usage') as mock_disk_usage:
            mock_disk_usage.side_effect = OSError("Disk calculation failed")

            # Act
            result = checker.check()

            # Assert
            assert result.status == "WARN"
            assert "error" in result.message.lower() or "failed" in result.message.lower()

    def test_should_return_warn_when_permission_denied(self):
        """
        Test: Permission denied on path → WARN status

        Given: shutil.disk_usage raises PermissionError
        When: DiskSpaceChecker.check() is called
        Then: Returns WARN status with permission context
        """
        # Arrange
        from src.installer.validators.disk_space_checker import DiskSpaceChecker

        checker = DiskSpaceChecker(target_path="/test/path")

        with patch('shutil.disk_usage') as mock_disk_usage:
            mock_disk_usage.side_effect = PermissionError("Access denied")

            # Act
            result = checker.check()

            # Assert
            assert result.status == "WARN"
            assert "permission" in result.message.lower() or "access" in result.message.lower()

    def test_should_return_warn_when_path_not_found(self):
        """
        Test: Path does not exist → WARN status

        Given: Target path does not exist
        When: DiskSpaceChecker.check() is called
        Then: Returns WARN status
        """
        # Arrange
        from src.installer.validators.disk_space_checker import DiskSpaceChecker

        checker = DiskSpaceChecker(target_path="/nonexistent/path")

        with patch('shutil.disk_usage') as mock_disk_usage:
            mock_disk_usage.side_effect = FileNotFoundError("Path not found")

            # Act
            result = checker.check()

            # Assert
            assert result.status == "WARN"

    # NFR-003: Performance - Disk check completes in <200ms

    def test_should_complete_check_within_200ms(self):
        """
        Test: Disk space check completes in <200ms (NFR-003)

        Given: shutil.disk_usage is mocked
        When: DiskSpaceChecker.check() is called
        Then: Execution completes in <200ms
        """
        # Arrange
        import time
        from src.installer.validators.disk_space_checker import DiskSpaceChecker

        checker = DiskSpaceChecker(target_path="/test/path")

        with patch('shutil.disk_usage') as mock_disk_usage:
            mock_disk_usage.return_value = Mock(free=200 * 1024 * 1024)

            # Act
            start = time.time()
            result = checker.check()
            duration_ms = (time.time() - start) * 1000

            # Assert
            assert duration_ms < 200, f"Check took {duration_ms}ms (expected <200ms)"
            assert result.status == "PASS"

    # NFR-006: Usability - Error messages include actionable resolution steps

    def test_should_include_resolution_steps_in_fail_message(self):
        """
        Test: FAIL message includes resolution steps (NFR-006)

        Given: Disk space check returns FAIL status
        When: Message is examined
        Then: Contains actionable resolution steps
        """
        # Arrange
        from src.installer.validators.disk_space_checker import DiskSpaceChecker

        checker = DiskSpaceChecker(target_path="/test/path")

        with patch('shutil.disk_usage') as mock_disk_usage:
            mock_disk_usage.return_value = Mock(free=50 * 1024 * 1024)

            # Act
            result = checker.check()

            # Assert
            assert result.status == "FAIL"
            # Message should contain resolution guidance
            message_lower = result.message.lower()
            resolution_keywords = ["free up", "delete", "space", "required", "retry"]
            matches = sum(1 for keyword in resolution_keywords if keyword in message_lower)
            assert matches >= 2, "Message should contain at least 2 resolution keywords"

    # Edge Case: Network mount disk space calculation

    def test_should_handle_network_mount_gracefully(self):
        """
        Test: Network mount disk calculation failure → WARN

        Given: Target path is network mount with calculation issues
        When: DiskSpaceChecker.check() is called
        Then: Returns WARN status (not FAIL)
        """
        # Arrange
        from src.installer.validators.disk_space_checker import DiskSpaceChecker

        checker = DiskSpaceChecker(target_path="/mnt/network/path")

        with patch('shutil.disk_usage') as mock_disk_usage:
            mock_disk_usage.side_effect = OSError("Network timeout")

            # Act
            result = checker.check()

            # Assert
            assert result.status == "WARN"

    # Configuration validation

    def test_should_use_configured_minimum_space(self):
        """
        Test: Uses MIN_DISK_SPACE_MB from config

        Given: MIN_DISK_SPACE_MB is configured as 100
        When: DiskSpaceChecker checks space
        Then: Compares against configured minimum
        """
        # Arrange
        from src.installer.validators.disk_space_checker import DiskSpaceChecker

        checker = DiskSpaceChecker(target_path="/test/path", min_space_mb=100)

        test_cases = [
            (100 * 1024 * 1024, "PASS"),  # Exactly 100MB
            (99 * 1024 * 1024, "FAIL"),   # Below 100MB
        ]

        for free_bytes, expected_status in test_cases:
            with patch('shutil.disk_usage') as mock_disk_usage:
                mock_disk_usage.return_value = Mock(free=free_bytes)

                # Act
                result = checker.check()

                # Assert
                assert result.status == expected_status, \
                    f"Expected {expected_status} for {free_bytes} bytes, got {result.status}"

    # Boundary testing

    def test_should_handle_zero_free_space(self):
        """
        Test: Zero free space → FAIL status

        Given: Disk has 0 bytes free
        When: DiskSpaceChecker.check() is called
        Then: Returns FAIL status
        """
        # Arrange
        from src.installer.validators.disk_space_checker import DiskSpaceChecker

        checker = DiskSpaceChecker(target_path="/test/path")

        with patch('shutil.disk_usage') as mock_disk_usage:
            mock_disk_usage.return_value = Mock(free=0)

            # Act
            result = checker.check()

            # Assert
            assert result.status == "FAIL"
            assert "0" in result.message

    def test_should_handle_very_large_disk_space(self):
        """
        Test: Very large disk (10TB) → PASS status

        Given: Disk has 10TB free
        When: DiskSpaceChecker.check() is called
        Then: Returns PASS status with correct conversion
        """
        # Arrange
        from src.installer.validators.disk_space_checker import DiskSpaceChecker

        checker = DiskSpaceChecker(target_path="/test/path")

        with patch('shutil.disk_usage') as mock_disk_usage:
            # 10TB in bytes
            mock_disk_usage.return_value = Mock(free=10 * 1024 * 1024 * 1024 * 1024)

            # Act
            result = checker.check()

            # Assert
            assert result.status == "PASS"
            # Message should show large number (likely in GB or TB)

    # Cross-platform compatibility

    def test_should_work_on_windows_paths(self):
        """
        Test: Windows path format supported

        Given: Target path is Windows format (C:\\path)
        When: DiskSpaceChecker.check() is called
        Then: Works correctly with Windows path
        """
        # Arrange
        from src.installer.validators.disk_space_checker import DiskSpaceChecker

        checker = DiskSpaceChecker(target_path="C:\\test\\path")

        with patch('shutil.disk_usage') as mock_disk_usage:
            mock_disk_usage.return_value = Mock(free=200 * 1024 * 1024)

            # Act
            result = checker.check()

            # Assert
            assert result.status == "PASS"

    def test_should_work_on_unix_paths(self):
        """
        Test: Unix path format supported

        Given: Target path is Unix format (/path/to/dir)
        When: DiskSpaceChecker.check() is called
        Then: Works correctly with Unix path
        """
        # Arrange
        from src.installer.validators.disk_space_checker import DiskSpaceChecker

        checker = DiskSpaceChecker(target_path="/test/path")

        with patch('shutil.disk_usage') as mock_disk_usage:
            mock_disk_usage.return_value = Mock(free=200 * 1024 * 1024)

            # Act
            result = checker.check()

            # Assert
            assert result.status == "PASS"

    # Edge Cases: Generic exception handling (Lines 79-80)

    def test_should_handle_generic_exception_during_disk_check(self):
        """
        Test: Generic exception during disk check → WARN status

        Given: shutil.disk_usage raises unexpected exception
        When: DiskSpaceChecker.check() is called
        Then: Returns WARN status with error context
        """
        # Arrange
        from src.installer.validators.disk_space_checker import DiskSpaceChecker

        checker = DiskSpaceChecker(target_path="/test/path")

        with patch('shutil.disk_usage') as mock_disk_usage:
            mock_disk_usage.side_effect = RuntimeError("Unexpected system error")

            # Act
            result = checker.check()

            # Assert
            assert result.status == "WARN"
            assert "error" in result.message.lower() or "unexpected" in result.message.lower()

    def test_should_handle_value_error_in_disk_calculation(self):
        """
        Test: ValueError during calculation → WARN status

        Given: Disk usage returns invalid data causing ValueError
        When: DiskSpaceChecker.check() is called
        Then: Returns WARN status gracefully
        """
        # Arrange
        from src.installer.validators.disk_space_checker import DiskSpaceChecker

        checker = DiskSpaceChecker(target_path="/test/path")

        with patch('shutil.disk_usage') as mock_disk_usage:
            mock_disk_usage.side_effect = ValueError("Invalid disk data")

            # Act
            result = checker.check()

            # Assert
            assert result.status == "WARN"

    def test_should_handle_attribute_error_on_disk_usage_result(self):
        """
        Test: AttributeError on disk_usage result → WARN status

        Given: disk_usage returns object without 'free' attribute
        When: DiskSpaceChecker.check() is called
        Then: Returns WARN status (caught by generic exception)
        """
        # Arrange
        from src.installer.validators.disk_space_checker import DiskSpaceChecker

        checker = DiskSpaceChecker(target_path="/test/path")

        with patch('shutil.disk_usage') as mock_disk_usage:
            mock_disk_usage.side_effect = AttributeError("'NoneType' has no attribute 'free'")

            # Act
            result = checker.check()

            # Assert
            assert result.status == "WARN"

    def test_should_handle_type_error_in_space_calculation(self):
        """
        Test: TypeError during space calculation → WARN status

        Given: Calculation fails due to type mismatch
        When: DiskSpaceChecker.check() is called
        Then: Returns WARN status
        """
        # Arrange
        from src.installer.validators.disk_space_checker import DiskSpaceChecker

        checker = DiskSpaceChecker(target_path="/test/path")

        with patch('shutil.disk_usage') as mock_disk_usage:
            mock_disk_usage.side_effect = TypeError("unsupported operand type(s)")

            # Act
            result = checker.check()

            # Assert
            assert result.status == "WARN"

    def test_should_include_error_details_in_generic_exception_message(self):
        """
        Test: Generic exception message includes error details

        Given: shutil.disk_usage raises exception with specific message
        When: DiskSpaceChecker.check() is called
        Then: WARN message includes original error context
        """
        # Arrange
        from src.installer.validators.disk_space_checker import DiskSpaceChecker

        checker = DiskSpaceChecker(target_path="/test/path")

        with patch('shutil.disk_usage') as mock_disk_usage:
            mock_disk_usage.side_effect = Exception("Custom error message")

            # Act
            result = checker.check()

            # Assert
            assert result.status == "WARN"
            # Message should contain some error context
            assert "error" in result.message.lower() or "unexpected" in result.message.lower()

    def test_should_handle_keyboard_interrupt_gracefully(self):
        """
        Test: KeyboardInterrupt during disk check → still returns WARN

        Given: User interrupts during disk check (rare edge case)
        When: DiskSpaceChecker.check() is called
        Then: Exception propagates (not caught by generic handler)

        Note: KeyboardInterrupt is BaseException, not Exception,
        so it should propagate up rather than be caught.
        """
        # Arrange
        from src.installer.validators.disk_space_checker import DiskSpaceChecker

        checker = DiskSpaceChecker(target_path="/test/path")

        with patch('shutil.disk_usage') as mock_disk_usage:
            mock_disk_usage.side_effect = KeyboardInterrupt()

            # Act & Assert
            # KeyboardInterrupt should propagate (not be caught)
            with pytest.raises(KeyboardInterrupt):
                checker.check()

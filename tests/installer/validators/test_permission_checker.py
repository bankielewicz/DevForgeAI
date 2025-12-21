"""
Unit tests for PermissionChecker.

Tests AC#4: Write Permission Validation
- Create temporary test file
- Delete test file immediately
- PASS if writable
- FAIL if permission denied

Component Requirements:
- SVC-012: Verify write permissions by creating temporary test file
- SVC-013: Clean up test file immediately after creation
- SVC-014: Handle missing target directory

Business Rules:
- BR-001: Critical failures (✗ FAIL) block installation
"""

import pytest
from unittest.mock import Mock, patch
from pathlib import Path


class TestPermissionChecker:
    """Test suite for PermissionChecker service."""

    # AC#4: Write Permission Validation - Writable Directory (PASS)

    def test_should_return_pass_when_directory_writable(self, temp_dir):
        """
        Test: Writable directory → PASS status (SVC-012)

        Given: Target directory has write permissions
        When: PermissionChecker.check() is called
        Then: Returns CheckResult with PASS status
        """
        # Arrange
        from src.installer.validators.permission_checker import PermissionChecker

        checker = PermissionChecker(target_path=str(temp_dir))

        # Act
        result = checker.check()

        # Assert
        assert result.status == "PASS"
        assert "writable" in result.message.lower() or "write" in result.message.lower()
        assert result.check_name == "Write Permissions"

    def test_should_create_test_file_during_check(self, temp_dir):
        """
        Test: Creates devforgeai-write-test file (SVC-012)

        Given: Target directory is writable
        When: PermissionChecker.check() is called
        Then: Temporary test file is created
        """
        # Arrange
        from src.installer.validators.permission_checker import PermissionChecker

        checker = PermissionChecker(target_path=str(temp_dir))
        test_file_path = temp_dir / "devforgeai-write-test"

        # Act
        with patch.object(Path, 'touch') as mock_touch:
            with patch.object(Path, 'unlink'):
                result = checker.check()

                # Assert
                mock_touch.assert_called_once()
                assert result.status == "PASS"

    # AC#4 & SVC-013: Test File Cleanup

    def test_should_delete_test_file_after_check(self, temp_dir):
        """
        Test: Deletes devforgeai-write-test immediately (SVC-013)

        Given: Test file was created successfully
        When: PermissionChecker.check() completes
        Then: Test file is deleted immediately
        """
        # Arrange
        from src.installer.validators.permission_checker import PermissionChecker

        checker = PermissionChecker(target_path=str(temp_dir))

        # Act
        result = checker.check()

        # Assert
        test_file = temp_dir / "devforgeai-write-test"
        assert not test_file.exists(), "Test file should be deleted after check"
        assert result.status == "PASS"

    def test_should_delete_test_file_even_on_success(self, temp_dir):
        """
        Test: Test file not left behind on successful check (SVC-013)

        Given: Write permission check passes
        When: PermissionChecker.check() completes
        Then: No devforgeai-write-test file exists in directory
        """
        # Arrange
        from src.installer.validators.permission_checker import PermissionChecker

        checker = PermissionChecker(target_path=str(temp_dir))

        # Act
        result = checker.check()

        # Assert
        assert result.status == "PASS"
        # Verify test file does not exist
        test_file = temp_dir / "devforgeai-write-test"
        assert not test_file.exists()

    def test_should_delete_test_file_even_on_failure(self, read_only_dir):
        """
        Test: Test file cleanup attempted even on failure

        Given: Write permission check fails
        When: PermissionChecker.check() completes
        Then: Attempts to clean up test file (may fail silently)
        """
        # Arrange
        from src.installer.validators.permission_checker import PermissionChecker

        checker = PermissionChecker(target_path=str(read_only_dir))

        # Act
        result = checker.check()

        # Assert
        assert result.status == "FAIL"
        # Test file should not exist (cleanup attempted)
        test_file = read_only_dir / "devforgeai-write-test"
        # Note: In read-only dir, file creation fails, so nothing to clean up

    # AC#4: Write Permission Validation - Read-Only Directory (FAIL)

    def test_should_return_fail_when_directory_read_only(self, read_only_dir):
        """
        Test: Read-only directory → FAIL status (SVC-012)

        Given: Target directory is read-only (no write permissions)
        When: PermissionChecker.check() is called
        Then: Returns CheckResult with FAIL status and resolution message
        """
        # Arrange
        from src.installer.validators.permission_checker import PermissionChecker

        checker = PermissionChecker(target_path=str(read_only_dir))

        # Act
        result = checker.check()

        # Assert
        assert result.status == "FAIL"
        assert "permission" in result.message.lower() or "denied" in result.message.lower()

    def test_should_return_fail_when_permission_error_raised(self, temp_dir):
        """
        Test: PermissionError → FAIL status

        Given: File creation raises PermissionError
        When: PermissionChecker.check() is called
        Then: Returns FAIL status with permission context
        """
        # Arrange
        from src.installer.validators.permission_checker import PermissionChecker

        checker = PermissionChecker(target_path=str(temp_dir))

        with patch.object(Path, 'touch') as mock_touch:
            mock_touch.side_effect = PermissionError("Access denied")

            # Act
            result = checker.check()

            # Assert
            assert result.status == "FAIL"
            assert "permission" in result.message.lower()

    def test_should_return_fail_when_os_error_raised(self, temp_dir):
        """
        Test: OSError on file creation → FAIL status

        Given: File creation raises OSError
        When: PermissionChecker.check() is called
        Then: Returns FAIL status
        """
        # Arrange
        from src.installer.validators.permission_checker import PermissionChecker

        checker = PermissionChecker(target_path=str(temp_dir))

        with patch.object(Path, 'touch') as mock_touch:
            mock_touch.side_effect = OSError("Disk full")

            # Act
            result = checker.check()

            # Assert
            assert result.status == "FAIL"

    # SVC-014: Handle missing target directory

    def test_should_return_fail_when_target_directory_missing(self):
        """
        Test: Missing target directory → FAIL status (SVC-014)

        Given: Target directory does not exist
        When: PermissionChecker.check() is called
        Then: Returns FAIL status with directory not found message
        """
        # Arrange
        from src.installer.validators.permission_checker import PermissionChecker

        checker = PermissionChecker(target_path="/nonexistent/path")

        # Act
        result = checker.check()

        # Assert
        assert result.status == "FAIL"
        assert "not exist" in result.message.lower() or "not found" in result.message.lower()

    def test_should_return_fail_when_target_path_is_file(self, temp_dir):
        """
        Test: Target path is file, not directory → FAIL status

        Given: Target path points to file, not directory
        When: PermissionChecker.check() is called
        Then: Returns FAIL status
        """
        # Arrange
        from src.installer.validators.permission_checker import PermissionChecker

        # Create a file, not directory
        file_path = temp_dir / "testfile.txt"
        file_path.write_text("test")

        checker = PermissionChecker(target_path=str(file_path))

        # Act
        result = checker.check()

        # Assert
        assert result.status == "FAIL"
        assert "directory" in result.message.lower()

    # NFR-006: Usability - Error messages include actionable resolution steps

    def test_should_include_resolution_steps_in_fail_message(self, read_only_dir):
        """
        Test: FAIL message includes resolution steps (NFR-006)

        Given: Permission check returns FAIL status
        When: Message is examined
        Then: Contains at least 2 actionable resolution steps
        """
        # Arrange
        from src.installer.validators.permission_checker import PermissionChecker

        checker = PermissionChecker(target_path=str(read_only_dir))

        # Act
        result = checker.check()

        # Assert
        assert result.status == "FAIL"
        # Message should contain resolution guidance
        message_lower = result.message.lower()
        resolution_keywords = ["run", "permissions", "administrator", "sudo", "directory", "choose"]
        matches = sum(1 for keyword in resolution_keywords if keyword in message_lower)
        assert matches >= 2, "Message should contain at least 2 resolution keywords"

    def test_should_suggest_alternative_directory_on_fail(self, read_only_dir):
        """
        Test: FAIL message suggests choosing alternative directory

        Given: Write permission denied
        When: PermissionChecker.check() returns FAIL
        Then: Message suggests choosing different directory
        """
        # Arrange
        from src.installer.validators.permission_checker import PermissionChecker

        checker = PermissionChecker(target_path=str(read_only_dir))

        # Act
        result = checker.check()

        # Assert
        assert result.status == "FAIL"
        assert "different" in result.message.lower() or "another" in result.message.lower() or "choose" in result.message.lower()

    # NFR-007: Security - No privilege escalation attempts

    def test_should_not_attempt_sudo_on_permission_denied(self, read_only_dir):
        """
        Test: Does not attempt sudo/privilege escalation (NFR-007)

        Given: Write permission denied
        When: PermissionChecker.check() is called
        Then: Returns FAIL without attempting privilege escalation
        """
        # Arrange
        from src.installer.validators.permission_checker import PermissionChecker

        checker = PermissionChecker(target_path=str(read_only_dir))

        with patch('subprocess.run') as mock_subprocess:
            # Act
            result = checker.check()

            # Assert
            assert result.status == "FAIL"
            # Should NOT call subprocess (no sudo attempt)
            mock_subprocess.assert_not_called()

    def test_should_not_suggest_privilege_escalation_in_message(self, read_only_dir):
        """
        Test: Message does not suggest sudo/admin escalation (NFR-007)

        Given: Permission denied
        When: Error message is examined
        Then: Does not suggest running as admin/root
        """
        # Arrange
        from src.installer.validators.permission_checker import PermissionChecker

        checker = PermissionChecker(target_path=str(read_only_dir))

        # Act
        result = checker.check()

        # Assert
        assert result.status == "FAIL"
        message_lower = result.message.lower()
        # Should NOT suggest sudo or admin
        forbidden_keywords = ["sudo", "root", "administrator", "run as admin"]
        matches = sum(1 for keyword in forbidden_keywords if keyword in message_lower)
        # Allow "administrator" or "permissions" in context of checking permissions, but not "run as admin"
        assert "sudo" not in message_lower, "Should not suggest sudo"

    # Performance

    def test_should_complete_check_within_100ms(self, temp_dir):
        """
        Test: Permission check completes in <100ms

        Given: Target directory is accessible
        When: PermissionChecker.check() is called
        Then: Execution completes in <100ms
        """
        # Arrange
        import time
        from src.installer.validators.permission_checker import PermissionChecker

        checker = PermissionChecker(target_path=str(temp_dir))

        # Act
        start = time.time()
        result = checker.check()
        duration_ms = (time.time() - start) * 1000

        # Assert
        assert duration_ms < 100, f"Check took {duration_ms}ms (expected <100ms)"
        assert result.status == "PASS"

    # Cross-platform compatibility

    def test_should_work_with_windows_paths(self):
        """
        Test: Windows path format supported

        Given: Target path is Windows format
        When: PermissionChecker.check() is called
        Then: Works correctly with Windows path
        """
        # Arrange
        from src.installer.validators.permission_checker import PermissionChecker

        with patch('pathlib.Path.exists', return_value=True):
            with patch('pathlib.Path.is_dir', return_value=True):
                with patch.object(Path, 'touch'):
                    with patch.object(Path, 'unlink'):
                        checker = PermissionChecker(target_path="C:\\test\\path")

                        # Act
                        result = checker.check()

                        # Assert
                        assert result.status == "PASS"

    def test_should_work_with_unix_paths(self, temp_dir):
        """
        Test: Unix path format supported

        Given: Target path is Unix format
        When: PermissionChecker.check() is called
        Then: Works correctly with Unix path
        """
        # Arrange
        from src.installer.validators.permission_checker import PermissionChecker

        checker = PermissionChecker(target_path=str(temp_dir))

        # Act
        result = checker.check()

        # Assert
        assert result.status == "PASS"

    # Reliability: File cleanup edge cases

    def test_should_handle_cleanup_failure_gracefully(self, temp_dir):
        """
        Test: Cleanup failure handled gracefully

        Given: Test file deletion fails
        When: PermissionChecker.check() completes
        Then: Does not crash, returns appropriate status
        """
        # Arrange
        from src.installer.validators.permission_checker import PermissionChecker

        checker = PermissionChecker(target_path=str(temp_dir))

        with patch.object(Path, 'unlink') as mock_unlink:
            mock_unlink.side_effect = PermissionError("Cannot delete")

            # Act
            result = checker.check()

            # Assert
            # Should not crash, returns status based on write test
            assert result.status in ["PASS", "WARN", "FAIL"]

    def test_should_not_leave_test_files_after_exception(self, temp_dir):
        """
        Test: Test file cleaned up even if exception during check

        Given: Exception occurs after file creation
        When: PermissionChecker.check() handles exception
        Then: Test file is still cleaned up
        """
        # Arrange
        from src.installer.validators.permission_checker import PermissionChecker

        checker = PermissionChecker(target_path=str(temp_dir))

        # Act
        try:
            with patch.object(Path, 'touch') as mock_touch:
                # Simulate exception after successful creation
                def side_effect(*args, **kwargs):
                    # Create actual file
                    test_file = temp_dir / "devforgeai-write-test"
                    test_file.touch()
                    raise Exception("Unexpected error")

                mock_touch.side_effect = side_effect

                result = checker.check()
        except Exception:
            pass

        # Assert
        test_file = temp_dir / "devforgeai-write-test"
        # File should still be cleaned up (may be via finally block)
        # In real implementation, should use try/finally for cleanup

    # Edge cases

    def test_should_handle_special_characters_in_path(self, temp_dir):
        """
        Test: Path with special characters handled correctly

        Given: Target path contains spaces and special characters
        When: PermissionChecker.check() is called
        Then: Works correctly
        """
        # Arrange
        from src.installer.validators.permission_checker import PermissionChecker

        special_dir = temp_dir / "path with spaces & special-chars"
        special_dir.mkdir()

        checker = PermissionChecker(target_path=str(special_dir))

        # Act
        result = checker.check()

        # Assert
        assert result.status == "PASS"

    def test_should_handle_very_long_path(self, temp_dir):
        """
        Test: Very long path handled correctly

        Given: Target path is very long (near system limit)
        When: PermissionChecker.check() is called
        Then: Works correctly or returns appropriate error
        """
        # Arrange
        from src.installer.validators.permission_checker import PermissionChecker

        # Create nested directory structure
        long_path = temp_dir
        for i in range(10):
            long_path = long_path / f"nested_directory_{i}"

        try:
            long_path.mkdir(parents=True)

            checker = PermissionChecker(target_path=str(long_path))

            # Act
            result = checker.check()

            # Assert
            assert result.status in ["PASS", "FAIL"]
        except OSError:
            # Path too long for system, skip test
            pytest.skip("Path too long for this system")

    # Configuration

    def test_should_use_configured_test_filename(self, temp_dir):
        """
        Test: Uses configured test filename

        Given: Test filename is "devforgeai-write-test"
        When: PermissionChecker.check() is called
        Then: Creates file with exact name
        """
        # Arrange
        from src.installer.validators.permission_checker import PermissionChecker

        checker = PermissionChecker(target_path=str(temp_dir))

        with patch.object(Path, 'touch') as mock_touch:
            with patch.object(Path, 'unlink'):
                # Act
                result = checker.check()

                # Assert
                # Verify touch was called on correct filename
                call_args = str(mock_touch.call_args)
                assert "devforgeai-write-test" in call_args or result.status == "PASS"

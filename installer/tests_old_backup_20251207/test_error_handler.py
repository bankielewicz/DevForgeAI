"""
STORY-074: Unit tests for ErrorHandler service.

Tests error categorization, user-friendly message formatting, and resolution guidance.
All tests follow TDD Red phase - they should FAIL until implementation exists.

Coverage Target: 95%+
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path


class TestErrorCategorization:
    """Test error categorization into 5 defined types (AC#1)."""

    def test_missing_source_error_returns_exit_code_1(self):
        """
        Test: ErrorHandler categorizes MISSING_SOURCE errors with exit code 1.

        Given: The installer encounters a FileNotFoundError for source files
        When: ErrorHandler categorizes the error
        Then: Error is classified as MISSING_SOURCE with exit code 1
        """
        # Arrange
        from installer.error_handler import ErrorHandler
        handler = ErrorHandler()
        error = FileNotFoundError("src/.claude/ not found")

        # Act
        category = handler.categorize_error(error)

        # Assert
        assert category.name == "MISSING_SOURCE"
        assert category.exit_code == 1

    def test_permission_denied_error_returns_exit_code_2(self):
        """
        Test: ErrorHandler categorizes PERMISSION_DENIED errors with exit code 2.

        Given: The installer encounters PermissionError
        When: ErrorHandler categorizes the error
        Then: Error is classified as PERMISSION_DENIED with exit code 2
        """
        # Arrange
        from installer.error_handler import ErrorHandler
        handler = ErrorHandler()
        error = PermissionError("Cannot write to .claude/")

        # Act
        category = handler.categorize_error(error)

        # Assert
        assert category.name == "PERMISSION_DENIED"
        assert category.exit_code == 2

    def test_rollback_occurred_returns_exit_code_3(self):
        """
        Test: ErrorHandler categorizes ROLLBACK_OCCURRED with exit code 3.

        Given: An error occurs after partial file installation
        When: ErrorHandler triggers rollback
        Then: Error is classified as ROLLBACK_OCCURRED with exit code 3
        """
        # Arrange
        from installer.error_handler import ErrorHandler
        handler = ErrorHandler()
        error = Exception("Error during file copy")

        # Act
        category = handler.categorize_error(error, rollback_triggered=True)

        # Assert
        assert category.name == "ROLLBACK_OCCURRED"
        assert category.exit_code == 3

    def test_validation_failed_returns_exit_code_4(self):
        """
        Test: ErrorHandler categorizes VALIDATION_FAILED with exit code 4.

        Given: Installation completes but validation fails
        When: ErrorHandler categorizes the validation error
        Then: Error is classified as VALIDATION_FAILED with exit code 4
        """
        # Arrange
        from installer.error_handler import ErrorHandler
        handler = ErrorHandler()
        error = ValueError("Installation validation failed")

        # Act
        category = handler.categorize_error(error, validation_phase=True)

        # Assert
        assert category.name == "VALIDATION_FAILED"
        assert category.exit_code == 4

    def test_success_returns_exit_code_0(self):
        """
        Test: ErrorHandler returns SUCCESS exit code 0 when no error.

        Given: Installation completes successfully
        When: ErrorHandler processes completion
        Then: Returns exit code 0
        """
        # Arrange
        from installer.error_handler import ErrorHandler
        handler = ErrorHandler()

        # Act
        exit_code = handler.get_exit_code(error=None)

        # Assert
        assert exit_code == 0


class TestUserFriendlyMessages:
    """Test user-friendly error messages without stack traces (AC#2)."""

    def test_console_message_contains_no_stack_trace(self):
        """
        Test: Console error messages contain no stack trace keywords.

        Given: An error occurs during installation
        When: ErrorHandler formats the console message
        Then: Message contains no stack trace keywords (Traceback, at, line, function)
        """
        # Arrange
        from installer.error_handler import ErrorHandler
        handler = ErrorHandler()
        error = FileNotFoundError("src/.claude/ not found")

        # Act
        console_message = handler.format_console_message(error)

        # Assert
        stack_trace_keywords = ["Traceback", "at line", "function", "File \""]
        for keyword in stack_trace_keywords:
            assert keyword not in console_message, f"Stack trace keyword '{keyword}' found in console output"

    def test_console_message_contains_plain_english_description(self):
        """
        Test: Console message includes clear plain English description.

        Given: An error occurs during installation
        When: ErrorHandler formats the console message
        Then: Message contains user-friendly description (no jargon)
        """
        # Arrange
        from installer.error_handler import ErrorHandler
        handler = ErrorHandler()
        error = FileNotFoundError("src/.claude/ not found")

        # Act
        console_message = handler.format_console_message(error)

        # Assert
        assert "ERROR:" in console_message
        assert "Missing Source Files" in console_message
        assert len(console_message) > 50, "Message too short to be descriptive"

    def test_console_message_includes_log_file_reference(self):
        """
        Test: Console message includes reference to log file location.

        Given: An error occurs during installation
        When: ErrorHandler formats the console message
        Then: Message includes devforgeai/install.log reference
        """
        # Arrange
        from installer.error_handler import ErrorHandler
        handler = ErrorHandler()
        error = FileNotFoundError("src/.claude/ not found")

        # Act
        console_message = handler.format_console_message(error)

        # Assert
        assert "devforgeai/install.log" in console_message

    def test_console_message_includes_1_to_3_resolution_steps(self):
        """
        Test: Console message includes 1-3 actionable resolution steps.

        Given: An error occurs during installation
        When: ErrorHandler formats the console message
        Then: Message includes between 1 and 3 resolution steps
        """
        # Arrange
        from installer.error_handler import ErrorHandler
        handler = ErrorHandler()
        error = FileNotFoundError("src/.claude/ not found")

        # Act
        console_message = handler.format_console_message(error)

        # Assert
        # Count numbered steps (1., 2., 3.)
        step_count = sum(1 for line in console_message.split('\n') if line.strip().startswith(('1.', '2.', '3.')))
        assert 1 <= step_count <= 3, f"Expected 1-3 resolution steps, found {step_count}"


class TestResolutionGuidance:
    """Test resolution guidance for each error category (AC#3)."""

    def test_missing_source_has_specific_resolution_steps(self):
        """
        Test: MISSING_SOURCE error provides specific resolution guidance.

        Given: A MISSING_SOURCE error occurs
        When: ErrorHandler formats resolution guidance
        Then: Guidance includes "Verify .claude/ directory exists in source"
        """
        # Arrange
        from installer.error_handler import ErrorHandler
        handler = ErrorHandler()
        error = FileNotFoundError("src/.claude/ not found")

        # Act
        resolution_steps = handler.get_resolution_steps(error)

        # Assert
        assert any("Verify .claude/ directory exists" in step for step in resolution_steps)

    def test_permission_denied_has_specific_resolution_steps(self):
        """
        Test: PERMISSION_DENIED error provides specific resolution guidance.

        Given: A PERMISSION_DENIED error occurs
        When: ErrorHandler formats resolution guidance
        Then: Guidance includes "Run with sudo OR change ownership"
        """
        # Arrange
        from installer.error_handler import ErrorHandler
        handler = ErrorHandler()
        error = PermissionError("Cannot write to .claude/")

        # Act
        resolution_steps = handler.get_resolution_steps(error)

        # Assert
        assert any("sudo" in step or "ownership" in step for step in resolution_steps)

    def test_validation_failed_has_specific_resolution_steps(self):
        """
        Test: VALIDATION_FAILED error provides specific resolution guidance.

        Given: A VALIDATION_FAILED error occurs
        When: ErrorHandler formats resolution guidance
        Then: Guidance includes "Check log file for details, verify source integrity"
        """
        # Arrange
        from installer.error_handler import ErrorHandler
        handler = ErrorHandler()
        error = ValueError("Installation validation failed")

        # Act
        resolution_steps = handler.get_resolution_steps(error)

        # Assert
        assert any("Check log file" in step for step in resolution_steps)
        assert any("source integrity" in step for step in resolution_steps)

    def test_resolution_steps_limited_to_3_maximum(self):
        """
        Test: Resolution steps limited to maximum of 3 (BR-005).

        Given: ErrorHandler generates resolution steps
        When: Steps are formatted
        Then: No error has more than 3 resolution steps
        """
        # Arrange
        from installer.error_handler import ErrorHandler
        handler = ErrorHandler()
        error = PermissionError("Cannot write to .claude/")

        # Act
        resolution_steps = handler.get_resolution_steps(error)

        # Assert
        assert len(resolution_steps) <= 3, f"Expected ≤3 resolution steps, found {len(resolution_steps)}"

    def test_resolution_steps_under_200_chars_each(self):
        """
        Test: Each resolution step is under 200 characters.

        Given: ErrorHandler generates resolution steps
        When: Steps are formatted
        Then: Each step is ≤200 characters
        """
        # Arrange
        from installer.error_handler import ErrorHandler
        handler = ErrorHandler()
        error = FileNotFoundError("src/.claude/ not found")

        # Act
        resolution_steps = handler.get_resolution_steps(error)

        # Assert
        for i, step in enumerate(resolution_steps):
            assert len(step) <= 200, f"Step {i+1} exceeds 200 chars: {len(step)} chars"


class TestErrorHandlerDependencies:
    """Test ErrorHandler integration with BackupService, RollbackService, InstallLogger."""

    def test_error_handler_triggers_rollback_service_on_error(self):
        """
        Test: ErrorHandler triggers RollbackService on partial installation failure (AC#4).

        Given: An error occurs after file copy phase
        When: ErrorHandler processes the error
        Then: RollbackService.rollback() is called
        """
        # Arrange
        from installer.error_handler import ErrorHandler
        mock_rollback_service = Mock()
        handler = ErrorHandler(rollback_service=mock_rollback_service)
        error = Exception("Error during file copy")

        # Act
        handler.handle_error(error, phase="file_copy")

        # Assert
        mock_rollback_service.rollback.assert_called_once()

    def test_error_handler_logs_to_install_logger(self):
        """
        Test: ErrorHandler logs detailed error to InstallLogger (AC#5).

        Given: An error occurs during installation
        When: ErrorHandler processes the error
        Then: InstallLogger.log_error() is called with full details
        """
        # Arrange
        from installer.error_handler import ErrorHandler
        mock_logger = Mock()
        handler = ErrorHandler(logger=mock_logger)
        error = FileNotFoundError("src/.claude/ not found")

        # Act
        handler.handle_error(error)

        # Assert
        mock_logger.log_error.assert_called_once()
        call_args = mock_logger.log_error.call_args
        assert "MISSING_SOURCE" in str(call_args)

    def test_error_handler_uses_backup_service_for_context(self):
        """
        Test: ErrorHandler queries BackupService for backup location.

        Given: An error occurs and rollback is needed
        When: ErrorHandler formats error message
        Then: BackupService is queried for backup directory path
        """
        # Arrange
        from installer.error_handler import ErrorHandler
        mock_backup_service = Mock()
        mock_backup_service.get_latest_backup.return_value = Path("/backups/install-backup-20251203")
        handler = ErrorHandler(backup_service=mock_backup_service)
        error = Exception("Error during file copy")

        # Act
        console_message = handler.format_console_message(error, include_rollback_info=True)

        # Assert
        mock_backup_service.get_latest_backup.assert_called_once()
        assert "install-backup-20251203" in console_message


class TestExitCodeHandling:
    """Test exit code standardization (AC#6)."""

    def test_get_exit_code_returns_correct_code_for_each_category(self):
        """
        Test: ErrorHandler.get_exit_code() returns correct code per error category.

        Given: ErrorHandler categorizes an error
        When: get_exit_code() is called
        Then: Returns correct exit code (0, 1, 2, 3, 4)
        """
        # Arrange
        from installer.error_handler import ErrorHandler
        handler = ErrorHandler()

        test_cases = [
            (None, 0),  # Success
            (FileNotFoundError("missing"), 1),  # MISSING_SOURCE
            (PermissionError("denied"), 2),  # PERMISSION_DENIED
            (ValueError("validation"), 4),  # VALIDATION_FAILED
        ]

        # Act & Assert
        for error, expected_code in test_cases:
            actual_code = handler.get_exit_code(error)
            assert actual_code == expected_code, f"Expected exit code {expected_code}, got {actual_code}"

    def test_rollback_error_overrides_original_exit_code(self):
        """
        Test: ROLLBACK_OCCURRED (exit code 3) overrides original error exit code.

        Given: An error occurs and rollback is triggered
        When: ErrorHandler determines exit code
        Then: Returns exit code 3 (ROLLBACK_OCCURRED) regardless of original error
        """
        # Arrange
        from installer.error_handler import ErrorHandler
        handler = ErrorHandler()
        original_error = FileNotFoundError("missing")  # Would be exit code 1

        # Act
        exit_code = handler.get_exit_code(original_error, rollback_triggered=True)

        # Assert
        assert exit_code == 3, "Rollback should override original exit code to 3"


class TestPathSanitization:
    """Test path sanitization in console output (NFR-007)."""

    def test_console_message_sanitizes_usernames_in_paths(self):
        """
        Test: Console output replaces /home/username with /home/$USER.

        Given: An error message contains path with username
        When: ErrorHandler formats console message
        Then: Username is replaced with $USER placeholder
        """
        # Arrange
        from installer.error_handler import ErrorHandler
        handler = ErrorHandler()
        error = FileNotFoundError("/home/alice/.claude/ not found")

        # Act
        console_message = handler.format_console_message(error)

        # Assert
        assert "/home/alice" not in console_message
        assert "/home/$USER" in console_message or "$HOME" in console_message

    def test_console_message_does_not_leak_sensitive_paths(self):
        """
        Test: Console message avoids exposing sensitive file paths.

        Given: An error occurs with sensitive path information
        When: ErrorHandler formats console message
        Then: Message uses generic path descriptions
        """
        # Arrange
        from installer.error_handler import ErrorHandler
        handler = ErrorHandler()
        error = PermissionError("/home/alice/.ssh/config: Permission denied")

        # Act
        console_message = handler.format_console_message(error)

        # Assert
        assert ".ssh/config" not in console_message or "sensitive" in console_message.lower()


class TestEdgeCases:
    """Test edge case error scenarios."""

    def test_concurrent_installation_error_detected(self):
        """
        Test: ErrorHandler detects concurrent installation via lock file.

        Given: A lock file exists from another installation
        When: ErrorHandler checks for concurrent installation
        Then: Raises appropriate error with guidance
        """
        # Arrange
        from installer.error_handler import ErrorHandler
        handler = ErrorHandler()

        # Act
        with pytest.raises(RuntimeError) as exc_info:
            handler.check_concurrent_installation(lock_file_exists=True)

        # Assert
        assert "concurrent" in str(exc_info.value).lower()

    def test_error_during_rollback_logged_but_does_not_crash(self):
        """
        Test: Error during rollback is logged but doesn't crash installer.

        Given: Rollback encounters an error (backup missing)
        When: ErrorHandler handles rollback error
        Then: Error is logged, manual intervention message displayed, process continues
        """
        # Arrange
        from installer.error_handler import ErrorHandler
        mock_logger = Mock()
        mock_rollback_service = Mock()
        mock_rollback_service.rollback.side_effect = FileNotFoundError("Backup not found")
        handler = ErrorHandler(rollback_service=mock_rollback_service, logger=mock_logger)

        # Act
        result = handler.handle_error(Exception("Original error"), phase="file_copy")

        # Assert
        assert result.exit_code == 3  # ROLLBACK_OCCURRED
        mock_logger.log_error.assert_called()
        assert any("manual intervention" in str(call) for call in mock_logger.log_error.call_args_list)

    def test_sigint_handled_gracefully_triggers_rollback(self):
        """
        Test: SIGINT (Ctrl+C) triggers graceful rollback.

        Given: User presses Ctrl+C during installation
        When: ErrorHandler catches KeyboardInterrupt
        Then: Rollback is triggered and user sees "Installation cancelled" message
        """
        # Arrange
        from installer.error_handler import ErrorHandler
        mock_rollback_service = Mock()
        handler = ErrorHandler(rollback_service=mock_rollback_service)
        error = KeyboardInterrupt()

        # Act
        result = handler.handle_error(error)

        # Assert
        mock_rollback_service.rollback.assert_called_once()
        assert result.exit_code == 3
        assert "cancelled" in result.console_message.lower()

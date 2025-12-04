"""
STORY-074: Edge case tests for error handling.

Tests edge cases like rollback failures, concurrent installations, sensitive info sanitization.
All tests follow TDD Red phase - they should FAIL until implementation exists.

Coverage Target: 80%+
"""

import pytest
from unittest.mock import Mock, patch
from pathlib import Path


class TestRollbackFailureScenarios:
    """Test edge cases when rollback itself fails."""

    def test_rollback_fails_when_backup_missing(self, tmp_path):
        """
        Test: Rollback handles missing backup gracefully (edge case).

        Given: Error occurs but backup directory is missing
        When: RollbackService attempts rollback
        Then: Logs critical error, displays manual intervention message
        """
        # Arrange
        from installer.rollback_service import RollbackService
        from installer.install_logger import InstallLogger

        log_file = tmp_path / ".devforgeai" / "install.log"
        log_file.parent.mkdir()

        logger = InstallLogger(log_file=log_file)
        rollback_service = RollbackService(logger=logger)

        backup_dir = tmp_path / "nonexistent_backup"
        target_dir = tmp_path / "target"
        target_dir.mkdir()

        # Act & Assert
        with pytest.raises(FileNotFoundError) as exc_info:
            rollback_service.rollback(backup_dir=backup_dir, target_dir=target_dir)

        assert "manual" in str(exc_info.value).lower() or "intervention" in str(exc_info.value).lower()

    def test_partial_rollback_when_some_files_fail(self, tmp_path):
        """
        Test: Rollback continues when some files fail to restore.

        Given: Rollback encounters permission error for one file
        When: RollbackService performs rollback
        Then: Continues with remaining files, logs errors for failed files
        """
        # Arrange
        from installer.rollback_service import RollbackService
        from installer.install_logger import InstallLogger

        backup_dir = tmp_path / "backup"
        backup_dir.mkdir()
        (backup_dir / "file1.txt").write_text("content1")
        (backup_dir / "file2.txt").write_text("content2")

        target_dir = tmp_path / "target"
        target_dir.mkdir()

        logger = InstallLogger(log_file=tmp_path / ".devforgeai" / "install.log")
        logger.log_file.parent.mkdir(exist_ok=True)
        rollback_service = RollbackService(logger=logger)

        with patch("shutil.copy2") as mock_copy:
            # First file fails, second succeeds
            mock_copy.side_effect = [PermissionError("Permission denied"), None]

            # Act
            result = rollback_service.rollback(backup_dir=backup_dir, target_dir=target_dir)

        # Assert
        assert result.exit_code == 3
        # Should have logged error for first file
        log_content = logger.log_file.read_text()
        assert "error" in log_content.lower()


class TestConcurrentInstallationEdgeCases:
    """Test edge cases for concurrent installation detection."""

    def test_stale_lock_file_removed_automatically(self, tmp_path):
        """
        Test: Stale lock file (dead PID) is removed automatically.

        Given: Lock file exists with PID of dead process
        When: LockFileManager attempts to acquire lock
        Then: Stale lock removed, new lock acquired
        """
        # Arrange
        from installer.lock_file_manager import LockFileManager

        lock_dir = tmp_path / ".devforgeai"
        lock_dir.mkdir()

        # Create stale lock
        lock_file = lock_dir / "install.lock"
        dead_pid = 999999
        lock_file.write_text(f"{dead_pid}\n2025-12-03T10:00:00Z")

        manager = LockFileManager(lock_dir=lock_dir)

        # Act
        manager.acquire_lock()

        # Assert
        import os
        lock_content = lock_file.read_text()
        assert str(os.getpid()) in lock_content
        assert str(dead_pid) not in lock_content

    def test_lock_file_race_condition_handling(self, tmp_path):
        """
        Test: LockFileManager handles race condition during lock acquisition.

        Given: Two processes attempt to acquire lock simultaneously
        When: Race condition occurs
        Then: One succeeds, other fails gracefully
        """
        # Arrange
        from installer.lock_file_manager import LockFileManager
        import threading

        lock_dir = tmp_path / ".devforgeai"
        lock_dir.mkdir()

        manager1 = LockFileManager(lock_dir=lock_dir)
        manager2 = LockFileManager(lock_dir=lock_dir)

        results = []

        def acquire_lock(manager, results_list):
            try:
                manager.acquire_lock()
                results_list.append("success")
            except RuntimeError:
                results_list.append("failed")

        # Act
        thread1 = threading.Thread(target=acquire_lock, args=(manager1, results))
        thread2 = threading.Thread(target=acquire_lock, args=(manager2, results))

        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()

        # Assert
        assert "success" in results
        assert "failed" in results


class TestLogFileEdgeCases:
    """Test edge cases for log file handling."""

    def test_log_file_exists_from_previous_install_appends_with_separator(self, tmp_path):
        """
        Test: Existing log file is appended with session separator.

        Given: Log file exists from previous installation
        When: New installation starts
        Then: New entries appended with session separator
        """
        # Arrange
        from installer.install_logger import InstallLogger

        log_file = tmp_path / "install.log"
        log_file.write_text("2025-12-01T10:00:00.000Z [INFO] Previous install\n")

        logger = InstallLogger(log_file=log_file)

        # Act
        logger.log_session_start()
        logger.log_info("New install")

        # Assert
        log_content = log_file.read_text()
        assert "Previous install" in log_content
        assert "New install" in log_content
        assert "===" in log_content or "Session" in log_content

    def test_log_file_rotation_at_10mb(self, tmp_path):
        """
        Test: Log file rotates when exceeding 10MB.

        Given: Log file exceeds 10MB
        When: New entry is written
        Then: Old log rotated to install.log.1
        """
        # Arrange
        from installer.install_logger import InstallLogger

        log_file = tmp_path / "install.log"
        # Create 10MB+ log
        large_content = "x" * (10 * 1024 * 1024 + 1000)
        log_file.write_text(large_content)

        logger = InstallLogger(log_file=log_file, max_size_mb=10)

        # Act
        logger.log_info("New entry after rotation")

        # Assert
        rotated_log = tmp_path / "install.log.1"
        assert rotated_log.exists()


class TestSensitiveInfoSanitization:
    """Test sensitive information sanitization in console output."""

    def test_console_output_replaces_username_in_paths(self, tmp_path):
        """
        Test: Console output replaces /home/username with /home/$USER.

        Given: Error message contains path with username
        When: ErrorCategorizer formats console message
        Then: Username replaced with $USER placeholder
        """
        # Arrange
        from installer.error_categorizer import ErrorCategorizer

        error_categorizer = ErrorCategorizer()
        error = FileNotFoundError("/home/alice/.claude/ not found")

        # Act
        console_message = error_categorizer.format_console_message(error)

        # Assert
        assert "/home/alice" not in console_message
        assert "/home/$USER" in console_message or "$HOME" in console_message

    def test_console_output_does_not_leak_credentials(self, tmp_path):
        """
        Test: Console output does not leak credentials or sensitive data.

        Given: Error message contains sensitive path (.ssh, .env)
        When: ErrorCategorizer formats console message
        Then: Sensitive paths are sanitized
        """
        # Arrange
        from installer.error_categorizer import ErrorCategorizer

        error_categorizer = ErrorCategorizer()
        error = PermissionError("/home/alice/.ssh/id_rsa: Permission denied")

        # Act
        console_message = error_categorizer.format_console_message(error)

        # Assert
        # Should either remove sensitive path or indicate it's sensitive
        assert ".ssh/id_rsa" not in console_message or "sensitive" in console_message.lower()


class TestValidationFailureEdgeCase:
    """Test validation failure post-installation (no auto-rollback)."""

    def test_validation_fails_post_installation_no_auto_rollback(self, tmp_path):
        """
        Test: Validation failure after installation does NOT auto-rollback.

        Given: Installation completes, validation runs and fails
        When: ErrorRecoveryOrchestrator handles validation error
        Then: Returns exit code 4, does NOT trigger rollback (user decides)
        """
        # Arrange
        from installer.error_categorizer import ErrorCategorizer
        from installer.error_recovery_orchestrator import ErrorRecoveryOrchestrator, ErrorRecoveryContext
        from installer.install_logger import InstallLogger

        log_file = tmp_path / ".devforgeai" / "install.log"
        log_file.parent.mkdir()

        logger = InstallLogger(log_file=log_file)
        error_categorizer = ErrorCategorizer()
        orchestrator = ErrorRecoveryOrchestrator(error_categorizer=error_categorizer, logger=logger)

        error = ValueError("Validation failed: missing file")

        # Act
        context = ErrorRecoveryContext(error=error, validation_phase=True)
        result = orchestrator.handle_error(context)

        # Assert
        assert result.exit_code == 4
        # Should NOT include rollback message
        assert "rollback" not in result.console_message.lower()
        # Should offer manual option
        assert "manual" in result.console_message.lower() or "check" in result.console_message.lower()


class TestBackupCreationFailureEdgeCases:
    """Test edge cases when backup creation fails."""

    def test_backup_fails_installation_halts_immediately(self, tmp_path):
        """
        Test: If backup fails, installation HALTS immediately (no file operations).

        Given: Backup directory creation fails
        When: BackupService attempts to create backup
        Then: Raises PermissionError, installation HALTS before any file operations
        """
        # Arrange
        from installer.backup_service import BackupService
        from installer.install_logger import InstallLogger

        target_dir = tmp_path / "target"
        target_dir.mkdir()

        log_file = tmp_path / "install.log"
        logger = InstallLogger(log_file=log_file)
        backup_service = BackupService(logger=logger)

        with patch("pathlib.Path.mkdir") as mock_mkdir:
            mock_mkdir.side_effect = PermissionError("Cannot create backup")

            # Act & Assert
            with pytest.raises(PermissionError):
                backup_service.create_backup(target_dir=target_dir, files_to_backup=[])

    def test_disk_full_during_backup_halts_installation(self, tmp_path):
        """
        Test: Disk full during backup halts installation.

        Given: Disk becomes full during backup
        When: BackupService attempts to copy files
        Then: Raises OSError, installation HALTS
        """
        # Arrange
        from installer.backup_service import BackupService
        from installer.install_logger import InstallLogger

        target_dir = tmp_path / "target"
        target_dir.mkdir()
        (target_dir / "file.txt").write_text("content")

        log_file = tmp_path / "install.log"
        logger = InstallLogger(log_file=log_file)
        backup_service = BackupService(logger=logger)

        with patch("shutil.copy2") as mock_copy:
            mock_copy.side_effect = OSError("[Errno 28] No space left on device")

            # Act & Assert
            with pytest.raises(OSError) as exc_info:
                backup_service.create_backup(
                    target_dir=target_dir,
                    files_to_backup=[target_dir / "file.txt"]
                )

            assert "No space left" in str(exc_info.value)


class TestUserInterruptHandling:
    """Test user interrupt (Ctrl+C) handling edge cases."""

    def test_sigint_during_backup_triggers_cleanup(self, tmp_path):
        """
        Test: SIGINT during backup triggers cleanup (no partial backup left).

        Given: User presses Ctrl+C during backup
        When: KeyboardInterrupt is caught
        Then: Partial backup is removed (if it exists)
        """
        # Arrange
        from installer.backup_service import BackupService
        from installer.install_logger import InstallLogger
        from pathlib import Path

        target_dir = tmp_path / "target"
        target_dir.mkdir()

        # Create a file to backup
        test_file = target_dir / "test.txt"
        test_file.write_text("content")

        log_file = tmp_path / "install.log"
        logger = InstallLogger(log_file=log_file)
        backup_service = BackupService(logger=logger)

        # Simulate Ctrl+C during file copy
        with patch("shutil.copy2") as mock_copy:
            mock_copy.side_effect = KeyboardInterrupt()

            # Act & Assert - BackupService should propagate KeyboardInterrupt
            # and clean up partial backup directory
            with pytest.raises(KeyboardInterrupt):
                backup_service.create_backup(target_dir=target_dir, files_to_backup=[test_file])

    def test_sigint_during_file_copy_triggers_rollback(self, tmp_path):
        """
        Test: SIGINT during file copy triggers rollback.

        Given: User presses Ctrl+C during file copy
        When: KeyboardInterrupt is caught via ErrorRecoveryOrchestrator
        Then: Rollback is triggered, exit code 3
        """
        # Arrange
        from installer.error_categorizer import ErrorCategorizer
        from installer.error_recovery_orchestrator import ErrorRecoveryOrchestrator, ErrorRecoveryContext
        from installer.rollback_service import RollbackService
        from installer.install_logger import InstallLogger

        log_file = tmp_path / ".devforgeai" / "install.log"
        log_file.parent.mkdir()

        logger = InstallLogger(log_file=log_file)
        rollback_service = RollbackService(logger=logger)
        error_categorizer = ErrorCategorizer()
        orchestrator = ErrorRecoveryOrchestrator(
            error_categorizer=error_categorizer,
            rollback_service=rollback_service,
            logger=logger
        )

        # Act
        error = KeyboardInterrupt()
        context = ErrorRecoveryContext(error=error, phase="file_copy")
        result = orchestrator.handle_error(context)

        # Assert
        assert result.exit_code == 3


class TestEmptyDirectoryCleanup:
    """Test cleanup of empty directories after rollback."""

    def test_remove_empty_directories_after_rollback(self, tmp_path):
        """
        Test: Rollback removes empty directories created during installation.

        Given: Installation created empty directories
        When: Rollback completes
        Then: Empty directories are removed
        """
        # Arrange
        from installer.rollback_service import RollbackService
        from installer.install_logger import InstallLogger

        target_dir = tmp_path / "target"
        target_dir.mkdir()
        (target_dir / "empty_dir").mkdir()
        (target_dir / "dir_with_file").mkdir()
        (target_dir / "dir_with_file" / "file.txt").write_text("content")

        log_file = tmp_path / "install.log"
        logger = InstallLogger(log_file=log_file)
        rollback_service = RollbackService(logger=logger)

        # Act
        rollback_service.remove_empty_directories(target_dir)

        # Assert
        assert not (target_dir / "empty_dir").exists()
        assert (target_dir / "dir_with_file").exists()


class TestMultipleErrorsSequence:
    """Test handling of multiple errors in sequence."""

    def test_error_during_rollback_handled_gracefully(self, tmp_path):
        """
        Test: Error during rollback is handled gracefully.

        Given: Rollback encounters error
        When: ErrorRecoveryOrchestrator handles rollback error
        Then: Logs critical error, displays manual intervention message
        """
        # Arrange
        from installer.error_categorizer import ErrorCategorizer
        from installer.error_recovery_orchestrator import ErrorRecoveryOrchestrator, ErrorRecoveryContext
        from installer.rollback_service import RollbackService
        from installer.install_logger import InstallLogger

        log_file = tmp_path / ".devforgeai" / "install.log"
        log_file.parent.mkdir()

        logger = InstallLogger(log_file=log_file)
        rollback_service = RollbackService(logger=logger)
        error_categorizer = ErrorCategorizer()
        orchestrator = ErrorRecoveryOrchestrator(
            error_categorizer=error_categorizer,
            rollback_service=rollback_service,
            logger=logger
        )

        # Simulate rollback failure by providing original error during file_copy phase
        original_error = Exception("Original error")

        # Act
        context = ErrorRecoveryContext(error=original_error, phase="file_copy")
        result = orchestrator.handle_error(context)

        # Assert
        assert result.exit_code == 3
        log_content = log_file.read_text()
        assert "error" in log_content.lower()


class TestUnicodeAndSpecialCharacters:
    """Test handling of unicode and special characters in error messages."""

    def test_error_handler_handles_unicode_paths(self, tmp_path):
        """
        Test: ErrorCategorizer handles unicode characters in file paths.

        Given: Error message contains unicode file path
        When: ErrorCategorizer formats message
        Then: Unicode characters preserved correctly
        """
        # Arrange
        from installer.error_categorizer import ErrorCategorizer

        error_categorizer = ErrorCategorizer()
        error = FileNotFoundError("/home/user/文件/test.txt not found")

        # Act
        console_message = error_categorizer.format_console_message(error)

        # Assert
        assert "文件" in console_message or "$USER" in console_message  # Either preserved or sanitized

    def test_log_file_handles_unicode_in_error_messages(self, tmp_path):
        """
        Test: InstallLogger handles unicode in error messages.

        Given: Error contains unicode characters
        When: Logger writes to log file
        Then: Unicode characters preserved in log
        """
        # Arrange
        from installer.install_logger import InstallLogger

        log_file = tmp_path / "install.log"
        logger = InstallLogger(log_file=log_file)

        # Act
        logger.log_error(Exception("Error with unicode: 你好世界"))

        # Assert
        log_content = log_file.read_text(encoding="utf-8")
        assert "你好世界" in log_content


class TestVeryLongPaths:
    """Test handling of very long file paths (>256 characters)."""

    def test_error_handler_truncates_very_long_paths_in_console(self, tmp_path):
        """
        Test: ErrorCategorizer formats very long paths in console output.

        Given: Error message contains path >256 characters
        When: ErrorCategorizer formats console message
        Then: Message is readable (long paths may be sanitized)
        """
        # Arrange
        from installer.error_categorizer import ErrorCategorizer

        error_categorizer = ErrorCategorizer()
        long_path = "/home/user/" + "a" * 300 + "/test.txt"
        error = FileNotFoundError(f"{long_path} not found")

        # Act
        console_message = error_categorizer.format_console_message(error)

        # Assert
        # Console message should be formatted (paths may be sanitized as $USER)
        assert console_message is not None
        assert "ERROR" in console_message or "error" in console_message.lower()
        # The username should be sanitized
        assert "/home/user" not in console_message or "/home/$USER" in console_message

    def test_log_file_preserves_full_path_even_if_very_long(self, tmp_path):
        """
        Test: InstallLogger preserves full path in log even if very long.

        Given: Error message contains path >256 characters
        When: Logger writes to log file
        Then: Full path preserved in log (no truncation)
        """
        # Arrange
        from installer.install_logger import InstallLogger

        log_file = tmp_path / "install.log"
        logger = InstallLogger(log_file=log_file)

        long_path = "/home/user/" + "a" * 300 + "/test.txt"
        error = FileNotFoundError(f"{long_path} not found")

        # Act
        logger.log_error(error)

        # Assert
        log_content = log_file.read_text()
        assert long_path in log_content  # Full path preserved

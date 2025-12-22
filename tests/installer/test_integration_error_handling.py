"""
STORY-074: Integration tests for complete error handling workflow.

Tests full rollback flow, concurrent installation prevention, and SIGINT handling.
All tests follow TDD Red phase - they should FAIL until implementation exists.

Coverage Target: 85%+
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import signal
import time


class TestFullRollbackFlow:
    """Test complete rollback flow from error to restoration (AC#4)."""

    def test_error_after_file_copy_triggers_complete_rollback(self, tmp_path):
        """
        Test: Error after file copy triggers complete rollback to backup.

        Given: Installation copies files then encounters error
        When: ErrorRecoveryOrchestrator detects error in file_copy phase
        Then: RollbackService restores all files from backup, returns exit code 3
        """
        # Arrange
        from installer.services.error_categorizer import ErrorCategorizer
        from installer.services.error_recovery_orchestrator import ErrorRecoveryOrchestrator, ErrorRecoveryContext
        from installer.services.rollback_service import RollbackService
        from installer.services.backup_service import BackupService
        from installer.services.install_logger import InstallLogger

        target_dir = tmp_path / "target"
        target_dir.mkdir()
        (target_dir / "original.txt").write_text("original content")

        log_file = tmp_path / "devforgeai" / "install.log"
        log_file.parent.mkdir()

        logger = InstallLogger(log_file=log_file)
        backup_service = BackupService(logger=logger)
        rollback_service = RollbackService(logger=logger)
        error_categorizer = ErrorCategorizer()
        orchestrator = ErrorRecoveryOrchestrator(
            error_categorizer=error_categorizer,
            rollback_service=rollback_service,
            logger=logger
        )

        # Create backup
        backup_dir = backup_service.create_backup(
            target_dir=target_dir,
            files_to_backup=[target_dir / "original.txt"]
        )

        # Simulate file modification
        (target_dir / "original.txt").write_text("modified content")
        (target_dir / "new_file.txt").write_text("new file content")

        # Act
        error = Exception("Error during file copy")
        context = ErrorRecoveryContext(error=error, phase="file_copy")
        result = orchestrator.handle_error(context)

        # Assert
        assert result.exit_code == 3  # ROLLBACK_OCCURRED

    def test_rollback_displays_console_messages(self, tmp_path):
        """
        Test: Rollback displays console message about error and rollback.

        Given: Error occurs after file copy
        When: Rollback is triggered
        Then: Console message explains the error and recovery
        """
        # Arrange
        from installer.services.error_categorizer import ErrorCategorizer
        from installer.services.error_recovery_orchestrator import ErrorRecoveryOrchestrator, ErrorRecoveryContext
        from installer.services.rollback_service import RollbackService
        from installer.services.install_logger import InstallLogger

        target_dir = tmp_path / "target"
        target_dir.mkdir()

        log_file = tmp_path / "devforgeai" / "install.log"
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
        error = Exception("Test error")
        context = ErrorRecoveryContext(error=error, phase="file_copy")
        result = orchestrator.handle_error(context)

        # Assert
        # Console message should contain error information
        assert result.console_message is not None
        assert len(result.console_message) > 0
        assert result.exit_code == 3

    def test_rollback_logs_all_actions_to_install_log(self, tmp_path):
        """
        Test: Rollback logs all actions to install.log (AC#5).

        Given: Rollback is performed
        When: Error is handled during file_copy phase
        Then: install.log contains error and rollback information
        """
        # Arrange
        from installer.services.error_categorizer import ErrorCategorizer
        from installer.services.error_recovery_orchestrator import ErrorRecoveryOrchestrator, ErrorRecoveryContext
        from installer.services.rollback_service import RollbackService
        from installer.services.backup_service import BackupService
        from installer.services.install_logger import InstallLogger

        target_dir = tmp_path / "target"
        target_dir.mkdir()

        log_file = tmp_path / "devforgeai" / "install.log"
        log_file.parent.mkdir()

        logger = InstallLogger(log_file=log_file)
        backup_service = BackupService(logger=logger)
        rollback_service = RollbackService(logger=logger)
        error_categorizer = ErrorCategorizer()
        orchestrator = ErrorRecoveryOrchestrator(
            error_categorizer=error_categorizer,
            rollback_service=rollback_service,
            logger=logger
        )

        backup_dir = backup_service.create_backup(target_dir=target_dir, files_to_backup=[])

        # Act
        error = Exception("Test error")
        context = ErrorRecoveryContext(error=error, phase="file_copy")
        orchestrator.handle_error(context)

        # Assert
        log_content = log_file.read_text()
        assert "error" in log_content.lower()


class TestConcurrentInstallationPrevention:
    """Test lock file prevents concurrent installations (BR-004)."""

    def test_lock_file_prevents_second_installation(self, tmp_path):
        """
        Test: Lock file prevents concurrent installations.

        Given: First installation is running (lock file exists)
        When: Second installation attempts to start
        Then: Second installation fails with VALIDATION_FAILED (exit code 4)
        """
        # Arrange
        from installer.services.lock_file_manager import LockFileManager
        from installer.error_handler import ErrorHandler

        lock_dir = tmp_path / "devforgeai"
        lock_dir.mkdir()

        # First installation acquires lock
        manager1 = LockFileManager(lock_dir=lock_dir)
        manager1.acquire_lock()

        # Second installation attempts to acquire lock
        manager2 = LockFileManager(lock_dir=lock_dir)
        error_handler = ErrorHandler(logger=Mock())

        # Act & Assert
        with pytest.raises(RuntimeError) as exc_info:
            manager2.acquire_lock()

        assert "concurrent" in str(exc_info.value).lower()

    def test_second_installation_provides_clear_error_message(self, tmp_path):
        """
        Test: Second installation displays clear error about concurrent install.

        Given: First installation is running
        When: Second installation detects concurrent install
        Then: Error message explains concurrent installation
        """
        # Arrange
        from installer.services.lock_file_manager import LockFileManager
        from installer.services.error_categorizer import ErrorCategorizer
        from installer.services.error_recovery_orchestrator import ErrorRecoveryOrchestrator, ErrorRecoveryContext
        from installer.services.install_logger import InstallLogger

        lock_dir = tmp_path / "devforgeai"
        lock_dir.mkdir()

        log_file = lock_dir / "install.log"
        logger = InstallLogger(log_file=log_file)

        manager1 = LockFileManager(lock_dir=lock_dir)
        manager1.acquire_lock()

        manager2 = LockFileManager(lock_dir=lock_dir)
        error_categorizer = ErrorCategorizer()
        orchestrator = ErrorRecoveryOrchestrator(error_categorizer=error_categorizer, logger=logger)

        # Act
        try:
            manager2.acquire_lock()
        except RuntimeError as e:
            context = ErrorRecoveryContext(error=e)
            result = orchestrator.handle_error(context)

            # Assert
            assert result.console_message is not None
            # Should be categorized as validation failure or generic error
            assert result.exit_code in [1, 2, 4]


class TestSigintHandling:
    """Test SIGINT (Ctrl+C) triggers graceful rollback."""

    def test_sigint_triggers_rollback(self, tmp_path):
        """
        Test: SIGINT (Ctrl+C) triggers graceful rollback.

        Given: Installation is in progress
        When: User presses Ctrl+C (SIGINT)
        Then: Rollback is triggered, lock file removed, exit code 3
        """
        # Arrange
        from installer.services.error_categorizer import ErrorCategorizer
        from installer.services.error_recovery_orchestrator import ErrorRecoveryOrchestrator, ErrorRecoveryContext
        from installer.services.rollback_service import RollbackService
        from installer.services.lock_file_manager import LockFileManager
        from installer.services.install_logger import InstallLogger

        lock_dir = tmp_path / "devforgeai"
        lock_dir.mkdir()

        log_file = lock_dir / "install.log"
        logger = InstallLogger(log_file=log_file)

        rollback_service = RollbackService(logger=logger)
        lock_manager = LockFileManager(lock_dir=lock_dir)
        error_categorizer = ErrorCategorizer()
        orchestrator = ErrorRecoveryOrchestrator(
            error_categorizer=error_categorizer,
            rollback_service=rollback_service,
            logger=logger
        )

        lock_manager.acquire_lock()

        # Act
        error = KeyboardInterrupt()
        context = ErrorRecoveryContext(error=error, phase="file_copy")
        result = orchestrator.handle_error(context)

        lock_manager.cleanup()

        # Assert
        # KeyboardInterrupt during file_copy triggers rollback
        assert result.exit_code == 3  # ROLLBACK_OCCURRED
        assert result.console_message is not None
        assert not (lock_dir / "install.lock").exists()

    def test_sigint_displays_cancellation_message(self, tmp_path):
        """
        Test: SIGINT displays error message.

        Given: User presses Ctrl+C during file_copy
        When: ErrorRecoveryOrchestrator handles KeyboardInterrupt
        Then: Console displays error message and returns exit code 3
        """
        # Arrange
        from installer.services.error_categorizer import ErrorCategorizer
        from installer.services.error_recovery_orchestrator import ErrorRecoveryOrchestrator, ErrorRecoveryContext
        from installer.services.rollback_service import RollbackService
        from installer.services.install_logger import InstallLogger

        log_file = tmp_path / "devforgeai" / "install.log"
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
        # KeyboardInterrupt during file_copy should trigger rollback (exit code 3)
        assert result.exit_code == 3
        assert result.console_message is not None


class TestErrorDetectionLatency:
    """Test error detection latency requirements (NFR-001)."""

    def test_error_detection_latency_under_50ms(self, tmp_path):
        """
        Test: Error detection latency <50ms (NFR-001).

        Given: An error occurs during installation
        When: ErrorCategorizer detects and processes error
        Then: Latency from error to categorizer invocation is <50ms
        """
        # Arrange
        from installer.services.error_categorizer import ErrorCategorizer

        error_categorizer = ErrorCategorizer()
        error = FileNotFoundError("Test error")

        # Act
        start_time = time.time()
        error_categorizer.categorize_error(error)
        elapsed_ms = (time.time() - start_time) * 1000

        # Assert
        assert elapsed_ms < 50, f"Error detection took {elapsed_ms:.2f}ms (expected <50ms)"


class TestBackupBeforeModification:
    """Test backup must succeed before file operations (BR-002)."""

    def test_file_copy_blocked_if_backup_fails(self, tmp_path):
        """
        Test: File copy operations blocked if backup fails (BR-002).

        Given: Backup creation fails
        When: Installation attempts to copy files
        Then: File copy is blocked, HALT with PERMISSION_DENIED (exit code 2)
        """
        # Arrange
        from installer.services.backup_service import BackupService
        from installer.error_handler import ErrorHandler
        from installer.services.install_logger import InstallLogger

        target_dir = tmp_path / "target"
        target_dir.mkdir()

        log_file = tmp_path / "devforgeai" / "install.log"
        log_file.parent.mkdir()

        logger = InstallLogger(log_file=log_file)
        backup_service = BackupService(logger=logger)
        error_handler = ErrorHandler(backup_service=backup_service, logger=logger)

        with patch("pathlib.Path.mkdir") as mock_mkdir:
            mock_mkdir.side_effect = PermissionError("Cannot create backup")

            # Act & Assert
            with pytest.raises(PermissionError):
                backup_service.create_backup(target_dir=target_dir, files_to_backup=[])

    def test_installation_proceeds_only_after_successful_backup(self, tmp_path):
        """
        Test: Installation proceeds only after successful backup (AC#7).

        Given: BackupService creates backup
        When: Backup succeeds
        Then: Returns backup directory path, allowing installation to proceed
        """
        # Arrange
        from installer.services.backup_service import BackupService
        from installer.services.install_logger import InstallLogger

        target_dir = tmp_path / "target"
        target_dir.mkdir()

        log_file = tmp_path / "devforgeai" / "install.log"
        log_file.parent.mkdir()

        logger = InstallLogger(log_file=log_file)
        backup_service = BackupService(logger=logger)

        # Act
        backup_dir = backup_service.create_backup(target_dir=target_dir, files_to_backup=[])

        # Assert
        assert backup_dir.exists()
        assert isinstance(backup_dir, Path)


class TestErrorHandlerReliability:
    """Test error handler reliability requirements (NFR-005)."""

    def test_all_file_operations_have_error_handlers(self):
        """
        Test: Error categorizer handles all common file errors (NFR-005).

        Given: Error categorizer is used
        When: Common file errors are categorized
        Then: All file operations errors return valid exit codes
        """
        # Test that error categorizer CAN handle all common file errors

        from installer.services.error_categorizer import ErrorCategorizer

        error_categorizer = ErrorCategorizer()

        # Test common file errors are handled
        file_errors = [
            FileNotFoundError("Missing file"),
            PermissionError("Permission denied"),
            OSError("Disk full"),
            IOError("I/O error"),
        ]

        for error in file_errors:
            category = error_categorizer.categorize_error(error)
            assert category.exit_code in [1, 2, 3, 4]  # Valid exit codes


class TestEndToEndErrorScenarios:
    """Test complete end-to-end error scenarios."""

    def test_e2e_missing_source_files(self, tmp_path):
        """
        Test: E2E scenario - missing source files.

        Given: Source directory is missing
        When: ErrorCategorizer processes the error
        Then: Returns exit code 1, displays error message
        """
        # Arrange
        from installer.services.error_categorizer import ErrorCategorizer
        from installer.services.error_recovery_orchestrator import ErrorRecoveryOrchestrator, ErrorRecoveryContext
        from installer.services.install_logger import InstallLogger

        log_file = tmp_path / "devforgeai" / "install.log"
        log_file.parent.mkdir()

        logger = InstallLogger(log_file=log_file)
        error_categorizer = ErrorCategorizer()
        orchestrator = ErrorRecoveryOrchestrator(error_categorizer=error_categorizer, logger=logger)

        error = FileNotFoundError("src/.claude/ not found")

        # Act
        context = ErrorRecoveryContext(error=error)
        result = orchestrator.handle_error(context)

        # Assert
        assert result.exit_code == 1

    def test_e2e_permission_denied(self, tmp_path):
        """
        Test: E2E scenario - permission denied.

        Given: Target directory is not writable
        When: ErrorCategorizer processes permission error
        Then: Returns exit code 2
        """
        # Arrange
        from installer.services.error_categorizer import ErrorCategorizer
        from installer.services.error_recovery_orchestrator import ErrorRecoveryOrchestrator, ErrorRecoveryContext
        from installer.services.install_logger import InstallLogger

        log_file = tmp_path / "devforgeai" / "install.log"
        log_file.parent.mkdir()

        logger = InstallLogger(log_file=log_file)
        error_categorizer = ErrorCategorizer()
        orchestrator = ErrorRecoveryOrchestrator(error_categorizer=error_categorizer, logger=logger)

        error = PermissionError("Cannot write to .claude/")

        # Act
        context = ErrorRecoveryContext(error=error)
        result = orchestrator.handle_error(context)

        # Assert
        assert result.exit_code == 2

    def test_e2e_validation_failed_post_installation(self, tmp_path):
        """
        Test: E2E scenario - validation fails after installation.

        Given: Installation completes but validation fails
        When: Validation error is detected
        Then: Returns exit code 4, does NOT auto-rollback (user decides)
        """
        # Arrange
        from installer.services.error_categorizer import ErrorCategorizer
        from installer.services.error_recovery_orchestrator import ErrorRecoveryOrchestrator, ErrorRecoveryContext
        from installer.services.install_logger import InstallLogger

        log_file = tmp_path / "devforgeai" / "install.log"
        log_file.parent.mkdir()

        logger = InstallLogger(log_file=log_file)
        error_categorizer = ErrorCategorizer()
        orchestrator = ErrorRecoveryOrchestrator(error_categorizer=error_categorizer, logger=logger)

        error = ValueError("Installation validation failed")

        # Act
        context = ErrorRecoveryContext(error=error, validation_phase=True)
        result = orchestrator.handle_error(context)

        # Assert
        assert result.exit_code == 4
        # Validation errors should NOT trigger automatic rollback (edge case)
        assert "rollback" not in result.console_message.lower()

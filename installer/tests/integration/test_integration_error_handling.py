"""
Integration tests for STORY-074 error handling services.

Tests cross-component workflows validating:
1. Full rollback flow: Error after file copy → backup restore → cleanup → exit code 3
2. Concurrent installation prevention via lock file
3. Error handling with actual file operations (not mocks)
4. Performance validation: <5s rollback, <10s backup for 500 files
5. Log file creation and content validation
6. End-to-end scenarios from error categorization through logging and rollback

Test Structure:
- TestFullRollbackFlow: 4 tests for complete rollback workflows
- TestConcurrentPrevention: 3 tests for lock file management
- TestRealFileOperations: 3 tests with actual file I/O
- TestPerformanceValidation: 2 tests for performance requirements
- TestLogCreationAndContent: 2 tests for logging validation

Total: 14 integration tests
Coverage: AC#1-7, all critical user journeys
"""

import pytest
import json
import shutil
import time
import os
from pathlib import Path
from datetime import datetime


class TestFullRollbackFlow:
    """Test complete rollback workflows from error to recovery."""

    def test_rollback_after_file_copy_error_exit_code_3(
        self, integration_project, source_framework
    ):
        """
        AC#4: Full rollback flow after file copy error.

        Scenario:
        1. Installation starts with 100 files
        2. 50 files copied successfully
        3. Error occurs during file 51 (permission denied)
        4. Backup restore initiated
        5. Partial files cleaned up
        6. Empty directories removed
        7. Exit code 3 returned

        Expected: Project restored to pre-install state, exit code = 3
        """
        from installer.error_handler import ErrorHandler
        from installer.services.backup_service import BackupService
        from installer.services.rollback_service import RollbackService
        from installer.install_logger import InstallLogger
        from src.installer.exit_codes import ROLLBACK_OCCURRED

        # Arrange
        target_root = integration_project["root"]
        logger = InstallLogger(str(target_root / ".devforgeai" / "install.log"))
        error_handler = ErrorHandler(logger)
        backup_service = BackupService(str(target_root / ".devforgeai"))
        rollback_service = RollbackService(logger)

        # Create initial files to backup
        initial_files = []
        for i in range(5):
            file_path = target_root / ".claude" / "agents" / f"agent_{i}.md"
            file_path.write_text(f"Initial content {i}")
            initial_files.append(str(file_path))

        # Create backup
        backup_path = backup_service.create_backup(target_root, initial_files)

        # Simulate partial installation (50 files copied)
        for i in range(50):
            file_path = target_root / ".claude" / "commands" / f"command_{i}.md"
            file_path.write_text(f"New content {i}")
            rollback_service.track_file_creation(str(file_path))

        # Simulate error during file 51
        error = PermissionError("Permission denied: .claude/commands/command_51.md")

        # Act - Handle error and trigger rollback
        message, exit_code = error_handler.log_and_format_error(
            error,
            file_paths={
                'source': str(source_framework["root"] / "claude"),
                'target': str(target_root / ".claude")
            }
        )

        # Execute rollback
        rollback_success = rollback_service.rollback(backup_path)

        # Assert - Exit code 3 (rollback occurred)
        assert exit_code == ROLLBACK_OCCURRED, f"Expected exit code 3, got {exit_code}"

        # Assert - Rollback completed successfully
        assert rollback_success is True, "Rollback should complete successfully"

        # Assert - Partial files removed (50 command files should be gone)
        commands_dir = target_root / ".claude" / "commands"
        remaining_files = list(commands_dir.glob("command_*.md"))
        assert len(remaining_files) == 0, f"Expected 0 partial files, found {len(remaining_files)}"

        # Assert - Original files restored
        for i in range(5):
            file_path = target_root / ".claude" / "agents" / f"agent_{i}.md"
            assert file_path.exists(), f"Original file {file_path} should be restored"
            content = file_path.read_text()
            assert content == f"Initial content {i}", "Restored content should match original"

        # Assert - Log contains error and rollback actions
        log_contents = logger.get_log_contents()
        assert "ERROR PERMISSION_DENIED" in log_contents
        assert "ROLLBACK_START" in log_contents
        assert "ROLLBACK_COMPLETE" in log_contents

    def test_rollback_restores_backup_correctly(
        self, integration_project
    ):
        """
        AC#4, AC#7: Backup restoration preserves directory structure.

        Scenario:
        1. Backup created with nested directory structure
        2. Target files modified/deleted
        3. Rollback triggered
        4. Directory structure and file contents restored

        Expected: All backed-up files restored with correct paths and content
        """
        from installer.services.backup_service import BackupService
        from installer.services.rollback_service import RollbackService
        from installer.install_logger import InstallLogger

        # Arrange
        target_root = integration_project["root"]
        logger = InstallLogger(str(target_root / ".devforgeai" / "install.log"))
        backup_service = BackupService(str(target_root / ".devforgeai"))
        rollback_service = RollbackService(logger)

        # Create nested directory structure
        nested_files = []
        for i in range(3):
            subdir = target_root / ".claude" / f"level1_{i}" / f"level2_{i}"
            subdir.mkdir(parents=True, exist_ok=True)
            file_path = subdir / f"file_{i}.md"
            file_path.write_text(f"Nested content {i}")
            nested_files.append(str(file_path))

        # Create backup
        backup_path = backup_service.create_backup(target_root, nested_files)

        # Modify/delete target files
        for file_path_str in nested_files:
            file_path = Path(file_path_str)
            if file_path.exists():
                file_path.unlink()

        # Act - Rollback
        rollback_success = rollback_service.rollback(backup_path)

        # Assert - All files restored with correct structure
        assert rollback_success is True
        for i in range(3):
            file_path = target_root / ".claude" / f"level1_{i}" / f"level2_{i}" / f"file_{i}.md"
            assert file_path.exists(), f"Nested file {file_path} should be restored"
            content = file_path.read_text()
            assert content == f"Nested content {i}", "Restored nested content should match"

    def test_rollback_cleanup_removes_empty_directories(
        self, integration_project
    ):
        """
        AC#4: Rollback cleanup removes empty directories created during installation.

        Scenario:
        1. Installation creates nested directory structure
        2. Error occurs before files written
        3. Rollback removes all empty directories
        4. Project tree clean

        Expected: No empty directories left after rollback
        """
        from installer.services.rollback_service import RollbackService
        from installer.install_logger import InstallLogger

        # Arrange
        target_root = integration_project["root"]
        logger = InstallLogger(str(target_root / ".devforgeai" / "install.log"))
        rollback_service = RollbackService(logger)

        # Create nested empty directories
        for i in range(5):
            dir_path = target_root / ".claude" / f"empty_level1_{i}" / f"empty_level2_{i}"
            dir_path.mkdir(parents=True, exist_ok=True)
            rollback_service.track_dir_creation(str(dir_path))
            rollback_service.track_dir_creation(str(dir_path.parent))

        # Act - Trigger cleanup (no backup needed for directory cleanup)
        rollback_service._clean_empty_directories()

        # Assert - Empty directories removed
        for i in range(5):
            dir_path = target_root / ".claude" / f"empty_level1_{i}" / f"empty_level2_{i}"
            assert not dir_path.exists(), f"Empty directory {dir_path} should be removed"

        # Assert - Parent directories also cleaned if empty
        base_dir = target_root / ".claude"
        empty_level1_dirs = list(base_dir.glob("empty_level1_*"))
        assert len(empty_level1_dirs) == 0, "All empty level1 directories should be removed"

    def test_rollback_performance_under_5_seconds(
        self, integration_project, performance_timer
    ):
        """
        NFR: Rollback completes in <5 seconds for 100 files.

        Scenario:
        1. Create backup with 100 files
        2. Modify all 100 files
        3. Trigger rollback with timer
        4. Measure completion time

        Expected: Rollback completes in <5 seconds
        """
        from installer.services.backup_service import BackupService
        from installer.services.rollback_service import RollbackService
        from installer.install_logger import InstallLogger

        # Arrange
        target_root = integration_project["root"]
        logger = InstallLogger(str(target_root / ".devforgeai" / "install.log"))
        backup_service = BackupService(str(target_root / ".devforgeai"))
        rollback_service = RollbackService(logger)

        # Create 100 files
        files_to_backup = []
        for i in range(100):
            file_path = target_root / ".claude" / "agents" / f"agent_{i:03d}.md"
            file_path.write_text(f"Original content {i}")
            files_to_backup.append(str(file_path))

        backup_path = backup_service.create_backup(target_root, files_to_backup)

        # Modify all files
        for file_path_str in files_to_backup:
            Path(file_path_str).write_text("Modified content")

        # Act - Rollback with timer
        with performance_timer.measure("rollback_100_files") as timer:
            rollback_success = rollback_service.rollback(backup_path)

        # Assert - Rollback successful
        assert rollback_success is True

        # Assert - Performance requirement met (<5 seconds)
        assert timer.elapsed < 5.0, f"Rollback took {timer.elapsed:.2f}s (expected <5s)"

        # Assert - Files restored correctly
        for i in range(100):
            file_path = target_root / ".claude" / "agents" / f"agent_{i:03d}.md"
            content = file_path.read_text()
            assert content == f"Original content {i}", f"File {i} not restored correctly"


class TestConcurrentPrevention:
    """Test concurrent installation prevention via lock file."""

    def test_concurrent_install_blocked_by_lock_file(
        self, integration_project
    ):
        """
        AC#8 (RCA-004): Concurrent installations prevented via lock file.

        Scenario:
        1. Process A acquires lock (creates .devforgeai/install.lock with PID)
        2. Process B attempts installation
        3. Process B detects lock file
        4. Process B exits with clear error message

        Expected: Second process cannot acquire lock, exits cleanly
        """
        from src.installer.lock_file_manager import LockFileManager

        # Arrange
        target_root = integration_project["root"]
        lock_manager_1 = LockFileManager(str(target_root / ".devforgeai" / "install.lock"))
        lock_manager_2 = LockFileManager(str(target_root / ".devforgeai" / "install.lock"))

        # Act - Process 1 acquires lock
        lock_acquired_1 = lock_manager_1.acquire_lock()

        # Act - Process 2 attempts to acquire lock
        lock_acquired_2 = lock_manager_2.acquire_lock()

        # Assert - Process 1 successful
        assert lock_acquired_1 is True, "First process should acquire lock"

        # Assert - Process 2 blocked
        assert lock_acquired_2 is False, "Second process should be blocked"

        # Assert - Lock file contains process 1 PID
        locked_pid = lock_manager_2.get_locked_pid()
        assert locked_pid == os.getpid(), "Lock file should contain first process PID"

        # Cleanup
        lock_manager_1.release_lock()

    def test_stale_lock_file_cleaned_up(
        self, integration_project
    ):
        """
        AC#8 (RCA-004): Stale lock file with dead PID is cleaned up.

        Scenario:
        1. Lock file exists with non-existent PID (process crashed)
        2. New installation attempts to acquire lock
        3. Lock manager detects stale lock (PID not running)
        4. Stale lock removed, new lock acquired

        Expected: Stale lock cleaned up, new installation proceeds
        """
        from src.installer.lock_file_manager import LockFileManager

        # Arrange
        target_root = integration_project["root"]
        lock_path = target_root / ".devforgeai" / "install.lock"

        # Create stale lock file with non-existent PID
        lock_path.write_text("99999")  # PID unlikely to exist

        lock_manager = LockFileManager(str(lock_path))

        # Act - Attempt to acquire lock
        lock_acquired = lock_manager.acquire_lock()

        # Assert - Lock acquired (stale lock cleaned)
        assert lock_acquired is True, "Should acquire lock after cleaning stale lock"

        # Assert - Lock file now contains current PID
        current_pid = lock_manager.get_locked_pid()
        assert current_pid == os.getpid(), "Lock file should contain current process PID"

        # Cleanup
        lock_manager.release_lock()

    def test_lock_release_allows_subsequent_install(
        self, integration_project
    ):
        """
        AC#8 (RCA-004): Lock release allows subsequent installations.

        Scenario:
        1. Process A acquires lock
        2. Process A completes installation
        3. Process A releases lock
        4. Process B acquires lock successfully
        5. Process B proceeds with installation

        Expected: Lock released, subsequent installation proceeds
        """
        from src.installer.lock_file_manager import LockFileManager

        # Arrange
        target_root = integration_project["root"]
        lock_path = target_root / ".devforgeai" / "install.lock"
        lock_manager_1 = LockFileManager(str(lock_path))
        lock_manager_2 = LockFileManager(str(lock_path))

        # Act - Process 1 acquires and releases lock
        lock_acquired_1 = lock_manager_1.acquire_lock()
        assert lock_acquired_1 is True

        lock_manager_1.release_lock()

        # Act - Process 2 acquires lock after release
        lock_acquired_2 = lock_manager_2.acquire_lock()

        # Assert - Process 2 successful
        assert lock_acquired_2 is True, "Second process should acquire lock after first releases"

        # Assert - Lock file contains process 2 PID
        locked_pid = lock_manager_2.get_locked_pid()
        assert locked_pid == os.getpid()

        # Cleanup
        lock_manager_2.release_lock()


class TestRealFileOperations:
    """Test error handling with actual file operations (not mocks)."""

    def test_missing_source_files_error_exit_code_1(
        self, integration_project
    ):
        """
        AC#1: Missing source files categorized correctly with exit code 1.

        Scenario:
        1. Installation attempts to copy from non-existent source
        2. FileNotFoundError raised
        3. Error handler categorizes as MISSING_SOURCE
        4. User-friendly message formatted
        5. Exit code 1 returned

        Expected: Error categorized correctly, helpful message, exit code 1
        """
        from installer.error_handler import ErrorHandler
        from installer.install_logger import InstallLogger
        from src.installer.exit_codes import MISSING_SOURCE

        # Arrange
        target_root = integration_project["root"]
        logger = InstallLogger(str(target_root / ".devforgeai" / "install.log"))
        error_handler = ErrorHandler(logger)

        # Simulate missing source error
        non_existent_path = target_root / "non_existent_source" / ".claude"
        error = FileNotFoundError(f"Source directory not found: {non_existent_path}")

        # Act
        message, exit_code = error_handler.log_and_format_error(
            error,
            file_paths={
                'source': str(non_existent_path),
                'target': str(target_root / ".claude")
            }
        )

        # Assert - Exit code 1
        assert exit_code == MISSING_SOURCE, f"Expected exit code 1, got {exit_code}"

        # Assert - Message contains helpful guidance
        assert "Missing Source Files" in message
        assert "resolution steps" in message.lower()
        assert ".devforgeai/install.log" in message

        # Assert - Log created
        log_path = target_root / ".devforgeai" / "install.log"
        assert log_path.exists(), "Log file should be created"

    def test_permission_denied_error_exit_code_2(
        self, integration_project
    ):
        """
        AC#1: Permission denied errors categorized correctly with exit code 2.

        Scenario:
        1. Installation attempts to write to read-only directory
        2. PermissionError raised
        3. Error handler categorizes as PERMISSION_DENIED
        4. Resolution steps include permission commands
        5. Exit code 2 returned

        Expected: Error categorized, actionable steps, exit code 2
        """
        from installer.error_handler import ErrorHandler
        from installer.install_logger import InstallLogger
        from src.installer.exit_codes import PERMISSION_DENIED

        # Arrange
        target_root = integration_project["root"]
        logger = InstallLogger(str(target_root / ".devforgeai" / "install.log"))
        error_handler = ErrorHandler(logger)

        # Create directory and make it read-only
        readonly_dir = target_root / "readonly_target"
        readonly_dir.mkdir(parents=True, exist_ok=True)
        readonly_dir.chmod(0o444)  # Read-only

        # Simulate permission error
        error = PermissionError(f"Permission denied: {readonly_dir}")

        # Act
        message, exit_code = error_handler.log_and_format_error(
            error,
            file_paths={
                'target': str(readonly_dir)
            }
        )

        # Assert - Exit code 2
        assert exit_code == PERMISSION_DENIED, f"Expected exit code 2, got {exit_code}"

        # Assert - Message contains permission guidance
        assert "Permission Denied" in message
        assert any(cmd in message for cmd in ["chmod", "chown", "sudo"]), \
            "Message should contain permission-related commands"

        # Cleanup
        readonly_dir.chmod(0o755)

    def test_validation_failed_error_exit_code_4(
        self, integration_project
    ):
        """
        AC#1: Validation failures categorized correctly with exit code 4.

        Scenario:
        1. Installation completes file deployment
        2. Post-install validation fails (file count mismatch)
        3. Error handler categorizes as VALIDATION_FAILED
        4. Message suggests retry installation
        5. Exit code 4 returned

        Expected: Error categorized, retry guidance, exit code 4
        """
        from installer.error_handler import ErrorHandler
        from installer.install_logger import InstallLogger
        from src.installer.exit_codes import VALIDATION_FAILED

        # Arrange
        target_root = integration_project["root"]
        logger = InstallLogger(str(target_root / ".devforgeai" / "install.log"))
        error_handler = ErrorHandler(logger)

        # Simulate validation error
        error = ValueError("Validation failed: Expected 450 files, found 445")

        # Act
        message, exit_code = error_handler.log_and_format_error(error)

        # Assert - Exit code 4
        assert exit_code == VALIDATION_FAILED, f"Expected exit code 4, got {exit_code}"

        # Assert - Message suggests validation and retry
        assert "Validation Failed" in message
        assert "retry" in message.lower() or "install" in message.lower()


class TestPerformanceValidation:
    """Test performance requirements for error handling operations."""

    def test_backup_creation_under_10_seconds_for_500_files(
        self, integration_project, performance_timer
    ):
        """
        NFR: Backup creation completes in <10 seconds for 500 files.

        Scenario:
        1. Create 500 files (mix of small and medium sizes)
        2. Trigger backup creation with timer
        3. Measure completion time

        Expected: Backup completes in <10 seconds
        """
        from installer.services.backup_service import BackupService

        # Arrange
        target_root = integration_project["root"]
        backup_service = BackupService(str(target_root / ".devforgeai"))

        # Create 500 files with varying sizes
        files_to_backup = []
        for i in range(500):
            subdir = target_root / ".claude" / f"dir_{i % 10}"
            subdir.mkdir(parents=True, exist_ok=True)
            file_path = subdir / f"file_{i:03d}.md"

            # Vary file sizes: 1KB, 5KB, 10KB
            size_bytes = [1024, 5120, 10240][i % 3]
            content = "x" * size_bytes
            file_path.write_text(content)
            files_to_backup.append(str(file_path))

        # Act - Backup with timer
        with performance_timer.measure("backup_500_files") as timer:
            backup_path = backup_service.create_backup(target_root, files_to_backup)

        # Assert - Backup created
        assert Path(backup_path).exists(), "Backup directory should be created"

        # Assert - Performance requirement met (<10 seconds)
        assert timer.elapsed < 10.0, f"Backup took {timer.elapsed:.2f}s (expected <10s)"

        # Assert - All files backed up
        backup_file_count = len(list(Path(backup_path).rglob("*.md")))
        assert backup_file_count == 500, f"Expected 500 files backed up, found {backup_file_count}"

    def test_log_file_creation_performance_under_100ms(
        self, integration_project, performance_timer
    ):
        """
        NFR: Log file creation and write completes in <100ms.

        Scenario:
        1. Initialize logger
        2. Log 100 error entries with timer
        3. Measure total time

        Expected: 100 log entries written in <100ms
        """
        from installer.install_logger import InstallLogger

        # Arrange
        target_root = integration_project["root"]
        log_path = target_root / ".devforgeai" / "install.log"
        logger = InstallLogger(str(log_path))

        # Act - Log 100 entries with timer
        with performance_timer.measure("log_100_entries") as timer:
            for i in range(100):
                logger.log_action(f"TEST_ACTION_{i}", f"Details for action {i}")

        # Assert - Performance requirement met (<100ms)
        assert timer.elapsed < 0.1, f"Logging took {timer.elapsed * 1000:.2f}ms (expected <100ms)"

        # Assert - Log file created
        assert log_path.exists(), "Log file should be created"

        # Assert - All entries written
        log_contents = logger.get_log_contents()
        assert log_contents.count("ACTION TEST_ACTION_") == 100, "All 100 entries should be logged"


class TestLogCreationAndContent:
    """Test log file creation and content validation."""

    def test_log_file_created_with_correct_permissions(
        self, integration_project
    ):
        """
        AC#5: Log file created with 0600 permissions (owner read/write only).

        Scenario:
        1. Logger initialized
        2. First log entry written
        3. Log file created with secure permissions

        Expected: Log file exists with 0600 permissions
        """
        from installer.install_logger import InstallLogger

        # Arrange
        target_root = integration_project["root"]
        log_path = target_root / ".devforgeai" / "install.log"
        logger = InstallLogger(str(log_path))

        # Act - Write first log entry
        logger.log_action("TEST_ACTION", "Initial log entry")

        # Assert - Log file created
        assert log_path.exists(), "Log file should be created"

        # Assert - Permissions are 0600 (owner read/write only)
        file_mode = log_path.stat().st_mode & 0o777
        assert file_mode == 0o600, f"Expected permissions 0600, got {oct(file_mode)}"

    def test_log_contains_iso8601_timestamps_and_context(
        self, integration_project
    ):
        """
        AC#5: Log entries contain ISO 8601 timestamps, error category, and system context.

        Scenario:
        1. Error occurs during installation
        2. Error logged with handler
        3. Log entry verified for required fields

        Expected: Log entry has timestamp, category, exit code, message, stack trace, OS
        """
        from installer.error_handler import ErrorHandler
        from installer.install_logger import InstallLogger

        # Arrange
        target_root = integration_project["root"]
        log_path = target_root / ".devforgeai" / "install.log"
        logger = InstallLogger(str(log_path))
        error_handler = ErrorHandler(logger)

        # Act - Log error
        error = PermissionError("Test permission error")
        error_handler.log_and_format_error(
            error,
            file_paths={
                'source': '/tmp/source',
                'target': '/tmp/target'
            }
        )

        # Assert - Log file created
        assert log_path.exists()

        # Read log contents
        log_contents = logger.get_log_contents()

        # Assert - ISO 8601 timestamp present (format: YYYY-MM-DDTHH:MM:SS.mmm)
        import re
        iso8601_pattern = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}'
        assert re.search(iso8601_pattern, log_contents), \
            "Log should contain ISO 8601 timestamp"

        # Assert - Error category present
        assert "ERROR PERMISSION_DENIED" in log_contents

        # Assert - Exit code present
        assert "(exit=2)" in log_contents

        # Assert - File paths present
        assert "Source: /tmp/source" in log_contents
        assert "Target: /tmp/target" in log_contents

        # Assert - OS context present
        assert f"OS: {os.name}" in log_contents

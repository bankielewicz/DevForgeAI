"""
STORY-074: Unit tests for LockFileManager.

Tests lock file creation, concurrent installation detection, and cleanup.
All tests follow TDD Red phase - they should FAIL until implementation exists.

Coverage Target: 95%+
"""

import pytest
from unittest.mock import Mock, patch
from pathlib import Path
import os
import time


class TestLockFileCreation:
    """Test lock file creation at installation start (SVC-013)."""

    def test_create_lock_file_at_installation_start(self, tmp_path):
        """
        Test: LockFileManager creates lock file at installation start (SVC-013).

        Given: Installation starts
        When: LockFileManager.acquire_lock() is called
        Then: Lock file created at .devforgeai/install.lock
        """
        # Arrange
        from installer.services.lock_file_manager import LockFileManager
        lock_dir = tmp_path / ".devforgeai"
        lock_dir.mkdir()

        manager = LockFileManager(lock_dir=lock_dir)

        # Act
        manager.acquire_lock()

        # Assert
        lock_file = lock_dir / "install.lock"
        assert lock_file.exists()

    def test_lock_file_contains_current_process_pid(self, tmp_path):
        """
        Test: Lock file contains current process PID.

        Given: LockFileManager creates lock file
        When: Lock file is written
        Then: File contains current process PID
        """
        # Arrange
        from installer.services.lock_file_manager import LockFileManager
        lock_dir = tmp_path / ".devforgeai"
        lock_dir.mkdir()

        manager = LockFileManager(lock_dir=lock_dir)

        # Act
        manager.acquire_lock()

        # Assert
        lock_file = lock_dir / "install.lock"
        lock_content = lock_file.read_text()
        current_pid = os.getpid()
        assert str(current_pid) in lock_content

    def test_lock_file_contains_timestamp(self, tmp_path):
        """
        Test: Lock file contains creation timestamp.

        Given: LockFileManager creates lock file
        When: Lock file is written
        Then: File contains ISO 8601 timestamp
        """
        # Arrange
        from installer.services.lock_file_manager import LockFileManager
        lock_dir = tmp_path / ".devforgeai"
        lock_dir.mkdir()

        manager = LockFileManager(lock_dir=lock_dir)

        # Act
        manager.acquire_lock()

        # Assert
        lock_file = lock_dir / "install.lock"
        lock_content = lock_file.read_text()
        # Should contain ISO 8601 timestamp
        import re
        iso_regex = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}'
        assert re.search(iso_regex, lock_content)


class TestConcurrentInstallationDetection:
    """Test detection of concurrent installations (SVC-014, BR-004)."""

    def test_detect_concurrent_installation_via_pid_check(self, tmp_path):
        """
        Test: LockFileManager detects concurrent installation via PID check (SVC-014).

        Given: A lock file exists with active PID
        When: Second installation attempts to acquire lock
        Then: Raises RuntimeError indicating concurrent installation
        """
        # Arrange
        from installer.services.lock_file_manager import LockFileManager
        lock_dir = tmp_path / ".devforgeai"
        lock_dir.mkdir()

        # First installation acquires lock
        manager1 = LockFileManager(lock_dir=lock_dir)
        manager1.acquire_lock()

        # Second installation attempts to acquire lock
        manager2 = LockFileManager(lock_dir=lock_dir)

        # Act & Assert
        with pytest.raises(RuntimeError) as exc_info:
            manager2.acquire_lock()

        assert "concurrent" in str(exc_info.value).lower()

    def test_lock_acquisition_succeeds_when_no_existing_lock(self, tmp_path):
        """
        Test: LockFileManager acquires lock successfully when no existing lock.

        Given: No lock file exists
        When: LockFileManager.acquire_lock() is called
        Then: Lock is acquired successfully
        """
        # Arrange
        from installer.services.lock_file_manager import LockFileManager
        lock_dir = tmp_path / ".devforgeai"
        lock_dir.mkdir()

        manager = LockFileManager(lock_dir=lock_dir)

        # Act
        result = manager.acquire_lock()

        # Assert
        assert result is True

    def test_second_install_fails_with_validation_failed_exit_code(self, tmp_path):
        """
        Test: Second install fails with VALIDATION_FAILED (exit code 4) when lock exists (BR-004).

        Given: Lock file exists from first installation
        When: Second installation checks for concurrent install
        Then: Raises error that maps to exit code 4
        """
        # Arrange
        from installer.services.lock_file_manager import LockFileManager
        lock_dir = tmp_path / ".devforgeai"
        lock_dir.mkdir()

        manager1 = LockFileManager(lock_dir=lock_dir)
        manager1.acquire_lock()

        manager2 = LockFileManager(lock_dir=lock_dir)

        # Act & Assert
        with pytest.raises(RuntimeError) as exc_info:
            manager2.acquire_lock()

        # Error should indicate VALIDATION_FAILED scenario
        assert "concurrent" in str(exc_info.value).lower()


class TestLockFileCleanup:
    """Test lock file cleanup on exit (SVC-015)."""

    def test_remove_lock_file_on_successful_exit(self, tmp_path):
        """
        Test: LockFileManager removes lock file on successful exit (SVC-015).

        Given: Lock file exists during installation
        When: Installation completes successfully
        Then: Lock file is removed
        """
        # Arrange
        from installer.services.lock_file_manager import LockFileManager
        lock_dir = tmp_path / ".devforgeai"
        lock_dir.mkdir()

        manager = LockFileManager(lock_dir=lock_dir)
        manager.acquire_lock()

        lock_file = lock_dir / "install.lock"
        assert lock_file.exists()

        # Act
        manager.release_lock()

        # Assert
        assert not lock_file.exists()

    def test_remove_lock_file_on_error_exit(self, tmp_path):
        """
        Test: LockFileManager removes lock file on error exit (SVC-015).

        Given: Lock file exists during installation
        When: Installation encounters error
        Then: Lock file is removed during cleanup
        """
        # Arrange
        from installer.services.lock_file_manager import LockFileManager
        lock_dir = tmp_path / ".devforgeai"
        lock_dir.mkdir()

        manager = LockFileManager(lock_dir=lock_dir)
        manager.acquire_lock()

        # Act
        manager.cleanup()

        # Assert
        lock_file = lock_dir / "install.lock"
        assert not lock_file.exists()

    def test_remove_lock_file_on_keyboard_interrupt(self, tmp_path):
        """
        Test: LockFileManager removes lock file on KeyboardInterrupt (Ctrl+C) (SVC-015).

        Given: Lock file exists during installation
        When: User presses Ctrl+C
        Then: Lock file is removed in signal handler
        """
        # Arrange
        from installer.services.lock_file_manager import LockFileManager
        lock_dir = tmp_path / ".devforgeai"
        lock_dir.mkdir()

        manager = LockFileManager(lock_dir=lock_dir)
        manager.acquire_lock()

        # Act
        try:
            raise KeyboardInterrupt()
        except KeyboardInterrupt:
            manager.cleanup()

        # Assert
        lock_file = lock_dir / "install.lock"
        assert not lock_file.exists()


class TestStaleLockDetection:
    """Test detection and removal of stale lock files (SVC-016)."""

    def test_detect_stale_lock_with_dead_pid(self, tmp_path):
        """
        Test: LockFileManager detects stale lock with dead PID (SVC-016).

        Given: Lock file exists with PID of dead process
        When: LockFileManager checks lock
        Then: Identifies lock as stale
        """
        # Arrange
        from installer.services.lock_file_manager import LockFileManager
        lock_dir = tmp_path / ".devforgeai"
        lock_dir.mkdir()

        # Create stale lock with dead PID
        lock_file = lock_dir / "install.lock"
        dead_pid = 999999  # PID that doesn't exist
        lock_file.write_text(f"{dead_pid}\n2025-12-03T10:00:00Z")

        manager = LockFileManager(lock_dir=lock_dir)

        # Act
        is_stale = manager.is_lock_stale()

        # Assert
        assert is_stale is True

    def test_remove_stale_lock_file(self, tmp_path):
        """
        Test: LockFileManager removes stale lock files (SVC-016).

        Given: Stale lock file exists
        When: LockFileManager attempts to acquire lock
        Then: Stale lock is removed, new lock acquired
        """
        # Arrange
        from installer.services.lock_file_manager import LockFileManager
        lock_dir = tmp_path / ".devforgeai"
        lock_dir.mkdir()

        # Create stale lock
        lock_file = lock_dir / "install.lock"
        dead_pid = 999999
        lock_file.write_text(f"{dead_pid}\n2025-12-03T10:00:00Z")

        manager = LockFileManager(lock_dir=lock_dir)

        # Act
        manager.acquire_lock()  # Should remove stale lock and acquire new lock

        # Assert
        assert lock_file.exists()
        # Lock should contain current PID, not dead PID
        lock_content = lock_file.read_text()
        assert str(os.getpid()) in lock_content
        assert str(dead_pid) not in lock_content

    def test_active_lock_is_not_considered_stale(self, tmp_path):
        """
        Test: LockFileManager does not consider active lock as stale.

        Given: Lock file exists with current process PID
        When: LockFileManager checks if lock is stale
        Then: Returns False (lock is active)
        """
        # Arrange
        from installer.services.lock_file_manager import LockFileManager
        lock_dir = tmp_path / ".devforgeai"
        lock_dir.mkdir()

        manager1 = LockFileManager(lock_dir=lock_dir)
        manager1.acquire_lock()

        manager2 = LockFileManager(lock_dir=lock_dir)

        # Act
        is_stale = manager2.is_lock_stale()

        # Assert
        assert is_stale is False


class TestLockFileEdgeCases:
    """Test lock file edge case scenarios."""

    def test_lock_acquisition_retries_on_race_condition(self, tmp_path):
        """
        Test: LockFileManager retries lock acquisition on race condition.

        Given: Two installations attempt to acquire lock simultaneously
        When: Race condition occurs
        Then: One succeeds, other retries or fails gracefully
        """
        # Arrange
        from installer.services.lock_file_manager import LockFileManager
        lock_dir = tmp_path / ".devforgeai"
        lock_dir.mkdir()

        manager1 = LockFileManager(lock_dir=lock_dir)
        manager2 = LockFileManager(lock_dir=lock_dir)

        # Simulate race condition with threading
        import threading

        results = []

        def acquire_lock_thread(manager):
            try:
                manager.acquire_lock()
                results.append("success")
            except RuntimeError:
                results.append("failed")

        # Act
        thread1 = threading.Thread(target=acquire_lock_thread, args=(manager1,))
        thread2 = threading.Thread(target=acquire_lock_thread, args=(manager2,))

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()

        # Assert
        # One should succeed, one should fail
        assert "success" in results
        assert "failed" in results

    def test_lock_file_permissions_0600(self, tmp_path):
        """
        Test: LockFileManager creates lock file with 0600 permissions (security).

        Given: LockFileManager creates lock file
        When: Lock file is created
        Then: Permissions are 0600 (owner read/write only)
        """
        # Arrange
        from installer.services.lock_file_manager import LockFileManager
        lock_dir = tmp_path / ".devforgeai"
        lock_dir.mkdir()

        manager = LockFileManager(lock_dir=lock_dir)

        # Act
        manager.acquire_lock()

        # Assert
        lock_file = lock_dir / "install.lock"
        import stat
        file_mode = lock_file.stat().st_mode
        permissions = stat.filemode(file_mode)
        assert permissions == "-rw-------" or (file_mode & 0o777) == 0o600

    def test_lock_file_survives_process_crash_simulation(self, tmp_path):
        """
        Test: LockFileManager handles lock file left by crashed process.

        Given: Process crashes without cleanup (lock file remains)
        When: New installation starts
        Then: Detects stale lock, removes it, proceeds with installation
        """
        # Arrange
        from installer.services.lock_file_manager import LockFileManager
        lock_dir = tmp_path / ".devforgeai"
        lock_dir.mkdir()

        # Simulate crashed process lock
        lock_file = lock_dir / "install.lock"
        dead_pid = 999999
        lock_file.write_text(f"{dead_pid}\n2025-12-03T10:00:00Z")

        manager = LockFileManager(lock_dir=lock_dir)

        # Act
        manager.acquire_lock()  # Should succeed by removing stale lock

        # Assert
        assert lock_file.exists()
        assert str(os.getpid()) in lock_file.read_text()

    def test_lock_handles_devforgeai_directory_missing(self, tmp_path):
        """
        Test: LockFileManager handles missing .devforgeai directory.

        Given: .devforgeai directory does not exist
        When: LockFileManager attempts to acquire lock
        Then: Creates directory and lock file
        """
        # Arrange
        from installer.services.lock_file_manager import LockFileManager
        lock_dir = tmp_path / ".devforgeai"
        # Note: directory does NOT exist

        manager = LockFileManager(lock_dir=lock_dir)

        # Act
        manager.acquire_lock()

        # Assert
        assert lock_dir.exists()
        assert (lock_dir / "install.lock").exists()


class TestLockFileTimeout:
    """Test lock acquisition timeout scenarios."""

    def test_lock_acquisition_fails_after_timeout(self, tmp_path):
        """
        Test: LockFileManager fails lock acquisition after timeout.

        Given: Lock file exists with active PID
        When: Second installation waits for lock with timeout
        Then: Raises TimeoutError after timeout expires
        """
        # Arrange
        from installer.services.lock_file_manager import LockFileManager
        lock_dir = tmp_path / ".devforgeai"
        lock_dir.mkdir()

        manager1 = LockFileManager(lock_dir=lock_dir)
        manager1.acquire_lock()

        manager2 = LockFileManager(lock_dir=lock_dir)

        # Act & Assert
        with pytest.raises((RuntimeError, TimeoutError)):
            manager2.acquire_lock(timeout_seconds=1)

    def test_lock_acquisition_succeeds_if_lock_released_before_timeout(self, tmp_path):
        """
        Test: LockFileManager acquires lock if released before timeout.

        Given: Lock file exists but will be released soon
        When: Second installation waits with timeout
        Then: Acquires lock when first installation releases
        """
        # Arrange
        from installer.services.lock_file_manager import LockFileManager
        lock_dir = tmp_path / ".devforgeai"
        lock_dir.mkdir()

        manager1 = LockFileManager(lock_dir=lock_dir)
        manager1.acquire_lock()

        manager2 = LockFileManager(lock_dir=lock_dir)

        import threading

        def release_after_delay():
            time.sleep(0.5)
            manager1.release_lock()

        thread = threading.Thread(target=release_after_delay)
        thread.start()

        # Act
        result = manager2.acquire_lock(timeout_seconds=2, retry_interval=0.1)

        thread.join()

        # Assert
        assert result is True


class TestLockFileContextManager:
    """Test LockFileManager as context manager (with statement)."""

    def test_lock_manager_works_as_context_manager(self, tmp_path):
        """
        Test: LockFileManager can be used as context manager (with statement).

        Given: LockFileManager is used with 'with' statement
        When: Context is entered and exited
        Then: Lock acquired on enter, released on exit
        """
        # Arrange
        from installer.services.lock_file_manager import LockFileManager
        lock_dir = tmp_path / ".devforgeai"
        lock_dir.mkdir()

        lock_file = lock_dir / "install.lock"

        # Act
        with LockFileManager(lock_dir=lock_dir) as manager:
            assert lock_file.exists()  # Lock acquired

        # Assert
        assert not lock_file.exists()  # Lock released after context exit

    def test_lock_released_even_if_exception_in_context(self, tmp_path):
        """
        Test: LockFileManager releases lock even if exception occurs in context.

        Given: LockFileManager is used in 'with' statement
        When: Exception is raised inside context
        Then: Lock is released during cleanup
        """
        # Arrange
        from installer.services.lock_file_manager import LockFileManager
        lock_dir = tmp_path / ".devforgeai"
        lock_dir.mkdir()

        lock_file = lock_dir / "install.lock"

        # Act & Assert
        try:
            with LockFileManager(lock_dir=lock_dir) as manager:
                assert lock_file.exists()
                raise ValueError("Test error")
        except ValueError:
            pass

        # Lock should still be released
        assert not lock_file.exists()

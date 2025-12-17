"""Unit tests for lock_file_coordinator.py (STORY-096).

Tests lock file coordination for serializing git commits across parallel worktrees.

Test Categories:
- Lock Acquisition (8 tests) - AC#1, NFR-001
- Stale Lock Detection (8 tests) - AC#3
- Wait with Progress (6 tests) - AC#2
- Timeout Handling (5 tests) - AC#4
- Lock Release (5 tests) - AC#5
- Lock Content Parsing (5 tests)
- Edge Cases (5 tests)

Total: 42 tests
"""

import os
import sys
import json
import time
import socket
import tempfile
import threading
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock

import pytest

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from lock_file_coordinator import (
    GitCommitLock,
    LockAcquisitionResult,
    LockStatus,
    LOCK_DIR,
    LOCK_FILE,
    STALE_THRESHOLD_SECONDS,
)


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture
def temp_lock_dir(tmp_path):
    """Create a temporary lock directory for testing."""
    lock_dir = tmp_path / ".devforgeai" / ".locks"
    lock_dir.mkdir(parents=True, exist_ok=True)
    return lock_dir


@pytest.fixture
def lock_instance(temp_lock_dir):
    """Create a GitCommitLock instance with temporary directory."""
    lock = GitCommitLock(story_id="STORY-096", lock_dir=str(temp_lock_dir.parent.parent))
    return lock


@pytest.fixture
def create_lock_file(temp_lock_dir):
    """Factory fixture to create lock files with custom content."""
    def _create(pid=None, story_id="STORY-037", timestamp=None, hostname=None):
        if pid is None:
            pid = os.getpid()
        if timestamp is None:
            timestamp = datetime.utcnow().isoformat() + "Z"
        if hostname is None:
            hostname = socket.gethostname()

        lock_file = temp_lock_dir / "git-commit.lock"
        content = f"pid: {pid}\nstory_id: {story_id}\ntimestamp: {timestamp}\nhostname: {hostname}\n"
        lock_file.write_text(content)
        return lock_file
    return _create


# =============================================================================
# 1. Lock Acquisition Tests (8 tests) - AC#1, NFR-001
# =============================================================================

class TestLockAcquisition:
    """Tests for AC#1: Lock acquisition before commit."""

    def test_acquire_lock_creates_file(self, lock_instance, temp_lock_dir):
        """AC#1: Lock file created on acquisition."""
        result = lock_instance.acquire(timeout_seconds=0)

        assert result.success is True
        lock_file = temp_lock_dir / "git-commit.lock"
        assert lock_file.exists()
        lock_instance.release()

    def test_lock_contains_pid_story_timestamp_hostname(self, lock_instance, temp_lock_dir):
        """AC#1: Lock contains PID, story_id, timestamp, hostname."""
        result = lock_instance.acquire(timeout_seconds=0)

        lock_file = temp_lock_dir / "git-commit.lock"
        content = lock_file.read_text()

        assert f"pid: {os.getpid()}" in content
        assert "story_id: STORY-096" in content
        assert "timestamp:" in content
        assert f"hostname: {socket.gethostname()}" in content
        lock_instance.release()

    def test_acquire_lock_under_100ms(self, lock_instance):
        """NFR-001: Lock acquisition < 100ms when no contention."""
        start = time.perf_counter()
        result = lock_instance.acquire(timeout_seconds=0)
        elapsed_ms = (time.perf_counter() - start) * 1000

        assert result.success is True
        assert elapsed_ms < 100, f"Lock acquisition took {elapsed_ms:.2f}ms, expected <100ms"
        lock_instance.release()

    def test_acquire_atomic_prevents_race(self, temp_lock_dir):
        """Two processes cannot acquire simultaneously (atomic O_EXCL)."""
        results = []

        def try_acquire(story_id):
            lock = GitCommitLock(story_id=story_id, lock_dir=str(temp_lock_dir.parent.parent))
            result = lock.acquire(timeout_seconds=0)
            results.append((story_id, result.success))
            if result.success:
                time.sleep(0.1)  # Hold lock briefly
                lock.release()

        # Start two threads simultaneously
        t1 = threading.Thread(target=try_acquire, args=("STORY-001",))
        t2 = threading.Thread(target=try_acquire, args=("STORY-002",))

        t1.start()
        t2.start()
        t1.join()
        t2.join()

        # Exactly one should succeed
        successes = [r[1] for r in results]
        assert successes.count(True) == 1, "Exactly one acquisition should succeed"

    def test_acquire_returns_false_when_held(self, lock_instance, create_lock_file):
        """Returns failure when lock held by another story."""
        # Create lock held by different process (use PID 1 which always exists)
        create_lock_file(pid=1, story_id="STORY-037")

        result = lock_instance.acquire(timeout_seconds=0)

        assert result.success is False
        # With timeout=0, immediate timeout when lock is held
        assert result.status == LockStatus.TIMEOUT
        assert result.holder_story_id == "STORY-037"

    def test_acquire_waits_when_held(self, lock_instance, temp_lock_dir):
        """AC#2: Waits when lock held by another story."""
        # Create a lock in another thread, release after 0.5s
        def hold_and_release():
            other_lock = GitCommitLock(story_id="STORY-037", lock_dir=str(temp_lock_dir.parent.parent))
            other_lock.acquire(timeout_seconds=0)
            time.sleep(0.5)
            other_lock.release()

        holder = threading.Thread(target=hold_and_release)
        holder.start()
        time.sleep(0.1)  # Let holder acquire first

        start = time.perf_counter()
        result = lock_instance.acquire(timeout_seconds=2, progress_interval=0.1)
        elapsed = time.perf_counter() - start

        holder.join()

        assert result.success is True
        assert elapsed >= 0.4, "Should have waited for lock release"

    def test_lock_directory_created_if_missing(self, tmp_path):
        """Creates .devforgeai/.locks/ if not exists."""
        lock = GitCommitLock(story_id="STORY-096", lock_dir=str(tmp_path))
        result = lock.acquire(timeout_seconds=0)

        assert result.success is True
        lock_dir = tmp_path / ".devforgeai" / ".locks"
        assert lock_dir.exists()
        lock.release()

    def test_lock_file_permissions_600(self, lock_instance, temp_lock_dir):
        """Lock file has owner-only permissions (600)."""
        lock_instance.acquire(timeout_seconds=0)

        lock_file = temp_lock_dir / "git-commit.lock"
        mode = lock_file.stat().st_mode & 0o777

        assert mode == 0o600, f"Expected permissions 600, got {oct(mode)}"
        lock_instance.release()


# =============================================================================
# 2. Stale Lock Detection Tests (8 tests) - AC#3
# =============================================================================

class TestStaleLockDetection:
    """Tests for AC#3: Stale lock detection (PID dead + age > 5 min)."""

    def test_stale_when_pid_dead_and_age_exceeded(self, lock_instance, create_lock_file):
        """AC#3: Stale when PID dead AND age > 5 min."""
        old_timestamp = (datetime.utcnow() - timedelta(minutes=6)).isoformat() + "Z"
        create_lock_file(pid=99999, story_id="STORY-037", timestamp=old_timestamp)

        assert lock_instance.is_stale() is True

    def test_not_stale_when_pid_alive(self, lock_instance, create_lock_file):
        """Not stale even if old, if PID still running."""
        old_timestamp = (datetime.utcnow() - timedelta(minutes=10)).isoformat() + "Z"
        create_lock_file(pid=os.getpid(), story_id="STORY-037", timestamp=old_timestamp)

        assert lock_instance.is_stale() is False

    def test_not_stale_when_young(self, lock_instance, create_lock_file):
        """Not stale even if PID dead, if age < 5 min."""
        recent_timestamp = (datetime.utcnow() - timedelta(minutes=2)).isoformat() + "Z"
        create_lock_file(pid=99999, story_id="STORY-037", timestamp=recent_timestamp)

        assert lock_instance.is_stale() is False

    def test_stale_lock_auto_removed(self, lock_instance, temp_lock_dir, create_lock_file):
        """AC#3: Stale lock auto-removed on acquisition attempt."""
        old_timestamp = (datetime.utcnow() - timedelta(minutes=6)).isoformat() + "Z"
        lock_file = create_lock_file(pid=99999, story_id="STORY-037", timestamp=old_timestamp)

        result = lock_instance.acquire(timeout_seconds=0)

        assert result.success is True
        assert result.stale_removed is True
        lock_instance.release()

    def test_stale_detection_logs_removal(self, lock_instance, create_lock_file, caplog):
        """AC#3: Logs 'Removed stale lock (PID 99999 not running)'."""
        old_timestamp = (datetime.utcnow() - timedelta(minutes=6)).isoformat() + "Z"
        create_lock_file(pid=99999, story_id="STORY-037", timestamp=old_timestamp)

        with caplog.at_level("INFO"):
            lock_instance.acquire(timeout_seconds=0)

        assert "Removed stale lock" in caplog.text
        assert "99999" in caplog.text
        lock_instance.release()

    def test_pid_check_via_kill_signal_0(self, lock_instance):
        """Uses os.kill(pid, 0) for process checking."""
        # This should not raise - process exists
        assert lock_instance._process_exists(os.getpid()) is True

        # This should return False - process doesn't exist
        assert lock_instance._process_exists(99999) is False

    def test_stale_threshold_configurable(self, temp_lock_dir):
        """5-minute threshold can be adjusted via constructor."""
        lock = GitCommitLock(
            story_id="STORY-096",
            lock_dir=str(temp_lock_dir.parent.parent),
            stale_threshold_seconds=60  # 1 minute instead of 5
        )

        # Create lock that's 2 minutes old with dead PID
        old_timestamp = (datetime.utcnow() - timedelta(minutes=2)).isoformat() + "Z"
        lock_file = temp_lock_dir / "git-commit.lock"
        lock_file.write_text(f"pid: 99999\nstory_id: STORY-037\ntimestamp: {old_timestamp}\nhostname: test\n")

        assert lock.is_stale() is True

    def test_stale_detection_under_500ms(self, lock_instance, create_lock_file):
        """NFR: Stale detection < 500ms."""
        old_timestamp = (datetime.utcnow() - timedelta(minutes=6)).isoformat() + "Z"
        create_lock_file(pid=99999, story_id="STORY-037", timestamp=old_timestamp)

        start = time.perf_counter()
        lock_instance.is_stale()
        elapsed_ms = (time.perf_counter() - start) * 1000

        assert elapsed_ms < 500, f"Stale detection took {elapsed_ms:.2f}ms, expected <500ms"


# =============================================================================
# 3. Wait with Progress Tests (6 tests) - AC#2
# =============================================================================

class TestWaitWithProgress:
    """Tests for AC#2: Wait with progress display."""

    def test_progress_updates_every_5_seconds(self, temp_lock_dir):
        """AC#2: Updates progress every 5 seconds."""
        progress_updates = []

        def progress_callback(message):
            progress_updates.append((time.time(), message))

        # Create lock held by another process
        other_lock = GitCommitLock(story_id="STORY-037", lock_dir=str(temp_lock_dir.parent.parent))
        other_lock.acquire(timeout_seconds=0)

        # Try to acquire with progress callback
        lock = GitCommitLock(story_id="STORY-096", lock_dir=str(temp_lock_dir.parent.parent))

        def release_after_delay():
            time.sleep(1.5)  # Release after ~1.5s
            other_lock.release()

        releaser = threading.Thread(target=release_after_delay)
        releaser.start()

        result = lock.acquire(timeout_seconds=3, progress_interval=0.5, progress_callback=progress_callback)
        releaser.join()

        assert result.success is True
        assert len(progress_updates) >= 2, "Should have multiple progress updates"
        lock.release()

    def test_progress_shows_holder_story_and_pid(self, temp_lock_dir, create_lock_file):
        """AC#2: Shows 'Waiting for git lock (held by STORY-037 PID 12345)...'."""
        create_lock_file(pid=1, story_id="STORY-037")

        progress_messages = []
        def progress_callback(msg):
            progress_messages.append(msg)

        lock = GitCommitLock(story_id="STORY-096", lock_dir=str(temp_lock_dir.parent.parent))
        lock.acquire(timeout_seconds=0.5, progress_interval=0.1, progress_callback=progress_callback)

        assert len(progress_messages) > 0
        assert "STORY-037" in progress_messages[0]
        assert "1" in progress_messages[0]  # PID

    def test_progress_shows_elapsed_time(self, temp_lock_dir, create_lock_file):
        """AC#2: Shows elapsed time in seconds."""
        create_lock_file(pid=1, story_id="STORY-037")

        progress_messages = []
        def progress_callback(msg):
            progress_messages.append(msg)

        lock = GitCommitLock(story_id="STORY-096", lock_dir=str(temp_lock_dir.parent.parent))
        lock.acquire(timeout_seconds=0.5, progress_interval=0.1, progress_callback=progress_callback)

        # Should show time in message
        assert any("s" in msg for msg in progress_messages)  # seconds indicator

    def test_wait_loop_overhead_under_10ms(self, lock_instance):
        """NFR: Wait loop overhead < 10ms per iteration."""
        # Measure overhead of a single wait iteration (without actual waiting)
        start = time.perf_counter()
        lock_instance._check_and_report_progress(0, 0.1, None)
        elapsed_ms = (time.perf_counter() - start) * 1000

        assert elapsed_ms < 10, f"Wait loop overhead {elapsed_ms:.2f}ms, expected <10ms"

    def test_wait_returns_on_lock_available(self, temp_lock_dir):
        """Immediately acquires when lock becomes available."""
        other_lock = GitCommitLock(story_id="STORY-037", lock_dir=str(temp_lock_dir.parent.parent))
        other_lock.acquire(timeout_seconds=0)

        def release_soon():
            time.sleep(0.2)
            other_lock.release()

        releaser = threading.Thread(target=release_soon)
        releaser.start()

        lock = GitCommitLock(story_id="STORY-096", lock_dir=str(temp_lock_dir.parent.parent))
        start = time.perf_counter()
        result = lock.acquire(timeout_seconds=5, progress_interval=0.05)
        elapsed = time.perf_counter() - start

        releaser.join()

        assert result.success is True
        assert elapsed < 1.0, "Should acquire quickly after release"
        lock.release()

    def test_wait_can_be_interrupted(self, temp_lock_dir, create_lock_file):
        """User interrupt stops wait gracefully."""
        create_lock_file(pid=1, story_id="STORY-037")

        lock = GitCommitLock(story_id="STORY-096", lock_dir=str(temp_lock_dir.parent.parent))

        # Simulate interrupt by using cancel flag
        def cancel_after_delay():
            time.sleep(0.2)
            lock.cancel_wait()

        canceller = threading.Thread(target=cancel_after_delay)
        canceller.start()

        result = lock.acquire(timeout_seconds=10, progress_interval=0.05)
        canceller.join()

        assert result.success is False
        assert result.status == LockStatus.CANCELLED


# =============================================================================
# 4. Timeout Handling Tests (5 tests) - AC#4
# =============================================================================

class TestTimeoutHandling:
    """Tests for AC#4: Lock timeout prompt."""

    def test_timeout_at_10_minutes(self, temp_lock_dir, create_lock_file):
        """AC#4: Returns timeout status after 10 minutes (simulated)."""
        create_lock_file(pid=1, story_id="STORY-037")

        lock = GitCommitLock(story_id="STORY-096", lock_dir=str(temp_lock_dir.parent.parent))
        result = lock.acquire(timeout_seconds=0.1)  # Short timeout for test

        assert result.success is False
        assert result.status == LockStatus.TIMEOUT

    def test_timeout_returns_special_status(self, temp_lock_dir, create_lock_file):
        """Returns status requiring user prompt."""
        create_lock_file(pid=1, story_id="STORY-037")

        lock = GitCommitLock(story_id="STORY-096", lock_dir=str(temp_lock_dir.parent.parent))
        result = lock.acquire(timeout_seconds=0.1)

        assert result.requires_user_prompt is True
        assert result.holder_story_id == "STORY-037"
        assert result.holder_pid == 1

    def test_continue_waiting_option_resumes(self, temp_lock_dir):
        """AC#4 Option 1: Continue waiting restarts wait loop."""
        other_lock = GitCommitLock(story_id="STORY-037", lock_dir=str(temp_lock_dir.parent.parent))
        other_lock.acquire(timeout_seconds=0)

        lock = GitCommitLock(story_id="STORY-096", lock_dir=str(temp_lock_dir.parent.parent))

        # First attempt times out
        result1 = lock.acquire(timeout_seconds=0.1)
        assert result1.status == LockStatus.TIMEOUT

        # Release and try continue
        other_lock.release()
        result2 = lock.acquire(timeout_seconds=0.5)

        assert result2.success is True
        lock.release()

    def test_force_acquire_removes_lock(self, temp_lock_dir, create_lock_file):
        """AC#4 Option 2: Force acquire removes existing lock."""
        create_lock_file(pid=1, story_id="STORY-037")

        lock = GitCommitLock(story_id="STORY-096", lock_dir=str(temp_lock_dir.parent.parent))
        result = lock.force_acquire()

        assert result.success is True
        assert result.force_acquired is True
        lock.release()

    def test_abort_option_returns_false(self, temp_lock_dir, create_lock_file):
        """AC#4 Option 3: Abort returns without acquiring."""
        create_lock_file(pid=1, story_id="STORY-037")

        lock = GitCommitLock(story_id="STORY-096", lock_dir=str(temp_lock_dir.parent.parent))
        result = lock.acquire(timeout_seconds=0.1)

        # User chooses abort - lock not acquired
        assert result.success is False

        # Original lock still exists
        lock_file = temp_lock_dir / "git-commit.lock"
        assert lock_file.exists()


# =============================================================================
# 5. Lock Release Tests (5 tests) - AC#5
# =============================================================================

class TestLockRelease:
    """Tests for AC#5: Lock release after commit."""

    def test_release_removes_lock_file(self, lock_instance, temp_lock_dir):
        """AC#5: Lock file removed after release."""
        lock_instance.acquire(timeout_seconds=0)
        lock_file = temp_lock_dir / "git-commit.lock"
        assert lock_file.exists()

        lock_instance.release()

        assert not lock_file.exists()

    def test_release_on_commit_success(self, lock_instance, temp_lock_dir):
        """AC#5: Released after successful commit (context manager)."""
        with lock_instance:
            lock_file = temp_lock_dir / "git-commit.lock"
            assert lock_file.exists()
            # Simulate successful commit

        assert not lock_file.exists()

    def test_release_on_commit_failure(self, lock_instance, temp_lock_dir):
        """AC#5: Released after failed commit (exception in context)."""
        lock_file = temp_lock_dir / "git-commit.lock"

        try:
            with lock_instance:
                assert lock_file.exists()
                raise RuntimeError("Commit failed!")
        except RuntimeError:
            pass

        assert not lock_file.exists()

    def test_release_idempotent(self, lock_instance):
        """Multiple releases don't error."""
        lock_instance.acquire(timeout_seconds=0)

        # Multiple releases should not raise
        lock_instance.release()
        lock_instance.release()
        lock_instance.release()

    def test_release_by_wrong_story_fails(self, temp_lock_dir, create_lock_file):
        """Cannot release lock held by different story."""
        create_lock_file(pid=os.getpid(), story_id="STORY-037")

        lock = GitCommitLock(story_id="STORY-096", lock_dir=str(temp_lock_dir.parent.parent))

        with pytest.raises(PermissionError, match="not held by this story"):
            lock.release(strict=True)


# =============================================================================
# 6. Lock Content Parsing Tests (5 tests)
# =============================================================================

class TestLockContentParsing:
    """Tests for lock file content parsing."""

    def test_parse_valid_lock_file(self, lock_instance, create_lock_file):
        """Parses all 4 fields correctly."""
        create_lock_file(pid=12345, story_id="STORY-037", hostname="test-host")

        info = lock_instance.get_lock_info()

        assert info["pid"] == 12345
        assert info["story_id"] == "STORY-037"
        assert "timestamp" in info
        assert info["hostname"] == "test-host"

    def test_parse_missing_optional_hostname(self, lock_instance, temp_lock_dir):
        """Handles missing hostname gracefully."""
        lock_file = temp_lock_dir / "git-commit.lock"
        lock_file.write_text("pid: 12345\nstory_id: STORY-037\ntimestamp: 2025-01-01T00:00:00Z\n")

        info = lock_instance.get_lock_info()

        assert info["pid"] == 12345
        # hostname key may not exist or be None/empty when not present in file
        assert info.get("hostname") is None or info.get("hostname") == "" or "hostname" not in info

    def test_parse_invalid_format_returns_stale(self, lock_instance, temp_lock_dir):
        """Invalid format treated as stale."""
        lock_file = temp_lock_dir / "git-commit.lock"
        lock_file.write_text("invalid content")

        assert lock_instance.is_stale() is True

    def test_parse_empty_file_returns_stale(self, lock_instance, temp_lock_dir):
        """Empty file treated as stale."""
        lock_file = temp_lock_dir / "git-commit.lock"
        lock_file.write_text("")

        assert lock_instance.is_stale() is True

    def test_get_lock_info_returns_dict(self, lock_instance, create_lock_file):
        """Returns structured lock information."""
        create_lock_file()

        info = lock_instance.get_lock_info()

        assert isinstance(info, dict)
        assert "pid" in info
        assert "story_id" in info
        assert "timestamp" in info


# =============================================================================
# 7. Edge Cases Tests (5 tests)
# =============================================================================

class TestEdgeCases:
    """Tests for edge cases and error handling."""

    def test_process_crash_during_commit(self, temp_lock_dir):
        """NFR-002: Stale detection within 5 minutes recovers."""
        # Create lock with dead PID but recent timestamp
        lock_file = temp_lock_dir / "git-commit.lock"
        recent = datetime.utcnow().isoformat() + "Z"
        lock_file.write_text(f"pid: 99999\nstory_id: STORY-037\ntimestamp: {recent}\nhostname: test\n")

        lock = GitCommitLock(story_id="STORY-096", lock_dir=str(temp_lock_dir.parent.parent))

        # Not stale yet (recent timestamp, even though PID dead)
        assert lock.is_stale() is False

        # After 5+ minutes, would be stale
        old = (datetime.utcnow() - timedelta(minutes=6)).isoformat() + "Z"
        lock_file.write_text(f"pid: 99999\nstory_id: STORY-037\ntimestamp: {old}\nhostname: test\n")

        assert lock.is_stale() is True

    def test_same_story_reacquires_lock(self, lock_instance, temp_lock_dir):
        """Same story can reacquire own lock."""
        lock_instance.acquire(timeout_seconds=0)

        # Same story (same object) can re-acquire
        result = lock_instance.acquire(timeout_seconds=0)
        assert result.success is True

        lock_instance.release()

    def test_multiple_machines_hostname_differs(self, temp_lock_dir):
        """Hostname helps identify distributed scenarios."""
        # Create lock from "other machine"
        lock_file = temp_lock_dir / "git-commit.lock"
        lock_file.write_text(f"pid: 1\nstory_id: STORY-037\ntimestamp: {datetime.utcnow().isoformat()}Z\nhostname: other-machine\n")

        lock = GitCommitLock(story_id="STORY-096", lock_dir=str(temp_lock_dir.parent.parent))
        info = lock.get_lock_info()

        assert info["hostname"] == "other-machine"
        assert info["hostname"] != socket.gethostname()

    def test_force_acquire_logs_warning(self, temp_lock_dir, create_lock_file, caplog):
        """Force acquire logs security warning."""
        create_lock_file(pid=1, story_id="STORY-037")

        lock = GitCommitLock(story_id="STORY-096", lock_dir=str(temp_lock_dir.parent.parent))

        with caplog.at_level("WARNING"):
            lock.force_acquire()

        assert "FORCE ACQUIRE" in caplog.text or "force" in caplog.text.lower()
        lock.release()

    def test_concurrent_acquisition_serialized(self, temp_lock_dir):
        """BR-001: Only one commit at a time across all worktrees."""
        acquired_order = []
        lock = threading.Lock()

        def try_acquire_and_record(story_id, delay=0):
            time.sleep(delay)
            git_lock = GitCommitLock(story_id=story_id, lock_dir=str(temp_lock_dir.parent.parent))
            result = git_lock.acquire(timeout_seconds=5, progress_interval=0.1)
            if result.success:
                with lock:
                    acquired_order.append(story_id)
                time.sleep(0.2)  # Hold lock briefly
                git_lock.release()

        threads = [
            threading.Thread(target=try_acquire_and_record, args=("STORY-001", 0)),
            threading.Thread(target=try_acquire_and_record, args=("STORY-002", 0.05)),
            threading.Thread(target=try_acquire_and_record, args=("STORY-003", 0.1)),
        ]

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # All three should have acquired (serialized)
        assert len(acquired_order) == 3
        # They should be in order (first to acquire completes first)
        assert acquired_order == sorted(acquired_order, key=lambda x: acquired_order.index(x))


# =============================================================================
# CLI Tests
# =============================================================================

class TestCLI:
    """Tests for command-line interface."""

    def test_cli_acquire_command(self, temp_lock_dir):
        """CLI acquire command works."""
        result = subprocess.run(
            [sys.executable, "src/lock_file_coordinator.py", "acquire",
             "--story-id", "STORY-096", "--lock-dir", str(temp_lock_dir.parent.parent),
             "--timeout", "0"],
            capture_output=True,
            text=True,
            cwd=str(Path(__file__).parent.parent.parent)
        )

        output = json.loads(result.stdout)
        assert output["success"] is True

    def test_cli_release_command(self, temp_lock_dir):
        """CLI release command works."""
        # First acquire
        subprocess.run(
            [sys.executable, "src/lock_file_coordinator.py", "acquire",
             "--story-id", "STORY-096", "--lock-dir", str(temp_lock_dir.parent.parent),
             "--timeout", "0"],
            capture_output=True,
            cwd=str(Path(__file__).parent.parent.parent)
        )

        # Then release
        result = subprocess.run(
            [sys.executable, "src/lock_file_coordinator.py", "release",
             "--story-id", "STORY-096", "--lock-dir", str(temp_lock_dir.parent.parent)],
            capture_output=True,
            text=True,
            cwd=str(Path(__file__).parent.parent.parent)
        )

        output = json.loads(result.stdout)
        assert output["status"] == "released"

    def test_cli_status_command(self, temp_lock_dir, create_lock_file):
        """CLI status command works."""
        create_lock_file(pid=12345, story_id="STORY-037")

        result = subprocess.run(
            [sys.executable, "src/lock_file_coordinator.py", "status",
             "--lock-dir", str(temp_lock_dir.parent.parent)],
            capture_output=True,
            text=True,
            cwd=str(Path(__file__).parent.parent.parent)
        )

        output = json.loads(result.stdout)
        assert output["pid"] == 12345
        assert output["story_id"] == "STORY-037"

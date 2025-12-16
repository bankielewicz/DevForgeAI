"""
Test concurrent execution handling for story-scoped test isolation.

Tests AC#7: Concurrent Execution Verification
- Lock file creation during QA
- Stale lock detection and removal
- Concurrent access handling
"""
import os
import time
import tempfile
import threading
import pytest
from pathlib import Path
from datetime import datetime, timedelta


def create_lock_file(story_id: str, base_path: str, config: dict) -> bool:
    """
    Create lock file for story test outputs.

    Args:
        story_id: Story identifier (e.g., "STORY-092")
        base_path: Project root path
        config: Test isolation configuration

    Returns:
        True if lock acquired, False if timeout exceeded
    """
    concurrency = config.get("concurrency", {})

    if not concurrency.get("locking_enabled", True):
        return True  # Locking disabled

    paths = config.get("paths", {})
    results_base = paths.get("results_base", "tests/results")
    lock_pattern = concurrency.get("lock_file_pattern", ".qa-lock")
    lock_timeout = concurrency.get("lock_timeout_seconds", 300)
    stale_threshold = concurrency.get("stale_lock_threshold_seconds", 3600)

    lock_file = Path(base_path) / results_base / story_id / lock_pattern
    lock_file.parent.mkdir(parents=True, exist_ok=True)

    start_time = time.time()

    while time.time() - start_time < lock_timeout:
        if not lock_file.exists():
            # Create lock file
            lock_content = (
                f"timestamp: {datetime.utcnow().isoformat()}Z\n"
                f"story: {story_id}\n"
                f"pid: {os.getpid()}\n"
            )
            lock_file.write_text(lock_content)
            return True

        # Check if existing lock is stale
        lock_age = time.time() - lock_file.stat().st_mtime
        if lock_age > stale_threshold:
            # Remove stale lock and retry
            lock_file.unlink()
            continue

        # Wait and retry
        time.sleep(0.1)  # Short sleep for testing

    return False


def release_lock_file(story_id: str, base_path: str, config: dict) -> bool:
    """
    Release lock file for story test outputs.

    Returns:
        True if lock released, False if lock didn't exist
    """
    paths = config.get("paths", {})
    concurrency = config.get("concurrency", {})

    results_base = paths.get("results_base", "tests/results")
    lock_pattern = concurrency.get("lock_file_pattern", ".qa-lock")

    lock_file = Path(base_path) / results_base / story_id / lock_pattern

    if lock_file.exists():
        lock_file.unlink()
        return True
    return False


def is_lock_stale(lock_file: Path, threshold_seconds: int) -> bool:
    """Check if lock file is stale (older than threshold)."""
    if not lock_file.exists():
        return False

    lock_age = time.time() - lock_file.stat().st_mtime
    return lock_age > threshold_seconds


class TestLockFileCreation:
    """Tests for lock file creation."""

    @pytest.fixture
    def default_config(self):
        return {
            "paths": {"results_base": "tests/results"},
            "concurrency": {
                "locking_enabled": True,
                "lock_file_pattern": ".qa-lock",
                "lock_timeout_seconds": 1,  # Short for testing
                "stale_lock_threshold_seconds": 0.5  # Short for testing
            }
        }

    def test_lock_file_created_during_qa(self, tmp_path, default_config):
        """Test: Lock file created during QA."""
        # Given: Story ID
        story_id = "STORY-092"

        # When: Acquiring lock
        success = create_lock_file(story_id, str(tmp_path), default_config)

        # Then: Lock file exists
        assert success
        lock_file = tmp_path / "tests" / "results" / story_id / ".qa-lock"
        assert lock_file.exists()

    def test_lock_file_contains_metadata(self, tmp_path, default_config):
        """Test: Lock file contains timestamp, story, pid."""
        # Given: Story ID
        story_id = "STORY-092"

        # When: Creating lock
        create_lock_file(story_id, str(tmp_path), default_config)

        # Then: Lock file contains required metadata
        lock_file = tmp_path / "tests" / "results" / story_id / ".qa-lock"
        content = lock_file.read_text()

        assert "timestamp:" in content
        assert f"story: {story_id}" in content
        assert "pid:" in content

    def test_lock_released_successfully(self, tmp_path, default_config):
        """Test: Lock file removed on release."""
        # Given: Existing lock
        story_id = "STORY-092"
        create_lock_file(story_id, str(tmp_path), default_config)

        # When: Releasing lock
        released = release_lock_file(story_id, str(tmp_path), default_config)

        # Then: Lock file removed
        assert released
        lock_file = tmp_path / "tests" / "results" / story_id / ".qa-lock"
        assert not lock_file.exists()


class TestStaleLockDetection:
    """Tests for stale lock detection."""

    @pytest.fixture
    def default_config(self):
        return {
            "paths": {"results_base": "tests/results"},
            "concurrency": {
                "locking_enabled": True,
                "lock_file_pattern": ".qa-lock",
                "lock_timeout_seconds": 2,
                "stale_lock_threshold_seconds": 0.1  # Very short for testing
            }
        }

    def test_stale_lock_detected(self, tmp_path):
        """Test: Stale lock detected based on age."""
        # Given: Old lock file
        story_id = "STORY-092"
        lock_dir = tmp_path / "tests" / "results" / story_id
        lock_dir.mkdir(parents=True)
        lock_file = lock_dir / ".qa-lock"
        lock_file.write_text("timestamp: old\nstory: STORY-092\npid: 1234")

        # Backdate the file
        old_time = time.time() - 100  # 100 seconds ago
        os.utime(lock_file, (old_time, old_time))

        # When: Checking staleness
        stale = is_lock_stale(lock_file, threshold_seconds=60)

        # Then: Lock is stale
        assert stale

    def test_fresh_lock_not_stale(self, tmp_path):
        """Test: Fresh lock not marked as stale."""
        # Given: Fresh lock file
        story_id = "STORY-092"
        lock_dir = tmp_path / "tests" / "results" / story_id
        lock_dir.mkdir(parents=True)
        lock_file = lock_dir / ".qa-lock"
        lock_file.write_text("timestamp: now\nstory: STORY-092\npid: 1234")

        # When: Checking staleness
        stale = is_lock_stale(lock_file, threshold_seconds=60)

        # Then: Lock is not stale
        assert not stale

    def test_stale_lock_removed_on_acquire(self, tmp_path, default_config):
        """Test: Stale lock removed when acquiring new lock."""
        # Given: Stale lock file
        story_id = "STORY-092"
        lock_dir = tmp_path / "tests" / "results" / story_id
        lock_dir.mkdir(parents=True)
        lock_file = lock_dir / ".qa-lock"
        lock_file.write_text("timestamp: old\nstory: STORY-092\npid: 1234")

        # Backdate to make stale
        old_time = time.time() - 1  # 1 second ago (threshold is 0.1)
        os.utime(lock_file, (old_time, old_time))

        # When: Acquiring lock
        success = create_lock_file(story_id, str(tmp_path), default_config)

        # Then: Lock acquired (stale lock was removed)
        assert success


class TestConcurrentAccess:
    """Tests for concurrent access handling."""

    @pytest.fixture
    def default_config(self):
        return {
            "paths": {"results_base": "tests/results"},
            "concurrency": {
                "locking_enabled": True,
                "lock_file_pattern": ".qa-lock",
                "lock_timeout_seconds": 0.5,  # Short timeout for testing
                "stale_lock_threshold_seconds": 10
            }
        }

    def test_concurrent_lock_blocked(self, tmp_path, default_config):
        """Test: Second lock request blocked when first holds lock."""
        story_id = "STORY-092"
        results = {"first": None, "second": None}

        def acquire_first():
            results["first"] = create_lock_file(story_id, str(tmp_path), default_config)
            time.sleep(0.3)  # Hold lock

        def acquire_second():
            time.sleep(0.1)  # Ensure first acquires first
            results["second"] = create_lock_file(story_id, str(tmp_path), default_config)

        # When: Two threads try to acquire
        t1 = threading.Thread(target=acquire_first)
        t2 = threading.Thread(target=acquire_second)

        t1.start()
        t2.start()
        t1.join()
        t2.join()

        # Then: First succeeds, second times out
        assert results["first"] == True
        assert results["second"] == False

    def test_lock_released_allows_next(self, tmp_path, default_config):
        """Test: Released lock allows next acquisition."""
        story_id = "STORY-092"

        # Given: First lock acquired and released
        create_lock_file(story_id, str(tmp_path), default_config)
        release_lock_file(story_id, str(tmp_path), default_config)

        # When: Second lock requested
        success = create_lock_file(story_id, str(tmp_path), default_config)

        # Then: Second lock succeeds
        assert success

    def test_different_stories_not_blocked(self, tmp_path, default_config):
        """Test: Different stories can be locked concurrently."""
        # When: Locking different stories
        success1 = create_lock_file("STORY-091", str(tmp_path), default_config)
        success2 = create_lock_file("STORY-092", str(tmp_path), default_config)

        # Then: Both succeed (independent locks)
        assert success1
        assert success2

    def test_locking_disabled_always_succeeds(self, tmp_path):
        """Test: Disabled locking always returns True."""
        # Given: Locking disabled
        config = {
            "paths": {"results_base": "tests/results"},
            "concurrency": {"locking_enabled": False}
        }

        # When: Multiple lock attempts (locking disabled)
        success1 = create_lock_file("STORY-092", str(tmp_path), config)
        success2 = create_lock_file("STORY-092", str(tmp_path), config)

        # Then: Both succeed (locking bypassed)
        assert success1
        assert success2

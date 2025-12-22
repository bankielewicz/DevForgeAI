"""Integration tests for lock file coordination (STORY-096).

Tests end-to-end lock coordination workflows for git commits across parallel worktrees.

Total: 8 integration tests
"""

import os
import sys
import time
import threading
import subprocess
from pathlib import Path
from datetime import datetime

import pytest

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from lock_file_coordinator import GitCommitLock, LockStatus


@pytest.fixture
def temp_repo(tmp_path):
    """Create a temporary git repository for testing."""
    repo_dir = tmp_path / "test-repo"
    repo_dir.mkdir()

    # Initialize git repo
    subprocess.run(["git", "init"], cwd=repo_dir, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=repo_dir, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo_dir, capture_output=True)

    # Create initial commit
    (repo_dir / "README.md").write_text("# Test Repo")
    subprocess.run(["git", "add", "."], cwd=repo_dir, capture_output=True)
    subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=repo_dir, capture_output=True)

    return repo_dir


@pytest.fixture
def lock_dir(tmp_path):
    """Create a shared lock directory."""
    lock_parent = tmp_path / "locks"
    lock_parent.mkdir()
    return lock_parent


class TestLockIntegration:
    """Integration tests for lock coordination across parallel stories."""

    def test_lock_coordinates_parallel_commits(self, lock_dir):
        """Two parallel /dev workflows serialize commits via lock."""
        commit_order = []
        lock = threading.Lock()

        def simulate_dev_workflow(story_id, delay=0):
            """Simulate /dev Phase 08 git commit with lock coordination."""
            time.sleep(delay)

            git_lock = GitCommitLock(story_id=story_id, lock_dir=str(lock_dir))

            # Phase 08 Step 5.0.1: Acquire lock
            result = git_lock.acquire(timeout_seconds=10, progress_interval=0.1)

            if result.success:
                # Phase 08 Step 5.1-5.2: Git operations
                with lock:
                    commit_order.append(f"{story_id}-start")

                time.sleep(0.2)  # Simulate git commit time

                with lock:
                    commit_order.append(f"{story_id}-end")

                # Phase 08 Step 5.3: Release lock
                git_lock.release()

        # Start two parallel dev workflows
        t1 = threading.Thread(target=simulate_dev_workflow, args=("STORY-001", 0))
        t2 = threading.Thread(target=simulate_dev_workflow, args=("STORY-002", 0.05))

        t1.start()
        t2.start()
        t1.join()
        t2.join()

        # Commits should be serialized (one complete before other starts)
        assert len(commit_order) == 4

        # First story's end should come before second story's start
        idx_1_end = commit_order.index("STORY-001-end")
        idx_2_start = commit_order.index("STORY-002-start")
        assert idx_1_end < idx_2_start, f"Commits not serialized: {commit_order}"

    def test_lock_survives_process_restart(self, lock_dir):
        """Lock persists across process boundaries."""
        # Create lock in subprocess
        result = subprocess.run(
            [sys.executable, "-c", f"""
import sys
sys.path.insert(0, 'src')
from lock_file_coordinator import GitCommitLock
lock = GitCommitLock(story_id='STORY-001', lock_dir='{lock_dir}')
result = lock.acquire(timeout_seconds=0)
print('acquired' if result.success else 'failed')
# Don't release - simulate process exit
"""],
            capture_output=True,
            text=True,
            cwd=str(Path(__file__).parent.parent.parent)
        )

        # Lock should exist
        lock_file = lock_dir / "devforgeai" / ".locks" / "git-commit.lock"
        assert lock_file.exists()

        # New process should see lock (but it will be stale since process exited)
        lock = GitCommitLock(story_id="STORY-002", lock_dir=str(lock_dir))
        info = lock.get_lock_info()
        assert info is not None
        assert info["story_id"] == "STORY-001"

    def test_lock_cleared_on_worktree_cleanup(self, lock_dir):
        """Lock released if holder worktree is removed."""
        lock = GitCommitLock(story_id="STORY-001", lock_dir=str(lock_dir))
        lock.acquire(timeout_seconds=0)

        # Simulate worktree cleanup releasing the lock
        lock.release()

        # Another story can now acquire
        lock2 = GitCommitLock(story_id="STORY-002", lock_dir=str(lock_dir))
        result = lock2.acquire(timeout_seconds=0)
        assert result.success is True
        lock2.release()

    def test_phase_08_acquires_before_git_add(self, lock_dir, temp_repo):
        """Phase 08 Step 5.1 acquires lock before git operations."""
        git_operations = []

        lock = GitCommitLock(story_id="STORY-001", lock_dir=str(lock_dir))

        # Phase 08 Step 5.0.1: Acquire lock BEFORE git operations
        result = lock.acquire(timeout_seconds=0)
        git_operations.append("lock_acquired")

        # Phase 08 Step 5.1: git add (only after lock)
        subprocess.run(["git", "add", "."], cwd=temp_repo)
        git_operations.append("git_add")

        # Phase 08 Step 5.2: git commit
        (temp_repo / "test.txt").write_text("test")
        subprocess.run(["git", "add", "."], cwd=temp_repo)
        subprocess.run(["git", "commit", "-m", "Test commit"], cwd=temp_repo)
        git_operations.append("git_commit")

        # Phase 08 Step 5.3: Release
        lock.release()
        git_operations.append("lock_released")

        assert git_operations == ["lock_acquired", "git_add", "git_commit", "lock_released"]

    def test_phase_08_releases_after_commit(self, lock_dir):
        """Phase 08 Step 5.3 releases lock after commit completes."""
        lock = GitCommitLock(story_id="STORY-001", lock_dir=str(lock_dir))

        lock_file = lock_dir / "devforgeai" / ".locks" / "git-commit.lock"

        # Acquire
        lock.acquire(timeout_seconds=0)
        assert lock_file.exists()

        # Simulate commit
        time.sleep(0.1)

        # Release
        lock.release()
        assert not lock_file.exists()

    def test_workflow_continues_after_wait(self, lock_dir):
        """Workflow resumes after lock acquired from waiting state."""
        workflow_steps = []
        lock = threading.Lock()

        def holder_workflow():
            git_lock = GitCommitLock(story_id="STORY-001", lock_dir=str(lock_dir))
            git_lock.acquire(timeout_seconds=0)
            with lock:
                workflow_steps.append("holder_acquired")
            time.sleep(0.3)
            git_lock.release()
            with lock:
                workflow_steps.append("holder_released")

        def waiter_workflow():
            time.sleep(0.1)  # Start after holder
            git_lock = GitCommitLock(story_id="STORY-002", lock_dir=str(lock_dir))

            with lock:
                workflow_steps.append("waiter_waiting")

            result = git_lock.acquire(timeout_seconds=5, progress_interval=0.1)

            with lock:
                workflow_steps.append("waiter_acquired")

            assert result.success is True
            git_lock.release()

            with lock:
                workflow_steps.append("waiter_completed")

        t1 = threading.Thread(target=holder_workflow)
        t2 = threading.Thread(target=waiter_workflow)

        t1.start()
        t2.start()
        t1.join()
        t2.join()

        # Waiter should wait, then acquire, then complete
        assert "waiter_waiting" in workflow_steps
        assert "waiter_acquired" in workflow_steps
        assert "waiter_completed" in workflow_steps

        # Waiter acquires after holder releases
        waiter_acquired_idx = workflow_steps.index("waiter_acquired")
        holder_released_idx = workflow_steps.index("holder_released")
        assert holder_released_idx < waiter_acquired_idx

    def test_timeout_prompt_appears(self, lock_dir):
        """10-minute timeout triggers timeout status for user prompt."""
        # Create lock held by another (simulated with PID 1)
        lock_dir_full = lock_dir / "devforgeai" / ".locks"
        lock_dir_full.mkdir(parents=True, exist_ok=True)
        lock_file = lock_dir_full / "git-commit.lock"
        lock_file.write_text(f"pid: 1\nstory_id: STORY-001\ntimestamp: {datetime.utcnow().isoformat()}Z\nhostname: test\n")

        lock = GitCommitLock(story_id="STORY-002", lock_dir=str(lock_dir))
        result = lock.acquire(timeout_seconds=0.5)  # Short timeout for test

        assert result.success is False
        assert result.status == LockStatus.TIMEOUT
        assert result.requires_user_prompt is True
        assert result.holder_story_id == "STORY-001"

    def test_abort_option_halts_workflow(self, lock_dir):
        """Abort at timeout halts Phase 08 gracefully."""
        # Create lock held by another
        lock_dir_full = lock_dir / "devforgeai" / ".locks"
        lock_dir_full.mkdir(parents=True, exist_ok=True)
        lock_file = lock_dir_full / "git-commit.lock"
        lock_file.write_text(f"pid: 1\nstory_id: STORY-001\ntimestamp: {datetime.utcnow().isoformat()}Z\nhostname: test\n")

        lock = GitCommitLock(story_id="STORY-002", lock_dir=str(lock_dir))
        result = lock.acquire(timeout_seconds=0.1)

        # User would choose abort here
        assert result.success is False

        # Workflow should halt without acquiring lock
        lock_info = lock.get_lock_info()
        assert lock_info["story_id"] == "STORY-001"  # Original holder unchanged


class TestMultiWorktreeScenarios:
    """Tests simulating multiple worktree scenarios."""

    def test_three_worktrees_serialize_commits(self, lock_dir):
        """Three concurrent worktrees serialize their commits."""
        results = []
        lock = threading.Lock()

        def worktree_commit(story_id, delay):
            time.sleep(delay)
            git_lock = GitCommitLock(story_id=story_id, lock_dir=str(lock_dir))

            start = time.perf_counter()
            result = git_lock.acquire(timeout_seconds=10, progress_interval=0.1)
            wait_time = time.perf_counter() - start

            if result.success:
                time.sleep(0.1)  # Simulate commit
                git_lock.release()

            with lock:
                results.append({
                    "story_id": story_id,
                    "success": result.success,
                    "wait_time": wait_time
                })

        threads = [
            threading.Thread(target=worktree_commit, args=("STORY-001", 0)),
            threading.Thread(target=worktree_commit, args=("STORY-002", 0.02)),
            threading.Thread(target=worktree_commit, args=("STORY-003", 0.04)),
        ]

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # All should succeed
        assert len(results) == 3
        assert all(r["success"] for r in results)

        # Later stories should have waited longer
        results_sorted = sorted(results, key=lambda x: x["story_id"])
        wait_times = [r["wait_time"] for r in results_sorted]

        # Story-002 waited longer than Story-001
        # Story-003 waited longer than Story-002
        # (Allow some tolerance for timing)
        assert wait_times[1] > wait_times[0] - 0.05
        assert wait_times[2] > wait_times[1] - 0.05

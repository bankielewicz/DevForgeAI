"""Lock file coordinator for serializing git commits across parallel worktrees (STORY-096).

Implements lock file coordination to prevent git index lock conflicts when multiple
worktrees commit simultaneously. Follows patterns from installer/services/lock_file_manager.py.

Key Features:
- AC#1: Lock acquisition with PID, story_id, timestamp, hostname
- AC#2: Wait with progress display (5-second updates)
- AC#3: Stale lock detection (PID dead + age > 5 minutes)
- AC#4: Timeout prompt after 10 minutes
- AC#5: Lock release after commit completes

Usage:
    # As Python module
    from lock_file_coordinator import GitCommitLock

    lock = GitCommitLock(story_id="STORY-096")
    result = lock.acquire(timeout_seconds=600)
    if result.success:
        # Do git operations
        lock.release()

    # As context manager
    with GitCommitLock(story_id="STORY-096") as lock:
        # Do git operations (auto-released)

    # CLI
    python lock_file_coordinator.py acquire --story-id STORY-096
    python lock_file_coordinator.py release --story-id STORY-096
    python lock_file_coordinator.py status
"""

import os
import sys
import json
import time
import socket
import logging
import argparse
from enum import Enum
from pathlib import Path
from datetime import datetime, timezone
from dataclasses import dataclass, field
from typing import Optional, Callable, Dict, Any

# Module-level constants
LOCK_DIR = ".devforgeai/.locks"
LOCK_FILE = "git-commit.lock"
STALE_THRESHOLD_SECONDS = 300  # 5 minutes
DEFAULT_TIMEOUT_SECONDS = 600  # 10 minutes
DEFAULT_PROGRESS_INTERVAL = 5  # 5 seconds

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


class LockStatus(Enum):
    """Status codes for lock acquisition results."""
    ACQUIRED = "acquired"
    HELD_BY_OTHER = "held_by_other"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"
    ERROR = "error"


@dataclass
class LockAcquisitionResult:
    """Result of a lock acquisition attempt."""
    success: bool
    status: LockStatus
    holder_pid: Optional[int] = None
    holder_story_id: Optional[str] = None
    holder_hostname: Optional[str] = None
    stale_removed: bool = False
    force_acquired: bool = False
    requires_user_prompt: bool = False
    error_message: Optional[str] = None
    wait_time_seconds: float = 0.0


class GitCommitLock:
    """Manages .devforgeai/.locks/git-commit.lock for serialized git commits.

    Implements lock coordination for parallel story development (EPIC-010).
    Prevents git index lock conflicts when multiple worktrees commit simultaneously.

    Attributes:
        story_id: Story ID requesting the lock (e.g., "STORY-096")
        lock_dir: Base directory for DevForgeAI (default: current working directory)
        stale_threshold_seconds: Age threshold for stale detection (default: 300s / 5 min)

    Example:
        >>> lock = GitCommitLock(story_id="STORY-096")
        >>> result = lock.acquire(timeout_seconds=600)
        >>> if result.success:
        ...     # Do git operations
        ...     lock.release()
    """

    def __init__(
        self,
        story_id: str,
        lock_dir: str = ".",
        stale_threshold_seconds: int = STALE_THRESHOLD_SECONDS
    ):
        """Initialize lock coordinator.

        Args:
            story_id: Story ID requesting the lock
            lock_dir: Base directory for DevForgeAI files
            stale_threshold_seconds: Age threshold for stale detection
        """
        self.story_id = story_id
        self.lock_dir = Path(lock_dir)
        self.lock_path = self.lock_dir / LOCK_DIR / LOCK_FILE
        self.stale_threshold_seconds = stale_threshold_seconds
        self._cancel_requested = False
        self._acquired = False

    def acquire(
        self,
        timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
        progress_interval: float = DEFAULT_PROGRESS_INTERVAL,
        progress_callback: Optional[Callable[[str], None]] = None
    ) -> LockAcquisitionResult:
        """Acquire lock with progress display and timeout.

        AC#1: Creates lock file with PID, story_id, timestamp, hostname.
        AC#2: Updates progress every progress_interval seconds while waiting.
        AC#3: Auto-removes stale locks (PID dead + age > threshold).
        AC#4: Returns timeout status after timeout_seconds for user prompt.

        Args:
            timeout_seconds: Maximum time to wait for lock (default: 600s / 10 min)
            progress_interval: Seconds between progress updates (default: 5s)
            progress_callback: Optional callback for progress messages

        Returns:
            LockAcquisitionResult with success status and metadata
        """
        self._cancel_requested = False
        start_time = time.time()
        stale_was_removed = False

        while True:
            # Check for cancellation
            if self._cancel_requested:
                return LockAcquisitionResult(
                    success=False,
                    status=LockStatus.CANCELLED,
                    wait_time_seconds=time.time() - start_time
                )

            # Ensure lock directory exists
            self.lock_path.parent.mkdir(parents=True, exist_ok=True)

            # Check for existing lock
            if self.lock_path.exists():
                # Check if we already hold the lock
                lock_info = self.get_lock_info()
                if lock_info and lock_info.get("story_id") == self.story_id:
                    # We already hold the lock
                    self._acquired = True
                    return LockAcquisitionResult(
                        success=True,
                        status=LockStatus.ACQUIRED,
                        stale_removed=stale_was_removed,
                        wait_time_seconds=time.time() - start_time
                    )

                # Check if lock is stale
                if self.is_stale():
                    stale_info = self.get_lock_info()
                    stale_pid = stale_info.get("pid") if stale_info else "unknown"
                    logger.info(f"Removed stale lock (PID {stale_pid} not running)")
                    try:
                        self.lock_path.unlink()
                        stale_was_removed = True
                    except OSError:
                        pass
                    # Retry acquisition
                    continue

                # Lock held by active process
                lock_info = self.get_lock_info()
                elapsed = time.time() - start_time

                # Check timeout
                if elapsed >= timeout_seconds:
                    return LockAcquisitionResult(
                        success=False,
                        status=LockStatus.TIMEOUT,
                        holder_pid=lock_info.get("pid") if lock_info else None,
                        holder_story_id=lock_info.get("story_id") if lock_info else None,
                        holder_hostname=lock_info.get("hostname") if lock_info else None,
                        requires_user_prompt=True,
                        wait_time_seconds=elapsed
                    )

                # Progress display
                self._check_and_report_progress(
                    elapsed, progress_interval, progress_callback, lock_info
                )

                # Wait and retry
                time.sleep(min(progress_interval, 0.1))
                continue

            # Try to create lock file atomically
            try:
                result = self._create_lock_file()
                if result:
                    self._acquired = True
                    return LockAcquisitionResult(
                        success=True,
                        status=LockStatus.ACQUIRED,
                        stale_removed=stale_was_removed,
                        wait_time_seconds=time.time() - start_time
                    )
            except FileExistsError:
                # Race condition: another process created lock
                continue
            except OSError as e:
                return LockAcquisitionResult(
                    success=False,
                    status=LockStatus.ERROR,
                    error_message=str(e),
                    wait_time_seconds=time.time() - start_time
                )

    def force_acquire(self) -> LockAcquisitionResult:
        """Force acquire lock by removing existing lock (AC#4 Option 2).

        WARNING: This is risky and may cause conflicts if another story
        is actively committing.

        Returns:
            LockAcquisitionResult with force_acquired=True on success
        """
        logger.warning(
            f"FORCE ACQUIRE requested by {self.story_id}. "
            "This may cause git conflicts if another story is actively committing!"
        )

        # Remove existing lock if present
        if self.lock_path.exists():
            try:
                self.lock_path.unlink()
            except OSError as e:
                return LockAcquisitionResult(
                    success=False,
                    status=LockStatus.ERROR,
                    error_message=f"Failed to remove existing lock: {e}"
                )

        # Create new lock
        try:
            self._create_lock_file()
            self._acquired = True
            return LockAcquisitionResult(
                success=True,
                status=LockStatus.ACQUIRED,
                force_acquired=True
            )
        except OSError as e:
            return LockAcquisitionResult(
                success=False,
                status=LockStatus.ERROR,
                error_message=str(e)
            )

    def release(self, strict: bool = False) -> None:
        """Release lock after commit completes (AC#5).

        Args:
            strict: If True, raise PermissionError if lock not held by this story

        Raises:
            PermissionError: If strict=True and lock not held by this story
        """
        if not self.lock_path.exists():
            self._acquired = False
            return

        if strict:
            lock_info = self.get_lock_info()
            if lock_info and lock_info.get("story_id") != self.story_id:
                raise PermissionError(
                    f"Lock not held by this story. "
                    f"Held by {lock_info.get('story_id')}, requested by {self.story_id}"
                )

        try:
            self.lock_path.unlink()
        except OSError:
            pass

        self._acquired = False

    def is_stale(self) -> bool:
        """Check if lock is stale (AC#3: PID dead AND age > threshold).

        A lock is stale when BOTH conditions are met:
        1. The process holding the lock is no longer running
        2. The lock is older than stale_threshold_seconds

        Returns:
            True if lock is stale, False otherwise
        """
        if not self.lock_path.exists():
            return True

        try:
            lock_info = self.get_lock_info()
            if not lock_info:
                return True

            # Check if PID is alive
            pid = lock_info.get("pid")
            if pid is None:
                return True

            pid_alive = self._process_exists(pid)
            if pid_alive:
                # Process alive = not stale (regardless of age)
                return False

            # PID is dead - check age
            timestamp_str = lock_info.get("timestamp")
            if not timestamp_str:
                return True

            try:
                # Parse ISO 8601 timestamp
                timestamp_str = timestamp_str.rstrip("Z")
                if "+" in timestamp_str:
                    timestamp_str = timestamp_str.split("+")[0]
                lock_time = datetime.fromisoformat(timestamp_str)
                lock_time = lock_time.replace(tzinfo=timezone.utc)
                now = datetime.now(timezone.utc)
                age_seconds = (now - lock_time).total_seconds()

                return age_seconds > self.stale_threshold_seconds
            except (ValueError, TypeError):
                return True

        except Exception:
            return True

    def get_lock_info(self) -> Optional[Dict[str, Any]]:
        """Return lock holder information for progress display.

        Returns:
            Dictionary with pid, story_id, timestamp, hostname or None
        """
        if not self.lock_path.exists():
            return None

        try:
            content = self.lock_path.read_text()
            info = {}

            for line in content.strip().split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    key = key.strip()
                    value = value.strip()

                    if key == "pid":
                        try:
                            info["pid"] = int(value)
                        except ValueError:
                            info["pid"] = None
                    else:
                        info[key] = value if value else None

            return info if info else None

        except Exception:
            return None

    def cancel_wait(self) -> None:
        """Cancel waiting for lock acquisition."""
        self._cancel_requested = True

    def _create_lock_file(self) -> bool:
        """Create lock file with atomic O_CREAT | O_EXCL.

        Returns:
            True if lock created successfully

        Raises:
            FileExistsError: If lock already exists (race condition)
            OSError: If lock creation fails
        """
        # Ensure directory exists
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)

        # Create lock content
        content = self._create_lock_content()

        # Atomic create (fails if file exists)
        fd = os.open(
            str(self.lock_path),
            os.O_CREAT | os.O_EXCL | os.O_WRONLY,
            0o600  # Owner read/write only
        )

        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)
        except Exception:
            # Clean up fd if write fails
            try:
                os.close(fd)
            except OSError:
                pass
            raise

        return True

    def _create_lock_content(self) -> str:
        """Create lock file content with PID, story_id, timestamp, hostname.

        Returns:
            Lock file content string
        """
        return (
            f"pid: {os.getpid()}\n"
            f"story_id: {self.story_id}\n"
            f"timestamp: {datetime.utcnow().isoformat()}Z\n"
            f"hostname: {socket.gethostname()}\n"
        )

    def _process_exists(self, pid: int) -> bool:
        """Check if process with PID exists using os.kill(pid, 0).

        Args:
            pid: Process ID to check

        Returns:
            True if process exists, False otherwise
        """
        try:
            os.kill(pid, 0)
            return True
        except (OSError, ProcessLookupError):
            return False

    def _check_and_report_progress(
        self,
        elapsed: float,
        interval: float,
        callback: Optional[Callable[[str], None]],
        lock_info: Optional[Dict[str, Any]] = None
    ) -> None:
        """Check if progress update needed and report via callback.

        Args:
            elapsed: Total elapsed time in seconds
            interval: Progress interval in seconds
            callback: Optional callback for progress messages
            lock_info: Lock holder information
        """
        if callback is None:
            return

        # Only report at interval boundaries (with some tolerance)
        if elapsed > 0 and (elapsed % interval) < 0.2:
            if lock_info:
                holder_story = lock_info.get("story_id", "unknown")
                holder_pid = lock_info.get("pid", "unknown")
                message = (
                    f"Waiting for git lock (held by {holder_story} "
                    f"PID {holder_pid})... {int(elapsed)}s"
                )
            else:
                message = f"Waiting for git lock... {int(elapsed)}s"

            callback(message)

    def __enter__(self):
        """Context manager entry - acquire lock."""
        result = self.acquire()
        if not result.success:
            raise RuntimeError(
                f"Failed to acquire lock: {result.status.value} - {result.error_message}"
            )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - release lock."""
        self.release()
        return False


def main():
    """CLI entry point for lock file coordinator."""
    parser = argparse.ArgumentParser(
        description="Lock file coordinator for git commit serialization (STORY-096)"
    )
    parser.add_argument(
        "action",
        choices=["acquire", "release", "status"],
        help="Action to perform"
    )
    parser.add_argument(
        "--story-id",
        required=False,
        help="Story ID (required for acquire/release)"
    )
    parser.add_argument(
        "--lock-dir",
        default=".",
        help="Base directory for DevForgeAI files"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT_SECONDS,
        help=f"Timeout in seconds (default: {DEFAULT_TIMEOUT_SECONDS})"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force acquire lock (risky!)"
    )

    args = parser.parse_args()

    # Validate story-id for acquire/release
    if args.action in ["acquire", "release"] and not args.story_id:
        parser.error(f"--story-id is required for {args.action}")

    # Execute action
    if args.action == "acquire":
        lock = GitCommitLock(story_id=args.story_id, lock_dir=args.lock_dir)

        if args.force:
            result = lock.force_acquire()
        else:
            def progress_print(msg):
                print(msg, file=sys.stderr)

            result = lock.acquire(
                timeout_seconds=args.timeout,
                progress_callback=progress_print
            )

        output = {
            "success": result.success,
            "status": result.status.value,
            "story_id": args.story_id,
            "holder_pid": result.holder_pid,
            "holder_story_id": result.holder_story_id,
            "stale_removed": result.stale_removed,
            "force_acquired": result.force_acquired,
            "requires_user_prompt": result.requires_user_prompt,
            "wait_time_seconds": result.wait_time_seconds
        }
        print(json.dumps(output))

    elif args.action == "release":
        lock = GitCommitLock(story_id=args.story_id, lock_dir=args.lock_dir)
        try:
            lock.release()
            print(json.dumps({"status": "released", "story_id": args.story_id}))
        except PermissionError as e:
            print(json.dumps({"status": "error", "error": str(e)}))
            sys.exit(1)

    elif args.action == "status":
        lock = GitCommitLock(story_id="status-check", lock_dir=args.lock_dir)
        info = lock.get_lock_info()

        if info:
            info["is_stale"] = lock.is_stale()
            print(json.dumps(info))
        else:
            print(json.dumps({"status": "unlocked"}))


if __name__ == "__main__":
    main()

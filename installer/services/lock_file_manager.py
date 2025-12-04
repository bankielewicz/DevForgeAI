"""Lock file manager (RCA-004).

AC#7: Lock File Management - Prevents concurrent installations via lock file with PID checking.

Manages installation lock files to prevent concurrent installations:
- Creates lock file with current process PID and timestamp
- Detects active locks (PID check) and prevents concurrent installs
- Removes stale locks (dead process PIDs) automatically
- Cleans up lock files on successful or failed exits
- Supports timeout-based lock acquisition with retries
"""
import os
import time
from pathlib import Path
from datetime import datetime
from typing import Optional


class LockFileManager:
    """Manages installation lock file to prevent concurrent installs.

    Implements SVC-013 (lock file creation), SVC-014 (concurrent detection),
    SVC-015 (cleanup), and SVC-016 (stale lock detection).
    """

    LOCK_FILENAME = "install.lock"

    def __init__(self, lock_dir: str = ".devforgeai"):
        """Initialize lock file manager.

        Args:
            lock_dir: Directory where lock file will be created.
                      Lock file will be at {lock_dir}/install.lock
        """
        self.lock_dir = Path(lock_dir)
        self.lock_path = self.lock_dir / self.LOCK_FILENAME

    def acquire_lock(self, timeout_seconds: int = 0, retry_interval: float = 0.1) -> bool:
        """Create lock file with current process ID and timestamp.

        AC#7: Lock File Management - Acquires exclusive lock for installation.
        SVC-013: Creates lock file at {lock_dir}/install.lock
        SVC-014: Detects concurrent installations via PID check
        SVC-016: Detects and removes stale locks (dead process PIDs)

        Args:
            timeout_seconds: Maximum seconds to wait for lock availability.
                           0 = fail immediately if locked. Default: 0
            retry_interval: Seconds between retry attempts. Default: 0.1

        Returns:
            True if lock acquired successfully

        Raises:
            RuntimeError: If another active process holds the lock
            TimeoutError: If lock not available within timeout period
        """
        start_time = time.time()

        while True:
            # Ensure lock directory exists
            self.lock_dir.mkdir(parents=True, exist_ok=True)

            # Check for existing lock
            if self.lock_path.exists():
                # Check if lock is stale (dead process)
                if self.is_lock_stale():
                    # Remove stale lock and proceed
                    try:
                        self.lock_path.unlink()
                    except OSError:
                        pass
                else:
                    # Lock is held by active process
                    if timeout_seconds <= 0:
                        # No timeout, fail immediately
                        locked_pid = self.get_locked_pid()
                        raise RuntimeError(
                            f"Concurrent installation detected. "
                            f"Process {locked_pid} is already installing."
                        )

                    # Check timeout
                    elapsed = time.time() - start_time
                    if elapsed >= timeout_seconds:
                        raise TimeoutError(
                            f"Lock acquisition timeout after {timeout_seconds} seconds"
                        )

                    # Wait and retry
                    time.sleep(retry_interval)
                    continue

            # Create new lock file with PID and ISO 8601 timestamp
            # Use atomic operation (O_CREAT | O_EXCL) to detect race conditions
            try:
                current_pid = os.getpid()
                timestamp = datetime.utcnow().isoformat() + "Z"

                # Atomically create lock file - fails if file exists (O_EXCL)
                # This ensures only one process can create the lock
                fd = os.open(
                    str(self.lock_path),
                    os.O_CREAT | os.O_EXCL | os.O_WRONLY,
                    0o600  # Permissions: owner read/write only
                )

                # Write PID and timestamp to lock file
                with os.fdopen(fd, 'w') as f:
                    f.write(f"{current_pid}\n{timestamp}\n")

                return True
            except FileExistsError:
                # Race condition: another process created lock between check and write
                # Re-check if lock is stale or still held
                if self.lock_path.exists() and not self.is_lock_stale():
                    # Lock is held by active process
                    if timeout_seconds <= 0:
                        # No timeout, fail immediately
                        raise RuntimeError(
                            f"Concurrent installation detected. "
                            f"Lock file created by another process."
                        )

                    # Check timeout
                    elapsed = time.time() - start_time
                    if elapsed >= timeout_seconds:
                        raise TimeoutError(
                            f"Lock acquisition timeout after {timeout_seconds} seconds"
                        )

                    # Wait and retry
                    time.sleep(retry_interval)
                    continue
                else:
                    # Lock is stale or disappeared, retry
                    continue
            except OSError:
                # Other OS errors
                if timeout_seconds <= 0:
                    raise RuntimeError(
                        f"Failed to create lock file: {self.lock_path}"
                    )

                # Check timeout
                elapsed = time.time() - start_time
                if elapsed >= timeout_seconds:
                    raise TimeoutError(
                        f"Lock acquisition timeout after {timeout_seconds} seconds"
                    )

                # Wait and retry
                time.sleep(retry_interval)
                continue

    def release_lock(self) -> None:
        """Remove lock file.

        AC#7: Lock File Management - Releases lock on successful completion.
        SVC-015: Removes lock file on exit
        """
        if self.lock_path.exists():
            try:
                self.lock_path.unlink()
            except OSError:
                pass

    def cleanup(self) -> None:
        """Remove lock file during error cleanup or interrupt handling.

        AC#7: Lock File Management - Ensures lock cleanup in all scenarios.
        SVC-015: Removes lock file on error or keyboard interrupt
        """
        self.release_lock()

    def is_lock_stale(self) -> bool:
        """Check if lock file has dead process PID.

        AC#7: Lock File Management - Validates lock staleness.
        SVC-016: Detects stale locks (process no longer running)

        Returns:
            True if lock is stale (process dead or invalid format), False if active
        """
        if not self.lock_path.exists():
            return True

        try:
            with open(self.lock_path, 'r') as f:
                content = f.read().strip()

            # Parse PID (first line)
            lines = content.split('\n')
            if not lines:
                return True

            pid_str = lines[0].strip()

            # Try to parse PID
            try:
                pid = int(pid_str)
            except ValueError:
                return True  # Invalid PID format, consider stale

            # Check if process is running
            return not self._process_exists(pid)

        except Exception:
            return True

    def is_locked(self) -> bool:
        """Check if installation is currently locked by active process.

        Returns:
            True if lock exists and is held by active process, False otherwise
        """
        if not self.lock_path.exists():
            return False

        return not self.is_lock_stale()

    def get_locked_pid(self) -> Optional[int]:
        """Return PID of process holding lock, or None if not locked.

        Returns:
            PID as int if lock held by active process, None otherwise
        """
        if not self.lock_path.exists():
            return None

        try:
            with open(self.lock_path, 'r') as f:
                pid_str = f.read().strip().split('\n')[0]
                pid = int(pid_str)

                # Only return PID if lock is active (not stale)
                if self._process_exists(pid):
                    return pid
                return None
        except Exception:
            return None

    def _process_exists(self, pid: int) -> bool:
        """Check if process with given PID exists.

        Uses os.kill with signal 0 to check without sending signal.

        Args:
            pid: Process ID to check

        Returns:
            True if process exists, False otherwise
        """
        try:
            # On Unix, os.kill with signal 0 doesn't kill but checks existence
            os.kill(pid, 0)
            return True
        except (OSError, ProcessLookupError):
            return False

    def __enter__(self):
        """Context manager entry - acquire lock.

        Returns:
            Self for use in 'with' statement
        """
        self.acquire_lock()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - release lock.

        Releases lock even if exception occurred in context.

        Args:
            exc_type: Exception type if raised
            exc_val: Exception value if raised
            exc_tb: Exception traceback if raised

        Returns:
            False to propagate any exception
        """
        self.cleanup()
        return False

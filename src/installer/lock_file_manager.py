"""Lock file manager (RCA-004).

Prevents concurrent installations via lock file with PID checking.
"""
import os
from pathlib import Path
from typing import Optional


class LockFileManager:
    """Manages installation lock file to prevent concurrent installs."""

    def __init__(self, lock_path: str = ".devforgeai/install.lock"):
        """Initialize lock file manager."""
        self.lock_path = Path(lock_path)
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)

    def acquire_lock(self) -> bool:
        """Create lock file with current process ID.

        Returns:
            True if lock acquired, False if already locked
        """
        # Check for existing lock with active PID
        if self.lock_path.exists():
            if not self._is_stale():
                return False  # Lock held by active process
            else:
                # Remove stale lock
                self.lock_path.unlink()

        # Create new lock file with PID
        try:
            with open(self.lock_path, 'w') as f:
                f.write(str(os.getpid()))
            return True
        except Exception:
            return False

    def release_lock(self) -> None:
        """Remove lock file."""
        if self.lock_path.exists():
            try:
                self.lock_path.unlink()
            except Exception:
                pass

    def _is_stale(self) -> bool:
        """Check if lock file has dead process PID."""
        if not self.lock_path.exists():
            return True

        try:
            with open(self.lock_path, 'r') as f:
                pid_str = f.read().strip()

            # Try to parse PID
            try:
                pid = int(pid_str)
            except ValueError:
                return True  # Invalid PID format, consider stale

            # Check if process is running
            return not self._process_exists(pid)

        except Exception:
            return True

    def _process_exists(self, pid: int) -> bool:
        """Check if process with given PID exists."""
        try:
            # On Unix, os.kill with signal 0 doesn't kill but checks existence
            os.kill(pid, 0)
            return True
        except (OSError, ProcessLookupError):
            return False

    def is_locked(self) -> bool:
        """Check if installation is currently locked."""
        if not self.lock_path.exists():
            return False

        return not self._is_stale()

    def get_locked_pid(self) -> Optional[int]:
        """Return PID of process holding lock, or None."""
        if not self.lock_path.exists():
            return None

        try:
            with open(self.lock_path, 'r') as f:
                return int(f.read().strip())
        except Exception:
            return None

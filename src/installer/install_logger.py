"""Install logger service (AC#5).

Writes detailed logs with ISO 8601 timestamps, stack traces, and system context.
"""
import os
from datetime import datetime
from pathlib import Path
from typing import Optional


class InstallLogger:
    """Logs installation events to .devforgeai/install.log."""

    def __init__(self, log_path: str = ".devforgeai/install.log"):
        """Initialize logger with target log file path."""
        self.log_path = Path(log_path)
        self._ensure_log_dir()
        self._set_permissions()

    def _ensure_log_dir(self) -> None:
        """Create log directory if needed."""
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def _set_permissions(self) -> None:
        """Set log file permissions to 0600 (owner read/write only)."""
        if self.log_path.exists():
            os.chmod(self.log_path, 0o600)

    def _get_iso_timestamp(self) -> str:
        """Return ISO 8601 timestamp with milliseconds."""
        return datetime.now().isoformat(timespec='milliseconds')

    def _rotate_log_if_needed(self) -> None:
        """Rotate log file when exceeding 10MB, keep 3 rotations."""
        if not self.log_path.exists():
            return

        if self.log_path.stat().st_size > 10 * 1024 * 1024:  # 10MB
            # Shift rotation files
            for i in range(2, 0, -1):
                old_path = Path(f"{self.log_path}.{i}")
                new_path = Path(f"{self.log_path}.{i + 1}")
                if old_path.exists() and i < 3:
                    old_path.rename(new_path)
                elif old_path.exists() and i >= 3:
                    old_path.unlink()

            # Rename current log
            self.log_path.rename(Path(f"{self.log_path}.1"))
            self._set_permissions()

    def log_error(self, error_category: str, exit_code: int, message: str,
                  stack_trace: Optional[str] = None, file_paths: Optional[dict] = None) -> None:
        """Log error with timestamp, stack trace, and context.

        Args:
            error_category: Error type (MISSING_SOURCE, etc.)
            exit_code: Exit code integer
            message: Error message
            stack_trace: Full stack trace
            file_paths: Dict with 'source' and 'target' keys
        """
        self._rotate_log_if_needed()

        timestamp = self._get_iso_timestamp()
        log_entry = f"[{timestamp}] ERROR {error_category} (exit={exit_code})\n"
        log_entry += f"  Message: {message}\n"

        if file_paths:
            if file_paths.get('source'):
                log_entry += f"  Source: {file_paths['source']}\n"
            if file_paths.get('target'):
                log_entry += f"  Target: {file_paths['target']}\n"

        log_entry += f"  OS: {os.name}\n"

        if stack_trace:
            log_entry += f"  Stack Trace:\n{stack_trace}\n"

        log_entry += "\n"

        with open(self.log_path, 'a') as f:
            f.write(log_entry)

        self._set_permissions()

    def log_action(self, action: str, details: Optional[str] = None) -> None:
        """Log installation action (backup, rollback, etc.)."""
        self._rotate_log_if_needed()

        timestamp = self._get_iso_timestamp()
        log_entry = f"[{timestamp}] ACTION {action}"
        if details:
            log_entry += f": {details}"
        log_entry += "\n"

        with open(self.log_path, 'a') as f:
            f.write(log_entry)

        self._set_permissions()

    def get_log_contents(self) -> str:
        """Return full log file contents."""
        if not self.log_path.exists():
            return ""

        with open(self.log_path, 'r') as f:
            return f.read()

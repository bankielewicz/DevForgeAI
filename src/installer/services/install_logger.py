"""Install logger service (AC#5).

Writes detailed logs with ISO 8601 timestamps, stack traces, and system context.

AC#5 Requirements:
- ISO 8601 timestamp with milliseconds and Z suffix (UTC)
- Error category and exit code in log
- Full error message and stack trace with line numbers
- File paths involved (source and target)
- System context (OS, shell version)
- Rollback actions taken (files restored, files removed)
- Append mode (never overwrite)
- Log rotation at 10MB with 3 rotations
- File permissions 0600

Log Requirements:
- LOG-001: ISO 8601 format (YYYY-MM-DDTHH:MM:SS.sssZ)
- LOG-002: Append mode and session separation
- LOG-003: Stack traces with "Traceback" and line numbers
- LOG-004: Log rotation at 10MB, keep 3 rotations
"""
import os
import sys
import platform
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, List


class InstallLogger:
    """Logs installation events with ISO 8601 timestamps and detailed context."""

    def __init__(
        self,
        log_file: str = "devforgeai/install.log",
        max_size_mb: int = 10,
        max_rotations: int = 3
    ):
        """Initialize logger with target log file path.

        Args:
            log_file: Path to log file (default: devforgeai/install.log)
            max_size_mb: Maximum log file size in MB before rotation (default: 10)
            max_rotations: Number of rotations to keep (default: 3)
        """
        self.log_file = Path(log_file)
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.max_rotations = max_rotations

        self._ensure_log_dir()
        self._set_permissions()

    def _ensure_log_dir(self) -> None:
        """Create log directory if needed."""
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    def _set_permissions(self) -> None:
        """Set log file permissions to 0600 (owner read/write only)."""
        if self.log_file.exists():
            os.chmod(self.log_file, 0o600)

    def _get_iso_timestamp(self) -> str:
        """Return ISO 8601 timestamp with milliseconds and Z suffix (UTC).

        Format: 2025-12-03T14:30:45.123456Z (includes microseconds, will be truncated)
        Returns: String in ISO 8601 format with 3 decimal places for milliseconds
        """
        now = datetime.now(timezone.utc)
        # Format with microseconds, then truncate to milliseconds
        iso_str = now.isoformat(timespec='microseconds')
        # Replace +00:00 with Z, and truncate to milliseconds
        iso_str = iso_str.replace('+00:00', 'Z')
        # Extract YYYY-MM-DDTHH:MM:SS.ffffff part
        if 'Z' in iso_str:
            base, z = iso_str.split('Z')
            # Truncate microseconds to milliseconds (first 3 digits)
            parts = base.split('.')
            if len(parts) == 2:
                iso_str = f"{parts[0]}.{parts[1][:3]}Z"
            else:
                iso_str = f"{base}Z"
        return iso_str

    def _rotate_log_if_needed(self) -> None:
        """Rotate log file when exceeding max_size_bytes, keep max_rotations rotations.

        LOG-004: Implements rotation at 10MB with 3 rotations
        """
        if not self.log_file.exists():
            return

        if self.log_file.stat().st_size > self.max_size_bytes:
            # Shift rotation files: delete oldest, move others up
            for i in range(self.max_rotations - 1, 0, -1):
                old_path = Path(f"{self.log_file}.{i}")
                new_path = Path(f"{self.log_file}.{i + 1}")

                if old_path.exists():
                    if i == self.max_rotations - 1:
                        # Delete the oldest rotation
                        old_path.unlink()
                    else:
                        # Shift to next number
                        if new_path.exists():
                            new_path.unlink()
                        old_path.rename(new_path)

            # Rename current log to .1
            new_log_path = Path(f"{self.log_file}.1")
            if new_log_path.exists():
                new_log_path.unlink()
            self.log_file.rename(new_log_path)
            self._set_permissions()

    def log_info(self, message: str) -> None:
        """Log informational message (LOG-001, LOG-002).

        Args:
            message: Message to log
        """
        self._rotate_log_if_needed()

        timestamp = self._get_iso_timestamp()
        log_entry = f"{timestamp} [INFO] {message}\n"

        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except FileNotFoundError:
            # Log file was deleted, recreate it
            self.log_file.touch()
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)

        self._set_permissions()

    def log_warning(self, message: str) -> None:
        """Log warning message.

        Args:
            message: Message to log
        """
        self._rotate_log_if_needed()

        timestamp = self._get_iso_timestamp()
        log_entry = f"{timestamp} [WARNING] {message}\n"

        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except FileNotFoundError:
            self.log_file.touch()
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)

        self._set_permissions()

    def log_error(
        self,
        error: Optional[Exception] = None,
        category: Optional[str] = None,
        exit_code: Optional[int] = None,
        message: Optional[str] = None,
        source_path: Optional[str] = None,
        target_path: Optional[str] = None
    ) -> None:
        """Log error with timestamp, stack trace, and context (AC#5, LOG-001, LOG-003).

        Args:
            error: Exception object (will extract message and stack trace)
            category: Error category (e.g., "MISSING_SOURCE")
            exit_code: Exit code integer
            message: Additional error message
            source_path: Source file path involved
            target_path: Target file path involved
        """
        self._rotate_log_if_needed()

        timestamp = self._get_iso_timestamp()
        log_entry = f"{timestamp} [ERROR]"

        # Add category and exit code if provided
        if category:
            log_entry += f" {category}"
        if exit_code is not None:
            log_entry += f" (exit code {exit_code})"

        log_entry += "\n"

        # Add message from parameter or exception
        if message:
            log_entry += f"  Message: {message}\n"
        elif error:
            log_entry += f"  Message: {str(error)}\n"

        # Add file paths if provided
        if source_path:
            log_entry += f"  Source: {source_path}\n"
        if target_path:
            log_entry += f"  Target: {target_path}\n"

        # Add stack trace if exception provided (LOG-003 - before system context)
        if error and hasattr(error, '__traceback__'):
            log_entry += "  Stack Trace:\n"
            # Format the exception with its traceback (LOG-003)
            tb_lines = traceback.format_exception(type(error), error, error.__traceback__)
            stack_trace = ''.join(tb_lines)
            # Indent each line of stack trace
            for line in stack_trace.split('\n'):
                if line:
                    log_entry += f"    {line}\n"

        # Add system context (after stack trace for better readability)
        log_entry += self._get_system_context()

        log_entry += "\n"

        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except FileNotFoundError:
            self.log_file.touch()
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)

        self._set_permissions()

    def log_file_operation(
        self,
        operation: str,
        source_path: str,
        target_path: str
    ) -> None:
        """Log file operation (copy, move, delete, etc.) with source and target paths (AC#5).

        Args:
            operation: Operation type (copy, move, delete, etc.)
            source_path: Source file path
            target_path: Target file path
        """
        self._rotate_log_if_needed()

        timestamp = self._get_iso_timestamp()
        log_entry = f"{timestamp} [INFO] File operation: {operation}\n"
        log_entry += f"  Source: {source_path}\n"
        log_entry += f"  Target: {target_path}\n"

        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except FileNotFoundError:
            self.log_file.touch()
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)

        self._set_permissions()

    def log_system_context(self) -> None:
        """Log system context information (OS, shell version) (AC#5).

        LOG-001, LOG-002: Includes ISO 8601 timestamps and system info
        """
        self._rotate_log_if_needed()

        timestamp = self._get_iso_timestamp()
        log_entry = f"{timestamp} [INFO] System Context\n"

        # Add system information
        system_info = self._get_system_context()
        for line in system_info.strip().split('\n'):
            log_entry += f"  {line}\n"

        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except FileNotFoundError:
            self.log_file.touch()
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)

        self._set_permissions()

    def log_rollback(
        self,
        files_restored: Optional[List[str]] = None,
        files_removed: Optional[List[str]] = None
    ) -> None:
        """Log rollback actions (AC#5).

        Args:
            files_restored: List of files restored during rollback
            files_removed: List of files removed during rollback
        """
        self._rotate_log_if_needed()

        timestamp = self._get_iso_timestamp()
        log_entry = f"{timestamp} [INFO] Rollback performed\n"

        if files_restored:
            log_entry += f"  Files restored: {len(files_restored)}\n"
            for file_path in files_restored:
                log_entry += f"    - {file_path}\n"

        if files_removed:
            log_entry += f"  Files removed: {len(files_removed)}\n"
            for file_path in files_removed:
                log_entry += f"    - {file_path}\n"

        log_entry += "\n"

        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except FileNotFoundError:
            self.log_file.touch()
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)

        self._set_permissions()

    def log_session_start(self) -> None:
        """Log installation session separator (LOG-002).

        LOG-002: Separates installation sessions
        """
        self._rotate_log_if_needed()

        timestamp = self._get_iso_timestamp()

        # Create separator line
        separator = "=" * 60
        log_entry = f"\n{separator}\n"
        log_entry += f"{timestamp} === Installation Started ===\n"
        log_entry += f"{separator}\n"

        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except FileNotFoundError:
            self.log_file.touch()
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)

        self._set_permissions()

    def _get_system_context(self) -> str:
        """Get system context information as formatted string.

        Returns:
            Formatted system context information
        """
        context = ""

        # OS information
        system_name = platform.system()
        context += f"OS: {system_name}\n"

        # OS version/release
        if system_name == "Linux":
            context += f"  OS Release: {platform.release()}\n"
        elif system_name == "Darwin":
            context += f"  OS Release: {platform.release()}\n"
        elif system_name == "Windows":
            context += f"  OS Release: {platform.release()}\n"

        # Python version
        context += f"  Python: {platform.python_version()}\n"

        # Shell information
        shell = os.getenv('SHELL', 'unknown')
        context += f"  Shell: {shell}\n"

        return context

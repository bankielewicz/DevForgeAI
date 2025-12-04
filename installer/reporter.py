"""
Installation Reporter Service (STORY-075).

Handles:
- Console summary report generation (AC#1)
- Log file creation with ISO 8601 timestamps (AC#2)
- JSON output mode (AC#3)
- Error categorization (AC#6)
- Audit trail compliance (AC#7)
"""

import json
import logging
import hashlib
import re
import traceback
import os
from pathlib import Path
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from installer.config.reporting_config import LOG_FILE_PATH, ERROR_TYPES


class InstallationReporter:
    """
    Service for generating installation reports and logs.

    Singleton lifecycle: One instance per installation session.
    Responsibilities:
    - Create and manage log files
    - Generate console reports
    - Generate JSON output
    - Categorize errors
    - Ensure audit trail compliance
    """

    def __init__(self):
        """Initialize the reporter."""
        self._log_file: Optional[Path] = None
        self._logger: Optional[logging.Logger] = None

    def create_log_file(self, target_directory: str) -> Path:
        """
        Create log file at .devforgeai/install.log.

        Args:
            target_directory: Installation target directory

        Returns:
            Path object pointing to the log file

        Raises:
            PermissionError: If .devforgeai directory not writable (with fallback to TMPDIR)
        """
        target_path = Path(target_directory)
        devforgeai_dir = target_path / ".devforgeai"

        try:
            # Create .devforgeai directory if it doesn't exist
            devforgeai_dir.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            # Fallback to TMPDIR if .devforgeai not writable
            import tempfile

            tmpdir = Path(tempfile.gettempdir())
            devforgeai_dir = tmpdir
            target_path = tmpdir

        log_file = devforgeai_dir / "install.log"

        # Set up logger
        self._log_file = log_file
        self._logger = logging.getLogger("installation")
        self._logger.setLevel(logging.DEBUG)

        # Remove existing handlers to avoid duplicates
        self._logger.handlers = []

        # Create file handler with UTF-8 encoding and LF line endings
        handler = logging.FileHandler(
            log_file, mode="a", encoding="utf-8"
        )
        # Force LF line endings by using a custom formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S",
        )
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)

        # Set file permissions to 644 (rw-r--r--)
        try:
            log_file.chmod(0o644)
        except (OSError, PermissionError):
            pass  # Ignore permission errors on setting perms

        return log_file

    def log_operation(
        self,
        operation_type: str,
        file_path: str,
        status: str,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Log a file operation with timestamp.

        Args:
            operation_type: Type of operation (copy, create, modify, etc)
            file_path: Path of file affected
            status: Status (success, failed, warning)
            details: Optional additional details
        """
        if not self._logger:
            return

        # Redact sensitive data from details
        sanitized_details = self._redact_sensitive_data(details or {})

        details_str = (
            f" | {json.dumps(sanitized_details)}" if sanitized_details else ""
        )
        message = (
            f"OPERATION: {operation_type} - {file_path} - {status}{details_str}"
        )
        self._logger.info(message)

    def log_validation(self, check_name: str, result: str) -> None:
        """
        Log a validation checkpoint.

        Args:
            check_name: Name of validation check
            result: Result (passed, failed, warning)
        """
        if not self._logger:
            return

        message = f"VALIDATION: {check_name} - {result}"
        self._logger.info(message)

    def log_error(self, context: str, error_message: str) -> None:
        """
        Log an error with context.

        Args:
            context: Context where error occurred
            error_message: Error message
        """
        if not self._logger:
            return

        message = f"ERROR: {context} - {error_message}"
        self._logger.error(message)

    def log_warning(self, context: str, warning_message: str) -> None:
        """
        Log a warning.

        Args:
            context: Context of warning
            warning_message: Warning message
        """
        if not self._logger:
            return

        message = f"WARNING: {context} - {warning_message}"
        self._logger.warning(message)

    def log_phase_start(self, phase_name: str) -> None:
        """
        Log the start of an installation phase.

        Args:
            phase_name: Name of phase (Pre-flight, Core, Post-install, Validation)
        """
        if not self._logger:
            return

        separator = "=" * 60
        message = f"{separator}\nPHASE START: {phase_name}\n{separator}"
        self._logger.info(message)

    def generate_console_report(self, report_data: Dict[str, Any]) -> str:
        """
        Generate a formatted console summary report (AC#1).

        Args:
            report_data: Dictionary containing report fields

        Returns:
            Formatted console report string
        """
        status = report_data.get("status", "unknown").upper()
        version = report_data.get("version", "unknown")
        files_installed = report_data.get("files_installed", 0)
        files_failed = report_data.get("files_failed", 0)
        duration = report_data.get("duration_seconds", 0)
        target_dir = report_data.get("target_directory", "unknown")
        log_file = report_data.get("log_file", "unknown")

        # Build report
        lines = []
        separator = "=" * 70

        lines.append(separator)
        lines.append(f"Installation Report - Status: {status}")
        lines.append(separator)
        lines.append("")
        lines.append(f"Version Installed:    {version}")
        lines.append(f"Files Processed:      {files_installed + files_failed}")
        lines.append(f"  - Successful:       {files_installed}")
        lines.append(f"  - Failed:           {files_failed}")
        lines.append(f"Duration:             {duration:.3f} seconds")
        lines.append("Target Directory:")
        lines.append(f"  {target_dir}")
        lines.append("Log File:")
        lines.append(f"  {log_file}")
        lines.append("")
        lines.append(separator)

        return "\n".join(lines)

    def generate_json_output(self, report_data: Dict[str, Any]) -> str:
        """
        Generate JSON output (AC#3).

        Args:
            report_data: Dictionary with report fields

        Returns:
            Compact JSON string (no pretty-print)
        """
        # Ensure duration has 3 decimal places
        duration = report_data.get("duration_seconds", 0)
        report_data["duration_seconds"] = round(duration, 3)

        # Return compact JSON (no indentation)
        return json.dumps(report_data, separators=(",", ":"))

    def categorize_error(
        self,
        exception: Exception,
        error_context: Optional[str] = None,
        file_path: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Categorize an error into one of 7 types (AC#6).

        Args:
            exception: The exception object
            error_context: Context hint (checksum_validation, git_operation, validation, dependency)
            file_path: Path of affected file

        Returns:
            Error object with type and message fields
        """
        message = str(exception)
        error_type = self._classify_error_type(exception, error_context)
        message = self._normalize_error_message(error_type, message)

        error_obj = {
            "type": error_type,
            "message": message or error_type,
        }

        if file_path:
            error_obj["file"] = file_path

        return error_obj

    def _classify_error_type(
        self,
        exception: Exception,
        error_context: Optional[str] = None,
    ) -> str:
        """
        Classify error type from exception and context.

        Args:
            exception: The exception object
            error_context: Context hint for classification

        Returns:
            Error type string
        """
        # Check exception type first
        exception_types = {
            PermissionError: "PERMISSION_DENIED",
            FileNotFoundError: "FILE_NOT_FOUND",
            ImportError: "DEPENDENCY_ERROR",
        }

        for exc_type, error_type in exception_types.items():
            if isinstance(exception, exc_type):
                return error_type

        # Check context-based classification
        context_types = {
            "checksum_validation": "CHECKSUM_MISMATCH",
            "git_operation": "GIT_ERROR",
            "validation": "VALIDATION_ERROR",
            "dependency": "DEPENDENCY_ERROR",
        }

        return context_types.get(error_context, "UNKNOWN_ERROR")

    def _normalize_error_message(self, error_type: str, message: str) -> str:
        """
        Normalize error message based on error type.

        Args:
            error_type: The classified error type
            message: Original error message

        Returns:
            Normalized error message
        """
        if error_type == "PERMISSION_DENIED":
            if "permission" not in message.lower():
                return f"Permission denied: {message}"
        return message

    def _redact_sensitive_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Redact sensitive patterns from data (AC#7).

        Args:
            data: Data dictionary potentially containing sensitive info

        Returns:
            Sanitized data with sensitive patterns redacted
        """
        sensitive_patterns = [
            "password",
            "token",
            "secret",
            "api_key",
            "api-key",
            "apikey",
            "auth",
        ]

        sanitized = {}
        for key, value in data.items():
            # Check if key is sensitive
            key_lower = key.lower()
            if any(pattern in key_lower for pattern in sensitive_patterns):
                sanitized[key] = "[REDACTED]"
            elif isinstance(value, str):
                # Check if value contains sensitive patterns
                value_lower = value.lower()
                if any(pattern in value_lower for pattern in sensitive_patterns):
                    sanitized[key] = "[REDACTED]"
                else:
                    sanitized[key] = value
            else:
                sanitized[key] = value

        return sanitized

"""Error handler service (AC#1, AC#2, AC#3).

Categorizes errors, formats user-friendly messages, provides resolution steps.
"""
import re
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from .exit_codes import (
    SUCCESS,
    MISSING_SOURCE,
    PERMISSION_DENIED,
    ROLLBACK_OCCURRED,
    VALIDATION_FAILED,
)
from .services.install_logger import InstallLogger


@dataclass
class ErrorCategory:
    """Error category with name and exit code."""
    name: str
    exit_code: int


@dataclass
class ErrorResult:
    """Result from handling an error."""
    exit_code: int
    console_message: str


class ErrorHandler:
    """Handles error categorization and user-friendly message formatting."""

    # Error category definitions
    ERROR_CATEGORIES = {
        'MISSING_SOURCE': {
            'exit_code': MISSING_SOURCE,
            'label': 'ERROR: Missing Source Files',
            'description': 'Required source files not found.',
            'resolution_steps': [
                'Verify .claude/ directory exists in source',
                'Check file permissions on source directory',
                'Ensure source path is correct'
            ]
        },
        'PERMISSION_DENIED': {
            'exit_code': PERMISSION_DENIED,
            'label': 'ERROR: Permission Denied',
            'description': 'Insufficient permissions for installation.',
            'resolution_steps': [
                'Run with appropriate permissions (sudo may be needed)',
                'Check file ownership: chown user:group <path>',
                'Verify directory write permissions: chmod u+w <path>'
            ]
        },
        'ROLLBACK_OCCURRED': {
            'exit_code': ROLLBACK_OCCURRED,
            'label': 'ERROR: Installation Failed and Rolled Back',
            'description': 'Installation encountered an error and was rolled back.',
            'resolution_steps': [
                'System has been restored to pre-installation state',
                'Review log file for error details',
                'Retry installation after addressing root cause'
            ]
        },
        'VALIDATION_FAILED': {
            'exit_code': VALIDATION_FAILED,
            'label': 'ERROR: Validation Failed',
            'description': 'Installation completed but validation checks failed.',
            'resolution_steps': [
                'Check log file for validation details',
                'Verify source integrity and try again',
                'Retry installation if files were modified'
            ]
        },
    }

    def __init__(
        self,
        logger: Optional[InstallLogger] = None,
        rollback_service=None,
        backup_service=None
    ):
        """Initialize error handler with optional dependencies.

        Args:
            logger: InstallLogger instance for logging errors
            rollback_service: RollbackService instance for rollback operations
            backup_service: BackupService instance for backup information
        """
        self.logger = logger or InstallLogger()
        self.rollback_service = rollback_service
        self.backup_service = backup_service

    def categorize_error(
        self,
        error: Exception,
        rollback_triggered: bool = False,
        validation_phase: bool = False
    ) -> ErrorCategory:
        """Categorize error into one of 5 types and return exit code.

        Args:
            error: Exception to categorize
            rollback_triggered: If True, categorize as ROLLBACK_OCCURRED
            validation_phase: If True, categorize as VALIDATION_FAILED

        Returns:
            ErrorCategory with name and exit code
        """
        # Handle rollback flag (highest priority)
        if rollback_triggered:
            return ErrorCategory(name='ROLLBACK_OCCURRED', exit_code=ROLLBACK_OCCURRED)

        # Handle validation phase flag
        if validation_phase:
            return ErrorCategory(name='VALIDATION_FAILED', exit_code=VALIDATION_FAILED)

        # Type-based detection
        if isinstance(error, FileNotFoundError):
            return ErrorCategory(name='MISSING_SOURCE', exit_code=MISSING_SOURCE)
        elif isinstance(error, PermissionError):
            return ErrorCategory(name='PERMISSION_DENIED', exit_code=PERMISSION_DENIED)

        # String-based fallback
        error_str = str(error).lower()

        if 'not found' in error_str or 'no such file' in error_str:
            return ErrorCategory(name='MISSING_SOURCE', exit_code=MISSING_SOURCE)
        elif 'permission' in error_str or 'denied' in error_str:
            return ErrorCategory(name='PERMISSION_DENIED', exit_code=PERMISSION_DENIED)
        elif 'rollback' in error_str:
            return ErrorCategory(name='ROLLBACK_OCCURRED', exit_code=ROLLBACK_OCCURRED)
        else:
            return ErrorCategory(name='VALIDATION_FAILED', exit_code=VALIDATION_FAILED)

    def format_console_message(
        self,
        error: Optional[Exception] = None,
        include_rollback_info: bool = False
    ) -> str:
        """Format error as console-friendly message (no stack traces).

        Args:
            error: Exception to format (None for success message)
            include_rollback_info: If True, include backup location info

        Returns:
            User-friendly error message for console output
        """
        if error is None:
            return "Installation completed successfully."

        # Sanitize error message first (extract username from error string)
        error_str = self._sanitize_paths(str(error))

        error_category = self.categorize_error(error)
        category_info = self.ERROR_CATEGORIES.get(error_category.name, {})

        message = f"\n{category_info.get('label', 'ERROR')}\n"
        message += f"{category_info.get('description', '')}\n\n"

        # Include sanitized error details if available
        if error_str:
            message += f"Details: {error_str}\n\n"

        # Add resolution steps
        steps = category_info.get('resolution_steps', [])
        message += "Resolution steps:\n"
        for i, step in enumerate(steps[:3], 1):  # Max 3 steps
            message += f"  {i}. {step}\n"

        message += f"\nFor details, see log file: .devforgeai/install.log\n"

        # Add rollback/backup info if requested
        if include_rollback_info and self.backup_service:
            try:
                backup_path = self.backup_service.get_latest_backup()
                if backup_path:
                    message += f"\nBackup location: {backup_path}\n"
            except Exception:
                pass

        # Sanitize sensitive paths in final message
        message = self._sanitize_paths(message)

        return message

    def format_user_message(self, error: Exception) -> str:
        """Format error as user-friendly message (no stack traces).

        Args:
            error: Exception to format

        Returns:
            User-friendly error message
        """
        return self.format_console_message(error)

    def format_console_output(self, error_category: str, message: str) -> str:
        """Format error for console output with path sanitization.

        Args:
            error_category: Error category name
            message: Error message

        Returns:
            Sanitized console output
        """
        category_info = self.ERROR_CATEGORIES.get(error_category, {})

        output = f"\n{category_info.get('label', 'ERROR')}\n"
        output += f"{category_info.get('description', '')}\n\n"

        # Sanitize paths in message
        sanitized_message = self._sanitize_paths(message)
        output += sanitized_message + "\n\n"

        # Add resolution steps
        steps = category_info.get('resolution_steps', [])
        if steps:
            output += "Resolution steps:\n"
            for i, step in enumerate(steps[:3], 1):
                output += f"  {i}. {step}\n"

        output += f"\nFor details, see log file: .devforgeai/install.log\n"

        return output

    def _sanitize_paths(self, message: str) -> str:
        """Remove usernames from paths and mask sensitive files in error messages.

        Args:
            message: Message to sanitize

        Returns:
            Sanitized message
        """
        # Replace /home/username with /home/$USER
        message = re.sub(r'/home/[a-zA-Z0-9_-]+', '/home/$USER', message)

        # Mask sensitive paths like .ssh, .aws, .kube, .netrc, etc.
        sensitive_patterns = [
            r'\.ssh/[^\s]*',      # .ssh directory
            r'\.aws/[^\s]*',      # .aws directory
            r'\.kube/[^\s]*',     # .kube directory
            r'\.netrc[^\s]*',     # .netrc file
            r'\.docker/[^\s]*',   # .docker directory
            r'\.pgpass[^\s]*',    # .pgpass file
        ]

        for pattern in sensitive_patterns:
            if re.search(pattern, message):
                # If we find a sensitive path, add a note about it being sensitive
                message = message.replace(
                    re.search(pattern, message).group(0),
                    '<sensitive file path>'
                )
                # Add note about sensitive paths
                if 'sensitive' not in message.lower():
                    message = message.replace('Details:', 'Details (sensitive file path masked):')

        return message

    def get_resolution_steps(self, error: Optional[Exception] = None) -> List[str]:
        """Get resolution steps for error category.

        Args:
            error: Exception to get steps for (can be None for generic steps)

        Returns:
            List of 1-3 resolution steps (≤200 chars each)
        """
        if error is None:
            # Default generic steps
            return [
                'Check log file for details',
                'Verify source integrity'
            ]

        # Categorize the error to get its type
        error_category = self.categorize_error(error)
        category_info = self.ERROR_CATEGORIES.get(error_category.name, {})
        steps = category_info.get('resolution_steps', [])

        # Ensure ≤200 chars per step
        validated_steps = []
        for step in steps[:3]:  # Max 3 steps
            if len(step) <= 200:
                validated_steps.append(step)
            else:
                validated_steps.append(step[:197] + '...')

        return validated_steps

    def get_exit_code(
        self,
        error: Optional[Exception] = None,
        rollback_triggered: bool = False
    ) -> int:
        """Get exit code for an error.

        Args:
            error: Exception to get exit code for (None = SUCCESS)
            rollback_triggered: If True, return ROLLBACK_OCCURRED code

        Returns:
            Exit code (0, 1, 2, 3, or 4)
        """
        if error is None:
            return SUCCESS

        category = self.categorize_error(error, rollback_triggered=rollback_triggered)
        return category.exit_code

    def handle_error(
        self,
        error: Optional[Exception] = None,
        phase: Optional[str] = None,
        include_rollback_info: bool = False
    ) -> 'ErrorResult':
        """Handle error with rollback and logging.

        Args:
            error: Exception to handle
            phase: Installation phase where error occurred
            include_rollback_info: If True, include backup location in message

        Returns:
            ErrorResult with exit code and console message
        """
        # Handle KeyboardInterrupt (Ctrl+C)
        if isinstance(error, KeyboardInterrupt):
            # Trigger rollback
            if self.rollback_service:
                try:
                    self.rollback_service.rollback()
                except Exception as rollback_error:
                    # Log but don't crash
                    if self.logger:
                        self.logger.log_error(
                            error=rollback_error,
                            category="ROLLBACK_ERROR",
                            exit_code=ROLLBACK_OCCURRED,
                            message=f"Error during rollback: {rollback_error}"
                        )

            console_msg = "Installation cancelled by user (Ctrl+C). System has been rolled back."
            return ErrorResult(
                exit_code=ROLLBACK_OCCURRED,
                console_message=console_msg
            )

        # For other errors, determine if rollback is needed
        rollback_needed = phase == "file_copy"

        # Trigger rollback if needed
        if rollback_needed and error and self.rollback_service:
            try:
                self.rollback_service.rollback()
            except Exception as rollback_error:
                # Log rollback error but continue
                if self.logger:
                    self.logger.log_error(
                        error=rollback_error,
                        category="ROLLBACK_ERROR",
                        exit_code=ROLLBACK_OCCURRED,
                        message=f"Error during rollback (manual intervention may be needed): {rollback_error}"
                    )

        # Categorize the error
        if error is None:
            category = ErrorCategory(name='SUCCESS', exit_code=SUCCESS)
        else:
            category = self.categorize_error(
                error,
                rollback_triggered=rollback_needed and error is not None
            )

        # Log the error
        if error and self.logger:
            self.logger.log_error(
                error=error,
                category=category.name,
                exit_code=category.exit_code,
                message=str(error)
            )

        # Format console message
        console_message = self.format_console_message(
            error,
            include_rollback_info=include_rollback_info
        )

        return ErrorResult(
            exit_code=category.exit_code,
            console_message=console_message
        )

    def check_concurrent_installation(self, lock_file_exists: bool) -> None:
        """Check if another installation is already in progress.

        Args:
            lock_file_exists: Whether lock file exists

        Raises:
            RuntimeError: If concurrent installation detected
        """
        if lock_file_exists:
            raise RuntimeError(
                "Concurrent installation detected. Another installation is currently in progress. "
                "Wait for it to complete or remove the lock file at "
                ".devforgeai/install.lock"
            )

    def log_and_format_error(self, error: Exception, file_paths: Optional[Dict] = None) -> Tuple[str, int]:
        """Log error and return formatted message + exit code.

        Args:
            error: Exception to handle
            file_paths: Optional dict with 'source' and 'target' keys

        Returns:
            Tuple of (formatted_message, exit_code)
        """
        error_category = self.categorize_error(error)

        # Log to file
        self.logger.log_error(
            error=error,
            category=error_category.name,
            exit_code=error_category.exit_code,
            message=str(error),
            source_path=file_paths.get('source') if file_paths else None,
            target_path=file_paths.get('target') if file_paths else None
        )

        # Format for console
        message = self.format_user_message(error)

        return message, error_category.exit_code

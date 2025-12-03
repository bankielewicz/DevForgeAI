"""Error handler service (AC#1, AC#2, AC#3).

Categorizes errors, formats user-friendly messages, provides resolution steps.
"""
import re
from typing import Dict, List, Optional, Tuple
from .exit_codes import (
    SUCCESS,
    MISSING_SOURCE,
    PERMISSION_DENIED,
    ROLLBACK_OCCURRED,
    VALIDATION_FAILED,
)
from .install_logger import InstallLogger


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
                'Verify installation integrity',
                'Retry installation if files were modified'
            ]
        },
    }

    def __init__(self, logger: Optional[InstallLogger] = None):
        """Initialize error handler."""
        self.logger = logger or InstallLogger()

    def categorize_error(self, error: Exception) -> Tuple[str, int]:
        """Categorize error into one of 5 types and return exit code.

        Args:
            error: Exception to categorize

        Returns:
            Tuple of (category_name, exit_code)
        """
        error_str = str(error).lower()

        if 'not found' in error_str or 'no such file' in error_str:
            return ('MISSING_SOURCE', MISSING_SOURCE)
        elif 'permission' in error_str or 'denied' in error_str:
            return ('PERMISSION_DENIED', PERMISSION_DENIED)
        elif 'rollback' in error_str:
            return ('ROLLBACK_OCCURRED', ROLLBACK_OCCURRED)
        else:
            return ('VALIDATION_FAILED', VALIDATION_FAILED)

    def format_user_message(self, error: Exception) -> str:
        """Format error as user-friendly message (no stack traces).

        Args:
            error: Exception to format

        Returns:
            User-friendly error message
        """
        category, exit_code = self.categorize_error(error)
        category_info = self.ERROR_CATEGORIES.get(category, {})

        message = f"\n{category_info.get('label', 'ERROR')}\n"
        message += f"{category_info.get('description', '')}\n\n"

        # Add resolution steps
        steps = category_info.get('resolution_steps', [])
        message += "Resolution steps:\n"
        for i, step in enumerate(steps[:3], 1):  # Max 3 steps
            message += f"  {i}. {step}\n"

        message += f"\nFor details, see log file: .devforgeai/install.log\n"

        return message

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
        """Remove usernames from paths in error messages.

        Args:
            message: Message to sanitize

        Returns:
            Sanitized message
        """
        # Replace /home/username with /home/$USER
        message = re.sub(r'/home/[a-zA-Z0-9_-]+', '/home/$USER', message)
        return message

    def get_resolution_steps(self, error_category: str) -> List[str]:
        """Get resolution steps for error category.

        Args:
            error_category: Error category name

        Returns:
            List of 1-3 resolution steps (≤200 chars each)
        """
        category_info = self.ERROR_CATEGORIES.get(error_category, {})
        steps = category_info.get('resolution_steps', [])

        # Ensure ≤200 chars per step
        validated_steps = []
        for step in steps[:3]:  # Max 3 steps
            if len(step) <= 200:
                validated_steps.append(step)
            else:
                validated_steps.append(step[:197] + '...')

        return validated_steps

    def log_and_format_error(self, error: Exception, file_paths: Optional[Dict] = None) -> Tuple[str, int]:
        """Log error and return formatted message + exit code.

        Args:
            error: Exception to handle
            file_paths: Optional dict with 'source' and 'target' keys

        Returns:
            Tuple of (formatted_message, exit_code)
        """
        category, exit_code = self.categorize_error(error)

        # Log to file
        self.logger.log_error(
            category,
            exit_code,
            str(error),
            stack_trace=str(error),
            file_paths=file_paths
        )

        # Format for console
        message = self.format_user_message(error)

        return message, exit_code

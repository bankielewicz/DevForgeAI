"""Exit code constants for installer (AC#6).

Standardized return values for installation success/failure scenarios.

STORY-237: Enhanced Exit Codes
- Added DISK_SPACE_ERROR (5), NTFS_PERMISSION (6), FILE_LOCKED (7)
- Added platform-aware resolution messages via get_resolution_message()
"""

from typing import Optional


class ExitCodes:
    """Standard exit codes for installer process.

    AC#6: Exit Codes - Standardized Return Values
    - 0: SUCCESS - installation completed without errors
    - 1: MISSING_SOURCE - required source files not found
    - 2: PERMISSION_DENIED - insufficient permissions
    - 3: ROLLBACK_OCCURRED - error during installation, system rolled back
    - 4: VALIDATION_FAILED - installation completed but validation failed
    - 5: DISK_SPACE_ERROR - insufficient disk space (< 25MB)
    - 6: NTFS_PERMISSION - NTFS/WSL permission mismatch
    - 7: FILE_LOCKED - file locked by another process
    """

    # Success
    SUCCESS = 0

    # Error codes
    MISSING_SOURCE = 1
    PERMISSION_DENIED = 2
    ROLLBACK_OCCURRED = 3
    VALIDATION_FAILED = 4

    # New exit codes (STORY-237)
    DISK_SPACE_ERROR = 5
    NTFS_PERMISSION = 6
    FILE_LOCKED = 7


# Module-level constants for direct import
SUCCESS = ExitCodes.SUCCESS
MISSING_SOURCE = ExitCodes.MISSING_SOURCE
PERMISSION_DENIED = ExitCodes.PERMISSION_DENIED
ROLLBACK_OCCURRED = ExitCodes.ROLLBACK_OCCURRED
VALIDATION_FAILED = ExitCodes.VALIDATION_FAILED
DISK_SPACE_ERROR = ExitCodes.DISK_SPACE_ERROR
NTFS_PERMISSION = ExitCodes.NTFS_PERMISSION
FILE_LOCKED = ExitCodes.FILE_LOCKED


# Platform-aware resolution messages (STORY-237 AC#3, AC#5)
_RESOLUTION_MESSAGES: dict[int, dict[str, str]] = {
    ExitCodes.SUCCESS: {
        "default": "Installation completed successfully.",
    },
    ExitCodes.MISSING_SOURCE: {
        "default": "Required source files not found. Check the installation package.",
    },
    ExitCodes.PERMISSION_DENIED: {
        "linux": "Run with sudo or check file ownership with 'ls -la'.",
        "darwin": "Run with sudo or check Gatekeeper settings in System Preferences > Security.",
        "windows": "Run as Administrator. Right-click the installer and select 'Run as administrator'.",
        "wsl": "Run with sudo or use a Linux-native path like ~/projects/ instead of /mnt/c/.",
        "default": "Check permissions and try running with elevated privileges.",
    },
    ExitCodes.ROLLBACK_OCCURRED: {
        "default": "An error occurred during installation. Changes have been rolled back.",
    },
    ExitCodes.VALIDATION_FAILED: {
        "default": "Installation completed but validation failed. Check the installation logs.",
    },
    ExitCodes.DISK_SPACE_ERROR: {
        "linux": "Free up at least 25MB of disk space. Use 'df -h' to check available space and delete unnecessary files.",
        "darwin": "Free up at least 25MB of disk space. Use 'df -h' to check available space and clean up files.",
        "windows": "Free up at least 25MB of disk space. Use Disk Cleanup or delete unnecessary files.",
        "wsl": "Free up at least 25MB of disk space on the target filesystem.",
        "default": "Free up at least 25MB of disk space.",
    },
    ExitCodes.NTFS_PERMISSION: {
        "wsl": "Use a Linux-native path (e.g., ~/projects/) or remount with metadata: sudo mount -o remount,metadata /mnt/c",
        "linux": "Check file permissions. NTFS-specific issues are typically WSL-related.",
        "darwin": "Check file permissions with 'ls -la'.",
        "windows": "Check file permissions in Windows Explorer or run as Administrator.",
        "default": "Check file permissions. This may be an NTFS filesystem issue.",
    },
    ExitCodes.FILE_LOCKED: {
        "linux": "Close any programs that may have the files open (e.g., VS Code, text editors).",
        "darwin": "Close any programs that may have the files open (e.g., VS Code, Finder).",
        "windows": "Close VS Code, Explorer, or other programs that may have the files open.",
        "wsl": "Close VS Code, Explorer, or other Windows programs accessing the files.",
        "default": "Close any programs that may have the files open.",
    },
}


# Check name to exit code mapping (STORY-237 AC#4)
_CHECK_TO_EXIT_CODE: dict[str, int] = {
    "disk_space": ExitCodes.DISK_SPACE_ERROR,
    "write_permission": ExitCodes.PERMISSION_DENIED,
    "ntfs_permission": ExitCodes.NTFS_PERMISSION,
    "file_locked": ExitCodes.FILE_LOCKED,
    "platform_compatibility": ExitCodes.PERMISSION_DENIED,  # Fallback for platform issues
    "source_audit": ExitCodes.MISSING_SOURCE,
}


def get_exit_code_for_check(check_name: str, is_wsl: bool = False) -> int:
    """Get the appropriate exit code for a failed pre-flight check.

    Maps pre-flight check names to their corresponding exit codes.
    Used by the installer to return specific exit codes based on
    which pre-flight check failed.

    Args:
        check_name: The name of the failed check (e.g., "disk_space", "write_permission")
        is_wsl: True if running on WSL (affects NTFS permission handling)

    Returns:
        The exit code to use for this failure type.
        Returns PERMISSION_DENIED (2) for unknown check names.

    Examples:
        >>> get_exit_code_for_check("disk_space")
        5  # DISK_SPACE_ERROR

        >>> get_exit_code_for_check("write_permission", is_wsl=True)
        6  # NTFS_PERMISSION (on WSL, permission issues may be NTFS-related)
    """
    # Special handling for WSL permission issues
    if check_name == "write_permission" and is_wsl:
        return ExitCodes.NTFS_PERMISSION

    return _CHECK_TO_EXIT_CODE.get(check_name, ExitCodes.PERMISSION_DENIED)


def get_resolution_message(exit_code: int, platform: str) -> str:
    """Get a platform-specific resolution message for an exit code.

    Args:
        exit_code: The exit code (0-7).
        platform: The platform name (Linux, Windows, Darwin, WSL).
                  Case-insensitive.

    Returns:
        A string with actionable resolution steps for the given exit code
        and platform. Returns a generic message for unknown codes/platforms.

    Examples:
        >>> get_resolution_message(2, "Linux")
        "Run with sudo or check file ownership with 'ls -la'."

        >>> get_resolution_message(5, "Windows")
        "Free up at least 25MB of disk space. Use Disk Cleanup..."
    """
    # Normalize platform name to lowercase
    platform_lower = platform.lower() if platform else "unknown"

    # Get messages for this exit code
    code_messages = _RESOLUTION_MESSAGES.get(exit_code)

    if code_messages is None:
        # Unknown exit code
        return f"Unknown error (exit code {exit_code}). Check installation logs."

    # Try platform-specific message first, fall back to default
    message = code_messages.get(platform_lower)
    if message is None:
        message = code_messages.get("default", "An error occurred.")

    return message

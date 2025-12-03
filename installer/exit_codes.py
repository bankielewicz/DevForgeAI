"""Exit code constants for installer (AC#6).

Standardized return values for installation success/failure scenarios.
"""


class ExitCodes:
    """Standard exit codes for installer process.

    AC#6: Exit Codes - Standardized Return Values
    - 0: SUCCESS - installation completed without errors
    - 1: MISSING_SOURCE - required source files not found
    - 2: PERMISSION_DENIED - insufficient permissions
    - 3: ROLLBACK_OCCURRED - error during installation, system rolled back
    - 4: VALIDATION_FAILED - installation completed but validation failed
    """

    # Success
    SUCCESS = 0

    # Error codes
    MISSING_SOURCE = 1
    PERMISSION_DENIED = 2
    ROLLBACK_OCCURRED = 3
    VALIDATION_FAILED = 4


# Module-level constants for direct import
SUCCESS = ExitCodes.SUCCESS
MISSING_SOURCE = ExitCodes.MISSING_SOURCE
PERMISSION_DENIED = ExitCodes.PERMISSION_DENIED
ROLLBACK_OCCURRED = ExitCodes.ROLLBACK_OCCURRED
VALIDATION_FAILED = ExitCodes.VALIDATION_FAILED

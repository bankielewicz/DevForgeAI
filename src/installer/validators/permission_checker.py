"""
Write permission validation checker.

Verifies target directory is writable by creating temporary test file.
"""

from pathlib import Path
from .models import CheckResult


class PermissionChecker:
    """
    Validates write permissions at target installation path.

    Creates and deletes a temporary test file (.devforgeai-write-test).
    """

    def __init__(self, target_path: str):
        """
        Initialize permission checker.

        Args:
            target_path: Directory path to check for write permissions
        """
        self.target_path = Path(target_path)
        self.test_filename = ".devforgeai-write-test"

    def check(self) -> CheckResult:
        """
        Check write permissions.

        Returns:
            CheckResult with PASS if writable, FAIL if not

        Process:
            1. Create temporary test file
            2. Delete test file immediately
            3. Return result based on success/failure

        Performance:
            Completes in <100ms

        Security:
            - No privilege escalation attempts
            - Safe file operations only
        """
        test_file = self.target_path / self.test_filename

        # Check if target exists and is directory
        if not self.target_path.exists():
            return CheckResult(
                check_name="Write Permissions",
                status="FAIL",
                message=f"Target directory does not exist: {self.target_path}"
            )

        if not self.target_path.is_dir():
            return CheckResult(
                check_name="Write Permissions",
                status="FAIL",
                message=f"Target path is not a directory: {self.target_path}"
            )

        try:
            # Attempt to create test file
            test_file.touch()

            # Successfully created - now delete it
            try:
                test_file.unlink()
            except Exception:
                # Deletion failed, but write succeeded
                pass

            return CheckResult(
                check_name="Write Permissions",
                status="PASS",
                message="Directory is writable"
            )

        except PermissionError:
            return CheckResult(
                check_name="Write Permissions",
                status="FAIL",
                message=f"Permission denied - cannot write to {self.target_path}. "
                        f"Choose a different directory or check directory permissions."
            )
        except OSError as e:
            return CheckResult(
                check_name="Write Permissions",
                status="FAIL",
                message=f"Cannot write to directory: {str(e)}"
            )
        except Exception as e:
            return CheckResult(
                check_name="Write Permissions",
                status="FAIL",
                message=f"Unexpected error during write permission check: {str(e)}"
            )
        finally:
            # Cleanup: ensure test file is deleted
            try:
                if test_file.exists():
                    test_file.unlink()
            except Exception:
                # Cleanup failed, but we've already determined result
                pass

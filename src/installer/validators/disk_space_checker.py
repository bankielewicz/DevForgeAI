"""
Disk space validation checker.

Verifies sufficient free space for installation (≥100MB).
"""

import shutil
from pathlib import Path
from .models import CheckResult


class DiskSpaceChecker:
    """
    Validates available disk space at target installation path.

    Uses shutil.disk_usage() to calculate free space.
    """

    def __init__(self, target_path: str, min_space_mb: int = 100):
        """
        Initialize disk space checker.

        Args:
            target_path: Directory path to check
            min_space_mb: Minimum required space in MB (default: 100)
        """
        self.target_path = Path(target_path)
        self.min_space_mb = min_space_mb

    def check(self) -> CheckResult:
        """
        Check available disk space.

        Returns:
            CheckResult with PASS if ≥100MB, FAIL if <100MB, WARN on errors

        Performance:
            Completes in <200ms
        """
        try:
            # Get disk usage statistics
            usage = shutil.disk_usage(self.target_path)

            # Convert bytes to MB
            free_mb = usage.free / (1024 * 1024)

            if free_mb >= self.min_space_mb:
                return CheckResult(
                    check_name="Disk Space",
                    status="PASS",
                    message=f"{int(free_mb)}MB available (required: {self.min_space_mb}MB)"
                )
            else:
                return CheckResult(
                    check_name="Disk Space",
                    status="FAIL",
                    message=f"Insufficient space: {int(free_mb)}MB available, {self.min_space_mb}MB required. "
                            f"Free up space or choose different installation directory."
                )

        except PermissionError:
            return CheckResult(
                check_name="Disk Space",
                status="WARN",
                message="Permission denied accessing target path for disk space calculation"
            )
        except FileNotFoundError:
            return CheckResult(
                check_name="Disk Space",
                status="WARN",
                message="Target path not found - disk space cannot be calculated"
            )
        except OSError as e:
            return CheckResult(
                check_name="Disk Space",
                status="WARN",
                message=f"Error calculating disk space: {str(e)}"
            )
        except Exception as e:
            return CheckResult(
                check_name="Disk Space",
                status="WARN",
                message=f"Unexpected error during disk space check: {str(e)}"
            )

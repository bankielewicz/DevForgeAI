"""
Python version validation checker.

Detects Python 3.10+ installation via subprocess.
"""

import subprocess
import re
from typing import Optional
from .models import CheckResult


class PythonVersionChecker:
    """
    Validates Python version availability and compatibility.

    Tries multiple Python executables in priority order and checks
    version against minimum requirement (3.10+).
    """

    def __init__(self, min_version: str = "3.10"):
        """
        Initialize Python version checker.

        Args:
            min_version: Minimum required Python version (default: "3.10")
        """
        self.min_version = min_version
        self.executables = ["python3", "python", "python3.11", "python3.10"]

    def check(self) -> CheckResult:
        """
        Check Python version availability.

        Returns:
            CheckResult with PASS if ≥3.10, WARN if <3.10 or missing

        Performance:
            Completes in <500ms
        """
        for executable in self.executables:
            try:
                # Execute python --version with subprocess
                result = subprocess.run(
                    [executable, "--version"],
                    capture_output=True,
                    text=True,
                    shell=False,  # Security: no shell injection
                    timeout=5
                )

                if result.returncode == 0:
                    # Parse version from output
                    version_str = result.stdout.strip()
                    version = self._parse_version(version_str)

                    if version:
                        # Compare against minimum
                        if self._is_version_sufficient(version):
                            return CheckResult(
                                check_name="Python Version",
                                status="PASS",
                                message=f"Python {version} found"
                            )
                        else:
                            return CheckResult(
                                check_name="Python Version",
                                status="WARN",
                                message=f"Python {version} found (3.10+ recommended for CLI validators, optional for framework)"
                            )
                    else:
                        # Could not parse version
                        return CheckResult(
                            check_name="Python Version",
                            status="WARN",
                            message=f"Could not parse Python version from: {version_str}"
                        )
                else:
                    # Non-zero return code, try next executable
                    continue

            except FileNotFoundError:
                # Executable not found, try next
                continue
            except subprocess.TimeoutExpired:
                # Timeout, try next
                continue
            except Exception:
                # Any other error, try next
                continue

        # No Python executable found
        return CheckResult(
            check_name="Python Version",
            status="WARN",
            message="Python not found (optional - CLI validators will be disabled, framework installation can proceed)"
        )

    def _parse_version(self, version_str: str) -> Optional[str]:
        """
        Parse version number from Python --version output.

        Args:
            version_str: Output from python --version

        Returns:
            Version string (e.g., "3.11.4") or None if parse fails

        Uses regex pattern: Python (\\d+)\\.(\\d+)\\.(\\d+)
        """
        match = re.search(r'Python (\d+)\.(\d+)\.(\d+)', version_str)
        if match:
            return f"{match.group(1)}.{match.group(2)}.{match.group(3)}"
        return None

    def _is_version_sufficient(self, version: str) -> bool:
        """
        Check if version meets minimum requirement.

        Args:
            version: Version string (e.g., "3.11.4")

        Returns:
            True if version >= min_version
        """
        try:
            # Parse version parts
            parts = version.split(".")
            major = int(parts[0])
            minor = int(parts[1])

            # Parse minimum version
            min_parts = self.min_version.split(".")
            min_major = int(min_parts[0])
            min_minor = int(min_parts[1])

            # Compare
            if major > min_major:
                return True
            elif major == min_major:
                return minor >= min_minor
            else:
                return False

        except (ValueError, IndexError):
            return False

"""
Data models for pre-flight validation results.

Provides immutable data structures for validation checks and results.
"""

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class CheckResult:
    """
    Result of a single validation check.

    Args:
        check_name: Name of the check (e.g., "Python Version")
        status: One of PASS/WARN/FAIL
        message: Descriptive message with context and resolution steps

    Raises:
        ValueError: If check_name or message is empty, or status is invalid
    """
    check_name: str
    status: str
    message: str

    def __post_init__(self):
        """Validate field constraints."""
        if not self.check_name or not self.check_name.strip():
            raise ValueError("check_name must be non-empty string")

        if self.status not in ("PASS", "WARN", "FAIL"):
            raise ValueError(f"status must be PASS/WARN/FAIL, got '{self.status}'")

        if not self.message or not self.message.strip():
            raise ValueError("message must be non-empty string")

    def __str__(self) -> str:
        """String representation for display."""
        return f"{self.check_name}: {self.status}"

    @staticmethod
    def create_pass(check_name: str, message: str) -> "CheckResult":
        """
        Create PASS status check result.

        Args:
            check_name: Name of the check
            message: Success message

        Returns:
            CheckResult with PASS status
        """
        return CheckResult(check_name=check_name, status="PASS", message=message)

    @staticmethod
    def create_warn(check_name: str, message: str) -> "CheckResult":
        """
        Create WARN status check result.

        Args:
            check_name: Name of the check
            message: Warning message

        Returns:
            CheckResult with WARN status
        """
        return CheckResult(check_name=check_name, status="WARN", message=message)

    @staticmethod
    def create_fail(check_name: str, message: str) -> "CheckResult":
        """
        Create FAIL status check result.

        Args:
            check_name: Name of the check
            message: Failure message

        Returns:
            CheckResult with FAIL status
        """
        return CheckResult(check_name=check_name, status="FAIL", message=message)


@dataclass
class ValidationResult:
    """
    Result of all pre-flight validation checks.

    Args:
        checks: List of exactly 4 CheckResult objects

    Properties:
        all_pass: True if all checks have status PASS
        warnings_present: True if any check has status WARN
        critical_failures: True if any check has status FAIL

    Raises:
        ValueError: If checks list is not exactly 4 elements
        TypeError: If checks list contains non-CheckResult objects
    """
    checks: List[CheckResult]

    def __post_init__(self):
        """Validate checks list."""
        if not isinstance(self.checks, list):
            raise TypeError("checks must be a list")

        if len(self.checks) == 0:
            raise ValueError("checks list cannot be empty")

        if len(self.checks) != 4:
            raise ValueError(f"checks list must contain exactly 4 elements, got {len(self.checks)}")

        # Validate each check has required attributes (duck typing for test mocks)
        for check in self.checks:
            if not hasattr(check, 'check_name') or not hasattr(check, 'status') or not hasattr(check, 'message'):
                raise TypeError(f"All checks must have check_name, status, and message attributes, got {type(check)}")

    @property
    def all_pass(self) -> bool:
        """Return True if all checks passed."""
        return all(check.status == "PASS" for check in self.checks)

    @property
    def warnings_present(self) -> bool:
        """Return True if any check has WARN status."""
        return any(check.status == "WARN" for check in self.checks)

    @property
    def critical_failures(self) -> bool:
        """Return True if any check has FAIL status."""
        return any(check.status == "FAIL" for check in self.checks)

    def __str__(self) -> str:
        """String representation showing summary."""
        return f"ValidationResult(4 checks, PASS={sum(1 for c in self.checks if c.status == 'PASS')}, " \
               f"WARN={sum(1 for c in self.checks if c.status == 'WARN')}, " \
               f"FAIL={sum(1 for c in self.checks if c.status == 'FAIL')})"

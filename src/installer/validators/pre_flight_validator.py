"""
Pre-flight validation orchestrator.

Coordinates all validation checks and produces structured results.
"""

from typing import Optional
from .models import ValidationResult, CheckResult
from .python_checker import PythonVersionChecker
from .disk_space_checker import DiskSpaceChecker
from .installation_detector import ExistingInstallationDetector
from .permission_checker import PermissionChecker


class PreFlightValidator:
    """
    Orchestrates all pre-flight validation checks.

    Runs 4 validation checks in sequence and produces structured ValidationResult.
    """

    def __init__(
        self,
        python_checker: Optional[PythonVersionChecker] = None,
        disk_checker: Optional[DiskSpaceChecker] = None,
        installation_detector: Optional[ExistingInstallationDetector] = None,
        permission_checker: Optional[PermissionChecker] = None
    ):
        """
        Initialize pre-flight validator with checkers.

        Args:
            python_checker: Python version checker (optional, uses default if None)
            disk_checker: Disk space checker (optional)
            installation_detector: Installation detector (optional)
            permission_checker: Permission checker (optional)

        Dependency Injection:
            All checkers injected for testability
        """
        self.python_checker = python_checker
        self.disk_checker = disk_checker
        self.installation_detector = installation_detector
        self.permission_checker = permission_checker

    def validate(self, force: bool = False) -> ValidationResult:
        """
        Execute all pre-flight validation checks.

        Args:
            force: If True, bypass warning prompts (but not failures)

        Returns:
            ValidationResult with all check results and computed outcome flags

        Business Rules:
            - BR-001: FAIL checks block installation
            - BR-002: WARN checks prompt user (unless force=True)
            - BR-003: force flag bypasses WARN only, never FAIL
            - BR-004: All checks run even if early check fails

        Performance:
            Completes in <5 seconds
        """
        checks = []

        # Run all 4 checks (BR-004: all checks run even if early failure)
        if self.python_checker:
            checks.append(self.python_checker.check())

        if self.disk_checker:
            checks.append(self.disk_checker.check())

        if self.installation_detector:
            checks.append(self.installation_detector.check())

        if self.permission_checker:
            checks.append(self.permission_checker.check())

        # Create ValidationResult (computes outcome flags)
        result = ValidationResult(checks=checks)

        return result

    def format_summary(self, result: ValidationResult) -> str:
        """
        Format validation results as human-readable table.

        Args:
            result: ValidationResult to format

        Returns:
            Formatted string with table and overall result

        Format:
            ┌─────────────────────────────────────────────────┐
            │  Check Name         │ Status │ Message          │
            ├─────────────────────────────────────────────────┤
            │  Python Version     │ ✓ PASS │ Python 3.11.4... │
            │  Disk Space         │ ⚠ WARN │ 50MB available...│
            │  Installation       │ ✓ PASS │ No existing...   │
            │  Permissions        │ ✗ FAIL │ Permission...    │
            └─────────────────────────────────────────────────┘
            Overall: Critical failures detected (installation blocked)
        """
        lines = []

        # Header
        lines.append("=" * 80)
        lines.append("PRE-FLIGHT VALIDATION RESULTS")
        lines.append("=" * 80)
        lines.append("")

        # Check results table
        for check in result.checks:
            # Status indicator
            if check.status == "PASS":
                indicator = "✓ PASS"
            elif check.status == "WARN":
                indicator = "⚠ WARN"
            else:  # FAIL
                indicator = "✗ FAIL"

            # Format check line
            lines.append(f"{check.check_name:25} {indicator:10} {check.message}")

        lines.append("")
        lines.append("=" * 80)

        # Overall result
        if result.all_pass:
            lines.append("Overall: All checks passed - installation can proceed")
        elif result.critical_failures:
            lines.append("Overall: Critical failures detected - installation blocked")
            lines.append("Resolution: Fix failures above and retry")
        elif result.warnings_present:
            lines.append("Overall: Warnings present - review warnings before proceeding")
            lines.append("Resolution: Address warnings or use --force to continue")
        else:
            lines.append("Overall: Unknown status")

        lines.append("=" * 80)

        return "\n".join(lines)

"""
Pre-Flight Validator Module for DevForgeAI Installer (STORY-236)

Provides pre-flight validation checks before deployment begins, including
disk space, write permissions, platform compatibility, and source file audit.

Usage:
    from installer.preflight import PreflightValidator, PreflightResult

    validator = PreflightValidator(target_dir="/path/to/target")
    result = validator.validate()

    if result.passed:
        print("All checks passed!")
    else:
        for error in result.errors:
            print(f"Error: {error}")

Business Rules:
    - BR-001: All checks complete even if one fails (no early exit)
    - BR-002: Test file cleanup must happen in finally block
    - BR-003: Overall passed=True only if no FAIL checks
"""

import os
import shutil
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Union

from installer.platform_detector import PlatformDetector, PlatformInfo


# Exclusion patterns for source file audit (from deploy.py)
EXCLUDE_PATTERNS = {
    "__pycache__",
    ".git",
    ".pytest_cache",
    ".mypy_cache",
    ".venv",
    "venv",
    "node_modules",
    ".env",
    "*.pyc",
    "*.pyo",
    ".DS_Store",
    "Thumbs.db",
}

# Directories that should never be deployed
NO_DEPLOY_DIRS = {
    "__pycache__",
    ".git",
    ".pytest_cache",
    ".mypy_cache",
    "node_modules",
}


@dataclass
class CheckResult:
    """
    Result of a single pre-flight check.

    Attributes:
        name: Check identifier (e.g., 'disk_space', 'write_permission')
        status: Check outcome - "PASS", "WARN", or "FAIL"
        message: Human-readable description of check result
    """

    name: str
    status: str  # "PASS", "WARN", "FAIL"
    message: str


@dataclass
class PreflightResult:
    """
    Aggregated results from all pre-flight checks.

    Attributes:
        passed: True if no FAIL checks, False otherwise
        checks: List of individual check results
        platform_info: Platform detection results from PlatformDetector
        warnings: Warning messages from WARN status checks
        errors: Error messages from FAIL status checks
        file_count: Total file count (for dry-run mode)
        exclusions: List of excluded patterns (for dry-run mode)
        dry_run_info: Additional dry-run information (if applicable)
        audit_info: Source file audit information (if source_dir provided)
    """

    passed: bool
    checks: List[CheckResult]
    platform_info: PlatformInfo
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    file_count: Optional[int] = None
    exclusions: Optional[List[str]] = None
    dry_run_info: Optional[dict] = None
    audit_info: Optional[dict] = None


class PreflightValidator:
    """
    Pre-flight validation service for the DevForgeAI installer.

    Performs validation checks before deployment including disk space,
    write permissions, platform compatibility, and source file audit.

    Args:
        target_dir: Target directory for installation
        source_dir: Optional source directory to audit
        dry_run: If True, generates detailed preview report
        min_disk_space_mb: Minimum required disk space in MB (default: 25)

    Example:
        >>> validator = PreflightValidator(target_dir="/home/user/project")
        >>> result = validator.validate()
        >>> print(f"Passed: {result.passed}")
    """

    # Default minimum disk space requirement
    DEFAULT_MIN_DISK_SPACE_MB = 25

    def __init__(
        self,
        target_dir: Union[str, Path],
        source_dir: Optional[Union[str, Path]] = None,
        dry_run: bool = False,
        min_disk_space_mb: int = DEFAULT_MIN_DISK_SPACE_MB,
    ):
        """Initialize the PreflightValidator with configuration."""
        self.target_dir = str(target_dir)
        self.source_dir = str(source_dir) if source_dir else None
        self.dry_run = dry_run
        self.min_disk_space_mb = min_disk_space_mb

    def _collect_check_result(
        self,
        check: CheckResult,
        checks: List[CheckResult],
        warnings: List[str],
        errors: List[str],
    ) -> None:
        """
        Process a check result by appending to appropriate collections.

        Centralizes the pattern of collecting check results into checks list
        and routing messages to warnings/errors based on status.

        Args:
            check: The check result to process
            checks: List to append check to
            warnings: List to append warning messages to
            errors: List to append error messages to
        """
        checks.append(check)
        if check.status == "FAIL":
            errors.append(check.message)
        elif check.status == "WARN":
            warnings.append(check.message)

    def validate(self) -> PreflightResult:
        """
        Run all pre-flight checks and return aggregated results.

        BR-001: All checks complete even if one fails (no early exit).
        BR-003: passed=True only if no FAIL checks.

        Returns:
            PreflightResult with all check results aggregated
        """
        checks: List[CheckResult] = []
        warnings: List[str] = []
        errors: List[str] = []

        # Get platform info first (needed for other checks)
        platform_info = PlatformDetector.detect(self.target_dir)

        # BR-001: Run ALL checks even if one fails
        # Check 1: Disk space
        self._collect_check_result(
            self._check_disk_space(), checks, warnings, errors
        )

        # Check 2: Write permission
        self._collect_check_result(
            self._check_write_permission(), checks, warnings, errors
        )

        # Check 3: Platform compatibility
        self._collect_check_result(
            self._check_platform_compatibility(platform_info), checks, warnings, errors
        )

        # Check 4: Source file audit (if source_dir provided)
        audit_info = None
        if self.source_dir:
            audit_check, audit_info = self._audit_source_files()
            self._collect_check_result(audit_check, checks, warnings, errors)

        # BR-003: passed=True only if no FAIL checks
        passed = all(check.status != "FAIL" for check in checks)

        # Build result
        result = PreflightResult(
            passed=passed,
            checks=checks,
            platform_info=platform_info,
            warnings=warnings,
            errors=errors,
        )

        # Add dry-run info if applicable
        if self.dry_run:
            result.file_count = audit_info.get("total_files", 0) if audit_info else 0
            result.exclusions = list(EXCLUDE_PATTERNS)
            result.dry_run_info = {
                "total_files": result.file_count,
                "exclusion_patterns": result.exclusions,
                "warnings": warnings,
                "status": "READY" if passed else "NOT READY",
            }

        # Add audit info if available
        if audit_info:
            result.audit_info = audit_info

        return result

    def _check_disk_space(self) -> CheckResult:
        """
        Check if sufficient disk space is available.

        SVC-001: Check disk space with configurable minimum (default 25MB).

        Returns:
            CheckResult with status PASS if >= threshold, FAIL otherwise
        """
        check_name = "disk_space"
        threshold_bytes = self.min_disk_space_mb * 1024 * 1024

        try:
            usage = shutil.disk_usage(self.target_dir)
            free_mb = usage.free / (1024 * 1024)

            if usage.free >= threshold_bytes:
                return CheckResult(
                    name=check_name,
                    status="PASS",
                    message=f"Disk space OK: {free_mb:.1f} MB available (>= {self.min_disk_space_mb} MB required)",
                )
            else:
                return CheckResult(
                    name=check_name,
                    status="FAIL",
                    message=f"Insufficient disk space: {free_mb:.1f} MB available, {self.min_disk_space_mb} MB required",
                )

        except FileNotFoundError:
            return CheckResult(
                name=check_name,
                status="FAIL",
                message=f"Target directory does not exist: {self.target_dir}",
            )
        except PermissionError:
            return CheckResult(
                name=check_name,
                status="FAIL",
                message=f"Permission denied checking disk space: {self.target_dir}",
            )
        except OSError as e:
            return CheckResult(
                name=check_name,
                status="FAIL",
                message=f"Error checking disk space: {e}",
            )

    def _check_write_permission(self) -> CheckResult:
        """
        Probe write permission by creating/deleting test file.

        SVC-002: Probe write permission by creating/deleting test file.
        BR-002: Test file cleanup must happen in finally block.

        Returns:
            CheckResult with status PASS if writable, FAIL on PermissionError
        """
        check_name = "write_permission"
        timestamp = int(time.time() * 1000)
        test_file_name = f".devforgeai-permission-test-{timestamp}"
        test_file_path = os.path.join(self.target_dir, test_file_name)

        try:
            # Try to create and write to test file
            with open(test_file_path, "w") as f:
                f.write("DevForgeAI permission test")

            return CheckResult(
                name=check_name,
                status="PASS",
                message=f"Write permission OK: {self.target_dir}",
            )

        except PermissionError:
            return CheckResult(
                name=check_name,
                status="FAIL",
                message=f"Permission denied: Cannot write to {self.target_dir}",
            )
        except OSError as e:
            return CheckResult(
                name=check_name,
                status="FAIL",
                message=f"Error checking write permission: {e}",
            )
        finally:
            # BR-002: Cleanup in finally block - ALWAYS attempt cleanup
            try:
                if os.path.exists(test_file_path):
                    os.unlink(test_file_path)
            except OSError:
                # Log warning but don't raise - cleanup failure is non-fatal
                pass

    def _check_platform_compatibility(self, platform_info: PlatformInfo) -> CheckResult:
        """
        Check platform compatibility and generate warnings.

        SVC-003: Invoke PlatformDetector and include results.
        SVC-004: Generate compatibility warnings for WSL/NTFS scenarios.

        Args:
            platform_info: Platform detection results

        Returns:
            CheckResult with WARN for cross-filesystem/chmod issues, PASS otherwise
        """
        check_name = "platform_compatibility"
        warnings_list = []

        # Check for cross-filesystem scenario (WSL accessing NTFS)
        if platform_info.is_cross_filesystem:
            warnings_list.append(
                "Cross-filesystem detected: chmod operations may not work"
            )

        # Check for chmod support
        if not platform_info.supports_chmod:
            warnings_list.append(
                f"chmod not supported on {platform_info.filesystem} filesystem"
            )

        # WSL-specific warning
        if platform_info.is_wsl and platform_info.filesystem == "ntfs-wsl":
            warnings_list.append(
                "WSL accessing NTFS path: File permissions may not be preserved"
            )

        if warnings_list:
            return CheckResult(
                name=check_name,
                status="WARN",
                message="; ".join(warnings_list),
            )
        else:
            return CheckResult(
                name=check_name,
                status="PASS",
                message=f"Platform compatible: {platform_info.os_type} ({platform_info.filesystem})",
            )

    def _audit_source_files(self) -> tuple[CheckResult, dict]:
        """
        Audit source files and categorize by criticality.

        SVC-005: Audit source files and categorize by criticality.

        Returns:
            Tuple of (CheckResult, audit_info dict)
        """
        check_name = "source_audit"
        audit_info = {
            "total_files": 0,
            "included_files": 0,
            "excluded_files": 0,
            "excluded_patterns_matched": [],
        }

        if not self.source_dir or not os.path.exists(self.source_dir):
            return (
                CheckResult(
                    name=check_name,
                    status="FAIL",
                    message=f"Source directory does not exist: {self.source_dir}",
                ),
                audit_info,
            )

        try:
            total_count = 0
            included_count = 0
            excluded_count = 0
            excluded_patterns_matched = set()

            for root, dirs, files in os.walk(self.source_dir):
                # Filter out excluded directories
                dirs[:] = [
                    d for d in dirs
                    if d not in NO_DEPLOY_DIRS and d not in EXCLUDE_PATTERNS
                ]

                for file_name in files:
                    total_count += 1

                    # Check if file matches exclusion pattern
                    excluded = False
                    for pattern in EXCLUDE_PATTERNS:
                        if pattern.startswith("*"):
                            # Wildcard pattern (e.g., *.pyc)
                            if file_name.endswith(pattern[1:]):
                                excluded = True
                                excluded_patterns_matched.add(pattern)
                                break
                        elif file_name == pattern:
                            excluded = True
                            excluded_patterns_matched.add(pattern)
                            break

                    if excluded:
                        excluded_count += 1
                    else:
                        included_count += 1

            audit_info = {
                "total_files": total_count,
                "included_files": included_count,
                "excluded_files": excluded_count,
                "excluded_patterns_matched": list(excluded_patterns_matched),
            }

            return (
                CheckResult(
                    name=check_name,
                    status="PASS",
                    message=f"Source audit complete: {total_count} total files, {included_count} to deploy, {excluded_count} excluded",
                ),
                audit_info,
            )

        except OSError as e:
            return (
                CheckResult(
                    name=check_name,
                    status="FAIL",
                    message=f"Error auditing source files: {e}",
                ),
                audit_info,
            )

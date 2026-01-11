"""
Repair Manager for DevForgeAI (STORY-251)

Provides repair operations for corrupted DevForgeAI installations:
- AC#2: Repair corrupted installation

Usage:
    from installer.repair import RepairManager

    manager = RepairManager(target_path=Path("/path/to/project"))
    report = manager.repair()
"""

import hashlib
import json
import logging
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

from installer.exit_codes import ExitCodes

logger = logging.getLogger(__name__)


@dataclass
class Issue:
    """Represents a detected file issue."""
    file_path: str
    issue_type: str  # "MISSING" or "CORRUPTED"
    expected_checksum: Optional[str] = None
    actual_checksum: Optional[str] = None


@dataclass
class RepairReport:
    """Report of repair operation."""
    issues_found: int = 0
    issues_fixed: int = 0
    issues_skipped: int = 0
    preserved_files: List[str] = field(default_factory=list)
    dry_run: bool = False
    message: str = ""


class RepairManager:
    """
    Manages repair operations for corrupted DevForgeAI installations.

    Implements AC#2: Repair Corrupted Installation.
    """

    VERSION_MARKER_FILE = ".devforgeai_installed"

    # User files to preserve during repair
    USER_FILE_PATTERNS = [
        "*.user.yaml",
        "*.user.json",
        "*.story.md",
        "custom-*",
    ]

    def __init__(self, target_path: Path, source_root: Optional[Path] = None):
        """
        Initialize RepairManager.

        Args:
            target_path: Path to DevForgeAI installation
            source_root: Path to source files for restoration
        """
        self.target_path = Path(target_path)
        self.source_root = Path(source_root) if source_root else None
        self._version_data: Optional[Dict] = None

        # Load version data
        self._load_version_data()

    def _load_version_data(self) -> None:
        """Load version data from marker file."""
        marker_path = self.target_path / self.VERSION_MARKER_FILE
        if marker_path.exists():
            try:
                self._version_data = json.loads(marker_path.read_text())
            except json.JSONDecodeError:
                logger.warning(f"Failed to parse version marker: {marker_path}")
                self._version_data = None

    def _compute_checksum(self, file_path: Path) -> str:
        """Compute SHA256 checksum of file."""
        sha256 = hashlib.sha256()
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(65536), b''):
                    sha256.update(chunk)
            return f"sha256:{sha256.hexdigest()}"
        except Exception as e:
            logger.error(f"Failed to compute checksum for {file_path}: {e}")
            return ""

    def _scan_for_issues(self) -> List[Issue]:
        """
        Scan installation for missing or corrupted files (AC#2).

        Returns:
            List of detected issues
        """
        issues = []

        if not self._version_data:
            logger.warning("No version data available for integrity check")
            return issues

        checksums = self._version_data.get("checksums", {})

        for file_path, expected_checksum in checksums.items():
            full_path = self.target_path / file_path

            if not full_path.exists():
                issues.append(Issue(
                    file_path=file_path,
                    issue_type="MISSING",
                    expected_checksum=expected_checksum
                ))
            else:
                actual_checksum = self._compute_checksum(full_path)
                if actual_checksum != expected_checksum:
                    issues.append(Issue(
                        file_path=file_path,
                        issue_type="CORRUPTED",
                        expected_checksum=expected_checksum,
                        actual_checksum=actual_checksum
                    ))

        return issues

    def _display_repair_plan(self, issues: List[Issue]) -> None:
        """
        Display repair plan to user (AC#2).

        Args:
            issues: List of detected issues
        """
        if not issues:
            print("No issues found. Installation is healthy.")
            return

        print("\nFound issues:")

        missing = [i for i in issues if i.issue_type == "MISSING"]
        corrupted = [i for i in issues if i.issue_type == "CORRUPTED"]

        if missing:
            print(f"  - Missing: {len(missing)} files")
            for issue in missing:
                print(f"    • {issue.file_path}")

        if corrupted:
            print(f"  - Corrupted: {len(corrupted)} files (checksum mismatch)")
            for issue in corrupted:
                print(f"    • {issue.file_path}")

        print("\nRepair will:")
        if missing:
            print(f"  - Restore {len(missing)} missing file(s)")
        if corrupted:
            print(f"  - Replace {len(corrupted)} corrupted file(s)")
        print("  - Preserve user configurations")
        print("")

    def _confirm_repair(self) -> bool:
        """
        Prompt user to confirm repair.

        Returns:
            True if user confirms
        """
        try:
            response = input("Proceed with repair? [Y/n] ").strip().lower()
            return response in ('', 'y', 'yes')
        except EOFError:
            return False

    def _is_user_file(self, file_path: str) -> bool:
        """Check if file is a user-created file to preserve."""
        path = Path(file_path)
        name = path.name

        for pattern in self.USER_FILE_PATTERNS:
            if pattern.startswith("*"):
                if name.endswith(pattern[1:]):
                    return True
            elif pattern.endswith("*"):
                if name.startswith(pattern[:-1]):
                    return True
            elif name == pattern:
                return True

        return False

    def _validate_path(self, file_path: str) -> bool:
        """
        Validate path doesn't escape target directory (path traversal protection).

        Args:
            file_path: Relative file path to validate

        Returns:
            True if path is safe, False if it escapes target directory
        """
        try:
            # Normalize and resolve the path
            target = (self.target_path / file_path).resolve()

            # Ensure it's within target_path
            target.relative_to(self.target_path.resolve())
            return True
        except ValueError:
            logger.error(f"Security violation: Path escapes target directory: {file_path}")
            return False

    def _apply_repairs(self, issues: List[Issue]) -> int:
        """
        Apply repairs to fix issues.

        Args:
            issues: List of issues to fix

        Returns:
            Number of issues fixed
        """
        fixed = 0

        if not self.source_root or not self.source_root.exists():
            logger.warning("No source root available for repairs")
            return fixed

        for issue in issues:
            # Skip user files
            if self._is_user_file(issue.file_path):
                continue

            # Validate path doesn't escape target directory
            if not self._validate_path(issue.file_path):
                continue

            source_path = self.source_root / issue.file_path
            target_path = self.target_path / issue.file_path

            # Validate no symlinks (security)
            if source_path.is_symlink():
                logger.warning(f"Skipping symlink: {source_path}")
                continue

            try:
                if source_path.exists():
                    # Create parent directories
                    target_path.parent.mkdir(parents=True, exist_ok=True)

                    # Copy file
                    shutil.copy2(source_path, target_path)
                    fixed += 1
                    logger.info(f"Restored: {issue.file_path}")
                else:
                    logger.warning(f"Source not found: {source_path}")
            except Exception as e:
                logger.error(f"Failed to restore {issue.file_path}: {e}")

        return fixed

    def repair(self, dry_run: bool = False, force: bool = False) -> RepairReport:
        """
        Repair corrupted installation (AC#2).

        Args:
            dry_run: If True, simulate repair without making changes
            force: If True, skip confirmation prompt (for silent mode)

        Returns:
            RepairReport with results
        """
        report = RepairReport(dry_run=dry_run)

        # Scan for issues
        issues = self._scan_for_issues()
        report.issues_found = len(issues)

        if not issues:
            report.message = "No issues found"
            return report

        # Display repair plan
        self._display_repair_plan(issues)

        if dry_run:
            report.message = "Dry-run complete (no changes made)"
            return report

        # Confirm with user (unless force mode or already confirmed)
        if not force and not self._confirm_repair():
            report.message = "Repair cancelled by user"
            return report

        # Apply repairs
        report.issues_fixed = self._apply_repairs(issues)
        report.issues_skipped = report.issues_found - report.issues_fixed

        # Collect preserved files
        for issue in issues:
            if self._is_user_file(issue.file_path):
                report.preserved_files.append(issue.file_path)

        report.message = f"Repair complete: {report.issues_fixed} fixed, {report.issues_skipped} skipped"
        return report

"""
Uninstall Manager for DevForgeAI (STORY-251)

Provides complete uninstall operations:
- AC#3: Uninstall completely

Usage:
    from installer.uninstall import UninstallManager

    manager = UninstallManager(target_path=Path("/path/to/project"))
    exit_code = manager.uninstall()
"""

import json
import logging
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Set

from installer.exit_codes import ExitCodes

logger = logging.getLogger(__name__)


class UninstallManager:
    """
    Manages uninstall operations for DevForgeAI installations.

    Implements AC#3: Uninstall Completely.
    """

    VERSION_MARKER_FILE = ".devforgeai_installed"
    UNINSTALL_LOG_FILE = "uninstall.log"

    # Framework directories to remove
    FRAMEWORK_DIRS = [
        ".claude/skills",
        ".claude/agents",
        ".claude/commands",
        ".claude/rules",
        ".claude/memory",
        ".claude/hooks",
        ".claude/scripts",
        "devforgeai/specs/context",
        "devforgeai/specs/adrs",
        "devforgeai/config",
        "devforgeai/workflows",
    ]

    # Framework files to remove
    FRAMEWORK_FILES = [
        ".devforgeai_installed",
        "CLAUDE.md",
    ]

    # User files/patterns to preserve
    USER_PATTERNS = [
        "*.story.md",
        "*.user.yaml",
        "*.user.json",
        "custom-*",
        ".git",
        ".gitignore",
    ]

    def __init__(self, target_path: Path):
        """
        Initialize UninstallManager.

        Args:
            target_path: Path to DevForgeAI installation
        """
        self.target_path = Path(target_path)
        self._version_data: Optional[Dict] = None
        self._framework_files: List[Path] = []
        self._user_files: List[Path] = []

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

    def _is_installed(self) -> bool:
        """
        Check if DevForgeAI is installed.

        Returns:
            True if installation marker exists
        """
        marker_path = self.target_path / self.VERSION_MARKER_FILE
        return marker_path.exists()

    def _is_user_file(self, file_path: Path) -> bool:
        """Check if file should be preserved as user file."""
        name = file_path.name

        for pattern in self.USER_PATTERNS:
            if pattern.startswith("*"):
                if name.endswith(pattern[1:]):
                    return True
            elif pattern.endswith("*"):
                if name.startswith(pattern[:-1]):
                    return True
            elif name == pattern:
                return True

        # Check if in Stories directory (user content)
        if "Stories" in str(file_path):
            return True

        return False

    def _get_framework_files(self) -> List[Path]:
        """
        Get list of framework-owned files to remove.

        Returns:
            List of paths to framework files
        """
        if self._framework_files:
            return self._framework_files

        framework_files = []

        # Get files from version marker checksums
        if self._version_data:
            checksums = self._version_data.get("checksums", {})
            for file_path in checksums.keys():
                full_path = self.target_path / file_path
                if full_path.exists() and not self._is_user_file(full_path):
                    framework_files.append(full_path)

        # Add known framework directories
        for dir_path in self.FRAMEWORK_DIRS:
            full_path = self.target_path / dir_path
            if full_path.exists():
                for file_path in full_path.rglob("*"):
                    if file_path.is_file() and not self._is_user_file(file_path):
                        framework_files.append(file_path)

        # Add known framework files
        for file_path in self.FRAMEWORK_FILES:
            full_path = self.target_path / file_path
            if full_path.exists():
                framework_files.append(full_path)

        self._framework_files = framework_files
        return framework_files

    def _get_user_files(self) -> List[Path]:
        """
        Get list of user-created files to preserve.

        Returns:
            List of paths to user files
        """
        if self._user_files:
            return self._user_files

        user_files = []

        # Scan all files in installation
        for file_path in self.target_path.rglob("*"):
            if file_path.is_file() and self._is_user_file(file_path):
                user_files.append(file_path)

        self._user_files = user_files
        return user_files

    def _display_uninstall_plan(self) -> None:
        """Display uninstall plan to user (AC#3)."""
        framework_files = self._get_framework_files()
        user_files = self._get_user_files()

        print("\nThis will remove:")
        print("  - DevForgeAI framework files")
        print("  - CLI tools")
        print("  - Templates and examples")
        print(f"  - {len(framework_files)} framework file(s)")

        print("\nUser files will be preserved:")
        if user_files:
            for file_path in user_files[:5]:  # Show first 5
                print(f"  - {file_path.relative_to(self.target_path)}")
            if len(user_files) > 5:
                print(f"  - ... and {len(user_files) - 5} more")
        else:
            print("  - (no user files detected)")

        print("  - Git repository (if present)")
        print("")

    def _confirm_uninstall(self) -> bool:
        """
        Prompt user to confirm uninstall.

        Returns:
            True if user confirms
        """
        try:
            response = input("Proceed with uninstall? [y/N] ").strip().lower()
            return response in ('y', 'yes')
        except EOFError:
            return False

    def _write_uninstall_log(self, removed_files: List[Path]) -> None:
        """
        Write uninstall log (AC#3).

        Args:
            removed_files: List of files that were removed
        """
        log_path = self.target_path / self.UNINSTALL_LOG_FILE

        log_content = [
            f"DevForgeAI Uninstall Log",
            f"========================",
            f"",
            f"Timestamp: {datetime.now(timezone.utc).isoformat()}",
            f"Installation Path: {self.target_path}",
            f"",
            f"Files Removed ({len(removed_files)}):",
        ]

        for file_path in removed_files:
            try:
                rel_path = file_path.relative_to(self.target_path)
            except ValueError:
                rel_path = file_path
            log_content.append(f"  - {rel_path}")

        log_path.write_text("\n".join(log_content))
        logger.info(f"Uninstall log saved to {log_path}")

    def _remove_empty_dirs(self) -> None:
        """Remove empty directories after file removal."""
        # Remove from deepest to shallowest
        dirs_to_check = [
            self.target_path / ".claude",
            self.target_path / "devforgeai",
        ]

        for base_dir in dirs_to_check:
            if not base_dir.exists():
                continue

            # Get all subdirs, sorted deepest first
            subdirs = sorted(
                [d for d in base_dir.rglob("*") if d.is_dir()],
                key=lambda p: len(p.parts),
                reverse=True
            )

            for subdir in subdirs:
                try:
                    if subdir.exists() and not any(subdir.iterdir()):
                        subdir.rmdir()
                except Exception:
                    pass  # Skip if can't remove

    def uninstall(self, force: bool = False) -> int:
        """
        Uninstall DevForgeAI (AC#3).

        Args:
            force: If True, skip confirmation prompt

        Returns:
            Exit code (0 = success)
        """
        # Check if installed
        if not self._is_installed():
            logger.error("No DevForgeAI installation found")
            print("Error: No DevForgeAI installation found at this location.")
            return ExitCodes.VALIDATION_FAILED

        # Display uninstall plan
        self._display_uninstall_plan()

        # Confirm with user
        if not force:
            if not self._confirm_uninstall():
                logger.info("Uninstall cancelled by user")
                print("Uninstall cancelled.")
                return ExitCodes.SUCCESS

        # Get files to remove
        framework_files = self._get_framework_files()

        # Remove files
        removed_files = []
        for file_path in framework_files:
            try:
                if file_path.exists():
                    file_path.unlink()
                    removed_files.append(file_path)
                    logger.debug(f"Removed: {file_path}")
            except Exception as e:
                logger.error(f"Failed to remove {file_path}: {e}")

        # Write uninstall log
        self._write_uninstall_log(removed_files)

        # Remove empty directories
        self._remove_empty_dirs()

        logger.info(f"Uninstall complete. Removed {len(removed_files)} files.")
        print(f"\nUninstall complete. Removed {len(removed_files)} framework files.")
        print(f"Log saved to: {self.UNINSTALL_LOG_FILE}")

        return ExitCodes.SUCCESS

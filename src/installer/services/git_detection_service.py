"""
Git Detection Service - STORY-073

Handles detection of Git repositories and repository root paths.

Requirements:
- SVC-011: Execute git rev-parse --show-toplevel to find repository root
- SVC-012: Handle non-git directories gracefully
- SVC-013: Validate git command availability
- SVC-014: Detect and warn about unusual repository roots (/)

Business Rules:
- BR-004: Git root validation rejects filesystem root
- NFR-003: Git detection completes in <100ms
- NFR-005: Git command uses shell=False (security)
"""

import logging
import shutil
import subprocess
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class GitInfo:
    """
    Data model for Git repository detection results.

    Fields:
        repository_root: Absolute path to git repository root (None if not in repo)
        is_submodule: Whether repository is a git submodule
    """

    def __init__(self, repository_root: Optional[Path], is_submodule: bool = False):
        self.repository_root = repository_root
        self.is_submodule = is_submodule


class GitDetectionService:
    """
    Service for detecting Git repositories and extracting repository information.

    Lifecycle: Singleton (one instance per target path)
    Dependencies: subprocess, pathlib, shutil
    """

    def __init__(self, target_path: str):
        """
        Initialize Git detection service.

        Args:
            target_path: Absolute path to directory to check
        """
        self.target_path = Path(target_path)

    def is_git_available(self) -> bool:
        """
        Check if git command is available in PATH.

        Returns:
            True if git is available, False otherwise

        Test Requirements:
            - Returns True when git in PATH
            - Returns False when git not in PATH
            - Uses shutil.which to check availability
        """
        return shutil.which("git") is not None

    def detect_git_root(self) -> Optional[Path]:
        """
        Execute git rev-parse --show-toplevel to find repository root.

        Returns:
            Path to repository root, or None if not in git repository

        Test Requirements:
            - Returns Path for valid git repository
            - Returns None for non-git directories
            - Returns None when git not installed
            - Returns None for filesystem root (/, C:\\)
            - Uses subprocess.run with shell=False (NFR-005)
            - Strips whitespace from git output
            - Sets timeout to prevent hanging
            - Handles subprocess errors gracefully (BR-001)
        """
        try:
            # Check if git is available (SVC-013)
            if not self.is_git_available():
                logger.debug("Git command not available")
                return None

            # Execute git rev-parse --show-toplevel (SVC-011)
            result = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                cwd=str(self.target_path),
                capture_output=True,
                text=True,
                shell=False,  # NFR-005: Security - prevent command injection
                timeout=5     # Prevent hanging
            )

            # Handle non-git directories (SVC-012)
            if result.returncode != 0:
                logger.debug(f"Not a git repository: {self.target_path}")
                return None

            # Parse git output
            git_root = result.stdout.strip()

            # Security: Validate path doesn't contain traversal attempts
            if ".." in git_root:
                logger.warning(f"Suspicious path with traversal attempt rejected: {git_root}")
                return None

            # Convert to Path
            root_path = Path(git_root)

            # Validate against filesystem root (BR-004, SVC-014)
            if self._is_filesystem_root(root_path):
                logger.warning(f"Git root is filesystem root: {root_path}")
                return None

            return root_path

        except subprocess.TimeoutExpired:
            logger.warning("Git command timed out")
            return None
        except subprocess.CalledProcessError as e:
            logger.debug(f"Git command failed: {e}")
            return None
        except FileNotFoundError:
            logger.debug("Git executable not found")
            return None
        except PermissionError as e:
            logger.warning(f"Permission denied executing git: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error detecting git root: {e}")
            return None

    def is_submodule(self) -> bool:
        """
        Detect if current directory is a git submodule.

        Returns:
            True if directory is a submodule, False otherwise

        Test Requirements:
            - Returns True when .git is a file (submodule indicator)
            - Returns False when .git is a directory (normal repository)
        """
        try:
            git_path = self.target_path / ".git"

            # Submodules have .git as file, not directory
            if git_path.exists() and git_path.is_file():
                return True

            return False

        except Exception as e:
            logger.error(f"Error detecting submodule: {e}")
            return False

    def _is_filesystem_root(self, path: Path) -> bool:
        """
        Check if path is filesystem root (/, C:\\, etc.).

        Args:
            path: Path to validate

        Returns:
            True if path is filesystem root, False otherwise
        """
        # Unix root
        if str(path) == "/":
            return True

        # Windows root (C:\, D:\, etc.)
        if len(str(path)) == 3 and str(path)[1:] == ":\\":
            return True

        # Parent equals self (root indicator)
        if path.parent == path:
            return True

        return False

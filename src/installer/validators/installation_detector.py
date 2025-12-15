"""
Existing installation detection checker.

Detects previous DevForgeAI installations by checking for .claude/ and devforgeai/ directories.
"""

import json
from pathlib import Path
from typing import Optional
from .models import CheckResult


class ExistingInstallationDetector:
    """
    Detects existing DevForgeAI installations.

    Checks for .claude/ and devforgeai/ directories and reads version.json if present.
    """

    def __init__(self, target_path: str):
        """
        Initialize installation detector.

        Args:
            target_path: Directory path to check for existing installation
        """
        self.target_path = Path(target_path)

    def check(self) -> CheckResult:
        """
        Check for existing DevForgeAI installation.

        Returns:
            CheckResult with PASS if no installation, WARN if found

        Checks:
            - .claude/ directory presence
            - devforgeai/ directory presence
            - version.json file (if exists)
        """
        try:
            claude_dir = self.target_path / ".claude"
            devforgeai_dir = self.target_path / ".devforgeai"

            claude_exists = claude_dir.exists()
            devforgeai_exists = devforgeai_dir.exists()

            if not claude_exists and not devforgeai_exists:
                return CheckResult(
                    check_name="Existing Installation",
                    status="PASS",
                    message="No existing installation found - fresh install"
                )

            # Existing installation detected
            version = self._read_version()

            # Build message
            found_dirs = []
            if claude_exists:
                found_dirs.append(".claude/")
            if devforgeai_exists:
                found_dirs.append("devforgeai/")

            dirs_str = " and ".join(found_dirs)

            if version:
                message = f"Existing DevForgeAI {version} found in {self.target_path} ({dirs_str}). " \
                         f"Choose: upgrade existing, fresh install (overwrites), or cancel."
            else:
                message = f"Existing installation found in {self.target_path} ({dirs_str}). " \
                         f"Choose: upgrade existing, fresh install (overwrites), or cancel."

            return CheckResult(
                check_name="Existing Installation",
                status="WARN",
                message=message
            )

        except PermissionError:
            return CheckResult(
                check_name="Existing Installation",
                status="WARN",
                message="Permission denied checking for existing installation"
            )
        except Exception as e:
            return CheckResult(
                check_name="Existing Installation",
                status="WARN",
                message=f"Error checking for existing installation: {str(e)}"
            )

    def _read_version(self) -> Optional[str]:
        """
        Read version from version.json if present.

        Returns:
            Version string (e.g., "v1.0.0") or None if not found/invalid
        """
        version_file = self.target_path / "version.json"

        try:
            if not version_file.exists():
                return None

            with open(version_file, 'r') as f:
                data = json.load(f)

            version = data.get("version")
            if version:
                # Format with 'v' prefix if not already present
                if not version.startswith("v"):
                    return f"v{version}"
                return version

            return None

        except (json.JSONDecodeError, KeyError, IOError):
            # Invalid JSON or missing version field
            return None
        except Exception:
            return None

"""
Version detector service for reading installed version from .version.json.

Implements SVC-001 through SVC-003:
- Read version from devforgeai/.version.json
- Handle missing version file gracefully
- Handle corrupted JSON gracefully
"""

import json
from pathlib import Path
from typing import Optional, Dict, Any

from installer.version_parser import Version, VersionParser


class VersionDetector:
    """Detects installed version from devforgeai/.version.json."""

    def __init__(self, devforgeai_path: Optional[Path] = None) -> None:
        """
        Initialize VersionDetector.

        Args:
            devforgeai_path: Path to devforgeai directory. Defaults to devforgeai in current directory.
        """
        if devforgeai_path is None:
            devforgeai_path = Path.cwd() / "devforgeai"
        selfdevforgeai_path = Path(devforgeai_path)
        self.version_file = selfdevforgeai_path / ".version.json"
        self.parser = VersionParser()

    def _read_file_content(self) -> Optional[Dict[str, Any]]:
        """
        Read and parse JSON content from version file.

        Returns:
            Parsed JSON dict if file exists and is valid, None otherwise.

        Raises:
            json.JSONDecodeError: If JSON parsing fails
        """
        if not self.version_file.exists():
            return None

        content = self.version_file.read_text(encoding="utf-8")
        if not content.strip():
            return None

        return json.loads(content)

    def read_version(self) -> Optional[Version]:
        """
        Read installed version from .version.json.

        Returns:
            Version object if file exists and is valid JSON with a version field,
            None if file doesn't exist.

        Raises:
            ValueError: Only if version string in JSON is invalid (not for file I/O errors)
        """
        try:
            data = self._read_file_content()
            if data is None or "version" not in data:
                return None

            version_string = data["version"]
            return self.parser.parse(version_string)
        except (json.JSONDecodeError, ValueError):
            return None

    def read_version_metadata(self) -> Optional[Dict[str, Any]]:
        """
        Read full version metadata from .version.json.

        Returns:
            Dict with version, installed_at, upgraded_from, schema_version if file exists,
            None otherwise.
        """
        try:
            return self._read_file_content()
        except (json.JSONDecodeError, OSError):
            return None

    def get_version_status(self) -> Dict[str, Any]:
        """
        Get status of version file (for error reporting).

        Returns:
            Dict with status and message fields describing what was found/failed.
        """
        if not self.version_file.exists():
            return {
                "status": "missing",
                "message": f"Version file not found at {self.version_file}",
            }

        try:
            content = self.version_file.read_text(encoding="utf-8")
            if not content.strip():
                return {"status": "corrupted", "message": "Version file is empty"}

            data = json.loads(content)

            if "version" not in data:
                return {
                    "status": "error",
                    "message": "Version file missing 'version' field",
                }

            version_string = data["version"]
            try:
                self.parser.parse(version_string)
                return {"status": "valid", "version": version_string}
            except ValueError as e:
                return {"status": "error", "message": f"Invalid version format: {e}"}

        except json.JSONDecodeError as e:
            return {
                "status": "error",
                "message": f"Invalid JSON in version file: {e}",
            }
        except OSError as e:
            return {"status": "error", "message": f"Error reading version file: {e}"}

    def display_version(self) -> str:
        """
        Get user-friendly version display string.

        Returns:
            Formatted version string for display to user.
        """
        version = self.read_version()
        if version is None:
            return "Version: unknown (not installed)"
        return f"Version: v{version}"

    def treat_as_fresh_install(self) -> Version:
        """
        Return 0.0.0 version for fresh install scenario.

        Returns:
            Version(0, 0, 0) to represent fresh installation.
        """
        return Version(major=0, minor=0, patch=0)

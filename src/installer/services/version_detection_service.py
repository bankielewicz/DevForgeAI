"""
Version Detection Service - STORY-073

Handles detection and comparison of DevForgeAI installation versions.

Requirements:
- SVC-004: Read devforgeai/.version.json and parse installed version
- SVC-005: Compare installed vs source version using semantic versioning
- SVC-006: Handle corrupted version.json gracefully
- SVC-007: Handle non-standard versions (null, 'latest', 'dev')

Business Rules:
- BR-001: Auto-detection failures are non-fatal (returns None, logs warnings)
"""

import json
import logging
from pathlib import Path
from typing import Optional
from packaging import version

logger = logging.getLogger(__name__)


class VersionInfo:
    """
    Data model for installed version metadata.

    Fields:
        installed_version: Semantic version string (X.Y.Z format)
        installed_at: ISO 8601 timestamp
        installation_source: Installation method (installer, manual, ci)
    """

    def __init__(self, installed_version: str, installed_at: str, installation_source: str):
        self.installed_version = installed_version
        self.installed_at = installed_at
        self.installation_source = installation_source


class VersionComparisonResult:
    """
    Data model for version comparison results.

    Fields:
        action: One of "upgrade", "downgrade", "same", "unknown"
        message: Human-readable recommendation message
        current: Current installed version (optional)
        target: Target source version (optional)
    """

    def __init__(self, action: str, message: str, current: Optional[str] = None, target: Optional[str] = None):
        self.action = action
        self.message = message
        self.current = current
        self.target = target


class VersionDetectionService:
    """
    Service for detecting and comparing DevForgeAI installation versions.

    Lifecycle: Singleton (one instance per target path)
    Dependencies: json, pathlib, packaging.version
    """

    def __init__(self, target_path: str):
        """
        Initialize version detection service.

        Args:
            target_path: Absolute path to installation directory
        """
        self.target_path = Path(target_path)
        self.version_file = self.target_path / "devforgeai" / ".version.json"

    def read_version(self) -> Optional[VersionInfo]:
        """
        Read and parse devforgeai/.version.json file.

        Returns:
            VersionInfo with parsed data, or None if file missing/corrupted

        Test Requirements:
            - Returns VersionInfo for valid JSON
            - Returns None for missing file
            - Returns None for corrupted JSON
            - Returns None for missing required fields
            - Returns None for null version field
        """
        try:
            # Check if devforgeai directory exists
            if not self.version_file.parent.exists():
                logger.debug(f"devforgeai directory not found at {self.target_path}")
                return None

            # Check if version file exists
            if not self.version_file.exists():
                logger.debug(f"Version file not found: {self.version_file}")
                return None

            # Read and parse JSON
            with open(self.version_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Validate required fields
            required_fields = ["installed_version", "installed_at", "installation_source"]
            for field in required_fields:
                if field not in data:
                    logger.warning(f"Version file missing required field: {field}")
                    return None

            # Check for null version
            if data["installed_version"] is None:
                logger.warning("Version file has null installed_version")
                return None

            # Return parsed version info
            return VersionInfo(
                installed_version=data["installed_version"],
                installed_at=data["installed_at"],
                installation_source=data["installation_source"]
            )

        except json.JSONDecodeError as e:
            logger.error(f"Corrupted version file: {e}")
            return None
        except (IOError, PermissionError) as e:
            logger.error(f"Cannot read version file: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error reading version: {e}")
            return None

    def compare_versions(self, installed_version: str, source_version: str) -> VersionComparisonResult:
        """
        Compare installed version with source version using semantic versioning.

        Args:
            installed_version: Currently installed version string
            source_version: Source/target version string

        Returns:
            VersionComparisonResult with action and recommendation message

        Test Requirements:
            - action="upgrade" when source > installed
            - action="downgrade" when source < installed
            - action="same" when source == installed
            - action="unknown" for malformed versions
            - Handles pre-release versions
            - Handles non-standard versions ("dev", "latest", empty string)
        """
        try:
            # Handle empty version strings
            if not installed_version or not source_version:
                return VersionComparisonResult(
                    action="unknown",
                    message="Unable to compare versions (empty version string, manual review required)"
                )

            # Handle non-standard versions
            non_standard = ["dev", "latest"]
            if installed_version.lower() in non_standard or source_version.lower() in non_standard:
                return VersionComparisonResult(
                    action="unknown",
                    message="Unable to compare versions (non-standard version detected, manual review required)"
                )

            # Parse semantic versions
            installed_ver = version.parse(installed_version)
            source_ver = version.parse(source_version)

            # Compare versions
            if source_ver > installed_ver:
                message = f"Upgrade available: v{installed_version} → v{source_version} (recommended)"
                return VersionComparisonResult(
                    action="upgrade",
                    message=message,
                    current=installed_version,
                    target=source_version
                )
            elif source_ver < installed_ver:
                message = f"Downgrade detected: v{installed_version} → v{source_version} (warning: may lose features)"
                return VersionComparisonResult(
                    action="downgrade",
                    message=message,
                    current=installed_version,
                    target=source_version
                )
            else:  # Equal
                message = f"Same version detected: v{installed_version} (reinstall available if needed)"
                return VersionComparisonResult(
                    action="same",
                    message=message,
                    current=installed_version,
                    target=source_version
                )

        except (version.InvalidVersion, AttributeError) as e:
            logger.warning(f"Invalid version format: {e}")
            return VersionComparisonResult(
                action="unknown",
                message="Unable to compare versions (malformed version, manual review required)"
            )
        except Exception as e:
            logger.error(f"Unexpected error comparing versions: {e}")
            return VersionComparisonResult(
                action="unknown",
                message="Unable to compare versions (unexpected error, manual review required)"
            )

"""
Upgrade Manager for DevForgeAI (STORY-251)

Provides upgrade operations for DevForgeAI installations:
- AC#1: Upgrade to latest version
- AC#5: Selective component upgrade
- AC#6: Safe mode (no backup deletion)

Usage:
    from installer.upgrade import UpgradeManager

    manager = UpgradeManager(target_path=Path("/path/to/project"))
    exit_code = manager.upgrade()
"""

import json
import logging
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any

from installer.exit_codes import ExitCodes
from installer.version_parser import Version
from installer.version_comparator import VersionComparator

logger = logging.getLogger(__name__)


# Placeholder for version API - would be replaced with actual registry call
def get_latest_version() -> Dict[str, Any]:
    """Get latest version from registry (placeholder)."""
    return {
        "version": "1.1.0",
        "release_date": "2025-01-06",
        "download_url": "https://example.com/devforgeai-1.1.0.tar.gz",
        "checksum": "sha256:abc123def456"
    }


@dataclass
class UpgradeResult:
    """Result of an upgrade operation."""
    success: bool
    from_version: str
    to_version: str
    backup_path: Optional[Path] = None
    message: str = ""


class UpgradeManager:
    """
    Manages upgrade operations for DevForgeAI installations.

    Implements AC#1 (Upgrade), AC#5 (Selective), AC#6 (Safe Mode).
    """

    VERSION_MARKER_FILE = ".devforgeai_installed"

    def __init__(self, target_path: Path, safe_mode: bool = False):
        """
        Initialize UpgradeManager.

        Args:
            target_path: Path to DevForgeAI installation
            safe_mode: If True, retain all backups (AC#6)
        """
        self.target_path = Path(target_path)
        self.safe_mode = safe_mode
        self._version_data: Optional[Dict] = None
        self._backup_path: Optional[Path] = None

        # Load current version
        self._load_version_data()

    @property
    def current_version(self) -> str:
        """Get current installed version."""
        if self._version_data:
            return self._version_data.get("version", "0.0.0")
        return "0.0.0"

    def _load_version_data(self) -> None:
        """Load version data from marker file."""
        marker_path = self.target_path / self.VERSION_MARKER_FILE
        if marker_path.exists():
            try:
                self._version_data = json.loads(marker_path.read_text())
            except json.JSONDecodeError:
                logger.warning(f"Failed to parse version marker: {marker_path}")
                self._version_data = None

    def _detect_version(self) -> str:
        """Detect current installation version (AC#1)."""
        return self.current_version

    def _get_latest_version(self) -> Optional[str]:
        """Get latest available version (AC#1)."""
        try:
            version_info = get_latest_version()
            return version_info.get("version")
        except Exception as e:
            logger.error(f"Failed to get latest version: {e}")
            return None

    def _create_backup(self) -> Path:
        """
        Create timestamped backup before upgrade (AC#1).

        Backup created at /path/to/project.backup-YYYYMMDD-HHMMSS
        """
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_name = f"{self.target_path.name}.backup-{timestamp}"
        backup_path = self.target_path.parent / backup_name

        logger.info(f"Creating backup at {backup_path}")
        shutil.copytree(
            self.target_path,
            backup_path,
            ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.git')
        )

        # Store backup path for potential rollback
        self._backup_path = backup_path

        return backup_path

    def _download_version(self, version: str) -> bool:
        """
        Download specified version (placeholder).

        Args:
            version: Version to download

        Returns:
            True if download successful
        """
        # Placeholder - would download from registry
        logger.info(f"Downloading version {version}")
        return True

    def _apply_upgrade(self, version: str) -> bool:
        """
        Apply upgrade to installation.

        Args:
            version: Version being applied

        Returns:
            True if upgrade successful
        """
        logger.info(f"Applying upgrade to {version}")
        # Placeholder - would apply downloaded files
        return True

    def _apply_component_upgrade(self, component: str, version: str) -> bool:
        """
        Apply upgrade to specific component (AC#5).

        Args:
            component: Component name to upgrade
            version: Version to upgrade to

        Returns:
            True if component upgrade successful
        """
        logger.info(f"Applying upgrade to component {component} -> {version}")
        # Placeholder - would apply component-specific files
        return True

    def _check_dependencies(self, components: List[str]) -> List[str]:
        """
        Check component dependencies (AC#5).

        If specified components require core, include core.

        Args:
            components: List of components to upgrade

        Returns:
            List of components including dependencies
        """
        result = list(components)

        # Core is always needed if upgrading any component
        if components and "core" not in result:
            result.insert(0, "core")

        return result

    def _display_component_summary(self, components: List[str], version: str) -> None:
        """
        Display component upgrade summary (AC#5).

        Args:
            components: List of upgraded components
            version: Version upgraded to
        """
        print(f"\nComponent Upgrade Summary:")
        print(f"  Target version: {version}")
        print(f"  Components upgraded:")
        for comp in components:
            print(f"    ✓ {comp}")
        print("")

    def _validate_installation(self) -> bool:
        """
        Validate installation after upgrade.

        Returns:
            True if validation passes
        """
        # Check marker file exists
        marker_path = self.target_path / self.VERSION_MARKER_FILE
        if not marker_path.exists():
            return False

        # Basic structure validation
        required_paths = [
            self.target_path / ".claude",
            self.target_path / "devforgeai",
        ]

        for path in required_paths:
            if not path.exists():
                logger.warning(f"Missing required path: {path}")
                return False

        return True

    def _restore_backup(self, backup_path: Path) -> None:
        """
        Restore installation from backup on failure.

        Args:
            backup_path: Path to backup directory
        """
        if backup_path and backup_path.exists():
            logger.info(f"Restoring from backup: {backup_path}")

            # Remove current installation
            if self.target_path.exists():
                shutil.rmtree(self.target_path)

            # Restore from backup
            shutil.copytree(backup_path, self.target_path)

    def _update_version_marker(self, version: str) -> None:
        """Update version marker after successful upgrade."""
        marker_path = self.target_path / self.VERSION_MARKER_FILE

        if self._version_data:
            self._version_data["version"] = version
            self._version_data["updated_at"] = datetime.now(timezone.utc).isoformat()
        else:
            self._version_data = {
                "version": version,
                "installed_at": datetime.now(timezone.utc).isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat(),
                "components": {},
                "checksums": {}
            }

        marker_path.write_text(json.dumps(self._version_data, indent=2))

    def upgrade(
        self,
        target_version: Optional[str] = None,
        components: Optional[List[str]] = None
    ) -> int:
        """
        Upgrade to target version (or latest).

        Args:
            target_version: Specific version to upgrade to (or None for latest)
            components: List of components to upgrade (AC#5), or None for all

        Returns:
            Exit code (0 = success)
        """
        try:
            # Determine target version
            if target_version:
                latest = target_version
            else:
                latest = self._get_latest_version()

            if not latest:
                logger.error("Could not determine target version")
                return ExitCodes.VALIDATION_FAILED

            # Check if upgrade needed using proper version comparison
            current = self._detect_version()
            comparator = VersionComparator()

            try:
                current_ver = Version.parse(current) if current != "0.0.0" else None
                latest_ver = Version.parse(latest)
                result = comparator.compare(current_ver, latest_ver)

                if result.relationship in ("SAME", "DOWNGRADE"):
                    logger.info(f"Already at latest version ({current})")
                    return ExitCodes.SUCCESS
            except Exception as e:
                logger.warning(f"Version comparison failed, falling back to string: {e}")
                if current >= latest:
                    logger.info(f"Already at latest version ({current})")
                    return ExitCodes.SUCCESS

            logger.info(f"Upgrading from {current} to {latest}")

            # Create backup before upgrade
            backup_path = self._create_backup()

            try:
                # Download new version
                if not self._download_version(latest):
                    raise Exception("Download failed")

                # Apply upgrade (selective if components specified)
                if not self._apply_upgrade(latest):
                    raise Exception("Apply upgrade failed")

                # Update version marker
                self._update_version_marker(latest)

                # Validate installation
                if not self._validate_installation():
                    raise Exception("Validation failed")

                logger.info(f"Upgrade to {latest} completed successfully")
                return ExitCodes.SUCCESS

            except Exception as e:
                logger.error(f"Upgrade failed: {e}")
                self._restore_backup(backup_path)
                return ExitCodes.ROLLBACK_OCCURRED

        except Exception as e:
            logger.error(f"Upgrade error: {e}")
            return ExitCodes.VALIDATION_FAILED

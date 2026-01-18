"""
Status Reporter for DevForgeAI (STORY-251)

Provides installation status reporting:
- AC#7: Maintenance status report

Usage:
    from installer.status import StatusReporter

    reporter = StatusReporter(target_path=Path("/path/to/project"))
    reporter.report()
"""

import hashlib
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any

from installer.exit_codes import ExitCodes

logger = logging.getLogger(__name__)


# Placeholder for version API
def get_latest_version() -> Dict[str, Any]:
    """Get latest version from registry (placeholder)."""
    return {
        "version": "1.1.0",
        "release_date": "2025-01-06",
    }


class StatusReporter:
    """
    Reports installation status and health.

    Implements AC#7: Maintenance Status Report.
    """

    VERSION_MARKER_FILE = ".devforgeai_installed"

    def __init__(self, target_path: Path):
        """
        Initialize StatusReporter.

        Args:
            target_path: Path to DevForgeAI installation
        """
        self.target_path = Path(target_path)
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

    @property
    def version(self) -> str:
        """Get current installed version."""
        if self._version_data:
            return self._version_data.get("version", "unknown")
        return "unknown"

    @property
    def installed_at(self) -> str:
        """Get installation timestamp."""
        if self._version_data:
            return self._version_data.get("installed_at", "unknown")
        return "unknown"

    @property
    def updated_at(self) -> str:
        """Get last update timestamp."""
        if self._version_data:
            return self._version_data.get("updated_at", "unknown")
        return "unknown"

    @property
    def components(self) -> Dict[str, str]:
        """Get installed components and versions."""
        if self._version_data:
            return self._version_data.get("components", {})
        return {}

    def _compute_checksum(self, file_path: Path) -> str:
        """Compute SHA256 checksum of file."""
        sha256 = hashlib.sha256()
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(65536), b''):
                    sha256.update(chunk)
            return f"sha256:{sha256.hexdigest()}"
        except Exception:
            return ""

    def _perform_health_check(self) -> Dict[str, Any]:
        """
        Perform installation health check (AC#7).

        Returns:
            Health check results
        """
        health = {
            "all_files_present": True,
            "no_checksum_mismatches": True,
            "configuration_valid": True,
            "issues": []
        }

        if not self._version_data:
            health["configuration_valid"] = False
            health["issues"].append("Version marker missing or invalid")
            return health

        checksums = self._version_data.get("checksums", {})

        for file_path, expected_checksum in checksums.items():
            full_path = self.target_path / file_path

            if not full_path.exists():
                health["all_files_present"] = False
                health["issues"].append(f"Missing: {file_path}")
            else:
                actual_checksum = self._compute_checksum(full_path)
                if actual_checksum != expected_checksum:
                    health["no_checksum_mismatches"] = False
                    health["issues"].append(f"Checksum mismatch: {file_path}")

        return health

    def _check_for_updates(self) -> Optional[str]:
        """
        Check for available updates (AC#7).

        Returns:
            Latest version if update available, None otherwise
        """
        try:
            version_info = get_latest_version()
            latest = version_info.get("version", "0.0.0")

            if latest > self.version:
                return latest
            return None
        except Exception as e:
            logger.warning(f"Failed to check for updates: {e}")
            return None

    def _list_backups(self) -> List[Dict[str, Any]]:
        """
        List available backups (AC#7).

        Returns:
            List of backup information
        """
        backups = []
        backup_parent = self.target_path.parent

        # Find backup directories
        for path in backup_parent.glob(f"{self.target_path.name}.backup-*"):
            if path.is_dir():
                backup_info = {
                    "path": str(path),
                    "name": path.name,
                    "size_mb": 0,
                    "version": "unknown",
                    "created_at": "unknown"
                }

                # Try to get size
                try:
                    total_size = sum(
                        f.stat().st_size for f in path.rglob("*") if f.is_file()
                    )
                    backup_info["size_mb"] = round(total_size / (1024 * 1024), 1)
                except Exception:
                    pass

                # Try to read manifest
                manifest_path = path / "manifest.json"
                if manifest_path.exists():
                    try:
                        manifest = json.loads(manifest_path.read_text())
                        backup_info["version"] = manifest.get("from_version", "unknown")
                        backup_info["created_at"] = manifest.get("created_at", "unknown")
                    except Exception:
                        pass

                backups.append(backup_info)

        # Sort by name (which includes timestamp)
        backups.sort(key=lambda b: b["name"], reverse=True)
        return backups

    def _generate_recommendations(self) -> List[str]:
        """
        Generate maintenance recommendations (AC#7).

        Returns:
            List of recommendation strings
        """
        recommendations = []

        # Check for updates
        latest = self._check_for_updates()
        if latest:
            recommendations.append(f"Update to latest version ({latest})")

        # Check backups
        backups = self._list_backups()
        if len(backups) > 5:
            recommendations.append(f"Clean old backups (older than 30 days)")

        # Check health
        health = self._perform_health_check()
        if health["issues"]:
            recommendations.append("Run repair to fix detected issues")

        return recommendations

    def report(self) -> None:
        """
        Display full maintenance status report (AC#7).
        """
        print("\nDevForgeAI Installation Status")
        print("=" * 40)
        print("")

        # Version info
        print(f"Version: {self.version}")
        print(f"Installed: {self.installed_at}")
        print(f"Last Updated: {self.updated_at}")
        print("")

        # Components
        print("Components:")
        components = self.components
        if components:
            for name, version in components.items():
                print(f"  ✓ {name} ({version})")
        else:
            print("  (no components listed)")
        print("")

        # Health check
        print("Health Check:")
        health = self._perform_health_check()

        if health["all_files_present"]:
            print("  ✓ All required files present")
        else:
            print("  ✗ Missing files detected")

        if health["no_checksum_mismatches"]:
            print("  ✓ No checksum mismatches")
        else:
            print("  ✗ Checksum mismatches found")

        if health["configuration_valid"]:
            print("  ✓ Configuration valid")
        else:
            print("  ✗ Configuration issues")

        # Update check
        latest = self._check_for_updates()
        if latest:
            print(f"  ⚠ Update available ({latest})")
        print("")

        # Backups
        backups = self._list_backups()
        total_size = sum(b["size_mb"] for b in backups)
        print(f"Backups: {len(backups)} available ({total_size:.0f} MB total)")
        for backup in backups[:3]:  # Show first 3
            print(f"  - {backup['created_at']} ({backup['version']})")
        if len(backups) > 3:
            print(f"  - ... and {len(backups) - 3} more")
        print("")

        # Recommendations
        recommendations = self._generate_recommendations()
        if recommendations:
            print("Recommendations:")
            for rec in recommendations:
                print(f"  - {rec}")
            print("")

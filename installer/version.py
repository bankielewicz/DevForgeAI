"""
Version detection and semantic version comparison using stdlib only.

This module handles:
- Reading installed version from devforgeai/.version.json
- Reading source version from src/devforgeai/version.json
- Semantic version comparison using stdlib only (no external dependencies)
- Installation mode determination (fresh, patch_upgrade, minor_upgrade, major_upgrade, reinstall, downgrade)

Functions:
- get_installed_version(devforgeai_path: Path) -> dict | None
- get_source_version(source_path: Path) -> dict
- compare_versions(installed: str, source: str) -> str
"""

import json
import re
from pathlib import Path

# Installation mode constants
MODE_FRESH_INSTALL = "fresh_install"
MODE_PATCH_UPGRADE = "patch_upgrade"
MODE_MINOR_UPGRADE = "minor_upgrade"
MODE_MAJOR_UPGRADE = "major_upgrade"
MODE_REINSTALL = "reinstall"
MODE_DOWNGRADE = "downgrade"

# Version file paths
INSTALLED_VERSION_FILE = ".version.json"
SOURCE_VERSION_FILE = "version.json"


def get_installed_version(devforgeai_path: Path) -> dict | None:
    """
    Read installed version from devforgeai/.version.json.

    Args:
        devforgeai_path: Path to devforgeai/ directory

    Returns:
        dict with version, installed_at, mode, schema_version
        None if file doesn't exist (fresh install)

    Raises:
        json.JSONDecodeError: If file content is invalid JSON
        ValueError: If version format is invalid
    """
    version_file = devforgeai_path / INSTALLED_VERSION_FILE

    if not version_file.exists():
        return None

    return _parse_version_file(version_file)


def get_source_version(source_path: Path) -> dict:
    """
    Read source version from src/devforgeai/version.json.

    Args:
        source_path: Path to src/devforgeai/ directory

    Returns:
        dict with version, released_at, schema_version, changes (optional)

    Raises:
        FileNotFoundError: If version.json doesn't exist
        json.JSONDecodeError: If file content is invalid JSON
        ValueError: If version format is invalid
    """
    version_file = source_path / SOURCE_VERSION_FILE

    if not version_file.exists():
        raise FileNotFoundError(f"Source version file not found: {version_file}")

    return _parse_version_file(version_file)


def _parse_version_file(version_file: Path) -> dict:
    """
    Parse and validate a version.json file.

    Args:
        version_file: Path to version.json file

    Returns:
        dict with version data

    Raises:
        json.JSONDecodeError: If file content is invalid JSON
        ValueError: If version format is invalid
    """
    try:
        content = json.loads(version_file.read_text())
        # Validate version format - must be X.Y.Z semantic versioning
        version_str = content.get("version", "")
        if not version_str:
            raise ValueError("Missing 'version' field")

        # Validate semantic versioning format (X.Y.Z) using stdlib only
        _validate_semantic_version(version_str)

        return content
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Failed to parse {version_file}: {e.msg}", e.doc, e.pos)


def _validate_semantic_version(version_str: str) -> None:
    """
    Validate semantic version format (X.Y.Z).

    Args:
        version_str: Version string to validate

    Raises:
        ValueError: If version format is invalid
    """
    parts = version_str.split(".")
    if len(parts) != 3:
        raise ValueError(f"Version must be X.Y.Z format, got: {version_str}")

    for i, part in enumerate(parts):
        try:
            int(part)
        except ValueError:
            raise ValueError(f"Version part {i} must be numeric, got: {part}")


def _parse_semver(version_str: str) -> tuple[int, int, int]:
    """
    Parse semantic version string (X.Y.Z) using stdlib only.

    Args:
        version_str: Version string like "1.0.0"

    Returns:
        Tuple of (major, minor, patch) as integers

    Raises:
        ValueError: If version format is invalid
    """
    parts = version_str.split('.')
    if len(parts) != 3:
        raise ValueError(f"Invalid version format: {version_str} (expected X.Y.Z)")

    try:
        return tuple(int(p) for p in parts)
    except ValueError:
        raise ValueError(f"Version parts must be numeric: {version_str}")


def compare_versions(installed: str | None, source: str) -> str:
    """
    Compare semantic versions and determine installation mode.

    Args:
        installed: Installed version string (e.g., "1.0.0"), or None for fresh install
        source: Source version string (e.g., "1.0.1")

    Returns:
        str: Installation mode - one of:
        - "fresh_install" (no installed version)
        - "patch_upgrade" (1.0.0 → 1.0.1, patch changes only)
        - "minor_upgrade" (1.0.0 → 1.1.0, backward compatible)
        - "major_upgrade" (1.0.0 → 2.0.0, breaking changes)
        - "reinstall" (1.0.0 → 1.0.0, same version)
        - "downgrade" (1.0.1 → 1.0.0, source older than installed)

    Raises:
        ValueError: If version format is invalid or inputs are invalid
    """
    # HIGH-1 FIX: Validate input types and values
    if installed is None:
        return MODE_FRESH_INSTALL

    if not isinstance(installed, str) or not isinstance(source, str):
        raise ValueError(
            f"Version must be string, got installed={type(installed).__name__}, "
            f"source={type(source).__name__}"
        )

    if not installed.strip() or not source.strip():
        raise ValueError("Version strings cannot be empty")

    # Parse versions using stdlib only (zero external dependencies)
    try:
        installed_tuple = _parse_semver(installed)
        source_tuple = _parse_semver(source)
    except ValueError as e:
        raise ValueError(f"Invalid version format: {e}")

    # Compare tuples (Python compares element by element)
    if installed_tuple == source_tuple:
        return MODE_REINSTALL

    if source_tuple < installed_tuple:
        return MODE_DOWNGRADE

    # Source is newer - determine upgrade type
    inst_major, inst_minor, inst_patch = installed_tuple
    src_major, src_minor, src_patch = source_tuple

    if src_major > inst_major:
        return MODE_MAJOR_UPGRADE

    if src_minor > inst_minor:
        return MODE_MINOR_UPGRADE

    return MODE_PATCH_UPGRADE

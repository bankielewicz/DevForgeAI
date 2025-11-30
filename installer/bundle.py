"""
Bundle structure verification and size measurement.

This module provides:
- Bundle structure validation (claude/, devforgeai/, checksums.json)
- File counting for completeness verification
- Bundle size measurement (compressed and uncompressed)
- NPM package compliance checks
- Path traversal protection (OWASP A03:2021)

Functions:
- verify_bundle_structure(bundle_root: Path) -> dict
- count_bundled_files(bundle_root: Path) -> int
- measure_bundle_size(bundle_root: Path) -> dict
- validate_bundle_path(bundle_path: str) -> Path

Dependencies: Standard library only (pathlib, subprocess, tarfile)
"""

import os
import re
import tarfile
import tempfile
from pathlib import Path

# Configuration constants
MIN_BUNDLED_FILES = 200
COMPRESSION_RATIO_ESTIMATE = 0.3  # Typical tar.gz compression (30% of original)
MB_DIVISOR = 1024 * 1024

# SECURITY: Path validation pattern (prevents directory traversal)
SAFE_PATH_PATTERN = re.compile(r'^[a-zA-Z0-9._-]+$')


def verify_bundle_structure(bundle_root: Path) -> dict:
    """
    Verify bundle contains required directory structure.

    Validates presence of:
    - bundled/claude/ directory with subdirectories
    - bundled/devforgeai/ directory
    - bundled/checksums.json file
    - bundled/version.json file

    Args:
        bundle_root: Root path of bundled directory

    Returns:
        dict with:
        - status: "success" or "failed"
        - file_count: int count of files in bundle
        - missing_components: list[str] of missing required files/dirs

    Raises:
        FileNotFoundError: If critical components missing

    Examples:
        >>> result = verify_bundle_structure(Path("bundled"))
        >>> if result['status'] == 'success':
        ...     print(f"Bundle verified: {result['file_count']} files")
    """
    result = {
        "status": "success",
        "file_count": 0,
        "missing_components": [],
    }

    bundle_root = Path(bundle_root)

    # Check critical directories
    required_dirs = [
        bundle_root / "claude",
        bundle_root / "claude" / "agents",
        bundle_root / "claude" / "commands",
        bundle_root / "claude" / "skills",
        bundle_root / "claude" / "memory",
        bundle_root / "devforgeai",
        bundle_root / "devforgeai" / "context",
    ]

    for dir_path in required_dirs:
        if not dir_path.exists():
            result["missing_components"].append(str(dir_path.relative_to(bundle_root)))
            result["status"] = "failed"

    # Check critical files
    required_files = [
        bundle_root / "checksums.json",
        bundle_root / "version.json",
        bundle_root / "CLAUDE.md",
    ]

    for file_path in required_files:
        if not file_path.exists():
            result["missing_components"].append(str(file_path.relative_to(bundle_root)))
            result["status"] = "failed"

    # Raise error if critical components missing
    if result["missing_components"]:
        raise FileNotFoundError(
            f"Bundle structure incomplete. Missing components:\n" +
            "\n".join(f"  - {comp}" for comp in result["missing_components"])
        )

    # Count total files
    result["file_count"] = count_bundled_files(bundle_root)

    return result


def count_bundled_files(bundle_root: Path) -> int:
    """
    Count total number of files in bundled directory recursively.

    Args:
        bundle_root: Root path of bundled directory

    Returns:
        int: Total file count (excluding directories)

    Examples:
        >>> file_count = count_bundled_files(Path("bundled"))
        >>> print(f"Bundle contains {file_count} files")
        Bundle contains 237 files
    """
    bundle_root = Path(bundle_root)

    if not bundle_root.exists():
        return 0

    file_count = 0
    for file_path in bundle_root.rglob("*"):
        if file_path.is_file():
            file_count += 1

    return file_count


def measure_bundle_size(bundle_root: Path) -> dict:
    """
    Measure bundle size (compressed and uncompressed).

    Calculates:
    - Uncompressed size (sum of all file sizes)
    - Compressed size (tar.gz archive simulation)

    Args:
        bundle_root: Root path of bundled directory

    Returns:
        dict with:
        - uncompressed: int bytes
        - compressed: int bytes (estimated via tar.gz)
        - uncompressed_mb: float megabytes
        - compressed_mb: float megabytes

    Examples:
        >>> sizes = measure_bundle_size(Path("bundled"))
        >>> print(f"Compressed: {sizes['compressed_mb']:.1f} MB")
        >>> print(f"Uncompressed: {sizes['uncompressed_mb']:.1f} MB")
        Compressed: 15.3 MB
        Uncompressed: 48.7 MB
    """
    bundle_root = Path(bundle_root)

    result = {
        "uncompressed": 0,
        "compressed": 0,
        "uncompressed_mb": 0.0,
        "compressed_mb": 0.0,
    }

    if not bundle_root.exists():
        return result

    # Calculate uncompressed size
    for file_path in bundle_root.rglob("*"):
        if file_path.is_file():
            result["uncompressed"] += file_path.stat().st_size

    # Estimate compressed size by creating temporary tar.gz
    try:
        with tempfile.NamedTemporaryFile(suffix=".tar.gz", delete=True) as temp_archive:
            with tarfile.open(temp_archive.name, "w:gz") as tar:
                tar.add(bundle_root, arcname=bundle_root.name)

            # Measure compressed archive size
            result["compressed"] = Path(temp_archive.name).stat().st_size

    except (OSError, tarfile.TarError):
        # If compression fails, estimate using typical tar.gz ratio
        result["compressed"] = int(result["uncompressed"] * COMPRESSION_RATIO_ESTIMATE)

    # Convert to megabytes
    result["uncompressed_mb"] = result["uncompressed"] / MB_DIVISOR
    result["compressed_mb"] = result["compressed"] / MB_DIVISOR

    return result


def validate_bundle_path(bundle_path: str, base_path: Path = None) -> Path:
    """
    Validate and sanitize bundle path to prevent path traversal attacks.

    SECURITY: Implements OWASP A03:2021 - Injection prevention
    - Validates path contains only safe characters (alphanumeric, dot, hyphen, underscore)
    - Prevents directory traversal attempts (../, ../../, etc.)
    - Ensures resolved path is within expected base directory

    Args:
        bundle_path: User-supplied bundle path string (relative or basename)
        base_path: Expected base directory (default: current working directory)

    Returns:
        Path: Validated absolute path

    Raises:
        ValueError: If path contains invalid characters or traversal attempts
        FileNotFoundError: If validated path doesn't exist

    Examples:
        >>> # Valid bundle name
        >>> path = validate_bundle_path("bundled")
        >>> print(path)
        /mnt/c/Projects/DevForgeAI2/bundled

        >>> # Path traversal attempt - BLOCKED
        >>> validate_bundle_path("../../etc/passwd")
        ValueError: Invalid bundle path: contains directory traversal or invalid characters

        >>> # Invalid characters - BLOCKED
        >>> validate_bundle_path("bundle; rm -rf /")
        ValueError: Invalid bundle path: contains directory traversal or invalid characters
    """
    if base_path is None:
        base_path = Path.cwd()

    # SECURITY FIX: Validate path contains only safe characters (CRITICAL violation #2)
    # Prevents: ../../../etc/passwd, bundle; rm -rf /, $(malicious command)
    if not SAFE_PATH_PATTERN.match(bundle_path):
        raise ValueError(
            f"Invalid bundle path '{bundle_path}': contains directory traversal or invalid characters.\n"
            "Allowed characters: alphanumeric, dot (.), hyphen (-), underscore (_)"
        )

    # Construct full path
    full_path = base_path / bundle_path

    # Resolve to absolute path (resolves symlinks and relative components)
    try:
        absolute_path = full_path.resolve()
    except (OSError, RuntimeError) as e:
        raise ValueError(f"Failed to resolve bundle path '{bundle_path}': {e}")

    # SECURITY: Ensure resolved path is within base directory
    # Prevents: Symlink attacks, mount point traversal
    try:
        absolute_path.relative_to(base_path.resolve())
    except ValueError:
        raise ValueError(
            f"Invalid bundle path '{bundle_path}': resolved path outside base directory.\n"
            f"Resolved: {absolute_path}\n"
            f"Expected base: {base_path.resolve()}"
        )

    # Check if path exists
    if not absolute_path.exists():
        raise FileNotFoundError(
            f"Bundle path does not exist: {absolute_path}\n"
            f"Original path: {bundle_path}"
        )

    return absolute_path

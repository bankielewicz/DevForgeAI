"""
Bundle structure verification and size measurement.

This module provides:
- Bundle structure validation (claude/, devforgeai/, checksums.json)
- File counting for completeness verification
- Bundle size measurement (compressed and uncompressed)
- NPM package compliance checks

Functions:
- verify_bundle_structure(bundle_root: Path) -> dict
- count_bundled_files(bundle_root: Path) -> int
- measure_bundle_size(bundle_root: Path) -> dict

Dependencies: Standard library only (pathlib, subprocess, tarfile)
"""

import tarfile
import tempfile
from pathlib import Path

# Configuration constants
MIN_BUNDLED_FILES = 200
COMPRESSION_RATIO_ESTIMATE = 0.3  # Typical tar.gz compression (30% of original)
MB_DIVISOR = 1024 * 1024


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

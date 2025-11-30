"""
Bundle integrity verification using SHA256 checksums.

This module provides:
- SHA256 checksum calculation for files
- Checksum manifest loading from checksums.json
- Bundle integrity verification with tamper detection
- Mismatch reporting and failure threshold enforcement

Functions:
- calculate_sha256(file_path: Path) -> str
- load_checksums(bundle_root: Path) -> dict
- verify_file_checksum(file_path: Path, expected_hash: str) -> bool
- verify_bundle_integrity(bundle_root: Path) -> dict

Dependencies: Standard library only (hashlib, json, pathlib)
"""

import hashlib
import json
from pathlib import Path

# Configuration constants
CHUNK_SIZE = 8192  # Bytes per read for memory efficiency
CHECKSUM_LENGTH = 64  # Expected length of SHA256 hex string
FAILURE_THRESHOLD = 3  # Halt after N checksum failures (tamper detection)


def calculate_sha256(file_path: Path) -> str:
    """
    Calculate SHA256 checksum for a file.

    Reads file in chunks for memory efficiency with large files.

    Args:
        file_path: Path to file to checksum

    Returns:
        str: SHA256 hash as 64-character hex string

    Raises:
        FileNotFoundError: If file doesn't exist
        IOError: If file cannot be read

    Examples:
        >>> hash_value = calculate_sha256(Path("test.txt"))
        >>> print(hash_value)
        'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    sha256_hash = hashlib.sha256()

    # Read file in chunks for memory efficiency
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(CHUNK_SIZE), b""):
            sha256_hash.update(chunk)

    return sha256_hash.hexdigest()


def load_checksums(bundle_root: Path) -> dict:
    """
    Load checksum manifest from bundled/checksums.json.

    Args:
        bundle_root: Root path of bundled directory

    Returns:
        dict: Mapping of relative file paths to SHA256 hashes

    Raises:
        FileNotFoundError: If checksums.json doesn't exist
        json.JSONDecodeError: If checksums.json is invalid JSON
        ValueError: If checksums.json format is invalid

    Examples:
        >>> checksums = load_checksums(Path("bundled"))
        >>> print(checksums["claude/agents/test.md"])
        'abc123...'
    """
    checksums_file = bundle_root / "checksums.json"

    if not checksums_file.exists():
        raise FileNotFoundError(
            f"Checksum manifest not found: {checksums_file}\n"
            "Bundle integrity cannot be verified."
        )

    try:
        content = checksums_file.read_text(encoding='utf-8')
        checksums = json.loads(content)

        if not isinstance(checksums, dict):
            raise ValueError("checksums.json must be a JSON object")

        # Validate format: all values should be proper-length hex strings
        for file_path, hash_value in checksums.items():
            if not isinstance(hash_value, str) or len(hash_value) != CHECKSUM_LENGTH:
                raise ValueError(
                    f"Invalid checksum format for {file_path}: {hash_value}\n"
                    f"Expected {CHECKSUM_LENGTH}-character SHA256 hex string"
                )

        return checksums

    except json.JSONDecodeError as e:
        # Preserve JSON error details for debugging
        raise ValueError(
            f"Invalid JSON in checksums.json: {str(e)}"
        ) from e


def verify_file_checksum(file_path: Path, expected_hash: str) -> bool:
    """
    Verify a single file's checksum matches expected hash.

    Args:
        file_path: Path to file to verify
        expected_hash: Expected SHA256 hash (64-character hex string)

    Returns:
        bool: True if checksum matches, False if mismatch

    Examples:
        >>> is_valid = verify_file_checksum(Path("test.txt"), "abc123...")
        >>> if not is_valid:
        ...     print("File corrupted or tampered!")
    """
    try:
        actual_hash = calculate_sha256(file_path)
        return actual_hash == expected_hash
    except (FileNotFoundError, IOError):
        return False


def verify_bundle_integrity(bundle_root: Path) -> dict:
    """
    Verify integrity of all bundled files using checksums.

    Performs comprehensive validation:
    - Loads checksum manifest
    - Verifies each file's SHA256 hash
    - Reports mismatches
    - Halts after 3 failures (tamper detection)

    Args:
        bundle_root: Root path of bundled directory

    Returns:
        dict with:
        - status: "success" or "failed"
        - files_verified: int count of files checked
        - all_valid: bool (True if all checksums match)
        - mismatches: list of files with checksum mismatches
        - failures: int count of checksum failures

    Raises:
        FileNotFoundError: If checksums.json missing
        ValueError: If 3+ checksum failures (tamper detection)

    Examples:
        >>> result = verify_bundle_integrity(Path("bundled"))
        >>> if result['all_valid']:
        ...     print("Bundle integrity verified")
        ... else:
        ...     print(f"{result['failures']} files corrupted")
    """
    result = {
        "status": "success",
        "files_verified": 0,
        "all_valid": True,
        "mismatches": [],
        "failures": 0,
    }

    try:
        checksums = load_checksums(bundle_root)
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        result["status"] = "failed"
        result["all_valid"] = False
        result["mismatches"] = [str(e)]
        raise

    # Verify each file
    for relative_path, expected_hash in checksums.items():
        file_path = bundle_root / relative_path
        result["files_verified"] += 1

        if not verify_file_checksum(file_path, expected_hash):
            result["all_valid"] = False
            result["failures"] += 1
            result["mismatches"].append(relative_path)

            print(f"✗ Checksum mismatch: {relative_path}")

            # Halt after failure threshold (potential tampering)
            if result["failures"] >= FAILURE_THRESHOLD:
                result["status"] = "failed"
                raise ValueError(
                    f"{FAILURE_THRESHOLD} checksum failures detected - bundle may be tampered.\n"
                    f"Mismatched files:\n" +
                    "\n".join(f"  - {f}" for f in result["mismatches"])
                )

    # All files verified successfully
    if result["all_valid"]:
        print(f"✓ Bundle integrity verified: {result['files_verified']} files")
    else:
        result["status"] = "failed"
        print(
            f"\n⚠ Warning: {result['failures']} file(s) failed checksum verification"
        )

    return result


def verify_all_files_have_checksums(bundle_root: Path) -> None:
    """
    Verify all bundled files have corresponding checksum entries.

    Ensures completeness of checksum manifest (no files without checksums).

    Args:
        bundle_root: Root path of bundled directory

    Raises:
        FileNotFoundError: If checksums.json missing
        ValueError: If files exist without checksum entries

    Examples:
        >>> verify_all_files_have_checksums(Path("bundled"))
        # Passes if all files have checksums

        >>> verify_all_files_have_checksums(Path("bundled"))
        ValueError: Files missing checksums: claude/agents/new-file.md
    """
    checksums = load_checksums(bundle_root)

    # Recursively find all files in bundle
    all_files = set()
    for file_path in bundle_root.rglob("*"):
        if file_path.is_file() and file_path.name != "checksums.json":
            relative_path = str(file_path.relative_to(bundle_root)).replace("\\", "/")
            all_files.add(relative_path)

    # Check for files without checksums
    checksum_keys = set(checksums.keys())
    missing_checksums = all_files - checksum_keys

    if missing_checksums:
        raise ValueError(
            f"Files missing checksums ({len(missing_checksums)} files):\n" +
            "\n".join(f"  - {f}" for f in sorted(missing_checksums)[:10]) +
            (f"\n  ... and {len(missing_checksums) - 10} more" if len(missing_checksums) > 10 else "")
        )

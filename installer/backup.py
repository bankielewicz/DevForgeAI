"""
Backup management for framework installation.

This module handles:
- Creating timestamped backup directories (.backups/devforgeai-upgrade-YYYYMMDD-HHMMSS/)
- Copying .claude/, devforgeai/, CLAUDE.md to backup
- Generating manifest.json with metadata and integrity hash (SHA256)
- Verifying backup integrity before proceeding

Functions:
- create_backup(project_root: Path, reason: str, from_version: str, to_version: str) -> tuple[Path, dict]
- verify_backup_integrity(backup_path: Path) -> dict
"""

import json
import shutil
import hashlib
from pathlib import Path
from datetime import datetime, timezone

# Constants
HASH_ALGORITHM = "sha256"
CHUNK_SIZE = 65536  # 64KB chunks for reading files
MANIFEST_FILENAME = "manifest.json"


def _generate_backup_hash(backup_path: Path) -> str:
    """
    Generate SHA256 hash of all backup files for integrity verification.

    Args:
        backup_path: Path to backup directory

    Returns:
        str: SHA256 hash in format "sha256:abcdef..."
    """
    hasher = hashlib.sha256()

    # Walk through all files in backup directory (sorted for determinism)
    # Exclude manifest.json from hash (it's not hashed, only data files are)
    for file_path in sorted(backup_path.rglob("*")):
        if file_path.is_file() and file_path.name != MANIFEST_FILENAME:
            _hash_file(file_path, hasher)

    return f"{HASH_ALGORITHM}:{hasher.hexdigest()}"


def _hash_file(file_path: Path, hasher) -> None:
    """
    Update hasher with file content.

    Args:
        file_path: Path to file to hash
        hasher: hashlib hasher object to update
    """
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(CHUNK_SIZE):
                hasher.update(chunk)
    except (OSError, IOError) as e:
        # Log warning but continue (non-fatal for hash calculation)
        # File count mismatch will be detected during backup verification
        import sys
        print(f"Warning: Could not read {file_path}: {e}", file=sys.stderr)


def _count_backup_files(backup_path: Path) -> tuple[int, float]:
    """
    Count files in backup and calculate total size.

    Args:
        backup_path: Path to backup directory

    Returns:
        tuple: (file_count, total_size_mb)
    """
    file_count = 0
    total_size = 0

    for file_path in backup_path.rglob("*"):
        if file_path.is_file():
            file_count += 1
            total_size += file_path.stat().st_size

    total_size_mb = total_size / (1024 * 1024)
    return file_count, total_size_mb


def create_backup(
    project_root: Path,
    reason: str,
    from_version: str | None = None,
    to_version: str | None = None,
) -> tuple[Path, dict]:
    """
    Create timestamped backup of framework directories.

    Creates .backups/devforgeai-upgrade-YYYYMMDD-HHMMSS/ with:
    - Copy of .claude/ directory
    - Copy of devforgeai/ directory
    - Copy of CLAUDE.md file
    - manifest.json with metadata and integrity hash

    Args:
        project_root: Root path of project
        reason: Backup reason (e.g., "upgrade", "downgrade")
        from_version: Current installed version (optional)
        to_version: Version being installed (optional)

    Returns:
        tuple: (backup_path, manifest_dict)
        - backup_path: Path to created backup directory
        - manifest_dict: Backup manifest with metadata

    Raises:
        OSError: If backup directory can't be created
        IOError: If files can't be copied
    """
    # Create backup directory with timestamp
    now = datetime.now(timezone.utc)
    timestamp = now.strftime("%Y%m%d-%H%M%S-%f")  # CRITICAL-2 FIX: Add microseconds for uniqueness
    backup_name = f"devforgeai-upgrade-{timestamp}"
    backups_dir = project_root / ".backups"
    backups_dir.mkdir(parents=True, exist_ok=True)
    backup_path = backups_dir / backup_name

    # CRITICAL-2 FIX: Use exclusive creation to prevent race conditions
    try:
        backup_path.mkdir(parents=False, exist_ok=False)  # Fails if exists
    except FileExistsError:
        raise OSError(f"Backup path already exists (race condition detected): {backup_path}")

    try:
        # Copy .claude/ directory
        source_claude = project_root / ".claude"
        if source_claude.exists():
            backup_claude = backup_path / ".claude"
            shutil.copytree(source_claude, backup_claude)

        # Copy devforgeai/ directory
        source_devforgeai = project_root / ".devforgeai"
        if source_devforgeai.exists():
            backup_devforgeai = backup_path / ".devforgeai"
            shutil.copytree(source_devforgeai, backup_devforgeai)

        # Copy CLAUDE.md if it exists
        source_claude_md = project_root / "CLAUDE.md"
        if source_claude_md.exists():
            backup_claude_md = backup_path / "CLAUDE.md"
            shutil.copy2(source_claude_md, backup_claude_md)

        # Count files and calculate size
        file_count, total_size_mb = _count_backup_files(backup_path)

        # Generate integrity hash
        integrity_hash = _generate_backup_hash(backup_path)

        # Create manifest
        manifest = {
            "created_at": now.isoformat(timespec="seconds") + "Z",
            "reason": reason,
            "files_backed_up": file_count,
            "total_size_mb": round(total_size_mb, 1),
            "backup_integrity_hash": integrity_hash,
        }

        if from_version:
            manifest["from_version"] = from_version

        if to_version:
            manifest["to_version"] = to_version

        # Write manifest
        manifest_file = backup_path / MANIFEST_FILENAME
        manifest_file.write_text(json.dumps(manifest, indent=2))

        return backup_path, manifest

    except Exception as e:
        # Clean up on failure
        if backup_path.exists():
            shutil.rmtree(backup_path, ignore_errors=True)
        raise


def verify_backup_integrity(backup_path: Path) -> dict:
    """
    Verify backup integrity by checking manifest and files.

    Args:
        backup_path: Path to backup directory

    Returns:
        dict: Verification result with keys:
        - "valid": bool - True if backup is valid
        - "file_count": int - Number of files in backup
        - "manifest_file_count": int - Files claimed in manifest
        - "hash_matches": bool - Whether calculated hash matches manifest
        - "errors": list[str] - Any validation errors

    Raises:
        FileNotFoundError: If manifest.json doesn't exist
        json.JSONDecodeError: If manifest is invalid JSON
    """
    errors = []
    result = {
        "valid": False,
        "file_count": 0,
        "manifest_file_count": 0,
        "hash_matches": False,
        "errors": errors,
    }

    # Load manifest
    manifest = _load_backup_manifest(backup_path, result)
    if manifest is None:
        return result

    # Count actual files and verify
    file_count = _count_actual_files(backup_path)
    result["file_count"] = file_count
    result["manifest_file_count"] = manifest.get("files_backed_up", 0)

    # Check file count
    if file_count != manifest.get("files_backed_up", 0):
        errors.append(
            f"File count mismatch: {file_count} actual vs {manifest.get('files_backed_up')} expected"
        )

    # Verify hash (if it fails, continue - it's not fatal)
    _verify_hash(backup_path, manifest, result)

    # Determine validity
    result["valid"] = len(errors) == 0

    return result


def _load_backup_manifest(backup_path: Path, result: dict) -> dict | None:
    """
    Load and parse backup manifest file.

    Args:
        backup_path: Path to backup directory
        result: Result dict to update with errors

    Returns:
        dict: Manifest content, or None if load failed
    """
    manifest_file = backup_path / MANIFEST_FILENAME
    if not manifest_file.exists():
        result["errors"].append("manifest.json not found")
        return None

    try:
        return json.loads(manifest_file.read_text())
    except json.JSONDecodeError as e:
        result["errors"].append(f"Invalid manifest JSON: {e}")
        return None


def _count_actual_files(backup_path: Path) -> int:
    """
    Count backup files excluding manifest.json.

    Args:
        backup_path: Path to backup directory

    Returns:
        int: Number of files
    """
    count = 0
    for file_path in backup_path.rglob("*"):
        if file_path.is_file() and file_path.name != MANIFEST_FILENAME:
            count += 1
    return count


def _verify_hash(backup_path: Path, manifest: dict, result: dict) -> None:
    """
    Verify backup hash against manifest.

    Args:
        backup_path: Path to backup directory
        manifest: Backup manifest dict
        result: Result dict to update with hash status
    """
    if "backup_integrity_hash" not in manifest:
        return

    calculated_hash = _generate_backup_hash(backup_path)
    result["hash_matches"] = calculated_hash == manifest["backup_integrity_hash"]
    if not result["hash_matches"]:
        result["errors"].append(
            f"Hash mismatch: {calculated_hash} vs {manifest['backup_integrity_hash']}"
        )

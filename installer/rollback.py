"""
Backup listing and rollback restoration.

This module handles:
- Listing available backups sorted by timestamp (newest first)
- Verifying backup integrity before restore
- Restoring all files from backup
- Reverting version.json to backup version
- Verifying checksums match backup

Functions:
- list_backups(project_root: Path) -> list[dict]
- restore_from_backup(project_root: Path, backup_path: Path) -> dict
- verify_rollback(project_root: Path, backup_path: Path) -> dict
"""

import json
import shutil
import hashlib
from pathlib import Path
from typing import Optional


def list_backups(project_root: Path) -> list[dict]:
    """
    List all available backups sorted by timestamp (newest first).

    Args:
        project_root: Root path of project

    Returns:
        list[dict]: List of backup info dicts, each containing:
        - "path": Path object to backup directory
        - "name": Backup directory name
        - "timestamp": ISO timestamp from manifest (if available)
        - "reason": Backup reason from manifest (if available)
        - "from_version": Original version (if available)
        - "to_version": Target version (if available)

    Returns empty list if no backups found.
    """
    backups_dir = project_root / ".backups"

    if not backups_dir.exists():
        return []

    backups = []

    for backup_path in sorted(backups_dir.iterdir(), reverse=True):
        if not backup_path.is_dir():
            continue

        backup_info = {
            "path": backup_path,
            "name": backup_path.name,
            "timestamp": None,
            "reason": None,
            "from_version": None,
            "to_version": None,
        }

        # Try to load manifest for additional info
        manifest_file = backup_path / "manifest.json"
        if manifest_file.exists():
            try:
                manifest = json.loads(manifest_file.read_text())
                backup_info["timestamp"] = manifest.get("created_at")
                backup_info["reason"] = manifest.get("reason")
                backup_info["from_version"] = manifest.get("from_version")
                backup_info["to_version"] = manifest.get("to_version")
            except (json.JSONDecodeError, IOError):
                # Manifest unavailable, use what we have
                pass

        backups.append(backup_info)

    return backups


def restore_from_backup(project_root: Path, backup_path: Path) -> dict:
    """
    Restore all files from backup to project root.

    Restores:
    - .claude/ directory
    - .devforgeai/ directory
    - CLAUDE.md file
    - Reverts version.json to backed-up version

    Args:
        project_root: Root path of target project
        backup_path: Path to backup directory to restore from

    Returns:
        dict: Restoration report with:
        - "status": "success" or "failed"
        - "files_restored": int count
        - "version_reverted": bool
        - "errors": list[str] of any errors

    Raises:
        FileNotFoundError: If backup doesn't exist
        OSError: If files can't be restored
    """
    result = {
        "status": "success",
        "files_restored": 0,
        "version_reverted": False,
        "errors": [],
    }

    if not backup_path.exists():
        raise FileNotFoundError(f"Backup not found: {backup_path}")

    # CRITICAL-1 FIX: Validate backup path is within .backups/ directory (prevent path traversal)
    backups_dir = project_root / ".backups"
    try:
        backup_path.relative_to(backups_dir)
    except ValueError:
        raise ValueError(
            f"Security violation: Backup path is not within .backups/: {backup_path}"
        )

    try:
        # Restore .claude/ directory
        backup_claude = backup_path / ".claude"
        target_claude = project_root / ".claude"

        if backup_claude.exists():
            # CRITICAL-1 FIX: Validate no symlinks in backup (prevent symlink attacks)
            if backup_claude.is_symlink():
                raise ValueError(f"Security violation: Backup contains symlink: {backup_claude}")

            if target_claude.exists():
                shutil.rmtree(target_claude)
            shutil.copytree(backup_claude, target_claude, symlinks=False)  # Don't follow symlinks
            # Count restored files
            result["files_restored"] += sum(1 for _ in target_claude.rglob("*") if _.is_file())

        # Restore .devforgeai/ directory
        backup_devforgeai = backup_path / ".devforgeai"
        target_devforgeai = project_root / ".devforgeai"

        if backup_devforgeai.exists():
            # CRITICAL-1 FIX: Validate no symlinks in backup
            if backup_devforgeai.is_symlink():
                raise ValueError(f"Security violation: Backup contains symlink: {backup_devforgeai}")

            if target_devforgeai.exists():
                shutil.rmtree(target_devforgeai)
            shutil.copytree(backup_devforgeai, target_devforgeai, symlinks=False)
            # Count restored files
            result["files_restored"] += sum(
                1 for _ in target_devforgeai.rglob("*") if _.is_file()
            )

        # Restore CLAUDE.md
        backup_claude_md = backup_path / "CLAUDE.md"
        target_claude_md = project_root / "CLAUDE.md"

        if backup_claude_md.exists():
            # CRITICAL-1 FIX: Validate no symlinks in backup
            if backup_claude_md.is_symlink():
                raise ValueError(f"Security violation: Backup contains symlink: {backup_claude_md}")

            shutil.copy2(backup_claude_md, target_claude_md)
            result["files_restored"] += 1

        # Check if version.json was restored (indicates successful revert)
        version_file = target_devforgeai / ".version.json"
        if version_file.exists():
            result["version_reverted"] = True

    except (FileNotFoundError, OSError) as e:
        result["status"] = "failed"
        result["errors"].append(f"Restoration failed: {e}")
        raise

    return result


def verify_rollback(project_root: Path, backup_path: Path) -> dict:
    """
    Verify that rollback was successful by comparing files.

    Args:
        project_root: Root path of target project
        backup_path: Path to backup directory used for restoration

    Returns:
        dict: Verification result with:
        - "valid": bool - True if rollback successful
        - "backup_files": int - Files in backup
        - "restored_files": int - Files restored to project
        - "checksums_match": bool - Whether checksums match (100% validation)
        - "errors": list[str] - Any validation errors
    """
    result = {
        "valid": False,
        "backup_files": 0,
        "restored_files": 0,
        "checksums_match": False,
        "errors": [],
    }

    # Count backup files (excluding manifest)
    backup_files = 0
    backup_hashes = {}

    for file_path in backup_path.rglob("*"):
        if file_path.is_file() and file_path.name != "manifest.json":
            backup_files += 1
            try:
                with open(file_path, "rb") as f:
                    file_hash = hashlib.sha256(f.read()).hexdigest()
                    relative = file_path.relative_to(backup_path)
                    backup_hashes[str(relative)] = file_hash
            except (IOError, OSError):
                pass

    result["backup_files"] = backup_files

    # Count restored files
    restored_files = 0
    restored_hashes = {}

    for backup_subdir in [".claude", ".devforgeai", "CLAUDE.md"]:
        if backup_subdir == "CLAUDE.md":
            target_file = project_root / "CLAUDE.md"
            if target_file.exists():
                restored_files += 1
                try:
                    with open(target_file, "rb") as f:
                        file_hash = hashlib.sha256(f.read()).hexdigest()
                        restored_hashes["CLAUDE.md"] = file_hash
                except (IOError, OSError):
                    pass
        else:
            target_dir = project_root / backup_subdir
            if target_dir.exists():
                for file_path in target_dir.rglob("*"):
                    if file_path.is_file():
                        restored_files += 1
                        try:
                            with open(file_path, "rb") as f:
                                file_hash = hashlib.sha256(f.read()).hexdigest()
                                relative = file_path.relative_to(project_root)
                                restored_hashes[str(relative)] = file_hash
                        except (IOError, OSError):
                            pass

    result["restored_files"] = restored_files

    # Verify checksums (100% validation)
    if backup_files == restored_files and backup_files > 0:
        # Compare hashes - CRITICAL-3 FIX: Strict matching required for data integrity
        matches = 0
        mismatches = []
        for rel_path, backup_hash in backup_hashes.items():
            if rel_path in restored_hashes:
                if restored_hashes[rel_path] == backup_hash:
                    matches += 1
                else:
                    mismatches.append(f"{rel_path}: hash mismatch")

        # CRITICAL-3 FIX: Require 100% match (was 95%)
        result["checksums_match"] = matches == backup_files
        if mismatches:
            result["errors"].extend(mismatches[:10])  # First 10 mismatches
            if len(mismatches) > 10:
                result["errors"].append(f"... and {len(mismatches) - 10} more mismatches")

    # Determine validity
    if backup_files > 0 and restored_files > 0 and result["checksums_match"]:
        result["valid"] = True
    elif backup_files == 0:
        result["errors"].append("Backup appears empty")
    elif restored_files == 0:
        result["errors"].append("No files were restored")
    else:
        result["errors"].append("File count or hash verification mismatch")

    return result

"""
BackupService for creating and restoring DevForgeAI installation backups (STORY-078).

Implements:
- SVC-004: Create complete backup of DevForgeAI installation
- SVC-005: Restore from backup
- SVC-006: List available backups
- SVC-007: Delete old backups (retention policy)

Follows clean architecture with dependency injection and atomic operations.
"""

import json
import shutil
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from abc import ABC, abstractmethod
import time
import os
import stat

from installer.models import (
    BackupMetadata,
    FileEntry,
    BackupReason,
    BackupError,
)

# Constants for backup operations
BACKUP_TIMEOUT_SECONDS = 30
CHECKSUM_CHUNK_SIZE = 65536  # 64KB chunks for SHA256 calculation
PERMISSION_PRESERVE_ERRORS = (OSError, AttributeError)  # Errors to ignore when preserving permissions

# Directory permissions for security (owner only)
BACKUP_DIR_PERMISSIONS = 0o700  # rwx------
MANIFEST_FILE_PERMISSIONS = 0o600  # rw-------

# JSON formatting
JSON_INDENT = 2
JSON_ENCODING = "utf-8"


class IBackupService(ABC):
    """Interface for backup operations."""

    @abstractmethod
    def create_backup(
        self,
        source_root: Path,
        version: str,
        reason: BackupReason = BackupReason.UPGRADE,
    ) -> BackupMetadata:
        """Create backup of installation."""
        pass

    @abstractmethod
    def restore(self, backup_id: str, target_root: Path) -> None:
        """Restore installation from backup."""
        pass

    @abstractmethod
    def list_backups(self) -> List[BackupMetadata]:
        """List all available backups."""
        pass

    @abstractmethod
    def cleanup(self, retention_count: int = 5) -> int:
        """Delete old backups, keep most recent N."""
        pass


class BackupService(IBackupService):
    """Creates and manages installation backups."""

    # Directories to exclude from backup
    EXCLUDED_DIRS = {
        ".git",
        "__pycache__",
        ".pytest_cache",
        ".tox",
        ".venv",
        "venv",
        "node_modules",
        ".egg-info",
        ".dist-info",
        ".devforgeai/backups",  # Don't backup old backups
    }

    # Files to exclude from backup
    EXCLUDED_FILES = {
        ".pyc",
        ".pyo",
        ".DS_Store",
        "thumbs.db",
    }

    def __init__(self, backups_root: Optional[Path] = None, allow_external_path: bool = False) -> None:
        """
        Initialize BackupService.

        Args:
            backups_root: Root directory for backups.
                Defaults to .devforgeai/backups in current directory.
            allow_external_path: If True, bypass path traversal validation.
                ONLY use for testing scenarios. Production code should never use this.
        """
        if backups_root is None:
            backups_root = Path.cwd() / ".devforgeai" / "backups"

        # Validate path to prevent traversal attacks
        backups_root = Path(backups_root).resolve()
        cwd_root = Path.cwd().resolve()

        # Ensure backup directory is within or at current working directory
        # Skip validation if allow_external_path=True (testing only)
        if not allow_external_path:
            try:
                backups_root.relative_to(cwd_root)
            except ValueError:
                raise BackupError(
                    f"Backup directory must be within current working directory. "
                    f"Provided: {backups_root}, Current: {cwd_root}"
                )

        self.backups_root = backups_root

    def create_backup(
        self,
        source_root: Path,
        version: str,
        reason: BackupReason = BackupReason.UPGRADE,
    ) -> BackupMetadata:
        """
        Create complete backup of installation.

        Args:
            source_root: Root directory to backup (.devforgeai, .claude, CLAUDE.md, etc.)
            version: Version being backed up
            reason: Reason for backup creation

        Returns:
            BackupMetadata with backup information

        Raises:
            BackupError: If backup creation fails
        """
        start_time = time.time()

        try:
            # Validate source exists
            source_root = Path(source_root)
            if not source_root.exists():
                raise BackupError(f"Source directory not found: {source_root}")

            # Create backup directory with timestamp
            now = datetime.now(timezone.utc)
            timestamp = now.strftime("%Y%m%d-%H%M%S-%f")[:-3]  # millisecond precision
            backup_id = f"v{version}-{timestamp}"
            backup_dir = self.backups_root / backup_id

            # Ensure backups directory exists with proper permissions
            self.backups_root.mkdir(parents=True, exist_ok=True)

            if backup_dir.exists():
                raise BackupError(f"Backup directory already exists: {backup_dir}")

            backup_dir.mkdir(parents=True, exist_ok=False)
            # Set restrictive permissions on backup directory (owner only)
            os.chmod(backup_dir, BACKUP_DIR_PERMISSIONS)

            # Copy files and collect metadata
            files: List[FileEntry] = []
            self._copy_directory_tree(source_root, backup_dir, files)

            # Create manifest
            duration = time.time() - start_time
            if duration > BACKUP_TIMEOUT_SECONDS:
                raise BackupError(
                    f"Backup creation exceeded {BACKUP_TIMEOUT_SECONDS} seconds: {duration:.1f}s"
                )

            metadata = BackupMetadata(
                backup_id=backup_id,
                version=version,
                created_at=now.isoformat(),
                files=files,
                reason=reason,
                duration_seconds=duration,
            )

            # Write manifest file
            manifest_path = backup_dir / "backup-manifest.json"
            manifest_json = {
                "backup_id": metadata.backup_id,
                "version": metadata.version,
                "created_at": metadata.created_at,
                "duration_seconds": metadata.duration_seconds,
                "reason": metadata.reason.value,
                "files": [
                    {
                        "relative_path": f.relative_path,
                        "checksum_sha256": f.checksum_sha256,
                        "size_bytes": f.size_bytes,
                        "modification_time": f.modification_time,
                    }
                    for f in metadata.files
                ],
            }

            manifest_path.write_text(
                json.dumps(manifest_json, indent=JSON_INDENT),
                encoding=JSON_ENCODING
            )
            # Set restrictive permissions on manifest file (owner only, read/write)
            os.chmod(manifest_path, MANIFEST_FILE_PERMISSIONS)

            return metadata

        except BackupError:
            raise
        except OSError as e:
            if "No space left on device" in str(e):
                raise BackupError(f"Insufficient disk space for backup: {e}")
            if "Permission denied" in str(e):
                raise BackupError(
                    f"Permission denied creating backup at {self.backups_root}: {e}"
                )
            raise BackupError(f"OS error during backup creation: {e}")
        except Exception as e:
            raise BackupError(f"Backup creation failed: {e}")

    def _should_exclude_path(self, rel_path: Path, src_path: Path) -> bool:
        """
        Check if path should be excluded from backup.

        Args:
            rel_path: Relative path within source
            src_path: Absolute source path

        Returns:
            True if path should be excluded, False otherwise
        """
        # Check if any part of path is in excluded directories
        if any(excluded in rel_path.parts for excluded in self.EXCLUDED_DIRS):
            return True

        # Check if file has excluded extension
        if any(src_path.name.endswith(ext) for ext in self.EXCLUDED_FILES):
            return True

        return False

    def _copy_file_with_metadata(
        self, src_path: Path, dst_path: Path, rel_path: Path, files_list: List[FileEntry]
    ) -> None:
        """
        Copy a file and record its metadata.

        Args:
            src_path: Source file path
            dst_path: Destination file path
            rel_path: Relative path for metadata
            files_list: List to accumulate FileEntry objects
        """
        # Create parent directories
        dst_path.parent.mkdir(parents=True, exist_ok=True)

        # Copy file
        shutil.copy2(src_path, dst_path)

        # Calculate checksum
        checksum = self._calculate_sha256(dst_path)

        # Get file info
        stat_info = src_path.stat()

        # Add to files list
        files_list.append(
            FileEntry(
                relative_path=str(rel_path),
                checksum_sha256=checksum,
                size_bytes=stat_info.st_size,
                modification_time=stat_info.st_mtime,
            )
        )

    def _copy_directory_with_permissions(self, src_path: Path, dst_path: Path) -> None:
        """
        Copy directory and preserve permissions.

        Args:
            src_path: Source directory path
            dst_path: Destination directory path
        """
        # Create directory
        dst_path.mkdir(parents=True, exist_ok=True)

        # Preserve permissions
        try:
            stat_info = src_path.stat()
            os.chmod(dst_path, stat.S_IMODE(stat_info.st_mode))
        except PERMISSION_PRESERVE_ERRORS:
            pass

    def _copy_symlink(self, src_path: Path, dst_path: Path) -> None:
        """
        Copy symlink or target if symlinks not supported.

        Args:
            src_path: Source symlink path
            dst_path: Destination symlink path
        """
        try:
            link_target = src_path.readlink()
            dst_path.symlink_to(link_target)
        except (OSError, NotImplementedError):
            # If symlink not supported (Windows), copy target
            if src_path.exists():
                shutil.copy2(src_path, dst_path)

    def _copy_directory_tree(
        self, src_dir: Path, dst_dir: Path, files_list: List[FileEntry]
    ) -> None:
        """
        Recursively copy directory tree, excluding certain directories/files.

        Args:
            src_dir: Source directory
            dst_dir: Destination directory
            files_list: List to accumulate FileEntry objects
        """
        for src_path in src_dir.rglob("*"):
            # Get relative path and skip excluded paths
            try:
                rel_path = src_path.relative_to(src_dir)
                if self._should_exclude_path(rel_path, src_path):
                    continue
            except ValueError:
                continue

            dst_path = dst_dir / rel_path

            if src_path.is_dir():
                self._copy_directory_with_permissions(src_path, dst_path)
            elif src_path.is_file():
                self._copy_file_with_metadata(src_path, dst_path, rel_path, files_list)
            elif src_path.is_symlink():
                self._copy_symlink(src_path, dst_path)

    def _calculate_sha256(self, file_path: Path) -> str:
        """Calculate SHA256 checksum of file."""
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(CHECKSUM_CHUNK_SIZE), b""):
                sha256.update(chunk)
        return sha256.hexdigest()

    def _validate_path_safety(self, rel_path: str, target_root: Path) -> Path:
        """
        Validate path is safe and within target directory (prevent traversal attacks).

        Args:
            rel_path: Relative path from manifest
            target_root: Target installation root

        Returns:
            Resolved absolute path

        Raises:
            BackupError: If path is outside target directory
        """
        try:
            rel_path_obj = Path(rel_path)
            # Resolve to absolute and check if within target directory
            resolved = (target_root / rel_path_obj).resolve()
            target_resolved = target_root.resolve()
            if not str(resolved).startswith(str(target_resolved)):
                raise BackupError(
                    f"Invalid path in manifest (directory traversal attempt): {rel_path}"
                )
            return resolved
        except ValueError:
            raise BackupError(f"Invalid path format in manifest: {rel_path}")

    def _restore_file(
        self, file_entry_dict: dict, backup_dir: Path, target_root: Path
    ) -> None:
        """
        Restore a single file from backup with checksum verification.

        Args:
            file_entry_dict: File entry from manifest
            backup_dir: Backup directory
            target_root: Target installation root

        Raises:
            BackupError: If file restoration fails
        """
        rel_path = file_entry_dict["relative_path"]
        expected_checksum = file_entry_dict["checksum_sha256"]

        # Validate path safety
        dst_file = self._validate_path_safety(rel_path, target_root)

        src_file = backup_dir / rel_path

        if not src_file.exists():
            raise BackupError(f"Backup file missing: {rel_path}")

        # Verify checksum
        actual_checksum = self._calculate_sha256(src_file)
        if actual_checksum != expected_checksum:
            raise BackupError(
                f"Backup file corrupted (checksum mismatch): {rel_path}"
            )

        # Ensure parent directory exists
        dst_file.parent.mkdir(parents=True, exist_ok=True)

        # Restore file
        shutil.copy2(src_file, dst_file)

    def restore(self, backup_id: str, target_root: Path) -> None:
        """
        Restore installation from backup.

        Args:
            backup_id: ID of backup to restore (e.g., "v1.0.0-20240115-143022-001")
            target_root: Root directory to restore to

        Raises:
            BackupError: If restoration fails
        """
        try:
            backup_dir = self.backups_root / backup_id
            if not backup_dir.exists():
                raise BackupError(f"Backup not found: {backup_id}")

            # Read and validate manifest
            manifest_path = backup_dir / "backup-manifest.json"
            if not manifest_path.exists():
                raise BackupError(f"Backup manifest not found: {manifest_path}")

            try:
                manifest_json = json.loads(manifest_path.read_text(encoding=JSON_ENCODING))
            except json.JSONDecodeError as e:
                raise BackupError(f"Invalid backup manifest JSON: {e}")

            # Create target root if needed
            target_root = Path(target_root)
            target_root.mkdir(parents=True, exist_ok=True)

            # Restore files with checksum verification
            for file_entry_dict in manifest_json.get("files", []):
                self._restore_file(file_entry_dict, backup_dir, target_root)

        except BackupError:
            raise
        except Exception as e:
            raise BackupError(f"Restore failed: {e}")

    def list_backups(self) -> List[BackupMetadata]:
        """
        List all available backups.

        Returns:
            List of BackupMetadata objects, sorted by creation time (newest first)
        """
        backups = []

        if not self.backups_root.exists():
            return backups

        for backup_dir in sorted(self.backups_root.iterdir(), reverse=True):
            if not backup_dir.is_dir():
                continue

            manifest_path = backup_dir / "backup-manifest.json"
            if not manifest_path.exists():
                continue

            try:
                manifest_json = json.loads(manifest_path.read_text(encoding=JSON_ENCODING))

                files = [
                    FileEntry(
                        relative_path=f["relative_path"],
                        checksum_sha256=f["checksum_sha256"],
                        size_bytes=f["size_bytes"],
                        modification_time=f["modification_time"],
                    )
                    for f in manifest_json.get("files", [])
                ]

                metadata = BackupMetadata(
                    backup_id=manifest_json["backup_id"],
                    version=manifest_json["version"],
                    created_at=manifest_json["created_at"],
                    files=files,
                    reason=BackupReason(manifest_json.get("reason", "UPGRADE")),
                    duration_seconds=manifest_json.get("duration_seconds"),
                )

                backups.append(metadata)
            except (json.JSONDecodeError, ValueError, KeyError):
                # Skip invalid backups
                continue

        return backups

    def cleanup(self, retention_count: int = 5) -> int:
        """
        Delete old backups, keeping most recent N.

        Args:
            retention_count: Number of backups to keep

        Returns:
            Number of backups deleted
        """
        if retention_count < 1:
            raise ValueError("retention_count must be at least 1")

        backups = self.list_backups()
        deleted_count = 0

        # Delete backups beyond retention count (older ones)
        for backup in backups[retention_count:]:
            backup_dir = self.backups_root / backup.backup_id
            try:
                shutil.rmtree(backup_dir)
                deleted_count += 1
            except Exception:
                # Continue cleanup even if one fails
                continue

        return deleted_count

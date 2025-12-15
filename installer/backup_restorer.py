"""
BackupRestorer for file restoration from backup with user content preservation (STORY-080).

Restores files from backup to target directory with:
- User content path exclusion by default (devforgeai/specs/, devforgeai/specs/context/, devforgeai/specs/adrs/)
- Optional inclusion of user content with include_user_content=True
- Checksum verification against manifest

Implements:
- AC#4: Restore all files from backup
- AC#5: Preserve user content by default
- AC#6: Verify checksums
"""

import json
import hashlib
import shutil
from pathlib import Path
from typing import Optional
from abc import ABC, abstractmethod

from installer.models import RestoreResult


class ILogger(ABC):
    """Logger interface for dependency injection."""

    @abstractmethod
    def info(self, message: str) -> None:
        """Log info level message."""
        pass

    @abstractmethod
    def error(self, message: str) -> None:
        """Log error level message."""
        pass


CHECKSUM_CHUNK_SIZE = 65536  # 64KB chunks for SHA256

# Paths to skip by default (user content)
USER_CONTENT_PATHS = [
    "devforgeai/specs/Stories",
    "devforgeai/specs/Epics",
    "devforgeai/context",
    "devforgeai/adrs",
]


class BackupRestorer:
    """Restores files from backup to target directory."""

    def __init__(self, logger: Optional[ILogger] = None):
        """
        Initialize restorer with optional logger.

        Args:
            logger: Optional logger for info/error messages
        """
        self.logger = logger

    def restore(
        self,
        backup_dir: Path,
        target_dir: Path,
        include_user_content: bool = False,
    ) -> RestoreResult:
        """
        Restore files from backup to target directory.

        Args:
            backup_dir: Path to backup directory
            target_dir: Path to target directory
            include_user_content: If True, restore user content; if False, preserve it

        Returns:
            RestoreResult with files restored/preserved counts and checksum status

        Raises:
            Exception: If backup directory not found
        """
        backup_dir = Path(backup_dir)
        target_dir = Path(target_dir)

        if not backup_dir.exists():
            raise Exception(f"Backup directory not found: {backup_dir}")

        try:

            files_restored = 0
            files_preserved = 0
            checksums_verified = True

            # Load manifest if exists
            manifest_path = backup_dir / "manifest.json"
            manifest = {}
            if manifest_path.exists():
                with open(manifest_path, "r") as f:
                    manifest = json.load(f)

            # Walk through backup files
            for item in backup_dir.rglob("*"):
                if item.is_dir():
                    continue

                # Skip manifest.json itself
                if item.name == "manifest.json":
                    continue

                # Calculate relative path from backup_dir
                relative_path = item.relative_to(backup_dir)
                relative_str = str(relative_path)

                # Check if this is user content
                is_user_content = self._is_user_content(relative_str)

                # Skip user content if not requested
                if is_user_content and not include_user_content:
                    files_preserved += 1
                    if self.logger:
                        self.logger.info(f"Preserving user content: {relative_str}")
                    continue

                # Create target path
                target_path = target_dir / relative_path

                # Create parent directories
                target_path.parent.mkdir(parents=True, exist_ok=True)

                # Copy file
                try:
                    shutil.copy2(item, target_path)
                    files_restored += 1
                    if self.logger:
                        self.logger.info(f"Restored: {relative_str}")
                except Exception as e:
                    if self.logger:
                        self.logger.error(f"Failed to restore {relative_str}: {e}")
                    raise

            # Verify checksums if manifest exists
            if manifest and "files" in manifest:
                checksums_verified = self._verify_checksums(target_dir, manifest)

            return RestoreResult(
                files_restored=files_restored,
                files_preserved=files_preserved,
                checksums_verified=checksums_verified,
            )

        except Exception as e:
            if self.logger:
                self.logger.error(f"Restore error: {str(e)}")
            return RestoreResult(
                files_restored=0,
                files_preserved=0,
                checksums_verified=False,
                error=str(e),
            )

    def _is_user_content(self, relative_path: str) -> bool:
        """
        Check if path is user content that should be preserved by default.

        Args:
            relative_path: Relative path string

        Returns:
            True if path is user content, False otherwise
        """
        # Normalize path separators
        path = relative_path.replace("\\", "/")

        for user_path in USER_CONTENT_PATHS:
            if path.startswith(user_path):
                return True

        return False

    def _verify_checksums(self, target_dir: Path, manifest: dict) -> bool:
        """
        Verify file checksums against manifest.

        Args:
            target_dir: Path to target directory
            manifest: Manifest dict with file checksums

        Returns:
            True if all checksums verified, False if any mismatch
        """
        files_info = manifest.get("files", {})

        for file_path_str, file_info in files_info.items():
            file_path = target_dir / file_path_str

            # Skip if file doesn't exist (may have been user content)
            if not file_path.exists():
                continue

            # Get expected checksum
            if isinstance(file_info, dict) and "checksum" in file_info:
                expected_checksum = file_info["checksum"]

                # Calculate actual checksum
                actual_checksum = self._calculate_checksum(file_path)

                if actual_checksum != expected_checksum:
                    if self.logger:
                        self.logger.error(
                            f"Checksum mismatch for {file_path_str}: "
                            f"expected {expected_checksum}, got {actual_checksum}"
                        )
                    return False

        return True

    def _calculate_checksum(self, file_path: Path) -> str:
        """
        Calculate SHA256 checksum of file.

        Args:
            file_path: Path to file

        Returns:
            SHA256 hex digest
        """
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(CHECKSUM_CHUNK_SIZE), b""):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()

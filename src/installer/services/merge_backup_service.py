"""
MergeBackupService for creating and verifying backup files.

Requirements:
- SVC-006: Generate unique timestamped backup filenames
- SVC-007: Handle backup file collision with counter
- SVC-008: Verify backup integrity (size and hash)
- SVC-009: Preserve original file permissions
- BR-001: Backup MUST be created before any file modification
- NFR-003: Backup creation <1s for 1MB files
- NFR-004: Backup preserves file permissions
- NFR-006: Atomic backup creation (no partial backups)
"""

import shutil
import hashlib
import os
from pathlib import Path
from datetime import datetime
from typing import Protocol, Optional

from ..config.merge_config import MergeConfig


class Logger(Protocol):
    """Logger protocol for dependency injection."""
    def log(self, message: str) -> None: ...


class MergeBackupService:
    """
    Service for creating and verifying backup files.

    CRITICAL REQUIREMENT: Use specific exception types (FileNotFoundError, PermissionError, OSError).
    Never use bare except or generic Exception.
    """

    def __init__(self, logger: Optional[Logger] = None):
        """
        Initialize backup service.

        Args:
            logger: Optional logger following ILogger protocol. If provided, all operations
                   will be logged for debugging and audit trails.
        """
        self.logger = logger
        self._log = self.logger.log if logger else lambda msg: None

    def create_backup(self, original_file: Path, logger: Optional[Logger] = None) -> Path:
        """
        Create timestamped backup of original file.

        Requirements:
        - SVC-006: Filename format CLAUDE.md.backup-YYYYMMDD-HHMMSS
        - SVC-007: Handle collisions with -001, -002 counters
        - SVC-009: Preserve original file permissions
        - NFR-003: Complete in <1s for 1MB files

        Args:
            original_file: Path to file to backup
            logger: Optional logger for this operation

        Returns:
            Path to backup file created

        Raises:
            FileNotFoundError: If source file doesn't exist
            PermissionError: If no read permission on source
            OSError: If write fails (disk full, etc.)
        """
        logger = logger or self.logger

        # Validate source file exists
        original_file = Path(original_file)

        # Security: Reject symlinks (prevents symlink attacks)
        if original_file.is_symlink():
            raise PermissionError(
                f"Cannot backup symlink (security risk): {original_file}. "
                "Symlinks must be resolved to actual files."
            )

        if not original_file.exists():
            raise FileNotFoundError(f"Source file not found: {original_file}")

        # Check read permission
        if not os.access(original_file, os.R_OK):
            raise PermissionError(f"Cannot read source file: {original_file}")

        # Generate timestamped filename
        timestamp = datetime.now().strftime(MergeConfig.BACKUP_TIMESTAMP_FORMAT)
        backup_name = f"{original_file.name}.backup-{timestamp}"
        backup_path = original_file.parent / backup_name

        # Handle collision (multiple backups in same second)
        if backup_path.exists():
            counter = 1
            while backup_path.exists():
                backup_name = f"{original_file.name}.backup-{timestamp}-{counter:03d}"
                backup_path = original_file.parent / backup_name
                counter += 1

        # Copy file with permission preservation
        try:
            shutil.copy2(original_file, backup_path)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Source file not found during copy: {original_file}") from e
        except PermissionError as e:
            raise PermissionError(f"Cannot write to destination: {backup_path}") from e
        except OSError as e:
            raise OSError(f"IO error during backup copy: {e}") from e

        # Verify backup was created
        if not backup_path.exists():
            raise OSError(f"Backup file was not created: {backup_path}")

        if logger:
            logger.log(f"Backup created: {backup_path}")

        return backup_path

    def verify_backup(self, original_file: Path, backup_file: Path) -> bool:
        """
        Verify backup integrity (size and SHA256 hash).

        Requirements:
        - SVC-008: Verify backup integrity (size and hash match)

        Args:
            original_file: Path to original file
            backup_file: Path to backup file

        Returns:
            True if backup is valid (size and hash match), False otherwise
        """
        original_file = Path(original_file)
        backup_file = Path(backup_file)

        # Check backup exists
        if not backup_file.exists():
            if self.logger:
                self.logger.log(f"Backup file does not exist: {backup_file}")
            return False

        # Compare sizes
        try:
            original_size = original_file.stat().st_size
            backup_size = backup_file.stat().st_size
            if original_size != backup_size:
                if self.logger:
                    self.logger.log(
                        f"Backup size mismatch: original {original_size}, backup {backup_size}"
                    )
                return False
        except OSError as e:
            if self.logger:
                self.logger.log(f"Error checking file size: {e}")
            return False

        # Compare SHA256 hashes
        try:
            original_hash = self._calculate_file_hash(original_file)
            backup_hash = self._calculate_file_hash(backup_file)
            if original_hash != backup_hash:
                if self.logger:
                    self.logger.log(
                        f"Backup hash mismatch: original {original_hash}, backup {backup_hash}"
                    )
                return False
        except OSError as e:
            if self.logger:
                self.logger.log(f"Error calculating file hash: {e}")
            return False

        if self.logger:
            self.logger.log(f"Backup verified successfully: {backup_file}")

        return True

    def _calculate_file_hash(self, file_path: Path) -> str:
        """
        Calculate SHA256 hash of file (private method).

        Uses efficient streaming for large files to minimize memory footprint.

        Args:
            file_path: Path to file to hash

        Returns:
            Hex digest of SHA256 hash as lowercase string

        Raises:
            OSError: If file cannot be read
        """
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except OSError as e:
            raise OSError(f"Cannot read file for hashing: {file_path}") from e

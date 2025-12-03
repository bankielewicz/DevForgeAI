"""
CLAUDE.md Detection Service - STORY-073

Handles detection of existing CLAUDE.md files and backup recommendations.

Requirements:
- SVC-008: Detect existing CLAUDE.md and extract metadata (size, modified date)
- SVC-009: Determine if backup is needed (skip for 0-byte files)
- SVC-010: Generate backup filename with timestamp

Business Rules:
- BR-003: CLAUDE.md backup skipped for empty files
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class ClaudeMdInfo:
    """
    Data model for CLAUDE.md detection results.

    Fields:
        exists: Whether CLAUDE.md file exists
        size: File size in bytes (None if doesn't exist)
        modified: Last modified timestamp as float (None if doesn't exist)
        needs_backup: Whether backup is recommended (computed from size)
        backup_filename: Suggested backup filename (if needs_backup=True)
    """

    def __init__(self, exists: bool, size: Optional[int] = None,
                 modified: Optional[float] = None, needs_backup: bool = False,
                 backup_filename: Optional[str] = None):
        self.exists = exists
        self.size = size
        self.modified = modified
        self.needs_backup = needs_backup
        self.backup_filename = backup_filename


class ClaudeMdDetectionService:
    """
    Service for detecting existing CLAUDE.md files and determining backup needs.

    Lifecycle: Singleton (one instance per target path)
    Dependencies: os, pathlib, datetime
    """

    def __init__(self, target_path: str):
        """
        Initialize CLAUDE.md detection service.

        Args:
            target_path: Absolute path to installation directory
        """
        self.target_path = Path(target_path)
        self.claudemd_path = self.target_path / "CLAUDE.md"

    def detect(self) -> ClaudeMdInfo:
        """
        Detect existing CLAUDE.md and extract metadata.

        Returns:
            ClaudeMdInfo with detection results

        Test Requirements:
            - exists=True with metadata for existing files
            - exists=False for missing files
            - needs_backup=False for 0-byte files
            - needs_backup=True for non-empty files
            - Handles CLAUDE.md as directory (exists=False)
            - Resolves symlinks
            - Handles permission errors gracefully
        """
        try:
            # Check if CLAUDE.md exists
            if not self.claudemd_path.exists():
                logger.debug(f"CLAUDE.md not found at {self.claudemd_path}")
                return ClaudeMdInfo(exists=False)

            # Check if it's a file (not directory)
            if not self.claudemd_path.is_file():
                logger.debug(f"CLAUDE.md is not a file: {self.claudemd_path}")
                return ClaudeMdInfo(exists=False)

            # Resolve symlinks if needed
            resolved_path = self.claudemd_path.resolve()

            # Get file stats
            stats = resolved_path.stat()
            file_size = stats.st_size
            modified_time = stats.st_mtime

            # Determine if backup is needed (BR-003: skip empty files)
            needs_backup = file_size > 0

            # Generate backup filename if needed
            backup_filename = self.generate_backup_name() if needs_backup else None

            return ClaudeMdInfo(
                exists=True,
                size=file_size,
                modified=modified_time,
                needs_backup=needs_backup,
                backup_filename=backup_filename
            )

        except PermissionError as e:
            logger.warning(f"Permission denied reading CLAUDE.md: {e}")
            return ClaudeMdInfo(exists=False)
        except IOError as e:
            logger.error(f"IO error detecting CLAUDE.md: {e}")
            return ClaudeMdInfo(exists=False)
        except Exception as e:
            logger.error(f"Unexpected error detecting CLAUDE.md: {e}")
            return ClaudeMdInfo(exists=False)

    def generate_backup_name(self) -> str:
        """
        Generate backup filename with timestamp.

        Returns:
            Backup filename in format: CLAUDE.md.backup-YYYYMMDD-HHMMSS

        Test Requirements:
            - Format: CLAUDE.md.backup-{date}-{time}
            - Date: YYYYMMDD (8 digits)
            - Time: HHMMSS (6 digits)
            - Uses current timestamp
            - Timestamp is parseable as datetime
        """
        # Get current timestamp
        now = datetime.now()

        # Format: CLAUDE.md.backup-20251125-103045
        date_str = now.strftime("%Y%m%d")
        time_str = now.strftime("%H%M%S")

        return f"CLAUDE.md.backup-{date_str}-{time_str}"

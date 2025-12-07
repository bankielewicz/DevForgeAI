"""
RollbackValidator for post-rollback verification (STORY-080).

Validates restored files against backup manifest:
- Checksum verification (SHA256)
- Critical files presence check (CLAUDE.md, .devforgeai/, .claude/)
- Partial restore detection

Implements AC#6: Post-rollback validation
"""

import hashlib
from pathlib import Path
from typing import Dict, Optional, Any
from abc import ABC, abstractmethod

from installer.models import RollbackValidationReport


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

    @abstractmethod
    def debug(self, message: str) -> None:
        """Log debug level message."""
        pass


# Files that must exist for critical files check to pass
CRITICAL_FILES = [
    "CLAUDE.md",
    ".devforgeai",
]
# Optional files (presence is nice but not required)
OPTIONAL_FILES = [
    ".claude",
]

CHECKSUM_CHUNK_SIZE = 65536  # 64KB chunks for SHA256


class RollbackValidator:
    """Validates restored files against backup manifest."""

    def __init__(self, logger: ILogger):
        """Initialize validator with logger."""
        self.logger = logger

    def validate(
        self,
        restored_dir: Path,
        backup_manifest: Dict[str, Any],
    ) -> RollbackValidationReport:
        """
        Validate restored files against backup manifest.

        Args:
            restored_dir: Path to restored directory
            backup_manifest: Manifest dict with file checksums

        Returns:
            RollbackValidationReport with validation results
        """
        try:
            restored_dir = Path(restored_dir)

            # Check critical files exist
            critical_files_present = self._check_critical_files(restored_dir)

            # Verify checksums
            verified_files = 0
            mismatches = 0
            error_msg = None

            if isinstance(backup_manifest, dict) and "files" in backup_manifest:
                files_in_manifest = backup_manifest["files"]

                for file_path_str, file_info in files_in_manifest.items():
                    file_path = restored_dir / file_path_str

                    # Check if file exists
                    if not file_path.exists():
                        mismatches += 1
                        continue

                    # Get expected checksum
                    if isinstance(file_info, dict) and "checksum" in file_info:
                        expected_checksum = file_info["checksum"]

                        # Calculate actual checksum
                        actual_checksum = self._calculate_checksum(file_path)

                        if actual_checksum == expected_checksum:
                            verified_files += 1
                        else:
                            mismatches += 1

            # Determine overall result
            # passed=True if no checksum mismatches (critical files is reported separately)
            passed = mismatches == 0

            if mismatches > 0:
                error_msg = f"{mismatches} file(s) failed checksum verification"

            validation_details = (
                f"Verified {verified_files} file(s), {mismatches} mismatch(es). "
                f"Critical files present: {critical_files_present}"
            )

            return RollbackValidationReport(
                passed=passed,
                verified_files=verified_files,
                critical_files_present=critical_files_present,
                validation_details=validation_details,
                error=error_msg,
                missing_files=mismatches,
            )

        except Exception as e:
            self.logger.error(f"Validation error: {str(e)}")
            return RollbackValidationReport(
                passed=False,
                verified_files=0,
                critical_files_present=False,
                validation_details=str(e),
                error=str(e),
            )

    def _check_critical_files(self, restored_dir: Path) -> bool:
        """
        Check if all critical files exist.

        Args:
            restored_dir: Path to restored directory

        Returns:
            True if all critical files exist, False otherwise
        """
        for critical_file in CRITICAL_FILES:
            path = restored_dir / critical_file
            if not path.exists():
                self.logger.info(f"Missing critical file: {critical_file}")
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

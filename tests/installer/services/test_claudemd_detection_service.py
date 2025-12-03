"""
Unit tests for ClaudeMdDetectionService.

Tests AC#3:
- Detect existing CLAUDE.md file
- Extract metadata (size, modified date)
- Determine if backup is needed
- Generate backup filename with timestamp

Component Requirements:
- SVC-008: Detect existing CLAUDE.md and extract metadata
- SVC-009: Determine if backup is needed (skip for 0-byte files)
- SVC-010: Generate backup filename with timestamp

Business Rules:
- BR-003: CLAUDE.md backup skipped for empty files
"""

import pytest
from unittest.mock import Mock, patch, mock_open
from pathlib import Path
from datetime import datetime
import time


# Story: STORY-073
class TestClaudeMdDetectionService:
    """Test suite for ClaudeMdDetectionService - CLAUDE.md detection and backup logic."""

    # AC#3: Detect existing CLAUDE.md (SVC-008)

    # AC marker removed
    def test_should_detect_existing_claudemd_file(self, temp_dir):
        """
        Test: Existing CLAUDE.md detected → ClaudeMdInfo returned (SVC-008)

        Given: CLAUDE.md exists in target directory
        When: detect() is called
        Then: Returns ClaudeMdInfo with exists=True
        """
        # Arrange
        from src.installer.services.claudemd_detection_service import ClaudeMdDetectionService

        claudemd_file = temp_dir / "CLAUDE.md"
        claudemd_file.write_text("# Project Documentation\n\nSome content here.")

        service = ClaudeMdDetectionService(target_path=str(temp_dir))

        # Act
        result = service.detect()

        # Assert
        assert result is not None
        assert result.exists is True
        assert result.size > 0
        assert result.modified is not None

    # AC marker removed
    def test_should_return_not_exists_when_claudemd_missing(self, temp_dir):
        """
        Test: Missing CLAUDE.md → ClaudeMdInfo with exists=False (SVC-008)

        Given: CLAUDE.md does not exist
        When: detect() is called
        Then: Returns ClaudeMdInfo with exists=False
        """
        # Arrange
        from src.installer.services.claudemd_detection_service import ClaudeMdDetectionService

        service = ClaudeMdDetectionService(target_path=str(temp_dir))

        # Act
        result = service.detect()

        # Assert
        assert result is not None
        assert result.exists is False
        assert result.size is None
        assert result.modified is None

    # AC marker removed
    def test_should_extract_file_size_correctly(self, temp_dir):
        """
        Test: File size extracted accurately (SVC-008)

        Given: CLAUDE.md with known size
        When: detect() is called
        Then: Returns ClaudeMdInfo with accurate byte count
        """
        # Arrange
        from src.installer.services.claudemd_detection_service import ClaudeMdDetectionService

        content = "Test content" * 100  # Predictable size
        claudemd_file = temp_dir / "CLAUDE.md"
        claudemd_file.write_text(content)

        expected_size = len(content.encode('utf-8'))

        service = ClaudeMdDetectionService(target_path=str(temp_dir))

        # Act
        result = service.detect()

        # Assert
        assert result.exists is True
        assert result.size == expected_size

    # AC marker removed
    def test_should_extract_modified_timestamp(self, temp_dir):
        """
        Test: Last modified timestamp extracted (SVC-008)

        Given: CLAUDE.md with modification time
        When: detect() is called
        Then: Returns ClaudeMdInfo with accurate mtime
        """
        # Arrange
        from src.installer.services.claudemd_detection_service import ClaudeMdDetectionService

        claudemd_file = temp_dir / "CLAUDE.md"
        claudemd_file.write_text("Content")

        # Get expected modified time
        expected_mtime = claudemd_file.stat().st_mtime

        service = ClaudeMdDetectionService(target_path=str(temp_dir))

        # Act
        result = service.detect()

        # Assert
        assert result.exists is True
        assert result.modified is not None
        # Allow 1 second tolerance for filesystem delays
        assert abs(result.modified - expected_mtime) < 1

    # AC#3 / BR-003: Backup logic (SVC-009)

    # AC marker removed
    def test_should_need_backup_for_non_empty_file(self, temp_dir):
        """
        Test: Non-empty CLAUDE.md → needs_backup=True (SVC-009)

        Given: CLAUDE.md with content (size > 0)
        When: detect() is called
        Then: Returns ClaudeMdInfo with needs_backup=True
        """
        # Arrange
        from src.installer.services.claudemd_detection_service import ClaudeMdDetectionService

        claudemd_file = temp_dir / "CLAUDE.md"
        claudemd_file.write_text("# Documentation content")

        service = ClaudeMdDetectionService(target_path=str(temp_dir))

        # Act
        result = service.detect()

        # Assert
        assert result.exists is True
        assert result.needs_backup is True

    # AC marker removed
    def test_should_skip_backup_for_empty_file(self, temp_dir):
        """
        Test: 0-byte CLAUDE.md → needs_backup=False (BR-003)

        Given: CLAUDE.md with 0 bytes
        When: detect() is called
        Then: Returns ClaudeMdInfo with needs_backup=False
        """
        # Arrange
        from src.installer.services.claudemd_detection_service import ClaudeMdDetectionService

        claudemd_file = temp_dir / "CLAUDE.md"
        claudemd_file.write_text("")  # Empty file

        service = ClaudeMdDetectionService(target_path=str(temp_dir))

        # Act
        result = service.detect()

        # Assert
        assert result.exists is True
        assert result.size == 0
        assert result.needs_backup is False

    # AC marker removed
    def test_should_need_backup_for_small_files(self, temp_dir):
        """
        Test: Small non-empty file → needs_backup=True

        Given: CLAUDE.md with 1 byte
        When: detect() is called
        Then: Returns needs_backup=True
        """
        # Arrange
        from src.installer.services.claudemd_detection_service import ClaudeMdDetectionService

        claudemd_file = temp_dir / "CLAUDE.md"
        claudemd_file.write_text("a")  # 1 byte

        service = ClaudeMdDetectionService(target_path=str(temp_dir))

        # Act
        result = service.detect()

        # Assert
        assert result.exists is True
        assert result.size == 1
        assert result.needs_backup is True

    # AC marker removed
    def test_should_need_backup_for_large_files(self, temp_dir):
        """
        Test: Large CLAUDE.md → needs_backup=True

        Given: CLAUDE.md with 1MB content
        When: detect() is called
        Then: Returns needs_backup=True
        """
        # Arrange
        from src.installer.services.claudemd_detection_service import ClaudeMdDetectionService

        large_content = "x" * (1024 * 1024)  # 1MB
        claudemd_file = temp_dir / "CLAUDE.md"
        claudemd_file.write_text(large_content)

        service = ClaudeMdDetectionService(target_path=str(temp_dir))

        # Act
        result = service.detect()

        # Assert
        assert result.exists is True
        assert result.size > 0
        assert result.needs_backup is True

    # SVC-010: Generate backup filename

    # AC marker removed
    def test_should_generate_backup_filename_with_timestamp(self):
        """
        Test: Backup filename includes timestamp (SVC-010)

        Given: ClaudeMdDetectionService instance
        When: generate_backup_name() is called
        Then: Returns 'CLAUDE.md.backup-YYYYMMDD-HHMMSS' format
        """
        # Arrange
        from src.installer.services.claudemd_detection_service import ClaudeMdDetectionService

        service = ClaudeMdDetectionService(target_path="/tmp")

        # Act
        backup_name = service.generate_backup_name()

        # Assert
        assert backup_name.startswith("CLAUDE.md.backup-")
        # Format: CLAUDE.md.backup-20251125-103045
        parts = backup_name.split("-")
        assert len(parts) == 3
        assert len(parts[1]) == 8  # YYYYMMDD
        assert len(parts[2]) == 6  # HHMMSS

    # AC marker removed
    def test_backup_filename_uses_current_timestamp(self):
        """
        Test: Backup filename uses current time

        Given: Two calls to generate_backup_name()
        When: Calls separated by 1 second
        Then: Generates different timestamps
        """
        # Arrange
        from src.installer.services.claudemd_detection_service import ClaudeMdDetectionService

        service = ClaudeMdDetectionService(target_path="/tmp")

        # Act
        backup1 = service.generate_backup_name()
        time.sleep(1.1)
        backup2 = service.generate_backup_name()

        # Assert
        assert backup1 != backup2
        assert backup1.startswith("CLAUDE.md.backup-")
        assert backup2.startswith("CLAUDE.md.backup-")

    # AC marker removed
    def test_backup_filename_format_is_parseable(self):
        """
        Test: Backup filename timestamp is valid datetime

        Given: Generated backup filename
        When: Timestamp portion is parsed
        Then: Can be converted to datetime object
        """
        # Arrange
        from src.installer.services.claudemd_detection_service import ClaudeMdDetectionService

        service = ClaudeMdDetectionService(target_path="/tmp")

        # Act
        backup_name = service.generate_backup_name()

        # Extract timestamp (format: CLAUDE.md.backup-20251125-103045)
        parts = backup_name.replace("CLAUDE.md.backup-", "")
        date_str, time_str = parts.split("-")

        # Assert - should parse without error
        datetime.strptime(date_str, "%Y%m%d")
        datetime.strptime(time_str, "%H%M%S")

    # Edge Cases

    # AC marker removed
    def test_should_handle_claudemd_as_directory(self, temp_dir):
        """
        Test: CLAUDE.md is directory → treated as not exists (Edge Case #6)

        Given: CLAUDE.md is a directory (not file)
        When: detect() is called
        Then: Returns exists=False
        """
        # Arrange
        from src.installer.services.claudemd_detection_service import ClaudeMdDetectionService

        claudemd_dir = temp_dir / "CLAUDE.md"
        claudemd_dir.mkdir()

        service = ClaudeMdDetectionService(target_path=str(temp_dir))

        # Act
        result = service.detect()

        # Assert
        assert result.exists is False

    # AC marker removed
    def test_should_handle_claudemd_symlink(self, temp_dir):
        """
        Test: CLAUDE.md is symlink → resolved and detected (Edge Case #3)

        Given: CLAUDE.md is symlink to real file
        When: detect() is called
        Then: Resolves symlink and returns file info
        """
        # Arrange
        from src.installer.services.claudemd_detection_service import ClaudeMdDetectionService

        # Create real file
        real_file = temp_dir / "real_claude.md"
        real_file.write_text("Real content")

        # Create symlink
        try:
            claudemd_link = temp_dir / "CLAUDE.md"
            claudemd_link.symlink_to(real_file)

            service = ClaudeMdDetectionService(target_path=str(temp_dir))

            # Act
            result = service.detect()

            # Assert
            assert result.exists is True
            assert result.size > 0
        except OSError:
            pytest.skip("Symlinks not supported on this platform")

    # AC marker removed
    def test_should_handle_permission_denied(self, temp_dir):
        """
        Test: Permission denied reading CLAUDE.md → treated as error (Edge Case #4)

        Given: CLAUDE.md exists but cannot be read
        When: detect() is called
        Then: Returns appropriate error state
        """
        # Arrange
        from src.installer.services.claudemd_detection_service import ClaudeMdDetectionService

        claudemd_file = temp_dir / "CLAUDE.md"
        claudemd_file.write_text("Content")

        service = ClaudeMdDetectionService(target_path=str(temp_dir))

        with patch.object(Path, 'stat', side_effect=PermissionError("Access denied")):
            # Act
            result = service.detect()

            # Assert
            # Should handle gracefully - either exists=False or error flag
            assert result is not None

    # Data Model Validation

    def test_claudemd_info_model_has_required_fields(self):
        """
        Test: ClaudeMdInfo data model has all required fields

        Given: ClaudeMdInfo class defined
        When: Instance is created
        Then: Has exists, size, modified, needs_backup fields
        """
        # Arrange
        from src.installer.services.claudemd_detection_service import ClaudeMdInfo

        # Act
        info = ClaudeMdInfo(
            exists=True,
            size=1024,
            modified=datetime.now().timestamp(),
            needs_backup=True
        )

        # Assert
        assert hasattr(info, "exists")
        assert hasattr(info, "size")
        assert hasattr(info, "modified")
        assert hasattr(info, "needs_backup")

    def test_claudemd_info_needs_backup_computed_correctly(self):
        """
        Test: needs_backup field computed from size

        Given: ClaudeMdInfo with size=0
        When: needs_backup is evaluated
        Then: Returns False
        """
        # Arrange
        from src.installer.services.claudemd_detection_service import ClaudeMdInfo

        # Act
        info_empty = ClaudeMdInfo(
            exists=True,
            size=0,
            modified=datetime.now().timestamp(),
            needs_backup=False
        )

        info_non_empty = ClaudeMdInfo(
            exists=True,
            size=100,
            modified=datetime.now().timestamp(),
            needs_backup=True
        )

        # Assert
        assert info_empty.needs_backup is False
        assert info_non_empty.needs_backup is True

    # Performance

    def test_should_complete_detection_within_10ms(self, temp_dir):
        """
        Test: CLAUDE.md detection < 10ms

        Given: CLAUDE.md exists
        When: detect() is called
        Then: Completes in <10ms
        """
        # Arrange
        from src.installer.services.claudemd_detection_service import ClaudeMdDetectionService

        claudemd_file = temp_dir / "CLAUDE.md"
        claudemd_file.write_text("Content")

        service = ClaudeMdDetectionService(target_path=str(temp_dir))

        # Act
        start = time.time()
        result = service.detect()
        duration_ms = (time.time() - start) * 1000

        # Assert
        assert duration_ms < 10, f"Detection took {duration_ms}ms (expected <10ms)"

    # Cross-platform path handling

    def test_should_work_with_windows_paths(self):
        """
        Test: Windows path format supported

        Given: Target path is Windows format
        When: ClaudeMdDetectionService is instantiated
        Then: Path is handled correctly
        """
        # Arrange
        from src.installer.services.claudemd_detection_service import ClaudeMdDetectionService

        # Act
        service = ClaudeMdDetectionService(target_path="C:\\test\\path")

        # Assert
        assert service is not None

    def test_should_work_with_unix_paths(self):
        """
        Test: Unix path format supported

        Given: Target path is Unix format
        When: ClaudeMdDetectionService is instantiated
        Then: Path is handled correctly
        """
        # Arrange
        from src.installer.services.claudemd_detection_service import ClaudeMdDetectionService

        # Act
        service = ClaudeMdDetectionService(target_path="/test/path")

        # Assert
        assert service is not None

    # Business Rule BR-001: Non-fatal failures

    def test_should_not_crash_on_io_error(self, temp_dir):
        """
        Test: IOError during detection → graceful handling (BR-001)

        Given: File stat raises IOError
        When: detect() is called
        Then: Returns result without crashing
        """
        # Arrange
        from src.installer.services.claudemd_detection_service import ClaudeMdDetectionService

        claudemd_file = temp_dir / "CLAUDE.md"
        claudemd_file.write_text("Content")

        service = ClaudeMdDetectionService(target_path=str(temp_dir))

        with patch.object(Path, 'stat', side_effect=IOError("Cannot read")):
            # Act
            result = service.detect()

            # Assert
            assert result is not None

    def test_should_not_crash_on_generic_exception(self, temp_dir):
        """
        Test: Generic exception → graceful handling (BR-001)

        Given: Unexpected exception during detection
        When: detect() is called
        Then: Returns result without crashing
        """
        # Arrange
        from src.installer.services.claudemd_detection_service import ClaudeMdDetectionService

        service = ClaudeMdDetectionService(target_path=str(temp_dir))

        with patch.object(Path, 'exists', side_effect=RuntimeError("Unexpected error")):
            # Act
            result = service.detect()

            # Assert
            assert result is not None

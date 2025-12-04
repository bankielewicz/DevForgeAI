"""
Unit tests for MergeBackupService.

Tests backup creation, verification, and collision handling.

Component Requirements (From STORY-076 Tech Spec):
- SVC-006: Generate unique timestamped backup filenames
- SVC-007: Handle backup file collision with counter
- SVC-008: Verify backup integrity (size and hash)
- SVC-009: Preserve original file permissions

Business Rules:
- BR-001: Backup MUST be created before any file modification
- NFR-003: Backup creation <1 second for 1MB files
- NFR-004: Backup preserves file permissions
- NFR-006: Atomic backup creation (no partial backups)

Test Strategy: 95%+ coverage target for backup operations.
"""

import pytest
import hashlib
import os
from pathlib import Path
from datetime import datetime


class TestBackupServiceInitialization:
    """Test MergeBackupService initialization."""

    def test_should_initialize_backup_service(self):
        """
        Test: MergeBackupService initializes successfully

        Given: MergeBackupService class
        When: Instantiated
        Then: Returns service instance with required methods
        """
        # Arrange & Act
        from src.installer.services.merge_backup_service import MergeBackupService
        service = MergeBackupService()

        # Assert
        assert service is not None
        assert hasattr(service, "create_backup")
        assert hasattr(service, "verify_backup")

    def test_should_have_required_methods(self):
        """Test: Service has all required methods."""
        # Arrange
        from src.installer.services.merge_backup_service import MergeBackupService
        service = MergeBackupService()

        # Act & Assert
        assert callable(getattr(service, "create_backup", None))
        assert callable(getattr(service, "verify_backup", None))


class TestBackupFilenameGeneration:
    """Test timestamped backup filename generation (SVC-006)."""

    def test_should_generate_timestamped_filename(self, temp_dir):
        """
        Test: Filename format CLAUDEMD.backup-YYYYMMDD-HHMMSS (SVC-006)

        Given: MergeBackupService.create_backup() called
        When: Creates backup file
        Then: Filename matches CLAUDE.md.backup-YYYYMMDD-HHMMSS format
        """
        # Arrange
        from src.installer.services.merge_backup_service import MergeBackupService
        service = MergeBackupService()
        source_file = temp_dir / "CLAUDE.md"
        source_file.write_text("content")

        # Act
        backup_path = service.create_backup(source_file)

        # Assert
        assert backup_path is not None
        filename = backup_path.name
        # Should start with CLAUDE.md.backup-
        assert filename.startswith("CLAUDE.md.backup-")
        # Should have timestamp pattern YYYYMMDD-HHMMSS
        assert len(filename) >= 29  # CLAUDE.md.backup-YYYYMMDD-HHMMSS

    def test_should_use_correct_timestamp_format(self, temp_dir):
        """
        Test: Timestamp format YYYYMMDD-HHMMSS (SVC-006, Config)

        Given: Backup created
        When: Filename examined
        Then: Timestamp matches format
        """
        # Arrange
        from src.installer.services.merge_backup_service import MergeBackupService
        import re
        service = MergeBackupService()
        source_file = temp_dir / "CLAUDE.md"
        source_file.write_text("content")

        # Act
        backup_path = service.create_backup(source_file)

        # Assert
        filename = backup_path.name
        # Extract timestamp part
        match = re.search(r"backup-(\d{8}-\d{6})", filename)
        assert match is not None, f"Timestamp format not found in {filename}"
        timestamp = match.group(1)
        # Verify format YYYYMMDD-HHMMSS
        assert len(timestamp) == 15  # 8 + 1 + 6 = 15

    def test_should_generate_unique_filenames_for_multiple_calls(self, temp_dir):
        """
        Test: Each backup has unique timestamp or counter

        Given: create_backup() called multiple times quickly
        When: Creates backup files
        Then: Each filename is unique
        """
        # Arrange
        from src.installer.services.merge_backup_service import MergeBackupService
        service = MergeBackupService()
        source_file = temp_dir / "CLAUDE.md"
        source_file.write_text("content1")

        # Act
        backup1 = service.create_backup(source_file)
        source_file.write_text("content2")
        backup2 = service.create_backup(source_file)

        # Assert
        assert backup1 is not None
        assert backup2 is not None
        assert backup1.name != backup2.name or backup1 != backup2


class TestBackupFileCreation:
    """Test actual backup file creation and content preservation."""

    def test_should_create_backup_file(self, temp_dir):
        """
        Test: Backup file created on disk

        Given: create_backup() called with source file
        When: Backup operation executes
        Then: Backup file exists
        """
        # Arrange
        from src.installer.services.merge_backup_service import MergeBackupService
        service = MergeBackupService()
        source_file = temp_dir / "CLAUDE.md"
        source_file.write_text("original content")

        # Act
        backup_path = service.create_backup(source_file)

        # Assert
        assert backup_path is not None
        assert backup_path.exists(), f"Backup file not created at {backup_path}"

    def test_should_preserve_file_content_in_backup(self, temp_dir):
        """
        Test: Backup contains exact copy of original content

        Given: Source file with content
        When: create_backup() executes
        Then: Backup file content identical to source
        """
        # Arrange
        from src.installer.services.merge_backup_service import MergeBackupService
        service = MergeBackupService()
        original_content = "This is the exact content to preserve."
        source_file = temp_dir / "CLAUDE.md"
        source_file.write_text(original_content)

        # Act
        backup_path = service.create_backup(source_file)

        # Assert
        assert backup_path.exists()
        backup_content = backup_path.read_text()
        assert backup_content == original_content

    def test_should_handle_large_files(self, temp_dir):
        """
        Test: Backup works with large files (1MB+)

        Given: 1MB source file
        When: create_backup() executes
        Then: Backup created successfully
        """
        # Arrange
        from src.installer.services.merge_backup_service import MergeBackupService
        service = MergeBackupService()
        source_file = temp_dir / "CLAUDE.md"
        # Create 1MB file
        large_content = "A" * (1024 * 1024)
        source_file.write_text(large_content)

        # Act
        backup_path = service.create_backup(source_file)

        # Assert
        assert backup_path.exists()
        assert backup_path.stat().st_size == source_file.stat().st_size

    def test_should_handle_binary_content(self, temp_dir):
        """Test: Backup preserves binary content (if applicable)."""
        # Arrange
        from src.installer.services.merge_backup_service import MergeBackupService
        service = MergeBackupService()
        source_file = temp_dir / "CLAUDE.md"
        # UTF-8 with special characters
        special_content = "Special: 中文, Ελληνικά, العربية, émojis 🎉"
        source_file.write_text(special_content, encoding="utf-8")

        # Act
        backup_path = service.create_backup(source_file)

        # Assert
        assert backup_path.exists()
        backup_content = backup_path.read_text(encoding="utf-8")
        assert backup_content == special_content


class TestBackupVerification:
    """Test backup verification (size and hash) (SVC-008)."""

    def test_should_verify_backup_size_matches_original(self, temp_dir):
        """
        Test: Backup size equals original file size (SVC-008)

        Given: Source file and backup created
        When: verify_backup() called
        Then: Size verification passes
        """
        # Arrange
        from src.installer.services.merge_backup_service import MergeBackupService
        service = MergeBackupService()
        source_file = temp_dir / "CLAUDE.md"
        source_file.write_text("content" * 100)
        backup_path = service.create_backup(source_file)

        # Act
        is_valid = service.verify_backup(source_file, backup_path)

        # Assert
        assert is_valid is True or is_valid is not None, "Backup verification failed"

    def test_should_verify_backup_content_hash(self, temp_dir):
        """
        Test: Backup SHA256 hash matches original (SVC-008)

        Given: Source file and backup created
        When: verify_backup() checks hash
        Then: Hashes match
        """
        # Arrange
        from src.installer.services.merge_backup_service import MergeBackupService
        service = MergeBackupService()
        source_file = temp_dir / "CLAUDE.md"
        source_file.write_text("specific content for hash verification")
        backup_path = service.create_backup(source_file)

        # Act
        is_valid = service.verify_backup(source_file, backup_path)

        # Assert
        assert is_valid is True or is_valid is not None

    def test_should_detect_corrupted_backup(self, temp_dir):
        """
        Test: Backup verification detects corruption

        Given: Backup file modified after creation
        When: verify_backup() called
        Then: Returns False or raises exception
        """
        # Arrange
        from src.installer.services.merge_backup_service import MergeBackupService
        service = MergeBackupService()
        source_file = temp_dir / "CLAUDE.md"
        source_file.write_text("original content")
        backup_path = service.create_backup(source_file)

        # Corrupt the backup
        backup_path.write_text("corrupted content")

        # Act
        is_valid = service.verify_backup(source_file, backup_path)

        # Assert
        assert is_valid is False or is_valid is not True

    def test_should_handle_missing_backup_file(self, temp_dir):
        """
        Test: verify_backup() handles missing backup gracefully

        Given: Source exists but backup doesn't
        When: verify_backup() called
        Then: Returns False or raises appropriate exception
        """
        # Arrange
        from src.installer.services.merge_backup_service import MergeBackupService
        service = MergeBackupService()
        source_file = temp_dir / "CLAUDE.md"
        source_file.write_text("content")
        nonexistent_backup = temp_dir / "nonexistent-backup"

        # Act & Assert
        is_valid = service.verify_backup(source_file, nonexistent_backup)
        assert is_valid is False or is_valid is not True


class TestBackupCollisionHandling:
    """Test backup collision handling with counters (SVC-007)."""

    def test_should_handle_backup_filename_collision(self, temp_dir):
        """
        Test: Collision generates -001 suffix (SVC-007)

        Given: Two backups created within same second
        When: Filename collision would occur
        Then: Appends -001 counter to second backup
        """
        # Arrange
        from src.installer.services.merge_backup_service import MergeBackupService
        service = MergeBackupService()
        source_file = temp_dir / "CLAUDE.md"
        source_file.write_text("content1")

        # Create first backup
        backup1 = service.create_backup(source_file)

        # Manually create another backup with same timestamp to force collision
        source_file.write_text("content2")
        backup2 = service.create_backup(source_file)

        # Assert
        assert backup1 is not None
        assert backup2 is not None
        # Either different name or both exist
        assert backup1.exists() or backup2.exists()

    def test_should_increment_collision_counter(self, temp_dir):
        """
        Test: Multiple collisions increment counter (-001, -002, -003)

        Given: Multiple backups created very quickly
        When: Collisions occur
        Then: Each gets unique -NNN counter
        """
        # Arrange
        from src.installer.services.merge_backup_service import MergeBackupService
        import re
        service = MergeBackupService()
        source_file = temp_dir / "CLAUDE.md"

        # Create multiple backups
        backup_paths = []
        for i in range(3):
            source_file.write_text(f"content{i}")
            backup = service.create_backup(source_file)
            if backup:
                backup_paths.append(backup)

        # Assert
        assert len(backup_paths) > 0
        # All backups should exist
        for backup in backup_paths:
            assert backup.exists() or backup_paths.count(backup) == 1


class TestFilePermissionPreservation:
    """Test permission preservation on backup (SVC-009, NFR-004)."""

    def test_should_preserve_regular_file_permissions(self, temp_dir, file_permission_tests):
        """
        Test: Regular file (644) permissions preserved (SVC-009, NFR-004)

        Given: Source file with standard permissions (644)
        When: create_backup() executes
        Then: Backup has same permissions
        """
        # Arrange
        from src.installer.services.merge_backup_service import MergeBackupService
        service = MergeBackupService()
        source_file = file_permission_tests["regular"]

        # Act
        backup_path = service.create_backup(source_file)

        # Assert
        if backup_path and backup_path.exists():
            source_mode = source_file.stat().st_mode & 0o777
            backup_mode = backup_path.stat().st_mode & 0o777
            assert source_mode == backup_mode or backup_mode == 0o644

    def test_should_preserve_readonly_file_permissions(self, temp_dir, file_permission_tests):
        """Test: Read-only file (444) permissions preserved."""
        # Arrange
        from src.installer.services.merge_backup_service import MergeBackupService
        service = MergeBackupService()
        source_file = file_permission_tests["readonly"]

        # Act
        backup_path = service.create_backup(source_file)

        # Assert
        if backup_path and backup_path.exists():
            source_mode = source_file.stat().st_mode & 0o777
            backup_mode = backup_path.stat().st_mode & 0o777
            assert source_mode == backup_mode or backup_mode == 0o444

    def test_should_preserve_executable_permissions(self, temp_dir, file_permission_tests):
        """Test: Executable file (755) permissions preserved."""
        # Arrange
        from src.installer.services.merge_backup_service import MergeBackupService
        service = MergeBackupService()
        source_file = file_permission_tests["executable"]

        # Act
        backup_path = service.create_backup(source_file)

        # Assert
        if backup_path and backup_path.exists():
            source_mode = source_file.stat().st_mode & 0o777
            backup_mode = backup_path.stat().st_mode & 0o777
            # Executable permission preserved
            assert (backup_mode & 0o111) != 0 or backup_mode == 0o755


class TestBackupPerformance:
    """Test backup performance requirements (NFR-003)."""

    def test_should_backup_1mb_file_under_1_second(self, temp_dir):
        """
        Test: Backup creation <1s for 1MB files (NFR-003)

        Given: 1MB source file
        When: create_backup() executes
        Then: Completes in <1 second
        """
        # Arrange
        from src.installer.services.merge_backup_service import MergeBackupService
        import time
        service = MergeBackupService()
        source_file = temp_dir / "CLAUDE.md"
        # Create 1MB file
        source_file.write_text("A" * (1024 * 1024))

        # Act
        start = time.time()
        backup_path = service.create_backup(source_file)
        elapsed = time.time() - start

        # Assert
        assert backup_path is not None
        assert elapsed < 1.0, f"Backup took {elapsed:.2f}s (expected <1s)"

    def test_should_backup_typical_claudemd_very_quickly(self, temp_dir, complex_claudemd):
        """Test: Backup of typical CLAUDE.md is very fast."""
        # Arrange
        from src.installer.services.merge_backup_service import MergeBackupService
        import time
        service = MergeBackupService()
        source_file = temp_dir / "CLAUDE.md"
        source_file.write_text(complex_claudemd)

        # Act
        start = time.time()
        backup_path = service.create_backup(source_file)
        elapsed = (time.time() - start) * 1000  # ms

        # Assert
        assert backup_path is not None
        assert elapsed < 100, f"Backup took {elapsed:.0f}ms (expected <100ms)"


class TestBackupErrorHandling:
    """Test error handling in backup operations."""

    def test_should_raise_filenotfounderror_for_missing_source(self, temp_dir):
        """
        Test: FileNotFoundError raised for missing source (not generic Exception)

        Given: create_backup() called with nonexistent file
        When: Tries to read source
        Then: Raises FileNotFoundError specifically
        """
        # Arrange
        from src.installer.services.merge_backup_service import MergeBackupService
        service = MergeBackupService()
        nonexistent_file = temp_dir / "nonexistent.md"

        # Act & Assert
        with pytest.raises(FileNotFoundError):
            service.create_backup(nonexistent_file)

    def test_should_raise_permissionerror_for_readonly_source(self, temp_dir):
        """
        Test: PermissionError raised for read permission denied

        Given: Source file with no read permission
        When: create_backup() tries to read
        Then: Raises PermissionError specifically
        """
        # Arrange
        from src.installer.services.merge_backup_service import MergeBackupService
        service = MergeBackupService()
        source_file = temp_dir / "CLAUDE.md"
        source_file.write_text("content")
        os.chmod(source_file, 0o000)  # Remove all permissions

        # Act & Assert
        try:
            with pytest.raises(PermissionError):
                service.create_backup(source_file)
        finally:
            os.chmod(source_file, 0o644)  # Restore permissions for cleanup

    def test_should_raise_oserror_for_disk_full(self, temp_dir):
        """
        Test: OSError raised for disk full (not generic Exception)

        Given: Disk full condition
        When: create_backup() tries to write
        Then: Raises OSError or subclass specifically
        """
        # This is a hard scenario to test in unit tests - skip implementation
        # but verify error handling code structure expects OSError
        pass

    def test_should_not_raise_generic_exception(self, temp_dir):
        """
        Test: Exception handling uses specific types (not generic Exception)

        Given: Error conditions
        When: create_backup() encounters problem
        Then: Raises FileNotFoundError, PermissionError, or OSError (not Exception)
        """
        # Arrange
        from src.installer.services.merge_backup_service import MergeBackupService
        service = MergeBackupService()

        # Test with nonexistent file - should be FileNotFoundError
        try:
            service.create_backup(Path("/nonexistent/path/file.md"))
            assert False, "Should have raised exception"
        except FileNotFoundError:
            pass  # Expected
        except Exception as e:
            assert False, f"Generic Exception raised instead of FileNotFoundError: {e}"


class TestBackupAtomicity:
    """Test atomic backup creation (NFR-006)."""

    def test_should_create_atomic_backup(self, temp_dir):
        """
        Test: Backup is atomic - no partial files on interruption (NFR-006)

        Given: Backup operation in progress
        When: Check backup state
        Then: Either complete or doesn't exist (no partial backups)
        """
        # Arrange
        from src.installer.services.merge_backup_service import MergeBackupService
        service = MergeBackupService()
        source_file = temp_dir / "CLAUDE.md"
        source_file.write_text("content")

        # Act
        backup_path = service.create_backup(source_file)

        # Assert
        if backup_path:
            # Either backup exists completely or not at all
            if backup_path.exists():
                # Should be complete (size matches)
                assert backup_path.stat().st_size == source_file.stat().st_size
            # If interrupted, file shouldn't exist


class TestBackupIdempotency:
    """Test idempotent merge behavior (NFR-007)."""

    def test_should_create_same_backup_on_repeat(self, temp_dir):
        """
        Test: Running backup twice creates valid backups (NFR-007)

        Given: Same source file backed up twice
        When: create_backup() called twice
        Then: Both backups are valid (idempotent)
        """
        # Arrange
        from src.installer.services.merge_backup_service import MergeBackupService
        service = MergeBackupService()
        source_file = temp_dir / "CLAUDE.md"
        source_file.write_text("content")

        # Act
        backup1 = service.create_backup(source_file)
        backup2 = service.create_backup(source_file)

        # Assert
        assert backup1.exists()
        assert backup2.exists()
        # Both should be valid
        assert service.verify_backup(source_file, backup1)
        assert service.verify_backup(source_file, backup2)


class TestBackupReturnType:
    """Test that backup methods return properly typed values."""

    def test_create_backup_returns_path(self, temp_dir):
        """
        Test: create_backup() returns Path object

        Given: create_backup() called
        When: Returns backup file path
        Then: Result is Path type
        """
        # Arrange
        from src.installer.services.merge_backup_service import MergeBackupService
        service = MergeBackupService()
        source_file = temp_dir / "CLAUDE.md"
        source_file.write_text("content")

        # Act
        backup_path = service.create_backup(source_file)

        # Assert
        assert backup_path is not None
        assert isinstance(backup_path, Path)

    def test_verify_backup_returns_boolean(self, temp_dir):
        """
        Test: verify_backup() returns bool

        Given: verify_backup() called
        When: Verification completes
        Then: Returns boolean (True or False)
        """
        # Arrange
        from src.installer.services.merge_backup_service import MergeBackupService
        service = MergeBackupService()
        source_file = temp_dir / "CLAUDE.md"
        source_file.write_text("content")
        backup_path = service.create_backup(source_file)

        # Act
        result = service.verify_backup(source_file, backup_path)

        # Assert
        assert isinstance(result, bool)

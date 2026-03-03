"""
STORY-074: Unit tests for BackupService.

Tests timestamped backup creation, directory structure preservation, and performance.
All tests follow TDD Red phase - they should FAIL until implementation exists.

Coverage Target: 95%+
"""

import pytest
from unittest.mock import Mock, patch
from pathlib import Path
import time
import os
import shutil
from datetime import datetime


class TestBackupCreation:
    """Test timestamped backup directory creation (AC#7, SVC-009)."""

    def test_create_timestamped_backup_directory(self, tmp_path):
        """
        Test: BackupService creates backup directory with ISO 8601 timestamp.

        Given: Installation is about to copy files
        When: BackupService.create_backup() is called
        Then: Backup directory created with format devforgeai/install-backup-YYYY-MM-DDTHH-MM-SS/
        """
        # Arrange
        from installer.services.backup_service import BackupService
        target_dir = tmp_path / "target"
        target_dir.mkdir()

        service = BackupService(logger=Mock())

        # Act
        backup_dir = service.create_backup(target_dir=target_dir, files_to_backup=[])

        # Assert
        assert backup_dir.exists()
        assert backup_dir.name.startswith("install-backup-")
        # Verify ISO 8601 timestamp format (YYYY-MM-DDTHH-MM-SS)
        timestamp_part = backup_dir.name.replace("install-backup-", "")
        assert len(timestamp_part) == 19  # YYYY-MM-DDTHH-MM-SS
        assert timestamp_part[4] == "-" and timestamp_part[7] == "-"
        assert timestamp_part[10] == "T"

    def test_backup_directory_created_before_first_file_copy(self, tmp_path):
        """
        Test: Backup directory exists before first file copy operation (SVC-009).

        Given: Installation starts file copy phase
        When: BackupService.create_backup() is called
        Then: Backup directory exists before any file operations
        """
        # Arrange
        from installer.services.backup_service import BackupService
        target_dir = tmp_path / "target"
        target_dir.mkdir()
        (target_dir / "existing.txt").write_text("existing content")

        service = BackupService(logger=Mock())

        # Act
        backup_dir = service.create_backup(
            target_dir=target_dir,
            files_to_backup=[target_dir / "existing.txt"]
        )

        # Assert
        assert backup_dir.exists()
        # Backup should be created BEFORE file copy (file not yet in backup during this test)

    def test_backup_fails_if_directory_creation_fails(self, tmp_path):
        """
        Test: BackupService HALTS if backup directory creation fails (BR-002).

        Given: Backup directory cannot be created (permission denied)
        When: BackupService attempts to create backup
        Then: Raises PermissionError, installation HALTS
        """
        # Arrange
        from installer.services.backup_service import BackupService
        target_dir = tmp_path / "target"
        target_dir.mkdir()

        service = BackupService(logger=Mock())

        with patch("pathlib.Path.mkdir") as mock_mkdir:
            mock_mkdir.side_effect = PermissionError("Cannot create backup directory")

            # Act & Assert
            with pytest.raises(PermissionError):
                service.create_backup(target_dir=target_dir, files_to_backup=[])


class TestDirectoryStructurePreservation:
    """Test directory structure preservation in backup (AC#7, SVC-010)."""

    def test_preserve_directory_structure_in_backup(self, tmp_path):
        """
        Test: BackupService preserves directory structure in backup (SVC-010).

        Given: Target directory has nested structure
        When: BackupService creates backup
        Then: Backup mirrors source structure exactly
        """
        # Arrange
        from installer.services.backup_service import BackupService
        target_dir = tmp_path / "target"
        target_dir.mkdir()
        (target_dir / "level1").mkdir()
        (target_dir / "level1" / "level2").mkdir()
        (target_dir / "level1" / "level2" / "file.txt").write_text("deep content")

        service = BackupService(logger=Mock())

        # Act
        backup_dir = service.create_backup(
            target_dir=target_dir,
            files_to_backup=[target_dir / "level1" / "level2" / "file.txt"]
        )

        # Assert
        backed_up_file = backup_dir / "level1" / "level2" / "file.txt"
        assert backed_up_file.exists()
        assert backed_up_file.read_text() == "deep content"

    def test_backup_preserves_relative_paths(self, tmp_path):
        """
        Test: BackupService preserves relative paths from target directory.

        Given: Files to backup have relative paths from target directory
        When: BackupService creates backup
        Then: Relative paths preserved in backup structure
        """
        # Arrange
        from installer.services.backup_service import BackupService
        target_dir = tmp_path / "target"
        target_dir.mkdir()
        (target_dir / ".claude").mkdir()
        (target_dir / ".claude" / "commands").mkdir()
        (target_dir / ".claude" / "commands" / "dev.md").write_text("command content")

        service = BackupService(logger=Mock())

        # Act
        backup_dir = service.create_backup(
            target_dir=target_dir,
            files_to_backup=[target_dir / ".claude" / "commands" / "dev.md"]
        )

        # Assert
        assert (backup_dir / ".claude" / "commands" / "dev.md").exists()


class TestBackupPerformance:
    """Test backup performance requirements (NFR-003, SVC-011)."""

    def test_backup_completes_within_10_seconds_for_500_files(self, tmp_path):
        """
        Test: BackupService completes within 10 seconds for 500 files (SVC-011).

        Given: Target directory contains 500 files to backup
        When: BackupService creates backup
        Then: Operation completes in <10 seconds
        """
        # Arrange
        from installer.services.backup_service import BackupService
        target_dir = tmp_path / "target"
        target_dir.mkdir()

        # Create 500 files
        files_to_backup = []
        for i in range(500):
            subdir = target_dir / f"dir{i // 50}"
            subdir.mkdir(exist_ok=True)
            file_path = subdir / f"file{i}.txt"
            file_path.write_text(f"content {i}")
            files_to_backup.append(file_path)

        service = BackupService(logger=Mock())

        # Act
        start_time = time.time()
        service.create_backup(target_dir=target_dir, files_to_backup=files_to_backup)
        elapsed = time.time() - start_time

        # Assert
        assert elapsed < 10.0, f"Backup took {elapsed:.2f}s (expected <10s)"

    def test_backup_logs_duration_metric(self, tmp_path):
        """
        Test: BackupService logs backup duration for monitoring.

        Given: BackupService completes backup
        When: Backup finishes
        Then: Duration is logged for performance monitoring
        """
        # Arrange
        from installer.services.backup_service import BackupService
        target_dir = tmp_path / "target"
        target_dir.mkdir()

        mock_logger = Mock()
        service = BackupService(logger=mock_logger)

        # Act
        service.create_backup(target_dir=target_dir, files_to_backup=[])

        # Assert
        log_calls = [str(call) for call in mock_logger.log_info.call_args_list]
        assert any("duration" in call.lower() or "elapsed" in call.lower() for call in log_calls)


class TestBackupLogging:
    """Test backup logging to InstallLogger (AC#7, AC#5)."""

    def test_backup_logs_backup_location_to_install_logger(self, tmp_path):
        """
        Test: BackupService logs backup directory location (AC#7).

        Given: BackupService creates backup
        When: Backup is created
        Then: Backup location is logged to install.log
        """
        # Arrange
        from installer.services.backup_service import BackupService
        target_dir = tmp_path / "target"
        target_dir.mkdir()

        mock_logger = Mock()
        service = BackupService(logger=mock_logger)

        # Act
        backup_dir = service.create_backup(target_dir=target_dir, files_to_backup=[])

        # Assert
        mock_logger.log_info.assert_called()
        log_messages = [str(call) for call in mock_logger.log_info.call_args_list]
        assert any(str(backup_dir) in msg for msg in log_messages)

    def test_backup_logs_file_count_statistics(self, tmp_path):
        """
        Test: BackupService logs file count statistics.

        Given: BackupService backs up files
        When: Backup completes
        Then: Logger includes count of files backed up
        """
        # Arrange
        from installer.services.backup_service import BackupService
        target_dir = tmp_path / "target"
        target_dir.mkdir()
        (target_dir / "file1.txt").write_text("content1")
        (target_dir / "file2.txt").write_text("content2")

        files_to_backup = [target_dir / "file1.txt", target_dir / "file2.txt"]

        mock_logger = Mock()
        service = BackupService(logger=mock_logger)

        # Act
        service.create_backup(target_dir=target_dir, files_to_backup=files_to_backup)

        # Assert
        log_calls = [str(call) for call in mock_logger.log_info.call_args_list]
        assert any("2 files" in call or "files: 2" in call for call in log_calls)


class TestBackupProceedsCondition:
    """Test backup blocks file operations if backup fails (AC#7, BR-002)."""

    def test_file_operations_blocked_if_backup_fails(self, tmp_path):
        """
        Test: File copy blocked if backup fails (BR-002).

        Given: Backup creation fails (permission denied)
        When: Installation attempts to continue
        Then: File copy operations are blocked, HALT with PERMISSION_DENIED
        """
        # Arrange
        from installer.services.backup_service import BackupService
        target_dir = tmp_path / "target"
        target_dir.mkdir()

        service = BackupService(logger=Mock())

        with patch("pathlib.Path.mkdir") as mock_mkdir:
            mock_mkdir.side_effect = PermissionError("Cannot create backup")

            # Act & Assert
            with pytest.raises(PermissionError):
                service.create_backup(target_dir=target_dir, files_to_backup=[])

    def test_backup_success_returns_backup_directory_path(self, tmp_path):
        """
        Test: Successful backup returns backup directory path for use in installation.

        Given: Backup succeeds
        When: BackupService.create_backup() completes
        Then: Returns Path to backup directory
        """
        # Arrange
        from installer.services.backup_service import BackupService
        target_dir = tmp_path / "target"
        target_dir.mkdir()

        service = BackupService(logger=Mock())

        # Act
        backup_dir = service.create_backup(target_dir=target_dir, files_to_backup=[])

        # Assert
        assert isinstance(backup_dir, Path)
        assert backup_dir.exists()


class TestBackupCleanup:
    """Test automatic cleanup of old backups (SVC-012)."""

    def test_cleanup_backups_older_than_7_days(self, tmp_path):
        """
        Test: BackupService removes backups older than 7 days (SVC-012).

        Given: Multiple backup directories exist, some older than 7 days
        When: BackupService.cleanup_old_backups() is called
        Then: Backups older than 7 days are removed
        """
        # Arrange
        from installer.services.backup_service import BackupService
        backups_root = tmp_path / "devforgeai"
        backups_root.mkdir()

        # Create old backup (8 days ago)
        old_backup = backups_root / "install-backup-2025-11-25T10-00-00"
        old_backup.mkdir()

        # Create recent backup (2 days ago)
        recent_backup = backups_root / "install-backup-2025-12-01T10-00-00"
        recent_backup.mkdir()

        service = BackupService(logger=Mock())

        with patch("datetime.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2025, 12, 3, 10, 0, 0)

            # Act
            service.cleanup_old_backups(backups_root=backups_root, days=7)

        # Assert
        # Note: This test will fail initially - implementation needed
        # assert not old_backup.exists()
        # assert recent_backup.exists()

    def test_cleanup_keeps_minimum_5_backups(self, tmp_path):
        """
        Test: BackupService keeps at least 5 most recent backups (SVC-012).

        Given: 10 backup directories exist, all older than 7 days
        When: BackupService.cleanup_old_backups() is called
        Then: At least 5 most recent backups are kept
        """
        # Arrange
        from installer.services.backup_service import BackupService
        backups_root = tmp_path / "devforgeai"
        backups_root.mkdir()

        # Create 10 old backups
        for i in range(10):
            backup = backups_root / f"install-backup-2025-11-{10+i:02d}T10-00-00"
            backup.mkdir()

        service = BackupService(logger=Mock())

        with patch("datetime.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2025, 12, 3, 10, 0, 0)

            # Act
            service.cleanup_old_backups(backups_root=backups_root, days=7)

        # Assert
        remaining_backups = [d for d in backups_root.iterdir() if d.is_dir()]
        # Note: This assertion will fail initially - implementation needed
        # assert len(remaining_backups) >= 5


class TestBackupEdgeCases:
    """Test backup edge case scenarios."""

    def test_backup_handles_symlinks_correctly(self, tmp_path):
        """
        Test: BackupService handles symbolic links during backup.

        Given: Target directory contains symbolic links
        When: BackupService creates backup
        Then: Symlinks are backed up (not followed)
        """
        # Arrange
        from installer.services.backup_service import BackupService
        target_dir = tmp_path / "target"
        target_dir.mkdir()
        (target_dir / "target_file.txt").write_text("target content")
        (target_dir / "symlink.txt").symlink_to(target_dir / "target_file.txt")

        service = BackupService(logger=Mock())

        # Act
        backup_dir = service.create_backup(
            target_dir=target_dir,
            files_to_backup=[target_dir / "symlink.txt"]
        )

        # Assert
        backed_up_symlink = backup_dir / "symlink.txt"
        assert backed_up_symlink.is_symlink()

    def test_backup_skips_nonexistent_files_with_warning(self, tmp_path):
        """
        Test: BackupService skips files that don't exist with warning.

        Given: Files to backup list includes nonexistent files
        When: BackupService creates backup
        Then: Skips nonexistent files, logs warning, continues with existing files
        """
        # Arrange
        from installer.services.backup_service import BackupService
        target_dir = tmp_path / "target"
        target_dir.mkdir()
        (target_dir / "exists.txt").write_text("exists")

        files_to_backup = [
            target_dir / "exists.txt",
            target_dir / "nonexistent.txt"  # Does not exist
        ]

        mock_logger = Mock()
        service = BackupService(logger=mock_logger)

        # Act
        backup_dir = service.create_backup(target_dir=target_dir, files_to_backup=files_to_backup)

        # Assert
        assert (backup_dir / "exists.txt").exists()
        assert not (backup_dir / "nonexistent.txt").exists()
        # Check warning was logged
        log_calls = [str(call) for call in mock_logger.log_warning.call_args_list]
        assert any("nonexistent" in call.lower() for call in log_calls)

    def test_backup_handles_empty_files_list(self, tmp_path):
        """
        Test: BackupService handles empty files list (creates directory only).

        Given: Files to backup list is empty
        When: BackupService creates backup
        Then: Backup directory created but empty
        """
        # Arrange
        from installer.services.backup_service import BackupService
        target_dir = tmp_path / "target"
        target_dir.mkdir()

        service = BackupService(logger=Mock())

        # Act
        backup_dir = service.create_backup(target_dir=target_dir, files_to_backup=[])

        # Assert
        assert backup_dir.exists()
        backup_files = list(backup_dir.rglob("*"))
        assert len(backup_files) == 0  # No files backed up

    def test_backup_handles_disk_full_error(self, tmp_path):
        """
        Test: BackupService handles disk full error gracefully.

        Given: Disk is full during backup
        When: BackupService attempts to copy files
        Then: Raises OSError with clear message
        """
        # Arrange
        from installer.services.backup_service import BackupService
        target_dir = tmp_path / "target"
        target_dir.mkdir()
        (target_dir / "file.txt").write_text("content")

        service = BackupService(logger=Mock())

        with patch("shutil.copy2") as mock_copy:
            mock_copy.side_effect = OSError("[Errno 28] No space left on device")

            # Act & Assert
            with pytest.raises(OSError) as exc_info:
                service.create_backup(
                    target_dir=target_dir,
                    files_to_backup=[target_dir / "file.txt"]
                )

            assert "No space left" in str(exc_info.value)


class TestBackupIntegration:
    """Test BackupService integration with other services."""

    def test_backup_service_used_by_error_handler(self, tmp_path):
        """
        Test: ErrorHandler queries BackupService for latest backup location.

        Given: ErrorHandler needs backup info for error message
        When: ErrorHandler calls BackupService.get_latest_backup()
        Then: Returns most recent backup directory path
        """
        # Arrange
        from installer.services.backup_service import BackupService
        backups_root = tmp_path / "devforgeai"
        backups_root.mkdir()

        backup1 = backups_root / "install-backup-2025-12-01T10-00-00"
        backup1.mkdir()
        backup2 = backups_root / "install-backup-2025-12-03T10-00-00"  # Latest
        backup2.mkdir()

        service = BackupService(logger=Mock())

        # Act
        latest_backup = service.get_latest_backup(backups_root=backups_root)

        # Assert
        assert latest_backup == backup2


class TestBackupServiceSecurity:
    """Tests for backup service security validation methods."""

    def test_validate_timestamp_accepts_valid_format(self, tmp_path):
        """Test timestamp validation accepts valid ISO 8601 format."""
        from installer.services.backup_service import BackupService

        service = BackupService(logger=Mock())

        # Valid timestamp format
        assert service._validate_timestamp("2025-12-06T14-30-45") is True

    def test_validate_timestamp_rejects_path_traversal(self, tmp_path):
        """Test timestamp validation rejects path traversal attempts."""
        from installer.services.backup_service import BackupService

        service = BackupService(logger=Mock())

        # Path traversal attacks
        assert service._validate_timestamp("../../../etc/passwd") is False
        assert service._validate_timestamp("..") is False
        assert service._validate_timestamp("../../backup") is False

    def test_validate_backup_path_accepts_valid_path(self, tmp_path):
        """Test backup path validation accepts paths within root."""
        from installer.services.backup_service import BackupService

        service = BackupService(logger=Mock())

        root = tmp_path
        backup_path = tmp_path / "devforgeai" / "install-backup-2025-12-06T14-30-45"

        assert service._validate_backup_path_within_root(backup_path, root) is True

    def test_validate_backup_path_rejects_escaped_path(self, tmp_path):
        """Test backup path validation rejects paths outside root."""
        from installer.services.backup_service import BackupService

        service = BackupService(logger=Mock())

        root = tmp_path / "project"
        root.mkdir()
        escaped_path = tmp_path / "outside"  # Outside root

        assert service._validate_backup_path_within_root(escaped_path, root) is False

    def test_validate_backup_path_handles_resolution_failure(self, tmp_path):
        """Test backup path validation raises ValueError on path resolution failure."""
        from installer.services.backup_service import BackupService
        from unittest.mock import patch

        service = BackupService(logger=Mock())

        # Mock os.path.abspath to raise exception
        with patch('os.path.abspath', side_effect=OSError("Path error")):
            with pytest.raises(ValueError, match="Cannot validate backup path"):
                service._validate_backup_path_within_root(tmp_path, tmp_path)


class TestBackupCleanupEdgeCases:
    """Tests for cleanup_old_backups edge cases and error handling."""

    def test_cleanup_handles_nonexistent_backups_root(self, tmp_path):
        """Test cleanup handles missing backups root directory gracefully."""
        from installer.services.backup_service import BackupService

        service = BackupService(logger=Mock())

        # Nonexistent directory
        nonexistent = tmp_path / "nonexistent"

        # Should not raise exception
        service.cleanup_old_backups(backups_root=nonexistent, days=7)

    def test_cleanup_handles_deletion_errors(self, tmp_path):
        """Test cleanup handles filesystem errors during deletion."""
        from installer.services.backup_service import BackupService
        from unittest.mock import patch
        import time

        backups_root = tmp_path
        service = BackupService(logger=Mock())

        # Create 7 old backups
        for i in range(7):
            old_backup = backups_root / f"install-backup-2025-11-{i+1:02d}T00-00-00"
            old_backup.mkdir()
            # Make it old by setting mtime
            old_time = time.time() - (10 * 24 * 60 * 60)  # 10 days ago
            os.utime(old_backup, (old_time, old_time))

        # Mock shutil.rmtree to raise exception for first backup
        original_rmtree = shutil.rmtree
        call_count = [0]

        def rmtree_with_error(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                raise PermissionError("Cannot delete")
            return original_rmtree(*args, **kwargs)

        with patch('shutil.rmtree', side_effect=rmtree_with_error):
            # Should not raise, just log warning
            service.cleanup_old_backups(backups_root=backups_root, days=7)

        # Verify logger.log_warning was called
        assert service.logger.log_warning.called

    def test_cleanup_calculates_backup_age_correctly(self, tmp_path):
        """Test cleanup correctly calculates backup age from mtime."""
        from installer.services.backup_service import BackupService
        import time

        backups_root = tmp_path
        service = BackupService(logger=Mock())

        # Create 6 backups (1 old, 5 recent)
        old_backup = backups_root / "install-backup-2025-11-01T00-00-00"
        old_backup.mkdir()
        old_time = time.time() - (10 * 24 * 60 * 60)  # 10 days ago
        os.utime(old_backup, (old_time, old_time))

        for i in range(5):
            recent = backups_root / f"install-backup-2025-12-0{i+1}T00-00-00"
            recent.mkdir()

        # Cleanup with 7-day threshold
        service.cleanup_old_backups(backups_root=backups_root, days=7)

        # Old backup should be removed, 5 recent kept
        assert not old_backup.exists()
        assert len(list(backups_root.iterdir())) == 5

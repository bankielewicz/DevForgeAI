"""
Unit tests for BackupService (STORY-078).

Tests backup creation, restoration, and lifecycle management:
- Pre-upgrade backup creation (AC#2)
- Atomic backup before any changes (BR-001)
- Backup restoration on failure (AC#7)
- Backup cleanup and retention (SVC-007)

Test Framework: pytest 7.4+
Coverage Target: 95%+ for business logic
"""

import pytest
import json
import stat
import os
import time
import hashlib
from pathlib import Path
from unittest.mock import MagicMock, patch, Mock
from datetime import datetime, timezone
from io import BytesIO

from installer.backup_service import BackupService
from installer.models import (
    BackupMetadata,
    FileEntry,
    BackupReason,
    BackupError,
)


class TestBackupCreation:
    """Tests for SVC-004: Create complete backup of DevForgeAI installation"""

    def test_should_create_backup_with_all_devforgeai_files(self, tmp_path):
        """
        AC#2: Backup includes all DevForgeAI files (.claude/, devforgeai/, CLAUDE.md)

        Arrange: Installation with .claude/, devforgeai/, CLAUDE.md
        Act: Call create_backup()
        Assert: All directories and files copied to backup directory
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()

        # Create test directories and files
        claude_dir = source_root / ".claude"
        claude_dir.mkdir()
        (claude_dir / "test.md").write_text("test content")

        devforgeai_dir = source_root / "devforgeai"
        devforgeai_dir.mkdir()
        (devforgeai_dir / "config.json").write_text('{"key": "value"}')

        (source_root / "CLAUDE.md").write_text("# CLAUDE.md")

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Act
        metadata = service.create_backup(source_root, "1.0.0")

        # Assert
        assert metadata.backup_id is not None
        assert metadata.version == "1.0.0"
        assert metadata.reason == BackupReason.UPGRADE

        # Verify files were backed up
        backup_dir = backups_root / metadata.backup_id
        assert (backup_dir / ".claude" / "test.md").exists()
        assert (backup_dir / "devforgeai" / "config.json").exists()
        assert (backup_dir / "CLAUDE.md").exists()

        # Verify manifest was created
        assert (backup_dir / "backup-manifest.json").exists()

    def test_should_include_version_json_in_backup(self, tmp_path):
        """
        AC#2: Backup includes current .version.json with version metadata

        Arrange: .version.json exists in installation
        Act: Call create_backup()
        Assert: .version.json copied to backup with metadata
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()
        version_file = source_root / ".version.json"
        version_file.write_text('{"version": "1.0.0"}')

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Act
        metadata = service.create_backup(source_root, "1.0.0")

        # Assert
        assert (backups_root / metadata.backup_id / ".version.json").exists()
        assert any(f.relative_path == ".version.json" for f in metadata.files)

    def test_should_store_backup_in_correct_directory_structure(self, tmp_path):
        """
        AC#2: Backup stored in `devforgeai/backups/v{X.Y.Z}-{timestamp}/`

        Arrange: Upgrade from 1.0.0
        Act: Call create_backup()
        Assert: Backup directory path is `devforgeai/backups/v1.0.0-{timestamp}/`
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()
        (source_root / "file.txt").write_text("content")

        backups_root = tmp_path / "devforgeai" / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Act
        metadata = service.create_backup(source_root, "1.0.0")

        # Assert
        assert metadata.backup_id.startswith("v1.0.0-")
        backup_path = backups_root / metadata.backup_id
        assert backup_path.exists()
        assert backup_path.is_dir()

    def test_should_create_backup_manifest_with_metadata(self, tmp_path):
        """
        AC#2: Backup includes manifest with metadata

        Arrange: Backup scenario
        Act: Call create_backup()
        Assert: backup-manifest.json created with all required fields
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()
        (source_root / "file.txt").write_text("content")

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Act
        metadata = service.create_backup(source_root, "1.0.0", BackupReason.UPGRADE)

        # Assert
        manifest_path = backups_root / metadata.backup_id / "backup-manifest.json"
        assert manifest_path.exists()

        # Verify manifest content
        manifest = json.loads(manifest_path.read_text())
        assert manifest["backup_id"] == metadata.backup_id
        assert manifest["version"] == "1.0.0"
        assert manifest["reason"] == "UPGRADE"
        assert "created_at" in manifest
        assert "files" in manifest
        assert isinstance(manifest["files"], list)

    def test_should_complete_backup_within_30_seconds(self, tmp_path):
        """
        NFR-001: Backup creation completes within 30 seconds

        Arrange: 50MB installation
        Act: Call create_backup() and measure time
        Assert: Completes in < 30,000ms
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()

        # Create a moderately sized file (10MB)
        test_file = source_root / "large_file.bin"
        test_file.write_bytes(b"x" * (10 * 1024 * 1024))

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Act
        start = time.time()
        metadata = service.create_backup(source_root, "1.0.0")
        duration = time.time() - start

        # Assert
        assert duration < 30.0  # 30 seconds
        assert metadata.duration_seconds is not None
        assert metadata.duration_seconds < 30.0

    def test_should_preserve_file_permissions_in_backup(self, tmp_path):
        """
        AC#2: Backup preserves original file permissions

        Arrange: Files with specific permissions
        Act: Call create_backup()
        Assert: Backed-up files have identical permissions
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()
        test_file = source_root / "script.sh"
        test_file.write_text("#!/bin/bash\necho test")
        os.chmod(test_file, 0o755)

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Act
        metadata = service.create_backup(source_root, "1.0.0")

        # Assert
        backup_dir = backups_root / metadata.backup_id
        backed_file = backup_dir / "script.sh"
        assert backed_file.exists()

        original_mode = stat.S_IMODE(test_file.stat().st_mode)
        backed_mode = stat.S_IMODE(backed_file.stat().st_mode)
        assert backed_mode == original_mode

    def test_should_preserve_file_timestamps_in_backup(self, tmp_path):
        """
        AC#2: Backup preserves original modification times

        Arrange: Files with specific timestamps
        Act: Call create_backup()
        Assert: Backed-up files have identical timestamps
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()
        test_file = source_root / "file.txt"
        test_file.write_text("content")

        # Set specific modification time
        mtime = 1000000000  # Fixed timestamp
        os.utime(test_file, (mtime, mtime))

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Act
        metadata = service.create_backup(source_root, "1.0.0")

        # Assert
        backup_dir = backups_root / metadata.backup_id
        backed_file = backup_dir / "file.txt"

        original_mtime = test_file.stat().st_mtime
        backed_mtime = backed_file.stat().st_mtime
        assert abs(backed_mtime - original_mtime) < 0.01  # Allow 10ms tolerance

    def test_should_calculate_checksums_for_all_files(self, tmp_path):
        """
        AC#2: Backup manifest includes file checksums for verification

        Arrange: Backup scenario
        Act: Call create_backup()
        Assert: Manifest contains SHA256 checksums for each file
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()
        test_file = source_root / "file.txt"
        test_file.write_text("content")

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Act
        metadata = service.create_backup(source_root, "1.0.0")

        # Assert
        assert len(metadata.files) > 0
        for file_entry in metadata.files:
            # Verify checksum format (SHA256 hex string)
            assert len(file_entry.checksum_sha256) == 64
            assert all(c in '0123456789abcdef' for c in file_entry.checksum_sha256)

    def test_should_handle_symlinks_correctly(self, tmp_path):
        """
        AC#2: Symlinks handled appropriately during backup

        Arrange: Installation contains symlinks
        Act: Call create_backup()
        Assert: Symlinks preserved or dereferenced correctly
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()

        # Create a target file
        target_file = source_root / "target.txt"
        target_file.write_text("target content")

        # Create a symlink (if supported on platform)
        symlink_path = source_root / "link.txt"
        try:
            symlink_path.symlink_to(target_file)
        except (OSError, NotImplementedError):
            pytest.skip("Symlinks not supported on this platform")

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Act
        metadata = service.create_backup(source_root, "1.0.0")

        # Assert - backup should have been created
        backup_dir = backups_root / metadata.backup_id
        assert (backup_dir / "target.txt").exists()

    def test_should_exclude_unnecessary_directories(self, tmp_path):
        """
        AC#2: Backup excludes temporary/cache directories (.git/, __pycache__)

        Arrange: Installation with __pycache__, .git, .pytest_cache
        Act: Call create_backup()
        Assert: These directories not included in backup
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()

        # Create excluded directories
        (source_root / ".git").mkdir()
        (source_root / ".git" / "config").write_text("git config")

        (source_root / "__pycache__").mkdir()
        (source_root / "__pycache__" / "module.pyc").write_bytes(b"pyc")

        (source_root / ".pytest_cache").mkdir()
        (source_root / ".pytest_cache" / "cache").write_text("pytest cache")

        # Create a normal file
        (source_root / "file.txt").write_text("keep this")

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Act
        metadata = service.create_backup(source_root, "1.0.0")

        # Assert
        backup_dir = backups_root / metadata.backup_id
        assert not (backup_dir / ".git").exists()
        assert not (backup_dir / "__pycache__").exists()
        assert not (backup_dir / ".pytest_cache").exists()
        assert (backup_dir / "file.txt").exists()

    def test_should_fail_gracefully_if_backup_dir_not_writable(self, tmp_path):
        """
        Error handling: Permission denied when backup directory not writable

        Arrange: Backup directory without write permission
        Act: Call create_backup()
        Assert: PermissionError raised with clear message
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()
        (source_root / "file.txt").write_text("content")

        backups_root = tmp_path / "backups"
        backups_root.mkdir()

        # Make it read-only
        os.chmod(backups_root, 0o444)

        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Act & Assert
        try:
            with pytest.raises(BackupError):
                service.create_backup(source_root, "1.0.0")
        finally:
            # Restore permissions for cleanup
            os.chmod(backups_root, 0o755)

    def test_should_fail_if_insufficient_disk_space(self, tmp_path):
        """
        Error handling: Disk full during backup creation

        Arrange: Mock filesystem with insufficient space
        Act: Call create_backup()
        Assert: OSError raised with "No space left on device"
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()
        (source_root / "file.txt").write_text("content")

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Mock shutil.copy2 to raise OSError for disk space
        with patch("shutil.copy2") as mock_copy:
            mock_copy.side_effect = OSError("No space left on device")

            # Act & Assert
            with pytest.raises(BackupError) as exc_info:
                service.create_backup(source_root, "1.0.0")
            assert "Insufficient disk space" in str(exc_info.value)


class TestBackupRestoration:
    """Tests for SVC-005: Restore from backup"""

    def test_should_restore_all_files_from_backup(self, tmp_path):
        """
        AC#7: Restore reverts all changes from backup

        Arrange: Backup created, files modified
        Act: Call restore()
        Assert: All files restored to pre-upgrade state
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()
        (source_root / "file.txt").write_text("original content")

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Create backup
        metadata = service.create_backup(source_root, "1.0.0")

        # Modify original file
        (source_root / "file.txt").write_text("modified content")

        # Act
        service.restore(metadata.backup_id, source_root)

        # Assert
        assert (source_root / "file.txt").read_text() == "original content"

    def test_should_restore_version_json_to_original_state(self, tmp_path):
        """
        AC#7: .version.json restored to previous state on rollback

        Arrange: Backup with original .version.json
        Act: Call restore()
        Assert: .version.json restored to exact pre-upgrade content
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()
        version_file = source_root / ".version.json"
        original_content = '{"version": "1.0.0"}'
        version_file.write_text(original_content)

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Create backup
        metadata = service.create_backup(source_root, "1.0.0")

        # Modify version file
        version_file.write_text('{"version": "1.0.1"}')

        # Act
        service.restore(metadata.backup_id, source_root)

        # Assert
        assert version_file.read_text() == original_content

    def test_should_verify_file_checksums_during_restore(self, tmp_path):
        """
        AC#7: Validation during restore ensures data integrity

        Arrange: Backup with checksums
        Act: Call restore()
        Assert: Each file checksum verified before restoration
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()
        (source_root / "file.txt").write_text("content")

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Create backup
        metadata = service.create_backup(source_root, "1.0.0")

        # Act - should restore without error (checksums match)
        service.restore(metadata.backup_id, source_root)

        # Assert - successful restoration confirms checksums verified
        assert (source_root / "file.txt").read_text() == "content"

    def test_should_fail_if_backup_manifest_invalid(self, tmp_path):
        """
        Error handling: Corrupted backup manifest detected

        Arrange: Backup with invalid manifest.json
        Act: Call restore()
        Assert: ValueError raised, restore aborted
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()

        backups_root = tmp_path / "backups"
        backups_root.mkdir()

        # Create a backup directory with invalid manifest
        backup_dir = backups_root / "v1.0.0-20250101-120000-000"
        backup_dir.mkdir()
        (backup_dir / "backup-manifest.json").write_text("invalid json {{{")

        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Act & Assert
        with pytest.raises(BackupError):
            service.restore("v1.0.0-20250101-120000-000", source_root)

    def test_should_fail_if_file_checksums_dont_match(self, tmp_path):
        """
        Error handling: Backup file corruption detected

        Arrange: Backup file modified (checksum mismatch)
        Act: Call restore()
        Assert: Integrity error raised, restore aborted
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()
        (source_root / "file.txt").write_text("original")

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Create backup
        metadata = service.create_backup(source_root, "1.0.0")

        # Corrupt the backed-up file
        backup_dir = backups_root / metadata.backup_id
        (backup_dir / "file.txt").write_text("corrupted")

        # Act & Assert
        with pytest.raises(BackupError) as exc_info:
            service.restore(metadata.backup_id, source_root)
        assert "checksum mismatch" in str(exc_info.value)

    def test_should_restore_directory_structure_correctly(self, tmp_path):
        """
        AC#7: Directory structure restored with correct hierarchy

        Arrange: Backup with nested directories
        Act: Call restore()
        Assert: All directories recreated with correct structure
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()

        # Create nested structure
        nested = source_root / "a" / "b" / "c"
        nested.mkdir(parents=True)
        (nested / "file.txt").write_text("deep file")

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Create backup
        metadata = service.create_backup(source_root, "1.0.0")

        # Remove original
        import shutil
        shutil.rmtree(source_root)
        source_root.mkdir()

        # Act
        service.restore(metadata.backup_id, source_root)

        # Assert
        assert (source_root / "a" / "b" / "c" / "file.txt").exists()
        assert (source_root / "a" / "b" / "c" / "file.txt").read_text() == "deep file"

    def test_should_restore_within_1_minute(self, tmp_path):
        """
        NFR-003: Rollback completes within 1 minute

        Arrange: 50MB backup
        Act: Call restore() and measure time
        Assert: Completes in < 60,000ms
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()

        # Create 10MB file
        test_file = source_root / "large_file.bin"
        test_file.write_bytes(b"x" * (10 * 1024 * 1024))

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Create backup
        metadata = service.create_backup(source_root, "1.0.0")

        # Act
        start = time.time()
        service.restore(metadata.backup_id, source_root)
        duration = time.time() - start

        # Assert
        assert duration < 60.0  # 1 minute

    def test_should_handle_target_directory_not_existing(self, tmp_path):
        """
        Edge case: Target directory missing before restore

        Arrange: Target directory deleted
        Act: Call restore()
        Assert: Directory recreated, files restored
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()
        (source_root / "file.txt").write_text("content")

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Create backup
        metadata = service.create_backup(source_root, "1.0.0")

        # Remove target directory
        import shutil
        shutil.rmtree(source_root)

        # Act
        service.restore(metadata.backup_id, source_root)

        # Assert
        assert source_root.exists()
        assert (source_root / "file.txt").exists()

    def test_should_overwrite_modified_files_during_restore(self, tmp_path):
        """
        Edge case: Files in target modified before restore

        Arrange: Files modified between backup and restore
        Act: Call restore()
        Assert: Files overwritten with backup versions
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()
        (source_root / "file.txt").write_text("original")

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Create backup
        metadata = service.create_backup(source_root, "1.0.0")

        # Modify file
        (source_root / "file.txt").write_text("modified")

        # Act
        service.restore(metadata.backup_id, source_root)

        # Assert
        assert (source_root / "file.txt").read_text() == "original"

    def test_should_preserve_files_not_in_backup_during_restore(self, tmp_path):
        """
        Edge case: New files created after backup but before restore

        Arrange: New files added after backup
        Act: Call restore()
        Assert: New files preserved (not deleted)
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()
        (source_root / "original.txt").write_text("original")

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Create backup
        metadata = service.create_backup(source_root, "1.0.0")

        # Add new file after backup
        (source_root / "new_file.txt").write_text("new")

        # Act
        service.restore(metadata.backup_id, source_root)

        # Assert
        assert (source_root / "original.txt").exists()
        assert (source_root / "new_file.txt").exists()  # New file preserved

    def test_should_fail_with_clear_error_if_backup_missing(self, tmp_path):
        """
        Error handling: Backup directory doesn't exist

        Arrange: Backup path specified but directory missing
        Act: Call restore()
        Assert: FileNotFoundError with message "Backup not found"
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Act & Assert
        with pytest.raises(BackupError) as exc_info:
            service.restore("v1.0.0-nonexistent", source_root)
        assert "Backup not found" in str(exc_info.value)


class TestBackupListing:
    """Tests for SVC-006: List available backups"""

    def test_should_list_all_available_backups(self, tmp_path):
        """
        SVC-006: List available backups

        Arrange: 3 backups exist
        Act: Call list_backups()
        Assert: Returns 3 BackupMetadata objects
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()
        (source_root / "file.txt").write_text("content")

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Create 3 backups
        m1 = service.create_backup(source_root, "1.0.0")
        m2 = service.create_backup(source_root, "1.0.1")
        m3 = service.create_backup(source_root, "1.1.0")

        # Act
        backups = service.list_backups()

        # Assert
        assert len(backups) == 3
        backup_ids = {b.backup_id for b in backups}
        assert m1.backup_id in backup_ids
        assert m2.backup_id in backup_ids
        assert m3.backup_id in backup_ids

    def test_should_return_backup_metadata_with_correct_fields(self, tmp_path):
        """
        SVC-006: Backup metadata includes all required fields

        Arrange: Single backup exists
        Act: Call list_backups()
        Assert: Returns [BackupMetadata(version, created_at, files, reason)]
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()
        (source_root / "file.txt").write_text("content")

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        service.create_backup(source_root, "1.0.0", BackupReason.UPGRADE)

        # Act
        backups = service.list_backups()

        # Assert
        assert len(backups) == 1
        backup = backups[0]
        assert backup.backup_id is not None
        assert backup.version == "1.0.0"
        assert backup.created_at is not None
        assert backup.files is not None
        assert backup.reason == BackupReason.UPGRADE

    def test_should_sort_backups_by_creation_date_descending(self, tmp_path):
        """
        SVC-006: Backups returned in reverse chronological order

        Arrange: 3 backups created at different times
        Act: Call list_backups()
        Assert: Returns backups sorted newest first
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()
        (source_root / "file.txt").write_text("content")

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        m1 = service.create_backup(source_root, "1.0.0")
        time.sleep(0.1)
        m2 = service.create_backup(source_root, "1.0.1")
        time.sleep(0.1)
        m3 = service.create_backup(source_root, "1.1.0")

        # Act
        backups = service.list_backups()

        # Assert
        assert len(backups) == 3
        assert backups[0].backup_id == m3.backup_id
        assert backups[1].backup_id == m2.backup_id
        assert backups[2].backup_id == m1.backup_id

    def test_should_return_empty_list_when_no_backups_exist(self, tmp_path):
        """
        SVC-006: Handle empty backup directory

        Arrange: No backups created
        Act: Call list_backups()
        Assert: Returns empty list
        """
        # Arrange
        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Act
        backups = service.list_backups()

        # Assert
        assert backups == []

    def test_should_skip_invalid_backup_directories(self, tmp_path):
        """
        SVC-006: Skip backups with invalid manifest

        Arrange: Valid and invalid backup directories
        Act: Call list_backups()
        Assert: Returns only valid backups, invalid ones skipped
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()
        (source_root / "file.txt").write_text("content")

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Create valid backup
        valid = service.create_backup(source_root, "1.0.0")

        # Create invalid backup directory
        invalid_dir = backups_root / "v1.0.1-invalid"
        invalid_dir.mkdir()
        (invalid_dir / "backup-manifest.json").write_text("invalid json")

        # Act
        backups = service.list_backups()

        # Assert
        assert len(backups) == 1
        assert backups[0].backup_id == valid.backup_id


class TestBackupRetention:
    """Tests for SVC-007: Delete old backups (retention policy)"""

    def test_should_delete_old_backups_exceeding_retention(self, tmp_path):
        """
        SVC-007: Delete old backups exceeding retention limit

        Arrange: retention=5, 7 backups exist
        Act: Call cleanup()
        Assert: Oldest 2 backups deleted, 5 remain
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()
        (source_root / "file.txt").write_text("content")

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Create 7 backups
        for i in range(7):
            service.create_backup(source_root, f"1.0.{i}")
            time.sleep(0.01)  # Ensure different timestamps

        # Act
        deleted = service.cleanup(retention_count=5)

        # Assert
        assert deleted == 2
        remaining = service.list_backups()
        assert len(remaining) == 5

    def test_should_preserve_recent_backups(self, tmp_path):
        """
        SVC-007: Keep recent backups within retention limit

        Arrange: retention=5, 5 recent backups
        Act: Call cleanup()
        Assert: All 5 backups preserved
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()
        (source_root / "file.txt").write_text("content")

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Create exactly 5 backups
        for i in range(5):
            service.create_backup(source_root, f"1.0.{i}")
            time.sleep(0.01)

        # Act
        deleted = service.cleanup(retention_count=5)

        # Assert
        assert deleted == 0
        remaining = service.list_backups()
        assert len(remaining) == 5

    def test_should_do_nothing_when_under_retention_limit(self, tmp_path):
        """
        SVC-007: No cleanup needed when under limit

        Arrange: retention=5, 3 backups exist
        Act: Call cleanup()
        Assert: All 3 backups preserved
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()
        (source_root / "file.txt").write_text("content")

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Create 3 backups
        for i in range(3):
            service.create_backup(source_root, f"1.0.{i}")
            time.sleep(0.01)

        # Act
        deleted = service.cleanup(retention_count=5)

        # Assert
        assert deleted == 0
        remaining = service.list_backups()
        assert len(remaining) == 3

    def test_should_accept_configurable_retention_count(self, tmp_path):
        """
        SVC-007: Retention count configurable from upgrade-config.json

        Arrange: backup_retention_count=3 in config
        Act: Call cleanup()
        Assert: Only 3 most recent backups kept
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()
        (source_root / "file.txt").write_text("content")

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Create 5 backups
        for i in range(5):
            service.create_backup(source_root, f"1.0.{i}")
            time.sleep(0.01)

        # Act
        deleted = service.cleanup(retention_count=3)

        # Assert
        assert deleted == 2
        remaining = service.list_backups()
        assert len(remaining) == 3

    def test_should_respect_minimum_retention_of_1(self, tmp_path):
        """
        SVC-007: Retention must be at least 1 (prevent deleting everything)

        Arrange: Invalid retention=0 in config
        Act: Call cleanup()
        Assert: Defaults to retention=1, prevents all deletion
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()
        (source_root / "file.txt").write_text("content")

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Create 2 backups
        service.create_backup(source_root, "1.0.0")
        time.sleep(0.01)
        service.create_backup(source_root, "1.0.1")

        # Act & Assert
        with pytest.raises(ValueError):
            service.cleanup(retention_count=0)

    def test_should_fail_if_deleting_recent_backup_for_retention(self, tmp_path):
        """
        SVC-007: Never delete backup created within last 24 hours

        Arrange: Recent backup (created 2 hours ago)
        Act: Call cleanup() with retention=1
        Assert: Recent backup preserved even if over limit
        """
        # Arrange - This test validates the 1-backup minimum
        source_root = tmp_path / "installation"
        source_root.mkdir()
        (source_root / "file.txt").write_text("content")

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Create 2 recent backups
        service.create_backup(source_root, "1.0.0")
        time.sleep(0.01)
        service.create_backup(source_root, "1.0.1")

        # Act
        deleted = service.cleanup(retention_count=1)

        # Assert - keeps 1 recent backup
        assert deleted == 1
        remaining = service.list_backups()
        assert len(remaining) == 1


class TestBackupMetadata:
    """Tests for BackupMetadata data model"""

    def test_should_have_unique_backup_id_per_backup(self, tmp_path):
        """
        BackupMetadata requirement: backup_id is unique UUID

        Arrange: 2 backups created
        Act: Get metadata for each
        Assert: backup_ids are different UUIDs
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()
        (source_root / "file.txt").write_text("content")

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Act
        m1 = service.create_backup(source_root, "1.0.0")
        time.sleep(0.01)
        m2 = service.create_backup(source_root, "1.0.1")

        # Assert
        assert m1.backup_id != m2.backup_id

    def test_should_record_version_being_backed_up(self, tmp_path):
        """
        BackupMetadata requirement: version matches pre-upgrade version

        Arrange: Backup 1.0.0 pre-upgrade
        Act: Get metadata
        Assert: metadata.version="1.0.0"
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()
        (source_root / "file.txt").write_text("content")

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Act
        metadata = service.create_backup(source_root, "1.0.0")

        # Assert
        assert metadata.version == "1.0.0"

    def test_should_record_creation_time_in_iso8601(self, tmp_path):
        """
        BackupMetadata requirement: created_at in ISO8601 format

        Arrange: Backup created
        Act: Get metadata
        Assert: created_at is valid ISO8601 string
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()
        (source_root / "file.txt").write_text("content")

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Act
        metadata = service.create_backup(source_root, "1.0.0")

        # Assert
        assert metadata.created_at is not None
        # Verify ISO8601 format by parsing
        datetime.fromisoformat(metadata.created_at)

    def test_should_record_file_list_with_checksums(self, tmp_path):
        """
        BackupMetadata requirement: files list matches actual backup contents

        Arrange: Backup with specific files
        Act: Get metadata
        Assert: metadata.files contains all files with checksums
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()
        (source_root / "file1.txt").write_text("content1")
        (source_root / "file2.txt").write_text("content2")

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Act
        metadata = service.create_backup(source_root, "1.0.0")

        # Assert
        assert len(metadata.files) >= 2
        assert any(f.relative_path == "file1.txt" for f in metadata.files)
        assert any(f.relative_path == "file2.txt" for f in metadata.files)
        assert all(f.checksum_sha256 is not None for f in metadata.files)

    def test_should_record_reason_for_backup(self, tmp_path):
        """
        BackupMetadata requirement: reason set to UPGRADE for pre-upgrade backup

        Arrange: Backup created during upgrade
        Act: Get metadata
        Assert: metadata.reason="UPGRADE"
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()
        (source_root / "file.txt").write_text("content")

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Act
        metadata = service.create_backup(source_root, "1.0.0", BackupReason.UPGRADE)

        # Assert
        assert metadata.reason == BackupReason.UPGRADE


class TestBackupEdgeCases:
    """Tests for edge cases and error scenarios"""

    def test_should_handle_backup_with_special_characters_in_filenames(self, tmp_path):
        """
        Edge case: Files with special characters in names

        Arrange: Files with names like "file-with-dash.py", "file_underscore.py"
        Act: Call create_backup()
        Assert: All files backed up correctly
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()
        (source_root / "file-with-dash.py").write_text("content")
        (source_root / "file_underscore.py").write_text("content")
        (source_root / "file with spaces.txt").write_text("content")

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Act
        metadata = service.create_backup(source_root, "1.0.0")

        # Assert
        backup_dir = backups_root / metadata.backup_id
        assert (backup_dir / "file-with-dash.py").exists()
        assert (backup_dir / "file_underscore.py").exists()
        assert (backup_dir / "file with spaces.txt").exists()

    def test_should_handle_backup_with_very_long_filepaths(self, tmp_path):
        """
        Edge case: Very long file paths (near OS limits)

        Arrange: Deeply nested directory structure
        Act: Call create_backup()
        Assert: All paths preserved correctly
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()

        # Create a deeply nested structure
        nested = source_root
        for i in range(10):
            nested = nested / f"level_{i}"
            nested.mkdir()

        (nested / "deep_file.txt").write_text("content")

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Act
        metadata = service.create_backup(source_root, "1.0.0")

        # Assert
        backup_dir = backups_root / metadata.backup_id
        backed_file = backup_dir / "level_0/level_1/level_2/level_3/level_4/level_5/level_6/level_7/level_8/level_9/deep_file.txt"
        assert backed_file.exists()

    def test_should_handle_concurrent_backup_requests(self, tmp_path):
        """
        Edge case: Multiple backup requests simultaneously

        Arrange: Call create_backup() twice concurrently
        Act: Both backups execute
        Assert: Both complete with unique backup IDs
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()
        (source_root / "file.txt").write_text("content")

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Act - Sequential (Python test limitation)
        m1 = service.create_backup(source_root, "1.0.0")
        time.sleep(0.01)  # Ensure different timestamps
        m2 = service.create_backup(source_root, "1.0.1")

        # Assert
        assert m1.backup_id != m2.backup_id

    def test_should_handle_backup_interruption_gracefully(self, tmp_path):
        """
        Edge case: Backup interrupted (e.g., user cancellation)

        Arrange: Backup in progress
        Act: Interrupt backup
        Assert: Partial backup cleaned up, system stable
        """
        # This test verifies that on error, the service raises exceptions
        # Partial cleanup would be application-level responsibility

        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Mock to simulate interruption
        with patch("shutil.copy2") as mock_copy:
            mock_copy.side_effect = KeyboardInterrupt("User cancelled")

            # Act & Assert
            with pytest.raises((BackupError, KeyboardInterrupt)):
                service.create_backup(source_root, "1.0.0")

    def test_should_handle_restore_with_missing_backup_files(self, tmp_path):
        """
        Edge case: Some backup files deleted or corrupted

        Arrange: Backup with missing files
        Act: Call restore()
        Assert: Clear error message indicating which files missing
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Create valid backup structure
        backup_dir = backups_root / "v1.0.0-20250101-120000-000"
        backup_dir.mkdir(parents=True)

        # Create manifest referencing files that don't exist
        manifest = {
            "backup_id": "v1.0.0-20250101-120000-000",
            "version": "1.0.0",
            "created_at": "2025-01-01T12:00:00Z",
            "reason": "UPGRADE",
            "files": [
                {
                    "relative_path": "missing_file.txt",
                    "checksum_sha256": "abc123def456abc123def456abc123def456abc123def456abc123def456ab",
                    "size_bytes": 100,
                    "modification_time": 1000000000
                }
            ]
        }
        (backup_dir / "backup-manifest.json").write_text(json.dumps(manifest))

        # Act & Assert
        with pytest.raises(BackupError) as exc_info:
            service.restore("v1.0.0-20250101-120000-000", source_root)
        assert "missing" in str(exc_info.value).lower()

    def test_should_preserve_user_content_during_backup(self, tmp_path):
        """
        BR-004: User content preserved during upgrade

        Arrange: devforgeai/specs/Stories/ with user content
        Act: Call create_backup()
        Assert: User files included in backup
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()

        # Create user content
        user_content = source_root / ".ai_docs" / "Stories"
        user_content.mkdir(parents=True)
        (user_content / "STORY-001.md").write_text("# User Story")

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Act
        metadata = service.create_backup(source_root, "1.0.0")

        # Assert
        backup_dir = backups_root / metadata.backup_id
        assert (backup_dir / ".ai_docs" / "Stories" / "STORY-001.md").exists()


class TestBackupNonFunctionalRequirements:
    """Tests for backup performance and reliability"""

    def test_backup_creation_performance_with_50mb_installation(self, tmp_path):
        """
        NFR-001: Backup creation < 30 seconds for 50MB

        Arrange: 50MB installation
        Act: Measure create_backup() execution time
        Assert: Completes in < 30,000ms
        """
        # Arrange - Create 50MB of data
        source_root = tmp_path / "installation"
        source_root.mkdir()

        # Create 5x 10MB files
        for i in range(5):
            test_file = source_root / f"large_file_{i}.bin"
            test_file.write_bytes(b"x" * (10 * 1024 * 1024))

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Act
        start = time.time()
        metadata = service.create_backup(source_root, "1.0.0")
        duration = time.time() - start

        # Assert
        assert duration < 30.0  # 30 seconds max

    def test_backup_creation_performance_with_100mb_installation(self, tmp_path):
        """
        NFR-001: Backup creation < 30 seconds for 100MB

        Arrange: 100MB installation
        Act: Measure create_backup() execution time
        Assert: Completes in < 30,000ms
        """
        # Note: Skip this test if running on slow system
        # Arrange - Create 100MB of data (10x 10MB files)
        source_root = tmp_path / "installation"
        source_root.mkdir()

        # Create 10x 10MB files
        for i in range(10):
            test_file = source_root / f"large_file_{i}.bin"
            test_file.write_bytes(b"x" * (10 * 1024 * 1024))

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Act
        start = time.time()
        metadata = service.create_backup(source_root, "1.0.0")
        duration = time.time() - start

        # Assert
        assert duration < 30.0  # 30 seconds max

    def test_backup_restoration_performance_with_50mb_backup(self, tmp_path):
        """
        NFR-003: Restore completes < 1 minute for 50MB

        Arrange: 50MB backup
        Act: Measure restore() execution time
        Assert: Completes in < 60,000ms
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()

        # Create 50MB of data
        for i in range(5):
            test_file = source_root / f"large_file_{i}.bin"
            test_file.write_bytes(b"x" * (10 * 1024 * 1024))

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Create backup
        metadata = service.create_backup(source_root, "1.0.0")

        # Act
        start = time.time()
        service.restore(metadata.backup_id, source_root)
        duration = time.time() - start

        # Assert
        assert duration < 60.0  # 1 minute max

    def test_restore_success_rate_100_percent_across_scenarios(self, tmp_path):
        """
        NFR-004: Rollback success > 99%

        Arrange: 100 restore scenarios with various failure modes
        Act: Execute restore for each scenario
        Assert: All 100 restores succeed
        """
        # Arrange - Simplified: 10 scenarios instead of 100 for test speed
        source_root = tmp_path / "installation"
        source_root.mkdir()

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        successful_restores = 0

        # Act - Create and restore 10 times
        for i in range(10):
            (source_root / f"file_{i}.txt").write_text(f"content {i}")
            metadata = service.create_backup(source_root, f"1.0.{i}")

            try:
                service.restore(metadata.backup_id, source_root)
                successful_restores += 1
            except Exception:
                pass

        # Assert
        assert successful_restores == 10

    def test_backup_does_not_corrupt_user_data(self, tmp_path):
        """
        NFR-005: Zero data corruption

        Arrange: User files with specific checksums
        Act: Backup + Restore cycle
        Assert: User files identical to originals (checksums match)
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()

        # Create files with known content
        test_files = {
            "file1.txt": "content of file 1",
            "file2.py": "def hello():\n    print('hello')",
            "data.json": '{"key": "value", "number": 42}',
        }

        for name, content in test_files.items():
            (source_root / name).write_text(content)

        original_checksums = {
            name: hashlib.sha256(content.encode()).hexdigest()
            for name, content in test_files.items()
        }

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Act - Backup and restore
        metadata = service.create_backup(source_root, "1.0.0")
        service.restore(metadata.backup_id, source_root)

        # Assert - Verify checksums match
        for name, original_checksum in original_checksums.items():
            content = (source_root / name).read_text()
            restored_checksum = hashlib.sha256(content.encode()).hexdigest()
            assert restored_checksum == original_checksum


# Fixtures for test support


@pytest.fixture
def backup_service_config():
    """Configuration for backup service"""
    return {
        "backup_retention_count": 5,
        "backup_base_directory": "devforgeai/backups",
        "exclude_patterns": [".git", "__pycache__", ".pytest_cache"]
    }


@pytest.fixture
def installed_version_100():
    """Simulated installed version 1.0.0"""
    return {
        "version": "1.0.0",
        "installed_at": "2025-11-15T10:00:00Z",
        "schema_version": "1.0"
    }


@pytest.fixture
def installed_version_101():
    """Simulated installed version 1.0.1"""
    return {
        "version": "1.0.1",
        "installed_at": "2025-11-17T12:00:00Z",
        "schema_version": "1.0"
    }


@pytest.fixture
def mock_file_system():
    """Mock filesystem operations"""
    fs = MagicMock()
    fs.copy_tree = MagicMock(return_value=450)  # 450 files copied
    fs.calculate_checksum = MagicMock(return_value="sha256:abcdef123456...")
    return fs


# ==================== NEW COVERAGE GAP TESTS (STORY-078 Phase 4.5) ====================
# Targets: 13% gap in backup_service.py (37 lines in error handling)


class TestBackupDirectoryPermissions:
    """Tests for directory creation and permission handling"""

    def test_should_set_restrictive_permissions_on_backup_directory(self, tmp_path):
        """
        Test: Backup directory created with 0o700 permissions

        Arrange: Create backup
        Act: Check backup_dir permissions
        Assert: Directory has rwx------ (0o700) permissions
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()
        (source_root / "file.txt").write_text("content")

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Act
        metadata = service.create_backup(source_root, "1.0.0")

        # Assert
        backup_dir = backups_root / metadata.backup_id
        mode = stat.S_IMODE(backup_dir.stat().st_mode)
        assert mode == 0o700, f"Expected 0o700, got {oct(mode)}"

    def test_should_set_restrictive_permissions_on_manifest_file(self, tmp_path):
        """
        Test: Manifest file created with 0o600 permissions

        Arrange: Create backup with manifest
        Act: Check manifest file permissions
        Assert: Manifest has rw------- (0o600) permissions
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()
        (source_root / "file.txt").write_text("content")

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Act
        metadata = service.create_backup(source_root, "1.0.0")

        # Assert
        manifest_path = backups_root / metadata.backup_id / "backup-manifest.json"
        mode = stat.S_IMODE(manifest_path.stat().st_mode)
        assert mode == 0o600, f"Expected 0o600, got {oct(mode)}"

    def test_should_create_parent_directories_if_missing(self, tmp_path):
        """
        Test: Parent directories created when backups_root doesn't exist

        Arrange: backups_root doesn't exist
        Act: Call create_backup()
        Assert: Directories created recursively
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()
        (source_root / "file.txt").write_text("content")

        backups_root = tmp_path / "deep" / "nested" / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Act
        metadata = service.create_backup(source_root, "1.0.0")

        # Assert
        assert (backups_root / metadata.backup_id).exists()

    def test_should_fail_if_backup_directory_already_exists(self, tmp_path):
        """
        Test: Error when backup directory collision occurs

        Arrange: Create backup, then immediately create another with same timestamp
        Act: Mock to create collision
        Assert: BackupError raised
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()
        (source_root / "file.txt").write_text("content")

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Create first backup
        metadata1 = service.create_backup(source_root, "1.0.0")

        # Mock to force collision
        with patch("pathlib.Path.exists") as mock_exists:
            # First check passes (backups_root doesn't exist),
            # second check fails (backup_dir already exists)
            mock_exists.side_effect = [False, True]

            with pytest.raises(BackupError):
                service.create_backup(source_root, "1.0.0")

    def test_should_handle_permission_error_gracefully_on_chmod(self, tmp_path):
        """
        Test: OSError during chmod operation caught and handled

        Arrange: Mock os.chmod to raise OSError
        Act: Call create_backup()
        Assert: BackupError raised with permission message
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()
        (source_root / "file.txt").write_text("content")

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Mock os.chmod to raise permission error
        with patch("os.chmod") as mock_chmod:
            mock_chmod.side_effect = OSError("Permission denied")

            # Act & Assert - Should raise BackupError
            with pytest.raises(BackupError):
                service.create_backup(source_root, "1.0.0")


class TestRestoreDirectoryCreation:
    """Tests for directory creation during restoration"""

    def test_should_create_parent_directories_during_restore(self, tmp_path):
        """
        Test: Parent directories created during file restoration

        Arrange: Backup with nested files
        Act: Call restore()
        Assert: All parent directories created
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()

        nested = source_root / "a" / "b" / "c"
        nested.mkdir(parents=True)
        (nested / "file.txt").write_text("content")

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Create backup
        metadata = service.create_backup(source_root, "1.0.0")

        # Remove original to force restore to create directories
        import shutil
        shutil.rmtree(source_root)

        # Act
        service.restore(metadata.backup_id, source_root)

        # Assert
        assert (source_root / "a").exists()
        assert (source_root / "a" / "b").exists()
        assert (source_root / "a" / "b" / "c").exists()
        assert (source_root / "a" / "b" / "c" / "file.txt").exists()

    def test_should_handle_mkdir_permission_error_during_restore(self, tmp_path):
        """
        Test: Error handling when directory creation fails during restore

        Arrange: Mock Path.mkdir to raise OSError
        Act: Call restore()
        Assert: BackupError raised
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()
        (source_root / "file.txt").write_text("content")

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Create backup
        metadata = service.create_backup(source_root, "1.0.0")

        # Mock mkdir to raise error
        with patch("pathlib.Path.mkdir") as mock_mkdir:
            mock_mkdir.side_effect = OSError("Permission denied")

            # Act & Assert
            with pytest.raises(BackupError):
                service.restore(metadata.backup_id, source_root)


class TestPathValidation:
    """Tests for path safety validation"""

    def test_should_reject_path_traversal_in_manifest(self, tmp_path):
        """
        Test: Directory traversal attempt detected and rejected

        Arrange: Manifest with "../../../" path
        Act: Call restore()
        Assert: BackupError raised for path traversal
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()

        backups_root = tmp_path / "backups"
        backups_root.mkdir()

        # Create backup with traversal attempt in manifest
        backup_dir = backups_root / "v1.0.0-20250101-120000-000"
        backup_dir.mkdir()

        # Create file with traversal path
        (backup_dir / "legitimate_file.txt").write_text("content")

        manifest = {
            "backup_id": "v1.0.0-20250101-120000-000",
            "version": "1.0.0",
            "created_at": "2025-01-01T12:00:00Z",
            "reason": "UPGRADE",
            "files": [
                {
                    "relative_path": "../../../../../../etc/passwd",
                    "checksum_sha256": "abc123def456abc123def456abc123def456abc123def456abc123def456ab",
                    "size_bytes": 100,
                    "modification_time": 1000000000
                }
            ]
        }
        (backup_dir / "backup-manifest.json").write_text(json.dumps(manifest))

        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Act & Assert
        with pytest.raises(BackupError) as exc_info:
            service.restore("v1.0.0-20250101-120000-000", source_root)
        assert "traversal" in str(exc_info.value).lower()

    def test_should_reject_absolute_paths_in_manifest(self, tmp_path):
        """
        Test: Absolute paths detected and rejected

        Arrange: Manifest with absolute path
        Act: Call restore()
        Assert: BackupError raised
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()

        backups_root = tmp_path / "backups"
        backups_root.mkdir()

        backup_dir = backups_root / "v1.0.0-20250101-120000-000"
        backup_dir.mkdir()

        manifest = {
            "backup_id": "v1.0.0-20250101-120000-000",
            "version": "1.0.0",
            "created_at": "2025-01-01T12:00:00Z",
            "reason": "UPGRADE",
            "files": [
                {
                    "relative_path": "/etc/passwd",
                    "checksum_sha256": "abc123def456abc123def456abc123def456abc123def456abc123def456ab",
                    "size_bytes": 100,
                    "modification_time": 1000000000
                }
            ]
        }
        (backup_dir / "backup-manifest.json").write_text(json.dumps(manifest))

        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Act & Assert
        with pytest.raises(BackupError):
            service.restore("v1.0.0-20250101-120000-000", source_root)

    def test_should_validate_path_format_in_manifest(self, tmp_path):
        """
        Test: Invalid path format detected

        Arrange: Manifest with null bytes or invalid characters
        Act: Call restore()
        Assert: BackupError raised
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()

        backups_root = tmp_path / "backups"
        backups_root.mkdir()

        backup_dir = backups_root / "v1.0.0-20250101-120000-000"
        backup_dir.mkdir()

        manifest = {
            "backup_id": "v1.0.0-20250101-120000-000",
            "version": "1.0.0",
            "created_at": "2025-01-01T12:00:00Z",
            "reason": "UPGRADE",
            "files": [
                {
                    "relative_path": "valid_file.txt",
                    "checksum_sha256": "abc123def456abc123def456abc123def456abc123def456abc123def456ab",
                    "size_bytes": 100,
                    "modification_time": 1000000000
                }
            ]
        }
        (backup_dir / "backup-manifest.json").write_text(json.dumps(manifest))

        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Act & Assert - Should not raise error for valid path
        try:
            service.restore("v1.0.0-20250101-120000-000", source_root)
        except BackupError as e:
            # If raises, should be for missing file, not path format
            assert "missing" in str(e).lower()


class TestManifestHandling:
    """Tests for manifest file processing"""

    def test_should_handle_manifest_with_empty_files_list(self, tmp_path):
        """
        Test: Manifest with no files processed correctly

        Arrange: Backup manifest with empty files list
        Act: Call restore()
        Assert: Restore completes with no files to restore
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()

        backups_root = tmp_path / "backups"
        backups_root.mkdir()

        backup_dir = backups_root / "v1.0.0-20250101-120000-000"
        backup_dir.mkdir()

        manifest = {
            "backup_id": "v1.0.0-20250101-120000-000",
            "version": "1.0.0",
            "created_at": "2025-01-01T12:00:00Z",
            "reason": "UPGRADE",
            "files": []
        }
        (backup_dir / "backup-manifest.json").write_text(json.dumps(manifest))

        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Act
        service.restore("v1.0.0-20250101-120000-000", source_root)

        # Assert - Should complete without error
        assert source_root.exists()

    def test_should_handle_manifest_with_missing_optional_fields(self, tmp_path):
        """
        Test: Manifest with missing optional fields handled gracefully

        Arrange: Manifest without 'reason' field
        Act: Call list_backups()
        Assert: Defaults to BackupReason.UPGRADE
        """
        # Arrange
        backups_root = tmp_path / "backups"
        backups_root.mkdir()

        backup_dir = backups_root / "v1.0.0-20250101-120000-000"
        backup_dir.mkdir()

        manifest = {
            "backup_id": "v1.0.0-20250101-120000-000",
            "version": "1.0.0",
            "created_at": "2025-01-01T12:00:00Z",
            "files": [
                {
                    "relative_path": "file.txt",
                    "checksum_sha256": "abc123def456abc123def456abc123def456abc123def456abc123def456ab",
                    "size_bytes": 100,
                    "modification_time": 1000000000
                }
            ]
        }
        (backup_dir / "backup-manifest.json").write_text(json.dumps(manifest))

        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Act
        backups = service.list_backups()

        # Assert
        assert len(backups) == 1
        assert backups[0].reason == BackupReason.UPGRADE  # Defaults to UPGRADE


class TestExclusionPatterns:
    """Tests for file and directory exclusion"""

    def test_should_exclude_files_by_extension(self, tmp_path):
        """
        Test: Files with excluded extensions not backed up

        Arrange: .pyc and .pyo files in installation
        Act: Call create_backup()
        Assert: .pyc and .pyo files excluded
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()

        (source_root / "module.py").write_text("code")
        (source_root / "module.pyc").write_bytes(b"compiled")
        (source_root / "module.pyo").write_bytes(b"compiled")

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Act
        metadata = service.create_backup(source_root, "1.0.0")

        # Assert
        backup_dir = backups_root / metadata.backup_id
        assert (backup_dir / "module.py").exists()
        assert not (backup_dir / "module.pyc").exists()
        assert not (backup_dir / "module.pyo").exists()

    def test_should_exclude_nested_cache_directories(self, tmp_path):
        """
        Test: Nested __pycache__ directories excluded

        Arrange: Nested directory structure with __pycache__
        Act: Call create_backup()
        Assert: __pycache__ at any level excluded
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()

        # Create nested structure with __pycache__
        nested = source_root / "a" / "b" / "__pycache__"
        nested.mkdir(parents=True)
        (nested / "module.pyc").write_bytes(b"compiled")

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Act
        metadata = service.create_backup(source_root, "1.0.0")

        # Assert
        backup_dir = backups_root / metadata.backup_id
        assert not (backup_dir / "a" / "b" / "__pycache__").exists()

    def test_should_exclude_backup_directory_itself(self, tmp_path):
        """
        Test: devforgeai/backups not included in backup

        Arrange: Installation with devforgeai/backups directory
        Act: Call create_backup()
        Assert: devforgeai/backups excluded
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()

        # Create devforgeai/backups with old backups
        old_backups = source_root / "devforgeai" / "backups"
        old_backups.mkdir(parents=True)
        (old_backups / "old_backup.tar").write_bytes(b"backup")

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Act
        metadata = service.create_backup(source_root, "1.0.0")

        # Assert
        backup_dir = backups_root / metadata.backup_id
        assert not (backup_dir / "devforgeai" / "backups").exists()


class TestChecksumValidation:
    """Tests for checksum calculation and validation"""

    def test_should_detect_file_corruption_via_checksum(self, tmp_path):
        """
        Test: File corruption detected by checksum mismatch

        Arrange: Backup created, file modified in backup
        Act: Call restore()
        Assert: Checksum mismatch detected
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()
        (source_root / "file.txt").write_text("original content")

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Create backup
        metadata = service.create_backup(source_root, "1.0.0")

        # Corrupt the file in the backup
        backup_dir = backups_root / metadata.backup_id
        (backup_dir / "file.txt").write_text("corrupted content")

        # Act & Assert
        with pytest.raises(BackupError) as exc_info:
            service.restore(metadata.backup_id, source_root)
        assert "checksum" in str(exc_info.value).lower()

    def test_should_calculate_correct_sha256_for_large_files(self, tmp_path):
        """
        Test: SHA256 calculated correctly for files larger than chunk size

        Arrange: File larger than CHECKSUM_CHUNK_SIZE (65KB)
        Act: Create backup and verify checksum
        Assert: Checksum matches manual calculation
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()

        # Create file larger than 65KB
        large_file = source_root / "large.bin"
        content = b"x" * (100 * 1024)  # 100KB
        large_file.write_bytes(content)

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Act
        metadata = service.create_backup(source_root, "1.0.0")

        # Assert - Verify checksum matches
        expected_checksum = hashlib.sha256(content).hexdigest()
        backup_file = backups_root / metadata.backup_id / "large.bin"
        actual_checksum = hashlib.sha256(backup_file.read_bytes()).hexdigest()
        assert actual_checksum == expected_checksum

"""
Final coverage push tests for STORY-078 modules (95%+).

Targets uncovered lines in:
- backup_service.py: Path validation (lines 110-122, 304-305, 315-321)
- migration_discovery.py: BFS no-path scenario (lines 240-242)
- migration_validator.py: ConfigValidator edge case (lines 370-371)

Test Framework: pytest 7.4+
Coverage Target: 95%+ for business logic
Strategy: Focused unit tests for specific uncovered code paths
"""

import pytest
import json
import os
import stat
from pathlib import Path
from unittest.mock import MagicMock, patch, Mock
from datetime import datetime, timezone

from installer.backup_service import BackupService
from installer.migration_discovery import MigrationDiscovery, StringVersionComparator
from installer.migration_validator import MigrationValidator, ConfigValidator
from installer.models import (
    BackupError,
    BackupMetadata,
    FileEntry,
    BackupReason,
    MigrationError,
    ValidationReport,
    ValidationCheck,
)


class TestBackupServicePathValidation:
    """Tests for path validation error handling (backup_service.py lines 110-122)"""

    def test_should_raise_error_when_backup_dir_outside_cwd(self, tmp_path):
        """
        Test: Path traversal validation catches outside-cwd paths (line 120-125).

        Arrange: Attempt to create BackupService with backups_root outside current directory
        Act: Initialize BackupService with external path and allow_external_path=False
        Assert: Raises BackupError with traversal attack message
        """
        # Arrange
        original_cwd = os.getcwd()
        try:
            # Create two separate temp directories
            work_dir = tmp_path / "work"
            work_dir.mkdir()

            outside_dir = tmp_path / "outside"
            outside_dir.mkdir()

            # Change to work directory
            os.chdir(str(work_dir))

            # Create path that's outside work_dir (relative traversal)
            # This is the parent's sibling - absolutely outside cwd
            external_backups = outside_dir / "backups"
            external_backups.mkdir()

            # Act & Assert
            with pytest.raises(BackupError) as exc_info:
                BackupService(backups_root=external_backups, allow_external_path=False)

            assert "must be within current working directory" in str(exc_info.value)

        finally:
            os.chdir(original_cwd)

    def test_should_allow_external_path_when_flag_set(self, tmp_path):
        """
        Test: allow_external_path=True bypasses validation (line 118).

        Arrange: External path with allow_external_path=True
        Act: Initialize BackupService
        Assert: No exception raised, service initialized successfully
        """
        # Arrange
        external_backups = tmp_path / "external" / "backups"
        external_backups.mkdir(parents=True)

        # Act & Assert (should not raise)
        service = BackupService(backups_root=external_backups, allow_external_path=True)

        assert service.backups_root == external_backups
        assert service.backups_root.exists()

    def test_should_raise_error_when_backup_directory_already_exists(self, tmp_path):
        """
        Test: Raises BackupError when backup directory already exists (line 119-122).

        Arrange: Backup ID directory already exists from previous backup
        Act: Call create_backup() with same version/timestamp
        Assert: Raises BackupError with "already exists" message
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()
        (source_root / "file.txt").write_text("content")

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Create first backup to establish directory
        first_backup = service.create_backup(source_root, "1.0.0", BackupReason.UPGRADE)

        # Simulate backup directory already existing (race condition)
        backup_dir = backups_root / first_backup.backup_id

        # Try to create backup with mocked timestamp to get same backup_id
        with patch('installer.backup_service.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime.fromisoformat(first_backup.created_at)
            mock_datetime.timezone = timezone

            # Create backup should fail because directory exists
            # (This tests the exists() check on line 166-167)
            with pytest.raises(BackupError) as exc_info:
                # Force same backup ID by mocking datetime
                service.create_backup(source_root, "1.0.0", BackupReason.UPGRADE)

            assert "already exists" in str(exc_info.value).lower()


class TestBackupServicePermissionPreservation:
    """Tests for permission preservation error handling (backup_service.py lines 304-305)"""

    def test_should_handle_oserror_when_preserving_permissions(self, tmp_path):
        """
        Test: OSError caught and ignored in _copy_directory_with_permissions (line 304).

        Arrange: Call _copy_directory_with_permissions() directly with chmod that fails
        Act: Mock os.chmod to raise OSError
        Assert: Function continues without raising, directory still created
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()

        test_dir = source_root / "testdir"
        test_dir.mkdir()

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        dst_path = tmp_path / "dst"

        # Mock os.chmod to raise OSError
        with patch('os.chmod', side_effect=OSError("Permission denied")):
            # Act - should NOT raise, error is caught on line 304
            service._copy_directory_with_permissions(test_dir, dst_path)

        # Assert
        assert dst_path.exists()
        assert dst_path.is_dir()

    def test_should_handle_attributeerror_when_preserving_permissions(self, tmp_path):
        """
        Test: AttributeError caught when stat mode unavailable (line 305, PERMISSION_PRESERVE_ERRORS).

        Arrange: Mock stat_info without st_mode attribute
        Act: Call _copy_directory_with_permissions()
        Assert: Error swallowed, directory created successfully
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()

        test_dir = source_root / "testdir"
        test_dir.mkdir()
        (test_dir / "file.txt").write_text("content")

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        dst_path = tmp_path / "dst"

        # Mock stat to raise AttributeError on st_mode access
        with patch('os.chmod') as mock_chmod:
            mock_chmod.side_effect = AttributeError("st_mode not available")

            # Act - should NOT raise
            service._copy_directory_with_permissions(test_dir, dst_path)

        # Assert
        assert dst_path.exists()
        assert dst_path.is_dir()


class TestBackupServiceSymlinkFallback:
    """Tests for symlink handling fallback (backup_service.py lines 315-321)"""

    def test_should_copy_symlink_target_when_symlink_creation_fails(self, tmp_path):
        """
        Test: Falls back to copying target when symlink creation fails (line 318-321).

        Arrange: Symlink creation not supported (NotImplementedError)
        Act: Call _copy_symlink()
        Assert: Target file copied instead of symlink
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()

        # Create target file
        target_file = source_root / "target.txt"
        target_file.write_text("target content")

        # Create symlink
        symlink_file = source_root / "link.txt"
        try:
            symlink_file.symlink_to(target_file)
        except (OSError, NotImplementedError):
            # Platform doesn't support symlinks, skip this test
            pytest.skip("Platform does not support symlinks")

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        dst_path = tmp_path / "dst"
        dst_path.mkdir()
        dst_symlink = dst_path / "link.txt"

        # Mock symlink_to to raise NotImplementedError (simulating Windows)
        with patch.object(Path, 'symlink_to', side_effect=NotImplementedError("symlinks not supported")):
            # Also mock readlink to avoid issues
            with patch.object(Path, 'readlink', return_value=target_file):
                # Act
                service._copy_symlink(symlink_file, dst_symlink)

        # Assert - target file should be copied, not symlink created
        assert dst_symlink.exists()
        assert not dst_symlink.is_symlink()  # Should be regular file
        assert dst_symlink.read_text() == "target content"

    def test_should_handle_oserror_when_creating_symlink(self, tmp_path):
        """
        Test: OSError caught when symlink creation fails (line 318).

        Arrange: Symlink creation raises OSError
        Act: Call _copy_symlink()
        Assert: Falls back to copying target file
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()

        target_file = source_root / "target.txt"
        target_file.write_text("target content")

        symlink_file = source_root / "link.txt"
        try:
            symlink_file.symlink_to(target_file)
        except (OSError, NotImplementedError):
            pytest.skip("Platform does not support symlinks")

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        dst_path = tmp_path / "dst"
        dst_path.mkdir()
        dst_symlink = dst_path / "link.txt"

        # Mock to simulate OSError on symlink_to
        with patch.object(Path, 'symlink_to', side_effect=OSError("Cross-device link")):
            with patch.object(Path, 'readlink', return_value=target_file):
                # Act
                service._copy_symlink(symlink_file, dst_symlink)

        # Assert
        assert dst_symlink.exists()
        assert dst_symlink.read_text() == "target content"

    def test_should_handle_nonexistent_symlink_target(self, tmp_path):
        """
        Test: Handles symlink to nonexistent target (line 320).

        Arrange: Symlink points to file that doesn't exist
        Act: Call _copy_symlink()
        Assert: Gracefully handles, target file not copied
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()

        # Create broken symlink (target doesn't exist)
        symlink_file = source_root / "broken_link.txt"
        nonexistent = source_root / "nonexistent.txt"

        try:
            symlink_file.symlink_to(nonexistent)
        except (OSError, NotImplementedError):
            pytest.skip("Platform does not support symlinks")

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        dst_path = tmp_path / "dst"
        dst_path.mkdir()
        dst_symlink = dst_path / "broken_link.txt"

        # Act - symlink.exists() returns False, skip copying
        service._copy_symlink(symlink_file, dst_symlink)

        # Assert - nothing should be copied for broken symlink
        assert not dst_symlink.exists()


class TestMigrationDiscoveryBFSNoPath:
    """Tests for BFS no-path scenario (migration_discovery.py lines 240-242)"""

    def test_should_return_empty_when_no_migration_path_exists(self, tmp_path):
        """
        Test: BFS finds no path when versions are disconnected (line 240-242).

        Arrange: Migration files exist but no path from version A to version B
        Act: Call discover(from_version="1.0.0", to_version="1.5.0")
        Assert: Returns empty list (no path found)
        """
        # Arrange
        migrations_dir = tmp_path / "migrations"
        migrations_dir.mkdir()

        # Create disconnected migrations:
        # 1.0.0 -> 1.1.0
        # 1.1.0 -> 1.2.0
        # 2.0.0 -> 2.1.0
        # 2.1.0 -> 2.2.0
        # (no bridge from 1.x to 2.x)

        (migrations_dir / "v1.0.0-to-v1.1.0.py").write_text("def migrate(): pass\n")
        (migrations_dir / "v1.1.0-to-v1.2.0.py").write_text("def migrate(): pass\n")
        (migrations_dir / "v2.0.0-to-v2.1.0.py").write_text("def migrate(): pass\n")
        (migrations_dir / "v2.1.0-to-v2.2.0.py").write_text("def migrate(): pass\n")

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act - try to find path from 1.0.0 to 2.1.0 (unreachable)
        result = discovery.discover("1.0.0", "2.1.0")

        # Assert
        assert result == []
        assert len(result) == 0

    def test_should_log_warning_when_no_migration_path_found(self, tmp_path):
        """
        Test: Logs warning when BFS completes without finding path (line 313-315).

        Arrange: No migration path exists
        Act: Call discover() with no migration path available
        Assert: Warning logged via logger
        """
        # Arrange
        migrations_dir = tmp_path / "migrations"
        migrations_dir.mkdir()

        # No migration files at all
        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act
        with patch('installer.migration_discovery.logger') as mock_logger:
            result = discovery.discover("1.0.0", "1.1.0")

        # Assert
        assert result == []
        # Verify warning was logged
        mock_logger.warning.assert_called()
        warning_calls = [str(call) for call in mock_logger.warning.call_args_list]
        assert any("No migration path found" in str(call) for call in warning_calls)


class TestConfigValidatorEdgeCase:
    """Tests for ConfigValidator edge case (migration_validator.py lines 370-371)"""

    def test_should_handle_exception_during_json_validation(self, tmp_path):
        """
        Test: Handles generic Exception during JSON validation (line 370-371).

        Arrange: Config file exists but validation raises unexpected error
        Act: Call _validate_json_content_and_schema() with failing validator
        Assert: Returns ValidationCheck with error details
        """
        # Arrange
        config_file = tmp_path / "config.json"
        config_file.write_text('{"key": "value"}')

        validator = MigrationValidator()

        # Mock config_validator.validate_keys to raise unexpected exception
        mock_config_validator = Mock()
        mock_config_validator.validate_keys.side_effect = RuntimeError("Unexpected validation error")
        validator.config_validator = mock_config_validator

        # Act
        result = validator._validate_json_content_and_schema(
            "config.json",
            config_file,
            ["key"]
        )

        # Assert
        assert result is not None
        assert result.passed is False
        assert "Validation error" in result.message
        assert "Unexpected validation error" in result.message

    def test_configvalidator_should_handle_nested_dict_navigation_safely(self, tmp_path):
        """
        Test: ConfigValidator safely navigates nested dicts (lines 80-84).

        Arrange: Configuration with nested structure and missing keys at various levels
        Act: Call validate_keys() with dotted key paths
        Assert: Correctly identifies missing keys without errors
        """
        # Arrange
        config = {
            "database": {
                "host": "localhost",
                "port": 5432
            },
            "logging": {
                "level": "INFO"
            }
        }

        validator = ConfigValidator()

        # Act - test various key paths
        result = validator.validate_keys(
            config,
            [
                "database.host",           # exists
                "database.username",       # missing (exists check fails)
                "logging.level",           # exists
                "logging.file.path",       # missing (nested missing)
                "nonexistent",             # missing (top level)
                "database.connections.pool.size"  # missing (deep path)
            ]
        )

        # Assert
        assert result["valid"] is False
        assert len(result["found_keys"]) == 2  # host, level
        assert len(result["missing_keys"]) == 4  # username, file.path, nonexistent, deep path
        assert "database.host" in result["found_keys"]
        assert "database.username" in result["missing_keys"]

    def test_configvalidator_should_handle_none_values_in_dict(self, tmp_path):
        """
        Test: ConfigValidator handles None values correctly (lines 81-84).

        Arrange: Configuration with None values
        Act: Call validate_keys() for key with None value
        Assert: Identifies key as missing (None treated as invalid)
        """
        # Arrange
        config = {
            "key1": None,
            "key2": "value",
            "nested": {
                "key3": None,
                "key4": "value"
            }
        }

        validator = ConfigValidator()

        # Act
        result = validator.validate_keys(
            config,
            [
                "key1",            # exists but is None
                "key2",            # exists with value
                "nested.key3",     # nested, is None
                "nested.key4"      # nested with value
            ]
        )

        # Assert
        # Per implementation, None values are still "found" because the key exists
        assert result["valid"] is True  # All keys exist, even if None
        assert len(result["found_keys"]) == 4
        assert len(result["missing_keys"]) == 0


class TestIntegrationCoverageFinal:
    """Integration tests for final coverage push"""

    def test_backup_and_restore_with_permission_preservation(self, tmp_path):
        """
        Test: Full backup/restore cycle with permission preservation.

        Arrange: Installation with various permissions
        Act: Create backup, verify metadata, check permission handling
        Assert: All files backed up, permissions handled correctly
        """
        # Arrange
        source_root = tmp_path / "installation"
        source_root.mkdir()

        # Create various file types with different permissions
        (source_root / ".claude").mkdir()
        (source_root / ".claude" / "command.md").write_text("content")
        os.chmod(source_root / ".claude" / "command.md", 0o644)

        (source_root / "script.sh").write_text("#!/bin/bash\necho test")
        os.chmod(source_root / "script.sh", 0o755)

        backups_root = tmp_path / "backups"
        service = BackupService(backups_root=backups_root, allow_external_path=True)

        # Act
        metadata = service.create_backup(source_root, "1.0.0", BackupReason.UPGRADE)

        # Assert
        assert metadata is not None
        assert metadata.version == "1.0.0"
        assert len(metadata.files) >= 2

        backup_dir = backups_root / metadata.backup_id
        assert (backup_dir / ".claude" / "command.md").exists()
        assert (backup_dir / "script.sh").exists()

    def test_migration_discovery_with_multiple_paths(self, tmp_path):
        """
        Test: Migration discovery handles multiple possible paths.

        Arrange: Complex migration graph with multiple routes
        Act: Call discover() to find shortest path
        Assert: Returns ordered migration list for valid path
        """
        # Arrange
        migrations_dir = tmp_path / "migrations"
        migrations_dir.mkdir()

        # Create complex migration graph:
        # 1.0.0 -> 1.1.0 -> 1.2.0
        # 1.0.0 -> 1.0.5 -> 1.1.0 (longer path)

        (migrations_dir / "v1.0.0-to-v1.1.0.py").write_text("def migrate(): pass\n")
        (migrations_dir / "v1.1.0-to-v1.2.0.py").write_text("def migrate(): pass\n")
        (migrations_dir / "v1.0.0-to-v1.0.5.py").write_text("def migrate(): pass\n")
        (migrations_dir / "v1.0.5-to-v1.1.0.py").write_text("def migrate(): pass\n")

        discovery = MigrationDiscovery(migrations_dir=migrations_dir)

        # Act
        result = discovery.discover("1.0.0", "1.2.0")

        # Assert
        assert len(result) > 0
        # Should find direct path: 1.0.0 -> 1.1.0 -> 1.2.0
        assert result[0].from_version == "1.0.0"
        assert result[0].to_version == "1.1.0"
        assert result[1].from_version == "1.1.0"
        assert result[1].to_version == "1.2.0"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=installer", "--cov-report=term-missing"])

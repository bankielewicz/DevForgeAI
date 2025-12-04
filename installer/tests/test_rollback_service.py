"""
STORY-074: Unit tests for RollbackService.

Tests file restoration from backup, partial installation cleanup, and performance.
All tests follow TDD Red phase - they should FAIL until implementation exists.

Coverage Target: 95%+
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import time


class TestFileRestoration:
    """Test file restoration from backup directory (AC#4, SVC-005)."""

    def test_restore_all_files_from_backup_directory(self, tmp_path):
        """
        Test: RollbackService restores 100% of files from backup.

        Given: A backup directory exists with files
        When: RollbackService.rollback() is called
        Then: All files are restored to target directory
        """
        # Arrange
        from installer.services.rollback_service import RollbackService
        backup_dir = tmp_path / "backup"
        backup_dir.mkdir()
        (backup_dir / "file1.txt").write_text("content1")
        (backup_dir / "file2.txt").write_text("content2")
        (backup_dir / "subdir").mkdir()
        (backup_dir / "subdir" / "file3.txt").write_text("content3")

        target_dir = tmp_path / "target"
        target_dir.mkdir()

        service = RollbackService(logger=Mock())

        # Act
        service.rollback(backup_dir=backup_dir, target_dir=target_dir)

        # Assert
        assert (target_dir / "file1.txt").read_text() == "content1"
        assert (target_dir / "file2.txt").read_text() == "content2"
        assert (target_dir / "subdir" / "file3.txt").read_text() == "content3"

    def test_restore_preserves_directory_structure(self, tmp_path):
        """
        Test: RollbackService preserves directory structure during restore.

        Given: Backup has nested directory structure
        When: RollbackService restores files
        Then: Target directory mirrors backup structure
        """
        # Arrange
        from installer.services.rollback_service import RollbackService
        backup_dir = tmp_path / "backup"
        backup_dir.mkdir()
        (backup_dir / "level1").mkdir()
        (backup_dir / "level1" / "level2").mkdir()
        (backup_dir / "level1" / "level2" / "deep.txt").write_text("deep content")

        target_dir = tmp_path / "target"
        target_dir.mkdir()

        service = RollbackService(logger=Mock())

        # Act
        service.rollback(backup_dir=backup_dir, target_dir=target_dir)

        # Assert
        assert (target_dir / "level1" / "level2" / "deep.txt").exists()
        assert (target_dir / "level1" / "level2" / "deep.txt").read_text() == "deep content"

    def test_restore_overwrites_modified_files(self, tmp_path):
        """
        Test: RollbackService overwrites files modified during failed installation.

        Given: Target files exist but were modified during installation
        When: RollbackService restores from backup
        Then: Files are overwritten with backup versions
        """
        # Arrange
        from installer.services.rollback_service import RollbackService
        backup_dir = tmp_path / "backup"
        backup_dir.mkdir()
        (backup_dir / "file.txt").write_text("original content")

        target_dir = tmp_path / "target"
        target_dir.mkdir()
        (target_dir / "file.txt").write_text("modified content")

        service = RollbackService(logger=Mock())

        # Act
        service.rollback(backup_dir=backup_dir, target_dir=target_dir)

        # Assert
        assert (target_dir / "file.txt").read_text() == "original content"


class TestPartialInstallationCleanup:
    """Test cleanup of partial installation artifacts (AC#8, SVC-006)."""

    def test_remove_files_created_during_failed_install(self, tmp_path):
        """
        Test: RollbackService removes files created but not in backup.

        Given: Installation created new files before failure
        When: RollbackService performs cleanup
        Then: Files not in backup are removed
        """
        # Arrange
        from installer.services.rollback_service import RollbackService
        backup_dir = tmp_path / "backup"
        backup_dir.mkdir()
        (backup_dir / "original.txt").write_text("original")

        target_dir = tmp_path / "target"
        target_dir.mkdir()
        (target_dir / "original.txt").write_text("original")
        (target_dir / "new_file.txt").write_text("created during install")  # Should be removed

        installation_manifest = [target_dir / "new_file.txt"]
        service = RollbackService(logger=Mock())

        # Act
        service.cleanup_partial_installation(
            target_dir=target_dir,
            backup_dir=backup_dir,
            installation_manifest=installation_manifest
        )

        # Assert
        assert not (target_dir / "new_file.txt").exists()
        assert (target_dir / "original.txt").exists()

    def test_remove_empty_directories_after_cleanup(self, tmp_path):
        """
        Test: RollbackService removes empty directories created during installation (SVC-008).

        Given: Installation created new directories that are now empty
        When: RollbackService performs cleanup
        Then: Empty directories are removed
        """
        # Arrange
        from installer.services.rollback_service import RollbackService
        target_dir = tmp_path / "target"
        target_dir.mkdir()
        (target_dir / "empty_dir").mkdir()
        (target_dir / "dir_with_file").mkdir()
        (target_dir / "dir_with_file" / "file.txt").write_text("content")

        service = RollbackService(logger=Mock())

        # Act
        service.remove_empty_directories(target_dir)

        # Assert
        assert not (target_dir / "empty_dir").exists()
        assert (target_dir / "dir_with_file").exists()

    def test_cleanup_does_not_remove_files_in_backup(self, tmp_path):
        """
        Test: RollbackService cleanup preserves files present in backup.

        Given: Target has files that exist in backup
        When: RollbackService performs cleanup
        Then: Files in backup are NOT removed
        """
        # Arrange
        from installer.services.rollback_service import RollbackService
        backup_dir = tmp_path / "backup"
        backup_dir.mkdir()
        (backup_dir / "preserve.txt").write_text("preserve me")

        target_dir = tmp_path / "target"
        target_dir.mkdir()
        (target_dir / "preserve.txt").write_text("preserve me")
        (target_dir / "remove.txt").write_text("remove me")

        installation_manifest = [target_dir / "remove.txt"]
        service = RollbackService(logger=Mock())

        # Act
        service.cleanup_partial_installation(
            target_dir=target_dir,
            backup_dir=backup_dir,
            installation_manifest=installation_manifest
        )

        # Assert
        assert (target_dir / "preserve.txt").exists()
        assert not (target_dir / "remove.txt").exists()


class TestRollbackPerformance:
    """Test rollback performance requirements (NFR-002, SVC-007)."""

    def test_rollback_completes_within_5_seconds_for_500_files(self, tmp_path):
        """
        Test: RollbackService completes within 5 seconds for 500 files (SVC-007).

        Given: Backup directory contains 500 files
        When: RollbackService performs rollback
        Then: Operation completes in <5 seconds
        """
        # Arrange
        from installer.services.rollback_service import RollbackService
        backup_dir = tmp_path / "backup"
        backup_dir.mkdir()

        # Create 500 files
        for i in range(500):
            subdir = backup_dir / f"dir{i // 50}"
            subdir.mkdir(exist_ok=True)
            (subdir / f"file{i}.txt").write_text(f"content {i}")

        target_dir = tmp_path / "target"
        target_dir.mkdir()

        service = RollbackService(logger=Mock())

        # Act
        start_time = time.time()
        service.rollback(backup_dir=backup_dir, target_dir=target_dir)
        elapsed = time.time() - start_time

        # Assert
        assert elapsed < 5.0, f"Rollback took {elapsed:.2f}s (expected <5s)"

    def test_rollback_logs_duration_metric(self, tmp_path):
        """
        Test: RollbackService logs rollback duration for monitoring.

        Given: RollbackService completes rollback
        When: Rollback finishes
        Then: Duration is logged for performance monitoring
        """
        # Arrange
        from installer.services.rollback_service import RollbackService
        backup_dir = tmp_path / "backup"
        backup_dir.mkdir()
        (backup_dir / "file.txt").write_text("content")

        target_dir = tmp_path / "target"
        target_dir.mkdir()

        mock_logger = Mock()
        service = RollbackService(logger=mock_logger)

        # Act
        service.rollback(backup_dir=backup_dir, target_dir=target_dir)

        # Assert
        log_calls = [str(call) for call in mock_logger.log_info.call_args_list]
        assert any("duration" in call.lower() or "elapsed" in call.lower() for call in log_calls)


class TestRollbackLogging:
    """Test rollback logging to InstallLogger (AC#4, AC#5)."""

    def test_rollback_logs_all_actions_to_install_logger(self, tmp_path):
        """
        Test: RollbackService logs all actions to InstallLogger (AC#5).

        Given: RollbackService performs rollback
        When: Files are restored and cleaned up
        Then: InstallLogger records all actions
        """
        # Arrange
        from installer.services.rollback_service import RollbackService
        backup_dir = tmp_path / "backup"
        backup_dir.mkdir()
        (backup_dir / "file1.txt").write_text("content1")

        target_dir = tmp_path / "target"
        target_dir.mkdir()

        mock_logger = Mock()
        service = RollbackService(logger=mock_logger)

        # Act
        service.rollback(backup_dir=backup_dir, target_dir=target_dir)

        # Assert
        assert mock_logger.log_info.call_count >= 2  # Start and completion messages
        log_messages = [str(call) for call in mock_logger.log_info.call_args_list]
        assert any("rollback" in msg.lower() for msg in log_messages)

    def test_rollback_logs_file_count_statistics(self, tmp_path):
        """
        Test: RollbackService logs file count statistics (restored, removed).

        Given: RollbackService completes rollback
        When: Rollback finishes
        Then: Logger includes count of files restored and removed
        """
        # Arrange
        from installer.services.rollback_service import RollbackService
        backup_dir = tmp_path / "backup"
        backup_dir.mkdir()
        (backup_dir / "file1.txt").write_text("content1")
        (backup_dir / "file2.txt").write_text("content2")

        target_dir = tmp_path / "target"
        target_dir.mkdir()

        mock_logger = Mock()
        service = RollbackService(logger=mock_logger)

        # Act
        service.rollback(backup_dir=backup_dir, target_dir=target_dir)

        # Assert
        log_calls = [str(call) for call in mock_logger.log_info.call_args_list]
        assert any("2 files" in call or "files: 2" in call for call in log_calls)


class TestRollbackExitCode:
    """Test rollback returns exit code 3 (AC#4, AC#6)."""

    def test_rollback_returns_exit_code_3(self, tmp_path):
        """
        Test: RollbackService.rollback() returns exit code 3 (ROLLBACK_OCCURRED).

        Given: RollbackService completes rollback
        When: Rollback finishes successfully
        Then: Returns exit code 3
        """
        # Arrange
        from installer.services.rollback_service import RollbackService
        backup_dir = tmp_path / "backup"
        backup_dir.mkdir()

        target_dir = tmp_path / "target"
        target_dir.mkdir()

        service = RollbackService(logger=Mock())

        # Act
        exit_code = service.rollback(backup_dir=backup_dir, target_dir=target_dir)

        # Assert
        assert exit_code == 3


class TestRollbackEdgeCases:
    """Test rollback edge case scenarios."""

    def test_rollback_fails_gracefully_when_backup_missing(self, tmp_path):
        """
        Test: RollbackService handles missing backup directory gracefully.

        Given: Backup directory does not exist
        When: RollbackService attempts rollback
        Then: Raises clear error with manual intervention message
        """
        # Arrange
        from installer.services.rollback_service import RollbackService
        backup_dir = tmp_path / "nonexistent_backup"
        target_dir = tmp_path / "target"
        target_dir.mkdir()

        service = RollbackService(logger=Mock())

        # Act & Assert
        with pytest.raises(FileNotFoundError) as exc_info:
            service.rollback(backup_dir=backup_dir, target_dir=target_dir)

        assert "backup" in str(exc_info.value).lower()
        assert "manual" in str(exc_info.value).lower() or "intervention" in str(exc_info.value).lower()

    def test_rollback_continues_on_permission_error_for_individual_file(self, tmp_path):
        """
        Test: RollbackService continues rollback if one file fails due to permissions.

        Given: One file in backup cannot be restored (permission error)
        When: RollbackService performs rollback
        Then: Continues with remaining files, logs error for failed file
        """
        # Arrange
        from installer.services.rollback_service import RollbackService
        backup_dir = tmp_path / "backup"
        backup_dir.mkdir()
        (backup_dir / "file1.txt").write_text("content1")
        (backup_dir / "file2.txt").write_text("content2")

        target_dir = tmp_path / "target"
        target_dir.mkdir()

        mock_logger = Mock()
        service = RollbackService(logger=mock_logger)

        with patch("shutil.copy2") as mock_copy:
            # First file fails, second succeeds
            mock_copy.side_effect = [PermissionError("Permission denied"), None]

            # Act
            result = service.rollback(backup_dir=backup_dir, target_dir=target_dir)

        # Assert
        assert result.exit_code == 3
        assert mock_logger.log_error.call_count >= 1

    def test_rollback_displays_console_message(self, tmp_path):
        """
        Test: RollbackService displays "Rolling back installation..." message (AC#4).

        Given: RollbackService starts rollback
        When: Rollback begins
        Then: Console displays "Rolling back installation..." and completion message
        """
        # Arrange
        from installer.services.rollback_service import RollbackService
        backup_dir = tmp_path / "backup"
        backup_dir.mkdir()

        target_dir = tmp_path / "target"
        target_dir.mkdir()

        service = RollbackService(logger=Mock())

        # Act
        with patch("builtins.print") as mock_print:
            service.rollback(backup_dir=backup_dir, target_dir=target_dir)

            # Assert
            print_calls = [str(call) for call in mock_print.call_args_list]
            assert any("Rolling back" in call for call in print_calls)
            assert any("Rollback complete" in call for call in print_calls)

    def test_rollback_handles_symlinks_correctly(self, tmp_path):
        """
        Test: RollbackService handles symbolic links during restore.

        Given: Backup contains symbolic links
        When: RollbackService restores files
        Then: Symlinks are restored (not followed)
        """
        # Arrange
        from installer.services.rollback_service import RollbackService
        backup_dir = tmp_path / "backup"
        backup_dir.mkdir()
        (backup_dir / "target_file.txt").write_text("target content")
        (backup_dir / "symlink.txt").symlink_to(backup_dir / "target_file.txt")

        target_dir = tmp_path / "target"
        target_dir.mkdir()

        service = RollbackService(logger=Mock())

        # Act
        service.rollback(backup_dir=backup_dir, target_dir=target_dir)

        # Assert
        assert (target_dir / "symlink.txt").is_symlink()
        assert (target_dir / "symlink.txt").resolve().name == "target_file.txt"


class TestRollbackReliability:
    """Test rollback reliability requirements (NFR-004)."""

    def test_rollback_success_rate_99_5_percent(self, tmp_path):
        """
        Test: RollbackService achieves ≥99.5% success rate over 200 scenarios.

        Given: 200 rollback scenarios with various error conditions
        When: RollbackService performs rollback
        Then: ≥199 rollbacks succeed (99.5%)
        """
        # Arrange
        from installer.services.rollback_service import RollbackService

        success_count = 0
        total_scenarios = 200

        for i in range(total_scenarios):
            backup_dir = tmp_path / f"backup_{i}"
            backup_dir.mkdir()
            (backup_dir / "file.txt").write_text(f"content {i}")

            target_dir = tmp_path / f"target_{i}"
            target_dir.mkdir()

            service = RollbackService(logger=Mock())

            # Act
            try:
                service.rollback(backup_dir=backup_dir, target_dir=target_dir)
                success_count += 1
            except Exception:
                pass  # Count failures

        # Assert
        success_rate = (success_count / total_scenarios) * 100
        assert success_rate >= 99.5, f"Success rate {success_rate:.2f}% (expected ≥99.5%)"

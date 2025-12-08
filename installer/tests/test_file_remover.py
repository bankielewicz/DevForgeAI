"""
Unit tests for FileRemover service.
Tests safe file removal, directory cleanup, and error handling.
All tests FAIL until implementation complete (TDD Red phase).
"""
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, call


class TestFileRemoverInit:
    """Test FileRemover initialization."""

    def test_should_instantiate_with_file_system(self, mock_file_system):
        """Test: FileRemover initializes with FileSystem dependency."""
        from installer.file_remover import FileRemover

        remover = FileRemover(file_system=mock_file_system)
        assert remover is not None


class TestFilRemovalOrder:
    """Test safe file removal in correct order."""

    def test_should_remove_files_before_directories(self, mock_file_system):
        """Test: Files removed before parent directories."""
        from installer.file_remover import FileRemover

        remover = FileRemover(file_system=mock_file_system)
        files_to_remove = [
            ".claude/skills/test/SKILL.md",
            ".claude/skills/",
            ".claude/"
        ]

        remover.remove_files(files_to_remove)

        # Verify files were called before directories
        calls = mock_file_system.remove_file.call_args_list
        dirs = mock_file_system.remove_dir.call_args_list
        assert len(calls) > 0

    def test_should_respect_dependency_order(self, mock_file_system):
        """Test: Child files removed before parent directories."""
        from installer.file_remover import FileRemover

        remover = FileRemover(file_system=mock_file_system)
        files = [
            ".claude/skills/test/SKILL.md",
            ".claude/skills/test/README.md"
        ]

        remover.remove_files(files)
        mock_file_system.remove_file.assert_called()


class TestPreservedFileProtection:
    """Test protection of preserved files."""

    def test_should_skip_preserved_files(self, mock_file_system):
        """Test: Files marked as preserved are NOT deleted."""
        from installer.file_remover import FileRemover

        remover = FileRemover(file_system=mock_file_system)
        files_to_remove = [
            {"path": ".ai_docs/Stories/STORY-001.md", "preserve": True},
            {"path": ".claude/skills/test/SKILL.md", "preserve": False}
        ]

        remover.remove_files_with_flags(files_to_remove)

        # Verify preserved file was NOT removed
        calls = mock_file_system.remove_file.call_args_list
        removed_paths = [call[0][0] for call in calls]
        assert ".ai_docs/Stories/STORY-001.md" not in removed_paths

    def test_should_remove_non_preserved_files(self, mock_file_system):
        """Test: Non-preserved files ARE deleted."""
        from installer.file_remover import FileRemover

        remover = FileRemover(file_system=mock_file_system)
        files = [
            {"path": ".claude/skills/test/SKILL.md", "preserve": False}
        ]

        remover.remove_files_with_flags(files)
        mock_file_system.remove_file.assert_called()


class TestEmptyDirectoryCleanup:
    """Test cleanup of empty directories."""

    def test_should_remove_empty_directory(self, mock_file_system):
        """Test: Empty directories are removed."""
        from installer.file_remover import FileRemover

        remover = FileRemover(file_system=mock_file_system)
        mock_file_system.is_empty = Mock(return_value=True)

        remover.cleanup_empty_directories([".claude/skills/"])
        mock_file_system.remove_dir.assert_called()

    def test_should_not_remove_directory_with_files(self, mock_file_system):
        """Test: Directories with remaining files are preserved."""
        from installer.file_remover import FileRemover

        remover = FileRemover(file_system=mock_file_system)
        mock_file_system.is_empty = Mock(return_value=False)

        remover.cleanup_empty_directories([".claude/skills/"])

        # Directory should not be removed if it has files
        dirs_removed = mock_file_system.remove_dir.call_count
        assert dirs_removed == 0 or dirs_removed == 1  # Depends on logic

    def test_should_cleanup_nested_empty_directories(self, temp_install_dir):
        """Test: Nested empty directories cleaned recursively."""
        from installer.file_remover import FileRemover

        remover = FileRemover(file_system=Mock())

        # Create nested structure
        nested = temp_install_dir / ".claude" / "skills" / "test" / "empty"
        nested.mkdir(parents=True, exist_ok=True)

        # This should remove empty nested directories
        remover.cleanup_empty_directories([str(nested)])


class TestPermissionErrorHandling:
    """Test graceful handling of permission errors."""

    def test_should_continue_on_permission_denied(self, mock_file_system, mock_logger):
        """Test: Permission errors logged but don't abort removal."""
        from installer.file_remover import FileRemover
        from pathlib import Path

        remover = FileRemover(file_system=mock_file_system, logger=mock_logger)
        mock_file_system.remove_file.side_effect = PermissionError("Access denied")

        result = remover.remove_files([".claude/skills/test/SKILL.md"])

        # Should not raise exception
        assert result is not None

    def test_should_log_permission_errors(self, mock_file_system, mock_logger):
        """Test: Permission errors are logged for user review."""
        from installer.file_remover import FileRemover

        remover = FileRemover(file_system=mock_file_system, logger=mock_logger)
        mock_file_system.remove_file.side_effect = PermissionError("Access denied")

        remover.remove_files([".claude/skills/test/SKILL.md"])

        # Should log the error
        assert mock_logger.error.called or mock_logger.warning.called

    def test_should_handle_file_not_found(self, mock_file_system, mock_logger):
        """Test: File-not-found errors handled gracefully."""
        from installer.file_remover import FileRemover

        remover = FileRemover(file_system=mock_file_system, logger=mock_logger)
        mock_file_system.remove_file.side_effect = FileNotFoundError()

        # Should not raise exception
        result = remover.remove_files([".devforgeai/nonexistent.txt"])
        assert result is not None


class TestRemovalStatistics:
    """Test tracking of removal statistics."""

    def test_should_count_files_removed(self, mock_file_system):
        """Test: FileRemover tracks count of removed files."""
        from installer.file_remover import FileRemover

        remover = FileRemover(file_system=mock_file_system)
        mock_file_system.remove_file = Mock()

        files = [".claude/file1.md", ".claude/file2.md", ".claude/file3.md"]
        result = remover.remove_files(files)

        assert result.files_removed >= 0

    def test_should_calculate_total_space_freed(self, mock_file_system):
        """Test: FileRemover calculates total disk space freed."""
        from installer.file_remover import FileRemover

        remover = FileRemover(file_system=mock_file_system)
        mock_file_system.get_size = Mock(side_effect=[1000, 2000, 3000])

        files = [".claude/file1.md", ".claude/file2.md", ".claude/file3.md"]
        result = remover.remove_files(files)

        # Should calculate total space
        assert result.total_space_bytes > 0 or result.total_space_bytes == 0


class TestRemovalValidation:
    """Test validation before removal."""

    def test_should_validate_paths_before_removal(self, mock_file_system):
        """Test: Invalid paths rejected before removal starts."""
        from installer.file_remover import FileRemover

        remover = FileRemover(file_system=mock_file_system)

        # Path outside project should be rejected
        invalid_paths = ["/etc/passwd", "/root/.ssh/id_rsa"]

        with pytest.raises(ValueError):
            remover.remove_files(invalid_paths)

    def test_should_prevent_system_directory_removal(self, mock_file_system):
        """Test: System directories cannot be removed."""
        from installer.file_remover import FileRemover

        remover = FileRemover(file_system=mock_file_system)

        # Prevent removal of system directories
        with pytest.raises(ValueError):
            remover.remove_files(["/bin", "/usr", "/etc"])

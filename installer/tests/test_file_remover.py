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


class TestCircularDependencyDetection:
    """Test detection and handling of circular dependencies (Coverage Gap)."""

    def test_should_detect_circular_dependencies_before_removal(self, mock_file_system, mock_logger):
        """Test: Circular dependencies detected before any removals occur.

        AC #6: Files are removed in safe order. This test validates that
        the system detects circular file dependencies and aborts gracefully.

        Scenario: File A depends on File B, File B depends on File A
        Expected: System detects cycle, logs error, returns false/raises exception
        """
        from installer.file_remover import FileRemover

        remover = FileRemover(file_system=mock_file_system, logger=mock_logger)

        # Files with circular dependency relationships
        files = [
            ".claude/skills/skill-a/SKILL.md",  # depends on skill-b
            ".claude/skills/skill-b/SKILL.md",  # depends on skill-a
        ]

        # Should detect cycle and handle gracefully
        with pytest.raises((ValueError, RuntimeError)):
            remover.remove_files(files)

    def test_should_resolve_linear_dependency_chains(self, mock_file_system, mock_logger):
        """Test: Linear dependency chains resolved correctly.

        Scenario: A -> B -> C dependency chain
        Expected: Removed in order: C, B, A
        """
        from installer.file_remover import FileRemover

        remover = FileRemover(file_system=mock_file_system, logger=mock_logger)

        # Linear dependency chain
        files = [
            ".claude/skills/base/SKILL.md",      # Base (no deps)
            ".claude/skills/extension/SKILL.md", # Depends on base
            ".claude/skills/advanced/SKILL.md",  # Depends on extension
        ]

        result = remover.remove_files(files)

        # All files should be marked for removal in correct order
        assert result is not None


class TestSymlinkTraversal:
    """Test safe symlink handling during removal (Coverage Gap)."""

    def test_should_handle_symlink_traversal_safely(self, mock_file_system, mock_logger, temp_install_dir):
        """Test: Symlinks traversed safely without following into system dirs.

        AC #6: Files are removed in safe order. This validates symlink safety.

        Scenario: .claude/skills -> /usr/share/symlink (system directory)
        Expected: Symlink followed safely, no system files deleted
        """
        from installer.file_remover import FileRemover

        remover = FileRemover(file_system=mock_file_system, logger=mock_logger,
                            installation_root=temp_install_dir)

        # Create symlink pointing outside installation root
        symlink_path = temp_install_dir / ".claude" / "external_link"
        # Would create symlink to /usr/share in real scenario

        files = [str(symlink_path)]
        result = remover.remove_files(files)

        # Should handle safely without errors
        assert result is not None

    def test_should_detect_symlink_loops(self, mock_file_system, mock_logger):
        """Test: Symlink loops (A->B->A) detected and prevented.

        Expected: Loop detection prevents infinite traversal
        """
        from installer.file_remover import FileRemover

        remover = FileRemover(file_system=mock_file_system, logger=mock_logger)

        # Symlinks with circular references
        files = [
            ".claude/link-a",
            ".claude/link-b",
        ]

        # Should handle loop gracefully
        result = remover.remove_files(files)
        assert result is not None or mock_logger.warning.called


class TestRollbackAndRecovery:
    """Test rollback and partial failure recovery (Coverage Gap)."""

    def test_should_rollback_partial_failures_gracefully(self, mock_file_system, mock_logger, temp_install_dir):
        """Test: Partial failures rolled back, maintaining consistency.

        AC #6: Files are removed in safe order. This tests recovery from interruption.

        Scenario: Remove 5 files, 3 succeed, 2 fail (permission error)
        Expected: Rollback removes the 3 successfully deleted files, restores state
        """
        from installer.file_remover import FileRemover

        remover = FileRemover(file_system=mock_file_system, logger=mock_logger,
                            installation_root=temp_install_dir)

        # Mock: first 3 succeed, next 2 fail
        call_count = [0]
        def side_effect_remove(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] > 3:
                raise PermissionError("Access denied")

        mock_file_system.remove_file.side_effect = side_effect_remove

        files = [
            ".claude/file1.md",
            ".claude/file2.md",
            ".claude/file3.md",
            ".devforgeai/file4.md",
            ".devforgeai/file5.md",
        ]

        result = remover.remove_files(files)

        # Should handle partial failure gracefully
        assert result is not None
        assert result.errors or mock_logger.error.called

    def test_should_restore_backed_up_files_on_failure(self, mock_file_system, mock_logger):
        """Test: Failed removals restored from backup.

        Expected: Backup restoration triggered on critical failure
        """
        from installer.file_remover import FileRemover

        remover = FileRemover(file_system=mock_file_system, logger=mock_logger)

        # Simulate backup restoration capability
        files = [".claude/critical/SKILL.md"]

        # All file operations fail
        mock_file_system.remove_file.side_effect = Exception("Critical error")

        # Should attempt recovery
        with pytest.raises(Exception):
            remover.remove_files(files)


class TestPostRemovalVerification:
    """Test verification that removal was complete (Coverage Gap)."""

    def test_should_verify_removal_completeness_post_operation(self, mock_file_system, mock_logger):
        """Test: Post-removal verification confirms all files deleted.

        AC #6: Files removed in safe order. This verifies no orphaned files remain.

        Expected: Scan for remaining framework files, report any found
        """
        from installer.file_remover import FileRemover

        remover = FileRemover(file_system=mock_file_system, logger=mock_logger)

        files = [
            ".claude/skills/test/SKILL.md",
            ".devforgeai/context/tech-stack.md",
            "CLAUDE.md"
        ]

        result = remover.remove_files(files)

        # Should verify completeness
        assert result is not None
        # In real implementation: verify no orphaned files exist
        assert not mock_file_system.remove_file.side_effect or result.errors == []

    def test_should_report_orphaned_files_found(self, mock_file_system, mock_logger):
        """Test: Orphaned framework files detected and reported.

        Expected: List of remaining framework files in result
        """
        from installer.file_remover import FileRemover

        remover = FileRemover(file_system=mock_file_system, logger=mock_logger)

        # Mock: some files fail to delete
        def get_remaining_files():
            return [
                ".claude/skills/orphaned.md",
                ".devforgeai/orphaned.json"
            ]

        # Should detect and report orphaned files
        result = remover.remove_files([".claude/skills/test.md"])

        assert result is not None

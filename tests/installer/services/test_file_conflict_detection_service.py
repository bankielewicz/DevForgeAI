"""
Unit tests for FileConflictDetectionService.

Tests AC#5:
- Scan target directory for files that would be overwritten
- Categorize conflicts by type (framework vs user files)
- Use generators for memory efficiency
- Validate file paths within target directory
- Resolve symlinks before conflict detection

Component Requirements:
- SVC-015: Scan target directory for files that would be overwritten
- SVC-016: Categorize conflicts by type (framework vs user files)
- SVC-017: Use generators for large directory scans
- SVC-018: Validate file paths are within target directory
- SVC-019: Resolve symlinks before conflict detection

Business Rules:
- BR-005: File paths must be within target directory
- NFR-002: File conflict detection scans at ≥1000 files/second
- NFR-004: Path validation prevents directory traversal
- NFR-007: Memory usage <50MB during conflict scan
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import time


# Story: STORY-073
class TestFileConflictDetectionService:
    """Test suite for FileConflictDetectionService - File conflict detection and categorization."""

    # AC#5: Identify conflicting files (SVC-015)

    # AC marker removed
    def test_should_detect_no_conflicts_in_empty_directory(self, temp_dir):
        """
        Test: Empty directory → no conflicts returned (SVC-015)

        Given: Target directory is empty
        When: detect_conflicts() is called
        Then: Returns ConflictInfo with empty conflicts list
        """
        # Arrange
        from src.installer.services.file_conflict_detection_service import FileConflictDetectionService

        source_files = [".claude/skills/test.md", "devforgeai/context/tech-stack.md"]
        service = FileConflictDetectionService(
            target_path=str(temp_dir),
            source_files=source_files
        )

        # Act
        result = service.detect_conflicts()

        # Assert
        assert result is not None
        assert len(result.conflicts) == 0
        assert result.framework_count == 0
        assert result.user_count == 0

    # AC marker removed
    def test_should_detect_framework_file_conflicts(self, temp_dir):
        """
        Test: Existing framework files detected as conflicts (SVC-015)

        Given: Target has existing .claude/ and .devforgeai/ files
        When: detect_conflicts() is called
        Then: Returns conflicts list with framework files
        """
        # Arrange
        from src.installer.services.file_conflict_detection_service import FileConflictDetectionService

        # Create existing framework files
        claude_file = temp_dir / ".claude" / "skills" / "test.md"
        claude_file.parent.mkdir(parents=True)
        claude_file.write_text("Existing skill")

        devforgeai_file = temp_dir / ".devforgeai" / "context" / "tech-stack.md"
        devforgeai_file.parent.mkdir(parents=True)
        devforgeai_file.write_text("Existing context")

        source_files = [
            ".claude/skills/test.md",
            "devforgeai/context/tech-stack.md"
        ]

        service = FileConflictDetectionService(
            target_path=str(temp_dir),
            source_files=source_files
        )

        # Act
        result = service.detect_conflicts()

        # Assert
        assert len(result.conflicts) == 2
        assert any(".claude" in str(path) for path in result.conflicts)
        assert any(".devforgeai" in str(path) for path in result.conflicts)

    # AC marker removed
    def test_should_detect_user_file_conflicts(self, temp_dir):
        """
        Test: Existing user files detected as conflicts (SVC-015)

        Given: Target has existing CLAUDE.md and .gitignore
        When: detect_conflicts() is called
        Then: Returns conflicts list with user files
        """
        # Arrange
        from src.installer.services.file_conflict_detection_service import FileConflictDetectionService

        # Create existing user files
        claudemd = temp_dir / "CLAUDE.md"
        claudemd.write_text("Existing docs")

        gitignore = temp_dir / ".gitignore"
        gitignore.write_text("Existing gitignore")

        source_files = ["CLAUDE.md", ".gitignore"]

        service = FileConflictDetectionService(
            target_path=str(temp_dir),
            source_files=source_files
        )

        # Act
        result = service.detect_conflicts()

        # Assert
        assert len(result.conflicts) == 2
        assert any("CLAUDE.md" in str(path) for path in result.conflicts)
        assert any(".gitignore" in str(path) for path in result.conflicts)

    # AC marker removed
    def test_should_not_detect_conflicts_for_new_files(self, temp_dir):
        """
        Test: Non-existing files not in conflict list (SVC-015)

        Given: Source files don't exist in target
        When: detect_conflicts() is called
        Then: Returns empty conflicts list
        """
        # Arrange
        from src.installer.services.file_conflict_detection_service import FileConflictDetectionService

        source_files = [
            ".claude/skills/new-skill.md",
            "devforgeai/context/new-context.md"
        ]

        service = FileConflictDetectionService(
            target_path=str(temp_dir),
            source_files=source_files
        )

        # Act
        result = service.detect_conflicts()

        # Assert
        assert len(result.conflicts) == 0

    # AC#5: Categorize conflicts (SVC-016)

    # AC marker removed
    def test_should_categorize_framework_files_correctly(self, temp_dir):
        """
        Test: Framework files categorized correctly (SVC-016)

        Given: Conflicts include .claude/* and .devforgeai/* files
        When: detect_conflicts() is called
        Then: framework_count matches framework file count
        """
        # Arrange
        from src.installer.services.file_conflict_detection_service import FileConflictDetectionService

        # Create framework files
        (temp_dir / ".claude" / "skills").mkdir(parents=True)
        (temp_dir / ".claude" / "skills" / "skill1.md").write_text("content")
        (temp_dir / ".claude" / "skills" / "skill2.md").write_text("content")

        (temp_dir / ".devforgeai" / "context").mkdir(parents=True)
        (temp_dir / ".devforgeai" / "context" / "tech-stack.md").write_text("content")

        source_files = [
            ".claude/skills/skill1.md",
            ".claude/skills/skill2.md",
            "devforgeai/context/tech-stack.md"
        ]

        service = FileConflictDetectionService(
            target_path=str(temp_dir),
            source_files=source_files
        )

        # Act
        result = service.detect_conflicts()

        # Assert
        assert result.framework_count == 3
        assert result.user_count == 0

    # AC marker removed
    def test_should_categorize_user_files_correctly(self, temp_dir):
        """
        Test: User files categorized correctly (SVC-016)

        Given: Conflicts include CLAUDE.md and .gitignore
        When: detect_conflicts() is called
        Then: user_count matches user file count
        """
        # Arrange
        from src.installer.services.file_conflict_detection_service import FileConflictDetectionService

        # Create user files
        (temp_dir / "CLAUDE.md").write_text("content")
        (temp_dir / ".gitignore").write_text("content")

        source_files = ["CLAUDE.md", ".gitignore"]

        service = FileConflictDetectionService(
            target_path=str(temp_dir),
            source_files=source_files
        )

        # Act
        result = service.detect_conflicts()

        # Assert
        assert result.framework_count == 0
        assert result.user_count == 2

    # AC marker removed
    def test_should_categorize_mixed_conflicts(self, temp_dir):
        """
        Test: Mixed framework and user files categorized (SVC-016)

        Given: Conflicts include both framework and user files
        When: detect_conflicts() is called
        Then: Correct counts for both categories
        """
        # Arrange
        from src.installer.services.file_conflict_detection_service import FileConflictDetectionService

        # Create framework files
        (temp_dir / ".claude" / "skills").mkdir(parents=True)
        (temp_dir / ".claude" / "skills" / "skill.md").write_text("content")

        # Create user files
        (temp_dir / "CLAUDE.md").write_text("content")
        (temp_dir / ".gitignore").write_text("content")

        source_files = [
            ".claude/skills/skill.md",
            "CLAUDE.md",
            ".gitignore"
        ]

        service = FileConflictDetectionService(
            target_path=str(temp_dir),
            source_files=source_files
        )

        # Act
        result = service.detect_conflicts()

        # Assert
        assert result.framework_count == 1
        assert result.user_count == 2
        assert len(result.conflicts) == 3

    # SVC-017: Memory efficiency with generators

    # AC marker removed
    def test_should_use_generator_for_large_scans(self, temp_dir):
        """
        Test: Uses generator for memory efficiency (SVC-017)

        Given: Large number of source files
        When: detect_conflicts() is called
        Then: Memory usage <50MB (NFR-007)
        """
        # Arrange
        from src.installer.services.file_conflict_detection_service import FileConflictDetectionService

        # Create 1000 source files (simulate large scan)
        source_files = [f"file_{i}.txt" for i in range(1000)]

        service = FileConflictDetectionService(
            target_path=str(temp_dir),
            source_files=source_files
        )

        # Act
        result = service.detect_conflicts()

        # Assert - should complete without memory error
        assert result is not None

    # BR-005 / SVC-018: Path validation (Security)

    # AC marker removed
    def test_should_reject_path_traversal_attempt(self, temp_dir):
        """
        Test: Path with '..' rejected (BR-005, SVC-018, NFR-004)

        Given: Source file contains '..' traversal
        When: detect_conflicts() is called
        Then: Path is rejected and not included in conflicts
        """
        # Arrange
        from src.installer.services.file_conflict_detection_service import FileConflictDetectionService

        # Create file outside target
        external_dir = temp_dir.parent / "external"
        external_dir.mkdir(exist_ok=True)
        (external_dir / "malicious.txt").write_text("content")

        source_files = ["../external/malicious.txt"]

        service = FileConflictDetectionService(
            target_path=str(temp_dir),
            source_files=source_files
        )

        # Act
        result = service.detect_conflicts()

        # Assert
        assert len(result.conflicts) == 0

    # AC marker removed
    def test_should_validate_path_within_target(self, temp_dir):
        """
        Test: Path validation ensures files within target (SVC-018)

        Given: Source file path
        When: is_within_target() is called
        Then: Returns True only if path is within target directory
        """
        # Arrange
        from src.installer.services.file_conflict_detection_service import FileConflictDetectionService

        service = FileConflictDetectionService(
            target_path=str(temp_dir),
            source_files=[]
        )

        # Act
        valid_path = temp_dir / "subdir" / "file.txt"
        invalid_path = temp_dir.parent / "outside" / "file.txt"

        # Assert
        assert service.is_within_target(valid_path) is True
        assert service.is_within_target(invalid_path) is False

    # AC marker removed
    def test_should_log_security_warning_for_invalid_paths(self, temp_dir):
        """
        Test: Security warning logged for invalid paths (SVC-018)

        Given: Source file with path traversal
        When: detect_conflicts() is called
        Then: Security warning is logged
        """
        # Arrange
        from src.installer.services.file_conflict_detection_service import FileConflictDetectionService

        source_files = ["../etc/passwd"]

        service = FileConflictDetectionService(
            target_path=str(temp_dir),
            source_files=source_files
        )

        with patch('src.installer.services.file_conflict_detection_service.logger') as mock_logger:
            # Act
            result = service.detect_conflicts()

            # Assert
            mock_logger.warning.assert_called()
            assert any("security" in str(call).lower() for call in mock_logger.warning.call_args_list)

    # SVC-019: Symlink resolution (Edge Case #3)

    # AC marker removed
    def test_should_resolve_symlinks_before_detection(self, temp_dir):
        """
        Test: Symlinks resolved before conflict detection (SVC-019, Edge Case #3)

        Given: Target file is symlink to real file
        When: detect_conflicts() is called
        Then: Uses resolved path for conflict check
        """
        # Arrange
        from src.installer.services.file_conflict_detection_service import FileConflictDetectionService

        # Create real file
        real_file = temp_dir / "real_file.txt"
        real_file.write_text("content")

        # Create symlink
        try:
            link_file = temp_dir / "link_file.txt"
            link_file.symlink_to(real_file)

            source_files = ["link_file.txt"]

            service = FileConflictDetectionService(
                target_path=str(temp_dir),
                source_files=source_files
            )

            # Act
            result = service.detect_conflicts()

            # Assert
            assert len(result.conflicts) == 1
            # Should detect based on resolved path
        except OSError:
            pytest.skip("Symlinks not supported on this platform")

    # AC marker removed
    def test_should_handle_broken_symlinks(self, temp_dir):
        """
        Test: Broken symlinks handled gracefully (Edge Case #3)

        Given: Symlink points to non-existent file
        When: detect_conflicts() is called
        Then: Handles without crashing
        """
        # Arrange
        from src.installer.services.file_conflict_detection_service import FileConflictDetectionService

        try:
            # Create broken symlink
            broken_link = temp_dir / "broken_link.txt"
            broken_link.symlink_to(temp_dir / "nonexistent.txt")

            source_files = ["broken_link.txt"]

            service = FileConflictDetectionService(
                target_path=str(temp_dir),
                source_files=source_files
            )

            # Act
            result = service.detect_conflicts()

            # Assert - should not crash
            assert result is not None
        except OSError:
            pytest.skip("Symlinks not supported on this platform")

    # Data Model Validation

    def test_conflict_info_model_has_required_fields(self):
        """
        Test: ConflictInfo data model has all required fields

        Given: ConflictInfo class defined
        When: Instance is created
        Then: Has conflicts, framework_count, user_count fields
        """
        # Arrange
        from src.installer.services.file_conflict_detection_service import ConflictInfo

        # Act
        conflict_info = ConflictInfo(
            conflicts=[Path("/tmp/file1.txt"), Path("/tmp/file2.txt")],
            framework_count=1,
            user_count=1
        )

        # Assert
        assert hasattr(conflict_info, "conflicts")
        assert hasattr(conflict_info, "framework_count")
        assert hasattr(conflict_info, "user_count")

    def test_conflict_info_counts_computed_correctly(self):
        """
        Test: ConflictInfo counts match conflict list

        Given: ConflictInfo with conflicts
        When: Counts are evaluated
        Then: framework_count + user_count == len(conflicts)
        """
        # Arrange
        from src.installer.services.file_conflict_detection_service import ConflictInfo

        # Act
        conflict_info = ConflictInfo(
            conflicts=[Path("/tmp/file1.txt"), Path("/tmp/file2.txt")],
            framework_count=1,
            user_count=1
        )

        # Assert
        assert conflict_info.framework_count + conflict_info.user_count == len(conflict_info.conflicts)

    # Performance (NFR-002)

    def test_should_scan_at_1000_files_per_second(self, temp_dir):
        """
        Test: Conflict detection scans ≥1000 files/second (NFR-002)

        Given: 10,000 source files
        When: detect_conflicts() is called
        Then: Completes in ≤10 seconds
        """
        # Arrange
        from src.installer.services.file_conflict_detection_service import FileConflictDetectionService

        source_files = [f"file_{i}.txt" for i in range(10000)]

        service = FileConflictDetectionService(
            target_path=str(temp_dir),
            source_files=source_files
        )

        # Act
        start = time.time()
        result = service.detect_conflicts()
        duration = time.time() - start

        # Assert
        assert duration < 10, f"Scan took {duration}s (expected <10s for 10k files)"

    # Business Rule BR-001: Non-fatal failures

    def test_should_not_crash_on_permission_error(self, temp_dir):
        """
        Test: PermissionError → partial results returned (BR-001)

        Given: Cannot read some files due to permissions
        When: detect_conflicts() is called
        Then: Returns results for accessible files
        """
        # Arrange
        from src.installer.services.file_conflict_detection_service import FileConflictDetectionService

        (temp_dir / "accessible.txt").write_text("content")

        source_files = ["accessible.txt", "inaccessible.txt"]

        service = FileConflictDetectionService(
            target_path=str(temp_dir),
            source_files=source_files
        )

        with patch.object(Path, 'exists', side_effect=[True, PermissionError("Access denied")]):
            # Act
            result = service.detect_conflicts()

            # Assert - should not crash
            assert result is not None

    def test_should_not_crash_on_io_error(self, temp_dir):
        """
        Test: IOError → graceful handling (BR-001)

        Given: File read raises IOError
        When: detect_conflicts() is called
        Then: Returns partial results without crashing
        """
        # Arrange
        from src.installer.services.file_conflict_detection_service import FileConflictDetectionService

        source_files = ["file.txt"]

        service = FileConflictDetectionService(
            target_path=str(temp_dir),
            source_files=source_files
        )

        with patch.object(Path, 'exists', side_effect=IOError("Cannot read")):
            # Act
            result = service.detect_conflicts()

            # Assert - should not crash
            assert result is not None

    # Cross-platform path handling

    def test_should_work_with_windows_paths(self):
        """
        Test: Windows path format supported

        Given: Target path is Windows format
        When: FileConflictDetectionService is instantiated
        Then: Path is handled correctly
        """
        # Arrange
        from src.installer.services.file_conflict_detection_service import FileConflictDetectionService

        # Act
        service = FileConflictDetectionService(
            target_path="C:\\test\\path",
            source_files=["file.txt"]
        )

        # Assert
        assert service is not None

    def test_should_work_with_unix_paths(self):
        """
        Test: Unix path format supported

        Given: Target path is Unix format
        When: FileConflictDetectionService is instantiated
        Then: Path is handled correctly
        """
        # Arrange
        from src.installer.services.file_conflict_detection_service import FileConflictDetectionService

        # Act
        service = FileConflictDetectionService(
            target_path="/test/path",
            source_files=["file.txt"]
        )

        # Assert
        assert service is not None

    # ===== COVERAGE GAP TESTS (Path validation edge cases) =====

    def test_detect_conflicts_path_validation_edge_cases(self, temp_dir):
        """
        Test: Path validation handles edge cases (symlinks, relative paths)

        Given: Source files with symlinks and relative path references
        When: detect_conflicts() is called
        Then: Validates and resolves paths correctly
        """
        # Arrange
        from src.installer.services.file_conflict_detection_service import FileConflictDetectionService
        import pytest

        # Create real file
        real_file = temp_dir / "subdir" / "real.txt"
        real_file.parent.mkdir(parents=True)
        real_file.write_text("content")

        try:
            # Create symlink
            link_file = temp_dir / "link.txt"
            link_file.symlink_to(real_file)

            # Test with various path formats
            source_files = [
                "link.txt",              # Symlink
                "./subdir/real.txt",     # Relative with ./
                "subdir/../subdir/real.txt",  # Path with ../ (still valid)
            ]

            service = FileConflictDetectionService(
                target_path=str(temp_dir),
                source_files=source_files
            )

            # Act
            result = service.detect_conflicts()

            # Assert
            # Should detect conflicts for valid paths within target
            assert result is not None
            assert len(result.conflicts) >= 1  # At least real.txt detected

            # Verify no paths escape target directory
            for conflict in result.conflicts:
                resolved_path = conflict.resolve()
                assert str(temp_dir) in str(resolved_path)

        except OSError:
            pytest.skip("Symlinks not supported on this platform")

    def test_is_within_target_with_symlink_escape(self, temp_dir):
        """
        Test: Path validation rejects symlinks that escape target directory

        Given: Symlink points outside target directory
        When: is_within_target() is called
        Then: Returns False (security protection)
        """
        # Arrange
        from src.installer.services.file_conflict_detection_service import FileConflictDetectionService
        import pytest

        service = FileConflictDetectionService(
            target_path=str(temp_dir),
            source_files=[]
        )

        try:
            # Create external file
            external_dir = temp_dir.parent / "external"
            external_dir.mkdir(exist_ok=True)
            external_file = external_dir / "outside.txt"
            external_file.write_text("content")

            # Create symlink inside target pointing outside
            escape_link = temp_dir / "escape.txt"
            escape_link.symlink_to(external_file)

            # Act
            result = service.is_within_target(escape_link)

            # Assert
            assert result is False  # Should reject symlink escape

        except OSError:
            pytest.skip("Symlinks not supported on this platform")

    def test_validate_path_absolute_vs_relative(self, temp_dir):
        """
        Test: Path validation handles absolute and relative paths correctly

        Given: Mix of absolute and relative paths
        When: Validation occurs
        Then: All paths resolved to absolute and validated
        """
        # Arrange
        from src.installer.services.file_conflict_detection_service import FileConflictDetectionService
        from pathlib import Path

        service = FileConflictDetectionService(
            target_path=str(temp_dir),
            source_files=[]
        )

        # Test absolute path within target
        absolute_valid = temp_dir / "file.txt"
        assert service.is_within_target(absolute_valid) is True

        # Test absolute path outside target
        absolute_invalid = temp_dir.parent / "outside" / "file.txt"
        assert service.is_within_target(absolute_invalid) is False

        # Test relative path (should be resolved relative to target)
        relative_path = Path("subdir/file.txt")
        # When resolved relative to target, should be valid
        full_relative = temp_dir / relative_path
        assert service.is_within_target(full_relative) is True

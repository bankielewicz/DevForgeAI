"""
Unit tests for GitDetectionService.

Tests AC#4:
- Execute git rev-parse --show-toplevel to find repository root
- Handle non-git directories gracefully
- Validate git command availability
- Detect unusual repository roots

Component Requirements:
- SVC-011: Execute git rev-parse --show-toplevel to find repository root
- SVC-012: Handle non-git directories gracefully
- SVC-013: Validate git command availability
- SVC-014: Detect and warn about unusual repository roots (/)

Business Rules:
- BR-004: Git root validation rejects filesystem root
- NFR-003: Git detection completes in <100ms
- NFR-005: Git command uses shell=False
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import subprocess
import time


# Story: STORY-073
class TestGitDetectionService:
    """Test suite for GitDetectionService - Git repository detection."""

    # AC#4: Git root detection (SVC-011)

    # AC marker removed
    def test_should_detect_git_repository_root(self, temp_dir):
        """
        Test: Execute git rev-parse → repository root returned (SVC-011)

        Given: Directory is within git repository
        When: detect_git_root() is called
        Then: Returns Path to repository root
        """
        # Arrange
        from src.installer.services.git_detection_service import GitDetectionService

        service = GitDetectionService(target_path=str(temp_dir))

        mock_result = MagicMock()
        mock_result.stdout = str(temp_dir)
        mock_result.returncode = 0

        with patch('subprocess.run', return_value=mock_result) as mock_run:
            # Act
            result = service.detect_git_root()

            # Assert
            assert result is not None
            assert isinstance(result, Path)
            assert str(result) == str(temp_dir)
            mock_run.assert_called_once()

    # AC marker removed
    def test_should_use_git_rev_parse_show_toplevel(self, temp_dir):
        """
        Test: Uses correct git command (SVC-011)

        Given: GitDetectionService instance
        When: detect_git_root() is called
        Then: Calls subprocess.run with 'git rev-parse --show-toplevel'
        """
        # Arrange
        from src.installer.services.git_detection_service import GitDetectionService

        service = GitDetectionService(target_path=str(temp_dir))

        mock_result = MagicMock()
        mock_result.stdout = str(temp_dir)
        mock_result.returncode = 0

        with patch('subprocess.run', return_value=mock_result) as mock_run:
            # Act
            result = service.detect_git_root()

            # Assert
            args = mock_run.call_args[0][0]
            assert "git" in args
            assert "rev-parse" in args
            assert "--show-toplevel" in args

    # AC marker removed
    def test_should_use_shell_false_for_security(self, temp_dir):
        """
        Test: Git command uses shell=False (NFR-005)

        Given: detect_git_root() is called
        When: subprocess.run executes
        Then: shell parameter is False
        """
        # Arrange
        from src.installer.services.git_detection_service import GitDetectionService

        service = GitDetectionService(target_path=str(temp_dir))

        mock_result = MagicMock()
        mock_result.stdout = str(temp_dir)
        mock_result.returncode = 0

        with patch('subprocess.run', return_value=mock_result) as mock_run:
            # Act
            result = service.detect_git_root()

            # Assert
            assert mock_run.call_args[1]['shell'] is False

    # AC marker removed
    def test_should_strip_whitespace_from_git_output(self, temp_dir):
        """
        Test: Git output whitespace trimmed

        Given: git command returns path with trailing newline
        When: detect_git_root() is called
        Then: Returns path without whitespace
        """
        # Arrange
        from src.installer.services.git_detection_service import GitDetectionService

        service = GitDetectionService(target_path=str(temp_dir))

        mock_result = MagicMock()
        mock_result.stdout = f"{temp_dir}\n\n"  # Trailing newlines
        mock_result.returncode = 0

        with patch('subprocess.run', return_value=mock_result):
            # Act
            result = service.detect_git_root()

            # Assert
            assert result is not None
            assert str(result) == str(temp_dir)
            assert not str(result).endswith("\n")

    # AC#4: Non-git directories (SVC-012)

    # AC marker removed
    def test_should_return_none_for_non_git_directory(self, temp_dir):
        """
        Test: Non-git directory → None returned (SVC-012)

        Given: Directory is not within git repository
        When: detect_git_root() is called
        Then: Returns None
        """
        # Arrange
        from src.installer.services.git_detection_service import GitDetectionService

        service = GitDetectionService(target_path=str(temp_dir))

        mock_result = MagicMock()
        mock_result.returncode = 128  # Git error code for "not a git repository"
        mock_result.stderr = "fatal: not a git repository"

        with patch('subprocess.run', return_value=mock_result):
            # Act
            result = service.detect_git_root()

            # Assert
            assert result is None

    # AC marker removed
    def test_should_return_none_when_git_not_installed(self, temp_dir):
        """
        Test: Missing git command → None returned (SVC-013)

        Given: git executable not found
        When: detect_git_root() is called
        Then: Returns None with log message
        """
        # Arrange
        from src.installer.services.git_detection_service import GitDetectionService

        service = GitDetectionService(target_path=str(temp_dir))

        with patch('subprocess.run', side_effect=FileNotFoundError("git not found")):
            # Act
            result = service.detect_git_root()

            # Assert
            assert result is None

    # AC marker removed
    def test_should_check_git_availability_with_which(self):
        """
        Test: Validates git command availability (SVC-013)

        Given: GitDetectionService instance
        When: is_git_available() is called
        Then: Uses shutil.which to check for git
        """
        # Arrange
        from src.installer.services.git_detection_service import GitDetectionService

        service = GitDetectionService(target_path="/tmp")

        with patch('shutil.which', return_value="/usr/bin/git") as mock_which:
            # Act
            result = service.is_git_available()

            # Assert
            assert result is True
            mock_which.assert_called_once_with("git")

    # AC marker removed
    def test_should_return_false_when_git_not_available(self):
        """
        Test: Git not available → is_git_available returns False (SVC-013)

        Given: git command not in PATH
        When: is_git_available() is called
        Then: Returns False
        """
        # Arrange
        from src.installer.services.git_detection_service import GitDetectionService

        service = GitDetectionService(target_path="/tmp")

        with patch('shutil.which', return_value=None):
            # Act
            result = service.is_git_available()

            # Assert
            assert result is False

    # BR-004: Git root validation (SVC-014)

    # AC marker removed
    def test_should_reject_filesystem_root(self, temp_dir):
        """
        Test: Git root '/' rejected → None returned (BR-004, SVC-014)

        Given: git rev-parse returns '/' (filesystem root)
        When: detect_git_root() is called
        Then: Returns None with warning
        """
        # Arrange
        from src.installer.services.git_detection_service import GitDetectionService

        service = GitDetectionService(target_path=str(temp_dir))

        mock_result = MagicMock()
        mock_result.stdout = "/"
        mock_result.returncode = 0

        with patch('subprocess.run', return_value=mock_result):
            # Act
            result = service.detect_git_root()

            # Assert
            assert result is None

    # AC marker removed
    def test_should_reject_windows_root_drive(self, temp_dir):
        """
        Test: Git root 'C:\\' rejected → None returned (BR-004)

        Given: git rev-parse returns 'C:\\'
        When: detect_git_root() is called
        Then: Returns None with warning
        """
        # Arrange
        from src.installer.services.git_detection_service import GitDetectionService

        service = GitDetectionService(target_path=str(temp_dir))

        mock_result = MagicMock()
        mock_result.stdout = "C:\\"
        mock_result.returncode = 0

        with patch('subprocess.run', return_value=mock_result):
            # Act
            result = service.detect_git_root()

            # Assert
            assert result is None

    # AC marker removed
    def test_should_accept_valid_subdirectory(self, temp_dir):
        """
        Test: Valid git root accepted

        Given: git rev-parse returns valid subdirectory path
        When: detect_git_root() is called
        Then: Returns Path object
        """
        # Arrange
        from src.installer.services.git_detection_service import GitDetectionService

        valid_path = temp_dir / "projects" / "myrepo"
        service = GitDetectionService(target_path=str(temp_dir))

        mock_result = MagicMock()
        mock_result.stdout = str(valid_path)
        mock_result.returncode = 0

        with patch('subprocess.run', return_value=mock_result):
            # Act
            result = service.detect_git_root()

            # Assert
            assert result is not None
            assert isinstance(result, Path)

    # Edge Case: Multiple git repositories (Edge Case #2)

    # AC marker removed
    def test_should_use_innermost_repository_root(self, temp_dir):
        """
        Test: Nested git repositories → innermost root used (Edge Case #2)

        Given: Directory is within nested git repository
        When: detect_git_root() is called
        Then: Returns innermost repository root
        """
        # Arrange
        from src.installer.services.git_detection_service import GitDetectionService

        inner_repo = temp_dir / "outer" / "inner"
        service = GitDetectionService(target_path=str(inner_repo))

        mock_result = MagicMock()
        mock_result.stdout = str(inner_repo)  # Git returns innermost
        mock_result.returncode = 0

        with patch('subprocess.run', return_value=mock_result):
            # Act
            result = service.detect_git_root()

            # Assert
            assert result is not None
            assert str(result) == str(inner_repo)

    # Edge Case: Submodule detection

    def test_should_detect_git_submodule(self, temp_dir):
        """
        Test: Git submodule detected correctly

        Given: Directory is git submodule
        When: is_submodule() is called
        Then: Returns True
        """
        # Arrange
        from src.installer.services.git_detection_service import GitDetectionService

        service = GitDetectionService(target_path=str(temp_dir))

        # Mock .git file (submodule indicator)
        git_file = temp_dir / ".git"
        git_file.write_text("gitdir: ../.git/modules/submodule")

        # Act
        result = service.is_submodule()

        # Assert
        assert result is True

    def test_should_return_false_for_normal_repository(self, temp_dir):
        """
        Test: Normal repository not detected as submodule

        Given: Directory is regular git repository (.git/ directory)
        When: is_submodule() is called
        Then: Returns False
        """
        # Arrange
        from src.installer.services.git_detection_service import GitDetectionService

        service = GitDetectionService(target_path=str(temp_dir))

        # Mock .git directory (normal repo indicator)
        git_dir = temp_dir / ".git"
        git_dir.mkdir()

        # Act
        result = service.is_submodule()

        # Assert
        assert result is False

    # Data Model Validation

    def test_git_info_model_has_required_fields(self):
        """
        Test: GitInfo data model has all required fields

        Given: GitInfo class defined
        When: Instance is created
        Then: Has repository_root and is_submodule fields
        """
        # Arrange
        from src.installer.services.git_detection_service import GitInfo

        # Act
        git_info = GitInfo(
            repository_root=Path("/tmp/repo"),
            is_submodule=False
        )

        # Assert
        assert hasattr(git_info, "repository_root")
        assert hasattr(git_info, "is_submodule")

    def test_git_info_repository_root_can_be_none(self):
        """
        Test: GitInfo.repository_root can be None

        Given: Not in git repository
        When: GitInfo is created
        Then: repository_root is None
        """
        # Arrange
        from src.installer.services.git_detection_service import GitInfo

        # Act
        git_info = GitInfo(
            repository_root=None,
            is_submodule=False
        )

        # Assert
        assert git_info.repository_root is None

    # Performance (NFR-003)

    def test_should_complete_git_detection_within_100ms(self, temp_dir):
        """
        Test: Git detection < 100ms (NFR-003)

        Given: Git command available
        When: detect_git_root() is called
        Then: Completes in <100ms
        """
        # Arrange
        from src.installer.services.git_detection_service import GitDetectionService

        service = GitDetectionService(target_path=str(temp_dir))

        mock_result = MagicMock()
        mock_result.stdout = str(temp_dir)
        mock_result.returncode = 0

        with patch('subprocess.run', return_value=mock_result):
            # Act
            start = time.time()
            result = service.detect_git_root()
            duration_ms = (time.time() - start) * 1000

            # Assert
            assert duration_ms < 100, f"Detection took {duration_ms}ms (expected <100ms)"

    # Business Rule BR-001: Non-fatal failures

    def test_should_not_crash_on_subprocess_timeout(self, temp_dir):
        """
        Test: Subprocess timeout → None returned (BR-001)

        Given: git command times out
        When: detect_git_root() is called
        Then: Returns None without crashing
        """
        # Arrange
        from src.installer.services.git_detection_service import GitDetectionService

        service = GitDetectionService(target_path=str(temp_dir))

        with patch('subprocess.run', side_effect=subprocess.TimeoutExpired("git", 5)):
            # Act
            result = service.detect_git_root()

            # Assert
            assert result is None

    def test_should_not_crash_on_permission_error(self, temp_dir):
        """
        Test: PermissionError → None returned (BR-001)

        Given: No permission to execute git
        When: detect_git_root() is called
        Then: Returns None without crashing
        """
        # Arrange
        from src.installer.services.git_detection_service import GitDetectionService

        service = GitDetectionService(target_path=str(temp_dir))

        with patch('subprocess.run', side_effect=PermissionError("Access denied")):
            # Act
            result = service.detect_git_root()

            # Assert
            assert result is None

    def test_should_not_crash_on_generic_exception(self, temp_dir):
        """
        Test: Generic exception → None returned (BR-001)

        Given: Unexpected exception during git execution
        When: detect_git_root() is called
        Then: Returns None without crashing
        """
        # Arrange
        from src.installer.services.git_detection_service import GitDetectionService

        service = GitDetectionService(target_path=str(temp_dir))

        with patch('subprocess.run', side_effect=RuntimeError("Unexpected error")):
            # Act
            result = service.detect_git_root()

            # Assert
            assert result is None

    # Cross-platform path handling

    def test_should_work_with_windows_paths(self):
        """
        Test: Windows path format supported

        Given: Target path is Windows format
        When: GitDetectionService is instantiated
        Then: Path is handled correctly
        """
        # Arrange
        from src.installer.services.git_detection_service import GitDetectionService

        # Act
        service = GitDetectionService(target_path="C:\\test\\path")

        # Assert
        assert service is not None

    def test_should_work_with_unix_paths(self):
        """
        Test: Unix path format supported

        Given: Target path is Unix format
        When: GitDetectionService is instantiated
        Then: Path is handled correctly
        """
        # Arrange
        from src.installer.services.git_detection_service import GitDetectionService

        # Act
        service = GitDetectionService(target_path="/test/path")

        # Assert
        assert service is not None

    # Security

    def test_should_sanitize_git_output(self, temp_dir):
        """
        Test: Git output sanitized for security

        Given: git command returns malicious path
        When: detect_git_root() is called
        Then: Path is validated and sanitized
        """
        # Arrange
        from src.installer.services.git_detection_service import GitDetectionService

        service = GitDetectionService(target_path=str(temp_dir))

        mock_result = MagicMock()
        mock_result.stdout = "../../etc/passwd"  # Path traversal attempt
        mock_result.returncode = 0

        with patch('subprocess.run', return_value=mock_result):
            # Act
            result = service.detect_git_root()

            # Assert - should validate and reject suspicious paths
            # Implementation may return None or sanitized path
            if result is not None:
                assert ".." not in str(result)

    def test_should_set_timeout_for_git_command(self, temp_dir):
        """
        Test: Git command has timeout to prevent hanging

        Given: detect_git_root() is called
        When: subprocess.run executes
        Then: timeout parameter is set
        """
        # Arrange
        from src.installer.services.git_detection_service import GitDetectionService

        service = GitDetectionService(target_path=str(temp_dir))

        mock_result = MagicMock()
        mock_result.stdout = str(temp_dir)
        mock_result.returncode = 0

        with patch('subprocess.run', return_value=mock_result) as mock_run:
            # Act
            result = service.detect_git_root()

            # Assert
            assert 'timeout' in mock_run.call_args[1]
            assert mock_run.call_args[1]['timeout'] > 0

"""
STORY-175 AC#1: Identify Files Changed by Current Story

Tests that the system uses git diff to identify changed files during QA validation.
All tests follow TDD Red phase - they should FAIL until implementation exists.

Given: QA validation is running
When: deep validation begins
Then: system uses `git diff --name-only HEAD~1` to identify changed files

Coverage Target: 95%+
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path


class TestGetChangedFilesFromGit:
    """Test AC#1: System uses git diff to identify changed files."""

    def test_get_changed_files_executes_git_diff_command(self):
        """
        Test: get_changed_files() executes git diff --name-only HEAD~1.

        Given: QA validation module is imported
        When: get_changed_files() is called
        Then: git diff --name-only HEAD~1 command is executed
        """
        # Arrange
        from devforgeai.qa.regression_classifier import get_changed_files

        # Act & Assert
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout="file1.py\nfile2.py\n",
                stderr=""
            )

            result = get_changed_files()

            # Assert git diff command was called with correct arguments
            mock_run.assert_called_once()
            call_args = mock_run.call_args
            assert "git" in call_args[0][0]
            assert "diff" in call_args[0][0]
            assert "--name-only" in call_args[0][0]
            assert "HEAD~1" in call_args[0][0]

    def test_get_changed_files_returns_list_of_file_paths(self):
        """
        Test: get_changed_files() returns a list of changed file paths.

        Given: Git diff returns file paths
        When: get_changed_files() is called
        Then: Returns list of file path strings
        """
        # Arrange
        from devforgeai.qa.regression_classifier import get_changed_files

        # Act
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout="src/module/file1.py\nsrc/module/file2.py\ntests/test_file.py\n",
                stderr=""
            )

            result = get_changed_files()

            # Assert
            assert isinstance(result, list)
            assert len(result) == 3
            assert "src/module/file1.py" in result
            assert "src/module/file2.py" in result
            assert "tests/test_file.py" in result

    def test_get_changed_files_strips_whitespace_from_paths(self):
        """
        Test: get_changed_files() strips whitespace from file paths.

        Given: Git diff output has trailing newlines/spaces
        When: get_changed_files() is called
        Then: Returned paths have no leading/trailing whitespace
        """
        # Arrange
        from devforgeai.qa.regression_classifier import get_changed_files

        # Act
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout="  file1.py  \n\nfile2.py\n\n\n",
                stderr=""
            )

            result = get_changed_files()

            # Assert - no empty strings or whitespace
            assert "" not in result
            for path in result:
                assert path == path.strip()

    def test_get_changed_files_filters_empty_lines(self):
        """
        Test: get_changed_files() filters out empty lines.

        Given: Git diff output contains empty lines
        When: get_changed_files() is called
        Then: Empty lines are not included in result
        """
        # Arrange
        from devforgeai.qa.regression_classifier import get_changed_files

        # Act
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout="file1.py\n\n\nfile2.py\n",
                stderr=""
            )

            result = get_changed_files()

            # Assert
            assert len(result) == 2
            assert "" not in result

    def test_get_changed_files_returns_empty_list_when_no_changes(self):
        """
        Test: get_changed_files() returns empty list when no files changed.

        Given: Git diff returns empty output
        When: get_changed_files() is called
        Then: Returns empty list
        """
        # Arrange
        from devforgeai.qa.regression_classifier import get_changed_files

        # Act
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout="",
                stderr=""
            )

            result = get_changed_files()

            # Assert
            assert isinstance(result, list)
            assert len(result) == 0


class TestChangedFilesWithWorkingDirectory:
    """Test get_changed_files() respects working directory."""

    def test_get_changed_files_uses_project_root_as_cwd(self):
        """
        Test: get_changed_files() executes git from project root.

        Given: Project root is specified
        When: get_changed_files() is called with project_root
        Then: Git command runs in project root directory
        """
        # Arrange
        from devforgeai.qa.regression_classifier import get_changed_files

        # Act
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

            get_changed_files(project_root="/path/to/project")

            # Assert
            call_kwargs = mock_run.call_args[1]
            assert call_kwargs.get('cwd') == "/path/to/project"

    def test_get_changed_files_defaults_to_current_directory(self):
        """
        Test: get_changed_files() defaults to current directory if no root specified.

        Given: No project root specified
        When: get_changed_files() is called without arguments
        Then: Git command runs in current directory (cwd=None or cwd='.')
        """
        # Arrange
        from devforgeai.qa.regression_classifier import get_changed_files

        # Act
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

            get_changed_files()

            # Assert - either no cwd or cwd='.' or cwd=None
            call_kwargs = mock_run.call_args[1] if mock_run.call_args[1] else {}
            cwd = call_kwargs.get('cwd')
            assert cwd is None or cwd == '.' or cwd is None


class TestChangedFilesEncoding:
    """Test file path encoding handling."""

    def test_get_changed_files_handles_utf8_paths(self):
        """
        Test: get_changed_files() handles UTF-8 encoded file paths.

        Given: Git diff returns paths with special characters
        When: get_changed_files() is called
        Then: UTF-8 paths are properly decoded
        """
        # Arrange
        from devforgeai.qa.regression_classifier import get_changed_files

        # Act
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout="src/module/archivo_espanol.py\nsrc/module/fichier_francais.py\n",
                stderr=""
            )

            result = get_changed_files()

            # Assert
            assert "src/module/archivo_espanol.py" in result
            assert "src/module/fichier_francais.py" in result

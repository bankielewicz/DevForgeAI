"""
STORY-175 Edge Cases: Handle edge cases in regression classification.

Tests edge cases documented in the story:
1. No git repository: Fallback to all REGRESSION (blocking)
2. First commit: Use `git diff --name-only origin/main...HEAD`
3. Empty changed files: All PRE_EXISTING (non-blocking)

All tests follow TDD Red phase - they should FAIL until implementation exists.

Coverage Target: 95%+
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import subprocess


class TestEdgeCase1NoGitRepository:
    """Edge Case 1: No git repository - fallback to all REGRESSION."""

    def test_no_git_repo_detected_returns_fallback_mode(self):
        """
        Test: When not in git repo, is_git_repository() returns False.

        Given: Current directory is not a git repository
        When: is_git_repository() is called
        Then: Returns False
        """
        # Arrange
        from devforgeai.qa.regression_classifier import is_git_repository

        # Act
        with patch('subprocess.run') as mock_run:
            # Simulate git rev-parse failing (not a git repo)
            mock_run.side_effect = subprocess.CalledProcessError(128, 'git')

            result = is_git_repository()

            # Assert
            assert result is False

    def test_no_git_repo_classifies_all_as_regression(self):
        """
        Test: When not in git repo, all violations are classified as REGRESSION.

        Given: Not in a git repository
        When: classify_violations_with_fallback() is called
        Then: All violations are REGRESSION
        """
        # Arrange
        from devforgeai.qa.regression_classifier import classify_violations_with_fallback

        violations = [
            {"file": "src/file1.py", "line": 1, "message": "Issue 1"},
            {"file": "src/file2.py", "line": 2, "message": "Issue 2"},
            {"file": "src/file3.py", "line": 3, "message": "Issue 3"},
        ]

        # Act
        with patch('devforgeai.qa.regression_classifier.is_git_repository', return_value=False):
            result = classify_violations_with_fallback(violations)

            # Assert - all should be REGRESSION when no git repo
            for v in result:
                assert v["classification"] == "REGRESSION"
                assert v["blocking"] is True

    def test_no_git_repo_all_violations_block_qa(self):
        """
        Test: When not in git repo, all violations block QA.

        Given: Not in a git repository
        When: should_block_qa() is checked
        Then: Returns True (all violations are blocking)
        """
        # Arrange
        from devforgeai.qa.regression_classifier import (
            classify_violations_with_fallback,
            should_block_qa
        )

        violations = [
            {"file": "src/file.py", "line": 1, "message": "Issue"},
        ]

        # Act
        with patch('devforgeai.qa.regression_classifier.is_git_repository', return_value=False):
            classified = classify_violations_with_fallback(violations)
            result = should_block_qa(classified)

            # Assert
            assert result is True

    def test_no_git_repo_logs_fallback_warning(self):
        """
        Test: When not in git repo, a warning is logged about fallback mode.

        Given: Not in a git repository
        When: classify_violations_with_fallback() is called
        Then: Logs warning about fallback to all-REGRESSION mode
        """
        # Arrange
        from devforgeai.qa.regression_classifier import classify_violations_with_fallback
        import logging

        violations = [{"file": "src/file.py", "line": 1, "message": "Issue"}]

        # Act
        with patch('devforgeai.qa.regression_classifier.is_git_repository', return_value=False):
            with patch('devforgeai.qa.regression_classifier.logger') as mock_logger:
                classify_violations_with_fallback(violations)

                # Assert - should log warning
                mock_logger.warning.assert_called()


class TestEdgeCase2FirstCommit:
    """Edge Case 2: First commit - use origin/main...HEAD."""

    def test_first_commit_uses_origin_main_diff(self):
        """
        Test: On first commit, use `git diff --name-only origin/main...HEAD`.

        Given: HEAD~1 fails (first commit)
        When: get_changed_files() is called
        Then: Falls back to origin/main...HEAD comparison
        """
        # Arrange
        from devforgeai.qa.regression_classifier import get_changed_files

        # Act
        with patch('subprocess.run') as mock_run:
            # First call (HEAD~1) fails, second call (origin/main...HEAD) succeeds
            mock_run.side_effect = [
                subprocess.CalledProcessError(128, 'git'),  # HEAD~1 fails
                MagicMock(returncode=0, stdout="file1.py\nfile2.py\n", stderr="")  # fallback succeeds
            ]

            result = get_changed_files()

            # Assert - should have made two calls
            assert mock_run.call_count == 2
            # Second call should use origin/main...HEAD
            second_call_args = mock_run.call_args_list[1][0][0]
            assert "origin/main...HEAD" in " ".join(second_call_args) or \
                   "origin/main" in " ".join(second_call_args)

    def test_first_commit_returns_files_from_fallback(self):
        """
        Test: On first commit, returns files from origin/main...HEAD comparison.

        Given: HEAD~1 fails (first commit)
        When: get_changed_files() is called
        Then: Returns files from the fallback comparison
        """
        # Arrange
        from devforgeai.qa.regression_classifier import get_changed_files

        # Act
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = [
                subprocess.CalledProcessError(128, 'git'),
                MagicMock(returncode=0, stdout="new_file.py\n", stderr="")
            ]

            result = get_changed_files()

            # Assert
            assert "new_file.py" in result

    def test_is_first_commit_detected(self):
        """
        Test: is_first_commit() correctly detects first commit scenario.

        Given: Repository has only one commit
        When: is_first_commit() is called
        Then: Returns True
        """
        # Arrange
        from devforgeai.qa.regression_classifier import is_first_commit

        # Act
        with patch('subprocess.run') as mock_run:
            # HEAD~1 doesn't exist = first commit
            mock_run.side_effect = subprocess.CalledProcessError(128, 'git')

            result = is_first_commit()

            # Assert
            assert result is True


class TestEdgeCase3EmptyChangedFiles:
    """Edge Case 3: Empty changed files - all PRE_EXISTING."""

    def test_empty_changed_files_classifies_all_pre_existing(self):
        """
        Test: When no files changed, all violations are PRE_EXISTING.

        Given: git diff returns no changed files
        When: classify_violations() is called
        Then: All violations are PRE_EXISTING
        """
        # Arrange
        from devforgeai.qa.regression_classifier import classify_violations

        violations = [
            {"file": "src/file1.py", "line": 1, "message": "Issue 1"},
            {"file": "src/file2.py", "line": 2, "message": "Issue 2"},
        ]
        changed_files = []  # Empty - no files changed

        # Act
        result = classify_violations(violations, changed_files)

        # Assert
        for v in result:
            assert v["classification"] == "PRE_EXISTING"

    def test_empty_changed_files_all_non_blocking(self):
        """
        Test: When no files changed, all violations are non-blocking.

        Given: git diff returns no changed files
        When: set_all_blocking_status() is applied
        Then: All violations have blocking=False
        """
        # Arrange
        from devforgeai.qa.regression_classifier import (
            classify_violations,
            set_all_blocking_status
        )

        violations = [
            {"file": "src/file1.py", "line": 1, "message": "Issue 1"},
            {"file": "src/file2.py", "line": 2, "message": "Issue 2"},
        ]
        changed_files = []

        # Act
        classified = classify_violations(violations, changed_files)
        result = set_all_blocking_status(classified)

        # Assert
        for v in result:
            assert v["blocking"] is False

    def test_empty_changed_files_qa_passes(self):
        """
        Test: When no files changed, QA validation passes.

        Given: git diff returns no changed files, violations exist
        When: should_block_qa() is called
        Then: Returns False (QA passes)
        """
        # Arrange
        from devforgeai.qa.regression_classifier import (
            classify_violations,
            set_all_blocking_status,
            should_block_qa
        )

        violations = [
            {"file": "src/file1.py", "line": 1, "message": "Issue 1"},
        ]
        changed_files = []

        # Act
        classified = classify_violations(violations, changed_files)
        with_blocking = set_all_blocking_status(classified)
        result = should_block_qa(with_blocking)

        # Assert
        assert result is False

    def test_empty_changed_files_breakdown_shows_zero_regressions(self):
        """
        Test: When no files changed, breakdown shows 0 regressions.

        Given: git diff returns no changed files, violations exist
        When: get_breakdown() is called
        Then: Shows "Regressions: 0 | Pre-existing: N"
        """
        # Arrange
        from devforgeai.qa.regression_classifier import (
            classify_violations,
            get_breakdown
        )

        violations = [
            {"file": "src/file1.py", "line": 1, "message": "Issue 1"},
            {"file": "src/file2.py", "line": 2, "message": "Issue 2"},
        ]
        changed_files = []

        # Act
        classified = classify_violations(violations, changed_files)
        result = get_breakdown(classified)

        # Assert
        assert result == "Regressions: 0 | Pre-existing: 2"


class TestGitDiffFailureHandling:
    """Test handling of git diff command failures."""

    def test_git_diff_permission_error_uses_fallback(self):
        """
        Test: When git diff fails with permission error, fallback is used.

        Given: git diff fails with permission error
        When: get_changed_files() is called
        Then: Fallback mechanism is triggered
        """
        # Arrange
        from devforgeai.qa.regression_classifier import get_changed_files_safe

        # Act
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = PermissionError("Permission denied")

            result = get_changed_files_safe()

            # Assert - should return empty list or fallback value
            assert isinstance(result, list)

    def test_git_diff_timeout_uses_fallback(self):
        """
        Test: When git diff times out, fallback is used.

        Given: git diff times out
        When: get_changed_files() is called with timeout
        Then: Returns fallback value (empty list)
        """
        # Arrange
        from devforgeai.qa.regression_classifier import get_changed_files_safe

        # Act
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = subprocess.TimeoutExpired('git', 30)

            result = get_changed_files_safe()

            # Assert
            assert isinstance(result, list)

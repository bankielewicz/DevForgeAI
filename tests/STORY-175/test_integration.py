"""
STORY-175 Integration Tests: End-to-end regression classification workflow.

Tests the complete flow from git diff to classified violations with blocking status.
All tests follow TDD Red phase - they should FAIL until implementation exists.

Coverage Target: 95%+
"""

import pytest
from unittest.mock import Mock, patch, MagicMock


class TestFullClassificationWorkflow:
    """Integration tests for complete classification workflow."""

    def test_full_workflow_classifies_and_sets_blocking(self):
        """
        Test: Complete workflow from violations to classified + blocking violations.

        Given: List of violations and git diff output
        When: Full classification workflow runs
        Then: All violations have classification and blocking status
        """
        # Arrange
        from devforgeai.qa.regression_classifier import run_classification_workflow

        violations = [
            {"file": "src/changed.py", "line": 1, "message": "Issue in changed"},
            {"file": "src/old.py", "line": 2, "message": "Issue in old"},
        ]

        # Act
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout="src/changed.py\n",
                stderr=""
            )

            result = run_classification_workflow(violations)

            # Assert
            assert len(result) == 2

            # First violation (in changed file) - REGRESSION, blocking
            assert result[0]["classification"] == "REGRESSION"
            assert result[0]["blocking"] is True

            # Second violation (in old file) - PRE_EXISTING, non-blocking
            assert result[1]["classification"] == "PRE_EXISTING"
            assert result[1]["blocking"] is False

    def test_full_workflow_with_multiple_changed_files(self):
        """
        Test: Workflow correctly handles multiple changed files.

        Given: Multiple files changed, violations in some of them
        When: Full classification workflow runs
        Then: Correct classification based on file membership
        """
        # Arrange
        from devforgeai.qa.regression_classifier import run_classification_workflow

        violations = [
            {"file": "src/api/endpoint.py", "line": 10, "message": "API issue"},
            {"file": "src/service/logic.py", "line": 20, "message": "Service issue"},
            {"file": "src/utils/helper.py", "line": 30, "message": "Util issue"},
            {"file": "src/legacy/old_code.py", "line": 40, "message": "Legacy issue"},
        ]

        # Act
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout="src/api/endpoint.py\nsrc/service/logic.py\n",
                stderr=""
            )

            result = run_classification_workflow(violations)

            # Assert
            assert result[0]["classification"] == "REGRESSION"  # endpoint.py changed
            assert result[1]["classification"] == "REGRESSION"  # logic.py changed
            assert result[2]["classification"] == "PRE_EXISTING"  # helper.py not changed
            assert result[3]["classification"] == "PRE_EXISTING"  # old_code.py not changed

    def test_full_workflow_generates_correct_breakdown(self):
        """
        Test: Workflow generates correct breakdown string.

        Given: Mixed violations
        When: Full workflow runs including breakdown
        Then: Breakdown string is accurate
        """
        # Arrange
        from devforgeai.qa.regression_classifier import (
            run_classification_workflow,
            get_breakdown
        )

        violations = [
            {"file": "src/changed1.py", "line": 1, "message": "Issue 1"},
            {"file": "src/changed2.py", "line": 2, "message": "Issue 2"},
            {"file": "src/old1.py", "line": 3, "message": "Issue 3"},
            {"file": "src/old2.py", "line": 4, "message": "Issue 4"},
            {"file": "src/old3.py", "line": 5, "message": "Issue 5"},
        ]

        # Act
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout="src/changed1.py\nsrc/changed2.py\n",
                stderr=""
            )

            classified = run_classification_workflow(violations)
            breakdown = get_breakdown(classified)

            # Assert
            assert breakdown == "Regressions: 2 | Pre-existing: 3"


class TestQADecisionIntegration:
    """Integration tests for QA pass/fail decision."""

    def test_qa_decision_integration_with_regressions(self):
        """
        Test: QA decision correctly blocks when regressions exist.

        Given: Some violations are in changed files
        When: Full workflow + QA decision
        Then: QA is blocked
        """
        # Arrange
        from devforgeai.qa.regression_classifier import (
            run_classification_workflow,
            should_block_qa
        )

        violations = [
            {"file": "src/changed.py", "line": 1, "message": "Regression"},
            {"file": "src/old.py", "line": 2, "message": "Pre-existing"},
        ]

        # Act
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout="src/changed.py\n",
                stderr=""
            )

            classified = run_classification_workflow(violations)
            should_block = should_block_qa(classified)

            # Assert
            assert should_block is True

    def test_qa_decision_integration_without_regressions(self):
        """
        Test: QA decision passes when no regressions.

        Given: All violations are in unchanged files
        When: Full workflow + QA decision
        Then: QA passes
        """
        # Arrange
        from devforgeai.qa.regression_classifier import (
            run_classification_workflow,
            should_block_qa
        )

        violations = [
            {"file": "src/old1.py", "line": 1, "message": "Pre-existing 1"},
            {"file": "src/old2.py", "line": 2, "message": "Pre-existing 2"},
        ]

        # Act
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout="src/unrelated.py\n",  # No overlap with violations
                stderr=""
            )

            classified = run_classification_workflow(violations)
            should_block = should_block_qa(classified)

            # Assert
            assert should_block is False


class TestReportGenerationIntegration:
    """Integration tests for report generation with classification."""

    def test_report_includes_classification_breakdown(self):
        """
        Test: Generated report includes classification breakdown line.

        Given: Classified violations
        When: Report is generated
        Then: Report includes breakdown in correct format
        """
        # Arrange
        from devforgeai.qa.regression_classifier import (
            run_classification_workflow,
            generate_qa_report_section
        )

        violations = [
            {"file": "src/changed.py", "line": 1, "message": "Issue", "severity": "HIGH"},
        ]

        # Act
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout="src/changed.py\n",
                stderr=""
            )

            classified = run_classification_workflow(violations)
            report_section = generate_qa_report_section(classified)

            # Assert
            assert "Regressions:" in report_section
            assert "Pre-existing:" in report_section
            assert "|" in report_section

    def test_report_section_shows_blocking_status(self):
        """
        Test: Report section indicates blocking status for violations.

        Given: Classified violations
        When: Report section is generated
        Then: Shows which violations are blocking
        """
        # Arrange
        from devforgeai.qa.regression_classifier import (
            run_classification_workflow,
            generate_detailed_report
        )

        violations = [
            {"file": "src/changed.py", "line": 1, "message": "Regression issue"},
            {"file": "src/old.py", "line": 2, "message": "Legacy issue"},
        ]

        # Act
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout="src/changed.py\n",
                stderr=""
            )

            classified = run_classification_workflow(violations)
            report = generate_detailed_report(classified)

            # Assert - report should distinguish blocking from non-blocking
            assert "REGRESSION" in report or "blocking" in report.lower()
            assert "PRE_EXISTING" in report or "warning" in report.lower()

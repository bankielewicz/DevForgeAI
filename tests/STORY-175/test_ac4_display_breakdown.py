"""
STORY-175 AC#4: Display Classification Breakdown

Tests that QA report displays classification breakdown: `Regressions: {count} | Pre-existing: {count}`.
All tests follow TDD Red phase - they should FAIL until implementation exists.

Given: violations counted
When: generating QA report
Then: display: `Regressions: {count} | Pre-existing: {count}`

Coverage Target: 95%+
"""

import pytest
from unittest.mock import Mock, patch, MagicMock


class TestClassificationBreakdownFormat:
    """Test AC#4: Display format matches specification."""

    def test_format_breakdown_returns_correct_string_format(self):
        """
        Test: format_breakdown() returns string in exact format specified.

        Given: Regression and pre-existing counts
        When: format_breakdown() is called
        Then: Returns "Regressions: {count} | Pre-existing: {count}"
        """
        # Arrange
        from devforgeai.qa.regression_classifier import format_breakdown

        regression_count = 3
        pre_existing_count = 7

        # Act
        result = format_breakdown(regression_count, pre_existing_count)

        # Assert
        assert result == "Regressions: 3 | Pre-existing: 7"

    def test_format_breakdown_with_zero_regressions(self):
        """
        Test: format_breakdown() handles zero regressions correctly.

        Given: Zero regressions, some pre-existing
        When: format_breakdown() is called
        Then: Returns "Regressions: 0 | Pre-existing: {count}"
        """
        # Arrange
        from devforgeai.qa.regression_classifier import format_breakdown

        # Act
        result = format_breakdown(0, 5)

        # Assert
        assert result == "Regressions: 0 | Pre-existing: 5"

    def test_format_breakdown_with_zero_pre_existing(self):
        """
        Test: format_breakdown() handles zero pre-existing correctly.

        Given: Some regressions, zero pre-existing
        When: format_breakdown() is called
        Then: Returns "Regressions: {count} | Pre-existing: 0"
        """
        # Arrange
        from devforgeai.qa.regression_classifier import format_breakdown

        # Act
        result = format_breakdown(3, 0)

        # Assert
        assert result == "Regressions: 3 | Pre-existing: 0"

    def test_format_breakdown_with_both_zero(self):
        """
        Test: format_breakdown() handles both counts being zero.

        Given: Zero regressions, zero pre-existing
        When: format_breakdown() is called
        Then: Returns "Regressions: 0 | Pre-existing: 0"
        """
        # Arrange
        from devforgeai.qa.regression_classifier import format_breakdown

        # Act
        result = format_breakdown(0, 0)

        # Assert
        assert result == "Regressions: 0 | Pre-existing: 0"

    def test_format_breakdown_with_large_numbers(self):
        """
        Test: format_breakdown() handles large numbers correctly.

        Given: Large regression and pre-existing counts
        When: format_breakdown() is called
        Then: Returns correctly formatted string with large numbers
        """
        # Arrange
        from devforgeai.qa.regression_classifier import format_breakdown

        # Act
        result = format_breakdown(1234, 5678)

        # Assert
        assert result == "Regressions: 1234 | Pre-existing: 5678"


class TestBreakdownFromViolations:
    """Test generating breakdown from violations list."""

    def test_get_breakdown_from_violations(self):
        """
        Test: get_breakdown() calculates counts from violations list.

        Given: List of classified violations
        When: get_breakdown() is called
        Then: Returns formatted breakdown string
        """
        # Arrange
        from devforgeai.qa.regression_classifier import get_breakdown

        violations = [
            {"classification": "REGRESSION"},
            {"classification": "PRE_EXISTING"},
            {"classification": "REGRESSION"},
            {"classification": "PRE_EXISTING"},
            {"classification": "PRE_EXISTING"},
        ]

        # Act
        result = get_breakdown(violations)

        # Assert
        assert result == "Regressions: 2 | Pre-existing: 3"

    def test_get_breakdown_counts_classifications_correctly(self):
        """
        Test: get_breakdown() counts each classification type accurately.

        Given: All REGRESSION violations
        When: get_breakdown() is called
        Then: Correct counts are returned
        """
        # Arrange
        from devforgeai.qa.regression_classifier import get_breakdown

        violations = [
            {"classification": "REGRESSION"},
            {"classification": "REGRESSION"},
            {"classification": "REGRESSION"},
        ]

        # Act
        result = get_breakdown(violations)

        # Assert
        assert result == "Regressions: 3 | Pre-existing: 0"

    def test_get_breakdown_with_empty_violations(self):
        """
        Test: get_breakdown() handles empty violations list.

        Given: Empty violations list
        When: get_breakdown() is called
        Then: Returns "Regressions: 0 | Pre-existing: 0"
        """
        # Arrange
        from devforgeai.qa.regression_classifier import get_breakdown

        violations = []

        # Act
        result = get_breakdown(violations)

        # Assert
        assert result == "Regressions: 0 | Pre-existing: 0"


class TestBreakdownInQAReport:
    """Test breakdown inclusion in QA report."""

    def test_qa_report_includes_breakdown_line(self):
        """
        Test: QA report output includes the breakdown line.

        Given: Classified violations
        When: QA report is generated
        Then: Report contains breakdown line
        """
        # Arrange
        from devforgeai.qa.regression_classifier import generate_classification_summary

        violations = [
            {"classification": "REGRESSION"},
            {"classification": "PRE_EXISTING"},
        ]

        # Act
        result = generate_classification_summary(violations)

        # Assert
        assert "Regressions:" in result
        assert "Pre-existing:" in result
        assert "|" in result

    def test_breakdown_uses_pipe_separator(self):
        """
        Test: Breakdown uses pipe (|) as separator between counts.

        Given: Classification breakdown
        When: Formatted
        Then: Uses " | " as separator
        """
        # Arrange
        from devforgeai.qa.regression_classifier import format_breakdown

        # Act
        result = format_breakdown(5, 10)

        # Assert
        assert " | " in result
        parts = result.split(" | ")
        assert len(parts) == 2
        assert parts[0].startswith("Regressions:")
        assert parts[1].startswith("Pre-existing:")


class TestBreakdownCounts:
    """Test individual count extraction."""

    def test_count_regressions(self):
        """
        Test: count_regressions() returns count of REGRESSION violations.

        Given: List of classified violations
        When: count_regressions() is called
        Then: Returns correct count
        """
        # Arrange
        from devforgeai.qa.regression_classifier import count_regressions

        violations = [
            {"classification": "REGRESSION"},
            {"classification": "PRE_EXISTING"},
            {"classification": "REGRESSION"},
        ]

        # Act
        result = count_regressions(violations)

        # Assert
        assert result == 2

    def test_count_pre_existing(self):
        """
        Test: count_pre_existing() returns count of PRE_EXISTING violations.

        Given: List of classified violations
        When: count_pre_existing() is called
        Then: Returns correct count
        """
        # Arrange
        from devforgeai.qa.regression_classifier import count_pre_existing

        violations = [
            {"classification": "REGRESSION"},
            {"classification": "PRE_EXISTING"},
            {"classification": "PRE_EXISTING"},
            {"classification": "PRE_EXISTING"},
        ]

        # Act
        result = count_pre_existing(violations)

        # Assert
        assert result == 3

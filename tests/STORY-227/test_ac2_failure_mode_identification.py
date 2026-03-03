"""
Tests for AC#2: Failure Mode Identification

Acceptance Criteria:
Given error entries,
When analyzing patterns,
Then most common failure modes are identified and ranked.

Test Framework: pytest
Test Pattern: AAA (Arrange, Act, Assert)
TDD Phase: Red (all tests should FAIL initially - no implementation exists)
"""
import pytest
from typing import Dict, List, Any

# Import the module under test (does not exist yet - TDD Red phase)
# These stub functions will fail tests until real implementation is created
try:
    from devforgeai_cli.metrics.failure_modes import (
        identify_failure_modes,
        rank_failure_modes,
        categorize_failure_mode,
        get_failure_mode_summary,
    )
except ModuleNotFoundError:
    # Stub functions that raise NotImplementedError for TDD Red phase
    def identify_failure_modes(error_entries):
        raise NotImplementedError("Module devforgeai_cli.metrics.failure_modes not implemented")

    def rank_failure_modes(error_entries):
        raise NotImplementedError("Module devforgeai_cli.metrics.failure_modes not implemented")

    def categorize_failure_mode(error_type):
        raise NotImplementedError("Module devforgeai_cli.metrics.failure_modes not implemented")

    def get_failure_mode_summary(error_entries):
        raise NotImplementedError("Module devforgeai_cli.metrics.failure_modes not implemented")


class TestIdentifyFailureModes:
    """Tests for failure mode identification from error entries."""

    def test_identify_failure_modes_from_errors(
        self, sample_error_entries: List[Dict[str, Any]]
    ):
        """
        Given: Error entries with different error types
        When: Identifying failure modes
        Then: Returns list of unique failure modes found
        """
        # Arrange & Act
        result = identify_failure_modes(sample_error_entries)

        # Assert
        expected_modes = {"test_failure", "coverage_gap", "validation_failure", "timeout"}
        assert set(result) == expected_modes, f"Expected {expected_modes}, got {set(result)}"

    def test_identify_failure_modes_returns_list(
        self, sample_error_entries: List[Dict[str, Any]]
    ):
        """
        Given: Error entries
        When: Identifying failure modes
        Then: Returns a list (not set or other type)
        """
        # Arrange & Act
        result = identify_failure_modes(sample_error_entries)

        # Assert
        assert isinstance(result, list), f"Expected list, got {type(result)}"

    def test_identify_failure_modes_with_no_errors_returns_empty(
        self, empty_error_entries: List[Dict[str, Any]]
    ):
        """
        Given: Empty error entries
        When: Identifying failure modes
        Then: Returns empty list
        """
        # Arrange & Act
        result = identify_failure_modes(empty_error_entries)

        # Assert
        assert result == [], f"Expected empty list for no errors, got {result}"

    def test_identify_failure_modes_handles_missing_error_type(self):
        """
        Given: Error entries with some missing error_type field
        When: Identifying failure modes
        Then: Gracefully handles and ignores entries without error_type
        """
        # Arrange
        entries = [
            {"error_type": "test_failure", "message": "Test failed"},
            {"message": "No error type"},  # Missing error_type
            {"error_type": "coverage_gap", "message": "Coverage low"},
        ]

        # Act
        result = identify_failure_modes(entries)

        # Assert
        assert "test_failure" in result
        assert "coverage_gap" in result
        assert len(result) == 2


class TestRankFailureModes:
    """Tests for failure mode ranking by frequency."""

    def test_rank_failure_modes_by_frequency(
        self, sample_error_entries: List[Dict[str, Any]]
    ):
        """
        Given: Error entries with varying error type frequencies
        When: Ranking failure modes
        Then: Returns list sorted by frequency (most common first)
        """
        # Arrange & Act
        result = rank_failure_modes(sample_error_entries)

        # Assert
        # Expected order: test_failure (4), coverage_gap (3), validation_failure (2), timeout (1)
        assert result[0]["error_type"] == "test_failure", f"Expected test_failure first, got {result[0]}"
        assert result[1]["error_type"] == "coverage_gap", f"Expected coverage_gap second, got {result[1]}"
        assert result[2]["error_type"] == "validation_failure", f"Expected validation_failure third, got {result[2]}"
        assert result[3]["error_type"] == "timeout", f"Expected timeout fourth, got {result[3]}"

    def test_rank_failure_modes_includes_count(
        self, sample_error_entries: List[Dict[str, Any]]
    ):
        """
        Given: Error entries
        When: Ranking failure modes
        Then: Each ranked item includes count/frequency
        """
        # Arrange & Act
        result = rank_failure_modes(sample_error_entries)

        # Assert
        assert result[0]["count"] == 4, f"Expected count 4 for test_failure, got {result[0].get('count')}"
        assert result[1]["count"] == 3, f"Expected count 3 for coverage_gap, got {result[1].get('count')}"
        assert result[2]["count"] == 2, f"Expected count 2 for validation_failure, got {result[2].get('count')}"
        assert result[3]["count"] == 1, f"Expected count 1 for timeout, got {result[3].get('count')}"

    def test_rank_failure_modes_includes_percentage(
        self, sample_error_entries: List[Dict[str, Any]]
    ):
        """
        Given: Error entries (10 total)
        When: Ranking failure modes
        Then: Each ranked item includes percentage of total errors
        """
        # Arrange & Act
        result = rank_failure_modes(sample_error_entries)

        # Assert
        # test_failure: 4/10 = 40%
        assert result[0]["percentage"] == 40.0, f"Expected 40.0% for test_failure, got {result[0].get('percentage')}"
        # coverage_gap: 3/10 = 30%
        assert result[1]["percentage"] == 30.0, f"Expected 30.0% for coverage_gap, got {result[1].get('percentage')}"

    def test_rank_failure_modes_with_no_errors_returns_empty(
        self, empty_error_entries: List[Dict[str, Any]]
    ):
        """
        Given: Empty error entries
        When: Ranking failure modes
        Then: Returns empty list
        """
        # Arrange & Act
        result = rank_failure_modes(empty_error_entries)

        # Assert
        assert result == [], f"Expected empty list for no errors, got {result}"

    def test_rank_failure_modes_returns_list_of_dicts(
        self, sample_error_entries: List[Dict[str, Any]]
    ):
        """
        Given: Error entries
        When: Ranking failure modes
        Then: Returns list of dictionaries with required fields
        """
        # Arrange & Act
        result = rank_failure_modes(sample_error_entries)

        # Assert
        assert isinstance(result, list)
        for item in result:
            assert isinstance(item, dict)
            assert "error_type" in item
            assert "count" in item
            assert "percentage" in item


class TestCategorizeFailureMode:
    """Tests for failure mode categorization."""

    def test_failure_mode_categorization_test_failure(self):
        """
        Given: A test_failure error type
        When: Categorizing the failure mode
        Then: Returns appropriate category (e.g., "testing")
        """
        # Arrange
        error_type = "test_failure"

        # Act
        result = categorize_failure_mode(error_type)

        # Assert
        assert result == "testing", f"Expected 'testing' category for test_failure, got {result}"

    def test_failure_mode_categorization_coverage_gap(self):
        """
        Given: A coverage_gap error type
        When: Categorizing the failure mode
        Then: Returns appropriate category (e.g., "quality")
        """
        # Arrange
        error_type = "coverage_gap"

        # Act
        result = categorize_failure_mode(error_type)

        # Assert
        assert result == "quality", f"Expected 'quality' category for coverage_gap, got {result}"

    def test_failure_mode_categorization_validation_failure(self):
        """
        Given: A validation_failure error type
        When: Categorizing the failure mode
        Then: Returns appropriate category (e.g., "validation")
        """
        # Arrange
        error_type = "validation_failure"

        # Act
        result = categorize_failure_mode(error_type)

        # Assert
        assert result == "validation", f"Expected 'validation' category for validation_failure, got {result}"

    def test_failure_mode_categorization_timeout(self):
        """
        Given: A timeout error type
        When: Categorizing the failure mode
        Then: Returns appropriate category (e.g., "infrastructure")
        """
        # Arrange
        error_type = "timeout"

        # Act
        result = categorize_failure_mode(error_type)

        # Assert
        assert result == "infrastructure", f"Expected 'infrastructure' category for timeout, got {result}"

    def test_failure_mode_categorization_unknown(self):
        """
        Given: An unknown error type
        When: Categorizing the failure mode
        Then: Returns "unknown" category
        """
        # Arrange
        error_type = "some_random_error"

        # Act
        result = categorize_failure_mode(error_type)

        # Assert
        assert result == "unknown", f"Expected 'unknown' category for unknown error, got {result}"


class TestGetFailureModeSummary:
    """Tests for failure mode summary generation."""

    def test_get_failure_mode_summary_structure(
        self, sample_error_entries: List[Dict[str, Any]]
    ):
        """
        Given: Error entries
        When: Getting failure mode summary
        Then: Returns dictionary with expected structure
        """
        # Arrange & Act
        result = get_failure_mode_summary(sample_error_entries)

        # Assert
        assert "total_errors" in result
        assert "unique_failure_modes" in result
        assert "ranked_modes" in result
        assert "by_category" in result

    def test_get_failure_mode_summary_total_count(
        self, sample_error_entries: List[Dict[str, Any]]
    ):
        """
        Given: Error entries (10 total)
        When: Getting failure mode summary
        Then: total_errors equals 10
        """
        # Arrange & Act
        result = get_failure_mode_summary(sample_error_entries)

        # Assert
        assert result["total_errors"] == 10, f"Expected 10 total errors, got {result['total_errors']}"

    def test_get_failure_mode_summary_empty_entries(
        self, empty_error_entries: List[Dict[str, Any]]
    ):
        """
        Given: Empty error entries
        When: Getting failure mode summary
        Then: Returns summary with zeros
        """
        # Arrange & Act
        result = get_failure_mode_summary(empty_error_entries)

        # Assert
        assert result["total_errors"] == 0
        assert result["unique_failure_modes"] == 0
        assert result["ranked_modes"] == []
        assert result["by_category"] == {}

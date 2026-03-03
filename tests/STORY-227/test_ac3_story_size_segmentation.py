"""
Tests for AC#3: Story Size Segmentation

Acceptance Criteria:
Given workflow metrics,
When analyzing by story size,
Then metrics are segmented by story points (1, 2, 3, 5, 8 points).

Test Framework: pytest
Test Pattern: AAA (Arrange, Act, Assert)
TDD Phase: Red (all tests should FAIL initially - no implementation exists)
"""
import pytest
from typing import Dict, List, Any

# Import the module under test (does not exist yet - TDD Red phase)
# These stub functions will fail tests until real implementation is created
try:
    from devforgeai_cli.metrics.story_segmentation import (
        segment_metrics_by_story_points,
        get_valid_story_points,
        is_valid_story_point,
        calculate_segment_averages,
        get_segmentation_summary,
    )
except ModuleNotFoundError:
    # Stub functions that raise NotImplementedError for TDD Red phase
    def segment_metrics_by_story_points(workflow_metrics):
        raise NotImplementedError("Module devforgeai_cli.metrics.story_segmentation not implemented")

    def get_valid_story_points():
        raise NotImplementedError("Module devforgeai_cli.metrics.story_segmentation not implemented")

    def is_valid_story_point(point):
        raise NotImplementedError("Module devforgeai_cli.metrics.story_segmentation not implemented")

    def calculate_segment_averages(segments):
        raise NotImplementedError("Module devforgeai_cli.metrics.story_segmentation not implemented")

    def get_segmentation_summary(workflow_metrics):
        raise NotImplementedError("Module devforgeai_cli.metrics.story_segmentation not implemented")


class TestSegmentMetricsByStoryPoints:
    """Tests for metrics segmentation by story points."""

    def test_segment_metrics_by_story_points(
        self, sample_workflow_metrics_with_story_points: List[Dict[str, Any]]
    ):
        """
        Given: Workflow metrics with story point assignments
        When: Segmenting by story points
        Then: Returns dictionary with metrics grouped by point value
        """
        # Arrange & Act
        result = segment_metrics_by_story_points(sample_workflow_metrics_with_story_points)

        # Assert
        assert 1 in result, "Expected segment for 1-point stories"
        assert 2 in result, "Expected segment for 2-point stories"
        assert 3 in result, "Expected segment for 3-point stories"
        assert 5 in result, "Expected segment for 5-point stories"
        assert 8 in result, "Expected segment for 8-point stories"

    def test_segment_contains_correct_stories(
        self, sample_workflow_metrics_with_story_points: List[Dict[str, Any]]
    ):
        """
        Given: Workflow metrics with known story point distribution
        When: Segmenting by story points
        Then: Each segment contains correct number of stories
        """
        # Arrange & Act
        result = segment_metrics_by_story_points(sample_workflow_metrics_with_story_points)

        # Assert
        assert len(result[1]) == 2, f"Expected 2 stories for 1-point, got {len(result[1])}"
        assert len(result[2]) == 2, f"Expected 2 stories for 2-point, got {len(result[2])}"
        assert len(result[3]) == 3, f"Expected 3 stories for 3-point, got {len(result[3])}"
        assert len(result[5]) == 2, f"Expected 2 stories for 5-point, got {len(result[5])}"
        assert len(result[8]) == 1, f"Expected 1 story for 8-point, got {len(result[8])}"

    def test_segment_excludes_invalid_points(
        self, sample_workflow_metrics_with_story_points: List[Dict[str, Any]]
    ):
        """
        Given: Workflow metrics with some invalid story points (0, 4, 13)
        When: Segmenting by story points
        Then: Invalid points are NOT included in segments
        """
        # Arrange & Act
        result = segment_metrics_by_story_points(sample_workflow_metrics_with_story_points)

        # Assert
        assert 0 not in result, "Should not include 0-point segment"
        assert 4 not in result, "Should not include 4-point segment (not Fibonacci)"
        assert 13 not in result, "Should not include 13-point segment"

    def test_segment_with_empty_metrics_returns_empty_segments(self):
        """
        Given: Empty workflow metrics
        When: Segmenting by story points
        Then: Returns dictionary with empty lists for each valid point value
        """
        # Arrange
        empty_metrics: List[Dict[str, Any]] = []

        # Act
        result = segment_metrics_by_story_points(empty_metrics)

        # Assert
        # Should return structure with valid point keys but empty lists
        assert result == {1: [], 2: [], 3: [], 5: [], 8: []}, f"Unexpected result for empty metrics: {result}"


class TestValidStoryPoints:
    """Tests for valid story points validation."""

    def test_valid_story_points_1_2_3_5_8(self, valid_story_points: List[int]):
        """
        Given: The list of valid story points
        When: Checking get_valid_story_points()
        Then: Returns [1, 2, 3, 5, 8] (Fibonacci-based)
        """
        # Arrange & Act
        result = get_valid_story_points()

        # Assert
        assert result == [1, 2, 3, 5, 8], f"Expected [1, 2, 3, 5, 8], got {result}"

    def test_is_valid_story_point_returns_true_for_valid(self):
        """
        Given: Valid story point values (1, 2, 3, 5, 8)
        When: Checking is_valid_story_point()
        Then: Returns True for each
        """
        # Arrange
        valid_points = [1, 2, 3, 5, 8]

        # Act & Assert
        for point in valid_points:
            assert is_valid_story_point(point) is True, f"Expected True for {point}"

    def test_is_valid_story_point_returns_false_for_invalid(self):
        """
        Given: Invalid story point values (0, 4, 6, 7, 10, 13)
        When: Checking is_valid_story_point()
        Then: Returns False for each
        """
        # Arrange
        invalid_points = [0, 4, 6, 7, 10, 13, -1, 100]

        # Act & Assert
        for point in invalid_points:
            assert is_valid_story_point(point) is False, f"Expected False for {point}"

    def test_is_valid_story_point_handles_none(self):
        """
        Given: None as story point
        When: Checking is_valid_story_point()
        Then: Returns False
        """
        # Arrange & Act
        result = is_valid_story_point(None)

        # Assert
        assert result is False, "Expected False for None value"


class TestInvalidStoryPointsExcluded:
    """Tests for exclusion of invalid story points."""

    def test_invalid_story_points_excluded(
        self, sample_workflow_metrics_with_story_points: List[Dict[str, Any]]
    ):
        """
        Given: Workflow metrics with invalid story points (0, 4, 13)
        When: Segmenting by story points
        Then: Stories with invalid points are excluded from all segments
        """
        # Arrange & Act
        result = segment_metrics_by_story_points(sample_workflow_metrics_with_story_points)

        # Assert
        # Count total stories across all segments
        total_segmented = sum(len(stories) for stories in result.values())
        # We have 10 valid stories (1, 2, 3, 5, 8 points) and 3 invalid (0, 4, 13)
        assert total_segmented == 10, f"Expected 10 segmented stories, got {total_segmented}"

    def test_story_ids_in_segments_match_valid_stories(
        self, sample_workflow_metrics_with_story_points: List[Dict[str, Any]]
    ):
        """
        Given: Workflow metrics with known valid/invalid story points
        When: Segmenting by story points
        Then: Only story IDs with valid points appear in segments
        """
        # Arrange & Act
        result = segment_metrics_by_story_points(sample_workflow_metrics_with_story_points)

        # Assert
        all_story_ids = []
        for stories in result.values():
            all_story_ids.extend([s["story_id"] for s in stories])

        # STORY-011, STORY-012, STORY-013 have invalid points
        assert "STORY-011" not in all_story_ids, "STORY-011 (0 points) should be excluded"
        assert "STORY-012" not in all_story_ids, "STORY-012 (4 points) should be excluded"
        assert "STORY-013" not in all_story_ids, "STORY-013 (13 points) should be excluded"


class TestSegmentationWithMissingPoints:
    """Tests for handling missing story points."""

    def test_segmentation_with_missing_points(
        self, workflow_metrics_missing_points: List[Dict[str, Any]]
    ):
        """
        Given: Workflow metrics with some missing story_points fields
        When: Segmenting by story points
        Then: Stories without story_points are excluded
        """
        # Arrange & Act
        result = segment_metrics_by_story_points(workflow_metrics_missing_points)

        # Assert
        # Only STORY-001 (3 points) and STORY-003 (5 points) should be included
        total_segmented = sum(len(stories) for stories in result.values())
        assert total_segmented == 2, f"Expected 2 segmented stories, got {total_segmented}"

    def test_segmentation_handles_none_story_points(
        self, workflow_metrics_missing_points: List[Dict[str, Any]]
    ):
        """
        Given: Workflow metrics with None story_points
        When: Segmenting by story points
        Then: Stories with None are excluded
        """
        # Arrange & Act
        result = segment_metrics_by_story_points(workflow_metrics_missing_points)

        # Assert
        all_story_ids = []
        for stories in result.values():
            all_story_ids.extend([s["story_id"] for s in stories])

        # STORY-004 has story_points=None
        assert "STORY-004" not in all_story_ids, "STORY-004 (None points) should be excluded"


class TestCalculateSegmentAverages:
    """Tests for calculating averages within segments."""

    def test_calculate_segment_averages(
        self, sample_workflow_metrics_with_story_points: List[Dict[str, Any]]
    ):
        """
        Given: Segmented workflow metrics
        When: Calculating averages per segment
        Then: Returns average completion_rate, error_rate per segment
        """
        # Arrange
        segments = segment_metrics_by_story_points(sample_workflow_metrics_with_story_points)

        # Act
        result = calculate_segment_averages(segments)

        # Assert
        assert 1 in result
        assert "avg_completion_rate" in result[1]
        assert "avg_error_rate" in result[1]

        # 1-point stories: (100 + 100) / 2 = 100% avg completion
        assert result[1]["avg_completion_rate"] == 100.0

    def test_calculate_segment_averages_for_3_point(
        self, sample_workflow_metrics_with_story_points: List[Dict[str, Any]]
    ):
        """
        Given: Segmented workflow metrics with 3-point stories
        When: Calculating averages
        Then: Returns correct average for 3-point segment
        """
        # Arrange
        segments = segment_metrics_by_story_points(sample_workflow_metrics_with_story_points)

        # Act
        result = calculate_segment_averages(segments)

        # Assert
        # 3-point stories: (85 + 80 + 90) / 3 = 85% avg completion
        assert result[3]["avg_completion_rate"] == 85.0
        # 3-point stories error: (20 + 25 + 10) / 3 = 18.33% avg error
        assert abs(result[3]["avg_error_rate"] - 18.33) < 0.01

    def test_calculate_segment_averages_empty_segment(self):
        """
        Given: Segments with some empty (no stories)
        When: Calculating averages
        Then: Empty segments have None or 0 for averages
        """
        # Arrange
        segments = {1: [], 2: [], 3: [], 5: [], 8: []}  # All empty

        # Act
        result = calculate_segment_averages(segments)

        # Assert
        for point in [1, 2, 3, 5, 8]:
            assert result[point]["avg_completion_rate"] == 0.0 or result[point]["avg_completion_rate"] is None


class TestGetSegmentationSummary:
    """Tests for overall segmentation summary."""

    def test_get_segmentation_summary_structure(
        self, sample_workflow_metrics_with_story_points: List[Dict[str, Any]]
    ):
        """
        Given: Workflow metrics
        When: Getting segmentation summary
        Then: Returns summary with expected structure
        """
        # Arrange & Act
        result = get_segmentation_summary(sample_workflow_metrics_with_story_points)

        # Assert
        assert "total_stories" in result
        assert "segmented_stories" in result
        assert "excluded_stories" in result
        assert "segments" in result
        assert "averages_by_segment" in result

    def test_get_segmentation_summary_counts(
        self, sample_workflow_metrics_with_story_points: List[Dict[str, Any]]
    ):
        """
        Given: Workflow metrics with 13 total (10 valid, 3 invalid)
        When: Getting segmentation summary
        Then: Counts are correct
        """
        # Arrange & Act
        result = get_segmentation_summary(sample_workflow_metrics_with_story_points)

        # Assert
        assert result["total_stories"] == 13
        assert result["segmented_stories"] == 10
        assert result["excluded_stories"] == 3

    def test_get_segmentation_summary_empty_metrics(self):
        """
        Given: Empty workflow metrics
        When: Getting segmentation summary
        Then: Returns summary with zeros
        """
        # Arrange
        empty_metrics: List[Dict[str, Any]] = []

        # Act
        result = get_segmentation_summary(empty_metrics)

        # Assert
        assert result["total_stories"] == 0
        assert result["segmented_stories"] == 0
        assert result["excluded_stories"] == 0

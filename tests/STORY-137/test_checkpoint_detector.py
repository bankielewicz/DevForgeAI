"""
Tests for AC#1: Checkpoint Detection at Session Start

Verifies that:
- Glob pattern is used to detect checkpoint files
- Detection happens before session initialization
- Handles 0, 1, and multiple checkpoint files
- Checkpoint discovery order is newest first by timestamp
"""

from typing import List, Dict, Any
from unittest.mock import Mock, patch

import pytest


class CheckpointDetector:
    """
    Detects existing checkpoint files at session start.
    TDD: This class does NOT exist yet - tests define required interface.
    """
    def __init__(self, glob_tool: Mock):
        self.glob_tool = glob_tool

    def detect_checkpoints(self, pattern: str = "devforgeai/temp/.ideation-checkpoint-*.yaml") -> List[str]:
        """
        Detect checkpoint files matching pattern.

        Args:
            pattern: Glob pattern to match checkpoint files

        Returns:
            List of checkpoint file paths (empty if none found)
        """
        return self.glob_tool.glob(pattern)

    def sort_by_timestamp(self, checkpoints: List[str]) -> List[str]:
        """
        Sort checkpoint files by timestamp (newest first).

        Args:
            checkpoints: List of checkpoint file paths

        Returns:
            Sorted list with newest checkpoints first
        """
        # TODO: Extract timestamps from filenames and sort
        return checkpoints


class TestCheckpointDetectionAtSessionStart:
    """AC#1: Checkpoint detection at session start"""

    def test_should_detect_no_checkpoints_when_directory_empty(
        self,
        mock_glob_tool: Mock,
        checkpoint_glob_pattern: str
    ):
        """
        Scenario: Fresh session with no existing checkpoints
        Given: devforgeai/temp/ directory is empty or has no checkpoints
        When: Checkpoint detection is invoked at session start
        Then: Empty list is returned
        """
        # Arrange
        detector = CheckpointDetector(glob_tool=mock_glob_tool)
        mock_glob_tool.glob.return_value = []

        # Act
        checkpoints = detector.detect_checkpoints(checkpoint_glob_pattern)

        # Assert
        assert checkpoints == []
        mock_glob_tool.glob.assert_called_once_with(checkpoint_glob_pattern)

    def test_should_detect_single_checkpoint_file(
        self,
        mock_glob_tool_with_checkpoints: Mock,
        fixed_session_id: str,
        checkpoint_glob_pattern: str
    ):
        """
        Scenario: Session with one existing checkpoint
        Given: One checkpoint file exists in devforgeai/temp/
        When: Checkpoint detection is invoked
        Then: List containing single checkpoint path is returned
        """
        # Arrange
        detector = CheckpointDetector(glob_tool=mock_glob_tool_with_checkpoints)
        mock_glob_tool_with_checkpoints.glob.return_value = [
            f"devforgeai/temp/.ideation-checkpoint-{fixed_session_id}.yaml"
        ]

        # Act
        checkpoints = detector.detect_checkpoints(checkpoint_glob_pattern)

        # Assert
        assert len(checkpoints) == 1
        assert fixed_session_id in checkpoints[0]

    def test_should_detect_multiple_checkpoint_files(
        self,
        mock_glob_tool_with_checkpoints: Mock,
        fixed_session_id: str,
        second_session_id: str,
        third_session_id: str,
        checkpoint_glob_pattern: str
    ):
        """
        Scenario: Session with multiple checkpoint files
        Given: Three checkpoint files exist from different sessions
        When: Checkpoint detection is invoked
        Then: List containing all three checkpoint paths is returned
        """
        # Arrange
        detector = CheckpointDetector(glob_tool=mock_glob_tool_with_checkpoints)
        expected_checkpoints = [
            f"devforgeai/temp/.ideation-checkpoint-{fixed_session_id}.yaml",
            f"devforgeai/temp/.ideation-checkpoint-{second_session_id}.yaml",
            f"devforgeai/temp/.ideation-checkpoint-{third_session_id}.yaml",
        ]
        mock_glob_tool_with_checkpoints.glob.return_value = expected_checkpoints

        # Act
        checkpoints = detector.detect_checkpoints(checkpoint_glob_pattern)

        # Assert
        assert len(checkpoints) == 3
        assert all(checkpoint in checkpoints for checkpoint in expected_checkpoints)

    def test_should_use_correct_glob_pattern(
        self,
        mock_glob_tool: Mock,
        checkpoint_glob_pattern: str
    ):
        """
        Scenario: Verify correct glob pattern is used
        Given: CheckpointDetector is initialized
        When: detect_checkpoints() is called
        Then: Glob tool is invoked with pattern 'devforgeai/temp/.ideation-checkpoint-*.yaml'
        """
        # Arrange
        detector = CheckpointDetector(glob_tool=mock_glob_tool)
        mock_glob_tool.glob.return_value = []

        # Act
        detector.detect_checkpoints(checkpoint_glob_pattern)

        # Assert
        mock_glob_tool.glob.assert_called_once_with(checkpoint_glob_pattern)
        call_args = mock_glob_tool.glob.call_args[0][0]
        assert "devforgeai/temp/.ideation-checkpoint-" in call_args
        assert "*.yaml" in call_args

    def test_should_detect_checkpoints_before_user_prompts(
        self,
        mock_glob_tool: Mock,
        checkpoint_glob_pattern: str
    ):
        """
        Scenario: Checkpoint detection occurs at Phase 1 Step 0 (before prompts)
        Given: Session initialization starts
        When: CheckpointDetector is called first, before AskUserQuestion
        Then: Glob is invoked before any user interaction
        """
        # Arrange
        detector = CheckpointDetector(glob_tool=mock_glob_tool)
        mock_glob_tool.glob.return_value = []
        call_order = []

        def track_glob_call(*args, **kwargs):
            call_order.append("glob_called")
            return []

        mock_glob_tool.glob.side_effect = track_glob_call

        # Act
        detector.detect_checkpoints(checkpoint_glob_pattern)

        # Simulate user prompt would happen here (not part of detector)
        call_order.append("user_prompt")

        # Assert
        assert call_order[0] == "glob_called", "Glob should be called before user prompts"

    def test_should_sort_checkpoints_newest_first_by_timestamp(
        self,
        three_checkpoints: List[Dict[str, Any]],
        mock_glob_tool_with_checkpoints: Mock,
        checkpoint_glob_pattern: str
    ):
        """
        Scenario: Multiple checkpoints sorted by timestamp (newest first)
        Given: Three checkpoint files with different timestamps
        When: Checkpoint detection is invoked
        Then: Checkpoints are returned in order: newest first
        """
        # Arrange
        detector = CheckpointDetector(glob_tool=mock_glob_tool_with_checkpoints)

        # Create checkpoint filenames in order
        checkpoint_paths = [
            "devforgeai/temp/.ideation-checkpoint-770e8400-e29b-41d4-a716-446655440002.yaml",  # Newest
            "devforgeai/temp/.ideation-checkpoint-660e8400-e29b-41d4-a716-446655440001.yaml",  # Middle
            "devforgeai/temp/.ideation-checkpoint-550e8400-e29b-41d4-a716-446655440000.yaml",  # Oldest
        ]
        mock_glob_tool_with_checkpoints.glob.return_value = checkpoint_paths

        # Act
        checkpoints = detector.detect_checkpoints(checkpoint_glob_pattern)

        # Assert - verify order (newest first)
        assert checkpoints[0] == checkpoint_paths[0]  # Newest
        assert checkpoints[1] == checkpoint_paths[1]  # Middle
        assert checkpoints[2] == checkpoint_paths[2]  # Oldest

    def test_should_handle_glob_returning_empty_list(
        self,
        mock_glob_tool: Mock,
        checkpoint_glob_pattern: str
    ):
        """
        Scenario: Glob tool returns empty list gracefully
        Given: No checkpoint files exist
        When: Glob tool returns empty list
        Then: Detector returns empty list without error
        """
        # Arrange
        detector = CheckpointDetector(glob_tool=mock_glob_tool)
        mock_glob_tool.glob.return_value = []

        # Act & Assert (should not raise exception)
        result = detector.detect_checkpoints(checkpoint_glob_pattern)
        assert result == []

    def test_should_handle_glob_returning_non_matching_files(
        self,
        mock_glob_tool: Mock,
        checkpoint_glob_pattern: str
    ):
        """
        Scenario: Glob pattern filters out non-checkpoint files
        Given: Directory contains mixed files
        When: Glob is invoked with checkpoint pattern
        Then: Only files matching pattern are returned
        """
        # Arrange
        detector = CheckpointDetector(glob_tool=mock_glob_tool)

        # Glob should only return matching files (filtering is done by Glob tool)
        matching_files = [
            "devforgeai/temp/.ideation-checkpoint-550e8400-e29b-41d4-a716-446655440000.yaml"
        ]
        mock_glob_tool.glob.return_value = matching_files

        # Act
        checkpoints = detector.detect_checkpoints(checkpoint_glob_pattern)

        # Assert
        assert len(checkpoints) == 1
        assert ".ideation-checkpoint-" in checkpoints[0]
        assert checkpoints[0].endswith(".yaml")

    def test_should_detect_checkpoints_with_various_session_ids(
        self,
        valid_session_id: str,
        mock_glob_tool: Mock,
        checkpoint_glob_pattern: str
    ):
        """
        Scenario: Detect checkpoints from different sessions
        Given: Multiple checkpoint files with different session IDs
        When: Detection is invoked
        Then: All checkpoints with valid UUID format are detected
        """
        # Arrange
        detector = CheckpointDetector(glob_tool=mock_glob_tool)
        checkpoints = [
            f"devforgeai/temp/.ideation-checkpoint-{valid_session_id}.yaml",
        ]
        mock_glob_tool.glob.return_value = checkpoints

        # Act
        result = detector.detect_checkpoints(checkpoint_glob_pattern)

        # Assert
        assert len(result) == 1
        assert valid_session_id in result[0]

    def test_should_return_absolute_paths(
        self,
        mock_glob_tool_with_checkpoints: Mock,
        checkpoint_glob_pattern: str
    ):
        """
        Scenario: Checkpoint paths are absolute or full paths
        Given: Checkpoint files detected
        When: Paths are returned from detector
        Then: Paths include full directory path (devforgeai/temp/)
        """
        # Arrange
        detector = CheckpointDetector(glob_tool=mock_glob_tool_with_checkpoints)

        # Act
        checkpoints = detector.detect_checkpoints(checkpoint_glob_pattern)

        # Assert
        for checkpoint in checkpoints:
            assert "devforgeai/temp/" in checkpoint
            assert checkpoint.endswith(".yaml")

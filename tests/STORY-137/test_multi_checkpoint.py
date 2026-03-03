"""
Tests for AC#6: Multi-Checkpoint Selection (Multiple Sessions)

Verifies that:
- Multiple checkpoints listed with identifying info
- Sorted by timestamp (newest first)
- Correct checkpoint loaded based on selection
"""

from typing import Dict, Any, List
from unittest.mock import Mock

import pytest


class MultiCheckpointSelector:
    """
    Handles selection and loading of multiple checkpoint files.
    TDD: This class does NOT exist yet - tests define required interface.
    """
    def __init__(self, ask_tool: Mock):
        self.ask_tool = ask_tool

    def format_checkpoint_info(
        self,
        checkpoint: Dict[str, Any],
        index: int
    ) -> str:
        """
        Format checkpoint info for display.

        Args:
            checkpoint: Checkpoint dictionary
            index: Display index (1-based for user display)

        Returns:
            Formatted info: "[1] X/6 phases, Problem: ..., Timestamp: ..."
        """
        phase = checkpoint.get("current_phase", 0)
        timestamp = checkpoint.get("timestamp", "unknown")
        problem = checkpoint.get("brainstorm_context", {}).get("problem_statement", "")[:50]

        return f"[{index}] {phase}/6 phases - Problem: {problem} - {timestamp}"

    def sort_checkpoints_by_timestamp(
        self,
        checkpoints: List[str],
        checkpoint_data: List[Dict[str, Any]]
    ) -> tuple[List[str], List[Dict[str, Any]]]:
        """
        Sort checkpoints by timestamp (newest first).

        Args:
            checkpoints: List of checkpoint paths
            checkpoint_data: List of checkpoint dictionaries

        Returns:
            Tuple of (sorted_paths, sorted_data)
        """
        # Pair checkpoints with their data for sorting
        pairs = list(zip(checkpoints, checkpoint_data))

        # Sort by timestamp in descending order (newest first)
        sorted_pairs = sorted(
            pairs,
            key=lambda p: p[1].get("timestamp", ""),
            reverse=True
        )

        # Unzip back to separate lists
        sorted_checkpoints = [p[0] for p in sorted_pairs]
        sorted_data = [p[1] for p in sorted_pairs]

        return sorted_checkpoints, sorted_data

    def ask_checkpoint_selection(
        self,
        options: List[str]
    ) -> Dict[str, Any]:
        """
        Ask user to select checkpoint or fresh start.

        Args:
            options: List of formatted checkpoint options

        Returns:
            Dict with 'selected_index' or 'choice': 'fresh'
        """
        return self.ask_tool.ask(options=options)

    def load_selected_checkpoint(
        self,
        selection: Dict[str, Any],
        checkpoint_paths: List[str],
        checkpoint_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Load selected checkpoint.

        Args:
            selection: User selection result
            checkpoint_paths: Available checkpoint paths
            checkpoint_data: Available checkpoint data

        Returns:
            Selected checkpoint data or empty dict if fresh start
        """
        if selection.get("choice") == "fresh":
            return {}

        index = selection.get("selected_index", 0)
        if 0 <= index < len(checkpoint_data):
            return checkpoint_data[index]

        return {}


class TestMultiCheckpointSelection:
    """AC#6: Multi-checkpoint selection (multiple sessions)"""

    def test_should_list_all_checkpoints_with_info(
        self,
        two_checkpoints: List[Dict[str, Any]]
    ):
        """
        Scenario: List all checkpoints with identifying info
        Given: Two checkpoint files exist
        When: Checkpoints are presented for selection
        Then: Each checkpoint shows timestamp, phase count, problem preview
        """
        # Arrange
        selector = MultiCheckpointSelector(ask_tool=Mock())

        # Act
        info_1 = selector.format_checkpoint_info(two_checkpoints[0], 1)
        info_2 = selector.format_checkpoint_info(two_checkpoints[1], 2)

        # Assert
        assert "[1]" in info_1
        assert "[2]" in info_2
        assert "/6 phases" in info_1
        assert "/6 phases" in info_2
        assert "Problem:" in info_1
        assert "Problem:" in info_2

    def test_should_show_timestamp_for_each_checkpoint(
        self,
        three_checkpoints: List[Dict[str, Any]]
    ):
        """
        Scenario: Timestamp shown for each checkpoint
        Given: Multiple checkpoints with different timestamps
        When: Checkpoint info is formatted
        Then: Each checkpoint displays its timestamp
        """
        # Arrange
        selector = MultiCheckpointSelector(ask_tool=Mock())

        # Act & Assert
        for i, checkpoint in enumerate(three_checkpoints):
            info = selector.format_checkpoint_info(checkpoint, i + 1)
            timestamp = checkpoint.get("timestamp")
            assert timestamp in info

    def test_should_show_phases_completed_for_each_checkpoint(
        self,
        three_checkpoints: List[Dict[str, Any]]
    ):
        """
        Scenario: Phase completion count shown for each checkpoint
        Given: Checkpoints with different phase completions (1, 2, 3)
        When: Checkpoint info is formatted
        Then: Each shows: "X/6 phases"
        """
        # Arrange
        selector = MultiCheckpointSelector(ask_tool=Mock())

        # Act
        info_1 = selector.format_checkpoint_info(three_checkpoints[0], 1)
        info_2 = selector.format_checkpoint_info(three_checkpoints[1], 2)
        info_3 = selector.format_checkpoint_info(three_checkpoints[2], 3)

        # Assert
        assert "/6 phases" in info_1
        assert "/6 phases" in info_2
        assert "/6 phases" in info_3

    def test_should_show_problem_statement_preview(
        self,
        two_checkpoints: List[Dict[str, Any]]
    ):
        """
        Scenario: Problem statement preview (first 50 chars)
        Given: Checkpoints with problem statements
        When: Checkpoint info is formatted
        Then: Shows first 50 characters of problem
        """
        # Arrange
        selector = MultiCheckpointSelector(ask_tool=Mock())

        # Act
        info_1 = selector.format_checkpoint_info(two_checkpoints[0], 1)

        # Assert
        problem = two_checkpoints[0]["brainstorm_context"]["problem_statement"]
        preview = problem[:50]
        assert preview in info_1

    def test_should_sort_checkpoints_newest_first(
        self,
        three_checkpoints: List[Dict[str, Any]]
    ):
        """
        Scenario: Sort checkpoints by timestamp (newest first)
        Given: Three checkpoints with timestamps:
               - 2025-12-24T15:45:30.789Z (newest)
               - 2025-12-23T10:30:45.456Z (middle)
               - 2025-12-22T15:30:45.123Z (oldest)
        When: sort_checkpoints_by_timestamp() is called
        Then: Sorted order is: newest, middle, oldest
        """
        # Arrange
        selector = MultiCheckpointSelector(ask_tool=Mock())
        checkpoint_paths = [
            "devforgeai/temp/.ideation-checkpoint-session1.yaml",
            "devforgeai/temp/.ideation-checkpoint-session2.yaml",
            "devforgeai/temp/.ideation-checkpoint-session3.yaml",
        ]

        # Act
        sorted_paths, sorted_data = selector.sort_checkpoints_by_timestamp(
            checkpoint_paths,
            three_checkpoints
        )

        # Assert
        # Verify sort order by timestamp (newest first)
        assert sorted_data[0].get("timestamp") == "2025-12-24T15:45:30.789Z"  # Newest
        assert sorted_data[1].get("timestamp") == "2025-12-23T10:30:45.456Z"  # Middle
        assert sorted_data[2].get("timestamp") == "2025-12-22T15:30:45.123Z"  # Oldest

    def test_should_handle_two_checkpoints_selection(
        self,
        mock_ask_user_question_select_checkpoint: Mock,
        two_checkpoints: List[Dict[str, Any]],
        second_session_id: str
    ):
        """
        Scenario: User can select from 2 checkpoints
        Given: Two checkpoint files exist
        When: ask_checkpoint_selection() is called
        Then: User can select between two options
        """
        # Arrange
        selector = MultiCheckpointSelector(ask_tool=mock_ask_user_question_select_checkpoint)
        options = [
            selector.format_checkpoint_info(two_checkpoints[0], 1),
            selector.format_checkpoint_info(two_checkpoints[1], 2),
        ]
        mock_ask_user_question_select_checkpoint.ask.return_value = {"selected_index": 0}

        # Act
        result = selector.ask_checkpoint_selection(options)

        # Assert
        assert result["selected_index"] == 0

    def test_should_handle_three_checkpoints_selection(
        self,
        mock_ask_user_question_select_checkpoint: Mock,
        three_checkpoints: List[Dict[str, Any]]
    ):
        """
        Scenario: User can select from 3 checkpoints
        Given: Three checkpoint files exist
        When: ask_checkpoint_selection() is called
        Then: User can select from three options
        """
        # Arrange
        selector = MultiCheckpointSelector(ask_tool=mock_ask_user_question_select_checkpoint)
        options = [
            selector.format_checkpoint_info(three_checkpoints[0], 1),
            selector.format_checkpoint_info(three_checkpoints[1], 2),
            selector.format_checkpoint_info(three_checkpoints[2], 3),
        ]
        mock_ask_user_question_select_checkpoint.ask.return_value = {"selected_index": 1}

        # Act
        result = selector.ask_checkpoint_selection(options)

        # Assert
        assert result["selected_index"] == 1

    def test_should_handle_five_checkpoints_selection(
        self,
        mock_ask_user_question_select_checkpoint: Mock,
        five_checkpoints: List[Dict[str, Any]]
    ):
        """
        Scenario: User can select from 5 checkpoints
        Given: Five checkpoint files exist
        When: ask_checkpoint_selection() is called
        Then: User can select from five options
        """
        # Arrange
        selector = MultiCheckpointSelector(ask_tool=mock_ask_user_question_select_checkpoint)
        options = [
            selector.format_checkpoint_info(five_checkpoints[i], i + 1)
            for i in range(len(five_checkpoints))
        ]
        mock_ask_user_question_select_checkpoint.ask.return_value = {"selected_index": 2}

        # Act
        result = selector.ask_checkpoint_selection(options)

        # Assert
        assert result["selected_index"] == 2

    def test_should_load_correct_checkpoint_based_on_selection(
        self,
        three_checkpoints: List[Dict[str, Any]]
    ):
        """
        Scenario: Load correct checkpoint based on user selection
        Given: Three checkpoints, user selects index 1
        When: load_selected_checkpoint() is called
        Then: Checkpoint at index 1 is loaded and returned
        """
        # Arrange
        selector = MultiCheckpointSelector(ask_tool=Mock())
        checkpoint_paths = ["path1", "path2", "path3"]
        selection = {"selected_index": 1}

        # Act
        result = selector.load_selected_checkpoint(
            selection,
            checkpoint_paths,
            three_checkpoints
        )

        # Assert
        assert result == three_checkpoints[1]
        assert result["current_phase"] == 3  # Second checkpoint is phase 3

    def test_should_handle_fresh_start_selection(
        self,
        three_checkpoints: List[Dict[str, Any]]
    ):
        """
        Scenario: Handle fresh start selection
        Given: Checkpoints available but user selects fresh start
        When: load_selected_checkpoint() is called with choice='fresh'
        Then: Empty dict returned (no checkpoint loaded)
        """
        # Arrange
        selector = MultiCheckpointSelector(ask_tool=Mock())
        checkpoint_paths = ["path1", "path2", "path3"]
        selection = {"choice": "fresh"}

        # Act
        result = selector.load_selected_checkpoint(
            selection,
            checkpoint_paths,
            three_checkpoints
        )

        # Assert
        assert result == {}

    def test_should_preserve_checkpoint_order_through_selection(
        self,
        three_checkpoints: List[Dict[str, Any]]
    ):
        """
        Scenario: Checkpoint order preserved through selection
        Given: Checkpoints sorted by timestamp (newest first)
        When: User selects first option
        Then: Newest checkpoint is loaded
        """
        # Arrange
        selector = MultiCheckpointSelector(ask_tool=Mock())
        checkpoint_paths = ["path1", "path2", "path3"]
        selection = {"selected_index": 0}

        # Act
        result = selector.load_selected_checkpoint(
            selection,
            checkpoint_paths,
            three_checkpoints
        )

        # Assert
        # First checkpoint should be the newest (phase 1, timestamp newest)
        assert result["timestamp"] == "2025-12-24T15:45:30.789Z"

    def test_should_display_newest_checkpoint_first(
        self,
        three_checkpoints: List[Dict[str, Any]]
    ):
        """
        Scenario: Newest checkpoint displayed as option [1]
        Given: Three checkpoints with different timestamps
        When: Options are formatted
        Then: Newest checkpoint is [1] (default selection)
        """
        # Arrange
        selector = MultiCheckpointSelector(ask_tool=Mock())

        # Act
        info = selector.format_checkpoint_info(three_checkpoints[0], 1)

        # Assert
        assert "[1]" in info
        assert three_checkpoints[0].get("timestamp") in info

    def test_should_format_multiple_checkpoints_with_indices(
        self,
        five_checkpoints: List[Dict[str, Any]]
    ):
        """
        Scenario: Format 5 checkpoints with indices 1-5
        Given: Five checkpoints
        When: format_checkpoint_info() called for each
        Then: Each formatted with correct index [1] through [5]
        """
        # Arrange
        selector = MultiCheckpointSelector(ask_tool=Mock())

        # Act
        infos = [
            selector.format_checkpoint_info(five_checkpoints[i], i + 1)
            for i in range(len(five_checkpoints))
        ]

        # Assert
        for i, info in enumerate(infos):
            assert f"[{i + 1}]" in info

    def test_should_handle_selection_from_various_indices(
        self,
        five_checkpoints: List[Dict[str, Any]]
    ):
        """
        Scenario: Handle selections from indices 0-4
        Given: Five checkpoints available
        When: Users select different indices
        Then: Each selection returns correct checkpoint
        """
        # Arrange
        selector = MultiCheckpointSelector(ask_tool=Mock())
        checkpoint_paths = ["p1", "p2", "p3", "p4", "p5"]

        # Act & Assert
        for index in range(len(five_checkpoints)):
            selection = {"selected_index": index}
            result = selector.load_selected_checkpoint(
                selection,
                checkpoint_paths,
                five_checkpoints
            )
            assert result == five_checkpoints[index]

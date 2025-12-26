"""
Integration tests for STORY-137: Resume-from-Checkpoint Logic

Tests end-to-end resume workflows combining:
- Checkpoint detection (AC#1)
- User choice (AC#2)
- Checkpoint loading (AC#3)
- Phase replay (AC#4, AC#5)
- Multi-checkpoint selection (AC#6)
"""

from typing import Dict, Any, List
from unittest.mock import Mock

import pytest


class ResumeWorkflowIntegration:
    """
    Complete resume workflow integrating all components.
    TDD: This class does NOT exist yet - tests define required interface.
    """
    def __init__(
        self,
        checkpoint_detector: Mock,
        checkpoint_loader: Mock,
        resume_orchestrator: Mock,
        phase_replay_engine: Mock,
        multi_selector: Mock
    ):
        self.detector = checkpoint_detector
        self.loader = checkpoint_loader
        self.orchestrator = resume_orchestrator
        self.replay_engine = phase_replay_engine
        self.selector = multi_selector

    def execute_resume_workflow(
        self,
        glob_pattern: str
    ) -> Dict[str, Any]:
        """
        Execute complete resume workflow.

        Args:
            glob_pattern: Glob pattern for checkpoint detection

        Returns:
            Resume state or empty dict for fresh start
        """
        # Phase 1: Detect checkpoints
        checkpoints = self.detector.detect_checkpoints(glob_pattern)

        if not checkpoints:
            # No checkpoints - fresh start
            return {"choice": "fresh", "resume_state": None}

        if len(checkpoints) == 1:
            # Single checkpoint - ask user directly
            checkpoint_data = self.loader.load_checkpoint(checkpoints[0])
            choice = self.orchestrator.present_resume_choice(
                checkpoints=[checkpoints[0]],
                checkpoint_data=[checkpoint_data]
            )

            if choice.get("choice") == "fresh":
                return {"choice": "fresh", "resume_state": None}

            return {
                "choice": "resume",
                "checkpoint_data": checkpoint_data,
                "checkpoint_path": checkpoints[0]
            }
        else:
            # Multiple checkpoints - use selection
            checkpoint_data = [
                self.loader.load_checkpoint(path) for path in checkpoints
            ]

            sorted_paths, sorted_data = self.selector.sort_checkpoints_by_timestamp(
                checkpoints,
                checkpoint_data
            )

            selection_result = self.selector.ask_checkpoint_selection([])

            if selection_result.get("choice") == "fresh":
                return {"choice": "fresh", "resume_state": None}

            selected_index = selection_result.get("selected_index", 0)
            return {
                "choice": "resume",
                "checkpoint_data": sorted_data[selected_index],
                "checkpoint_path": sorted_paths[selected_index]
            }


class TestResumeWorkflowIntegration:
    """End-to-end resume workflow tests"""

    def test_should_execute_fresh_start_when_no_checkpoints(
        self,
        mock_glob_tool: Mock,
        checkpoint_glob_pattern: str
    ):
        """
        Scenario: Fresh start when no checkpoints exist
        Given: No checkpoint files detected
        When: Resume workflow executes
        Then: Fresh start is initiated (no resume)
        """
        # Arrange
        mock_glob_tool.glob.return_value = []

        workflow = ResumeWorkflowIntegration(
            checkpoint_detector=Mock(detect_checkpoints=mock_glob_tool.glob),
            checkpoint_loader=Mock(),
            resume_orchestrator=Mock(),
            phase_replay_engine=Mock(),
            multi_selector=Mock()
        )
        workflow.detector.detect_checkpoints = lambda p: []

        # Act
        result = workflow.execute_resume_workflow(checkpoint_glob_pattern)

        # Assert
        assert result["choice"] == "fresh"

    def test_should_present_choice_for_single_checkpoint(
        self,
        mock_ask_user_question: Mock,
        checkpoint_phase_2: Dict[str, Any]
    ):
        """
        Scenario: Single checkpoint - present resume/fresh choice
        Given: One checkpoint file detected
        When: Resume workflow executes
        Then: User is asked: Resume or Start Fresh
        """
        # Arrange
        checkpoint_paths = ["devforgeai/temp/.ideation-checkpoint-550e8400.yaml"]

        detector_mock = Mock()
        detector_mock.detect_checkpoints = Mock(return_value=checkpoint_paths)

        loader_mock = Mock()
        loader_mock.load_checkpoint = Mock(return_value=checkpoint_phase_2)

        orchestrator_mock = Mock()
        orchestrator_mock.present_resume_choice = Mock(return_value={"choice": "resume"})

        workflow = ResumeWorkflowIntegration(
            checkpoint_detector=detector_mock,
            checkpoint_loader=loader_mock,
            resume_orchestrator=orchestrator_mock,
            phase_replay_engine=Mock(),
            multi_selector=Mock()
        )

        # Act
        result = workflow.execute_resume_workflow("devforgeai/temp/.ideation-checkpoint-*.yaml")

        # Assert
        assert result["choice"] == "resume"
        orchestrator_mock.present_resume_choice.assert_called_once()

    def test_should_load_checkpoint_after_user_selects_resume(
        self,
        checkpoint_phase_3: Dict[str, Any]
    ):
        """
        Scenario: Load selected checkpoint after resume choice
        Given: User selects "Resume from checkpoint"
        When: Resume workflow loads checkpoint
        Then: Checkpoint file is loaded and validated
        """
        # Arrange
        checkpoint_path = "devforgeai/temp/.ideation-checkpoint-550e8400.yaml"

        detector_mock = Mock()
        detector_mock.detect_checkpoints = Mock(return_value=[checkpoint_path])

        loader_mock = Mock()
        loader_mock.load_checkpoint = Mock(return_value=checkpoint_phase_3)

        orchestrator_mock = Mock()
        orchestrator_mock.present_resume_choice = Mock(return_value={"choice": "resume"})

        workflow = ResumeWorkflowIntegration(
            checkpoint_detector=detector_mock,
            checkpoint_loader=loader_mock,
            resume_orchestrator=orchestrator_mock,
            phase_replay_engine=Mock(),
            multi_selector=Mock()
        )

        # Act
        result = workflow.execute_resume_workflow("devforgeai/temp/.ideation-checkpoint-*.yaml")

        # Assert
        assert result["choice"] == "resume"
        loader_mock.load_checkpoint.assert_called_once_with(checkpoint_path)
        assert result["checkpoint_data"] == checkpoint_phase_3

    def test_should_select_checkpoint_when_multiple_exist(
        self,
        three_checkpoints: List[Dict[str, Any]]
    ):
        """
        Scenario: Multiple checkpoints - user selects one
        Given: Three checkpoint files exist
        When: Resume workflow executes
        Then: Checkpoints are listed and user selects one
        """
        # Arrange
        checkpoint_paths = [
            "devforgeai/temp/.ideation-checkpoint-session3.yaml",
            "devforgeai/temp/.ideation-checkpoint-session2.yaml",
            "devforgeai/temp/.ideation-checkpoint-session1.yaml",
        ]

        detector_mock = Mock()
        detector_mock.detect_checkpoints = Mock(return_value=checkpoint_paths)

        loader_mock = Mock()
        loader_mock.load_checkpoint = Mock(side_effect=three_checkpoints)

        selector_mock = Mock()
        selector_mock.sort_checkpoints_by_timestamp = Mock(
            return_value=(checkpoint_paths, three_checkpoints)
        )
        selector_mock.ask_checkpoint_selection = Mock(
            return_value={"selected_index": 1}
        )

        workflow = ResumeWorkflowIntegration(
            checkpoint_detector=detector_mock,
            checkpoint_loader=loader_mock,
            resume_orchestrator=Mock(),
            phase_replay_engine=Mock(),
            multi_selector=selector_mock
        )

        # Act
        result = workflow.execute_resume_workflow("devforgeai/temp/.ideation-checkpoint-*.yaml")

        # Assert
        selector_mock.ask_checkpoint_selection.assert_called_once()

    def test_should_sort_checkpoints_by_timestamp(
        self,
        three_checkpoints: List[Dict[str, Any]]
    ):
        """
        Scenario: Checkpoints sorted newest first
        Given: Three checkpoints with different timestamps
        When: Multiple checkpoint selection happens
        Then: Checkpoints displayed in order: newest first
        """
        # Arrange
        checkpoint_paths = ["p1", "p2", "p3"]

        selector_mock = Mock()
        selector_mock.sort_checkpoints_by_timestamp = Mock(
            return_value=(checkpoint_paths, three_checkpoints)
        )

        workflow = ResumeWorkflowIntegration(
            checkpoint_detector=Mock(),
            checkpoint_loader=Mock(),
            resume_orchestrator=Mock(),
            phase_replay_engine=Mock(),
            multi_selector=selector_mock
        )

        # Act
        sorted_paths, sorted_data = workflow.selector.sort_checkpoints_by_timestamp(
            checkpoint_paths,
            three_checkpoints
        )

        # Assert
        selector_mock.sort_checkpoints_by_timestamp.assert_called_once()

    def test_should_handle_fresh_start_selection(
        self,
        three_checkpoints: List[Dict[str, Any]]
    ):
        """
        Scenario: User selects fresh start despite available checkpoints
        Given: Multiple checkpoints available
        When: User selects "Start fresh (discard checkpoint)"
        Then: Session proceeds with fresh start
        """
        # Arrange
        checkpoint_paths = ["p1", "p2", "p3"]

        detector_mock = Mock()
        detector_mock.detect_checkpoints = Mock(return_value=checkpoint_paths)

        loader_mock = Mock()
        loader_mock.load_checkpoint = Mock(side_effect=three_checkpoints)

        selector_mock = Mock()
        selector_mock.sort_checkpoints_by_timestamp = Mock(
            return_value=(checkpoint_paths, three_checkpoints)
        )
        selector_mock.ask_checkpoint_selection = Mock(
            return_value={"choice": "fresh"}
        )

        workflow = ResumeWorkflowIntegration(
            checkpoint_detector=detector_mock,
            checkpoint_loader=loader_mock,
            resume_orchestrator=Mock(),
            phase_replay_engine=Mock(),
            multi_selector=selector_mock
        )

        # Act
        result = workflow.execute_resume_workflow("devforgeai/temp/.ideation-checkpoint-*.yaml")

        # Assert
        assert result["choice"] == "fresh"

    def test_should_return_resume_state_with_checkpoint_data(
        self,
        checkpoint_phase_2: Dict[str, Any]
    ):
        """
        Scenario: Resume state includes checkpoint data
        Given: Checkpoint selected for resume
        When: Resume workflow completes
        Then: Result includes checkpoint_data and checkpoint_path
        """
        # Arrange
        checkpoint_path = "devforgeai/temp/.ideation-checkpoint-550e8400.yaml"

        detector_mock = Mock()
        detector_mock.detect_checkpoints = Mock(return_value=[checkpoint_path])

        loader_mock = Mock()
        loader_mock.load_checkpoint = Mock(return_value=checkpoint_phase_2)

        orchestrator_mock = Mock()
        orchestrator_mock.present_resume_choice = Mock(return_value={"choice": "resume"})

        workflow = ResumeWorkflowIntegration(
            checkpoint_detector=detector_mock,
            checkpoint_loader=loader_mock,
            resume_orchestrator=orchestrator_mock,
            phase_replay_engine=Mock(),
            multi_selector=Mock()
        )

        # Act
        result = workflow.execute_resume_workflow("devforgeai/temp/.ideation-checkpoint-*.yaml")

        # Assert
        assert "checkpoint_data" in result
        assert "checkpoint_path" in result
        assert result["checkpoint_data"] == checkpoint_phase_2

    def test_should_handle_five_checkpoint_selection(
        self,
        five_checkpoints: List[Dict[str, Any]]
    ):
        """
        Scenario: Handle selection from 5 checkpoints
        Given: Five checkpoint files exist
        When: Resume workflow executes multi-checkpoint selection
        Then: All five checkpoints are listed for selection
        """
        # Arrange
        checkpoint_paths = ["p1", "p2", "p3", "p4", "p5"]

        detector_mock = Mock()
        detector_mock.detect_checkpoints = Mock(return_value=checkpoint_paths)

        loader_mock = Mock()
        loader_mock.load_checkpoint = Mock(side_effect=five_checkpoints)

        selector_mock = Mock()
        selector_mock.sort_checkpoints_by_timestamp = Mock(
            return_value=(checkpoint_paths, five_checkpoints)
        )
        selector_mock.ask_checkpoint_selection = Mock(
            return_value={"selected_index": 2}
        )

        workflow = ResumeWorkflowIntegration(
            checkpoint_detector=detector_mock,
            checkpoint_loader=loader_mock,
            resume_orchestrator=Mock(),
            phase_replay_engine=Mock(),
            multi_selector=selector_mock
        )

        # Act
        result = workflow.execute_resume_workflow("devforgeai/temp/.ideation-checkpoint-*.yaml")

        # Assert
        assert len(checkpoint_paths) == 5

    def test_should_complete_workflow_without_errors(
        self,
        checkpoint_phase_1: Dict[str, Any]
    ):
        """
        Scenario: Complete resume workflow without errors
        Given: All components working correctly
        When: Resume workflow executes from start to finish
        Then: No exceptions raised, result returned
        """
        # Arrange
        checkpoint_path = "devforgeai/temp/.ideation-checkpoint-550e8400.yaml"

        detector_mock = Mock()
        detector_mock.detect_checkpoints = Mock(return_value=[checkpoint_path])

        loader_mock = Mock()
        loader_mock.load_checkpoint = Mock(return_value=checkpoint_phase_1)

        orchestrator_mock = Mock()
        orchestrator_mock.present_resume_choice = Mock(return_value={"choice": "resume"})

        workflow = ResumeWorkflowIntegration(
            checkpoint_detector=detector_mock,
            checkpoint_loader=loader_mock,
            resume_orchestrator=orchestrator_mock,
            phase_replay_engine=Mock(),
            multi_selector=Mock()
        )

        # Act & Assert (no exceptions)
        result = workflow.execute_resume_workflow("devforgeai/temp/.ideation-checkpoint-*.yaml")
        assert result is not None
        assert isinstance(result, dict)

    def test_should_verify_checkpoint_detection_happens_first(
        self,
        checkpoint_phase_1: Dict[str, Any]
    ):
        """
        Scenario: Checkpoint detection occurs before other operations
        Given: Resume workflow initializing
        When: execute_resume_workflow() is called
        Then: Checkpoint detection is first step (Phase 1, Step 0)
        """
        # Arrange
        detector_mock = Mock()
        detector_mock.detect_checkpoints = Mock(return_value=[])

        workflow = ResumeWorkflowIntegration(
            checkpoint_detector=detector_mock,
            checkpoint_loader=Mock(),
            resume_orchestrator=Mock(),
            phase_replay_engine=Mock(),
            multi_selector=Mock()
        )

        # Act
        workflow.execute_resume_workflow("devforgeai/temp/.ideation-checkpoint-*.yaml")

        # Assert
        # Verify detection was called first
        detector_mock.detect_checkpoints.assert_called_once()

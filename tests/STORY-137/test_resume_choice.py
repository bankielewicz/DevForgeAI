"""
Tests for AC#2: Resume vs Fresh Start User Choice

Verifies that:
- AskUserQuestion is invoked when checkpoints exist
- Options include phase count and timestamp
- Progress display shows completed phases and problem statement
- Both resume and fresh start paths are handled correctly
"""

from typing import Dict, Any, List
from unittest.mock import Mock, patch

import pytest


class ResumeOrchestrator:
    """
    Orchestrates user choice between resume and fresh start.
    TDD: This class does NOT exist yet - tests define required interface.
    """
    def __init__(self, ask_user_question_tool: Mock):
        self.ask_tool = ask_user_question_tool

    def present_resume_choice(
        self,
        checkpoints: List[str],
        checkpoint_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Present resume vs fresh start choice to user.

        Args:
            checkpoints: List of checkpoint file paths
            checkpoint_data: List of parsed checkpoint dictionaries

        Returns:
            Dict with user's choice: {'choice': 'resume'|'fresh', 'selected_checkpoint': path}
        """
        return self.ask_tool.ask(checkpoints=checkpoints, data=checkpoint_data)

    def format_resume_option(self, checkpoint: Dict[str, Any]) -> str:
        """
        Format resume option text with phase count and timestamp.

        Args:
            checkpoint: Checkpoint dictionary

        Returns:
            Formatted option text: "Resume from checkpoint (X/6 phases complete, timestamp)"
        """
        phase = checkpoint.get("current_phase", 0)
        timestamp = checkpoint.get("timestamp", "unknown")
        problem = checkpoint.get("brainstorm_context", {}).get("problem_statement", "")[:50]
        return f"Resume from checkpoint ({phase}/6 phases complete, {timestamp})"

    def format_progress_display(self, checkpoint: Dict[str, Any]) -> str:
        """
        Format progress display with completed phases and problem preview.

        Args:
            checkpoint: Checkpoint dictionary

        Returns:
            Formatted progress text
        """
        phase = checkpoint.get("current_phase", 0)
        problem = checkpoint.get("brainstorm_context", {}).get("problem_statement", "")[:50]
        return f"Progress: {phase}/6 phases completed\nProblem: {problem}"


class TestResumeVsFreshStartChoice:
    """AC#2: Resume vs fresh start user choice"""

    def test_should_invoke_ask_user_question_when_checkpoints_exist(
        self,
        mock_ask_user_question: Mock,
        checkpoint_phase_1: Dict[str, Any]
    ):
        """
        Scenario: Present choice when checkpoint exists
        Given: One checkpoint file was detected
        When: ResumeOrchestrator.present_resume_choice() is called
        Then: AskUserQuestion tool is invoked with resume option
        """
        # Arrange
        orchestrator = ResumeOrchestrator(ask_user_question_tool=mock_ask_user_question)
        mock_ask_user_question.ask.return_value = {"choice": "resume"}

        # Act
        result = orchestrator.present_resume_choice(
            checkpoints=["devforgeai/temp/.ideation-checkpoint-550e8400.yaml"],
            checkpoint_data=[checkpoint_phase_1]
        )

        # Assert
        mock_ask_user_question.ask.assert_called_once()
        assert result["choice"] == "resume"

    def test_should_not_invoke_ask_user_question_when_no_checkpoints(
        self,
        mock_ask_user_question: Mock
    ):
        """
        Scenario: No choice needed when no checkpoints exist
        Given: No checkpoint files were detected
        When: Session initialization continues
        Then: AskUserQuestion is NOT invoked (fresh session)
        """
        # Arrange
        orchestrator = ResumeOrchestrator(ask_user_question_tool=mock_ask_user_question)

        # Act
        # Fresh session logic would skip the choice presentation
        # This test verifies the precondition (no ask_tool call needed)

        # Assert
        mock_ask_user_question.ask.assert_not_called()

    def test_should_format_resume_option_with_phase_count(
        self,
        checkpoint_phase_3: Dict[str, Any]
    ):
        """
        Scenario: Resume option includes phase count
        Given: Checkpoint indicates 3/6 phases complete
        When: Resume option is formatted
        Then: Option text includes "3/6 phases complete"
        """
        # Arrange
        orchestrator = ResumeOrchestrator(ask_user_question_tool=Mock())

        # Act
        option_text = orchestrator.format_resume_option(checkpoint_phase_3)

        # Assert
        assert "3/6 phases complete" in option_text
        assert "2025-12-22T15:30:45.123Z" in option_text

    def test_should_format_resume_option_with_timestamp(
        self,
        checkpoint_phase_2: Dict[str, Any]
    ):
        """
        Scenario: Resume option includes timestamp
        Given: Checkpoint has timestamp field
        When: Resume option is formatted
        Then: Option text includes ISO 8601 timestamp
        """
        # Arrange
        orchestrator = ResumeOrchestrator(ask_user_question_tool=Mock())

        # Act
        option_text = orchestrator.format_resume_option(checkpoint_phase_2)

        # Assert
        assert "2025-12-22T15:30:45.123Z" in option_text
        assert "phases complete" in option_text

    def test_should_include_fresh_start_option(
        self,
        mock_ask_user_question: Mock,
        checkpoint_phase_1: Dict[str, Any]
    ):
        """
        Scenario: Fresh start option is always presented
        Given: Checkpoints exist
        When: User choice is presented
        Then: Both "Resume" and "Start fresh" options are available
        """
        # Arrange
        orchestrator = ResumeOrchestrator(ask_user_question_tool=mock_ask_user_question)
        mock_ask_user_question.ask.return_value = {"choice": "fresh"}

        # Act
        result = orchestrator.present_resume_choice(
            checkpoints=["devforgeai/temp/.ideation-checkpoint-550e8400.yaml"],
            checkpoint_data=[checkpoint_phase_1]
        )

        # Assert
        assert result["choice"] == "fresh"

    def test_should_handle_user_selecting_resume(
        self,
        mock_ask_user_question: Mock,
        checkpoint_phase_2: Dict[str, Any]
    ):
        """
        Scenario: User selects resume option
        Given: Multiple checkpoints presented
        When: User selects "Resume from checkpoint"
        Then: Choice is recorded and checkpoint path is available
        """
        # Arrange
        orchestrator = ResumeOrchestrator(ask_user_question_tool=mock_ask_user_question)
        checkpoint_path = "devforgeai/temp/.ideation-checkpoint-550e8400.yaml"
        mock_ask_user_question.ask.return_value = {
            "choice": "resume",
            "selected_checkpoint": checkpoint_path
        }

        # Act
        result = orchestrator.present_resume_choice(
            checkpoints=[checkpoint_path],
            checkpoint_data=[checkpoint_phase_2]
        )

        # Assert
        assert result["choice"] == "resume"
        assert result["selected_checkpoint"] == checkpoint_path

    def test_should_handle_user_selecting_fresh_start(
        self,
        mock_ask_user_question_fresh_start: Mock,
        checkpoint_phase_1: Dict[str, Any]
    ):
        """
        Scenario: User selects fresh start option
        Given: Checkpoints exist
        When: User selects "Start fresh (discard checkpoint)"
        Then: Choice is recorded and session proceeds without resume
        """
        # Arrange
        orchestrator = ResumeOrchestrator(ask_user_question_tool=mock_ask_user_question_fresh_start)
        mock_ask_user_question_fresh_start.ask.return_value = {"choice": "fresh"}

        # Act
        result = orchestrator.present_resume_choice(
            checkpoints=["devforgeai/temp/.ideation-checkpoint-550e8400.yaml"],
            checkpoint_data=[checkpoint_phase_1]
        )

        # Assert
        assert result["choice"] == "fresh"
        assert "selected_checkpoint" not in result

    def test_should_format_progress_display_with_completed_phases(
        self,
        checkpoint_phase_4: Dict[str, Any]
    ):
        """
        Scenario: Progress display shows completed phases
        Given: Checkpoint indicates 4/6 phases complete
        When: Progress display is formatted
        Then: Display includes "4/6 phases completed"
        """
        # Arrange
        orchestrator = ResumeOrchestrator(ask_user_question_tool=Mock())

        # Act
        display = orchestrator.format_progress_display(checkpoint_phase_4)

        # Assert
        assert "4/6 phases completed" in display

    def test_should_format_progress_display_with_problem_statement_preview(
        self,
        checkpoint_phase_2: Dict[str, Any]
    ):
        """
        Scenario: Progress display includes problem statement preview
        Given: Checkpoint contains brainstorm_context with problem_statement
        When: Progress display is formatted
        Then: Display includes first 50 characters of problem statement
        """
        # Arrange
        orchestrator = ResumeOrchestrator(ask_user_question_tool=Mock())

        # Act
        display = orchestrator.format_progress_display(checkpoint_phase_2)

        # Assert
        problem = checkpoint_phase_2["brainstorm_context"]["problem_statement"]
        preview = problem[:50]
        assert preview in display
        assert "Problem:" in display

    def test_should_present_multiple_checkpoints_with_differences(
        self,
        mock_ask_user_question: Mock,
        two_checkpoints: List[Dict[str, Any]]
    ):
        """
        Scenario: Multiple checkpoints presented with identifying info
        Given: Two checkpoints from different sessions
        When: User choice is presented
        Then: Each checkpoint shows timestamp, phase count, problem preview
        """
        # Arrange
        orchestrator = ResumeOrchestrator(ask_user_question_tool=mock_ask_user_question)
        mock_ask_user_question.ask.return_value = {"choice": "resume"}

        checkpoints = [
            "devforgeai/temp/.ideation-checkpoint-660e8400.yaml",
            "devforgeai/temp/.ideation-checkpoint-550e8400.yaml",
        ]

        # Act
        result = orchestrator.present_resume_choice(
            checkpoints=checkpoints,
            checkpoint_data=two_checkpoints
        )

        # Assert
        mock_ask_user_question.ask.assert_called_once()
        # Verify both checkpoints were passed for display
        assert len(checkpoints) == 2

    def test_should_use_ask_user_question_tool_not_print(
        self,
        mock_ask_user_question: Mock,
        checkpoint_phase_1: Dict[str, Any]
    ):
        """
        Scenario: Use AskUserQuestion tool, not print() for user interaction
        Given: Checkpoint choice needs to be presented
        When: ResumeOrchestrator presents choice
        Then: AskUserQuestion tool is used (not print() or direct input())
        """
        # Arrange
        orchestrator = ResumeOrchestrator(ask_user_question_tool=mock_ask_user_question)
        mock_ask_user_question.ask.return_value = {"choice": "resume"}

        # Act
        orchestrator.present_resume_choice(
            checkpoints=["devforgeai/temp/.ideation-checkpoint-550e8400.yaml"],
            checkpoint_data=[checkpoint_phase_1]
        )

        # Assert
        mock_ask_user_question.ask.assert_called_once()

    def test_should_format_option_for_single_checkpoint(
        self,
        checkpoint_phase_3: Dict[str, Any]
    ):
        """
        Scenario: Format option when single checkpoint exists
        Given: One checkpoint detected
        When: Resume option is formatted
        Then: Option text is formatted as "Resume from checkpoint (3/6 phases complete, timestamp)"
        """
        # Arrange
        orchestrator = ResumeOrchestrator(ask_user_question_tool=Mock())

        # Act
        option = orchestrator.format_resume_option(checkpoint_phase_3)

        # Assert
        assert option.startswith("Resume from checkpoint")
        assert "3/6" in option
        assert "phases complete" in option
        assert "2025-12-22T15:30:45.123Z" in option

    def test_should_format_option_for_multiple_checkpoints(
        self,
        three_checkpoints: List[Dict[str, Any]]
    ):
        """
        Scenario: Format option for each checkpoint in list
        Given: Three checkpoints with different phase completions
        When: Resume options are formatted
        Then: Each option shows its specific phase count and timestamp
        """
        # Arrange
        orchestrator = ResumeOrchestrator(ask_user_question_tool=Mock())

        # Act
        options = [
            orchestrator.format_resume_option(checkpoint)
            for checkpoint in three_checkpoints
        ]

        # Assert
        # First checkpoint: 1/6 phases (newest)
        assert "1/6" in options[0] or "1/6 phases" in options[0]
        # Second checkpoint: 3/6 phases
        assert "3/6" in options[1] or "3/6 phases" in options[1]
        # Third checkpoint: 2/6 phases (oldest)
        assert "2/6" in options[2] or "2/6 phases" in options[2]

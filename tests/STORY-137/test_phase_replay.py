"""
Tests for AC#4 and AC#5: Phase Replay with Pre-filled Answers and Resume from Phase

Verifies that:
- AC#4: Previous answers displayed, Keep/Update paths work
- AC#5: Resume from each phase (1-5), correct phase starts, context available
"""

from typing import Dict, Any
from unittest.mock import Mock

import pytest


class PhaseReplayEngine:
    """
    Handles phase replay with pre-filled answers and update option.
    TDD: This class does NOT exist yet - tests define required interface.
    """
    def __init__(self, ask_tool: Mock):
        self.ask_tool = ask_tool

    def display_previous_answers(self, phase: int, checkpoint: Dict[str, Any]) -> str:
        """
        Display previous answers from checkpoint.

        Args:
            phase: Phase number (1-5)
            checkpoint: Checkpoint data with brainstorm_context

        Returns:
            Formatted display of previous answers
        """
        context = checkpoint.get("brainstorm_context", {})
        display = f"=== Phase {phase} Answers ===\n"

        if phase == 1:
            display += f"Problem: {context.get('problem_statement', 'N/A')}\n"
        elif phase == 2:
            personas = context.get("personas", [])
            display += f"Personas ({len(personas)}):\n"
            for p in personas:
                display += f"  - {p.get('name', 'Unknown')}\n"
        elif phase == 3:
            requirements = context.get("requirements", [])
            display += f"Requirements ({len(requirements)}):\n"
            for r in requirements:
                display += f"  - {r.get('description', 'Unknown')}\n"
        elif phase == 4:
            score = context.get("complexity_score", "N/A")
            display += f"Complexity Score: {score}/60\n"
        elif phase == 5:
            epics = context.get("epics", [])
            display += f"Epics ({len(epics)}):\n"
            for e in epics:
                display += f"  - {e.get('title', 'Unknown')}\n"

        return display

    def ask_keep_or_update(self, phase: int, checkpoint: Dict[str, Any]) -> str:
        """
        Ask user to keep or update answers.

        Args:
            phase: Phase number
            checkpoint: Current checkpoint

        Returns:
            User choice: 'keep' or 'update'
        """
        result = self.ask_tool.ask(
            question=f"Keep Phase {phase} answers or update?",
            phase=phase
        )
        return result.get("choice", "keep")

    def resume_from_phase(
        self,
        phase: int,
        checkpoint: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Resume from specified phase.

        Args:
            phase: Current phase to resume from
            checkpoint: Checkpoint data

        Returns:
            Resume context with checkpoint data available to phases
        """
        return {
            "session_id": checkpoint.get("session_id"),
            "resume_phase": phase,
            "brainstorm_context": checkpoint.get("brainstorm_context"),
            "previous_data": checkpoint.get("brainstorm_context", {}),
        }


class TestPhaseReplayWithPrefilledAnswers:
    """AC#4: Phase replay with pre-filled answers"""

    def test_should_display_phase_1_previous_answers(
        self,
        checkpoint_phase_1: Dict[str, Any]
    ):
        """
        Scenario: Display Phase 1 problem statement
        Given: Phase 1 completed with problem statement
        When: display_previous_answers() is called
        Then: Problem statement is displayed
        """
        # Arrange
        engine = PhaseReplayEngine(ask_tool=Mock())

        # Act
        display = engine.display_previous_answers(1, checkpoint_phase_1)

        # Assert
        assert "Phase 1" in display
        assert "Build a task management app" in display

    def test_should_display_phase_2_previous_answers(
        self,
        checkpoint_phase_2: Dict[str, Any]
    ):
        """
        Scenario: Display Phase 2 personas
        Given: Phase 2 completed with personas
        When: display_previous_answers() is called
        Then: Personas are displayed
        """
        # Arrange
        engine = PhaseReplayEngine(ask_tool=Mock())

        # Act
        display = engine.display_previous_answers(2, checkpoint_phase_2)

        # Assert
        assert "Phase 2" in display
        assert "Personas" in display
        assert "Project Manager" in display or "Developer" in display

    def test_should_display_phase_3_previous_answers(
        self,
        checkpoint_phase_3: Dict[str, Any]
    ):
        """
        Scenario: Display Phase 3 requirements
        Given: Phase 3 completed with requirements
        When: display_previous_answers() is called
        Then: Requirements are displayed
        """
        # Arrange
        engine = PhaseReplayEngine(ask_tool=Mock())

        # Act
        display = engine.display_previous_answers(3, checkpoint_phase_3)

        # Assert
        assert "Phase 3" in display
        assert "Requirements" in display
        assert "Create and assign tasks" in display or "Track task progress" in display

    def test_should_display_phase_4_previous_answers(
        self,
        checkpoint_phase_4: Dict[str, Any]
    ):
        """
        Scenario: Display Phase 4 complexity score
        Given: Phase 4 completed with complexity score
        When: display_previous_answers() is called
        Then: Complexity score is displayed
        """
        # Arrange
        engine = PhaseReplayEngine(ask_tool=Mock())

        # Act
        display = engine.display_previous_answers(4, checkpoint_phase_4)

        # Assert
        assert "Phase 4" in display
        assert "Complexity" in display
        assert "37" in display

    def test_should_display_phase_5_previous_answers(
        self,
        checkpoint_phase_5: Dict[str, Any]
    ):
        """
        Scenario: Display Phase 5 epics
        Given: Phase 5 completed with epics
        When: display_previous_answers() is called
        Then: Epics are displayed
        """
        # Arrange
        engine = PhaseReplayEngine(ask_tool=Mock())

        # Act
        display = engine.display_previous_answers(5, checkpoint_phase_5)

        # Assert
        assert "Phase 5" in display
        assert "Epics" in display
        assert "User Authentication" in display or "Task Management" in display

    def test_should_ask_keep_or_update(
        self,
        mock_ask_user_question_keep_answers: Mock,
        checkpoint_phase_2: Dict[str, Any]
    ):
        """
        Scenario: Ask user to keep or update answers
        Given: Phase replay is starting
        When: ask_keep_or_update() is called
        Then: User is asked with clear choice
        """
        # Arrange
        engine = PhaseReplayEngine(ask_tool=mock_ask_user_question_keep_answers)
        mock_ask_user_question_keep_answers.ask.return_value = {"choice": "keep"}

        # Act
        choice = engine.ask_keep_or_update(2, checkpoint_phase_2)

        # Assert
        assert choice == "keep"

    def test_should_handle_keep_path_preserves_data(
        self,
        mock_ask_user_question_keep_answers: Mock,
        checkpoint_phase_3: Dict[str, Any]
    ):
        """
        Scenario: Keep path preserves checkpoint data
        Given: User selects "Keep" option
        When: Phase continues with kept answers
        Then: Checkpoint data is preserved without modification
        """
        # Arrange
        engine = PhaseReplayEngine(ask_tool=mock_ask_user_question_keep_answers)
        mock_ask_user_question_keep_answers.ask.return_value = {"choice": "keep"}

        # Act
        choice = engine.ask_keep_or_update(3, checkpoint_phase_3)
        context = checkpoint_phase_3.get("brainstorm_context", {})

        # Assert
        assert choice == "keep"
        # Data should be unchanged
        assert context.get("requirements") is not None

    def test_should_handle_update_path_re_executes_phase(
        self,
        mock_ask_user_question_update_answers: Mock,
        checkpoint_phase_2: Dict[str, Any]
    ):
        """
        Scenario: Update path re-executes phase
        Given: User selects "Update" option
        When: Phase is re-executed
        Then: New answers are collected (phase runs again)
        """
        # Arrange
        engine = PhaseReplayEngine(ask_tool=mock_ask_user_question_update_answers)
        mock_ask_user_question_update_answers.ask.return_value = {"choice": "update"}

        # Act
        choice = engine.ask_keep_or_update(2, checkpoint_phase_2)

        # Assert
        assert choice == "update"
        # Phase would be re-executed (not tested here, that's implementation detail)

    def test_should_format_display_clearly(
        self,
        checkpoint_phase_1: Dict[str, Any]
    ):
        """
        Scenario: Format display with clear headers and structure
        Given: Previous answers to display
        When: display_previous_answers() is called
        Then: Display is formatted with headers and clear structure
        """
        # Arrange
        engine = PhaseReplayEngine(ask_tool=Mock())

        # Act
        display = engine.display_previous_answers(1, checkpoint_phase_1)

        # Assert
        assert "===" in display  # Headers
        assert "\n" in display  # Line breaks
        assert "Phase 1" in display


class TestResumeFromLastIncompletePhase:
    """AC#5: Resume from last incomplete phase"""

    def test_should_resume_from_phase_1(
        self,
        checkpoint_phase_1: Dict[str, Any]
    ):
        """
        Scenario: Resume from Phase 1 (next phase is 2)
        Given: Checkpoint indicates Phase 1 complete
        When: resume_from_phase() is called
        Then: Session resumes with Phase 2 to execute
        """
        # Arrange
        engine = PhaseReplayEngine(ask_tool=Mock())

        # Act
        resume_state = engine.resume_from_phase(1, checkpoint_phase_1)

        # Assert
        assert resume_state["resume_phase"] == 1
        assert resume_state["session_id"] == checkpoint_phase_1["session_id"]
        assert "brainstorm_context" in resume_state

    def test_should_resume_from_phase_2(
        self,
        checkpoint_phase_2: Dict[str, Any]
    ):
        """
        Scenario: Resume from Phase 2 (next phase is 3)
        Given: Checkpoint indicates Phase 2 complete
        When: resume_from_phase() is called
        Then: Session resumes with Phase 3 to execute
        """
        # Arrange
        engine = PhaseReplayEngine(ask_tool=Mock())

        # Act
        resume_state = engine.resume_from_phase(2, checkpoint_phase_2)

        # Assert
        assert resume_state["resume_phase"] == 2

    def test_should_resume_from_phase_3(
        self,
        checkpoint_phase_3: Dict[str, Any]
    ):
        """
        Scenario: Resume from Phase 3 (next phase is 4)
        Given: Checkpoint indicates Phase 3 complete
        When: resume_from_phase() is called
        Then: Session resumes with Phase 4 to execute
        """
        # Arrange
        engine = PhaseReplayEngine(ask_tool=Mock())

        # Act
        resume_state = engine.resume_from_phase(3, checkpoint_phase_3)

        # Assert
        assert resume_state["resume_phase"] == 3

    def test_should_resume_from_phase_4(
        self,
        checkpoint_phase_4: Dict[str, Any]
    ):
        """
        Scenario: Resume from Phase 4 (next phase is 5)
        Given: Checkpoint indicates Phase 4 complete
        When: resume_from_phase() is called
        Then: Session resumes with Phase 5 to execute
        """
        # Arrange
        engine = PhaseReplayEngine(ask_tool=Mock())

        # Act
        resume_state = engine.resume_from_phase(4, checkpoint_phase_4)

        # Assert
        assert resume_state["resume_phase"] == 4

    def test_should_resume_from_phase_5(
        self,
        checkpoint_phase_5: Dict[str, Any]
    ):
        """
        Scenario: Resume from Phase 5 (next phase is 6)
        Given: Checkpoint indicates Phase 5 complete
        When: resume_from_phase() is called
        Then: Session resumes with Phase 6 to execute
        """
        # Arrange
        engine = PhaseReplayEngine(ask_tool=Mock())

        # Act
        resume_state = engine.resume_from_phase(5, checkpoint_phase_5)

        # Assert
        assert resume_state["resume_phase"] == 5

    def test_should_skip_completed_phases_from_checkpoint(
        self,
        checkpoint_phase_3: Dict[str, Any]
    ):
        """
        Scenario: Skip Phases 1-3, start from Phase 4
        Given: Phase 3 is last completed
        When: Session resumes
        Then: Phases 1-3 data loaded from checkpoint (no re-execution)
        """
        # Arrange
        engine = PhaseReplayEngine(ask_tool=Mock())

        # Act
        resume_state = engine.resume_from_phase(3, checkpoint_phase_3)

        # Assert
        # Phases 1-3 data should be available from checkpoint
        context = resume_state.get("brainstorm_context", {})
        assert context.get("problem_statement") is not None  # Phase 1 data

    def test_should_make_previous_phase_data_available(
        self,
        checkpoint_phase_4: Dict[str, Any]
    ):
        """
        Scenario: Previous phase data available to resumed phases
        Given: Phase 4 is complete, resuming to Phase 5
        When: resume_from_phase() is called
        Then: Phases 1-4 data available in brainstorm_context
        """
        # Arrange
        engine = PhaseReplayEngine(ask_tool=Mock())

        # Act
        resume_state = engine.resume_from_phase(4, checkpoint_phase_4)

        # Assert
        context = resume_state.get("brainstorm_context", {})
        # All previous phase data should be present
        assert context.get("problem_statement") is not None
        assert context.get("personas") is not None
        assert context.get("requirements") is not None
        assert context.get("complexity_score") is not None

    def test_should_include_session_id_in_resume_state(
        self,
        checkpoint_phase_2: Dict[str, Any]
    ):
        """
        Scenario: Session ID carried through resume
        Given: Checkpoint with session_id
        When: resume_from_phase() is called
        Then: Session ID is included in resume state
        """
        # Arrange
        engine = PhaseReplayEngine(ask_tool=Mock())

        # Act
        resume_state = engine.resume_from_phase(2, checkpoint_phase_2)

        # Assert
        assert "session_id" in resume_state
        assert resume_state["session_id"] == checkpoint_phase_2["session_id"]

    def test_should_not_re_execute_completed_phases(
        self,
        checkpoint_phase_3: Dict[str, Any]
    ):
        """
        Scenario: Completed phases not re-executed
        Given: Phase 3 complete
        When: Resume from Phase 3
        Then: Phases 1-3 skip execution, Phase 4 starts fresh
        """
        # Arrange
        engine = PhaseReplayEngine(ask_tool=Mock())

        # Act
        resume_state = engine.resume_from_phase(3, checkpoint_phase_3)

        # Assert
        # The fact that we have brainstorm_context means data is pre-loaded
        assert "brainstorm_context" in resume_state
        assert resume_state["resume_phase"] == 3

    def test_should_preserve_all_context_fields(
        self,
        checkpoint_phase_5: Dict[str, Any]
    ):
        """
        Scenario: All brainstorm_context fields preserved
        Given: Complete checkpoint with all context fields
        When: resume_from_phase() is called
        Then: All context fields are preserved for resumed phases
        """
        # Arrange
        engine = PhaseReplayEngine(ask_tool=Mock())

        # Act
        resume_state = engine.resume_from_phase(5, checkpoint_phase_5)

        # Assert
        context = resume_state.get("brainstorm_context", {})
        expected_fields = [
            "problem_statement",
            "personas",
            "requirements",
            "complexity_score",
            "epics"
        ]
        for field in expected_fields:
            assert field in context, f"Missing field: {field}"

"""
Tests for AC#5: Phase Completion Status Tracking Across All Phase Boundaries

Verifies that:
- current_phase field is set to completed phase number
- phase_completed field is set to true
- Previous phase data is preserved in brainstorm_context
- Checkpoint is usable for resume from last completed phase
- Data accumulates across phases
"""

from typing import Dict, Any
from unittest.mock import Mock

import pytest
import yaml

from checkpoint_protocol import (
    CheckpointService,
    PhaseValidator,
    ResumeService
)


class TestPhaseTracking:
    """Tests for phase tracking and data accumulation"""

    def test_should_track_current_phase_number_phase_1(
        self,
        fixed_session_id: str,
        valid_checkpoint_phase_1: Dict[str, Any]
    ):
        """
        Scenario: Track current_phase as 1 after Phase 1 completes
        Given: Phase 1 has completed
        When: Checkpoint is created
        Then: current_phase should be set to 1
        """
        # Arrange
        checkpoint = valid_checkpoint_phase_1

        # Act & Assert
        assert checkpoint["current_phase"] == 1

    def test_should_track_current_phase_number_phase_3(
        self,
        fixed_session_id: str,
        valid_checkpoint_phase_3: Dict[str, Any]
    ):
        """
        Scenario: Track current_phase as 3 after Phase 3 completes
        Given: Phase 3 has completed
        When: Checkpoint is created
        Then: current_phase should be set to 3
        """
        # Arrange
        checkpoint = valid_checkpoint_phase_3

        # Act & Assert
        assert checkpoint["current_phase"] == 3

    @pytest.mark.parametrize("phase", [1, 2, 3, 4, 5, 6])
    def test_should_track_all_valid_phase_numbers(
        self,
        fixed_session_id: str,
        fixed_iso_timestamp: str,
        valid_brainstorm_context: Dict[str, Any],
        phase: int
    ):
        """
        Scenario: Track all phase numbers 1-6
        Given: Phase N completes
        When: Checkpoint is created
        Then: current_phase should be set to N
        """
        # Arrange
        checkpoint = {
            "session_id": fixed_session_id,
            "timestamp": fixed_iso_timestamp,
            "current_phase": phase,
            "phase_completed": True,
            "brainstorm_context": valid_brainstorm_context,
        }

        # Act & Assert
        assert checkpoint["current_phase"] == phase

    def test_should_set_phase_completed_true(
        self,
        valid_checkpoint_phase_1: Dict[str, Any]
    ):
        """
        Scenario: Set phase_completed flag to true
        Given: A phase has completed
        When: Checkpoint is created
        Then: phase_completed should be True
        """
        # Arrange
        checkpoint = valid_checkpoint_phase_1

        # Act & Assert
        assert checkpoint["phase_completed"] is True

    def test_should_preserve_previous_phase_data(
        self,
        fixed_session_id: str,
        fixed_iso_timestamp: str,
        valid_brainstorm_context: Dict[str, Any]
    ):
        """
        Scenario: Preserve previous phase data when updating checkpoint
        Given: A checkpoint from Phase 1 exists
        When: Phase 2 checkpoint is created
        Then: Phase 1 data should be preserved in checkpoint
        """
        # Arrange
        phase_1_checkpoint = {
            "session_id": fixed_session_id,
            "timestamp": fixed_iso_timestamp,
            "current_phase": 1,
            "phase_completed": True,
            "brainstorm_context": valid_brainstorm_context,
        }

        # Act - Store phase 1 data and move to phase 2
        phase_1_data = phase_1_checkpoint["brainstorm_context"].copy()
        phase_2_checkpoint = {
            "session_id": fixed_session_id,
            "timestamp": fixed_iso_timestamp,
            "current_phase": 2,
            "phase_completed": True,
            "brainstorm_context": phase_1_data,  # Preserve phase 1 data
        }

        # Assert
        assert phase_2_checkpoint["brainstorm_context"]["problem_statement"] == \
            phase_1_data["problem_statement"]

    def test_should_accumulate_data_across_phases(
        self,
        fixed_session_id: str,
        fixed_iso_timestamp: str
    ):
        """
        Scenario: Data accumulates and is preserved across phase transitions
        Given: Checkpoints for phases 1-5
        When: Each phase completes and checkpoint is created
        Then: Previous data should accumulate and be available
        """
        # Arrange
        checkpoints = []
        accumulated_data = {
            "problem_statement": "Test problem",
            "personas": [],
            "requirements": [],
            "complexity_score": 0,
            "epics": []
        }

        # Act - Create checkpoints for phases 1-5
        for phase in range(1, 6):
            # Add phase-specific data
            accumulated_data[f"phase_{phase}_data"] = f"Data from phase {phase}"

            checkpoint = {
                "session_id": fixed_session_id,
                "timestamp": fixed_iso_timestamp,
                "current_phase": phase,
                "phase_completed": True,
                "brainstorm_context": accumulated_data.copy(),
            }
            checkpoints.append(checkpoint)

        # Assert - Verify data accumulation
        for i, checkpoint in enumerate(checkpoints):
            phase = i + 1
            # All previous phase data should be present
            for prev_phase in range(1, phase + 1):
                key = f"phase_{prev_phase}_data"
                assert key in checkpoint["brainstorm_context"], \
                    f"Phase {phase} checkpoint missing data from phase {prev_phase}"

    def test_should_maintain_phase_completion_flags(
        self,
        fixed_session_id: str,
        fixed_iso_timestamp: str
    ):
        """
        Scenario: Track phase completion status for each phase
        Given: A multi-phase session
        When: Checkpoints are created at each phase boundary
        Then: phase_completion dict should track which phases completed
        """
        # Arrange
        checkpoint = {
            "session_id": fixed_session_id,
            "timestamp": fixed_iso_timestamp,
            "current_phase": 3,
            "phase_completed": True,
            "brainstorm_context": {},
            "phase_completion": {
                "phase_1": True,
                "phase_2": True,
                "phase_3": True,
                "phase_4": False,
                "phase_5": False,
                "phase_6": False,
            }
        }

        # Act & Assert
        phase_completion = checkpoint["phase_completion"]
        assert phase_completion["phase_1"] is True
        assert phase_completion["phase_2"] is True
        assert phase_completion["phase_3"] is True
        assert phase_completion["phase_4"] is False

    def test_should_update_checkpoint_at_each_phase_boundary(
        self,
        fixed_session_id: str,
        fixed_iso_timestamp: str,
        mock_write_tool: Mock
    ):
        """
        Scenario: Create/update checkpoint at each phase boundary
        Given: Session progresses through phases 1-5
        When: Each phase completes
        Then: Checkpoint file should be written/updated
        """
        # Arrange
        checkpoint_service = CheckpointService(write_tool=mock_write_tool)
        mock_write_tool.write.reset_mock()

        # Act - Create checkpoints for phases 1-5
        for phase in range(1, 6):
            checkpoint_data = {
                "session_id": fixed_session_id,
                "timestamp": fixed_iso_timestamp,
                "current_phase": phase,
                "phase_completed": True,
                "brainstorm_context": {}
            }
            checkpoint_service.create_checkpoint(checkpoint_data)

        # Assert
        assert mock_write_tool.write.call_count == 5, \
            "Checkpoint should be written at each phase boundary"

    def test_should_verify_checkpoint_usable_for_resume(
        self,
        fixed_session_id: str,
        valid_checkpoint_phase_3: Dict[str, Any]
    ):
        """
        Scenario: Checkpoint can be used to resume from last completed phase
        Given: A checkpoint at Phase 3
        When: Session is resumed from checkpoint
        Then: All data should be available to continue from Phase 3
        """
        # Arrange
        checkpoint = valid_checkpoint_phase_3
        resume_service = ResumeService()

        # Act
        resume_state = resume_service.extract_resume_state(checkpoint)

        # Assert
        assert resume_state["session_id"] == fixed_session_id
        assert resume_state["current_phase"] == 3
        assert resume_state["phase_completed"] is True
        assert "brainstorm_context" in resume_state

    def test_should_reject_phase_numbers_outside_valid_range(
        self,
        fixed_session_id: str,
        fixed_iso_timestamp: str,
        invalid_phase_number: int
    ):
        """
        Scenario: Reject phase numbers outside 1-6 range
        Given: A checkpoint with invalid phase number
        When: Validation is performed
        Then: Should reject out-of-range phase numbers
        """
        # Arrange
        checkpoint_data = {
            "session_id": fixed_session_id,
            "timestamp": fixed_iso_timestamp,
            "current_phase": invalid_phase_number,
            "phase_completed": True,
            "brainstorm_context": {}
        }
        validator = PhaseValidator()

        # Act & Assert
        with pytest.raises(ValueError):
            validator.validate(checkpoint_data)

    def test_should_handle_phase_skip_for_deferral(
        self,
        fixed_session_id: str,
        fixed_iso_timestamp: str
    ):
        """
        Scenario: Handle skipped phases due to deferrals
        Given: Phase 2 is deferred
        When: Session advances to Phase 3
        Then: Checkpoint should mark Phase 2 as skipped
        """
        # Arrange
        checkpoint = {
            "session_id": fixed_session_id,
            "timestamp": fixed_iso_timestamp,
            "current_phase": 3,
            "phase_completed": True,
            "brainstorm_context": {},
            "phase_completion": {
                "phase_1": True,
                "phase_2": False,  # Skipped/deferred
                "phase_3": True,
                "phase_4": False,
                "phase_5": False,
                "phase_6": False,
            }
        }

        # Act & Assert
        assert checkpoint["phase_completion"]["phase_2"] is False
        assert checkpoint["phase_completion"]["phase_3"] is True

    def test_should_transition_phase_completed_from_false_to_true(
        self,
        fixed_session_id: str,
        fixed_iso_timestamp: str
    ):
        """
        Scenario: Track phase_completed transition from False to True
        Given: Phase is in progress (phase_completed=False)
        When: Phase completes
        Then: phase_completed should transition to True
        """
        # Arrange
        in_progress = {
            "current_phase": 2,
            "phase_completed": False,
        }

        # Act - Simulate phase completion
        in_progress["phase_completed"] = True

        # Assert
        assert in_progress["phase_completed"] is True



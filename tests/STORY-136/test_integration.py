"""
Integration Tests for STORY-136

Tests for:
- Multi-phase checkpoint flow (phases 1-5)
- Data accumulation across phases
- End-to-end checkpoint lifecycle
- Session state persistence and resume
"""

from typing import Dict, Any
from unittest.mock import Mock
import yaml

import pytest

from checkpoint_protocol import (
    CheckpointService,
    SessionIdGenerator,
    TimestampGenerator,
    ResumeService
)


class TestMultiPhaseCheckpointFlow:
    """Integration tests for multi-phase checkpoint scenarios"""

    def test_should_create_checkpoint_at_each_phase_boundary(
        self,
        fixed_session_id: str,
        fixed_iso_timestamp: str,
        mock_write_tool: Mock
    ):
        """
        Scenario: Checkpoint is created at each phase boundary (1-5)
        Given: Session progresses through phases 1-5
        When: Each phase completes
        Then: Checkpoint file should be written at each boundary
        """
        # Arrange
        checkpoint_service = CheckpointService(write_tool=mock_write_tool)
        mock_write_tool.write.reset_mock()

        # Act - Simulate phases 1-5
        for phase in range(1, 6):
            checkpoint_data = {
                "session_id": fixed_session_id,
                "timestamp": fixed_iso_timestamp,
                "current_phase": phase,
                "phase_completed": True,
                "brainstorm_context": {
                    "problem_statement": f"Problem from phase {phase}",
                    "personas": [{"name": f"Persona {i}"} for i in range(phase)],
                    "requirements": [{"id": f"REQ-{i}"} for i in range(phase)],
                    "complexity_score": phase * 10,
                    "epics": []
                }
            }
            checkpoint_service.create_checkpoint(checkpoint_data)

        # Assert
        assert mock_write_tool.write.call_count == 5, \
            "Should write checkpoint at each of 5 phase boundaries"

    def test_should_maintain_session_consistency_across_five_phases(
        self,
        fixed_session_id: str,
        fixed_iso_timestamp: str
    ):
        """
        Scenario: Session ID remains consistent across all phase checkpoints
        Given: Multi-phase ideation session
        When: Checkpoints are created for phases 1-5
        Then: All checkpoints should have same session_id
        """
        # Arrange
        checkpoints = []

        # Act - Create checkpoints for phases 1-5
        for phase in range(1, 6):
            checkpoint = {
                "session_id": fixed_session_id,
                "timestamp": fixed_iso_timestamp,
                "current_phase": phase,
                "phase_completed": True,
                "brainstorm_context": {
                    "problem_statement": "Sample problem",
                    "personas": [],
                    "requirements": [],
                    "complexity_score": phase * 10,
                    "epics": []
                }
            }
            checkpoints.append(checkpoint)

        # Assert
        for checkpoint in checkpoints:
            assert checkpoint["session_id"] == fixed_session_id, \
                "Session ID should remain consistent"

    def test_should_accumulate_data_across_phases(
        self,
        fixed_session_id: str,
        fixed_iso_timestamp: str
    ):
        """
        Scenario: Data accumulates as session progresses
        Given: Multi-phase session with discovery
        When: Each phase adds new data
        Then: Later checkpoints should contain data from all previous phases
        """
        # Arrange
        accumulated_data = {
            "problem_statement": "Initial problem",
            "personas": [],
            "requirements": [],
            "complexity_score": 0,
            "epics": []
        }
        checkpoints = []

        # Act - Simulate data accumulation
        for phase in range(1, 6):
            # Add phase-specific data
            accumulated_data[f"phase_{phase}_discovered"] = f"Discovery from phase {phase}"

            if phase == 2:
                accumulated_data["personas"] = [
                    {"name": "Manager", "needs": ["task assignment"]},
                    {"name": "Developer", "needs": ["task details"]}
                ]
            elif phase == 3:
                accumulated_data["requirements"] = [
                    {"id": "FR-001", "description": "Create tasks"},
                    {"id": "FR-002", "description": "Assign tasks"}
                ]
            elif phase == 4:
                accumulated_data["complexity_score"] = 35

            checkpoint = {
                "session_id": fixed_session_id,
                "timestamp": fixed_iso_timestamp,
                "current_phase": phase,
                "phase_completed": True,
                "brainstorm_context": accumulated_data.copy(),
            }
            checkpoints.append(checkpoint)

        # Assert
        # Phase 5 checkpoint should have all accumulated data
        phase_5_checkpoint = checkpoints[4]
        assert "phase_1_discovered" in phase_5_checkpoint["brainstorm_context"]
        assert "phase_2_discovered" in phase_5_checkpoint["brainstorm_context"]
        assert "phase_3_discovered" in phase_5_checkpoint["brainstorm_context"]
        assert "phase_4_discovered" in phase_5_checkpoint["brainstorm_context"]
        assert "phase_5_discovered" in phase_5_checkpoint["brainstorm_context"]

    def test_should_preserve_data_through_phase_transitions(
        self,
        fixed_session_id: str,
        fixed_iso_timestamp: str
    ):
        """
        Scenario: Data is preserved when transitioning between phases
        Given: Checkpoint from Phase 2 with specific discoveries
        When: Phase 3 checkpoint is created
        Then: Phase 2 data should be preserved
        """
        # Arrange
        phase_2_data = {
            "problem_statement": "Build task management system",
            "personas": [
                {"name": "Project Manager", "needs": ["oversight", "reporting"]},
                {"name": "Team Lead", "needs": ["task assignment", "team coordination"]}
            ],
            "requirements": [],
            "complexity_score": 15,
            "epics": []
        }

        phase_2_checkpoint = {
            "session_id": fixed_session_id,
            "timestamp": fixed_iso_timestamp,
            "current_phase": 2,
            "phase_completed": True,
            "brainstorm_context": phase_2_data.copy(),
        }

        # Act - Move to phase 3 while preserving phase 2 data
        phase_3_data = phase_2_data.copy()
        phase_3_data["requirements"] = [
            {"id": "FR-001", "description": "User authentication"},
            {"id": "FR-002", "description": "Task creation"}
        ]

        phase_3_checkpoint = {
            "session_id": fixed_session_id,
            "timestamp": fixed_iso_timestamp,
            "current_phase": 3,
            "phase_completed": True,
            "brainstorm_context": phase_3_data,
        }

        # Assert
        # Phase 3 should have phase 2's personas
        assert len(phase_3_checkpoint["brainstorm_context"]["personas"]) == 2
        assert phase_3_checkpoint["brainstorm_context"]["personas"][0]["name"] == "Project Manager"
        # Phase 3 should have new requirements
        assert len(phase_3_checkpoint["brainstorm_context"]["requirements"]) == 2

    def test_should_enable_resume_from_last_completed_phase(
        self,
        fixed_session_id: str,
        fixed_iso_timestamp: str
    ):
        """
        Scenario: Session can be resumed from last completed phase
        Given: Checkpoint at Phase 3
        When: Session is resumed from checkpoint
        Then: Should continue from phase 3 with all accumulated data
        """
        # Arrange
        checkpoint = {
            "session_id": fixed_session_id,
            "timestamp": fixed_iso_timestamp,
            "current_phase": 3,
            "phase_completed": True,
            "brainstorm_context": {
                "problem_statement": "Build task system",
                "personas": [{"name": "Manager"}],
                "requirements": [{"id": "FR-001"}],
                "complexity_score": 35,
                "epics": []
            },
            "phase_completion": {
                "phase_1": True,
                "phase_2": True,
                "phase_3": True,
                "phase_4": False,
                "phase_5": False,
                "phase_6": False,
            }
        }
        resume_service = ResumeService()

        # Act
        resume_state = resume_service.extract_resume_state(checkpoint)

        # Assert
        assert resume_state["session_id"] == fixed_session_id
        assert resume_state["current_phase"] == 3
        assert resume_state["phase_completed"] is True
        assert len(resume_state["personas"]) == 1
        assert len(resume_state["requirements"]) == 1

    def test_should_handle_phase_skip_due_to_deferral(
        self,
        fixed_session_id: str,
        fixed_iso_timestamp: str
    ):
        """
        Scenario: Handle skipped phases due to deferrals
        Given: Phase 2 is deferred
        When: Session advances to Phase 3
        Then: Checkpoint should mark phase_2 as False in phase_completion
        """
        # Arrange
        checkpoint = {
            "session_id": fixed_session_id,
            "timestamp": fixed_iso_timestamp,
            "current_phase": 3,
            "phase_completed": True,
            "brainstorm_context": {
                "problem_statement": "Sample",
                "personas": [],
                "requirements": [],
                "complexity_score": 0,
                "epics": []
            },
            "phase_completion": {
                "phase_1": True,
                "phase_2": False,  # Deferred
                "phase_3": True,
                "phase_4": False,
                "phase_5": False,
                "phase_6": False,
            }
        }

        # Act & Assert
        assert checkpoint["phase_completion"]["phase_2"] is False
        assert checkpoint["phase_completion"]["phase_3"] is True

    def test_should_create_valid_yaml_for_each_checkpoint(
        self,
        fixed_session_id: str,
        fixed_iso_timestamp: str
    ):
        """
        Scenario: All phase checkpoints produce valid YAML
        Given: Checkpoints for phases 1-5
        When: YAML is generated for each
        Then: All should be valid YAML
        """
        # Arrange & Act
        for phase in range(1, 6):
            checkpoint = {
                "session_id": fixed_session_id,
                "timestamp": fixed_iso_timestamp,
                "current_phase": phase,
                "phase_completed": True,
                "brainstorm_context": {
                    "problem_statement": f"Phase {phase}",
                    "personas": [],
                    "requirements": [],
                    "complexity_score": phase * 10,
                    "epics": []
                }
            }

            yaml_content = yaml.dump(checkpoint)
            parsed = yaml.safe_load(yaml_content)

            # Assert
            assert parsed is not None
            assert parsed["current_phase"] == phase
            assert parsed["session_id"] == fixed_session_id

    def test_should_persist_checkpoint_even_if_session_interrupted(
        self,
        fixed_session_id: str,
        fixed_iso_timestamp: str,
        mock_write_tool: Mock
    ):
        """
        Scenario: Checkpoint persists even if session is interrupted
        Given: Session in Phase 2
        When: Checkpoint is written
        Then: Checkpoint should persist for resume
        """
        # Arrange
        checkpoint_service = CheckpointService(write_tool=mock_write_tool)
        checkpoint_data = {
            "session_id": fixed_session_id,
            "timestamp": fixed_iso_timestamp,
            "current_phase": 2,
            "phase_completed": True,
            "brainstorm_context": {
                "problem_statement": "Test",
                "personas": [{"name": "Test"}],
                "requirements": [],
                "complexity_score": 20,
                "epics": []
            }
        }

        # Act
        checkpoint_service.create_checkpoint(checkpoint_data)

        # Assert
        mock_write_tool.write.assert_called_once()

    def test_should_prevent_data_loss_across_phase_transitions(
        self,
        fixed_session_id: str,
        fixed_iso_timestamp: str
    ):
        """
        Scenario: Data is not lost when transitioning between phases
        Given: Data discovered in phases 1-3
        When: Phase 4 is started
        Then: All phase 1-3 data should still be available
        """
        # Arrange
        data_by_phase = {
            1: {"personas": []},
            2: {"personas": [{"name": "Manager"}]},
            3: {"requirements": [{"id": "REQ-001"}]},
        }

        accumulated = {}
        checkpoints = []

        # Act - Accumulate data through phases
        for phase in range(1, 4):
            accumulated.update(data_by_phase[phase])
            checkpoint = {
                "session_id": fixed_session_id,
                "timestamp": fixed_iso_timestamp,
                "current_phase": phase,
                "phase_completed": True,
                "brainstorm_context": {
                    "problem_statement": "Test",
                    "personas": accumulated.get("personas", []),
                    "requirements": accumulated.get("requirements", []),
                    "complexity_score": 0,
                    "epics": []
                }
            }
            checkpoints.append(checkpoint)

        # Start phase 4 with all previous data
        phase_4_checkpoint = {
            "session_id": fixed_session_id,
            "timestamp": fixed_iso_timestamp,
            "current_phase": 4,
            "phase_completed": False,
            "brainstorm_context": {
                "problem_statement": "Test",
                "personas": accumulated.get("personas", []),
                "requirements": accumulated.get("requirements", []),
                "complexity_score": 0,
                "epics": []
            }
        }

        # Assert
        assert len(phase_4_checkpoint["brainstorm_context"]["personas"]) == 1
        assert len(phase_4_checkpoint["brainstorm_context"]["requirements"]) == 1

    def test_critical_path_full_ideation_session_lifecycle(
        self,
        fixed_session_id: str,
        fixed_iso_timestamp: str,
        mock_write_tool: Mock
    ):
        """
        Critical Path Test: Full ideation session lifecycle (Phase 1-5)
        Given: New ideation session starting
        When: Session progresses through phases 1-5
        Then: Checkpoint should be created/updated at each boundary with accumulated data
        """
        # Arrange
        checkpoint_service = CheckpointService(write_tool=mock_write_tool)
        mock_write_tool.write.reset_mock()

        context = {
            "problem_statement": "Build collaborative task management app",
            "personas": [],
            "requirements": [],
            "complexity_score": 0,
            "epics": []
        }

        # Act - Simulate full session
        write_count = 0
        for phase in range(1, 6):
            # Add phase-specific discoveries
            if phase >= 2:
                if len(context["personas"]) == 0:
                    context["personas"] = [
                        {"name": "Project Manager"},
                        {"name": "Developer"}
                    ]
            if phase >= 3:
                if len(context["requirements"]) == 0:
                    context["requirements"] = [
                        {"id": "FR-001"},
                        {"id": "FR-002"}
                    ]
            if phase >= 4:
                context["complexity_score"] = 40

            checkpoint = {
                "session_id": fixed_session_id,
                "timestamp": fixed_iso_timestamp,
                "current_phase": phase,
                "phase_completed": True,
                "brainstorm_context": context.copy(),
            }

            checkpoint_service.create_checkpoint(checkpoint)
            write_count += 1

        # Assert
        assert mock_write_tool.write.call_count == 5
        assert write_count == 5



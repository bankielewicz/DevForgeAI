"""
Test: AC#3 - phase-complete Succeeds with All Required Steps
Story: STORY-517
Generated: 2026-02-28

Tests that phase-complete exits 0 when all steps_required are in
steps_completed, updates status to completed, and advances current_phase.
"""

import json
import pytest
from pathlib import Path

from devforgeai_cli.commands.phase_commands import phase_complete_command


def _create_qa_state_with_all_steps(tmp_path, story_id):
    """Helper to create qa-phase-state.json with phase 1.5 fully completed steps."""
    workflows_dir = tmp_path / "devforgeai" / "workflows"
    workflows_dir.mkdir(parents=True, exist_ok=True)

    state = {
        "story_id": story_id,
        "workflow": "qa",
        "current_phase": "1.5",
        "workflow_started": "2026-02-28T00:00:00Z",
        "blocking_status": False,
        "phases": {
            "00": {"status": "completed", "steps_required": ["setup_validation", "story_file_loading"], "steps_completed": ["setup_validation", "story_file_loading"], "checkpoint_passed": True},
            "01": {"status": "completed", "steps_required": ["constraint_validation", "anti_pattern_scan", "security_audit"], "steps_completed": ["constraint_validation", "anti_pattern_scan", "security_audit"], "checkpoint_passed": True},
            "1.5": {"status": "pending", "steps_required": ["diff_regression_detection", "test_integrity_verification"], "steps_completed": ["diff_regression_detection", "test_integrity_verification"], "checkpoint_passed": False},
            "02": {"status": "pending", "steps_required": ["coverage_analysis", "code_quality_metrics"], "steps_completed": [], "checkpoint_passed": False},
            "03": {"status": "pending", "steps_required": ["report_generation", "result_determination"], "steps_completed": [], "checkpoint_passed": False},
            "04": {"status": "pending", "steps_required": ["cleanup", "state_preservation"], "steps_completed": [], "checkpoint_passed": False},
        },
        "validation_errors": [],
        "observations": [],
    }

    state_path = workflows_dir / f"{story_id}-qa-phase-state.json"
    state_path.write_text(json.dumps(state, indent=2))
    return state_path


class TestPhaseCompleteSucceedsWithAllSteps:
    """Tests that phase-complete succeeds when all required steps are present."""

    def test_should_exit_0_when_all_steps_completed(self, tmp_path):
        """phase-complete exits 0 when all steps_required are in steps_completed."""
        # Arrange
        _create_qa_state_with_all_steps(tmp_path, "STORY-517")

        # Act
        exit_code = phase_complete_command(
            story_id="STORY-517",
            phase="1.5",
            checkpoint_passed=True,
            project_root=str(tmp_path),
            workflow="qa",
        )

        # Assert
        assert exit_code == 0, f"Expected exit code 0, got {exit_code}"

    def test_should_update_status_to_completed(self, tmp_path):
        """Phase status updated to 'completed' after successful phase-complete."""
        # Arrange
        state_path = _create_qa_state_with_all_steps(tmp_path, "STORY-517")

        # Act
        phase_complete_command(
            story_id="STORY-517",
            phase="1.5",
            checkpoint_passed=True,
            project_root=str(tmp_path),
            workflow="qa",
        )

        # Assert
        state = json.loads(state_path.read_text())
        assert state["phases"]["1.5"]["status"] == "completed", (
            f"Phase 1.5 status should be 'completed', got '{state['phases']['1.5']['status']}'"
        )

    def test_should_set_checkpoint_passed_true(self, tmp_path):
        """checkpoint_passed set to true after successful phase-complete."""
        # Arrange
        state_path = _create_qa_state_with_all_steps(tmp_path, "STORY-517")

        # Act
        phase_complete_command(
            story_id="STORY-517",
            phase="1.5",
            checkpoint_passed=True,
            project_root=str(tmp_path),
            workflow="qa",
        )

        # Assert
        state = json.loads(state_path.read_text())
        assert state["phases"]["1.5"]["checkpoint_passed"] is True

    def test_should_advance_current_phase_to_02(self, tmp_path):
        """current_phase advances to '02' after completing phase 1.5."""
        # Arrange
        state_path = _create_qa_state_with_all_steps(tmp_path, "STORY-517")

        # Act
        phase_complete_command(
            story_id="STORY-517",
            phase="1.5",
            checkpoint_passed=True,
            project_root=str(tmp_path),
            workflow="qa",
        )

        # Assert
        state = json.loads(state_path.read_text())
        assert state["current_phase"] == "02", (
            f"current_phase should advance to '02', got '{state['current_phase']}'"
        )

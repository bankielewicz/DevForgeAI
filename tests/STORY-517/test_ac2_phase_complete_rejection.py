"""
Test: AC#2 - phase-complete Rejects Incomplete Steps
Story: STORY-517
Generated: 2026-02-28

Tests that phase-complete exits code 1 when steps_completed is missing
required steps, and identifies the missing step by name.
"""

import json
import pytest
from pathlib import Path

from devforgeai_cli.commands.phase_commands import phase_complete_command


def _create_qa_state_file(tmp_path, story_id, phase_data_override=None):
    """Helper to create a qa-phase-state.json with customizable phase data."""
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
            "1.5": {"status": "pending", "steps_required": ["diff_regression_detection", "test_integrity_verification"], "steps_completed": ["diff_regression_detection"], "checkpoint_passed": False},
            "02": {"status": "pending", "steps_required": ["coverage_analysis", "code_quality_metrics"], "steps_completed": [], "checkpoint_passed": False},
            "03": {"status": "pending", "steps_required": ["report_generation", "result_determination"], "steps_completed": [], "checkpoint_passed": False},
            "04": {"status": "pending", "steps_required": ["cleanup", "state_preservation"], "steps_completed": [], "checkpoint_passed": False},
        },
        "validation_errors": [],
        "observations": [],
    }

    if phase_data_override:
        for phase_key, overrides in phase_data_override.items():
            state["phases"][phase_key].update(overrides)

    state_path = workflows_dir / f"{story_id}-qa-phase-state.json"
    state_path.write_text(json.dumps(state, indent=2))
    return state_path


class TestPhaseCompleteRejectsIncompleteSteps:
    """Tests that phase-complete rejects when required steps are missing."""

    def test_should_exit_1_when_step_missing(self, tmp_path, capsys):
        """phase-complete exits 1 when test_integrity_verification not in steps_completed."""
        # Arrange
        _create_qa_state_file(tmp_path, "STORY-517")

        # Act
        exit_code = phase_complete_command(
            story_id="STORY-517",
            phase="1.5",
            checkpoint_passed=True,
            project_root=str(tmp_path),
            workflow="qa",
        )

        # Assert
        assert exit_code == 1, f"Expected exit code 1 for missing step, got {exit_code}"

    def test_should_identify_missing_step_in_error(self, tmp_path, capsys):
        """Error message identifies test_integrity_verification as missing."""
        # Arrange
        _create_qa_state_file(tmp_path, "STORY-517")

        # Act
        phase_complete_command(
            story_id="STORY-517",
            phase="1.5",
            checkpoint_passed=True,
            project_root=str(tmp_path),
            workflow="qa",
        )

        # Assert
        captured = capsys.readouterr()
        assert "test_integrity_verification" in captured.out or "test_integrity_verification" in captured.err, (
            f"Error should identify 'test_integrity_verification' as missing. Output: {captured.out}{captured.err}"
        )

    def test_should_not_update_phase_status_when_step_missing(self, tmp_path):
        """Phase status remains 'pending' when steps are incomplete."""
        # Arrange
        state_path = _create_qa_state_file(tmp_path, "STORY-517")

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
        assert state["phases"]["1.5"]["status"] != "completed", (
            "Phase 1.5 status should NOT be 'completed' when steps are missing"
        )

    def test_should_exit_1_when_multiple_steps_missing(self, tmp_path, capsys):
        """phase-complete exits 1 when multiple required steps are missing."""
        # Arrange - phase 1.5 with NO steps completed
        _create_qa_state_file(tmp_path, "STORY-517", {
            "1.5": {"steps_completed": []},
        })

        # Act
        exit_code = phase_complete_command(
            story_id="STORY-517",
            phase="1.5",
            checkpoint_passed=True,
            project_root=str(tmp_path),
            workflow="qa",
        )

        # Assert
        assert exit_code == 1
        captured = capsys.readouterr()
        output = captured.out + captured.err
        assert "diff_regression_detection" in output, "Should identify diff_regression_detection as missing"
        assert "test_integrity_verification" in output, "Should identify test_integrity_verification as missing"

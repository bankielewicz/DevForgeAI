"""
Test: AC#1 - --workflow=qa Flag Accepted by CLI Commands
Story: STORY-517
Generated: 2026-02-28

Tests that phase-init with --workflow=qa creates a qa-phase-state.json
with correct schema, and that omitting --workflow defaults to dev behavior.
"""

import json
import pytest
from pathlib import Path
from unittest.mock import patch

from devforgeai_cli.commands.phase_commands import phase_init_command
from devforgeai_cli.phase_state import PhaseState


# Expected QA phases schema
QA_PHASES = {
    "00": {"steps_required": ["setup_validation", "story_file_loading"], "subagents_required": []},
    "01": {"steps_required": ["constraint_validation", "anti_pattern_scan", "security_audit"], "subagents_required": ["anti-pattern-scanner", "security-auditor"]},
    "1.5": {"steps_required": ["diff_regression_detection", "test_integrity_verification"], "subagents_required": []},
    "02": {"steps_required": ["coverage_analysis", "code_quality_metrics"], "subagents_required": ["coverage-analyzer", "code-quality-auditor"]},
    "03": {"steps_required": ["report_generation", "result_determination"], "subagents_required": ["qa-result-interpreter"]},
    "04": {"steps_required": ["cleanup", "state_preservation"], "subagents_required": []},
}

QA_PHASE_KEYS = ["00", "01", "1.5", "02", "03", "04"]


class TestQaPhaseInit:
    """Tests for phase-init --workflow=qa creating correct state file."""

    def test_should_create_qa_phase_state_file_when_workflow_qa(self, tmp_path):
        """phase-init with --workflow=qa creates STORY-NNN-qa-phase-state.json."""
        # Arrange
        project_root = str(tmp_path)
        (tmp_path / "devforgeai" / "workflows").mkdir(parents=True)

        # Act
        exit_code = phase_init_command(
            story_id="STORY-517",
            project_root=project_root,
            workflow="qa",
        )

        # Assert
        assert exit_code == 0
        qa_state_path = tmp_path / "devforgeai" / "workflows" / "STORY-517-qa-phase-state.json"
        assert qa_state_path.exists(), "qa-phase-state.json was not created"

    def test_should_contain_all_6_qa_phases_when_workflow_qa(self, tmp_path):
        """Created qa-phase-state.json contains all 6 QA phases."""
        # Arrange
        project_root = str(tmp_path)
        (tmp_path / "devforgeai" / "workflows").mkdir(parents=True)

        # Act
        phase_init_command(
            story_id="STORY-517",
            project_root=project_root,
            workflow="qa",
        )

        # Assert
        qa_state_path = tmp_path / "devforgeai" / "workflows" / "STORY-517-qa-phase-state.json"
        state = json.loads(qa_state_path.read_text())
        phases = state["phases"]
        for key in QA_PHASE_KEYS:
            assert key in phases, f"QA phase '{key}' missing from state file"
        assert len(phases) == 6, f"Expected 6 QA phases, got {len(phases)}"

    def test_should_have_steps_required_per_phase_when_workflow_qa(self, tmp_path):
        """Each QA phase has correct steps_required array."""
        # Arrange
        project_root = str(tmp_path)
        (tmp_path / "devforgeai" / "workflows").mkdir(parents=True)

        # Act
        phase_init_command(
            story_id="STORY-517",
            project_root=project_root,
            workflow="qa",
        )

        # Assert
        qa_state_path = tmp_path / "devforgeai" / "workflows" / "STORY-517-qa-phase-state.json"
        state = json.loads(qa_state_path.read_text())
        for phase_key, expected in QA_PHASES.items():
            actual = state["phases"][phase_key]
            assert actual["steps_required"] == expected["steps_required"], (
                f"Phase {phase_key}: expected steps_required={expected['steps_required']}, "
                f"got {actual.get('steps_required')}"
            )

    def test_should_have_empty_steps_completed_when_workflow_qa(self, tmp_path):
        """Each QA phase starts with steps_completed: []."""
        # Arrange
        project_root = str(tmp_path)
        (tmp_path / "devforgeai" / "workflows").mkdir(parents=True)

        # Act
        phase_init_command(
            story_id="STORY-517",
            project_root=project_root,
            workflow="qa",
        )

        # Assert
        qa_state_path = tmp_path / "devforgeai" / "workflows" / "STORY-517-qa-phase-state.json"
        state = json.loads(qa_state_path.read_text())
        for phase_key in QA_PHASE_KEYS:
            actual = state["phases"][phase_key]
            assert actual["steps_completed"] == [], (
                f"Phase {phase_key}: steps_completed should be empty, got {actual.get('steps_completed')}"
            )

    def test_should_have_checkpoint_passed_false_when_workflow_qa(self, tmp_path):
        """Each QA phase starts with checkpoint_passed: false."""
        # Arrange
        project_root = str(tmp_path)
        (tmp_path / "devforgeai" / "workflows").mkdir(parents=True)

        # Act
        phase_init_command(
            story_id="STORY-517",
            project_root=project_root,
            workflow="qa",
        )

        # Assert
        qa_state_path = tmp_path / "devforgeai" / "workflows" / "STORY-517-qa-phase-state.json"
        state = json.loads(qa_state_path.read_text())
        for phase_key in QA_PHASE_KEYS:
            actual = state["phases"][phase_key]
            assert actual["checkpoint_passed"] is False, (
                f"Phase {phase_key}: checkpoint_passed should be False"
            )

    def test_should_have_workflow_qa_field_when_workflow_qa(self, tmp_path):
        """Created state file has top-level "workflow": "qa" field."""
        # Arrange
        project_root = str(tmp_path)
        (tmp_path / "devforgeai" / "workflows").mkdir(parents=True)

        # Act
        phase_init_command(
            story_id="STORY-517",
            project_root=project_root,
            workflow="qa",
        )

        # Assert
        qa_state_path = tmp_path / "devforgeai" / "workflows" / "STORY-517-qa-phase-state.json"
        state = json.loads(qa_state_path.read_text())
        assert state.get("workflow") == "qa", (
            f"Expected top-level 'workflow': 'qa', got '{state.get('workflow')}'"
        )


class TestDevWorkflowBackwardCompatibility:
    """Tests that omitting --workflow defaults to dev phase-state.json."""

    def test_should_create_dev_phase_state_when_workflow_omitted(self, tmp_path):
        """Omitting --workflow creates dev phase-state.json (backward-compatible)."""
        # Arrange
        project_root = str(tmp_path)
        (tmp_path / "devforgeai" / "workflows").mkdir(parents=True)

        # Act - no workflow parameter (should default to dev)
        exit_code = phase_init_command(
            story_id="STORY-517",
            project_root=project_root,
        )

        # Assert
        assert exit_code == 0
        dev_state_path = tmp_path / "devforgeai" / "workflows" / "STORY-517-phase-state.json"
        assert dev_state_path.exists(), "Dev phase-state.json was not created"
        qa_state_path = tmp_path / "devforgeai" / "workflows" / "STORY-517-qa-phase-state.json"
        assert not qa_state_path.exists(), "QA state file should not be created when workflow omitted"

    def test_should_create_dev_phase_state_when_workflow_dev(self, tmp_path):
        """Explicit --workflow=dev creates dev phase-state.json."""
        # Arrange
        project_root = str(tmp_path)
        (tmp_path / "devforgeai" / "workflows").mkdir(parents=True)

        # Act
        exit_code = phase_init_command(
            story_id="STORY-517",
            project_root=project_root,
            workflow="dev",
        )

        # Assert
        assert exit_code == 0
        dev_state_path = tmp_path / "devforgeai" / "workflows" / "STORY-517-phase-state.json"
        assert dev_state_path.exists(), "Dev phase-state.json was not created with --workflow=dev"

    def test_should_reject_invalid_workflow_value(self, tmp_path):
        """Invalid --workflow value exits with code 2."""
        # Arrange
        project_root = str(tmp_path)
        (tmp_path / "devforgeai" / "workflows").mkdir(parents=True)

        # Act
        exit_code = phase_init_command(
            story_id="STORY-517",
            project_root=project_root,
            workflow="release",
        )

        # Assert
        assert exit_code == 2, f"Expected exit code 2 for invalid workflow, got {exit_code}"

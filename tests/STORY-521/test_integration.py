"""
Integration Tests for STORY-521: Cross-component interactions between
phase_state.py and phase_commands.py.

Verifies:
1. Full dev workflow lifecycle: init -> record subagent -> complete phase -> status check
2. Full QA workflow lifecycle: init -> complete phases sequentially
3. Cross-workflow isolation: dev and qa state files do not interfere
4. CLI commands calling PhaseState methods correctly (end-to-end)
5. WORKFLOW_SCHEMAS driving both paths consistently
"""
import json
import sys
from io import StringIO
from pathlib import Path

import pytest

from devforgeai_cli.phase_state import (
    PhaseState,
    WORKFLOW_SCHEMAS,
    VALID_WORKFLOWS,
    PhaseTransitionError,
    PhaseNotFoundError,
)
from devforgeai_cli.commands.phase_commands import (
    phase_init_command,
    phase_complete_command,
    phase_record_command,
    phase_status_command,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def capture_stdout(fn, *args, **kwargs):
    """Capture printed output from a command function."""
    buf = StringIO()
    old_stdout = sys.stdout
    sys.stdout = buf
    try:
        exit_code = fn(*args, **kwargs)
    finally:
        sys.stdout = old_stdout
    return exit_code, buf.getvalue()


# ---------------------------------------------------------------------------
# 1. Full dev workflow lifecycle
# ---------------------------------------------------------------------------

class TestDevWorkflowLifecycle:
    """Integration: full dev lifecycle through CLI -> PhaseState."""

    def test_init_creates_dev_state_file_with_first_phase(self, tmp_path):
        """phase_init_command creates dev state file; current_phase is '01'."""
        # Arrange
        story_id = "STORY-521"
        project_root = str(tmp_path)

        # Act
        exit_code, output = capture_stdout(
            phase_init_command, story_id, project_root, workflow="dev"
        )

        # Assert
        assert exit_code == 0
        state_path = tmp_path / "devforgeai" / "workflows" / "STORY-521-phase-state.json"
        assert state_path.exists(), "dev state file must be created"
        with state_path.open() as f:
            state = json.load(f)
        assert state["current_phase"] == "01"
        assert state["story_id"] == story_id

    def test_record_subagent_is_persisted_in_state_file(self, tmp_path):
        """phase_record_command persists subagent name in phases['01']['subagents_invoked']."""
        # Arrange
        story_id = "STORY-521"
        project_root = str(tmp_path)
        phase_init_command(story_id, project_root, workflow="dev")

        # Act
        exit_code, _ = capture_stdout(
            phase_record_command, story_id, "01", "git-validator", project_root
        )

        # Assert
        assert exit_code == 0
        ps = PhaseState(project_root=tmp_path)
        state = ps.read(story_id)
        assert "git-validator" in state["phases"]["01"]["subagents_invoked"]

    def test_complete_phase_advances_current_phase(self, tmp_path):
        """phase_complete_command advances current_phase from '01' to '02'."""
        # Arrange
        story_id = "STORY-521"
        project_root = str(tmp_path)
        phase_init_command(story_id, project_root, workflow="dev")

        # Record required subagents for phase 01 (bypass enforcement)
        ps = PhaseState(project_root=tmp_path)
        for subagent in ["git-validator", "tech-stack-detector"]:
            ps.record_subagent(story_id, "01", subagent)

        # Act
        exit_code, _ = capture_stdout(
            phase_complete_command, story_id, "01", True, project_root, workflow="dev"
        )

        # Assert
        assert exit_code == 0
        state = ps.read(story_id)
        assert state["current_phase"] == "02"
        assert state["phases"]["01"]["status"] == "completed"
        assert state["phases"]["01"]["checkpoint_passed"] is True

    def test_status_command_reflects_completed_phase(self, tmp_path):
        """phase_status_command shows phase 01 as completed after completion."""
        # Arrange
        story_id = "STORY-521"
        project_root = str(tmp_path)
        phase_init_command(story_id, project_root, workflow="dev")
        ps = PhaseState(project_root=tmp_path)
        for subagent in ["git-validator", "tech-stack-detector"]:
            ps.record_subagent(story_id, "01", subagent)
        phase_complete_command(story_id, "01", True, project_root, workflow="dev")

        # Act
        exit_code, output = capture_stdout(
            phase_status_command, story_id, project_root
        )

        # Assert
        assert exit_code == 0
        assert "Phase 01: completed" in output or "[x] Phase 01" in output

    def test_complete_workflow_phase_does_not_enforce_subagents(self, tmp_path):
        """complete_workflow_phase (STORY-521 unified path) does not enforce subagent
        requirements — that enforcement lives in the legacy complete_phase() method.
        CLI phase_complete_command succeeds even without recorded subagents."""
        # Arrange
        story_id = "STORY-521"
        project_root = str(tmp_path)
        phase_init_command(story_id, project_root, workflow="dev")

        # Act — do NOT record required subagents
        exit_code, _ = capture_stdout(
            phase_complete_command, story_id, "01", True, project_root, workflow="dev"
        )

        # Assert: unified path does not block on missing subagents
        assert exit_code == 0
        # But state file is still advanced
        ps = PhaseState(project_root=tmp_path)
        state = ps.read(story_id)
        assert state["current_phase"] == "02"

    def test_complete_out_of_order_phase_returns_error(self, tmp_path):
        """Attempting to complete phase 03 when current_phase is 01 returns exit code 1."""
        # Arrange
        story_id = "STORY-521"
        project_root = str(tmp_path)
        phase_init_command(story_id, project_root, workflow="dev")

        # Act
        exit_code, _ = capture_stdout(
            phase_complete_command, story_id, "03", False, project_root, workflow="dev"
        )

        # Assert
        assert exit_code == 1


# ---------------------------------------------------------------------------
# 2. Full QA workflow lifecycle
# ---------------------------------------------------------------------------

class TestQAWorkflowLifecycle:
    """Integration: full QA lifecycle init -> sequential phase completion."""

    def test_init_creates_qa_state_file_with_phase_00(self, tmp_path):
        """phase_init_command --workflow=qa creates qa state file starting at phase '00'."""
        # Arrange
        story_id = "STORY-521"
        project_root = str(tmp_path)

        # Act
        exit_code, _ = capture_stdout(
            phase_init_command, story_id, project_root, workflow="qa"
        )

        # Assert
        assert exit_code == 0
        state_path = tmp_path / "devforgeai" / "workflows" / "STORY-521-qa-phase-state.json"
        assert state_path.exists(), "qa state file must be created"
        with state_path.open() as f:
            state = json.load(f)
        assert state["current_phase"] == "00"
        assert state["workflow"] == "qa"

    def test_qa_phases_complete_sequentially(self, tmp_path):
        """QA phases 00 -> 01 -> 1.5 -> 02 -> 03 -> 04 complete in order."""
        # Arrange
        story_id = "STORY-521"
        project_root = str(tmp_path)
        phase_init_command(story_id, project_root, workflow="qa")
        ps = PhaseState(project_root=tmp_path)

        qa_phases = ["00", "01", "1.5", "02", "03", "04"]

        for phase in qa_phases:
            # Act — checkpoint_passed=False to bypass step validation
            exit_code, _ = capture_stdout(
                phase_complete_command,
                story_id, phase, False, project_root, workflow="qa"
            )

            # Assert
            assert exit_code == 0, f"Phase {phase} completion failed"

        # Assert final state: all phases completed
        state_path = tmp_path / "devforgeai" / "workflows" / "STORY-521-qa-phase-state.json"
        with state_path.open() as f:
            state = json.load(f)
        for phase in qa_phases:
            assert state["phases"][phase]["status"] == "completed", (
                f"QA phase {phase} should be completed"
            )

    def test_qa_init_is_idempotent(self, tmp_path):
        """Calling phase_init_command twice for QA returns exit code 1 (already exists)."""
        # Arrange
        story_id = "STORY-521"
        project_root = str(tmp_path)

        # Act
        first_code, _ = capture_stdout(
            phase_init_command, story_id, project_root, workflow="qa"
        )
        second_code, output = capture_stdout(
            phase_init_command, story_id, project_root, workflow="qa"
        )

        # Assert
        assert first_code == 0
        assert second_code == 1
        assert "already exists" in output

    def test_qa_phase_out_of_order_returns_error(self, tmp_path):
        """Attempting to complete qa phase 02 when current is 00 returns exit code 1."""
        # Arrange
        story_id = "STORY-521"
        project_root = str(tmp_path)
        phase_init_command(story_id, project_root, workflow="qa")

        # Act
        exit_code, _ = capture_stdout(
            phase_complete_command, story_id, "02", False, project_root, workflow="qa"
        )

        # Assert
        assert exit_code == 1


# ---------------------------------------------------------------------------
# 3. Cross-workflow isolation
# ---------------------------------------------------------------------------

class TestCrossWorkflowIsolation:
    """Integration: dev and qa state files must not interfere with each other."""

    def test_dev_and_qa_state_files_use_different_paths(self, tmp_path):
        """Dev and QA workflows write to separate files for the same story."""
        # Arrange
        story_id = "STORY-521"
        project_root = str(tmp_path)

        # Act
        phase_init_command(story_id, project_root, workflow="dev")
        phase_init_command(story_id, project_root, workflow="qa")

        # Assert
        dev_path = tmp_path / "devforgeai" / "workflows" / "STORY-521-phase-state.json"
        qa_path = tmp_path / "devforgeai" / "workflows" / "STORY-521-qa-phase-state.json"
        assert dev_path.exists(), "dev state file must exist"
        assert qa_path.exists(), "qa state file must exist"
        assert dev_path != qa_path

    def test_completing_qa_phase_does_not_affect_dev_state(self, tmp_path):
        """Completing a QA phase leaves the dev state file unchanged."""
        # Arrange
        story_id = "STORY-521"
        project_root = str(tmp_path)
        phase_init_command(story_id, project_root, workflow="dev")
        phase_init_command(story_id, project_root, workflow="qa")

        ps = PhaseState(project_root=tmp_path)
        dev_state_before = ps.read(story_id)

        # Act: complete qa phase 00
        phase_complete_command(story_id, "00", False, project_root, workflow="qa")

        # Assert: dev state unchanged
        dev_state_after = ps.read(story_id)
        assert dev_state_after["current_phase"] == dev_state_before["current_phase"]
        assert dev_state_after["phases"]["01"]["status"] == "pending"

    def test_dev_phase_completion_does_not_affect_qa_state(self, tmp_path):
        """Completing a dev phase (via escape hatch) leaves the QA state file unchanged."""
        # Arrange
        story_id = "STORY-521"
        project_root = str(tmp_path)
        phase_init_command(story_id, project_root, workflow="dev")
        phase_init_command(story_id, project_root, workflow="qa")

        ps = PhaseState(project_root=tmp_path)
        qa_state_before = ps.read_qa(story_id)

        # Act: complete dev phase 01 via escape hatch (checkpoint_passed=False)
        phase_complete_command(story_id, "01", False, project_root, workflow="dev")

        # Assert: qa state unchanged
        qa_state_after = ps.read_qa(story_id)
        assert qa_state_after["current_phase"] == qa_state_before["current_phase"]

    def test_different_story_ids_have_isolated_state_files(self, tmp_path):
        """Two different story IDs produce two independent dev state files."""
        # Arrange
        project_root = str(tmp_path)

        # Act
        phase_init_command("STORY-521", project_root, workflow="dev")
        phase_init_command("STORY-522", project_root, workflow="dev")

        # Complete phase 01 for STORY-521 only (escape hatch)
        phase_complete_command("STORY-521", "01", False, project_root, workflow="dev")

        # Assert: STORY-522 is unaffected
        ps = PhaseState(project_root=tmp_path)
        state_521 = ps.read("STORY-521")
        state_522 = ps.read("STORY-522")
        assert state_521["current_phase"] == "02"
        assert state_522["current_phase"] == "01"


# ---------------------------------------------------------------------------
# 4. CLI commands calling PhaseState methods correctly (end-to-end)
# ---------------------------------------------------------------------------

class TestCLIToPhaseStateEndToEnd:
    """Integration: CLI command functions correctly delegate to PhaseState methods."""

    def test_phase_init_json_format_returns_valid_json(self, tmp_path):
        """phase_init_command with format='json' prints parseable JSON with correct keys."""
        # Arrange
        story_id = "STORY-521"
        project_root = str(tmp_path)

        # Act
        exit_code, output = capture_stdout(
            phase_init_command, story_id, project_root, format="json", workflow="dev"
        )

        # Assert
        assert exit_code == 0
        result = json.loads(output)
        assert result["success"] is True
        assert result["story_id"] == story_id
        assert result["current_phase"] == "01"

    def test_phase_complete_json_format_returns_updated_state(self, tmp_path):
        """phase_complete_command with format='json' returns current_phase after advance."""
        # Arrange
        story_id = "STORY-521"
        project_root = str(tmp_path)
        phase_init_command(story_id, project_root, workflow="dev")

        # Act — escape hatch so subagent enforcement is skipped
        exit_code, output = capture_stdout(
            phase_complete_command,
            story_id, "01", False, project_root,
            format="json", workflow="dev"
        )

        # Assert
        assert exit_code == 0
        result = json.loads(output)
        assert result["success"] is True
        assert result["completed_phase"] == "01"
        assert result["current_phase"] == "02"

    def test_phase_status_json_format_returns_full_state(self, tmp_path):
        """phase_status_command with format='json' returns complete state dict."""
        # Arrange
        story_id = "STORY-521"
        project_root = str(tmp_path)
        phase_init_command(story_id, project_root, workflow="dev")

        # Act
        exit_code, output = capture_stdout(
            phase_status_command, story_id, project_root, format="json"
        )

        # Assert
        assert exit_code == 0
        state = json.loads(output)
        assert state["story_id"] == story_id
        assert "phases" in state
        assert "current_phase" in state

    def test_phase_record_idempotent_cli_call(self, tmp_path):
        """Recording the same subagent twice via CLI does not duplicate the entry."""
        # Arrange
        story_id = "STORY-521"
        project_root = str(tmp_path)
        phase_init_command(story_id, project_root, workflow="dev")

        # Act
        phase_record_command(story_id, "01", "git-validator", project_root)
        exit_code, _ = capture_stdout(
            phase_record_command, story_id, "01", "git-validator", project_root
        )

        # Assert
        assert exit_code == 0
        ps = PhaseState(project_root=tmp_path)
        state = ps.read(story_id)
        invoked = state["phases"]["01"]["subagents_invoked"]
        assert invoked.count("git-validator") == 1

    def test_phase_status_missing_story_returns_exit_1(self, tmp_path):
        """phase_status_command returns exit code 1 when story state does not exist."""
        # Act
        exit_code, output = capture_stdout(
            phase_status_command, "STORY-521", str(tmp_path)
        )

        # Assert
        assert exit_code == 1
        assert "not found" in output.lower()

    def test_phase_init_invalid_workflow_returns_exit_2(self, tmp_path):
        """phase_init_command with unknown workflow returns exit code 2."""
        # Act
        exit_code, output = capture_stdout(
            phase_init_command, "STORY-521", str(tmp_path), workflow="bogus"
        )

        # Assert
        assert exit_code == 2
        assert "Invalid workflow" in output


# ---------------------------------------------------------------------------
# 5. WORKFLOW_SCHEMAS driving both paths consistently
# ---------------------------------------------------------------------------

class TestWorkflowSchemaConsistency:
    """Integration: WORKFLOW_SCHEMAS governs both create_workflow() and complete_workflow_phase()."""

    def test_workflow_schemas_contains_dev_and_qa(self):
        """WORKFLOW_SCHEMAS registry must contain exactly 'dev' and 'qa' keys."""
        assert "dev" in WORKFLOW_SCHEMAS
        assert "qa" in WORKFLOW_SCHEMAS

    def test_valid_workflows_matches_schema_keys(self):
        """VALID_WORKFLOWS list must exactly match keys of WORKFLOW_SCHEMAS."""
        assert set(VALID_WORKFLOWS) == set(WORKFLOW_SCHEMAS.keys())

    def test_create_workflow_dev_initial_phase_matches_schema(self, tmp_path):
        """create_workflow('dev') starts at the first phase defined in WORKFLOW_SCHEMAS."""
        # Arrange
        ps = PhaseState(project_root=tmp_path)
        expected_first_phase = WORKFLOW_SCHEMAS["dev"]["valid_phases"][0]

        # Act
        state = ps.create_workflow("STORY-521", "dev")

        # Assert
        assert state["current_phase"] == expected_first_phase

    def test_create_workflow_qa_initial_phase_matches_schema(self, tmp_path):
        """create_workflow('qa') starts at the first phase defined in WORKFLOW_SCHEMAS."""
        # Arrange
        ps = PhaseState(project_root=tmp_path)
        expected_first_phase = WORKFLOW_SCHEMAS["qa"]["valid_phases"][0]

        # Act
        state = ps.create_workflow("STORY-521", "qa")

        # Assert
        assert state["current_phase"] == expected_first_phase

    def test_complete_workflow_phase_dev_respects_valid_phases_list(self, tmp_path):
        """complete_workflow_phase rejects a phase not in dev valid_phases."""
        # Arrange
        ps = PhaseState(project_root=tmp_path)
        ps.create_workflow("STORY-521", "dev")

        # Act + Assert: phase "00" is not valid for dev workflow
        with pytest.raises(PhaseNotFoundError):
            ps.complete_workflow_phase("STORY-521", "dev", "00", False)

    def test_complete_workflow_phase_qa_respects_valid_phases_list(self, tmp_path):
        """complete_workflow_phase rejects a dev phase used in qa context."""
        # Arrange
        ps = PhaseState(project_root=tmp_path)
        ps.create_workflow("STORY-521", "qa")

        # Act + Assert: phase "09" is not valid for qa workflow
        with pytest.raises(PhaseNotFoundError):
            ps.complete_workflow_phase("STORY-521", "qa", "09", False)

    def test_complete_workflow_phase_advances_through_dev_schema_phases(self, tmp_path):
        """complete_workflow_phase advances current_phase through all dev phases in schema order."""
        # Arrange
        ps = PhaseState(project_root=tmp_path)
        ps.create_workflow("STORY-521", "dev")
        dev_phases = WORKFLOW_SCHEMAS["dev"]["valid_phases"]

        # Act: complete each phase via escape hatch and verify advancement
        for i, phase in enumerate(dev_phases[:-1]):
            state = ps.complete_workflow_phase("STORY-521", "dev", phase, False)
            expected_next = dev_phases[i + 1]
            assert state["current_phase"] == expected_next, (
                f"After completing phase {phase}, expected current_phase={expected_next}, "
                f"got {state['current_phase']}"
            )

    def test_complete_workflow_phase_advances_through_qa_schema_phases(self, tmp_path):
        """complete_workflow_phase advances current_phase through all QA phases in schema order."""
        # Arrange
        ps = PhaseState(project_root=tmp_path)
        ps.create_workflow("STORY-521", "qa")
        qa_phases = WORKFLOW_SCHEMAS["qa"]["valid_phases"]

        # Act: complete each phase via escape hatch and verify advancement
        for i, phase in enumerate(qa_phases[:-1]):
            state = ps.complete_workflow_phase("STORY-521", "qa", phase, False)
            expected_next = qa_phases[i + 1]
            assert state["current_phase"] == expected_next, (
                f"After completing QA phase {phase}, expected current_phase={expected_next}, "
                f"got {state['current_phase']}"
            )

    def test_unknown_workflow_raises_value_error(self, tmp_path):
        """create_workflow and complete_workflow_phase raise ValueError for unknown workflows."""
        # Arrange
        ps = PhaseState(project_root=tmp_path)

        # Act + Assert: create
        with pytest.raises(ValueError, match="Unknown workflow"):
            ps.create_workflow("STORY-521", "unknown")

    def test_dev_schema_phases_have_required_keys(self):
        """Each phase in DEV_PHASES schema contains steps_required and subagents_required."""
        dev_phases = WORKFLOW_SCHEMAS["dev"]["phases"]
        for phase_id, phase_def in dev_phases.items():
            assert "steps_required" in phase_def, (
                f"DEV phase {phase_id} missing 'steps_required'"
            )
            assert "subagents_required" in phase_def, (
                f"DEV phase {phase_id} missing 'subagents_required'"
            )

    def test_qa_schema_phases_have_required_keys(self):
        """Each phase in QA_PHASES schema contains steps_required and subagents_required."""
        qa_phases = WORKFLOW_SCHEMAS["qa"]["phases"]
        for phase_id, phase_def in qa_phases.items():
            assert "steps_required" in phase_def, (
                f"QA phase {phase_id} missing 'steps_required'"
            )
            assert "subagents_required" in phase_def, (
                f"QA phase {phase_id} missing 'subagents_required'"
            )

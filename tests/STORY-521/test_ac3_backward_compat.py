"""
Test: AC#3 - Backward Compatibility
Story: STORY-521 - Unify Dev and QA Phase Tracking Under Single CLI Interface

Tests that existing behavior is preserved when --workflow flag is omitted
(defaults to "dev").

These tests exercise existing functionality but through the lens of the
unified interface. They should pass if backward compatibility is maintained.
"""

import json
import pytest
from pathlib import Path


class TestPhaseInitDefaultWorkflow:
    """phase_init_command without --workflow flag defaults to 'dev'."""

    def test_should_default_to_dev_workflow(self, project_root):
        """Calling phase_init_command without workflow param uses dev."""
        from devforgeai_cli.commands.phase_commands import phase_init_command

        # No workflow parameter - should default to "dev"
        result = phase_init_command("STORY-521", project_root)
        assert result == 0

    def test_should_create_phase_state_json(self, project_root):
        """Default workflow creates {STORY_ID}-phase-state.json."""
        from devforgeai_cli.commands.phase_commands import phase_init_command

        phase_init_command("STORY-521", project_root)

        state_file = (
            Path(project_root) / "devforgeai" / "workflows" / "STORY-521-phase-state.json"
        )
        assert state_file.exists(), f"Expected state file at {state_file}"

    def test_should_have_dev_phases_in_state(self, project_root):
        """State file must contain dev workflow phases."""
        from devforgeai_cli.commands.phase_commands import phase_init_command
        from devforgeai_cli.phase_state import PhaseState

        phase_init_command("STORY-521", project_root)

        ps = PhaseState(project_root=Path(project_root))
        state = ps.read("STORY-521")
        assert state is not None
        assert "01" in state["phases"]
        assert "10" in state["phases"]


class TestPhaseCompleteDefaultWorkflow:
    """phase_complete_command without --workflow flag defaults to 'dev'."""

    def test_should_default_to_dev_workflow(self, project_root):
        """Calling phase_complete_command without workflow param uses dev."""
        from devforgeai_cli.commands.phase_commands import (
            phase_init_command,
            phase_complete_command,
        )

        phase_init_command("STORY-521", project_root)
        result = phase_complete_command("STORY-521", "01", True, project_root)
        assert result == 0


class TestExistingDevBehaviorPreserved:
    """All existing dev workflow behavior must be identical."""

    def test_should_return_exit_1_for_existing_state(self, project_root):
        """Double init returns exit code 1 (state exists)."""
        from devforgeai_cli.commands.phase_commands import phase_init_command

        phase_init_command("STORY-521", project_root)
        result = phase_init_command("STORY-521", project_root)
        assert result == 1

    def test_should_return_exit_2_for_invalid_story_id(self, project_root):
        """Invalid story ID returns exit code 2."""
        from devforgeai_cli.commands.phase_commands import phase_init_command

        result = phase_init_command("INVALID", project_root)
        assert result == 2

    def test_should_advance_current_phase_after_complete(self, project_root):
        """Completing phase 01 advances current_phase to 02."""
        from devforgeai_cli.commands.phase_commands import (
            phase_init_command,
            phase_complete_command,
        )
        from devforgeai_cli.phase_state import PhaseState

        phase_init_command("STORY-521", project_root)
        phase_complete_command("STORY-521", "01", True, project_root)

        ps = PhaseState(project_root=Path(project_root))
        state = ps.read("STORY-521")
        assert state["current_phase"] == "02"

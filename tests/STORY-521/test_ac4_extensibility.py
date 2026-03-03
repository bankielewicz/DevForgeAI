"""
Test: AC#4 - Extensibility
Story: STORY-521 - Unify Dev and QA Phase Tracking Under Single CLI Interface

Tests that new workflow types can be added to WORKFLOW_SCHEMAS without
code changes, and that unknown workflow types return exit code 2.

These tests MUST FAIL in Red phase because WORKFLOW_SCHEMAS does not exist yet.
"""

import pytest


MOCK_RELEASE_PHASES = {
    "01": {
        "steps_required": ["pre_release_check"],
        "subagents_required": [],
        "checkpoint_description": "Pre-release validation",
    },
    "02": {
        "steps_required": ["deploy", "smoke_test"],
        "subagents_required": ["deployment-engineer"],
        "checkpoint_description": "Deployment and smoke test",
    },
}


class TestAddMockWorkflowToRegistry:
    """Adding a new workflow to WORKFLOW_SCHEMAS should work without code changes."""

    def test_should_accept_release_workflow_in_registry(self, monkeypatch):
        """Adding RELEASE_PHASES to WORKFLOW_SCHEMAS makes 'release' a valid workflow."""
        from devforgeai_cli import phase_state as ps_module
        from devforgeai_cli.phase_state import WORKFLOW_SCHEMAS

        # Monkeypatch: add release workflow to the registry
        patched = dict(WORKFLOW_SCHEMAS)
        patched["release"] = {
            "phases": MOCK_RELEASE_PHASES,
            "valid_phases": ["01", "02"],
        }
        monkeypatch.setattr(ps_module, "WORKFLOW_SCHEMAS", patched)

        # Also patch VALID_WORKFLOWS to include 'release'
        monkeypatch.setattr(ps_module, "VALID_WORKFLOWS", ["dev", "qa", "release"])

        from devforgeai_cli.phase_state import WORKFLOW_SCHEMAS as WS
        assert "release" in WS

    def test_should_init_release_workflow_via_registry(self, project_root, monkeypatch):
        """phase_init_command with workflow='release' creates state file."""
        from devforgeai_cli import phase_state as ps_module
        from devforgeai_cli.phase_state import WORKFLOW_SCHEMAS
        from devforgeai_cli.commands.phase_commands import phase_init_command

        patched = dict(WORKFLOW_SCHEMAS)
        patched["release"] = {
            "phases": MOCK_RELEASE_PHASES,
            "valid_phases": ["01", "02"],
        }
        monkeypatch.setattr(ps_module, "WORKFLOW_SCHEMAS", patched)
        monkeypatch.setattr(ps_module, "VALID_WORKFLOWS", ["dev", "qa", "release"])

        result = phase_init_command("STORY-521", project_root, workflow="release")
        assert result == 0


class TestUnknownWorkflowType:
    """Unknown workflow types must return exit code 2."""

    def test_should_return_exit_2_for_unknown_workflow(self, project_root):
        """phase_init_command with unknown workflow returns exit code 2."""
        from devforgeai_cli.commands.phase_commands import phase_init_command

        result = phase_init_command("STORY-521", project_root, workflow="unknown")
        assert result == 2

    def test_should_return_exit_2_for_empty_workflow(self, project_root):
        """phase_init_command with empty string workflow returns exit code 2."""
        from devforgeai_cli.commands.phase_commands import phase_init_command

        result = phase_init_command("STORY-521", project_root, workflow="")
        assert result == 2

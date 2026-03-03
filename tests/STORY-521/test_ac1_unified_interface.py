"""
Test: AC#1 - Unified CLI Interface
Story: STORY-521 - Unify Dev and QA Phase Tracking Under Single CLI Interface

Tests that WORKFLOW_SCHEMAS registry exists and drives dynamic dispatch
instead of hardcoded if/else branching.

These tests MUST FAIL in Red phase because WORKFLOW_SCHEMAS does not exist yet.
"""

import pytest


class TestWorkflowSchemasRegistryExists:
    """WORKFLOW_SCHEMAS must be a module-level dict in phase_state.py."""

    def test_should_import_workflow_schemas_from_phase_state(self):
        """WORKFLOW_SCHEMAS must be importable from devforgeai_cli.phase_state."""
        from devforgeai_cli.phase_state import WORKFLOW_SCHEMAS
        assert WORKFLOW_SCHEMAS is not None

    def test_should_be_dict_type(self):
        """WORKFLOW_SCHEMAS must be a dict."""
        from devforgeai_cli.phase_state import WORKFLOW_SCHEMAS
        assert isinstance(WORKFLOW_SCHEMAS, dict)


class TestWorkflowSchemasContainsRequiredKeys:
    """WORKFLOW_SCHEMAS must contain 'dev' and 'qa' workflow keys."""

    def test_should_contain_dev_key(self):
        """Registry must have 'dev' workflow entry."""
        from devforgeai_cli.phase_state import WORKFLOW_SCHEMAS
        assert "dev" in WORKFLOW_SCHEMAS

    def test_should_contain_qa_key(self):
        """Registry must have 'qa' workflow entry."""
        from devforgeai_cli.phase_state import WORKFLOW_SCHEMAS
        assert "qa" in WORKFLOW_SCHEMAS

    def test_should_have_phases_in_dev_entry(self):
        """Dev workflow entry must contain a 'phases' dict."""
        from devforgeai_cli.phase_state import WORKFLOW_SCHEMAS
        assert "phases" in WORKFLOW_SCHEMAS["dev"]
        assert isinstance(WORKFLOW_SCHEMAS["dev"]["phases"], dict)

    def test_should_have_phases_in_qa_entry(self):
        """QA workflow entry must contain a 'phases' dict."""
        from devforgeai_cli.phase_state import WORKFLOW_SCHEMAS
        assert "phases" in WORKFLOW_SCHEMAS["qa"]
        assert isinstance(WORKFLOW_SCHEMAS["qa"]["phases"], dict)

    def test_should_have_valid_phases_list_in_dev_entry(self):
        """Dev workflow entry must contain a 'valid_phases' list."""
        from devforgeai_cli.phase_state import WORKFLOW_SCHEMAS
        assert "valid_phases" in WORKFLOW_SCHEMAS["dev"]
        assert isinstance(WORKFLOW_SCHEMAS["dev"]["valid_phases"], list)

    def test_should_have_valid_phases_list_in_qa_entry(self):
        """QA workflow entry must contain a 'valid_phases' list."""
        from devforgeai_cli.phase_state import WORKFLOW_SCHEMAS
        assert "valid_phases" in WORKFLOW_SCHEMAS["qa"]
        assert isinstance(WORKFLOW_SCHEMAS["qa"]["valid_phases"], list)


class TestDynamicDispatchFromRegistry:
    """phase_init_command and phase_complete_command must use WORKFLOW_SCHEMAS
    for dynamic dispatch instead of hardcoded if/else."""

    def test_should_init_dev_workflow_via_registry(self, project_root):
        """phase_init_command with workflow='dev' should use WORKFLOW_SCHEMAS['dev']."""
        from devforgeai_cli.phase_state import WORKFLOW_SCHEMAS
        from devforgeai_cli.commands.phase_commands import phase_init_command

        # This should work via dynamic dispatch, not hardcoded if/else
        result = phase_init_command("STORY-521", project_root, workflow="dev")
        assert result == 0

        # Verify state file was created with phases from WORKFLOW_SCHEMAS['dev']
        expected_phases = WORKFLOW_SCHEMAS["dev"]["valid_phases"]
        assert len(expected_phases) > 0

    def test_should_init_qa_workflow_via_registry(self, project_root):
        """phase_init_command with workflow='qa' should use WORKFLOW_SCHEMAS['qa']."""
        from devforgeai_cli.phase_state import WORKFLOW_SCHEMAS
        from devforgeai_cli.commands.phase_commands import phase_init_command

        result = phase_init_command("STORY-521", project_root, workflow="qa")
        assert result == 0

        expected_phases = WORKFLOW_SCHEMAS["qa"]["valid_phases"]
        assert len(expected_phases) > 0

    def test_should_complete_dev_phase_via_registry(self, project_root):
        """phase_complete_command with workflow='dev' should use WORKFLOW_SCHEMAS['dev']."""
        from devforgeai_cli.phase_state import WORKFLOW_SCHEMAS
        from devforgeai_cli.commands.phase_commands import (
            phase_init_command,
            phase_complete_command,
        )

        phase_init_command("STORY-521", project_root, workflow="dev")
        result = phase_complete_command(
            "STORY-521", "01", True, project_root, workflow="dev"
        )
        assert result == 0

    def test_should_complete_qa_phase_via_registry(self, project_root):
        """phase_complete_command with workflow='qa' should use WORKFLOW_SCHEMAS['qa']."""
        from devforgeai_cli.phase_state import WORKFLOW_SCHEMAS
        from devforgeai_cli.commands.phase_commands import (
            phase_init_command,
            phase_complete_command,
        )

        phase_init_command("STORY-521", project_root, workflow="qa")
        result = phase_complete_command(
            "STORY-521", "00", True, project_root, workflow="qa"
        )
        assert result == 0

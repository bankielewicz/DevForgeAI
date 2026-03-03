"""
Test: AC#2 - Schema Constants
Story: STORY-521 - Unify Dev and QA Phase Tracking Under Single CLI Interface

Tests that DEV_PHASES and QA_PHASES dicts exist with correct structure
and that DEV_PHASES subagents_required matches PHASE_REQUIRED_SUBAGENTS.

These tests MUST FAIL in Red phase because DEV_PHASES does not exist yet.
"""

import pytest


# Expected dev phases: "01" through "10" including "4.5" and "5.5"
EXPECTED_DEV_PHASE_KEYS = [
    "01", "02", "03", "04", "4.5", "05", "5.5", "06", "07", "08", "09", "10"
]

EXPECTED_QA_PHASE_KEYS = ["00", "01", "1.5", "02", "03", "04"]

REQUIRED_PHASE_ENTRY_KEYS = {"steps_required", "subagents_required", "checkpoint_description"}


class TestDevPhasesExists:
    """DEV_PHASES must be a module-level dict in phase_state.py."""

    def test_should_import_dev_phases_from_phase_state(self):
        """DEV_PHASES must be importable from devforgeai_cli.phase_state."""
        from devforgeai_cli.phase_state import DEV_PHASES
        assert DEV_PHASES is not None

    def test_should_be_dict_type(self):
        """DEV_PHASES must be a dict."""
        from devforgeai_cli.phase_state import DEV_PHASES
        assert isinstance(DEV_PHASES, dict)

    def test_should_contain_all_12_dev_phases(self):
        """DEV_PHASES must have all 12 phase keys."""
        from devforgeai_cli.phase_state import DEV_PHASES
        for phase_key in EXPECTED_DEV_PHASE_KEYS:
            assert phase_key in DEV_PHASES, f"Missing phase key: {phase_key}"
        assert len(DEV_PHASES) == 12


class TestDevPhasesStructure:
    """Each DEV_PHASES entry must have required keys."""

    @pytest.mark.parametrize("phase_key", EXPECTED_DEV_PHASE_KEYS)
    def test_should_have_required_keys_for_phase(self, phase_key):
        """Each phase entry must have steps_required, subagents_required, checkpoint_description."""
        from devforgeai_cli.phase_state import DEV_PHASES
        phase_entry = DEV_PHASES[phase_key]
        for key in REQUIRED_PHASE_ENTRY_KEYS:
            assert key in phase_entry, (
                f"Phase '{phase_key}' missing key: '{key}'"
            )

    @pytest.mark.parametrize("phase_key", EXPECTED_DEV_PHASE_KEYS)
    def test_should_have_list_for_steps_required(self, phase_key):
        """steps_required must be a list."""
        from devforgeai_cli.phase_state import DEV_PHASES
        assert isinstance(DEV_PHASES[phase_key]["steps_required"], list)

    @pytest.mark.parametrize("phase_key", EXPECTED_DEV_PHASE_KEYS)
    def test_should_have_list_for_subagents_required(self, phase_key):
        """subagents_required must be a list."""
        from devforgeai_cli.phase_state import DEV_PHASES
        assert isinstance(DEV_PHASES[phase_key]["subagents_required"], list)

    @pytest.mark.parametrize("phase_key", EXPECTED_DEV_PHASE_KEYS)
    def test_should_have_string_for_checkpoint_description(self, phase_key):
        """checkpoint_description must be a non-empty string."""
        from devforgeai_cli.phase_state import DEV_PHASES
        desc = DEV_PHASES[phase_key]["checkpoint_description"]
        assert isinstance(desc, str)
        assert len(desc) > 0


class TestQaPhasesStructure:
    """QA_PHASES must have the same structure with checkpoint_description."""

    @pytest.mark.parametrize("phase_key", EXPECTED_QA_PHASE_KEYS)
    def test_should_have_checkpoint_description(self, phase_key):
        """Each QA phase entry must have checkpoint_description key."""
        from devforgeai_cli.phase_state import QA_PHASES
        assert "checkpoint_description" in QA_PHASES[phase_key], (
            f"QA phase '{phase_key}' missing 'checkpoint_description'"
        )

    @pytest.mark.parametrize("phase_key", EXPECTED_QA_PHASE_KEYS)
    def test_should_have_string_checkpoint_description(self, phase_key):
        """checkpoint_description must be a non-empty string."""
        from devforgeai_cli.phase_state import QA_PHASES
        desc = QA_PHASES[phase_key]["checkpoint_description"]
        assert isinstance(desc, str)
        assert len(desc) > 0


class TestDevPhasesMatchesExistingSubagents:
    """DEV_PHASES subagents_required must match PHASE_REQUIRED_SUBAGENTS values."""

    @pytest.mark.parametrize("phase_key", EXPECTED_DEV_PHASE_KEYS)
    def test_should_match_phase_required_subagents(self, phase_key):
        """DEV_PHASES[phase].subagents_required must equal PHASE_REQUIRED_SUBAGENTS[phase]."""
        from devforgeai_cli.phase_state import DEV_PHASES, PHASE_REQUIRED_SUBAGENTS

        expected = PHASE_REQUIRED_SUBAGENTS.get(phase_key, [])
        actual = DEV_PHASES[phase_key]["subagents_required"]
        assert actual == expected, (
            f"Phase '{phase_key}': DEV_PHASES subagents {actual} != "
            f"PHASE_REQUIRED_SUBAGENTS {expected}"
        )

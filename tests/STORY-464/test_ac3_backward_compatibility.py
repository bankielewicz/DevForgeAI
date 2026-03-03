"""
Test: AC#3 - Non-OR phases remain backward compatible
Story: STORY-464
Generated: 2026-02-21

Validates that phase_check_command continues to work correctly with
simple string-only subagents_required lists (no nested OR-groups).
The fix must not regress existing behavior for flat requirement lists.

These tests verify backward compatibility. They should PASS against both
the current and fixed code for the simple cases, but the test suite as
a whole exercises the OR-group path which crashes the current code.
"""

import json
import sys
from pathlib import Path

import pytest

# Add source path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src" / "claude" / "scripts"))

from devforgeai_cli.commands.phase_commands import phase_check_command


def _all_phases_dict(overrides: dict = None) -> dict:
    """Build a complete phases dict with all 12 valid phases."""
    valid_phases = [
        "01", "02", "03", "04", "4.5", "05", "5.5",
        "06", "07", "08", "09", "10"
    ]
    phases = {}
    for phase in valid_phases:
        phases[phase] = {
            "status": "pending",
            "subagents_required": [],
            "subagents_invoked": [],
        }
    if overrides:
        for phase_id, phase_data in overrides.items():
            phases[phase_id].update(phase_data)
    return phases


def _write_state(tmp_path: Path, story_id: str, state: dict) -> Path:
    """Write a phase state JSON file and return its path."""
    workflows_dir = tmp_path / "devforgeai" / "workflows"
    workflows_dir.mkdir(parents=True, exist_ok=True)
    state_file = workflows_dir / f"{story_id}-phase-state.json"
    state_file.write_text(json.dumps(state, indent=2))
    return state_file


class TestAC3BackwardCompatibility:
    """AC#3: Simple string requirements behave identically before and after fix."""

    def test_should_allow_transition_when_simple_string_invoked(self, tmp_path):
        """
        Given: subagents_required: ["test-automator"] (flat string, no OR-group)
               with "test-automator" in subagents_invoked
        When: phase_check_command checks 02->03
        Then: Returns exit code 0 (transition allowed)
        """
        state = {
            "story_id": "STORY-920",
            "current_phase": "03",
            "workflow_started": "2026-02-21T00:00:00Z",
            "blocking_status": False,
            "phases": _all_phases_dict({
                "02": {
                    "status": "completed",
                    "subagents_required": ["test-automator"],
                    "subagents_invoked": ["test-automator"],
                },
            }),
            "validation_errors": [],
            "observations": [],
        }

        _write_state(tmp_path, "STORY-920", state)

        exit_code = phase_check_command(
            story_id="STORY-920",
            from_phase="02",
            to_phase="03",
            project_root=str(tmp_path),
            format="text",
        )

        assert exit_code == 0, (
            f"Expected exit code 0 but got {exit_code}. "
            "Simple string requirement invoked should allow transition."
        )

    def test_should_block_transition_when_simple_string_missing(self, tmp_path):
        """
        Given: subagents_required: ["test-automator"] (flat string)
               with empty subagents_invoked
        When: phase_check_command checks 02->03
        Then: Returns exit code 2 (missing subagents)
        """
        state = {
            "story_id": "STORY-921",
            "current_phase": "03",
            "workflow_started": "2026-02-21T00:00:00Z",
            "blocking_status": False,
            "phases": _all_phases_dict({
                "02": {
                    "status": "completed",
                    "subagents_required": ["test-automator"],
                    "subagents_invoked": [],
                },
            }),
            "validation_errors": [],
            "observations": [],
        }

        _write_state(tmp_path, "STORY-921", state)

        exit_code = phase_check_command(
            story_id="STORY-921",
            from_phase="02",
            to_phase="03",
            project_root=str(tmp_path),
            format="text",
        )

        assert exit_code == 2, (
            f"Expected exit code 2 (missing subagents) but got {exit_code}. "
            "Missing simple string requirement should block transition."
        )

    def test_should_allow_transition_when_empty_requirements(self, tmp_path):
        """
        Given: subagents_required is empty []
        When: phase_check_command checks transition
        Then: Returns exit code 0 (no requirements to check)
        """
        state = {
            "story_id": "STORY-922",
            "current_phase": "08",
            "workflow_started": "2026-02-21T00:00:00Z",
            "blocking_status": False,
            "phases": _all_phases_dict({
                "07": {
                    "status": "completed",
                    "subagents_required": [],
                    "subagents_invoked": [],
                },
            }),
            "validation_errors": [],
            "observations": [],
        }

        _write_state(tmp_path, "STORY-922", state)

        exit_code = phase_check_command(
            story_id="STORY-922",
            from_phase="07",
            to_phase="08",
            project_root=str(tmp_path),
            format="text",
        )

        assert exit_code == 0, (
            f"Expected exit code 0 but got {exit_code}. "
            "Empty subagents_required should allow transition."
        )

    def test_should_allow_transition_with_multiple_simple_strings_all_invoked(self, tmp_path):
        """
        Given: subagents_required: ["git-validator", "tech-stack-detector"]
               with both invoked
        When: phase_check_command checks 01->02
        Then: Returns exit code 0
        """
        state = {
            "story_id": "STORY-923",
            "current_phase": "02",
            "workflow_started": "2026-02-21T00:00:00Z",
            "blocking_status": False,
            "phases": _all_phases_dict({
                "01": {
                    "status": "completed",
                    "subagents_required": ["git-validator", "tech-stack-detector"],
                    "subagents_invoked": ["git-validator", "tech-stack-detector"],
                },
            }),
            "validation_errors": [],
            "observations": [],
        }

        _write_state(tmp_path, "STORY-923", state)

        exit_code = phase_check_command(
            story_id="STORY-923",
            from_phase="01",
            to_phase="02",
            project_root=str(tmp_path),
            format="text",
        )

        assert exit_code == 0, (
            f"Expected exit code 0 but got {exit_code}. "
            "Multiple simple strings all invoked should allow transition."
        )

    def test_should_block_when_one_of_multiple_simple_strings_missing(self, tmp_path, capsys):
        """
        Given: subagents_required: ["git-validator", "tech-stack-detector"]
               with only "git-validator" invoked
        When: phase_check_command checks 01->02
        Then: Returns exit code 2 and reports "tech-stack-detector" as missing
        """
        state = {
            "story_id": "STORY-924",
            "current_phase": "02",
            "workflow_started": "2026-02-21T00:00:00Z",
            "blocking_status": False,
            "phases": _all_phases_dict({
                "01": {
                    "status": "completed",
                    "subagents_required": ["git-validator", "tech-stack-detector"],
                    "subagents_invoked": ["git-validator"],
                },
            }),
            "validation_errors": [],
            "observations": [],
        }

        _write_state(tmp_path, "STORY-924", state)

        exit_code = phase_check_command(
            story_id="STORY-924",
            from_phase="01",
            to_phase="02",
            project_root=str(tmp_path),
            format="text",
        )

        output = capsys.readouterr().out

        assert exit_code == 2, (
            f"Expected exit code 2 but got {exit_code}."
        )
        assert "tech-stack-detector" in output, (
            f"Expected 'tech-stack-detector' in missing subagents output but got:\n{output}"
        )

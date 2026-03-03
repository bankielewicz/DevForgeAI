"""
Test: AC#2 - OR-group with missing subagent reports descriptive error
Story: STORY-464
Generated: 2026-02-21

Validates that when an OR-group requirement is unsatisfied (no members invoked),
phase_check_command returns exit code 2 and the error output contains the
OR-group formatted as "(backend-architect OR frontend-developer)".

These tests MUST FAIL against the current broken code (TDD Red phase)
because the set() conversion on line 223 crashes before any error message
can be produced.
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


class TestAC2OrGroupErrorMessage:
    """AC#2: Unsatisfied OR-groups produce descriptive error messages."""

    def test_should_return_exit_2_when_or_group_unsatisfied(self, tmp_path, capsys):
        """
        Given: OR-group ["backend-architect", "frontend-developer"] with neither invoked
               and "context-validator" invoked
        When: phase_check_command is called for 03->04
        Then: Returns exit code 2 (missing subagents)
        """
        state = {
            "story_id": "STORY-910",
            "current_phase": "04",
            "workflow_started": "2026-02-21T00:00:00Z",
            "blocking_status": False,
            "phases": _all_phases_dict({
                "03": {
                    "status": "completed",
                    "subagents_required": [
                        ["backend-architect", "frontend-developer"],
                        "context-validator"
                    ],
                    "subagents_invoked": ["context-validator"],
                },
            }),
            "validation_errors": [],
            "observations": [],
        }

        _write_state(tmp_path, "STORY-910", state)

        exit_code = phase_check_command(
            story_id="STORY-910",
            from_phase="03",
            to_phase="04",
            project_root=str(tmp_path),
            format="text",
        )

        assert exit_code == 2, (
            f"Expected exit code 2 (missing subagents) but got {exit_code}. "
            "Unsatisfied OR-group should report missing subagents."
        )

    def test_should_output_or_group_format_in_error(self, tmp_path, capsys):
        """
        Given: OR-group ["backend-architect", "frontend-developer"] unsatisfied
        When: phase_check_command outputs the error
        Then: Output contains "(backend-architect OR frontend-developer)"
              matching the convention from phase_state.py line 619
        """
        state = {
            "story_id": "STORY-911",
            "current_phase": "04",
            "workflow_started": "2026-02-21T00:00:00Z",
            "blocking_status": False,
            "phases": _all_phases_dict({
                "03": {
                    "status": "completed",
                    "subagents_required": [
                        ["backend-architect", "frontend-developer"],
                        "context-validator"
                    ],
                    "subagents_invoked": ["context-validator"],
                },
            }),
            "validation_errors": [],
            "observations": [],
        }

        _write_state(tmp_path, "STORY-911", state)

        exit_code = phase_check_command(
            story_id="STORY-911",
            from_phase="03",
            to_phase="04",
            project_root=str(tmp_path),
            format="text",
        )

        output = capsys.readouterr().out

        assert exit_code == 2
        assert "(backend-architect OR frontend-developer)" in output, (
            f"Expected '(backend-architect OR frontend-developer)' in output but got:\n{output}\n"
            "OR-group format must use parentheses and uppercase OR, matching phase_state.py line 619."
        )

    def test_should_report_only_unsatisfied_requirements(self, tmp_path, capsys):
        """
        Given: Mixed requirements - OR-group satisfied, simple string unsatisfied
        When: phase_check_command outputs the error
        Then: Only the unsatisfied requirement appears in error output
              The satisfied OR-group does NOT appear
        """
        state = {
            "story_id": "STORY-912",
            "current_phase": "04",
            "workflow_started": "2026-02-21T00:00:00Z",
            "blocking_status": False,
            "phases": _all_phases_dict({
                "03": {
                    "status": "completed",
                    "subagents_required": [
                        ["backend-architect", "frontend-developer"],
                        "context-validator"
                    ],
                    # OR-group satisfied (backend-architect), but context-validator missing
                    "subagents_invoked": ["backend-architect"],
                },
            }),
            "validation_errors": [],
            "observations": [],
        }

        _write_state(tmp_path, "STORY-912", state)

        exit_code = phase_check_command(
            story_id="STORY-912",
            from_phase="03",
            to_phase="04",
            project_root=str(tmp_path),
            format="text",
        )

        output = capsys.readouterr().out

        assert exit_code == 2, (
            f"Expected exit code 2 but got {exit_code}. "
            "Missing context-validator should block transition."
        )
        assert "context-validator" in output, (
            f"Expected 'context-validator' in output but got:\n{output}"
        )
        assert "(backend-architect OR frontend-developer)" not in output, (
            "Satisfied OR-group should NOT appear in error output, "
            f"but found it in:\n{output}"
        )

    def test_should_report_all_unsatisfied_when_mixed(self, tmp_path, capsys):
        """
        Given: Both an unsatisfied OR-group AND an unsatisfied simple string
        When: phase_check_command outputs the error
        Then: Both appear in the error output
        """
        state = {
            "story_id": "STORY-913",
            "current_phase": "04",
            "workflow_started": "2026-02-21T00:00:00Z",
            "blocking_status": False,
            "phases": _all_phases_dict({
                "03": {
                    "status": "completed",
                    "subagents_required": [
                        ["backend-architect", "frontend-developer"],
                        "context-validator"
                    ],
                    # Nothing invoked
                    "subagents_invoked": [],
                },
            }),
            "validation_errors": [],
            "observations": [],
        }

        _write_state(tmp_path, "STORY-913", state)

        exit_code = phase_check_command(
            story_id="STORY-913",
            from_phase="03",
            to_phase="04",
            project_root=str(tmp_path),
            format="text",
        )

        output = capsys.readouterr().out

        assert exit_code == 2
        assert "(backend-architect OR frontend-developer)" in output, (
            f"Expected OR-group format in output but got:\n{output}"
        )
        assert "context-validator" in output, (
            f"Expected 'context-validator' in output but got:\n{output}"
        )

    def test_should_report_single_element_or_group_unsatisfied(self, tmp_path, capsys):
        """
        Given: Single-element OR-group ["only-agent"] that is unsatisfied
        When: phase_check_command outputs the error
        Then: Output contains "(only-agent)" formatted as an OR-group
        """
        state = {
            "story_id": "STORY-914",
            "current_phase": "04",
            "workflow_started": "2026-02-21T00:00:00Z",
            "blocking_status": False,
            "phases": _all_phases_dict({
                "03": {
                    "status": "completed",
                    "subagents_required": [
                        ["only-agent"],
                    ],
                    "subagents_invoked": [],
                },
            }),
            "validation_errors": [],
            "observations": [],
        }

        _write_state(tmp_path, "STORY-914", state)

        exit_code = phase_check_command(
            story_id="STORY-914",
            from_phase="03",
            to_phase="04",
            project_root=str(tmp_path),
            format="text",
        )

        output = capsys.readouterr().out

        assert exit_code == 2
        assert "(only-agent)" in output, (
            f"Expected '(only-agent)' in output but got:\n{output}\n"
            "Single-element OR-group should still use parenthesized format."
        )

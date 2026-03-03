"""
Test: AC#4 - JSON output format includes OR-group strings
Story: STORY-464
Generated: 2026-02-21

Validates that when --format=json is used and an OR-group requirement is
unsatisfied, the JSON output is valid (parseable by json.loads()) and contains
a "missing_subagents" array with the OR-group formatted as
"(backend-architect OR frontend-developer)".

These tests MUST FAIL against the current broken code (TDD Red phase)
because the set() conversion crashes before JSON output can be produced.
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


class TestAC4JsonOutputOrGroups:
    """AC#4: JSON output with --format=json includes OR-group strings."""

    def test_should_produce_valid_json_with_missing_or_group(self, tmp_path, capsys):
        """
        Given: Unsatisfied OR-group with --format=json
        When: phase_check_command outputs the result
        Then: Output is valid JSON parseable by json.loads()
        """
        state = {
            "story_id": "STORY-930",
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

        _write_state(tmp_path, "STORY-930", state)

        exit_code = phase_check_command(
            story_id="STORY-930",
            from_phase="03",
            to_phase="04",
            project_root=str(tmp_path),
            format="json",
        )

        output = capsys.readouterr().out

        # Must not crash (exit code would be 1 from exception handler if it crashed)
        assert exit_code == 2, (
            f"Expected exit code 2 (missing subagents) but got {exit_code}. "
            "Unsatisfied OR-group should return exit code 2 even in JSON mode."
        )

        # Output must be valid JSON
        try:
            result = json.loads(output)
        except json.JSONDecodeError as e:
            pytest.fail(
                f"JSON output is not valid: {e}\nRaw output:\n{output}"
            )

    def test_should_include_missing_subagents_array_in_json(self, tmp_path, capsys):
        """
        Given: Unsatisfied OR-group with --format=json
        When: phase_check_command outputs JSON
        Then: JSON contains "missing_subagents" array
        """
        state = {
            "story_id": "STORY-931",
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

        _write_state(tmp_path, "STORY-931", state)

        exit_code = phase_check_command(
            story_id="STORY-931",
            from_phase="03",
            to_phase="04",
            project_root=str(tmp_path),
            format="json",
        )

        output = capsys.readouterr().out
        result = json.loads(output)

        assert exit_code == 2
        assert "missing_subagents" in result, (
            f"Expected 'missing_subagents' key in JSON output but got keys: {list(result.keys())}"
        )
        assert isinstance(result["missing_subagents"], list), (
            f"Expected 'missing_subagents' to be a list but got {type(result['missing_subagents'])}"
        )

    def test_should_format_or_group_in_json_missing_subagents(self, tmp_path, capsys):
        """
        Given: Unsatisfied OR-group ["backend-architect", "frontend-developer"]
        When: phase_check_command outputs JSON with --format=json
        Then: missing_subagents array contains "(backend-architect OR frontend-developer)"
        """
        state = {
            "story_id": "STORY-932",
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

        _write_state(tmp_path, "STORY-932", state)

        exit_code = phase_check_command(
            story_id="STORY-932",
            from_phase="03",
            to_phase="04",
            project_root=str(tmp_path),
            format="json",
        )

        output = capsys.readouterr().out
        result = json.loads(output)

        assert exit_code == 2
        assert "(backend-architect OR frontend-developer)" in result["missing_subagents"], (
            f"Expected '(backend-architect OR frontend-developer)' in missing_subagents "
            f"but got: {result['missing_subagents']}"
        )

    def test_should_include_allowed_false_in_json(self, tmp_path, capsys):
        """
        Given: Unsatisfied OR-group with --format=json
        When: phase_check_command outputs JSON
        Then: JSON contains "allowed": false
        """
        state = {
            "story_id": "STORY-933",
            "current_phase": "04",
            "workflow_started": "2026-02-21T00:00:00Z",
            "blocking_status": False,
            "phases": _all_phases_dict({
                "03": {
                    "status": "completed",
                    "subagents_required": [
                        ["backend-architect", "frontend-developer"],
                    ],
                    "subagents_invoked": [],
                },
            }),
            "validation_errors": [],
            "observations": [],
        }

        _write_state(tmp_path, "STORY-933", state)

        exit_code = phase_check_command(
            story_id="STORY-933",
            from_phase="03",
            to_phase="04",
            project_root=str(tmp_path),
            format="json",
        )

        output = capsys.readouterr().out
        result = json.loads(output)

        assert exit_code == 2
        assert result.get("allowed") is False, (
            f"Expected 'allowed': false in JSON but got: {result.get('allowed')}"
        )

    def test_should_include_error_field_in_json(self, tmp_path, capsys):
        """
        Given: Unsatisfied OR-group with --format=json
        When: phase_check_command outputs JSON
        Then: JSON contains "error" field with descriptive message
        """
        state = {
            "story_id": "STORY-934",
            "current_phase": "04",
            "workflow_started": "2026-02-21T00:00:00Z",
            "blocking_status": False,
            "phases": _all_phases_dict({
                "03": {
                    "status": "completed",
                    "subagents_required": [
                        ["backend-architect", "frontend-developer"],
                    ],
                    "subagents_invoked": [],
                },
            }),
            "validation_errors": [],
            "observations": [],
        }

        _write_state(tmp_path, "STORY-934", state)

        exit_code = phase_check_command(
            story_id="STORY-934",
            from_phase="03",
            to_phase="04",
            project_root=str(tmp_path),
            format="json",
        )

        output = capsys.readouterr().out
        result = json.loads(output)

        assert exit_code == 2
        assert "error" in result, (
            f"Expected 'error' key in JSON output but got keys: {list(result.keys())}"
        )
        assert len(result["error"]) > 0, "Error message should not be empty"

    def test_should_produce_valid_json_when_or_group_satisfied(self, tmp_path, capsys):
        """
        Given: OR-group satisfied, all requirements met, with --format=json
        When: phase_check_command outputs JSON
        Then: JSON contains "allowed": true
        """
        state = {
            "story_id": "STORY-935",
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
                    "subagents_invoked": [
                        "backend-architect",
                        "context-validator",
                    ],
                },
            }),
            "validation_errors": [],
            "observations": [],
        }

        _write_state(tmp_path, "STORY-935", state)

        exit_code = phase_check_command(
            story_id="STORY-935",
            from_phase="03",
            to_phase="04",
            project_root=str(tmp_path),
            format="json",
        )

        output = capsys.readouterr().out

        assert exit_code == 0, (
            f"Expected exit code 0 but got {exit_code}."
        )

        result = json.loads(output)
        assert result.get("allowed") is True, (
            f"Expected 'allowed': true but got: {result.get('allowed')}"
        )

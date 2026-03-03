"""
Test: AC#1 - OR-group handling in phase_check_command
Story: STORY-464
Generated: 2026-02-21

Validates that phase_check_command handles OR-group subagent requirements
(nested lists in subagents_required) without crashing with TypeError.

The current broken code on lines 222-225 of phase_commands.py uses:
    required = set(state["phases"][from_phase].get("subagents_required", []))
which crashes with TypeError: unhashable type: 'list' when subagents_required
contains nested lists like ["backend-architect", "frontend-developer"].

These tests MUST FAIL against the current broken code (TDD Red phase).
"""

import json
import sys
from pathlib import Path

import pytest

# Add source path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src" / "claude" / "scripts"))

from devforgeai_cli.commands.phase_commands import phase_check_command


def _all_phases_dict(overrides: dict = None) -> dict:
    """Build a complete phases dict with all 12 valid phases.

    Every phase defaults to pending with empty subagents.
    Pass overrides to customize specific phases.
    """
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


class TestAC1OrGroupHandling:
    """AC#1: phase_check_command must handle OR-groups without TypeError."""

    def test_should_not_crash_when_or_group_with_one_member_invoked(self, tmp_path):
        """
        Given: subagents_required contains OR-group ["backend-architect", "frontend-developer"]
               and simple "context-validator", with "backend-architect" and "context-validator" invoked
        When: phase_check_command is called for transition 03->04
        Then: Returns exit code 0 (no crash, no TypeError)

        This test exercises the exact crash path: set() cannot hash a list element.
        """
        state = {
            "story_id": "STORY-901",
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
                    "subagents_invoked": ["backend-architect", "context-validator"],
                },
                "04": {
                    "status": "pending",
                    "subagents_required": [],
                    "subagents_invoked": [],
                },
            }),
            "validation_errors": [],
            "observations": [],
        }

        _write_state(tmp_path, "STORY-901", state)

        # This MUST NOT raise TypeError: unhashable type: 'list'
        exit_code = phase_check_command(
            story_id="STORY-901",
            from_phase="03",
            to_phase="04",
            project_root=str(tmp_path),
            format="text",
        )

        assert exit_code == 0, (
            f"Expected exit code 0 (transition allowed) but got {exit_code}. "
            "OR-group with one member invoked should satisfy the requirement."
        )

    def test_should_not_raise_type_error_with_or_group(self, tmp_path):
        """
        Given: subagents_required contains a nested list (OR-group)
        When: phase_check_command processes the subagents
        Then: No TypeError is raised

        Directly asserts that no TypeError occurs, which is the primary bug.
        """
        state = {
            "story_id": "STORY-902",
            "current_phase": "04",
            "workflow_started": "2026-02-21T00:00:00Z",
            "blocking_status": False,
            "phases": _all_phases_dict({
                "03": {
                    "status": "completed",
                    "subagents_required": [
                        ["backend-architect", "frontend-developer"],
                    ],
                    "subagents_invoked": ["backend-architect"],
                },
            }),
            "validation_errors": [],
            "observations": [],
        }

        _write_state(tmp_path, "STORY-902", state)

        # The bug: set() constructor on line 223 raises TypeError
        # when encountering a list element inside subagents_required
        try:
            exit_code = phase_check_command(
                story_id="STORY-902",
                from_phase="03",
                to_phase="04",
                project_root=str(tmp_path),
                format="text",
            )
        except TypeError as e:
            pytest.fail(
                f"TypeError raised: {e}. "
                "phase_check_command must handle OR-group lists in subagents_required."
            )

        # Should succeed since backend-architect was invoked (satisfies OR-group)
        assert exit_code == 0

    def test_should_allow_transition_when_both_or_members_invoked(self, tmp_path):
        """
        Given: OR-group ["backend-architect", "frontend-developer"] with BOTH invoked
        When: phase_check_command checks the transition
        Then: Returns exit code 0 (all requirements satisfied)
        """
        state = {
            "story_id": "STORY-903",
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
                        "frontend-developer",
                        "context-validator",
                    ],
                },
            }),
            "validation_errors": [],
            "observations": [],
        }

        _write_state(tmp_path, "STORY-903", state)

        exit_code = phase_check_command(
            story_id="STORY-903",
            from_phase="03",
            to_phase="04",
            project_root=str(tmp_path),
            format="text",
        )

        assert exit_code == 0, (
            f"Expected exit code 0 but got {exit_code}. "
            "OR-group with both members invoked should be satisfied."
        )

    def test_should_allow_transition_when_second_or_member_invoked(self, tmp_path):
        """
        Given: OR-group ["backend-architect", "frontend-developer"]
               with only "frontend-developer" invoked (the second member)
        When: phase_check_command checks the transition
        Then: Returns exit code 0 (OR-group satisfied by second member)
        """
        state = {
            "story_id": "STORY-904",
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
                    "subagents_invoked": ["frontend-developer", "context-validator"],
                },
            }),
            "validation_errors": [],
            "observations": [],
        }

        _write_state(tmp_path, "STORY-904", state)

        exit_code = phase_check_command(
            story_id="STORY-904",
            from_phase="03",
            to_phase="04",
            project_root=str(tmp_path),
            format="text",
        )

        assert exit_code == 0, (
            f"Expected exit code 0 but got {exit_code}. "
            "OR-group satisfied by second member (frontend-developer)."
        )

    def test_should_handle_multiple_or_groups(self, tmp_path):
        """
        Given: Multiple OR-groups in subagents_required, all satisfied
        When: phase_check_command checks the transition
        Then: Returns exit code 0
        """
        state = {
            "story_id": "STORY-905",
            "current_phase": "04",
            "workflow_started": "2026-02-21T00:00:00Z",
            "blocking_status": False,
            "phases": _all_phases_dict({
                "03": {
                    "status": "completed",
                    "subagents_required": [
                        ["backend-architect", "frontend-developer"],
                        ["code-reviewer", "refactoring-specialist"],
                        "context-validator"
                    ],
                    "subagents_invoked": [
                        "backend-architect",
                        "code-reviewer",
                        "context-validator",
                    ],
                },
            }),
            "validation_errors": [],
            "observations": [],
        }

        _write_state(tmp_path, "STORY-905", state)

        exit_code = phase_check_command(
            story_id="STORY-905",
            from_phase="03",
            to_phase="04",
            project_root=str(tmp_path),
            format="text",
        )

        assert exit_code == 0, (
            f"Expected exit code 0 but got {exit_code}. "
            "Multiple OR-groups all satisfied should allow transition."
        )

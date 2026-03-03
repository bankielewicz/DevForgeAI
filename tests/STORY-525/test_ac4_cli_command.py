"""
Test: AC#4 - phase-record-step CLI Command Records Step via Command Line
Story: STORY-525
Generated: 2026-03-02

Tests FAIL initially because phase_record_step_command() does not exist.
"""

import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

SRC_ROOT = Path(__file__).resolve().parents[2] / "src" / "claude" / "scripts"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))


class TestPhaseRecordStepCommandExists:
    """phase_record_step_command function must exist."""

    def test_command_function_exists(self):
        """Arrange: Import module. Act: Check attribute. Assert: callable exists."""
        from devforgeai_cli.commands.phase_commands import phase_record_step_command
        assert callable(phase_record_step_command)


class TestPhaseRecordStepValidInput:
    """Valid input exits 0 and updates state file."""

    def test_valid_input_exits_0(self, initialized_state, registry_with_file):
        """Arrange: Valid state + registry. Act: Call command. Assert: exit code 0."""
        from devforgeai_cli.commands.phase_commands import phase_record_step_command
        ps = initialized_state

        exit_code = phase_record_step_command(
            story_id="STORY-525",
            phase="02",
            step_id="02.2",
            project_root=str(ps.project_root),
        )
        assert exit_code == 0

    def test_valid_input_updates_state_file(self, initialized_state, registry_with_file):
        """Arrange: Valid state + registry. Act: Call command. Assert: step in state."""
        from devforgeai_cli.commands.phase_commands import phase_record_step_command
        ps = initialized_state

        phase_record_step_command(
            story_id="STORY-525",
            phase="02",
            step_id="02.2",
            project_root=str(ps.project_root),
        )

        state = ps.read("STORY-525")
        assert "02.2" in state["phases"]["02"]["steps_completed"]

    def test_valid_input_idempotent(self, initialized_state, registry_with_file):
        """Arrange: Call twice. Act: Read state. Assert: step appears once."""
        from devforgeai_cli.commands.phase_commands import phase_record_step_command
        ps = initialized_state

        phase_record_step_command("STORY-525", "02", "02.2", str(ps.project_root))
        phase_record_step_command("STORY-525", "02", "02.2", str(ps.project_root))

        state = ps.read("STORY-525")
        assert state["phases"]["02"]["steps_completed"].count("02.2") == 1


class TestPhaseRecordStepInvalidStoryId:
    """Invalid story ID exits 1."""

    def test_invalid_story_id_exits_1(self, project_root):
        """Arrange: Invalid story ID. Act: Call command. Assert: exit code 1."""
        from devforgeai_cli.commands.phase_commands import phase_record_step_command

        exit_code = phase_record_step_command(
            story_id="INVALID",
            phase="02",
            step_id="02.2",
            project_root=str(project_root),
        )
        assert exit_code == 1


class TestPhaseRecordStepUnknownStepId:
    """Unknown step ID exits 1 with informative stderr."""

    def test_unknown_step_id_exits_1(self, initialized_state, registry_with_file, capsys):
        """Arrange: Unknown step ID. Act: Call command. Assert: exit 1 + error message."""
        from devforgeai_cli.commands.phase_commands import phase_record_step_command
        ps = initialized_state

        exit_code = phase_record_step_command(
            story_id="STORY-525",
            phase="02",
            step_id="02.99",  # Not in registry
            project_root=str(ps.project_root),
        )
        assert exit_code == 1

        captured = capsys.readouterr()
        # Error message should mention the unknown step
        assert "02.99" in captured.err or "02.99" in captured.out

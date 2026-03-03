"""
Test: AC#3 - Command Files Updated
Story: STORY-442
Generated: 2026-02-18

Validates that /brainstorm command invokes Skill(command="brainstorming")
and no command files reference devforgeai-brainstorming.
"""
import os
import glob
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


class TestAC3CommandsUpdated:
    """AC#3: Command files updated to reference brainstorming skill."""

    BRAINSTORM_CMD = os.path.join(
        PROJECT_ROOT, "src", "claude", "commands", "brainstorm.md"
    )
    COMMANDS_DIR = os.path.join(PROJECT_ROOT, "src", "claude", "commands")

    def test_should_invoke_brainstorming_skill_when_command_executed(self):
        """brainstorm.md contains Skill(command="brainstorming")."""
        assert os.path.isfile(self.BRAINSTORM_CMD), (
            f"brainstorm.md not found at {self.BRAINSTORM_CMD}"
        )
        with open(self.BRAINSTORM_CMD, "r", encoding="utf-8") as f:
            content = f.read()
        assert 'Skill(command="brainstorming")' in content or "Skill(command='brainstorming')" in content, (
            "Expected Skill(command=\"brainstorming\") in brainstorm.md"
        )

    def test_should_not_reference_old_skill_name_in_brainstorm_command(self):
        """brainstorm.md does not contain devforgeai-brainstorming."""
        assert os.path.isfile(self.BRAINSTORM_CMD)
        with open(self.BRAINSTORM_CMD, "r", encoding="utf-8") as f:
            content = f.read()
        assert "devforgeai-brainstorming" not in content, (
            "Old reference 'devforgeai-brainstorming' found in brainstorm.md"
        )

    def test_should_not_reference_old_skill_name_in_any_command(self):
        """No command file contains devforgeai-brainstorming."""
        cmd_files = glob.glob(os.path.join(self.COMMANDS_DIR, "*.md"))
        violations = []
        for cmd_file in cmd_files:
            with open(cmd_file, "r", encoding="utf-8") as f:
                if "devforgeai-brainstorming" in f.read():
                    violations.append(os.path.basename(cmd_file))
        assert not violations, (
            f"Commands still referencing devforgeai-brainstorming: {violations}"
        )

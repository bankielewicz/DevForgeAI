"""
Test: AC#1 - Command Invocation & Skill Delegation
Story: STORY-541
Generated: 2026-03-05

Validates:
- Command file exists at src/claude/commands/marketing-plan.md
- Command file < 500 lines (BR-001)
- No workflow logic (no if/else/conditional) in command
- Contains skill delegation to marketing-business
- Presents 4 workflow menu options
"""
import os
import re

import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
COMMAND_FILE = os.path.join(PROJECT_ROOT, "src", "claude", "commands", "marketing-plan.md")


@pytest.fixture
def command_content():
    """Arrange: Read command file content."""
    assert os.path.isfile(COMMAND_FILE), f"Command file not found: {COMMAND_FILE}"
    with open(COMMAND_FILE, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def command_lines(command_content):
    """Arrange: Split command file into lines."""
    return command_content.splitlines()


class TestCommandFileExists:
    """Tests for command file existence."""

    def test_should_exist_at_expected_path(self):
        """Act & Assert: Command file must exist at src/claude/commands/marketing-plan.md."""
        assert os.path.isfile(COMMAND_FILE), (
            f"Expected command file at {COMMAND_FILE}"
        )


class TestCommandFileSizeLimit:
    """Tests for BR-001: Command file < 500 lines."""

    def test_should_be_under_500_lines(self, command_lines):
        """Act & Assert: Command file must be under 500 lines per BR-001."""
        line_count = len(command_lines)
        assert line_count < 500, (
            f"Command file has {line_count} lines, exceeds 500 line limit (BR-001)"
        )


class TestNoWorkflowLogic:
    """Tests for BR-001: No conditional/workflow logic in command."""

    def test_should_not_contain_if_else_blocks(self, command_content):
        """Act & Assert: Command must not contain if/else workflow logic."""
        # Match markdown-fenced code patterns for if/else that indicate workflow logic
        # Allow if/else inside code examples but not as top-level command logic
        conditional_patterns = [
            r"^IF\s+",
            r"^ELSE\s*:",
            r"^ELIF\s+",
            r"^if\s*\(",
            r"^else\s*\{",
        ]
        for pattern in conditional_patterns:
            matches = re.findall(pattern, command_content, re.MULTILINE)
            assert len(matches) == 0, (
                f"Command contains workflow logic matching '{pattern}' (BR-001). "
                f"Command must be thin invoker only."
            )

    def test_should_not_contain_loop_constructs(self, command_content):
        """Act & Assert: Command must not contain loop workflow logic."""
        loop_patterns = [
            r"^FOR\s+",
            r"^WHILE\s+",
            r"^for\s*\(",
            r"^while\s*\(",
        ]
        for pattern in loop_patterns:
            matches = re.findall(pattern, command_content, re.MULTILINE)
            assert len(matches) == 0, (
                f"Command contains loop logic matching '{pattern}' (BR-001). "
                f"Command must be thin invoker only."
            )


class TestSkillDelegation:
    """Tests for skill delegation to marketing-business."""

    def test_should_delegate_to_marketing_business_skill(self, command_content):
        """Act & Assert: Command must reference marketing-business skill."""
        assert "marketing-business" in command_content, (
            "Command file must delegate to 'marketing-business' skill"
        )

    def test_should_contain_skill_invocation_pattern(self, command_content):
        """Act & Assert: Command must contain a skill invocation pattern."""
        # Look for skill invocation syntax
        has_skill_ref = (
            "Skill(" in command_content
            or "skill:" in command_content.lower()
            or "skill_invocation" in command_content
            or "invoke" in command_content.lower()
        )
        assert has_skill_ref, (
            "Command file must contain skill invocation/delegation pattern"
        )


class TestWorkflowMenuOptions:
    """Tests for 4 workflow menu options."""

    EXPECTED_OPTIONS = [
        "Go-to-Market Strategy",
        "Positioning",
        "Customer Discovery",
        "Content Strategy",
    ]

    @pytest.mark.parametrize("option", EXPECTED_OPTIONS)
    def test_should_present_menu_option(self, command_content, option):
        """Act & Assert: Command or skill must present each menu option."""
        assert option.lower() in command_content.lower(), (
            f"Command file must present menu option: '{option}'"
        )

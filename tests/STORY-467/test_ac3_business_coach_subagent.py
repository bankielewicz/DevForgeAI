"""
Test: AC#3 - Business-Coach Subagent
Story: STORY-467 - Dynamic Persona Blend Engine
Generated: 2026-03-04

Validates:
- business-coach.md exists at src/claude/agents/business-coach.md
- Valid YAML frontmatter with name: business-coach
- Tools restricted to Read, Grep, Glob, AskUserQuestion
- Under 500 lines
- Contains persona blend instructions
"""
import os
import re

import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AGENT_PATH = os.path.join(PROJECT_ROOT, "src", "claude", "agents", "business-coach.md")


@pytest.fixture
def agent_content():
    """Read the business-coach.md file content."""
    assert os.path.isfile(AGENT_PATH), f"business-coach.md not found at {AGENT_PATH}"
    with open(AGENT_PATH, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def agent_lines(agent_content):
    """Return business-coach.md as list of lines."""
    return agent_content.splitlines()


@pytest.fixture
def frontmatter(agent_content):
    """Extract YAML frontmatter from business-coach.md."""
    match = re.match(r"^---\s*\n(.*?)\n---", agent_content, re.DOTALL)
    assert match is not None, "business-coach.md must have YAML frontmatter delimited by ---"
    return match.group(1)


class TestAgentFileExists:
    """Verify business-coach.md exists at the correct path."""

    def test_agent_file_exists(self):
        assert os.path.isfile(AGENT_PATH), (
            f"business-coach.md must exist at {AGENT_PATH}"
        )


class TestYamlFrontmatter:
    """Verify business-coach.md has valid YAML frontmatter."""

    def test_frontmatter_contains_name(self, frontmatter):
        """Frontmatter must contain name: business-coach."""
        assert re.search(r"^name:\s*business-coach\s*$", frontmatter, re.MULTILINE), (
            "Frontmatter must contain 'name: business-coach'"
        )


class TestToolRestriction:
    """Verify tools are restricted to Read, Grep, Glob, AskUserQuestion."""

    def test_tools_field_exists(self, frontmatter):
        """Frontmatter must contain a tools field."""
        assert re.search(r"^tools:", frontmatter, re.MULTILINE), (
            "Frontmatter must contain a 'tools:' field"
        )

    def test_tools_contains_read(self, frontmatter):
        """Tools must include Read."""
        tools_match = re.search(r"^tools:\s*(.+)$", frontmatter, re.MULTILINE)
        assert tools_match, "tools field not found"
        tools = tools_match.group(1)
        assert "Read" in tools, f"Tools must include Read, got: {tools}"

    def test_tools_contains_grep(self, frontmatter):
        """Tools must include Grep."""
        tools_match = re.search(r"^tools:\s*(.+)$", frontmatter, re.MULTILINE)
        tools = tools_match.group(1)
        assert "Grep" in tools, f"Tools must include Grep, got: {tools}"

    def test_tools_contains_glob(self, frontmatter):
        """Tools must include Glob."""
        tools_match = re.search(r"^tools:\s*(.+)$", frontmatter, re.MULTILINE)
        tools = tools_match.group(1)
        assert "Glob" in tools, f"Tools must include Glob, got: {tools}"

    def test_tools_contains_askuserquestion(self, frontmatter):
        """Tools must include AskUserQuestion."""
        tools_match = re.search(r"^tools:\s*(.+)$", frontmatter, re.MULTILINE)
        tools = tools_match.group(1)
        assert "AskUserQuestion" in tools, f"Tools must include AskUserQuestion, got: {tools}"

    def test_tools_excludes_write(self, frontmatter):
        """Tools must NOT include Write (read-only subagent)."""
        tools_match = re.search(r"^tools:\s*(.+)$", frontmatter, re.MULTILINE)
        tools = tools_match.group(1)
        assert "Write" not in tools, f"Tools must NOT include Write, got: {tools}"

    def test_tools_excludes_edit(self, frontmatter):
        """Tools must NOT include Edit (read-only subagent)."""
        tools_match = re.search(r"^tools:\s*(.+)$", frontmatter, re.MULTILINE)
        tools = tools_match.group(1)
        assert "Edit" not in tools, f"Tools must NOT include Edit, got: {tools}"

    def test_tools_exactly_four(self, frontmatter):
        """Tools must be exactly: Read, Grep, Glob, AskUserQuestion."""
        tools_match = re.search(r"^tools:\s*(.+)$", frontmatter, re.MULTILINE)
        tools = tools_match.group(1)
        tool_list = [t.strip() for t in tools.split(",")]
        expected = {"Read", "Grep", "Glob", "AskUserQuestion"}
        assert set(tool_list) == expected, (
            f"Tools must be exactly {expected}, got: {set(tool_list)}"
        )


class TestLineCount:
    """Verify business-coach.md is under 500 lines."""

    def test_under_500_lines(self, agent_lines):
        line_count = len(agent_lines)
        assert line_count < 500, (
            f"business-coach.md must be under 500 lines, found {line_count}"
        )


class TestPersonaBlendInstructions:
    """Verify business-coach.md contains persona blend instructions."""

    def test_contains_persona_blend(self, agent_content):
        """business-coach.md must contain persona blend instructions."""
        assert re.search(r"(?i)persona\s+blend", agent_content), (
            "business-coach.md must contain persona blend instructions"
        )

    def test_references_coach_mode(self, agent_content):
        """business-coach.md must reference Coach mode."""
        assert re.search(r"(?i)coach\s+mode", agent_content), (
            "business-coach.md must reference Coach mode"
        )

    def test_references_consultant_mode(self, agent_content):
        """business-coach.md must reference Consultant mode."""
        assert re.search(r"(?i)consultant\s+mode", agent_content), (
            "business-coach.md must reference Consultant mode"
        )

"""AC#1: Market-Analyst Subagent Structure
Story: STORY-536
Tests that src/claude/agents/market-analyst.md exists with valid structure.
"""
import os
import re
import pytest


class TestSubagentFileExists:
    """Verify market-analyst.md exists at correct path."""

    def test_file_exists_at_src_path(self, subagent_path):
        # Arrange: path from fixture
        # Act & Assert
        assert os.path.isfile(subagent_path), (
            f"market-analyst.md not found at {subagent_path}"
        )


class TestSubagentYAMLFrontmatter:
    """Verify valid YAML frontmatter with required fields."""

    def test_has_yaml_frontmatter_delimiters(self, subagent_content):
        # Arrange
        assert subagent_content, "File is empty or missing"
        # Act
        lines = subagent_content.split("\n")
        # Assert: starts with --- and has closing ---
        assert lines[0].strip() == "---", "File must start with YAML frontmatter delimiter '---'"
        closing_idx = None
        for i, line in enumerate(lines[1:], start=1):
            if line.strip() == "---":
                closing_idx = i
                break
        assert closing_idx is not None, "Missing closing YAML frontmatter delimiter '---'"

    def test_frontmatter_contains_name(self, subagent_content):
        # Arrange
        frontmatter = _extract_frontmatter(subagent_content)
        # Assert
        assert re.search(r"^name:", frontmatter, re.MULTILINE), (
            "YAML frontmatter missing 'name' field"
        )

    def test_frontmatter_contains_description(self, subagent_content):
        frontmatter = _extract_frontmatter(subagent_content)
        assert re.search(r"^description:", frontmatter, re.MULTILINE), (
            "YAML frontmatter missing 'description' field"
        )

    def test_frontmatter_contains_tools(self, subagent_content):
        frontmatter = _extract_frontmatter(subagent_content)
        assert re.search(r"^tools:", frontmatter, re.MULTILINE), (
            "YAML frontmatter missing 'tools' field"
        )

    def test_frontmatter_contains_allowed_tools(self, subagent_content):
        frontmatter = _extract_frontmatter(subagent_content)
        assert re.search(r"^allowed_tools:", frontmatter, re.MULTILINE), (
            "YAML frontmatter missing 'allowed_tools' field"
        )


class TestSubagentLineLimit:
    """Verify file is under 500 lines."""

    def test_under_500_lines(self, subagent_content):
        assert subagent_content, "File is empty or missing"
        line_count = len(subagent_content.split("\n"))
        assert line_count < 500, f"Subagent has {line_count} lines, must be under 500"


class TestSubagentNoInvocationPatterns:
    """Verify no skill/command invocation patterns."""

    def test_no_skill_invocation(self, subagent_content):
        assert subagent_content, "File is empty or missing"
        assert not re.search(r"Skill\s*\(", subagent_content), (
            "Subagent must not contain Skill() invocation patterns"
        )

    def test_no_slash_command_invocation(self, subagent_content):
        assert subagent_content, "File is empty or missing"
        # Match /command-name patterns (slash commands)
        assert not re.search(r"(?m)^[^#]*`?/[a-z]+-[a-z]+", subagent_content), (
            "Subagent must not contain /command invocation patterns"
        )


def _extract_frontmatter(content: str) -> str:
    """Extract YAML frontmatter between --- delimiters."""
    if not content:
        return ""
    lines = content.split("\n")
    if lines[0].strip() != "---":
        return ""
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return "\n".join(lines[1:i])
    return ""

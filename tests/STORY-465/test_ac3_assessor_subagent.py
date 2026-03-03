"""Test AC#3: Entrepreneur-Assessor Subagent.

Story: STORY-465
Validates that the entrepreneur-assessor subagent file exists with valid
YAML frontmatter and restricted tool set.
"""
import pytest
from pathlib import Path
from conftest import parse_yaml_frontmatter


ALLOWED_TOOLS = {"Read", "Glob", "Grep", "AskUserQuestion"}


class TestSubagentFileExists:
    """Tests for subagent file existence."""

    def test_should_exist_at_correct_path(self, subagent_file):
        """entrepreneur-assessor.md must exist at src/claude/agents/."""
        assert subagent_file.exists(), (
            f"Subagent file not found at {subagent_file}. "
            "The entrepreneur-assessor subagent must be created."
        )

    def test_should_be_a_file(self, subagent_file):
        """Must be a regular file."""
        assert subagent_file.is_file(), (
            f"{subagent_file} exists but is not a regular file."
        )


class TestSubagentFrontmatter:
    """Tests for subagent YAML frontmatter."""

    def test_should_have_yaml_frontmatter(self, subagent_file):
        """Subagent file must have valid YAML frontmatter."""
        content = subagent_file.read_text(encoding="utf-8")
        assert content.startswith("---"), (
            "Subagent file must begin with YAML frontmatter (--- delimiter)."
        )

    def test_should_have_name_field(self, subagent_file):
        """Frontmatter must contain a 'name' field."""
        fm = parse_yaml_frontmatter(subagent_file)
        assert "name" in fm, "Subagent frontmatter missing required 'name' field."

    def test_should_have_tools_field(self, subagent_file):
        """Frontmatter must contain a 'tools' field."""
        fm = parse_yaml_frontmatter(subagent_file)
        assert "tools" in fm, "Subagent frontmatter missing required 'tools' field."

    def test_should_have_tools_restricted_to_allowed_set(self, subagent_file):
        """Tools must be restricted to: Read, Glob, Grep, AskUserQuestion."""
        fm = parse_yaml_frontmatter(subagent_file)
        tools_raw = fm.get("tools", "")

        # Tools may be a list or comma-separated string
        if isinstance(tools_raw, list):
            tools = {t.strip() for t in tools_raw}
        else:
            tools = {t.strip() for t in str(tools_raw).split(",")}

        unexpected = tools - ALLOWED_TOOLS
        assert len(unexpected) == 0, (
            f"Subagent has unauthorized tools: {unexpected}. "
            f"Allowed tools: {ALLOWED_TOOLS}"
        )

        missing = ALLOWED_TOOLS - tools
        assert len(missing) == 0, (
            f"Subagent missing required tools: {missing}. "
            f"All of {ALLOWED_TOOLS} must be listed."
        )


class TestSubagentFileSize:
    """Tests for subagent size constraints."""

    def test_should_be_under_500_lines(self, subagent_file):
        """Subagent file must be under 500 lines."""
        content = subagent_file.read_text(encoding="utf-8")
        line_count = len(content.splitlines())
        assert line_count < 500, (
            f"Subagent file has {line_count} lines, exceeds 500 line limit."
        )

    def test_should_be_non_empty(self, subagent_file):
        """Subagent file must contain substantive content."""
        content = subagent_file.read_text(encoding="utf-8")
        assert len(content.strip()) > 50, (
            "Subagent file appears empty or contains only minimal content."
        )

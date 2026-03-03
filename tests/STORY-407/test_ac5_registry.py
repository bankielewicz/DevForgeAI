"""
Test: AC#5 - CLAUDE.md Registry Updated with dead-code-detector Entry
Story: STORY-407
Generated: 2026-02-16

Validates that CLAUDE.md subagent registry table includes dead-code-detector
entry with description, tools, and proactive triggers.
"""
import os
import re
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CLAUDE_MD_PATH = os.path.join(PROJECT_ROOT, "CLAUDE.md")


@pytest.fixture(scope="module")
def claude_content():
    """Read CLAUDE.md content."""
    assert os.path.isfile(CLAUDE_MD_PATH), f"CLAUDE.md not found at {CLAUDE_MD_PATH}"
    with open(CLAUDE_MD_PATH, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture(scope="module")
def registry_section(claude_content):
    """Extract subagent registry section."""
    pattern = r"(?s)<!-- BEGIN SUBAGENT REGISTRY -->.*?<!-- END SUBAGENT REGISTRY -->"
    match = re.search(pattern, claude_content)
    assert match, "Subagent registry section not found in CLAUDE.md"
    return match.group(0)


class TestDeadCodeDetectorEntry:
    """Tests for dead-code-detector registry entry."""

    def test_should_have_dead_code_detector_in_registry_table(self, registry_section):
        """Assert: Registry table contains dead-code-detector row."""
        assert "dead-code-detector" in registry_section, (
            "Registry should contain dead-code-detector entry"
        )

    def test_should_have_description(self, registry_section):
        """Assert: dead-code-detector entry has a description."""
        # Find the table row for dead-code-detector
        pattern = r"\|\s*dead-code-detector\s*\|([^|]+)\|"
        match = re.search(pattern, registry_section)
        assert match, "dead-code-detector row not found in registry table"
        description = match.group(1).strip()
        assert len(description) > 10, (
            f"dead-code-detector description too short: '{description}'"
        )

    def test_should_have_tools_listed(self, registry_section):
        """Assert: dead-code-detector entry lists tools."""
        # Find the row and check tools column
        lines = registry_section.split("\n")
        detector_line = None
        for line in lines:
            if "dead-code-detector" in line and "|" in line:
                detector_line = line
                break
        assert detector_line, "dead-code-detector row not found"
        # Tools should include Read, Bash(treelint:*), Grep, Glob
        assert "Read" in detector_line, "Tools should include Read"
        assert "Grep" in detector_line, "Tools should include Grep"
        assert "Glob" in detector_line, "Tools should include Glob"

    def test_should_have_treelint_bash_tool(self, registry_section):
        """Assert: dead-code-detector lists Bash(treelint:*) tool."""
        lines = registry_section.split("\n")
        detector_line = None
        for line in lines:
            if "dead-code-detector" in line and "|" in line:
                detector_line = line
                break
        assert detector_line, "dead-code-detector row not found"
        assert re.search(r"Bash\(treelint", detector_line), (
            "Tools should include Bash(treelint:*)"
        )


class TestProactiveTriggers:
    """Tests for dead-code-detector proactive triggers in registry."""

    def test_should_have_proactive_trigger_entry(self, registry_section):
        """Assert: Proactive trigger mapping includes dead-code-detector."""
        # Check the trigger mapping table
        assert re.search(
            r"dead-code-detector.*\|", registry_section
        ), "Proactive trigger mapping should reference dead-code-detector"

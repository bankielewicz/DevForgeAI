"""
Test: AC#6 - Read-Only Constraint (ADR-016)
Story: STORY-403
Generated: 2026-02-14

Validates that the dead-code-detector subagent uses ONLY read-only tools:
Read, Bash(treelint:*), Grep, Glob -- NO Write/Edit tools.

These tests MUST FAIL initially (TDD Red phase).
"""
import re
import pytest


class TestReadOnlyConstraint:
    """Verify ADR-016 read-only tool constraint."""

    def test_should_include_read_tool_in_tools_list(
        self, subagent_content
    ):
        """AC#6: Read tool must be in the tools list."""
        content = subagent_content
        assert re.search(
            r"(?i)\bread\b", content
        ), "Read tool not found in tools list"

    def test_should_include_grep_tool_in_tools_list(
        self, subagent_content
    ):
        """AC#6: Grep tool must be in the tools list."""
        content = subagent_content
        assert re.search(
            r"(?i)\bgrep\b", content
        ), "Grep tool not found in tools list"

    def test_should_include_glob_tool_in_tools_list(
        self, subagent_content
    ):
        """AC#6: Glob tool must be in the tools list."""
        content = subagent_content
        assert re.search(
            r"(?i)\bglob\b", content
        ), "Glob tool not found in tools list"

    def test_should_include_bash_treelint_in_tools_list(
        self, subagent_content
    ):
        """AC#6: Bash(treelint:*) must be in the tools list."""
        content = subagent_content
        assert re.search(
            r"(?i)bash\s*\(\s*treelint", content
        ), "Bash(treelint:*) not found in tools list"

    def test_should_not_include_write_tool_in_tools_list(
        self, subagent_content
    ):
        """AC#6: Write tool must NOT be in the tools list (read-only)."""
        content = subagent_content
        # Look for tools section and check for Write
        tools_section = _extract_tools_section(content)
        assert tools_section is not None, "Tools section not found in subagent"
        assert not re.search(
            r"(?i)\bwrite\b", tools_section
        ), "Write tool found in tools list -- violates ADR-016 read-only constraint"

    def test_should_not_include_edit_tool_in_tools_list(
        self, subagent_content
    ):
        """AC#6: Edit tool must NOT be in the tools list (read-only)."""
        content = subagent_content
        tools_section = _extract_tools_section(content)
        assert tools_section is not None, "Tools section not found in subagent"
        assert not re.search(
            r"(?i)\bedit\b", tools_section
        ), "Edit tool found in tools list -- violates ADR-016 read-only constraint"

    def test_should_reference_adr_016_in_subagent(
        self, subagent_content
    ):
        """AC#6: Subagent must reference ADR-016 for read-only rationale."""
        content = subagent_content
        assert re.search(
            r"(?i)ADR-016", content
        ), "ADR-016 reference not found in subagent definition"

    def test_should_have_adr_016_document_created(
        self, adr_016_content
    ):
        """AC#6: ADR-016 document must exist with read-only decision."""
        content = adr_016_content
        assert re.search(
            r"(?i)read.only", content
        ), "ADR-016 does not contain read-only decision"
        assert re.search(
            r"(?i)dead.code.detector", content
        ), "ADR-016 does not reference dead-code-detector"


def _extract_tools_section(content: str) -> str | None:
    """Extract the tools section from subagent YAML frontmatter or markdown."""
    # Try YAML frontmatter tools: line
    match = re.search(
        r"(?i)^tools\s*:.*$(?:\n\s*-.*$)*", content, re.MULTILINE
    )
    if match:
        return match.group(0)

    # Try markdown tools section
    match = re.search(
        r"(?i)^#+\s*tool.*$\n((?:.*\n)*?)(?=^#+|\Z)", content, re.MULTILINE
    )
    if match:
        return match.group(0)

    # Fallback: look for tool restrictions section
    match = re.search(
        r"(?i)(tool\s*restriction|allowed\s*tool).*(?:\n.*){0,10}",
        content,
        re.MULTILINE,
    )
    if match:
        return match.group(0)

    return None

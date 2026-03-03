"""
Test: AC#10 - Registry Entry in CLAUDE.md
Story: STORY-403
Generated: 2026-02-14

Validates that the src/CLAUDE.md subagent registry table includes
dead-code-detector with description, tools, and proactive triggers.

These tests MUST FAIL initially (TDD Red phase).
"""
import re
import pytest


class TestRegistryEntry:
    """Verify CLAUDE.md registry includes dead-code-detector."""

    def test_should_include_dead_code_detector_in_registry_table(
        self, claude_md_content
    ):
        """AC#10: dead-code-detector must appear in subagent registry table."""
        content = claude_md_content
        assert re.search(
            r"(?i)dead-code-detector", content
        ), "dead-code-detector not found in CLAUDE.md subagent registry"

    def test_should_include_description_in_registry_entry(
        self, claude_md_content
    ):
        """AC#10: Registry entry must include a description."""
        content = claude_md_content
        # Find the dead-code-detector row in the table
        # Table format: | agent | description | tools |
        match = re.search(
            r"(?i)\|\s*dead-code-detector\s*\|([^|]+)\|", content
        )
        assert match, "dead-code-detector row not found in registry table"
        description = match.group(1).strip()
        assert len(description) > 10, (
            f"Description too short: '{description}'. Expected meaningful description."
        )

    def test_should_include_tools_in_registry_entry(
        self, claude_md_content
    ):
        """AC#10: Registry entry must include tools list."""
        content = claude_md_content
        # Find the row and extract tools column
        match = re.search(
            r"(?i)\|\s*dead-code-detector\s*\|[^|]+\|([^|]+)\|", content
        )
        assert match, "dead-code-detector tools column not found in registry table"
        tools = match.group(1).strip()
        assert len(tools) > 0, "Tools column is empty"

    def test_should_include_read_only_tools_in_registry(
        self, claude_md_content
    ):
        """AC#10: Registry tools must reflect read-only constraint (Read, Grep, Glob, Bash(treelint:*))."""
        content = claude_md_content
        match = re.search(
            r"(?i)\|\s*dead-code-detector\s*\|[^|]+\|([^|]+)\|", content
        )
        assert match, "dead-code-detector tools column not found"
        tools = match.group(1).strip()
        # Verify no Write/Edit in tools
        assert not re.search(
            r"(?i)\bwrite\b", tools
        ), "Write tool found in registry -- violates read-only constraint"
        assert not re.search(
            r"(?i)\bedit\b", tools
        ), "Edit tool found in registry -- violates read-only constraint"

    def test_should_include_proactive_triggers_in_registry(
        self, claude_md_content
    ):
        """AC#10: dead-code-detector must have proactive trigger entries."""
        content = claude_md_content
        # Proactive triggers are in the trigger mapping table
        assert re.search(
            r"(?i)dead-code-detector", content
        ), "dead-code-detector not in proactive trigger mapping"
        # Check for at least one trigger pattern mentioning dead-code-detector
        trigger_match = re.search(
            r"(?i)\|[^|]*\|\s*dead-code-detector\s*\|", content
        )
        assert trigger_match, (
            "No proactive trigger row found for dead-code-detector in trigger mapping table"
        )

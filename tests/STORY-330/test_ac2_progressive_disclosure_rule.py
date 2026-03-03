"""
STORY-330 AC#2: Add Progressive Disclosure Pattern for Subagents

Given: tech-stack.md lines 355-358 prescribe progressive disclosure
When: source-tree.md .claude/agents/ section is updated
Then: new rule specifying "references/ subdirectory ALLOWED for subagents exceeding 500 lines"
"""
import pytest
import re
from pathlib import Path

SOURCE_TREE_PATH = Path(__file__).parent.parent.parent / "devforgeai/specs/context/source-tree.md"


def test_progressive_disclosure_rule_added():
    """Verify progressive disclosure rule for >500 line subagents exists."""
    content = SOURCE_TREE_PATH.read_text()

    agents_section_match = re.search(
        r"### `\.claude/agents/`.*?(?=###|\Z)",
        content,
        re.DOTALL
    )
    assert agents_section_match, "Could not find .claude/agents/ section"
    agents_section = agents_section_match.group()

    # FAIL: Should have rule mentioning progressive disclosure
    assert "progressive disclosure" in agents_section.lower(), (
        "Progressive disclosure rule not found in .claude/agents/ section"
    )


def test_exceeding_500_lines_threshold():
    """Verify threshold is '>500' (strictly greater than)."""
    content = SOURCE_TREE_PATH.read_text()

    agents_section_match = re.search(
        r"### `\.claude/agents/`.*?(?=###|\Z)",
        content,
        re.DOTALL
    )
    assert agents_section_match, "Could not find .claude/agents/ section"
    agents_section = agents_section_match.group()

    # FAIL: Should specify "exceeding 500 lines" or ">500 lines"
    has_threshold = (
        re.search(r"exceed(ing|s)?\s+500\s*lines", agents_section, re.IGNORECASE) or
        re.search(r">\s*500\s*lines", agents_section)
    )
    assert has_threshold, (
        "Threshold '>500 lines' not specified in .claude/agents/ section"
    )


def test_references_subdirectory_allowed():
    """Verify references/ subdirectory is explicitly ALLOWED."""
    content = SOURCE_TREE_PATH.read_text()

    agents_section_match = re.search(
        r"### `\.claude/agents/`.*?(?=###|\Z)",
        content,
        re.DOTALL
    )
    assert agents_section_match, "Could not find .claude/agents/ section"
    agents_section = agents_section_match.group()

    # FAIL: Should have "references/ ... ALLOWED" or similar
    assert re.search(r"references/.*allowed|allowed.*references/", agents_section, re.IGNORECASE), (
        "references/ subdirectory not marked as ALLOWED"
    )

"""
STORY-330 AC#1: Remove Prohibition on Subagent Subdirectories

Given: source-tree.md line 582 states "NO subdirectories in `.claude/agents/`"
When: constitutional update is applied
Then: blanket prohibition removed and replaced with conditional permission
"""
import pytest
import re
from pathlib import Path

SOURCE_TREE_PATH = Path(__file__).parent.parent.parent / "devforgeai/specs/context/source-tree.md"


def test_blanket_prohibition_removed():
    """Verify 'NO subdirectories in .claude/agents/' prohibition is removed."""
    content = SOURCE_TREE_PATH.read_text()

    # Extract .claude/agents/ section (lines ~572-621)
    agents_section_match = re.search(
        r"### `\.claude/agents/`.*?(?=###|\Z)",
        content,
        re.DOTALL
    )
    assert agents_section_match, "Could not find .claude/agents/ section"
    agents_section = agents_section_match.group()

    # FAIL: Blanket prohibition should NOT exist
    assert "NO subdirectories in `.claude/agents/`" not in agents_section, (
        "Blanket prohibition still present - should be replaced with conditional permission"
    )


def test_conditional_permission_exists():
    """Verify conditional permission for references/ subdirectory exists."""
    content = SOURCE_TREE_PATH.read_text()

    agents_section_match = re.search(
        r"### `\.claude/agents/`.*?(?=###|\Z)",
        content,
        re.DOTALL
    )
    assert agents_section_match, "Could not find .claude/agents/ section"
    agents_section = agents_section_match.group()

    # FAIL: Should have conditional permission mentioning 500 lines threshold
    assert re.search(r"references/.*500\s*lines|500\s*lines.*references/", agents_section, re.IGNORECASE), (
        "Conditional permission for references/ subdirectory not found"
    )

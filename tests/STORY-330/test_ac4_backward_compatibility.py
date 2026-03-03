"""
STORY-330 AC#4: Maintain Backward Compatibility

Given: 6 existing subagents are under 500 lines
When: source-tree.md update is applied
Then: rules state subagents under 500 lines remain as single .md files
"""
import pytest
import re
from pathlib import Path

SOURCE_TREE_PATH = Path(__file__).parent.parent.parent / "devforgeai/specs/context/source-tree.md"


def test_backward_compatibility_statement_exists():
    """Verify statement about subagents <=500 lines remaining single-file."""
    content = SOURCE_TREE_PATH.read_text()

    agents_section_match = re.search(
        r"### `\.claude/agents/`.*?(?=###|\Z)",
        content,
        re.DOTALL
    )
    assert agents_section_match, "Could not find .claude/agents/ section"
    agents_section = agents_section_match.group()

    # FAIL: Should have backward compatibility statement
    has_backward_compat = (
        re.search(r"under\s+500\s*lines?.*single.*\.md|<=?\s*500.*single|single.*file.*500",
                  agents_section, re.IGNORECASE) or
        re.search(r"500\s*lines?.*remain.*single|remain.*single.*500",
                  agents_section, re.IGNORECASE)
    )
    assert has_backward_compat, (
        "Backward compatibility statement for subagents <=500 lines not found"
    )


def test_single_file_pattern_preserved():
    """Verify single .md file pattern is still documented."""
    content = SOURCE_TREE_PATH.read_text()

    agents_section_match = re.search(
        r"### `\.claude/agents/`.*?(?=###|\Z)",
        content,
        re.DOTALL
    )
    assert agents_section_match, "Could not find .claude/agents/ section"
    agents_section = agents_section_match.group()

    # FAIL: Should still mention single .md file as valid pattern
    assert "single `.md` file" in agents_section or "single .md file" in agents_section.lower(), (
        "Single .md file pattern not documented in rules"
    )

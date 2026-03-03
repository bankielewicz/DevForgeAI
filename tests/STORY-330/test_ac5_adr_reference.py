"""
STORY-330 AC#5: Cross-Reference ADR-012

Given: ADR-012 is the authoritative decision record
When: source-tree.md is updated
Then: reference to ADR-012 is added in .claude/agents/ section
"""
import pytest
import re
from pathlib import Path

SOURCE_TREE_PATH = Path(__file__).parent.parent.parent / "devforgeai/specs/context/source-tree.md"


def test_adr_012_referenced_in_agents_section():
    """Verify ADR-012 is referenced in .claude/agents/ section."""
    content = SOURCE_TREE_PATH.read_text()

    agents_section_match = re.search(
        r"### `\.claude/agents/`.*?(?=###|\Z)",
        content,
        re.DOTALL
    )
    assert agents_section_match, "Could not find .claude/agents/ section"
    agents_section = agents_section_match.group()

    # FAIL: Should reference ADR-012
    assert "ADR-012" in agents_section, (
        "ADR-012 reference not found in .claude/agents/ section"
    )


def test_adr_reference_provides_context():
    """Verify ADR reference provides decision context."""
    content = SOURCE_TREE_PATH.read_text()

    agents_section_match = re.search(
        r"### `\.claude/agents/`.*?(?=###|\Z)",
        content,
        re.DOTALL
    )
    assert agents_section_match, "Could not find .claude/agents/ section"
    agents_section = agents_section_match.group()

    # FAIL: ADR reference should be near progressive disclosure mention
    adr_match = re.search(r"ADR-012", agents_section)
    disclosure_match = re.search(r"progressive\s+disclosure", agents_section, re.IGNORECASE)

    assert adr_match and disclosure_match, (
        "ADR-012 should be referenced alongside progressive disclosure rationale"
    )

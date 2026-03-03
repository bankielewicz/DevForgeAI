"""
STORY-330 AC#3: Document Directory Structure Pattern

Given: ADR-012 defines the approved directory pattern
When: source-tree.md is updated
Then: directory structure code block shows {subagent-name}/ containing references/
"""
import pytest
import re
from pathlib import Path

SOURCE_TREE_PATH = Path(__file__).parent.parent.parent / "devforgeai/specs/context/source-tree.md"


def test_directory_structure_example_exists():
    """Verify directory structure example with subagent + references/ pattern."""
    content = SOURCE_TREE_PATH.read_text()

    agents_section_match = re.search(
        r"### `\.claude/agents/`.*?(?=###|\Z)",
        content,
        re.DOTALL
    )
    assert agents_section_match, "Could not find .claude/agents/ section"
    agents_section = agents_section_match.group()

    # FAIL: Should have code block showing directory pattern
    # Pattern: {subagent-name}.md alongside {subagent-name}/references/
    has_example = (
        "references/" in agents_section and
        re.search(r"```[\s\S]*?\.md[\s\S]*?references/[\s\S]*?```", agents_section)
    )
    assert has_example, (
        "Directory structure example with {subagent}.md and {subagent}/references/ not found"
    )


def test_example_shows_coexistence_pattern():
    """Verify example shows .md file coexisting with directory."""
    content = SOURCE_TREE_PATH.read_text()

    agents_section_match = re.search(
        r"### `\.claude/agents/`.*?(?=###|\Z)",
        content,
        re.DOTALL
    )
    assert agents_section_match, "Could not find .claude/agents/ section"
    agents_section = agents_section_match.group()

    # FAIL: Should show pattern like:
    # test-automator.md
    # test-automator/
    #     references/
    # Allow up to 100 chars between .md and directory (comments may be included)
    # Allow up to 100 chars between directory and references/ (comments on same line)
    has_coexistence = re.search(
        r"(\w+-\w+)\.md[\s\S]{0,100}\1/[\s\S]{0,100}references/",
        agents_section
    )
    assert has_coexistence, (
        "Coexistence pattern ({name}.md + {name}/references/) not shown in example"
    )

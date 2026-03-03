"""
STORY-359 AC#5: Enforcement Checklist Updated

Tests that a new (10th) checklist item is added to the Enforcement Checklist
referencing code search tool selection, bringing the total from 9 to 10 items
while maintaining consistency with existing checklist format.

TDD Red Phase: These tests WILL FAIL because the enforcement checklist
currently has only 9 items and no code search tool reference.
"""
import re

import pytest
from pathlib import Path


ANTI_PATTERNS_FILE = Path(
    "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/context/anti-patterns.md"
)


def _get_enforcement_checklist_content() -> str:
    """Extract Enforcement Checklist section from anti-patterns.md."""
    content = ANTI_PATTERNS_FILE.read_text()
    checklist_pos = content.find("## Enforcement Checklist")
    if checklist_pos == -1:
        pytest.fail("Enforcement Checklist section not found in anti-patterns.md")
    checklist_content = content[checklist_pos:]
    # Limit to checklist section (ends at next ## or ---)
    next_section = checklist_content.find("\n---", 10)
    if next_section != -1:
        checklist_content = checklist_content[:next_section]
    return checklist_content


class TestAC5EnforcementChecklist:
    """AC#5: Enforcement checklist must have 10 items with code search reference."""

    # --- Happy Path ---

    def test_should_contain_10_checklist_items(self):
        """Enforcement checklist must have exactly 10 items (9 existing + 1 new)."""
        checklist = _get_enforcement_checklist_content()
        items = re.findall(r"^- \[ \]", checklist, re.MULTILINE)
        assert len(items) == 10, (
            f"Expected 10 checklist items, found {len(items)}. "
            "A new item for code search tool selection must be added."
        )

    def test_should_reference_code_search_or_treelint_in_new_item(self):
        """New checklist item must reference code search tool selection or Treelint."""
        checklist = _get_enforcement_checklist_content()
        lower = checklist.lower()
        has_ref = (
            "treelint" in lower or
            "code search" in lower or
            "tool selection" in lower
        )
        assert has_ref, (
            "New checklist item must reference Treelint or code search tool selection"
        )

    def test_should_preserve_all_9_existing_items(self):
        """All 9 original checklist items must be preserved."""
        checklist = _get_enforcement_checklist_content()
        existing_items = [
            "No Bash for file operations",
            "Components within size limits",
            "No language-specific code in framework",
            "All ambiguities use AskUserQuestion",
            "Context files read before development",
            "No circular dependencies",
            "Direct instructions, not narrative prose",
            "All components have frontmatter",
            "No hardcoded absolute paths",
        ]
        for item in existing_items:
            assert item in checklist, (
                f"Existing checklist item missing: '{item}'. "
                "All 9 original items must be preserved."
            )

    def test_should_use_checkbox_format_for_new_item(self):
        """New item must use the standard '- [ ]' checkbox format."""
        checklist = _get_enforcement_checklist_content()
        lines = checklist.splitlines()
        checkbox_lines = [ln for ln in lines if ln.strip().startswith("- [ ]")]
        # All items including new one must use checkbox format
        assert len(checkbox_lines) >= 10, (
            f"Expected at least 10 checkbox items (- [ ]), found {len(checkbox_lines)}"
        )

    # --- Format Consistency ---

    def test_should_maintain_consistent_format_with_existing_items(self):
        """New item must follow same format: '- [ ] Description (parenthetical)'."""
        checklist = _get_enforcement_checklist_content()
        lines = checklist.splitlines()
        checkbox_lines = [ln.strip() for ln in lines if ln.strip().startswith("- [ ]")]
        # The new (10th) item should exist and match general pattern
        assert len(checkbox_lines) >= 10, (
            "Need at least 10 checklist items to validate format consistency"
        )
        new_item = checkbox_lines[-1]  # Last item should be the new one
        # Must start with '- [ ] ' and have descriptive text
        assert new_item.startswith("- [ ] "), (
            f"New item format incorrect: '{new_item}'"
        )
        # Descriptive text should be at least 20 chars
        description = new_item[6:]  # Remove '- [ ] ' prefix
        assert len(description) >= 20, (
            f"New item description too short ({len(description)} chars): '{description}'"
        )

    # --- Enforcement Section Preservation ---

    def test_should_preserve_enforcement_checklist_heading(self):
        """The '## Enforcement Checklist' heading must remain."""
        content = ANTI_PATTERNS_FILE.read_text()
        assert "## Enforcement Checklist" in content, (
            "Enforcement Checklist heading missing"
        )

    def test_should_preserve_preamble_text(self):
        """The 'Before committing framework changes:' preamble must remain."""
        content = ANTI_PATTERNS_FILE.read_text()
        assert "Before committing framework changes:" in content, (
            "Enforcement checklist preamble text missing"
        )

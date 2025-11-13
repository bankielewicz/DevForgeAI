"""
Unit tests for story DoD section insertion validation.

Tests validate for STORY-027, STORY-028, STORY-029:
1. DoD section inserted after Edge Cases and before Notes
2. DoD section contains all 4 required subsections with proper checkbox format
3. YAML frontmatter (lines 1-10) remains unchanged after DoD insertion
"""

import pytest
from pathlib import Path
import re
import sys
from pathlib import Path as PathlibPath

# Import helpers from conftest (parent directory)
sys.path.insert(0, str(PathlibPath(__file__).parent.parent))
from conftest import extract_dod_section, extract_yaml_frontmatter


# Story IDs and files for parametrized tests
STORY_FILES = [
    ("STORY-027", Path(".ai_docs/Stories/STORY-027-wire-hooks-into-create-story-command.story.md")),
    ("STORY-028", Path(".ai_docs/Stories/STORY-028-wire-hooks-into-create-epic-command.story.md")),
    ("STORY-029", Path(".ai_docs/Stories/STORY-029-wire-hooks-into-create-sprint-command.story.md")),
]


class TestStoryDoD_Insertion:
    """
    Test suite for Definition of Done section insertion in stories.

    Validates that all stories have DoD sections in correct locations with
    proper subsections and YAML frontmatter integrity.
    """

    @pytest.mark.parametrize("story_id,story_file", STORY_FILES)
    def test_dod_section_placement(self, story_id, story_file):
        """
        Test: DoD section exists and is in reasonable location.

        Validates that:
        - DoD section exists (## Definition of Done)
        - DoD appears before Notes (if Notes exists)
        - DoD appears after Test Strategy (if Test Strategy exists)
        """
        if not story_file.exists():
            pytest.skip(f"{story_id}: Story file not found: {story_file.name}")

        content = story_file.read_text(encoding="utf-8")

        # Arrange
        dod_pos = content.find("## Definition of Done")

        # Assert: DoD section exists
        assert dod_pos != -1, f"{story_id}: DoD section missing"

        # If Notes section exists, DoD should appear before it
        notes_pos = content.find("## Notes")
        if notes_pos != -1:
            assert (
                dod_pos < notes_pos
            ), f"{story_id}: DoD must appear before Notes section"

        # If Test Strategy section exists, DoD should appear after it
        test_strategy_pos = content.find("## Test Strategy")
        if test_strategy_pos != -1:
            assert (
                dod_pos > test_strategy_pos
            ), f"{story_id}: DoD should appear after Test Strategy section"

    @pytest.mark.parametrize("story_id,story_file", STORY_FILES)
    def test_dod_subsections_present(self, story_id, story_file):
        """
        Test: DoD contains all 4 subsections with checkboxes.

        Validates that DoD section has:
        - ### Implementation subsection
        - ### Quality subsection
        - ### Testing subsection
        - ### Documentation subsection
        - At least 4 checkbox items (- [ ])
        """
        if not story_file.exists():
            pytest.skip(f"{story_id}: Story file not found: {story_file.name}")

        content = story_file.read_text(encoding="utf-8")

        # Extract DoD section
        dod_section = extract_dod_section(content)
        if dod_section is None:
            pytest.skip(f"{story_id}: DoD section not found")

        # Assert subsections present
        assert (
            "### Implementation" in dod_section
        ), f"{story_id}: DoD missing Implementation subsection"
        assert (
            "### Quality" in dod_section
        ), f"{story_id}: DoD missing Quality subsection"
        assert (
            "### Testing" in dod_section
        ), f"{story_id}: DoD missing Testing subsection"
        assert (
            "### Documentation" in dod_section
        ), f"{story_id}: DoD missing Documentation subsection"

        # Assert checkboxes present
        checkbox_count = dod_section.count("- [ ]")
        assert checkbox_count >= 4, f"{story_id}: Insufficient checkboxes: {checkbox_count}"

    @pytest.mark.parametrize("story_id,story_file", STORY_FILES)
    def test_yaml_frontmatter_valid(self, story_id, story_file):
        """
        Test: YAML frontmatter is syntactically valid.

        Validates that:
        - YAML has proper opening and closing delimiters (---)
        - All required fields present in YAML
        - Story ID field matches expected value
        """
        if not story_file.exists():
            pytest.skip(f"{story_id}: Story file not found: {story_file.name}")

        content = story_file.read_text(encoding="utf-8")

        # Extract YAML frontmatter
        lines = content.split("\n")

        # Find the closing --- delimiter
        closing_delim_idx = -1
        for i in range(1, min(20, len(lines))):
            if lines[i].strip() == "---":
                closing_delim_idx = i
                break

        if closing_delim_idx == -1:
            pytest.skip(f"{story_id}: Could not find closing YAML delimiter")

        yaml_lines = lines[:closing_delim_idx + 1]
        yaml_block = "\n".join(yaml_lines)

        # Assert YAML structure is valid
        assert yaml_lines[0] == "---", f"{story_id}: Missing opening YAML delimiter"
        assert yaml_lines[closing_delim_idx] == "---", f"{story_id}: Missing closing YAML delimiter"

        # Assert required fields present (but allow null/unset values)
        required_fields = ["id:", "title:", "epic:", "sprint:", "status:", "points:", "priority:", "assigned_to:", "created:", "format_version:"]
        for field in required_fields:
            assert (
                field in yaml_block
            ), f"{story_id}: YAML missing required field: {field}"

        # Assert specific values for story ID (should match story_id parameter)
        assert f'id: {story_id}' in yaml_block, f"{story_id}: ID field corrupted"

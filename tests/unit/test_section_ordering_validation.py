"""
Unit tests for section ordering validation.

Tests validate:
1. Template has correct section sequence
2. All 3 stories have correct section sequence (matching template)
3. DoD section appears in correct position
"""

import pytest
from pathlib import Path
import re
import sys
from pathlib import Path as PathlibPath

# Import helpers from conftest (parent directory)
sys.path.insert(0, str(PathlibPath(__file__).parent.parent))
from conftest import extract_section_headers


# Story IDs and files for parametrized tests
STORY_FILES = [
    ("STORY-027", Path("devforgeai/specs/Stories/STORY-027-wire-hooks-into-create-story-command.story.md")),
    ("STORY-028", Path("devforgeai/specs/Stories/STORY-028-wire-hooks-into-create-epic-command.story.md")),
    ("STORY-029", Path("devforgeai/specs/Stories/STORY-029-wire-hooks-into-create-sprint-command.story.md")),
]

# Define sections that SHOULD be ordered correctly
# Note: Not all sections must appear in every story, but if they do, they should be in this order
CRITICAL_SECTIONS = [
    "Definition of Done",  # DoD must exist
    "Notes",  # Notes is the final section
]


class TestSectionOrdering_Validation:
    """
    Test suite for section ordering in template and stories.

    Validates that markdown sections appear in correct order, with
    Definition of Done appearing before Notes section.
    """

    @pytest.fixture
    def template_path(self):
        """
        Fixture: Path to story template.

        Returns:
            Path: Path to story template file
        """
        return Path(".claude/skills/devforgeai-story-creation/assets/templates/story-template.md")

    def test_template_section_ordering(self, template_path):
        """
        Test: Template has DoD section before Notes section.

        Validates critical section ordering in the template:
        - Template contains '## Definition of Done'
        - Template contains '## Notes'
        - DoD appears before Notes in document
        """
        # Arrange
        if not template_path.exists():
            pytest.skip(f"Template file not found: {template_path}")

        content = template_path.read_text(encoding="utf-8")

        # Act: Extract section headers
        headers = extract_section_headers(content)

        # Assert: Critical sections appear in correct order
        dod_idx = None
        notes_idx = None

        for i, header in enumerate(headers):
            if "Definition of Done" in header:
                dod_idx = i
            elif "Notes" in header:
                notes_idx = i

        assert dod_idx is not None, "Template missing '## Definition of Done' section"
        assert notes_idx is not None, "Template missing '## Notes' section"

        # Critical ordering check: DoD must come before Notes
        assert (
            dod_idx < notes_idx
        ), f"Incorrect section order in template. DoD must appear before Notes. Got: {headers}"

    @pytest.mark.parametrize("story_id,story_file", STORY_FILES)
    def test_story_section_ordering(self, story_id, story_file):
        """
        Test: Story has DoD before Notes (if both sections exist).

        Validates section ordering in each story:
        - Story contains '## Definition of Done'
        - DoD appears before Notes (if Notes exists)
        """
        # Arrange
        if not story_file.exists():
            pytest.skip(f"{story_id}: Story file not found: {story_file.name}")

        content = story_file.read_text(encoding="utf-8")

        # Act: Extract section headers
        headers = extract_section_headers(content)

        # Assert: Critical sections appear in correct order
        dod_idx = None
        notes_idx = None

        for i, header in enumerate(headers):
            if "Definition of Done" in header:
                dod_idx = i
            elif "Notes" in header:
                notes_idx = i

        assert dod_idx is not None, f"{story_id}: Missing '## Definition of Done' section"

        if notes_idx is not None:
            assert (
                dod_idx < notes_idx
            ), f"{story_id}: DoD must appear before Notes. Got: {headers}"

    def test_dod_section_has_correct_header_format(self, template_path):
        """
        Test: DoD section header matches exact format.

        Validates that DoD header is exactly '## Definition of Done'
        with correct capitalization and spacing.
        """
        # Arrange
        if not template_path.exists():
            pytest.skip(f"Template file not found: {template_path}")

        content = template_path.read_text(encoding="utf-8")

        # Act: Find DoD header
        pattern = r"^## Definition of Done$"
        match_found = False
        for line in content.split("\n"):
            if re.match(pattern, line):
                match_found = True
                break

        # Assert
        assert (
            match_found
        ), "Template: DoD section header must be exactly '## Definition of Done' (case-sensitive)"

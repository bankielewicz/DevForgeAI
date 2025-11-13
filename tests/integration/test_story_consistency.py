"""
Integration test for story DoD consistency.

Tests validate:
1. All 3 stories have identical DoD section structure
2. Checkbox count and format consistent across stories
3. Subsection headers match exactly
"""

import pytest
from pathlib import Path
import re
import sys
from pathlib import Path as PathlibPath

# Import helpers from conftest (parent directory)
sys.path.insert(0, str(PathlibPath(__file__).parent.parent))
from conftest import extract_dod_section, extract_dod_subsections


class TestStoryConsistency:
    """
    Integration test suite for DoD consistency across stories.

    Validates that all stories have consistent DoD section structure,
    subsection ordering, and checkbox formatting.
    """

    @pytest.fixture
    def story_files(self):
        """
        Fixture: List of story files to validate for consistency.

        Returns:
            list: List of Path objects for story files
        """
        return [
            Path(".ai_docs/Stories/STORY-027-wire-hooks-into-create-story-command.story.md"),
            Path(".ai_docs/Stories/STORY-028-wire-hooks-into-create-epic-command.story.md"),
            Path(".ai_docs/Stories/STORY-029-wire-hooks-into-create-sprint-command.story.md"),
        ]

    # Define canonical DoD structure
    CANONICAL_SUBSECTIONS = [
        "### Implementation",
        "### Quality",
        "### Testing",
        "### Documentation",
    ]

    def count_checkboxes_in_subsection(self, dod_section, subsection_name):
        """Helper: Count checkboxes in a specific subsection."""
        # Find subsection start
        subsection_start = dod_section.find(subsection_name)
        if subsection_start == -1:
            return 0

        # Find next subsection start (or end of DoD)
        next_subsection_start = len(dod_section)
        for other_subsection in self.CANONICAL_SUBSECTIONS:
            if other_subsection != subsection_name:
                pos = dod_section.find(other_subsection, subsection_start + 1)
                if pos != -1 and pos < next_subsection_start:
                    next_subsection_start = pos

        subsection_content = dod_section[subsection_start:next_subsection_start]
        return subsection_content.count("- [ ]")

    def test_all_stories_have_dod_sections(self, story_files):
        """Test: All 3 stories contain DoD sections."""
        # Arrange & Act
        for story_file in story_files:
            assert story_file.exists(), f"Story file not found: {story_file.name}"
            content = story_file.read_text(encoding="utf-8")
            dod_section = extract_dod_section(content)

            # Assert
            assert (
                dod_section is not None
            ), f"{story_file.stem}: DoD section not found"

    def test_all_stories_have_canonical_subsections(self, story_files):
        """Test: All 3 stories have canonical DoD subsections."""
        # Arrange
        story_dod_sections = {}
        for story_file in story_files:
            content = story_file.read_text(encoding="utf-8")
            dod_section = extract_dod_section(content)
            story_dod_sections[story_file.stem] = dod_section

        # Act & Assert: Check each story has all subsections
        for story_id, dod_section in story_dod_sections.items():
            for canonical_subsection in self.CANONICAL_SUBSECTIONS:
                assert (
                    canonical_subsection in dod_section
                ), f"{story_id}: DoD missing subsection {canonical_subsection}"

    def test_all_stories_have_consistent_checkbox_format(self, story_files):
        """Test: All 3 stories use consistent checkbox format."""
        # Arrange
        story_dod_sections = {}
        for story_file in story_files:
            content = story_file.read_text(encoding="utf-8")
            dod_section = extract_dod_section(content)
            story_dod_sections[story_file.stem] = dod_section

        # Act & Assert: Check format consistency
        for story_id, dod_section in story_dod_sections.items():
            # Should only use "- [ ]" format
            correct_format_count = dod_section.count("- [ ]")
            # Check for incorrect formats
            incorrect_empty = dod_section.count("- []")
            incorrect_asterisk = dod_section.count("* [ ]")
            incorrect_other = dod_section.count("- [x]") + dod_section.count("- [X]")

            assert (
                correct_format_count > 0
            ), f"{story_id}: No checkboxes found in DoD"
            assert (
                incorrect_empty == 0
            ), f"{story_id}: Found incorrect checkbox format '- []'"
            assert (
                incorrect_asterisk == 0
            ), f"{story_id}: Found incorrect checkbox format '* [ ]'"

    def test_all_stories_have_minimum_checkboxes(self, story_files):
        """Test: All 3 stories have minimum checkbox count per subsection."""
        # Arrange
        story_dod_sections = {}
        for story_file in story_files:
            content = story_file.read_text(encoding="utf-8")
            dod_section = extract_dod_section(content)
            story_dod_sections[story_file.stem] = dod_section

        # Act & Assert: Each subsection should have at least 1 checkbox
        for story_id, dod_section in story_dod_sections.items():
            for subsection in self.CANONICAL_SUBSECTIONS:
                checkbox_count = self.count_checkboxes_in_subsection(
                    dod_section, subsection
                )
                assert (
                    checkbox_count >= 1
                ), f"{story_id}: Subsection '{subsection}' has no checkboxes ({checkbox_count})"

    def test_all_stories_have_similar_checkbox_counts(self, story_files):
        """Test: All 3 stories have similar total checkbox counts (within 2 of each other)."""
        # Arrange
        story_dod_sections = {}
        for story_file in story_files:
            content = story_file.read_text(encoding="utf-8")
            dod_section = extract_dod_section(content)
            story_dod_sections[story_file.stem] = dod_section

        # Act: Count total checkboxes in each story
        checkbox_counts = {}
        for story_id, dod_section in story_dod_sections.items():
            total_checkboxes = dod_section.count("- [ ]")
            checkbox_counts[story_id] = total_checkboxes

        # Assert: Checkbox counts should be similar (within 2 of each other)
        if checkbox_counts:
            min_count = min(checkbox_counts.values())
            max_count = max(checkbox_counts.values())
            difference = max_count - min_count

            assert (
                difference <= 2
            ), f"Checkbox count inconsistent: {checkbox_counts}. Max difference: {difference} (expected ≤2)"

    @pytest.mark.slow
    def test_subsection_order_identical_across_stories(self, story_files):
        """Test: DoD subsection order is identical in all 3 stories."""
        # Arrange
        story_subsections = {}
        for story_file in story_files:
            content = story_file.read_text(encoding="utf-8")
            dod_section = extract_dod_section(content)
            subsections = extract_dod_subsections(dod_section)
            story_subsections[story_file.stem] = subsections

        # Get reference order (first story)
        reference_order = list(story_subsections.values())[0]

        # Assert: All stories have same order
        for story_id, subsections in story_subsections.items():
            assert (
                subsections == reference_order
            ), f"{story_id}: DoD subsection order differs from reference. Got: {subsections}, Expected: {reference_order}"

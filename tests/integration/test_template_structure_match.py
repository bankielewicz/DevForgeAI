"""
Integration test for template structure matching.

Tests validate:
1. Updated template structure matches STORY-007 reference
2. All required sections present and in correct order
3. DoD section structure matches across template and stories
"""

import pytest
from pathlib import Path
import re
import sys
from pathlib import Path as PathlibPath

# Import helpers from conftest (parent directory)
sys.path.insert(0, str(PathlibPath(__file__).parent.parent))
from conftest import extract_section_headers, extract_dod_subsections


class TestTemplateStructureMatch:
    """
    Integration test suite for template structure validation.

    Validates that story template has all required sections in correct
    order and that reference stories follow the template structure.
    """

    @pytest.fixture
    def template_path(self):
        """
        Fixture: Path to story template.

        Returns:
            Path: Path to story template file
        """
        return Path(".claude/skills/devforgeai-story-creation/assets/templates/story-template.md")

    @pytest.fixture
    def reference_story_path(self):
        """
        Fixture: Path to STORY-007 (reference story with complete structure).

        Returns:
            Path: Path to reference story file
        """
        return Path(".ai_docs/Stories/STORY-007-post-operation-retrospective-conversation.story.md")

    # Define critical sections that MUST be present
    CRITICAL_SECTIONS = [
        "## Description",
        "## Acceptance Criteria",
        "## Definition of Done",
        "## Notes",
    ]

    CANONICAL_DOD_SUBSECTIONS = [
        "### Implementation",
        "### Quality",
        "### Testing",
        "### Documentation",
    ]

    def test_template_contains_all_canonical_sections(self, template_path):
        """
        Test: Template contains all critical sections.

        Validates that template has the following sections:
        - ## Description
        - ## Acceptance Criteria
        - ## Definition of Done
        - ## Notes
        """
        # Arrange
        if not template_path.exists():
            pytest.skip(f"Template file not found: {template_path}")

        content = template_path.read_text(encoding="utf-8")

        # Act: Extract sections
        sections = extract_section_headers(content)

        # Assert: All critical sections present
        for critical_section in self.CRITICAL_SECTIONS:
            assert (
                critical_section in sections
            ), f"Template missing critical section: {critical_section}"

    def test_template_sections_in_critical_order(self, template_path):
        """
        Test: Template critical sections DoD appears before Notes.

        Validates that in the template, the Definition of Done section
        appears before the Notes section.
        """
        # Arrange
        if not template_path.exists():
            pytest.skip(f"Template file not found: {template_path}")

        content = template_path.read_text(encoding="utf-8")

        # Act: Extract sections
        sections = extract_section_headers(content)

        # Assert: DoD appears before Notes
        dod_section = "## Definition of Done"
        notes_section = "## Notes"

        if dod_section in sections and notes_section in sections:
            dod_idx = sections.index(dod_section)
            notes_idx = sections.index(notes_section)
            assert (
                dod_idx < notes_idx
            ), f"DoD must appear before Notes"

    def test_template_dod_subsections_correct(self, template_path):
        """
        Test: Template DoD section has all canonical subsections.

        Validates that the DoD section contains:
        - ### Implementation
        - ### Quality
        - ### Testing
        - ### Documentation
        """
        # Arrange
        if not template_path.exists():
            pytest.skip(f"Template file not found: {template_path}")

        content = template_path.read_text(encoding="utf-8")

        # Act: Extract DoD subsections
        subsections = extract_dod_subsections(content)

        # Assert: All canonical subsections present
        for canonical_subsection in self.CANONICAL_DOD_SUBSECTIONS:
            assert (
                canonical_subsection in subsections
            ), f"Template DoD missing canonical subsection: {canonical_subsection}"

    def test_template_dod_subsections_in_canonical_order(self, template_path):
        """
        Test: Template DoD subsections appear in canonical order.

        Validates that DoD subsections appear in order:
        1. Implementation
        2. Quality
        3. Testing
        4. Documentation
        """
        # Arrange
        if not template_path.exists():
            pytest.skip(f"Template file not found: {template_path}")

        content = template_path.read_text(encoding="utf-8")

        # Act: Extract DoD subsections
        subsections = extract_dod_subsections(content)

        # Build index of canonical subsections as they appear
        canonical_indices = {}
        for canonical_subsection in self.CANONICAL_DOD_SUBSECTIONS:
            if canonical_subsection in subsections:
                canonical_indices[canonical_subsection] = subsections.index(canonical_subsection)

        # Assert: Subsections appear in canonical order
        previous_idx = -1
        for canonical_subsection in self.CANONICAL_DOD_SUBSECTIONS:
            if canonical_subsection in canonical_indices:
                current_idx = canonical_indices[canonical_subsection]
                assert (
                    current_idx > previous_idx
                ), f"DoD subsection '{canonical_subsection}' out of order"
                previous_idx = current_idx

    @pytest.mark.slow
    def test_reference_story_matches_template_structure(self, reference_story_path, template_path):
        """
        Test: STORY-007 (reference story) has same structure as template.

        Validates that existing reference stories follow the template pattern,
        confirming the template structure is correct. Checks that:
        - Both have DoD section
        - Both have Notes section (if template has it)
        - DoD appears before Notes in both
        """
        # Arrange
        if not reference_story_path.exists():
            pytest.skip(f"Reference story not found: {reference_story_path}")
        if not template_path.exists():
            pytest.skip(f"Template not found: {template_path}")

        template_content = template_path.read_text(encoding="utf-8")
        reference_content = reference_story_path.read_text(encoding="utf-8")

        # Extract sections from both
        template_sections = extract_section_headers(template_content)
        reference_sections = extract_section_headers(reference_content)

        # Act & Assert: Both have DoD and Notes with DoD before Notes
        assert (
            "## Definition of Done" in template_sections
        ), "Template missing DoD section"
        assert (
            "## Definition of Done" in reference_sections
        ), "Reference story missing DoD section"

        # Check that DoD appears before Notes if Notes exists
        if "## Notes" in template_sections and "## Definition of Done" in template_sections:
            template_dod_idx = template_sections.index("## Definition of Done")
            template_notes_idx = template_sections.index("## Notes")
            assert (
                template_dod_idx < template_notes_idx
            ), "Template: DoD must appear before Notes"

        if "## Notes" in reference_sections and "## Definition of Done" in reference_sections:
            reference_dod_idx = reference_sections.index("## Definition of Done")
            reference_notes_idx = reference_sections.index("## Notes")
            assert (
                reference_dod_idx < reference_notes_idx
            ), "Reference: DoD must appear before Notes"

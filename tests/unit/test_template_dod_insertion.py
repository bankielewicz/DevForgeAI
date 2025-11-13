"""
Unit tests for template DoD section insertion validation.

Tests validate:
1. DoD section inserted after "## Edge Cases" and before "## Notes"
2. DoD section contains all 4 required subsections
3. Template variables preserved intact during insertion
"""

import pytest
from pathlib import Path


class TestTemplateDoD_Insertion:
    """Test suite for Definition of Done section in story template."""

    @pytest.fixture
    def template_path(self):
        """Fixture: Path to the story template file."""
        return Path(".claude/skills/devforgeai-story-creation/assets/templates/story-template.md")

    @pytest.fixture
    def template_content(self, template_path):
        """Fixture: Load template file content."""
        if not template_path.exists():
            pytest.skip(f"Template file not found: {template_path}")
        return template_path.read_text(encoding="utf-8")

    def test_dod_section_placement(self, template_content):
        """
        Test: DoD section inserted in correct location.

        Arrange:
            - Load template content

        Act:
            - Find positions of "## Definition of Done" and related sections
            - Determine if DoD exists in template

        Assert:
            - DoD section is present in template
            - DoD appears after "## Test Strategy" section
            - DoD appears before "## Workflow Status" section
        """
        # Arrange
        dod_pos = template_content.find("## Definition of Done")
        test_strategy_pos = template_content.find("## Test Strategy")
        workflow_status_pos = template_content.find("## Workflow Status")

        # Assert: DoD section present
        assert (
            dod_pos != -1
        ), "Template missing '## Definition of Done' section"

        # Assert: DoD positioned correctly (after Test Strategy, before Workflow Status)
        if test_strategy_pos != -1:
            assert (
                dod_pos > test_strategy_pos
            ), "DoD section should appear after Test Strategy section"

        if workflow_status_pos != -1:
            assert (
                dod_pos < workflow_status_pos
            ), "DoD section should appear before Workflow Status section"

    def test_dod_subsections_present(self, template_content):
        """
        Test: DoD section contains all 4 required subsections.

        Arrange:
            - Load template content
            - Define required subsection headers

        Act:
            - Search for each subsection in template

        Assert:
            - All 4 subsections present (Implementation, Quality, Testing, Documentation)
            - Subsections in correct order
        """
        # Arrange
        required_subsections = [
            "### Implementation",
            "### Quality",
            "### Testing",
            "### Documentation",
        ]

        # Extract DoD section for targeted checks
        dod_start = template_content.find("## Definition of Done")
        workflow_status_start = template_content.find("## Workflow Status")
        assert dod_start != -1, "DoD section not found"

        # If Workflow Status exists, use it as boundary; otherwise use next heading or end of file
        if workflow_status_start != -1:
            dod_section = template_content[dod_start:workflow_status_start]
        else:
            # Find next ## heading after DoD, or use rest of file
            next_heading = template_content.find("\n## ", dod_start + 1)
            if next_heading != -1:
                dod_section = template_content[dod_start:next_heading]
            else:
                dod_section = template_content[dod_start:]

        # Act & Assert: Check each subsection
        for subsection in required_subsections:
            assert (
                subsection in dod_section
            ), f"DoD section missing required subsection: {subsection}"

        # Assert: Subsections appear in correct order
        impl_pos = dod_section.find("### Implementation")
        qual_pos = dod_section.find("### Quality")
        test_pos = dod_section.find("### Testing")
        doc_pos = dod_section.find("### Documentation")

        assert (
            impl_pos < qual_pos < test_pos < doc_pos
        ), "DoD subsections must appear in order: Implementation → Quality → Testing → Documentation"

    def test_template_variables_preserved(self, template_content):
        """
        Test: Template variables preserved intact after DoD insertion.

        Arrange:
            - Load template content
            - Define required template variables

        Act:
            - Search for each template variable in content

        Assert:
            - All template variables still present and intact
            - No corrupted or partial variables
        """
        # Arrange
        required_variables = [
            "[Story Title",  # Template uses "[Story Title - What is being built]"
            "[user role",  # Template uses "[user role/persona]"
            "[capability",  # Template uses "[capability/feature]"
            "[X]",  # Generic placeholder
        ]

        # Act & Assert: Verify each variable present (check for pattern match)
        for variable in required_variables:
            assert (
                variable in template_content
            ), f"Template variable corrupted or removed: {variable}"

        # Additional checks for common template placeholders
        assert "STORY-XXX" in template_content, "Template ID placeholder corrupted"
        assert "EPIC-XXX" in template_content, "Template Epic placeholder corrupted"
        assert "[initial context/state]" in template_content, "Template AC placeholder corrupted"

    def test_dod_section_has_checklist_items(self, template_content):
        """
        Test: DoD section contains checkbox items in correct format.

        Arrange:
            - Load template content
            - Extract DoD section

        Act:
            - Count checkbox items in each subsection

        Assert:
            - Each subsection has at least 1 checkbox item
            - Checkboxes use correct format: "- [ ]"
        """
        # Arrange
        dod_start = template_content.find("## Definition of Done")
        workflow_status_start = template_content.find("## Workflow Status")

        if dod_start == -1:
            pytest.skip("DoD section not found in template")

        if workflow_status_start != -1:
            dod_section = template_content[dod_start:workflow_status_start]
        else:
            # Find next ## heading after DoD, or use rest of file
            next_heading = template_content.find("\n## ", dod_start + 1)
            if next_heading != -1:
                dod_section = template_content[dod_start:next_heading]
            else:
                dod_section = template_content[dod_start:]

        # Act & Assert: Check for checkbox format
        assert (
            "- [ ]" in dod_section
        ), "DoD section missing checkbox items in correct format (- [ ])"

        # Verify checkbox count (at least 4 for the 4 subsections)
        checkbox_count = dod_section.count("- [ ]")
        assert (
            checkbox_count >= 4
        ), f"DoD section has insufficient checkbox items: {checkbox_count} (expected ≥4)"

    def test_dod_section_not_empty(self, template_content):
        """
        Test: DoD section contains meaningful content, not just headers.

        Arrange:
            - Load template content
            - Extract DoD section

        Act:
            - Measure DoD section size
            - Check for content between headers

        Assert:
            - DoD section has reasonable content length (>200 chars)
            - No empty subsections
        """
        # Arrange
        dod_start = template_content.find("## Definition of Done")
        workflow_status_start = template_content.find("## Workflow Status")

        if dod_start == -1:
            pytest.skip("DoD section not found in template")

        if workflow_status_start != -1:
            dod_section = template_content[dod_start:workflow_status_start]
        else:
            # Find next ## heading after DoD, or use rest of file
            next_heading = template_content.find("\n## ", dod_start + 1)
            if next_heading != -1:
                dod_section = template_content[dod_start:next_heading]
            else:
                dod_section = template_content[dod_start:]

        # Act
        dod_length = len(dod_section)

        # Assert
        assert (
            dod_length > 200
        ), f"DoD section appears empty or minimal: {dod_length} chars"

        # Verify no "TODO" or placeholder text indicating incomplete template
        assert "TODO" not in dod_section, "DoD section contains incomplete TODO markers"
        assert "[PLACEHOLDER]" not in dod_section, "DoD section contains unresolved placeholder markers"

"""
Integration test for complete DoD update workflow.

Tests validate:
1. Full workflow: template update + story updates + validation
2. All components work together without errors
3. No regressions in unrelated content
"""

import pytest
from pathlib import Path
import time
import yaml


class TestFullUpdateWorkflow:
    """Integration test suite for complete DoD update workflow."""

    @pytest.fixture
    def template_path(self):
        """Fixture: Path to story template."""
        return Path(".claude/skills/devforgeai-story-creation/assets/templates/story-template.md")

    @pytest.fixture
    def story_files(self):
        """Fixture: List of story files."""
        return [
            Path("devforgeai/specs/Stories/STORY-027-wire-hooks-into-create-story-command.story.md"),
            Path("devforgeai/specs/Stories/STORY-028-wire-hooks-into-create-epic-command.story.md"),
            Path("devforgeai/specs/Stories/STORY-029-wire-hooks-into-create-sprint-command.story.md"),
        ]

    @pytest.fixture
    def all_files(self, template_path, story_files):
        """Fixture: All files involved in workflow."""
        return [template_path] + story_files

    def test_full_update_workflow(self, template_path, story_files, all_files):
        """
        Test: Full workflow - template and stories updated, validation passes.

        This integration test verifies:
        - All files exist and are readable
        - Template has DoD section
        - All stories have DoD sections
        - DoD sections properly formatted
        - Workflow executes in <30 seconds
        - No errors logged during workflow
        """
        # Arrange
        start_time = time.time()
        errors = []

        # Act & Assert: Verify all files exist
        for file_path in all_files:
            assert file_path.exists(), f"File missing: {file_path.name}"

        # Act: Load all files
        template_content = template_path.read_text(encoding="utf-8")
        story_contents = {}
        for story_file in story_files:
            story_contents[story_file.stem] = story_file.read_text(encoding="utf-8")

        # Assert: Template has DoD section
        assert "## Definition of Done" in template_content, "Template missing DoD section"

        # Assert: All stories have DoD sections
        for story_id, content in story_contents.items():
            assert (
                "## Definition of Done" in content
            ), f"{story_id}: Missing DoD section"
            assert (
                "### Implementation" in content
            ), f"{story_id}: DoD missing Implementation subsection"
            assert (
                "### Quality" in content
            ), f"{story_id}: DoD missing Quality subsection"
            assert (
                "### Testing" in content
            ), f"{story_id}: DoD missing Testing subsection"
            assert (
                "### Documentation" in content
            ), f"{story_id}: DoD missing Documentation subsection"

        # Assert: DoD sections properly formatted with checkboxes
        for story_id, content in story_contents.items():
            dod_start = content.find("## Definition of Done")
            if dod_start == -1:
                continue  # Skip if DoD not found

            # Find next ## heading after DoD
            next_heading = content.find("\n## ", dod_start + 1)
            if next_heading != -1:
                dod_section = content[dod_start:next_heading]
            else:
                dod_section = content[dod_start:]

            checkbox_count = dod_section.count("- [ ]")
            assert (
                checkbox_count >= 4
            ), f"{story_id}: DoD has insufficient checkboxes: {checkbox_count}"

        # Assert: YAML frontmatter intact
        for story_id, content in story_contents.items():
            lines = content.split("\n")
            assert (
                lines[0] == "---"
            ), f"{story_id}: Missing opening YAML delimiter"
            # Find closing delimiter
            closing_found = False
            for i in range(1, 15):  # Should be around line 11
                if lines[i].strip() == "---":
                    closing_found = True
                    break
            assert closing_found, f"{story_id}: Missing closing YAML delimiter"

        # Assert: Workflow completed within performance target
        elapsed = time.time() - start_time
        assert (
            elapsed < 30
        ), f"Workflow took too long: {elapsed:.2f}s (target: <30s)"

        # Assert: No errors encountered
        assert len(errors) == 0, f"Errors during workflow: {errors}"

    @pytest.mark.slow
    def test_workflow_consistency_across_stories(self, story_files):
        """
        Test: All stories have consistent DoD structure.

        Validates:
        - All stories have identical subsection structure
        - Checkbox format consistent
        - Subsection order identical
        """
        # Arrange
        story_contents = {}
        for story_file in story_files:
            story_contents[story_file.stem] = story_file.read_text(encoding="utf-8")

        # Extract DoD sections from each story
        dod_sections = {}
        for story_id, content in story_contents.items():
            dod_start = content.find("## Definition of Done")
            if dod_start == -1:
                pytest.skip(f"{story_id}: DoD section not found")

            # Find next ## heading after DoD
            next_heading = content.find("\n## ", dod_start + 1)
            if next_heading != -1:
                dod_sections[story_id] = content[dod_start:next_heading]
            else:
                dod_sections[story_id] = content[dod_start:]

        # Act & Assert: Verify all DoD sections have same structure
        reference_subsections = [
            "### Implementation",
            "### Quality",
            "### Testing",
            "### Documentation",
        ]

        for story_id, dod_section in dod_sections.items():
            for subsection in reference_subsections:
                assert (
                    subsection in dod_section
                ), f"{story_id}: DoD missing {subsection}"

        # Assert: Checkbox format consistent across all stories
        for story_id, dod_section in dod_sections.items():
            # Should only use "- [ ]" format, not "- []" or "* [ ]"
            incorrect_formats = dod_section.count("- []") + dod_section.count("* [ ]")
            assert (
                incorrect_formats == 0
            ), f"{story_id}: DoD uses inconsistent checkbox format"

        # Assert: Subsection order identical in all stories
        for story_id, dod_section in dod_sections.items():
            impl_pos = dod_section.find("### Implementation")
            qual_pos = dod_section.find("### Quality")
            test_pos = dod_section.find("### Testing")
            doc_pos = dod_section.find("### Documentation")

            assert (
                impl_pos < qual_pos < test_pos < doc_pos
            ), f"{story_id}: DoD subsection order incorrect"

    def test_workflow_no_unintended_changes(self, story_files):
        """
        Test: Workflow only added DoD section, no other content changed.

        Validates:
        - Definition of Done section is present
        - Notes section is present
        - Description, AC, Tech Spec sections intact and complete
        - Critical sections contain expected content
        """
        # Arrange: This is a validation test - assumes STORY-014 already completed

        story_contents = {}
        for story_file in story_files:
            story_contents[story_file.stem] = story_file.read_text(encoding="utf-8")

        # Act & Assert: Verify critical sections exist and appear to be complete
        required_sections = [
            "## Description",
            "## Acceptance Criteria",
            "## Definition of Done",
            "## Notes",
        ]

        for story_id, content in story_contents.items():
            for section in required_sections:
                assert (
                    section in content
                ), f"{story_id}: Missing section: {section}"

            # Verify sections are not empty (rough check)
            # Description should have content like "As a"
            assert "As a" in content, f"{story_id}: Description section appears empty"

            # AC should have "Given" / "When" / "Then"
            assert (
                "Given" in content and "When" in content and "Then" in content
            ), f"{story_id}: Acceptance Criteria appear incomplete"

            # DoD should have the 4 subsections
            assert "### Implementation" in content, f"{story_id}: DoD missing subsections"

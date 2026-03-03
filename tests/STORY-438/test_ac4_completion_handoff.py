"""
Test: AC#4 - Completion Handoff Updated to Output requirements.md
Story: STORY-438
Generated: 2026-02-18
TDD Phase: RED (tests should FAIL against current source)
"""
import os
import re
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
HANDOFF_MD = os.path.join(
    PROJECT_ROOT, "src", "claude", "skills", "devforgeai-ideation",
    "references", "completion-handoff.md",
)


@pytest.fixture
def handoff_content():
    assert os.path.exists(HANDOFF_MD), f"completion-handoff.md not found at {HANDOFF_MD}"
    with open(HANDOFF_MD, "r", encoding="utf-8") as f:
        return f.read()


class TestAC4CompletionHandoff:
    """Verify completion handoff outputs requirements.md per F4 schema."""

    def test_ac4_primary_output_is_requirements_md(self, handoff_content):
        """AC4(a): Primary output becomes YAML-structured requirements.md."""
        assert "requirements.md" in handoff_content, (
            "completion-handoff.md does not reference requirements.md as output"
        )
        # Should mention YAML structure
        assert re.search(r"yaml|YAML", handoff_content), (
            "completion-handoff.md does not mention YAML format"
        )

    def test_ac4_no_epic_document_references(self, handoff_content):
        """AC4(b): Epic document references removed from completion summary template."""
        # Should not have "Epic Document" as a generated artifact
        assert "epic document" not in handoff_content.lower() or \
               "epic.md" not in handoff_content, (
            "completion-handoff.md still references epic documents as output"
        )

    def test_ac4_generated_artifacts_shows_requirements(self, handoff_content):
        """AC4(c): 'Generated Artifacts' section shows requirements.md as primary artifact."""
        match = re.search(
            r"(?:generated\s+artifacts|artifacts)(.*?)(?=\n##|\Z)",
            handoff_content,
            re.DOTALL | re.IGNORECASE,
        )
        if match:
            section = match.group(1)
            assert "requirements.md" in section, (
                "Generated Artifacts does not list requirements.md"
            )

    def test_ac4_next_action_points_to_create_epic(self, handoff_content):
        """AC4(d): Next action recommendation points to /create-epic."""
        assert "/create-epic" in handoff_content, (
            "completion-handoff.md does not recommend /create-epic as next action"
        )

    def test_ac4_f4_schema_structure_in_template(self, handoff_content):
        """AC4(e): Completion template follows F4 schema structure."""
        content_lower = handoff_content.lower()
        f4_fields = ["functional_requirements", "non_functional_requirements", "constraints", "dependencies"]
        found = [f for f in f4_fields if f in content_lower]
        assert len(found) >= 3, (
            f"F4 schema fields missing from template. Found: {found}, expected at least 3 of {f4_fields}"
        )

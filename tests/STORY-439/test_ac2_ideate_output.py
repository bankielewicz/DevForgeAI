"""
Test: AC#2 - /ideate Command Output Changed to requirements.md
Story: STORY-439
Phase: RED (TDD - tests expected to FAIL)
Pattern: AAA (Arrange, Act, Assert)
"""
import os
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
IDEATE_SRC = os.path.join(PROJECT_ROOT, "src", "claude", "commands", "ideate.md")


@pytest.fixture
def ideate_content():
    """Load ideate.md content from src/ tree."""
    with open(IDEATE_SRC, "r", encoding="utf-8") as f:
        return f.read()


class TestIdeateOutputDescription:
    """IDE-001: Description shows requirements.md as primary output."""

    def test_should_mention_requirements_md_in_description_when_updated(self, ideate_content):
        # Arrange
        expected = "requirements.md"
        # Act - check first 30 lines (description area)
        description_area = "\n".join(ideate_content.splitlines()[:30])
        has_requirements = expected in description_area
        # Assert
        assert has_requirements, (
            "ideate.md description must mention 'requirements.md' as primary output"
        )

    def test_should_not_list_epic_documents_as_direct_output_when_updated(self, ideate_content):
        # Arrange
        forbidden_phrases = ["epic documents", "Epic documents"]
        # Act
        has_epic_output = any(phrase in ideate_content for phrase in forbidden_phrases)
        # Assert
        assert not has_epic_output, (
            "ideate.md must NOT list 'epic documents' as direct ideation output"
        )


class TestIdeateOutputSection:
    """IDE-002: Output section describes YAML requirements format."""

    def test_should_describe_yaml_requirements_format_when_updated(self, ideate_content):
        # Arrange - look for YAML/requirements references in output section
        content_lower = ideate_content.lower()
        # Act
        has_yaml_ref = "yaml" in content_lower and "requirements" in content_lower
        # Assert
        assert has_yaml_ref, (
            "ideate.md output section must describe YAML-structured requirements.md"
        )


class TestIdeateNextStepGuidance:
    """IDE-003: Completion guidance recommends /create-epic."""

    def test_should_recommend_create_epic_as_next_step_when_updated(self, ideate_content):
        # Arrange
        expected = "/create-epic"
        # Act
        has_next_step = expected in ideate_content
        # Assert
        assert has_next_step, (
            "ideate.md must recommend '/create-epic' as next step for epic generation"
        )

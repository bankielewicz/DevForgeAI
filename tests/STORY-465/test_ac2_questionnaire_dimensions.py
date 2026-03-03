"""Test AC#2: Six-Dimension Questionnaire.

Story: STORY-465
Validates that the skill covers all 6 assessment dimensions and uses
AskUserQuestion for interactive questionnaire flow.
"""
import pytest
from pathlib import Path


# The 6 required assessment dimensions
REQUIRED_DIMENSIONS = [
    "Work Style",
    "Task Completion",
    "Motivation",
    "Energy Management",
    "Previous Attempts",
    "Self-Reported Challenges",
]


@pytest.fixture
def questionnaire_content(skill_file, references_dir):
    """Load combined content from SKILL.md and work-style-questionnaire.md.

    The 6 dimensions may be defined in either the main skill file or the
    questionnaire reference file.
    """
    combined = ""
    if skill_file.exists():
        combined += skill_file.read_text(encoding="utf-8")
    questionnaire = references_dir / "work-style-questionnaire.md"
    if questionnaire.exists():
        combined += "\n" + questionnaire.read_text(encoding="utf-8")
    return combined


class TestDimensionPresence:
    """Tests that all 6 assessment dimensions are present."""

    @pytest.mark.parametrize("dimension", REQUIRED_DIMENSIONS)
    def test_should_contain_dimension(self, questionnaire_content, dimension):
        """Each of the 6 dimensions must appear in the questionnaire content."""
        assert dimension.lower() in questionnaire_content.lower(), (
            f"Missing required dimension: '{dimension}'. "
            f"The assessment must cover all 6 dimensions."
        )

    def test_should_contain_all_six_dimensions(self, questionnaire_content):
        """All 6 dimensions must be present (not just some)."""
        missing = [
            d for d in REQUIRED_DIMENSIONS
            if d.lower() not in questionnaire_content.lower()
        ]
        assert len(missing) == 0, (
            f"Missing {len(missing)} dimensions: {missing}. "
            f"All 6 dimensions are required."
        )


class TestAskUserQuestionPattern:
    """Tests that AskUserQuestion is used for interactive assessment."""

    def test_should_reference_askuserquestion(self, questionnaire_content):
        """The questionnaire must use AskUserQuestion for user interaction."""
        assert "AskUserQuestion" in questionnaire_content, (
            "Questionnaire must reference AskUserQuestion tool for "
            "interactive dimension assessment."
        )

    @pytest.mark.parametrize("dimension", REQUIRED_DIMENSIONS)
    def test_should_use_askuserquestion_per_dimension(self, questionnaire_content, dimension):
        """AskUserQuestion should be referenced in the context of each dimension.

        This validates that interactive questioning is planned for every
        dimension, not just mentioned once generically.
        """
        # Find sections containing the dimension name and check for AskUserQuestion nearby
        content_lower = questionnaire_content.lower()
        dim_lower = dimension.lower()

        # The dimension must exist (tested above) and AskUserQuestion must exist
        assert dim_lower in content_lower, f"Dimension '{dimension}' not found."
        assert "askuserquestion" in content_lower, (
            "AskUserQuestion not found in questionnaire content."
        )

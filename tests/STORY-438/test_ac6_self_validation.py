"""
Test: AC#6 - Self-Validation Workflow Updated
Story: STORY-438
Generated: 2026-02-18
TDD Phase: RED (tests should FAIL against current source)
"""
import os
import re
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
VALIDATION_MD = os.path.join(
    PROJECT_ROOT, "src", "claude", "skills", "devforgeai-ideation",
    "references", "self-validation-workflow.md",
)


@pytest.fixture
def validation_content():
    assert os.path.exists(VALIDATION_MD), f"self-validation-workflow.md not found at {VALIDATION_MD}"
    with open(VALIDATION_MD, "r", encoding="utf-8") as f:
        return f.read()


class TestAC6SelfValidation:
    """Verify self-validation workflow updated for PM-only outputs."""

    def test_ac6_no_epic_document_checks(self, validation_content):
        """AC6(a): Validation removes epic document checks."""
        content_lower = validation_content.lower()
        # Should not validate epic document existence/structure
        assert "epic document" not in content_lower or "epic.md" not in validation_content, (
            "self-validation-workflow.md still validates epic documents"
        )

    def test_ac6_no_complexity_score_validation(self, validation_content):
        """AC6(b): Validation removes complexity score validation (0-60, tier 1-4)."""
        content_lower = validation_content.lower()
        has_complexity_score = re.search(r"complexity\s+score", content_lower)
        has_tier_range = re.search(r"tier\s+[1-4]", content_lower)
        has_score_range = re.search(r"0[-\s]60", validation_content)
        assert not has_complexity_score, (
            "self-validation-workflow.md still validates complexity scores"
        )
        assert not has_score_range, (
            "self-validation-workflow.md still references 0-60 score range"
        )

    def test_ac6_no_feasibility_assessment_checks(self, validation_content):
        """AC6(c): Validation removes feasibility assessment checks."""
        content_lower = validation_content.lower()
        assert "feasibility" not in content_lower, (
            "self-validation-workflow.md still validates feasibility assessments"
        )

    def test_ac6_requirements_schema_checks_retained(self, validation_content):
        """AC6(d): Validation retains requirements.md schema compliance checks."""
        assert "requirements" in validation_content.lower(), (
            "self-validation-workflow.md lost requirements validation"
        )

    def test_ac6_f4_schema_validation_added(self, validation_content):
        """AC6(e): Validation adds F4 schema validation (YAML structure, required fields)."""
        content_lower = validation_content.lower()
        has_yaml = re.search(r"yaml", content_lower)
        has_f4 = re.search(r"f4|schema", content_lower)
        assert has_yaml, (
            "self-validation-workflow.md does not validate YAML structure"
        )
        assert has_f4, (
            "self-validation-workflow.md does not reference F4 schema validation"
        )

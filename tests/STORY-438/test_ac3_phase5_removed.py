"""
Test: AC#3 - Phase 5 (Feasibility & Constraints Analysis) Removed from SKILL.md
Story: STORY-438
Generated: 2026-02-18
TDD Phase: RED (tests should FAIL against current source)
"""
import os
import re
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SKILL_MD = os.path.join(PROJECT_ROOT, "src", "claude", "skills", "devforgeai-ideation", "SKILL.md")


@pytest.fixture
def skill_content():
    assert os.path.exists(SKILL_MD), f"SKILL.md not found at {SKILL_MD}"
    with open(SKILL_MD, "r", encoding="utf-8") as f:
        return f.read()


class TestAC3Phase5Removed:
    """Verify Phase 5 (Feasibility & Constraints Analysis) is fully removed from SKILL.md."""

    def test_ac3_no_phase5_header(self, skill_content):
        """AC3(a): No 'Phase 5' header exists in SKILL.md."""
        matches = re.findall(r"^#{1,4}\s+.*Phase\s+5\b", skill_content, re.MULTILINE)
        assert len(matches) == 0, (
            f"Phase 5 header(s) still present in SKILL.md: {matches}"
        )

    def test_ac3_no_feasibility_analysis_workflow_ref(self, skill_content):
        """AC3(b): No references to 'feasibility-analysis-workflow.md' in phase definitions."""
        assert "feasibility-analysis-workflow.md" not in skill_content, (
            "Reference to feasibility-analysis-workflow.md still present in SKILL.md"
        )

    def test_ac3_description_no_feasibility_analysis(self, skill_content):
        """AC3(c): SKILL.md description no longer mentions 'feasibility analysis'."""
        assert "feasibility analysis" not in skill_content.lower(), (
            "SKILL.md still mentions 'feasibility analysis'"
        )

    def test_ac3_error_handling_no_error_type_5(self, skill_content):
        """AC3(d): Error Handling section removes error-type-5-constraint-conflicts.md."""
        assert "error-type-5" not in skill_content, (
            "SKILL.md still references error-type-5"
        )

    def test_ac3_reference_files_no_feasibility_entries(self, skill_content):
        """AC3(e): Reference Files section removes feasibility-related entries."""
        match = re.search(
            r"##\s+Reference\s+Files(.*?)(?=\n##\s|\Z)",
            skill_content,
            re.DOTALL | re.IGNORECASE,
        )
        if match:
            section = match.group(1)
            assert "feasibility" not in section.lower(), (
                "Reference Files still lists feasibility-related entries"
            )

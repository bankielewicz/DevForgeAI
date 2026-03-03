"""
Test: AC#1 - Phase 3 (Complexity Assessment) Removed from SKILL.md
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


class TestAC1Phase3Removed:
    """Verify Phase 3 (Complexity Assessment) is fully removed from SKILL.md."""

    def test_ac1_no_phase3_complexity_header(self, skill_content):
        """AC1(a): No 'Phase 3: Complexity Assessment' header exists in SKILL.md."""
        # Phase 3 should NOT reference Complexity Assessment (it's now Requirements Documentation)
        # Match markdown headers like "## Phase 3: Complexity" or "### Phase 3: Complexity Assessment"
        matches = re.findall(r"^#{1,4}\s+.*Phase\s+3.*[Cc]omplexity", skill_content, re.MULTILINE)
        assert len(matches) == 0, (
            f"Phase 3 Complexity Assessment header(s) still present in SKILL.md: {matches}"
        )

    def test_ac1_no_complexity_assessment_workflow_ref(self, skill_content):
        """AC1(b): No references to 'complexity-assessment-workflow.md' in phase definitions."""
        assert "complexity-assessment-workflow.md" not in skill_content, (
            "Reference to complexity-assessment-workflow.md still present in SKILL.md"
        )

    def test_ac1_description_no_complexity_assessment(self, skill_content):
        """AC1(c): SKILL.md description no longer mentions 'complexity assessment'."""
        assert "complexity assessment" not in skill_content.lower(), (
            "SKILL.md still mentions 'complexity assessment'"
        )

    def test_ac1_success_criteria_no_complexity_tier(self, skill_content):
        """AC1(d): Success Criteria section no longer includes complexity tier validation."""
        # Extract Success Criteria section
        match = re.search(
            r"##\s+Success\s+Criteria(.*?)(?=\n##\s|\Z)",
            skill_content,
            re.DOTALL | re.IGNORECASE,
        )
        if match:
            section = match.group(1)
            assert "complexity" not in section.lower(), (
                "Success Criteria still references complexity"
            )
            assert "tier" not in section.lower() or "complexity" not in skill_content.lower(), (
                "Success Criteria still references complexity tiers"
            )

    def test_ac1_reference_files_no_complexity_entries(self, skill_content):
        """AC1(e): Reference Files section removes complexity-related entries."""
        match = re.search(
            r"##\s+Reference\s+Files(.*?)(?=\n##\s|\Z)",
            skill_content,
            re.DOTALL | re.IGNORECASE,
        )
        if match:
            section = match.group(1)
            assert "complexity-assessment" not in section, (
                "Reference Files still lists complexity-assessment entries"
            )

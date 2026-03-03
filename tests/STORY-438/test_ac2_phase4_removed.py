"""
Test: AC#2 - Phase 4 (Epic & Feature Decomposition) Removed from SKILL.md
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


class TestAC2Phase4Removed:
    """Verify Phase 4 (Epic & Feature Decomposition) is fully removed from SKILL.md."""

    def test_ac2_no_phase4_header(self, skill_content):
        """AC2(a): No 'Phase 4' header exists in SKILL.md."""
        matches = re.findall(r"^#{1,4}\s+.*Phase\s+4\b", skill_content, re.MULTILINE)
        assert len(matches) == 0, (
            f"Phase 4 header(s) still present in SKILL.md: {matches}"
        )

    def test_ac2_no_epic_decomposition_workflow_ref(self, skill_content):
        """AC2(b): No references to 'epic-decomposition-workflow.md' in phase definitions."""
        assert "epic-decomposition-workflow.md" not in skill_content, (
            "Reference to epic-decomposition-workflow.md still present in SKILL.md"
        )

    def test_ac2_success_criteria_no_epic_count(self, skill_content):
        """AC2(c): Success Criteria section no longer includes '1-3 epics with 3-8 features each'."""
        assert "1-3 epics" not in skill_content, (
            "SKILL.md still mentions '1-3 epics'"
        )
        assert "3-8 features" not in skill_content, (
            "SKILL.md still mentions '3-8 features'"
        )

    def test_ac2_when_to_use_no_epic_creation(self, skill_content):
        """AC2(d): When to Use section no longer mentions 'epic creation'."""
        match = re.search(
            r"##\s+When\s+to\s+Use(.*?)(?=\n##\s|\Z)",
            skill_content,
            re.DOTALL | re.IGNORECASE,
        )
        if match:
            section = match.group(1)
            assert "epic creation" not in section.lower(), (
                "When to Use section still mentions 'epic creation'"
            )

    def test_ac2_reference_files_no_epic_decomposition(self, skill_content):
        """AC2(e): Reference Files section removes epic-decomposition entry."""
        match = re.search(
            r"##\s+Reference\s+Files(.*?)(?=\n##\s|\Z)",
            skill_content,
            re.DOTALL | re.IGNORECASE,
        )
        if match:
            section = match.group(1)
            assert "epic-decomposition" not in section, (
                "Reference Files still lists epic-decomposition entry"
            )

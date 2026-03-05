"""
Test: AC#4 - Skill Size Compliance
Story: STORY-537
Generated: 2026-03-05

Validates that src/claude/skills/researching-market/SKILL.md
remains under 1,000 lines after interview phase addition.
"""
import os
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SKILL_FILE = os.path.join(
    PROJECT_ROOT, "src", "claude", "skills", "researching-market", "SKILL.md"
)


class TestSkillSizeCompliance:
    """Verify SKILL.md remains under 1,000 lines."""

    def test_should_exist(self):
        """AC4: SKILL.md must exist."""
        assert os.path.isfile(SKILL_FILE), f"SKILL.md not found at {SKILL_FILE}"

    def test_should_be_under_1000_lines(self, skill_content):
        """AC4: SKILL.md must be under 1,000 lines."""
        line_count = len(skill_content.splitlines())
        assert line_count < 1000, (
            f"SKILL.md has {line_count} lines, must be under 1,000"
        )

    def test_should_contain_interview_question_phase(self, skill_content):
        """AC4: SKILL.md must contain the interview question generation phase."""
        assert "interview" in skill_content.lower(), (
            "SKILL.md does not contain an interview question generation phase"
        )

    def test_should_reference_customer_interview_guide(self, skill_content):
        """AC4: SKILL.md must reference customer-interview-guide.md for deep docs."""
        assert "customer-interview-guide" in skill_content.lower(), (
            "SKILL.md does not reference customer-interview-guide.md"
        )

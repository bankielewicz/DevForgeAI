"""
Test: AC#3 - Epic-Related Subagent References Removed
Story: STORY-437
TDD Phase: RED - All tests should FAIL before implementation.

Verifies that Subagent Coordination in SKILL.md lists only 2 subagents
(sprint-planner, technical-debt-analyzer) and epic-related subagents
are removed.
"""
import re
import pytest


class TestSubagentCoordinationCount:
    """Verify Subagent Coordination lists only 2 subagents."""

    def test_should_list_2_subagents_not_4_when_skill_read(self, skill_md_content):
        """Subagent count must be 2, not 4."""
        assert "4 subagents" not in skill_md_content, (
            "SKILL.md still references '4 subagents'"
        )
        assert "2 subagents" in skill_md_content, (
            "SKILL.md does not reference '2 subagents'"
        )


class TestRequirementsAnalystRemoved:
    """Verify requirements-analyst not listed as orchestration subagent."""

    def test_should_not_list_requirements_analyst_as_subagent_when_skill_read(self, skill_md_content):
        """requirements-analyst must not be listed as orchestration subagent."""
        # Look for requirements-analyst in subagent coordination context
        # Find the Subagent Coordination section
        subagent_section = re.search(
            r"(?i)subagent\s+coordination.*?(?=\n##\s|\Z)",
            skill_md_content,
            re.DOTALL,
        )
        if subagent_section:
            section_text = subagent_section.group(0)
            assert "requirements-analyst" not in section_text, (
                "requirements-analyst still listed in Subagent Coordination"
            )
        else:
            # If no section found, check the whole file
            assert "requirements-analyst" not in skill_md_content, (
                "requirements-analyst still referenced in SKILL.md"
            )


class TestArchitectReviewerRemoved:
    """Verify architect-reviewer not listed as orchestration subagent."""

    def test_should_not_list_architect_reviewer_as_subagent_when_skill_read(self, skill_md_content):
        """architect-reviewer must not be listed as orchestration subagent."""
        subagent_section = re.search(
            r"(?i)subagent\s+coordination.*?(?=\n##\s|\Z)",
            skill_md_content,
            re.DOTALL,
        )
        if subagent_section:
            section_text = subagent_section.group(0)
            assert "architect-reviewer" not in section_text, (
                "architect-reviewer still listed in Subagent Coordination"
            )
        else:
            assert "architect-reviewer" not in skill_md_content, (
                "architect-reviewer still referenced in SKILL.md"
            )


class TestRetainedSubagentsPresent:
    """Verify sprint-planner and technical-debt-analyzer remain."""

    def test_should_list_sprint_planner_when_skill_read(self, skill_md_content):
        """sprint-planner must be listed."""
        assert "sprint-planner" in skill_md_content, (
            "sprint-planner missing from SKILL.md"
        )

    def test_should_list_technical_debt_analyzer_when_skill_read(self, skill_md_content):
        """technical-debt-analyzer must be listed."""
        assert "technical-debt-analyzer" in skill_md_content, (
            "technical-debt-analyzer missing from SKILL.md"
        )

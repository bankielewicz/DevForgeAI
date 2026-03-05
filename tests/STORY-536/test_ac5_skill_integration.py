"""AC#5: Skill Phase Integration
Story: STORY-536
Tests that SKILL.md references competitive analysis and invokes market-analyst.
"""
import os
import re
import pytest


class TestSkillFileExists:
    """Verify SKILL.md exists at correct path."""

    def test_skill_file_exists(self, skill_path):
        assert os.path.isfile(skill_path), (
            f"SKILL.md not found at {skill_path}"
        )


class TestSkillReferencesCompetitiveAnalysis:
    """SKILL.md must reference competitive analysis phase."""

    def test_skill_mentions_competitive_analysis(self, skill_content):
        assert skill_content, "SKILL.md is empty or missing"
        assert re.search(r"(?i)competitive\s+analysis", skill_content), (
            "SKILL.md must reference a competitive analysis phase"
        )


class TestSkillLineLimit:
    """SKILL.md must be under 1,000 lines."""

    def test_under_1000_lines(self, skill_content):
        assert skill_content, "SKILL.md is empty or missing"
        line_count = len(skill_content.split("\n"))
        assert line_count < 1000, (
            f"SKILL.md has {line_count} lines, must be under 1,000"
        )


class TestSkillInvokesMarketAnalyst:
    """Phase must invoke market-analyst subagent."""

    def test_skill_references_market_analyst(self, skill_content):
        assert skill_content, "SKILL.md is empty or missing"
        assert re.search(r"(?i)market.analyst", skill_content), (
            "SKILL.md must reference the market-analyst subagent"
        )

    def test_skill_invokes_market_analyst_subagent(self, skill_content):
        assert skill_content, "SKILL.md is empty or missing"
        # Must contain Task() invocation specifically for market-analyst
        has_task_market_analyst = re.search(
            r'Task\s*\([^)]*market.analyst', skill_content, re.DOTALL
        )
        has_subagent_ref = re.search(
            r'(?i)subagent_type\s*=\s*["\']market-analyst["\']', skill_content
        )
        assert has_task_market_analyst or has_subagent_ref, (
            "SKILL.md must invoke market-analyst subagent via Task(subagent_type='market-analyst')"
        )

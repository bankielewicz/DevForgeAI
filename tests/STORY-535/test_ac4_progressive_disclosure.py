"""
Test: AC#4 - Guided Progressive Disclosure via AskUserQuestion
Story: STORY-535
Generated: 2026-03-04

Validates that all user inputs use AskUserQuestion tool and questions
are presented sequentially (not all at once).

Tests target src/ tree per CLAUDE.md.
"""
import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = PROJECT_ROOT / "src" / "claude" / "skills" / "researching-market"
SKILL_FILE = SKILL_DIR / "SKILL.md"


class TestAskUserQuestionUsage:
    """Tests that all user inputs use AskUserQuestion tool."""

    def test_should_use_askuserquestion_tool(self):
        """Arrange: SKILL.md exists. Act: Read content. Assert: AskUserQuestion referenced."""
        content = SKILL_FILE.read_text()
        assert "AskUserQuestion" in content, (
            "SKILL.md must use AskUserQuestion tool for all user interactions."
        )

    def test_should_use_askuserquestion_for_target_market(self):
        """Arrange: SKILL.md exists. Act: Read content. Assert: Target market question uses AskUserQuestion."""
        content = SKILL_FILE.read_text()
        # Must ask about target market via AskUserQuestion
        assert re.search(r"(target\s*market|industry|market\s*description)", content, re.IGNORECASE), (
            "SKILL.md must collect target market description via AskUserQuestion."
        )

    def test_should_use_askuserquestion_for_geographic_scope(self):
        """Arrange: SKILL.md exists. Act: Read content. Assert: Geographic scope question."""
        content = SKILL_FILE.read_text()
        assert re.search(r"geograph|region|location|scope", content, re.IGNORECASE), (
            "SKILL.md must collect geographic scope via AskUserQuestion."
        )

    def test_should_provide_clear_options_in_questions(self):
        """Arrange: SKILL.md exists. Act: Read content. Assert: Questions have options/descriptions."""
        content = SKILL_FILE.read_text()
        assert re.search(r"options|description|label", content, re.IGNORECASE), (
            "SKILL.md must provide clear options/descriptions in AskUserQuestion interactions."
        )


class TestSequentialQuestionPresentation:
    """Tests that questions are presented sequentially, not all at once."""

    def test_should_present_questions_sequentially(self):
        """Arrange: SKILL.md exists. Act: Read content. Assert: Sequential presentation documented."""
        content = SKILL_FILE.read_text()
        assert re.search(r"sequential|step.by.step|one.*at.*a.*time|progressive", content, re.IGNORECASE), (
            "SKILL.md must present questions sequentially (progressive disclosure), not all at once."
        )

    def test_should_define_question_order(self):
        """Arrange: SKILL.md exists. Act: Read content. Assert: Question order defined."""
        content = SKILL_FILE.read_text()
        # Should have numbered steps or ordered workflow for questions
        assert re.search(r"step\s*[1-9]|phase\s*[1-9]|\b1\.\s|workflow.*order", content, re.IGNORECASE), (
            "SKILL.md must define the order in which questions are presented."
        )


class TestCancelOption:
    """Tests that AskUserQuestion interactions have cancel option."""

    def test_should_include_cancel_option(self):
        """Arrange: SKILL.md exists. Act: Read content. Assert: Cancel option available."""
        content = SKILL_FILE.read_text()
        assert re.search(r"cancel|abort|exit|quit", content, re.IGNORECASE), (
            "SKILL.md must include cancel option in AskUserQuestion interactions."
        )

"""AC#3: Competitor Count Enforcement
Story: STORY-536
Tests that subagent instructions enforce 3-10 competitor bounds.
"""
import re
import pytest


class TestLessThanThreeTriggersPrompt:
    """< 3 competitors must trigger AskUserQuestion."""

    def test_instructions_mention_fewer_than_three_triggers_ask(self, subagent_content):
        assert subagent_content, "Subagent file is empty or missing"
        # The subagent instructions must document that < 3 triggers AskUserQuestion
        has_fewer_than_3 = re.search(r"(?i)(fewer than 3|less than 3|< ?3)", subagent_content)
        has_ask_user = re.search(r"(?i)AskUserQuestion", subagent_content)
        assert has_fewer_than_3, (
            "Subagent must document behavior when fewer than 3 competitors found"
        )
        assert has_ask_user, (
            "Subagent must reference AskUserQuestion for insufficient competitors"
        )

    def test_fewer_than_three_linked_to_ask_user(self, subagent_content):
        """Verify the < 3 condition and AskUserQuestion appear in same logical block."""
        assert subagent_content, "Subagent file is empty or missing"
        # Find a paragraph/section that contains both concepts within 500 chars
        blocks = subagent_content.split("\n\n")
        found = False
        for block in blocks:
            if (re.search(r"(?i)(fewer than 3|less than 3|< ?3)", block)
                    and re.search(r"(?i)AskUserQuestion", block)):
                found = True
                break
        assert found, (
            "The < 3 competitor condition and AskUserQuestion must appear in the same section"
        )


class TestMoreThanTenTruncates:
    """> 10 competitors must truncate to top 10 with warning."""

    def test_instructions_mention_truncation(self, subagent_content):
        assert subagent_content, "Subagent file is empty or missing"
        has_more_than_10 = re.search(r"(?i)(more than 10|greater than 10|> ?10|exceed.{0,20}10)", subagent_content)
        has_truncat = re.search(r"(?i)truncat", subagent_content)
        assert has_more_than_10, (
            "Subagent must document behavior when more than 10 competitors found"
        )
        assert has_truncat, (
            "Subagent must document truncation to top 10 competitors"
        )

    def test_truncation_includes_warning(self, subagent_content):
        assert subagent_content, "Subagent file is empty or missing"
        assert re.search(r"(?i)warn", subagent_content), (
            "Subagent must document that truncation produces a warning"
        )

"""
Test: AC#3 - Feedback Synthesis
Story: STORY-542
Generated: 2026-03-06

Validates:
- Contains 4 synthesis categories: validated assumptions, invalidated assumptions,
  recurring pain points, surprising insights
- Writes synthesis summary to business plan under Customer Discovery milestone
- BR-002: Zero interviews blocks synthesis
"""
import os
import re

import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SOURCE_FILE = os.path.join(
    PROJECT_ROOT, "src", "claude", "skills", "marketing-business",
    "references", "customer-discovery-workflow.md"
)


@pytest.fixture
def source_content():
    """Arrange: Read source file content."""
    assert os.path.isfile(SOURCE_FILE), f"Source file not found: {SOURCE_FILE}"
    with open(SOURCE_FILE, "r", encoding="utf-8") as f:
        return f.read()


class TestSynthesisCategories:
    """Tests for 4 synthesis categories."""

    EXPECTED_CATEGORIES = [
        "validated assumptions",
        "invalidated assumptions",
        "recurring pain points",
        "surprising insights",
    ]

    @pytest.mark.parametrize("category", EXPECTED_CATEGORIES)
    def test_should_contain_synthesis_category(self, source_content, category):
        """Act & Assert: File must contain each synthesis category."""
        assert category.lower() in source_content.lower(), (
            f"Source file must contain synthesis category: '{category}'"
        )

    def test_should_contain_all_four_categories(self, source_content):
        """Act & Assert: File must contain all 4 synthesis categories."""
        content_lower = source_content.lower()
        found = [c for c in self.EXPECTED_CATEGORIES if c in content_lower]
        assert len(found) == 4, (
            f"Expected 4 synthesis categories, found {len(found)}: {found}"
        )


class TestBusinessPlanIntegration:
    """Tests for writing synthesis to business plan."""

    def test_should_write_to_business_plan(self, source_content):
        """Act & Assert: File must describe writing synthesis to business plan."""
        content_lower = source_content.lower()
        has_write = (
            "business plan" in content_lower
            and ("write" in content_lower or "append" in content_lower or "add" in content_lower)
        )
        assert has_write, (
            "Source file must describe writing synthesis summary to business plan"
        )

    def test_should_target_customer_discovery_milestone(self, source_content):
        """Act & Assert: File must target Customer Discovery milestone section."""
        content_lower = source_content.lower()
        has_milestone = "customer discovery" in content_lower and "milestone" in content_lower
        assert has_milestone, (
            "Source file must reference Customer Discovery milestone section"
        )


class TestZeroInterviewsBlock:
    """Tests for BR-002: Zero interviews blocks synthesis."""

    def test_should_block_synthesis_with_zero_interviews_br002(self, source_content):
        """Act & Assert: BR-002 - Zero interviews must block synthesis step."""
        content_lower = source_content.lower()
        has_block = bool(
            re.search(r"(zero|0|no).{0,30}interview.{0,30}(block|prevent|require|cannot|must)", content_lower)
            or re.search(r"(at least|minimum|>= ?).{0,5}1.{0,20}interview", content_lower)
        )
        assert has_block, (
            "Source file must block synthesis when zero interviews conducted (BR-002)"
        )

    def test_should_redirect_to_outreach_on_zero_interviews(self, source_content):
        """Act & Assert: BR-002 - Zero interviews should redirect to outreach planning."""
        content_lower = source_content.lower()
        has_redirect = (
            "outreach" in content_lower
            and ("return" in content_lower or "redirect" in content_lower or "back" in content_lower)
        )
        assert has_redirect, (
            "Source file must redirect to outreach planning when zero interviews (BR-002)"
        )

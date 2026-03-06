"""
Test: AC#4 - Milestone Tracking
Story: STORY-542
Generated: 2026-03-06

Validates:
- Milestone section contains: completion date (YYYY-MM-DD pattern), interview count (>= 1),
  top 3 validated assumptions, top 3 invalidated assumptions, discovery confidence score (0-100%)
- BR-003: Duplicate milestone triggers user prompt with 3 options
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


class TestMilestoneFields:
    """Tests for required milestone fields."""

    def test_should_include_completion_date_format(self, source_content):
        """Act & Assert: Milestone must include YYYY-MM-DD date format."""
        has_date = bool(re.search(r"YYYY-MM-DD", source_content))
        assert has_date, (
            "Source file must specify YYYY-MM-DD date format for completion date"
        )

    def test_should_include_interview_count(self, source_content):
        """Act & Assert: Milestone must include interview count field."""
        content_lower = source_content.lower()
        has_count = (
            "interview" in content_lower
            and ("count" in content_lower or "number" in content_lower or "conducted" in content_lower)
        )
        assert has_count, (
            "Source file must include interview count in milestone"
        )

    def test_should_include_top_three_validated_assumptions(self, source_content):
        """Act & Assert: Milestone must include top 3 validated assumptions."""
        has_validated = bool(
            re.search(r"(top.{0,5}3|three).{0,20}validated", source_content, re.IGNORECASE)
        )
        assert has_validated, (
            "Source file must include top 3 validated assumptions in milestone"
        )

    def test_should_include_top_three_invalidated_assumptions(self, source_content):
        """Act & Assert: Milestone must include top 3 invalidated assumptions."""
        has_invalidated = bool(
            re.search(r"(top.{0,5}3|three).{0,20}invalidated", source_content, re.IGNORECASE)
        )
        assert has_invalidated, (
            "Source file must include top 3 invalidated assumptions in milestone"
        )

    def test_should_include_confidence_score(self, source_content):
        """Act & Assert: Milestone must include discovery confidence score (0-100%)."""
        content_lower = source_content.lower()
        has_confidence = (
            "confidence" in content_lower
            and ("score" in content_lower or "%" in source_content or "percent" in content_lower)
        )
        assert has_confidence, (
            "Source file must include discovery confidence score (0-100%)"
        )

    def test_should_calculate_confidence_from_ratio(self, source_content):
        """Act & Assert: Confidence score derived from validated/total ratio."""
        content_lower = source_content.lower()
        has_ratio = bool(
            re.search(r"(validated.{0,20}total|ratio|validated.{0,10}/)", content_lower)
        )
        assert has_ratio, (
            "Source file must calculate confidence score from validated/total ratio"
        )


class TestDuplicateMilestone:
    """Tests for BR-003: Duplicate milestone triggers user prompt."""

    def test_should_detect_existing_milestone_br003(self, source_content):
        """Act & Assert: BR-003 - File must check for existing milestone section."""
        content_lower = source_content.lower()
        has_detect = (
            "exist" in content_lower or "duplicate" in content_lower or "already" in content_lower
        ) and "milestone" in content_lower
        assert has_detect, (
            "Source file must detect existing/duplicate milestone section (BR-003)"
        )

    def test_should_offer_three_options_on_duplicate_br003(self, source_content):
        """Act & Assert: BR-003 - Duplicate milestone must offer 3 options."""
        content_lower = source_content.lower()
        has_append = "append" in content_lower
        has_replace = "replace" in content_lower or "overwrite" in content_lower
        has_cancel = "cancel" in content_lower or "abort" in content_lower
        options_found = sum([has_append, has_replace, has_cancel])
        assert options_found >= 3, (
            f"Source file must offer 3 options (append/replace/cancel) on duplicate milestone, "
            f"found {options_found} (BR-003)"
        )

    def test_should_not_silently_overwrite_br003(self, source_content):
        """Act & Assert: BR-003 - Must not silently overwrite existing milestone."""
        content_lower = source_content.lower()
        has_no_silent = (
            "prompt" in content_lower
            or "ask" in content_lower
            or "choose" in content_lower
            or "user" in content_lower
        )
        assert has_no_silent, (
            "Source file must prompt user (no silent overwrite) on duplicate milestone (BR-003)"
        )

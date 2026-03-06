"""
Test: AC#2 - Fallback Interview Templates
Story: STORY-542
Generated: 2026-03-06

Validates:
- Contains fallback warning message "Market research outputs not found"
- Loads 5 core discovery topics as fallback
- Continues without halting (no HALT on missing EPIC-074)
- BR-001: Missing EPIC-074 triggers fallback
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


class TestFallbackWarningMessage:
    """Tests for fallback warning display."""

    def test_should_contain_fallback_warning_message(self, source_content):
        """Act & Assert: File must contain the exact fallback warning text."""
        assert "Market research outputs not found" in source_content, (
            "Source file must contain warning: 'Market research outputs not found'"
        )

    def test_should_indicate_proceeding_with_defaults(self, source_content):
        """Act & Assert: Warning must indicate proceeding with default templates."""
        content_lower = source_content.lower()
        has_proceed = (
            "default" in content_lower
            and ("template" in content_lower or "fallback" in content_lower)
        )
        assert has_proceed, (
            "Source file must indicate proceeding with default/fallback templates"
        )


class TestFallbackTopics:
    """Tests for 5 core discovery topics as fallback."""

    def test_should_contain_five_fallback_topics(self, source_content):
        """Act & Assert: File must define 5 core discovery fallback topics."""
        # Look for a numbered or bulleted list of fallback topics
        content_lower = source_content.lower()
        has_five = bool(
            re.search(r"(5|five).{0,20}(topic|template|question|fallback)", content_lower)
        )
        assert has_five, (
            "Source file must define 5 core discovery topics as fallback"
        )

    def test_should_contain_fallback_section(self, source_content):
        """Act & Assert: File must have a dedicated fallback section."""
        content_lower = source_content.lower()
        has_fallback_section = (
            "fallback" in content_lower
            and ("template" in content_lower or "topic" in content_lower)
        )
        assert has_fallback_section, (
            "Source file must have a fallback templates/topics section"
        )


class TestNoHaltOnMissing:
    """Tests for BR-001: No HALT when EPIC-074 missing."""

    def test_should_not_halt_when_epic074_missing_br001(self, source_content):
        """Act & Assert: BR-001 - File must not HALT when EPIC-074 outputs missing."""
        # The workflow should explicitly state it continues without halting
        content_lower = source_content.lower()
        has_continue = (
            "continue" in content_lower
            or "proceed" in content_lower
            or "graceful" in content_lower
        )
        assert has_continue, (
            "Source file must indicate graceful continuation without HALT (BR-001)"
        )

    def test_should_describe_graceful_degradation(self, source_content):
        """Act & Assert: File must describe graceful degradation behavior."""
        content_lower = source_content.lower()
        has_degradation = (
            "graceful" in content_lower
            or "degradation" in content_lower
            or "fallback" in content_lower
        )
        assert has_degradation, (
            "Source file must describe graceful degradation for missing EPIC-074"
        )

"""
Test: AC#2 - Social Media Presence Guide
Story: STORY-543
Generated: 2026-03-06

Validates:
- Platform recommendation list with minimum 3 platforms
- Each platform has recommended/optional/skip designation
- Basic posting cadence table with posts-per-week
- Brief rationale (1-3 sentences) per platform
"""
import os
import re

import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SOURCE_FILE = os.path.join(
    PROJECT_ROOT, "src", "claude", "skills", "marketing-business",
    "references", "content-channel-strategy.md"
)


@pytest.fixture
def source_content():
    """Arrange: Read source file content."""
    assert os.path.isfile(SOURCE_FILE), f"Source file not found: {SOURCE_FILE}"
    with open(SOURCE_FILE, "r", encoding="utf-8") as f:
        return f.read()


class TestPlatformRecommendations:
    """Tests for platform recommendation list."""

    def test_should_list_at_least_3_platforms(self, source_content):
        """Act & Assert: At least 3 social media platforms must be listed."""
        platforms = [
            "twitter", "x\\.com", "linkedin", "instagram", "facebook",
            "youtube", "tiktok", "reddit", "pinterest", "threads",
            "mastodon", "bluesky", "medium", "substack", "discord",
        ]
        found_platforms = []
        for platform in platforms:
            if re.search(platform, source_content, re.IGNORECASE):
                found_platforms.append(platform)
        assert len(found_platforms) >= 3, (
            f"Expected at least 3 platforms, found {len(found_platforms)}: {found_platforms}"
        )

    def test_should_have_recommendation_designations(self, source_content):
        """Act & Assert: Platforms must have recommended/optional/skip designations."""
        content_lower = source_content.lower()
        has_recommended = "recommended" in content_lower or "priority" in content_lower
        has_optional = "optional" in content_lower or "consider" in content_lower
        has_skip = "skip" in content_lower or "not recommended" in content_lower or "avoid" in content_lower
        designation_count = sum([has_recommended, has_optional, has_skip])
        assert designation_count >= 2, (
            "Platforms must have at least 2 of: recommended, optional, skip designations"
        )


class TestPostingCadenceTable:
    """Tests for posting cadence with numeric values."""

    def test_should_have_cadence_with_numeric_values(self, source_content):
        """Act & Assert: Cadence table must have numeric posts-per-week values."""
        # Look for patterns like "3-5 posts" or "| 3 |" or "2x per week"
        numeric_cadence = re.findall(
            r"\d+(?:\s*[-–]\s*\d+)?\s*(?:posts?|times?|x)\s*(?:per|/)\s*(?:week|month|day)",
            source_content, re.IGNORECASE
        )
        # Also match table cells with numbers
        table_numeric = re.findall(
            r"\|[^|]*\d+[^|]*(?:per|/|week|month|daily)[^|]*\|",
            source_content, re.IGNORECASE
        )
        total = len(numeric_cadence) + len(table_numeric)
        assert total >= 3, (
            f"Expected at least 3 numeric cadence entries, found {total}"
        )


class TestPlatformRationale:
    """Tests for platform rationale (1-3 sentences per platform)."""

    def test_should_have_rationale_text(self, source_content):
        """Act & Assert: File must contain rationale/reason text for platforms."""
        content_lower = source_content.lower()
        has_rationale = (
            "rationale" in content_lower
            or "reason" in content_lower
            or "why" in content_lower
            or "because" in content_lower
            or "best for" in content_lower
            or "ideal for" in content_lower
        )
        assert has_rationale, (
            "File must contain rationale text explaining platform recommendations"
        )

    def test_should_have_rationale_per_recommended_platform(self, source_content):
        """Act & Assert: Each platform section should have explanatory text (sentences with periods)."""
        # Find platform-related sections and check for sentence-level content
        platform_sections = re.split(
            r"#{2,4}\s+.*(?:Twitter|LinkedIn|Instagram|Facebook|YouTube|TikTok|Reddit|X\.com|Medium)",
            source_content, flags=re.IGNORECASE
        )
        sections_with_rationale = 0
        for section in platform_sections[1:]:  # Skip content before first platform
            # A rationale has at least one sentence (text ending with period)
            sentences = re.findall(r"[A-Z][^.!?]*[.!?]", section[:500])
            if len(sentences) >= 1:
                sections_with_rationale += 1
        assert sections_with_rationale >= 2, (
            f"Expected rationale for at least 2 platforms, found {sections_with_rationale}"
        )

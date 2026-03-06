"""
Test: AC#1 - Content Strategy Skeleton Generation
Story: STORY-543
Generated: 2026-03-06

Validates:
- Source file exists at expected path
- Contains content topic skeleton with at least 3 topic categories
- Contains posting frequency table per channel
- Contains channel selection guide with platform priorities
- File is under 500 lines (BR-001)
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


@pytest.fixture
def source_lines(source_content):
    """Arrange: Split source file into lines."""
    return source_content.splitlines()


class TestSourceFileExists:
    """Tests for source file existence."""

    def test_should_exist_at_expected_path(self):
        """Act & Assert: content-channel-strategy.md must exist."""
        assert os.path.isfile(SOURCE_FILE), (
            f"Expected source file at {SOURCE_FILE}"
        )


class TestContentTopicSkeleton:
    """Tests for content topic categories (minimum 3)."""

    def test_should_contain_topic_section(self, source_content):
        """Act & Assert: File must contain a topic/content categories section."""
        content_lower = source_content.lower()
        has_topics = (
            "topic" in content_lower
            and ("categor" in content_lower or "theme" in content_lower)
        )
        assert has_topics, (
            "File must contain a content topic categories section"
        )

    def test_should_have_at_least_3_topic_categories(self, source_content):
        """Act & Assert: At least 3 distinct topic categories must be present."""
        # Match markdown headers or bold items that indicate categories
        category_patterns = [
            r"#{2,4}\s+.*(?:educational|promotional|community|thought\s*leadership|behind.the.scenes|product|tutorial|industry|engagement|entertainment|case.stud)",
            r"\*\*(?:educational|promotional|community|thought\s*leadership|behind.the.scenes|product|tutorial|industry|engagement|entertainment|case.stud)",
        ]
        categories_found = set()
        for pattern in category_patterns:
            matches = re.findall(pattern, source_content, re.IGNORECASE)
            for m in matches:
                categories_found.add(m.strip().lower())

        # Alternative: count numbered or bulleted category sections
        category_header_pattern = r"#{2,4}\s+\d*\.?\s*\w+.*(?:Content|Topic|Category)"
        alt_matches = re.findall(category_header_pattern, source_content, re.IGNORECASE)

        total_categories = max(len(categories_found), len(alt_matches))
        assert total_categories >= 3, (
            f"Expected at least 3 topic categories, found {total_categories}"
        )


class TestPostingFrequencyTable:
    """Tests for posting frequency table."""

    def test_should_contain_frequency_section(self, source_content):
        """Act & Assert: File must contain posting frequency/cadence section."""
        content_lower = source_content.lower()
        has_frequency = (
            ("frequency" in content_lower or "cadence" in content_lower)
            and ("post" in content_lower or "publish" in content_lower)
        )
        assert has_frequency, (
            "File must contain a posting frequency/cadence section"
        )

    def test_should_contain_markdown_table_with_frequency(self, source_content):
        """Act & Assert: File must have a markdown table with numeric frequency values."""
        # Match markdown table rows with numeric values (posts per week/month)
        table_row_pattern = r"\|[^|]+\|[^|]*\d+[^|]*\|"
        matches = re.findall(table_row_pattern, source_content)
        assert len(matches) >= 3, (
            f"Expected frequency table with at least 3 rows of data, found {len(matches)}"
        )


class TestChannelSelectionGuide:
    """Tests for channel selection guide."""

    def test_should_contain_channel_selection_section(self, source_content):
        """Act & Assert: File must contain channel selection/platform guide."""
        content_lower = source_content.lower()
        has_channel = (
            ("channel" in content_lower or "platform" in content_lower)
            and ("select" in content_lower or "guide" in content_lower or "recommend" in content_lower)
        )
        assert has_channel, (
            "File must contain a channel selection guide section"
        )


class TestFileSizeLimit:
    """Tests for BR-001: Output file under 500 lines."""

    def test_should_be_under_500_lines(self, source_lines):
        """Act & Assert: File must not exceed 500 lines."""
        line_count = len(source_lines)
        assert line_count <= 500, (
            f"File has {line_count} lines, exceeds 500-line limit (BR-001)"
        )

    def test_should_be_valid_markdown(self, source_content):
        """Act & Assert: File must start with markdown heading or YAML frontmatter."""
        first_line = source_content.strip().split("\n")[0]
        is_heading = first_line.startswith("#")
        is_frontmatter = first_line.strip() == "---"
        assert is_heading or is_frontmatter, (
            f"File must start with markdown heading or YAML frontmatter, got: {first_line}"
        )

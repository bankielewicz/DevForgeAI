"""
Test: AC#3 - Topic Categories with Examples
Story: STORY-543
Generated: 2026-03-06

Validates:
- At least 3 content topic categories present
- Each category has 3-5 example topic ideas
- Each example labeled with recommended content type (blog, video, thread, etc.)
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
def topic_sections(source_content):
    """Arrange: Extract topic category sections from file."""
    # Split by category-level headers (## or ### with category keywords)
    sections = re.split(
        r"#{2,3}\s+\d*\.?\s*(?:Educational|Promotional|Community|Thought Leadership|Behind.the.Scenes|Product|Tutorial|Industry|Engagement|Entertainment|Case Stud)",
        source_content, flags=re.IGNORECASE
    )
    return sections[1:]  # Skip content before first category


class TestTopicCategoryCount:
    """Tests for minimum 3 topic categories."""

    def test_should_have_at_least_3_categories(self, topic_sections):
        """Act & Assert: File must contain at least 3 distinct topic categories."""
        assert len(topic_sections) >= 3, (
            f"Expected at least 3 topic categories, found {len(topic_sections)}"
        )


class TestExampleTopicIdeas:
    """Tests for 3-5 example topic ideas per category."""

    def test_should_have_examples_per_category(self, topic_sections):
        """Act & Assert: Each category must have at least 3 example topic ideas."""
        for i, section in enumerate(topic_sections):
            # Count bullet points or numbered items as examples
            examples = re.findall(r"^\s*[-*]\s+.{10,}", section, re.MULTILINE)
            numbered = re.findall(r"^\s*\d+\.\s+.{10,}", section, re.MULTILINE)
            total_examples = len(examples) + len(numbered)
            assert total_examples >= 3, (
                f"Category {i + 1} has {total_examples} examples, expected at least 3"
            )


class TestContentTypeLabels:
    """Tests for content type labels on examples."""

    def test_should_label_examples_with_content_type(self, source_content):
        """Act & Assert: Examples must include content type labels."""
        content_types = [
            "blog", "video", "short.form video", "thread", "carousel",
            "newsletter", "podcast", "infographic", "reel", "story",
            "post", "article", "guide", "tutorial", "webinar",
            "live stream", "case study", "whitepaper",
        ]
        found_types = set()
        for ct in content_types:
            if re.search(ct, source_content, re.IGNORECASE):
                found_types.add(ct)
        assert len(found_types) >= 3, (
            f"Expected at least 3 content type labels, found {len(found_types)}: {found_types}"
        )

    def test_should_associate_content_types_with_examples(self, source_content):
        """Act & Assert: Content types should appear near example topics (within same line or next line)."""
        # Match lines that have both an example (bullet/number) and a content type reference
        content_type_pattern = r"(?:blog|video|thread|carousel|newsletter|podcast|infographic|reel|article|guide|tutorial|post)"
        labeled_examples = re.findall(
            r"^\s*[-*\d.]+\s+.*" + content_type_pattern,
            source_content, re.MULTILINE | re.IGNORECASE
        )
        assert len(labeled_examples) >= 5, (
            f"Expected at least 5 examples with content type labels, found {len(labeled_examples)}"
        )

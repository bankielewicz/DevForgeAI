"""
Test: AC#4 - Minimal Input Handling
Story: STORY-543
Generated: 2026-03-06

Validates:
- Placeholder indicators present in [ALL_CAPS_WITH_UNDERSCORES] format
- Key placeholders: [YOUR_PRODUCT], [TARGET_AUDIENCE]
- Templated sections clearly marked for customization
- Generic but usable skeleton produced with sensible defaults
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


class TestPlaceholderFormat:
    """Tests for [ALL_CAPS_WITH_UNDERSCORES] placeholder format."""

    def test_should_contain_placeholders_in_correct_format(self, source_content):
        """Act & Assert: Placeholders must follow [ALL_CAPS_WITH_UNDERSCORES] format."""
        placeholder_pattern = r"\[(?:[A-Z]+_)*[A-Z]+\]"
        placeholders = re.findall(placeholder_pattern, source_content)
        assert len(placeholders) >= 2, (
            f"Expected at least 2 placeholders in [ALL_CAPS] format, found {len(placeholders)}: {placeholders}"
        )

    def test_should_contain_your_product_placeholder(self, source_content):
        """Act & Assert: Must contain [YOUR_PRODUCT] or equivalent product placeholder."""
        has_product = bool(re.search(
            r"\[YOUR_PRODUCT\]|\[PRODUCT_NAME\]|\[YOUR_PRODUCT_NAME\]",
            source_content
        ))
        assert has_product, (
            "File must contain [YOUR_PRODUCT] or [PRODUCT_NAME] placeholder"
        )

    def test_should_contain_target_audience_placeholder(self, source_content):
        """Act & Assert: Must contain [TARGET_AUDIENCE] or equivalent audience placeholder."""
        has_audience = bool(re.search(
            r"\[TARGET_AUDIENCE\]|\[YOUR_AUDIENCE\]|\[AUDIENCE\]|\[YOUR_TARGET_AUDIENCE\]",
            source_content
        ))
        assert has_audience, (
            "File must contain [TARGET_AUDIENCE] or equivalent placeholder"
        )


class TestTemplateNotices:
    """Tests for template customization notices."""

    def test_should_mark_customizable_sections(self, source_content):
        """Act & Assert: File must indicate which sections need customization."""
        content_lower = source_content.lower()
        has_customize_notice = (
            "customize" in content_lower
            or "replace" in content_lower
            or "fill in" in content_lower
            or "adapt" in content_lower
            or "tailor" in content_lower
            or "update with" in content_lower
        )
        assert has_customize_notice, (
            "File must contain notices indicating sections that need customization"
        )


class TestSensibleDefaults:
    """Tests for generic but usable skeleton with defaults."""

    def test_should_provide_default_topic_categories(self, source_content):
        """Act & Assert: Default categories should be present even without specific product input."""
        # Generic category types that work for any product
        generic_categories = [
            "educational", "promotional", "community",
            "thought leadership", "behind the scenes",
        ]
        found = sum(
            1 for cat in generic_categories
            if cat.lower() in source_content.lower()
        )
        assert found >= 3, (
            f"Expected at least 3 default topic categories, found {found}"
        )

    def test_should_not_contain_executable_code(self, source_content):
        """Act & Assert: No executable code or API references (BR-003)."""
        code_patterns = [
            r"import\s+\w+",
            r"require\s*\(",
            r"fetch\s*\(",
            r"axios\.",
            r"api_key",
            r"curl\s+",
        ]
        for pattern in code_patterns:
            matches = re.findall(pattern, source_content, re.IGNORECASE)
            assert len(matches) == 0, (
                f"File must not contain executable code. Found pattern '{pattern}': {matches}"
            )

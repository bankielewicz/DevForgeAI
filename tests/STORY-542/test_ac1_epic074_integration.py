"""
Test: AC#1 - EPIC-074 Integration with Graceful Degradation
Story: STORY-542
Generated: 2026-03-06

Validates:
- Source file exists at expected path
- Contains interview question loading section
- Questions organized by 3 themes: problem validation, solution fit, pricing
- Prompts user for at least 3 target customer segments
- BR-004: Maximum 10 customer segments
- NFR-002: Skill file under 1,000 lines
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


@pytest.fixture
def source_lines(source_content):
    """Arrange: Split source file into lines."""
    return source_content.splitlines()


class TestSourceFileExists:
    """Tests for source file existence."""

    def test_should_exist_at_expected_path(self):
        """Act & Assert: customer-discovery-workflow.md must exist at expected path."""
        assert os.path.isfile(SOURCE_FILE), (
            f"Expected source file at {SOURCE_FILE}"
        )


class TestInterviewQuestionLoading:
    """Tests for EPIC-074 interview question loading."""

    def test_should_contain_interview_loading_section(self, source_content):
        """Act & Assert: File must contain an interview question loading section."""
        content_lower = source_content.lower()
        has_loading = (
            "interview" in content_lower
            and ("load" in content_lower or "import" in content_lower)
        )
        assert has_loading, (
            "Source file must contain interview question loading section"
        )

    def test_should_reference_epic074_outputs(self, source_content):
        """Act & Assert: File must reference EPIC-074 outputs path."""
        assert "epic-074" in source_content.lower() or "EPIC-074" in source_content, (
            "Source file must reference EPIC-074 outputs"
        )


class TestThemeOrganization:
    """Tests for question organization by 3 themes."""

    EXPECTED_THEMES = [
        "problem validation",
        "solution fit",
        "pricing",
    ]

    @pytest.mark.parametrize("theme", EXPECTED_THEMES)
    def test_should_contain_theme(self, source_content, theme):
        """Act & Assert: File must organize questions by each theme."""
        assert theme.lower() in source_content.lower(), (
            f"Source file must contain theme: '{theme}'"
        )

    def test_should_contain_all_three_themes(self, source_content):
        """Act & Assert: File must contain all 3 themes."""
        content_lower = source_content.lower()
        found = [t for t in self.EXPECTED_THEMES if t in content_lower]
        assert len(found) == 3, (
            f"Expected 3 themes, found {len(found)}: {found}"
        )


class TestCustomerSegments:
    """Tests for customer segment prompting."""

    def test_should_prompt_for_customer_segments(self, source_content):
        """Act & Assert: File must prompt user to identify customer segments."""
        content_lower = source_content.lower()
        has_segments = "segment" in content_lower or "customer segment" in content_lower
        assert has_segments, (
            "Source file must prompt user to identify customer segments"
        )

    def test_should_require_minimum_three_segments(self, source_content):
        """Act & Assert: File must require at least 3 target customer segments."""
        # Look for minimum 3 segments requirement
        has_min_3 = bool(
            re.search(r"(at least 3|minimum.{0,10}3|>= ?3|3.{0,15}segment)", source_content, re.IGNORECASE)
        )
        assert has_min_3, (
            "Source file must require at least 3 customer segments"
        )

    def test_should_enforce_maximum_ten_segments_br004(self, source_content):
        """Act & Assert: BR-004 - File must enforce maximum 10 customer segments."""
        has_max_10 = bool(
            re.search(r"(maximum.{0,10}10|max.{0,10}10|<= ?10|10.{0,15}segment.{0,10}(limit|max))", source_content, re.IGNORECASE)
        )
        assert has_max_10, (
            "Source file must enforce maximum 10 customer segments (BR-004)"
        )


class TestFileSizeLimit:
    """Tests for NFR-002: Skill file under 1,000 lines."""

    def test_should_be_under_1000_lines_nfr002(self, source_lines):
        """Act & Assert: NFR-002 - File must be under 1,000 lines."""
        line_count = len(source_lines)
        assert line_count <= 999, (
            f"Source file has {line_count} lines, exceeds 999 line limit (NFR-002)"
        )

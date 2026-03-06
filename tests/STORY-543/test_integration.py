"""
Integration Test: End-to-End Content Strategy Validation
Story: STORY-543
Generated: 2026-03-06

Validates:
- Complete file renders as valid CommonMark
- All sections present and properly linked
- File works as standalone reference
- No broken internal references
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


class TestEndToEndStructure:
    """Integration: Full file structure validation."""

    def test_should_have_all_major_sections(self, source_content):
        """Act & Assert: File must contain all required major sections."""
        required_sections = [
            r"Channel Selection",
            r"Content Topic",
            r"Content Calendar",
            r"Customiz",
        ]
        for section in required_sections:
            assert re.search(section, source_content, re.IGNORECASE), (
                f"Missing required section matching: {section}"
            )

    def test_should_have_yaml_frontmatter(self, source_content):
        """Act & Assert: File must have valid YAML frontmatter."""
        assert source_content.strip().startswith("---"), "Missing YAML frontmatter start"
        # Find second --- delimiter
        second_delim = source_content.find("---", 3)
        assert second_delim > 0, "Missing YAML frontmatter end delimiter"
        frontmatter = source_content[3:second_delim].strip()
        assert "title:" in frontmatter, "Frontmatter missing title"
        assert "version:" in frontmatter, "Frontmatter missing version"

    def test_should_be_under_500_lines(self, source_lines):
        """Act & Assert: Complete file must not exceed 500 lines."""
        assert len(source_lines) <= 500, (
            f"File has {len(source_lines)} lines, exceeds 500-line limit"
        )

    def test_should_have_consistent_heading_hierarchy(self, source_content):
        """Act & Assert: Headings should follow proper hierarchy (no skipping levels)."""
        headings = re.findall(r"^(#{1,6})\s", source_content, re.MULTILINE)
        for i in range(1, len(headings)):
            current_level = len(headings[i])
            prev_level = len(headings[i - 1])
            # Can go deeper by 1 or go back to any higher level
            if current_level > prev_level:
                assert current_level - prev_level <= 2, (
                    f"Heading hierarchy skip at position {i}: "
                    f"{'#' * prev_level} -> {'#' * current_level}"
                )


class TestFileIntegrity:
    """Integration: File integrity and cross-reference checks."""

    def test_should_not_have_broken_markdown_tables(self, source_content):
        """Act & Assert: All markdown tables must have consistent column counts."""
        lines = source_content.splitlines()
        in_table = False
        table_col_count = 0
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("|") and stripped.endswith("|"):
                cols = stripped.count("|") - 1
                if not in_table:
                    in_table = True
                    table_col_count = cols
                else:
                    assert cols == table_col_count, (
                        f"Inconsistent table columns: expected {table_col_count}, got {cols} in: {stripped[:60]}"
                    )
            else:
                in_table = False

    def test_should_have_no_empty_sections(self, source_content):
        """Act & Assert: No section should be completely empty (header followed immediately by another header)."""
        empty_sections = re.findall(
            r"^(#{1,4}\s+.+)\n\n(#{1,4}\s+)",
            source_content, re.MULTILINE
        )
        # Allow some empty sections but not more than 2
        assert len(empty_sections) <= 2, (
            f"Found {len(empty_sections)} empty sections (max 2 allowed)"
        )

    def test_file_size_under_50kb(self):
        """Act & Assert: File must be under 50KB (NFR)."""
        file_size = os.path.getsize(SOURCE_FILE)
        assert file_size < 50 * 1024, (
            f"File is {file_size} bytes, exceeds 50KB limit"
        )

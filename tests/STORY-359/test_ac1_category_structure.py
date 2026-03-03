"""
STORY-359 AC#1: Category 11 Section Structure

Tests that Category 11 "Code Search Tool Selection" is added to anti-patterns.md
with correct positioning (after Category 10, before Anti-Pattern Detection Protocol),
follows existing format (SEVERITY, FORBIDDEN, Correct, Rationale), and version is
bumped from 1.0 to 1.1.

TDD Red Phase: These tests WILL FAIL because Category 11 does not exist yet
in anti-patterns.md.
"""
import re

import pytest
from pathlib import Path


ANTI_PATTERNS_FILE = Path(
    "/mnt/c/Projects/DevForgeAI2/devforgeai/specs/context/anti-patterns.md"
)


class TestAC1CategoryStructure:
    """AC#1: Category 11 must exist with correct structure and positioning."""

    # --- Happy Path ---

    def test_should_contain_category_11_header_when_section_added(self):
        """Category 11 header must exist in anti-patterns.md."""
        content = ANTI_PATTERNS_FILE.read_text()
        assert "### Category 11:" in content, (
            "Missing '### Category 11:' header in anti-patterns.md"
        )

    def test_should_title_category_code_search_tool_selection(self):
        """Category 11 title must be 'Code Search Tool Selection'."""
        content = ANTI_PATTERNS_FILE.read_text()
        assert "Code Search Tool Selection" in content, (
            "Missing 'Code Search Tool Selection' in Category 11 title"
        )

    def test_should_include_severity_level_in_category_11_header(self):
        """Category 11 header must include a SEVERITY level (CRITICAL, HIGH, or MEDIUM)."""
        content = ANTI_PATTERNS_FILE.read_text()
        pattern = re.compile(
            r"### Category 11:.*\(SEVERITY:\s*(CRITICAL|HIGH|MEDIUM)\)"
        )
        match = pattern.search(content)
        assert match is not None, (
            "Category 11 header missing SEVERITY level. "
            "Expected format: '### Category 11: ... (SEVERITY: CRITICAL|HIGH|MEDIUM)'"
        )

    def test_should_position_category_11_after_category_10(self):
        """Category 11 must appear after Category 10 in the file."""
        content = ANTI_PATTERNS_FILE.read_text()
        cat10_pos = content.find("### Category 10:")
        cat11_pos = content.find("### Category 11:")
        assert cat10_pos != -1, "Category 10 not found"
        assert cat11_pos != -1, "Category 11 not found"
        assert cat11_pos > cat10_pos, (
            f"Category 11 (pos {cat11_pos}) must appear after "
            f"Category 10 (pos {cat10_pos})"
        )

    def test_should_position_category_11_before_detection_protocol(self):
        """Category 11 must appear before 'Anti-Pattern Detection Protocol' section."""
        content = ANTI_PATTERNS_FILE.read_text()
        cat11_pos = content.find("### Category 11:")
        protocol_pos = content.find("## Anti-Pattern Detection Protocol")
        assert cat11_pos != -1, "Category 11 not found"
        assert protocol_pos != -1, "Anti-Pattern Detection Protocol section not found"
        assert cat11_pos < protocol_pos, (
            f"Category 11 (pos {cat11_pos}) must appear before "
            f"Anti-Pattern Detection Protocol (pos {protocol_pos})"
        )

    def test_should_bump_version_to_1_1(self):
        """File version must be bumped from 1.0 to 1.1."""
        content = ANTI_PATTERNS_FILE.read_text()
        assert "**Version**: 1.1" in content, (
            "Version not bumped to 1.1. "
            "Expected '**Version**: 1.1' in file header"
        )

    def test_should_not_contain_version_1_0(self):
        """Old version 1.0 must be replaced by 1.1."""
        content = ANTI_PATTERNS_FILE.read_text()
        # Version line should show 1.1, not 1.0
        lines = content.splitlines()
        for line in lines:
            if line.startswith("**Version**:"):
                assert "1.0" not in line, (
                    f"Version still shows 1.0: '{line}'. Must be bumped to 1.1"
                )
                break

    def test_should_update_last_updated_date(self):
        """Last Updated date must be changed from 2025-10-30."""
        content = ANTI_PATTERNS_FILE.read_text()
        assert "**Last Updated**: 2025-10-30" not in content, (
            "Last Updated date not changed from original 2025-10-30"
        )

    # --- Format Compliance ---

    def test_should_contain_forbidden_block_in_category_11(self):
        """Category 11 must contain at least one FORBIDDEN block."""
        content = ANTI_PATTERNS_FILE.read_text()
        cat11_pos = content.find("### Category 11:")
        if cat11_pos == -1:
            pytest.fail("Category 11 not found")
        cat11_content = content[cat11_pos:]
        # Look for FORBIDDEN before next major section
        protocol_pos = cat11_content.find("## Anti-Pattern Detection Protocol")
        if protocol_pos != -1:
            cat11_content = cat11_content[:protocol_pos]
        assert "FORBIDDEN" in cat11_content, (
            "Category 11 section missing FORBIDDEN block"
        )

    def test_should_contain_wrong_example_in_category_11(self):
        """Category 11 must contain at least one 'Wrong' example."""
        content = ANTI_PATTERNS_FILE.read_text()
        cat11_pos = content.find("### Category 11:")
        if cat11_pos == -1:
            pytest.fail("Category 11 not found")
        cat11_content = content[cat11_pos:]
        protocol_pos = cat11_content.find("## Anti-Pattern Detection Protocol")
        if protocol_pos != -1:
            cat11_content = cat11_content[:protocol_pos]
        assert "**Wrong**" in cat11_content, (
            "Category 11 section missing '**Wrong**' example"
        )

    def test_should_contain_correct_example_in_category_11(self):
        """Category 11 must contain at least one 'Correct' example."""
        content = ANTI_PATTERNS_FILE.read_text()
        cat11_pos = content.find("### Category 11:")
        if cat11_pos == -1:
            pytest.fail("Category 11 not found")
        cat11_content = content[cat11_pos:]
        protocol_pos = cat11_content.find("## Anti-Pattern Detection Protocol")
        if protocol_pos != -1:
            cat11_content = cat11_content[:protocol_pos]
        assert "**Correct**" in cat11_content, (
            "Category 11 section missing '**Correct**' example"
        )

    def test_should_contain_rationale_in_category_11(self):
        """Category 11 must contain at least one 'Rationale' section."""
        content = ANTI_PATTERNS_FILE.read_text()
        cat11_pos = content.find("### Category 11:")
        if cat11_pos == -1:
            pytest.fail("Category 11 not found")
        cat11_content = content[cat11_pos:]
        protocol_pos = cat11_content.find("## Anti-Pattern Detection Protocol")
        if protocol_pos != -1:
            cat11_content = cat11_content[:protocol_pos]
        assert "**Rationale**" in cat11_content, (
            "Category 11 section missing '**Rationale**' section"
        )

    # --- Preservation Tests ---

    def test_should_preserve_locked_status_marker(self):
        """LOCKED status marker on line 3 must remain unchanged."""
        content = ANTI_PATTERNS_FILE.read_text()
        assert "**Status**: LOCKED" in content, (
            "LOCKED status marker missing or modified"
        )

    def test_should_preserve_all_10_existing_categories(self):
        """All 10 existing category headers must remain present."""
        content = ANTI_PATTERNS_FILE.read_text()
        for i in range(1, 11):
            assert f"### Category {i}:" in content, (
                f"Category {i} header missing -- existing categories must be preserved"
            )

"""
Test: AC#5 - Output File Structure Validation
Story: STORY-539
Generated: 2026-03-04

Tests validate that the go-to-market-framework.md defines the 4 required
output sections and that reference files use ATX headings throughout.
"""
import os
import re
import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GTM_FRAMEWORK = os.path.join(PROJECT_ROOT, "src", "claude", "skills", "marketing-business", "references", "go-to-market-framework.md")

REQUIRED_SECTIONS = [
    "Executive Summary",
    "Channel Strategy",
    "Budget Allocation",
    "30-Day Launch Plan",
]


class TestRequiredSections:
    """AC#5: Output must contain all 4 required top-level sections."""

    @pytest.fixture
    def framework_content(self):
        with open(GTM_FRAMEWORK, "r") as f:
            return f.read()

    @pytest.mark.parametrize("section", REQUIRED_SECTIONS)
    def test_should_have_required_section(self, framework_content, section):
        # Arrange & Act
        pattern = rf"^## {re.escape(section)}"
        has_section = bool(re.search(pattern, framework_content, re.MULTILINE))
        # Assert
        assert has_section, f"Missing required section '## {section}' in framework file"

    def test_should_have_all_4_required_sections(self, framework_content):
        # Arrange
        found = 0
        # Act
        for section in REQUIRED_SECTIONS:
            if re.search(rf"^## {re.escape(section)}", framework_content, re.MULTILINE):
                found += 1
        # Assert
        assert found == 4, f"Only {found}/4 required sections found"


class TestSectionContent:
    """AC#5: Each required section must be non-empty."""

    @pytest.fixture
    def framework_content(self):
        with open(GTM_FRAMEWORK, "r") as f:
            return f.read()

    @pytest.mark.parametrize("section", REQUIRED_SECTIONS)
    def test_should_have_nonempty_section(self, framework_content, section):
        # Arrange
        pattern = rf"^## {re.escape(section)}\s*\n(.*?)(?=^## |\Z)"
        # Act
        match = re.search(pattern, framework_content, re.MULTILINE | re.DOTALL)
        # Assert
        assert match is not None, f"Section '## {section}' not found"
        content = match.group(1).strip()
        assert len(content) > 0, f"Section '## {section}' is empty"


class TestATXHeadingStyle:
    """AC#5: All headings must use ATX style (# prefix)."""

    @pytest.fixture
    def framework_content(self):
        with open(GTM_FRAMEWORK, "r") as f:
            return f.read()

    def test_should_use_atx_headings_exclusively(self, framework_content):
        # Arrange & Act - setext headings use === or --- underlines
        setext_matches = re.findall(r"^[^\n]+\n[=\-]{3,}$", framework_content, re.MULTILINE)
        # Assert
        assert len(setext_matches) == 0, f"Found {len(setext_matches)} setext headings, ATX required"

    def test_should_have_properly_formatted_h2_headings(self, framework_content):
        # Arrange & Act
        h2_headings = re.findall(r"^## .+", framework_content, re.MULTILINE)
        # Assert
        assert len(h2_headings) >= 4, f"Only {len(h2_headings)} H2 headings, need at least 4"


class TestBusinessRuleZeroBudget:
    """BR-003: Zero-budget must fall back to organic-only channels."""

    @pytest.fixture
    def framework_content(self):
        with open(GTM_FRAMEWORK, "r") as f:
            return f.read()

    def test_should_document_zero_budget_handling(self, framework_content):
        # Arrange & Act
        has_zero_budget = bool(re.search(r"(?i)(zero.?budget|no.?budget|\$0|organic.only)", framework_content))
        # Assert
        assert has_zero_budget, "Framework must document zero-budget organic-only fallback"

    def test_should_recommend_organic_channels_for_zero_budget(self, framework_content):
        # Arrange & Act
        has_organic = bool(re.search(r"(?i)organic", framework_content))
        # Assert
        assert has_organic, "Framework must mention organic channels for zero-budget scenario"


class TestBusinessRuleExistingFile:
    """BR-004: Existing file must trigger user prompt before overwrite."""

    @pytest.fixture
    def framework_content(self):
        with open(GTM_FRAMEWORK, "r") as f:
            return f.read()

    def test_should_document_overwrite_protection(self, framework_content):
        # Arrange & Act
        has_overwrite = bool(re.search(r"(?i)(overwrite|existing.file|already.exists|prompt.*before)", framework_content))
        # Assert
        assert has_overwrite, "Framework must document overwrite protection for existing output files"

"""
Test: AC#5 - SKILL.md Size and Progressive Disclosure
Story: STORY-550
Generated: 2026-03-05

Tests validate:
- SKILL.md remains under 1,000 lines after break-even phase added
- SKILL.md contains break-even phase definition
- SKILL.md references break-even-analysis.md via progressive disclosure link
- break-even-analysis.md reference file exists with required content
"""

import os
import re
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SKILL_FILE = os.path.join(
    PROJECT_ROOT,
    "src", "claude", "skills", "managing-finances", "SKILL.md",
)
REFERENCE_FILE = os.path.join(
    PROJECT_ROOT,
    "src", "claude", "skills", "managing-finances", "references", "break-even-analysis.md",
)


@pytest.fixture
def skill_content():
    """Load SKILL.md content from src/ tree."""
    assert os.path.exists(SKILL_FILE), (
        f"SKILL.md does not exist: {SKILL_FILE}"
    )
    with open(SKILL_FILE, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def skill_lines():
    """Load SKILL.md lines from src/ tree."""
    assert os.path.exists(SKILL_FILE), (
        f"SKILL.md does not exist: {SKILL_FILE}"
    )
    with open(SKILL_FILE, "r", encoding="utf-8") as f:
        return f.readlines()


@pytest.fixture
def reference_content():
    """Load break-even-analysis.md content from src/ tree."""
    assert os.path.exists(REFERENCE_FILE), (
        f"Reference file does not exist: {REFERENCE_FILE}"
    )
    with open(REFERENCE_FILE, "r", encoding="utf-8") as f:
        return f.read()


# ---------------------------------------------------------------------------
# SKILL.md size constraint
# ---------------------------------------------------------------------------

class TestSkillFileSize:
    """SKILL.md must remain under 1,000 lines."""

    def test_should_be_under_1000_lines_when_break_even_added(self, skill_lines):
        """AC5: SKILL.md must be under 1,000 lines total."""
        line_count = len(skill_lines)
        assert line_count < 1000, (
            f"SKILL.md is {line_count} lines, must be under 1,000"
        )


# ---------------------------------------------------------------------------
# Break-even phase in SKILL.md
# ---------------------------------------------------------------------------

class TestBreakEvenPhasePresence:
    """SKILL.md must contain a break-even phase definition."""

    def test_should_contain_break_even_phase(self, skill_content):
        """AC5: SKILL.md must define a break-even analysis phase."""
        assert re.search(
            r"break.even", skill_content, re.IGNORECASE
        ), "SKILL.md must contain a break-even phase definition"

    def test_should_contain_break_even_section_heading(self, skill_content):
        """AC5: SKILL.md must have a section heading for break-even."""
        assert re.search(
            r"^#{1,3}\s+.*break.even", skill_content, re.IGNORECASE | re.MULTILINE
        ), "SKILL.md must have a section heading for break-even analysis"


# ---------------------------------------------------------------------------
# Progressive disclosure reference
# ---------------------------------------------------------------------------

class TestProgressiveDisclosureLink:
    """SKILL.md must reference break-even-analysis.md."""

    def test_should_reference_break_even_analysis_md(self, skill_content):
        """AC5: SKILL.md must reference break-even-analysis.md."""
        assert re.search(
            r"break-even-analysis\.md", skill_content
        ), "SKILL.md must reference break-even-analysis.md"

    def test_should_use_references_directory_path(self, skill_content):
        """AC5: Reference must use references/ directory path."""
        assert re.search(
            r"references/break-even-analysis\.md", skill_content
        ), "SKILL.md must reference via references/break-even-analysis.md path"


# ---------------------------------------------------------------------------
# Reference file existence and structure
# ---------------------------------------------------------------------------

class TestReferenceFileStructure:
    """break-even-analysis.md must exist with required content."""

    def test_should_exist_as_separate_file(self):
        """AC5: break-even-analysis.md must exist as a separate reference file."""
        assert os.path.exists(REFERENCE_FILE), (
            f"break-even-analysis.md does not exist: {REFERENCE_FILE}"
        )

    def test_should_contain_calculation_methodology(self, reference_content):
        """AC5: Reference must contain calculation methodology."""
        assert re.search(
            r"(calculation|formula|methodology)", reference_content, re.IGNORECASE
        ), "Reference must contain calculation methodology"

    def test_should_contain_chart_rendering_spec(self, reference_content):
        """AC5: Reference must contain chart rendering specification."""
        assert re.search(
            r"(chart|render|visual)", reference_content, re.IGNORECASE
        ), "Reference must contain chart rendering specification"

    def test_should_contain_edge_case_handling(self, reference_content):
        """AC5: Reference must contain edge case handling."""
        assert re.search(
            r"edge\s+case", reference_content, re.IGNORECASE
        ), "Reference must contain edge case handling section"

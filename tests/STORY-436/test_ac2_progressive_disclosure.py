"""
Test: AC#2 - Progressive Disclosure References
Story: STORY-436
Generated: 2026-02-18

Validates each sub-phase includes Read() references to specific
reference files loaded on-demand.
"""
import re
from pathlib import Path

import pytest

SKILL_MD = Path(__file__).resolve().parents[2] / "src" / "claude" / "skills" / "devforgeai-architecture" / "SKILL.md"


@pytest.fixture
def skill_content():
    assert SKILL_MD.exists(), f"SKILL.md not found at {SKILL_MD}"
    return SKILL_MD.read_text(encoding="utf-8")


@pytest.fixture
def phase6_section(skill_content):
    """Extract Phase 6 section from SKILL.md."""
    match = re.search(r"(##\s+Phase\s+6.*?)(?=\n##\s+[^#]|\Z)", skill_content, re.DOTALL)
    assert match, "Phase 6 section not found in SKILL.md"
    return match.group(1)


class TestReadReferencesPresent:
    """Each sub-phase must include Read() references to reference files."""

    def test_should_contain_read_calls_in_phase6(self, phase6_section):
        """Phase 6 must contain at least one Read() call."""
        assert "Read(" in phase6_section, \
            "Phase 6 must contain Read() references for progressive disclosure"

    EXPECTED_REFERENCES = {
        "6.1": "epic-management.md",
        "6.3": "feature-decomposition",
        "6.4": "complexity-assessment",
        "6.6": "epic-validation-checklist.md",
        "6.7": "epic-template.md",
    }

    @pytest.mark.parametrize("sub_phase,ref_fragment", list(EXPECTED_REFERENCES.items()))
    def test_should_reference_correct_file_for_subphase(self, phase6_section, sub_phase, ref_fragment):
        # Find the sub-phase section and check for reference
        pattern = rf"{re.escape(sub_phase)}.*?(?:Read\(|reference).*?{re.escape(ref_fragment)}"
        assert re.search(pattern, phase6_section, re.DOTALL | re.IGNORECASE), \
            f"Sub-phase {sub_phase} must reference '{ref_fragment}'"


class TestOnDemandLoading:
    """References must be on-demand (Read() calls), not preloaded."""

    def test_should_use_read_calls_not_inline_content(self, phase6_section):
        """Phase 6 sub-phases must use Read() for progressive disclosure."""
        read_count = len(re.findall(r"Read\(", phase6_section))
        assert read_count >= 5, \
            f"Expected at least 5 Read() references in Phase 6, found {read_count}"

    def test_should_keep_subphases_under_15_lines_each(self, phase6_section):
        """Each sub-phase must be <= 15 lines (progressive disclosure)."""
        subphase_sections = re.split(r"(?=###?\s+(?:Phase\s+)?6\.\d)", phase6_section)
        for section in subphase_sections:
            if not section.strip():
                continue
            line_count = len(section.strip().split("\n"))
            header_match = re.search(r"6\.(\d)", section)
            if header_match:
                assert line_count <= 15, \
                    f"Sub-phase 6.{header_match.group(1)} has {line_count} lines (max 15)"

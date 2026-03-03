"""
Test: AC#1 - Phase 6 Epic Creation Added to Architecture SKILL.md
Story: STORY-436
Generated: 2026-02-18

Validates that SKILL.md contains Phase 6 with 8 sub-phases (6.1-6.8)
listed after existing Phase 5.
"""
import re
from pathlib import Path

import pytest

SKILL_MD = Path(__file__).resolve().parents[2] / "src" / "claude" / "skills" / "devforgeai-architecture" / "SKILL.md"


@pytest.fixture
def skill_content():
    assert SKILL_MD.exists(), f"SKILL.md not found at {SKILL_MD}"
    return SKILL_MD.read_text(encoding="utf-8")


class TestPhase6Exists:
    """Phase 6 must exist as a top-level phase in SKILL.md."""

    def test_should_contain_phase6_header_when_skill_loaded(self, skill_content):
        """Phase 6 header must be present."""
        assert re.search(r"##\s+Phase\s+6", skill_content), \
            "SKILL.md must contain a '## Phase 6' header"

    def test_should_contain_epic_creation_in_phase6_title(self, skill_content):
        """Phase 6 title must reference Epic Creation."""
        assert re.search(r"Phase\s+6.*Epic\s+Creation", skill_content, re.IGNORECASE), \
            "Phase 6 title must include 'Epic Creation'"


class TestEightSubPhases:
    """Phase 6 must have exactly 8 sub-phases numbered 6.1 through 6.8."""

    @pytest.mark.parametrize("sub_phase", [
        "6.1", "6.2", "6.3", "6.4", "6.5", "6.6", "6.7", "6.8"
    ])
    def test_should_contain_subphase_when_phase6_defined(self, skill_content, sub_phase):
        pattern = rf"(?:Phase\s+)?{re.escape(sub_phase)}"
        assert re.search(pattern, skill_content), \
            f"SKILL.md must contain sub-phase {sub_phase}"

    def test_should_have_exactly_8_subphases(self, skill_content):
        """Count sub-phases 6.1-6.8; must find all 8."""
        found = set()
        for i in range(1, 9):
            tag = f"6.{i}"
            if re.search(rf"(?:Phase\s+)?{re.escape(tag)}", skill_content):
                found.add(tag)
        assert len(found) == 8, f"Expected 8 sub-phases, found {len(found)}: {found}"


class TestPhase6AfterPhase5:
    """Phase 6 must appear after Phase 5 in SKILL.md."""

    def test_should_place_phase6_after_phase5(self, skill_content):
        phase5_match = re.search(r"##\s+Phase\s+5", skill_content)
        phase6_match = re.search(r"##\s+Phase\s+6", skill_content)
        assert phase5_match, "Phase 5 header not found"
        assert phase6_match, "Phase 6 header not found"
        assert phase6_match.start() > phase5_match.start(), \
            "Phase 6 must appear after Phase 5"


class TestSubPhaseNames:
    """Sub-phases must have expected names per story mapping."""

    EXPECTED_NAMES = {
        "6.1": "Discovery",
        "6.2": "Requirements Input Parsing",
        "6.3": "Feature Decomposition",
        "6.4": "Technical Assessment",
        "6.5": "Epic Document Generation",
        "6.6": "Validation",
        "6.7": "Epic File Creation",
        "6.8": "Feedback Hook",
    }

    @pytest.mark.parametrize("sub_phase,name_fragment", list(EXPECTED_NAMES.items()))
    def test_should_have_named_subphase(self, skill_content, sub_phase, name_fragment):
        pattern = rf"{re.escape(sub_phase)}.*{re.escape(name_fragment)}"
        assert re.search(pattern, skill_content, re.IGNORECASE), \
            f"Sub-phase {sub_phase} must contain '{name_fragment}' in its title"

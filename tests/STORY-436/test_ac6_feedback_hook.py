"""
Test: AC#6 - Post-Epic Feedback Hook Preserved
Story: STORY-436
Generated: 2026-02-18

Validates Phase 6.8 includes non-blocking feedback hook.
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
    match = re.search(r"(##\s+Phase\s+6.*?)(?=\n##\s+[^#]|\Z)", skill_content, re.DOTALL)
    assert match, "Phase 6 section not found"
    return match.group(1)


class TestFeedbackHookExists:
    """Phase 6.8 must include a feedback hook."""

    def test_should_contain_feedback_hook_in_phase_6_8(self, phase6_section):
        match = re.search(r"6\.8.*?(?=\n##|\Z)", phase6_section, re.DOTALL)
        assert match, "Sub-phase 6.8 not found"
        assert re.search(r"feedback", match.group(0), re.IGNORECASE), \
            "Phase 6.8 must reference feedback hook"

    def test_should_reference_feedback_as_final_subphase(self, phase6_section):
        """6.8 must be the last sub-phase (no 6.9 exists)."""
        assert not re.search(r"6\.9", phase6_section), \
            "Phase 6.8 must be the final sub-phase (no 6.9 should exist)"


class TestNonBlockingBehavior:
    """Feedback hook must be non-blocking."""

    def test_should_specify_non_blocking(self, phase6_section):
        match = re.search(r"6\.8.*?(?=\n##|\Z)", phase6_section, re.DOTALL)
        assert match, "Sub-phase 6.8 not found"
        section = match.group(0)
        assert re.search(r"non.?blocking", section, re.IGNORECASE), \
            "Phase 6.8 must specify non-blocking behavior"

    def test_should_reference_story_028(self, phase6_section):
        """Feedback hook originates from STORY-028."""
        assert "STORY-028" in phase6_section or "story-028" in phase6_section.lower(), \
            "Phase 6 feedback hook must reference its origin (STORY-028)"

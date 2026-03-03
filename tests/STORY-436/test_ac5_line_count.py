"""
Test: AC#5 - SKILL.md Under 1,000-Line Limit
Story: STORY-436
Generated: 2026-02-18

Validates total line count <= 400 (target) and <= 1,000 (hard limit).
"""
from pathlib import Path

import pytest

SKILL_MD = Path(__file__).resolve().parents[2] / "src" / "claude" / "skills" / "devforgeai-architecture" / "SKILL.md"


@pytest.fixture
def skill_content():
    assert SKILL_MD.exists(), f"SKILL.md not found at {SKILL_MD}"
    return SKILL_MD.read_text(encoding="utf-8")


@pytest.fixture
def line_count(skill_content):
    return len(skill_content.split("\n"))


class TestLineCountLimits:
    """SKILL.md must stay within size constraints."""

    def test_should_not_exceed_hard_limit_of_1000_lines(self, line_count):
        assert line_count <= 1000, \
            f"SKILL.md has {line_count} lines, exceeding 1,000-line hard limit"

    def test_should_meet_target_of_400_lines(self, line_count):
        assert line_count <= 400, \
            f"SKILL.md has {line_count} lines, exceeding 400-line target"

    def test_should_have_grown_from_baseline(self, line_count):
        """After Phase 6 addition, SKILL.md should be > 279 lines (baseline)."""
        assert line_count > 279, \
            f"SKILL.md has {line_count} lines but should be > 279 after Phase 6 addition"

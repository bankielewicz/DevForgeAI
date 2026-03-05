"""
Test: AC#4 - Profile-Driven Adaptation
Story: STORY-470 (Terminal-Compatible Gamification)
Generated: 2026-03-04

Verifies gamification respects profile settings
(celebration_intensity, progress_visualization).
"""

import pytest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SKILL_FILE = PROJECT_ROOT / "src" / "claude" / "skills" / "coaching-entrepreneur" / "SKILL.md"
CELEBRATION_ENGINE = PROJECT_ROOT / "src" / "claude" / "skills" / "coaching-entrepreneur" / "references" / "celebration-engine.md"


class TestSkillFileExists:
    """Verify coaching-entrepreneur SKILL.md exists."""

    def test_skill_file_exists(self):
        """Arrange: Path to coaching-entrepreneur SKILL.md.
        Act: Check file existence.
        Assert: SKILL.md exists in src/ tree."""
        assert SKILL_FILE.exists(), (
            f"coaching-entrepreneur SKILL.md not found at {SKILL_FILE}"
        )


class TestCelebrationIntensityProfile:
    """Verify profile celebration_intensity setting is referenced."""

    @pytest.fixture(autouse=True)
    def load_content(self):
        self.skill_content = SKILL_FILE.read_text(encoding="utf-8")

    def test_celebration_intensity_dimension_referenced(self):
        """Arrange: SKILL.md content loaded.
        Act: Search for celebration_intensity profile dimension.
        Assert: celebration_intensity is referenced in skill."""
        assert "celebration_intensity" in self.skill_content, (
            "Missing 'celebration_intensity' profile dimension in SKILL.md"
        )

    def test_progress_visualization_dimension_referenced(self):
        """Arrange: SKILL.md content loaded.
        Act: Search for progress_visualization profile dimension.
        Assert: progress_visualization is referenced in skill."""
        assert "progress_visualization" in self.skill_content, (
            "Missing 'progress_visualization' profile dimension in SKILL.md"
        )


class TestHighAdaptationBehavior:
    """Verify high-adaptation users see progress after every task."""

    @pytest.fixture(autouse=True)
    def load_content(self):
        self.skill_content = SKILL_FILE.read_text(encoding="utf-8")

    def test_high_adaptation_frequent_progress(self):
        """Arrange: SKILL.md content loaded.
        Act: Search for high-adaptation behavior description.
        Assert: High adaptation shows progress after every task."""
        content_lower = self.skill_content.lower()
        # High adaptation should mention frequent/every-task progress
        has_high_freq = (
            ("high" in content_lower and "every" in content_lower)
            or ("high" in content_lower and "frequent" in content_lower)
            or ("high" in content_lower and "each task" in content_lower)
        )
        assert has_high_freq, (
            "SKILL.md must describe high-adaptation users seeing progress after every task"
        )


class TestLowAdaptationBehavior:
    """Verify low-adaptation users see weekly summaries."""

    @pytest.fixture(autouse=True)
    def load_content(self):
        self.skill_content = SKILL_FILE.read_text(encoding="utf-8")

    def test_low_adaptation_weekly_summaries(self):
        """Arrange: SKILL.md content loaded.
        Act: Search for low-adaptation behavior description.
        Assert: Low adaptation shows weekly summaries."""
        content_lower = self.skill_content.lower()
        has_low_weekly = (
            ("low" in content_lower and "weekly" in content_lower)
            or ("low" in content_lower and "summary" in content_lower)
            or ("minimal" in content_lower and "weekly" in content_lower)
        )
        assert has_low_weekly, (
            "SKILL.md must describe low-adaptation users seeing weekly summaries"
        )

    def test_low_adaptation_milestone_only_celebrations(self):
        """Arrange: SKILL.md content loaded.
        Act: Search for low-adaptation celebration behavior.
        Assert: Low adaptation triggers celebrations on milestones only."""
        content_lower = self.skill_content.lower()
        has_milestone_only = "milestone" in content_lower and "low" in content_lower
        assert has_milestone_only, (
            "SKILL.md must describe low-adaptation users getting milestone-only celebrations"
        )


class TestProfileFallbackBehavior:
    """BR-002: Default to medium if profile unavailable."""

    @pytest.fixture(autouse=True)
    def load_content(self):
        # Check both files for fallback documentation
        self.celebration_content = CELEBRATION_ENGINE.read_text(encoding="utf-8")
        self.skill_content = SKILL_FILE.read_text(encoding="utf-8")
        self.combined = self.celebration_content + self.skill_content

    def test_default_medium_when_profile_unavailable(self):
        """Arrange: Both celebration engine and SKILL.md loaded.
        Act: Search for fallback/default behavior.
        Assert: Default to medium intensity when profile unavailable."""
        combined_lower = self.combined.lower()
        has_default = (
            ("default" in combined_lower and "medium" in combined_lower)
            or ("fallback" in combined_lower and "medium" in combined_lower)
            or ("unavailable" in combined_lower and "medium" in combined_lower)
        )
        assert has_default, (
            "Must document default to medium celebration intensity when profile unavailable (BR-002)"
        )

    def test_missing_profile_handled(self):
        """Arrange: Both celebration engine and SKILL.md loaded.
        Act: Search for missing/unavailable profile handling.
        Assert: Document addresses missing profile scenario."""
        combined_lower = self.combined.lower()
        has_handling = (
            "missing" in combined_lower
            or "unavailable" in combined_lower
            or "not found" in combined_lower
            or "fallback" in combined_lower
        )
        assert has_handling, (
            "Must document handling for missing/unavailable user profile"
        )

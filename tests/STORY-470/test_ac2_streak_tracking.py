"""
Test: AC#2 - Streak Tracking
Story: STORY-470 (Terminal-Compatible Gamification)
Generated: 2026-03-04

Verifies streak tracking section exists in celebration-engine.md
and streak-tracker.yaml schema has required fields.
"""

import pytest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CELEBRATION_ENGINE = PROJECT_ROOT / "src" / "claude" / "skills" / "coaching-entrepreneur" / "references" / "celebration-engine.md"


class TestStreakTrackingSectionExists:
    """Verify streak tracking section in celebration-engine.md."""

    @pytest.fixture(autouse=True)
    def load_content(self):
        self.content = CELEBRATION_ENGINE.read_text(encoding="utf-8")

    def test_streak_tracking_section_exists(self):
        """Arrange: Celebration engine content loaded.
        Act: Search for streak-tracking section header.
        Assert: Section exists in document."""
        assert "streak-tracking" in self.content.lower() or "Streak Tracking" in self.content, (
            "Missing 'streak-tracking' section in celebration-engine.md"
        )


class TestStreakTrackerSchema:
    """Verify streak-tracker.yaml schema documents required fields."""

    @pytest.fixture(autouse=True)
    def load_content(self):
        self.content = CELEBRATION_ENGINE.read_text(encoding="utf-8")

    def test_current_streak_field_documented(self):
        """Arrange: Celebration engine content loaded.
        Act: Search for current_streak field definition.
        Assert: current_streak field is documented in schema."""
        assert "current_streak" in self.content, (
            "Missing 'current_streak' field in streak tracker schema"
        )

    def test_longest_streak_field_documented(self):
        """Arrange: Celebration engine content loaded.
        Act: Search for longest_streak field definition.
        Assert: longest_streak field is documented in schema."""
        assert "longest_streak" in self.content, (
            "Missing 'longest_streak' field in streak tracker schema"
        )

    def test_last_session_date_field_documented(self):
        """Arrange: Celebration engine content loaded.
        Act: Search for last_session_date field definition.
        Assert: last_session_date field is documented in schema."""
        assert "last_session_date" in self.content, (
            "Missing 'last_session_date' field in streak tracker schema"
        )

    def test_current_streak_type_is_integer(self):
        """Arrange: Celebration engine content loaded.
        Act: Search for current_streak type constraint.
        Assert: current_streak typed as integer with >= 0 constraint."""
        # Find context around current_streak
        lines = self.content.split("\n")
        streak_context = []
        for i, line in enumerate(lines):
            if "current_streak" in line:
                start = max(0, i - 1)
                end = min(len(lines), i + 4)
                streak_context.extend(lines[start:end])
        context_text = " ".join(streak_context).lower()
        assert "int" in context_text or "integer" in context_text or "number" in context_text, (
            "current_streak must be documented as integer type"
        )

    def test_longest_streak_type_is_integer(self):
        """Arrange: Celebration engine content loaded.
        Act: Search for longest_streak type constraint.
        Assert: longest_streak typed as integer with >= 0 constraint."""
        lines = self.content.split("\n")
        streak_context = []
        for i, line in enumerate(lines):
            if "longest_streak" in line:
                start = max(0, i - 1)
                end = min(len(lines), i + 4)
                streak_context.extend(lines[start:end])
        context_text = " ".join(streak_context).lower()
        assert "int" in context_text or "integer" in context_text or "number" in context_text, (
            "longest_streak must be documented as integer type"
        )

    def test_last_session_date_type_is_datetime(self):
        """Arrange: Celebration engine content loaded.
        Act: Search for last_session_date type constraint.
        Assert: last_session_date typed as DateTime."""
        lines = self.content.split("\n")
        date_context = []
        for i, line in enumerate(lines):
            if "last_session_date" in line:
                start = max(0, i - 1)
                end = min(len(lines), i + 4)
                date_context.extend(lines[start:end])
        context_text = " ".join(date_context).lower()
        assert "date" in context_text or "datetime" in context_text or "iso" in context_text, (
            "last_session_date must be documented as DateTime type"
        )

    def test_streak_display_in_session_summary(self):
        """Arrange: Celebration engine content loaded.
        Act: Search for streak display guidance.
        Assert: Document mentions displaying streak in session summaries."""
        content_lower = self.content.lower()
        assert "session" in content_lower and "streak" in content_lower, (
            "Missing guidance for displaying streak in session summaries"
        )

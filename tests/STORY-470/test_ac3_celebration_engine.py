"""
Test: AC#3 - Celebration Engine
Story: STORY-470 (Terminal-Compatible Gamification)
Generated: 2026-03-04

Verifies celebration engine has 3 tiers (high/medium/low)
with achievement-specific messages.
"""

import pytest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CELEBRATION_ENGINE = PROJECT_ROOT / "src" / "claude" / "skills" / "coaching-entrepreneur" / "references" / "celebration-engine.md"


class TestCelebrationTiersSection:
    """Verify celebration-tiers section exists."""

    @pytest.fixture(autouse=True)
    def load_content(self):
        self.content = CELEBRATION_ENGINE.read_text(encoding="utf-8")

    def test_celebration_tiers_section_exists(self):
        """Arrange: Celebration engine content loaded.
        Act: Search for celebration-tiers section header.
        Assert: Section exists in document."""
        assert "celebration-tiers" in self.content.lower() or "Celebration Tiers" in self.content, (
            "Missing 'celebration-tiers' section in celebration-engine.md"
        )


class TestThreeTiersDefined:
    """Verify all three celebration intensity tiers are defined."""

    @pytest.fixture(autouse=True)
    def load_content(self):
        self.content = CELEBRATION_ENGINE.read_text(encoding="utf-8")
        self.content_lower = self.content.lower()

    def test_high_tier_defined(self):
        """Arrange: Celebration engine content loaded.
        Act: Search for high celebration tier.
        Assert: High tier is defined."""
        assert "high" in self.content_lower, (
            "Missing 'high' celebration tier definition"
        )

    def test_medium_tier_defined(self):
        """Arrange: Celebration engine content loaded.
        Act: Search for medium celebration tier.
        Assert: Medium tier is defined."""
        assert "medium" in self.content_lower, (
            "Missing 'medium' celebration tier definition"
        )

    def test_low_tier_defined(self):
        """Arrange: Celebration engine content loaded.
        Act: Search for low celebration tier.
        Assert: Low tier is defined."""
        assert "low" in self.content_lower, (
            "Missing 'low' celebration tier definition"
        )


class TestHighTierBehavior:
    """Verify high tier acknowledges every completion."""

    @pytest.fixture(autouse=True)
    def load_content(self):
        self.content = CELEBRATION_ENGINE.read_text(encoding="utf-8")

    def test_high_tier_every_completion(self):
        """Arrange: Celebration engine content loaded.
        Act: Find high tier section and check behavior.
        Assert: High tier triggers on every task completion."""
        # Extract text around "high" tier definition
        lines = self.content.split("\n")
        high_context = []
        for i, line in enumerate(lines):
            if "high" in line.lower() and ("tier" in line.lower() or "celebrat" in line.lower() or "intensity" in line.lower()):
                start = max(0, i)
                end = min(len(lines), i + 8)
                high_context.extend(lines[start:end])
        context_text = " ".join(high_context).lower()
        assert "every" in context_text or "all" in context_text or "each" in context_text, (
            "High tier must acknowledge every task completion"
        )


class TestMediumTierBehavior:
    """Verify medium tier triggers on significant tasks."""

    @pytest.fixture(autouse=True)
    def load_content(self):
        self.content = CELEBRATION_ENGINE.read_text(encoding="utf-8")

    def test_medium_tier_significant_tasks(self):
        """Arrange: Celebration engine content loaded.
        Act: Find medium tier section and check behavior.
        Assert: Medium tier triggers on significant tasks only."""
        lines = self.content.split("\n")
        medium_context = []
        for i, line in enumerate(lines):
            if "medium" in line.lower() and ("tier" in line.lower() or "celebrat" in line.lower() or "intensity" in line.lower()):
                start = max(0, i)
                end = min(len(lines), i + 8)
                medium_context.extend(lines[start:end])
        context_text = " ".join(medium_context).lower()
        assert "significant" in context_text or "important" in context_text or "notable" in context_text, (
            "Medium tier must trigger on significant tasks"
        )


class TestLowTierBehavior:
    """Verify low tier triggers on milestones only."""

    @pytest.fixture(autouse=True)
    def load_content(self):
        self.content = CELEBRATION_ENGINE.read_text(encoding="utf-8")

    def test_low_tier_milestones_only(self):
        """Arrange: Celebration engine content loaded.
        Act: Find low tier section and check behavior.
        Assert: Low tier triggers on milestones only."""
        lines = self.content.split("\n")
        low_context = []
        for i, line in enumerate(lines):
            if "low" in line.lower() and ("tier" in line.lower() or "celebrat" in line.lower() or "intensity" in line.lower()):
                start = max(0, i)
                end = min(len(lines), i + 8)
                low_context.extend(lines[start:end])
        context_text = " ".join(low_context).lower()
        assert "milestone" in context_text, (
            "Low tier must trigger on milestones only"
        )


class TestAchievementSpecificMessages:
    """Verify celebration messages are achievement-specific, not generic."""

    @pytest.fixture(autouse=True)
    def load_content(self):
        self.content = CELEBRATION_ENGINE.read_text(encoding="utf-8")

    def test_contains_achievement_specific_examples(self):
        """Arrange: Celebration engine content loaded.
        Act: Search for context-specific celebration message examples.
        Assert: At least one achievement-specific message example exists."""
        # Achievement-specific messages reference the actual accomplishment
        specific_indicators = [
            "customer segment", "validated", "revenue", "prototype",
            "first", "milestone", "completed", "launched", "built"
        ]
        content_lower = self.content.lower()
        matches = sum(1 for indicator in specific_indicators if indicator in content_lower)
        assert matches >= 2, (
            f"Only {matches} achievement-specific indicators found. "
            "Celebration messages must be specific to achievements, not generic."
        )

    def test_no_purely_generic_messages(self):
        """Arrange: Celebration engine content loaded.
        Act: Check that messages are not purely generic like 'Good job!'.
        Assert: Document discourages or avoids purely generic messages."""
        # The doc should either warn against generic messages or simply not have them
        content_lower = self.content.lower()
        # Check that the document addresses specificity
        has_specificity_guidance = (
            "specific" in content_lower
            or "context" in content_lower
            or "achievement" in content_lower
            or "not generic" in content_lower
        )
        assert has_specificity_guidance, (
            "Celebration engine must include guidance for achievement-specific (not generic) messages"
        )

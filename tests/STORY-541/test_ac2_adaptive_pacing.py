"""
Test: AC#2 - User Profile Adaptive Pacing
Story: STORY-541
Generated: 2026-03-05

Validates:
- SKILL.md reads user profile when available
- Adapts pacing based on experience level
- Pre-populates known business context
- BR-003: Missing profile degrades gracefully
"""
import os
import re

import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SKILL_FILE = os.path.join(PROJECT_ROOT, "src", "claude", "skills", "marketing-business", "SKILL.md")


@pytest.fixture
def skill_content():
    """Arrange: Read SKILL.md content."""
    assert os.path.isfile(SKILL_FILE), f"SKILL.md not found: {SKILL_FILE}"
    with open(SKILL_FILE, "r", encoding="utf-8") as f:
        return f.read()


class TestUserProfileReading:
    """Tests for user profile detection and reading."""

    def test_should_reference_user_profile(self, skill_content):
        """Act & Assert: SKILL.md must reference user profile reading."""
        profile_patterns = ["user.profile", "user profile", "user-profile", "profile"]
        found = any(p.lower() in skill_content.lower() for p in profile_patterns)
        assert found, "SKILL.md must reference user profile reading"

    def test_should_detect_experience_level(self, skill_content):
        """Act & Assert: SKILL.md must reference experience level detection."""
        experience_patterns = [
            "experience.level",
            "experience level",
            "experience_level",
            "beginner",
            "experienced",
            "first-time",
        ]
        found = any(p.lower() in skill_content.lower() for p in experience_patterns)
        assert found, "SKILL.md must detect and reference experience level"


class TestAdaptivePacing:
    """Tests for pacing adaptation based on experience."""

    def test_should_adapt_pacing_for_experienced_users(self, skill_content):
        """Act & Assert: SKILL.md must describe pacing adaptation for experienced users."""
        # Must mention skipping/simplifying for experienced users
        patterns = ["skip", "adapt", "pacing", "onboarding"]
        found = sum(1 for p in patterns if p.lower() in skill_content.lower())
        assert found >= 2, (
            "SKILL.md must describe adaptive pacing (expected at least 2 of: "
            "skip, adapt, pacing, onboarding)"
        )

    def test_should_prepopulate_known_context(self, skill_content):
        """Act & Assert: SKILL.md must pre-populate known business context."""
        patterns = ["pre-populat", "prepopulat", "known context", "existing context"]
        found = any(p.lower() in skill_content.lower() for p in patterns)
        assert found, "SKILL.md must pre-populate known business context fields"


class TestGracefulDegradation:
    """Tests for BR-003: Missing profile degrades gracefully."""

    def test_should_handle_missing_profile_gracefully(self, skill_content):
        """Act & Assert: SKILL.md must handle missing profile without error."""
        patterns = [
            "graceful",
            "fallback",
            "default",
            "not found",
            "missing profile",
            "profile not available",
        ]
        found = any(p.lower() in skill_content.lower() for p in patterns)
        assert found, (
            "SKILL.md must describe graceful degradation when user profile is missing (BR-003)"
        )

    def test_should_not_require_profile_as_mandatory(self, skill_content):
        """Act & Assert: Profile must not be listed as mandatory/required dependency."""
        content_lower = skill_content.lower()
        # Check that profile is not marked as required/mandatory
        has_optional = any(
            p in content_lower
            for p in ["optional", "when available", "if available", "if present"]
        )
        assert has_optional, (
            "SKILL.md must treat user profile as optional (BR-003)"
        )

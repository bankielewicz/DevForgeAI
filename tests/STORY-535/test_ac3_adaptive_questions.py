"""
Test: AC#3 - Adaptive Question Depth Based on User Profile
Story: STORY-535
Generated: 2026-03-04

Validates that the skill adapts question depth based on user profile
business_knowledge field (beginner/intermediate/advanced).

Tests target src/ tree per CLAUDE.md.
"""
import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = PROJECT_ROOT / "src" / "claude" / "skills" / "researching-market"
SKILL_FILE = SKILL_DIR / "SKILL.md"


class TestBeginnerQuestionDepth:
    """Tests that beginner users receive explanatory context."""

    def test_should_define_beginner_knowledge_level(self):
        """Arrange: SKILL.md exists. Act: Read content. Assert: Beginner level defined."""
        content = SKILL_FILE.read_text()
        assert re.search(r"beginner", content, re.IGNORECASE), (
            "SKILL.md must define beginner knowledge level behavior."
        )

    def test_should_provide_explanatory_context_for_beginners(self):
        """Arrange: SKILL.md exists. Act: Read content. Assert: Explanatory context for beginners."""
        content = SKILL_FILE.read_text()
        assert re.search(r"beginner.*explain|beginner.*context|explain.*TAM.*SAM.*SOM|what.*TAM.*means", content, re.IGNORECASE), (
            "SKILL.md must provide explanatory context (what TAM/SAM/SOM means, why it matters) for beginner users."
        )


class TestIntermediateQuestionDepth:
    """Tests that intermediate users receive standard prompts."""

    def test_should_define_intermediate_knowledge_level(self):
        """Arrange: SKILL.md exists. Act: Read content. Assert: Intermediate level defined."""
        content = SKILL_FILE.read_text()
        assert re.search(r"intermediate", content, re.IGNORECASE), (
            "SKILL.md must define intermediate knowledge level behavior."
        )

    def test_should_provide_standard_prompts_for_intermediate(self):
        """Arrange: SKILL.md exists. Act: Read content. Assert: Standard prompts for intermediate."""
        content = SKILL_FILE.read_text()
        assert re.search(r"intermediate.*standard|standard.*prompt", content, re.IGNORECASE), (
            "SKILL.md must provide standard prompts for intermediate users."
        )


class TestAdvancedQuestionDepth:
    """Tests that advanced users receive abbreviated prompts."""

    def test_should_define_advanced_knowledge_level(self):
        """Arrange: SKILL.md exists. Act: Read content. Assert: Advanced level defined."""
        content = SKILL_FILE.read_text()
        assert re.search(r"advanced", content, re.IGNORECASE), (
            "SKILL.md must define advanced knowledge level behavior."
        )

    def test_should_provide_abbreviated_prompts_for_advanced(self):
        """Arrange: SKILL.md exists. Act: Read content. Assert: Abbreviated prompts for advanced."""
        content = SKILL_FILE.read_text()
        assert re.search(r"advanced.*abbreviat|abbreviat.*prompt|advanced.*direct.*input", content, re.IGNORECASE), (
            "SKILL.md must provide abbreviated prompts with direct input option for advanced users."
        )


class TestUserProfileIntegration:
    """Tests that the skill reads from user profile."""

    def test_should_reference_user_profile_path(self):
        """Arrange: SKILL.md exists. Act: Read content. Assert: User profile path referenced."""
        content = SKILL_FILE.read_text()
        assert re.search(r"user-profile\.md|user.profile", content, re.IGNORECASE), (
            "SKILL.md must reference user profile file for business_knowledge level."
        )

    def test_should_reference_business_knowledge_field(self):
        """Arrange: SKILL.md exists. Act: Read content. Assert: business_knowledge field referenced."""
        content = SKILL_FILE.read_text()
        assert "business_knowledge" in content, (
            "SKILL.md must reference the business_knowledge field from user profile."
        )


class TestDefaultBeginnerWhenProfileMissing:
    """BR-004: Default to beginner when user profile is missing."""

    def test_should_default_to_beginner_when_profile_missing(self):
        """Arrange: SKILL.md exists. Act: Read content. Assert: Default to beginner documented."""
        content = SKILL_FILE.read_text()
        assert re.search(r"default.*beginner|missing.*beginner|absent.*beginner", content, re.IGNORECASE), (
            "SKILL.md must default to beginner level when user profile is missing (BR-004)."
        )

    def test_should_log_warning_when_profile_missing(self):
        """Arrange: SKILL.md exists. Act: Read content. Assert: Warning logged on missing profile."""
        content = SKILL_FILE.read_text()
        assert re.search(r"warn|log.*missing.*profile|profile.*not.*found", content, re.IGNORECASE), (
            "SKILL.md must log a warning when user profile is missing."
        )

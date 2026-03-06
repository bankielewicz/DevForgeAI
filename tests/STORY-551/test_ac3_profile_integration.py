"""
Test: AC#3 - User Profile Integration for Adaptive Pacing
Story: STORY-551
Generated: 2026-03-05

Verifies managing-finances SKILL.md references user profile / EPIC-072,
documents adaptive pacing for beginner/intermediate/advanced levels,
and documents the profile read mechanism.
"""

import re


class TestProfileReference:
    """Verify SKILL.md references user profile and EPIC-072."""

    def test_should_reference_epic_072(self, skill_content):
        """SKILL.md must reference EPIC-072 for adaptive profile integration."""
        assert "EPIC-072" in skill_content, (
            "SKILL.md does not reference EPIC-072. "
            "AC#3 requires integration with EPIC-072 adaptive user profile."
        )

    def test_should_reference_user_profile(self, skill_content):
        """SKILL.md must reference user profile concept."""
        assert re.search(r'(?i)(user\s+profile|adaptive\s+profile)', skill_content), (
            "SKILL.md does not reference user profile. "
            "AC#3 requires reading user profile for adaptive pacing."
        )


class TestAdaptivePacingLevels:
    """Verify SKILL.md documents pacing for all experience levels."""

    def test_should_document_beginner_pacing(self, skill_content):
        """SKILL.md must document beginner-level adaptive pacing."""
        assert re.search(r'(?i)beginner', skill_content), (
            "SKILL.md missing 'beginner' experience level. "
            "AC#3 requires adaptive pacing for beginners."
        )

    def test_should_document_intermediate_pacing(self, skill_content):
        """SKILL.md must document intermediate-level adaptive pacing."""
        assert re.search(r'(?i)intermediate', skill_content), (
            "SKILL.md missing 'intermediate' experience level."
        )

    def test_should_document_advanced_pacing(self, skill_content):
        """SKILL.md must document advanced-level adaptive pacing."""
        assert re.search(r'(?i)advanced', skill_content), (
            "SKILL.md missing 'advanced' experience level."
        )

    def test_should_describe_beginner_explanatory_context(self, skill_content):
        """Beginners should receive explanatory context per AC#3."""
        assert re.search(
            r'(?i)beginner.*(?:explain|context|guided|detail)',
            skill_content,
            re.DOTALL
        ), (
            "SKILL.md does not describe explanatory context for beginners. "
            "AC#3: Beginners receive explanatory context and guided sub-questions."
        )

    def test_should_describe_advanced_concise_prompts(self, skill_content):
        """Advanced users should receive concise prompts per AC#3."""
        assert re.search(
            r'(?i)advanced.*(?:concise|brief|direct|streamlined)',
            skill_content,
            re.DOTALL
        ), (
            "SKILL.md does not describe concise prompts for advanced users. "
            "AC#3: Advanced users receive concise prompts."
        )


class TestProfileReadMechanism:
    """Verify SKILL.md documents how the profile is read."""

    def test_should_document_profile_read_mechanism(self, skill_content):
        """SKILL.md must document how the user profile is read."""
        assert re.search(
            r'(?i)(read.*profile|profile.*read|load.*profile|profile.*load)',
            skill_content
        ), (
            "SKILL.md does not document profile read mechanism. "
            "AC#3 requires a documented profile read mechanism."
        )

    def test_should_reference_adaptive_pacing_section(self, skill_content):
        """SKILL.md must have an identifiable adaptive pacing section."""
        assert re.search(
            r'(?i)(adaptive\s+pacing|experience.based\s+pacing|profile.based\s+adaptation)',
            skill_content
        ), (
            "SKILL.md missing adaptive pacing section. "
            "AC#3 requires documented adaptive pacing behavior."
        )


class TestEdgeCaseEC001MissingExperienceField:
    """EC-001: Missing experience field in profile defaults to intermediate."""

    def test_should_handle_missing_experience_field(self, skill_content):
        """SKILL.md must document fallback when experience field is missing."""
        assert re.search(
            r'(?i)(missing.*experience|experience.*missing|absent.*experience)',
            skill_content
        ), (
            "EC-001: SKILL.md does not document behavior when experience field "
            "is missing from user profile."
        )

    def test_should_default_to_intermediate_for_missing_field(self, skill_content):
        """Missing experience field should default to intermediate."""
        # Look for pattern linking missing field to intermediate default
        assert re.search(
            r'(?i)missing.*(?:default|fall\s*back).*intermediate',
            skill_content,
            re.DOTALL
        ), (
            "EC-001: Missing experience field must default to intermediate pacing."
        )

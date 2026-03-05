"""
Test: AC#4 - User Profile Reading
Story: STORY-467 - Dynamic Persona Blend Engine
Generated: 2026-03-04

Validates:
- SKILL.md contains instructions to read user-profile.yaml at session start
- Adjusts persona blend based on profile dimensions
- Graceful fallback if profile missing (default to Coach mode)
- NEVER writes to user-profile.yaml
"""
import os
import re

import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SKILL_PATH = os.path.join(PROJECT_ROOT, "src", "claude", "skills", "coaching-entrepreneur", "SKILL.md")


@pytest.fixture
def skill_content():
    """Read the SKILL.md file content."""
    with open(SKILL_PATH, "r", encoding="utf-8") as f:
        return f.read()


class TestProfileReadingInstructions:
    """Verify SKILL.md instructs reading user-profile.yaml at session start."""

    def test_references_user_profile_yaml(self, skill_content):
        """SKILL.md must reference user-profile.yaml."""
        assert "user-profile.yaml" in skill_content, (
            "SKILL.md must reference user-profile.yaml"
        )

    def test_read_profile_at_session_start(self, skill_content):
        """SKILL.md must instruct reading profile at session start."""
        # Look for read instruction near session start context
        has_read = re.search(r"(?i)read.*user.profile|user.profile.*read", skill_content)
        has_session = re.search(r"(?i)session\s+start", skill_content)
        assert has_read and has_session, (
            "SKILL.md must instruct reading user-profile.yaml at session start"
        )


class TestPersonaBlendAdaptation:
    """Verify persona blend adjusts based on profile dimensions."""

    def test_adapts_based_on_profile(self, skill_content):
        """SKILL.md must describe adapting persona blend based on profile."""
        assert re.search(r"(?i)adapt.*persona|persona.*adapt|adjust.*persona|persona.*adjust", skill_content), (
            "SKILL.md must describe adapting persona blend based on profile dimensions"
        )

    def test_references_profile_dimensions(self, skill_content):
        """SKILL.md must reference profile dimensions for persona adjustment."""
        # Should mention at least one dimension concept (confidence, experience, etc.)
        assert re.search(r"(?i)(dimension|confidence|experience|comfort)", skill_content), (
            "SKILL.md must reference profile dimensions for persona adjustment"
        )


class TestGracefulFallback:
    """Verify graceful fallback when profile is missing."""

    def test_fallback_when_profile_missing(self, skill_content):
        """SKILL.md must handle missing profile gracefully."""
        assert re.search(r"(?i)(missing|unavailable|not\s+found|fallback|default)", skill_content), (
            "SKILL.md must describe fallback behavior when profile is missing"
        )

    def test_default_to_coach_mode(self, skill_content):
        """When profile is missing, default must be Coach mode."""
        # Look for default + coach in proximity
        assert re.search(r"(?i)default.*coach", skill_content), (
            "SKILL.md must default to Coach mode when profile is missing"
        )


class TestNeverWritesToProfile:
    """Verify SKILL.md never instructs writing to user-profile.yaml."""

    def test_no_write_to_profile(self, skill_content):
        """SKILL.md must NOT contain write instructions for user-profile.yaml."""
        # Should not have Write() or write to user-profile.yaml
        has_write_instruction = re.search(
            r"(?i)write.*user.profile\.yaml|edit.*user.profile\.yaml",
            skill_content
        )
        assert not has_write_instruction, (
            "SKILL.md must NEVER instruct writing to user-profile.yaml"
        )

    def test_explicitly_states_read_only(self, skill_content):
        """SKILL.md must explicitly state user-profile.yaml is read-only."""
        assert re.search(r"(?i)(read.only|never\s+write|do\s+not\s+write|must\s+not\s+write).*profile", skill_content), (
            "SKILL.md must explicitly state user-profile.yaml is read-only"
        )

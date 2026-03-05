"""
Test: AC#2 - Coach and Consultant Persona Definitions
Story: STORY-467 - Dynamic Persona Blend Engine
Generated: 2026-03-04

Validates:
- Coach mode defined (empathetic, encouraging, celebrates wins, addresses self-doubt)
- Consultant mode defined (structured, deliverable-focused, professional frameworks)
- Explicit indicators for when to use each persona
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


class TestCoachModeDefinition:
    """Verify Coach mode persona is defined with required characteristics."""

    def test_coach_mode_section_exists(self, skill_content):
        """SKILL.md must have a Coach mode section."""
        assert re.search(r"(?i)##.*coach\s+mode", skill_content), (
            "SKILL.md must contain a 'Coach mode' section heading"
        )

    def test_coach_mode_empathetic(self, skill_content):
        """Coach mode must describe empathetic behavior."""
        assert re.search(r"(?i)empath", skill_content), (
            "Coach mode must describe empathetic behavior"
        )

    def test_coach_mode_encouraging(self, skill_content):
        """Coach mode must describe encouraging behavior."""
        assert re.search(r"(?i)encourag", skill_content), (
            "Coach mode must describe encouraging behavior"
        )

    def test_coach_mode_celebrates_wins(self, skill_content):
        """Coach mode must celebrate wins."""
        assert re.search(r"(?i)celebrat.*win", skill_content), (
            "Coach mode must describe celebrating wins"
        )

    def test_coach_mode_addresses_self_doubt(self, skill_content):
        """Coach mode must address self-doubt."""
        assert re.search(r"(?i)self.doubt", skill_content), (
            "Coach mode must address self-doubt"
        )


class TestConsultantModeDefinition:
    """Verify Consultant mode persona is defined with required characteristics."""

    def test_consultant_mode_section_exists(self, skill_content):
        """SKILL.md must have a Consultant mode section."""
        assert re.search(r"(?i)##.*consultant\s+mode", skill_content), (
            "SKILL.md must contain a 'Consultant mode' section heading"
        )

    def test_consultant_mode_structured(self, skill_content):
        """Consultant mode must describe structured approach."""
        # Look for 'structured' near consultant context
        assert re.search(r"(?i)consultant.*structured|structured.*consultant", skill_content, re.DOTALL), (
            "Consultant mode must describe structured approach"
        )

    def test_consultant_mode_deliverable_focused(self, skill_content):
        """Consultant mode must be deliverable-focused."""
        assert re.search(r"(?i)deliverable", skill_content), (
            "Consultant mode must describe deliverable-focused behavior"
        )

    def test_consultant_mode_professional_frameworks(self, skill_content):
        """Consultant mode must reference professional frameworks."""
        assert re.search(r"(?i)professional\s+framework", skill_content), (
            "Consultant mode must reference professional frameworks"
        )


class TestPersonaTransitionIndicators:
    """Verify explicit indicators for when to use each persona."""

    def test_when_to_use_coach(self, skill_content):
        """SKILL.md must specify when to use Coach mode."""
        # Look for explicit trigger/indicator language for coach
        assert re.search(r"(?i)(when|trigger|indicator|signal|use\s+coach)", skill_content), (
            "SKILL.md must specify when to use Coach mode"
        )

    def test_when_to_use_consultant(self, skill_content):
        """SKILL.md must specify when to use Consultant mode."""
        # Look for explicit trigger/indicator language for consultant
        assert re.search(r"(?i)(when|trigger|indicator|signal|use\s+consultant).*consultant|(consultant).*(when|trigger|indicator|signal)", skill_content, re.DOTALL), (
            "SKILL.md must specify when to use Consultant mode"
        )

    def test_transition_indicators_section(self, skill_content):
        """SKILL.md must have an explicit section for persona transition indicators."""
        assert re.search(r"(?i)##.*(?:transition|indicator|when\s+to|persona\s+select)", skill_content), (
            "SKILL.md must have a section defining persona transition indicators"
        )

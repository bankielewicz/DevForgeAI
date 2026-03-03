"""
Test: AC#7 - Retained Phases Still Functional (Regression Guard)
Story: STORY-438
Generated: 2026-02-18
TDD Phase: RED (tests should FAIL against current source)
"""
import os
import re
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SKILL_MD = os.path.join(PROJECT_ROOT, "src", "claude", "skills", "devforgeai-ideation", "SKILL.md")


@pytest.fixture
def skill_content():
    assert os.path.exists(SKILL_MD), f"SKILL.md not found at {SKILL_MD}"
    with open(SKILL_MD, "r", encoding="utf-8") as f:
        return f.read()


class TestAC7RetainedPhases:
    """Verify retained phases remain intact after phase removal."""

    def test_ac7_phase1_discovery_intact(self, skill_content):
        """AC7(a): Phase 1 (Discovery & Problem Understanding) intact with all references."""
        # Phase 1 header must exist
        assert re.search(r"^#{1,4}\s+.*Phase\s+1\b", skill_content, re.MULTILINE), (
            "Phase 1 header missing from SKILL.md"
        )
        # Discovery workflow reference should be present
        assert "discovery-workflow.md" in skill_content, (
            "discovery-workflow.md reference missing from SKILL.md"
        )

    def test_ac7_phase2_elicitation_intact(self, skill_content):
        """AC7(b): Phase 2 (Requirements Elicitation) intact with question flow."""
        assert re.search(r"^#{1,4}\s+.*Phase\s+2\b", skill_content, re.MULTILINE), (
            "Phase 2 header missing from SKILL.md"
        )
        assert "requirements-elicitation" in skill_content.lower(), (
            "Requirements elicitation reference missing from SKILL.md"
        )

    def test_ac7_phase3_requirements_output_exists(self, skill_content):
        """AC7(c): Phase 3 (renamed to Requirements Output or similar) intact."""
        # After renumbering, old Phase 6 becomes Phase 3
        phase3_match = re.search(r"^#{1,4}\s+.*Phase\s+3\b", skill_content, re.MULTILINE)
        assert phase3_match, (
            "Phase 3 (renumbered Requirements Output) missing from SKILL.md"
        )
        # Should relate to requirements/artifact output, not complexity
        phase3_pos = phase3_match.start()
        # Get text after Phase 3 header (next 500 chars or until next phase)
        snippet = skill_content[phase3_pos:phase3_pos + 500].lower()
        assert "complexity" not in snippet, (
            "Phase 3 still contains complexity content (should be Requirements Output)"
        )

    def test_ac7_brainstorm_context_handling_unchanged(self, skill_content):
        """AC7(d): Brainstorm context handling (from /brainstorm) unchanged."""
        assert "brainstorm" in skill_content.lower(), (
            "Brainstorm context handling missing from SKILL.md"
        )

    def test_ac7_retained_error_types_unchanged(self, skill_content):
        """AC7(e): Error handling for retained phases (error-type-1, error-type-2, error-type-4) unchanged."""
        assert "error-type-1" in skill_content, (
            "error-type-1 reference missing from SKILL.md"
        )
        assert "error-type-2" in skill_content, (
            "error-type-2 reference missing from SKILL.md"
        )
        assert "error-type-4" in skill_content, (
            "error-type-4 reference missing from SKILL.md"
        )

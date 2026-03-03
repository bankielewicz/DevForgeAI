"""
Test: AC#4 - SKILL.md Uses CLI Gates Instead of Marker Files
Story: STORY-517
Generated: 2026-02-28

Tests that the QA SKILL.md has no .qa-phase-N.marker Write() calls
and instead uses CLI gate invocations.
"""

import pytest
from pathlib import Path


SKILL_MD_PATH = Path("/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-qa/SKILL.md")


class TestSkillUsesCliGates:
    """Tests that SKILL.md replaced marker files with CLI gates."""

    def test_should_have_no_marker_write_calls(self):
        """SKILL.md contains no .qa-phase-N.marker Write() calls."""
        # Arrange
        assert SKILL_MD_PATH.exists(), f"SKILL.md not found at {SKILL_MD_PATH}"
        content = SKILL_MD_PATH.read_text()

        # Act & Assert
        # Check for any pattern of writing marker files
        marker_patterns = [
            ".qa-phase-0.marker",
            ".qa-phase-1.marker",
            ".qa-phase-1.5.marker",
            ".qa-phase-2.marker",
            ".qa-phase-3.marker",
            ".qa-phase-4.marker",
            ".qa-phase-N.marker",
            "qa-phase-0.marker",
            "qa-phase-1.marker",
            "qa-phase-1.5.marker",
            "qa-phase-2.marker",
            "qa-phase-3.marker",
            "qa-phase-4.marker",
        ]
        found_markers = [p for p in marker_patterns if p in content]
        assert len(found_markers) == 0, (
            f"SKILL.md still contains marker file references: {found_markers}"
        )

    def test_should_have_cli_gate_calls_for_phases(self):
        """SKILL.md contains devforgeai-validate phase-complete CLI gate calls."""
        # Arrange
        assert SKILL_MD_PATH.exists(), f"SKILL.md not found at {SKILL_MD_PATH}"
        content = SKILL_MD_PATH.read_text()

        # Act & Assert
        assert "phase-complete" in content, (
            "SKILL.md should contain 'phase-complete' CLI gate calls"
        )
        assert "--workflow=qa" in content, (
            "SKILL.md should contain '--workflow=qa' flag in CLI gate calls"
        )

    def test_should_have_phase_init_workflow_qa_in_phase_0(self):
        """SKILL.md Phase 0 contains phase-init --workflow=qa."""
        # Arrange
        assert SKILL_MD_PATH.exists(), f"SKILL.md not found at {SKILL_MD_PATH}"
        content = SKILL_MD_PATH.read_text()

        # Act & Assert
        assert "phase-init" in content and "--workflow=qa" in content, (
            "SKILL.md should contain 'phase-init --workflow=qa' in Phase 0 pre-flight"
        )

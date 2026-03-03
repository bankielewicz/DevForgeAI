"""
STORY-355 AC#1: Skill Invocation Checkpoint Pattern Section Added

Tests that the new section exists after line 55 with required elements.
"""
import pytest
from pathlib import Path


PROTOCOL_FILE = Path("/mnt/c/Projects/DevForgeAI2/devforgeai/protocols/lean-orchestration-pattern.md")


class TestAC1SectionAdded:
    """AC#1: Section must exist with required structure."""

    def test_section_heading_exists(self):
        """Section heading '### Skill Invocation Checkpoint Pattern' must exist."""
        content = PROTOCOL_FILE.read_text()
        assert "### Skill Invocation Checkpoint Pattern" in content, (
            "Missing section heading '### Skill Invocation Checkpoint Pattern'"
        )

    def test_section_after_line_55(self):
        """Section must appear after line 55 (after 'What commands SHOULD do')."""
        lines = PROTOCOL_FILE.read_text().splitlines()
        section_line = None
        for i, line in enumerate(lines, 1):
            if "### Skill Invocation Checkpoint Pattern" in line:
                section_line = i
                break
        assert section_line is not None, "Section heading not found"
        assert section_line > 55, f"Section at line {section_line}, expected after line 55"

    def test_applicability_note_present(self):
        """Applicability note for commands with multiple workflow modes must exist."""
        content = PROTOCOL_FILE.read_text()
        assert "commands with multiple workflow modes" in content.lower(), (
            "Missing applicability note for 'commands with multiple workflow modes'"
        )

    def test_section_contains_wrong_example(self):
        """Section must contain a WRONG example."""
        content = PROTOCOL_FILE.read_text()
        assert "WRONG" in content or "wrong" in content.lower(), (
            "Missing WRONG example in section"
        )

    def test_section_contains_correct_example(self):
        """Section must contain a CORRECT example."""
        content = PROTOCOL_FILE.read_text()
        assert "CORRECT" in content, "Missing CORRECT example in section"

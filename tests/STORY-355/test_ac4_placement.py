"""
STORY-355 AC#4: Section Placement Correct

Tests that section appears after 'What commands SHOULD do' and before 'What commands should NOT do'.
"""
import pytest
from pathlib import Path


PROTOCOL_FILE = Path("/mnt/c/Projects/DevForgeAI2/devforgeai/protocols/lean-orchestration-pattern.md")


class TestAC4Placement:
    """AC#4: Section must be correctly placed between existing sections."""

    def test_section_after_should_do(self):
        """Section must appear after 'What commands SHOULD do' list."""
        content = PROTOCOL_FILE.read_text()
        should_do_pos = content.find("What commands SHOULD do")
        section_pos = content.find("### Skill Invocation Checkpoint Pattern")

        assert should_do_pos != -1, "'What commands SHOULD do' section not found"
        assert section_pos != -1, "Skill Invocation Checkpoint Pattern section not found"
        assert section_pos > should_do_pos, (
            f"Section at pos {section_pos} must be after 'What commands SHOULD do' at pos {should_do_pos}"
        )

    def test_section_before_should_not_do(self):
        """Section must appear before 'What commands should NOT do' section."""
        content = PROTOCOL_FILE.read_text()
        should_not_do_pos = content.find("What commands should NOT do")
        section_pos = content.find("### Skill Invocation Checkpoint Pattern")

        assert should_not_do_pos != -1, "'What commands should NOT do' section not found"
        assert section_pos != -1, "Skill Invocation Checkpoint Pattern section not found"
        assert section_pos < should_not_do_pos, (
            f"Section at pos {section_pos} must be before 'should NOT do' at pos {should_not_do_pos}"
        )

    def test_section_line_range(self):
        """Section should appear around lines 55-60 based on story spec."""
        lines = PROTOCOL_FILE.read_text().splitlines()
        section_line = None
        for i, line in enumerate(lines, 1):
            if "### Skill Invocation Checkpoint Pattern" in line:
                section_line = i
                break

        assert section_line is not None, "Section heading not found"
        # Allow some flexibility (55-70) for section placement
        assert 55 <= section_line <= 70, (
            f"Section at line {section_line}, expected between lines 55-70"
        )

    def test_maintains_document_structure(self):
        """New section must not break existing document structure."""
        content = PROTOCOL_FILE.read_text()

        # Verify key existing sections still present in order
        sections = [
            "What commands SHOULD do",
            "What commands should NOT do",
            "Skill Responsibilities",
        ]

        last_pos = -1
        for section in sections:
            pos = content.find(section)
            assert pos != -1, f"Missing expected section: {section}"
            assert pos > last_pos, f"Section '{section}' out of order"
            last_pos = pos

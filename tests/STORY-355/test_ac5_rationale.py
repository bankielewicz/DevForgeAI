"""
STORY-355 AC#5: Rationale Provided

Tests that rationale statement explains why explicit syntax prevents ambiguity.
"""
import pytest
from pathlib import Path


PROTOCOL_FILE = Path("/mnt/c/Projects/DevForgeAI2/devforgeai/protocols/lean-orchestration-pattern.md")


class TestAC5Rationale:
    """AC#5: Rationale statement must explain the pattern's purpose."""

    def test_rationale_section_exists(self):
        """Rationale statement or section must exist."""
        content = PROTOCOL_FILE.read_text()
        # Look for Rationale header or inline rationale
        has_rationale = (
            "Rationale" in content or
            "rationale" in content.lower() or
            "why" in content.lower()
        )
        assert has_rationale, "No rationale statement found in section"

    def test_rationale_mentions_ambiguity(self):
        """Rationale must mention ambiguity problem."""
        content = PROTOCOL_FILE.read_text()
        assert "ambiguity" in content.lower() or "ambiguous" in content.lower(), (
            "Rationale does not mention 'ambiguity'"
        )

    def test_rationale_mentions_summary_language(self):
        """Rationale must explain that summary language creates problems."""
        content = PROTOCOL_FILE.read_text()
        # Look for explanation about summary language issues
        has_summary_ref = (
            "summary" in content.lower() or
            "arrow" in content.lower() or
            "implicit" in content.lower()
        )
        assert has_summary_ref, (
            "Rationale does not explain summary language problem"
        )

    def test_rationale_mentions_explicit_syntax(self):
        """Rationale must explain that explicit syntax is unambiguous."""
        content = PROTOCOL_FILE.read_text()
        has_explicit = "explicit" in content.lower() or "unambiguous" in content.lower()
        assert has_explicit, (
            "Rationale does not mention explicit syntax benefit"
        )

    def test_rationale_in_correct_section(self):
        """Rationale must be within the Skill Invocation Checkpoint Pattern section."""
        content = PROTOCOL_FILE.read_text()
        section_start = content.find("### Skill Invocation Checkpoint Pattern")

        if section_start == -1:
            pytest.fail("Section not found")

        # Find next H3 section or end, but skip headers inside code blocks
        # Look for "\n### " that's NOT inside a code block
        pos = section_start + 1
        in_code_block = False
        next_section = -1

        lines = content[section_start:].split('\n')
        char_count = section_start

        for i, line in enumerate(lines):
            if i == 0:
                char_count += len(line) + 1
                continue
            if line.startswith('```'):
                in_code_block = not in_code_block
            elif line.startswith('### ') and not in_code_block:
                next_section = char_count
                break
            char_count += len(line) + 1

        if next_section == -1:
            next_section = len(content)

        section_content = content[section_start:next_section]

        # Rationale should be in this section
        assert "rationale" in section_content.lower(), (
            "Rationale not within Skill Invocation Checkpoint Pattern section"
        )

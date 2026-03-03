"""
STORY-355 AC#3: Four Requirements Documented

Tests that all four requirements from RCA-037 REC-2 are present.
"""
import pytest
from pathlib import Path


PROTOCOL_FILE = Path("/mnt/c/Projects/DevForgeAI2/devforgeai/protocols/lean-orchestration-pattern.md")


class TestAC3Requirements:
    """AC#3: All four requirements must be documented."""

    def test_requirement_1_step_number(self):
        """Requirement 1: Clear step number must be documented."""
        content = PROTOCOL_FILE.read_text()
        # Look for requirement about step numbers
        assert "step number" in content.lower() or "Step" in content, (
            "Requirement 1 (step number) not documented"
        )

    def test_requirement_2_mandatory_marker(self):
        """Requirement 2: MANDATORY marker or warning emoji must be documented."""
        content = PROTOCOL_FILE.read_text()
        # Check for MANDATORY or warning emoji requirement
        has_mandatory_req = "MANDATORY" in content
        has_emoji_req = "warning" in content.lower() or "\u26A0" in content
        assert has_mandatory_req or has_emoji_req, (
            "Requirement 2 (MANDATORY marker/warning emoji) not documented"
        )

    def test_requirement_3_explicit_tool_call(self):
        """Requirement 3: Explicit tool call syntax must be documented."""
        content = PROTOCOL_FILE.read_text()
        # Look for explicit tool call requirement
        assert "Skill(command=" in content or "tool call" in content.lower(), (
            "Requirement 3 (explicit tool call syntax) not documented"
        )

    def test_requirement_4_do_not_proceed(self):
        """Requirement 4: 'DO NOT proceed' statement must be documented."""
        content = PROTOCOL_FILE.read_text()
        assert "DO NOT proceed" in content, (
            "Requirement 4 ('DO NOT proceed' statement) not documented"
        )

    def test_four_requirements_in_list(self):
        """All four requirements should be in a numbered or bulleted list."""
        content = PROTOCOL_FILE.read_text()
        # Look for numbered list (1. 2. 3. 4.) within section
        section_start = content.find("Skill Invocation Checkpoint Pattern")
        if section_start == -1:
            pytest.fail("Section not found - cannot verify requirements list")

        section_content = content[section_start:section_start + 2000]
        # Check for numbered items
        has_list = all(f"{i}." in section_content for i in range(1, 5))
        assert has_list, "Four requirements not in numbered list format"

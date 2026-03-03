"""
STORY-355 AC#2: WRONG vs CORRECT Examples Present

Tests that both examples contain required elements.
"""
import pytest
from pathlib import Path


PROTOCOL_FILE = Path("/mnt/c/Projects/DevForgeAI2/devforgeai/protocols/lean-orchestration-pattern.md")


class TestAC2Examples:
    """AC#2: WRONG and CORRECT examples with required elements."""

    def test_wrong_example_shows_summary_language(self):
        """WRONG example must show summary language like 'Skill' arrow notation."""
        content = PROTOCOL_FILE.read_text()
        # Look for summary arrow pattern in WRONG example context
        assert "Loop:" in content or "Markers" in content, (
            "WRONG example missing summary language pattern"
        )

    def test_correct_example_has_step_number(self):
        """CORRECT example must include step number (e.g., 'Step 4.3')."""
        content = PROTOCOL_FILE.read_text()
        assert "Step" in content and "4.3" in content or "step" in content.lower(), (
            "CORRECT example missing step number"
        )

    def test_correct_example_has_warning_emoji(self):
        """CORRECT example must include warning emoji."""
        content = PROTOCOL_FILE.read_text()
        # Check for warning emoji or MANDATORY marker
        has_warning = any(char in content for char in ["\u26A0", "\u26A0\uFE0F"])
        assert has_warning, "CORRECT example missing warning emoji"

    def test_correct_example_has_mandatory_marker(self):
        """CORRECT example must include MANDATORY marker."""
        content = PROTOCOL_FILE.read_text()
        assert "MANDATORY" in content, "CORRECT example missing MANDATORY marker"

    def test_correct_example_has_skill_command_syntax(self):
        """CORRECT example must have explicit Skill(command='...') syntax."""
        content = PROTOCOL_FILE.read_text()
        assert 'Skill(command="' in content or "Skill(command='" in content, (
            "CORRECT example missing explicit Skill(command=...) syntax"
        )

    def test_correct_example_has_do_not_proceed_statement(self):
        """CORRECT example must have 'DO NOT proceed' statement."""
        content = PROTOCOL_FILE.read_text()
        assert "DO NOT proceed" in content or "do not proceed" in content.lower(), (
            "CORRECT example missing 'DO NOT proceed' statement"
        )

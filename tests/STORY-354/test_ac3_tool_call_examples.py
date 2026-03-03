"""
STORY-354: Add Explicit Skill Invocation to Epic Batch Workflow
AC#3 Tests: Tool Call Syntax Examples in Steps 1-3

Tests validate Steps 1-3 contain explicit tool call examples.
"""

import pytest
from pathlib import Path

pytestmark = [pytest.mark.story_354, pytest.mark.ac3]

PROJECT_ROOT = Path(__file__).parent.parent.parent
TARGET_FILE = PROJECT_ROOT / "src" / "claude" / "commands" / "create-story.md"


class TestAC3ToolCallExamples:
    """AC#3: Tool Call Syntax Examples in Steps 1-3."""

    def test_step1_contains_grep_example(self):
        """Step 1 must contain Grep code block for feature extraction."""
        content = TARGET_FILE.read_text()
        # Look for Grep pattern in Step 1 context
        assert "Grep(" in content and "Feature" in content, \
            "Step 1 missing Grep code block for feature extraction"

    def test_step2_contains_askuserquestion_multiselect(self):
        """Step 2 must contain AskUserQuestion with multiSelect: true."""
        content = TARGET_FILE.read_text()
        assert "AskUserQuestion(" in content and "multiSelect" in content, \
            "Step 2 missing AskUserQuestion with multiSelect parameter"

    def test_step2_multiselect_true(self):
        """Step 2 AskUserQuestion must have multiSelect: true."""
        content = TARGET_FILE.read_text()
        assert "multiSelect: true" in content or 'multiSelect":true' in content or \
               "multiSelect=true" in content, \
            "Step 2 AskUserQuestion must have multiSelect: true"

    def test_step3_contains_askuserquestion_metadata(self):
        """Step 3 must contain AskUserQuestion for batch metadata."""
        content = TARGET_FILE.read_text()
        # Count AskUserQuestion occurrences - should have at least 2 (Step 2 and Step 3)
        count = content.count("AskUserQuestion(")
        assert count >= 2, \
            f"Expected at least 2 AskUserQuestion calls (Steps 2 & 3), found {count}"

    def test_grep_in_code_block(self):
        """Grep example must be in a code block."""
        content = TARGET_FILE.read_text()
        lines = content.split('\n')
        in_code_block = False
        grep_in_block = False
        for line in lines:
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
            if in_code_block and 'Grep(' in line:
                grep_in_block = True
                break
        assert grep_in_block, \
            "Grep example must appear within a code block"

    def test_askuserquestion_in_code_block(self):
        """AskUserQuestion examples must be in code blocks."""
        content = TARGET_FILE.read_text()
        lines = content.split('\n')
        in_code_block = False
        ask_in_block = False
        for line in lines:
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
            if in_code_block and 'AskUserQuestion(' in line:
                ask_in_block = True
                break
        assert ask_in_block, \
            "AskUserQuestion must appear within a code block"

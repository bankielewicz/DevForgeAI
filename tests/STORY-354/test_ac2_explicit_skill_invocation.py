"""
STORY-354: Add Explicit Skill Invocation to Epic Batch Workflow
AC#2 Tests: Explicit Skill Invocation in Step 4.3

Tests validate Step 4.3 contains explicit Skill() invocation with warning markers.
"""

import pytest
from pathlib import Path

pytestmark = [pytest.mark.story_354, pytest.mark.ac2]

PROJECT_ROOT = Path(__file__).parent.parent.parent
TARGET_FILE = PROJECT_ROOT / "src" / "claude" / "commands" / "create-story.md"


class TestAC2ExplicitSkillInvocation:
    """AC#2: Explicit Skill Invocation in Step 4.3."""

    def test_step_4_3_contains_mandatory_marker(self):
        """Step 4.3 must contain INVOKE SKILL NOW (MANDATORY) text."""
        content = TARGET_FILE.read_text()
        assert "INVOKE SKILL NOW (MANDATORY)" in content, \
            "Step 4.3 missing 'INVOKE SKILL NOW (MANDATORY)' marker"

    def test_step_4_3_contains_warning_emoji(self):
        """Step 4.3 must contain warning emoji before MANDATORY marker."""
        content = TARGET_FILE.read_text()
        # Check for warning emoji pattern with MANDATORY
        assert "**\u26a0\ufe0f INVOKE SKILL NOW (MANDATORY):**" in content or \
               "**:warning: INVOKE SKILL NOW (MANDATORY):**" in content, \
            "Step 4.3 missing warning emoji pattern"

    def test_step_4_3_contains_explicit_skill_command(self):
        """Step 4.3 must contain explicit Skill(command=...) invocation."""
        content = TARGET_FILE.read_text()
        assert 'Skill(command="devforgeai-story-creation")' in content, \
            "Step 4.3 missing explicit 'Skill(command=\"devforgeai-story-creation\")'"

    def test_step_4_3_contains_do_not_proceed_warning(self):
        """Step 4.3 must contain 'DO NOT proceed with manual analysis' warning."""
        content = TARGET_FILE.read_text()
        assert "DO NOT proceed with manual analysis" in content, \
            "Step 4.3 missing 'DO NOT proceed with manual analysis' warning"

    def test_skill_invocation_in_code_block(self):
        """Skill invocation must be in a code block."""
        content = TARGET_FILE.read_text()
        # Check that Skill command appears within code block context
        lines = content.split('\n')
        in_code_block = False
        skill_in_block = False
        for line in lines:
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
            if in_code_block and 'Skill(command="devforgeai-story-creation")' in line:
                skill_in_block = True
                break
        assert skill_in_block, \
            "Skill(command=...) must appear within a code block"

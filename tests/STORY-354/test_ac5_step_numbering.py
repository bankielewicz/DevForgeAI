"""
STORY-354: Add Explicit Skill Invocation to Epic Batch Workflow
AC#5 Tests: Step Numbering Consistency

Tests validate all steps use "### Step N:" format with substeps 4.1-4.4.
"""

import pytest
from pathlib import Path
import re

pytestmark = [pytest.mark.story_354, pytest.mark.ac5]

PROJECT_ROOT = Path(__file__).parent.parent.parent
TARGET_FILE = PROJECT_ROOT / "src" / "claude" / "commands" / "create-story.md"


class TestAC5StepNumbering:
    """AC#5: Step Numbering Consistency."""

    def test_step_format_uses_h3_heading(self):
        """All steps must use ### (H3) markdown heading format."""
        content = TARGET_FILE.read_text()
        # Find all Step N patterns and verify they use ###
        step_lines = [line for line in content.split('\n')
                     if 'Step ' in line and ':' in line]

        h3_steps = [line for line in step_lines
                   if line.strip().startswith('### Step')]

        assert len(h3_steps) >= 5, \
            f"Expected at least 5 steps with '### Step N:' format, found {len(h3_steps)}"

    def test_step1_uses_correct_format(self):
        """Step 1 must use '### Step 1:' format."""
        content = TARGET_FILE.read_text()
        assert re.search(r"### Step 1:", content), \
            "Step 1 not using '### Step 1:' format"

    def test_step2_uses_correct_format(self):
        """Step 2 must use '### Step 2:' format."""
        content = TARGET_FILE.read_text()
        assert re.search(r"### Step 2:", content), \
            "Step 2 not using '### Step 2:' format"

    def test_step3_uses_correct_format(self):
        """Step 3 must use '### Step 3:' format."""
        content = TARGET_FILE.read_text()
        assert re.search(r"### Step 3:", content), \
            "Step 3 not using '### Step 3:' format"

    def test_step4_uses_correct_format(self):
        """Step 4 must use '### Step 4:' format."""
        content = TARGET_FILE.read_text()
        assert re.search(r"### Step 4:", content), \
            "Step 4 not using '### Step 4:' format"

    def test_step5_uses_correct_format(self):
        """Step 5 must use '### Step 5:' format."""
        content = TARGET_FILE.read_text()
        assert re.search(r"### Step 5:", content), \
            "Step 5 not using '### Step 5:' format"

    def test_substep_4_1_exists(self):
        """Substep 4.1 must exist."""
        content = TARGET_FILE.read_text()
        assert "4.1" in content, \
            "Substep 4.1 not found"

    def test_substep_4_2_exists(self):
        """Substep 4.2 must exist."""
        content = TARGET_FILE.read_text()
        assert "4.2" in content, \
            "Substep 4.2 not found"

    def test_substep_4_3_exists(self):
        """Substep 4.3 must exist."""
        content = TARGET_FILE.read_text()
        assert "4.3" in content, \
            "Substep 4.3 not found"

    def test_substep_4_4_exists(self):
        """Substep 4.4 must exist."""
        content = TARGET_FILE.read_text()
        assert "4.4" in content, \
            "Substep 4.4 not found"

    def test_all_substeps_present(self):
        """All substeps 4.1, 4.2, 4.3, 4.4 must be present."""
        content = TARGET_FILE.read_text()
        substeps = ["4.1", "4.2", "4.3", "4.4"]
        missing = [s for s in substeps if s not in content]
        assert not missing, \
            f"Missing substeps: {missing}"

    def test_step_numbering_sequential(self):
        """Steps must be numbered sequentially 1-5."""
        content = TARGET_FILE.read_text()
        step_pattern = r"### Step (\d):"
        matches = re.findall(step_pattern, content)

        # Convert to integers and check sequence
        step_nums = sorted([int(m) for m in matches])
        expected = [1, 2, 3, 4, 5]

        assert step_nums == expected, \
            f"Step numbering not sequential. Found: {step_nums}, Expected: {expected}"

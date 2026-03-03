"""
STORY-354: Add Explicit Skill Invocation to Epic Batch Workflow
AC#1 Tests: Replace Epic Batch Workflow Section with Detailed Steps

Tests validate that lines 46-67 are replaced with Steps 1-5 with detailed substeps.
"""

import pytest
from pathlib import Path
import re

pytestmark = [pytest.mark.story_354, pytest.mark.ac1]

PROJECT_ROOT = Path(__file__).parent.parent.parent
TARGET_FILE = PROJECT_ROOT / "src" / "claude" / "commands" / "create-story.md"


class TestAC1WorkflowStructure:
    """AC#1: Replace Epic Batch Workflow Section with Detailed Steps."""

    def test_epic_batch_workflow_section_exists(self):
        """Epic Batch Workflow section must exist in command file."""
        content = TARGET_FILE.read_text()
        assert "## Epic Batch Workflow" in content, \
            "Epic Batch Workflow section header not found"

    def test_step1_extract_features_exists(self):
        """Step 1: Extract Features from Epic must exist."""
        content = TARGET_FILE.read_text()
        assert "### Step 1:" in content and "Extract" in content, \
            "Step 1 (Extract Features) not found with ### Step N: format"

    def test_step2_multi_select_features_exists(self):
        """Step 2: Multi-Select Features must exist."""
        content = TARGET_FILE.read_text()
        assert "### Step 2:" in content, \
            "Step 2 (Multi-Select Features) not found with ### Step N: format"

    def test_step3_batch_metadata_exists(self):
        """Step 3: Batch Metadata must exist."""
        content = TARGET_FILE.read_text()
        assert "### Step 3:" in content, \
            "Step 3 (Batch Metadata) not found with ### Step N: format"

    def test_step4_story_creation_loop_exists(self):
        """Step 4: Story Creation Loop must exist."""
        content = TARGET_FILE.read_text()
        assert "### Step 4:" in content, \
            "Step 4 (Story Creation Loop) not found with ### Step N: format"

    def test_step5_summary_exists(self):
        """Step 5: Summary must exist."""
        content = TARGET_FILE.read_text()
        assert "### Step 5:" in content, \
            "Step 5 (Summary) not found with ### Step N: format"

    def test_all_five_steps_present(self):
        """All 5 steps must be present in Epic Batch Workflow section."""
        content = TARGET_FILE.read_text()
        step_pattern = r"### Step (\d):"
        matches = re.findall(step_pattern, content)
        step_numbers = set(matches)
        expected = {"1", "2", "3", "4", "5"}
        assert expected.issubset(step_numbers), \
            f"Missing steps. Found: {step_numbers}, Expected: {expected}"

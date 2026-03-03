"""
STORY-354: Add Explicit Skill Invocation to Epic Batch Workflow
AC#4 Tests: Workflow Discipline Reminder

Tests validate reminder box after "Triggered:" line with 4 warning points.
"""

import pytest
from pathlib import Path
import re

pytestmark = [pytest.mark.story_354, pytest.mark.ac4]

PROJECT_ROOT = Path(__file__).parent.parent.parent
TARGET_FILE = PROJECT_ROOT / "src" / "claude" / "commands" / "create-story.md"


class TestAC4DisciplineReminder:
    """AC#4: Workflow Discipline Reminder."""

    def test_triggered_line_exists(self):
        """Triggered: MODE='EPIC_BATCH' line must exist."""
        content = TARGET_FILE.read_text()
        assert "Triggered:" in content and "EPIC_BATCH" in content, \
            "Triggered line with EPIC_BATCH not found"

    def test_reminder_box_after_triggered(self):
        """Reminder box must appear after Triggered: line."""
        content = TARGET_FILE.read_text()
        triggered_idx = content.find("Triggered:")
        assert triggered_idx != -1, "Triggered: line not found"

        # Look for reminder content after triggered line
        after_triggered = content[triggered_idx:]
        # Reminder should mention following steps or workflow discipline
        has_reminder = ("follow" in after_triggered.lower() and
                       "step" in after_triggered.lower()) or \
                      "IMPORTANT" in after_triggered or \
                      "WARNING" in after_triggered or \
                      "discipline" in after_triggered.lower()
        assert has_reminder, \
            "Workflow discipline reminder not found after Triggered: line"

    def test_warning_follow_steps_in_order(self):
        """Reminder must warn to follow steps 1-5 IN ORDER."""
        content = TARGET_FILE.read_text()
        # Check for order/sequence warning
        has_order_warning = ("IN ORDER" in content.upper() or
                            "in order" in content.lower() or
                            "sequential" in content.lower())
        assert has_order_warning, \
            "Reminder missing 'follow steps IN ORDER' warning"

    def test_warning_not_add_preparatory_analysis(self):
        """Reminder must warn NOT to add preparatory analysis steps."""
        content = TARGET_FILE.read_text()
        has_no_prep_warning = ("NOT add" in content or
                              "DO NOT add" in content or
                              "preparatory" in content.lower() or
                              "do not add" in content.lower())
        assert has_no_prep_warning, \
            "Reminder missing 'NOT add preparatory analysis' warning"

    def test_warning_not_skip_ahead(self):
        """Reminder must warn NOT to skip ahead or optimize."""
        content = TARGET_FILE.read_text()
        has_no_skip_warning = ("NOT skip" in content or
                              "DO NOT skip" in content or
                              "do not skip" in content.lower() or
                              "optimize" in content.lower())
        assert has_no_skip_warning, \
            "Reminder missing 'NOT skip ahead or optimize' warning"

    def test_warning_skill_handles_complexity(self):
        """Reminder must state skill handles all complexity."""
        content = TARGET_FILE.read_text()
        has_skill_handles = ("skill handles" in content.lower() or
                            "handles all" in content.lower() or
                            "skill does" in content.lower())
        assert has_skill_handles, \
            "Reminder missing 'skill handles all complexity' statement"

    def test_four_warning_points_present(self):
        """Reminder must contain at least 4 warning points."""
        content = TARGET_FILE.read_text()
        # Count bullet points or numbered items in Epic Batch section
        batch_start = content.find("## Epic Batch Workflow")
        batch_end = content.find("## Phase 1:", batch_start) if batch_start != -1 else len(content)
        batch_section = content[batch_start:batch_end] if batch_start != -1 else ""

        # Count warning indicators (bullets, numbered items, or warning statements)
        warning_patterns = [
            r"- NOT",
            r"- DO NOT",
            r"\d\. NOT",
            r"\d\. DO NOT",
            r"follow.*step",
            r"NOT add",
            r"NOT skip",
            r"skill handles"
        ]
        warning_count = sum(1 for p in warning_patterns
                          if re.search(p, batch_section, re.IGNORECASE))
        assert warning_count >= 4, \
            f"Expected at least 4 warning points, found patterns matching: {warning_count}"

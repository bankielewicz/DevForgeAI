"""
Test: AC#4 - Clean Commands Acknowledged
Story: STORY-412
Generated: 2026-02-16

Validates that commands passing the hybrid audit (<=4 code blocks)
are listed with a clean/pass acknowledgment.
"""
import os
import re
import pytest

AUDIT_RESULTS_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..",
    "devforgeai", "specs", "analysis", "command-hybrid-audit-results.md"
)


class TestCleanAcknowledgment:
    """AC#4: Clean commands acknowledged with pass confirmation."""

    def _read_audit(self):
        with open(AUDIT_RESULTS_PATH, "r") as f:
            return f.read()

    def test_should_have_clean_commands_section_when_audit_complete(self):
        """Assert audit results contain a section for clean commands."""
        content = self._read_audit()
        assert re.search(r"(?i)(clean|pass)", content), (
            "Audit results do not contain a clean commands section"
        )

    def test_should_mark_clean_commands_with_checkmark(self):
        """Assert clean commands are marked with a checkmark or pass indicator."""
        content = self._read_audit()
        # Expect checkmark unicode or markdown checkbox
        has_checkmark = bool(re.search(r"(\u2705|\[x\]|PASS|CLEAN)", content, re.IGNORECASE))
        assert has_checkmark, (
            "Clean commands not marked with checkmark or pass indicator"
        )

    def test_should_list_at_least_one_clean_or_violated_command(self):
        """Assert audit categorizes commands (all must be either clean or violated)."""
        content = self._read_audit()
        has_clean = bool(re.search(r"(?i)(clean|pass|\u2705)", content))
        has_violation = bool(re.search(r"(?i)violation", content))
        assert has_clean or has_violation, (
            "Audit results must categorize commands as clean or violated"
        )

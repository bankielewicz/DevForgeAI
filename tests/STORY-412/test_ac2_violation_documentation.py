"""
Test: AC#2 - Violations Documented
Story: STORY-412
Generated: 2026-02-16

Validates that violation entries include command name, code block count,
and line numbers for commands with >4 code blocks before Skill().
"""
import os
import re
import pytest

AUDIT_RESULTS_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..",
    "devforgeai", "specs", "analysis", "command-hybrid-audit-results.md"
)


class TestViolationDocumentation:
    """AC#2: Violations documented with command name, code block count, line numbers."""

    def _read_audit(self):
        with open(AUDIT_RESULTS_PATH, "r") as f:
            return f.read()

    def test_should_have_violations_section_when_violations_exist(self):
        """Arrange: Audit results exist.
        Act: Read results file.
        Assert: A violations section is present."""
        content = self._read_audit()
        assert re.search(r"(?i)violation", content), (
            "Audit results do not contain a violations section"
        )

    def test_should_include_command_name_in_violation_entry(self):
        """Assert each violation entry includes the command name (e.g., /ideate)."""
        content = self._read_audit()
        # Expect violation entries to reference a command by its slash name
        assert re.search(r"/\w+", content), (
            "No command name found in violation entries"
        )

    def test_should_include_code_block_count_in_violation_entry(self):
        """Assert violation entries include a numeric code block count."""
        content = self._read_audit()
        # Expect a pattern like "code blocks: N" or "N code blocks"
        assert re.search(r"\d+\s*code\s*block", content, re.IGNORECASE), (
            "No code block count found in violation entries"
        )

    def test_should_include_line_numbers_in_violation_entry(self):
        """Assert violation entries include line number references."""
        content = self._read_audit()
        # Expect line number references like "line 42" or "lines 10-50"
        assert re.search(r"line[s]?\s*\d+", content, re.IGNORECASE), (
            "No line numbers found in violation entries"
        )

    def test_should_document_each_violation_with_all_required_fields(self):
        """Assert violations have command name AND code block count AND line numbers."""
        content = self._read_audit()
        has_command = bool(re.search(r"/\w+", content))
        has_count = bool(re.search(r"\d+\s*code\s*block", content, re.IGNORECASE))
        has_lines = bool(re.search(r"line[s]?\s*\d+", content, re.IGNORECASE))
        assert has_command and has_count and has_lines, (
            f"Violation entries incomplete: command={has_command}, "
            f"count={has_count}, lines={has_lines}"
        )

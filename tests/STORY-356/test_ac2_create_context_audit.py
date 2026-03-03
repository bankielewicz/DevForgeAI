"""
STORY-356 AC#2: Audit /create-context command for explicit Skill(command="...") syntax.

Tests verify that src/claude/commands/create-context.md contains an explicit
Skill(command="devforgeai-architecture") invocation.

TDD Red Phase: These tests WILL FAIL because the audit_skill_invocation module
does not exist yet.
"""
import re
from pathlib import Path

import pytest

# This import will fail (TDD Red) - module does not exist yet
from audit_skill_invocation import audit_command, AuditResult


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
COMMAND_NAME = "create-context"
EXPECTED_SKILL = "devforgeai-architecture"
COMMAND_FILE = Path(
    "/mnt/c/Projects/DevForgeAI2/src/claude/commands/create-context.md"
)


class TestAC2CreateContextAudit:
    """AC#2: Audit /create-context command for Skill(command="devforgeai-architecture")."""

    # --- Happy Path ---

    def test_should_find_command_file_when_create_context_exists(self):
        """Verify that create-context.md exists in src/claude/commands/."""
        result = audit_command(COMMAND_NAME, EXPECTED_SKILL)
        assert result.file_found is True, (
            f"Expected {COMMAND_FILE} to exist but audit reported file not found"
        )

    def test_should_detect_explicit_skill_invocation_when_create_context_audited(self):
        """Verify explicit Skill(command="devforgeai-architecture") syntax is found."""
        result = audit_command(COMMAND_NAME, EXPECTED_SKILL)
        assert result.compliant is True, (
            f"Expected compliant=True for {COMMAND_NAME} but got {result.compliant}. "
            f"Pattern Skill(command=\"{EXPECTED_SKILL}\") not found."
        )

    def test_should_report_line_number_when_skill_invocation_found(self):
        """Verify the audit reports the line number where Skill() was found."""
        result = audit_command(COMMAND_NAME, EXPECTED_SKILL)
        assert result.line_number is not None, (
            "Expected line_number to be populated when Skill() invocation found"
        )
        assert result.line_number > 0, (
            f"Expected positive line number, got {result.line_number}"
        )

    def test_should_match_exact_skill_name_when_create_context_audited(self):
        """Verify the matched skill name is exactly 'devforgeai-architecture'."""
        result = audit_command(COMMAND_NAME, EXPECTED_SKILL)
        assert result.skill_name == EXPECTED_SKILL, (
            f"Expected skill_name='{EXPECTED_SKILL}', got '{result.skill_name}'"
        )

    def test_should_report_compliant_status_when_explicit_syntax_present(self):
        """Verify status is 'COMPLIANT' when explicit Skill() syntax found."""
        result = audit_command(COMMAND_NAME, EXPECTED_SKILL)
        assert result.status == "COMPLIANT", (
            f"Expected status='COMPLIANT', got '{result.status}'"
        )

    def test_should_report_no_remediation_needed_when_compliant(self):
        """Verify remediation_needed is False when command is compliant."""
        result = audit_command(COMMAND_NAME, EXPECTED_SKILL)
        assert result.remediation_needed is False, (
            "Expected remediation_needed=False for compliant command"
        )

    # --- BR-001: Regex pattern matching ---

    def test_should_match_br001_regex_when_skill_invocation_present(self):
        """BR-001: Pattern must match regex Skill\\(command="[a-z0-9-]+"."""
        result = audit_command(COMMAND_NAME, EXPECTED_SKILL)
        pattern = re.compile(r'Skill\(command="[a-z0-9-]+"')
        assert result.matched_text is not None, "Expected matched_text to be populated"
        assert pattern.search(result.matched_text), (
            f"BR-001 regex did not match: {result.matched_text}"
        )

    # --- BR-002: Summary language detection ---

    def test_should_not_count_summary_language_as_compliant(self):
        """BR-002: Summary language like '-> Skill ->' is NOT compliant."""
        fake_content = "Workflow: Input -> Skill -> devforgeai-architecture output"
        result = audit_command(
            COMMAND_NAME, EXPECTED_SKILL, content_override=fake_content
        )
        assert result.compliant is False, (
            "Summary language should NOT be counted as compliant (BR-002)"
        )

    # --- Edge Case: Skill() in WRONG example section ---

    def test_should_not_count_wrong_example_as_compliant(self):
        """Skill() in a WRONG example section should NOT count as compliant."""
        fake_content = (
            "**WRONG** (Bad pattern):\n"
            "```\n"
            'Skill(command="devforgeai-architecture")\n'
            "```\n"
        )
        result = audit_command(
            COMMAND_NAME, EXPECTED_SKILL, content_override=fake_content
        )
        assert result.compliant is False, (
            "Skill() in WRONG example section should not count as compliant"
        )


class TestAC2CreateContextAuditEdgeCases:
    """Edge case tests for AC#2 create-context audit."""

    def test_should_handle_missing_file_gracefully(self):
        """Missing command file should report NOT FOUND, not raise exception."""
        result = audit_command("totally-fake-command", EXPECTED_SKILL)
        assert result.file_found is False
        assert result.status == "NOT FOUND"
        assert result.compliant is False

    def test_should_detect_multiple_skill_invocations(self):
        """Multiple Skill() invocations should all be captured."""
        fake_content = (
            'Line one\n'
            'Skill(command="devforgeai-architecture")\n'
            'More text\n'
            'Skill(command="devforgeai-architecture")\n'
            'Even more text\n'
            'Skill(command="devforgeai-architecture")\n'
        )
        result = audit_command(
            COMMAND_NAME, EXPECTED_SKILL, content_override=fake_content
        )
        assert result.compliant is True
        assert result.invocation_count >= 3, (
            f"Expected at least 3 invocations, got {result.invocation_count}"
        )

    def test_should_report_command_name_in_result(self):
        """Result should include the command name being audited."""
        result = audit_command(COMMAND_NAME, EXPECTED_SKILL)
        assert result.command_name == COMMAND_NAME

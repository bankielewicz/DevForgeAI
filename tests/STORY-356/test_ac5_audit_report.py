"""
STORY-356 AC#5: Generate Audit Summary Report.

Tests verify that the audit module can compile findings from AC1-AC4 into a
structured report containing: command name, skill invoked, line number,
compliance status, and remediation needed.

TDD Red Phase: These tests WILL FAIL because the audit_skill_invocation module
does not exist yet.
"""
from typing import Dict, List

import pytest

# This import will fail (TDD Red) - module does not exist yet
from audit_skill_invocation import (
    audit_command,
    generate_audit_report,
    AuditResult,
    AuditReport,
)


# ---------------------------------------------------------------------------
# Constants: Command -> Expected Skill mapping (AC1-AC4)
# ---------------------------------------------------------------------------
AUDIT_COMMANDS = {
    "ideate": "devforgeai-ideation",
    "create-context": "devforgeai-architecture",
    "create-epic": "devforgeai-orchestration",
    "brainstorm": "devforgeai-brainstorming",
}


class TestAC5AuditReportGeneration:
    """AC#5: Compile findings from AC1-AC4 into audit summary report."""

    # --- Report Structure ---

    def test_should_generate_report_with_all_four_commands(self):
        """Report must include findings for all 4 audited commands."""
        report = generate_audit_report(AUDIT_COMMANDS)
        assert len(report.findings) == 4, (
            f"Expected 4 findings (one per command), got {len(report.findings)}"
        )

    def test_should_include_command_name_in_each_finding(self):
        """Each finding must include the command name."""
        report = generate_audit_report(AUDIT_COMMANDS)
        command_names = {f.command_name for f in report.findings}
        expected_names = set(AUDIT_COMMANDS.keys())
        assert command_names == expected_names, (
            f"Expected command names {expected_names}, got {command_names}"
        )

    def test_should_include_skill_name_in_each_finding(self):
        """Each finding must include the skill invoked."""
        report = generate_audit_report(AUDIT_COMMANDS)
        for finding in report.findings:
            expected_skill = AUDIT_COMMANDS[finding.command_name]
            assert finding.skill_name == expected_skill, (
                f"Finding for {finding.command_name}: expected skill "
                f"'{expected_skill}', got '{finding.skill_name}'"
            )

    def test_should_include_line_number_in_each_finding(self):
        """Each finding must include the line number (None if not found)."""
        report = generate_audit_report(AUDIT_COMMANDS)
        for finding in report.findings:
            # line_number should be an int or None
            assert finding.line_number is None or isinstance(
                finding.line_number, int
            ), (
                f"Finding for {finding.command_name}: line_number should be "
                f"int or None, got {type(finding.line_number)}"
            )

    def test_should_include_compliance_status_in_each_finding(self):
        """Each finding must include compliance status (COMPLIANT/NON-COMPLIANT/NOT FOUND)."""
        valid_statuses = {"COMPLIANT", "NON-COMPLIANT", "NOT FOUND"}
        report = generate_audit_report(AUDIT_COMMANDS)
        for finding in report.findings:
            assert finding.status in valid_statuses, (
                f"Finding for {finding.command_name}: status '{finding.status}' "
                f"not in {valid_statuses}"
            )

    def test_should_include_remediation_flag_in_each_finding(self):
        """Each finding must include a remediation_needed boolean."""
        report = generate_audit_report(AUDIT_COMMANDS)
        for finding in report.findings:
            assert isinstance(finding.remediation_needed, bool), (
                f"Finding for {finding.command_name}: remediation_needed should "
                f"be bool, got {type(finding.remediation_needed)}"
            )

    # --- Report Metadata ---

    def test_should_include_total_commands_audited(self):
        """Report must include total number of commands audited."""
        report = generate_audit_report(AUDIT_COMMANDS)
        assert report.total_audited == 4, (
            f"Expected total_audited=4, got {report.total_audited}"
        )

    def test_should_include_compliant_count(self):
        """Report must include count of compliant commands."""
        report = generate_audit_report(AUDIT_COMMANDS)
        assert isinstance(report.compliant_count, int), (
            f"Expected compliant_count to be int, got {type(report.compliant_count)}"
        )
        assert 0 <= report.compliant_count <= report.total_audited, (
            f"compliant_count ({report.compliant_count}) out of range "
            f"[0, {report.total_audited}]"
        )

    def test_should_include_non_compliant_count(self):
        """Report must include count of non-compliant commands."""
        report = generate_audit_report(AUDIT_COMMANDS)
        assert isinstance(report.non_compliant_count, int), (
            f"Expected non_compliant_count to be int, got "
            f"{type(report.non_compliant_count)}"
        )

    def test_should_have_consistent_counts(self):
        """compliant + non_compliant + not_found should equal total_audited."""
        report = generate_audit_report(AUDIT_COMMANDS)
        total = (
            report.compliant_count
            + report.non_compliant_count
            + report.not_found_count
        )
        assert total == report.total_audited, (
            f"Count mismatch: {report.compliant_count} compliant + "
            f"{report.non_compliant_count} non-compliant + "
            f"{report.not_found_count} not-found = {total}, "
            f"but total_audited = {report.total_audited}"
        )

    # --- Report as Dict ---

    def test_should_convert_to_dict(self):
        """Report must be convertible to a dictionary for structured output."""
        report = generate_audit_report(AUDIT_COMMANDS)
        report_dict = report.to_dict()
        assert isinstance(report_dict, dict), (
            f"Expected dict, got {type(report_dict)}"
        )

    def test_should_include_findings_list_in_dict(self):
        """Dict representation must include 'findings' list."""
        report = generate_audit_report(AUDIT_COMMANDS)
        report_dict = report.to_dict()
        assert "findings" in report_dict, "Missing 'findings' key in report dict"
        assert isinstance(report_dict["findings"], list), (
            f"Expected list, got {type(report_dict['findings'])}"
        )
        assert len(report_dict["findings"]) == 4

    def test_should_include_summary_in_dict(self):
        """Dict representation must include 'summary' section."""
        report = generate_audit_report(AUDIT_COMMANDS)
        report_dict = report.to_dict()
        assert "summary" in report_dict, "Missing 'summary' key in report dict"
        summary = report_dict["summary"]
        assert "total_audited" in summary
        assert "compliant_count" in summary
        assert "non_compliant_count" in summary

    # --- Edge Cases ---

    def test_should_handle_empty_command_map(self):
        """Empty command map should produce report with zero findings."""
        report = generate_audit_report({})
        assert report.total_audited == 0
        assert len(report.findings) == 0

    def test_should_handle_single_command(self):
        """Single-command map should produce report with one finding."""
        single = {"ideate": "devforgeai-ideation"}
        report = generate_audit_report(single)
        assert report.total_audited == 1
        assert len(report.findings) == 1

    def test_should_handle_nonexistent_commands_in_map(self):
        """Commands that don't exist should appear as NOT FOUND in report."""
        commands_with_fake = {
            "ideate": "devforgeai-ideation",
            "fake-command": "devforgeai-fake",
        }
        report = generate_audit_report(commands_with_fake)
        fake_finding = next(
            (f for f in report.findings if f.command_name == "fake-command"),
            None,
        )
        assert fake_finding is not None, "Expected finding for fake-command"
        assert fake_finding.file_found is False
        assert fake_finding.status == "NOT FOUND"


class TestAC5AuditReportWithContentOverrides:
    """Test audit report generation with content overrides for controlled testing."""

    def test_should_report_mixed_compliance_correctly(self):
        """Report with mix of compliant and non-compliant should have correct counts."""
        # Create content overrides: one compliant, one non-compliant
        overrides = {
            "ideate": 'Skill(command="devforgeai-ideation")\nMore content.',
            "brainstorm": "No skill invocation here.",
        }
        report = generate_audit_report(
            {"ideate": "devforgeai-ideation", "brainstorm": "devforgeai-brainstorming"},
            content_overrides=overrides,
        )
        compliant_findings = [f for f in report.findings if f.compliant]
        non_compliant_findings = [f for f in report.findings if not f.compliant]
        assert len(compliant_findings) == 1, (
            f"Expected 1 compliant, got {len(compliant_findings)}"
        )
        assert len(non_compliant_findings) == 1, (
            f"Expected 1 non-compliant, got {len(non_compliant_findings)}"
        )

    def test_should_identify_remediation_needed_for_non_compliant(self):
        """Non-compliant commands should have remediation_needed=True."""
        overrides = {
            "brainstorm": "This file has no Skill() call.",
        }
        report = generate_audit_report(
            {"brainstorm": "devforgeai-brainstorming"},
            content_overrides=overrides,
        )
        finding = report.findings[0]
        assert finding.remediation_needed is True, (
            "Non-compliant command should have remediation_needed=True"
        )
        assert finding.status == "NON-COMPLIANT"


class TestAC5AuditResultDataClass:
    """Test the AuditResult data class structure."""

    def test_should_have_required_fields(self):
        """AuditResult must have all required fields."""
        result = audit_command("ideate", "devforgeai-ideation")
        required_attrs = [
            "command_name",
            "skill_name",
            "file_found",
            "line_number",
            "compliant",
            "status",
            "remediation_needed",
            "matched_text",
            "invocation_count",
        ]
        for attr in required_attrs:
            assert hasattr(result, attr), (
                f"AuditResult missing required attribute: {attr}"
            )

    def test_should_have_to_dict_method(self):
        """AuditResult must have a to_dict() method for serialization."""
        result = audit_command("ideate", "devforgeai-ideation")
        result_dict = result.to_dict()
        assert isinstance(result_dict, dict)
        assert "command_name" in result_dict
        assert "compliant" in result_dict

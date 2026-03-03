"""
Test: AC#8 - JSON Output Format with Summary
Story: STORY-403
Generated: 2026-02-14

Validates that the output includes a findings array with required fields
and a summary object with aggregate statistics.

These tests MUST FAIL initially (TDD Red phase).
"""
import re
import pytest


class TestJsonOutputFormat:
    """Verify JSON output structure for dead code findings."""

    # === Findings Array Fields ===

    def test_should_include_findings_array_in_output(
        self, subagent_content
    ):
        """AC#8: Output must include a findings array."""
        content = subagent_content
        assert re.search(
            r"(?i)findings", content
        ), "findings array not documented in output format"

    def test_should_include_smell_type_field_in_findings(
        self, subagent_content
    ):
        """AC#8: Each finding must have smell_type field."""
        content = subagent_content
        assert re.search(
            r"(?i)smell_type", content
        ), "smell_type field not documented in findings"

    def test_should_include_severity_field_in_findings(
        self, subagent_content
    ):
        """AC#8: Each finding must have severity field."""
        content = subagent_content
        assert re.search(
            r"(?i)severity", content
        ), "severity field not documented in findings"

    def test_should_include_function_name_field_in_findings(
        self, subagent_content
    ):
        """AC#8: Each finding must have function_name field."""
        content = subagent_content
        assert re.search(
            r"(?i)function_name", content
        ), "function_name field not documented in findings"

    def test_should_include_file_field_in_findings(
        self, subagent_content
    ):
        """AC#8: Each finding must have file field."""
        content = subagent_content
        # file is a common word, look specifically in output/findings context
        assert re.search(
            r'(?i)"file"', content
        ), "file field not documented in findings"

    def test_should_include_line_field_in_findings(
        self, subagent_content
    ):
        """AC#8: Each finding must have line field."""
        content = subagent_content
        assert re.search(
            r'(?i)"line"', content
        ), "line field not documented in findings"

    def test_should_include_callers_count_field_in_findings(
        self, subagent_content
    ):
        """AC#8: Each finding must have callers_count field."""
        content = subagent_content
        assert re.search(
            r"(?i)callers_count", content
        ), "callers_count field not documented in findings"

    def test_should_include_is_entry_point_field_in_findings(
        self, subagent_content
    ):
        """AC#8: Each finding must have is_entry_point field."""
        content = subagent_content
        assert re.search(
            r"(?i)is_entry_point", content
        ), "is_entry_point field not documented in findings"

    def test_should_include_exclusion_reason_field_in_findings(
        self, subagent_content
    ):
        """AC#8: Each finding must have exclusion_reason field."""
        content = subagent_content
        assert re.search(
            r"(?i)exclusion_reason", content
        ), "exclusion_reason field not documented in findings"

    def test_should_include_confidence_field_in_findings(
        self, subagent_content
    ):
        """AC#8: Each finding must have confidence field."""
        content = subagent_content
        assert re.search(
            r"(?i)confidence", content
        ), "confidence field not documented in findings"

    def test_should_include_evidence_field_in_findings(
        self, subagent_content
    ):
        """AC#8: Each finding must have evidence field."""
        content = subagent_content
        assert re.search(
            r"(?i)evidence", content
        ), "evidence field not documented in findings"

    def test_should_include_remediation_field_in_findings(
        self, subagent_content
    ):
        """AC#8: Each finding must have remediation field."""
        content = subagent_content
        assert re.search(
            r"(?i)remediation", content
        ), "remediation field not documented in findings"

    # === Summary Object Fields ===

    def test_should_include_summary_object_in_output(
        self, subagent_content
    ):
        """AC#8: Output must include a summary object."""
        content = subagent_content
        assert re.search(
            r"(?i)summary", content
        ), "summary object not documented in output format"

    def test_should_include_total_functions_in_summary(
        self, subagent_content
    ):
        """AC#8: Summary must have total_functions count."""
        content = subagent_content
        assert re.search(
            r"(?i)total_functions", content
        ), "total_functions not documented in summary"

    def test_should_include_zero_caller_functions_in_summary(
        self, subagent_content
    ):
        """AC#8: Summary must have zero_caller_functions count."""
        content = subagent_content
        assert re.search(
            r"(?i)zero_caller_functions", content
        ), "zero_caller_functions not documented in summary"

    def test_should_include_excluded_entry_points_in_summary(
        self, subagent_content
    ):
        """AC#8: Summary must have excluded_entry_points count."""
        content = subagent_content
        assert re.search(
            r"(?i)excluded_entry_points", content
        ), "excluded_entry_points not documented in summary"

    def test_should_include_reported_dead_code_in_summary(
        self, subagent_content
    ):
        """AC#8: Summary must have reported_dead_code count."""
        content = subagent_content
        assert re.search(
            r"(?i)reported_dead_code", content
        ), "reported_dead_code not documented in summary"

    def test_should_include_suppressed_low_confidence_in_summary(
        self, subagent_content
    ):
        """AC#8: Summary must have suppressed_low_confidence count."""
        content = subagent_content
        assert re.search(
            r"(?i)suppressed_low_confidence", content
        ), "suppressed_low_confidence not documented in summary"

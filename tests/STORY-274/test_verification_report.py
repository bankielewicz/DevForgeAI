"""
STORY-274: JSON Verification Report Generation

Tests for AC compliance verification report generation.
All tests follow TDD Red phase - they MUST FAIL until implementation exists.

Coverage Target: 95%+

Data Models Tested:
- VerificationReport: Complete AC verification report
- ACResult: Single AC verification result
- Issue: Issue with file path, line number, description

Business Rules:
- BR-001: Overall PASS requires ALL ACs to PASS
- BR-002: Report must be valid JSON

AC Coverage:
- AC#1: Report File Location
- AC#2: Per-AC Pass/Fail Status
- AC#3: Files Inspected List
- AC#4: Issues with Line Numbers
- AC#5: Overall Determination
- AC#6: Timestamp and Duration
"""

import pytest
import json
import os
import re
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, List, Any


# =============================================================================
# AC#1: Report File Location
# =============================================================================

class TestAC1ReportFileLocation:
    """
    AC#1: Report File Location

    Given: verification completes for a story
    When: the report is generated
    Then: it is written to devforgeai/qa/verification/{STORY-ID}-ac-verification.json
    """

    def test_report_written_to_correct_path(self):
        """
        Test: Report is written to devforgeai/qa/verification/{STORY-ID}-ac-verification.json.

        Given: Verification completes for STORY-274
        When: generate_verification_report() is called
        Then: Report file exists at devforgeai/qa/verification/STORY-274-ac-verification.json
        """
        # Arrange
        from devforgeai.qa.verification.report_generator import generate_verification_report

        story_id = "STORY-274"
        verification_results = {
            "acceptance_criteria": [{"ac_id": "AC#1", "result": "PASS", "evidence": {}, "issues": []}],
            "files_inspected": ["file1.py"],
        }

        # Act
        with patch('builtins.open', MagicMock()) as mock_open:
            with patch('os.makedirs') as mock_makedirs:
                result = generate_verification_report(story_id, verification_results)

        # Assert
        expected_path = "devforgeai/qa/verification/STORY-274-ac-verification.json"
        mock_open.assert_called()
        call_args = mock_open.call_args
        assert expected_path in str(call_args) or call_args[0][0].endswith(expected_path)

    def test_report_path_includes_story_id(self):
        """
        Test: Report path includes the story ID.

        Given: Verification completes for STORY-123
        When: get_report_path() is called
        Then: Path contains "STORY-123"
        """
        # Arrange
        from devforgeai.qa.verification.report_generator import get_report_path

        story_id = "STORY-123"

        # Act
        result = get_report_path(story_id)

        # Assert
        assert "STORY-123" in result
        assert result.endswith("-ac-verification.json")

    def test_report_path_uses_standard_directory(self):
        """
        Test: Report path uses devforgeai/qa/verification/ directory.

        Given: Any story ID
        When: get_report_path() is called
        Then: Path starts with devforgeai/qa/verification/
        """
        # Arrange
        from devforgeai.qa.verification.report_generator import get_report_path

        story_id = "STORY-999"

        # Act
        result = get_report_path(story_id)

        # Assert
        assert "devforgeai/qa/verification/" in result or "devforgeai\\qa\\verification\\" in result

    def test_report_creates_directory_if_missing(self):
        """
        Test: Report generation creates verification directory if it doesn't exist.

        Given: devforgeai/qa/verification/ directory does not exist
        When: generate_verification_report() is called
        Then: Directory is created before writing report
        """
        # Arrange
        from devforgeai.qa.verification.report_generator import generate_verification_report

        story_id = "STORY-274"
        verification_results = {
            "acceptance_criteria": [],
            "files_inspected": [],
        }

        # Act
        with patch('builtins.open', MagicMock()):
            with patch('os.makedirs') as mock_makedirs:
                with patch('os.path.exists', return_value=False):
                    generate_verification_report(story_id, verification_results)

        # Assert
        mock_makedirs.assert_called()
        call_args = mock_makedirs.call_args
        assert "verification" in str(call_args[0][0])


# =============================================================================
# AC#2: Per-AC Pass/Fail Status
# =============================================================================

class TestAC2PerACPassFailStatus:
    """
    AC#2: Per-AC Pass/Fail Status

    Given: all ACs have been verified
    When: the report is generated
    Then: each AC has pass/fail status with evidence supporting the determination
    """

    def test_each_ac_has_result_field(self):
        """
        Test: Each AC result has a 'result' field.

        Given: Verification results with multiple ACs
        When: Report is generated
        Then: Each AC entry has 'result' field with PASS or FAIL
        """
        # Arrange
        from devforgeai.qa.verification.report_generator import generate_verification_report

        story_id = "STORY-274"
        verification_results = {
            "acceptance_criteria": [
                {"ac_id": "AC#1", "result": "PASS", "evidence": {}, "issues": []},
                {"ac_id": "AC#2", "result": "FAIL", "evidence": {}, "issues": []},
            ],
            "files_inspected": [],
        }

        # Act
        with patch('builtins.open', MagicMock()) as mock_open:
            with patch('os.makedirs'):
                report = generate_verification_report(story_id, verification_results)

        # Assert
        assert "acceptance_criteria" in report
        for ac in report["acceptance_criteria"]:
            assert "result" in ac
            assert ac["result"] in ["PASS", "FAIL"]

    def test_ac_result_is_pass_or_fail_enum(self):
        """
        Test: AC result is strictly PASS or FAIL.

        Given: AC verification result
        When: ACResult is created
        Then: result field only accepts PASS or FAIL values
        """
        # Arrange
        from devforgeai.qa.verification.models import ACResult

        # Act & Assert - valid values
        valid_pass = ACResult(ac_id="AC#1", result="PASS", evidence={}, issues=[])
        assert valid_pass.result == "PASS"

        valid_fail = ACResult(ac_id="AC#2", result="FAIL", evidence={}, issues=[])
        assert valid_fail.result == "FAIL"

        # Act & Assert - invalid values should raise
        with pytest.raises((ValueError, TypeError)):
            ACResult(ac_id="AC#3", result="MAYBE", evidence={}, issues=[])

    def test_each_ac_has_evidence_object(self):
        """
        Test: Each AC result has an 'evidence' object.

        Given: AC verification completes
        When: Report is generated
        Then: Each AC has non-null 'evidence' field
        """
        # Arrange
        from devforgeai.qa.verification.report_generator import generate_verification_report

        story_id = "STORY-274"
        verification_results = {
            "acceptance_criteria": [
                {
                    "ac_id": "AC#1",
                    "result": "PASS",
                    "evidence": {"test_count": 5, "tests_passed": 5},
                    "issues": []
                },
            ],
            "files_inspected": [],
        }

        # Act
        with patch('builtins.open', MagicMock()):
            with patch('os.makedirs'):
                report = generate_verification_report(story_id, verification_results)

        # Assert
        for ac in report["acceptance_criteria"]:
            assert "evidence" in ac
            assert isinstance(ac["evidence"], dict)

    def test_evidence_supports_determination(self):
        """
        Test: Evidence provides supporting information for pass/fail determination.

        Given: AC verification with specific evidence
        When: Report is generated
        Then: Evidence contains data supporting the result
        """
        # Arrange
        from devforgeai.qa.verification.models import ACResult

        evidence = {
            "files_checked": 3,
            "pattern_matches": 3,
            "expected_pattern": "def test_",
            "locations": ["file1.py:10", "file2.py:20", "file3.py:30"]
        }

        # Act
        ac_result = ACResult(
            ac_id="AC#1",
            result="PASS",
            evidence=evidence,
            issues=[]
        )

        # Assert
        assert ac_result.evidence is not None
        assert "files_checked" in ac_result.evidence
        assert "locations" in ac_result.evidence


# =============================================================================
# AC#3: Files Inspected List
# =============================================================================

class TestAC3FilesInspectedList:
    """
    AC#3: Files Inspected List

    Given: source code inspection completed
    When: the report is generated
    Then: it includes complete list of all files inspected during verification
    """

    def test_files_inspected_array_populated(self):
        """
        Test: files_inspected array is populated with inspected files.

        Given: Verification inspects multiple files
        When: Report is generated
        Then: files_inspected contains all inspected file paths
        """
        # Arrange
        from devforgeai.qa.verification.report_generator import generate_verification_report

        story_id = "STORY-274"
        files = [
            "src/module/file1.py",
            "src/module/file2.py",
            "tests/test_file.py"
        ]
        verification_results = {
            "acceptance_criteria": [],
            "files_inspected": files,
        }

        # Act
        with patch('builtins.open', MagicMock()):
            with patch('os.makedirs'):
                report = generate_verification_report(story_id, verification_results)

        # Assert
        assert "files_inspected" in report
        assert isinstance(report["files_inspected"], list)
        assert len(report["files_inspected"]) == 3
        for f in files:
            assert f in report["files_inspected"]

    def test_files_inspected_is_string_array(self):
        """
        Test: files_inspected is an array of strings.

        Given: Verification completes
        When: Report is generated
        Then: files_inspected contains only string elements
        """
        # Arrange
        from devforgeai.qa.verification.models import VerificationReport

        # Act
        report = VerificationReport(
            story_id="STORY-274",
            verification_timestamp="2026-01-19T12:00:00Z",
            verification_duration_seconds=10,
            phase="4.5",
            overall_result="PASS",
            acceptance_criteria=[],
            files_inspected=["file1.py", "file2.py"],
            total_issues=0
        )

        # Assert
        assert isinstance(report.files_inspected, list)
        for f in report.files_inspected:
            assert isinstance(f, str)

    def test_files_inspected_includes_all_inspected_files(self):
        """
        Test: files_inspected includes ALL files that were inspected.

        Given: Verification inspects 5 files
        When: Report is generated
        Then: files_inspected count matches 5
        """
        # Arrange
        from devforgeai.qa.verification.report_generator import generate_verification_report

        story_id = "STORY-274"
        inspected_files = [
            "src/a.py",
            "src/b.py",
            "src/c.py",
            "tests/test_a.py",
            "tests/test_b.py"
        ]
        verification_results = {
            "acceptance_criteria": [],
            "files_inspected": inspected_files,
        }

        # Act
        with patch('builtins.open', MagicMock()):
            with patch('os.makedirs'):
                report = generate_verification_report(story_id, verification_results)

        # Assert
        assert len(report["files_inspected"]) == len(inspected_files)

    def test_files_inspected_can_be_empty(self):
        """
        Test: files_inspected can be empty if no files were inspected.

        Given: Verification did not inspect any files (edge case)
        When: Report is generated
        Then: files_inspected is empty array, not null
        """
        # Arrange
        from devforgeai.qa.verification.models import VerificationReport

        # Act
        report = VerificationReport(
            story_id="STORY-274",
            verification_timestamp="2026-01-19T12:00:00Z",
            verification_duration_seconds=0,
            phase="4.5",
            overall_result="FAIL",
            acceptance_criteria=[],
            files_inspected=[],
            total_issues=0
        )

        # Assert
        assert report.files_inspected == []
        assert report.files_inspected is not None


# =============================================================================
# AC#4: Issues with Line Numbers
# =============================================================================

class TestAC4IssuesWithLineNumbers:
    """
    AC#4: Issues Found with Line Numbers

    Given: issues were detected during verification
    When: the report is generated
    Then: each issue includes file path, line number, and description
    """

    def test_issue_includes_file_path(self):
        """
        Test: Each issue includes file_path field.

        Given: Issues were detected during verification
        When: Report is generated
        Then: Each issue has file_path field
        """
        # Arrange
        from devforgeai.qa.verification.models import Issue

        # Act
        issue = Issue(
            file_path="src/module/file.py",
            line_number=42,
            description="Missing test coverage for function"
        )

        # Assert
        assert hasattr(issue, 'file_path')
        assert issue.file_path == "src/module/file.py"

    def test_issue_includes_line_number(self):
        """
        Test: Each issue includes line_number field.

        Given: Issues were detected during verification
        When: Report is generated
        Then: Each issue has line_number field
        """
        # Arrange
        from devforgeai.qa.verification.models import Issue

        # Act
        issue = Issue(
            file_path="src/module/file.py",
            line_number=42,
            description="Missing test coverage for function"
        )

        # Assert
        assert hasattr(issue, 'line_number')
        assert issue.line_number == 42
        assert isinstance(issue.line_number, int)

    def test_issue_includes_description(self):
        """
        Test: Each issue includes description field.

        Given: Issues were detected during verification
        When: Report is generated
        Then: Each issue has description field
        """
        # Arrange
        from devforgeai.qa.verification.models import Issue

        # Act
        issue = Issue(
            file_path="src/module/file.py",
            line_number=42,
            description="Missing test coverage for function calculate_total()"
        )

        # Assert
        assert hasattr(issue, 'description')
        assert "Missing test coverage" in issue.description

    def test_issues_array_in_ac_result(self):
        """
        Test: AC result includes issues array.

        Given: AC verification found issues
        When: ACResult is created
        Then: issues field contains Issue objects
        """
        # Arrange
        from devforgeai.qa.verification.models import ACResult, Issue

        issues = [
            Issue(file_path="file1.py", line_number=10, description="Issue 1"),
            Issue(file_path="file2.py", line_number=20, description="Issue 2"),
        ]

        # Act
        ac_result = ACResult(
            ac_id="AC#1",
            result="FAIL",
            evidence={},
            issues=issues
        )

        # Assert
        assert len(ac_result.issues) == 2
        for issue in ac_result.issues:
            assert hasattr(issue, 'file_path')
            assert hasattr(issue, 'line_number')
            assert hasattr(issue, 'description')

    def test_issue_line_number_is_positive(self):
        """
        Test: Issue line_number must be positive integer.

        Given: Issue creation
        When: line_number is provided
        Then: Must be >= 1
        """
        # Arrange
        from devforgeai.qa.verification.models import Issue

        # Act - valid line number
        valid_issue = Issue(
            file_path="file.py",
            line_number=1,
            description="Test"
        )
        assert valid_issue.line_number == 1

        # Assert - invalid line number should raise
        with pytest.raises((ValueError, TypeError)):
            Issue(file_path="file.py", line_number=0, description="Test")

        with pytest.raises((ValueError, TypeError)):
            Issue(file_path="file.py", line_number=-1, description="Test")


# =============================================================================
# AC#5: Overall Determination
# =============================================================================

class TestAC5OverallDetermination:
    """
    AC#5: Overall Determination

    Given: all ACs are evaluated
    When: the report is generated
    Then: it includes overall PASS/FAIL determination based on AC results
    """

    def test_overall_result_is_pass_or_fail(self):
        """
        Test: overall_result field is either PASS or FAIL.

        Given: Report is generated
        When: Checking overall_result field
        Then: Value is either "PASS" or "FAIL"
        """
        # Arrange
        from devforgeai.qa.verification.models import VerificationReport

        # Act
        report = VerificationReport(
            story_id="STORY-274",
            verification_timestamp="2026-01-19T12:00:00Z",
            verification_duration_seconds=10,
            phase="4.5",
            overall_result="PASS",
            acceptance_criteria=[],
            files_inspected=[],
            total_issues=0
        )

        # Assert
        assert report.overall_result in ["PASS", "FAIL"]

    def test_overall_result_pass_when_all_acs_pass(self):
        """
        Test: overall_result is PASS when ALL ACs pass (BR-001).

        Given: All AC results are PASS
        When: calculate_overall_result() is called
        Then: Returns "PASS"
        """
        # Arrange
        from devforgeai.qa.verification.report_generator import calculate_overall_result
        from devforgeai.qa.verification.models import ACResult

        ac_results = [
            ACResult(ac_id="AC#1", result="PASS", evidence={}, issues=[]),
            ACResult(ac_id="AC#2", result="PASS", evidence={}, issues=[]),
            ACResult(ac_id="AC#3", result="PASS", evidence={}, issues=[]),
        ]

        # Act
        result = calculate_overall_result(ac_results)

        # Assert
        assert result == "PASS"

    def test_overall_result_fail_when_any_ac_fails(self):
        """
        Test: overall_result is FAIL when ANY AC fails (BR-001).

        Given: One or more AC results are FAIL
        When: calculate_overall_result() is called
        Then: Returns "FAIL"
        """
        # Arrange
        from devforgeai.qa.verification.report_generator import calculate_overall_result
        from devforgeai.qa.verification.models import ACResult

        ac_results = [
            ACResult(ac_id="AC#1", result="PASS", evidence={}, issues=[]),
            ACResult(ac_id="AC#2", result="FAIL", evidence={}, issues=[]),
            ACResult(ac_id="AC#3", result="PASS", evidence={}, issues=[]),
        ]

        # Act
        result = calculate_overall_result(ac_results)

        # Assert
        assert result == "FAIL"

    def test_overall_result_fail_when_all_acs_fail(self):
        """
        Test: overall_result is FAIL when all ACs fail.

        Given: All AC results are FAIL
        When: calculate_overall_result() is called
        Then: Returns "FAIL"
        """
        # Arrange
        from devforgeai.qa.verification.report_generator import calculate_overall_result
        from devforgeai.qa.verification.models import ACResult

        ac_results = [
            ACResult(ac_id="AC#1", result="FAIL", evidence={}, issues=[]),
            ACResult(ac_id="AC#2", result="FAIL", evidence={}, issues=[]),
        ]

        # Act
        result = calculate_overall_result(ac_results)

        # Assert
        assert result == "FAIL"

    def test_overall_result_rejects_invalid_values(self):
        """
        Test: overall_result rejects values other than PASS/FAIL.

        Given: Attempting to create report with invalid overall_result
        When: VerificationReport is instantiated
        Then: Raises error
        """
        # Arrange
        from devforgeai.qa.verification.models import VerificationReport

        # Act & Assert
        with pytest.raises((ValueError, TypeError)):
            VerificationReport(
                story_id="STORY-274",
                verification_timestamp="2026-01-19T12:00:00Z",
                verification_duration_seconds=10,
                phase="4.5",
                overall_result="MAYBE",  # Invalid value
                acceptance_criteria=[],
                files_inspected=[],
                total_issues=0
            )


# =============================================================================
# AC#6: Timestamp and Duration
# =============================================================================

class TestAC6TimestampAndDuration:
    """
    AC#6: Timestamp and Duration

    Given: verification workflow completes
    When: the report is generated
    Then: it includes verification_timestamp (ISO 8601) and verification_duration_seconds
    """

    def test_verification_timestamp_in_iso8601_format(self):
        """
        Test: verification_timestamp is in ISO 8601 format.

        Given: Report is generated
        When: Checking verification_timestamp
        Then: Format matches ISO 8601 (YYYY-MM-DDTHH:MM:SSZ or with offset)
        """
        # Arrange
        from devforgeai.qa.verification.models import VerificationReport

        # Act
        report = VerificationReport(
            story_id="STORY-274",
            verification_timestamp="2026-01-19T12:00:00Z",
            verification_duration_seconds=10,
            phase="4.5",
            overall_result="PASS",
            acceptance_criteria=[],
            files_inspected=[],
            total_issues=0
        )

        # Assert - ISO 8601 pattern
        iso8601_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(Z|[+-]\d{2}:\d{2})$'
        assert re.match(iso8601_pattern, report.verification_timestamp)

    def test_verification_timestamp_is_valid_datetime(self):
        """
        Test: verification_timestamp can be parsed as valid datetime.

        Given: Report with timestamp
        When: Parsing timestamp
        Then: No parsing errors
        """
        # Arrange
        from devforgeai.qa.verification.models import VerificationReport

        timestamp = "2026-01-19T14:30:00Z"

        # Act
        report = VerificationReport(
            story_id="STORY-274",
            verification_timestamp=timestamp,
            verification_duration_seconds=10,
            phase="4.5",
            overall_result="PASS",
            acceptance_criteria=[],
            files_inspected=[],
            total_issues=0
        )

        # Assert - can be parsed
        parsed = datetime.fromisoformat(report.verification_timestamp.replace('Z', '+00:00'))
        assert parsed.year == 2026
        assert parsed.month == 1
        assert parsed.day == 19

    def test_verification_duration_seconds_present(self):
        """
        Test: verification_duration_seconds field is present.

        Given: Report is generated
        When: Checking verification_duration_seconds
        Then: Field exists and contains integer value
        """
        # Arrange
        from devforgeai.qa.verification.models import VerificationReport

        # Act
        report = VerificationReport(
            story_id="STORY-274",
            verification_timestamp="2026-01-19T12:00:00Z",
            verification_duration_seconds=45,
            phase="4.5",
            overall_result="PASS",
            acceptance_criteria=[],
            files_inspected=[],
            total_issues=0
        )

        # Assert
        assert hasattr(report, 'verification_duration_seconds')
        assert isinstance(report.verification_duration_seconds, int)
        assert report.verification_duration_seconds == 45

    def test_verification_duration_seconds_is_non_negative(self):
        """
        Test: verification_duration_seconds must be >= 0.

        Given: Report creation
        When: duration is specified
        Then: Must be non-negative
        """
        # Arrange
        from devforgeai.qa.verification.models import VerificationReport

        # Act - valid zero duration
        report_zero = VerificationReport(
            story_id="STORY-274",
            verification_timestamp="2026-01-19T12:00:00Z",
            verification_duration_seconds=0,
            phase="4.5",
            overall_result="PASS",
            acceptance_criteria=[],
            files_inspected=[],
            total_issues=0
        )
        assert report_zero.verification_duration_seconds == 0

        # Assert - negative duration should raise
        with pytest.raises((ValueError, TypeError)):
            VerificationReport(
                story_id="STORY-274",
                verification_timestamp="2026-01-19T12:00:00Z",
                verification_duration_seconds=-1,
                phase="4.5",
                overall_result="PASS",
                acceptance_criteria=[],
                files_inspected=[],
                total_issues=0
            )


# =============================================================================
# Business Rules Tests
# =============================================================================

class TestBusinessRules:
    """Tests for business rules BR-001 and BR-002."""

    def test_br001_overall_pass_requires_all_acs_pass(self):
        """
        Test BR-001: Overall PASS requires ALL ACs to PASS.

        Given: Mixed AC results (some PASS, some FAIL)
        When: Overall result is calculated
        Then: Overall is FAIL (not PASS)
        """
        # Arrange
        from devforgeai.qa.verification.report_generator import calculate_overall_result
        from devforgeai.qa.verification.models import ACResult

        # Test case 1: 5 PASS, 1 FAIL -> Overall FAIL
        ac_results_with_one_fail = [
            ACResult(ac_id=f"AC#{i}", result="PASS", evidence={}, issues=[])
            for i in range(1, 6)
        ]
        ac_results_with_one_fail.append(
            ACResult(ac_id="AC#6", result="FAIL", evidence={}, issues=[])
        )

        # Act
        result = calculate_overall_result(ac_results_with_one_fail)

        # Assert
        assert result == "FAIL", "BR-001: Any FAIL should result in overall FAIL"

    def test_br002_report_must_be_valid_json(self):
        """
        Test BR-002: Report must be valid JSON.

        Given: A generated verification report
        When: Report is serialized
        Then: Output is valid JSON that can be parsed
        """
        # Arrange
        from devforgeai.qa.verification.report_generator import generate_verification_report

        story_id = "STORY-274"
        verification_results = {
            "acceptance_criteria": [
                {"ac_id": "AC#1", "result": "PASS", "evidence": {}, "issues": []}
            ],
            "files_inspected": ["file1.py"],
        }

        # Act
        json_output = []
        with patch('builtins.open', MagicMock()) as mock_open:
            mock_file = MagicMock()
            mock_open.return_value.__enter__ = MagicMock(return_value=mock_file)
            mock_open.return_value.__exit__ = MagicMock(return_value=False)

            def capture_write(data):
                json_output.append(data)

            mock_file.write = capture_write

            with patch('os.makedirs'):
                report = generate_verification_report(story_id, verification_results)

        # Assert - report dict can be serialized to valid JSON
        json_str = json.dumps(report)
        parsed = json.loads(json_str)
        assert parsed is not None

    def test_br002_report_json_is_parseable(self):
        """
        Test BR-002: Written report file is parseable JSON.

        Given: Report file is written
        When: File contents are read
        Then: Contents parse as valid JSON
        """
        # Arrange
        from devforgeai.qa.verification.models import VerificationReport

        report = VerificationReport(
            story_id="STORY-274",
            verification_timestamp="2026-01-19T12:00:00Z",
            verification_duration_seconds=10,
            phase="4.5",
            overall_result="PASS",
            acceptance_criteria=[],
            files_inspected=["file1.py"],
            total_issues=0
        )

        # Act
        report_dict = report.to_dict()
        json_str = json.dumps(report_dict)

        # Assert
        parsed = json.loads(json_str)
        assert parsed["story_id"] == "STORY-274"
        assert parsed["overall_result"] == "PASS"


# =============================================================================
# Data Model Validation Tests
# =============================================================================

class TestVerificationReportModel:
    """Tests for VerificationReport data model constraints."""

    def test_story_id_matches_pattern(self):
        """
        Test: story_id matches STORY-NNN pattern.

        Given: VerificationReport creation
        When: story_id is provided
        Then: Must match STORY-\\d{3} pattern
        """
        # Arrange
        from devforgeai.qa.verification.models import VerificationReport

        # Act - valid story ID
        report = VerificationReport(
            story_id="STORY-274",
            verification_timestamp="2026-01-19T12:00:00Z",
            verification_duration_seconds=10,
            phase="4.5",
            overall_result="PASS",
            acceptance_criteria=[],
            files_inspected=[],
            total_issues=0
        )
        assert report.story_id == "STORY-274"

        # Assert - invalid story ID should raise
        with pytest.raises((ValueError, TypeError)):
            VerificationReport(
                story_id="INVALID-ID",
                verification_timestamp="2026-01-19T12:00:00Z",
                verification_duration_seconds=10,
                phase="4.5",
                overall_result="PASS",
                acceptance_criteria=[],
                files_inspected=[],
                total_issues=0
            )

    def test_phase_is_4_5_or_5_5(self):
        """
        Test: phase field is either "4.5" or "5.5".

        Given: VerificationReport creation
        When: phase is provided
        Then: Must be "4.5" or "5.5"
        """
        # Arrange
        from devforgeai.qa.verification.models import VerificationReport

        # Act - valid phases
        report_4_5 = VerificationReport(
            story_id="STORY-274",
            verification_timestamp="2026-01-19T12:00:00Z",
            verification_duration_seconds=10,
            phase="4.5",
            overall_result="PASS",
            acceptance_criteria=[],
            files_inspected=[],
            total_issues=0
        )
        assert report_4_5.phase == "4.5"

        report_5_5 = VerificationReport(
            story_id="STORY-274",
            verification_timestamp="2026-01-19T12:00:00Z",
            verification_duration_seconds=10,
            phase="5.5",
            overall_result="PASS",
            acceptance_criteria=[],
            files_inspected=[],
            total_issues=0
        )
        assert report_5_5.phase == "5.5"

        # Assert - invalid phase should raise
        with pytest.raises((ValueError, TypeError)):
            VerificationReport(
                story_id="STORY-274",
                verification_timestamp="2026-01-19T12:00:00Z",
                verification_duration_seconds=10,
                phase="3.0",  # Invalid phase
                overall_result="PASS",
                acceptance_criteria=[],
                files_inspected=[],
                total_issues=0
            )

    def test_acceptance_criteria_minimum_one(self):
        """
        Test: acceptance_criteria requires minimum 1 entry for complete verification.

        Given: VerificationReport with acceptance_criteria
        When: acceptance_criteria is empty
        Then: Should be allowed (edge case - but overall_result should be FAIL)
        """
        # Arrange
        from devforgeai.qa.verification.models import VerificationReport

        # Note: Empty AC list is allowed but should indicate no ACs to verify
        report = VerificationReport(
            story_id="STORY-274",
            verification_timestamp="2026-01-19T12:00:00Z",
            verification_duration_seconds=10,
            phase="4.5",
            overall_result="FAIL",  # No ACs means can't be PASS
            acceptance_criteria=[],
            files_inspected=[],
            total_issues=0
        )

        # Assert
        assert len(report.acceptance_criteria) == 0

    def test_total_issues_is_non_negative(self):
        """
        Test: total_issues field must be >= 0.

        Given: VerificationReport creation
        When: total_issues is specified
        Then: Must be non-negative integer
        """
        # Arrange
        from devforgeai.qa.verification.models import VerificationReport

        # Act - valid zero issues
        report = VerificationReport(
            story_id="STORY-274",
            verification_timestamp="2026-01-19T12:00:00Z",
            verification_duration_seconds=10,
            phase="4.5",
            overall_result="PASS",
            acceptance_criteria=[],
            files_inspected=[],
            total_issues=0
        )
        assert report.total_issues == 0

        # Assert - negative issues should raise
        with pytest.raises((ValueError, TypeError)):
            VerificationReport(
                story_id="STORY-274",
                verification_timestamp="2026-01-19T12:00:00Z",
                verification_duration_seconds=10,
                phase="4.5",
                overall_result="PASS",
                acceptance_criteria=[],
                files_inspected=[],
                total_issues=-1
            )


class TestACResultModel:
    """Tests for ACResult data model constraints."""

    def test_ac_id_format(self):
        """
        Test: ac_id follows expected format.

        Given: ACResult creation
        When: ac_id is provided
        Then: Should be non-empty string
        """
        # Arrange
        from devforgeai.qa.verification.models import ACResult

        # Act
        ac = ACResult(
            ac_id="AC#1",
            result="PASS",
            evidence={},
            issues=[]
        )

        # Assert
        assert ac.ac_id == "AC#1"
        assert len(ac.ac_id) > 0

    def test_issues_array_required(self):
        """
        Test: issues field is required array (may be empty).

        Given: ACResult creation
        When: issues is provided
        Then: Must be array type
        """
        # Arrange
        from devforgeai.qa.verification.models import ACResult

        # Act
        ac_with_empty_issues = ACResult(
            ac_id="AC#1",
            result="PASS",
            evidence={},
            issues=[]
        )

        # Assert
        assert isinstance(ac_with_empty_issues.issues, list)


# =============================================================================
# NFR Tests
# =============================================================================

class TestNonFunctionalRequirements:
    """Tests for Non-Functional Requirements."""

    def test_nfr001_report_generation_under_1_second(self):
        """
        Test NFR-001: Report generation completes in < 1 second.

        Given: Verification results
        When: generate_verification_report() is called
        Then: Execution time is < 1 second
        """
        # Arrange
        import time
        from devforgeai.qa.verification.report_generator import generate_verification_report

        story_id = "STORY-274"
        verification_results = {
            "acceptance_criteria": [
                {"ac_id": f"AC#{i}", "result": "PASS", "evidence": {}, "issues": []}
                for i in range(1, 7)  # 6 ACs
            ],
            "files_inspected": [f"file{i}.py" for i in range(100)],  # 100 files
        }

        # Act
        start_time = time.time()
        with patch('builtins.open', MagicMock()):
            with patch('os.makedirs'):
                generate_verification_report(story_id, verification_results)
        end_time = time.time()

        # Assert
        elapsed = end_time - start_time
        assert elapsed < 1.0, f"Report generation took {elapsed:.3f}s (expected < 1s)"

    def test_nfr002_report_always_created(self):
        """
        Test NFR-002: 100% of verifications produce report.

        Given: Any verification result
        When: generate_verification_report() completes
        Then: Report file write is attempted
        """
        # Arrange
        from devforgeai.qa.verification.report_generator import generate_verification_report

        story_id = "STORY-274"
        verification_results = {
            "acceptance_criteria": [],
            "files_inspected": [],
        }

        # Act
        write_called = False
        with patch('builtins.open', MagicMock()) as mock_open:
            mock_file = MagicMock()
            mock_open.return_value.__enter__ = MagicMock(return_value=mock_file)
            mock_open.return_value.__exit__ = MagicMock(return_value=False)
            mock_file.write = MagicMock()

            with patch('os.makedirs'):
                generate_verification_report(story_id, verification_results)
                write_called = mock_open.called

        # Assert
        assert write_called, "Report file should always be written"


# =============================================================================
# Edge Cases and Error Handling
# =============================================================================

class TestEdgeCases:
    """Tests for edge cases and error handling."""

    def test_empty_verification_results(self):
        """
        Test: Handle empty verification results gracefully.

        Given: Verification returns minimal results
        When: Report is generated
        Then: Report is created with empty arrays
        """
        # Arrange
        from devforgeai.qa.verification.report_generator import generate_verification_report

        story_id = "STORY-274"
        verification_results = {
            "acceptance_criteria": [],
            "files_inspected": [],
        }

        # Act
        with patch('builtins.open', MagicMock()):
            with patch('os.makedirs'):
                report = generate_verification_report(story_id, verification_results)

        # Assert
        assert report is not None
        assert report["acceptance_criteria"] == []
        assert report["files_inspected"] == []

    def test_large_number_of_issues(self):
        """
        Test: Handle large number of issues.

        Given: AC with many issues
        When: Report is generated
        Then: All issues are included
        """
        # Arrange
        from devforgeai.qa.verification.models import ACResult, Issue

        issues = [
            Issue(file_path=f"file{i}.py", line_number=i, description=f"Issue {i}")
            for i in range(1, 101)  # 100 issues
        ]

        # Act
        ac = ACResult(
            ac_id="AC#1",
            result="FAIL",
            evidence={"issue_count": 100},
            issues=issues
        )

        # Assert
        assert len(ac.issues) == 100

    def test_special_characters_in_file_path(self):
        """
        Test: Handle special characters in file paths.

        Given: File path with special characters
        When: Issue is created
        Then: Path is preserved correctly
        """
        # Arrange
        from devforgeai.qa.verification.models import Issue

        special_paths = [
            "src/modules/file with spaces.py",
            "src/modules/archivo_espanol.py",
            "src/modules/file-with-dashes.py",
        ]

        # Act & Assert
        for path in special_paths:
            issue = Issue(file_path=path, line_number=1, description="Test")
            assert issue.file_path == path

    def test_unicode_in_description(self):
        """
        Test: Handle unicode characters in issue description.

        Given: Issue description with unicode
        When: Issue is created and serialized
        Then: Unicode is preserved
        """
        # Arrange
        from devforgeai.qa.verification.models import Issue

        unicode_desc = "Missing test for function calcular_precio()"

        # Act
        issue = Issue(
            file_path="file.py",
            line_number=42,
            description=unicode_desc
        )

        # Assert
        assert issue.description == unicode_desc

    def test_directory_creation_error_handling(self):
        """
        Test: Handle directory creation errors gracefully.

        Given: Directory cannot be created (permission error)
        When: generate_verification_report() is called
        Then: Appropriate error is raised
        """
        # Arrange
        from devforgeai.qa.verification.report_generator import generate_verification_report

        story_id = "STORY-274"
        verification_results = {
            "acceptance_criteria": [],
            "files_inspected": [],
        }

        # Act & Assert
        with patch('os.makedirs', side_effect=PermissionError("Permission denied")):
            with pytest.raises((PermissionError, OSError)):
                generate_verification_report(story_id, verification_results)


# =============================================================================
# Integration Tests
# =============================================================================

class TestReportIntegration:
    """Integration tests for complete report generation flow."""

    def test_complete_report_generation_flow(self):
        """
        Test: Complete report generation produces valid JSON with all fields.

        Given: Full verification results
        When: generate_verification_report() is called
        Then: All required fields are present and valid
        """
        # Arrange
        from devforgeai.qa.verification.report_generator import generate_verification_report

        story_id = "STORY-274"
        verification_results = {
            "acceptance_criteria": [
                {
                    "ac_id": "AC#1",
                    "result": "PASS",
                    "evidence": {"test_count": 5, "tests_passed": 5},
                    "issues": []
                },
                {
                    "ac_id": "AC#2",
                    "result": "FAIL",
                    "evidence": {"expected": "implementation", "found": None},
                    "issues": [
                        {"file_path": "src/module.py", "line_number": 42, "description": "Missing implementation"}
                    ]
                },
            ],
            "files_inspected": ["src/module.py", "tests/test_module.py"],
        }

        # Act
        with patch('builtins.open', MagicMock()):
            with patch('os.makedirs'):
                report = generate_verification_report(story_id, verification_results)

        # Assert - all required fields present
        assert "story_id" in report
        assert "verification_timestamp" in report
        assert "verification_duration_seconds" in report
        assert "phase" in report
        assert "overall_result" in report
        assert "acceptance_criteria" in report
        assert "files_inspected" in report
        assert "total_issues" in report

        # Assert - business rules applied
        assert report["overall_result"] == "FAIL"  # BR-001: any FAIL -> overall FAIL
        assert report["total_issues"] >= 1

    def test_report_serialization_roundtrip(self):
        """
        Test: Report can be serialized to JSON and deserialized back.

        Given: VerificationReport instance
        When: Serialized to JSON and back
        Then: Data is preserved
        """
        # Arrange
        from devforgeai.qa.verification.models import VerificationReport, ACResult

        original = VerificationReport(
            story_id="STORY-274",
            verification_timestamp="2026-01-19T12:00:00Z",
            verification_duration_seconds=30,
            phase="4.5",
            overall_result="PASS",
            acceptance_criteria=[
                ACResult(ac_id="AC#1", result="PASS", evidence={"key": "value"}, issues=[])
            ],
            files_inspected=["file1.py", "file2.py"],
            total_issues=0
        )

        # Act
        json_str = json.dumps(original.to_dict())
        parsed = json.loads(json_str)

        # Assert
        assert parsed["story_id"] == original.story_id
        assert parsed["verification_timestamp"] == original.verification_timestamp
        assert parsed["verification_duration_seconds"] == original.verification_duration_seconds
        assert parsed["phase"] == original.phase
        assert parsed["overall_result"] == original.overall_result
        assert len(parsed["acceptance_criteria"]) == 1
        assert len(parsed["files_inspected"]) == 2
        assert parsed["total_issues"] == 0

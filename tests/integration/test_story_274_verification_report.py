"""
STORY-274: Integration Tests for JSON Verification Report Generation

Integration Points Tested:
1. File System Integration - Report creation at correct path
2. Module Import Integration - Package imports work correctly
3. End-to-End Flow - Complete workflow from data to file

Test Coverage Target: 95%+ (Business Logic)
"""

import json
import os
import sys
import tempfile
import shutil
from datetime import datetime, timezone
from pathlib import Path

import pytest

# Ensure project root is in path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from devforgeai.qa.verification import (
    Issue,
    ACResult,
    VerificationReport,
    get_report_path,
    calculate_overall_result,
    generate_verification_report,
)


# =============================================================================
# TEST FIXTURES
# =============================================================================

@pytest.fixture
def temp_dir():
    """Create a temporary directory for test file operations."""
    original_cwd = os.getcwd()
    temp_path = tempfile.mkdtemp()
    os.chdir(temp_path)
    yield temp_path
    os.chdir(original_cwd)
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def sample_issue():
    """Create a sample Issue for testing."""
    return Issue(
        file_path="src/module.py",
        line_number=42,
        description="Missing test coverage"
    )


@pytest.fixture
def sample_ac_result(sample_issue):
    """Create a sample ACResult for testing."""
    return ACResult(
        ac_id="AC#1",
        result="PASS",
        evidence={"tests_found": 5, "coverage": 95.0},
        issues=[]
    )


@pytest.fixture
def sample_ac_result_with_issues(sample_issue):
    """Create a sample ACResult with issues for testing."""
    return ACResult(
        ac_id="AC#2",
        result="FAIL",
        evidence={"tests_found": 2, "coverage": 60.0},
        issues=[sample_issue]
    )


@pytest.fixture
def sample_verification_results(sample_ac_result, sample_ac_result_with_issues):
    """Create sample verification results dict."""
    return {
        "acceptance_criteria": [sample_ac_result, sample_ac_result_with_issues],
        "files_inspected": ["src/module.py", "tests/test_module.py"],
    }


# =============================================================================
# INTEGRATION TEST 1: FILE SYSTEM INTEGRATION
# =============================================================================

class TestFileSystemIntegration:
    """Tests for file system integration - AC#1: Report File Location."""

    def test_report_path_format(self):
        """Verify get_report_path returns correct path format."""
        story_id = "STORY-274"
        path = get_report_path(story_id)

        assert path == "devforgeai/qa/verification/STORY-274-ac-verification.json"
        assert story_id in path
        assert path.endswith(".json")

    def test_report_path_different_story_ids(self):
        """Verify path varies by story ID."""
        path_274 = get_report_path("STORY-274")
        path_100 = get_report_path("STORY-100")

        assert path_274 != path_100
        assert "STORY-274" in path_274
        assert "STORY-100" in path_100

    def test_directory_creation(self, temp_dir):
        """Verify directory is created if missing."""
        story_id = "STORY-274"
        verification_results = {
            "acceptance_criteria": [
                {
                    "ac_id": "AC#1",
                    "result": "PASS",
                    "evidence": {"test": True},
                    "issues": []
                }
            ],
            "files_inspected": []
        }

        # Directory doesn't exist yet
        report_path = get_report_path(story_id)
        report_dir = os.path.dirname(report_path)
        assert not os.path.exists(report_dir)

        # Generate report - should create directory
        generate_verification_report(story_id, verification_results)

        # Directory now exists
        assert os.path.exists(report_dir)
        assert os.path.isdir(report_dir)

    def test_report_file_created(self, temp_dir):
        """Verify report file is actually written to disk."""
        story_id = "STORY-274"
        verification_results = {
            "acceptance_criteria": [{
                "ac_id": "AC#1",
                "result": "PASS",
                "evidence": {"verified": True},
                "issues": []
            }],
            "files_inspected": ["test.py"]
        }

        generate_verification_report(story_id, verification_results)

        report_path = get_report_path(story_id)
        assert os.path.exists(report_path)
        assert os.path.isfile(report_path)

    def test_report_file_readable(self, temp_dir):
        """Verify report file is readable after creation."""
        story_id = "STORY-274"
        verification_results = {
            "acceptance_criteria": [{
                "ac_id": "AC#1",
                "result": "PASS",
                "evidence": {},
                "issues": []
            }],
            "files_inspected": []
        }

        generate_verification_report(story_id, verification_results)
        report_path = get_report_path(story_id)

        # File should be readable
        with open(report_path, 'r', encoding='utf-8') as f:
            content = f.read()

        assert len(content) > 0

    def test_report_valid_json(self, temp_dir):
        """Verify report is valid JSON (BR-002)."""
        story_id = "STORY-274"
        verification_results = {
            "acceptance_criteria": [{
                "ac_id": "AC#1",
                "result": "PASS",
                "evidence": {"key": "value"},
                "issues": []
            }],
            "files_inspected": ["file1.py"]
        }

        generate_verification_report(story_id, verification_results)
        report_path = get_report_path(story_id)

        # Should parse as valid JSON without errors
        with open(report_path, 'r', encoding='utf-8') as f:
            parsed = json.load(f)

        assert isinstance(parsed, dict)


# =============================================================================
# INTEGRATION TEST 2: MODULE IMPORT INTEGRATION
# =============================================================================

class TestModuleImportIntegration:
    """Tests for module import integration."""

    def test_issue_import_from_package(self):
        """Verify Issue can be imported from package root."""
        from devforgeai.qa.verification import Issue

        issue = Issue(file_path="test.py", line_number=1, description="test")
        assert issue.file_path == "test.py"

    def test_acresult_import_from_package(self):
        """Verify ACResult can be imported from package root."""
        from devforgeai.qa.verification import ACResult

        ac = ACResult(ac_id="AC#1", result="PASS", evidence={})
        assert ac.ac_id == "AC#1"

    def test_verification_report_import_from_package(self):
        """Verify VerificationReport can be imported from package root."""
        from devforgeai.qa.verification import VerificationReport

        report = VerificationReport(
            story_id="STORY-274",
            verification_timestamp="2026-01-19T12:00:00Z",
            verification_duration_seconds=5,
            phase="4.5",
            overall_result="PASS",
            acceptance_criteria=[],
            files_inspected=[],
            total_issues=0
        )
        assert report.story_id == "STORY-274"

    def test_get_report_path_import(self):
        """Verify get_report_path function import."""
        from devforgeai.qa.verification import get_report_path

        path = get_report_path("STORY-123")
        assert "STORY-123" in path

    def test_calculate_overall_result_import(self):
        """Verify calculate_overall_result function import."""
        from devforgeai.qa.verification import calculate_overall_result

        result = calculate_overall_result([])
        assert result == "FAIL"  # Empty list fails

    def test_generate_verification_report_import(self):
        """Verify generate_verification_report function import."""
        from devforgeai.qa.verification import generate_verification_report

        assert callable(generate_verification_report)

    def test_all_exports_accessible(self):
        """Verify all __all__ exports are accessible."""
        from devforgeai.qa import verification

        expected_exports = [
            "Issue",
            "ACResult",
            "VerificationReport",
            "get_report_path",
            "calculate_overall_result",
            "generate_verification_report",
        ]

        for export in expected_exports:
            assert hasattr(verification, export), f"Missing export: {export}"


# =============================================================================
# INTEGRATION TEST 3: END-TO-END FLOW
# =============================================================================

class TestEndToEndFlow:
    """Tests for complete end-to-end verification report workflow."""

    def test_e2e_generate_and_read_report(self, temp_dir):
        """Test complete flow: generate report -> read -> verify structure."""
        story_id = "STORY-274"

        # Prepare verification data
        verification_results = {
            "acceptance_criteria": [
                {
                    "ac_id": "AC#1",
                    "result": "PASS",
                    "evidence": {"tests_found": 10, "all_passing": True},
                    "issues": []
                },
                {
                    "ac_id": "AC#2",
                    "result": "PASS",
                    "evidence": {"coverage_percent": 96.5},
                    "issues": []
                }
            ],
            "files_inspected": [
                "src/main.py",
                "src/utils.py",
                "tests/test_main.py"
            ]
        }

        # Generate report
        result = generate_verification_report(story_id, verification_results)

        # Read report from file
        report_path = get_report_path(story_id)
        with open(report_path, 'r', encoding='utf-8') as f:
            read_report = json.load(f)

        # Verify structure matches
        assert read_report == result

        # Verify all AC#1-AC#6 fields present
        assert read_report["story_id"] == "STORY-274"  # AC#1
        assert len(read_report["acceptance_criteria"]) == 2  # AC#2
        assert read_report["files_inspected"] == verification_results["files_inspected"]  # AC#3
        assert read_report["overall_result"] == "PASS"  # AC#5
        assert "verification_timestamp" in read_report  # AC#6
        assert "verification_duration_seconds" in read_report  # AC#6

    def test_e2e_with_issues(self, temp_dir):
        """Test E2E flow with issues detected (AC#4)."""
        story_id = "STORY-274"

        verification_results = {
            "acceptance_criteria": [
                {
                    "ac_id": "AC#1",
                    "result": "FAIL",
                    "evidence": {"reason": "coverage below threshold"},
                    "issues": [
                        {
                            "file_path": "src/module.py",
                            "line_number": 42,
                            "description": "Missing test for function process_data"
                        },
                        {
                            "file_path": "src/helper.py",
                            "line_number": 15,
                            "description": "Untested exception handler"
                        }
                    ]
                }
            ],
            "files_inspected": ["src/module.py", "src/helper.py"]
        }

        # Generate
        generate_verification_report(story_id, verification_results)

        # Read and verify
        report_path = get_report_path(story_id)
        with open(report_path, 'r', encoding='utf-8') as f:
            report = json.load(f)

        # Verify issues structure (AC#4)
        issues = report["acceptance_criteria"][0]["issues"]
        assert len(issues) == 2

        for issue in issues:
            assert "file_path" in issue
            assert "line_number" in issue
            assert "description" in issue
            assert isinstance(issue["line_number"], int)

        # Verify overall result is FAIL (BR-001)
        assert report["overall_result"] == "FAIL"
        assert report["total_issues"] == 2

    def test_e2e_mixed_results(self, temp_dir):
        """Test E2E with mixed PASS/FAIL results."""
        story_id = "STORY-274"

        verification_results = {
            "acceptance_criteria": [
                {
                    "ac_id": "AC#1",
                    "result": "PASS",
                    "evidence": {"verified": True},
                    "issues": []
                },
                {
                    "ac_id": "AC#2",
                    "result": "FAIL",
                    "evidence": {"verified": False, "reason": "missing implementation"},
                    "issues": [{
                        "file_path": "src/feature.py",
                        "line_number": 100,
                        "description": "Required function not found"
                    }]
                },
                {
                    "ac_id": "AC#3",
                    "result": "PASS",
                    "evidence": {"verified": True},
                    "issues": []
                }
            ],
            "files_inspected": ["src/feature.py"]
        }

        generate_verification_report(story_id, verification_results)

        report_path = get_report_path(story_id)
        with open(report_path, 'r', encoding='utf-8') as f:
            report = json.load(f)

        # BR-001: One FAIL means overall FAIL
        assert report["overall_result"] == "FAIL"

        # Verify per-AC status preserved
        results = {ac["ac_id"]: ac["result"] for ac in report["acceptance_criteria"]}
        assert results["AC#1"] == "PASS"
        assert results["AC#2"] == "FAIL"
        assert results["AC#3"] == "PASS"

    def test_e2e_all_pass_results(self, temp_dir):
        """Test E2E with all PASS results."""
        story_id = "STORY-274"

        verification_results = {
            "acceptance_criteria": [
                {"ac_id": "AC#1", "result": "PASS", "evidence": {}, "issues": []},
                {"ac_id": "AC#2", "result": "PASS", "evidence": {}, "issues": []},
                {"ac_id": "AC#3", "result": "PASS", "evidence": {}, "issues": []},
            ],
            "files_inspected": ["src/module.py"]
        }

        generate_verification_report(story_id, verification_results)

        report_path = get_report_path(story_id)
        with open(report_path, 'r', encoding='utf-8') as f:
            report = json.load(f)

        # All PASS means overall PASS
        assert report["overall_result"] == "PASS"
        assert report["total_issues"] == 0

    def test_e2e_timestamp_format(self, temp_dir):
        """Test E2E verifies timestamp is ISO 8601 (AC#6)."""
        story_id = "STORY-274"

        verification_results = {
            "acceptance_criteria": [
                {"ac_id": "AC#1", "result": "PASS", "evidence": {}, "issues": []}
            ],
            "files_inspected": []
        }

        before = datetime.now(timezone.utc)
        generate_verification_report(story_id, verification_results)
        after = datetime.now(timezone.utc)

        report_path = get_report_path(story_id)
        with open(report_path, 'r', encoding='utf-8') as f:
            report = json.load(f)

        # Parse timestamp to verify format
        timestamp_str = report["verification_timestamp"]

        # Should be parseable as ISO 8601
        parsed_time = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%SZ")
        parsed_time = parsed_time.replace(tzinfo=timezone.utc)

        # Should be within our before/after window
        assert parsed_time >= before.replace(microsecond=0)
        # Allow 1 second margin
        assert parsed_time <= after.replace(microsecond=0).replace(second=after.second + 1)

    def test_e2e_duration_calculation(self, temp_dir):
        """Test E2E verifies duration is calculated (AC#6)."""
        story_id = "STORY-274"

        verification_results = {
            "acceptance_criteria": [
                {"ac_id": "AC#1", "result": "PASS", "evidence": {}, "issues": []}
            ],
            "files_inspected": []
        }

        # Provide explicit start_time to test duration
        import time
        start = datetime.now(timezone.utc)
        time.sleep(0.1)  # Small delay to ensure measurable duration

        generate_verification_report(story_id, verification_results, start_time=start)

        report_path = get_report_path(story_id)
        with open(report_path, 'r', encoding='utf-8') as f:
            report = json.load(f)

        # Duration should be present and non-negative
        assert "verification_duration_seconds" in report
        assert isinstance(report["verification_duration_seconds"], int)
        assert report["verification_duration_seconds"] >= 0

    def test_e2e_phase_values(self, temp_dir):
        """Test E2E with different phase values."""
        story_id = "STORY-274"

        verification_results = {
            "acceptance_criteria": [
                {"ac_id": "AC#1", "result": "PASS", "evidence": {}, "issues": []}
            ],
            "files_inspected": []
        }

        # Test phase 4.5
        generate_verification_report(story_id, verification_results, phase="4.5")

        report_path = get_report_path(story_id)
        with open(report_path, 'r', encoding='utf-8') as f:
            report = json.load(f)

        assert report["phase"] == "4.5"

        # Test phase 5.5
        generate_verification_report(story_id, verification_results, phase="5.5")

        with open(report_path, 'r', encoding='utf-8') as f:
            report = json.load(f)

        assert report["phase"] == "5.5"

    def test_e2e_files_inspected_preserved(self, temp_dir):
        """Test E2E verifies all files_inspected are preserved (AC#3)."""
        story_id = "STORY-274"

        files = [
            "src/main.py",
            "src/utils/helper.py",
            "src/models/user.py",
            "tests/test_main.py",
            "tests/test_utils.py"
        ]

        verification_results = {
            "acceptance_criteria": [
                {"ac_id": "AC#1", "result": "PASS", "evidence": {}, "issues": []}
            ],
            "files_inspected": files
        }

        generate_verification_report(story_id, verification_results)

        report_path = get_report_path(story_id)
        with open(report_path, 'r', encoding='utf-8') as f:
            report = json.load(f)

        # All files should be present
        assert report["files_inspected"] == files
        assert len(report["files_inspected"]) == 5


# =============================================================================
# BUSINESS RULE TESTS
# =============================================================================

class TestBusinessRules:
    """Tests for business rules from technical specification."""

    def test_br001_overall_pass_requires_all_pass(self):
        """BR-001: Overall PASS requires ALL ACs to PASS."""
        ac_results = [
            ACResult(ac_id="AC#1", result="PASS", evidence={}),
            ACResult(ac_id="AC#2", result="PASS", evidence={}),
            ACResult(ac_id="AC#3", result="PASS", evidence={}),
        ]

        result = calculate_overall_result(ac_results)
        assert result == "PASS"

    def test_br001_single_fail_causes_overall_fail(self):
        """BR-001: Single FAIL causes overall FAIL."""
        ac_results = [
            ACResult(ac_id="AC#1", result="PASS", evidence={}),
            ACResult(ac_id="AC#2", result="FAIL", evidence={}),
            ACResult(ac_id="AC#3", result="PASS", evidence={}),
        ]

        result = calculate_overall_result(ac_results)
        assert result == "FAIL"

    def test_br001_empty_list_is_fail(self):
        """BR-001: Empty AC list means FAIL."""
        result = calculate_overall_result([])
        assert result == "FAIL"

    def test_br002_valid_json_output(self, temp_dir):
        """BR-002: Report must be valid JSON."""
        story_id = "STORY-274"

        # Include various data types to stress JSON serialization
        verification_results = {
            "acceptance_criteria": [{
                "ac_id": "AC#1",
                "result": "PASS",
                "evidence": {
                    "string": "value",
                    "number": 42,
                    "float": 3.14,
                    "boolean": True,
                    "null": None,
                    "array": [1, 2, 3],
                    "nested": {"a": {"b": "c"}}
                },
                "issues": []
            }],
            "files_inspected": ["file1.py", "file2.py"]
        }

        generate_verification_report(story_id, verification_results)

        report_path = get_report_path(story_id)

        # This will raise if not valid JSON
        with open(report_path, 'r', encoding='utf-8') as f:
            parsed = json.load(f)

        assert parsed is not None
        assert parsed["story_id"] == "STORY-274"


# =============================================================================
# DATA MODEL VALIDATION TESTS
# =============================================================================

class TestDataModelValidation:
    """Tests for data model validation from technical specification."""

    def test_story_id_pattern_valid(self):
        """Test story_id matches STORY-NNN pattern."""
        # Valid patterns
        report = VerificationReport(
            story_id="STORY-274",
            verification_timestamp="2026-01-19T12:00:00Z",
            verification_duration_seconds=5,
            phase="4.5",
            overall_result="PASS",
            acceptance_criteria=[],
            files_inspected=[],
            total_issues=0
        )
        assert report.story_id == "STORY-274"

    def test_story_id_pattern_invalid(self):
        """Test invalid story_id patterns rejected."""
        with pytest.raises(ValueError, match="story_id must match"):
            VerificationReport(
                story_id="story-274",  # lowercase
                verification_timestamp="2026-01-19T12:00:00Z",
                verification_duration_seconds=5,
                phase="4.5",
                overall_result="PASS",
                acceptance_criteria=[],
                files_inspected=[],
                total_issues=0
            )

    def test_phase_validation(self):
        """Test phase must be 4.5 or 5.5."""
        with pytest.raises(ValueError, match="phase must be one of"):
            VerificationReport(
                story_id="STORY-274",
                verification_timestamp="2026-01-19T12:00:00Z",
                verification_duration_seconds=5,
                phase="3.0",  # Invalid
                overall_result="PASS",
                acceptance_criteria=[],
                files_inspected=[],
                total_issues=0
            )

    def test_overall_result_validation(self):
        """Test overall_result must be PASS or FAIL."""
        with pytest.raises(ValueError, match="overall_result must be"):
            VerificationReport(
                story_id="STORY-274",
                verification_timestamp="2026-01-19T12:00:00Z",
                verification_duration_seconds=5,
                phase="4.5",
                overall_result="PARTIAL",  # Invalid
                acceptance_criteria=[],
                files_inspected=[],
                total_issues=0
            )

    def test_duration_non_negative(self):
        """Test verification_duration_seconds must be >= 0."""
        with pytest.raises(ValueError, match="must be >= 0"):
            VerificationReport(
                story_id="STORY-274",
                verification_timestamp="2026-01-19T12:00:00Z",
                verification_duration_seconds=-1,  # Invalid
                phase="4.5",
                overall_result="PASS",
                acceptance_criteria=[],
                files_inspected=[],
                total_issues=0
            )

    def test_issue_line_number_validation(self):
        """Test Issue line_number must be >= 1."""
        with pytest.raises(ValueError, match="must be >= 1"):
            Issue(file_path="test.py", line_number=0, description="test")

    def test_acresult_result_validation(self):
        """Test ACResult result must be PASS or FAIL."""
        with pytest.raises(ValueError, match="must be 'PASS' or 'FAIL'"):
            ACResult(ac_id="AC#1", result="MAYBE", evidence={})


# =============================================================================
# NFR TESTS
# =============================================================================

class TestNonFunctionalRequirements:
    """Tests for NFRs from technical specification."""

    def test_nfr001_performance(self, temp_dir):
        """NFR-001: Report generation < 1 second."""
        import time

        story_id = "STORY-274"

        # Create reasonably sized verification data
        verification_results = {
            "acceptance_criteria": [
                {
                    "ac_id": f"AC#{i}",
                    "result": "PASS",
                    "evidence": {"index": i, "data": "x" * 100},
                    "issues": []
                }
                for i in range(1, 11)  # 10 ACs
            ],
            "files_inspected": [f"src/file{i}.py" for i in range(100)]  # 100 files
        }

        start = time.time()
        generate_verification_report(story_id, verification_results)
        elapsed = time.time() - start

        assert elapsed < 1.0, f"Report generation took {elapsed:.2f}s, should be < 1s"

    def test_nfr002_reliability(self, temp_dir):
        """NFR-002: 100% of verifications produce report."""
        story_id = "STORY-274"

        # Run multiple times
        for i in range(5):
            verification_results = {
                "acceptance_criteria": [{
                    "ac_id": f"AC#{i}",
                    "result": "PASS",
                    "evidence": {},
                    "issues": []
                }],
                "files_inspected": []
            }

            generate_verification_report(story_id, verification_results)

            report_path = get_report_path(story_id)
            assert os.path.exists(report_path), f"Report not created on iteration {i}"


# =============================================================================
# ERROR HANDLING TESTS
# =============================================================================

class TestErrorHandling:
    """Tests for error handling scenarios."""

    def test_missing_acceptance_criteria_key(self, temp_dir):
        """Test handling of missing acceptance_criteria key."""
        story_id = "STORY-274"

        # Empty dict
        verification_results = {}

        # Should handle gracefully
        result = generate_verification_report(story_id, verification_results)

        assert result["acceptance_criteria"] == []
        assert result["overall_result"] == "FAIL"  # Empty = fail

    def test_missing_files_inspected_key(self, temp_dir):
        """Test handling of missing files_inspected key."""
        story_id = "STORY-274"

        verification_results = {
            "acceptance_criteria": [{
                "ac_id": "AC#1",
                "result": "PASS",
                "evidence": {},
                "issues": []
            }]
        }

        result = generate_verification_report(story_id, verification_results)

        assert result["files_inspected"] == []


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

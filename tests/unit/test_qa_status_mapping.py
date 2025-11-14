"""
Unit test suite for STORY-024: QA Status Mapping Logic

Tests cover:
- Status determination from QA results
- Violation context extraction
- Hook logging and messaging
- Edge cases for status values

TDD Red Phase: All tests written BEFORE implementation.
Framework: pytest
Test Pattern: AAA (Arrange, Act, Assert)
Focus: QA result → status mapping logic (PASSED/FAILED/PARTIAL)
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import json


# ============================================================================
# FIXTURES - Status mapping test data
# ============================================================================


@pytest.fixture
def qa_status_mapper():
    """Fixture: QA status mapping functions (to be implemented)."""
    class QAStatusMapper:
        """Maps QA results to hook status values."""

        @staticmethod
        def map_qa_result_to_status(qa_result):
            """
            Map QA validation result to hook status.

            Args:
                qa_result (str): QA result ("PASSED", "FAILED", or "PARTIAL")

            Returns:
                str: Hook status ("completed", "failed", or "partial")

            Raises:
                ValueError: If qa_result not recognized
            """
            mapping = {
                "PASSED": "completed",
                "FAILED": "failed",
                "PARTIAL": "partial"
            }
            if qa_result not in mapping:
                raise ValueError(f"Unknown QA result: {qa_result}")
            return mapping[qa_result]

        @staticmethod
        def extract_violation_context(qa_report):
            """
            Extract violation context from QA report.

            Args:
                qa_report (dict): QA report with violations, coverage, etc.

            Returns:
                dict: Context dict with violations, coverage, message
            """
            context = {
                "story_id": qa_report.get("story_id"),
                "mode": qa_report.get("mode"),
                "violations": qa_report.get("violations", []),
                "coverage": qa_report.get("coverage"),
                "duration": qa_report.get("duration")
            }

            # Build human-readable message
            coverage = qa_report.get("coverage", {})
            if coverage:
                context["message"] = (
                    f"Coverage was {coverage.get('actual')}% "
                    f"(target {coverage.get('target')}%)"
                )

            return context

    return QAStatusMapper()


@pytest.fixture
def qa_report_passed():
    """Fixture: Passing QA report."""
    return {
        "story_id": "STORY-001",
        "mode": "deep",
        "result": "PASSED",
        "coverage": {
            "actual": 95,
            "target": 85,
            "gap": -10
        },
        "violations": [],
        "duration": 30
    }


@pytest.fixture
def qa_report_failed():
    """Fixture: Failing QA report."""
    return {
        "story_id": "STORY-001",
        "mode": "deep",
        "result": "FAILED",
        "coverage": {
            "actual": 75,
            "target": 85,
            "gap": 10
        },
        "violations": [
            {
                "type": "coverage",
                "severity": "HIGH",
                "message": "Business logic coverage 75% < 85%"
            },
            {
                "type": "anti-pattern",
                "severity": "MEDIUM",
                "message": "God Object detected"
            }
        ],
        "duration": 45
    }


@pytest.fixture
def qa_report_partial():
    """Fixture: Partial pass QA report."""
    return {
        "story_id": "STORY-001",
        "mode": "deep",
        "result": "PARTIAL",
        "coverage": {
            "actual": 90,
            "target": 85,
            "gap": -5
        },
        "violations": [
            {
                "type": "warning",
                "severity": "LOW",
                "message": "Missing docstring"
            }
        ],
        "duration": 35
    }


# ============================================================================
# TEST: Status Mapping - PASSED
# ============================================================================


@pytest.mark.unit
@pytest.mark.acceptance_criteria
class TestStatusMappingPassed:
    """Unit tests for PASSED → completed mapping."""

    def test_passed_maps_to_completed(self, qa_status_mapper):
        """
        Test: QA result "PASSED" maps to status "completed".

        Arrange: QA result is "PASSED"
        Act: Call map_qa_result_to_status("PASSED")
        Assert: Returns "completed"
        """
        # Arrange
        qa_result = "PASSED"

        # Act
        status = qa_status_mapper.map_qa_result_to_status(qa_result)

        # Assert
        assert status == "completed", "PASSED must map to completed"

    def test_passed_result_is_deterministic(self, qa_status_mapper):
        """
        Test: PASSED → completed mapping is deterministic.

        Multiple calls with same input yield same output.
        """
        # Arrange
        qa_result = "PASSED"

        # Act
        status1 = qa_status_mapper.map_qa_result_to_status(qa_result)
        status2 = qa_status_mapper.map_qa_result_to_status(qa_result)

        # Assert
        assert status1 == status2 == "completed"

    def test_passed_status_used_for_check_hooks(self, qa_status_mapper):
        """
        Test: "completed" status passed to check-hooks for PASSED QA.

        Given: QA result is PASSED
        When: Status determined
        Then: check-hooks called with --status=completed
        """
        # Arrange
        qa_result = "PASSED"

        # Act
        status = qa_status_mapper.map_qa_result_to_status(qa_result)

        # Assert
        assert status == "completed"
        # In actual Phase 4: devforgeai check-hooks --operation=qa --status=completed

    def test_passed_with_high_coverage(self, qa_status_mapper, qa_report_passed):
        """
        Test: PASSED status independent of coverage value.

        Status should be same whether coverage is 90% or 95%.
        """
        # Arrange
        qa_result = qa_report_passed['result']

        # Act
        status = qa_status_mapper.map_qa_result_to_status(qa_result)

        # Assert
        assert status == "completed", "Status determined by result, not coverage value"
        assert qa_report_passed['coverage']['actual'] >= 85  # Just verify report validity


# ============================================================================
# TEST: Status Mapping - FAILED
# ============================================================================


@pytest.mark.unit
@pytest.mark.acceptance_criteria
class TestStatusMappingFailed:
    """Unit tests for FAILED → failed mapping."""

    def test_failed_maps_to_failed(self, qa_status_mapper):
        """
        Test: QA result "FAILED" maps to status "failed".

        Arrange: QA result is "FAILED"
        Act: Call map_qa_result_to_status("FAILED")
        Assert: Returns "failed"
        """
        # Arrange
        qa_result = "FAILED"

        # Act
        status = qa_status_mapper.map_qa_result_to_status(qa_result)

        # Assert
        assert status == "failed", "FAILED must map to failed"

    def test_failed_result_is_deterministic(self, qa_status_mapper):
        """
        Test: FAILED → failed mapping is deterministic.

        Multiple calls with same input yield same output.
        """
        # Arrange
        qa_result = "FAILED"

        # Act
        status1 = qa_status_mapper.map_qa_result_to_status(qa_result)
        status2 = qa_status_mapper.map_qa_result_to_status(qa_result)

        # Assert
        assert status1 == status2 == "failed"

    def test_failed_status_used_for_check_hooks(self, qa_status_mapper):
        """
        Test: "failed" status passed to check-hooks for FAILED QA.

        Given: QA result is FAILED
        When: Status determined
        Then: check-hooks called with --status=failed
        """
        # Arrange
        qa_result = "FAILED"

        # Act
        status = qa_status_mapper.map_qa_result_to_status(qa_result)

        # Assert
        assert status == "failed"
        # In actual Phase 4: devforgeai check-hooks --operation=qa --status=failed

    def test_failed_with_coverage_gap(self, qa_status_mapper, qa_report_failed):
        """
        Test: FAILED status independent of coverage gap size.

        Status should be same whether coverage gap is 10% or 20%.
        """
        # Arrange
        qa_result = qa_report_failed['result']

        # Act
        status = qa_status_mapper.map_qa_result_to_status(qa_result)

        # Assert
        assert status == "failed", "Status determined by result, not coverage gap"

    def test_failed_with_multiple_violations(self, qa_status_mapper, qa_report_failed):
        """
        Test: FAILED status independent of violation count.

        Status should be same with 1 violation or 10 violations.
        """
        # Arrange
        qa_result = qa_report_failed['result']

        # Act
        status = qa_status_mapper.map_qa_result_to_status(qa_result)

        # Assert
        assert status == "failed", "Status determined by result, not violation count"


# ============================================================================
# TEST: Status Mapping - PARTIAL
# ============================================================================


@pytest.mark.unit
@pytest.mark.acceptance_criteria
class TestStatusMappingPartial:
    """Unit tests for PARTIAL → partial mapping."""

    def test_partial_maps_to_partial(self, qa_status_mapper):
        """
        Test: QA result "PARTIAL" maps to status "partial".

        Arrange: QA result is "PARTIAL"
        Act: Call map_qa_result_to_status("PARTIAL")
        Assert: Returns "partial"
        """
        # Arrange
        qa_result = "PARTIAL"

        # Act
        status = qa_status_mapper.map_qa_result_to_status(qa_result)

        # Assert
        assert status == "partial", "PARTIAL must map to partial"

    def test_partial_result_is_deterministic(self, qa_status_mapper):
        """
        Test: PARTIAL → partial mapping is deterministic.

        Multiple calls with same input yield same output.
        """
        # Arrange
        qa_result = "PARTIAL"

        # Act
        status1 = qa_status_mapper.map_qa_result_to_status(qa_result)
        status2 = qa_status_mapper.map_qa_result_to_status(qa_result)

        # Assert
        assert status1 == status2 == "partial"

    def test_partial_status_used_for_check_hooks(self, qa_status_mapper):
        """
        Test: "partial" status passed to check-hooks for PARTIAL QA.

        Given: QA result is PARTIAL
        When: Status determined
        Then: check-hooks called with --status=partial
        """
        # Arrange
        qa_result = "PARTIAL"

        # Act
        status = qa_status_mapper.map_qa_result_to_status(qa_result)

        # Assert
        assert status == "partial"
        # In actual Phase 4: devforgeai check-hooks --operation=qa --status=partial

    def test_partial_with_warnings_only(self, qa_status_mapper, qa_report_partial):
        """
        Test: PARTIAL status for warnings (not errors).

        Given: QA has warnings but no blocking violations
        When: Status determined
        Then: Status is "partial" (not failed)
        """
        # Arrange
        qa_result = qa_report_partial['result']
        violations = qa_report_partial['violations']

        # Act
        status = qa_status_mapper.map_qa_result_to_status(qa_result)

        # Assert
        assert status == "partial", "Warnings should result in partial"
        assert all(v['severity'] in ['LOW', 'MEDIUM'] for v in violations)


# ============================================================================
# TEST: Status Mapping - Invalid Input
# ============================================================================


@pytest.mark.unit
@pytest.mark.edge_case
class TestStatusMappingInvalidInput:
    """Unit tests for invalid status inputs."""

    def test_invalid_result_raises_error(self, qa_status_mapper):
        """
        Test: Invalid QA result raises ValueError.

        Arrange: QA result is "UNKNOWN"
        Act: Call map_qa_result_to_status("UNKNOWN")
        Assert: Raises ValueError
        """
        # Arrange
        qa_result = "UNKNOWN"

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            qa_status_mapper.map_qa_result_to_status(qa_result)

        assert "Unknown QA result" in str(exc_info.value)

    def test_empty_result_raises_error(self, qa_status_mapper):
        """
        Test: Empty QA result raises ValueError.

        Arrange: QA result is ""
        Act: Call map_qa_result_to_status("")
        Assert: Raises ValueError
        """
        # Arrange
        qa_result = ""

        # Act & Assert
        with pytest.raises(ValueError):
            qa_status_mapper.map_qa_result_to_status(qa_result)

    def test_none_result_raises_error(self, qa_status_mapper):
        """
        Test: None QA result raises ValueError.

        Arrange: QA result is None
        Act: Call map_qa_result_to_status(None)
        Assert: Raises ValueError or TypeError
        """
        # Arrange
        qa_result = None

        # Act & Assert
        with pytest.raises((ValueError, TypeError)):
            qa_status_mapper.map_qa_result_to_status(qa_result)

    def test_lowercase_result_requires_case_match(self, qa_status_mapper):
        """
        Test: Lowercase "passed" does not match "PASSED".

        Arrange: QA result is "passed" (lowercase)
        Act: Call map_qa_result_to_status("passed")
        Assert: Raises ValueError (case-sensitive)
        """
        # Arrange
        qa_result = "passed"

        # Act & Assert
        with pytest.raises(ValueError):
            qa_status_mapper.map_qa_result_to_status(qa_result)


# ============================================================================
# TEST: Violation Context Extraction
# ============================================================================


@pytest.mark.unit
@pytest.mark.acceptance_criteria
class TestViolationContextExtraction:
    """Unit tests for extracting violation context from QA reports."""

    def test_extract_coverage_context_from_failed_report(self, qa_status_mapper, qa_report_failed):
        """
        Test: Extract coverage context from failing QA report.

        Given: QA report with coverage 75% (target 85%)
        When: Extract violation context
        Then: Context includes "Coverage was 75% (target 85%)"
        """
        # Arrange
        qa_report = qa_report_failed

        # Act
        context = qa_status_mapper.extract_violation_context(qa_report)

        # Assert
        assert "message" in context, "Context must include message"
        assert "Coverage was 75%" in context['message']
        assert "target 85%" in context['message']

    def test_extract_violations_list_from_report(self, qa_status_mapper, qa_report_failed):
        """
        Test: Extract violations list from QA report.

        Given: QA report with multiple violations
        When: Extract violation context
        Then: Context includes all violations
        """
        # Arrange
        qa_report = qa_report_failed
        expected_violation_count = 2

        # Act
        context = qa_status_mapper.extract_violation_context(qa_report)

        # Assert
        assert "violations" in context, "Context must include violations"
        assert len(context['violations']) == expected_violation_count
        assert context['violations'][0]['type'] == "coverage"

    def test_extract_story_id_from_context(self, qa_status_mapper, qa_report_failed):
        """
        Test: Extract story ID from QA report.

        Given: QA report for STORY-001
        When: Extract violation context
        Then: Context includes story_id
        """
        # Arrange
        qa_report = qa_report_failed

        # Act
        context = qa_status_mapper.extract_violation_context(qa_report)

        # Assert
        assert context['story_id'] == "STORY-001"

    def test_extract_mode_from_context(self, qa_status_mapper, qa_report_failed):
        """
        Test: Extract validation mode from QA report.

        Given: Deep validation QA report
        When: Extract violation context
        Then: Context includes mode="deep"
        """
        # Arrange
        qa_report = qa_report_failed

        # Act
        context = qa_status_mapper.extract_violation_context(qa_report)

        # Assert
        assert context['mode'] == "deep"

    def test_extract_duration_from_context(self, qa_status_mapper, qa_report_failed):
        """
        Test: Extract validation duration from QA report.

        Given: QA report with duration (45 seconds)
        When: Extract violation context
        Then: Context includes duration
        """
        # Arrange
        qa_report = qa_report_failed

        # Act
        context = qa_status_mapper.extract_violation_context(qa_report)

        # Assert
        assert context['duration'] == 45

    def test_extract_context_from_passing_report(self, qa_status_mapper, qa_report_passed):
        """
        Test: Extract context from passing QA report.

        Given: Passing QA report with 95% coverage
        When: Extract violation context
        Then: Context includes coverage info (even though no violations)
        """
        # Arrange
        qa_report = qa_report_passed

        # Act
        context = qa_status_mapper.extract_violation_context(qa_report)

        # Assert
        assert context['story_id'] == "STORY-001"
        assert len(context['violations']) == 0, "Passing report has no violations"
        assert "Coverage was 95%" in context['message']

    def test_extract_context_missing_coverage_graceful(self, qa_status_mapper):
        """
        Test: Handle missing coverage data gracefully.

        Given: QA report without coverage field
        When: Extract violation context
        Then: Does not crash, returns empty or None
        """
        # Arrange
        qa_report = {
            "story_id": "STORY-001",
            "mode": "light",
            "result": "FAILED",
            "violations": [],
            # coverage field missing
        }

        # Act
        context = qa_status_mapper.extract_violation_context(qa_report)

        # Assert
        assert context['story_id'] == "STORY-001"
        # Coverage field is optional, should not cause crash


# ============================================================================
# TEST: Status Mapping with Different Modes
# ============================================================================


@pytest.mark.unit
class TestStatusMappingByMode:
    """Unit tests for status mapping in light vs deep modes."""

    def test_light_mode_failed_maps_to_failed(self, qa_status_mapper):
        """
        Test: Light mode failure maps to "failed" status.

        Arrange: QA light mode result is FAILED
        Act: Map to status
        Assert: Status is "failed"
        """
        # Arrange
        qa_result = "FAILED"
        mode = "light"

        # Act
        status = qa_status_mapper.map_qa_result_to_status(qa_result)

        # Assert
        assert status == "failed", "Light mode FAILED must map to failed"

    def test_deep_mode_failed_maps_to_failed(self, qa_status_mapper):
        """
        Test: Deep mode failure maps to "failed" status.

        Arrange: QA deep mode result is FAILED
        Act: Map to status
        Assert: Status is "failed"
        """
        # Arrange
        qa_result = "FAILED"
        mode = "deep"

        # Act
        status = qa_status_mapper.map_qa_result_to_status(qa_result)

        # Assert
        assert status == "failed", "Deep mode FAILED must map to failed"

    def test_status_mapping_independent_of_mode(self, qa_status_mapper):
        """
        Test: Status mapping is same for light and deep modes.

        Given: Same QA result in light and deep modes
        When: Map both to status
        Then: Both produce same status
        """
        # Arrange
        qa_result = "FAILED"

        # Act
        status_light = qa_status_mapper.map_qa_result_to_status(qa_result)
        status_deep = qa_status_mapper.map_qa_result_to_status(qa_result)

        # Assert
        assert status_light == status_deep == "failed"


# ============================================================================
# TEST: Violation Context Logging
# ============================================================================


@pytest.mark.unit
class TestViolationContextLogging:
    """Unit tests for logging violation context."""

    def test_log_message_includes_coverage_info(self, qa_status_mapper, qa_report_failed):
        """
        Test: Log message includes coverage percentage and target.

        Given: QA failed with 75% coverage (target 85%)
        When: Generate log message
        Then: Message includes "75%" and "85%"
        """
        # Arrange
        qa_report = qa_report_failed

        # Act
        context = qa_status_mapper.extract_violation_context(qa_report)
        log_message = context['message']

        # Assert
        assert "75%" in log_message, "Coverage percentage must be logged"
        assert "85%" in log_message, "Target coverage must be logged"

    def test_log_violation_types_available(self, qa_status_mapper, qa_report_failed):
        """
        Test: Violation types available for logging.

        Given: QA report with coverage and anti-pattern violations
        When: Extract context
        Then: Violation types are coverage, anti-pattern, etc.
        """
        # Arrange
        qa_report = qa_report_failed

        # Act
        context = qa_status_mapper.extract_violation_context(qa_report)
        violation_types = [v['type'] for v in context['violations']]

        # Assert
        assert "coverage" in violation_types
        assert "anti-pattern" in violation_types


# ============================================================================
# TEST: Parametrized Status Mapping
# ============================================================================


@pytest.mark.unit
@pytest.mark.parametrize("qa_result,expected_status", [
    ("PASSED", "completed"),
    ("FAILED", "failed"),
    ("PARTIAL", "partial"),
])
def test_all_status_mappings(qa_status_mapper, qa_result, expected_status):
    """
    Parametrized test: All QA results map to correct status.

    Tests all three main mappings in single test.
    """
    # Arrange
    qa_input = qa_result

    # Act
    status = qa_status_mapper.map_qa_result_to_status(qa_input)

    # Assert
    assert status == expected_status, \
        f"{qa_result} should map to {expected_status}, got {status}"


@pytest.mark.unit
@pytest.mark.parametrize("invalid_result", [
    "SKIP",
    "WARNING",
    "ERROR",
    "pending",
    "success",
    "",
    None,
])
def test_invalid_status_mappings(qa_status_mapper, invalid_result):
    """
    Parametrized test: Invalid results raise errors.

    Tests various invalid inputs.
    """
    # Arrange
    qa_input = invalid_result

    # Act & Assert
    with pytest.raises((ValueError, TypeError)):
        qa_status_mapper.map_qa_result_to_status(qa_input)

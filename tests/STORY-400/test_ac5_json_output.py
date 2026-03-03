"""
Test: AC#5 - JSON Output Format Compliance
Story: STORY-400
Generated: 2026-02-14

Validates that long parameter list findings include all required fields
matching the LongParameterListFinding schema: smell_type, severity,
function_name, file, line, parameter_count, parameters, evidence, remediation.

These tests will FAIL until the output format is implemented in the
anti-pattern-scanner Phase 5 long parameter list detection.
"""

import os
import sys
import pytest

# Add test directory to path for import (directory has hyphen, not valid Python module name)
sys.path.insert(0, os.path.dirname(__file__))
from long_parameter_list_detector import (
    detect_long_parameter_list,
)


# =============================================================================
# Fixtures: Expected finding output
# =============================================================================


@pytest.fixture
def treelint_function_violation():
    """Mock Treelint output for a function that violates the threshold."""
    return {
        "results": [
            {
                "name": "process_order",
                "type": "function",
                "file": "src/services/order_service.py",
                "lines": {"start": 10, "end": 25},
                "signature": "def process_order(customer_id, product_id, quantity, discount, shipping_method)",
            }
        ]
    }


@pytest.fixture
def treelint_method_violation_with_self():
    """Mock Treelint output for a Python method with self that violates threshold."""
    return {
        "results": [
            {
                "name": "send_email",
                "type": "function",
                "file": "src/services/email_service.py",
                "lines": {"start": 30, "end": 50},
                "signature": "def send_email(self, recipient, subject, body, cc, bcc, reply_to)",
            }
        ]
    }


# =============================================================================
# Required fields for LongParameterListFinding schema
# =============================================================================

REQUIRED_FIELDS = [
    "smell_type",
    "severity",
    "function_name",
    "file",
    "line",
    "parameter_count",
    "parameters",
    "evidence",
    "remediation",
]


# =============================================================================
# Implementation imported from shared module (TDD Green phase)
# detect_long_parameter_list imported at top of file
# =============================================================================


# =============================================================================
# Tests: Required Field Presence
# =============================================================================


class TestRequiredFieldPresence:
    """Tests that all required fields exist in findings (AC#5)."""

    def test_should_include_all_required_fields(self, treelint_function_violation):
        """Every finding must include all 9 required fields."""
        findings = detect_long_parameter_list(treelint_function_violation, threshold=4)
        assert len(findings) == 1
        finding = findings[0]
        for field in REQUIRED_FIELDS:
            assert field in finding, f"Missing required field: {field}"

    def test_should_not_include_extra_unexpected_fields(
        self, treelint_function_violation
    ):
        """Findings should only contain expected fields (no extraneous data)."""
        findings = detect_long_parameter_list(treelint_function_violation, threshold=4)
        finding = findings[0]
        allowed_fields = set(REQUIRED_FIELDS)
        actual_fields = set(finding.keys())
        unexpected = actual_fields - allowed_fields
        assert unexpected == set(), f"Unexpected fields: {unexpected}"


# =============================================================================
# Tests: Field Value Constraints
# =============================================================================


class TestSmellTypeField:
    """Tests for smell_type field value (AC#5)."""

    def test_should_have_smell_type_long_parameter_list(
        self, treelint_function_violation
    ):
        """smell_type must always be 'long_parameter_list'."""
        findings = detect_long_parameter_list(treelint_function_violation, threshold=4)
        assert findings[0]["smell_type"] == "long_parameter_list"

    def test_smell_type_should_be_string(self, treelint_function_violation):
        """smell_type must be a string type."""
        findings = detect_long_parameter_list(treelint_function_violation, threshold=4)
        assert isinstance(findings[0]["smell_type"], str)


class TestSeverityField:
    """Tests for severity field value (AC#5)."""

    def test_should_have_severity_medium(self, treelint_function_violation):
        """severity must always be 'MEDIUM' for long parameter list."""
        findings = detect_long_parameter_list(treelint_function_violation, threshold=4)
        assert findings[0]["severity"] == "MEDIUM"

    def test_severity_should_be_string(self, treelint_function_violation):
        """severity must be a string type."""
        findings = detect_long_parameter_list(treelint_function_violation, threshold=4)
        assert isinstance(findings[0]["severity"], str)


class TestFunctionNameField:
    """Tests for function_name field value (AC#5)."""

    def test_should_have_correct_function_name(self, treelint_function_violation):
        """function_name must match the actual function identifier."""
        findings = detect_long_parameter_list(treelint_function_violation, threshold=4)
        assert findings[0]["function_name"] == "process_order"

    def test_function_name_should_be_string(self, treelint_function_violation):
        """function_name must be a string type."""
        findings = detect_long_parameter_list(treelint_function_violation, threshold=4)
        assert isinstance(findings[0]["function_name"], str)


class TestFileField:
    """Tests for file field value (AC#5)."""

    def test_should_have_correct_file_path(self, treelint_function_violation):
        """file must be a relative path matching the Treelint output."""
        findings = detect_long_parameter_list(treelint_function_violation, threshold=4)
        assert findings[0]["file"] == "src/services/order_service.py"

    def test_file_should_be_relative_path(self, treelint_function_violation):
        """file must be a relative path (not absolute)."""
        findings = detect_long_parameter_list(treelint_function_violation, threshold=4)
        assert not findings[0]["file"].startswith("/")


class TestLineField:
    """Tests for line field value (AC#5)."""

    def test_should_have_correct_line_number(self, treelint_function_violation):
        """line must match the function definition start line from Treelint."""
        findings = detect_long_parameter_list(treelint_function_violation, threshold=4)
        assert findings[0]["line"] == 10

    def test_line_should_be_positive_integer(self, treelint_function_violation):
        """line must be a positive integer."""
        findings = detect_long_parameter_list(treelint_function_violation, threshold=4)
        assert isinstance(findings[0]["line"], int)
        assert findings[0]["line"] > 0


class TestParameterCountField:
    """Tests for parameter_count field value (AC#5)."""

    def test_should_have_correct_parameter_count(self, treelint_function_violation):
        """parameter_count must match actual count (excluding self/cls/*args/**kwargs)."""
        findings = detect_long_parameter_list(treelint_function_violation, threshold=4)
        assert findings[0]["parameter_count"] == 5

    def test_parameter_count_should_exceed_threshold(
        self, treelint_function_violation
    ):
        """parameter_count must be greater than the threshold (> 4)."""
        findings = detect_long_parameter_list(treelint_function_violation, threshold=4)
        assert findings[0]["parameter_count"] > 4

    def test_parameter_count_should_be_integer(self, treelint_function_violation):
        """parameter_count must be an integer type."""
        findings = detect_long_parameter_list(treelint_function_violation, threshold=4)
        assert isinstance(findings[0]["parameter_count"], int)

    def test_parameter_count_excludes_self_in_method(
        self, treelint_method_violation_with_self
    ):
        """parameter_count for method should exclude self."""
        findings = detect_long_parameter_list(
            treelint_method_violation_with_self, threshold=4
        )
        # send_email(self, recipient, subject, body, cc, bcc, reply_to) = 6 real params
        assert findings[0]["parameter_count"] == 6


class TestParametersArrayField:
    """Tests for parameters array field value (AC#5)."""

    def test_should_have_correct_parameters_list(self, treelint_function_violation):
        """parameters must contain actual parameter names."""
        findings = detect_long_parameter_list(treelint_function_violation, threshold=4)
        expected_params = [
            "customer_id",
            "product_id",
            "quantity",
            "discount",
            "shipping_method",
        ]
        assert findings[0]["parameters"] == expected_params

    def test_parameters_should_be_list(self, treelint_function_violation):
        """parameters must be a list type."""
        findings = detect_long_parameter_list(treelint_function_violation, threshold=4)
        assert isinstance(findings[0]["parameters"], list)

    def test_parameters_should_not_include_self(
        self, treelint_method_violation_with_self
    ):
        """parameters list for methods should not include self."""
        findings = detect_long_parameter_list(
            treelint_method_violation_with_self, threshold=4
        )
        assert "self" not in findings[0]["parameters"]

    def test_parameters_count_matches_parameter_count_field(
        self, treelint_function_violation
    ):
        """len(parameters) must equal parameter_count."""
        findings = detect_long_parameter_list(treelint_function_violation, threshold=4)
        assert len(findings[0]["parameters"]) == findings[0]["parameter_count"]


class TestEvidenceField:
    """Tests for evidence field value (AC#5)."""

    def test_should_include_parameter_count_in_evidence(
        self, treelint_function_violation
    ):
        """evidence must include the parameter count."""
        findings = detect_long_parameter_list(treelint_function_violation, threshold=4)
        assert "5" in findings[0]["evidence"]

    def test_should_include_threshold_in_evidence(self, treelint_function_violation):
        """evidence must include the threshold value."""
        findings = detect_long_parameter_list(treelint_function_violation, threshold=4)
        assert "4" in findings[0]["evidence"]

    def test_evidence_should_be_human_readable(self, treelint_function_violation):
        """evidence must be a non-empty human-readable string."""
        findings = detect_long_parameter_list(treelint_function_violation, threshold=4)
        assert isinstance(findings[0]["evidence"], str)
        assert len(findings[0]["evidence"]) > 10


class TestRemediationField:
    """Tests for remediation field value (AC#5)."""

    def test_should_suggest_parameter_object_pattern(
        self, treelint_function_violation
    ):
        """remediation must suggest the Parameter Object pattern."""
        findings = detect_long_parameter_list(treelint_function_violation, threshold=4)
        remediation = findings[0]["remediation"].lower()
        assert (
            "parameter object" in remediation
            or "data class" in remediation
            or "group" in remediation
        ), f"Remediation should suggest Parameter Object pattern, got: {findings[0]['remediation']}"

    def test_remediation_should_be_non_empty_string(
        self, treelint_function_violation
    ):
        """remediation must be a non-empty string."""
        findings = detect_long_parameter_list(treelint_function_violation, threshold=4)
        assert isinstance(findings[0]["remediation"], str)
        assert len(findings[0]["remediation"]) > 10


# =============================================================================
# Tests: No Two-Stage Filtering (BR-004)
# =============================================================================


class TestNoTwoStageFiltering:
    """Tests that long parameter list detection is immediate (no Stage 2 LLM assessment)."""

    def test_should_detect_without_stage2_assessment(
        self, treelint_function_violation
    ):
        """Detection must be immediate - no two-stage filtering for parameter counts."""
        # Parameter count is deterministic; LLM assessment adds no value (BR-004)
        findings = detect_long_parameter_list(treelint_function_violation, threshold=4)
        assert len(findings) == 1
        # Finding should NOT have a 'confidence' field (that is for two-stage smells like data_class)
        assert "confidence" not in findings[0], (
            "Long parameter list findings should NOT have 'confidence' field - "
            "detection is deterministic, not probabilistic"
        )

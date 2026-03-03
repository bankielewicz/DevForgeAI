"""
Test: AC#5 - JSON Output Format Compliance
Story: STORY-405
Generated: 2026-02-15

Validates that middle man findings include all required fields matching
the MiddleManFinding schema: smell_type, severity, class_name, file, line,
total_methods, delegating_methods, delegation_ratio, evidence, remediation.

These tests will FAIL until the output format is implemented in the
anti-pattern-scanner Phase 5 middle man detection.
"""

import os
import sys
import pytest

# Add test directory to path for import
sys.path.insert(0, os.path.dirname(__file__))
from middle_man_detector import (
    detect_middle_man,
    build_middle_man_finding,
)


# =============================================================================
# Fixtures: Expected finding output
# =============================================================================


@pytest.fixture
def treelint_middle_man_class():
    """Mock Treelint output for a class that is a middle man."""
    return {
        "results": [
            {
                "name": "OrderProxy",
                "type": "class",
                "file": "src/services/order_proxy.py",
                "lines": {"start": 5, "end": 40},
                "members": {
                    "methods": [
                        {"name": "get_order", "lines": {"start": 8, "end": 9}},
                        {"name": "create_order", "lines": {"start": 12, "end": 13}},
                        {"name": "update_order", "lines": {"start": 16, "end": 17}},
                        {"name": "delete_order", "lines": {"start": 20, "end": 21}},
                    ]
                },
            }
        ]
    }


# =============================================================================
# Required fields for MiddleManFinding schema
# =============================================================================

REQUIRED_FIELDS = [
    "smell_type",
    "severity",
    "class_name",
    "file",
    "line",
    "total_methods",
    "delegating_methods",
    "delegation_ratio",
    "evidence",
    "remediation",
]


# =============================================================================
# Tests: Required Field Presence
# =============================================================================


class TestRequiredFieldPresence:
    """Tests that all required fields exist in findings (AC#5)."""

    def test_should_include_all_required_fields(self, treelint_middle_man_class):
        """Every finding must include all 10 required fields."""
        findings = detect_middle_man(treelint_middle_man_class)
        assert len(findings) == 1, "Expected 1 middle man finding"
        finding = findings[0]
        for field in REQUIRED_FIELDS:
            assert field in finding, f"Missing required field: {field}"

    def test_should_not_include_extra_unexpected_fields(
        self, treelint_middle_man_class
    ):
        """Findings should only contain expected fields (no extraneous data)."""
        findings = detect_middle_man(treelint_middle_man_class)
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

    def test_should_have_smell_type_middle_man(self, treelint_middle_man_class):
        """smell_type must always be 'middle_man'."""
        findings = detect_middle_man(treelint_middle_man_class)
        assert findings[0]["smell_type"] == "middle_man"

    def test_smell_type_should_be_string(self, treelint_middle_man_class):
        """smell_type must be a string type."""
        findings = detect_middle_man(treelint_middle_man_class)
        assert isinstance(findings[0]["smell_type"], str)


class TestSeverityField:
    """Tests for severity field value (AC#5)."""

    def test_should_have_severity_medium(self, treelint_middle_man_class):
        """severity must always be 'MEDIUM' for middle man."""
        findings = detect_middle_man(treelint_middle_man_class)
        assert findings[0]["severity"] == "MEDIUM"

    def test_severity_should_be_string(self, treelint_middle_man_class):
        """severity must be a string type."""
        findings = detect_middle_man(treelint_middle_man_class)
        assert isinstance(findings[0]["severity"], str)


class TestClassNameField:
    """Tests for class_name field value (AC#5)."""

    def test_should_have_correct_class_name(self, treelint_middle_man_class):
        """class_name must match the actual class identifier."""
        findings = detect_middle_man(treelint_middle_man_class)
        assert findings[0]["class_name"] == "OrderProxy"

    def test_class_name_should_be_string(self, treelint_middle_man_class):
        """class_name must be a string type."""
        findings = detect_middle_man(treelint_middle_man_class)
        assert isinstance(findings[0]["class_name"], str)


class TestFileField:
    """Tests for file field value (AC#5)."""

    def test_should_have_correct_file_path(self, treelint_middle_man_class):
        """file must be a relative path matching the Treelint output."""
        findings = detect_middle_man(treelint_middle_man_class)
        assert findings[0]["file"] == "src/services/order_proxy.py"

    def test_file_should_be_relative_path(self, treelint_middle_man_class):
        """file must be a relative path (not absolute)."""
        findings = detect_middle_man(treelint_middle_man_class)
        assert not findings[0]["file"].startswith("/")


class TestLineField:
    """Tests for line field value (AC#5)."""

    def test_should_have_correct_line_number(self, treelint_middle_man_class):
        """line must match the class definition start line from Treelint."""
        findings = detect_middle_man(treelint_middle_man_class)
        assert findings[0]["line"] == 5

    def test_line_should_be_positive_integer(self, treelint_middle_man_class):
        """line must be a positive integer."""
        findings = detect_middle_man(treelint_middle_man_class)
        assert isinstance(findings[0]["line"], int)
        assert findings[0]["line"] > 0


class TestTotalMethodsField:
    """Tests for total_methods field value (AC#5)."""

    def test_should_have_correct_total_methods(self, treelint_middle_man_class):
        """total_methods must equal the number of methods in the class."""
        findings = detect_middle_man(treelint_middle_man_class)
        assert findings[0]["total_methods"] == 4

    def test_total_methods_should_be_at_least_3(self, treelint_middle_man_class):
        """total_methods must be >= 3 (minimum threshold)."""
        findings = detect_middle_man(treelint_middle_man_class)
        assert findings[0]["total_methods"] >= 3

    def test_total_methods_should_be_integer(self, treelint_middle_man_class):
        """total_methods must be an integer type."""
        findings = detect_middle_man(treelint_middle_man_class)
        assert isinstance(findings[0]["total_methods"], int)


class TestDelegatingMethodsField:
    """Tests for delegating_methods field value (AC#5)."""

    def test_should_have_correct_delegating_methods(self, treelint_middle_man_class):
        """delegating_methods must match actual count of short methods."""
        findings = detect_middle_man(treelint_middle_man_class)
        assert findings[0]["delegating_methods"] == 4

    def test_delegating_methods_should_be_integer(self, treelint_middle_man_class):
        """delegating_methods must be an integer type."""
        findings = detect_middle_man(treelint_middle_man_class)
        assert isinstance(findings[0]["delegating_methods"], int)


class TestDelegationRatioField:
    """Tests for delegation_ratio field value (AC#5)."""

    def test_should_have_correct_delegation_ratio(self, treelint_middle_man_class):
        """delegation_ratio must equal delegating_methods / total_methods."""
        findings = detect_middle_man(treelint_middle_man_class)
        expected_ratio = 4 / 4  # 1.0
        assert findings[0]["delegation_ratio"] == pytest.approx(expected_ratio)

    def test_delegation_ratio_should_be_float(self, treelint_middle_man_class):
        """delegation_ratio must be a float type."""
        findings = detect_middle_man(treelint_middle_man_class)
        assert isinstance(findings[0]["delegation_ratio"], float)

    def test_delegation_ratio_should_be_in_range(self, treelint_middle_man_class):
        """delegation_ratio must be between 0.0 and 1.0."""
        findings = detect_middle_man(treelint_middle_man_class)
        ratio = findings[0]["delegation_ratio"]
        assert 0.0 <= ratio <= 1.0, f"Ratio {ratio} out of range [0.0, 1.0]"

    def test_delegation_ratio_equals_delegating_over_total(
        self, treelint_middle_man_class
    ):
        """delegation_ratio must equal delegating_methods / total_methods."""
        findings = detect_middle_man(treelint_middle_man_class)
        finding = findings[0]
        expected = finding["delegating_methods"] / finding["total_methods"]
        assert finding["delegation_ratio"] == pytest.approx(expected)


class TestEvidenceField:
    """Tests for evidence field value (AC#5)."""

    def test_should_describe_delegation_pattern(self, treelint_middle_man_class):
        """evidence must describe the delegation pattern detected."""
        findings = detect_middle_man(treelint_middle_man_class)
        evidence = findings[0]["evidence"]
        assert "delegation" in evidence.lower() or "delegate" in evidence.lower(), (
            f"Evidence should describe delegation pattern, got: {evidence}"
        )

    def test_should_include_class_name_in_evidence(self, treelint_middle_man_class):
        """evidence must mention the class name."""
        findings = detect_middle_man(treelint_middle_man_class)
        assert "OrderProxy" in findings[0]["evidence"]

    def test_evidence_should_be_human_readable(self, treelint_middle_man_class):
        """evidence must be a non-empty human-readable string."""
        findings = detect_middle_man(treelint_middle_man_class)
        assert isinstance(findings[0]["evidence"], str)
        assert len(findings[0]["evidence"]) > 10


class TestRemediationField:
    """Tests for remediation field value (AC#5)."""

    def test_should_suggest_removing_proxy(self, treelint_middle_man_class):
        """remediation must suggest removing the proxy/middle man."""
        findings = detect_middle_man(treelint_middle_man_class)
        remediation = findings[0]["remediation"].lower()
        assert (
            "remov" in remediation
            or "eliminat" in remediation
            or "direct" in remediation
            or "bypass" in remediation
        ), f"Remediation should suggest removing the proxy, got: {findings[0]['remediation']}"

    def test_remediation_should_be_non_empty_string(self, treelint_middle_man_class):
        """remediation must be a non-empty string."""
        findings = detect_middle_man(treelint_middle_man_class)
        assert isinstance(findings[0]["remediation"], str)
        assert len(findings[0]["remediation"]) > 10


# =============================================================================
# Tests: Build Finding Helper
# =============================================================================


class TestBuildMiddleManFinding:
    """Tests for the build_middle_man_finding helper function."""

    def test_should_build_finding_with_all_fields(self):
        """Builder must produce a dict with all 10 required fields."""
        finding = build_middle_man_finding(
            class_name="TestProxy",
            file_path="src/test.py",
            line=10,
            total_methods=5,
            delegating_methods=4,
            delegation_ratio=0.80,
        )
        for field in REQUIRED_FIELDS:
            assert field in finding, f"Builder missing required field: {field}"

    def test_should_set_smell_type_to_middle_man(self):
        """Builder must set smell_type to 'middle_man'."""
        finding = build_middle_man_finding(
            class_name="TestProxy",
            file_path="src/test.py",
            line=10,
            total_methods=5,
            delegating_methods=4,
            delegation_ratio=0.80,
        )
        assert finding["smell_type"] == "middle_man"

    def test_should_set_severity_to_medium(self):
        """Builder must set severity to 'MEDIUM'."""
        finding = build_middle_man_finding(
            class_name="TestProxy",
            file_path="src/test.py",
            line=10,
            total_methods=5,
            delegating_methods=4,
            delegation_ratio=0.80,
        )
        assert finding["severity"] == "MEDIUM"

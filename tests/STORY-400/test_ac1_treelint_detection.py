"""
Test: AC#1 - Treelint-Based Parameter Count Detection
Story: STORY-400
Generated: 2026-02-14

Validates that the anti-pattern-scanner Phase 5 detects functions with
parameter_count > 4 (excluding self/cls) as long parameter list violations
when using Treelint AST-aware search.

These tests will FAIL until the long parameter list detection logic is
implemented in src/claude/agents/anti-pattern-scanner.md Phase 5.
"""

import json
import os
import sys
import pytest

# Add test directory to path for import (directory has hyphen, not valid Python module name)
sys.path.insert(0, os.path.dirname(__file__))
from long_parameter_list_detector import (
    detect_long_parameter_list,
    parse_parameters_from_signature,
    count_effective_parameters,
)


# =============================================================================
# Fixtures: Mock Treelint JSON output for parameter detection scenarios
# =============================================================================


@pytest.fixture
def treelint_function_5_params():
    """Mock Treelint JSON output for a function with 5 parameters (violation)."""
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
def treelint_function_4_params():
    """Mock Treelint JSON output for a function with exactly 4 parameters (no violation)."""
    return {
        "results": [
            {
                "name": "update_profile",
                "type": "function",
                "file": "src/services/user_service.py",
                "lines": {"start": 15, "end": 30},
                "signature": "def update_profile(user_id, name, email, phone)",
            }
        ]
    }


@pytest.fixture
def treelint_function_3_params():
    """Mock Treelint JSON output for a function with 3 parameters (no violation)."""
    return {
        "results": [
            {
                "name": "create_user",
                "type": "function",
                "file": "src/services/user_service.py",
                "lines": {"start": 5, "end": 12},
                "signature": "def create_user(name, email, password)",
            }
        ]
    }


@pytest.fixture
def treelint_function_6_params():
    """Mock Treelint JSON output for a function with 6 parameters (violation)."""
    return {
        "results": [
            {
                "name": "send_notification",
                "type": "function",
                "file": "src/services/notification_service.py",
                "lines": {"start": 20, "end": 40},
                "signature": "def send_notification(user_id, channel, subject, body, priority, retry_count)",
            }
        ]
    }


@pytest.fixture
def treelint_multiple_functions():
    """Mock Treelint JSON output with multiple functions, some violating threshold."""
    return {
        "results": [
            {
                "name": "simple_func",
                "type": "function",
                "file": "src/utils.py",
                "lines": {"start": 1, "end": 5},
                "signature": "def simple_func(a, b)",
            },
            {
                "name": "complex_func",
                "type": "function",
                "file": "src/utils.py",
                "lines": {"start": 10, "end": 30},
                "signature": "def complex_func(a, b, c, d, e, f)",
            },
            {
                "name": "boundary_func",
                "type": "function",
                "file": "src/utils.py",
                "lines": {"start": 35, "end": 45},
                "signature": "def boundary_func(a, b, c, d)",
            },
        ]
    }


# =============================================================================
# Implementation imported from shared module (TDD Green phase)
# parse_parameters_from_signature, count_effective_parameters,
# detect_long_parameter_list imported at top of file
# =============================================================================


# =============================================================================
# Tests: Parameter Count Threshold Detection
# =============================================================================


class TestTreelintParameterCountDetection:
    """Tests for Treelint-based parameter count detection (AC#1)."""

    def test_should_detect_violation_when_function_has_5_params(
        self, treelint_function_5_params
    ):
        """Function with 5 parameters (> threshold of 4) should be flagged."""
        findings = detect_long_parameter_list(treelint_function_5_params, threshold=4)
        assert len(findings) == 1
        assert findings[0]["function_name"] == "process_order"
        assert findings[0]["parameter_count"] == 5

    def test_should_not_detect_violation_when_function_has_4_params(
        self, treelint_function_4_params
    ):
        """Function with exactly 4 parameters (= threshold) should NOT be flagged."""
        findings = detect_long_parameter_list(treelint_function_4_params, threshold=4)
        assert len(findings) == 0

    def test_should_not_detect_violation_when_function_has_3_params(
        self, treelint_function_3_params
    ):
        """Function with 3 parameters (< threshold) should NOT be flagged."""
        findings = detect_long_parameter_list(treelint_function_3_params, threshold=4)
        assert len(findings) == 0

    def test_should_detect_violation_when_function_has_6_params(
        self, treelint_function_6_params
    ):
        """Function with 6 parameters should be flagged with correct count."""
        findings = detect_long_parameter_list(treelint_function_6_params, threshold=4)
        assert len(findings) == 1
        assert findings[0]["parameter_count"] == 6

    def test_should_detect_only_violating_functions_in_batch(
        self, treelint_multiple_functions
    ):
        """Only functions exceeding threshold should be flagged in batch scan."""
        findings = detect_long_parameter_list(treelint_multiple_functions, threshold=4)
        # simple_func has 2 params (ok), complex_func has 6 (violation), boundary_func has 4 (ok)
        assert len(findings) == 1
        assert findings[0]["function_name"] == "complex_func"
        assert findings[0]["parameter_count"] == 6

    def test_should_include_file_and_line_in_finding(
        self, treelint_function_5_params
    ):
        """Each finding must include file path and line number from Treelint output."""
        findings = detect_long_parameter_list(treelint_function_5_params, threshold=4)
        assert findings[0]["file"] == "src/services/order_service.py"
        assert findings[0]["line"] == 10

    def test_should_use_default_threshold_of_4(self, treelint_function_5_params):
        """Default threshold should be 4 (5+ params = violation)."""
        findings = detect_long_parameter_list(treelint_function_5_params)
        assert len(findings) == 1

    def test_should_return_empty_list_for_empty_results(self):
        """Empty Treelint results should return no findings."""
        empty_output = {"results": []}
        findings = detect_long_parameter_list(empty_output, threshold=4)
        assert findings == []


class TestParameterParsing:
    """Tests for parsing parameters from Treelint signature strings."""

    def test_should_parse_simple_parameter_list(self):
        """Parse basic parameter names from signature."""
        signature = "def func(a, b, c, d, e)"
        params = parse_parameters_from_signature(signature)
        assert params == ["a", "b", "c", "d", "e"]

    def test_should_parse_typed_parameters(self):
        """Parse parameter names ignoring type annotations."""
        signature = "def func(name: str, age: int, active: bool)"
        params = parse_parameters_from_signature(signature)
        assert params == ["name", "age", "active"]

    def test_should_parse_parameters_with_defaults(self):
        """Parse parameter names ignoring default values."""
        signature = 'def func(a, b=10, c="test", d=None, e=True)'
        params = parse_parameters_from_signature(signature)
        assert params == ["a", "b", "c", "d", "e"]

    def test_should_handle_no_parameters(self):
        """Function with no parameters returns empty list."""
        signature = "def func()"
        params = parse_parameters_from_signature(signature)
        assert params == []

    def test_should_parse_typescript_function_signature(self):
        """Parse TypeScript function parameters from Treelint signature."""
        signature = "function processOrder(customerId: string, productId: string, qty: number, discount: number, method: string)"
        params = parse_parameters_from_signature(signature)
        assert params == ["customerId", "productId", "qty", "discount", "method"]

    def test_should_parse_javascript_arrow_function(self):
        """Parse JavaScript arrow function parameters."""
        signature = "const handler = (req, res, next, options, config) =>"
        params = parse_parameters_from_signature(signature)
        assert params == ["req", "res", "next", "options", "config"]


class TestTreelintQueryConstruction:
    """Tests that the scanner constructs the correct Treelint query."""

    def test_should_use_treelint_search_type_function(self):
        """Scanner must use 'treelint search --type function --format json' for detection."""
        # Validate that the anti-pattern-scanner.md specification
        # includes the correct Treelint command for function enumeration
        expected_command = "treelint search --type function --format json"
        scanner_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "src",
            "claude",
            "agents",
            "anti-pattern-scanner.md",
        )
        scanner_path = os.path.normpath(scanner_path)
        with open(scanner_path, "r", encoding="utf-8") as f:
            scanner_content = f.read()
        assert expected_command in scanner_content, (
            f"anti-pattern-scanner.md must contain '{expected_command}' "
            "for long parameter list detection"
        )

    def test_should_handle_treelint_exit_code_0_with_results(
        self, treelint_function_5_params
    ):
        """Exit code 0 with results should process findings normally."""
        findings = detect_long_parameter_list(treelint_function_5_params, threshold=4)
        assert len(findings) >= 1

    def test_should_handle_treelint_exit_code_0_empty_results(self):
        """Exit code 0 with empty results is valid - do NOT fall back to Grep."""
        empty_output = {"results": []}
        findings = detect_long_parameter_list(empty_output, threshold=4)
        assert findings == []

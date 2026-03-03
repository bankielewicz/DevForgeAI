"""
Test: AC#2 - Python Self/Cls Exclusion
Story: STORY-400
Generated: 2026-02-14

Validates that self and cls parameters are excluded from parameter count
when detecting long parameter lists in Python methods.

These tests will FAIL until the self/cls exclusion logic is implemented
in the anti-pattern-scanner Phase 5 long parameter list detection.
"""

import os
import sys
import pytest

# Add test directory to path for import (directory has hyphen, not valid Python module name)
sys.path.insert(0, os.path.dirname(__file__))
from long_parameter_list_detector import (
    detect_long_parameter_list,
    count_effective_parameters,
)


# =============================================================================
# Fixtures: Mock Treelint output for Python methods with self/cls
# =============================================================================


@pytest.fixture
def treelint_method_self_6_total_params():
    """Python method with self + 5 real params (should flag: 5 > 4)."""
    return {
        "results": [
            {
                "name": "process_order",
                "type": "function",
                "file": "src/services/order_service.py",
                "lines": {"start": 10, "end": 25},
                "signature": "def process_order(self, customer_id, product_id, quantity, discount, shipping_method)",
            }
        ]
    }


@pytest.fixture
def treelint_method_self_5_total_params():
    """Python method with self + 4 real params (should NOT flag: 4 = threshold)."""
    return {
        "results": [
            {
                "name": "update_profile",
                "type": "function",
                "file": "src/services/user_service.py",
                "lines": {"start": 15, "end": 30},
                "signature": "def update_profile(self, user_id, name, email, phone)",
            }
        ]
    }


@pytest.fixture
def treelint_classmethod_cls_6_total_params():
    """Python classmethod with cls + 5 real params (should flag: 5 > 4)."""
    return {
        "results": [
            {
                "name": "from_config",
                "type": "function",
                "file": "src/models/config.py",
                "lines": {"start": 20, "end": 35},
                "signature": "def from_config(cls, host, port, database, user, password)",
            }
        ]
    }


@pytest.fixture
def treelint_classmethod_cls_5_total_params():
    """Python classmethod with cls + 4 real params (should NOT flag: 4 = threshold)."""
    return {
        "results": [
            {
                "name": "create",
                "type": "function",
                "file": "src/models/user.py",
                "lines": {"start": 30, "end": 40},
                "signature": "def create(cls, name, email, role, active)",
            }
        ]
    }


@pytest.fixture
def treelint_function_no_self_5_params():
    """Regular function (no self/cls) with 5 params (should flag: 5 > 4)."""
    return {
        "results": [
            {
                "name": "calculate_total",
                "type": "function",
                "file": "src/utils/calculator.py",
                "lines": {"start": 5, "end": 15},
                "signature": "def calculate_total(price, quantity, tax_rate, discount, shipping)",
            }
        ]
    }


@pytest.fixture
def treelint_method_self_only():
    """Python method with only self parameter (should NOT flag: 0 real params)."""
    return {
        "results": [
            {
                "name": "reset",
                "type": "function",
                "file": "src/models/session.py",
                "lines": {"start": 50, "end": 55},
                "signature": "def reset(self)",
            }
        ]
    }


# =============================================================================
# Implementation imported from shared module (TDD Green phase)
# detect_long_parameter_list, count_effective_parameters imported at top of file
# =============================================================================


# =============================================================================
# Tests: Self/Cls Exclusion Logic
# =============================================================================


class TestSelfExclusion:
    """Tests for Python self parameter exclusion from count (AC#2)."""

    def test_should_exclude_self_from_count_method_with_5_real_params(
        self, treelint_method_self_6_total_params
    ):
        """def method(self, a, b, c, d, e) should count 5 params, not 6."""
        findings = detect_long_parameter_list(
            treelint_method_self_6_total_params, threshold=4
        )
        assert len(findings) == 1
        assert findings[0]["parameter_count"] == 5
        assert "self" not in findings[0]["parameters"]

    def test_should_exclude_self_from_count_method_at_threshold(
        self, treelint_method_self_5_total_params
    ):
        """def method(self, a, b, c, d) should count 4 params (at threshold, not flagged)."""
        findings = detect_long_parameter_list(
            treelint_method_self_5_total_params, threshold=4
        )
        assert len(findings) == 0

    def test_should_exclude_self_only_method(self, treelint_method_self_only):
        """def method(self) should count 0 params (not flagged)."""
        findings = detect_long_parameter_list(
            treelint_method_self_only, threshold=4
        )
        assert len(findings) == 0

    def test_should_not_count_self_as_parameter(self):
        """self should be excluded from effective parameter count."""
        params = ["self", "a", "b", "c", "d", "e"]
        count = count_effective_parameters(params)
        assert count == 5


class TestClsExclusion:
    """Tests for Python cls parameter exclusion from count (AC#2)."""

    def test_should_exclude_cls_from_count_classmethod_with_5_real_params(
        self, treelint_classmethod_cls_6_total_params
    ):
        """def method(cls, a, b, c, d, e) should count 5 params, not 6."""
        findings = detect_long_parameter_list(
            treelint_classmethod_cls_6_total_params, threshold=4
        )
        assert len(findings) == 1
        assert findings[0]["parameter_count"] == 5
        assert "cls" not in findings[0]["parameters"]

    def test_should_exclude_cls_from_count_classmethod_at_threshold(
        self, treelint_classmethod_cls_5_total_params
    ):
        """def method(cls, a, b, c, d) should count 4 params (at threshold, not flagged)."""
        findings = detect_long_parameter_list(
            treelint_classmethod_cls_5_total_params, threshold=4
        )
        assert len(findings) == 0

    def test_should_not_count_cls_as_parameter(self):
        """cls should be excluded from effective parameter count."""
        params = ["cls", "host", "port", "database", "user", "password"]
        count = count_effective_parameters(params)
        assert count == 5


class TestSelfClsOnlyFirstPosition:
    """Tests that self/cls exclusion only applies to first parameter position."""

    def test_should_not_exclude_self_in_non_first_position(self):
        """A parameter named 'self' in non-first position should be counted."""
        params = ["other", "self", "a", "b", "c"]
        count = count_effective_parameters(params)
        # 'self' in second position is not the implicit Python self, so count it
        assert count == 5

    def test_should_not_exclude_cls_in_non_first_position(self):
        """A parameter named 'cls' in non-first position should be counted."""
        params = ["other", "cls", "a", "b", "c"]
        count = count_effective_parameters(params)
        assert count == 5

    def test_should_not_exclude_self_for_regular_function(
        self, treelint_function_no_self_5_params
    ):
        """Regular functions (no self/cls) should count all 5 params."""
        findings = detect_long_parameter_list(
            treelint_function_no_self_5_params, threshold=4
        )
        assert len(findings) == 1
        assert findings[0]["parameter_count"] == 5

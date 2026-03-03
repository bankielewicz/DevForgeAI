"""
Test: AC#2 - Delegation Ratio Calculation
Story: STORY-405
Generated: 2026-02-15

Validates that delegation_ratio = delegation_methods / total_methods is
calculated correctly, and classes with delegation_ratio > 0.80 AND
total_methods >= 3 are flagged as middle men.

Business Rules Tested:
- BR-002: Middle man threshold = delegation_ratio > 0.80
- BR-003: Minimum method count >= 3 (tested jointly with ratio)

These tests will FAIL until the middle man detection logic is
implemented in src/claude/agents/anti-pattern-scanner.md Phase 5.
"""

import os
import sys
import pytest

# Add test directory to path for import
sys.path.insert(0, os.path.dirname(__file__))
from middle_man_detector import (
    calculate_delegation_ratio,
    count_delegation_methods,
    detect_middle_man,
)


# =============================================================================
# Fixtures: Mock Treelint class data with methods of varying body sizes
# =============================================================================


@pytest.fixture
def class_8_methods_7_delegation():
    """Class with 8 methods, 7 delegation (ratio 0.875) - SHOULD be flagged."""
    return {
        "results": [
            {
                "name": "OrderProxy",
                "type": "class",
                "file": "src/services/order_proxy.py",
                "lines": {"start": 5, "end": 60},
                "members": {
                    "methods": [
                        {"name": "get_order", "lines": {"start": 8, "end": 9}},
                        {"name": "create_order", "lines": {"start": 12, "end": 13}},
                        {"name": "update_order", "lines": {"start": 16, "end": 17}},
                        {"name": "delete_order", "lines": {"start": 20, "end": 21}},
                        {"name": "list_orders", "lines": {"start": 24, "end": 25}},
                        {"name": "get_status", "lines": {"start": 28, "end": 29}},
                        {"name": "cancel_order", "lines": {"start": 32, "end": 33}},
                        # This one has orchestration logic (3 lines)
                        {"name": "process_order", "lines": {"start": 36, "end": 39}},
                    ]
                },
            }
        ]
    }


@pytest.fixture
def class_8_methods_6_delegation():
    """Class with 8 methods, 6 delegation (ratio 0.75) - should NOT be flagged."""
    return {
        "results": [
            {
                "name": "ServiceFacade",
                "type": "class",
                "file": "src/services/facade.py",
                "lines": {"start": 5, "end": 80},
                "members": {
                    "methods": [
                        {"name": "get_data", "lines": {"start": 8, "end": 9}},
                        {"name": "set_data", "lines": {"start": 12, "end": 13}},
                        {"name": "validate", "lines": {"start": 16, "end": 17}},
                        {"name": "transform", "lines": {"start": 20, "end": 21}},
                        {"name": "save", "lines": {"start": 24, "end": 25}},
                        {"name": "load", "lines": {"start": 28, "end": 29}},
                        # Two methods with orchestration logic (> 2 lines)
                        {"name": "process", "lines": {"start": 32, "end": 38}},
                        {"name": "execute", "lines": {"start": 42, "end": 48}},
                    ]
                },
            }
        ]
    }


@pytest.fixture
def class_5_methods_5_delegation():
    """Class with 5 methods, all delegation (ratio 1.0) - SHOULD be flagged."""
    return {
        "results": [
            {
                "name": "PureProxy",
                "type": "class",
                "file": "src/services/pure_proxy.py",
                "lines": {"start": 1, "end": 30},
                "members": {
                    "methods": [
                        {"name": "method_a", "lines": {"start": 3, "end": 4}},
                        {"name": "method_b", "lines": {"start": 7, "end": 8}},
                        {"name": "method_c", "lines": {"start": 11, "end": 12}},
                        {"name": "method_d", "lines": {"start": 15, "end": 16}},
                        {"name": "method_e", "lines": {"start": 19, "end": 20}},
                    ]
                },
            }
        ]
    }


@pytest.fixture
def class_3_methods_3_delegation():
    """Class with 3 methods, all delegation (ratio 1.0) - borderline, SHOULD be flagged."""
    return {
        "results": [
            {
                "name": "SmallProxy",
                "type": "class",
                "file": "src/utils/small_proxy.py",
                "lines": {"start": 1, "end": 20},
                "members": {
                    "methods": [
                        {"name": "get", "lines": {"start": 3, "end": 4}},
                        {"name": "set", "lines": {"start": 7, "end": 8}},
                        {"name": "delete", "lines": {"start": 11, "end": 12}},
                    ]
                },
            }
        ]
    }


@pytest.fixture
def class_10_methods_exact_boundary():
    """Class with 10 methods, 8 delegation (ratio 0.80) - exactly AT boundary, NOT flagged."""
    methods = []
    for i in range(8):
        methods.append({"name": f"delegate_{i}", "lines": {"start": 10 + i * 4, "end": 11 + i * 4}})
    # 2 orchestration methods
    methods.append({"name": "orchestrate_a", "lines": {"start": 50, "end": 55}})
    methods.append({"name": "orchestrate_b", "lines": {"start": 60, "end": 65}})

    return {
        "results": [
            {
                "name": "BoundaryClass",
                "type": "class",
                "file": "src/services/boundary.py",
                "lines": {"start": 1, "end": 70},
                "members": {"methods": methods},
            }
        ]
    }


@pytest.fixture
def methods_for_ratio_calc():
    """Standalone method list for ratio calculation tests."""
    return [
        {"name": "m1", "lines": {"start": 1, "end": 2}},   # delegation (1 line)
        {"name": "m2", "lines": {"start": 5, "end": 6}},   # delegation (1 line)
        {"name": "m3", "lines": {"start": 9, "end": 11}},  # delegation (2 lines)
        {"name": "m4", "lines": {"start": 14, "end": 20}},  # NOT delegation (6 lines)
    ]


# =============================================================================
# Tests: Delegation Ratio Calculation (BR-002)
# =============================================================================


class TestDelegationRatioCalculation:
    """Tests for delegation_ratio = delegation_methods / total_methods."""

    def test_should_calculate_ratio_3_of_4(self, methods_for_ratio_calc):
        """3 delegation methods out of 4 total should give ratio 0.75."""
        ratio = calculate_delegation_ratio(methods_for_ratio_calc)
        assert ratio == pytest.approx(0.75), (
            f"Expected ratio 0.75 (3/4), got {ratio}"
        )

    def test_should_calculate_ratio_all_delegation(self):
        """All methods being delegation should give ratio 1.0."""
        methods = [
            {"name": "m1", "lines": {"start": 1, "end": 2}},
            {"name": "m2", "lines": {"start": 5, "end": 6}},
            {"name": "m3", "lines": {"start": 9, "end": 10}},
        ]
        ratio = calculate_delegation_ratio(methods)
        assert ratio == pytest.approx(1.0), (
            f"Expected ratio 1.0 (all delegation), got {ratio}"
        )

    def test_should_calculate_ratio_no_delegation(self):
        """No delegation methods should give ratio 0.0."""
        methods = [
            {"name": "m1", "lines": {"start": 1, "end": 10}},
            {"name": "m2", "lines": {"start": 15, "end": 25}},
            {"name": "m3", "lines": {"start": 30, "end": 40}},
        ]
        ratio = calculate_delegation_ratio(methods)
        assert ratio == pytest.approx(0.0), (
            f"Expected ratio 0.0 (no delegation), got {ratio}"
        )

    def test_should_return_zero_for_empty_methods(self):
        """Empty methods list should return ratio 0.0."""
        ratio = calculate_delegation_ratio([])
        assert ratio == pytest.approx(0.0), (
            f"Expected ratio 0.0 for empty methods, got {ratio}"
        )

    def test_should_calculate_ratio_7_of_8(self):
        """7 delegation out of 8 total should give ratio 0.875 (BR-002 example)."""
        methods = [
            {"name": f"d{i}", "lines": {"start": i * 4, "end": i * 4 + 1}}
            for i in range(7)
        ]
        methods.append({"name": "complex", "lines": {"start": 50, "end": 55}})
        ratio = calculate_delegation_ratio(methods)
        assert ratio == pytest.approx(0.875), (
            f"Expected ratio 0.875 (7/8), got {ratio}"
        )


# =============================================================================
# Tests: Delegation Method Counting
# =============================================================================


class TestDelegationMethodCounting:
    """Tests for counting delegation methods in a class."""

    def test_should_count_3_delegation_methods(self, methods_for_ratio_calc):
        """3 of 4 methods with body <= 2 should yield count 3."""
        count = count_delegation_methods(methods_for_ratio_calc)
        assert count == 3, f"Expected 3 delegation methods, got {count}"

    def test_should_count_zero_for_empty_list(self):
        """Empty method list should yield count 0."""
        count = count_delegation_methods([])
        assert count == 0, f"Expected 0 delegation methods, got {count}"

    def test_should_count_all_when_all_short(self):
        """All methods with body <= 2 should all be counted."""
        methods = [
            {"name": f"m{i}", "lines": {"start": i * 3, "end": i * 3 + 1}}
            for i in range(5)
        ]
        count = count_delegation_methods(methods)
        assert count == 5, f"Expected 5 delegation methods, got {count}"


# =============================================================================
# Tests: Middle Man Detection with Threshold (BR-002)
# =============================================================================


class TestMiddleManDetection:
    """Tests for middle man detection combining ratio and threshold."""

    def test_should_flag_class_with_ratio_above_080(
        self, class_8_methods_7_delegation
    ):
        """Class with ratio 0.875 (> 0.80) and 8 methods should be flagged."""
        findings = detect_middle_man(class_8_methods_7_delegation)
        assert len(findings) == 1, (
            f"Expected 1 finding for ratio 0.875, got {len(findings)}"
        )
        assert findings[0]["class_name"] == "OrderProxy"
        assert findings[0]["delegation_ratio"] == pytest.approx(0.875)

    def test_should_not_flag_class_with_ratio_075(
        self, class_8_methods_6_delegation
    ):
        """Class with ratio 0.75 (< 0.80) should NOT be flagged."""
        findings = detect_middle_man(class_8_methods_6_delegation)
        assert len(findings) == 0, (
            f"Expected 0 findings for ratio 0.75, got {len(findings)}"
        )

    def test_should_flag_pure_proxy_ratio_100(
        self, class_5_methods_5_delegation
    ):
        """Class with ratio 1.0 (all delegation) should be flagged."""
        findings = detect_middle_man(class_5_methods_5_delegation)
        assert len(findings) == 1
        assert findings[0]["delegation_ratio"] == pytest.approx(1.0)

    def test_should_not_flag_class_at_exact_boundary_080(
        self, class_10_methods_exact_boundary
    ):
        """Class with ratio exactly 0.80 should NOT be flagged (> 0.80 required)."""
        findings = detect_middle_man(class_10_methods_exact_boundary)
        assert len(findings) == 0, (
            "Ratio 0.80 is AT boundary; threshold is '> 0.80', so should NOT flag"
        )

    def test_should_include_correct_total_methods_in_finding(
        self, class_8_methods_7_delegation
    ):
        """Finding must include correct total_methods count."""
        findings = detect_middle_man(class_8_methods_7_delegation)
        assert findings[0]["total_methods"] == 8

    def test_should_include_correct_delegating_methods_in_finding(
        self, class_8_methods_7_delegation
    ):
        """Finding must include correct delegating_methods count."""
        findings = detect_middle_man(class_8_methods_7_delegation)
        assert findings[0]["delegating_methods"] == 7

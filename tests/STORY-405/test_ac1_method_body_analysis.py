"""
Test: AC#1 - Treelint-Based Method Body Analysis
Story: STORY-405
Generated: 2026-02-15

Validates that method body sizes are calculated as (lines.end - lines.start),
and methods with body size <= 2 are classified as delegation methods.

Business Rules Tested:
- BR-001: Delegation method = body size <= 2 lines
- BR-004: Facade classes with complex orchestration (>2 lines) are NOT middle men

These tests will FAIL until the middle man detection logic is
implemented in src/claude/agents/anti-pattern-scanner.md Phase 5.
"""

import os
import sys
import pytest

# Add test directory to path for import
sys.path.insert(0, os.path.dirname(__file__))
from middle_man_detector import (
    calculate_method_body_size,
    is_delegation_method,
)


# =============================================================================
# Fixtures: Mock Treelint method data for body size analysis
# =============================================================================


@pytest.fixture
def method_1_line_body():
    """Method with 1-line body (single delegation call): lines 10-11."""
    return {
        "name": "get_name",
        "lines": {"start": 10, "end": 11},
    }


@pytest.fixture
def method_2_line_body():
    """Method with 2-line body (delegation + return): lines 20-22."""
    return {
        "name": "get_value",
        "lines": {"start": 20, "end": 22},
    }


@pytest.fixture
def method_3_line_body():
    """Method with 3-line body (orchestration logic): lines 30-33."""
    return {
        "name": "process_data",
        "lines": {"start": 30, "end": 33},
    }


@pytest.fixture
def method_5_line_body():
    """Method with 5-line body (complex orchestration): lines 40-45."""
    return {
        "name": "orchestrate_workflow",
        "lines": {"start": 40, "end": 45},
    }


@pytest.fixture
def method_0_line_body():
    """Method with 0-line body (edge case: start == end): lines 50-50."""
    return {
        "name": "empty_method",
        "lines": {"start": 50, "end": 50},
    }


@pytest.fixture
def method_missing_lines():
    """Method with no lines data (edge case)."""
    return {
        "name": "unknown_method",
    }


# =============================================================================
# Tests: Method Body Size Calculation (BR-001)
# =============================================================================


class TestMethodBodySizeCalculation:
    """Tests for calculating method body size from Treelint lines data."""

    def test_should_calculate_body_size_1_line(self, method_1_line_body):
        """Body size for lines 10-11 should be 1 (11 - 10 = 1)."""
        size = calculate_method_body_size(method_1_line_body)
        assert size == 1, f"Expected body_size=1, got {size}"

    def test_should_calculate_body_size_2_lines(self, method_2_line_body):
        """Body size for lines 20-22 should be 2 (22 - 20 = 2)."""
        size = calculate_method_body_size(method_2_line_body)
        assert size == 2, f"Expected body_size=2, got {size}"

    def test_should_calculate_body_size_3_lines(self, method_3_line_body):
        """Body size for lines 30-33 should be 3 (33 - 30 = 3)."""
        size = calculate_method_body_size(method_3_line_body)
        assert size == 3, f"Expected body_size=3, got {size}"

    def test_should_calculate_body_size_5_lines(self, method_5_line_body):
        """Body size for lines 40-45 should be 5 (45 - 40 = 5)."""
        size = calculate_method_body_size(method_5_line_body)
        assert size == 5, f"Expected body_size=5, got {size}"

    def test_should_handle_zero_body_size(self, method_0_line_body):
        """Body size for lines 50-50 should be 0 (50 - 50 = 0)."""
        size = calculate_method_body_size(method_0_line_body)
        assert size == 0, f"Expected body_size=0, got {size}"

    def test_should_return_negative_1_when_lines_missing(self, method_missing_lines):
        """Missing lines data should return -1 (skip this method)."""
        size = calculate_method_body_size(method_missing_lines)
        assert size == -1, (
            "Expected body_size=-1 for missing lines data "
            "(method should be skipped in analysis)"
        )


# =============================================================================
# Tests: Delegation Method Classification (BR-001, BR-004)
# =============================================================================


class TestDelegationMethodClassification:
    """Tests for classifying methods as delegation vs orchestration."""

    def test_should_classify_1_line_as_delegation(self, method_1_line_body):
        """1-line body (<= 2) should be classified as delegation method."""
        result = is_delegation_method(method_1_line_body)
        assert result is True, (
            "1-line method should be classified as delegation (BR-001)"
        )

    def test_should_classify_2_line_as_delegation(self, method_2_line_body):
        """2-line body (<= 2) should be classified as delegation method."""
        result = is_delegation_method(method_2_line_body)
        assert result is True, (
            "2-line method should be classified as delegation (BR-001)"
        )

    def test_should_not_classify_3_line_as_delegation(self, method_3_line_body):
        """3-line body (> 2) should NOT be classified as delegation (BR-004)."""
        result = is_delegation_method(method_3_line_body)
        assert result is False, (
            "3-line method indicates orchestration, not delegation (BR-004)"
        )

    def test_should_not_classify_5_line_as_delegation(self, method_5_line_body):
        """5-line body (> 2) should NOT be classified as delegation (BR-004)."""
        result = is_delegation_method(method_5_line_body)
        assert result is False, (
            "5-line method indicates complex orchestration (BR-004)"
        )

    def test_should_classify_0_line_as_delegation(self, method_0_line_body):
        """0-line body (<= 2) should be classified as delegation."""
        result = is_delegation_method(method_0_line_body)
        assert result is True, (
            "0-line method (empty/abstract) should be classified as delegation"
        )

    def test_should_not_classify_when_lines_missing(self, method_missing_lines):
        """Missing lines data should return False (cannot determine)."""
        result = is_delegation_method(method_missing_lines)
        assert result is False, (
            "Method with missing lines data should not be classified as delegation"
        )

    def test_should_respect_custom_body_size_threshold(self, method_3_line_body):
        """Custom max_body_size=3 should classify 3-line method as delegation."""
        result = is_delegation_method(method_3_line_body, max_body_size=3)
        assert result is True, (
            "With max_body_size=3, a 3-line method should be delegation"
        )

"""
Test: AC#3 - Minimum Method Threshold
Story: STORY-405
Generated: 2026-02-15

Validates that classes with fewer than 3 methods are NOT flagged as middle
men, regardless of their delegation ratio. This prevents false positives
on small utility classes.

Business Rules Tested:
- BR-003: Minimum method count >= 3

These tests will FAIL until the minimum method threshold logic is
implemented in src/claude/agents/anti-pattern-scanner.md Phase 5.
"""

import os
import sys
import pytest

# Add test directory to path for import
sys.path.insert(0, os.path.dirname(__file__))
from middle_man_detector import detect_middle_man


# =============================================================================
# Fixtures: Classes below minimum method threshold
# =============================================================================


@pytest.fixture
def class_2_methods_all_delegation():
    """Class with 2 methods, both delegation (ratio 1.0) - should NOT be flagged."""
    return {
        "results": [
            {
                "name": "TinyProxy",
                "type": "class",
                "file": "src/utils/tiny_proxy.py",
                "lines": {"start": 1, "end": 15},
                "members": {
                    "methods": [
                        {"name": "get", "lines": {"start": 3, "end": 4}},
                        {"name": "set", "lines": {"start": 7, "end": 8}},
                    ]
                },
            }
        ]
    }


@pytest.fixture
def class_1_method_delegation():
    """Class with 1 method, delegation (ratio 1.0) - should NOT be flagged."""
    return {
        "results": [
            {
                "name": "SingleMethodProxy",
                "type": "class",
                "file": "src/utils/single_method.py",
                "lines": {"start": 1, "end": 8},
                "members": {
                    "methods": [
                        {"name": "execute", "lines": {"start": 3, "end": 4}},
                    ]
                },
            }
        ]
    }


@pytest.fixture
def class_0_methods():
    """Class with 0 methods - should NOT be flagged."""
    return {
        "results": [
            {
                "name": "EmptyClass",
                "type": "class",
                "file": "src/utils/empty.py",
                "lines": {"start": 1, "end": 3},
                "members": {
                    "methods": []
                },
            }
        ]
    }


@pytest.fixture
def class_3_methods_all_delegation():
    """Class with 3 methods, all delegation (ratio 1.0) - SHOULD be flagged (meets minimum)."""
    return {
        "results": [
            {
                "name": "MinimumProxy",
                "type": "class",
                "file": "src/services/minimum_proxy.py",
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
def multiple_classes_mixed_sizes():
    """Multiple classes: one below threshold, one above - only above should be flagged."""
    return {
        "results": [
            {
                "name": "SmallUtil",
                "type": "class",
                "file": "src/utils/small.py",
                "lines": {"start": 1, "end": 10},
                "members": {
                    "methods": [
                        {"name": "a", "lines": {"start": 3, "end": 4}},
                        {"name": "b", "lines": {"start": 7, "end": 8}},
                    ]
                },
            },
            {
                "name": "LargeProxy",
                "type": "class",
                "file": "src/services/large_proxy.py",
                "lines": {"start": 1, "end": 40},
                "members": {
                    "methods": [
                        {"name": "m1", "lines": {"start": 3, "end": 4}},
                        {"name": "m2", "lines": {"start": 7, "end": 8}},
                        {"name": "m3", "lines": {"start": 11, "end": 12}},
                        {"name": "m4", "lines": {"start": 15, "end": 16}},
                    ]
                },
            },
        ]
    }


# =============================================================================
# Tests: Minimum Method Threshold Enforcement (BR-003)
# =============================================================================


class TestMinimumMethodThreshold:
    """Tests that classes with < 3 methods are never flagged."""

    def test_should_not_flag_class_with_2_methods(self, class_2_methods_all_delegation):
        """2-method class with 100% delegation should NOT be flagged (BR-003)."""
        findings = detect_middle_man(class_2_methods_all_delegation)
        assert len(findings) == 0, (
            "Class with 2 methods must not be flagged regardless of delegation ratio. "
            "BR-003: Minimum method count >= 3"
        )

    def test_should_not_flag_class_with_1_method(self, class_1_method_delegation):
        """1-method class should NOT be flagged (BR-003)."""
        findings = detect_middle_man(class_1_method_delegation)
        assert len(findings) == 0, (
            "Class with 1 method must not be flagged. BR-003: min_methods >= 3"
        )

    def test_should_not_flag_class_with_0_methods(self, class_0_methods):
        """0-method class should NOT be flagged (BR-003)."""
        findings = detect_middle_man(class_0_methods)
        assert len(findings) == 0, (
            "Class with 0 methods must not be flagged. BR-003: min_methods >= 3"
        )

    def test_should_flag_class_with_exactly_3_methods(
        self, class_3_methods_all_delegation
    ):
        """3-method class with 100% delegation SHOULD be flagged (meets minimum)."""
        findings = detect_middle_man(class_3_methods_all_delegation)
        assert len(findings) == 1, (
            "Class with 3 methods and 100% delegation should be flagged. "
            "3 >= min_methods (3)"
        )

    def test_should_only_flag_class_above_threshold_in_batch(
        self, multiple_classes_mixed_sizes
    ):
        """Only classes with >= 3 methods and high delegation should be flagged."""
        findings = detect_middle_man(multiple_classes_mixed_sizes)
        assert len(findings) == 1, (
            f"Expected only LargeProxy (4 methods) to be flagged, got {len(findings)} findings"
        )
        assert findings[0]["class_name"] == "LargeProxy"

    def test_should_respect_custom_min_methods_threshold(
        self, class_2_methods_all_delegation
    ):
        """Custom min_methods=2 should allow 2-method classes to be flagged."""
        findings = detect_middle_man(
            class_2_methods_all_delegation, min_methods=2
        )
        assert len(findings) == 1, (
            "With min_methods=2, a 2-method class with 100% delegation should be flagged"
        )

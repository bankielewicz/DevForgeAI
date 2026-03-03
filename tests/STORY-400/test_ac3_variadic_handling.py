"""
Test: AC#3 - Variadic Parameter Handling
Story: STORY-400
Generated: 2026-02-14

Validates that *args and **kwargs are NOT counted as individual parameters
when detecting long parameter lists.

These tests will FAIL until the variadic parameter exclusion logic is
implemented in the anti-pattern-scanner Phase 5.
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
# Fixtures: Mock Treelint output for functions with variadic parameters
# =============================================================================


@pytest.fixture
def treelint_func_with_args_kwargs_2_real_params():
    """Function with 2 real params + *args + **kwargs (should NOT flag: 2 < 4)."""
    return {
        "results": [
            {
                "name": "flexible_func",
                "type": "function",
                "file": "src/utils/helpers.py",
                "lines": {"start": 10, "end": 20},
                "signature": "def flexible_func(a, b, *args, **kwargs)",
            }
        ]
    }


@pytest.fixture
def treelint_func_with_args_5_real_params():
    """Function with 5 real params + *args (should flag: 5 > 4)."""
    return {
        "results": [
            {
                "name": "overloaded_func",
                "type": "function",
                "file": "src/services/handler.py",
                "lines": {"start": 15, "end": 30},
                "signature": "def overloaded_func(a, b, c, d, e, *args)",
            }
        ]
    }


@pytest.fixture
def treelint_func_with_kwargs_only():
    """Function with only **kwargs (should NOT flag: 0 real params)."""
    return {
        "results": [
            {
                "name": "config_func",
                "type": "function",
                "file": "src/config.py",
                "lines": {"start": 5, "end": 10},
                "signature": "def config_func(**kwargs)",
            }
        ]
    }


@pytest.fixture
def treelint_func_with_args_only():
    """Function with only *args (should NOT flag: 0 real params)."""
    return {
        "results": [
            {
                "name": "variadic_func",
                "type": "function",
                "file": "src/utils/misc.py",
                "lines": {"start": 1, "end": 5},
                "signature": "def variadic_func(*args)",
            }
        ]
    }


@pytest.fixture
def treelint_method_self_args_kwargs_4_real_params():
    """Method with self + 4 real params + *args + **kwargs (should NOT flag: 4 = threshold)."""
    return {
        "results": [
            {
                "name": "execute",
                "type": "function",
                "file": "src/services/executor.py",
                "lines": {"start": 25, "end": 45},
                "signature": "def execute(self, action, target, mode, timeout, *args, **kwargs)",
            }
        ]
    }


@pytest.fixture
def treelint_method_self_args_kwargs_5_real_params():
    """Method with self + 5 real params + **kwargs (should flag: 5 > 4)."""
    return {
        "results": [
            {
                "name": "configure",
                "type": "function",
                "file": "src/services/config_service.py",
                "lines": {"start": 30, "end": 50},
                "signature": "def configure(self, host, port, database, user, password, **kwargs)",
            }
        ]
    }


# =============================================================================
# Implementation imported from shared module (TDD Green phase)
# detect_long_parameter_list, count_effective_parameters imported at top of file
# =============================================================================


# =============================================================================
# Tests: Variadic Parameter Exclusion
# =============================================================================


class TestArgsExclusion:
    """Tests for *args exclusion from parameter count (AC#3)."""

    def test_should_not_count_args_as_parameter(self):
        """*args should be excluded from effective parameter count."""
        params = ["a", "b", "*args"]
        count = count_effective_parameters(params)
        assert count == 2

    def test_should_not_flag_func_with_args_kwargs_below_threshold(
        self, treelint_func_with_args_kwargs_2_real_params
    ):
        """def func(a, b, *args, **kwargs) counts 2 real params (not flagged)."""
        findings = detect_long_parameter_list(
            treelint_func_with_args_kwargs_2_real_params, threshold=4
        )
        assert len(findings) == 0

    def test_should_flag_func_with_args_above_threshold(
        self, treelint_func_with_args_5_real_params
    ):
        """def func(a, b, c, d, e, *args) counts 5 real params (flagged)."""
        findings = detect_long_parameter_list(
            treelint_func_with_args_5_real_params, threshold=4
        )
        assert len(findings) == 1
        assert findings[0]["parameter_count"] == 5

    def test_should_not_flag_args_only_function(
        self, treelint_func_with_args_only
    ):
        """def func(*args) counts 0 real params (not flagged)."""
        findings = detect_long_parameter_list(
            treelint_func_with_args_only, threshold=4
        )
        assert len(findings) == 0


class TestKwargsExclusion:
    """Tests for **kwargs exclusion from parameter count (AC#3)."""

    def test_should_not_count_kwargs_as_parameter(self):
        """**kwargs should be excluded from effective parameter count."""
        params = ["a", "b", "**kwargs"]
        count = count_effective_parameters(params)
        assert count == 2

    def test_should_not_flag_kwargs_only_function(
        self, treelint_func_with_kwargs_only
    ):
        """def func(**kwargs) counts 0 real params (not flagged)."""
        findings = detect_long_parameter_list(
            treelint_func_with_kwargs_only, threshold=4
        )
        assert len(findings) == 0


class TestCombinedExclusions:
    """Tests for combined self/cls + *args/**kwargs exclusion (AC#2 + AC#3)."""

    def test_should_exclude_self_and_args_and_kwargs(self):
        """self, *args, **kwargs all excluded from count."""
        params = ["self", "a", "b", "c", "d", "*args", "**kwargs"]
        count = count_effective_parameters(params)
        assert count == 4

    def test_should_not_flag_method_with_self_args_kwargs_at_threshold(
        self, treelint_method_self_args_kwargs_4_real_params
    ):
        """def method(self, a, b, c, d, *args, **kwargs) counts 4 real params (not flagged)."""
        findings = detect_long_parameter_list(
            treelint_method_self_args_kwargs_4_real_params, threshold=4
        )
        assert len(findings) == 0

    def test_should_flag_method_with_self_kwargs_above_threshold(
        self, treelint_method_self_args_kwargs_5_real_params
    ):
        """def method(self, a, b, c, d, e, **kwargs) counts 5 real params (flagged)."""
        findings = detect_long_parameter_list(
            treelint_method_self_args_kwargs_5_real_params, threshold=4
        )
        assert len(findings) == 1
        assert findings[0]["parameter_count"] == 5
        assert "self" not in findings[0]["parameters"]
        assert "**kwargs" not in findings[0]["parameters"]

    def test_should_exclude_custom_star_params(self):
        """Parameters like *extra or **options should also be excluded."""
        params = ["a", "b", "c", "*extra", "**options"]
        count = count_effective_parameters(params)
        assert count == 3

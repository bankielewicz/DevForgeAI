"""
Test: AC#4 - Grep Fallback for Unsupported Languages
Story: STORY-400
Generated: 2026-02-14

Validates that Grep patterns detecting 5+ commas in function signatures
are used for languages not supported by Treelint (C#, Java, Go).

These tests will FAIL until the Grep fallback logic is implemented
in the anti-pattern-scanner Phase 5.
"""

import os
import re
import sys
import pytest

# Add test directory to path for import (directory has hyphen, not valid Python module name)
sys.path.insert(0, os.path.dirname(__file__))
from long_parameter_list_detector import (
    get_long_param_grep_pattern,
    detect_long_parameter_list_grep,
    should_use_grep_fallback,
)


# =============================================================================
# Fixtures: Sample code snippets for unsupported languages
# =============================================================================


@pytest.fixture
def csharp_method_5_params():
    """C# method with 5 parameters (violation)."""
    return """
public class OrderService
{
    public void ProcessOrder(int customerId, int productId, int quantity, decimal discount, string shippingMethod)
    {
        // implementation
    }
}
"""


@pytest.fixture
def csharp_method_4_params():
    """C# method with 4 parameters (no violation)."""
    return """
public class UserService
{
    public void UpdateProfile(int userId, string name, string email, string phone)
    {
        // implementation
    }
}
"""


@pytest.fixture
def java_method_6_params():
    """Java method with 6 parameters (violation)."""
    return """
public class NotificationService {
    public void sendNotification(String userId, String channel, String subject, String body, int priority, int retryCount) {
        // implementation
    }
}
"""


@pytest.fixture
def java_method_3_params():
    """Java method with 3 parameters (no violation)."""
    return """
public class AuthService {
    public boolean authenticate(String username, String password, String token) {
        return true;
    }
}
"""


@pytest.fixture
def go_function_5_params():
    """Go function with 5 parameters (violation)."""
    return """
func ProcessOrder(customerID int, productID int, quantity int, discount float64, shippingMethod string) error {
    return nil
}
"""


@pytest.fixture
def go_function_4_params():
    """Go function with 4 parameters (no violation)."""
    return """
func UpdateProfile(userID int, name string, email string, phone string) error {
    return nil
}
"""


# =============================================================================
# Implementation imported from shared module (TDD Green phase)
# get_long_param_grep_pattern, detect_long_parameter_list_grep,
# should_use_grep_fallback imported at top of file
# =============================================================================


# =============================================================================
# Tests: Grep Fallback Activation
# =============================================================================


class TestGrepFallbackActivation:
    """Tests for when Grep fallback should be activated (AC#4)."""

    def test_should_use_grep_for_csharp(self):
        """C# files should use Grep fallback (not supported by Treelint)."""
        assert should_use_grep_fallback("csharp", treelint_exit_code=0) is True

    def test_should_use_grep_for_java(self):
        """Java files should use Grep fallback (not supported by Treelint)."""
        assert should_use_grep_fallback("java", treelint_exit_code=0) is True

    def test_should_use_grep_for_go(self):
        """Go files should use Grep fallback (not supported by Treelint)."""
        assert should_use_grep_fallback("go", treelint_exit_code=0) is True

    def test_should_not_use_grep_for_python(self):
        """Python files should NOT use Grep fallback (supported by Treelint)."""
        assert should_use_grep_fallback("python", treelint_exit_code=0) is False

    def test_should_not_use_grep_for_typescript(self):
        """TypeScript files should NOT use Grep fallback."""
        assert should_use_grep_fallback("typescript", treelint_exit_code=0) is False

    def test_should_use_grep_when_treelint_not_found(self):
        """Exit code 127 (binary not found) should trigger Grep fallback."""
        assert should_use_grep_fallback("python", treelint_exit_code=127) is True

    def test_should_use_grep_when_treelint_permission_denied(self):
        """Exit code 126 (permission denied) should trigger Grep fallback."""
        assert should_use_grep_fallback("python", treelint_exit_code=126) is True

    def test_should_not_fallback_on_treelint_exit_0(self):
        """Exit code 0 for supported language should NOT trigger fallback."""
        assert should_use_grep_fallback("python", treelint_exit_code=0) is False


# =============================================================================
# Tests: Grep Pattern for 5+ Parameters
# =============================================================================


class TestGrepPatternDetection:
    """Tests for Grep pattern detecting 5+ parameter signatures (AC#4)."""

    def test_should_detect_csharp_method_with_5_params(self, csharp_method_5_params):
        """Grep should detect C# method with 5 parameters."""
        findings = detect_long_parameter_list_grep(
            csharp_method_5_params, "src/OrderService.cs", "csharp"
        )
        assert len(findings) == 1
        assert findings[0]["function_name"] == "ProcessOrder"

    def test_should_not_detect_csharp_method_with_4_params(self, csharp_method_4_params):
        """Grep should NOT detect C# method with 4 parameters."""
        findings = detect_long_parameter_list_grep(
            csharp_method_4_params, "src/UserService.cs", "csharp"
        )
        assert len(findings) == 0

    def test_should_detect_java_method_with_6_params(self, java_method_6_params):
        """Grep should detect Java method with 6 parameters."""
        findings = detect_long_parameter_list_grep(
            java_method_6_params, "src/NotificationService.java", "java"
        )
        assert len(findings) == 1
        assert findings[0]["parameter_count"] >= 5

    def test_should_not_detect_java_method_with_3_params(self, java_method_3_params):
        """Grep should NOT detect Java method with 3 parameters."""
        findings = detect_long_parameter_list_grep(
            java_method_3_params, "src/AuthService.java", "java"
        )
        assert len(findings) == 0

    def test_should_detect_go_function_with_5_params(self, go_function_5_params):
        """Grep should detect Go function with 5 parameters."""
        findings = detect_long_parameter_list_grep(
            go_function_5_params, "src/order.go", "go"
        )
        assert len(findings) == 1

    def test_should_not_detect_go_function_with_4_params(self, go_function_4_params):
        """Grep should NOT detect Go function with 4 parameters."""
        findings = detect_long_parameter_list_grep(
            go_function_4_params, "src/user.go", "go"
        )
        assert len(findings) == 0


class TestGrepPatternFormat:
    """Tests for the Grep regex pattern format (AC#4)."""

    def test_grep_pattern_should_match_5_comma_signatures(self):
        """Pattern should match signatures with 4+ commas (5+ parameters)."""
        pattern = get_long_param_grep_pattern()
        # A signature with 5 parameters has 4 commas
        test_sig = "def func(a, b, c, d, e)"
        assert re.search(pattern, test_sig) is not None

    def test_grep_pattern_should_not_match_4_comma_signatures(self):
        """Pattern should NOT match signatures with 3 commas (4 parameters)."""
        pattern = get_long_param_grep_pattern()
        test_sig = "def func(a, b, c, d)"
        assert re.search(pattern, test_sig) is None

    def test_grep_pattern_should_match_many_comma_signatures(self):
        """Pattern should match signatures with many parameters."""
        pattern = get_long_param_grep_pattern()
        test_sig = "def func(a, b, c, d, e, f, g, h)"
        assert re.search(pattern, test_sig) is not None


class TestGrepFallbackGracefulDegradation:
    """Tests for graceful degradation when Treelint is unavailable."""

    def test_should_complete_scan_when_treelint_binary_missing(self):
        """Scanner should complete using Grep when Treelint binary is not found."""
        # Simulates Treelint exit code 127 (command not found)
        fallback_needed = should_use_grep_fallback("python", treelint_exit_code=127)
        assert fallback_needed is True

    def test_should_not_halt_on_treelint_unavailable(self):
        """Scanner must NOT HALT when Treelint is unavailable - use Grep instead."""
        # This validates the NFR-002 requirement: graceful degradation
        fallback_needed = should_use_grep_fallback("python", treelint_exit_code=127)
        assert fallback_needed is True
        # Scanner should continue with Grep fallback, not raise/halt

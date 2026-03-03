"""
Test: AC#4 - Grep Fallback for Unsupported Languages
Story: STORY-405
Generated: 2026-02-15

Validates that when Treelint is unavailable or the language is unsupported
(C#, Java, Go), Grep-based method detection with line counting is used
as a fallback for middle man detection.

These tests will FAIL until the Grep fallback logic is implemented in
src/claude/agents/anti-pattern-scanner.md Phase 5.
"""

import os
import sys
import pytest

# Add test directory to path for import
sys.path.insert(0, os.path.dirname(__file__))
from middle_man_detector import (
    detect_middle_man_grep,
    should_use_grep_fallback,
)


# =============================================================================
# Fixtures: Source code samples for Grep fallback testing
# =============================================================================


@pytest.fixture
def csharp_middle_man_class():
    """C# class with mostly single-line delegation methods."""
    return """
using System;

public class OrderProxy
{
    private readonly IOrderService _service;

    public OrderProxy(IOrderService service)
    {
        _service = service;
    }

    public Order GetOrder(int id) => _service.GetOrder(id);

    public void CreateOrder(Order order) => _service.CreateOrder(order);

    public void UpdateOrder(Order order) => _service.UpdateOrder(order);

    public void DeleteOrder(int id) => _service.DeleteOrder(id);

    public List<Order> ListOrders() => _service.ListOrders();
}
"""


@pytest.fixture
def java_middle_man_class():
    """Java class with mostly single-line delegation methods."""
    return """
package com.example.services;

public class UserProxy {
    private final UserService service;

    public UserProxy(UserService service) {
        this.service = service;
    }

    public User getUser(int id) { return service.getUser(id); }

    public void createUser(User user) { service.createUser(user); }

    public void deleteUser(int id) { service.deleteUser(id); }

    public List<User> listUsers() { return service.listUsers(); }
}
"""


@pytest.fixture
def go_middle_man_struct():
    """Go struct with mostly single-line delegation methods."""
    return """
package services

type OrderProxy struct {
    service OrderService
}

func (p *OrderProxy) GetOrder(id int) Order {
    return p.service.GetOrder(id)
}

func (p *OrderProxy) CreateOrder(order Order) error {
    return p.service.CreateOrder(order)
}

func (p *OrderProxy) DeleteOrder(id int) error {
    return p.service.DeleteOrder(id)
}

func (p *OrderProxy) ListOrders() []Order {
    return p.service.ListOrders()
}
"""


@pytest.fixture
def csharp_non_middle_man_class():
    """C# class with substantial method bodies (not a middle man)."""
    return """
public class OrderService
{
    public Order ProcessOrder(int id)
    {
        var order = _repository.GetById(id);
        ValidateOrder(order);
        ApplyDiscounts(order);
        CalculateTax(order);
        return order;
    }

    public void ValidateOrder(Order order)
    {
        if (order == null) throw new ArgumentNullException(nameof(order));
        if (order.Items.Count == 0) throw new InvalidOperationException("Empty order");
        foreach (var item in order.Items)
        {
            ValidateItem(item);
        }
    }

    public decimal CalculateTotal(Order order)
    {
        var subtotal = order.Items.Sum(i => i.Price * i.Quantity);
        var tax = subtotal * 0.1m;
        var discount = GetDiscount(order);
        return subtotal + tax - discount;
    }
}
"""


# =============================================================================
# Tests: Grep Fallback Decision Logic
# =============================================================================


class TestGrepFallbackDecision:
    """Tests for should_use_grep_fallback() decision logic."""

    def test_should_use_fallback_for_csharp(self):
        """C# is unsupported by Treelint, should use Grep fallback."""
        result = should_use_grep_fallback("csharp", treelint_exit_code=0)
        assert result is True, "C# should trigger Grep fallback"

    def test_should_use_fallback_for_java(self):
        """Java is unsupported by Treelint, should use Grep fallback."""
        result = should_use_grep_fallback("java", treelint_exit_code=0)
        assert result is True, "Java should trigger Grep fallback"

    def test_should_use_fallback_for_go(self):
        """Go is unsupported by Treelint, should use Grep fallback."""
        result = should_use_grep_fallback("go", treelint_exit_code=0)
        assert result is True, "Go should trigger Grep fallback"

    def test_should_not_use_fallback_for_python(self):
        """Python is supported by Treelint, should NOT use Grep fallback."""
        result = should_use_grep_fallback("python", treelint_exit_code=0)
        assert result is False, "Python should use Treelint (supported)"

    def test_should_not_use_fallback_for_typescript(self):
        """TypeScript is supported by Treelint, should NOT use Grep fallback."""
        result = should_use_grep_fallback("typescript", treelint_exit_code=0)
        assert result is False, "TypeScript should use Treelint (supported)"

    def test_should_use_fallback_when_treelint_exit_127(self):
        """Treelint exit code 127 (not found) should trigger fallback."""
        result = should_use_grep_fallback("python", treelint_exit_code=127)
        assert result is True, "Exit code 127 (binary not found) should trigger fallback"

    def test_should_use_fallback_when_treelint_exit_126(self):
        """Treelint exit code 126 (permission denied) should trigger fallback."""
        result = should_use_grep_fallback("python", treelint_exit_code=126)
        assert result is True, "Exit code 126 (permission denied) should trigger fallback"


# =============================================================================
# Tests: Grep-Based Middle Man Detection
# =============================================================================


class TestGrepMiddleManDetection:
    """Tests for Grep-based middle man detection on unsupported languages."""

    def test_should_detect_csharp_middle_man(self, csharp_middle_man_class):
        """Should detect C# middle man class via Grep fallback."""
        findings = detect_middle_man_grep(
            csharp_middle_man_class,
            file_path="src/Services/OrderProxy.cs",
            language="csharp",
        )
        assert len(findings) >= 1, (
            "C# middle man class with 5 delegation methods should be detected via Grep"
        )

    def test_should_detect_java_middle_man(self, java_middle_man_class):
        """Should detect Java middle man class via Grep fallback."""
        findings = detect_middle_man_grep(
            java_middle_man_class,
            file_path="src/services/UserProxy.java",
            language="java",
        )
        assert len(findings) >= 1, (
            "Java middle man class with 4 delegation methods should be detected via Grep"
        )

    def test_should_detect_go_middle_man(self, go_middle_man_struct):
        """Should detect Go middle man struct via Grep fallback."""
        findings = detect_middle_man_grep(
            go_middle_man_struct,
            file_path="services/order_proxy.go",
            language="go",
        )
        assert len(findings) >= 1, (
            "Go middle man struct with 4 delegation methods should be detected via Grep"
        )

    def test_should_not_detect_non_middle_man_csharp(self, csharp_non_middle_man_class):
        """C# class with substantial method bodies should NOT be detected."""
        findings = detect_middle_man_grep(
            csharp_non_middle_man_class,
            file_path="src/Services/OrderService.cs",
            language="csharp",
        )
        assert len(findings) == 0, (
            "C# class with complex methods should NOT be flagged as middle man"
        )

    def test_should_return_empty_for_unsupported_grep_language(self):
        """Unknown language should return empty findings list."""
        findings = detect_middle_man_grep(
            "some code", file_path="file.rs", language="rust"
        )
        assert findings == [], (
            "Unsupported language in Grep fallback should return empty list"
        )

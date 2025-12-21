"""
Test Fixture: Nested Conditionals Vulnerable Pattern (Python)

This file contains deeply nested conditionals (4+ levels).
Expected detections: >=1 violation for AP-006
Rule ID: AP-006
Severity: MEDIUM (info)
"""


def deeply_nested_logic(user, order, payment, shipping):
    """VULNERABLE: 4+ levels of nested conditionals."""
    if user:
        if user.is_active:
            if order:
                if order.is_valid:
                    if payment:
                        if payment.is_approved:
                            if shipping:
                                if shipping.is_available:
                                    # Level 8 - extremely deep nesting
                                    return "Order processed successfully"
                                else:
                                    return "Shipping not available"
                            else:
                                return "No shipping info"
                        else:
                            return "Payment not approved"
                    else:
                        return "No payment info"
                else:
                    return "Invalid order"
            else:
                return "No order"
        else:
            return "User not active"
    else:
        return "No user"


def another_nested_example(a, b, c, d, e):
    """VULNERABLE: Multiple levels of mixed nesting."""
    if a > 0:
        if b > 0:
            if c > 0:
                if d > 0:
                    # 4th level - triggers detection
                    return a + b + c + d + e
    return 0

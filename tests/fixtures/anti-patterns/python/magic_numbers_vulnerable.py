"""
Test Fixture: Magic Numbers Vulnerable Patterns (Python)

This file contains hardcoded numeric literals that should be named constants.
Expected detections: >=3 violations for AP-004
Rule ID: AP-004
Severity: MEDIUM (info)
"""


def calculate_discount(quantity, price):
    """Calculate discount with magic numbers."""
    if quantity > 50:  # VULNERABLE: Magic number 50
        discount_rate = 0.15  # VULNERABLE: Magic number 0.15
    elif quantity > 25:  # VULNERABLE: Magic number 25
        discount_rate = 0.10  # VULNERABLE: Magic number 0.10
    else:
        discount_rate = 0.0

    return price * (1 - discount_rate)


def set_timeout():
    """Set timeout with magic number."""
    timeout = 30000  # VULNERABLE: Magic number 30000
    max_retries = 5  # VULNERABLE: Magic number 5
    return timeout, max_retries


def calculate_price():
    """Calculate price with magic number."""
    base_price = 29.99  # VULNERABLE: Magic number 29.99
    tax_rate = 0.0825  # VULNERABLE: Magic number 0.0825
    return base_price * (1 + tax_rate)

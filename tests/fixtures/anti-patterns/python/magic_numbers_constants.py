"""
Test Fixture: Magic Numbers as Named Constants (Python)

This file uses named constants instead of magic numbers.
Expected detections: 0 violations (named constants are acceptable)
Rule ID: AP-004
Severity: N/A (should not trigger for named constants)
"""

# Named constants at module level - SAFE pattern
MAX_QUANTITY = 50
BULK_DISCOUNT_RATE = 0.15
STANDARD_DISCOUNT_RATE = 0.10
TIMEOUT_MS = 30000
MAX_RETRIES = 5
BASE_PRICE = 29.99
TAX_RATE = 0.0825


def calculate_discount(quantity, price):
    """Calculate discount using named constants."""
    if quantity > MAX_QUANTITY:  # SAFE: Uses constant
        discount_rate = BULK_DISCOUNT_RATE  # SAFE: Uses constant
    else:
        discount_rate = STANDARD_DISCOUNT_RATE  # SAFE: Uses constant

    return price * (1 - discount_rate)


def set_timeout():
    """Set timeout using named constants."""
    timeout = TIMEOUT_MS  # SAFE: Uses constant
    max_retries = MAX_RETRIES  # SAFE: Uses constant
    return timeout, max_retries

"""
Test Fixture: Magic Numbers Allowlist (Python)

This file contains allowlisted numeric values (0, 1, -1, 100, 1000).
Expected detections: 0 violations (allowlisted values)
Rule ID: AP-004
Severity: N/A (should not trigger for allowlisted values)
"""


def check_boundaries(value):
    """Check value boundaries using allowlisted numbers."""
    if value == 0:  # SAFE: 0 is allowlisted
        return "zero"
    elif value == 1:  # SAFE: 1 is allowlisted
        return "one"
    elif value == -1:  # SAFE: -1 is allowlisted
        return "negative one"
    elif value == 100:  # SAFE: 100 is allowlisted
        return "hundred"
    elif value == 1000:  # SAFE: 1000 is allowlisted
        return "thousand"
    return "other"


def initialize_defaults():
    """Initialize with common default values."""
    count = 0  # SAFE: 0 is allowlisted
    index = -1  # SAFE: -1 is allowlisted
    percentage = 100  # SAFE: 100 is allowlisted
    return count, index, percentage

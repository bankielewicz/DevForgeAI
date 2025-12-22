"""
Test Fixture: Console Log / Print Vulnerable Patterns (Python)

This file contains print() statements that should be caught in production code.
Expected detections: >=3 violations for AP-003
Rule ID: AP-003
Severity: MEDIUM (info)
"""


def process_user_data(user):
    """Process user data with debug prints."""
    print("Processing user:", user)  # VULNERABLE: Debug print

    if not user.get("email"):
        print("Warning: User has no email")  # VULNERABLE: Should use logging

    result = transform_user(user)
    print(f"Transformed result: {result}")  # VULNERABLE: Debug print

    return result


def transform_user(user):
    """Transform user data."""
    return {"id": user.get("id"), "name": user.get("name")}

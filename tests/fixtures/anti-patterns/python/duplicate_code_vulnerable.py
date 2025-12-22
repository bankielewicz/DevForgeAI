"""
Test Fixture: Duplicate Code Vulnerable Pattern (Python)

This file contains repeated code blocks that should be extracted.
Expected detections: >=1 violation for AP-009
Rule ID: AP-009
Severity: HIGH (warning)
"""


def process_user_a(user):
    """VULNERABLE: This code block is duplicated in process_user_b."""
    # Duplicated block starts here
    if not user:
        raise ValueError("User is required")

    user_id = user.get("id")
    username = user.get("username")
    email = user.get("email")

    if not user_id:
        raise ValueError("User ID is required")

    if not username:
        raise ValueError("Username is required")

    if not email:
        raise ValueError("Email is required")

    validated_user = {
        "id": user_id,
        "username": username.lower(),
        "email": email.lower(),
    }
    # Duplicated block ends here

    return validated_user


def process_user_b(user):
    """VULNERABLE: This code block is duplicated from process_user_a."""
    # Duplicated block starts here
    if not user:
        raise ValueError("User is required")

    user_id = user.get("id")
    username = user.get("username")
    email = user.get("email")

    if not user_id:
        raise ValueError("User ID is required")

    if not username:
        raise ValueError("Username is required")

    if not email:
        raise ValueError("Email is required")

    validated_user = {
        "id": user_id,
        "username": username.lower(),
        "email": email.lower(),
    }
    # Duplicated block ends here

    return validated_user

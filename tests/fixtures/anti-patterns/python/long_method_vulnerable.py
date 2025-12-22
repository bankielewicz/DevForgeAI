"""
Test Fixture: Long Method Vulnerable Pattern (Python)

This file contains a method with 60+ lines - too long.
Expected detections: >=1 violation for AP-005
Rule ID: AP-005
Severity: MEDIUM (info)
"""


def very_long_processing_method(data):
    """VULNERABLE: Method with 60+ lines of sequential operations."""
    # Step 1: Initialize
    result = {}
    errors = []
    warnings = []

    # Step 2: Validate input
    if not data:
        errors.append("Data is empty")
        return None

    if not isinstance(data, dict):
        errors.append("Data must be dictionary")
        return None

    # Step 3: Extract fields
    user_id = data.get("user_id")
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    first_name = data.get("first_name")
    last_name = data.get("last_name")

    # Step 4: Validate fields
    if not user_id:
        errors.append("Missing user_id")

    if not username:
        errors.append("Missing username")
    elif len(username) < 3:
        errors.append("Username too short")

    if not email:
        errors.append("Missing email")
    elif "@" not in email:
        errors.append("Invalid email format")

    if not password:
        errors.append("Missing password")
    elif len(password) < 8:
        errors.append("Password too short")

    # Step 5: Process first name
    if first_name:
        first_name = first_name.strip()
        first_name = first_name.title()
    else:
        warnings.append("No first name provided")

    # Step 6: Process last name
    if last_name:
        last_name = last_name.strip()
        last_name = last_name.title()
    else:
        warnings.append("No last name provided")

    # Step 7: Check for errors
    if errors:
        result["status"] = "error"
        result["errors"] = errors
        result["warnings"] = warnings
        return result

    # Step 8: Build result
    result["user_id"] = user_id
    result["username"] = username.lower()
    result["email"] = email.lower()
    result["first_name"] = first_name
    result["last_name"] = last_name
    result["full_name"] = f"{first_name} {last_name}"
    result["status"] = "success"
    result["warnings"] = warnings

    # Step 9: Additional processing
    result["display_name"] = username
    result["email_verified"] = False
    result["created_at"] = "now"
    result["updated_at"] = "now"

    # Step 10: Return result
    return result

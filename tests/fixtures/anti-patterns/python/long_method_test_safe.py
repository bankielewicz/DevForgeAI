"""
Test Fixture: Long Test Method (Python)

This is a TEST file - long test methods are sometimes acceptable.
Expected detections: 0 violations (test methods excluded)
Rule ID: AP-005
Severity: N/A (should not trigger in test methods)
"""


def test_comprehensive_user_registration():
    """SAFE: Long test method with extensive assertions."""
    # Arrange - setup test data
    user_data = {
        "user_id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "password": "securepassword123",
        "first_name": "Test",
        "last_name": "User",
    }

    # Act - perform operations
    result = process_registration(user_data)

    # Assert - verify all fields
    assert result is not None
    assert result["status"] == "success"
    assert result["user_id"] == 1
    assert result["username"] == "testuser"
    assert result["email"] == "test@example.com"
    assert result["first_name"] == "Test"
    assert result["last_name"] == "User"
    assert result["full_name"] == "Test User"
    assert result["email_verified"] is False
    assert "created_at" in result
    assert "updated_at" in result

    # Additional assertions
    assert len(result["warnings"]) == 0
    assert "errors" not in result or len(result["errors"]) == 0


def process_registration(data):
    """Helper function for test."""
    return {
        "status": "success",
        "user_id": data["user_id"],
        "username": data["username"],
        "email": data["email"],
        "first_name": data["first_name"],
        "last_name": data["last_name"],
        "full_name": f"{data['first_name']} {data['last_name']}",
        "email_verified": False,
        "created_at": "now",
        "updated_at": "now",
        "warnings": [],
    }

"""
Test Fixture: Console Log in Test File (Python)

This is a TEST file - print statements in tests are acceptable.
Expected detections: 0 violations (test file exclusion)
Rule ID: AP-003
Severity: N/A (should not trigger in test files)

Note: Test file exclusion is typically handled at scan-level, not rule-level.
"""


def test_user_processing():
    """Test user processing with debug output."""
    user = {"id": 1, "name": "Test User"}

    print("Setting up test data")  # SAFE: In test file
    result = {"processed": True}
    print(f"Test result: {result}")  # SAFE: In test file

    assert result["processed"] is True

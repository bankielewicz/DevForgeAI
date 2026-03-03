"""
Test Fixture: Well-Designed Small Class (Python)

This class follows Single Responsibility Principle with focused methods.
Expected detections: 0 violations (no false positives)
Rule ID: AP-001
Severity: N/A (should not trigger)
"""


class UserRepository:
    """SAFE: Small, focused class with single responsibility."""

    def __init__(self, database):
        self.database = database

    def find_by_id(self, user_id):
        """Find user by ID."""
        return self.database.query(f"SELECT * FROM users WHERE id = ?", [user_id])

    def save(self, user):
        """Save user to database."""
        return self.database.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            [user.name, user.email]
        )

    def delete(self, user_id):
        """Delete user by ID."""
        return self.database.execute("DELETE FROM users WHERE id = ?", [user_id])

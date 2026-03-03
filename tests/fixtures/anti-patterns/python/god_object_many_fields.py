"""
Test Fixture: God Object with Many Fields (Python)

This class has too many fields (20+) which indicates a god object anti-pattern.
Expected detections: >=1 violation for AP-001
Rule ID: AP-001
Severity: HIGH (warning)
"""


class GodObjectManyFields:
    """VULNERABLE: Class with 20+ fields - data clump smell."""

    def __init__(self):
        # User data
        self.user_id = None
        self.username = None
        self.email = None
        self.password_hash = None
        self.first_name = None
        self.last_name = None

        # Address data
        self.street_address = None
        self.city = None
        self.state = None
        self.zip_code = None
        self.country = None

        # Account data
        self.account_status = None
        self.created_at = None
        self.updated_at = None
        self.last_login = None

        # Preferences
        self.theme = None
        self.language = None
        self.timezone = None
        self.notifications_enabled = None
        self.email_notifications = None

    def save(self):
        """Save all fields."""
        pass

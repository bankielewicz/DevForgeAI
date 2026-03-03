"""Test fixture: Contains hardcoded secrets for detection testing."""


# BAD: Hardcoded API key
API_KEY = "sk-abc123xyz789def456ghi"

# BAD: Hardcoded password
DATABASE_PASSWORD = "SuperSecretPassword123!"

# BAD: Hardcoded connection string with credentials
CONNECTION_STRING = "postgresql://admin:password123@localhost:5432/mydb"


class Config:
    """Configuration with hardcoded secrets."""

    # BAD: Hardcoded AWS credentials
    AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
    AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

    # BAD: Hardcoded JWT secret
    JWT_SECRET = "my-super-secret-jwt-key-12345"


def get_api_key() -> str:
    """Returns hardcoded API key (bad practice)."""
    return "ghp_1234567890abcdefghijklmnopqrstuvwxyz"

"""
Test Fixture: Hardcoded Secrets Safe Patterns (Python)

This file contains SAFE secret management patterns that should NOT trigger false positives
for SEC-003 rule.

Expected detections: 0 violations (no false positives)
Rule ID: SEC-003
Severity: CRITICAL
"""

import os
from typing import Optional


# Safe Pattern 1: Environment variable for API key
def send_request_with_env_key():
    """SAFE: API key from environment variable"""
    import requests

    # SAFE - os.getenv() reads from environment
    api_key = os.getenv("API_KEY")

    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get("https://api.example.com/data", headers=headers)

    return response.json()


# Safe Pattern 2: Environment variable for database password
def connect_to_database_safe():
    """SAFE: Database password from environment"""
    import psycopg2

    # SAFE - all credentials from environment
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    return conn


# Safe Pattern 3: Configuration file loading
def load_aws_credentials():
    """SAFE: AWS credentials from config file"""
    import boto3

    # SAFE - boto3 reads from ~/.aws/credentials
    s3_client = boto3.client('s3')

    return s3_client


# Safe Pattern 4: Secrets manager integration
def get_jwt_secret() -> str:
    """SAFE: JWT secret from secrets manager"""

    # SAFE - reads from external secrets manager
    secret_name = "prod/jwt/secret"
    jwt_secret = os.getenv("JWT_SECRET") or fetch_from_secrets_manager(secret_name)

    return jwt_secret


def fetch_from_secrets_manager(secret_name: str) -> Optional[str]:
    """SAFE: Abstraction for secrets manager"""
    # Implementation would use AWS Secrets Manager, Azure Key Vault, etc.
    pass


# Safe Pattern 5: Vault integration
class ConfigLoader:
    """SAFE: Configuration from HashiCorp Vault"""

    def __init__(self):
        # SAFE - reads from Vault
        self.vault_url = os.getenv("VAULT_ADDR")
        self.vault_token = os.getenv("VAULT_TOKEN")

    def get_encryption_key(self) -> bytes:
        """SAFE: Encryption key from Vault"""
        # SAFE - retrieves key from Vault, not hardcoded
        key = self._fetch_from_vault("secret/encryption/key")
        return key.encode()

    def _fetch_from_vault(self, path: str) -> str:
        """SAFE: Vault API integration"""
        # Implementation would call Vault API
        pass


# Safe Pattern 6: OAuth credentials from environment
class OAuthClientSafe:
    """SAFE: OAuth credentials from environment"""

    def __init__(self):
        # SAFE - environment variables
        self.client_id = os.getenv("OAUTH_CLIENT_ID")
        self.client_secret = os.getenv("OAUTH_CLIENT_SECRET")


# Safe Pattern 7: String constants that aren't secrets
DEFAULT_MESSAGE = "Hello, World!"
APP_NAME = "MyApplication"
VERSION = "1.0.0"


# Safe Pattern 8: Configuration template (placeholders)
DATABASE_URL_TEMPLATE = "postgresql://{user}:{password}@{host}:{port}/{database}"


def build_connection_string():
    """SAFE: Build connection string from environment"""

    # SAFE - placeholders filled from environment
    return DATABASE_URL_TEMPLATE.format(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB_NAME")
    )

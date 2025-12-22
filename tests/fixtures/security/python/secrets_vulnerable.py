"""
Test Fixture: Hardcoded Secrets Vulnerable Patterns (Python)

This file contains 6+ hardcoded secret patterns that MUST be detected by
SEC-003 rule (devforgeai/ast-grep/rules/python/security/hardcoded-secrets.yml).

Expected detections: ≥6 violations
Rule ID: SEC-003
Severity: CRITICAL
"""


# Pattern 1: Hardcoded API key
API_KEY = "sk-1234567890abcdef1234567890abcdef"


def send_request_with_hardcoded_key():
    """VULNERABLE: Hardcoded API key"""
    import requests

    # SEC-003 should detect hardcoded API key
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get("https://api.example.com/data", headers=headers)

    return response.json()


# Pattern 2: Hardcoded password
def connect_to_database():
    """VULNERABLE: Hardcoded database password"""
    import psycopg2

    # SEC-003 should detect hardcoded password
    conn = psycopg2.connect(
        host="localhost",
        database="mydb",
        user="admin",
        password="SuperSecret123!"  # CRITICAL: Hardcoded password
    )

    return conn


# Pattern 3: Hardcoded connection string with password
DATABASE_URL = "postgresql://admin:P@ssw0rd123@localhost:5432/production_db"


# Pattern 4: Hardcoded AWS access keys
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"


def upload_to_s3():
    """VULNERABLE: Hardcoded AWS credentials"""
    import boto3

    # SEC-003 should detect hardcoded AWS keys
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

    return s3_client


# Pattern 5: Hardcoded JWT secret
JWT_SECRET = "my-super-secret-jwt-key-do-not-share"


def create_token(user_id: int):
    """VULNERABLE: Hardcoded JWT secret"""
    import jwt

    # SEC-003 should detect hardcoded JWT secret
    payload = {"user_id": user_id}
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

    return token


# Pattern 6: Hardcoded encryption key
ENCRYPTION_KEY = b"sixteen byte key"


def encrypt_data(plaintext: str):
    """VULNERABLE: Hardcoded encryption key"""
    from cryptography.fernet import Fernet
    import base64

    # SEC-003 should detect hardcoded encryption key
    key = base64.urlsafe_b64encode(ENCRYPTION_KEY.ljust(32)[:32])
    cipher = Fernet(key)

    encrypted = cipher.encrypt(plaintext.encode())
    return encrypted


# Pattern 7: Hardcoded private key (partial example)
PRIVATE_KEY = """
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA1234567890abcdefghijklmnopqrstuvwxyz...
-----END RSA PRIVATE KEY-----
"""


# Pattern 8: Hardcoded OAuth client secret
class OAuthClient:
    """VULNERABLE: Hardcoded OAuth credentials"""

    def __init__(self):
        # SEC-003 should detect these
        self.client_id = "1234567890.apps.googleusercontent.com"
        self.client_secret = "GOCSPX-abcdefghijklmnopqrstuvw"

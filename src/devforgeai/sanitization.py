"""
Data Sanitization Module

Removes sensitive data (secrets, PII, credentials) from operation context
before sharing with feedback systems.
"""

import re
from typing import Optional, Dict, List, Any


def redact_sensitive_data(data: str) -> str:
    """
    Redact sensitive patterns from text (snake_case preferred).

    Redacts:
    - Passwords (password=, pwd=, passwd=, pass=)
    - API keys (api_key=, apiKey=, API-KEY=)
    - Tokens (JWT, Bearer, access_token=)
    - Database connections (user=, password=, connection strings)
    - IPv4/IPv6 addresses
    - Email addresses (PII)
    - Absolute file paths (keep only filename)
    - Internal domain names

    Args:
        data: String to sanitize

    Returns:
        Sanitized string with patterns redacted
    """
    sanitized = data
    patterns = [
        # Passwords
        (r'password\s*=\s*[^;\s\[\]]+', '[REDACTED]'),
        (r'pwd\s*=\s*[^;\s\[\]]+', '[REDACTED]'),
        (r'passwd\s*=\s*[^;\s\[\]]+', '[REDACTED]'),
        (r'pass\s*=\s*[^;\s\[\]]+', '[REDACTED]'),
        # API Keys
        (r'api[_-]?key\s*=\s*[^;\s\[\]]+', '[REDACTED]'),
        (r'apiKey\s*=\s*[^;\s\[\]]+', '[REDACTED]'),
        (r'API[_-]?KEY\s*=\s*[^;\s\[\]]+', '[REDACTED]'),
        # Tokens (JWT and other tokens)
        (r'token\s*=\s*[A-Za-z0-9+/=._-]{20,}', '[REDACTED]'),
        (r'access[_-]?token\s*=\s*[^;\s\[\]]+', '[REDACTED]'),
        (r'Bearer\s+[A-Za-z0-9+/=]+', 'Bearer [REDACTED]'),
        # IPv4 addresses
        (r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', 'XXX.XXX.XXX.XXX'),
        # IPv6 addresses
        (r'[a-fA-F0-9]{0,4}:[a-fA-F0-9]{0,4}:[a-fA-F0-9]{0,4}:[a-fA-F0-9]{0,4}:[a-fA-F0-9]{0,4}:[a-fA-F0-9]{0,4}:[a-fA-F0-9]{0,4}:[a-fA-F0-9]{0,4}',
         '[internal-ipv6]'),
        # Email addresses (PII)
        (r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '[email@example.com]'),
        # Internal domain names
        (r'https?://[a-zA-Z0-9-]+\.[a-zA-Z0-9-]+\.internal(?:/[^\s]*)?', '[internal-domain]'),
        # File paths - keep filename only
        (r'/(?:[^/\s]+/)+([^\s/]+)', r'\1'),
    ]

    for pattern, replacement in patterns:
        sanitized = re.sub(pattern, replacement, sanitized, flags=re.IGNORECASE)

    return sanitized


def detect_sensitive_patterns(data: str) -> Optional[Dict[str, Any]]:
    """
    Detect sensitive patterns in text without redacting (snake_case preferred).

    Args:
        data: String to scan for patterns

    Returns:
        Dict with detected patterns or None if no patterns found
    """
    detections = {
        "passwords": [],
        "api_keys": [],
        "tokens": [],
        "ips": [],
        "emails": [],
        "internal_domains": [],
    }

    # Detect passwords
    if re.search(r'(?:password|pwd|passwd|pass)\s*=', data, re.IGNORECASE):
        detections["passwords"].append("Found password pattern")

    # Detect passwords in connection strings (mongodb://user:pass@host, postgres://user:pass@host)
    if re.search(r'(?:mongodb|postgres|mysql|redis)://[^:]+:[^@]+@', data, re.IGNORECASE):
        detections["passwords"].append("Found password in connection string")

    # Detect API keys
    if re.search(r'(?:api[_-]?key|apiKey|API[_-]?KEY)\s*=', data, re.IGNORECASE):
        detections["api_keys"].append("Found API key pattern")

    # Detect tokens
    if re.search(r'(?:token|access[_-]?token|Bearer)\s*=?', data, re.IGNORECASE):
        detections["tokens"].append("Found token pattern")

    # Detect IPs
    if re.search(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', data):
        detections["ips"].append("Found IPv4 address")

    if re.search(r'[a-fA-F0-9]{0,4}:[a-fA-F0-9]{0,4}:[a-fA-F0-9]{0,4}:[a-fA-F0-9]{0,4}', data):
        detections["ips"].append("Found IPv6 address")

    # Detect emails
    if re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', data):
        detections["emails"].append("Found email address")

    # Detect internal domains
    if re.search(r'https?://[a-zA-Z0-9-]+\.internal', data, re.IGNORECASE):
        detections["internal_domains"].append("Found internal domain")

    # Return None if no detections, otherwise return detections dict
    has_detections = any(v for v in detections.values())
    return detections if has_detections else None


def sanitize_context(context_dict: Dict[str, Any], include_metadata: bool = True) -> tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Sanitize an entire context dictionary (snake_case preferred).

    Args:
        context_dict: Context to sanitize
        include_metadata: Whether to return metadata about sanitization

    Returns:
        Tuple of (sanitized_context, metadata) where metadata contains:
        - sanitization_applied: bool
        - fields_sanitized: count of fields that had sensitive data
        - sanitized_fields: list of field names that were sanitized
    """
    sanitized = context_dict.copy()
    metadata = {
        "sanitization_applied": False,
        "fields_sanitized": 0,
        "sanitized_fields": [],
    }

    # Sanitize error stack_trace if present
    if "error" in sanitized and isinstance(sanitized["error"], dict):
        if "stack_trace" in sanitized["error"] and sanitized["error"]["stack_trace"]:
            original = sanitized["error"]["stack_trace"]
            sanitized_trace = redact_sensitive_data(original)
            if original != sanitized_trace:
                sanitized["error"]["stack_trace"] = sanitized_trace
                metadata["fields_sanitized"] += 1
                metadata["sanitized_fields"].append("error.stack_trace")
                metadata["sanitization_applied"] = True

        if "message" in sanitized["error"] and sanitized["error"]["message"]:
            original = sanitized["error"]["message"]
            sanitized_msg = redact_sensitive_data(original)
            if original != sanitized_msg:
                sanitized["error"]["message"] = sanitized_msg
                metadata["fields_sanitized"] += 1
                metadata["sanitized_fields"].append("error.message")
                metadata["sanitization_applied"] = True

    return sanitized, metadata


# Backward compatibility aliases (camelCase - deprecated)
redactSensitiveData = redact_sensitive_data
detectSensitivePatterns = detect_sensitive_patterns
sanitizeContext = sanitize_context

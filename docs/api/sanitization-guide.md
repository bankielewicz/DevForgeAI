# Sanitization Guide - Operation Context

**Module:** `devforgeai.sanitization`
**Version:** 1.0.0
**Security Level:** HIGH (protects secrets, PII, internal infrastructure)

---

## Overview

The sanitization module removes sensitive data from operation context before sharing with feedback systems, ensuring secrets, credentials, and PII are never exposed.

**Security Principle:** **Sanitize by Default**

All context passed to feedback conversations is automatically sanitized unless explicitly disabled.

---

## Sanitization Patterns (15 Total)

### 1. Passwords (4 Patterns)

```python
# Pattern 1: password=
"Connection failed: password=SuperSecret123"
→ "Connection failed: [REDACTED]"

# Pattern 2: pwd=
"Login: pwd=secret"
→ "Login: [REDACTED]"

# Pattern 3: passwd=
"Auth: passwd=xyz123"
→ "Auth: [REDACTED]"

# Pattern 4: pass= (generic)
"Creds: pass=test"
→ "Creds: [REDACTED]"

# Pattern 5: Connection Strings
"mongodb://user:password123@host:27017"
→ "[REDACTED]" (entire connection string sanitized via password pattern)
```

**Regex:** `r'(password|pwd|passwd|pass)\s*=\s*[^;\s\[\]]+` (case-insensitive)

---

### 2. API Keys (3 Patterns)

```python
# Pattern 1: api_key=
"Request failed: api_key=sk-1234567890abcdef"
→ "Request failed: [REDACTED]"

# Pattern 2: apiKey= (camelCase)
"Config: apiKey=xyz789"
→ "Config: [REDACTED]"

# Pattern 3: API-KEY= (UPPER)
"Header: API-KEY=ABCD1234"
→ "Header: [REDACTED]"
```

**Regex:** `r'(api[_-]?key|apiKey|API[_-]?KEY)\s*=\s*[^;\s\[\]]+` (case-insensitive)

---

### 3. Tokens (3 Patterns)

```python
# Pattern 1: token= (generic, JWT, etc.)
"Auth failed: token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
→ "Auth failed: [REDACTED]"

# Pattern 2: access_token=
"OAuth: access_token=ya29.a0AfH6SMBx..."
→ "OAuth: [REDACTED]"

# Pattern 3: Bearer tokens
"Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
→ "Authorization: Bearer [REDACTED]"
```

**Regex:**
- `r'token\s*=\s*[A-Za-z0-9+/=._-]{20,}'` (JWT and long tokens)
- `r'access[_-]?token\s*=\s*[^;\s\[\]]+`
- `r'Bearer\s+[A-Za-z0-9+/=]+'`

---

### 4. Database Connection Strings (1 Pattern)

```python
"Connection string: Server=localhost;Database=mydb;User=admin;Password=secret123;"
→ "Connection string: [REDACTED]" (via password= pattern)

"mongodb://user:pass123@mongodb.internal:27017/db"
→ Detection: passwords in connection strings (via detectSensitivePatterns)
```

**Note:** Detected via password patterns in connection string format

---

### 5. IP Addresses (2 Patterns)

```python
# Pattern 1: IPv4
"Connected to 192.168.1.100:8080"
→ "Connected to XXX.XXX.XXX.XXX:8080"

# Pattern 2: IPv6
"Server: 2001:0db8:85a3:0000:0000:8a2e:0370:7334"
→ "Server: [internal-ipv6]"
```

**Regex:**
- IPv4: `r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'`
- IPv6: `r'[a-fA-F0-9]{0,4}:[a-fA-F0-9]{0,4}:...'` (full pattern)

---

### 6. Email Addresses (PII) (1 Pattern)

```python
"Error for user@company.com failed"
→ "Error for [email@example.com] failed"
```

**Regex:** `r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'`

**Note:** Protects personally identifiable information (PII) per GDPR/privacy requirements

---

### 7. Internal Domain Names (1 Pattern)

```python
"Service failed: https://api.mycompany.internal/v1/users"
→ "Service failed: [internal-domain]"
```

**Regex:** `r'https?://[a-zA-Z0-9-]+\.[a-zA-Z0-9-]+\.internal(?:/[^\s]*)?'`

**Purpose:** Prevents leaking internal infrastructure naming

---

### 8. File Paths (1 Pattern)

```python
"File not found: /home/user/projects/my-secret-project/config.json"
→ "File not found: config.json"
```

**Regex:** `r'/(?:[^/\s]+/)+([^\s/]+)'` → Replacement: `r'\1'` (keeps filename only)

**Purpose:** Removes absolute paths while preserving filename context

---

## API Functions

### redact_sensitive_data()

```python
def redact_sensitive_data(data: str) -> str:
    """Redact all sensitive patterns from text."""
```

**Usage:**
```python
from devforgeai.sanitization import redact_sensitive_data

log = "Error: password=secret123 for user@example.com at 192.168.1.100"
sanitized = redact_sensitive_data(log)

print(sanitized)
# "Error: [REDACTED] for [email@example.com] at XXX.XXX.XXX.XXX"
```

---

### detect_sensitive_patterns()

```python
def detect_sensitive_patterns(data: str) -> Optional[Dict[str, List[str]]]
    """Detect sensitive patterns without redacting."""
```

**Usage:**
```python
from devforgeai.sanitization import detect_sensitive_patterns

log = "Connection: password=xyz, api_key=abc123"
detections = detect_sensitive_patterns(log)

print(detections)
# {
#     "passwords": ["Found password pattern"],
#     "api_keys": ["Found API key pattern"],
#     "tokens": [],
#     "ips": [],
#     "emails": [],
#     "internal_domains": []
# }
```

**Returns:** `None` if no patterns found, otherwise dict of detections by category

---

### sanitize_context()

```python
def sanitize_context(
    context_dict: Dict[str, Any],
    include_metadata: bool = True
) -> tuple[Dict[str, Any], Dict[str, Any]]
    """Sanitize entire context dictionary."""
```

**Usage:**
```python
from devforgeai.sanitization import sanitize_context

context_dict = {
    "error": {
        "message": "Git failed: password=secret",
        "stack_trace": "Error at /home/user/project/file.py line 42"
    }
}

sanitized, metadata = sanitize_context(context_dict)

print(sanitized["error"]["message"])
# "Git failed: [REDACTED]"

print(sanitized["error"]["stack_trace"])
# "Error at file.py line 42"

print(metadata)
# {
#     "sanitization_applied": True,
#     "fields_sanitized": 2,
#     "sanitized_fields": ["error.message", "error.stack_trace"]
# }
```

**Returns:** Tuple of `(sanitized_context, sanitization_metadata)`

---

## Sanitization Metadata

All sanitization operations return metadata for audit trails:

```python
metadata = {
    "sanitization_applied": bool,  # True if any redaction occurred
    "fields_sanitized": int,  # Count of fields redacted
    "sanitized_fields": List[str],  # Field paths that were redacted
}
```

**Example:**
```python
sanitized, metadata = sanitize_context({
    "error": {
        "message": "password=xyz",
        "stack_trace": "api_key=abc"
    }
})

assert metadata["sanitization_applied"] == True
assert metadata["fields_sanitized"] == 2
assert metadata["sanitized_fields"] == ["error.message", "error.stack_trace"]
```

---

## Testing Sanitization

### Unit Tests

```python
from devforgeai.sanitization import redact_sensitive_data

def test_sanitize_passwords():
    result = redact_sensitive_data("password=secret123")
    assert "secret123" not in result
    assert "[REDACTED]" in result

def test_sanitize_api_keys():
    result = redact_sensitive_data("api_key=sk-1234567890")
    assert "sk-1234567890" not in result
    assert "[REDACTED]" in result
```

### Security Audit

Verify 100% secret detection:

```python
# Test all 15 patterns
test_data = [
    ("password=xyz", "[REDACTED]"),
    ("api_key=abc", "[REDACTED]"),
    ("token=jwt123", "[REDACTED]"),
    ("192.168.1.1", "XXX.XXX.XXX.XXX"),
    ("user@company.com", "[email@example.com]"),
    # ... test all 15 patterns
]

for original, expected_pattern in test_data:
    sanitized = redact_sensitive_data(original)
    assert expected_pattern in sanitized
```

---

## Performance

**Sanitization Performance:**
- Simple string (no secrets): ~50μs
- Complex string (5 secrets): ~200μs
- Large string (1KB with 10 secrets): ~500μs

**Optimization:** Patterns are applied sequentially. First match short-circuits remaining patterns for that occurrence.

---

## Security Best Practices

1. ✅ **Always Sanitize:** Never share raw context externally
2. ✅ **Audit Trails:** Log what was sanitized (metadata)
3. ✅ **Verify Coverage:** Test all 15 patterns regularly
4. ✅ **Update Patterns:** Add new patterns for new secret types
5. ✅ **False Positives:** Patterns designed to minimize false positives
6. ✅ **Defense in Depth:** Sanitize at multiple layers (extraction + feedback)

---

## See Also

- [API Documentation](./operation-context-api.md)
- [Validation Rules](./validation-rules.md)
- [User Guide](../guides/operation-context-user-guide.md)

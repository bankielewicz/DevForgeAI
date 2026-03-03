---
name: security-auditor-owasp-patterns
description: OWASP Top 10 vulnerability detection patterns with Grep patterns and secure code examples
version: "1.0"
status: Reference (loaded on demand)
---

# OWASP Top 10 Security Check Patterns

**Version**: 1.0
**Purpose**: Detailed Grep patterns and secure code examples for each OWASP Top 10 category.

---

## 1. Injection (A03:2021)

### SQL Injection

```javascript
// VULNERABLE: SQL injection via string concatenation
const query = `SELECT * FROM users WHERE id = ${userId}`;

// SECURE: Parameterized query
const query = 'SELECT * FROM users WHERE id = ?';
db.query(query, [userId]);
```

**Grep Patterns:**
```
Grep(pattern="SELECT.*\\$|INSERT.*\\$|UPDATE.*\\$|DELETE.*\\$", glob="**/*.{js,py,cs}")
```

### Command Injection

```python
# VULNERABLE: Command injection
os.system(f"ping {user_input}")

# SECURE: Use safe subprocess
subprocess.run(["ping", user_input], check=True)
```

---

## 2. Broken Authentication (A07:2021)

### Password Requirements

```javascript
// SECURE: Strong password policy
const MIN_PASSWORD_LENGTH = 12;
const requireUppercase = true;
const requireLowercase = true;
const requireDigits = true;
const requireSpecialChars = true;
```

### Session Management

```javascript
// SECURE: Session configuration
{
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: false,
  cookie: {
    secure: true,
    httpOnly: true,
    maxAge: 3600000,
    sameSite: 'strict'
  }
}
```

**Grep Patterns:**
```
Grep(pattern="(password|secret|api_key|token).*=.*['\"]", glob="**/*.{js,py,cs}")
```

---

## 3. Sensitive Data Exposure (A02:2021)

### Encryption

```python
# SECURE: Strong encryption
from cryptography.fernet import Fernet
key = os.environ['ENCRYPTION_KEY']
cipher = Fernet(key)
encrypted = cipher.encrypt(sensitive_data.encode())
```

### Logging

```javascript
// VULNERABLE: Logs sensitive data
console.log('User logged in:', { email, password });

// SECURE: No sensitive data in logs
console.log('User logged in:', { userId: user.id });
```

---

## 4. XML External Entities (A05:2021)

```python
# SECURE: Disable external entity processing
from lxml import etree
parser = etree.XMLParser(resolve_entities=False, no_network=True)
tree = etree.parse(xml_file, parser)
```

---

## 5. Broken Access Control (A01:2021)

```javascript
// VULNERABLE: Missing authorization
app.get('/api/users/:id', async (req, res) => {
  const user = await db.getUser(req.params.id);
  res.json(user);
});

// SECURE: Authorization check
app.get('/api/users/:id', authenticateUser, async (req, res) => {
  if (req.user.id !== req.params.id && !req.user.isAdmin) {
    return res.status(403).json({ error: 'Forbidden' });
  }
  const user = await db.getUser(req.params.id);
  res.json(user);
});
```

**Grep Patterns:**
```
Grep(pattern="app\\.(get|post|put|delete)\\(", glob="**/*.js", output_mode="content")
# Then check if auth middleware is present in route definitions
```

---

## 6. Security Misconfiguration (A05:2021)

```python
# VULNERABLE: Debug mode in production
DEBUG = True

# SECURE: Environment-based config
DEBUG = os.getenv('ENVIRONMENT') != 'production'
```

```javascript
// VULNERABLE: Exposes stack trace
app.use((err, req, res, next) => {
  res.status(500).json({ error: err.stack });
});

// SECURE: Generic error message
app.use((err, req, res, next) => {
  logger.error(err);
  res.status(500).json({ error: 'Internal server error' });
});
```

---

## 7. Cross-Site Scripting (A03:2021)

```javascript
// VULNERABLE: XSS via innerHTML
element.innerHTML = userInput;

// SECURE: Use textContent or sanitize
element.textContent = userInput;
element.innerHTML = DOMPurify.sanitize(userInput);
```

**Content Security Policy:**
```javascript
// SECURE: CSP header
app.use((req, res, next) => {
  res.setHeader("Content-Security-Policy",
    "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'"
  );
  next();
});
```

---

## 8. Insecure Deserialization (A08:2021)

```python
# VULNERABLE: Pickle deserialization
import pickle
data = pickle.loads(user_input)

# SECURE: Use JSON
import json
data = json.loads(user_input)
```

---

## 9. Using Components with Known Vulnerabilities (A06:2021)

**Check Dependencies:**
```bash
npm audit --production      # Node.js
pip check                   # Python
safety check                # Python (safety library)
dotnet list package --vulnerable  # .NET
```

---

## 10. Insufficient Logging and Monitoring (A09:2021)

```javascript
// SECURE: Log security events
logger.info('Login attempt', {
  userId: user.id,
  ip: req.ip,
  success: true,
  timestamp: new Date()
});

logger.warn('Failed login attempt', {
  email: email,
  ip: req.ip,
  timestamp: new Date(),
  attempts: failedAttempts
});
```

---

## Hardcoded Secrets Detection Patterns

```
# API Keys
Grep(pattern="api[_-]?key\\s*=\\s*['\"][A-Za-z0-9]{20,}", glob="**/*.{js,py,cs}")

# AWS Keys
Grep(pattern="AKIA[0-9A-Z]{16}", glob="**/*")

# Private Keys
Grep(pattern="BEGIN.*PRIVATE KEY", glob="**/*")

# JWT Secrets
Grep(pattern="jwt[_-]?secret\\s*=\\s*['\"]", glob="**/*.{js,py}")

# Database URLs with credentials
Grep(pattern="(postgres|mysql|mongodb)://[^:]+:[^@]+@", glob="**/*")
```

---

## References

- OWASP Top 10 (2021): https://owasp.org/www-project-top-ten/
- CWE/SANS Top 25 Most Dangerous Software Errors
- NIST Cybersecurity Framework

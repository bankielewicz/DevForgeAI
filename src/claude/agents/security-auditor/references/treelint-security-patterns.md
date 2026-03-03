---
name: security-auditor-treelint-patterns
description: Treelint AST-aware semantic vulnerability detection patterns for security-auditor subagent
version: "1.0"
requires: treelint v0.12.0+
status: LOCKED (ADR-013)
story: STORY-366
---

# Treelint Security Patterns for Security-Auditor

**Version**: 1.0
**Requires**: Treelint v0.12.0+
**Status**: LOCKED (ADR-013)
**Purpose**: AST-aware security-sensitive function discovery for vulnerability detection

---

## Security-Sensitive Function Pattern Categories

**Use these Treelint search patterns to discover security-critical functions across 5 OWASP-aligned categories.**

### 1. Authentication Functions

**OWASP Alignment**: A07:2021 - Identification and Authentication Failures

```markdown
Bash(command="treelint search --type function --name 'authenticate*' --format json")
Bash(command="treelint search --type function --name 'login*' --format json")
Bash(command="treelint search --type function --name 'verify_password*' --format json")
Bash(command="treelint search --type function --name 'verify_token*' --format json")
Bash(command="treelint search --type function --name 'check_credentials*' --format json")
```

**What to inspect**: Password hashing strength, timing attack resistance, brute force protection, session creation after auth.

### 2. Cryptography Functions

**OWASP Alignment**: A02:2021 - Cryptographic Failures

```markdown
Bash(command="treelint search --type function --name 'encrypt*' --format json")
Bash(command="treelint search --type function --name 'decrypt*' --format json")
Bash(command="treelint search --type function --name 'hash*' --format json")
Bash(command="treelint search --type function --name 'sign*' --format json")
Bash(command="treelint search --type function --name 'generate_key*' --format json")
```

**What to inspect**: Algorithm strength (no MD5/SHA1 for passwords), key management, IV/nonce reuse, padding oracle vulnerability.

### 3. Input Validation Functions

**OWASP Alignment**: A03:2021 - Injection

```markdown
Bash(command="treelint search --type function --name 'validate*' --format json")
Bash(command="treelint search --type function --name 'sanitize*' --format json")
Bash(command="treelint search --type function --name 'escape*' --format json")
Bash(command="treelint search --type function --name 'filter*' --format json")
Bash(command="treelint search --type function --name 'clean*' --format json")
```

**What to inspect**: SQL injection prevention, XSS protection, command injection prevention, path traversal prevention, input type enforcement.

### 4. Authorization Functions

**OWASP Alignment**: A01:2021 - Broken Access Control

```markdown
Bash(command="treelint search --type function --name 'authorize*' --format json")
Bash(command="treelint search --type function --name 'check_permission*' --format json")
Bash(command="treelint search --type function --name 'is_admin*' --format json")
Bash(command="treelint search --type function --name 'has_role*' --format json")
Bash(command="treelint search --type function --name 'can_access*' --format json")
```

**What to inspect**: Missing authorization checks, privilege escalation paths, IDOR (insecure direct object reference), horizontal access control.

### 5. Data Access Functions (Injection Risk)

**OWASP Alignment**: A03:2021 - Injection

```markdown
Bash(command="treelint search --type function --name 'query*' --format json")
Bash(command="treelint search --type function --name 'execute*' --format json")
Bash(command="treelint search --type function --name 'raw_sql*' --format json")
Bash(command="treelint search --type function --name 'run_query*' --format json")
Bash(command="treelint search --type function --name 'fetch*' --format json")
```

**What to inspect**: Parameterized queries vs string concatenation, ORM raw query usage, stored procedure invocation, dynamic SQL generation.

---

## JSON Response Parsing for Security Analysis

**Parse Treelint JSON output to extract structured security function information.**

### Required Fields

| Field | Description | Security Usage |
|-------|-------------|----------------|
| `name` | Function name | Match against security-sensitive naming patterns |
| `file` | File path | Locate source for detailed vulnerability analysis |
| `lines` | Line range `{"start": N, "end": M}` | Targeted Read() to inspect function body for vulnerabilities |
| `signature` | Full function signature | Identify user-input parameters that need validation |

### Parsing Pattern for Security Analysis

```markdown
# Parse Treelint results for security function analysis
FOR each result in treelint_output.results:
    # Extract function identity
    func_name = result.name
    file_path = result.file
    start_line = result.lines.start
    end_line = result.lines.end
    func_signature = result.signature

    # Targeted Read to inspect function body for vulnerabilities
    Read(file_path=file_path, offset=start_line, limit=end_line - start_line + 1)

    # Analyze function body for:
    # 1. SQL string concatenation (injection risk)
    # 2. Hardcoded secrets (API keys, passwords)
    # 3. Weak cryptographic algorithms (MD5, SHA1, DES)
    # 4. Missing input validation on user parameters
    # 5. Insecure deserialization (pickle, eval)
```

### Example: Authentication Function Analysis

**Command**: `treelint search --type function --name "authenticate*" --format json`

**Output**:
```json
{
  "results": [
    {
      "type": "function",
      "name": "authenticate_user",
      "file": "src/auth/service.py",
      "lines": {"start": 45, "end": 78},
      "signature": "def authenticate_user(email: str, password: str) -> Optional[User]"
    }
  ],
  "count": 1
}
```

**Security analysis from parsed data**:
1. `signature` shows `password: str` parameter - verify it is hashed before comparison
2. `lines` gives range 45-78 - Read() those lines to inspect password handling
3. `file` gives `src/auth/service.py` - check for timing-safe comparison

---

## Fallback: Grep for Unsupported Languages (Detail)

### Supported vs Unsupported Languages

| Treelint Supported | Use Grep Fallback |
|-------------------|-------------------|
| `.py`, `.ts`, `.tsx`, `.js`, `.jsx`, `.rs`, `.md` | `.cs`, `.java`, `.go`, `.rb`, `.php`, other |

### 5 Failure Modes (All Handled)

| # | Failure Mode | Exit Code | Detection | Action |
|---|-------------|-----------|-----------|--------|
| 1 | Binary not found | 127 | `command -v treelint` empty | Grep fallback with warning |
| 2 | Permission denied | 126 | OS permission error | Grep fallback with warning |
| 3 | Runtime error | 1+ | Any non-zero exit | Grep fallback with warning |
| 4 | Unsupported file type | N/A | Check extension first | Grep immediately |
| 5 | Malformed JSON | 0 | JSON.parse fails | Grep fallback with warning |

### Empty Results vs Failure (BR-002)

**CRITICAL**: Distinguish between valid empty results and actual failures.

| Scenario | Exit Code | Results | Action |
|----------|-----------|---------|--------|
| No matching functions found | 0 | `[]` | Return empty list. Do NOT trigger Grep fallback |
| Treelint command failed | Non-zero | N/A | Trigger Grep fallback with warning |

```markdown
IF treelint exit_code == 0:
    return treelint_output.results  # May be [] - this is valid
IF treelint exit_code != 0:
    Display: "Treelint fallback: {reason}, using Grep"
    return grep_fallback_results()
```

### Security-Specific Grep Fallback Patterns

| Security Category | Grep Pattern | Glob |
|-------------------|-------------|------|
| Authentication | `Grep(pattern="(authenticate\|login\|verify_password)", glob="**/*.cs")` | Per language |
| Cryptography | `Grep(pattern="(encrypt\|decrypt\|hash\|sign)", glob="**/*.java")` | Per language |
| Input Validation | `Grep(pattern="(validate\|sanitize\|escape\|filter)", glob="**/*.go")` | Per language |
| Authorization | `Grep(pattern="(authorize\|check_permission\|is_admin)", glob="**/*.cs")` | Per language |
| Data Access | `Grep(pattern="(query\|execute\|raw_sql)", glob="**/*.java")` | Per language |

### Warning Message Format

```
Treelint fallback: {reason}, using Grep
```

**Examples**:
- `Treelint fallback: .cs files not supported, using Grep`
- `Treelint fallback: binary not found, using Grep`
- `Treelint fallback: permission denied, using Grep`
- `Treelint fallback: malformed JSON output, using Grep`
- `Treelint fallback: runtime failure (exit 1), using Grep`

**Severity**: WARNING (not error). Do NOT halt workflow on Treelint failures.

---

## False Positive Reduction via AST-Aware Search

### Why AST-Aware Search Matters for Security Auditing

Text-based Grep matches ANY occurrence of a pattern, including non-functional contexts. Treelint's `--type function` filter returns ONLY actual function definitions, eliminating noise.

### False Positive Sources Eliminated

| # | False Positive Source | Grep Example (Matched) | Treelint (Not Matched) |
|---|---------------------|------------------------|----------------------|
| 1 | **Comments** | `# TODO: fix authenticate function` | Only matches `def authenticate(...)` |
| 2 | **String literals** | `error_msg = "password authentication failed"` | Only matches function definitions |
| 3 | **Variable names** | `authentication_enabled = True` | Only matches `def authentication(...)` |
| 4 | **Import statements** | `from auth import authenticate` | Only matches function definition, not import |

### Token Reduction Impact

- **Grep**: Returns ALL lines containing pattern - comments, strings, variables, imports, actual definitions
- **Treelint**: Returns ONLY function definitions with structured metadata (name, file, lines, signature)
- **Reduction**: 40-80% fewer tokens in search results, allowing more context budget for actual vulnerability analysis

### Combined Approach: AST + Content Search

Treelint finds security functions by name (structural discovery). Existing Grep content patterns (SQL injection, hardcoded secrets) remain for behavior-based detection:

```markdown
# Step 1: Treelint discovers security functions by name (AST-aware)
Bash(command="treelint search --type function --name 'query*' --format json")

# Step 2: Read function body using line ranges from Treelint
Read(file_path=result.file, offset=result.lines.start, limit=result.lines.end - result.lines.start + 1)

# Step 3: Grep within function body for vulnerability patterns (content-aware)
# Check for SQL concatenation, hardcoded secrets, weak crypto
```

---

## References

- **ADR-013**: Treelint Integration for AST-Aware Code Search (APPROVED)
- **tech-stack.md**: AST-Aware Code Search Tools section (lines 104-166)
- **anti-patterns.md**: Category 11 (Code search tool selection guidance)
- **Shared Reference**: `.claude/agents/references/treelint-search-patterns.md` (STORY-361)
- **OWASP Top 10 (2021)**: Security vulnerability categories

---

**Document Version**: 1.0
**Last Updated**: 2026-02-06
**Story**: STORY-366

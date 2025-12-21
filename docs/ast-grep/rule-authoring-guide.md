# Rule Authoring Guide

**Version:** 1.0
**Story:** STORY-116 - Configuration Infrastructure - ast-grep Rule Storage

---

## Introduction

This guide covers how to create ast-grep rules for DevForgeAI projects. Rules detect code patterns (anti-patterns, security issues, complexity violations) using AST-based pattern matching.

---

## Prerequisites

1. **ast-grep installed:** `npm install -g @ast-grep/cli` or `cargo install ast-grep`
2. **Configuration initialized:** `devforgeai ast-grep init`
3. **Basic understanding of AST concepts**

---

## Rule File Structure

Rules are YAML files placed in language-specific directories:

```
devforgeai/ast-grep/rules/
├── python/
│   └── SEC-001-sql-injection.yml
├── csharp/
│   └── AP-001-god-class.yml
├── typescript/
│   └── SEC-002-xss-vulnerability.yml
└── javascript/
    └── PERF-001-expensive-loop.yml
```

---

## RuleMetadata Schema

Each rule file follows this schema:

```yaml
id: "SEC-001"                    # Required: Unique identifier within language
language: "python"               # Required: python|csharp|typescript|javascript
severity: "CRITICAL"             # Required: CRITICAL|HIGH|MEDIUM|LOW
message: "Potential SQL injection detected - use parameterized queries"  # Required: min 10 chars
pattern: |                       # Required: ast-grep pattern
  cursor.execute($SQL)
fix: |                           # Optional: Auto-fix pattern
  cursor.execute($SQL, params)
note: |                          # Optional: Developer notes
  This rule detects raw SQL execution. Always use parameterized queries.
```

### Field Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique rule identifier (e.g., SEC-001, AP-002) |
| `language` | enum | Yes | Target language: `python`, `csharp`, `typescript`, `javascript` |
| `severity` | enum | Yes | Severity level: `CRITICAL`, `HIGH`, `MEDIUM`, `LOW` |
| `message` | string | Yes | Human-readable violation message (minimum 10 characters) |
| `pattern` | string | Yes | ast-grep pattern to match |
| `fix` | string | No | Auto-fix pattern (optional) |
| `note` | string | No | Additional notes for developers (optional) |

---

## Severity Levels

| Level | Description | Example Patterns |
|-------|-------------|------------------|
| `CRITICAL` | Security vulnerabilities, data exposure | SQL injection, hardcoded secrets |
| `HIGH` | Anti-patterns, architectural violations | God classes, layer violations |
| `MEDIUM` | Code quality issues, complexity | High cyclomatic complexity, duplication |
| `LOW` | Style issues, minor improvements | Naming conventions, comment quality |

---

## Pattern Syntax

ast-grep uses a pattern syntax that matches AST nodes.

### Basic Patterns

**Match function call:**
```yaml
pattern: print($MSG)
```

**Match method call:**
```yaml
pattern: $OBJ.execute($SQL)
```

**Match multiple arguments:**
```yaml
pattern: open($FILE, $MODE)
```

### Metavariables

- `$VAR` - Single node (identifier, expression)
- `$$$ARGS` - Multiple nodes (variadic)
- `$_` - Anonymous single node (don't capture)

### Examples by Language

**Python - Detect os.system:**
```yaml
pattern: os.system($CMD)
```

**C# - Detect string concatenation in SQL:**
```yaml
pattern: |
  new SqlCommand($QUERY + $$$REST)
```

**TypeScript - Detect innerHTML assignment:**
```yaml
pattern: |
  $ELEMENT.innerHTML = $VALUE
```

**JavaScript - Detect eval usage:**
```yaml
pattern: eval($CODE)
```

---

## Creating Your First Rule

### Step 1: Identify the Pattern

Decide what code pattern you want to detect. Example: Detecting hardcoded passwords in Python.

### Step 2: Create the Rule File

Create `devforgeai/ast-grep/rules/python/SEC-002-hardcoded-password.yml`:

```yaml
id: "SEC-002"
language: "python"
severity: "CRITICAL"
message: "Hardcoded password detected - use environment variables or secrets manager"
pattern: |
  password = $VALUE
note: |
  Passwords should never be hardcoded in source code.
  Use os.environ.get('PASSWORD') or a secrets manager.
```

### Step 3: Test Locally

```bash
# Test the rule against a file
ast-grep scan --rule devforgeai/ast-grep/rules/python/SEC-002-hardcoded-password.yml src/

# Or use the DevForgeAI CLI
devforgeai ast-grep scan src/ --language python
```

### Step 4: Validate Configuration

```bash
devforgeai ast-grep validate-config
```

---

## Rule Categories

Organize rules by category subdirectory for better management:

```
devforgeai/ast-grep/rules/python/
├── security/
│   ├── SEC-001-sql-injection.yml
│   └── SEC-002-hardcoded-password.yml
├── anti-patterns/
│   ├── AP-001-god-class.yml
│   └── AP-002-circular-import.yml
└── complexity/
    └── CX-001-nested-loops.yml
```

---

## Rule ID Conventions

| Prefix | Category | Examples |
|--------|----------|----------|
| `SEC-` | Security | SEC-001, SEC-002 |
| `AP-` | Anti-patterns | AP-001, AP-002 |
| `CX-` | Complexity | CX-001, CX-002 |
| `PERF-` | Performance | PERF-001, PERF-002 |
| `ARCH-` | Architecture | ARCH-001, ARCH-002 |

---

## Validation Rules

The DevForgeAI framework enforces these validation rules:

1. **Unique IDs:** Rule IDs must be unique within a language directory
2. **Valid Language:** Language must be one of: `python`, `csharp`, `typescript`, `javascript`
3. **Valid Severity:** Severity must be one of: `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`
4. **Message Length:** Message must be at least 10 characters
5. **Non-empty Pattern:** Pattern string cannot be empty

---

## Testing Rules

### Local Testing

```bash
# Test specific rule file
ast-grep scan --rule path/to/rule.yml target/directory

# Test with inline pattern
ast-grep --pattern 'os.system($CMD)' path/to/file.py
```

### Integration with DevForgeAI

```bash
# Scan directory with all rules
devforgeai ast-grep scan src/

# Filter by category
devforgeai ast-grep scan src/ --category security

# Filter by language
devforgeai ast-grep scan src/ --language python

# JSON output for CI/CD
devforgeai ast-grep scan src/ --format json
```

---

## Best Practices

### DO

- Use clear, actionable messages explaining **why** and **how to fix**
- Test rules against real codebase before committing
- Use appropriate severity levels (don't over-classify as CRITICAL)
- Include fix patterns when auto-fix is possible
- Add notes with context and references

### DON'T

- Create overly broad patterns that cause false positives
- Duplicate existing rules with different IDs
- Use CRITICAL for style issues (use LOW or MEDIUM)
- Write patterns that match test fixtures

---

## Related Documentation

- [sgconfig.yml Schema](./sgconfig-schema.md)
- [ast-grep Pattern Reference](https://ast-grep.github.io/guide/pattern-syntax.html)
- [DevForgeAI Anti-Patterns](../../devforgeai/specs/context/anti-patterns.md)

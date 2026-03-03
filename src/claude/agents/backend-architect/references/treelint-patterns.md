---
name: backend-architect-treelint-patterns
description: Treelint AST-aware code search patterns for backend-architect subagent
version: "1.0"
requires: treelint v0.12.0+
status: LOCKED (ADR-013)
story: STORY-365
---

# Treelint Patterns for Backend-Architect

**Version**: 1.0
**Requires**: Treelint v0.12.0+
**Status**: LOCKED (ADR-013)
**Purpose**: AST-aware class/method discovery for implementation workflow

---

## Treelint-Aware Class Discovery

**Use when discovering existing class definitions, interfaces, or abstract base classes for implementation decisions.**

### Command Pattern

```bash
treelint search --type class --name "PATTERN" --format json [--path DIR]
```

### Subagent Invocation

```markdown
Bash(command="treelint search --type class --name 'OrderService' --format json")
Bash(command="treelint search --type class --name '*Repository' --format json")
Bash(command="treelint search --type class --name 'Base*' --format json")
```

### When to Use

- Discovering domain entities before implementing new business logic
- Finding existing repositories to understand data access patterns
- Locating service classes for dependency injection points
- Identifying base classes for extension

### Supported File Extensions

- Python: `.py`
- TypeScript: `.ts`, `.tsx`
- JavaScript: `.js`, `.jsx`
- Rust: `.rs`
- Markdown: `.md`

---

## Treelint-Aware Method/Function Discovery

**Use when discovering specific methods or functions within a class for override points or functionality placement.**

### Command Pattern

```bash
treelint search --type function --name "PATTERN" --format json [--path DIR]
```

### Subagent Invocation

```markdown
Bash(command="treelint search --type function --name 'validate*' --format json")
Bash(command="treelint search --type function --name '*Handler' --format json")
Bash(command="treelint search --type function --name 'process_*' --format json")
```

### When to Use

- Finding methods implementing an interface contract
- Locating async handlers or lifecycle hooks
- Discovering validation methods for consistency
- Identifying override points in base classes

---

## JSON Response Parsing

**Parse Treelint JSON output to extract structured code information.**

### Required Fields

| Field | Description | Usage |
|-------|-------------|-------|
| `name` | Class/function name | Identify target by semantic name |
| `file` | File path | Locate source code for Read() operations |
| `lines` | Line range `{"start": N, "end": M}` | Targeted Read() with offset/limit |
| `signature` | Full signature string | Understand method contracts and parameters |

### Parsing Pattern

```markdown
# Parse JSON results from Treelint
FOR each result in treelint_output.results:
    # Extract name for identification
    entity_name = result.name

    # Extract file and line range for targeted reading
    file_path = result.file
    start_line = result.lines.start
    end_line = result.lines.end

    # Use signature for dependency analysis
    method_signature = result.signature

    # Targeted Read with line range (avoid loading entire file)
    Read(file_path=file_path, offset=start_line, limit=end_line - start_line + 1)
```

### Example JSON Output

```json
{
  "results": [
    {
      "type": "class",
      "name": "UserService",
      "file": "src/services/user_service.py",
      "lines": {"start": 10, "end": 150},
      "signature": "class UserService(BaseService, Auditable)",
      "members": {
        "methods": ["create_user", "get_user", "update_user"],
        "properties": ["_repository", "_cache"]
      }
    }
  ],
  "count": 1
}
```

---

## Fallback: Grep for Unsupported Languages

**When Treelint cannot process a file type or fails, fall back to native Grep tool.**

### Supported vs Unsupported

| Treelint Supported | Use Grep Fallback |
|-------------------|-------------------|
| `.py`, `.ts`, `.tsx`, `.js`, `.jsx`, `.rs`, `.md` | `.cs`, `.java`, `.go`, `.rb`, `.php`, other |

### Fallback Conditions

1. **Unsupported file extension** - Use Grep immediately
2. **Exit code 127** - Binary not found, use Grep
3. **Exit code 126** - Permission denied, use Grep
4. **Exit code 1+** - Runtime failure, use Grep
5. **Malformed JSON** - Parse error, use Grep

### Fallback Invocation (Native Grep Tool)

```markdown
# For class discovery
Grep(pattern="class\\s+\\w+", glob="**/*.cs")

# For method discovery
Grep(pattern="(public|private|protected).*\\w+\\s*\\(", glob="**/*.java")

# For Go functions
Grep(pattern="func\\s+\\w+\\(", glob="**/*.go")
```

### Warning-Level Messaging

```markdown
Display: "Treelint fallback: {reason}, using Grep"
```

**Warning levels (do NOT use HALT):**
- `Treelint fallback: .cs files not supported, using Grep`
- `Treelint fallback: binary not found, using Grep`
- `Treelint fallback: permission denied, using Grep`
- `Treelint fallback: malformed JSON output, using Grep`

### Empty Results vs Command Failure

**CRITICAL (BR-002):** Distinguish between valid empty results and actual failures.

**Exit code 0 with empty results is NOT a failure** - it means the query succeeded but no matches were found.

| Scenario | Exit Code | Action |
|----------|-----------|--------|
| Empty results (class doesn't exist) | 0 | Return empty list, do NOT use Grep fallback |
| Command failure | Non-zero | Use Grep fallback, emit warning |

```markdown
IF treelint exit_code == 0:
    # Success - even if results array is empty
    return treelint_output.results  # May be []

IF treelint exit_code != 0:
    # Failure - fall back to Grep
    Display: "Treelint fallback: runtime failure (exit {exit_code}), using Grep"
    return grep_fallback_results()
```

### Graceful Degradation (BR-003)

**CRITICAL:** When Treelint encounters issues, use Grep fallback - never interrupt the workflow.

```markdown
# CORRECT - Fall back gracefully when tool is unavailable
IF treelint_command_fails:
    Display: "Treelint fallback: {reason}, using Grep"
    results = grep_fallback()
    # Workflow continues normally with Grep results
```

**Principle:** Code discovery must never block implementation. Grep provides a valid fallback path.

---

## Implementation Pattern Discovery via Treelint

**Use during Phase 3 (Design Solution) to understand existing codebase patterns before writing new code.**

### Repository Pattern Discovery

```markdown
# Find all repository implementations
Bash(command="treelint search --type class --name '*Repository' --format json")

# Parse results to understand data access patterns
FOR each repo in results:
    Read(file_path=repo.file, offset=repo.lines.start, limit=50)
    # Analyze: What methods do existing repos implement?
    # Analyze: How is dependency injection structured?
```

### Service Pattern Discovery

```markdown
# Find all service classes
Bash(command="treelint search --type class --name '*Service' --format json")

# Parse results to understand service layer patterns
FOR each service in results:
    Read(file_path=service.file, offset=service.lines.start, limit=50)
    # Analyze: What dependencies are injected?
    # Analyze: How are business rules encapsulated?
```

### Interface/Abstract Base Discovery

```markdown
# Find interfaces (naming convention: I* prefix or *Interface suffix)
Bash(command="treelint search --type class --name 'I*' --format json")
Bash(command="treelint search --type class --name '*Interface' --format json")

# For Python abstract base classes
Bash(command="treelint search --type class --name '*ABC' --format json")
Bash(command="treelint search --type class --name 'Base*' --format json")
```

### Targeted Read from Line Ranges

**Use line ranges from Treelint results for efficient file reading:**

```markdown
# Instead of reading entire file
Read(file_path="src/services/user_service.py")  # Loads all 500 lines

# Use targeted Read with offset/limit from Treelint results
Read(file_path="src/services/user_service.py", offset=10, limit=140)  # Only lines 10-150
```

---

## References

- **ADR-013**: Treelint Integration for AST-Aware Code Search (APPROVED)
- **tech-stack.md**: AST-Aware Code Search Tools section (lines 104-166)
- **anti-patterns.md**: Category 11 (Code search tool selection guidance)
- **Shared Reference**: `.claude/agents/references/treelint-search-patterns.md` (STORY-361)

---

**Document Version**: 1.0
**Last Updated**: 2026-02-06
**Story**: STORY-365

---
name: treelint-search-patterns
description: Shared Treelint reference for subagent integration
version: "1.0"
---

# Treelint Search Patterns Reference

**Version**: 1.0
**Requires**: Treelint v0.12.0+
**Status**: LOCKED (ADR-013)
**Target Audience**: DevForgeAI subagents (test-automator, backend-architect, code-reviewer, security-auditor, refactoring-specialist, coverage-analyzer, anti-pattern-scanner)

---

**CRITICAL**: All Treelint commands MUST include `--format json` for AI consumption (BR-001).

---

## Search Command Patterns

### 1. Function Search

**Locate function definitions by name pattern.**

```bash
treelint search --type function --name "PATTERN" --format json [--path DIR]
```

| Argument | Required | Description |
|----------|----------|-------------|
| `--type function` | Yes | Search for function definitions |
| `--name "PATTERN"` | Yes | Glob pattern (e.g., `"validate*"`, `"*Handler"`) |
| `--path DIR` | No | Search directory (default: current) |

**Subagent Invocation**:
```markdown
Bash(command="treelint search --type function --name 'validate*' --format json")
```

---

### 2. Class Search

**Locate class definitions with member enumeration.**

```bash
treelint search --type class --name "PATTERN" --format json [--path DIR]
```

| Argument | Required | Description |
|----------|----------|-------------|
| `--type class` | Yes | Search for class definitions |
| `--name "PATTERN"` | Yes | Glob pattern (e.g., `"*Service"`, `"Base*"`) |
| `--path DIR` | No | Search directory (default: current) |

**Subagent Invocation**:
```markdown
Bash(command="treelint search --type class --name '*Service' --format json")
```

---

### 3. Ranked File Map

**Generate ranked importance map of codebase files.**

```bash
treelint map --ranked --format json [--path DIR] [--top N]
```

| Argument | Required | Description |
|----------|----------|-------------|
| `--ranked` | Yes | Sort by importance score |
| `--path DIR` | No | Target directory (default: current) |
| `--top N` | No | Limit to top N files |

**Subagent Invocation**:
```markdown
Bash(command="treelint map --ranked --format json --top 20")
```

---

### 4. Call Dependency Analysis

**Analyze function call relationships.**

```bash
treelint deps --calls --format json [--path DIR] [--function NAME]
```

| Argument | Required | Description |
|----------|----------|-------------|
| `--calls` | Yes | Analyze call dependencies |
| `--path DIR` | No | Target directory (default: current) |
| `--function NAME` | No | Focus on specific function |

**Subagent Invocation**:
```markdown
Bash(command="treelint deps --calls --format json")
```

---

## JSON Output Parsing Examples

### Example 1: Function Search Result

**Command**: `treelint search --type function --name "validate*" --format json`

**Output**:
```json
{
  "results": [
    {
      "type": "function",
      "name": "validate_input",
      "file": "src/validators/input_validator.py",
      "lines": {"start": 15, "end": 42},
      "signature": "def validate_input(data: dict, schema: Schema) -> ValidationResult",
      "body": "def validate_input(data: dict, schema: Schema) -> ValidationResult:\n    \"\"\"Validate input against schema.\"\"\"\n    ..."
    }
  ],
  "count": 1,
  "query": {"type": "function", "name": "validate*"}
}
```

**Parse by extracting:** `results[].name` (function names), `results[].file` + `results[].lines.start` (navigation), `results[].signature` (interface)

---

### Example 2: Class Search Result

**Command**: `treelint search --type class --name "*Service" --format json`

**Output**:
```json
{
  "results": [
    {
      "type": "class",
      "name": "UserService",
      "file": "src/services/user_service.py",
      "lines": {"start": 10, "end": 150},
      "members": {
        "methods": ["create_user", "get_user", "update_user", "delete_user"],
        "properties": ["_repository", "_cache"],
        "class_methods": ["from_config"]
      },
      "bases": ["BaseService", "Auditable"]
    }
  ],
  "count": 1,
  "query": {"type": "class", "name": "*Service"}
}
```

**Parse by extracting:** `results[].members.methods` (method inventory), `results[].bases` (inheritance), `members.properties` (attributes)

---

### Example 3: Ranked Map Result

**Command**: `treelint map --ranked --format json --top 5`

**Output**:
```json
{
  "files": [
    {"path": "src/core/engine.py", "rank": 1, "score": 95.2, "references": 47, "complexity": 12},
    {"path": "src/api/router.py", "rank": 2, "score": 82.1, "references": 38, "complexity": 8},
    {"path": "src/models/user.py", "rank": 3, "score": 71.5, "references": 31, "complexity": 5},
    {"path": "src/utils/helpers.py", "rank": 4, "score": 65.3, "references": 28, "complexity": 3},
    {"path": "src/config.py", "rank": 5, "score": 58.9, "references": 24, "complexity": 2}
  ],
  "total_files": 127,
  "returned": 5
}
```

**Parse by:** Higher `score` = more important file; `references` = import count; `complexity` = cyclomatic complexity estimate

---

## Fallback Decision Tree

### When to Use Treelint vs Grep

```
Step 1: Check file extension
    ├─ .py, .ts, .tsx, .js, .jsx, .rs, .md → SUPPORTED (Step 2)
    └─ .cs, .java, .go, .rb, .php, other → UNSUPPORTED (Step 4)

Step 2: Attempt Treelint
    ├─ Success (exit 0) → Step 6 (return results)
    └─ Failure (exit != 0) → Step 3 (detect failure)

Step 3: Detect failure via exit code
    ├─ Exit 127 (binary not found) → Step 4 (fallback to Grep)
    ├─ Exit 126 (permission denied) → Step 4 (fallback to Grep)
    ├─ Exit 1+ (runtime failure) → Step 4 (fallback to Grep)
    └─ Malformed JSON output → Step 4 (fallback to Grep)

Step 4: Fall back to Grep
    └─ Use Grep pattern equivalent (see table below)

Step 5: Log warning with fallback reason
    └─ Display: "Treelint fallback: {reason}, using Grep"
    └─ Do NOT treat as error (valid fallback path)

Step 6: Return results to caller
    └─ Return Treelint results (from Step 2) OR Grep results (from Step 4)
    └─ Caller receives usable results regardless of tool used
```

### Grep Pattern Equivalents (BR-002)

| Treelint Command | Grep Fallback | Notes |
|------------------|---------------|-------|
| `treelint search --type function --format json` | `Grep(pattern="def \\w+\\(", glob="**/*.py")` | Python-specific; see language table below for other languages |
| `treelint search --type class --format json` | `Grep(pattern="class \\w+", glob="**/*.py")` | Misses nested classes; adjust pattern per language |
| `treelint map --ranked --format json` | `Glob(pattern="**/*.py")` + `Grep(pattern="(def|class)", glob="**/*.py")` | Glob for file list, Grep to count definitions as importance heuristic |
| `treelint deps --calls --format json` | `Grep(pattern="(import|from .* import)", glob="**/*.py")` | Search for import statements to approximate dependencies |

### Language-Specific Grep Patterns

| Language | Function Pattern | Class Pattern |
|----------|-----------------|---------------|
| Python | `def \w+\(` | `class \w+` |
| TypeScript/JS | `function \w+\(` or `\w+ = \(` | `class \w+` |
| C# | `(public|private|protected).*\w+\s*\(` | `class \w+` |
| Java | `(public|private|protected).*\w+\s*\(` | `class \w+` |
| Go | `func \w+\(` | `type \w+ struct` |

---

## Language Support Matrix

| Language | File Extensions | Treelint Support | Fallback Strategy | Notes |
|----------|-----------------|------------------|-------------------|-------|
| Python | `.py` | ✅ Supported | N/A | Full AST analysis |
| TypeScript | `.ts`, `.tsx` | ✅ Supported | N/A | Includes JSX/TSX |
| JavaScript | `.js`, `.jsx` | ✅ Supported | N/A | ES6+ supported |
| Rust | `.rs` | ✅ Supported | N/A | Full Rust grammar |
| Markdown | `.md` | ✅ Supported | N/A | Heading/link extraction |
| C# | `.cs` | ❌ Unsupported | Grep patterns | Use regex for methods/classes |
| Java | `.java` | ❌ Unsupported | Grep patterns | Use regex for methods/classes |
| Go | `.go` | ❌ Unsupported | Grep patterns | Use regex for funcs/types |
| Other | `*` | ❌ Unsupported | Grep patterns | Generic text search |

**Version Requirement**: Treelint v0.12.0+ required for all supported languages.

---

## Error Handling Patterns

### Scenario 1: Binary Unavailable (Exit Code 127 or 126)

**Detection**: Exit code 127 (binary not found) or exit code 126 (permission denied), or `command -v treelint` returns empty
**Recovery**: Fall back to Grep patterns immediately. Do NOT halt or raise error.
**Warning Message**: Display `Treelint fallback: binary not found, using Grep` or `Treelint fallback: permission denied, using Grep`

### Scenario 2: Version Too Old (Missing --format json)

**Detection**: `treelint --version` shows v0.11.x or lower; error mentions unknown `--format` flag
**Recovery**: Fall back to Grep patterns; recommend upgrade to v0.12.0+

### Scenario 3: Empty Results (Valid Query, No Matches)

**Detection**: `{"results": [], "count": 0}` returned
**Recovery**: Return empty set (NOT an error); do NOT fall back to Grep

### Scenario 4: Malformed JSON (Parse Error)

**Detection**: JSON.parse() fails or output contains non-JSON text mixed with JSON
**Recovery**: Extract valid JSON portion; if extraction fails, use Grep fallback
**Warning Message**: Display `Treelint fallback: malformed JSON output, using Grep`

### Scenario 5: Daemon Crashed or Unresponsive

**Detection**: Treelint daemon process is not responding; socket connection refused (ECONNREFUSED); daemon.sock file missing or stale
**Recovery**: Attempt to restart daemon with `treelint daemon start`; if restart fails, fall back to Grep patterns. Do NOT HALT.
**Warning Message**: Display `Treelint fallback: daemon unresponsive (connection refused), using Grep`

### Scenario 6: Corrupted or Missing Index

**Detection**: index.db file is corrupted, missing, or incompatible with current Treelint version; queries return parse errors referencing the index
**Recovery**: Attempt to rebuild index with `treelint index --rebuild`; if re-indexing fails, fall back to Grep patterns. Do NOT HALT.
**Warning Message**: Display `Treelint fallback: corrupted index (re-index failed), using Grep`

---

## Warning Message Format (FALLBACK-003)

**All fallback warnings MUST use the `Treelint fallback:` prefix.**

**Format Template**:
```
Treelint fallback: {reason}, using Grep
```

**Examples**:
- `Treelint fallback: .cs files not supported, using Grep`
- `Treelint fallback: binary not found, using Grep`
- `Treelint fallback: permission denied, using Grep`
- `Treelint fallback: malformed JSON output, using Grep`
- `Treelint fallback: runtime failure (exit 1), using Grep`

**Requirements**:
- Message severity is WARNING (not error)
- Message includes specific reason for fallback
- Workflow continues without halting after warning
- No exception propagation to parent skill

---

## References

- **ADR-013**: Treelint Integration for AST-Aware Code Search (APPROVED)
- **tech-stack.md**: AST-Aware Code Search Tools section (Treelint language support, version requirements)
- **anti-patterns.md**: Category 11 (Code search tool selection guidance)
- **dependencies.md**: Binary Dependencies section (Treelint installation)

---

**Document Version**: 1.0
**Last Updated**: 2026-02-06
**Maintained By**: DevForgeAI Framework Team

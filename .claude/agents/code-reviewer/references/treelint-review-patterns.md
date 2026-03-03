---
name: treelint-review-patterns
description: Treelint AST-aware pattern detection for code-reviewer subagent
version: "1.0"
---

# Treelint Review Patterns for Code-Reviewer

**Version**: 1.0 | **Requires**: Treelint v0.12.0+ | **Status**: LOCKED (ADR-013)

**CRITICAL**: All Treelint commands MUST include `--format json` for AI consumption.

---

## 1. God Class Detection via Treelint

**Purpose:** Identify classes with excessive methods (>20), indicating God Object anti-pattern.

### Invocation

```markdown
Bash(command="treelint search --type class --format json --path src/")
```

### Detection Logic

```markdown
FOR each class in results:
    method_count = len(class.members.methods)
    IF method_count > 20:
        Flag as God Class (WARNING severity)
```

**Threshold:** >20 methods per class

### Reporting Fields

| Field | JSON Path | Description |
|-------|-----------|-------------|
| Class name | `results[].name` | Class identifier |
| File path | `results[].file` | Source file location |
| Method count | `len(results[].members.methods)` | Number of methods |
| Line range | `results[].lines.start` to `.end` | Class boundaries |

---

## 2. Long Method Detection via Treelint

**Purpose:** Identify functions exceeding 50 lines, indicating complexity violations.

### Invocation

```markdown
Bash(command="treelint search --type function --format json --path src/")
```

### Detection Logic

```markdown
FOR each function in results:
    line_count = function.lines.end - function.lines.start
    IF line_count > 50:
        Flag as Long Method (WARNING severity)
```

**Threshold:** >50 lines per function
**Line Calculation:** `lines[1] - lines[0]` (or `lines.end - lines.start`)

### Reporting Fields

| Field | JSON Path | Description |
|-------|-----------|-------------|
| Function name | `results[].name` | Function identifier |
| File path | `results[].file` | Source file location |
| Line count | `lines.end - lines.start` | Actual line count |
| Start/End | `results[].lines.start`, `.end` | Line boundaries |

---

## 3. Review Prioritization via Treelint Map

**Purpose:** Rank files by structural importance for review depth prioritization.

### Invocation

```markdown
Bash(command="treelint map --ranked --format json --top 20")
```

### Prioritization Logic

| Rank | Review Depth | Checklist Items |
|------|--------------|-----------------|
| 1-5 (High) | Deep review | All 8 sections |
| 6-15 (Medium) | Standard review | Security, Error Handling, Testing |
| 16+ (Low) | Light review | Critical security only |

### Rationale Documentation

Document prioritization in review report with rank, score, and reason for each file.

---

## 4. Supported Languages and Fallback

### Supported Extensions (Treelint)

`.py`, `.ts`, `.tsx`, `.js`, `.jsx`, `.rs`, `.md`

### Unsupported Languages (Grep Fallback)

`.cs` (C#), `.java` (Java), `.go` (Go), `.rb` (Ruby), `.php` (PHP)

### Extension Check Before Invocation

```markdown
supported = [".py", ".ts", ".tsx", ".js", ".jsx", ".rs", ".md"]
IF file.extension in supported:
    Use Treelint
ELSE:
    Use Grep fallback
    Display: "Treelint fallback: {ext} files not supported, using Grep"
```

### Grep Fallback Patterns

| Search Type | Grep Pattern |
|-------------|--------------|
| Function | `Grep(pattern="(def|function|func|public.*void)\\s+\\w+\\(", glob="**/*.{cs,java,go}")` |
| Class | `Grep(pattern="class\\s+\\w+", glob="**/*.{cs,java,go}")` |

**Warning Messaging:** Fallback is WARNING severity, NOT error. Workflow continues.

**Equivalent Output:** Both Treelint and Grep produce same review output format.

---

## 5. Parsing Treelint JSON Output

### Core JSON Fields

| Field | Purpose |
|-------|---------|
| `results[].name` | Function/class name |
| `results[].file` | Source file path |
| `results[].lines` | Start/end line numbers |

### Class-Specific Extraction

- Class name: `results[].name`
- Method count: `len(results[].members.methods)`
- File path: `results[].file`

### Function-Specific Extraction

- Function name: `results[].name`
- Line range: `results[].lines.start` to `.end`
- Signature: `results[].signature`

### Empty Results Handling

When `{"results": [], "count": 0}` returned:

```markdown
Display: "No structural issues found in analyzed files."
# Do NOT fall back to Grep - empty results is valid, not an error
```

### Malformed JSON Fallback

```markdown
TRY:
    results = parse_json(output)
CATCH parse_error:
    Display: "Treelint fallback: malformed JSON output, using Grep"
    Use Grep fallback patterns
    # Continue review - do NOT halt
```

---

## References

- **Shared Patterns**: `.claude/agents/references/treelint-search-patterns.md`
- **tech-stack.md**: Treelint v0.12.0+ requirement
- **anti-patterns.md**: Category 11 (Code search tool selection)
- **ADR-013**: Treelint Integration for AST-Aware Code Search

---

**Document Version**: 1.0 | **Last Updated**: 2026-02-06 | **Created By**: STORY-364

---
name: phase5-treelint-detection
description: Treelint AST-aware code smell detection for anti-pattern-scanner Phase 5
version: "1.0"
requires: treelint v0.12.0+
status: LOCKED (ADR-013)
story: STORY-369
---

# Treelint AST-Aware Code Smell Detection

**Purpose**: Replace text-based Grep heuristics with AST-aware Treelint searches for god class detection (>20 methods) and long function detection (>50 lines) in Phase 5 of the anti-pattern-scanner workflow.

**Requires**: Treelint v0.12.0+ with `--format json` support

**Scope**: Phase 5 Check 1 (God Objects) and Check 2 (Long Methods) only. Check 3 (Magic Numbers) remains Grep-based and is unaffected.

---

## Step 0: Load Shared Treelint Reference

Load the shared STORY-361 Treelint patterns file for common search patterns and fallback decision tree:

```markdown
Read(file_path=".claude/agents/references/treelint-search-patterns.md")
```

---

## Step 1: Treelint Class Enumeration for God Class Detection

**Command**: Enumerate all classes in the project to detect god classes (classes with >20 methods).

```bash
treelint search --type class --format json
```

**Subagent Invocation**:

```markdown
Bash(command="treelint search --type class --format json")
```

### JSON Response Parsing

Parse the JSON output to extract structured class information. Required fields:

| Field | Type | Description | Usage |
|-------|------|-------------|-------|
| `name` | string | Class name | Identify the class for violation reporting |
| `file` | string | File path | Generate evidence with exact file location |
| `lines` | object | `{"start": N, "end": M}` | Define class boundary for method correlation |
| `signature` | string | Class declaration line | Include in violation evidence |

**IMPORTANT**: Do NOT consume the `body` field from Treelint class results. The body may contain thousands of lines and will exhaust the context window. Use only `name`, `file`, `lines`, and `signature` fields.

**Parsing Pattern**:

```markdown
FOR each class_result in treelint_output.results:
    class_name = class_result.name
    class_file = class_result.file
    class_start = class_result.lines.start
    class_end = class_result.lines.end
    class_signature = class_result.signature
    # NOTE: Do NOT extract class_result.body - context window hazard
```

---

## Step 2: Treelint Function Enumeration for Long Function Detection

**Command**: Enumerate all functions to detect long functions (>50 lines) and to correlate methods with classes.

```bash
treelint search --type function --format json
```

**Subagent Invocation**:

```markdown
Bash(command="treelint search --type function --format json")
```

### JSON Response Parsing

Parse function results using the same field structure:

| Field | Type | Description | Usage |
|-------|------|-------------|-------|
| `name` | string | Function/method name | Identify the function for reporting |
| `file` | string | File path | Match functions to classes in same file |
| `lines` | object | `{"start": N, "end": M}` | Calculate function length and check containment |
| `signature` | string | Function declaration | Include in violation evidence |

**Function Length Calculation**:

```markdown
function_length = result.lines.end - result.lines.start + 1
IF function_length > 50:
    Flag as MEDIUM violation: "Long function: {name} is {function_length} lines"
```

---

## Step 3: Class-to-Function Correlation (God Class Detection)

**Purpose**: Correlate function enumeration results with class boundaries to count methods per class. A function is considered a method of a class if its line range falls within the class line range.

**Design Decision**: Line-range containment is used instead of Treelint's `members.methods` array to ensure consistent behavior across all supported languages and Treelint versions. The `members` field availability varies by language parser (e.g., Rust may not populate it), whereas line-range containment works universally. This approach also enables standalone function detection (Step 2) using the same function enumeration data.

### Correlation Algorithm

```markdown
FOR each class in class_results:
    method_count = 0
    FOR each function in function_results:
        # Check if function is in the same file as the class
        IF function.file == class.file:
            # Check if function line range falls within class line range (containment)
            IF function.lines.start >= class.lines.start AND function.lines.end <= class.lines.end:
                method_count += 1

    # God class threshold: >20 methods for Treelint mode
    IF method_count > 20:
        Flag as MEDIUM violation (non-blocking):
            class_name: class.name
            method_count: method_count
            file_path: class.file
            start_line: class.lines.start
            evidence: "{class.name} has {method_count} methods (threshold: >20)"
```

**Threshold Note**: Both Treelint-based and legacy Grep-based god class detection now use the unified >20 method threshold per REC-369-001. This ensures identical detection results regardless of which detection method is used. <!-- Threshold unified to >20 per REC-369-001 to match Treelint mode -->

### Standalone Function Handling

Functions that exist outside any class boundary (module-level functions in Python, top-level functions in JavaScript/TypeScript) must be handled separately:

- **Standalone functions** are functions whose line range does NOT fall within any class's line range in the same file
- These functions are checked for the >50 line long function threshold (Step 2)
- They are NOT counted toward any class's method count for god class detection
- Report standalone long functions as: "Long function: {name} ({length} lines, module-level)"

---

## Step 4: Fallback - Grep for Unsupported Languages

**Trigger**: Use Grep fallback when:
1. File extension is not supported by Treelint (e.g., `.cs`, `.java`, `.go`, `.rb`)
2. Treelint binary is unavailable (exit code 127)
3. Treelint fails at runtime (any non-zero exit code)
4. Treelint output is malformed JSON

### Supported File Extensions (Treelint)

Treelint supports AST analysis for these extensions:
- `.py` (Python)
- `.ts` (TypeScript)
- `.tsx` (TypeScript JSX)
- `.js` (JavaScript)
- `.jsx` (JavaScript JSX)
- `.rs` (Rust)
- `.md` (Markdown)

All other file extensions require Grep fallback.

### Fallback Invocation (Native Grep Tool)

Use the native Grep tool (NOT `Bash(command="grep ...")`):

```markdown
# For class discovery in unsupported languages
Grep(pattern="class\\s+\\w+", glob="**/*.cs")
Grep(pattern="public\\s+class\\s+\\w+", glob="**/*.java")

# For method discovery in unsupported languages
Grep(pattern="(public|private|protected).*\\w+\\s*\\(", glob="**/*.cs")
Grep(pattern="func\\s+\\w+\\(", glob="**/*.go")
```

### Warning-Level Messaging

When falling back to Grep, emit a warning using the standard `Treelint fallback:` prefix. This is warning-level messaging only (the workflow continues, does not stop):

```markdown
Display: "Treelint fallback: {extension} files not supported, using Grep"
```

**Warning examples** (FALLBACK-003 compliant format):
- `"Treelint fallback: .cs files not supported, using Grep"`
- `"Treelint fallback: binary not found, using Grep"`
- `"Treelint fallback: runtime failure (exit {code}), using Grep"`

The workflow continues normally after the warning. Code smell detection completes using Grep results.

### Empty Results vs Command Failure (BR-002)

**CRITICAL**: Distinguish between valid empty results and actual command failures.

| Scenario | Exit Code | Action |
|----------|-----------|--------|
| No classes/functions found (valid empty results) | exit code 0 | Return empty list, do NOT trigger Grep fallback |
| Treelint binary not found | exit code 127 | Trigger Grep fallback with warning |
| Permission denied | exit code 126 | Trigger Grep fallback with warning |
| Runtime error | non-zero | Trigger Grep fallback with warning |
| Malformed JSON output | 0 (but parse fails) | Trigger Grep fallback with warning |

An exit code 0 with zero matches means the file or project has no class or function declarations. This is valid information (e.g., a constants-only module) and must NOT trigger Grep fallback.

---

## Performance Targets

- Each Treelint search (class or function) should complete in <100ms for CLI mode
- Verify via the `stats.elapsed_ms` field in Treelint JSON output
- Total Phase 5 code smell detection with Treelint adds no more than 200ms overhead vs Grep-and-Read
- If performance exceeds targets, log timing for diagnostic purposes but do not halt

---

## References

- **ADR-013**: Treelint Integration for AST-Aware Code Search (APPROVED)
- **tech-stack.md**: AST-Aware Code Search Tools section (Treelint language support)
- **anti-patterns.md**: Category 11 (Code search tool selection guidance)
- **Shared Reference**: `src/.claude/agents/references/treelint-search-patterns.md` (STORY-361)
- **Sibling Reference**: `phase5-code-smells.md` (legacy Grep-based code smell detection)

---

**Document Version**: 1.0
**Last Updated**: 2026-02-07
**Story**: STORY-369

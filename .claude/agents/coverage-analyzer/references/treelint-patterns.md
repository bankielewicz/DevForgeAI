---
name: coverage-analyzer-treelint-patterns
description: Treelint AST-aware function-level coverage mapping patterns for coverage-analyzer subagent
version: "1.0"
---

# Treelint Function-Level Coverage Mapping Patterns

**Version**: 1.0
**Requires**: Treelint v0.12.0+
**Status**: LOCKED (ADR-013)
**Parent Agent**: coverage-analyzer
**Phase**: Phase 6 (Identify Gaps) - Treelint function enumeration enhances gap identification

---

## Function Enumeration for Coverage Mapping (Phase 6)

### Step 6.5: Enumerate Functions in Under-Covered Files

For each file identified as under-covered in Phase 6:

```
# Check if file extension is Treelint-supported
supported_extensions = [".py", ".ts", ".tsx", ".js", ".jsx", ".rs", ".md"]

IF file_extension in supported_extensions:
    # Use Treelint for AST-aware function enumeration
    Bash(command="treelint search --type function --format json --path {file_path}")
ELSE:
    # Fall back to Grep for unsupported languages
    GOTO Fallback: Grep for Unsupported Languages
```

### Step 6.6: Parse Treelint JSON Response

Extract function information from JSON output:

| JSON Field | Purpose | Usage |
|------------|---------|-------|
| `name` | Function identifier | Gap report: "uncovered function: {name}" |
| `file` | Source file path | Locate source code for Read() |
| `lines` | Object `{start, end}` | Correlate with uncovered_lines |
| `signature` | Full function signature | Human-readable gap description |

**Example JSON Output:**
```json
{
  "results": [
    {
      "name": "calculateCoverage",
      "file": "src/coverage.py",
      "lines": {"start": 10, "end": 45},
      "signature": "def calculateCoverage(data: dict) -> float"
    }
  ],
  "stats": { "elapsed_ms": 42 }
}
```

**Performance Target:** Treelint search latency <100ms (verify via `stats.elapsed_ms` field). Total function enumeration overhead <200ms compared to line-only gap identification.

---

## Fallback: Grep for Unsupported Languages

### Trigger Conditions (use Grep, NOT Treelint)

| Condition | Detection | Action |
|-----------|-----------|--------|
| Unsupported file extension | `.cs`, `.java`, `.go`, `.rb`, `.php`, other | Use Grep patterns |
| Binary not found | Exit code 127 | Grep fallback + warning |
| Permission denied | Exit code 126 | Grep fallback + warning |
| Runtime failure | Exit code 1+ | Grep fallback + warning |
| Malformed JSON output | JSON.parse() fails | Grep fallback + warning |

### CRITICAL: Empty Results is NOT a Failure

- Exit code 0 with `{"results": [], "count": 0}` is VALID (no functions in file)
- Do NOT trigger Grep fallback for empty results
- Return empty function list (file may contain only module-level code)

### Grep Fallback Patterns

```
# Python functions
Grep(pattern="def \\w+\\(", glob="**/*.py")

# C# methods
Grep(pattern="(public|private|protected).*\\w+\\s*\\(", glob="**/*.cs")

# Java methods
Grep(pattern="(public|private|protected).*\\w+\\s*\\(", glob="**/*.java")

# Go functions
Grep(pattern="func \\w+\\(", glob="**/*.go")
```

### Warning Message Format

```
Treelint fallback: {reason}, using Grep
```

**Examples:**
- `Treelint fallback: .cs files not supported, using Grep`
- `Treelint fallback: binary not found, using Grep`
- `Treelint fallback: permission denied, using Grep`
- `Treelint fallback: malformed JSON output, using Grep`

**Workflow Continuity:** Fallback is warning-level only. Coverage analysis never stops due to Treelint unavailability - it completes with line-level granularity for unsupported languages.

---

## Coverage Data Correlation with Function Boundaries

### Step 6.7: Correlate Uncovered Lines with Functions

```
FOR each uncovered_line in file.uncovered_lines:
    # Find functions whose range contains this line
    matching_functions = []
    FOR each function in treelint_results:
        IF function.lines.start <= uncovered_line <= function.lines.end:
            matching_functions.append(function)

    # Handle nested functions: attribute to innermost (smallest range)
    IF len(matching_functions) > 1:
        matching_functions.sort(by=range_size, ascending=True)
        attributed_function = matching_functions[0]  # Innermost
    ELIF len(matching_functions) == 1:
        attributed_function = matching_functions[0]
    ELSE:
        # Line is outside all function boundaries
        attributed_function = null  # Module-level code
```

### Step 6.8: Aggregate Function-Level Coverage

```
FOR each function in treelint_results:
    function_lines = range(function.lines.start, function.lines.end + 1)
    uncovered_in_function = intersection(file.uncovered_lines, function_lines)
    function.uncovered_count = len(uncovered_in_function)
    function.total_lines = function.lines.end - function.lines.start + 1
    function.coverage_percentage = ((function.total_lines - function.uncovered_count) / function.total_lines) * 100
```

### Step 6.9: Handle Module-Level Uncovered Code

Lines outside any function boundary (e.g., global statements, class-level initializers):

```
module_level_lines = file.uncovered_lines - all_function_lines
IF module_level_lines:
    gap.module_level_gaps = {
        "uncovered_lines": module_level_lines,
        "description": "Module-level code outside function boundaries"
    }
```

---

## Enhanced Gap Output Schema

When Treelint function enumeration succeeds, enhance gap reports with function-level detail:

```json
{
  "file": "src/coverage.py",
  "layer": "business_logic",
  "current_coverage": 72.5,
  "target_coverage": 95.0,
  "function_gaps": [
    {
      "function_name": "calculateCoverage",
      "function_lines": [10, 45],
      "function_signature": "def calculateCoverage(data: dict) -> float",
      "uncovered_lines_in_function": [23, 24, 25, 38, 39],
      "function_coverage_percentage": 85.7
    }
  ],
  "module_level_gaps": {
    "uncovered_lines": [1, 2, 5],
    "description": "Module-level code outside function boundaries"
  },
  "suggested_tests": [
    "Add tests for calculateCoverage at src/coverage.py:10-45 (85.7% covered, 5 lines uncovered)"
  ]
}
```

**Field Descriptions:**

| Field | Type | Description |
|-------|------|-------------|
| `function_gaps` | Array | Per-function coverage breakdown |
| `function_name` | String | Function identifier from Treelint |
| `function_lines` | Array[2] | Start and end line numbers |
| `function_signature` | String | Full function signature for human readability |
| `uncovered_lines_in_function` | Array | Specific uncovered lines within function |
| `function_coverage_percentage` | Number | Coverage percentage for this function |
| `module_level_gaps` | Object | Uncovered code outside function boundaries |

---

## Language Support Matrix

| Language | Extensions | Treelint | Fallback |
|----------|------------|----------|----------|
| Python | `.py` | ✅ Supported | N/A |
| TypeScript | `.ts`, `.tsx` | ✅ Supported | N/A |
| JavaScript | `.js`, `.jsx` | ✅ Supported | N/A |
| Rust | `.rs` | ✅ Supported | N/A |
| Markdown | `.md` | ✅ Supported | N/A |
| C# | `.cs` | ❌ Unsupported | Grep patterns |
| Java | `.java` | ❌ Unsupported | Grep patterns |
| Go | `.go` | ❌ Unsupported | Grep patterns |
| Ruby | `.rb` | ❌ Unsupported | Grep patterns |

---

## References

- `.claude/agents/references/treelint-search-patterns.md` - Shared Treelint reference file (STORY-361)
- `devforgeai/specs/context/tech-stack.md` - Treelint v0.12.0+ approval (ADR-013)
- `devforgeai/specs/context/anti-patterns.md` - Code search tool selection guidance (Category 11)

---

**Document Version**: 1.0
**Created**: 2026-02-07
**Story**: STORY-368

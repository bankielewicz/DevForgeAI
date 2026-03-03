---
name: refactoring-specialist-treelint-patterns
description: Treelint AST-aware refactoring patterns for code smell detection and structure analysis
version: "1.0"
requires: treelint v0.12.0+
status: LOCKED (ADR-013)
story: STORY-367
---

# Treelint Refactoring Patterns

**Version**: 1.0
**Requires**: Treelint v0.12.0+
**Status**: LOCKED (ADR-013)
**Purpose**: AST-aware code structure analysis for refactoring candidate detection

---

## Treelint-Aware Code Structure Analysis

**Use Treelint for semantic code structure analysis to detect refactoring candidates with precision.**

### Class Discovery

Locate class definitions to assess size, responsibility count, and Extract Class candidates.

```markdown
Bash(command="treelint search --type class --format json")
Bash(command="treelint search --type class --name '*Service' --format json")
Bash(command="treelint search --type class --name '*Manager' --format json")
```

### Function Discovery

Locate function definitions to assess method size, parameter count, and Extract Method candidates.

```markdown
Bash(command="treelint search --type function --format json")
Bash(command="treelint search --type function --name 'process*' --format json")
Bash(command="treelint search --type function --name 'calculate*' --format json")
```

### Supported File Extensions

Treelint supports: `.py`, `.ts`, `.tsx`, `.js`, `.jsx`, `.rs`, `.md`

For unsupported languages (`.cs`, `.java`, `.go`), see Fallback section below.

---

## JSON Response Parsing for Refactoring Analysis

**Parse Treelint JSON output to extract structured information for code smell detection.**

### Required Fields

| Field | Description | Refactoring Usage |
|-------|-------------|-------------------|
| `name` field | Class/function name | Identify target entity by semantic name |
| `file` field | File path | Locate source code for Read() operations |
| `lines` field | Line range `{"start": N, "end": M}` | Calculate entity size for smell thresholds |
| `signature` field | Full function signature | Analyze parameter count for Long Parameter List |

### Line Range Calculation for Code Smell Detection

Calculate entity size from Treelint line range to detect size-based code smells:

```markdown
# Line range calculation: end - start = entity size in lines
entity_size = lines["end"] - lines["start"]

# Equivalent index notation: lines[1] - lines[0]
# Where lines[0] = start line, lines[1] = end line

# Apply thresholds:
IF entity_size > 500 AND type == "class":
    Flag as God Object candidate
IF entity_size > 50 AND type == "function":
    Flag as Long Method candidate
```

### Parameter Count from Signature

Extract parameter count from the `signature` field to detect Long Parameter List smell:

```markdown
# Parse signature to count parameters
# Example: "def process_order(self, order_id, customer, items, discount, shipping, tax)"
# Parameter count = 6 (excluding self) -> exceeds threshold of >4 params

FOR each result in treelint_output.results:
    signature = result.signature
    param_count = count_parameters(signature)
    IF param_count > 4:
        Flag as Long Parameter List candidate
```

### Parsing Pattern

```markdown
FOR each result in treelint_output.results:
    # Extract name for identification
    entity_name = result.name

    # Extract file and line range for targeted reading
    file_path = result.file
    start_line = result.lines.start
    end_line = result.lines.end

    # Calculate size from line range
    entity_size = end_line - start_line

    # Use signature for parameter analysis
    method_signature = result.signature

    # Targeted Read with line range
    Read(file_path=file_path, offset=start_line, limit=end_line - start_line + 1)
```

---

## Treelint-Powered Code Smell Detection

Four refactoring patterns powered by Treelint AST analysis.

### Pattern 1: God Object Detection

**Smell**: Class with too many responsibilities, exceeding >500 lines.

**Detection via Treelint**:

```markdown
# Step 1: Search all classes
Bash(command="treelint search --type class --format json")

# Step 2: Calculate class size from line range
FOR each class_result in results:
    class_size = class_result.lines.end - class_result.lines.start
    IF class_size > 500:
        Flag: "God Object detected: {class_result.name} is {class_size} lines"
        # Check member count for confirmation
        method_count = len(class_result.members.methods)
        IF method_count > 20:
            Confirm: "God Object: {method_count} methods in {class_result.name}"
```

**Refactoring**: Extract Class - split into focused, single-responsibility classes.

**Treelint Advantage**: Line range from AST gives exact class size including all nested members, unlike Grep which misses class boundaries.

### Pattern 2: Long Method Detection

**Smell**: Function/method exceeding >50 lines, too complex for single responsibility.

**Detection via Treelint**:

```markdown
# Step 1: Search all functions
Bash(command="treelint search --type function --format json")

# Step 2: Calculate function size from line range
FOR each func_result in results:
    method_size = func_result.lines.end - func_result.lines.start
    IF method_size > 50:
        Flag: "Long Method detected: {func_result.name} is {method_size} lines"
        # Read the function for Extract Method analysis
        Read(file_path=func_result.file, offset=func_result.lines.start, limit=method_size)
```

**Refactoring**: Extract Method - break into smaller, focused methods.

**Treelint Advantage**: AST-aware function boundaries are exact, unlike Grep which cannot determine where a function ends.

### Pattern 3: Extract Class Candidates via Ranked File Map

**Smell**: Files with high symbol density indicate classes doing too much.

**Detection via Treelint**:

```markdown
# Step 1: Generate ranked file importance map
Bash(command="treelint map --ranked --format json --top 20")

# Step 2: Prioritize files with highest symbol density for refactoring
FOR each file_entry in ranked_results.files:
    IF file_entry.complexity > 15 OR file_entry.references > 40:
        Flag: "Extract Class candidate: {file_entry.path} (complexity={file_entry.complexity})"
        # Load file for detailed analysis
        Read(file_path=file_entry.path)
```

**Refactoring**: Extract Class - decompose high-complexity files into multiple classes.

**Integration with Step 1 (Detect Code Smells)**: Use the ranked map to prioritize which files to analyze first, focusing refactoring effort on the highest impact files.

### Pattern 4: Long Parameter List Detection

**Smell**: Functions with more than 4 parameters indicate needed parameter objects.

**Detection via Treelint**:

```markdown
# Step 1: Search all functions
Bash(command="treelint search --type function --format json")

# Step 2: Analyze signature for parameter count
FOR each func_result in results:
    signature = func_result.signature
    # Count comma-separated parameters in signature
    # Exclude 'self', 'cls' for Python methods
    param_count = count_params(signature)
    IF param_count > 4:
        Flag: "Long Parameter List: {func_result.name} has {param_count} parameters"
```

**Refactoring**: Introduce Parameter Object - group related parameters into a class/dataclass.

**Treelint Advantage**: Signature field provides the complete parameter list without needing to parse source code manually.

---

## Ranked File Map for Refactoring Prioritization

**Use `treelint map --ranked` to prioritize which files need refactoring most urgently.**

### Command

```markdown
Bash(command="treelint map --ranked --format json --top 20")
```

### JSON Output Structure

```json
{
  "files": [
    {"path": "src/core/engine.py", "rank": 1, "score": 95.2, "references": 47, "complexity": 12},
    {"path": "src/api/router.py", "rank": 2, "score": 82.1, "references": 38, "complexity": 8}
  ],
  "total_files": 127,
  "returned": 20
}
```

### Prioritization Strategy

Files are ranked by score which combines symbol density, reference count, and complexity:

- **Higher `score`** = more important file, higher refactoring impact
- **Higher `references`** = more dependents affected by changes (proceed with caution)
- **Higher `complexity`** = most complex file, likely candidate for decomposition

**Workflow Integration**: Run ranked map as the first step when beginning refactoring to identify the most impactful files to target. This ensures refactoring effort focuses on the highest-value targets.

---

## Fallback: Grep for Unsupported Languages

**When Treelint is unavailable or file type is unsupported, fall back to native Grep tool.**

### Fallback Conditions

Use Grep fallback when:

1. **Unsupported file type** (`.cs`, `.java`, `.go`, `.rb`, `.php`)
2. **Exit code 127** - binary not found
3. **Exit code 126** - permission denied
4. **Runtime failure** - exit code 1+ (runtime error)
5. **Malformed JSON** - JSON parse error in output

### Warning-Level Messaging

**All fallback events use warning-level messaging (never HALT):**

```markdown
Display: "Treelint fallback: {reason}, using Grep"
```

Examples:
- `Treelint fallback: .cs files not supported, using Grep`
- `Treelint fallback: binary not found, using Grep`
- `Treelint fallback: permission denied, using Grep`
- `Treelint fallback: runtime failure (exit 1), using Grep`
- `Treelint fallback: malformed JSON output, using Grep`

**Workflow continues normally after warning - no exception propagation.**

### Native Grep Tool Fallback Patterns

```markdown
# Class detection fallback (per language)
Grep(pattern="class\\s+\\w+", glob="**/*.py")
Grep(pattern="class\\s+\\w+", glob="**/*.cs")
Grep(pattern="class\\s+\\w+", glob="**/*.java")

# Function detection fallback (per language)
Grep(pattern="def\\s+\\w+\\(", glob="**/*.py")
Grep(pattern="(public|private|protected).*\\w+\\s*\\(", glob="**/*.cs")
Grep(pattern="func\\s+\\w+\\(", glob="**/*.go")
```

### Empty Results vs Command Failure

**CRITICAL**: Distinguish between valid empty results and actual command failures.

- **Exit code 0 with empty results** is NOT a failure - the query succeeded but found no matches. Do NOT fall back to Grep.
- **Non-zero exit code** indicates a command failure - fall back to Grep and emit warning.

```markdown
IF treelint exit_code == 0:
    # Valid result - even if results array is empty
    return treelint_output.results  # May be []

IF treelint exit_code != 0:
    # Command failure - use Grep fallback
    Display: "Treelint fallback: command failure (exit {exit_code}), using Grep"
    return grep_fallback_results()
```

---

## References

- **ADR-013**: Treelint Integration for AST-Aware Code Search (APPROVED)
- **tech-stack.md**: AST-Aware Code Search Tools section (Treelint v0.12.0+)
- **anti-patterns.md**: Category 11 (Code search tool selection guidance)
- **Shared Reference**: `.claude/agents/references/treelint-search-patterns.md` (STORY-361)
- **Backend-Architect Pattern**: `.claude/agents/backend-architect/references/treelint-patterns.md` (STORY-365)

---

**Document Version**: 1.0
**Last Updated**: 2026-02-07
**Story**: STORY-367

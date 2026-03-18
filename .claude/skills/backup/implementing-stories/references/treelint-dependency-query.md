# Treelint Dependency Query Service

**Purpose:** Query function call relationships via `treelint deps --calls` for impact analysis during refactoring and code review.

**Reference:** ADR-013 (Treelint Integration), STORY-370

---

## Command Syntax

```bash
treelint deps --calls --symbol <name> --format json
```

### Command Flags

| Flag | Required | Description |
|------|----------|-------------|
| `--calls` | Yes | Query function call relationships (callers and callees) |
| `--symbol` | Yes | Symbol name to query (function, method, or class) |
| `--format json` | Yes | Output in JSON format for AI consumption |

### Example Invocation

```bash
# Query callers and callees for a function
Bash(command="treelint deps --calls --symbol validateInput --format json", timeout=5000)
```

---

## JSON Output Structure

### Success Response

```json
{
  "symbol": "validateInput",
  "callers": [
    {"name": "processForm", "file": "src/handlers/form.py", "line": 42},
    {"name": "handleRequest", "file": "src/api/routes.py", "line": 115}
  ],
  "callees": [
    {"name": "sanitizeString", "file": "src/utils/sanitize.py", "line": 28},
    {"name": "checkLength", "file": "src/utils/validate.py", "line": 55},
    {"name": "logValidation", "file": "src/logging/audit.py", "line": 12}
  ]
}
```

### Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `"symbol"` | string | The queried symbol name |
| `"callers"` | array | List of functions that call this symbol |
| `"callees"` | array | List of functions called by this symbol |

### Caller/Callee Entry Structure

Each entry in `callers` or `callees` array contains:

| Field | Type | Description |
|-------|------|-------------|
| `"name"` | string | Function/method name |
| `"file"` | string | Relative file path from project root |
| `"line"` | number | Line number (positive integer) |

---

## JSON Parsing

### Parsing Instructions

1. **Extract symbol as string:**
   ```
   parsed_symbol = response["symbol"]  # Type: string
   ```

2. **Extract callers as list:**
   ```
   callers_list = response["callers"]  # Type: array of objects
   ```

3. **Extract callees as list:**
   ```
   callees_list = response["callees"]  # Type: array of objects
   ```

4. **Validate field types:**
   - `symbol`: Must be non-empty string
   - `callers`: Must be array (may be empty)
   - `callees`: Must be array (may be empty)
   - Each entry `name`: string
   - Each entry `file`: string (relative path)
   - Each entry `line`: positive integer (number > 0)

### Malformed JSON Handling

When JSON parsing fails (invalid JSON, missing required fields):
- Do NOT crash
- Return structured error object (see Error Handling section)
- Log parsing error for debugging

---

## Error Handling

### Error Types

| Error Type | Trigger Condition |
|------------|-------------------|
| `symbol_not_found` | Queried symbol does not exist in index |
| `daemon_not_running` | Treelint daemon socket unavailable |
| `treelint_unavailable` | Treelint CLI not installed (exit code 127) |
| `unknown_error` | Any other unexpected error |

### Structured Error Object

When errors occur, return a structured error object:

```json
{
  "error_type": "symbol_not_found",
  "queried_symbol": "nonExistentFunction",
  "message": "Symbol 'nonExistentFunction' not found in Treelint index"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `error_type` | string | One of: symbol_not_found, daemon_not_running, treelint_unavailable, unknown_error |
| `queried_symbol` | string | The original symbol name that was queried |
| `message` | string | Human-readable error description |

---

## Fallback Chain

### 3-tier Fallback Strategy

The fallback chain order is: daemon → CLI → Grep

```
Tier 1: Treelint Daemon → Tier 2: Treelint CLI → Tier 3: Grep Text Search
```

| Tier | Mode | Data Source Marker | When Used |
|------|------|-------------------|-----------|
| 1 | Daemon | `treelint-daemon` | Daemon socket available |
| 2 | CLI | `treelint-cli` | Daemon unavailable, CLI installed |
| 3 | Grep | `grep-approximation` | Treelint not installed (exit code 127) |

### Exit Code 127 Handling

When Bash returns exit code 127 (command not found):
- Set `error_type`: `treelint_unavailable`
- Trigger Grep fallback automatically
- Mark results with `source: "grep-approximation"`

### Grep Fallback Logic

When Treelint is unavailable:
```bash
# Fallback to text-based search
Grep(pattern="def\\s+${symbol}|${symbol}\\(", glob="**/*.py")
```

**Note:** Grep fallback provides text-based approximation, not AST-aware analysis.

---

## Timeout Configuration

### 5-Second Timeout

All Treelint Bash invocations MUST include a 5-second timeout:

```bash
Bash(command="treelint deps --calls --symbol name --format json", timeout=5000)
```

**Rationale:** Prevents indefinite hangs on dead daemon sockets or unresponsive processes.

---

## Performance Requirements

### Query Timing

| Metric | Target | Condition |
|--------|--------|-----------|
| Dependency query | < 200ms | Symbols with < 50 callers/callees |
| JSON parsing | < 10ms | Responses up to 100 entries |
| Grep fallback | < 500ms | When Treelint unavailable |

### Wall-Clock Time Measurement

Measure from command invocation to output capture:
```
start_time = now()
result = Bash(command="treelint deps ...")
elapsed_ms = now() - start_time
```

---

## Integration Patterns

### Pre-Refactoring Impact Analysis

Before refactoring a function:
1. Query `treelint deps --calls --symbol functionName --format json`
2. Extract `callers` list
3. Log impact scope: `{caller_count} callers, {callee_count} callees`
4. List affected files from caller entries

### Code Review Dependency Validation

During code review of modified functions:
1. Query deps for each modified function
2. Check if callers are compatible with changes
3. Flag potentially broken call sites
4. Include Dependency Impact section in review report

---

## Data Source Markers

Results MUST include source tier for transparency:

```json
{
  "symbol": "validateInput",
  "source": "treelint-daemon",
  "callers": [...],
  "callees": [...]
}
```

| Marker | Description |
|--------|-------------|
| `treelint-daemon` | Full AST accuracy via daemon mode |
| `treelint-cli` | Full AST accuracy via CLI mode |
| `grep-approximation` | Text-based approximation (may have false positives) |

---

## Usage Examples

### Query Function Dependencies

```bash
# Query a specific function
Bash(command="treelint deps --calls --symbol processPayment --format json", timeout=5000)
```

### Handle Results

```
result = parse_json(output)

IF result.error_type:
    # Handle error
    log(f"Error querying {result.queried_symbol}: {result.message}")
ELSE:
    # Process callers and callees
    log(f"Found {len(result.callers)} callers, {len(result.callees)} callees")
    FOR caller IN result.callers:
        log(f"  Called by {caller.name} at {caller.file}:{caller.line}")
```

---

**Reference:** tech-stack.md (Treelint APPROVED), ADR-013

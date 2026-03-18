# Treelint Repository Map Reference

**Purpose:** Document the `treelint map --ranked --format json` command for generating a ranked codebase symbol map, enabling context-efficient brownfield analysis and codebase understanding.

**Version:** 1.0
**Story:** STORY-373

---

## Prerequisites

Before executing the map command, ensure the Treelint index exists:

- The `.treelint/index.db` file must be present in the project root
- If the index is missing, run `treelint index` to generate it
- The index should be up-to-date relative to source file modifications

---

## Command Usage

Generate a ranked repository map using the following command:

```bash
treelint map --ranked --format json
```

**Flags:**
- `--ranked` - Sort symbols by reference count importance (most referenced first)
- `--format json` - Output in JSON format for programmatic consumption by AI subagents

**Invocation via Bash tool:**
```
Bash(command="treelint map --ranked --format json", timeout=15000)
```

---

## JSON Response Schema

The JSON response from `treelint map --ranked --format json` contains the following structure:

```json
{
  "total_symbols": 1250,
  "total_files": 87,
  "symbols": [
    {
      "name": "validateInput",
      "type": "function",
      "rank": 1,
      "references": 142
    },
    {
      "name": "UserService",
      "type": "class",
      "rank": 2,
      "references": 98
    },
    {
      "name": "handleRequest",
      "type": "method",
      "rank": 3,
      "references": 76
    },
    {
      "name": "MAX_RETRIES",
      "type": "variable",
      "rank": 4,
      "references": 45
    }
  ]
}
```

### Top-Level Fields

| Field | Type | Description |
|-------|------|-------------|
| `"total_symbols"` | Positive integer | Total number of symbols indexed across the entire codebase |
| `"total_files"` | Positive integer | Total number of files scanned and indexed by Treelint |
| `"symbols"` | Array | Ordered array of symbol entries, sorted by ascending rank |

### Symbol Entry Fields

Each entry in the `"symbols"` array contains exactly four required fields:

| Field | Type | Description |
|-------|------|-------------|
| `"name"` | String | The symbol identifier (function name, class name, etc.) |
| `"type"` | String | Symbol category: `function`, `class`, `method`, or `variable` |
| `"rank"` | Positive integer | Importance rank where rank 1 = highest importance (most referenced) |
| `"references"` | Non-negative integer | Count of references to this symbol across the codebase |

**Type field valid values:**
- `function` - Standalone functions and procedures
- `class` - Class definitions
- `method` - Methods within classes
- `variable` - Module-level variables, constants, and exports

---

## Parsing Guidance

### Rank Order

The `"symbols"` array is sorted in ascending rank order (rank 1 first, rank 2 second, etc.). Rank 1 represents the most important symbol -- the one with the highest reference count across the codebase.

### Schema Validation Rules

When parsing the JSON response, validate the following:

1. **`"total_symbols"` equals the length of the `"symbols"` array** - If these do not match, the response may be truncated or corrupted
2. **`"total_files"` is a positive integer greater than 0** - A value of 0 indicates an indexing problem
3. **Each symbol entry contains all four required fields** (`"name"`, `"type"`, `"rank"`, `"references"`)
4. **`"name"` is a non-empty string** - Empty names indicate parsing errors
5. **`"rank"` is a positive integer** starting from 1
6. **`"references"` is a non-negative integer** (0 or higher)

### Malformed JSON Error Handling

If the JSON response is malformed or invalid JSON, the consuming subagent must return a structured error object rather than crashing:

```json
{
  "error_type": "json_parse_error",
  "message": "Failed to parse treelint map response: invalid JSON at position 1024"
}
```

### Truncated Response Handling

If the response appears to be truncated (incomplete JSON or partial response), treat it as a parse error. Common indicators:
- JSON does not end with `}`
- `"symbols"` array is not properly closed with `]`
- The `"total_symbols"` count does not match the actual array length

---

## Top-N Symbol Filtering

### Purpose

Large codebases may contain thousands of symbols. To optimize context window usage, subagents should filter to the Top-N most important symbols using a configurable parameter K.

### Default Configuration

The default Top-N value is K=50. This provides good context coverage without overwhelming the AI agent context window. The K parameter is configurable and can be overridden per invocation.

### Filtering Logic

Given a parsed map result with N total symbols, return only the K highest-ranked symbols (ranks 1 through K). The filtered result preserves all fields per symbol entry.

**Critical:** The `"total_symbols"` field in the filtered result must still reflect the full codebase symbol count (the original unfiltered total), NOT the filtered count. This enables the consumer to calculate the context coverage ratio: K/total_symbols.

For example, if a codebase has 5,000 symbols and the consumer requests the top 50, the filtered result contains 50 symbol entries but `"total_symbols"` remains 5,000. The coverage ratio is 50/5000 = 1%.

### Clamping Rules (BR-004)

The Top-N parameter K is validated and clamped as follows:

| Input | Behavior |
|-------|----------|
| K < 1 (e.g., K=0) | Clamped to minimum of 1 -- at least one symbol is always returned |
| K between 1 and 10,000 | Used as-is |
| K > 10,000 | Clamped to maximum cap of 10,000 to prevent excessive context usage |
| Non-integer K (e.g., K="abc") | Rejected with validation error: "K must be a positive integer" |

### Edge Cases

- **K > total_symbols:** When K exceeds the total number of symbols in the codebase, all symbols are returned. The result contains all N symbols where N < K.
- **K=1:** Returns only the single most important symbol (rank 1). Useful for identifying the primary entry point or most-referenced function.
- **Empty codebase:** Returns an empty symbols array regardless of K value.

---

## Error Handling and Failure Modes

### Structured Error Response

All error conditions return a structured error object with consistent fields:

```json
{
  "error_type": "treelint_unavailable",
  "message": "Treelint CLI not found. Exit code 127. Falling back to Grep-based enumeration.",
  "data_source": "grep-approximation"
}
```

**Fields:**
- `error_type` - One of the 6 defined error types (see below)
- `message` - Human-readable description of the error and any recovery action taken

### Error Types

| Error Type | Trigger | Exit Code | Recovery |
|------------|---------|-----------|----------|
| `treelint_unavailable` | Treelint CLI not installed or not in PATH | 127 | Fall back to Grep-based enumeration |
| `empty_codebase` | No indexable source files found | 0 | Return empty symbols array (this is a valid success, not an error -- total_symbols: 0 with appropriate total_files count) |
| `stale_index` | `.treelint/index.db` is older than most recent source file | 0 | Return results with staleness warning flag (stale_index: true) |
| `daemon_not_running` | Treelint daemon socket not responding | Non-zero | Fall back to CLI mode |
| `index_corrupted` | `.treelint/index.db` is unreadable or contains invalid data | Non-zero | Regenerate index or fall back to Grep |
| `unknown_error` | Any unrecognized error condition | Varies | Log error details and fall back to next tier |

### Exit Code 127 Handling

When the Bash command returns exit code 127, this indicates the `treelint` binary is not found in the system PATH. The subagent must:

1. Set `error_type` to `treelint_unavailable`
2. Initiate Grep fallback immediately
3. Mark the result with `data_source: "grep-approximation"`

### 3-Tier Fallback Chain

The repository map service implements a 3-tier fallback chain: daemon -> CLI -> Grep.

```
Tier 1: treelint-daemon (fastest, < 5ms)
  ↓ fails (daemon_not_running, timeout)
Tier 2: treelint-cli (standard, < 10s)
  ↓ fails (treelint_unavailable, index_corrupted)
Tier 3: Grep fallback (degraded, < 3s)
```

Each tier marks results with the `data_source` field:
- `treelint-daemon` - Results from running daemon process
- `treelint-cli` - Results from direct CLI invocation
- `grep-approximation` - Results from Grep-based fallback enumeration

### Grep Fallback Behavior

When Treelint is unavailable and Grep fallback executes:

- Symbols are discovered using regex patterns: `def `, `function `, `class `, `const `, `let `, `var `
- Results are sorted in alphabetical order (not by importance)
- All symbols have `references: 0` (Grep cannot determine reference counts)
- Results are marked with `data_source: "grep-approximation"`
- Quality is degraded compared to Treelint (no semantic analysis, no ranking)

### Stale Index Detection

Staleness is detected by comparing the modification time (mtime) of `.treelint/index.db` against the most recent source file modification time:

1. Get mtime of `.treelint/index.db`
2. Find the most recently modified source file
3. If index mtime < source file mtime, the index is stale

When a stale index is detected:
- Results are still returned (stale data is better than no data)
- A staleness warning flag is included: `stale_index: true`
- The `message` field advises re-indexing: "Index is stale. Run treelint index to refresh."

### Empty Codebase Handling (BR-003)

An empty symbols array is a valid result (not an error) for codebases with no indexable symbols. This can occur when:

- The codebase contains only configuration files (.yaml, .json, .toml)
- No supported language files are present
- The project is newly initialized with no source code

The response reports `total_symbols: 0` with the appropriate `total_files` count. This is treated as a successful query, not an error condition.

---

## Performance Requirements

### Response Time Targets

All performance requirements are measured in wall-clock elapsed time:

| Scenario | Target | Metric |
|----------|--------|--------|
| Large codebase (up to 100,000 files) | < 10 seconds | p95 wall-clock time |
| Small codebase (under 10,000 files) | < 2 seconds | p95 wall-clock time |
| Daemon mode query (warm index) | < 5ms | p95 when daemon is running |
| JSON parsing (up to 50,000 symbols) | < 50ms | p95 for large responses |
| Top-N filtering (K=50 from 50,000) | < 5ms | p95 for filter operation |
| Grep fallback enumeration | < 3 seconds | p95 for Grep-based fallback |

### Timeout Configuration

All Treelint map Bash invocations use a 15-second timeout (15000ms) to prevent indefinite hangs on dead daemon sockets or unresponsive CLI processes:

```
Bash(command="treelint map --ranked --format json", timeout=15000)
```

If the command exceeds the 15s timeout, the service triggers the next tier in the fallback chain.

### Scalability

The service is designed to handle codebases with up to 50,000 symbols in a single map response without memory issues. For codebases with more than 50,000 symbols, Top-N filtering is strongly recommended to keep context window usage reasonable.

---

## Configuration

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| `default_top_n` | 50 | 1-10,000 | Default number of top symbols to return |
| `bash_timeout_seconds` | 15 | 5-60 | Timeout for Treelint map Bash invocations |

---

## Integration Points

This reference is consumed by:

- **implementing-stories skill** - During Phase 03 (Implementation) for codebase understanding
- **spec-driven-architecture skill** - During brownfield analysis (see `brownfield-map-integration.md`)
- **code-analyzer subagent** - For deep codebase analysis and metadata extraction
- **backend-architect subagent** - For understanding existing codebase structure

---

## References

- **ADR-013:** Treelint Integration for AST-Aware Code Search
- **EPIC-058:** Treelint Advanced Features
- **STORY-370:** Integrate Dependency Graph Analysis (sibling integration, same patterns)
- **tech-stack.md:** Treelint v0.12.0+ approved (Source: devforgeai/specs/context/tech-stack.md)

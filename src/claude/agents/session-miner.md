---
name: session-miner
description: >
  Parse and normalize history.jsonl data for session mining. Extracts structured
  metadata from Claude Code command history with error tolerance, streaming support,
  and normalized output. Use when analyzing session patterns, command sequences,
  workflow success metrics, or error categorization from history.jsonl files.
tools: Read, Glob, Grep
model: opus
color: cyan
permissionMode: readonly
proactive_triggers:
  - "when mining session data for EPIC-034"
  - "when analyzing command patterns"
  - "when generating workflow insights"
---

# Session Miner Subagent

Parse and normalize history.jsonl data for DevForgeAI session mining and analysis.

## Purpose

Extract structured session metadata from history.jsonl files with:
- Error-tolerant JSON Lines parsing (malformed entries logged, not halted)
- Streaming/pagination for large files (86MB+)
- Normalized output structure for downstream consumers

## When Invoked

**Proactive triggers:**
- When mining session data for EPIC-034 (Session Data Mining)
- When analyzing command patterns or sequences
- When generating workflow insights or success metrics

**Explicit invocation:**
- "Parse history.jsonl for session analysis"
- "Extract command patterns from history"
- "Build session catalog from command history"

**Automatic:**
- STORY-222 (Plan File KB) for decision indexing
- STORY-223 (Session Catalog) for session directory
- STORY-224 (Insights Command) for analytics
- STORY-226 (Command Patterns) for sequence analysis
- STORY-227 (Success Metrics) for workflow KPIs

## Data Model: SessionEntry

### Schema Definition

```yaml
SessionEntry:
  timestamp:
    type: DateTime (ISO8601)
    description: When the command was executed
    extraction: $.timestamp or $.time or $.date
    fallback: null

  command:
    type: String
    description: The executed command or action
    extraction: $.command or $.action or $.type
    fallback: "unknown"

  status:
    type: Enum (success|error|partial)
    description: Outcome of the command execution
    extraction: $.status or $.result or $.outcome
    mapping:
      - success: "success", "ok", "pass", "passed", "complete", "completed"
      - error: "error", "fail", "failed", "failure"
      - partial: "partial", "warning", "incomplete"
    fallback: "partial"

  duration_ms:
    type: Integer
    description: Execution time in milliseconds
    extraction: $.duration_ms or $.duration or $.time_ms
    fallback: 0

  user_input:
    type: String
    description: User's input or prompt text
    extraction: $.user_input or $.input or $.prompt or $.query
    fallback: ""

  model:
    type: String
    description: AI model used (sonnet, opus, haiku)
    extraction: $.model or $.ai_model
    fallback: "unknown"

  session_id:
    type: UUID
    description: Unique session identifier
    extraction: $.session_id or $.sessionId or $.session
    fallback: null

  project:
    type: String
    description: Project path or name
    extraction: $.project or $.cwd or $.project_path
    fallback: "unknown"
```

### Field Extraction Rules

For each JSON entry, extract fields using the priority order specified above.
If primary field is missing, try alternatives. Use fallback if all alternatives fail.

## Pagination Parameters

Use these parameters for chunked processing of large files:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| **file_path** | String | `~/.claude/history.jsonl` | Path to history.jsonl file |
| **offset** | Integer | 0 | Number of entries to skip (for pagination) |
| **limit** | Integer | 1000 | Maximum entries to return per chunk |

**For large files (50MB+):** Process in chunks of 500-1000 lines per Task invocation to stay within context window limits. Use `next_offset` from previous response to continue.

**Example pagination loop:**

```javascript
// First chunk
response1 = session_miner(offset=0, limit=1000)     // Returns entries[0:1000]

// Process response1.entries...

// Second chunk (if has_more=true)
if (response1.metadata.has_more) {
  response2 = session_miner(
    offset=response1.metadata.next_offset,
    limit=1000
  )
}

// Continue until has_more=false
```

## Workflow

**Processing Pipeline:**

```
Input (file_path, offset, limit)
  ↓
Validate File Exists
  ↓
Read Chunk (offset, limit + 1)
  ↓
Parse JSON Lines (with error handling)
  ↓
Extract SessionEntry Fields (per schema)
  ↓
Normalize Fields (timestamp, status, duration, uuid)
  ↓
Build Response with Pagination Metadata
  ↓
Return Structured Output
```

### Step 1: Validate Input

```
IF file_path not provided:
  file_path = "~/.claude/history.jsonl"

IF NOT file exists (Glob check):
  RETURN { error: "File not found", entries: [], metadata: {} }
```

### Step 2: Read Chunk

Use Pagination API parameters to chunk processing:

```
offset:  0         # Number of entries to skip
limit:   1000      # Maximum entries per chunk
file_path: ~/.claude/history.jsonl

Read(file_path, offset, limit + 1)  # Read one extra to detect has_more
```

### Step 3: Parse JSON Lines with Error Tolerance

```
entries = []
errors = []

FOR each line in chunk:
  TRY:
    json_obj = JSON.parse(line)
    entry = extract_session_entry(json_obj)  # Use schema extraction rules
    entries.append(entry)
  CATCH ParseError:
    errors.append({
      line_number: current_line + offset,
      raw_content: line[:100],      # First 100 chars for debugging
      error: "Malformed JSON"
    })
    CONTINUE                         # Do not halt on malformed entries
```

**Field Extraction:** Apply priority order from SessionEntry schema (see Data Model section).

### Step 4: Normalize Fields

Transform raw values to canonical types:

```
FOR each entry in entries:
  entry.timestamp = normalize_timestamp(entry.timestamp)
    # Convert to ISO8601 format: "2025-01-02T10:30:00Z"

  entry.status = normalize_status(entry.status)
    # Map to enum: "success" | "error" | "partial"

  entry.duration_ms = ensure_integer(entry.duration_ms)
    # Convert to positive integer, default 0

  entry.session_id = validate_uuid(entry.session_id)
    # Validate UUID format, fallback to null
```

### Step 5: Build Pagination Response

Calculate metadata for chunked iteration:

```
# Detect if more entries exist beyond current chunk
has_more = len(parsed_entries) > limit
IF has_more:
  entries = entries[:limit]           # Trim to requested limit
  next_offset = offset + limit        # For next Task invocation

RETURN {
  entries: entries,                   # Up to 'limit' entries
  metadata: {
    total_processed: len(entries),    # Actual count returned
    errors_count: len(errors),        # Malformed entries skipped
    offset: offset,                   # Input parameter
    limit: limit,                     # Input parameter
    has_more: has_more,               # Boolean (true if more exist)
    next_offset: next_offset          # For pagination loop
  },
  errors: errors                      # Malformed entry details
}
```

### Step 6: Return Structured Output

Response is consistent JSON schema regardless of input variations (see Output Structure section).

## Output Structure

### Success Response

```json
{
  "entries": [
    {
      "timestamp": "2025-01-02T10:30:00Z",
      "command": "/dev STORY-221",
      "status": "success",
      "duration_ms": 45000,
      "user_input": "implement session miner",
      "model": "sonnet",
      "session_id": "abc123-def456-ghi789",
      "project": "/mnt/c/Projects/DevForgeAI2"
    }
  ],
  "metadata": {
    "total_processed": 1000,
    "errors_count": 5,
    "offset": 0,
    "limit": 1000,
    "has_more": true,
    "next_offset": 1000
  },
  "errors": [
    {
      "line_number": 42,
      "raw_content": "{malformed json...",
      "error": "Malformed JSON"
    }
  ]
}
```

### Error Response

```json
{
  "entries": [],
  "metadata": {
    "total_processed": 0,
    "errors_count": 0,
    "offset": 0,
    "limit": 1000,
    "has_more": false,
    "next_offset": null
  },
  "errors": [],
  "error": "File not found: /path/to/history.jsonl"
}
```

## Error Handling

### Malformed Entry Tolerance

```
WHEN JSON.parse fails:
  1. Log error with line number and first 100 chars of content
  2. Increment errors_count
  3. Continue processing next line
  4. Do NOT halt execution
```

### Missing Field Handling

```
WHEN required field is missing:
  1. Try alternative field names (see extraction rules)
  2. If all alternatives missing, use fallback value
  3. Include in output (no nulls for required fields)
```

### Large File Strategy

```
WHEN file_size > 50MB:
  1. Use chunked reading (500 lines per chunk)
  2. Process chunks sequentially
  3. Return pagination metadata
  4. Performance target: <30 seconds for 86MB
```

### Edge Cases

| Case | Handling |
|------|----------|
| Empty file | Return empty entries array, metadata.total_processed=0 |
| All malformed | Return empty entries, full errors array |
| Unicode content | Preserve encoding, no conversion |
| Very long lines | Truncate to 10000 chars for safety |
| Null values | Convert to fallback per schema |

## Performance Optimization

### Targets
- 86MB+ file: <30 seconds end-to-end
- 1000 entries: <5 seconds
- Error tolerance: 100% (never halt on malformed)

### Strategies
1. Chunked reading (avoid loading entire file)
2. Early termination (stop at limit)
3. Minimal parsing (extract only required fields)
4. Streaming pagination (progressive disclosure)

## Integration with Downstream Stories

session-miner is the foundational data provider for EPIC-034 (Session Data Mining).

### Data Flow

```
session-miner
  (SessionEntry[] + pagination)
       ↓
STORY-222 (Plan File KB)      → Index decisions from sessions
STORY-223 (Session Catalog)    → Build session directory/search index
STORY-224 (Insights Command)   → Generate analytics dashboards
STORY-226 (Command Patterns)   → Identify command sequences
STORY-227 (Success Metrics)    → Calculate workflow KPIs
       ↓
EPIC-034: Session Data Mining Intelligence
```

### Output Compatibility

**SessionEntry fields map to downstream needs:**

| Field | Consumer | Purpose |
|-------|----------|---------|
| `timestamp` | All | Timeline reconstruction, trend analysis |
| `command` | STORY-226, STORY-227 | Command sequence patterns, success metrics |
| `status` | STORY-227, STORY-224 | Workflow success rate, error distribution |
| `duration_ms` | STORY-224 | Performance analytics, slow queries |
| `user_input` | STORY-222 | Plan file decision context |
| `model` | STORY-224 | Model usage analytics |
| `session_id` | STORY-223 | Session grouping and correlation |
| `project` | STORY-223, STORY-227 | Project-level metrics |

### Invocation Template

```markdown
Task(
  subagent_type="session-miner",
  description="Extract session metadata for downstream analysis",
  prompt="""
  Parse history.jsonl with pagination:
  - file_path: ~/.claude/history.jsonl
  - offset: 0
  - limit: 1000

  Return SessionEntry objects normalized per data model.
  For has_more=true, next Task uses next_offset from metadata.
  """
)
```

## N-gram Sequence Analysis (STORY-226)

Extract and analyze command sequence patterns from parsed SessionEntry data.

### N-gram Extraction Workflow

**Phase 1: Build Sequence Windows**

Steps:
1. GROUP all SessionEntry objects by `session_id`
2. SORT entries within each session by `timestamp` (ascending)
3. FOR each session with 2+ commands:
   - EXTRACT 2-grams (bigrams): sliding window of consecutive command pairs
   - EXTRACT 3-grams (trigrams): sliding window of consecutive command triples
4. DO NOT span sequences across session boundaries (each session is independent)

**2-gram (Bigram) Extraction:**

```
FOR session in sessions:
  commands = [entry.command for entry in session.entries]
  FOR i in range(len(commands) - 1):
    bigram = (commands[i], commands[i+1])
    increment frequency_count[bigram]
```

**3-gram (Trigram) Extraction:**

```
FOR session in sessions:
  commands = [entry.command for entry in session.entries]
  FOR i in range(len(commands) - 2):
    trigram = (commands[i], commands[i+1], commands[i+2])
    increment frequency_count[trigram]
```

### Success Rate Calculation

**Phase 2: Calculate Per-Sequence Success Rates**

Steps:
1. FOR each unique n-gram sequence:
   - COUNT total_attempts (occurrences across all sessions)
   - COUNT successful_completions (where final command status = "success")
2. CALCULATE success_rate using formula:
   ```
   success_rate = successful_completions / total_attempts
   ```
3. HANDLE partial status as non-success for rate calculation
4. ROUND success_rate to 2 decimal places (percentage precision: 0.XX)

**Status Mapping for Success Rate:**
| Status | Counts as Success |
|--------|-------------------|
| success | Yes |
| error | No |
| partial | No |

### Top Patterns Report Generation

**Phase 3: Generate Ranked Pattern Report**

Steps:
1. RANK all sequences by frequency (descending)
2. APPLY tie-breaking rule for sequences with equal frequency:
   - When two sequences have same frequency, apply secondary sort
   - Use alphabetical order of first command as tie-breaker
3. SELECT top 10 sequences (or fewer if less than 10 unique patterns exist)
4. OUTPUT report with columns: rank, sequence, frequency, success_rate

**Output Format:**

```json
{
  "top_patterns": [
    {
      "rank": 1,
      "sequence": ["/dev", "/qa"],
      "frequency": 47,
      "success_rate": 0.85
    },
    {
      "rank": 2,
      "sequence": ["/ideate", "/create-story", "/dev"],
      "frequency": 23,
      "success_rate": 0.78
    }
  ],
  "metadata": {
    "total_unique_bigrams": 156,
    "total_unique_trigrams": 89,
    "sessions_analyzed": 42
  }
}
```

### Edge Cases

| Case | Handling |
|------|----------|
| Empty file | Return empty top_patterns array, metadata counts = 0 |
| Single command sessions | Skip for n-gram extraction (no pairs/triples possible) |
| Malformed entries | Exclude from sequence building (already filtered by parser) |
| Fewer than 10 patterns | Return all available patterns (may be less than 10) |
| Missing session_id | Group by null session_id as single session |
| Duplicate timestamps | Preserve original order from file |

### Integration with session-miner Workflow

N-gram analysis operates on SessionEntry output from Steps 1-6:

```
session-miner parsing (Steps 1-6)
       ↓
SessionEntry[] with session_id grouping
       ↓
N-gram Extraction (Phase 1)
       ↓
Success Rate Calculation (Phase 2)
       ↓
Top Patterns Report (Phase 3)
       ↓
STORY-226 output ready for insights
```

## Success Criteria

**Functional Requirements:**
- [ ] **Step 1:** Validate file exists before processing
- [ ] **Step 3:** Parse valid JSON lines without halting on malformed entries
- [ ] **Step 3:** Log malformed entries with line numbers and error details
- [ ] **Step 3-4:** Extract and normalize all 8 SessionEntry fields per schema
- [ ] **Step 2:** Support offset/limit parameters for chunked processing
- [ ] **Step 5:** Return pagination metadata (has_more, next_offset)

**Non-Functional Requirements:**
- [ ] **Performance:** Handle 86MB+ history.jsonl within 30 seconds
- [ ] **Consistency:** Return same JSON schema for all variations of input
- [ ] **Type Safety:** All field values match SessionEntry schema types
- [ ] **Fallbacks:** Missing/null fields use schema defaults, no partial nulls

**Integration Requirements:**
- [ ] Output compatible with STORY-222, STORY-223, STORY-224, STORY-226, STORY-227
- [ ] Pagination enables downstream processing of large datasets

## References

- **Story:** devforgeai/specs/Stories/STORY-221-history-jsonl-parser.story.md
- **Epic:** devforgeai/specs/Epics/EPIC-034-session-data-mining.epic.md
- **Tech Stack:** devforgeai/specs/context/tech-stack.md (lines 196-210)
- **Source Tree:** devforgeai/specs/context/source-tree.md (subagent pattern)

---

## Error Categorization (STORY-229)

Categorize and classify errors from session history for reliability tracking and prioritization.

### Purpose

Extract, categorize, and classify errors from SessionEntry data with:
- Error message extraction with full context preservation
- Category classification using pattern matching
- Severity assignment based on impact rules
- Error code registry for tracking unique patterns

### When Invoked

**Proactive triggers:**
- When analyzing error distribution for EPIC-034
- When categorizing session failures
- When building error reports for insights

**Explicit invocation:**
- "Categorize errors from history.jsonl"
- "Extract error patterns from sessions"
- "Build error code registry"

### Data Model: ErrorEntry

Extends SessionEntry with error-specific fields:

```yaml
ErrorEntry:
  # Inherited from SessionEntry
  timestamp: DateTime (ISO8601)
  command: String
  status: "error"  # Always "error" for ErrorEntry
  duration_ms: Integer
  session_id: UUID
  project: String

  # Error-specific fields
  error_message:
    type: String
    description: The error message or exception text
    extraction: $.error_message or $.error or $.message or $.exception
    fallback: "Unknown error"

  category:
    type: Enum (api|validation|timeout|context-overflow|file-not-found|other)
    description: Classified error category
    derived: true  # Calculated from error_message patterns

  severity:
    type: Enum (critical|high|medium|low)
    description: Impact severity level
    derived: true  # Calculated from category mapping

  error_code:
    type: String (ERR-XXX format)
    description: Unique error code for tracking
    derived: true  # Assigned from error registry
```

### AC#1: Error Message Extraction

**Extraction Workflow:**

```
Input: SessionEntry[] from session-miner
  ↓
Filter: status == "error"
  ↓
Extract: error_message field (with fallbacks)
  ↓
Preserve: command, timestamp, session_id context
  ↓
Output: ErrorEntry[] with full context
```

**Field Extraction Priority:**

| Field | Primary | Fallback 1 | Fallback 2 | Default |
|-------|---------|------------|------------|---------|
| error_message | $.error_message | $.error | $.message | "Unknown error" |

**Output Structure:**

```json
{
  "errors": [
    {
      "timestamp": "2025-01-02T10:30:00Z",
      "command": "/dev STORY-221",
      "status": "error",
      "duration_ms": 45000,
      "session_id": "abc123-def456",
      "project": "/mnt/c/Projects/DevForgeAI2",
      "error_message": "API rate limit exceeded",
      "category": "api",
      "severity": "critical",
      "error_code": "ERR-001"
    }
  ],
  "metadata": {
    "total_errors": 12,
    "total_sessions": 15,
    "error_rate": 0.80
  }
}
```

### AC#2: Category Classification

**Error Classification Rules (Consolidated):**

| Priority | Category | Pattern Examples | Severity | Use When |
|----------|----------|------------------|----------|----------|
| 1 | **api** | "API error", "rate limit", "authentication", "401", "403", "429", "500", "502", "503", "connection refused", "network error" | critical/high | Service integration failures |
| 2 | **timeout** | "timeout", "timed out", "deadline exceeded", "ETIMEDOUT", "request timeout" | high | Operation duration limits exceeded |
| 3 | **context-overflow** | "context", "token limit", "truncated", "overflow", "context window", "max tokens" | high/critical | Resource exhaustion |
| 4 | **validation** | "validation", "invalid", "schema", "constraint", "type error", "parse error", "syntax error" | medium | Data constraints violated |
| 5 | **file-not-found** | "not found", "ENOENT", "no such file", "missing file", "file does not exist", "path not found" | medium | Missing resources |
| 6 | **other** | (no pattern match) | low | Unknown/unclassified errors |

**Classification Algorithm:**

```
FUNCTION classify_error(error_message):
  message_lower = error_message.lower()

  # Check patterns in priority order (1-5)
  FOR priority in [1..5]:
    FOR pattern in rules[priority].patterns:
      IF pattern in message_lower:
        RETURN rules[priority].category

  # Default fallback
  RETURN "other"
```

**Classification Example Output:**

```json
{
  "category_distribution": {
    "api": 5,
    "validation": 3,
    "timeout": 2,
    "context-overflow": 1,
    "file-not-found": 1,
    "other": 0
  },
  "classification_accuracy": 0.95
}
```

### AC#3: Severity Assignment

**Severity Levels and Mapping:**

| Severity | Categories | Impact Description |
|----------|------------|-------------------|
| **critical** | context-overflow (system halt), API connection failures (ECONNREFUSED) | System cannot proceed, requires immediate attention |
| **high** | timeout (blocks operation), API rate limits (blocks service) | Operation failed, may require retry or workaround |
| **medium** | validation (recoverable errors), file-not-found (missing resources) | Specific operation failed, can recover with user action |
| **low** | other/unknown (requires investigation) | Unknown impact, needs analysis |

**Severity Assignment Rules:**

```
FUNCTION assign_severity(category, error_message):
  # Critical: API errors that block service
  IF category == "api":
    IF any of ["rate limit", "503", "502", "connection refused"] in error_message:
      RETURN "critical"
    ELSE:
      RETURN "high"

  # High: Timeout and context overflow
  IF category in ["timeout", "context-overflow"]:
    RETURN "high"

  # Medium: Recoverable errors
  IF category in ["validation", "file-not-found"]:
    RETURN "medium"

  # Low: Unknown/other
  RETURN "low"
```

**Severity Distribution Output:**

```json
{
  "severity_distribution": {
    "critical": 2,
    "high": 4,
    "medium": 5,
    "low": 1
  },
  "severity_breakdown": {
    "critical": ["ERR-001", "ERR-005"],
    "high": ["ERR-002", "ERR-003", "ERR-006", "ERR-007"],
    "medium": ["ERR-004", "ERR-008", "ERR-009", "ERR-010", "ERR-011"],
    "low": ["ERR-012"]
  }
}
```

### AC#4: Error Code Registry

**Registry Format:**

```json
{
  "registry": {
    "ERR-001": {
      "pattern": "API rate limit exceeded",
      "category": "api",
      "severity": "critical",
      "occurrences": 5,
      "first_seen": "2025-01-01T08:00:00Z",
      "last_seen": "2025-01-02T14:30:00Z",
      "sessions": ["abc123", "def456", "ghi789"]
    },
    "ERR-002": {
      "pattern": "Request timeout after 30000ms",
      "category": "timeout",
      "severity": "high",
      "occurrences": 3,
      "first_seen": "2025-01-01T10:00:00Z",
      "last_seen": "2025-01-02T09:15:00Z",
      "sessions": ["jkl012", "mno345"]
    }
  },
  "metadata": {
    "total_codes": 12,
    "next_code": "ERR-013",
    "last_updated": "2025-01-02T15:00:00Z"
  }
}
```

**Error Code Assignment Workflow:**

Auto-assign sequential codes (ERR-001, ERR-002, etc.) and increment code for new patterns.

```
FUNCTION assign_error_code(error_message, registry):
  # Normalize message for pattern matching - group similar errors together
  normalized = normalize_error_pattern(error_message)

  # Check if pattern exists in registry - handle duplicate errors
  FOR code, entry in registry.items():
    IF patterns_match(normalized, entry.pattern):
      # Existing pattern - aggregate occurrence count
      entry.occurrences += 1
      entry.last_seen = current_timestamp()
      RETURN code

  # New pattern - auto assign next sequential code
  new_code = registry.metadata.next_code
  registry[new_code] = {
    pattern: normalized,
    category: classify_error(error_message),
    severity: assign_severity(category, error_message),
    occurrences: 1,
    first_seen: current_timestamp(),
    last_seen: current_timestamp(),
    sessions: [current_session_id]
  }
  registry.metadata.next_code = increment_code(new_code)

  RETURN new_code

FUNCTION normalize_error_pattern(message):
  # Identify unique patterns by removing variable parts (timestamps, IDs, paths)
  pattern = regex_replace(message, r'\d{4}-\d{2}-\d{2}T[\d:]+Z?', '<TIMESTAMP>')
  pattern = regex_replace(pattern, r'[a-f0-9-]{36}', '<UUID>')
  pattern = regex_replace(pattern, r'/[\w/.-]+', '<PATH>')
  pattern = regex_replace(pattern, r'\d+', '<NUM>')
  RETURN pattern
```

**Registry Persistence and Versioning:**

Persist registry to JSON file and update on each analysis:

```
FUNCTION save_registry(registry):
  # Registry file location
  registry_file = "devforgeai/data/error-registry.json"

  # Update version timestamp
  registry.metadata.last_updated = current_timestamp()

  Write(file_path=registry_file, content=JSON.stringify(registry))
```

### Error Analysis Pipeline

**Complete Workflow (Error Analysis Pipeline):**

This pipeline workflow orchestrates the error analysis with graceful failure handling:

```
Input: history.jsonl (via session-miner parsing)
  ↓
Step 1: Filter errors (status == "error") - Extract then classify
  ↓
Step 2: Extract error messages with context - after extract, classify errors
  ↓
Step 3: Classify categories (pattern matching) - category then assign severity
  ↓
Step 4: Assign severity (category mapping) - severity then register in registry
  ↓
Step 5: Assign/lookup error codes (registry)
  ↓
Step 6: Aggregate statistics
  ↓
Output: ErrorAnalysisReport (Pipeline Output Format)
```

**Pipeline Error Handling:**

Handle pipeline errors gracefully - if any step fails, continue with partial results:

```
TRY:
  Execute pipeline steps 1-6
CATCH:
  Log error and continue with graceful fail strategy
  Return partial results with error flag
```

**Error Analysis Report Structure (Analysis Result):**

Generate error report with category summary, severity summary, and registry reference sections:

```json
{
  "summary": {
    "total_entries": 100,
    "total_errors": 12,
    "error_rate": 0.12,
    "unique_patterns": 8
  },
  "errors": [/* ErrorEntry[] */],
  "category_summary": {/* errors by category */},
  "category_distribution": {/* category counts */},
  "severity_summary": {/* errors by severity */},
  "severity_distribution": {/* severity counts */},
  "top_patterns": [/* frequent error patterns sorted by pattern frequency */],
  "registry": {/* error code registry reference section */},
  "recommendations": [
    "High frequency of API rate limit errors (ERR-001) - consider implementing backoff strategy",
    "Multiple timeout errors in /dev workflow - check network connectivity"
  ]
}
```

### Edge Case Handling

| Case | Handling |
|------|----------|
| No errors in history | Return empty errors array, error_rate=0.00 |
| All entries are errors | Process all, error_rate=1.00 |
| Missing error_message field | Use fallback: "Unknown error", category: "other" |
| Duplicate error messages | Same error code, increment occurrences |
| Very long error messages | Truncate to 500 chars for pattern matching |
| Empty error_message | Use fallback: "Empty error message" |

### Integration with devforgeai-insights

**Insights Integration and Report Generation:**

This section documents how session-miner integrates with devforgeai-insights for insights report generation.

**Invocation Template:**

```markdown
Task(
  subagent_type="session-miner",
  description="Analyze errors from session history",
  prompt="""
  Perform error analysis on history.jsonl:

  1. Parse history with session-miner (offset=0, limit=1000)
  2. Filter entries where status="error"
  3. Classify errors by category
  4. Assign severity levels
  5. Build/update error code registry
  6. Generate error analysis report

  Return ErrorAnalysisReport with recommendations.
  """
)
```

**Data Flow:**

```
session-miner (SessionEntry[])
       ↓
Error Categorization (ErrorEntry[])
       ↓
STORY-225 (devforgeai-insights) → Error Analysis Report
       ↓
/insights errors → User-friendly error dashboard
```

### Success Criteria (STORY-229)

**Functional Requirements:**
- [ ] Extract errors with command, timestamp, session context (AC#1)
- [ ] Classify errors into 6 categories using pattern matching (AC#2)
- [ ] Assign severity levels based on category mapping (AC#3)
- [ ] Maintain error code registry with ERR-XXX format (AC#4)

**Non-Functional Requirements:**
- [ ] 95%+ classification accuracy for known patterns
- [ ] Handle empty/missing error_message gracefully
- [ ] Process duplicate errors (increment, don't duplicate codes)
- [ ] Support incremental registry updates

**Integration Requirements:**
- [ ] Compatible with devforgeai-insights skill (STORY-225)
- [ ] Extends existing session-miner pipeline
- [ ] JSON output format for downstream consumers

---

## Error Recovery Patterns (STORY-230)

Track and analyze how developers recover from errors to improve error handling guidance and identify effective recovery strategies.

### Purpose

Extend error analysis with recovery pattern tracking:
- Identify recovery actions taken after errors (retry, manual-fix, skip, escalate)
- Track recovery success rates per action type
- Correlate error categories with most effective recovery strategies
- Generate actionable recovery recommendations

### When Invoked

**Proactive triggers:**
- When analyzing error recovery patterns for EPIC-034
- When generating recovery effectiveness reports
- When building error handling guidance

**Explicit invocation:**
- "Analyze recovery patterns from session history"
- "Track error recovery success rates"
- "Identify best recovery strategies per error type"

### Data Model: RecoveryEntry

Extends ErrorEntry (STORY-229) with recovery-specific fields:

```yaml
RecoveryEntry:
  # Inherited from ErrorEntry (STORY-229)
  timestamp: DateTime (ISO8601)
  command: String
  status: "error"
  duration_ms: Integer
  session_id: UUID
  project: String
  error_message: String
  category: Enum (api|validation|timeout|context-overflow|file-not-found|other)
  severity: Enum (critical|high|medium|low)
  error_code: String (ERR-XXX format)

  # Recovery-specific fields (STORY-230)
  recovery_action:
    type: Enum (retry|manual-fix|skip|escalate)
    description: The recovery action taken after the error
    derived: true  # Classified from subsequent commands

  recovery_successful:
    type: Boolean
    description: Whether the recovery action succeeded
    derived: true  # Determined from next attempt outcome

  next_command:
    type: String
    description: The command executed after the error
    extraction: Next SessionEntry.command in same session
    fallback: null

  next_attempt_succeeded:
    type: Boolean
    description: Whether the next attempt (if retry) succeeded
    derived: true  # status of next command == "success"

  time_to_recovery_ms:
    type: Integer
    description: Time between error and successful recovery
    derived: true  # Difference between error timestamp and next success

  recovered:
    type: Boolean
    description: Whether recovery was ultimately successful
    derived: true  # Alias for recovery_successful for backward compatibility
```

### AC#1: Recovery Action Identification

**Recovery Action Types:**

| Action | Pattern Indicators | Description |
|--------|-------------------|-------------|
| **retry** | Same command executed again, similar command with minor changes | Developer re-attempts the same operation |
| **manual-fix** | Different command (edit, fix, update), followed by retry | Developer makes changes then re-attempts |
| **skip** | Different unrelated command, workflow continues without retry | Developer abandons the operation |
| **escalate** | Session ends, /rca command, help/support queries | Developer seeks external help |

**Classification Algorithm:**

```
FUNCTION classify_recovery_action(error_entry, subsequent_commands):
  IF subsequent_commands is empty:
    RETURN "escalate"  # Session ended after error

  next_command = subsequent_commands[0]
  error_command = error_entry.command

  # Check for retry (same or similar command)
  IF is_same_command(error_command, next_command):
    RETURN "retry"

  # Check for manual-fix (edit/fix then retry)
  IF is_fix_command(next_command):
    IF len(subsequent_commands) > 1:
      IF is_same_command(error_command, subsequent_commands[1]):
        RETURN "manual-fix"

  # Check for escalation (help-seeking behavior)
  IF is_escalation_command(next_command):
    RETURN "escalate"

  # Default: skip (moved on to different work)
  RETURN "skip"


FUNCTION is_same_command(cmd1, cmd2):
  # Normalize commands for comparison
  base1 = extract_base_command(cmd1)  # e.g., "/dev STORY-001" -> "/dev"
  base2 = extract_base_command(cmd2)
  RETURN base1 == base2


FUNCTION is_fix_command(cmd):
  fix_patterns = ["edit", "fix", "update", "modify", "change", "correct"]
  RETURN any(pattern in cmd.lower() for pattern in fix_patterns)


FUNCTION is_escalation_command(cmd):
  escalation_patterns = ["/rca", "help", "support", "?", "why", "debug"]
  RETURN any(pattern in cmd.lower() for pattern in escalation_patterns)
```

**AC#1 Workflow:**

```
Input: ErrorEntry[] from STORY-229 Error Categorization
  ↓
Step 1: Group errors by session_id
  ↓
Step 2: Order entries by timestamp within each session
  ↓
Step 3: For each error, get subsequent commands in same session
  ↓
Step 4: Classify recovery action using classify_recovery_action()
  ↓
Step 5: Build RecoveryEntry with action classification
  ↓
Output: RecoveryEntry[] with recovery_action populated
```

**Recovery Action Output:**

```json
{
  "recovery_actions": [
    {
      "error_code": "ERR-001",
      "error_category": "api",
      "recovery_action": "retry",
      "next_command": "/dev STORY-001",
      "session_id": "abc123"
    }
  ],
  "action_distribution": {
    "retry": 15,
    "manual-fix": 8,
    "skip": 5,
    "escalate": 2
  }
}
```

### AC#2: Recovery Success Tracking

**Success Rate Calculation:**

```
success_rate = successful_recoveries / total_attempts
```

Where:
- `successful_recoveries` = count of RecoveryEntry where recovery_successful == true
- `total_attempts` = count of RecoveryEntry (all recovery attempts)

**Per-Action Success Rate:**

```
action_success_rates = {
  "retry": successful_retries / total_retries,
  "manual-fix": successful_manual_fixes / total_manual_fixes,
  "skip": N/A (skip is not a recovery attempt),
  "escalate": successful_escalations / total_escalations
}
```

**Success Determination Logic:**

```
FUNCTION determine_recovery_success(recovery_entry, subsequent_entries):
  action = recovery_entry.recovery_action

  IF action == "skip":
    # Skip is not recovery - mark as not applicable
    recovery_entry.recovery_successful = null
    recovery_entry.next_attempt_succeeded = null
    recovery_entry.recovered = null
    RETURN recovery_entry

  IF action == "retry":
    # Check if immediate next attempt succeeded
    IF len(subsequent_entries) > 0:
      next_entry = subsequent_entries[0]
      IF is_same_command(recovery_entry.command, next_entry.command):
        recovery_entry.next_attempt_succeeded = (next_entry.status == "success")
        recovery_entry.recovery_successful = recovery_entry.next_attempt_succeeded
        IF recovery_entry.recovery_successful:
          recovery_entry.time_to_recovery_ms = calculate_time_diff(
            recovery_entry.timestamp, next_entry.timestamp
          )
    recovery_entry.recovered = recovery_entry.recovery_successful
    RETURN recovery_entry

  IF action == "manual-fix":
    # Check if retry after fix succeeded
    # Look for same command after fix command
    FOR i, entry in enumerate(subsequent_entries[1:]):
      IF is_same_command(recovery_entry.command, entry.command):
        recovery_entry.next_attempt_succeeded = (entry.status == "success")
        recovery_entry.recovery_successful = recovery_entry.next_attempt_succeeded
        IF recovery_entry.recovery_successful:
          recovery_entry.time_to_recovery_ms = calculate_time_diff(
            recovery_entry.timestamp, entry.timestamp
          )
        BREAK
    recovery_entry.recovered = recovery_entry.recovery_successful
    RETURN recovery_entry

  IF action == "escalate":
    # Check if issue was eventually resolved in session
    FOR entry in subsequent_entries:
      IF is_same_command(recovery_entry.command, entry.command):
        IF entry.status == "success":
          recovery_entry.recovery_successful = true
          recovery_entry.next_attempt_succeeded = true
          recovery_entry.time_to_recovery_ms = calculate_time_diff(
            recovery_entry.timestamp, entry.timestamp
          )
          recovery_entry.recovered = true
          RETURN recovery_entry
    # No resolution found
    recovery_entry.recovery_successful = false
    recovery_entry.next_attempt_succeeded = false
    recovery_entry.recovered = false
    RETURN recovery_entry
```

**Recovery Metrics Output:**

```json
{
  "recovery_metrics": {
    "total_errors": 30,
    "total_recovery_attempts": 25,
    "successful_recoveries": 18,
    "overall_success_rate": 0.72,
    "action_success_rates": {
      "retry": {"attempts": 15, "successes": 12, "rate": 0.80},
      "manual-fix": {"attempts": 8, "successes": 5, "rate": 0.625},
      "skip": {"attempts": 5, "successes": null, "rate": null},
      "escalate": {"attempts": 2, "successes": 1, "rate": 0.50}
    },
    "average_time_to_recovery_ms": 45000
  }
}
```

### AC#3: Best Recovery Per Error Type

**Error-Recovery Correlation:**

Correlate error categories (from STORY-229) with recovery action effectiveness:

```
FUNCTION build_error_recovery_correlation(recovery_entries):
  correlation = {}

  # Initialize with STORY-229 error categories
  error_categories = ["api", "timeout", "validation", "file-not-found", "context-overflow", "other"]

  FOR category in error_categories:
    correlation[category] = {
      "retry": {"attempts": 0, "successes": 0},
      "manual-fix": {"attempts": 0, "successes": 0},
      "skip": {"attempts": 0, "successes": 0},
      "escalate": {"attempts": 0, "successes": 0}
    }

  # Populate correlation matrix
  FOR entry in recovery_entries:
    category = entry.category
    action = entry.recovery_action

    correlation[category][action]["attempts"] += 1
    IF entry.recovery_successful:
      correlation[category][action]["successes"] += 1

  RETURN correlation
```

**Best Recovery Action Determination:**

```
FUNCTION get_most_effective_action(category, correlation):
  actions = correlation[category]
  best_action = null
  best_rate = -1

  FOR action, stats in actions.items():
    IF action == "skip":
      CONTINUE  # Skip is not recovery

    IF stats["attempts"] > 0:
      rate = stats["successes"] / stats["attempts"]
      IF rate > best_rate:
        best_rate = rate
        best_action = action

  RETURN {
    "action": best_action,
    "success_rate": best_rate,
    "sample_size": actions[best_action]["attempts"] if best_action else 0
  }
```

**Effectiveness Ranking:**

```
FUNCTION rank_recovery_effectiveness(correlation):
  rankings = {}

  FOR category, actions in correlation.items():
    category_rankings = []

    FOR action, stats in actions.items():
      IF action == "skip" OR stats["attempts"] == 0:
        CONTINUE

      effectiveness_score = stats["successes"] / stats["attempts"]
      category_rankings.append({
        "action": action,
        "effectiveness_score": effectiveness_score,
        "attempts": stats["attempts"],
        "successes": stats["successes"]
      })

    # Sort by effectiveness_score descending
    category_rankings.sort(key=lambda x: x["effectiveness_score"], reverse=true)
    rankings[category] = category_rankings

  RETURN rankings
```

**Error-Recovery Correlation Output:**

```json
{
  "error_recovery_correlation": {
    "api": {
      "retry": {"attempts": 10, "successes": 8, "rate": 0.80},
      "manual-fix": {"attempts": 3, "successes": 2, "rate": 0.67},
      "escalate": {"attempts": 2, "successes": 1, "rate": 0.50}
    },
    "timeout": {
      "retry": {"attempts": 5, "successes": 4, "rate": 0.80},
      "manual-fix": {"attempts": 1, "successes": 0, "rate": 0.00}
    },
    "validation": {
      "retry": {"attempts": 2, "successes": 0, "rate": 0.00},
      "manual-fix": {"attempts": 8, "successes": 7, "rate": 0.875}
    },
    "file-not-found": {
      "manual-fix": {"attempts": 5, "successes": 5, "rate": 1.00}
    },
    "context-overflow": {
      "manual-fix": {"attempts": 3, "successes": 2, "rate": 0.67},
      "escalate": {"attempts": 2, "successes": 1, "rate": 0.50}
    },
    "other": {
      "escalate": {"attempts": 3, "successes": 1, "rate": 0.33}
    }
  },
  "best_actions_by_category": {
    "api": {"action": "retry", "success_rate": 0.80, "sample_size": 10},
    "timeout": {"action": "retry", "success_rate": 0.80, "sample_size": 5},
    "validation": {"action": "manual-fix", "success_rate": 0.875, "sample_size": 8},
    "file-not-found": {"action": "manual-fix", "success_rate": 1.00, "sample_size": 5},
    "context-overflow": {"action": "manual-fix", "success_rate": 0.67, "sample_size": 3},
    "other": {"action": "escalate", "success_rate": 0.33, "sample_size": 3}
  },
  "error_recovery_recommendations": [
    "API errors: Retry is most effective (80% success) - typically transient issues",
    "Timeout errors: Retry is most effective (80% success) - often resolves on second attempt",
    "Validation errors: Manual fix is most effective (87.5% success) - requires code/config changes",
    "File not found: Manual fix is 100% effective - create missing file or fix path",
    "Context overflow: Manual fix is most effective (67% success) - split or simplify prompts",
    "Other errors: Escalation recommended (33% success) - requires investigation"
  ]
}
```

### Recovery Analysis Pipeline

**Complete Workflow:**

```
Input: history.jsonl (via session-miner parsing)
  ↓
Step 1: Parse sessions using session-miner (STORY-221)
  ↓
Step 2: Extract and categorize errors using STORY-229 Error Categorization
  ↓
Step 3: For each error, identify recovery action (AC#1)
  - Group by session_id
  - Analyze subsequent commands
  - Classify recovery action type
  ↓
Step 4: Track recovery success (AC#2)
  - Determine if recovery succeeded
  - Calculate success rates per action type
  - Calculate average time to recovery
  ↓
Step 5: Build error-recovery correlation (AC#3)
  - Correlate error categories with recovery actions
  - Identify most effective recovery per error type
  - Rank recovery effectiveness
  ↓
Step 6: Generate recommendations
  - Best recovery action per error category
  - Actionable guidance based on data
  ↓
Output: RecoveryAnalysisReport
```

**Recovery Analysis Report Structure:**

```json
{
  "summary": {
    "total_sessions": 42,
    "total_errors": 30,
    "total_recovery_attempts": 25,
    "overall_recovery_rate": 0.72
  },
  "recovery_entries": [/* RecoveryEntry[] */],
  "action_distribution": {
    "retry": 15,
    "manual-fix": 8,
    "skip": 5,
    "escalate": 2
  },
  "recovery_metrics": {/* per-action success rates */},
  "error_recovery_correlation": {/* category -> action -> stats */},
  "best_actions_by_category": {/* most effective action per error type */},
  "error_recovery_recommendations": [/* actionable guidance */],
  "metadata": {
    "analysis_timestamp": "2025-01-05T15:00:00Z",
    "story_id": "STORY-230",
    "depends_on": ["STORY-229"]
  }
}
```

### Integration with STORY-229 Error Categorization

**Data Flow:**

```
session-miner (SessionEntry[])
       ↓
STORY-229 Error Categorization (ErrorEntry[])
       ↓
STORY-230 Error Recovery Patterns (RecoveryEntry[])
       ↓
/insights recovery → Recovery Analysis Report
```

**Invocation Template:**

```markdown
Task(
  subagent_type="session-miner",
  description="Analyze error recovery patterns",
  prompt="""
  Perform recovery pattern analysis on history.jsonl:

  1. Parse history with session-miner (STORY-221)
  2. Categorize errors using STORY-229 Error Categorization
  3. Identify recovery actions for each error (AC#1)
  4. Track recovery success rates (AC#2)
  5. Build error-recovery correlation (AC#3)
  6. Generate recommendations

  Return RecoveryAnalysisReport with best recovery actions per error type.
  """
)
```

### Edge Case Handling

| Case | Handling |
|------|----------|
| No subsequent commands after error | recovery_action = "escalate" (session ended) |
| Error is last entry in session | recovery_action = "escalate", recovery_successful = false |
| Multiple errors in sequence | Each error analyzed independently with its own subsequent commands |
| Same error repeated | Each occurrence gets own RecoveryEntry |
| Skip action success | recovery_successful = null (skip is not recovery) |
| Missing error_category | Use "other" category from STORY-229 |

### Success Criteria (STORY-230)

**Functional Requirements:**
- [ ] Identify recovery actions (retry, manual-fix, skip, escalate) from subsequent commands (AC#1)
- [ ] Calculate recovery success rates per action type (AC#2)
- [ ] Identify most effective recovery action per error category (AC#3)

**Non-Functional Requirements:**
- [ ] Process recovery patterns within session context (session_id grouping)
- [ ] Handle edge cases (no subsequent commands, session boundaries)
- [ ] Support incremental analysis (pagination-compatible)

**Integration Requirements:**
- [ ] Compatible with STORY-229 Error Categorization (extends ErrorEntry)
- [ ] References all 6 error categories (api, timeout, validation, file-not-found, context-overflow, other)
- [ ] JSON output format for downstream consumers (devforgeai-insights)

### References

- **Story:** devforgeai/specs/Stories/STORY-230-error-recovery-patterns.story.md
- **Depends on:** STORY-229 (Error Categorization)
- **Epic:** devforgeai/specs/Epics/EPIC-034-session-data-mining.epic.md
- **Tech Stack:** devforgeai/specs/context/tech-stack.md (lines 196-210)

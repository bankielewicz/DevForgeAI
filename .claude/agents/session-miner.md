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

**Severity Assignment Decision Matrix:**

| Category | Critical Conditions | Default Severity | Notes |
|----------|-------------------|------------------|-------|
| **api** | "rate limit", "503", "502", "connection refused" in message | high | Service integration failures blocking operation |
| **timeout** | (none - inherently high impact) | high | Operation duration limits block execution |
| **context-overflow** | (always critical - system halt) | critical | Resource exhaustion prevents continuation |
| **validation** | (none - recoverable) | medium | Data constraint violations can be corrected |
| **file-not-found** | (none - recoverable) | medium | Missing resources can be provided |
| **other** | (requires investigation) | low | Unknown impact requires analysis |

**Severity Assignment Algorithm:**

```
FUNCTION assign_severity(category, error_message):
  # Check critical conditions first (highest impact)
  IF category == "context-overflow":
    RETURN "critical"

  IF category == "api":
    RETURN "critical" IF ["rate limit", "503", "502", "connection refused"] in message
    RETURN "high"

  # Map category to default severity
  severity_map = {
    "timeout": "high",
    "validation": "medium",
    "file-not-found": "medium",
    "other": "low"
  }

  RETURN severity_map[category]
```

**Example Severity Distribution:**

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

Auto-assign sequential codes (ERR-001, ERR-002, etc.) based on normalized error patterns.

**Pattern Normalization Rules:**

Apply these transformations to identify unique error patterns (removes variable parts):

| Pattern Type | Regex | Replacement |
|--------------|-------|-------------|
| ISO8601 Timestamps | `\d{4}-\d{2}-\d{2}T[\d:]+Z?` | `<TIMESTAMP>` |
| UUID Values | `[a-f0-9-]{36}` | `<UUID>` |
| File Paths | `/[\w/.-]+` | `<PATH>` |
| Numeric Values | `\d+` | `<NUM>` |

**Error Code Assignment Algorithm:**

For duplicate errors with identical messages, aggregate occurrence counts and sum occurrences together.

```
FUNCTION assign_error_code(error_message, registry):
  # Step 1: Normalize message for pattern grouping
  normalized = normalize_pattern(error_message)

  # Step 2: Check if pattern exists - occurrence aggregate for duplicates
  FOR code, entry in registry.items():
    IF patterns_match(normalized, entry.pattern):
      # Aggregate count for same pattern
      entry.occurrences += 1
      entry.last_seen = current_timestamp()
      RETURN code

  # Step 3: New pattern - assign sequential code
  new_code = registry.metadata.next_code
  registry[new_code] = create_registry_entry(
    pattern=normalized,
    category=classify_error(error_message),
    severity=assign_severity(category, error_message),
    timestamp=current_timestamp(),
    session=current_session_id
  )
  registry.metadata.next_code = increment_code(new_code)

  RETURN new_code

FUNCTION normalize_pattern(message):
  # Remove variable components to group similar errors
  pattern = message
    .replace(/\d{4}-\d{2}-\d{2}T[\d:]+Z?/g, '<TIMESTAMP>')
    .replace(/[a-f0-9-]{36}/g, '<UUID>')
    .replace(/\/[\w/.-]+/g, '<PATH>')
    .replace(/\d+/g, '<NUM>')
  RETURN pattern
```

**Registry Persistence:**

```
FUNCTION save_registry(registry, file_path="devforgeai/data/error-registry.json"):
  registry.metadata.last_updated = current_timestamp()
  Write(file_path=file_path, content=JSON.stringify(registry, null, 2))
```

### Error Analysis Pipeline

**Pipeline Workflow (6 Steps):**

Orchestrates error analysis from raw session data to categorized report. Each step flows into the next: extract then classify, classify then assign severity, severity then register in registry.

```
Input: history.jsonl (SessionEntry[])
  ↓
[1] Filter errors (status == "error")
[2] Extract error messages with context (command, timestamp, session) - after extract, classify
[3] Classify categories using pattern matching (priority 1-6) - category then assign severity
[4] Assign severity using decision matrix - severity then register in error registry
[5] Assign/lookup error codes from registry (auto-increment)
[6] Aggregate statistics (distribution, top patterns)
  ↓
Output: ErrorAnalysisReport with all above sections
```

**Pipeline Error Handling:**

If any step fails, continue with partial results (graceful degradation):

```
TRY:
  For each SessionEntry:
    IF status == "error": process through steps 1-6
CATCH error_in_step:
  Log error with context
  Include partial results in report with error_flag=true
  Continue to next entry
```

**Error Analysis Report Structure:**

Complete report with summary, categorized errors, and recommendations:

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

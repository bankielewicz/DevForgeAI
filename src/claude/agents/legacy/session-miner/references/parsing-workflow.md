---
parent: session-miner
topic: parsing-workflow
description: JSON Lines parsing workflow, SessionEntry extraction, and pagination
---

# Parsing Workflow

**Purpose:** Complete workflow for parsing history.jsonl files with pagination support.

---

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

---

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

---

## Processing Pipeline

```
Input (file_path, offset, limit)
  |
Validate File Exists
  |
Read Chunk (offset, limit + 1)
  |
Parse JSON Lines (with error handling)
  |
Extract SessionEntry Fields (per schema)
  |
Normalize Fields (timestamp, status, duration, uuid)
  |
Build Response with Pagination Metadata
  |
Return Structured Output
```

---

## Step 1: Validate Input

```
IF file_path not provided:
  file_path = "~/.claude/history.jsonl"

IF NOT file exists (Glob check):
  RETURN { error: "File not found", entries: [], metadata: {} }
```

---

## Step 2: Read Chunk

Use Pagination API parameters to chunk processing:

```
offset:  0         # Number of entries to skip
limit:   1000      # Maximum entries per chunk
file_path: ~/.claude/history.jsonl

Read(file_path, offset, limit + 1)  # Read one extra to detect has_more
```

---

## Step 3: Parse JSON Lines with Error Tolerance

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

---

## Step 4: Normalize Fields

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

---

## Step 5: Build Pagination Response

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

---

## Step 6: Return Structured Output

Response is consistent JSON schema regardless of input variations (see output-formats.md).

---

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

---

## Invocation Template

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

---

## Edge Cases

| Case | Handling |
|------|----------|
| Empty file | Return empty entries array, metadata.total_processed=0 |
| All malformed | Return empty entries, full errors array |
| Unicode content | Preserve encoding, no conversion |
| Very long lines | Truncate to 10000 chars for safety |
| Null values | Convert to fallback per schema |

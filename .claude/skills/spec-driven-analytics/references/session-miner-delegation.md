# Session-Miner Delegation Reference

**Loaded by:** Phase 02 (Query Routing & Subagent Orchestration)
**Purpose:** Subagent invocation contract, Task() template, response schema, error handling

---

## Subagent Overview

**Agent:** session-miner
**Location:** `.claude/agents/session-miner.md`
**Enforcement:** BLOCKING — Must invoke via Task() and wait for response
**Capabilities:**
- Parse and normalize history.jsonl data
- Extract structured metadata from Claude Code command history
- Error-tolerant processing (malformed entries logged, not halted)
- Streaming support with pagination (offset/limit)
- Normalized output with SessionEntry objects

---

## Task() Invocation Template

```
Task(
  subagent_type="session-miner",
  description="{query_description}",
  prompt="{session_miner_prompt}"
)
```

**Example for dashboard query:**
```
Task(
  subagent_type="session-miner",
  description="Generate dashboard metrics from session data",
  prompt="Analyze Claude Code session history to generate a dashboard overview. Focus: Extract total session counts, workflow execution frequency, error rates, average completion times. Return structured JSON with entries array containing SessionEntry objects."
)
```

---

## SessionEntry Response Schema

The session-miner returns an array of SessionEntry objects with these 8 fields:

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | ISO 8601 string | When the entry was recorded |
| `command` | String | The command or tool executed |
| `status` | Enum: success, error, partial | Execution outcome |
| `duration_ms` | Integer | Execution time in milliseconds |
| `user_input` | String | The user's input text |
| `model` | String | Model used (claude-opus-4-6, claude-sonnet-4-20250514, etc.) |
| `session_id` | UUID string | Unique session identifier |
| `project` | String | Project path or name |

---

## Full Response Format

```json
{
  "success": true,
  "entries": [
    {
      "timestamp": "2026-02-13T12:34:56.789Z",
      "session_id": "uuid-string",
      "status": "success",
      "duration_ms": 1234,
      "command": "/dev STORY-224",
      "user_input": "/dev STORY-224",
      "model": "claude-opus-4-6",
      "project": "/mnt/c/Projects/DevForgeAI2"
    }
  ],
  "pagination": {
    "offset": 0,
    "limit": 1000,
    "has_more": true,
    "next_offset": 1000,
    "total_errors": 5
  }
}
```

---

## Pagination Parameters

For large datasets, session-miner supports chunked processing:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `offset` | 0 | Number of entries to skip |
| `limit` | 1000 | Maximum entries per chunk |

**Large File Handling:**
- Files 50MB+: Use pagination with 1000-entry chunks
- Performance target: 86MB+ file in <30 seconds
- 1000 entries: <5 seconds

---

## Error Handling

### Subagent Not Available
```
IF session-miner subagent is not available:
  Display: "WARNING: session-miner subagent not found"
  AskUserQuestion:
    Question: "Session-miner subagent is unavailable. How should we proceed?"
    Options:
      - label: "Retry"
        description: "Try invoking session-miner again"
      - label: "Abort"
        description: "Cancel the analytics query"
  IF "Abort": HALT
```

### Subagent Returns Error
```
IF session-miner response contains error:
  Log: checkpoint.output.error = error_details
  Do NOT cache error responses
  Display error template with troubleshooting:
    1. Check history.jsonl exists at ~/.claude/history.jsonl
    2. Verify file is not empty
    3. Try with --days 7 to limit data volume
    4. Run /analytics --force to bypass cache
```

### Subagent Returns Empty
```
IF session-miner returns 0 entries:
  Display: "No session data found matching query criteria"
  Continue to Phase 03 with empty entries (will render "no results" template)
```

### Timeout Handling
```
IF session-miner does not respond within reasonable time:
  Display: "Session-miner is taking longer than expected"
  Continue waiting (BLOCKING invocation)
  Do NOT timeout prematurely — large history files take time
```

---

## Data Sources

The session-miner extracts data from:

| Source | Path | Content |
|--------|------|---------|
| Session history | `~/.claude/history.jsonl` | All Claude Code command history |
| Feedback data | `devforgeai/feedback/` | Captured feedback sessions |
| Story files | `devforgeai/specs/Stories/` | Story development records |

---

## Best Practices

1. **Be specific in prompts** — Specific query focus yields better results than broad requests
2. **Use pagination for large datasets** — Prevents memory issues with 50MB+ history files
3. **Filter by time window** — Use `--days N` to limit data volume for faster results
4. **Error tolerance** — session-miner skips malformed entries; some data loss is acceptable
5. **Do NOT cache errors** — Only cache successful query results

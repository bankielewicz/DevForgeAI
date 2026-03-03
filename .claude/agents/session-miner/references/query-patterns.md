---
parent: session-miner
topic: query-patterns
description: Query and extraction patterns for SessionEntry fields
---

# Query Patterns

**Purpose:** Field extraction patterns and query syntax for SessionEntry data.

---

## Field Extraction Priority

For each field, extract using priority order. If primary is missing, try alternatives.

### timestamp

**Extraction Priority:**
1. `$.timestamp` (primary)
2. `$.time`
3. `$.date`

**Normalization:**
- Convert to ISO8601 format: `"2025-01-02T10:30:00Z"`
- Handle Unix timestamps (convert to ISO8601)
- Handle various date string formats

**Examples:**
```json
{"timestamp": "2025-01-02T10:30:00Z"}  -> "2025-01-02T10:30:00Z"
{"time": "2025-01-02 10:30:00"}        -> "2025-01-02T10:30:00Z"
{"date": 1735816200000}                -> "2025-01-02T10:30:00Z"
```

---

### command

**Extraction Priority:**
1. `$.command` (primary)
2. `$.action`
3. `$.type`

**Fallback:** `"unknown"`

**Examples:**
```json
{"command": "/dev STORY-221"}  -> "/dev STORY-221"
{"action": "chat"}             -> "chat"
{"type": "message"}            -> "message"
{}                             -> "unknown"
```

---

### status

**Extraction Priority:**
1. `$.status` (primary)
2. `$.result`
3. `$.outcome`

**Status Mapping:**

| Raw Value | Normalized |
|-----------|------------|
| success, ok, pass, passed, complete, completed | `"success"` |
| error, fail, failed, failure | `"error"` |
| partial, warning, incomplete | `"partial"` |
| (other/missing) | `"partial"` |

**Fallback:** `"partial"`

---

### duration_ms

**Extraction Priority:**
1. `$.duration_ms` (primary)
2. `$.duration`
3. `$.time_ms`

**Normalization:**
- Convert to positive integer
- Handle float values (truncate to integer)
- Handle null/missing (use 0)

**Fallback:** `0`

---

### user_input

**Extraction Priority:**
1. `$.user_input` (primary)
2. `$.input`
3. `$.prompt`
4. `$.query`

**Fallback:** `""`

---

### model

**Extraction Priority:**
1. `$.model` (primary)
2. `$.ai_model`

**Known Values:** `"sonnet"`, `"opus"`, `"haiku"`, `"claude-3-sonnet"`, etc.

**Fallback:** `"unknown"`

---

### session_id

**Extraction Priority:**
1. `$.session_id` (primary)
2. `$.sessionId`
3. `$.session`

**Validation:**
- Must be valid UUID format
- Invalid UUIDs fallback to null

**Fallback:** `null`

---

### project

**Extraction Priority:**
1. `$.project` (primary)
2. `$.cwd`
3. `$.project_path`

**Fallback:** `"unknown"`

---

## Query Syntax Examples

### Filter by Status

```javascript
entries.filter(e => e.status === "error")
```

### Filter by Command Pattern

```javascript
entries.filter(e => e.command.startsWith("/dev"))
```

### Filter by Time Range

```javascript
entries.filter(e =>
  new Date(e.timestamp) >= startDate &&
  new Date(e.timestamp) <= endDate
)
```

### Group by Session

```javascript
const bySession = entries.reduce((acc, e) => {
  const sid = e.session_id || "no-session";
  if (!acc[sid]) acc[sid] = [];
  acc[sid].push(e);
  return acc;
}, {});
```

---

## Common Query Patterns

### Error Rate Calculation

```javascript
const errorRate = entries.filter(e => e.status === "error").length / entries.length;
```

### Average Duration

```javascript
const avgDuration = entries.reduce((sum, e) => sum + e.duration_ms, 0) / entries.length;
```

### Command Frequency

```javascript
const frequency = entries.reduce((acc, e) => {
  acc[e.command] = (acc[e.command] || 0) + 1;
  return acc;
}, {});
```

### Session Timeline

```javascript
const timeline = entries
  .sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp))
  .map(e => ({ time: e.timestamp, command: e.command, status: e.status }));
```

---

## Output Field Compatibility

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

---
parent: session-miner
topic: error-handling
description: STORY-229 error categorization, ErrorEntry model, and classification
---

# Error Handling and Categorization (STORY-229)

**Purpose:** Categorize and classify errors from session history for reliability tracking.

---

## Purpose

Extract, categorize, and classify errors from SessionEntry data with:
- Error message extraction with full context preservation
- Category classification using pattern matching
- Severity assignment based on impact rules
- Error code registry for tracking unique patterns

---

## When Invoked

**Proactive triggers:**
- When analyzing error distribution for EPIC-034
- When categorizing session failures
- When building error reports for insights

**Explicit invocation:**
- "Categorize errors from history.jsonl"
- "Extract error patterns from sessions"
- "Build error code registry"

---

## Data Model: ErrorEntry

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

---

## AC#1: Error Message Extraction

**Extraction Workflow:**

```
Input: SessionEntry[] from session-miner
  |
Filter: status == "error"
  |
Extract: error_message field (with fallbacks)
  |
Preserve: command, timestamp, session_id context
  |
Output: ErrorEntry[] with full context
```

**Field Extraction Priority:**

| Field | Primary | Fallback 1 | Fallback 2 | Default |
|-------|---------|------------|------------|---------|
| error_message | $.error_message | $.error | $.message | "Unknown error" |

---

## AC#2: Category Classification

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

---

## AC#3: Severity Assignment

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

---

## AC#4: Error Code Registry

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

**Pattern Normalization Rules:**

Apply these transformations to identify unique error patterns:

| Pattern Type | Regex | Replacement |
|--------------|-------|-------------|
| ISO8601 Timestamps | `\d{4}-\d{2}-\d{2}T[\d:]+Z?` | `<TIMESTAMP>` |
| UUID Values | `[a-f0-9-]{36}` | `<UUID>` |
| File Paths | `/[\w/.-]+` | `<PATH>` |
| Numeric Values | `\d+` | `<NUM>` |

**Error Code Assignment Algorithm:**

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
  pattern = message
    .replace(/\d{4}-\d{2}-\d{2}T[\d:]+Z?/g, '<TIMESTAMP>')
    .replace(/[a-f0-9-]{36}/g, '<UUID>')
    .replace(/\/[\w/.-]+/g, '<PATH>')
    .replace(/\d+/g, '<NUM>')
  RETURN pattern
```

---

## Error Analysis Pipeline

**Pipeline Workflow (6 Steps):**

```
Input: history.jsonl (SessionEntry[])
  |
[1] Filter errors (status == "error")
[2] Extract error messages with context (command, timestamp, session)
[3] Classify categories using pattern matching (priority 1-6)
[4] Assign severity using decision matrix
[5] Assign/lookup error codes from registry (auto-increment)
[6] Aggregate statistics (distribution, top patterns)
  |
Output: ErrorAnalysisReport with all above sections
```

**Pipeline Error Handling:**

```
TRY:
  For each SessionEntry:
    IF status == "error": process through steps 1-6
CATCH error_in_step:
  Log error with context
  Include partial results in report with error_flag=true
  Continue to next entry
```

---

## Edge Case Handling

| Case | Handling |
|------|----------|
| No errors in history | Return empty errors array, error_rate=0.00 |
| All entries are errors | Process all, error_rate=1.00 |
| Missing error_message field | Use fallback: "Unknown error", category: "other" |
| Duplicate error messages | Same error code, increment occurrences |
| Very long error messages | Truncate to 500 chars for pattern matching |
| Empty error_message | Use fallback: "Empty error message" |

---

## Integration with devforgeai-insights

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
       |
Error Categorization (ErrorEntry[])
       |
STORY-225 (devforgeai-insights) -> Error Analysis Report
       |
/insights errors -> User-friendly error dashboard
```

---

## Success Criteria (STORY-229)

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

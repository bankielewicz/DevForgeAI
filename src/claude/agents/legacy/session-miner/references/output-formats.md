---
parent: session-miner
topic: output-formats
description: Response schemas and output structures for session-miner
---

# Output Formats

**Purpose:** JSON schemas for success and error responses from session-miner.

---

## Success Response

Standard response when parsing succeeds:

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

---

## Error Response

Response when file not found or critical failure:

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

---

## Field Schemas

### SessionEntry

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `timestamp` | String (ISO8601) | No | When command was executed |
| `command` | String | Yes | The executed command or action |
| `status` | Enum | Yes | success, error, or partial |
| `duration_ms` | Integer | Yes | Execution time in milliseconds |
| `user_input` | String | Yes | User's input or prompt text |
| `model` | String | Yes | AI model used |
| `session_id` | String (UUID) | No | Unique session identifier |
| `project` | String | Yes | Project path or name |

### Metadata

| Field | Type | Description |
|-------|------|-------------|
| `total_processed` | Integer | Actual count of entries returned |
| `errors_count` | Integer | Number of malformed entries skipped |
| `offset` | Integer | Input offset parameter |
| `limit` | Integer | Input limit parameter |
| `has_more` | Boolean | True if more entries exist |
| `next_offset` | Integer/null | Offset for next pagination call |

### Error Entry

| Field | Type | Description |
|-------|------|-------------|
| `line_number` | Integer | Line number in source file |
| `raw_content` | String | First 100 chars of malformed line |
| `error` | String | Error description |

---

## Pagination Response Patterns

### First Chunk

```json
{
  "metadata": {
    "offset": 0,
    "limit": 1000,
    "has_more": true,
    "next_offset": 1000
  }
}
```

### Middle Chunk

```json
{
  "metadata": {
    "offset": 1000,
    "limit": 1000,
    "has_more": true,
    "next_offset": 2000
  }
}
```

### Final Chunk

```json
{
  "metadata": {
    "offset": 2000,
    "limit": 1000,
    "has_more": false,
    "next_offset": null
  }
}
```

---

## Aggregation Report Format

For downstream consumers that aggregate multiple chunks:

```json
{
  "summary": {
    "total_entries": 5000,
    "total_errors": 25,
    "error_rate": 0.005,
    "date_range": {
      "start": "2025-01-01T00:00:00Z",
      "end": "2025-01-31T23:59:59Z"
    }
  },
  "by_status": {
    "success": 4500,
    "error": 300,
    "partial": 200
  },
  "by_command": {
    "/dev": 1500,
    "/qa": 800,
    "/ideate": 400
  },
  "by_project": {
    "/mnt/c/Projects/DevForgeAI2": 3000,
    "/mnt/c/Projects/OtherProject": 2000
  }
}
```

---

## N-gram Analysis Output Format

For STORY-226 command pattern analysis:

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

---

## Error Analysis Output Format

For STORY-229 error categorization:

```json
{
  "summary": {
    "total_entries": 100,
    "total_errors": 12,
    "error_rate": 0.12,
    "unique_patterns": 8
  },
  "errors": [],
  "category_distribution": {
    "api": 5,
    "validation": 3,
    "timeout": 2,
    "context-overflow": 1,
    "file-not-found": 1,
    "other": 0
  },
  "severity_distribution": {
    "critical": 2,
    "high": 4,
    "medium": 5,
    "low": 1
  },
  "top_patterns": [],
  "registry": {},
  "recommendations": [
    "High frequency of API rate limit errors (ERR-001) - consider implementing backoff strategy",
    "Multiple timeout errors in /dev workflow - check network connectivity"
  ]
}
```

---

## Anti-Pattern Analysis Output Format

For STORY-231 anti-pattern mining:

```json
{
  "violations": [],
  "category_distribution": {
    "bash_for_file_ops": 3,
    "monolithic_components": 0,
    "making_assumptions": 1,
    "size_violations": 1,
    "language_specific_code": 0,
    "context_file_violations": 1,
    "circular_dependencies": 0,
    "narrative_documentation": 0,
    "missing_frontmatter": 0,
    "hardcoded_paths": 1
  },
  "severity_distribution": {
    "critical": 5,
    "high": 1,
    "medium": 1,
    "low": 0
  },
  "metadata": {
    "total_entries": 8,
    "total_violations": 7,
    "violation_rate": 0.875,
    "unique_patterns": 6
  },
  "consequence_correlation": {
    "total_violations_with_errors": 2,
    "correlation_rate": 0.286,
    "high_risk_patterns": []
  },
  "registry": {}
}
```

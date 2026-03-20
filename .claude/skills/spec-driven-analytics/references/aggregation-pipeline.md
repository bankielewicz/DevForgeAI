# Aggregation Pipeline Reference

**Loaded by:** Phase 03 (Result Aggregation & Analysis)
**Purpose:** group_by, filter_by, calculate_metrics, rank_by_relevance functions and SessionEntry handling

---

## Pipeline Overview

```
Raw Entries → Parse → Group → Filter → Calculate Metrics → Rank → Output
```

Each stage transforms the data progressively:
1. **Parse:** Raw session-miner output → structured SessionEntry objects
2. **Group:** SessionEntry list → dictionary keyed by aggregation attribute
3. **Filter:** Apply time, story, and query filters
4. **Calculate:** Compute counts, rates, averages per group
5. **Rank:** Score by composite relevance (recency + frequency + severity)

---

## SessionEntry Structure

Each entry from session-miner is normalized to:

```json
{
  "timestamp": "2026-03-19T10:30:00Z",
  "entry_type": "tool_call",
  "content": "/dev STORY-224",
  "metadata": {
    "story_id": "STORY-224",
    "phase": "02",
    "status": "success",
    "duration_ms": 45000,
    "session_id": "abc-123"
  }
}
```

**Entry Types:**
- `tool_call` — A tool invocation (Read, Write, Bash, Task, etc.)
- `user_message` — User input text
- `assistant_response` — Claude's response
- `error` — An error occurrence

---

## Group-By Function

Groups entries by an aggregation key based on query type:

| Query Type | Aggregation Key | Groups By |
|------------|----------------|-----------|
| dashboard | `entry_type` | tool_call, user_message, assistant_response, error |
| workflows | `content` | /dev, /qa, /create-story, etc. |
| errors | `content` | Error message text |
| decisions | `metadata.story_id` | STORY-224, STORY-225, etc. |
| story | `metadata.phase` | 01, 02, 03, etc. |
| command-patterns | `content` | Command sequence (n-gram) |

**Nested Key Access:**
For keys like `metadata.story_id`, use dot-notation traversal:
```
def extract_nested(entry, key):
    parts = key.split(".")
    value = entry
    for part in parts:
        value = value.get(part, None)
        if value is None: break
    return value
```

---

## Filter-By Function

Applies inclusion/exclusion criteria to grouped data:

### Time Filter (`--days N`)
```
cutoff = now - timedelta(days=DAYS_LIMIT)
filtered = [e for e in entries if parse_datetime(e.timestamp) >= cutoff]
```

### Story Filter (`--story-id STORY-XXX`)
```
filtered = [e for e in entries if e.metadata.story_id == STORY_ID]
```

### Query Parameter Filter (decisions)
```
filtered = [e for e in entries if QUERY_PARAM.lower() in e.content.lower()]
```

### Null/Empty Key Exclusion
Always exclude entries where the grouping key is null or empty string.

---

## Calculate Metrics Function

Computes per-group summary statistics:

```python
def calculate_metrics(group_entries):
    return {
        "count": len(group_entries),
        "success_count": len([e for e in group_entries if e.metadata.status == "success"]),
        "error_count": len([e for e in group_entries if e.metadata.status == "error"]),
        "success_rate": success_count / max(count, 1) * 100,
        "average_duration_ms": mean([e.metadata.duration_ms for e in group_entries if e.metadata.duration_ms]),
        "first_seen": min(e.timestamp for e in group_entries),
        "last_seen": max(e.timestamp for e in group_entries)
    }
```

### Global Metrics

Computed across all groups:

```python
global_metrics = {
    "total_entries": sum(m.count for m in all_metrics),
    "total_categories": len(all_metrics),
    "overall_success_rate": total_success / max(total_entries, 1) * 100,
    "overall_error_rate": total_errors / max(total_entries, 1) * 100
}
```

---

## Rank-By-Relevance Function

Scores each group by a composite relevance metric:

### Weights

| Factor | Weight | Rationale |
|--------|--------|-----------|
| Recency | 0.3 | Recent data is more actionable |
| Frequency | 0.5 | Common patterns have wider impact |
| Severity | 0.2 | Errors warrant more attention |

### Scoring

```python
def calculate_relevance(metric, max_count):
    recency = recency_score(metric.last_seen)     # 0.0 - 1.0 (1.0 = today)
    frequency = metric.count / max(max_count, 1)   # 0.0 - 1.0
    severity = metric.error_count / max(metric.count, 1)  # 0.0 - 1.0

    return 0.3 * recency + 0.5 * frequency + 0.2 * severity
```

### Recency Score

```python
def recency_score(last_seen_timestamp):
    age_days = (now - parse_datetime(last_seen_timestamp)).days
    if age_days <= 1: return 1.0
    if age_days <= 7: return 0.8
    if age_days <= 30: return 0.5
    if age_days <= 90: return 0.2
    return 0.1
```

### Final Ranking

Sort all groups by `relevance_score` descending. Return top 15 for display.

---

## Empty Results Handling

When no entries match the query:
- `entries = []`
- `grouped = {}`
- `metrics = {}`
- `global_metrics = { total_entries: 0, total_categories: 0, ... }`
- `ranked = []`

Phase 04 will detect the empty ranked list and render the "no results" template.

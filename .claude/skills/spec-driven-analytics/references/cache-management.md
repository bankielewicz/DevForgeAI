# Cache Management Reference

**Loaded by:** Phase 01 (Cache Management)
**Purpose:** TTL logic, cache key generation, invalidation rules, force refresh behavior

---

## Cache Architecture

```
devforgeai/cache/analytics/
  ├── dashboard.json
  ├── workflows.json
  ├── errors.json
  ├── decisions_{query_param}.json
  ├── story_{story_id}.json
  ├── command-patterns.json
  └── {query_type}_{filters_hash}.json
```

---

## Cache Key Generation

Cache keys are deterministic strings built from query parameters:

```
key_parts = [query_type]
IF story_id: key_parts.append(story_id)
IF days_limit: key_parts.append(f"days-{days_limit}")
IF query_param: key_parts.append(query_param.replace(" ", "-"))

cache_key = "_".join(key_parts)
```

**Examples:**
- Dashboard: `dashboard`
- Workflows: `workflows`
- Errors with 7-day window: `errors_days-7`
- Story query: `story_STORY-224`
- Decisions with search: `decisions_caching`
- Command patterns: `command-patterns`

---

## Cache Entry JSON Schema

```json
{
  "cache_key": "dashboard",
  "created_at": "2026-03-19T10:00:00Z",
  "ttl_seconds": 3600,
  "expires_at": "2026-03-19T11:00:00Z",
  "query": {
    "type": "dashboard",
    "story_id": null,
    "days_limit": null,
    "query_param": null
  },
  "results": {
    "summary": {
      "total_entries": 1500,
      "total_categories": 12,
      "overall_success_rate": 87.3,
      "overall_error_rate": 12.7
    },
    "data": [
      {
        "key": "category_name",
        "metrics": {
          "count": 150,
          "success_rate": 92.0,
          "average_duration_ms": 45000
        }
      }
    ],
    "recommendations": [
      "Recommendation 1",
      "Recommendation 2"
    ],
    "formatted_output": "## Dashboard Overview\n..."
  }
}
```

---

## TTL Management

| Behavior | Condition | Action |
|----------|-----------|--------|
| Cache Hit | Cache exists AND age < 3600s AND NOT force_refresh | Return cached results, skip Phases 02-04 |
| Cache Miss | Cache missing OR expired | Invoke session-miner, cache new results |
| Force Refresh | `--force` flag present | Ignore cache, execute full pipeline, overwrite cache |
| Invalidation | TTL expires (1 hour) | Next query treats as cache miss |

**Default TTL:** 3600 seconds (1 hour)

---

## Cache Freshness Check

```python
cache_created = parse_datetime(cache_data["created_at"])
cache_age_seconds = (now - cache_created).total_seconds()
TTL = 3600

is_fresh = cache_age_seconds < TTL
```

---

## Force Refresh Behavior

When `--force` flag is present:
1. Set `FORCE_REFRESH = true` in checkpoint
2. Ignore any existing cache (treat as miss)
3. Execute full pipeline (Phases 02-04)
4. Overwrite cache with new results
5. New cache entry gets fresh TTL (3600s from now)

---

## Error Handling

### Cache Read Failure
If cache file exists but Read() fails (corrupt JSON, permission error):
- Set `cache_exists = false`
- Proceed as cache miss
- Log warning in checkpoint

### Cache Write Failure
If Write() fails when caching results:
- Display warning: "Cache write failed - results not cached"
- Continue to Phase 05 (display) — do NOT halt the workflow
- Log error in checkpoint

### Cache Directory Missing
If `devforgeai/cache/analytics/` does not exist:
- Create directory before writing
- If creation fails, skip caching with warning

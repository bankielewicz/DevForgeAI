# Phase 03: Result Aggregation & Analysis

## Entry Gate

```bash
source .venv/bin/activate && devforgeai-validate phase-check ${ANALYTICS_ID} --workflow=analytics --from=02 --to=03 --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Proceed to Phase 03 |
| 127 | CLI not installed - proceed without enforcement |
| Other | HALT - Phase 02 not complete |

## Contract

- **PURPOSE:** Aggregate raw session-miner data into structured metrics, apply filters, and rank results by relevance
- **REQUIRED SUBAGENTS:** none
- **REQUIRED REFERENCES:** `references/aggregation-pipeline.md`
- **REQUIRED ARTIFACTS:** `raw_entries` from Phase 02 stored in checkpoint or in-memory
- **STEP COUNT:** 6 mandatory steps

---

## Reference Loading [MANDATORY]

```
Read(file_path="src/claude/skills/spec-driven-analytics/references/aggregation-pipeline.md")
```

IF Read fails: HALT -- "aggregation-pipeline.md reference missing"

---

## Mandatory Steps (6)

### Step 3.1: Parse SessionEntry Objects

**EXECUTE:**
```
# Parse raw session-miner output into structured SessionEntry objects
# Session-miner may return various formats depending on query type

entries = []
FOR each item in raw_entries:
  entry = {
    "timestamp": item.timestamp OR extract_timestamp(item),
    "entry_type": item.entry_type OR classify_entry(item),  # tool_call, user_message, assistant_response, error
    "content": item.content OR item.command OR str(item),
    "metadata": {
      "story_id": item.story_id OR extract_story_id(item),
      "phase": item.phase OR null,
      "status": item.status OR "unknown",
      "duration_ms": item.duration_ms OR null,
      "session_id": item.session_id OR null
    }
  }
  entries.append(entry)

Display: f"Parsed {len(entries)} SessionEntry objects"
```

**VERIFY:**
`entries` is a list with length > 0. Each entry has `timestamp`, `entry_type`, `content`, and `metadata` keys.
IF entries is empty:
  Display: "WARNING: No entries parsed from session-miner output"
  # Continue with empty set - Phase 04 will render "no results" template

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${ANALYTICS_ID} --workflow=analytics --phase=03 --step=3.1 --project-root=. 2>&1
```
Update checkpoint: `phases["03"].steps_completed.append("3.1")`

---

### Step 3.2: Apply Group-By Aggregation

**EXECUTE:**
```
# Group entries by the appropriate key based on query type
AGGREGATION_KEYS = {
  "dashboard": "entry_type",
  "workflows": "content",       # Group by workflow/command name
  "errors": "content",          # Group by error message
  "decisions": "metadata.story_id",  # Group by story
  "story": "metadata.phase",    # Group by development phase
  "command-patterns": "content"  # Group by command sequence
}

aggregation_key = AGGREGATION_KEYS[QUERY_TYPE]
grouped = {}

FOR entry in entries:
  key_value = extract_nested(entry, aggregation_key)
  IF key_value not in grouped:
    grouped[key_value] = []
  grouped[key_value].append(entry)

Display: f"Grouped into {len(grouped)} categories by '{aggregation_key}'"
```

**VERIFY:**
`grouped` is a dictionary. At least 1 key exists (unless entries was empty).

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${ANALYTICS_ID} --workflow=analytics --phase=03 --step=3.2 --project-root=. 2>&1
```
Update checkpoint: `phases["03"].steps_completed.append("3.2")`

---

### Step 3.3: Apply Filter Criteria

**EXECUTE:**
```
# Apply inclusion/exclusion filters
filtered = {}

FOR key, group_entries in grouped.items():
  # Exclude empty/null keys
  IF key is null or key == "":
    continue

  # Apply days_limit filter if specified
  IF DAYS_LIMIT:
    cutoff = now - timedelta(days=DAYS_LIMIT)
    group_entries = [e for e in group_entries if parse_datetime(e.timestamp) >= cutoff]

  # Apply story_id filter if specified
  IF STORY_ID:
    group_entries = [e for e in group_entries if e.metadata.story_id == STORY_ID]

  # Apply query_param filter for decisions
  IF QUERY_PARAM AND QUERY_TYPE == "decisions":
    group_entries = [e for e in group_entries if QUERY_PARAM.lower() in e.content.lower()]

  IF len(group_entries) > 0:
    filtered[key] = group_entries

Display: f"Filtered to {len(filtered)} categories ({sum(len(v) for v in filtered.values())} total entries)"
```

**VERIFY:**
`filtered` is a dictionary. Filters were applied correctly (no entries outside date range, story filter applied).

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${ANALYTICS_ID} --workflow=analytics --phase=03 --step=3.3 --project-root=. 2>&1
```
Update checkpoint: `phases["03"].steps_completed.append("3.3")`

---

### Step 3.4: Calculate Metrics

**EXECUTE:**
```
metrics = {}

FOR key, group_entries in filtered.items():
  metrics[key] = {
    "count": len(group_entries),
    "success_count": len([e for e in group_entries if e.metadata.status == "success"]),
    "error_count": len([e for e in group_entries if e.metadata.status == "error"]),
    "success_rate": calculate_success_rate(group_entries),
    "average_duration_ms": calculate_avg_duration(group_entries),
    "first_seen": min(e.timestamp for e in group_entries),
    "last_seen": max(e.timestamp for e in group_entries)
  }

# Calculate global metrics
global_metrics = {
  "total_entries": sum(m["count"] for m in metrics.values()),
  "total_categories": len(metrics),
  "overall_success_rate": calculate_overall_success_rate(metrics),
  "overall_error_rate": calculate_overall_error_rate(metrics)
}

Display: f"Calculated metrics for {len(metrics)} categories"
Display: f"Global: {global_metrics['total_entries']} entries, {global_metrics['overall_success_rate']:.1f}% success rate"
```

**VERIFY:**
`metrics` dict has same keys as `filtered`. Each value has `count`, `success_rate` keys.
`global_metrics` has `total_entries` and `overall_success_rate`.

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${ANALYTICS_ID} --workflow=analytics --phase=03 --step=3.4 --project-root=. 2>&1
```
Update checkpoint: `phases["03"].steps_completed.append("3.4")`

---

### Step 3.5: Rank by Relevance

**EXECUTE:**
```
# Rank entries by composite relevance score
# Relevance = recency_weight * recency + frequency_weight * frequency + severity_weight * severity

WEIGHTS = {
  "recency": 0.3,    # Newer = more relevant
  "frequency": 0.5,  # More common = more relevant
  "severity": 0.2    # More severe = more relevant (errors > warnings > info)
}

ranked = []
max_count = max(m["count"] for m in metrics.values()) if metrics else 1

FOR key, metric in metrics.items():
  recency_score = calculate_recency_score(metric["last_seen"])  # 0.0 - 1.0
  frequency_score = metric["count"] / max_count                  # 0.0 - 1.0
  severity_score = metric["error_count"] / max(metric["count"], 1)  # 0.0 - 1.0

  relevance = (
    WEIGHTS["recency"] * recency_score +
    WEIGHTS["frequency"] * frequency_score +
    WEIGHTS["severity"] * severity_score
  )

  ranked.append({
    "key": key,
    "metrics": metric,
    "relevance_score": relevance,
    "entries": filtered[key]
  })

# Sort by relevance score descending
ranked.sort(key=lambda x: x["relevance_score"], reverse=True)

Display: f"Ranked {len(ranked)} categories by relevance"
IF ranked:
  Display: f"Top result: '{ranked[0]['key']}' (score: {ranked[0]['relevance_score']:.3f})"
```

**VERIFY:**
`ranked` is a list sorted by `relevance_score` descending. Each item has `key`, `metrics`, `relevance_score`, `entries`.

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${ANALYTICS_ID} --workflow=analytics --phase=03 --step=3.5 --project-root=. 2>&1
```
Update checkpoint: `phases["03"].steps_completed.append("3.5")`

---

### Step 3.6: Record Aggregated Results in Checkpoint

**EXECUTE:**
```
# Store aggregated results for Phase 04
aggregated_results = {
  "query_type": QUERY_TYPE,
  "global_metrics": global_metrics,
  "ranked_results": [
    {
      "key": r["key"],
      "count": r["metrics"]["count"],
      "success_rate": r["metrics"]["success_rate"],
      "relevance_score": r["relevance_score"]
    }
    for r in ranked[:20]  # Top 20 for checkpoint (full data in memory)
  ],
  "total_categories": len(ranked),
  "timestamp": now_iso8601()
}

checkpoint.output.aggregated_results = aggregated_results

# Write updated checkpoint
Write(file_path=f"devforgeai/workflows/{ANALYTICS_ID}-phase-state.json", content=json_dumps(checkpoint))
```

**VERIFY:**
```
Glob(pattern=f"devforgeai/workflows/{ANALYTICS_ID}-phase-state.json")
```
Checkpoint file exists and contains `aggregated_results`.

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${ANALYTICS_ID} --workflow=analytics --phase=03 --step=3.6 --project-root=. 2>&1
```
Update checkpoint: `phases["03"].steps_completed.append("3.6")`

---

## Exit Gate

```bash
source .venv/bin/activate && devforgeai-validate phase-complete ${ANALYTICS_ID} --workflow=analytics --phase=03 --checkpoint-passed --project-root=. 2>&1
```

Update checkpoint:
- `phases["03"].status = "completed"`
- `progress.phases_completed.append("03")`
- `progress.current_phase = 4`
- `progress.total_steps_completed += 6`

Write updated checkpoint to disk. Verify via `Glob()`.

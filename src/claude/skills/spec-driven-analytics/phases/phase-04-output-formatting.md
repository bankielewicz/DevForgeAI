# Phase 04: Output Formatting & Caching

## Entry Gate

```bash
source .venv/bin/activate && devforgeai-validate phase-check ${ANALYTICS_ID} --workflow=analytics --from=03 --to=04 --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Proceed to Phase 04 |
| 127 | CLI not installed - proceed without enforcement |
| Other | HALT - Phase 03 not complete |

## Contract

- **PURPOSE:** Format aggregated results as user-friendly markdown using query-specific templates, then cache the output
- **REQUIRED SUBAGENTS:** none
- **REQUIRED REFERENCES:** `references/output-templates.md`
- **REQUIRED ARTIFACTS:** `aggregated_results` and `ranked` data from Phase 03
- **STEP COUNT:** 5 mandatory steps

---

## Reference Loading [MANDATORY]

```
Read(file_path="src/claude/skills/spec-driven-analytics/references/output-templates.md")
```

IF Read fails: HALT -- "output-templates.md reference missing"

---

## Mandatory Steps (5)

### Step 4.1: Load Output Templates

**EXECUTE:**
```
# Template definitions loaded from reference file above
# Select the template matching the current query type

TEMPLATES = {
  "dashboard": {
    "title": "Dashboard Overview",
    "section": "Key Metrics",
    "columns": ["Metric", "Value", "Trend"]
  },
  "workflows": {
    "title": "Workflow Distribution",
    "section": "Workflow Patterns",
    "columns": ["Workflow Type", "Count", "Success Rate"]
  },
  "errors": {
    "title": "Error Analysis",
    "section": "Top Errors by Frequency",
    "columns": ["Error Type", "Count", "Last Seen"]
  },
  "decisions": {
    "title": "Decision Archive",
    "section": "Key Decisions",
    "columns": ["Date", "Story", "Decision", "Rationale"]
  },
  "story": {
    "title": f"Story Deep Dive: {STORY_ID}",
    "section": "Timeline",
    "columns": ["Phase", "Started", "Completed", "Duration"]
  },
  "command-patterns": {
    "title": "Command Sequence Analysis",
    "section": "Top Command Sequences",
    "columns": ["Rank", "Sequence", "Frequency", "Success Rate"]
  }
}

template = TEMPLATES[QUERY_TYPE]
Display: f"Template selected: {template['title']}"
```

**VERIFY:**
`template` contains `title`, `section`, and `columns` keys.
IF template is null: HALT -- "No template for query type: {QUERY_TYPE}"

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${ANALYTICS_ID} --workflow=analytics --phase=04 --step=4.1 --project-root=. 2>&1
```
Update checkpoint: `phases["04"].steps_completed.append("4.1")`

---

### Step 4.2: Generate Markdown Table

**EXECUTE:**
```
# Build the results table based on template columns and ranked data
table_header = "| " + " | ".join(template["columns"]) + " |"
table_separator = "|" + "|".join(["---" for _ in template["columns"]]) + "|"

table_rows = []
FOR i, result in enumerate(ranked[:15]):  # Top 15 results
  row = format_row(result, QUERY_TYPE, template["columns"])
  table_rows.append("| " + " | ".join(row) + " |")

IF len(table_rows) == 0:
  table_rows = ["| No results found | - | - |"]

results_table = "\n".join([table_header, table_separator] + table_rows)

Display: f"Generated table with {len(table_rows)} rows"
```

**VERIFY:**
`results_table` is a non-empty string containing markdown table syntax (pipes and dashes).

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${ANALYTICS_ID} --workflow=analytics --phase=04 --step=4.2 --project-root=. 2>&1
```
Update checkpoint: `phases["04"].steps_completed.append("4.2")`

---

### Step 4.3: Generate Full Markdown Output

**EXECUTE:**
```
# Assemble the complete markdown output
cache_status = "hit" IF CACHE_HIT ELSE "miss"
timestamp = now_iso8601()
period = f"Last {DAYS_LIMIT} days" IF DAYS_LIMIT ELSE "All available data"

# Generate recommendations based on data
recommendations = generate_recommendations(ranked, QUERY_TYPE, global_metrics)

formatted_output = f"""## {template['title']}

**Generated:** {timestamp} | **Period:** {period} | **Cache:** {cache_status}

### Summary

**Total entries analyzed:** {global_metrics['total_entries']}
**Categories found:** {global_metrics['total_categories']}
**Overall success rate:** {global_metrics['overall_success_rate']:.1f}%

### {template['section']}

{results_table}

### Recommendations

{chr(10).join(f'{i+1}. {rec}' for i, rec in enumerate(recommendations))}

---
*Source: session-miner subagent | Analytics ID: {ANALYTICS_ID} | Cached for: {3600 if not CACHE_HIT else 'N/A'}s*
"""

Display: f"Formatted output generated ({len(formatted_output)} chars)"
```

**VERIFY:**
`formatted_output` is a non-empty string containing the template title, results table, and recommendations.
IF formatted_output length < 50: HALT -- "Formatted output suspiciously short"

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${ANALYTICS_ID} --workflow=analytics --phase=04 --step=4.3 --project-root=. 2>&1
```
Update checkpoint: `phases["04"].steps_completed.append("4.3")`

---

### Step 4.4: Write Cache Entry

**EXECUTE:**
```
# Write results to cache for future queries
cache_entry = {
  "cache_key": checkpoint.cache.cache_key,
  "created_at": now_iso8601(),
  "ttl_seconds": 3600,
  "expires_at": (now + timedelta(hours=1)).isoformat(),
  "query": {
    "type": QUERY_TYPE,
    "story_id": STORY_ID,
    "days_limit": DAYS_LIMIT,
    "query_param": QUERY_PARAM
  },
  "results": {
    "summary": global_metrics,
    "data": [{"key": r["key"], "metrics": r["metrics"]} for r in ranked[:20]],
    "recommendations": recommendations,
    "formatted_output": formatted_output
  }
}

# Ensure cache directory exists
cache_dir = "devforgeai/cache/analytics"
Write(file_path=f"{cache_dir}/{checkpoint.cache.cache_key}.json", content=json_dumps(cache_entry))
```

**VERIFY:**
```
Glob(pattern=f"devforgeai/cache/analytics/{checkpoint.cache.cache_key}.json")
```
Cache file exists on disk.
IF not found: Display "WARNING: Cache write failed - continuing without cache"

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${ANALYTICS_ID} --workflow=analytics --phase=04 --step=4.4 --project-root=. 2>&1
```
Update checkpoint: `phases["04"].steps_completed.append("4.4")`

---

### Step 4.5: Record Formatted Output in Checkpoint

**EXECUTE:**
```
checkpoint.output.formatted_output = formatted_output

# Write updated checkpoint
Write(file_path=f"devforgeai/workflows/{ANALYTICS_ID}-phase-state.json", content=json_dumps(checkpoint))
```

**VERIFY:**
```
Glob(pattern=f"devforgeai/workflows/{ANALYTICS_ID}-phase-state.json")
```
Checkpoint file exists and was updated.

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${ANALYTICS_ID} --workflow=analytics --phase=04 --step=4.5 --project-root=. 2>&1
```
Update checkpoint: `phases["04"].steps_completed.append("4.5")`

---

## Exit Gate

```bash
source .venv/bin/activate && devforgeai-validate phase-complete ${ANALYTICS_ID} --workflow=analytics --phase=04 --checkpoint-passed --project-root=. 2>&1
```

Update checkpoint:
- `phases["04"].status = "completed"`
- `progress.phases_completed.append("04")`
- `progress.current_phase = 5`
- `progress.total_steps_completed += 5`

Write updated checkpoint to disk. Verify via `Glob()`.

# Phase 05: Display & Delivery

## Entry Gate

```bash
source .venv/bin/activate && devforgeai-validate phase-check ${ANALYTICS_ID} --workflow=analytics --from=04 --to=05 --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Proceed to Phase 05 |
| 127 | CLI not installed - proceed without enforcement |
| Other | HALT - Phase 04 not complete (or Phase 01 if cache hit) |

**Note:** This phase executes after Phase 04 (cache miss) OR after Phase 01 (cache hit, short-circuit).
When arriving via cache hit, `formatted_output` is loaded from cached results.

## Contract

- **PURPOSE:** Render formatted markdown to user display and show metadata footer
- **REQUIRED SUBAGENTS:** none
- **REQUIRED REFERENCES:** none (self-contained)
- **REQUIRED ARTIFACTS:** `formatted_output` in checkpoint (from Phase 04 or from cache)
- **STEP COUNT:** 3 mandatory steps

---

## Mandatory Steps (3)

### Step 5.1: Render Formatted Markdown to User

**EXECUTE:**
```
# Retrieve formatted output
IF CACHE_HIT:
  # From cache (Phase 01 loaded this)
  formatted_output = checkpoint.output.formatted_output
  IF formatted_output is null:
    # Cache entry may store in results.formatted_output
    formatted_output = cached_results.get("formatted_output", null)
  IF formatted_output is null:
    HALT -- "Cache hit but no formatted output found in cache entry"
ELSE:
  # From Phase 04
  formatted_output = checkpoint.output.formatted_output
  IF formatted_output is null:
    HALT -- "No formatted output from Phase 04"

# Display the formatted analytics to the user
Display: formatted_output
```

**VERIFY:**
`formatted_output` was displayed to the user. Output contains markdown structure (headers, tables).

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${ANALYTICS_ID} --workflow=analytics --phase=05 --step=5.1 --project-root=. 2>&1
```
Update checkpoint: `phases["05"].steps_completed.append("5.1")`

---

### Step 5.2: Display Metadata Footer

**EXECUTE:**
```
cache_status = "HIT (cached)" IF CACHE_HIT ELSE "MISS (fresh)"
remaining_ttl = "N/A"

IF CACHE_HIT:
  # Calculate remaining TTL
  cache_age = calculate_cache_age(checkpoint.cache)
  remaining_ttl = f"{max(0, 3600 - cache_age):.0f}s"

Display: f"""
---
**Analytics Metadata:**
- **Analytics ID:** {ANALYTICS_ID}
- **Query Type:** {QUERY_TYPE}
- **Cache Status:** {cache_status}
- **TTL Remaining:** {remaining_ttl}
- **Source:** session-miner subagent
- **Generated:** {now_iso8601()}

**Quick Commands:**
- `/analytics --force {QUERY_TYPE}` — Force refresh this query
- `/analytics --help` — View all query types
---
"""
```

**VERIFY:**
Metadata footer was displayed. Contains Analytics ID and cache status.

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${ANALYTICS_ID} --workflow=analytics --phase=05 --step=5.2 --project-root=. 2>&1
```
Update checkpoint: `phases["05"].steps_completed.append("5.2")`

---

### Step 5.3: Record Delivery Status in Checkpoint

**EXECUTE:**
```
checkpoint.output.delivery = {
  "displayed": true,
  "cache_status": "hit" IF CACHE_HIT ELSE "miss",
  "timestamp": now_iso8601()
}

# Write updated checkpoint
Write(file_path=f"devforgeai/workflows/{ANALYTICS_ID}-phase-state.json", content=json_dumps(checkpoint))
```

**VERIFY:**
```
Glob(pattern=f"devforgeai/workflows/{ANALYTICS_ID}-phase-state.json")
```
Checkpoint file exists and contains `output.delivery.displayed == true`.

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${ANALYTICS_ID} --workflow=analytics --phase=05 --step=5.3 --project-root=. 2>&1
```
Update checkpoint: `phases["05"].steps_completed.append("5.3")`

---

## Exit Gate

```bash
source .venv/bin/activate && devforgeai-validate phase-complete ${ANALYTICS_ID} --workflow=analytics --phase=05 --checkpoint-passed --project-root=. 2>&1
```

Update checkpoint:
- `phases["05"].status = "completed"`
- `progress.phases_completed.append("05")`
- `progress.current_phase = 6`
- `progress.total_steps_completed += 3`

Write updated checkpoint to disk. Verify via `Glob()`.

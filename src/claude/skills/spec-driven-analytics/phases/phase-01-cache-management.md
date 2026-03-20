# Phase 01: Cache Management

## Entry Gate

```bash
source .venv/bin/activate && devforgeai-validate phase-check ${ANALYTICS_ID} --workflow=analytics --from=00 --to=01 --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Proceed to Phase 01 |
| 127 | CLI not installed - proceed without enforcement |
| Other | HALT - Phase 00 not complete |

## Contract

- **PURPOSE:** Check cache for existing results matching the query, determine cache hit/miss, handle force refresh
- **REQUIRED SUBAGENTS:** none
- **REQUIRED REFERENCES:** `references/cache-management.md`
- **REQUIRED ARTIFACTS:** Checkpoint JSON must exist from Phase 00 with `input.query_type` populated
- **STEP COUNT:** 5 mandatory steps

---

## Reference Loading [MANDATORY]

```
Read(file_path="src/claude/skills/spec-driven-analytics/references/cache-management.md")
```

IF Read fails: HALT -- "cache-management.md reference missing"

---

## Mandatory Steps (5)

### Step 1.1: Generate Cache Key

**EXECUTE:**
```
# Build cache key from query parameters
query_type = checkpoint.input.query_type
story_id = checkpoint.input.story_id
days_limit = checkpoint.input.days_limit
query_param = checkpoint.input.query_param

# Deterministic key generation
key_parts = [query_type]
IF story_id: key_parts.append(story_id)
IF days_limit: key_parts.append(f"days-{days_limit}")
IF query_param: key_parts.append(query_param.replace(" ", "-"))

cache_key = "_".join(key_parts)
cache_path = f"devforgeai/cache/analytics/{cache_key}.json"

Display: f"Cache key: {cache_key}"
Display: f"Cache path: {cache_path}"
```

**VERIFY:**
`cache_key` is a non-empty string. `cache_path` follows pattern `devforgeai/cache/analytics/*.json`.
IF either is empty: HALT -- "Cache key generation failed"

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${ANALYTICS_ID} --workflow=analytics --phase=01 --step=1.1 --project-root=. 2>&1
```
Update checkpoint: `cache.cache_key = cache_key`, `cache.cache_path = cache_path`, `phases["01"].steps_completed.append("1.1")`

---

### Step 1.2: Check Cache File Existence

**EXECUTE:**
```
cache_files = Glob(pattern=cache_path)

IF cache_files:
  Display: f"Cache file found: {cache_path}"
  cache_exists = true
ELSE:
  Display: "No cache file found - cache miss"
  cache_exists = false
```

**VERIFY:**
`cache_exists` is a boolean (true or false). Glob completed without error.

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${ANALYTICS_ID} --workflow=analytics --phase=01 --step=1.2 --project-root=. 2>&1
```
Update checkpoint: `phases["01"].steps_completed.append("1.2")`

---

### Step 1.3: Validate Cache Freshness

**EXECUTE:**
```
IF cache_exists:
  Read(file_path=cache_path)
  cache_data = parse_json(content)

  cache_created = parse_datetime(cache_data.created_at)
  cache_age_seconds = (now - cache_created).total_seconds()
  TTL = 3600  # 1 hour

  IF cache_age_seconds < TTL:
    Display: f"Cache is fresh ({cache_age_seconds:.0f}s old, TTL={TTL}s)"
    cache_fresh = true
    cached_results = cache_data.results
  ELSE:
    Display: f"Cache is stale ({cache_age_seconds:.0f}s old, TTL={TTL}s expired)"
    cache_fresh = false
ELSE:
  cache_fresh = false
```

**VERIFY:**
`cache_fresh` is a boolean. If cache_exists was true, `cache_age_seconds` is a non-negative number.

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${ANALYTICS_ID} --workflow=analytics --phase=01 --step=1.3 --project-root=. 2>&1
```
Update checkpoint: `phases["01"].steps_completed.append("1.3")`

---

### Step 1.4: Handle Force Refresh

**EXECUTE:**
```
force_refresh = checkpoint.input.force_refresh

IF force_refresh AND cache_exists:
  Display: "Force refresh requested - invalidating cache"
  # Mark cache as stale regardless of TTL
  cache_fresh = false
  cache_exists = false
  Display: f"Cache invalidated: {cache_path}"
ELIF force_refresh AND NOT cache_exists:
  Display: "Force refresh requested but no cache exists - proceeding to mine"
```

**VERIFY:**
If `force_refresh` is true, then `cache_fresh` must be false.

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${ANALYTICS_ID} --workflow=analytics --phase=01 --step=1.4 --project-root=. 2>&1
```
Update checkpoint: `phases["01"].steps_completed.append("1.4")`

---

### Step 1.5: Record Cache Status and Set CACHE_HIT

**EXECUTE:**
```
CACHE_HIT = cache_exists AND cache_fresh AND NOT force_refresh

IF CACHE_HIT:
  Display: "CACHE HIT - Loading cached results (skipping Phases 02-04)"
  # Store cached results for Phase 05 to display
  checkpoint.output.aggregated_results = cached_results
  checkpoint.output.formatted_output = cached_results
ELSE:
  Display: "CACHE MISS - Proceeding to session-miner orchestration"

checkpoint.cache.cache_hit = CACHE_HIT
```

**VERIFY:**
`CACHE_HIT` is a boolean. If CACHE_HIT is true, `checkpoint.output.aggregated_results` is populated.
If CACHE_HIT is false, checkpoint is ready for Phase 02.

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${ANALYTICS_ID} --workflow=analytics --phase=01 --step=1.5 --project-root=. 2>&1
```
Update checkpoint: `cache.cache_hit = CACHE_HIT`, `phases["01"].steps_completed.append("1.5")`

---

## Exit Gate

```bash
source .venv/bin/activate && devforgeai-validate phase-complete ${ANALYTICS_ID} --workflow=analytics --phase=01 --checkpoint-passed --project-root=. 2>&1
```

Update checkpoint:
- `phases["01"].status = "completed"`
- `progress.phases_completed.append("01")`
- `progress.current_phase = 2` (or 5 if CACHE_HIT)
- `progress.total_steps_completed += 5`

Write updated checkpoint to disk. Verify via `Glob()`.

**CACHE HIT SHORT-CIRCUIT:** If CACHE_HIT is true, set `progress.current_phase = 5` and skip to Phase 05.
Also mark Phases 02, 03, 04 as "skipped_cache_hit" in the checkpoint.

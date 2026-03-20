# Phase 06: Completion & Summary

## Entry Gate

```bash
source .venv/bin/activate && devforgeai-validate phase-check ${ANALYTICS_ID} --workflow=analytics --from=05 --to=06 --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Proceed to Phase 06 |
| 127 | CLI not installed - proceed without enforcement |
| Other | HALT - Phase 05 not complete |

## Contract

- **PURPOSE:** Validate workflow completion, update final checkpoint status, and display completion banner
- **REQUIRED SUBAGENTS:** none
- **REQUIRED REFERENCES:** none (self-contained)
- **REQUIRED ARTIFACTS:** All checkpoint data from Phases 01-05
- **STEP COUNT:** 3 mandatory steps

---

## Mandatory Steps (3)

### Step 6.1: Workflow Completion Validation

**EXECUTE:**
```
# Read current checkpoint
Read(file_path=f"devforgeai/workflows/{ANALYTICS_ID}-phase-state.json")

# Verify required phases completed
completed_phases = checkpoint.progress.phases_completed

IF CACHE_HIT:
  # On cache hit, only phases 01, 05 must be completed (02-04 skipped)
  required_phases = ["01", "05"]
  skipped_phases = ["02", "03", "04"]
ELSE:
  # On cache miss, all phases 01-05 must be completed
  required_phases = ["01", "02", "03", "04", "05"]
  skipped_phases = []

missing_phases = [p for p in required_phases if p not in completed_phases]

IF missing_phases:
  HALT -- f"WORKFLOW INCOMPLETE - Missing required phases: {missing_phases}"

# Verify output was delivered
IF checkpoint.output.delivery is null OR checkpoint.output.delivery.displayed != true:
  HALT -- "Output was not delivered to user (Phase 05 incomplete)"

Display: f"Workflow completion validation passed - {len(completed_phases)} phases completed"
IF skipped_phases:
  Display: f"Phases skipped (cache hit): {skipped_phases}"
```

**VERIFY:**
All required phases appear in `completed_phases`. Output delivery confirmed.

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${ANALYTICS_ID} --workflow=analytics --phase=06 --step=6.1 --project-root=. 2>&1
```
Update checkpoint: `phases["06"].steps_completed.append("6.1")`

---

### Step 6.2: Display Completion Banner

**EXECUTE:**
```
# Gather summary data from checkpoint
query_type = checkpoint.input.query_type
cache_hit = checkpoint.cache.cache_hit
total_steps = checkpoint.progress.total_steps_completed
created_at = checkpoint.created_at

Display: f"""
------------------------------------------------------------
  Analytics Session Complete
------------------------------------------------------------

Session Details:
  Analytics ID:   {ANALYTICS_ID}
  Query Type:     {query_type}
  Cache Status:   {"HIT (fast path)" IF cache_hit ELSE "MISS (full pipeline)"}
  Phases Run:     {len(checkpoint.progress.phases_completed) + 1}/7
  Steps Executed: {total_steps}
  Started:        {created_at}
  Completed:      {now_iso8601()}

Quick Commands:
  /analytics                          # Dashboard overview
  /analytics workflows                # Workflow patterns
  /analytics errors                   # Error mining
  /analytics decisions "query"        # Decision search
  /analytics story STORY-XXX          # Story analysis
  /analytics command-patterns         # Command sequences
  /analytics --force {query_type}     # Refresh this query

------------------------------------------------------------
"""
```

**VERIFY:**
Completion banner was displayed with Analytics ID and session summary.

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${ANALYTICS_ID} --workflow=analytics --phase=06 --step=6.2 --project-root=. 2>&1
```
Update checkpoint: `phases["06"].steps_completed.append("6.2")`

---

### Step 6.3: Finalize Checkpoint

**EXECUTE:**
```
# Update final checkpoint status
checkpoint.status = "completed"
checkpoint.updated_at = now_iso8601()
checkpoint.phases["06"].status = "completed"
checkpoint.progress.phases_completed.append("06")
checkpoint.progress.current_phase = 7  # Workflow complete
checkpoint.progress.total_steps_completed += 3

# Write final checkpoint
Write(file_path=f"devforgeai/workflows/{ANALYTICS_ID}-phase-state.json", content=json_dumps(checkpoint))
```

**VERIFY:**
```
Glob(pattern=f"devforgeai/workflows/{ANALYTICS_ID}-phase-state.json")
```
Checkpoint file exists. Status is "completed".

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${ANALYTICS_ID} --workflow=analytics --phase=06 --step=6.3 --project-root=. 2>&1
```

---

## Exit Gate

```bash
source .venv/bin/activate && devforgeai-validate phase-complete ${ANALYTICS_ID} --workflow=analytics --phase=06 --checkpoint-passed --project-root=. 2>&1
```

Display: "Analytics workflow complete. All phases executed successfully."

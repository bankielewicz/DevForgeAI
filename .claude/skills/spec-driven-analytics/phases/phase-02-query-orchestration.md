# Phase 02: Query Routing & Subagent Orchestration

## Entry Gate

```bash
source .venv/bin/activate && devforgeai-validate phase-check ${ANALYTICS_ID} --workflow=analytics --from=01 --to=02 --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Proceed to Phase 02 |
| 127 | CLI not installed - proceed without enforcement |
| Other | HALT - Phase 01 not complete |

## Contract

- **PURPOSE:** Route query to session-miner subagent with query-specific prompts and capture raw session data
- **REQUIRED SUBAGENTS:** session-miner (BLOCKING)
- **REQUIRED REFERENCES:** `references/query-configuration.md`, `references/session-miner-delegation.md`
- **REQUIRED ARTIFACTS:** Checkpoint JSON with `input.query_type` and `cache.cache_hit == false`
- **STEP COUNT:** 5 mandatory steps

---

## Reference Loading [MANDATORY]

```
Read(file_path="src/claude/skills/spec-driven-analytics/references/query-configuration.md")
Read(file_path="src/claude/skills/spec-driven-analytics/references/session-miner-delegation.md")
```

IF either Read fails: HALT -- "Phase 02 reference file missing"

---

## Mandatory Steps (5)

### Step 2.1: Load Query Configuration

**EXECUTE:**
```
# Query configuration loaded from reference file above
# Map query_type to description and prompt focus

QUERY_CONFIGS = {
  "dashboard": {
    "description": "Generate dashboard metrics from session data",
    "prompt_focus": "Extract workflow counts, error rates, completion times, session duration metrics"
  },
  "workflows": {
    "description": "Analyze workflow patterns from sessions",
    "prompt_focus": "Group by workflow type (/dev, /qa, /create-story, etc.), calculate success rates, identify most frequent patterns"
  },
  "errors": {
    "description": "Extract error patterns from sessions",
    "prompt_focus": "Find error messages, categorize by type (tool error, validation error, timeout), rank by frequency"
  },
  "decisions": {
    "description": "Surface development decisions from sessions",
    "prompt_focus": "Extract ADR references, AskUserQuestion interactions, architecture choices, technology decisions"
  },
  "story": {
    "description": f"Deep analysis of story {STORY_ID}",
    "prompt_focus": f"Filter by story ID {STORY_ID}, extract timeline, identify key events, phase durations, blockers"
  },
  "command-patterns": {
    "description": "Extract high-frequency command sequences",
    "prompt_focus": "Route to n-gram analysis, extract 2-grams and 3-grams, top 10 by frequency with success rates"
  }
}

query_config = QUERY_CONFIGS[QUERY_TYPE]
Display: f"Query config loaded: {query_config['description']}"
```

**VERIFY:**
`query_config` contains `description` and `prompt_focus` keys. `QUERY_TYPE` is a valid key in `QUERY_CONFIGS`.
IF query_config is null: HALT -- "No configuration for query type: {QUERY_TYPE}"

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${ANALYTICS_ID} --workflow=analytics --phase=02 --step=2.1 --project-root=. 2>&1
```
Update checkpoint: `phases["02"].steps_completed.append("2.1")`

---

### Step 2.2: Build Session-Miner Prompt

**EXECUTE:**
```
# Construct the full prompt for session-miner subagent
# Include query type, focus, and any filters

prompt_parts = [
  f"Analyze Claude Code session history to {query_config['description'].lower()}.",
  f"Focus: {query_config['prompt_focus']}.",
]

IF DAYS_LIMIT:
  prompt_parts.append(f"Time window: Last {DAYS_LIMIT} days only.")

IF STORY_ID:
  prompt_parts.append(f"Filter: Only entries related to {STORY_ID}.")

IF QUERY_PARAM:
  prompt_parts.append(f"Search filter: '{QUERY_PARAM}'.")

prompt_parts.append("Return structured JSON with entries array containing SessionEntry objects.")
prompt_parts.append("Each entry: timestamp, command, status (success|error|partial), duration_ms, user_input, model, session_id, project.")

session_miner_prompt = "\n".join(prompt_parts)

Display: f"Session-miner prompt built ({len(session_miner_prompt)} chars)"
```

**VERIFY:**
`session_miner_prompt` is a non-empty string containing the query focus.
IF empty: HALT -- "Failed to build session-miner prompt"

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${ANALYTICS_ID} --workflow=analytics --phase=02 --step=2.2 --project-root=. 2>&1
```
Update checkpoint: `phases["02"].steps_completed.append("2.2")`

---

### Step 2.3: Invoke Session-Miner Subagent [BLOCKING]

**EXECUTE:**
```
Task(
  subagent_type="session-miner",
  description=query_config["description"],
  prompt=session_miner_prompt
)
```

This is a BLOCKING invocation. The workflow cannot proceed until the session-miner returns results.

**VERIFY:**
Session-miner returned a response. Response contains data (entries, counts, or structured output).
IF session-miner returns error:
  Log error to checkpoint.output.error
  Display: "session-miner subagent error: {error_details}"
  AskUserQuestion:
    Question: "Session-miner encountered an error. How should we proceed?"
    Header: "Error"
    Options:
      - label: "Retry"
        description: "Invoke session-miner again with the same prompt"
      - label: "Abort"
        description: "Stop the analytics workflow"
  IF "Retry": Re-execute Step 2.3
  IF "Abort": HALT -- "Analytics aborted by user after session-miner error"

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${ANALYTICS_ID} --workflow=analytics --phase=02 --step=2.3 --project-root=. 2>&1
```
Update checkpoint: `phases["02"].steps_completed.append("2.3")`

---

### Step 2.4: Verify Subagent Response Structure

**EXECUTE:**
```
# Validate the response from session-miner
raw_response = session_miner_output

# Check for expected structure
IF raw_response contains entries or structured data:
  entry_count = count(raw_response.entries) IF has_entries ELSE "unstructured"
  Display: f"Session-miner returned {entry_count} entries"
  raw_entries = raw_response
ELSE:
  Display: "WARNING: Session-miner returned unexpected format"
  raw_entries = raw_response  # Pass through for Phase 03 to handle
```

**VERIFY:**
`raw_entries` is populated (non-null). Response was received from session-miner.
IF raw_entries is null: HALT -- "Session-miner returned null response"

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${ANALYTICS_ID} --workflow=analytics --phase=02 --step=2.4 --project-root=. 2>&1
```
Update checkpoint: `phases["02"].steps_completed.append("2.4")`

---

### Step 2.5: Record Raw Response in Checkpoint

**EXECUTE:**
```
# Store raw response summary in checkpoint (not full data - may be large)
checkpoint.output.raw_entries = {
  "entry_count": entry_count,
  "query_type": QUERY_TYPE,
  "timestamp": now_iso8601(),
  "response_summary": truncate(str(raw_entries), 500)  # First 500 chars for debugging
}

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
source .venv/bin/activate && devforgeai-validate phase-record ${ANALYTICS_ID} --workflow=analytics --phase=02 --step=2.5 --project-root=. 2>&1
```
Update checkpoint: `phases["02"].steps_completed.append("2.5")`

---

## Exit Gate

```bash
source .venv/bin/activate && devforgeai-validate phase-complete ${ANALYTICS_ID} --workflow=analytics --phase=02 --checkpoint-passed --project-root=. 2>&1
```

Update checkpoint:
- `phases["02"].status = "completed"`
- `progress.phases_completed.append("02")`
- `progress.current_phase = 3`
- `progress.total_steps_completed += 5`

Write updated checkpoint to disk. Verify via `Glob()`.

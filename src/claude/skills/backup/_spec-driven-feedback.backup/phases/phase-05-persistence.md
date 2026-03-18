# Phase 05: Persistence & Indexing

## Entry Gate

```bash
devforgeai-validate phase-check ${SESSION_ID} --workflow=feedback --from=04 --to=05 --project-root=.
```

| Exit Code | Action |
|-----------|--------|
| 0 | Prerequisites met. Proceed. |
| 1 | Phase 04 incomplete. HALT. |
| 2 | Validation error. HALT. |
| 127 | CLI not installed. Proceed without enforcement. |

---

## Contract

- **PURPOSE:** Write validated feedback to filesystem, update feedback index, update feedback register, verify all artifacts on disk
- **REQUIRED SUBAGENTS:** none
- **REQUIRED ARTIFACTS:** Feedback file on disk, index.json updated, feedback-register.md updated, recommendations-queue.json updated (if ai_analysis)
- **STEP COUNT:** 5
- **REFERENCE FILES:**
  - `.claude/skills/devforgeai-feedback/references/feedback-persistence-guide.md`
  - `.claude/skills/devforgeai-feedback/references/feedback-export-formats.md`

---

## Reference Loading [MANDATORY]

```
Read(file_path=".claude/skills/devforgeai-feedback/references/feedback-persistence-guide.md")
Read(file_path=".claude/skills/devforgeai-feedback/references/feedback-export-formats.md")
```

IF either Read fails: HALT -- "Phase 05 reference files not loaded. Cannot proceed without reference material."

Do NOT rely on memory of previous reads. Load ALL references fresh.

---

## Skip Conditions

For operational feedback types (`config`, `search`) that do not produce persistent feedback documents:

```
IF $FEEDBACK_TYPE in ["config", "search"]:
  # These types produce real-time results, not stored feedback
  # Skip Steps 5.1-5.4, go directly to Step 5.5 (checkpoint update only)
  Update checkpoint:
    phases["05"].status = "completed"
    phases["05"].skipped_reason = "Operational type — no persistent artifact"
    output.feedback_file_path = "N/A"
  GOTO Exit Gate
```

For all other types, execute ALL steps below.

---

## Mandatory Steps (5)

### Step 5.1: Compute Output File Path

**EXECUTE:**
```
Generate file path based on feedback type and naming convention:

SWITCH $FEEDBACK_TYPE:
  CASE "conversation":
    file_path = "devforgeai/feedback/sessions/${timestamp}-${operation_type}-${story_id_or_session}.md"
    # Example: devforgeai/feedback/sessions/20260316-083045-dev-STORY-042.md

  CASE "summary":
    file_path = "devforgeai/feedback/sessions/${timestamp}-${operation_type}-${story_id_or_session}-summary.md"

  CASE "metrics":
    file_path = "devforgeai/feedback/sessions/${timestamp}-${operation_type}-${story_id_or_session}-metrics.json"

  CASE "checklist":
    file_path = "devforgeai/feedback/sessions/${timestamp}-sprint-retrospective.md"

  CASE "ai_analysis":
    file_path = "devforgeai/feedback/ai-analysis/${story_id}/${timestamp}-ai-analysis.json"

  CASE "triage":
    file_path = "devforgeai/feedback/sessions/${timestamp}-triage-results.md"

  CASE "export":
    file_path = $OUTPUT_PATH or "devforgeai/feedback/exports/${timestamp}-export.${format}"

  CASE "import":
    file_path = "N/A"  # Import does not create a new feedback file; it imports existing ones

WHERE:
  timestamp = YYYYMMDD-HHmmss (e.g., 20260316-083045)
  operation_type = dev, qa, release, etc.
  story_id_or_session = STORY-042 or SESSION_ID

# Verify parent directory exists
parent_dir = directory portion of file_path
parent_exists = Glob(pattern="${parent_dir}/*") or Glob(pattern="${parent_dir}/.gitkeep")
IF parent does not exist:
  Write(file_path="${parent_dir}/.gitkeep", content="")
```

**VERIFY:** File path is non-null and parent directory exists.
```
IF file_path is null AND $FEEDBACK_TYPE != "import": HALT -- "File path not computed"
```

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=feedback --phase=05 --step=5.1 --project-root=.
```
Update checkpoint:
```
checkpoint.phases["05"].file_path = file_path
checkpoint.output.feedback_file_path = file_path
checkpoint.phases["05"].steps_completed.append("5.1")
```

---

### Step 5.2: Write Feedback File

**EXECUTE:**
```
IF $FEEDBACK_TYPE == "import":
  # Import already wrote files in Phase 03 sub-workflow
  # Skip this step
  GOTO Step 5.3

Write(file_path=file_path, content=formatted_feedback_data)
```

**VERIFY:** File exists on disk.
```
Glob(pattern=file_path)
IF not found: HALT -- "Feedback file was NOT written to disk: ${file_path}"
```

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=feedback --phase=05 --step=5.2 --project-root=.
```
Update checkpoint:
```
checkpoint.phases["05"].file_written = true
checkpoint.phases["05"].steps_completed.append("5.2")
```

---

### Step 5.3: Update Feedback Index

**EXECUTE:**
```
index_path = "devforgeai/feedback/index.json"
index_exists = Glob(pattern=index_path)

IF index_exists:
  Read(file_path=index_path)
  Parse existing index JSON
ELSE:
  Create new index: { "version": "1.0", "last_updated": "", "entries": [] }

# Append new entry
new_entry = {
  "session_id": SESSION_ID,
  "filename": file_path,
  "operation": $OPERATION_CONTEXT.operation_type,
  "status": $OPERATION_CONTEXT.status,
  "story_id": $OPERATION_CONTEXT.story_id,
  "timestamp": current ISO 8601,
  "duration_ms": $OPERATION_CONTEXT.duration_seconds * 1000,
  "template": template_file or "N/A",
  "feedback_type": $FEEDBACK_TYPE,
  "keywords": extracted_keywords,
  "sentiment": detected_sentiment or "neutral"
}

index.entries.append(new_entry)
index.last_updated = current ISO 8601

Write(file_path=index_path, content=updated_index_json)
```

**VERIFY:**
```
Read(file_path=index_path)
Grep(pattern=SESSION_ID, path=index_path)
IF not found: HALT -- "Feedback index was NOT updated with session ${SESSION_ID}"
```

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=feedback --phase=05 --step=5.3 --project-root=.
```
Update checkpoint:
```
checkpoint.phases["05"].index_updated = true
checkpoint.phases["05"].steps_completed.append("5.3")
```

---

### Step 5.4: Update Feedback Register

**EXECUTE:**
```
register_path = "devforgeai/feedback/feedback-register.md"
register_exists = Glob(pattern=register_path)

IF register_exists:
  Read(file_path=register_path)
ELSE:
  Create new register with header:
  "# Feedback Register\n\n| ID | Date | Type | Operation | Story | Status | File |\n|---|---|---|---|---|---|---|"

# Append new row
new_row = "| ${SESSION_ID} | ${date} | ${FEEDBACK_TYPE} | ${operation_type} | ${story_id} | completed | ${file_path} |"

Append new_row to register content

Write(file_path=register_path, content=updated_register)
```

**VERIFY:**
```
Grep(pattern=SESSION_ID, path=register_path)
IF not found: HALT -- "Feedback register was NOT updated with session ${SESSION_ID}"
```

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=feedback --phase=05 --step=5.4 --project-root=.
```
Update checkpoint:
```
checkpoint.phases["05"].register_updated = true
checkpoint.phases["05"].steps_completed.append("5.4")
```

---

### Step 5.5: Update Recommendations Queue (Conditional)

**EXECUTE:**
```
IF $FEEDBACK_TYPE == "ai_analysis":
  # Queue was already updated in Phase 03 Step 3.5A
  # Verify it was actually written
  queue_path = "devforgeai/feedback/ai-analysis/aggregated/recommendations-queue.json"
  queue_exists = Glob(pattern=queue_path)

  IF queue_exists:
    Read(file_path=queue_path)
    # Verify our session's recommendations are in the queue
    checkpoint.phases["05"].queue_updated = true
  ELSE:
    checkpoint.phases["05"].queue_updated = false
    Log: "Recommendations queue not found — may not have had HIGH priority items"

ELSE:
  # Not ai_analysis type — no queue update needed
  checkpoint.phases["05"].queue_updated = "N/A"
```

**VERIFY:** If ai_analysis type, queue verification completed. Otherwise, marked N/A.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=feedback --phase=05 --step=5.5 --project-root=.
```
Update checkpoint:
```
checkpoint.phases["05"].status = "completed"
checkpoint.phases["05"].steps_completed.append("5.5")
checkpoint.progress.current_phase = 6
checkpoint.progress.phases_completed.append("05")
checkpoint.output.feedback_id = SESSION_ID
```
Write updated checkpoint to disk.

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --workflow=feedback --phase=05 --checkpoint-passed --project-root=.
```

---

## Exit Verification Checklist

Before proceeding to Phase 06, verify ALL:

- [ ] feedback-persistence-guide.md loaded successfully
- [ ] feedback-export-formats.md loaded successfully
- [ ] File path computed (or N/A for import/config/search)
- [ ] Feedback file written to disk (verified via Glob)
- [ ] Index updated (verified via Grep for SESSION_ID)
- [ ] Register updated (verified via Grep for SESSION_ID)
- [ ] Queue updated if ai_analysis (verified or N/A)
- [ ] Checkpoint updated with phase 05 completion
- [ ] Checkpoint written to disk (verified via Glob)

**IF any criterion is unmet: HALT. Do NOT proceed to Phase 06.**

---

## Phase Transition Display

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Phase 05: Persistence ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  File: ${file_path}
  Index: Updated ✓
  Register: Updated ✓
  Queue: ${queue_updated}
  Feedback ID: ${SESSION_ID}
  Steps: 5/5
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

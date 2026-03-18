# Phase 01: Context Detection & Sanitization

## Entry Gate

```bash
devforgeai-validate phase-check ${SESSION_ID} --workflow=feedback --from=00 --to=01 --project-root=.
```

| Exit Code | Action |
|-----------|--------|
| 0 | Prerequisites met. Proceed. |
| 1 | Phase 00 incomplete. HALT. |
| 2 | Validation error. HALT. |
| 127 | CLI not installed. Proceed without enforcement. |

---

## Contract

- **PURPOSE:** Extract operation context from conversation markers, resolve feedback type, sanitize data for PII/secrets
- **REQUIRED SUBAGENTS:** none
- **REQUIRED ARTIFACTS:** `$OPERATION_CONTEXT` populated, `$FEEDBACK_TYPE` resolved, sanitization applied
- **STEP COUNT:** 5
- **REFERENCE FILES:**
  - `references/context-extraction.md` (~250 lines)
  - `references/context-sanitization.md` (~200 lines)

---

## Reference Loading [MANDATORY]

```
Read(file_path="references/context-extraction.md")
Read(file_path="references/context-sanitization.md")
```

IF either Read fails: HALT -- "Phase 01 reference files not loaded. Cannot proceed without reference material."

Do NOT rely on memory of previous reads. Load ALL references fresh.

---

## Mandatory Steps (5)

### Step 1.1: Load Context Extraction Reference

**EXECUTE:**
```
Read(file_path="references/context-extraction.md")
```

**VERIFY:** Content loaded contains "OperationContext" data model definition.
```
IF content does NOT contain "OperationContext": HALT -- "context-extraction.md did not load correctly"
```

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=feedback --phase=01 --step=1.1 --project-root=.
```
Update checkpoint: `phases["01"].steps_completed.append("1.1")`

---

### Step 1.2: Extract Operation Context

**EXECUTE:**
```
Check conversation for context markers:
  - "**Feedback Mode:**"     → $FEEDBACK_MODE
  - "**Feedback Context:**"  → $FEEDBACK_CONTEXT
  - "**Feedback Source:**"   → $FEEDBACK_SOURCE
  - "**Search Query:**"      → $SEARCH_QUERY
  - "**Severity:**"          → $SEVERITY
  - "**Status:**"            → $STATUS
  - "**Priority Filter:**"   → $PRIORITY_FILTER
  - "**Selected Items:**"    → $SELECTED_ITEMS
  - "**Format:**"            → $FORMAT
  - "**Date Range:**"        → $DATE_RANGE
  - "**Subcommand:**"        → $SUBCOMMAND
  - "**Sanitize:**"          → $SANITIZE
  - "**Output:**"            → $OUTPUT_PATH
  - "**Archive:**"           → $ARCHIVE_PATH

IF no markers found:
  Extract from conversation history:
    - What operation just completed? (dev, qa, release, orchestrate)
    - What story was being worked on? (STORY-NNN)
    - What was the outcome? (success, failure, partial)

  Set defaults:
    $FEEDBACK_MODE = "conversation"
    $FEEDBACK_SOURCE = "manual"

Build $OPERATION_CONTEXT:
  operation_type: $operation_type or "unknown"
  status: $operation_status or "unknown"
  story_id: extracted story ID or null
  duration_seconds: extracted or null
  phases_completed: extracted or []
  error: extracted error or null
```

**VERIFY:** `$OPERATION_CONTEXT` contains at minimum `operation_type` and `status` fields (even if "unknown").
```
IF $OPERATION_CONTEXT is empty: HALT -- "Failed to extract any operation context"
```

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=feedback --phase=01 --step=1.2 --project-root=.
```
Update checkpoint:
```
checkpoint.phases["01"].context_extracted = true
checkpoint.phases["01"].operation_context = $OPERATION_CONTEXT
checkpoint.phases["01"].steps_completed.append("1.2")
```

---

### Step 1.3: Resolve Feedback Type

**EXECUTE:**
```
IF $FEEDBACK_MODE is explicitly set by context marker:
  $FEEDBACK_TYPE = $FEEDBACK_MODE
ELSE IF $SUBCOMMAND is set:
  $FEEDBACK_TYPE = "config"  # Configuration operation, not feedback collection
ELSE IF $SEARCH_QUERY is set:
  $FEEDBACK_TYPE = "search"  # Search operation
ELSE IF $PRIORITY_FILTER is set or $SELECTED_ITEMS is set:
  $FEEDBACK_TYPE = "triage"
ELSE IF $FORMAT is set or $DATE_RANGE is set:
  $FEEDBACK_TYPE = "export"  # Export operation
ELSE IF $ARCHIVE_PATH is set:
  $FEEDBACK_TYPE = "import"  # Import operation
ELSE IF $FEEDBACK_SOURCE == "hook" and context suggests ai_analysis:
  $FEEDBACK_TYPE = "ai_analysis"
ELSE:
  $FEEDBACK_TYPE = "conversation"  # Default
```

**VERIFY:** `$FEEDBACK_TYPE` is one of: `conversation`, `summary`, `metrics`, `checklist`, `ai_analysis`, `triage`, `config`, `search`, `export`, `import`
```
VALID_TYPES = ["conversation", "summary", "metrics", "checklist", "ai_analysis", "triage", "config", "search", "export", "import"]
IF $FEEDBACK_TYPE not in VALID_TYPES: HALT -- "Invalid feedback type: ${FEEDBACK_TYPE}"
```

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=feedback --phase=01 --step=1.3 --project-root=.
```
Update checkpoint:
```
checkpoint.phases["01"].feedback_type_resolved = $FEEDBACK_TYPE
checkpoint.phases["01"].steps_completed.append("1.3")
```

---

### Step 1.4: Load Sanitization Reference

**EXECUTE:**
```
Read(file_path="references/context-sanitization.md")
```

**VERIFY:** Content loaded contains sanitization patterns (secret removal, PII removal).
```
IF content does NOT contain "REDACTED": HALT -- "context-sanitization.md did not load correctly"
```

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=feedback --phase=01 --step=1.4 --project-root=.
```
Update checkpoint: `phases["01"].steps_completed.append("1.4")`

---

### Step 1.5: Apply Sanitization

**EXECUTE:**
```
Apply sanitization patterns from context-sanitization.md to $OPERATION_CONTEXT:

Secret Removal:
  - Environment variables: [A-Z_]*KEY/SECRET/TOKEN/PASSWORD/CREDENTIAL/AUTH[A-Z_]*\s*=\s*\S+
  - API keys: Bearer tokens, AWS (AKIA/ASIA), GitHub (ghp_), OpenAI (sk-)
  - Credential file paths: *.pem, *.key, id_rsa.*, *.env, credentials, secrets, password

PII Removal:
  - Email addresses
  - Phone numbers
  - SSN patterns
  - Credit card patterns

Replace with redaction markers:
  [REDACTED:SECRET], [REDACTED:API_KEY], [REDACTED:TOKEN],
  [REDACTED:EMAIL], [REDACTED:PHONE], [REDACTED:SSN], [REDACTED:CARD]

Apply 3-pass verification to prevent evasion.
```

**VERIFY:** Grep the sanitized context for common secret patterns. Expected: 0 matches.
```
IF Grep finds any of: api_key=, password=, secret=, Bearer , AKIA, ghp_, sk-
  in $OPERATION_CONTEXT: HALT -- "Sanitization failed. Secrets still present."
```

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=feedback --phase=01 --step=1.5 --project-root=.
```
Update checkpoint:
```
checkpoint.phases["01"].sanitization_applied = true
checkpoint.phases["01"].status = "completed"
checkpoint.phases["01"].steps_completed.append("1.5")
checkpoint.progress.current_phase = 2
checkpoint.progress.phases_completed.append("01")
```
Write updated checkpoint to disk.

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --workflow=feedback --phase=01 --checkpoint-passed --project-root=.
```

---

## Exit Verification Checklist

Before proceeding to Phase 02, verify ALL:

- [ ] context-extraction.md loaded successfully
- [ ] context-sanitization.md loaded successfully
- [ ] `$OPERATION_CONTEXT` has `operation_type` and `status`
- [ ] `$FEEDBACK_TYPE` resolved to valid type
- [ ] Sanitization applied (no secrets in context)
- [ ] Checkpoint updated with phase 01 completion
- [ ] Checkpoint written to disk (verified via Glob)

**IF any criterion is unmet: HALT. Do NOT proceed to Phase 02.**

---

## Phase Transition Display

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Phase 01: Context Detection ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Feedback Type: ${FEEDBACK_TYPE}
  Operation: ${OPERATION_CONTEXT.operation_type}
  Status: ${OPERATION_CONTEXT.status}
  Story: ${OPERATION_CONTEXT.story_id || 'N/A'}
  Sanitized: Yes
  Steps: 5/5
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

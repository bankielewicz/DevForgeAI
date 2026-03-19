# Phase 04: Interactive Selection

## Entry Gate

```bash
source .venv/bin/activate && devforgeai-validate phase-check ${SESSION_ID} --workflow=qa-remediation --from=03 --to=04 --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Phase 03 complete. Proceed. |
| 1 | Phase 03 incomplete. HALT. |
| 2 | Validation error. HALT. |
| 127 | CLI not installed. Proceed without enforcement. |

---

## Contract

| Field | Value |
|-------|-------|
| **PURPOSE** | Display gap summary, handle dry-run exit, interactive gap selection |
| **REFERENCE** | None (user interaction phase) |
| **STEP COUNT** | 4 mandatory steps |

---

## Phase Exit Criteria

- [ ] Gap summary table displayed to user
- [ ] IF dry-run: summary displayed and skill EXIT
- [ ] IF not dry-run: `$SELECTED_GAPS` populated (or user cancelled)
- [ ] `$SELECTION_COUNT` set
- [ ] Checkpoint updated

IF any applicable criteria unchecked: HALT -- "Phase 04 exit criteria not met"

---

## Reference Loading [MANDATORY]

Phase 04 is a user interaction phase -- no external reference files to load.

All logic is inline within this phase file.

---

## Mandatory Steps (4)

### Step 4.1: Display Gap Summary Table

**EXECUTE:**
```
# Calculate statistics
$BLOCKING_GAPS_COUNT = count where gap.blocking == true in $FILTERED_GAPS
$ADVISORY_GAPS_COUNT = count where gap.blocking == false in $FILTERED_GAPS

# Display summary table
Display:
"
+-----+-------------------+----------------------------------------+-----------+-------+-------------------+--------+
| #   | Type              | File                                   | Severity  | Score | Source            | Status |
+-----+-------------------+----------------------------------------+-----------+-------+-------------------+--------+
"

FOR i, gap in enumerate($FILTERED_GAPS):
    status_indicator = "[R]" IF gap.blocking ELSE "[Y]"
    source_display = gap.source_story
    IF gap.occurrences > 1:
        source_display += " (+{gap.occurrences - 1})"

    Display:
    "| {i+1:3} | {gap.type:17} | {gap.file:38} | {gap.severity:9} | {gap.score:5} | {source_display:17} | {status_indicator:6} |"

Display:
"
+-----+-------------------+----------------------------------------+-----------+-------+-------------------+--------+
Status: [R] = Blocking   [Y] = Advisory
"

# Display statistics summary
Display:
"
Gap Statistics:
  Files Processed:        ${FILES_PROCESSED}
  Total Gaps Found:       ${TOTAL_GAPS}
  After Deduplication:    ${len($UNIQUE_GAPS_LIST)}
  Above Threshold:        ${GAPS_ABOVE_THRESHOLD}
  Deferred (below):       ${len($DEFERRED_GAPS)}
  Blocking:               ${BLOCKING_GAPS_COUNT}
  Advisory:               ${ADVISORY_GAPS_COUNT}
"

IF $BLOCKING_ONLY == true:
    Display: "  Advisory Hidden:      ${ADVISORY_HIDDEN_COUNT} (--blocking-only active)"

IF $GAPS_ABOVE_THRESHOLD == 0:
    Display:
    ""
    "No gaps above the ${MIN_SEVERITY} severity threshold."
    "Consider re-running with --min-severity LOW to see all gaps."
```

**VERIFY:** Table rendered with correct column count. Statistics summary displayed. Status indicators [R] and [Y] correctly assigned based on `blocking` field.

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${SESSION_ID} --workflow=qa-remediation --phase=04 --step=4.1 --project-root=. 2>&1
```
Update checkpoint: `phases["04"].steps_completed.append("4.1")`

---

### Step 4.2: Handle Dry-Run Mode

**EXECUTE:**
```
IF $DRY_RUN == true:
    Display:
    "
    ============================================
    DRY-RUN COMPLETE
    ============================================
    Gap discovery, parsing, aggregation, and
    prioritization completed. No stories created.
    No reports updated. No debt entries added.

    To create stories from these gaps, re-run
    without --dry-run flag.
    ============================================
    "

    # Update checkpoint for dry-run completion
    Update checkpoint:
      status = "completed"
      progress.current_phase = 4
      progress.phases_completed.append("04")
      progress.phases_skipped = ["05", "06", "07"]
      phases["04"].status = "completed"
      phases["05"].status = "skipped"
      phases["06"].status = "skipped"
      phases["07"].status = "skipped"

    Write updated checkpoint to disk.

    # Record dry-run completion
    source .venv/bin/activate && devforgeai-validate phase-record ${SESSION_ID} --workflow=qa-remediation --phase=04 --step=4.2 --project-root=. 2>&1

    EXIT skill -- no further phases execute

ELSE:
    Display: "Not in dry-run mode. Proceeding to interactive selection."
```

**VERIFY:** If `$DRY_RUN == true`: summary displayed, checkpoint updated with "completed" status, phases 05-07 marked "skipped", skill EXITs. If `$DRY_RUN == false`: step passes through to Step 4.3.

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${SESSION_ID} --workflow=qa-remediation --phase=04 --step=4.2 --project-root=. 2>&1
```
Update checkpoint: `phases["04"].steps_completed.append("4.2")`

---

### Step 4.3: Interactive Selection

**EXECUTE:**
```
IF $GAPS_ABOVE_THRESHOLD == 0:
    Display: "No gaps to select. Proceeding with empty selection."
    $SELECTED_GAPS = []
    $SELECTION_COUNT = 0
    # Skip to Step 4.4
    GOTO Step 4.4

# Count gaps by severity for option labels
$CRITICAL_COUNT = count where gap.severity == "CRITICAL" in $FILTERED_GAPS
$HIGH_COUNT = count where gap.severity == "HIGH" in $FILTERED_GAPS
$CRITICAL_HIGH_COUNT = $CRITICAL_COUNT + $HIGH_COUNT

AskUserQuestion:
    Question: "Select which gaps to create remediation stories for:"
    Header: "Gap Selection"
    Options:
        - label: "All gaps above threshold (${GAPS_ABOVE_THRESHOLD} items)"
          description: "Create stories for all ${GAPS_ABOVE_THRESHOLD} gaps at ${MIN_SEVERITY}+ severity"
        - label: "CRITICAL only (${CRITICAL_COUNT} items)"
          description: "Create stories for CRITICAL severity gaps only"
        - label: "CRITICAL + HIGH only (${CRITICAL_HIGH_COUNT} items)"
          description: "Create stories for CRITICAL and HIGH severity gaps"
        - label: "None - cancel"
          description: "Exit without creating any stories"
    multiSelect: false

# Process user response
IF user selects "None - cancel":
    Display: "User cancelled gap selection. Exiting gracefully."

    Update checkpoint:
      status = "cancelled"
      progress.current_phase = 4
      progress.phases_completed.append("04")
      phases["04"].status = "completed"

    EXIT skill -- no further phases execute
```

**VERIFY:** AskUserQuestion was presented to user. User made a selection. If user cancelled, skill exits gracefully with checkpoint updated.

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${SESSION_ID} --workflow=qa-remediation --phase=04 --step=4.3 --project-root=. 2>&1
```
Update checkpoint: `phases["04"].steps_completed.append("4.3")`

---

### Step 4.4: Process Selection

**EXECUTE:**
```
# Map user choice to gap filter
IF user selected "All gaps above threshold":
    $SELECTED_GAPS = $FILTERED_GAPS
    $SELECTION_LABEL = "ALL (${MIN_SEVERITY}+)"

ELIF user selected "CRITICAL only":
    $SELECTED_GAPS = [gap for gap in $FILTERED_GAPS if gap.severity == "CRITICAL"]
    $SELECTION_LABEL = "CRITICAL only"

ELIF user selected "CRITICAL + HIGH only":
    $SELECTED_GAPS = [gap for gap in $FILTERED_GAPS if gap.severity in ["CRITICAL", "HIGH"]]
    $SELECTION_LABEL = "CRITICAL + HIGH"

ELIF $GAPS_ABOVE_THRESHOLD == 0:
    $SELECTED_GAPS = []
    $SELECTION_LABEL = "None (no gaps above threshold)"

$SELECTION_COUNT = len($SELECTED_GAPS)

# Enforce batch safety limit from config
IF $SELECTION_COUNT > $CONFIG.batch_mode.max_stories_per_run:
    Display:
    "Warning: Selection (${SELECTION_COUNT}) exceeds max_stories_per_run (${CONFIG.batch_mode.max_stories_per_run})."
    "Truncating to first ${CONFIG.batch_mode.max_stories_per_run} gaps by priority score."

    $SELECTED_GAPS = $SELECTED_GAPS[:$CONFIG.batch_mode.max_stories_per_run]
    $SELECTION_COUNT = len($SELECTED_GAPS)

Display:
"Selection: ${SELECTION_LABEL}"
"  Gaps selected: ${SELECTION_COUNT}"
"  Blocking: {count where blocking == true in $SELECTED_GAPS}"
"  Advisory: {count where blocking == false in $SELECTED_GAPS}"
```

**VERIFY:** `$SELECTED_GAPS` populated with correct filter applied. `$SELECTION_COUNT` matches `len($SELECTED_GAPS)`. If batch limit applied, `$SELECTION_COUNT <= $CONFIG.batch_mode.max_stories_per_run`.

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${SESSION_ID} --workflow=qa-remediation --phase=04 --step=4.4 --project-root=. 2>&1
```
Update checkpoint: `phases["04"].steps_completed.append("4.4")`

---

## Phase Exit Verification

```
Verify all exit criteria:
1. Gap summary table displayed to user                             -> CHECK
2. IF dry-run: summary displayed and skill EXIT                    -> CHECK (or N/A)
3. IF not dry-run: $SELECTED_GAPS populated (or user cancelled)    -> CHECK
4. $SELECTION_COUNT set                                            -> CHECK

Update checkpoint:
  progress.current_phase = 4
  progress.phases_completed.append("04")
  phases["04"].status = "completed"

IF any applicable check fails: HALT -- "Phase 04 exit verification failed on: {failed_criteria}"

Display:
"Phase 04 Complete: Interactive Selection"
"  Selection: ${SELECTION_LABEL}"
"  Gaps Selected: ${SELECTION_COUNT}"
"  Proceeding to Phase 05: Batch Story Creation..."
```

## Exit Gate

```bash
source .venv/bin/activate && devforgeai-validate phase-complete ${SESSION_ID} --workflow=qa-remediation --phase=04 --checkpoint-passed --project-root=. 2>&1
# Exit 0: proceed to Phase 05 | Exit 1: HALT
```

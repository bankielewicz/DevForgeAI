# Phase 07: Technical Debt Integration

## Entry Gate

```bash
source .venv/bin/activate && devforgeai-validate phase-check ${SESSION_ID} --workflow=qa-remediation --from=06 --to=07 --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Phase 06 verified complete. Proceed to Phase 07. |
| 1 | Phase 06 not complete. HALT -- resolve Phase 06 first. |
| 127 | CLI not installed. Proceed without enforcement. |

---

## Contract

| Field | Value |
|-------|-------|
| **PURPOSE** | Add deferred gaps to technical debt register with optional analysis |
| **REFERENCE** | references/technical-debt-update.md |
| **STEP COUNT** | 8 mandatory steps |

---

## Phase Exit Criteria

- [ ] `$DEFERRED_GAPS` either added to register or user declined
- [ ] `$DEBT_ENTRIES_ADDED` count set
- [ ] `$REGISTER_UPDATED` boolean set
- [ ] Register statistics updated (if entries added)
- [ ] Checkpoint updated

IF any unchecked: HALT -- "Phase 07 exit criteria not met"

---

## Reference Loading [MANDATORY]

```
Read(file_path=".claude/skills/spec-driven-qa-remediation/references/technical-debt-update.md")
```

This reference contains the debt register entry format, statistics update rules, analyzer invocation protocol, and entry template. It MUST be loaded before executing any steps in this phase.

---

## Mandatory Steps (8)

### Step 7.1: Load Reference

**EXECUTE:**
```
Read(file_path=".claude/skills/spec-driven-qa-remediation/references/technical-debt-update.md")

IF Read succeeds:
    $DEBT_UPDATE_REF = loaded content
    Display: "Reference loaded: technical-debt-update.md"
ELSE:
    HALT: "Required reference file not found: references/technical-debt-update.md"
```

**VERIFY:** `$DEBT_UPDATE_REF` is non-null and contains debt register update procedures. Confirm content includes "debt register" or "debt entry" terminology.

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${SESSION_ID} --workflow=qa-remediation --phase=07 --step=7.1 --project-root=. 2>&1
```
Update checkpoint: `phases["07"].steps_completed.append("7.1")`

---

### Step 7.2: Check Configuration

**EXECUTE:**
```
# Read configuration for technical debt auto-add setting
$AUTO_ADD_SKIPPED = $CONFIG.technical_debt.auto_add_skipped  # From Phase 01 config

Display:
  "Technical Debt Configuration:"
  "  auto_add_skipped: ${AUTO_ADD_SKIPPED}"
  "  --add-to-debt flag: ${ADD_TO_DEBT}"
  "  Deferred gaps count: ${len($DEFERRED_GAPS)}"

IF $AUTO_ADD_SKIPPED == false AND $ADD_TO_DEBT == false:
    Display: "Technical debt auto-add is disabled and --add-to-debt flag not set."
    Display: "Skipping to Step 7.8 (optional analyzer)."
    $SKIP_DEBT_INTEGRATION = true
ELSE:
    $SKIP_DEBT_INTEGRATION = false

IF len($DEFERRED_GAPS) == 0:
    Display: "No deferred gaps to add to debt register. Skipping to Step 7.8."
    $SKIP_DEBT_INTEGRATION = true
```

**VERIFY:** Configuration values read correctly. Skip decision is consistent with config and flags. If `$AUTO_ADD_SKIPPED == false AND $ADD_TO_DEBT == false`, skip is true. If `$DEFERRED_GAPS` is empty, skip is true.

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${SESSION_ID} --workflow=qa-remediation --phase=07 --step=7.2 --project-root=. 2>&1
```
Update checkpoint: `phases["07"].steps_completed.append("7.2")`

---

### Step 7.3: Handle Auto Mode

**EXECUTE:**
```
IF $SKIP_DEBT_INTEGRATION == true:
    Display: "Debt integration skipped (config or no deferred gaps). Proceeding to Step 7.8."
    $DEBT_ENTRIES_ADDED = 0
    $REGISTER_UPDATED = false
    # Jump to Step 7.8
ELSE:
    IF $ADD_TO_DEBT == true:
        # Auto mode: skip confirmation, set source
        $PROCEED_WITH_DEBT = true
        $DEBT_SOURCE = "qa_remediation"
        $SKIP_DEBT_CONFIRMATION = true

        Display:
          "--add-to-debt flag active: Auto-adding ${len($DEFERRED_GAPS)} deferred gaps to debt register"

        # Pre-populate Follow-up field with story IDs from Phase 05
        IF len($CREATED_STORIES) > 0:
            Display: "Pre-populating Follow-up with ${len($STORY_ID_MAP)} created story IDs"

    ELSE:
        # Config allows auto-add but flag not set -- will confirm in Step 7.4
        $PROCEED_WITH_DEBT = null  # Determined in Step 7.4
        $DEBT_SOURCE = "qa_remediation"
        $SKIP_DEBT_CONFIRMATION = false
```

**VERIFY:** If `$ADD_TO_DEBT == true`, `$PROCEED_WITH_DEBT` is true and `$SKIP_DEBT_CONFIRMATION` is true. If not auto-mode, `$PROCEED_WITH_DEBT` is null (awaiting user input in Step 7.4).

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${SESSION_ID} --workflow=qa-remediation --phase=07 --step=7.3 --project-root=. 2>&1
```
Update checkpoint: `phases["07"].steps_completed.append("7.3")`

---

### Step 7.4: User Confirmation

**EXECUTE:**
```
IF $SKIP_DEBT_INTEGRATION == true OR $SKIP_DEBT_CONFIRMATION == true:
    # Already decided in Step 7.2 or 7.3
    IF $SKIP_DEBT_INTEGRATION == true:
        Display: "Step 7.4 skipped: Debt integration not applicable."
    ELSE:
        Display: "Step 7.4 skipped: Auto-mode (--add-to-debt) bypasses confirmation."
ELSE:
    # Interactive confirmation required
    AskUserQuestion:
        Question: "Add ${len($DEFERRED_GAPS)} deferred gaps to technical debt register?"
        Header: "Technical Debt Integration"
        Options:
            - label: "Yes - Add to debt register"
              description: "Add all ${len($DEFERRED_GAPS)} deferred gaps as open debt items"
            - label: "No - Skip debt integration"
              description: "Do not add deferred gaps to the register"

    IF user selects "Yes":
        $PROCEED_WITH_DEBT = true
        Display: "User confirmed: Adding ${len($DEFERRED_GAPS)} gaps to debt register"
    ELSE:
        $PROCEED_WITH_DEBT = false
        $DEBT_ENTRIES_ADDED = 0
        $REGISTER_UPDATED = false
        Display: "User declined debt integration. Skipping to Step 7.8."
```

**VERIFY:** `$PROCEED_WITH_DEBT` is set to true or false. If false, `$DEBT_ENTRIES_ADDED` is 0 and `$REGISTER_UPDATED` is false.

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${SESSION_ID} --workflow=qa-remediation --phase=07 --step=7.4 --project-root=. 2>&1
```
Update checkpoint: `phases["07"].steps_completed.append("7.4")`

---

### Step 7.5: Read Current Register

**EXECUTE:**
```
IF $PROCEED_WITH_DEBT != true:
    Display: "Step 7.5 skipped: Debt integration not proceeding."
ELSE:
    $REGISTER_PATH = $CONFIG.technical_debt.register_path
        # Default: "devforgeai/technical-debt-register.md"

    register_content = Read(file_path=$REGISTER_PATH)

    IF Read fails:
        Display: "Debt register not found at: ${REGISTER_PATH}. Creating new register."
        $REGISTER_EXISTS = false
        $EXISTING_DEBT_COUNT = 0
    ELSE:
        $REGISTER_EXISTS = true

        # Locate "## Open Debt Items" section
        Grep(pattern="## Open Debt Items", path=$REGISTER_PATH)

        IF no match:
            HALT: "Debt register exists but missing '## Open Debt Items' section at: ${REGISTER_PATH}"

        # Count existing open items for statistics
        $EXISTING_DEBT_COUNT = count lines matching "^### GAP-" in register_content

        Display:
          "Debt register loaded: ${REGISTER_PATH}"
          "  Existing open items: ${EXISTING_DEBT_COUNT}"
          "  Section '## Open Debt Items' found"
```

**VERIFY:** If proceeding, either register was loaded with "## Open Debt Items" section found, or register does not exist and will be created. `$REGISTER_PATH` is set.

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${SESSION_ID} --workflow=qa-remediation --phase=07 --step=7.5 --project-root=. 2>&1
```
Update checkpoint: `phases["07"].steps_completed.append("7.5")`

---

### Step 7.6: Generate Debt Entries

**EXECUTE:**
```
IF $PROCEED_WITH_DEBT != true:
    Display: "Step 7.6 skipped: Debt integration not proceeding."
ELSE:
    $DEBT_ENTRIES = []
    $CURRENT_DATE = "{YYYY-MM-DD}"  # Current date

    FOR each gap in $DEFERRED_GAPS:
        # Determine follow-up field
        IF $STORY_ID_MAP contains gap.id:
            follow_up = $STORY_ID_MAP[gap.id]  # Created story ID from Phase 05
        ELSE:
            follow_up = "Pending remediation"

        # Format debt entry using template from reference
        entry = """
### GAP-${gap.id}

| Field | Value |
|-------|-------|
| **Date Added** | ${CURRENT_DATE} |
| **Type** | ${gap.gap_type} |
| **Source Report** | ${gap.source_file} |
| **Original Severity** | ${gap.severity} |
| **Skipped Reason** | ${gap.skip_reason or "Below severity threshold"} |
| **Follow-up** | ${follow_up} |
| **Priority** | ${map_severity_to_debt_priority(gap.severity)} |
| **Status** | Open |
| **Resolution Target** | Next sprint |
| **Estimated Effort** | ${estimate_effort(gap.gap_type)} |

**Gap Details:** ${gap.description}
"""
        $DEBT_ENTRIES.append(entry)

    Display: "Generated ${len($DEBT_ENTRIES)} debt entries"
    FOR each entry_preview in $DEBT_ENTRIES:
        Display: "  - GAP-${gap.id}: ${gap.gap_type} (${gap.severity})"
```

**VERIFY:** `$DEBT_ENTRIES` has same length as `$DEFERRED_GAPS`. Each entry contains all required fields (Date Added, Type, Source Report, Original Severity, Skipped Reason, Follow-up, Priority, Status, Resolution Target, Estimated Effort, Gap Details).

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${SESSION_ID} --workflow=qa-remediation --phase=07 --step=7.6 --project-root=. 2>&1
```
Update checkpoint: `phases["07"].steps_completed.append("7.6")`

---

### Step 7.7: Append to Register

**EXECUTE:**
```
IF $PROCEED_WITH_DEBT != true:
    Display: "Step 7.7 skipped: Debt integration not proceeding."
    $DEBT_ENTRIES_ADDED = 0
    $REGISTER_UPDATED = false
ELSE:
    IF $REGISTER_EXISTS == false:
        # Create new register with header and entries
        new_register = """# Technical Debt Register

## Summary Statistics

| Metric | Value |
|--------|-------|
| **Total Open Items** | ${len($DEBT_ENTRIES)} |
| **Last Analysis** | ${CURRENT_DATE} |

## Open Debt Items

${join($DEBT_ENTRIES, "\n")}
"""
        Write(file_path=$REGISTER_PATH, content=new_register)

    ELSE:
        # Insert new entries after "## Open Debt Items" header
        # Read current content to find insertion point
        register_content = Read(file_path=$REGISTER_PATH)

        # Insert entries immediately after "## Open Debt Items" line
        entries_block = join($DEBT_ENTRIES, "\n")

        Edit(
            file_path=$REGISTER_PATH,
            old_string="## Open Debt Items",
            new_string="## Open Debt Items\n\n${entries_block}"
        )

        # Update statistics section
        new_total = $EXISTING_DEBT_COUNT + len($DEBT_ENTRIES)

        # Update "Total Open Items" count
        Edit(
            file_path=$REGISTER_PATH,
            old_string="| **Total Open Items** | ${EXISTING_DEBT_COUNT} |",
            new_string="| **Total Open Items** | ${new_total} |"
        )

        # Update "Last Analysis" date
        Edit(
            file_path=$REGISTER_PATH,
            old_string="| **Last Analysis** |",
            new_string="| **Last Analysis** | ${CURRENT_DATE} |"
        )

    $DEBT_ENTRIES_ADDED = len($DEBT_ENTRIES)
    $REGISTER_UPDATED = true

    Display:
      "Debt register updated: ${REGISTER_PATH}"
      "  Entries added: ${DEBT_ENTRIES_ADDED}"
      "  New total open items: ${$EXISTING_DEBT_COUNT + $DEBT_ENTRIES_ADDED}"
      "  Last analysis date: ${CURRENT_DATE}"
```

**VERIFY:** Register file contains the new entries.
```
IF $REGISTER_UPDATED == true:
    FOR each gap in $DEFERRED_GAPS:
        Grep(pattern="GAP-${gap.id}", path=$REGISTER_PATH)
        IF no match:
            HALT: "Debt entry GAP-${gap.id} not found in register after update"

    Display: "All ${DEBT_ENTRIES_ADDED} entries verified in register"
```

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${SESSION_ID} --workflow=qa-remediation --phase=07 --step=7.7 --project-root=. 2>&1
```
Update checkpoint: `phases["07"].steps_completed.append("7.7")`

---

### Step 7.8: Optional Analyzer Invocation

**EXECUTE:**
```
# Check config for analyzer invocation setting
$INVOKE_ANALYZER = $CONFIG.technical_debt.invoke_analyzer  # From Phase 01 config

IF $INVOKE_ANALYZER == true:
    Display: "Invoking technical-debt-analyzer subagent..."

    Task(
        subagent_type="technical-debt-analyzer",
        context={
            register_path:     $REGISTER_PATH,
            new_items:         $DEBT_ENTRIES_ADDED,
            total_items:       $EXISTING_DEBT_COUNT + $DEBT_ENTRIES_ADDED,
            session_id:        $SESSION_ID,
            deferred_gaps:     $DEFERRED_GAPS,
            created_stories:   $CREATED_STORIES
        }
    )

    Display: "Technical debt analyzer completed"

ELSE:
    Display: "Technical debt analyzer not enabled (config.technical_debt.invoke_analyzer=${INVOKE_ANALYZER}). Skipping."
```

**VERIFY:** If analyzer was configured to run, Task completed without error. If not configured, step completed with skip message.

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${SESSION_ID} --workflow=qa-remediation --phase=07 --step=7.8 --project-root=. 2>&1
```
Update checkpoint: `phases["07"].steps_completed.append("7.8")`

---

## Phase Exit Verification

```
Verify all exit criteria:
1. $DEFERRED_GAPS either added to register or user declined     -> CHECK
   $PROCEED_WITH_DEBT == true AND $REGISTER_UPDATED == true
   OR $PROCEED_WITH_DEBT == false (user declined or config disabled)
   OR $SKIP_DEBT_INTEGRATION == true (no deferred gaps or config disabled)
2. $DEBT_ENTRIES_ADDED count set                                -> CHECK
   Integer >= 0
3. $REGISTER_UPDATED boolean set                                -> CHECK
   true or false
4. Register statistics updated (if entries added)               -> CHECK
   IF $REGISTER_UPDATED: "Total Open Items" and "Last Analysis" verified
5. Checkpoint updated with all 8 steps                          -> CHECK

IF any check fails: HALT -- "Phase 07 exit verification failed on: {failed_criteria}"

Update checkpoint:
  phases["07"].status = "completed"
  output.debt_entries_added = $DEBT_ENTRIES_ADDED

Display:
"Phase 07 Complete: Technical Debt Integration"
"  Deferred Gaps: ${len($DEFERRED_GAPS)}"
"  Entries Added to Register: ${DEBT_ENTRIES_ADDED}"
"  Register Updated: ${REGISTER_UPDATED}"
"  Analyzer Invoked: ${INVOKE_ANALYZER}"
"  All 7 phases complete. Proceeding to workflow completion..."
```

## Exit Gate

```bash
source .venv/bin/activate && devforgeai-validate phase-complete ${SESSION_ID} --workflow=qa-remediation --phase=07 --checkpoint-passed --project-root=. 2>&1
# Exit 0: workflow complete | Exit 1: HALT
```

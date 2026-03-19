# Phase 06: Source Report Update

## Entry Gate

```bash
source .venv/bin/activate && devforgeai-validate phase-check ${SESSION_ID} --workflow=qa-remediation --from=05 --to=06 --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Phase 05 verified complete. Proceed to Phase 06. |
| 1 | Phase 05 not complete. HALT -- resolve Phase 05 first. |
| 127 | CLI not installed. Proceed without enforcement. |

---

## Contract

| Field | Value |
|-------|-------|
| **PURPOSE** | Update gap files with story references and generate enhancement report |
| **REFERENCE** | references/report-update-protocol.md |
| **STEP COUNT** | 4 mandatory steps |

---

## Phase Exit Criteria

- [ ] Local gap files updated with `implemented_in` field (Grep confirms)
- [ ] Enhancement report file exists on disk (Glob confirms)
- [ ] `$REPORTS_UPDATED` count set
- [ ] `$ENHANCEMENT_REPORT_PATH` set
- [ ] Checkpoint updated

IF any unchecked: HALT -- "Phase 06 exit criteria not met"

---

## Reference Loading [MANDATORY]

```
Read(file_path=".claude/skills/spec-driven-qa-remediation/references/report-update-protocol.md")
```

This reference contains the gap file update protocol, imported file read-only policy, enhancement report template variables, and hook invocation specification. It MUST be loaded before executing any steps in this phase.

---

## Mandatory Steps (4)

### Step 6.1: Load Reference

**EXECUTE:**
```
Read(file_path=".claude/skills/spec-driven-qa-remediation/references/report-update-protocol.md")

IF Read succeeds:
    $REPORT_UPDATE_REF = loaded content
    Display: "Reference loaded: report-update-protocol.md"
ELSE:
    HALT: "Required reference file not found: references/report-update-protocol.md"
```

**VERIFY:** `$REPORT_UPDATE_REF` is non-null and contains report update procedures. Confirm content includes "update protocol" or "gap file" terminology.

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${SESSION_ID} --workflow=qa-remediation --phase=06 --step=6.1 --project-root=. 2>&1
```
Update checkpoint: `phases["06"].steps_completed.append("6.1")`

---

### Step 6.2: Update Local Gap Files

**EXECUTE:**
```
$REPORTS_UPDATED = 0
$UPDATE_ERRORS = []

FOR each created_story in $CREATED_STORIES:
    source_file = created_story.gap_id  # Contains source file path context
    gap_type = created_story.gap_type
    story_id = created_story.story_id

    # Determine the gap file path from source report
    # ONLY update LOCAL files (devforgeai/qa/reports/)
    # Imported files (devforgeai/qa/imports/) are READ-ONLY

    gap_file_path = resolve_gap_file_path(created_story)

    IF gap_file_path starts with "devforgeai/qa/imports/":
        Display: "  SKIP (read-only import): ${gap_file_path}"
        CONTINUE to next story

    # Read the source gap file
    gap_content = Read(file_path=gap_file_path)

    IF Read fails:
        $UPDATE_ERRORS.append({file: gap_file_path, error: "File not found"})
        Display: "  WARN: Could not read gap file: ${gap_file_path}"
        CONTINUE to next story

    # Parse JSON content
    gap_json = parse_json(gap_content)

    # Find the gap entry by type and index
    gap_entries = gap_json[gap_type]  # e.g., gap_json["coverage_gaps"]

    FOR each entry in gap_entries:
        IF entry matches created_story by gap_id or index:
            # Add implementation tracking fields
            entry["implemented_in"] = story_id
            entry["remediation_date"] = "{YYYY-MM-DD}"  # Current date

    # Write updated JSON back to file
    Write(file_path=gap_file_path, content=serialize_json(gap_json))

    $REPORTS_UPDATED = $REPORTS_UPDATED + 1
    Display: "  Updated: ${gap_file_path} -> implemented_in: ${story_id}"

Display:
  "Gap file updates complete:"
  "  Files updated: ${REPORTS_UPDATED}"
  "  Files skipped (imports): ${skipped_count}"
  "  Errors: ${len($UPDATE_ERRORS)}"
```

**VERIFY:** Local gap files contain `implemented_in` field for each created story.
```
FOR each updated_file in local_gap_files:
    Grep(pattern="implemented_in", path=updated_file)
    IF no match found AND file was expected to be updated:
        HALT: "Gap file update verification failed for: ${updated_file}"
```

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${SESSION_ID} --workflow=qa-remediation --phase=06 --step=6.2 --project-root=. 2>&1
```
Update checkpoint: `phases["06"].steps_completed.append("6.2")`

---

### Step 6.3: Generate Enhancement Report

**EXECUTE:**
```
# Load enhancement report template
template_content = Read(file_path=".claude/skills/spec-driven-qa-remediation/assets/templates/enhancement-report-template.md")

IF Read fails:
    HALT: "Enhancement report template not found at assets/templates/enhancement-report-template.md"

# Generate report date
$REPORT_DATE = "{YYYY-MM-DD}"  # Current date

# Compute report path
$ENHANCEMENT_REPORT_PATH = "devforgeai/qa/enhancement-reports/${REPORT_DATE}-enhancement-report.md"

# Fill template variables
report_content = template_content
    .replace("${DATE}", $REPORT_DATE)
    .replace("${SESSION_ID}", $SESSION_ID)
    .replace("${SOURCE}", $SOURCE)
    .replace("${MIN_SEVERITY}", $MIN_SEVERITY)
    .replace("${EPIC_ID}", $EPIC_ID or "N/A")
    .replace("${TOTAL_GAPS}", str($TOTAL_GAPS))
    .replace("${SELECTION_COUNT}", str($SELECTION_COUNT))
    .replace("${STORIES_CREATED_COUNT}", str($STORIES_CREATED_COUNT))
    .replace("${BLOCKING_STORIES_COUNT}", str($BLOCKING_STORIES_COUNT))
    .replace("${ADVISORY_STORIES_COUNT}", str($ADVISORY_STORIES_COUNT))
    .replace("${FAILED_COUNT}", str(len($FAILED_STORIES)))
    .replace("${REPORTS_UPDATED}", str($REPORTS_UPDATED))
    .replace("${CREATED_STORIES_LIST}", format_created_stories_list($CREATED_STORIES))
    .replace("${FAILED_STORIES_LIST}", format_failed_stories_list($FAILED_STORIES))

# Write the enhancement report
Write(file_path=$ENHANCEMENT_REPORT_PATH, content=report_content)

Display: "Enhancement report generated: ${ENHANCEMENT_REPORT_PATH}"
```

**VERIFY:** Enhancement report file exists on disk and contains expected content.
```
Glob(pattern=$ENHANCEMENT_REPORT_PATH)
IF not found:
    HALT: "Enhancement report file was not created at: ${ENHANCEMENT_REPORT_PATH}"

# Verify key content sections exist
Grep(pattern="Stories Created", path=$ENHANCEMENT_REPORT_PATH)
IF no match:
    HALT: "Enhancement report missing expected content sections"
```

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${SESSION_ID} --workflow=qa-remediation --phase=06 --step=6.3 --project-root=. 2>&1
```
Update checkpoint: `phases["06"].steps_completed.append("6.3")`

---

### Step 6.4: Optional Hook Invocation

**EXECUTE:**
```
# Check for post-qa-remediation hook configuration
hook_config_path = "devforgeai/config/hooks.yaml"

hook_content = Read(file_path=hook_config_path)

IF Read fails:
    Display: "No hooks.yaml found. Skipping post-qa-remediation hook."
    $HOOK_INVOKED = false
ELSE:
    # Parse hooks.yaml and check for post-qa-remediation hook
    hooks = parse_yaml(hook_content)

    IF hooks contains "post-qa-remediation" AND hooks["post-qa-remediation"].enabled == true:
        hook_script = hooks["post-qa-remediation"].script

        Display: "Invoking post-qa-remediation hook: ${hook_script}"

        # Build hook context
        hook_context = {
            stories_created:    $STORIES_CREATED_COUNT,
            gaps_deferred:      len($DEFERRED_GAPS),
            report_path:        $ENHANCEMENT_REPORT_PATH,
            session_id:         $SESSION_ID,
            created_story_ids:  [s.story_id for s in $CREATED_STORIES]
        }

        # Invoke hook
        Bash(command="source .venv/bin/activate && ${hook_script} '${json_serialize(hook_context)}' 2>&1")

        $HOOK_INVOKED = true
        Display: "Post-qa-remediation hook completed"

    ELSE:
        Display: "Post-qa-remediation hook not enabled in hooks.yaml. Skipping."
        $HOOK_INVOKED = false
```

**VERIFY:** If hook was configured and enabled, it was invoked. If not configured, step completed with skip message. No errors from hook invocation (warnings are acceptable).

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${SESSION_ID} --workflow=qa-remediation --phase=06 --step=6.4 --project-root=. 2>&1
```
Update checkpoint: `phases["06"].steps_completed.append("6.4")`

---

## Phase Exit Verification

```
Verify all exit criteria:
1. Local gap files updated with implemented_in field             -> CHECK
   Grep confirms "implemented_in" in each updated local gap file
2. Enhancement report file exists on disk                        -> CHECK
   Glob(pattern=$ENHANCEMENT_REPORT_PATH) returns result
3. $REPORTS_UPDATED count set                                    -> CHECK
   $REPORTS_UPDATED >= 0
4. $ENHANCEMENT_REPORT_PATH set                                 -> CHECK
   Non-null string pointing to existing file
5. Checkpoint updated with all 4 steps                           -> CHECK

IF any check fails: HALT -- "Phase 06 exit verification failed on: {failed_criteria}"

Update checkpoint:
  phases["06"].status = "completed"
  output.enhancement_report_path = $ENHANCEMENT_REPORT_PATH

Display:
"Phase 06 Complete: Source Report Update"
"  Gap Files Updated: ${REPORTS_UPDATED}"
"  Enhancement Report: ${ENHANCEMENT_REPORT_PATH}"
"  Hook Invoked: ${HOOK_INVOKED}"
"  Proceeding to Phase 07: Technical Debt Integration..."
```

## Exit Gate

```bash
source .venv/bin/activate && devforgeai-validate phase-complete ${SESSION_ID} --workflow=qa-remediation --phase=06 --checkpoint-passed --project-root=. 2>&1
# Exit 0: proceed to Phase 07 | Exit 1: HALT
```

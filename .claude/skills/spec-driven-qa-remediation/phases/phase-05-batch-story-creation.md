# Phase 05: Batch Story Creation

## Entry Gate

```bash
source .venv/bin/activate && devforgeai-validate phase-check ${SESSION_ID} --workflow=qa-remediation --from=04 --to=05 --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Phase 04 verified complete. Proceed to Phase 05. |
| 1 | Phase 04 not complete. HALT -- resolve Phase 04 first. |
| 127 | CLI not installed. Proceed without enforcement. |

---

## Contract

| Field | Value |
|-------|-------|
| **PURPOSE** | Convert selected gaps to user stories via batch mode |
| **REFERENCE** | references/gap-to-story-mapping.md |
| **STEP COUNT** | 7 mandatory steps |

---

## Phase Exit Criteria

- [ ] All selected gaps processed (created or failed)
- [ ] `$CREATED_STORIES` populated with `{story_id, gap_id, gap_type, is_advisory}`
- [ ] `$FAILED_STORIES` captured (may be empty)
- [ ] `$STORIES_CREATED_COUNT`, `$BLOCKING_STORIES_COUNT`, `$ADVISORY_STORIES_COUNT` set
- [ ] Batch summary displayed
- [ ] Checkpoint updated

IF any unchecked: HALT -- "Phase 05 exit criteria not met"

---

## Reference Loading [MANDATORY]

```
Read(file_path=".claude/skills/spec-driven-qa-remediation/references/gap-to-story-mapping.md")
```

This reference contains the story context marker generation rules, advisory naming conventions (STORY-348), severity-to-priority mapping, and batch invocation protocol. It MUST be loaded before executing any steps in this phase.

---

## Mandatory Steps (7)

### Step 5.1: Load Reference

**EXECUTE:**
```
Read(file_path=".claude/skills/spec-driven-qa-remediation/references/gap-to-story-mapping.md")

IF Read succeeds:
    $GAP_TO_STORY_REF = loaded content
    Display: "Reference loaded: gap-to-story-mapping.md"
ELSE:
    HALT: "Required reference file not found: references/gap-to-story-mapping.md"
```

**VERIFY:** `$GAP_TO_STORY_REF` is non-null and contains story mapping rules. Confirm content includes "context marker" or "story mapping" terminology.

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${SESSION_ID} --workflow=qa-remediation --phase=05 --step=5.1 --project-root=. 2>&1
```
Update checkpoint: `phases["05"].steps_completed.append("5.1")`

---

### Step 5.2: Initialize Tracking

**EXECUTE:**
```
$CREATED_STORIES = []
$FAILED_STORIES = []
$BATCH_INDEX = 0
$STORIES_CREATED_COUNT = 0
$BLOCKING_STORIES_COUNT = 0
$ADVISORY_STORIES_COUNT = 0
$STORY_ID_MAP = {}

Display:
  "Batch tracking initialized:"
  "  Selected gaps to process: ${len($SELECTED_GAPS)}"
  "  Create Stories mode: ${CREATE_STORIES}"
  "  Epic ID: ${EPIC_ID}"
```

**VERIFY:** All tracking variables are initialized. `$CREATED_STORIES` and `$FAILED_STORIES` are empty arrays. `$BATCH_INDEX` is 0. `$SELECTED_GAPS` from Phase 04 is non-empty.

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${SESSION_ID} --workflow=qa-remediation --phase=05 --step=5.2 --project-root=. 2>&1
```
Update checkpoint: `phases["05"].steps_completed.append("5.2")`

---

### Step 5.3: Get Next Story ID

**EXECUTE:**
```
# Discover existing story files to determine next available ID
story_files = Glob(pattern="devforgeai/specs/Stories/STORY-*.story.md")

IF story_files is empty:
    $NEXT_STORY_ID = 1
ELSE:
    # Extract numeric IDs from filenames
    story_ids = []
    FOR each file in story_files:
        Extract numeric portion from filename matching STORY-(\d+)
        story_ids.append(extracted_number)

    max_id = max(story_ids)
    $NEXT_STORY_ID = max_id + 1

Display: "Next available story ID: STORY-${NEXT_STORY_ID} (${len(story_files)} existing stories found)"
```

**VERIFY:** `$NEXT_STORY_ID` is a positive integer greater than 0. If existing stories were found, `$NEXT_STORY_ID` is strictly greater than the highest existing ID.

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${SESSION_ID} --workflow=qa-remediation --phase=05 --step=5.3 --project-root=. 2>&1
```
Update checkpoint: `phases["05"].steps_completed.append("5.3")`

---

### Step 5.4: Handle Auto Mode

**EXECUTE:**
```
IF $CREATE_STORIES == true:
    # Auto mode: skip confirmation, batch all selected gaps
    $GAPS_TO_CREATE = $SELECTED_GAPS
    $SKIP_CONFIRMATION = true

    Display:
      "--create-stories flag active: Batch mode enabled"
      "Processing all ${len($SELECTED_GAPS)} selected gaps without confirmation"

ELSE:
    # Interactive mode: confirm with user before proceeding
    AskUserQuestion:
        Question: "Create remediation stories for ${len($SELECTED_GAPS)} selected gaps?"
        Header: "Batch Story Creation"
        Options:
            - label: "Create all ${len($SELECTED_GAPS)} stories"
              description: "Proceed with batch story creation for all selected gaps"
            - label: "Cancel"
              description: "Skip story creation and proceed to Phase 06"

    IF user selects "Cancel":
        $GAPS_TO_CREATE = []
        $SKIP_CONFIRMATION = false
        Display: "Story creation cancelled by user. Proceeding to Phase 06."
    ELSE:
        $GAPS_TO_CREATE = $SELECTED_GAPS
        $SKIP_CONFIRMATION = false
        Display: "User confirmed: Creating ${len($SELECTED_GAPS)} stories"
```

**VERIFY:** `$GAPS_TO_CREATE` is set (may be empty if cancelled). `$SKIP_CONFIRMATION` reflects the mode used. If cancelled, `$GAPS_TO_CREATE` is empty and workflow proceeds to exit.

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${SESSION_ID} --workflow=qa-remediation --phase=05 --step=5.4 --project-root=. 2>&1
```
Update checkpoint: `phases["05"].steps_completed.append("5.4")`

---

### Step 5.5: Generate Story Context Markers

**EXECUTE:**
```
$STORY_CONTEXT_MARKERS = []

FOR each gap in $GAPS_TO_CREATE:
    $BATCH_INDEX = $BATCH_INDEX + 1
    current_story_id = $NEXT_STORY_ID + ($BATCH_INDEX - 1)

    # Determine if advisory (blocking:false per STORY-348)
    is_advisory = (gap.blocking == false)

    # Generate slug from gap description (lowercase, hyphens, max 40 chars)
    slug = slugify(gap.description)

    # Determine filename pattern
    IF is_advisory:
        filename = "STORY-${current_story_id}-advisory-${slug}.story.md"
        title_prefix = "[ADVISORY] "
        priority = "Low"
    ELSE:
        filename = "STORY-${current_story_id}-${slug}.story.md"
        title_prefix = ""
        priority = map_severity_to_priority(gap.severity)
            # CRITICAL -> High, HIGH -> High, MEDIUM -> Medium, LOW -> Low

    # Build context markers for spec-driven-stories skill
    markers = {
        story_id:           "STORY-${current_story_id}",
        epic_id:            $EPIC_ID or null,
        feature_name:       "${title_prefix}Remediate ${gap.gap_type}: ${gap.description}",
        feature_description: "Remediate QA gap: ${gap.gap_type} - ${gap.description}. Source: ${gap.source_file}, severity: ${gap.severity}.",
        priority:           priority,
        points:             2,  # Standard remediation effort
        type:               determine_type(gap.gap_type),
            # coverage_gap -> "bugfix"
            # anti_pattern_violation -> "refactor"
            # code_quality_violation -> "refactor"
            # deferral_issue -> "bugfix"
        sprint:             "Backlog",
        batch_mode:         true,
        source_report:      gap.source_file,
        source_gap_type:    gap.gap_type,
        source_gap_index:   gap.index,
        is_advisory:        is_advisory,
        source_gap_id:      gap.id,
        source_story_id:    gap.story_id or null,
        filename:           filename
    }

    $STORY_CONTEXT_MARKERS.append(markers)

Display:
  "Generated ${len($STORY_CONTEXT_MARKERS)} story context markers:"
  FOR each m in $STORY_CONTEXT_MARKERS:
      "  ${m.story_id}: ${m.feature_name} [${m.priority}] ${IF m.is_advisory THEN '(advisory)' ELSE '(blocking)'}"
```

**VERIFY:** `$STORY_CONTEXT_MARKERS` has the same length as `$GAPS_TO_CREATE`. Each marker has all required fields (story_id, feature_name, priority, type, batch_mode, is_advisory, filename). Advisory gaps have `[ADVISORY]` prefix in feature_name and `Low` priority.

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${SESSION_ID} --workflow=qa-remediation --phase=05 --step=5.5 --project-root=. 2>&1
```
Update checkpoint: `phases["05"].steps_completed.append("5.5")`

---

### Step 5.6: Invoke Story Creation

**EXECUTE:**
```
FOR each markers in $STORY_CONTEXT_MARKERS:
    Display: "Creating story ${markers.story_id} (${$BATCH_INDEX_CURRENT}/${len($STORY_CONTEXT_MARKERS)})..."

    # Invoke spec-driven-stories skill with batch context
    Skill(command="spec-driven-stories", args="--batch --story-id=${markers.story_id} --epic=${markers.epic_id} --feature='${markers.feature_name}' --description='${markers.feature_description}' --priority=${markers.priority} --points=${markers.points} --type=${markers.type} --sprint=${markers.sprint}")

    # Evaluate result
    IF story creation succeeded:
        created_entry = {
            story_id:     markers.story_id,
            gap_id:       markers.source_gap_id,
            gap_type:     markers.source_gap_type,
            is_advisory:  markers.is_advisory,
            filename:     markers.filename
        }
        $CREATED_STORIES.append(created_entry)
        $STORIES_CREATED_COUNT = $STORIES_CREATED_COUNT + 1

        IF markers.is_advisory:
            $ADVISORY_STORIES_COUNT = $ADVISORY_STORIES_COUNT + 1
        ELSE:
            $BLOCKING_STORIES_COUNT = $BLOCKING_STORIES_COUNT + 1

        # Track for Phase 07 combined flag operation
        $STORY_ID_MAP[markers.source_gap_id] = markers.story_id

        Display: "  Created: ${markers.story_id} -> ${markers.filename}"

    ELSE:
        # Failure isolation: log error, continue to next gap
        failed_entry = {
            gap_id:    markers.source_gap_id,
            gap_type:  markers.source_gap_type,
            story_id:  markers.story_id,
            error:     error_message
        }
        $FAILED_STORIES.append(failed_entry)

        Display: "  FAILED: ${markers.story_id} - ${error_message}"
        Display: "  Continuing to next gap (failure isolation)..."
```

**VERIFY:** `$STORIES_CREATED_COUNT + len($FAILED_STORIES) == len($STORY_CONTEXT_MARKERS)`. Every gap was processed -- either created or failed. No gaps were silently skipped.

```
total_processed = $STORIES_CREATED_COUNT + len($FAILED_STORIES)
IF total_processed != len($STORY_CONTEXT_MARKERS):
    HALT: "Gap processing incomplete: ${total_processed}/${len($STORY_CONTEXT_MARKERS)} processed"
```

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${SESSION_ID} --workflow=qa-remediation --phase=05 --step=5.6 --project-root=. 2>&1
```
Update checkpoint: `phases["05"].steps_completed.append("5.6")`

---

### Step 5.7: Batch Completion Summary

**EXECUTE:**
```
Display:
"============================================================"
"           Batch Story Creation Summary"
"============================================================"
""
"Blocking Stories Created:  ${BLOCKING_STORIES_COUNT}"
"Advisory Stories Created:  ${ADVISORY_STORIES_COUNT}"
"Total Created:             ${STORIES_CREATED_COUNT}"
"Failed:                    ${len($FAILED_STORIES)}"
""

IF len($CREATED_STORIES) > 0:
    Display: "Created Stories:"
    FOR each entry in $CREATED_STORIES:
        advisory_tag = " (advisory)" IF entry.is_advisory ELSE ""
        Display: "  - ${entry.story_id}: ${entry.gap_type}${advisory_tag} -> ${entry.filename}"

IF len($FAILED_STORIES) > 0:
    Display: ""
    Display: "Failed Stories:"
    FOR each entry in $FAILED_STORIES:
        Display: "  - ${entry.story_id}: ${entry.gap_type} -> ERROR: ${entry.error}"

Display:
""
"============================================================"
```

**VERIFY:** Summary displayed. Counts are consistent: `$BLOCKING_STORIES_COUNT + $ADVISORY_STORIES_COUNT == $STORIES_CREATED_COUNT`. All created and failed stories are listed.

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${SESSION_ID} --workflow=qa-remediation --phase=05 --step=5.7 --project-root=. 2>&1
```
Update checkpoint: `phases["05"].steps_completed.append("5.7")`

---

## Phase Exit Verification

```
Verify all exit criteria:
1. All selected gaps processed (created or failed)              -> CHECK
   $STORIES_CREATED_COUNT + len($FAILED_STORIES) == len($GAPS_TO_CREATE)
2. $CREATED_STORIES populated                                   -> CHECK
   len($CREATED_STORIES) >= 0 (may be 0 if all failed or cancelled)
3. $FAILED_STORIES captured                                     -> CHECK
   Array exists (may be empty)
4. Counts set and consistent                                    -> CHECK
   $BLOCKING_STORIES_COUNT + $ADVISORY_STORIES_COUNT == $STORIES_CREATED_COUNT
5. Batch summary displayed                                      -> CHECK
6. Checkpoint updated with all 7 steps                          -> CHECK

IF any check fails: HALT -- "Phase 05 exit verification failed on: {failed_criteria}"

Update checkpoint:
  phases["05"].status = "completed"
  output.stories_created = $STORIES_CREATED_COUNT

Display:
"Phase 05 Complete: Batch Story Creation"
"  Stories Created: ${STORIES_CREATED_COUNT} (${BLOCKING_STORIES_COUNT} blocking, ${ADVISORY_STORIES_COUNT} advisory)"
"  Stories Failed: ${len($FAILED_STORIES)}"
"  Story ID Map: ${len($STORY_ID_MAP)} entries (for Phase 07 debt integration)"
"  Proceeding to Phase 06: Source Report Update..."
```

## Exit Gate

```bash
source .venv/bin/activate && devforgeai-validate phase-complete ${SESSION_ID} --workflow=qa-remediation --phase=05 --checkpoint-passed --project-root=. 2>&1
# Exit 0: proceed to Phase 06 | Exit 1: HALT
```

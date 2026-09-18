# Phase 06: Epic/Sprint Linking

## Entry Gate

```bash
devforgeai-validate phase-check ${SESSION_ID} --workflow=stories --from=05 --to=06 --project-root=.
```

| Exit Code | Action |
|-----------|--------|
| 0 | Prerequisites met. Proceed. |
| 1 | Phase 05 incomplete. HALT. |
| 127 | CLI not installed. Proceed without enforcement. |

---

## Contract

- **PURPOSE:** Update parent epic and sprint documents with references to the newly created story; back-link qa-recommendations.md when FROM_RECOMMENDATIONS mode is active.
- **REQUIRED SUBAGENTS:** none
- **REQUIRED ARTIFACTS:** Epic file updated (if applicable), sprint file updated (if applicable), qa-recommendations.md mutated with `implemented_in: ${STORY_ID}` (FROM_RECOMMENDATIONS mode only).
- **STEP COUNT:** 4 (Step 6.4 is conditional — runs only in FROM_RECOMMENDATIONS mode)
- **REFERENCE FILES:**
  - `references/epic-sprint-linking.md`

---

## Reference Loading [MANDATORY]

```
Read(file_path=".claude/skills/spec-driven-stories/references/epic-sprint-linking.md")
```

IF Read fails: HALT -- "Phase 06 reference file not loaded."

---

## Mandatory Steps (3)

### Step 6.1: Update Epic File

**EXECUTE:**
```
IF $EPIC_ID is not null:
  epic_file = Glob(pattern="devforgeai/specs/Epics/${EPIC_ID}*.epic.md")

  IF epic_file found:
    # Sprint 3.3 — Prefer in-context $EPIC_CONTENT; Read as fallback only.
    # Read() here is cheap only if the variable is absent; if it's present (same
    # session as phase-01), skip the redundant Read and work from $EPIC_CONTENT.
    IF $EPIC_CONTENT is not null:
        epic_pre_edit = $EPIC_CONTENT
    ELSE:
        epic_pre_edit = Read(file_path=epic_file)

    # Add story reference to epic's story list
    # Format: "- ${STORY_ID}: ${story_title} (${PRIORITY}, ${POINTS}pts)"
    Edit epic file to include story reference

    # Sprint 3.3 — MARK CACHE STALE. After this Edit, $EPIC_CONTENT and
    # phase-01.json.epic_content are both stale. Phase 07.2.5 (AC fidelity)
    # MUST re-read from disk. See POST-EPIC-EDIT RE-READ CAVEAT in schema.
    $EPIC_CACHE_STALE = true

    Display: "Epic ${EPIC_ID} updated with ${STORY_ID} reference"
  ELSE:
    Display: "WARNING: Epic file for ${EPIC_ID} not found. Skipping epic link."

ELSE:
  Display: "No epic association. Skipping epic link."
```

**VERIFY:** If `$EPIC_ID` set: Epic file contains `$STORY_ID` reference. If no epic: Step explicitly skipped.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=06 --step=6.1 --project-root=.
```
Update checkpoint: `output.epic_linked = ($EPIC_ID is not null)`
Update checkpoint: `phases["06"].steps_completed.append("6.1")`

---

### Step 6.2: Update Sprint File

**EXECUTE:**
```
IF $SPRINT_ID != "Backlog":
  sprint_file = Glob(pattern="devforgeai/specs/Sprints/*${SPRINT_ID}*.md")

  IF sprint_file found:
    Read(file_path=sprint_file)
    # Add story reference to sprint's story list
    # Format: "- ${STORY_ID}: ${story_title} (${PRIORITY}, ${POINTS}pts)"
    Edit sprint file to include story reference
    Display: "Sprint ${SPRINT_ID} updated with ${STORY_ID} reference"
  ELSE:
    Display: "WARNING: Sprint file for ${SPRINT_ID} not found. Skipping sprint link."

ELSE:
  Display: "Story in Backlog. No sprint file to update."
```

**VERIFY:** If sprint assigned: Sprint file contains `$STORY_ID` reference. If backlog: Step explicitly skipped.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=06 --step=6.2 --project-root=.
```
Update checkpoint: `output.sprint_linked = ($SPRINT_ID != "Backlog")`
Update checkpoint: `phases["06"].steps_completed.append("6.2")`

---

### Step 6.3: Verify Links

**EXECUTE:**
```
IF $EPIC_ID is not null:
  Grep(pattern=$STORY_ID, path=epic_file)
  IF not found: Display "WARNING: Epic link verification failed"

IF $SPRINT_ID != "Backlog":
  Grep(pattern=$STORY_ID, path=sprint_file)
  IF not found: Display "WARNING: Sprint link verification failed"

Display: "Linking summary:"
Display: "  Epic: ${EPIC_ID || 'N/A'} - ${epic_linked ? 'Linked' : 'Skipped'}"
Display: "  Sprint: ${SPRINT_ID} - ${sprint_linked ? 'Linked' : 'Skipped'}"
```

**VERIFY:** Link verification completed (all links confirmed or warnings displayed).

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=06 --step=6.3 --project-root=.
```
Update checkpoint: `phases["06"].steps_completed.append("6.3")`

---

### Step 6.4: Recommendations Back-Link (conditional — FROM_RECOMMENDATIONS only)

**Applies when:** conversation contains `**From Recommendations:** true` (set by the command and confirmed by Phase 01 Step R.8). Otherwise skip this step entirely — it is a no-op for SINGLE_STORY and EPIC_BATCH paths.

**Purpose:** Mutate `devforgeai/qa/recommendations/${SOURCE_STORY_ID}-qa-recommendations.md` to annotate each matched REC entry with `implemented_in: ${STORY_ID}` (the newly-created follow-up story) and append a Cycle History entry "deferred-to-${STORY_ID}". This closes the provenance loop so the next `/qa ${SOURCE_STORY_ID}` run or any external tooling can trace each REC to the story implementing it.

**EXECUTE:**

```
# Sentinel — used by RECORD below, which fires unconditionally to satisfy the
# required-steps registry (phase_state.py STORIES_PHASES["06"]).
back_linked = false

IF conversation does NOT contain "**From Recommendations:** true":
    Display: "Step 6.4: Recommendations back-link — skipped (not FROM_RECOMMENDATIONS mode)"
    Skip EXECUTE body, proceed to VERIFY + RECORD (both no-op on skip).

# Extract marker values set by Phase 01 Step R.8
SOURCE_STORY_ID           = extract "**Source Story:**" marker            # e.g. STORY-648
SOURCE_RECOMMENDATION_IDS = extract "**Source Recommendation IDs:**" marker  # CSV of REC-IDs

IF SOURCE_STORY_ID is empty OR SOURCE_RECOMMENDATION_IDS is empty:
    HALT: "Step 6.4: FROM_RECOMMENDATIONS mode active but Source Story or Source Recommendation IDs marker missing. Phase 01 Step R.8 emission bug."

result = Bash(
  command="devforgeai-validate qa-recommendations-link \
           --story-id=${SOURCE_STORY_ID} \
           --rec-ids=${SOURCE_RECOMMENDATION_IDS} \
           --implementing-story=${STORY_ID} \
           --project-root=. --format=json"
)

parsed = json.loads(result.stdout)

IF result.exit_code == 0 AND parsed.success == true:
    back_linked = true
    Display: "Step 6.4: Back-linked ${len(parsed.rec_ids_annotated)} recommendation(s) in ${parsed.recommendations_file}"
    Display: "  Source story: ${SOURCE_STORY_ID}"
    Display: "  Implementing story: ${STORY_ID}"
    Display: "  Cycle History entry: Cycle ${parsed.cycle_history_appended_as}"
ELIF result.exit_code == 1:
    # Validation error — file vanished mid-flow or rec-id drift.
    # DO NOT HALT the story creation itself (story file is already on disk
    # from Phase 05). Display a WARNING so the user can re-link manually.
    Display: "WARNING: Step 6.4 qa-recommendations-link failed (exit 1): ${parsed.error}"
    Display: "  Story ${STORY_ID} was created successfully but the source qa-recommendations.md was NOT annotated."
    Display: "  Manual fix: devforgeai-validate qa-recommendations-link --story-id=${SOURCE_STORY_ID} --rec-ids=${SOURCE_RECOMMENDATION_IDS} --implementing-story=${STORY_ID}"
ELIF result.exit_code == 2:
    Display: "WARNING: Step 6.4 qa-recommendations-link IO error: ${parsed.error}"
    Display: "  Story ${STORY_ID} was created successfully. Re-run the CLI manually to link."
```

**VERIFY:**

```
IF back_linked == true:
    Grep(pattern="implemented_in: \"${STORY_ID}\"",
         path="devforgeai/qa/recommendations/${SOURCE_STORY_ID}-qa-recommendations.md",
         output_mode="count")
    IF count == 0:
        Display: "WARNING: implemented_in marker not found in source file after link call."
# Non-FROM_RECOMMENDATIONS path has nothing to verify (back_linked stays false).
```

**RECORD (unconditional — fires even on skip so phase-complete can verify):**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=06 --step=6.4 --project-root=.
```
Update checkpoint: `phases["06"].steps_completed.append("6.4")`

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --workflow=stories --phase=06 --checkpoint-passed --project-root=.
```

## Exit Verification Checklist

- [ ] Epic update attempted (if epic assigned) or explicitly skipped
- [ ] Sprint update attempted (if sprint assigned) or explicitly skipped
- [ ] Link verification completed
- [ ] Step 6.4 executed (if FROM_RECOMMENDATIONS mode) or explicitly skipped

IF any unchecked: HALT -- "Phase 06 exit criteria not met"

## Phase Transition Display

```
Display: "Phase 06 complete. Epic/sprint linking done."
Display: "Proceeding to Phase 07: Self-Validation..."
```

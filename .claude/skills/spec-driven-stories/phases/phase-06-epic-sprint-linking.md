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

- **PURPOSE:** Update parent epic and sprint documents with references to the newly created story
- **REQUIRED SUBAGENTS:** none
- **REQUIRED ARTIFACTS:** Epic file updated (if applicable), sprint file updated (if applicable)
- **STEP COUNT:** 3
- **REFERENCE FILES:**
  - `references/epic-sprint-linking.md`

---

## Reference Loading [MANDATORY]

```
Read(file_path="src/claude/skills/spec-driven-stories/references/epic-sprint-linking.md")
```

IF Read fails: HALT -- "Phase 06 reference file not loaded."

Do NOT rely on memory of previous reads. Load reference fresh.

---

## Mandatory Steps (3)

### Step 6.1: Update Epic File

**EXECUTE:**
```
IF $EPIC_ID is not null:
  epic_file = Glob(pattern="devforgeai/specs/Epics/${EPIC_ID}*.epic.md")

  IF epic_file found:
    Read(file_path=epic_file)
    # Add story reference to epic's story list
    # Format: "- ${STORY_ID}: ${story_title} (${PRIORITY}, ${POINTS}pts)"
    Edit epic file to include story reference
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

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --workflow=stories --phase=06 --checkpoint-passed --project-root=.
```

## Exit Verification Checklist

- [ ] Epic update attempted (if epic assigned) or explicitly skipped
- [ ] Sprint update attempted (if sprint assigned) or explicitly skipped
- [ ] Link verification completed

IF any unchecked: HALT -- "Phase 06 exit criteria not met"

## Phase Transition Display

```
Display: "Phase 06 complete. Epic/sprint linking done."
Display: "Proceeding to Phase 07: Self-Validation..."
```

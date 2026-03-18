# Phase 01: Story Discovery & Context

## Entry Gate

```bash
devforgeai-validate phase-check ${SESSION_ID} --workflow=stories --from=00 --to=01 --project-root=.
```

| Exit Code | Action |
|-----------|--------|
| 0 | Prerequisites met. Proceed. |
| 1 | Phase 00 incomplete. HALT. |
| 2 | Validation error. HALT. |
| 127 | CLI not installed. Proceed without enforcement. |

---

## Contract

- **PURPOSE:** Generate story ID, discover epic/sprint context, collect story metadata (priority, points, type), handle batch mode detection
- **REQUIRED SUBAGENTS:** none
- **REQUIRED ARTIFACTS:** `$STORY_ID` generated, `$EPIC_ID` resolved, `$SPRINT_ID` resolved, `$PRIORITY` set, `$POINTS` set, `$TYPE` set
- **STEP COUNT:** 6
- **REFERENCE FILES:**
  - `references/story-discovery.md`
  - `references/user-input-integration-guide.md`
  - `references/story-type-classification.md`

---

## Reference Loading [MANDATORY]

```
Read(file_path="src/claude/skills/spec-driven-stories/references/story-discovery.md")
Read(file_path="src/claude/skills/spec-driven-stories/references/user-input-integration-guide.md")
Read(file_path="src/claude/skills/spec-driven-stories/references/story-type-classification.md")
```

IF any Read fails: HALT -- "Phase 01 reference files not loaded. Cannot proceed without reference material."

Do NOT rely on memory of previous reads. Load ALL references fresh.

---

## Mandatory Steps (6)

### Step 1.1: Load User Input Guidance Patterns

**EXECUTE:**
```
TRY:
  Read(file_path="src/claude/skills/spec-driven-ideation/references/user-input-guidance.md")
  GUIDANCE_AVAILABLE = true
CATCH:
  GUIDANCE_AVAILABLE = false
  Log: "user-input-guidance.md not found, proceeding with baseline logic"
```

**VERIFY:** Variable `GUIDANCE_AVAILABLE` is set (true or false).

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=01 --step=1.1 --project-root=.
```
Update checkpoint: `phases["01"].steps_completed.append("1.1")`

---

### Step 1.2: Feature Capture & Story ID Generation

**EXECUTE:**
```
IF $BATCH_MODE == true:
  # Batch mode: Extract from context markers
  $STORY_ID = from "**Story ID:**" marker
  $FEATURE_DESCRIPTION = from "**Feature Description:**" marker
  Validate $STORY_ID matches STORY-\d+ pattern
ELSE:
  # Interactive mode: Capture feature description
  IF $FEATURE_DESCRIPTION is empty:
    AskUserQuestion:
      Question: "Describe the feature you want to create a story for (minimum 10 words):"
      Header: "Feature"
      Options: (none - free text)

  # Generate next story ID (gap-aware sequencing)
  existing_stories = Glob(pattern="devforgeai/specs/Stories/STORY-*.story.md")
  Extract all STORY-NNN numbers
  Find first gap in sequence, or increment highest
  $STORY_ID = "STORY-{next_number}"

Display: "Story ID: ${STORY_ID}"
Display: "Feature: ${FEATURE_DESCRIPTION}"
```

**VERIFY:** `$STORY_ID` matches pattern `STORY-\d+` AND `$FEATURE_DESCRIPTION` is non-empty.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=01 --step=1.2 --project-root=.
```
Update checkpoint: `output.story_id = $STORY_ID`
Update checkpoint: `phases["01"].steps_completed.append("1.2")`

---

### Step 1.3: Discover Epic Context

**EXECUTE:**
```
IF $BATCH_MODE == true:
  $EPIC_ID = from "**Epic ID:**" marker
ELSE:
  epic_files = Glob(pattern="devforgeai/specs/Epics/*.epic.md")

  IF epic_files is empty:
    $EPIC_ID = null
    Display: "No epics found - standalone story"
  ELSE:
    Build epic_options list from epic files
    AskUserQuestion:
      Question: "Which epic does this story belong to?"
      Header: "Epic"
      Options: [epic options + "None - standalone story"]
    $EPIC_ID = user selection (or null if standalone)
```

**VERIFY:** `$EPIC_ID` is set (may be null for standalone).

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=01 --step=1.3 --project-root=.
```
Update checkpoint: `input.epic_id = $EPIC_ID`
Update checkpoint: `phases["01"].steps_completed.append("1.3")`

---

### Step 1.4: Discover Sprint Context

**EXECUTE:**
```
IF $BATCH_MODE == true:
  $SPRINT_ID = from "**Sprint:**" marker
ELSE:
  sprint_files = Glob(pattern="devforgeai/specs/Sprints/*.md")

  IF sprint_files is empty:
    $SPRINT_ID = "Backlog"
  ELSE:
    Build sprint_options list from sprint files
    AskUserQuestion:
      Question: "Which sprint should this story be assigned to?"
      Header: "Sprint"
      Options: ["Backlog" + sprint options]
    $SPRINT_ID = user selection
```

**VERIFY:** `$SPRINT_ID` is set (non-empty string).

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=01 --step=1.4 --project-root=.
```
Update checkpoint: `phases["01"].steps_completed.append("1.4")`

---

### Step 1.5: Collect Story Metadata

**EXECUTE:**
```
IF $BATCH_MODE == true:
  $PRIORITY = from "**Priority:**" marker
  $POINTS = from "**Points:**" marker
  $TYPE = from "**Type:**" marker
ELSE:
  # Priority
  AskUserQuestion:
    Question: "What is the story priority?"
    Header: "Priority"
    Options:
      - {label: "Critical", description: "Blocking other work, must be done immediately"}
      - {label: "High", description: "Important for upcoming release"}
      - {label: "Medium", description: "Normal priority"}
      - {label: "Low", description: "Nice to have"}

  # Story Type (reference: story-type-classification.md)
  AskUserQuestion:
    Question: "What type of story is this?"
    Header: "Type"
    Options:
      - {label: "feature", description: "Full TDD workflow (default)"}
      - {label: "documentation", description: "Skip integration testing"}
      - {label: "bugfix", description: "Skip refactoring phase"}
      - {label: "refactor", description: "Skip test generation"}

  # Story Points (Fibonacci)
  AskUserQuestion:
    Question: "Estimate story complexity:"
    Header: "Points"
    Options:
      - {label: "1", description: "Trivial - Few hours"}
      - {label: "2", description: "Simple - Half day"}
      - {label: "3", description: "Standard - 1 day"}
      - {label: "5", description: "Complex - 2-3 days"}
```

**VERIFY:** `$PRIORITY`, `$POINTS`, and `$TYPE` are all non-empty.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=01 --step=1.5 --project-root=.
```
Update checkpoint: `phases["01"].steps_completed.append("1.5")`

---

### Step 1.6: Collect Dependencies (Optional)

**EXECUTE:**
```
IF $BATCH_MODE == true:
  $DEPENDS_ON = from "**Depends On:**" marker or null
ELSE:
  AskUserQuestion:
    Question: "Does this story depend on other stories?"
    Header: "Dependencies"
    Options:
      - {label: "No dependencies", description: "Story can be worked independently"}
      - {label: "Has dependencies", description: "Specify blocking stories"}

  IF "Has dependencies":
    AskUserQuestion to collect STORY-NNN IDs
```

**VERIFY:** Dependencies resolved (may be empty list).

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=01 --step=1.6 --project-root=.
```
Update checkpoint: `phases["01"].steps_completed.append("1.6")`

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --workflow=stories --phase=01 --checkpoint-passed --project-root=.
```

## Exit Verification Checklist

- [ ] `$STORY_ID` is set and matches STORY-\d+ pattern
- [ ] `$FEATURE_DESCRIPTION` is non-empty (10+ words)
- [ ] `$EPIC_ID` is resolved (set or explicitly null)
- [ ] `$SPRINT_ID` is set
- [ ] `$PRIORITY` is one of: Critical, High, Medium, Low
- [ ] `$POINTS` is set (Fibonacci number)
- [ ] `$TYPE` is one of: feature, documentation, bugfix, refactor

IF any unchecked: HALT -- "Phase 01 exit criteria not met"

## Phase Transition Display

```
Display: "Phase 01 complete. Story ${STORY_ID} metadata collected."
Display: "Proceeding to Phase 02: Requirements Analysis..."
```

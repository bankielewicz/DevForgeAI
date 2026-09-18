# Phase 01: Story Discovery & Context

## Entry Gate

Phase 00 Initialization (inline in `SKILL.md`) IS this phase's entry gate. The skill's Phase Orchestration Loop explicitly skips the `phase-check` call for phase 01 — `phase-init` already validated the session and created the checkpoint.

**Do NOT invoke any** `devforgeai-validate phase-check` command at the entry of this phase. Phase 00 is the skill's inline bootstrap, not a recorded CLI phase; a check that transitions *from* an inline-only phase has undefined semantics.

See `SKILL.md` → *Phase Orchestration Loop* (the branch that skips the entry check when `phase_id == "01"`) for the authoritative gate contract.

**Reconciliation (2026-04-13):** Prior versions of this file contained an executable `phase-check` snippet in a bash code block that contradicted `SKILL.md`. The snippet has been removed; `SKILL.md` is authoritative for phase 01 entry.

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
# Load mode-specific discovery reference (split for token efficiency):
IF $MODE == "EPIC_BATCH":
  Read(file_path=".claude/skills/spec-driven-stories/references/story-discovery-batch.md")
ELIF $MODE == "FROM_RECOMMENDATIONS":
  Read(file_path=".claude/skills/spec-driven-stories/references/story-discovery-from-recommendations.md")
ELSE:
  Read(file_path=".claude/skills/spec-driven-stories/references/story-discovery-interactive.md")

Read(file_path=".claude/skills/spec-driven-stories/references/user-input-integration-guide.md")
Read(file_path=".claude/skills/spec-driven-stories/references/story-type-classification.md")
```

IF any Read fails: HALT -- "Phase 01 reference files not loaded."

### FROM_RECOMMENDATIONS Branch (dispatch)

When `$MODE == "FROM_RECOMMENDATIONS"`:

- Execute the full Step R.1 → R.8 workflow from `story-discovery-from-recommendations.md` (status check, severity filter, selection, fetch, fidelity validation, source-story resolution, mapping, feature_description rendering, marker emission) **BEFORE** the Mandatory Steps below.
- After Step R.8 has emitted `**Batch Mode:** true`, the regular Mandatory Steps (1.1–1.6) run as for any batch-mode invocation: they consume the markers set by R.8 (Story ID, Epic ID, Feature Description, Priority, Points, Type, Sprint) rather than re-prompting interactively.
- The additional markers unique to FROM_RECOMMENDATIONS (`From Recommendations`, `Source Recommendations File`, `Source Recommendation IDs`, `Source Story`, `Cycle Recorded`, `Is Advisory`, `Story Filename Prefix`) flow through unchanged and are consumed by Phase 02 (requirements-analyst conditional), Phase 05 (frontmatter emission), and Phase 06 (back-link step).

---

## Mandatory Steps (6)

### Step 1.1: Load User Input Guidance Patterns

**EXECUTE:**
```
TRY:
  Read(file_path=".claude/skills/spec-driven-ideation/references/user-input-guidance.md")
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
# --- Sub-step 1.2.0: DEVARCH story-seed ingestion (schema-validated) ---
# When /create-story is invoked with a Development Architecture Document seed
# reference — a SEED-NNN id or a *.development-architecture.html path — in place
# of a free-form feature description, consume the reviewed story seed instead of
# capturing free-form input. ONE seed per invocation (re-invoke for each seed).
$IS_DEVARCH_SEED = ($FEATURE_DESCRIPTION matches "^SEED-[0-9]{3,}$"
                    OR $FEATURE_DESCRIPTION ends with ".development-architecture.html")
$FEATURE_REF = ""       # set below on the DEVARCH-seed path; emitted to frontmatter by Phase 05
$SOURCE_DEVARCH = ""    # set below on the DEVARCH-seed path; emitted to frontmatter by Phase 05

IF $IS_DEVARCH_SEED:
  # 1. Resolve the DEVARCH document file
  IF $FEATURE_DESCRIPTION ends with ".development-architecture.html":
    $DEVARCH_FILE = $FEATURE_DESCRIPTION
  ELSE:
    # A bare SEED-NNN id — locate the DEVARCH document whose story_seeds[] contains it
    devarch_files = Glob(pattern="devforgeai/specs/architecture/DEVARCH-*-*.development-architecture.html")
    $DEVARCH_FILE = the file whose JSON island story_seeds[] contains an entry id == $FEATURE_DESCRIPTION
  IF $DEVARCH_FILE not resolved:
    HALT -- "No Development Architecture Document found for seed reference '${FEATURE_DESCRIPTION}'."

  # 2. Read the file; extract the JSON data island
  devarch_content = Read(file_path=$DEVARCH_FILE)
  devarch_data = parse JSON from <script type="application/json" id="development-architecture-data">...</script>

  # 3. VALIDATE the DEVARCH document via the deterministic CLI gate (ADR-082, H5;
  #    ADR-086 ratified the schema_version equality semantic).
  #    The CLI performs the same 5-step structural check the prose used to enumerate
  #    inline — but as a binary gate the orchestrator cannot abbreviate or skip:
  #      a. schema_version == "1.0"
  #      b. id matches ^DEVARCH-[0-9]{3,}$
  #      c. feature_ref matches ^F-[0-9]{2,}$
  #      d. story_seeds[] present and non-empty
  #      e. handoff.recommended_build_order[] present
  #    On any failure it emits a per-check JSON diagnostic identifying which check
  #    failed and why. This is the deterministic-gate form of the same
  #    Schema-Validation-Before-Consumption pattern the 3 architecture skills apply
  #    prose-only in their Phase 01.
  Bash:
    devforgeai-validate validate-devarch-seed "$DEVARCH_FILE" --project-root=. --format=json
  IF exit code != 0:
    Display the CLI's JSON `checks[]` array (each failing row carries `name` and
    `diagnostic`) so the user sees which of the 5 checks failed.
    HALT -- "DEVARCH document malformed; cannot seed story (see CLI diagnostic above)."

  # 4. Select ONE seed (one seed per invocation — re-invoke for the rest)
  IF $FEATURE_DESCRIPTION is a SEED-NNN id:
    $SEED = story_seeds[] entry whose id == $FEATURE_DESCRIPTION
  ELSE:
    $SEED = the seed for the first id in handoff.recommended_build_order with no story yet
  IF $SEED not resolved: HALT -- "Seed id not found in the DEVARCH document's story_seeds[]."
  $REMAINING_SEEDS = handoff.recommended_build_order ids not yet converted to stories
  Display: "Seeding from ${SEED.id}. Remaining seeds: ${REMAINING_SEEDS} — re-invoke /create-story for each."

  # 5. Pre-populate story fields from the chosen seed
  $FEATURE_DESCRIPTION = $SEED.summary           # replaces the seed-ref argument with the real description
  $STORY_TITLE_SEED    = $SEED.title
  $AC_HINTS            = $SEED.acceptance_hint[]  # hints only — Phase 02 still owns the final ACs
  $FEATURE_REF         = $SEED.feature_ref        # F-NN
  $SOURCE_DEVARCH      = relative path of $DEVARCH_FILE
  $SEED_COMPONENTS     = $SEED.components[]
  $SEED_COMPLEXITY     = $SEED.estimated_complexity
  # $SEED_COMPONENTS / $SEED_COMPLEXITY are carried into the story's Technical
  # Specification section during later-phase assembly.

  # 5.5. Derive recommended metadata from the seed (advisory — user confirms in Steps 1.5/1.6)
  $DERIVED_POINTS   = Low→3, Medium→5, High→8  (from $SEED_COMPLEXITY)
  $DERIVED_PRIORITY = Low→Low, Medium→Medium, High→High  (from $SEED_COMPLEXITY)
  $DERIVED_TYPE     = "feature"  # default; override if summary matches doc-keyword heuristic
  IF $SEED.summary contains any of ["doc", "guide", "README", "reference"]:
    $DERIVED_TYPE = "documentation"
  $DEVARCH_PREDECESSOR_SEEDS = [
    seeds in handoff.recommended_build_order that appear BEFORE the index
    of $SEED.id; empty list if $SEED.id is the first entry in the order
  ]
  # $DERIVED_POINTS / $DERIVED_PRIORITY / $DERIVED_TYPE / $DEVARCH_PREDECESSOR_SEEDS
  # are consumed by Steps 1.5 and 1.6 (DEVARCH_SEED branch) instead of cold prompts.

  # 6. Resolve the story ID (same source as the other branches)
  $STORY_ID = from "**Next Story ID:**" context marker or CLI result.next_story_id

ELIF $BATCH_MODE == true:
  # Batch mode: Extract from context markers
  $STORY_ID = from "**Story ID:**" marker
  $FEATURE_DESCRIPTION = from "**Feature Description:**" marker
  Validate $STORY_ID matches STORY-\d+ pattern
ELSE:
  # Interactive mode: Capture feature description (no DEVARCH seed supplied —
  # legacy / ad-hoc story; $FEATURE_REF and $SOURCE_DEVARCH stay empty)
  IF $FEATURE_DESCRIPTION is empty:
    AskUserQuestion:
      Question: "Describe the feature you want to create a story for (minimum 10 words):"
      Header: "Feature"
      Options: (none - free text)

  # Story ID from CLI (no Glob — story-preflight scans instantly including archive)
  # Use "**Next Story ID:**" context marker from /create-story command
  # Or call: devforgeai-validate story-preflight ${EPIC_ID} --project-root=. --format=json
  $STORY_ID = from context marker or CLI result.next_story_id

Display: "Story ID: ${STORY_ID}"
Display: "Feature: ${FEATURE_DESCRIPTION}"
```

**VERIFY:** `$STORY_ID` matches pattern `STORY-\d+` AND `$FEATURE_DESCRIPTION` is non-empty. When Sub-step 1.2.0 ran (DEVARCH-seed path), `$FEATURE_REF` matches `^F-[0-9]{2,}$` and `$SOURCE_DEVARCH` is a non-empty path; on the batch/interactive paths both stay empty.

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

# Sprint 3.3 — Capture epic content once for downstream reuse.
# Contract: src/claude/skills/spec-driven-stories/contracts/phase-output-schema.json (phase01Output).
# Downstream: phase-05.3 (provenance embedding), phase-06.1 (linking), may reference
# $EPIC_CONTENT via context variable OR phase-01.json fallback.
# IMPORTANT: phase-07.2.5 (AC fidelity) MUST re-read from disk because phase-06.1
# EDITS the epic file. See phase-07 POST-EPIC-EDIT RE-READ CAVEAT.
$EPIC_CONTENT = null
$EPIC_FILE_PATH = null
IF $EPIC_ID is not null:
    $EPIC_FILE_PATH = Glob(pattern="devforgeai/specs/Epics/${EPIC_ID}*.epic.md") | first
    IF $EPIC_FILE_PATH is not null:
        TRY:
            $EPIC_CONTENT = Read(file_path=$EPIC_FILE_PATH)
            Display: "Epic content cached in-context (Sprint 3.3): ${EPIC_FILE_PATH}"
        CATCH:
            $EPIC_CONTENT = null
            Display: "WARNING: Epic file path resolved but read failed — downstream phases will re-read"
```

**VERIFY:** `$EPIC_ID` is set (may be null for standalone). If non-null, `$EPIC_FILE_PATH` resolved via Glob (may still be null if no matching file exists). `$EPIC_CONTENT` is set when Read succeeded.

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
ELSE IF $IS_DEVARCH_SEED:
  # Present derived values as a single confirm-or-override prompt
  # (replaces three separate cold AskUserQuestion calls)
  AskUserQuestion:
    Question: "Metadata derived from ${SEED.id} (complexity: ${SEED_COMPLEXITY}). Accept or override?"
    Header: "Metadata"
    Options:
      - {label: "Accept all: ${DERIVED_PRIORITY} / ${DERIVED_TYPE} / ${DERIVED_POINTS}pts (Recommended)",
         description: "Use derived: Priority=${DERIVED_PRIORITY}, Type=${DERIVED_TYPE}, Points=${DERIVED_POINTS}"}
      - {label: "Override priority",
         description: "Show priority picker only; keep Type=${DERIVED_TYPE}, Points=${DERIVED_POINTS}pts"}
      - {label: "Override type",
         description: "Show type picker only; keep Priority=${DERIVED_PRIORITY}, Points=${DERIVED_POINTS}pts"}
      - {label: "Override points",
         description: "Show points picker only; keep Priority=${DERIVED_PRIORITY}, Type=${DERIVED_TYPE}"}
  IF user chose "Accept all":
    $PRIORITY = $DERIVED_PRIORITY
    $TYPE     = $DERIVED_TYPE
    $POINTS   = $DERIVED_POINTS
  IF user chose "Override priority":
    → run cold priority AskUserQuestion only; keep $TYPE=$DERIVED_TYPE, $POINTS=$DERIVED_POINTS
  IF user chose "Override type":
    → run cold type AskUserQuestion only; keep $PRIORITY=$DERIVED_PRIORITY, $POINTS=$DERIVED_POINTS
  IF user chose "Override points":
    → run cold points AskUserQuestion only; keep $PRIORITY=$DERIVED_PRIORITY, $TYPE=$DERIVED_TYPE
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
ELSE IF $IS_DEVARCH_SEED:
  IF $DEVARCH_PREDECESSOR_SEEDS is empty:
    $DEPENDS_ON = null
    Display: "No dependencies derived: ${SEED.id} is first in recommended_build_order."
  ELSE:
    AskUserQuestion:
      Question: "Predecessor seeds in recommended_build_order: ${DEVARCH_PREDECESSOR_SEEDS}. Use as dependencies?"
      Header: "Dependencies"
      Options:
        - {label: "Yes — depend on all predecessors (Recommended)",
           description: "Add ${DEVARCH_PREDECESSOR_SEEDS} as blocking dependencies (map to STORY-NNN IDs after creation)"}
        - {label: "No dependencies",
           description: "Story can be worked independently despite build order"}
        - {label: "Specify manually",
           description: "Enter STORY-NNN IDs manually"}
    IF user chose "Yes — depend on all predecessors":
      $DEPENDS_ON = $DEVARCH_PREDECESSOR_SEEDS  # stored as SEED-NNN; resolved to STORY-NNN after creation
    IF user chose "No dependencies":
      $DEPENDS_ON = null
    IF user chose "Specify manually":
      → run cold STORY-NNN collection AskUserQuestion
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
# Sprint 3.3 — Persist phase-01 output cache for session-resume resilience.
# Contract: src/claude/skills/spec-driven-stories/contracts/phase-output-schema.json (phase01Output).
# Downstream phases prefer in-context $EPIC_CONTENT; this file is the fallback when
# a phase runs in a resumed session where the variable is lost.
mkdir -p tmp/${SESSION_ID}/phase-outputs
```

Write the cache file:
```
Write(file_path="tmp/${SESSION_ID}/phase-outputs/phase-01.json",
      content=json_serialize({
        "schema_version": "1.0",
        "phase_id": "01",
        "story_id": $STORY_ID,
        "epic_id": $EPIC_ID,
        "sprint_id": $SPRINT_ID,
        "priority": $PRIORITY,
        "points": $POINTS,
        "type": $TYPE,
        "epic_file_path": $EPIC_FILE_PATH,
        "epic_content": $EPIC_CONTENT
      }))
```

Then complete the phase:
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

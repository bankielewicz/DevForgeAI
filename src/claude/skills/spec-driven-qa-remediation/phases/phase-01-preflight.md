# Phase 01: Pre-Flight Validation

## Entry Gate

```bash
source .venv/bin/activate && devforgeai-validate phase-init ${SESSION_ID} --workflow=qa-remediation --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | New workflow. State file created. Set CURRENT_PHASE = "01". |
| 1 | Existing workflow. Resume from checkpoint. |
| 2 | Invalid session ID. HALT. |
| 127 | CLI not installed. Proceed without enforcement. |

---

## Contract

| Field | Value |
|-------|-------|
| **PURPOSE** | Validate environment, load config, parse arguments, create checkpoint |
| **REFERENCE** | None (inline bootstrap) |
| **STEP COUNT** | 6 mandatory steps |

---

## Phase Exit Criteria

- [ ] `$CONFIG` loaded and non-empty
- [ ] `$SOURCE`, `$MIN_SEVERITY`, `$GAP_PATHS` all set
- [ ] Checkpoint file exists on disk
- [ ] At least 1 gap file found in source paths

IF any unchecked: HALT -- "Phase 01 exit criteria not met"

---

## Reference Loading [MANDATORY]

Phase 01 is the bootstrap phase -- no external reference files to load.

All logic is inline within this phase file.

---

## Mandatory Steps (6)

### Step 1.1: Validate Project Root

**EXECUTE:**
```
Read(file_path="CLAUDE.md")

IF Read succeeds AND content contains "DevForgeAI" or "devforgeai":
    CWD_VALID = true
    Display: "Project root validated"
ELSE:
    Glob(pattern=".claude/skills/*.md")
    IF results found:
        CWD_VALID = true
    ELSE:
        CWD_VALID = false
        HALT: AskUserQuestion("Cannot confirm project root. Provide correct project root path?")
```

**VERIFY:** `CWD_VALID == true`. If false, workflow HALTED via AskUserQuestion.

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${SESSION_ID} --workflow=qa-remediation --phase=01 --step=1.1 --project-root=. 2>&1
```
Update checkpoint: `phases["01"].steps_completed.append("1.1")`

---

### Step 1.2: Load Configuration

**EXECUTE:**
```
Read(file_path="devforgeai/config/qa-remediation.yaml")

IF Read succeeds:
    $CONFIG = parsed YAML content
    Extract:
      $CONFIG.sources.local = sources.local pattern (default: "devforgeai/qa/reports/*-gaps.json")
      $CONFIG.sources.imports = sources.imports pattern (default: "devforgeai/qa/imports/**/*-gaps.json")
      $CONFIG.severity_weights = { CRITICAL: 100, HIGH: 75, MEDIUM: 50, LOW: 25 }
      $CONFIG.defaults.min_severity = defaults.min_severity (default: "MEDIUM")
      $CONFIG.defaults.sprint = defaults.sprint (default: "Backlog")
      $CONFIG.technical_debt.register_path = technical_debt.register_path
      $CONFIG.technical_debt.auto_add_skipped = technical_debt.auto_add_skipped
      $CONFIG.technical_debt.invoke_analyzer = technical_debt.invoke_analyzer
      $CONFIG.batch_mode.continue_on_failure = batch_mode.continue_on_failure
      $CONFIG.batch_mode.max_stories_per_run = batch_mode.max_stories_per_run
    Display: "Configuration loaded: min_severity=${CONFIG.defaults.min_severity}, max_stories=${CONFIG.batch_mode.max_stories_per_run}"

ELSE:
    HALT: "Configuration file not found at devforgeai/config/qa-remediation.yaml. Create config before running QA remediation."
```

**VERIFY:** `$CONFIG` is non-null and contains `sources`, `severity_weights`, and `defaults` sections.

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${SESSION_ID} --workflow=qa-remediation --phase=01 --step=1.2 --project-root=. 2>&1
```
Update checkpoint: `phases["01"].steps_completed.append("1.2")`

---

### Step 1.3: Parse Arguments

**EXECUTE:**
```
Extract 7 arguments from $ARGUMENTS (conversation context):

$SOURCE = extract "--source" value OR default "local"
    Valid values: "local", "imports", "all"
    IF invalid value: HALT with AskUserQuestion("Invalid --source value. Choose: local, imports, all")

$MIN_SEVERITY = extract "--min-severity" value OR default from $CONFIG.defaults.min_severity
    Valid values: "CRITICAL", "HIGH", "MEDIUM", "LOW"
    IF invalid value: HALT with AskUserQuestion("Invalid --min-severity value. Choose: CRITICAL, HIGH, MEDIUM, LOW")

$EPIC_ID = extract "--epic" value OR null
    IF provided: validate matches EPIC-\d+ pattern

$DRY_RUN = extract "--dry-run" flag OR false
    Boolean: true if flag present, false otherwise

$ADD_TO_DEBT = extract "--add-to-debt" flag OR false
    Boolean: true if flag present, false otherwise

$CREATE_STORIES = extract "--create-stories" flag OR false
    Boolean: true if flag present, false otherwise

$BLOCKING_ONLY = extract "--blocking-only" flag OR false
    Boolean: true if flag present, false otherwise

Display:
  "Arguments parsed:"
  "  Source: ${SOURCE}"
  "  Min Severity: ${MIN_SEVERITY}"
  "  Epic: ${EPIC_ID}"
  "  Dry Run: ${DRY_RUN}"
  "  Add to Debt: ${ADD_TO_DEBT}"
  "  Create Stories: ${CREATE_STORIES}"
  "  Blocking Only: ${BLOCKING_ONLY}"
```

**VERIFY:** All 7 variables are set (may be default values). `$SOURCE` is one of `local|imports|all`. `$MIN_SEVERITY` is one of `CRITICAL|HIGH|MEDIUM|LOW`.

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${SESSION_ID} --workflow=qa-remediation --phase=01 --step=1.3 --project-root=. 2>&1
```
Update checkpoint: `phases["01"].steps_completed.append("1.3")`

---

### Step 1.4: Validate Flag Dependencies

**EXECUTE:**
```
IF $ADD_TO_DEBT == true:
    # Check STORY-287 (QA Hook Integration) completion
    marker_path = "src/.claude/skills/spec-driven-qa-remediation/markers/STORY-287-complete.md"
    Glob(pattern=marker_path)

    IF marker not found:
        Display:
        "Flag --add-to-debt requires STORY-287 (QA Hook Integration) - not yet implemented"
        "Options:"
        "  1. Run /dev STORY-287 first"
        "  2. Remove --add-to-debt flag and use manual debt addition"

        HALT with exit code 1

IF $CREATE_STORIES == true:
    # Check STORY-288 (Remediation Story Automation) completion
    marker_path = "src/.claude/skills/spec-driven-qa-remediation/markers/STORY-288-complete.md"
    Glob(pattern=marker_path)

    IF marker not found:
        Display:
        "Flag --create-stories requires STORY-288 (Remediation Story Automation) - not yet implemented"
        "Options:"
        "  1. Run /dev STORY-288 first"
        "  2. Remove --create-stories flag and use manual story creation"

        HALT with exit code 1

IF $ADD_TO_DEBT == false AND $CREATE_STORIES == false:
    Display: "No flag dependencies to validate"
ELSE:
    Display: "Flag dependency validation passed"
```

**VERIFY:** If `$ADD_TO_DEBT == true`, STORY-287 marker exists. If `$CREATE_STORIES == true`, STORY-288 marker exists. If neither flag is set, this step passes unconditionally.

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${SESSION_ID} --workflow=qa-remediation --phase=01 --step=1.4 --project-root=. 2>&1
```
Update checkpoint: `phases["01"].steps_completed.append("1.4")`

---

### Step 1.5: Validate Source Paths

**EXECUTE:**
```
# Build glob patterns based on $SOURCE
IF $SOURCE == "local":
    $GAP_PATHS = [$CONFIG.sources.local]
ELIF $SOURCE == "imports":
    $GAP_PATHS = [$CONFIG.sources.imports]
ELIF $SOURCE == "all":
    $GAP_PATHS = [$CONFIG.sources.local, $CONFIG.sources.imports]

# Execute glob for each pattern to verify files exist
$DISCOVERED_FILES = []
FOR each pattern in $GAP_PATHS:
    results = Glob(pattern=pattern)
    $DISCOVERED_FILES.extend(results)

IF len($DISCOVERED_FILES) == 0:
    Display:
    "No gap files found matching source patterns:"
    FOR pattern in $GAP_PATHS:
        "  - {pattern}"
    ""
    "Ensure QA reports have been generated (run /qa first) or import external gap files."

    HALT: "No gap files found in source paths"

Display: "Found ${len($DISCOVERED_FILES)} gap file(s) across ${len($GAP_PATHS)} source pattern(s)"
FOR file in $DISCOVERED_FILES:
    Display: "  - {file}"
```

**VERIFY:** `$DISCOVERED_FILES` contains at least 1 file path. `$GAP_PATHS` is non-empty.

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${SESSION_ID} --workflow=qa-remediation --phase=01 --step=1.5 --project-root=. 2>&1
```
Update checkpoint: `phases["01"].steps_completed.append("1.5")`

---

### Step 1.6: Create Initial Checkpoint

**EXECUTE:**
```
$CHECKPOINT_PATH = "devforgeai/workflows/checkpoints/qa-remediation-${SESSION_ID}.checkpoint.json"

Write(file_path=$CHECKPOINT_PATH, content=
{
  "checkpoint_version": "1.0",
  "session_id": "${SESSION_ID}",
  "workflow": "qa-remediation",
  "created_at": "{ISO 8601 timestamp}",
  "updated_at": "{ISO 8601 timestamp}",
  "status": "in_progress",

  "input": {
    "source": "${SOURCE}",
    "min_severity": "${MIN_SEVERITY}",
    "epic_id": "${EPIC_ID}",
    "dry_run": ${DRY_RUN},
    "add_to_debt": ${ADD_TO_DEBT},
    "create_stories": ${CREATE_STORIES},
    "blocking_only": ${BLOCKING_ONLY}
  },

  "progress": {
    "current_phase": 1,
    "phases_completed": [],
    "phases_skipped": [],
    "total_steps_completed": 6
  },

  "phases": {
    "01": { "status": "completed", "steps_completed": ["1.1","1.2","1.3","1.4","1.5","1.6"] },
    "02": { "status": "pending", "steps_completed": [] },
    "03": { "status": "pending", "steps_completed": [] },
    "04": { "status": "pending", "steps_completed": [] },
    "05": { "status": "pending", "steps_completed": [] },
    "06": { "status": "pending", "steps_completed": [] },
    "07": { "status": "pending", "steps_completed": [] }
  },

  "output": {
    "gap_files_processed": 0,
    "total_gaps": 0,
    "stories_created": 0,
    "debt_entries_added": 0,
    "enhancement_report_path": null,
    "error": null
  }
}
)
```

**VERIFY:** Checkpoint file exists on disk.
```
Glob(pattern="devforgeai/workflows/checkpoints/qa-remediation-${SESSION_ID}.checkpoint.json")
IF not found: HALT -- "Checkpoint creation failed"
```

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${SESSION_ID} --workflow=qa-remediation --phase=01 --step=1.6 --project-root=. 2>&1
```
Update checkpoint: `phases["01"].steps_completed.append("1.6")`

---

## Phase Exit Verification

```
Verify all exit criteria:
1. $CONFIG is loaded and non-empty                    → CHECK
2. $SOURCE, $MIN_SEVERITY, $GAP_PATHS all set         → CHECK
3. Checkpoint file exists on disk                      → CHECK
4. At least 1 gap file found ($DISCOVERED_FILES >= 1)  → CHECK

IF any check fails: HALT -- "Phase 01 exit verification failed on: {failed_criteria}"

Display:
"Phase 01 Complete: Pre-Flight Validation"
"  Config: Loaded (min_severity=${CONFIG.defaults.min_severity})"
"  Source: ${SOURCE} (${len($GAP_PATHS)} pattern(s))"
"  Gap Files Found: ${len($DISCOVERED_FILES)}"
"  Dry Run: ${DRY_RUN}"
"  Checkpoint: ${CHECKPOINT_PATH}"
"  Proceeding to Phase 02: Discovery & Parsing..."
```

## Exit Gate

```bash
source .venv/bin/activate && devforgeai-validate phase-complete ${SESSION_ID} --workflow=qa-remediation --phase=01 --checkpoint-passed --project-root=. 2>&1
# Exit 0: proceed to Phase 02 | Exit 1: HALT
```

# Phase 01: Pre-Flight Validation

## Entry Gate

```bash
devforgeai-validate phase-init ${STORY_ID} --project-root=.
# Exit 0: new workflow | Exit 1: resume | Exit 2: invalid | Exit 127: CLI not installed
```

## Contract

PURPOSE: Validate environment, load context files, detect operating mode, and extract parameters before lifecycle orchestration begins.
REQUIRED SUBAGENTS: (none)
REQUIRED ARTIFACTS: Context files loaded in conversation context
STEP COUNT: 5 mandatory steps

---

## Mandatory Steps

### Step 1: Validate Project Root

EXECUTE: Verify current working directory is the project root.
```
Read(file_path="CLAUDE.md")
```
VERIFY: File exists and contains "DevForgeAI".
```
IF Read fails OR content does not contain "DevForgeAI": HALT -- "Not in project root. Navigate to project root."
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=01 --step=1`

### Step 2: Load 6 Context Files (Parallel)

EXECUTE: Load all 6 constitutional context files in a single message with 6 Read calls for parallel execution.
```
Read(file_path="devforgeai/specs/context/architecture-constraints.md")
Read(file_path="devforgeai/specs/context/tech-stack.md")
Read(file_path="devforgeai/specs/context/source-tree.md")
Read(file_path="devforgeai/specs/context/dependencies.md")
Read(file_path="devforgeai/specs/context/coding-standards.md")
Read(file_path="devforgeai/specs/context/anti-patterns.md")
```
All 6 Read calls MUST be in a single assistant message for implicit parallel execution.

VERIFY: All 6 files loaded successfully and are non-empty.
```
IF any file missing or empty: HALT -- "Missing context file: {filename}. Run /create-context first."
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=01 --step=2`

### Step 3: Detect Operating Mode

EXECUTE: Search conversation context for mode markers using priority order: Sprint > Audit > Story > Default.
```
# Priority 1: Sprint Planning
Grep for "**Operation:** plan-sprint" OR "**Command:** create-sprint" in conversation

# Priority 2: Audit Deferrals
Grep for "**Command:** audit-deferrals" in conversation

# Priority 3: Story Management
Grep for "**Story ID:** STORY-" in conversation

# Priority 4: Default
IF none found: Read references/mode-detection.md for inference logic
```

VERIFY: MODE variable is set to one of: "sprint-planning", "audit-deferrals", "story-management", "default".
```
IF MODE == "default" AND inference fails:
  AskUserQuestion:
    Question: "Cannot determine operating mode. What would you like to do?"
    Header: "Mode"
    Options:
      - label: "Orchestrate a story"
        description: "Manage story lifecycle (dev -> QA -> release)"
      - label: "Plan a sprint"
        description: "Create a sprint with story selection"
      - label: "Audit deferrals"
        description: "Audit deferred work in completed stories"
    multiSelect: false
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=01 --step=3`

### Step 4: Extract Parameters

EXECUTE: Based on detected mode, extract required parameters from conversation context.

**Story Management mode:**
```
$STORY_ID = Extract from "**Story ID:** STORY-NNN" marker
$AUTO_RESUME = Extract from "**Auto-Resume:** Enabled" marker (default: false)
```

**Sprint Planning mode:**
```
$SPRINT_NAME = Extract from "**Sprint Name:** {name}" marker
$SELECTED_STORIES = Extract from "**Selected Stories:** {ids}" marker
$DURATION = Extract from "**Duration:** {days} days" marker
$START_DATE = Extract from "**Start Date:** {date}" marker
$EPIC_ID = Extract from "**Epic:** {id}" marker (optional)
```

**Audit Deferrals mode:**
```
$AUDIT_MODE = Extract from "**Mode:** full-audit" marker (default: "full-audit")
```

See `references/parameter-extraction.md` for complete extraction algorithm.

VERIFY: All required parameters for the detected mode are present.
```
IF any required parameter missing: HALT -- "Missing parameter: {param_name} for {MODE} mode."
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=01 --step=4`

### Step 5: Set Phase Sequence

EXECUTE: Based on detected mode, set the PHASE_SEQUENCE for the orchestration loop.
```
IF MODE == "sprint-planning":
  PHASE_SEQUENCE = [01, 03S, 08]

ELSE IF MODE == "audit-deferrals":
  PHASE_SEQUENCE = [01, 03A, 04A, 08]

ELSE IF MODE == "story-management":
  PHASE_SEQUENCE = [01, 02, 03, 04, 05, 06, 07, 08]

ELSE IF MODE == "retrospective":
  PHASE_SEQUENCE = [01, 03R, 08]
```

Display:
```
"Mode: {MODE}
 Phase Sequence: {PHASE_SEQUENCE}
 Parameters: {extracted_params}"
```

VERIFY: PHASE_SEQUENCE is set and contains at least 2 phases (01 + 08 minimum).
```
IF PHASE_SEQUENCE is empty: HALT -- "Phase sequence not set."
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=01 --step=5`

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --phase=01 --checkpoint-passed
```

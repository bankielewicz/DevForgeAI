# Phase 01: Preflight & Mode Detection

## Entry Gate

```bash
devforgeai-validate phase-check ${SESSION_ID} --from=00 --to=01 ${WORKFLOW_FLAG}
# Exit 0: proceed | Exit 1: previous phase incomplete | Exit 127: CLI not installed (continue)
```

## Contract

PURPOSE: Validate project root, verify context files, extract parameters from conversation context, detect documentation mode (greenfield/brownfield/audit/fix), validate prerequisites per mode.
REQUIRED SUBAGENTS: (none)
REQUIRED ARTIFACTS: Session checkpoint, all parameters extracted, mode determined, prerequisites validated
STEP COUNT: 6 mandatory steps

---

## Reference Loading [MANDATORY]

```
Read(file_path="references/parameter-extraction.md")
```

IF Read fails: HALT -- "Phase 01 reference file not loaded. Cannot proceed without parameter-extraction.md."

---

## Mandatory Steps

### Step 1.1: Validate Project Root

EXECUTE: Read CLAUDE.md to confirm we are in the project root directory.
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
        HALT: AskUserQuestion("Cannot find project root. Provide correct path?")
```
VERIFY: CWD_VALID = true. If false, workflow HALTED via AskUserQuestion.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=01 --step=1.1 ${WORKFLOW_FLAG}`

---

### Step 1.2: Validate Context Files

EXECUTE: Verify all 6 constitutional context files exist.
```
context_files = [
    "devforgeai/specs/context/tech-stack.md",
    "devforgeai/specs/context/source-tree.md",
    "devforgeai/specs/context/dependencies.md",
    "devforgeai/specs/context/coding-standards.md",
    "devforgeai/specs/context/architecture-constraints.md",
    "devforgeai/specs/context/anti-patterns.md"
]

missing = []
FOR file in context_files:
    result = Glob(pattern=file)
    IF not found:
        missing.append(file)

IF missing is not empty:
    Display: "Missing context files: {missing}"
    Display: "Run /create-context first."
    HALT
ELSE:
    Display: "All 6 context files validated"
```
VERIFY: All 6 context files found. missing list is empty.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=01 --step=1.2 ${WORKFLOW_FLAG}`

---

### Step 1.3: Extract Parameters

EXECUTE: Extract all documentation parameters from conversation context using the algorithm in `references/parameter-extraction.md`.
```
# Extract from conversation context markers set by /document command:
$STORY_ID    = extracted story ID or empty
$DOC_TYPE    = extracted type or "readme" (default)
$MODE        = extracted mode or "greenfield" (default)
$EXPORT_FORMAT = extracted format or "markdown" (default)
$AUDIT_MODE  = extracted audit mode or null
$AUDIT_FIX   = extracted audit-fix flag or false
$FINDING_FILTER = extracted finding filter or "all"

Display: "Parameters extracted:"
Display: "  Story ID: {$STORY_ID or 'N/A'}"
Display: "  Type: {$DOC_TYPE}"
Display: "  Mode: {$MODE}"
Display: "  Export: {$EXPORT_FORMAT}"
Display: "  Audit: {$AUDIT_MODE or 'N/A'}"
Display: "  Fix: {$AUDIT_FIX}"
Display: "  Finding: {$FINDING_FILTER}"
```
VERIFY: At least one valid parameter combination extracted. If all empty/null AND no audit flags, HALT via AskUserQuestion.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=01 --step=1.3 ${WORKFLOW_FLAG}`

---

### Step 1.4: Determine Workflow Type

EXECUTE: Determine which workflow path to follow based on extracted parameters.
```
IF $AUDIT_MODE is set (dryrun):
    WORKFLOW_TYPE = "audit"
    Display: "Workflow: Audit (4-dimension DevEx scoring)"
ELIF $AUDIT_FIX is true:
    WORKFLOW_TYPE = "fix"
    Display: "Workflow: Fix (automated/interactive remediation)"
ELIF $STORY_ID provided:
    WORKFLOW_TYPE = "generation"
    $MODE = "greenfield"
    Display: "Workflow: Generation (greenfield, story-based)"
ELIF $MODE == "brownfield":
    WORKFLOW_TYPE = "generation"
    Display: "Workflow: Generation (brownfield, codebase analysis)"
ELSE:
    AskUserQuestion:
        Question: "No story ID or mode specified. Which documentation workflow?"
        Header: "Doc Mode"
        Options:
            - label: "Generate from stories (greenfield)"
              description: "Extract docs from completed story specifications"
            - label: "Analyze existing codebase (brownfield)"
              description: "Scan codebase and generate missing documentation"
            - label: "Audit documentation quality"
              description: "Score docs across 4 dimensions, generate findings"
        multiSelect: false

    Set WORKFLOW_TYPE based on user response.
```
VERIFY: WORKFLOW_TYPE is one of: "generation", "audit", "fix". If undetermined, user was prompted.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=01 --step=1.4 ${WORKFLOW_FLAG}`

---

### Step 1.5: Validate Prerequisites Per Mode

EXECUTE: Check mode-specific prerequisites.
```
IF WORKFLOW_TYPE == "generation" AND $MODE == "greenfield":
    IF $STORY_ID provided:
        story_file = Glob(pattern="devforgeai/specs/Stories/${STORY_ID}*.story.md")
        IF not found:
            HALT: "Story file not found for ${STORY_ID}"
        Read(file_path=story_file)
        Extract story status
        IF status not in ["Dev Complete", "QA Approved", "Released"]:
            Display: "Warning: Story status is '{status}'. Docs typically generated after Dev Complete."
            AskUserQuestion: "Continue generating docs for story in '{status}' state?"
    ELSE:
        # No specific story - will discover all completed stories
        Glob(pattern="devforgeai/specs/Stories/*.story.md")
        count = number of results
        Display: "Found {count} story files for discovery"

ELIF WORKFLOW_TYPE == "generation" AND $MODE == "brownfield":
    # Verify source code exists
    Glob(pattern="src/**/*")
    IF no results:
        HALT: "No source files found for brownfield analysis"
    Display: "Source tree detected for brownfield analysis"

ELIF WORKFLOW_TYPE == "fix":
    audit_file = "devforgeai/qa/audit/doc-audit.json"
    result = Read(file_path=audit_file)
    IF Read fails:
        HALT: "No audit file found at {audit_file}. Run '/document --audit=dryrun' first."
    Display: "Audit file loaded for fix workflow"

ELIF WORKFLOW_TYPE == "audit":
    # No special prerequisites beyond context files (already validated)
    Display: "Audit prerequisites met (context files validated)"
```
VERIFY: All mode-specific prerequisites passed without HALT.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=01 --step=1.5 ${WORKFLOW_FLAG}`

---

### Step 1.6: Create Session Checkpoint

EXECUTE: Write initial checkpoint to persist session state.
```
checkpoint = {
    "session_id": SESSION_ID,
    "workflow_type": WORKFLOW_TYPE,
    "current_phase": "01",
    "story_id": $STORY_ID or null,
    "doc_type": $DOC_TYPE,
    "mode": $MODE,
    "export_format": $EXPORT_FORMAT,
    "audit_mode": $AUDIT_MODE,
    "audit_fix": $AUDIT_FIX,
    "finding_filter": $FINDING_FILTER,
    "started_at": current_timestamp,
    "phases_completed": ["01"]
}

Bash(command="mkdir -p devforgeai/workflows")
Write(file_path="devforgeai/workflows/${SESSION_ID}-checkpoint.json", content=JSON(checkpoint))

Display: "Session checkpoint created: devforgeai/workflows/${SESSION_ID}-checkpoint.json"
```
VERIFY: Checkpoint file exists at `devforgeai/workflows/${SESSION_ID}-checkpoint.json`.
```
Glob(pattern="devforgeai/workflows/${SESSION_ID}-checkpoint.json")
IF not found: HALT -- "Checkpoint file not created"
```
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=01 --step=1.6 ${WORKFLOW_FLAG}`

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --phase=01 --checkpoint-passed ${WORKFLOW_FLAG}
```

## Phase Transition Display

```
Display: ""
Display: "Phase 01 complete: Preflight & Mode Detection"
Display: "  Workflow: {WORKFLOW_TYPE}"
Display: "  Mode: {$MODE}"
Display: "  Proceeding to Phase 02: Workflow Dispatch"
Display: ""
```

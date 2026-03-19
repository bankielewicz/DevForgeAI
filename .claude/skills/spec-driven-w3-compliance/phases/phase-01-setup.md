# Phase 01: Setup

## Entry Gate

```bash
devforgeai-validate phase-init W3-AUDIT --workflow=w3-compliance --project-root=.
# Exit 0: new workflow | Exit 1: resume | Exit 2: invalid | Exit 127: CLI not installed
```

## Contract

PURPOSE: Initialize W3 compliance audit environment -- validate CWD, extract parameters from command context markers, confirm scan readiness.
REQUIRED SUBAGENTS: none
REQUIRED ARTIFACTS: $MODE, $QUIET, $FIX_HINTS, CWD_VALID
STEP COUNT: 4 mandatory steps

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
    # Try secondary markers
    Glob(pattern=".claude/skills/*.md")
    IF results found:
        CWD_VALID = true
    ELSE:
        CWD_VALID = false
        HALT: AskUserQuestion("Cannot find project root. Provide correct path?")
```
VERIFY: CWD_VALID = true. If false, workflow HALTED via AskUserQuestion.
RECORD: `devforgeai-validate phase-record W3-AUDIT --workflow=w3-compliance --phase=01 --step=1.1 --project-root=.`

---

### Step 1.2: Extract Parameters from Context

EXECUTE: Extract scan parameters from command context markers set by /audit-w3. If context markers are not present (skill invoked directly), use defaults.
```
# Look for context markers in conversation:
#   **Mode:** ${MODE}
#   **Quiet:** ${QUIET}
#   **Fix Hints:** ${FIX_HINTS}

# If markers found:
$MODE = extracted value     # "normal" or "verbose"
$QUIET = extracted value    # true or false
$FIX_HINTS = extracted value # true or false

# If markers NOT found (direct invocation):
$MODE = "normal"
$QUIET = false
$FIX_HINTS = false

Display: "Parameters extracted:"
Display: "  Mode: ${MODE}"
Display: "  Quiet: ${QUIET}"
Display: "  Fix Hints: ${FIX_HINTS}"
```
VERIFY: $MODE is set to "normal" or "verbose". $QUIET is set to true or false. $FIX_HINTS is set to true or false.
RECORD: `devforgeai-validate phase-record W3-AUDIT --workflow=w3-compliance --phase=01 --step=1.2 --project-root=.`

---

### Step 1.3: Verify Scan Targets Exist

EXECUTE: Confirm that the directories to be scanned exist and contain files.
```
# Check agents directory
agent_files = Glob(pattern=".claude/agents/*.md")
Display: "Agent files found: {count(agent_files)}"

# Check skills directory
skill_files = Glob(pattern=".claude/skills/**/*.md")
Display: "Skill files found: {count(skill_files)}"

IF count(agent_files) == 0 AND count(skill_files) == 0:
    HALT: AskUserQuestion("No agent or skill files found. Is the .claude/ directory populated?")

$TOTAL_FILES = count(agent_files) + count(skill_files)
Display: "Total scan targets: ${TOTAL_FILES} files"
```
VERIFY: $TOTAL_FILES > 0. At least one of .claude/agents/ or .claude/skills/ contains .md files.
RECORD: `devforgeai-validate phase-record W3-AUDIT --workflow=w3-compliance --phase=01 --step=1.3 --project-root=.`

---

### Step 1.4: Display Setup Summary

EXECUTE: Display setup summary banner before scanning begins.
```
Display:
"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  W3 Compliance Audit - Setup Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Project root: Validated
  Mode: ${MODE}
  Quiet: ${QUIET}
  Fix Hints: ${FIX_HINTS}
  Scan targets: ${TOTAL_FILES} files
  Proceeding to Phase 02: Scanning...
"
```
VERIFY: Summary banner displayed with all parameter values populated.
RECORD: `devforgeai-validate phase-record W3-AUDIT --workflow=w3-compliance --phase=01 --step=1.4 --project-root=.`

---

## Exit Gate

```bash
devforgeai-validate phase-complete W3-AUDIT --workflow=w3-compliance --phase=01 --checkpoint-passed --project-root=.
# Exit 0: proceed to Phase 02 | Exit 1: HALT
```

## Phase 01 Completion Display

```
Phase 01 Complete: Setup
  CWD: Validated
  Parameters: Extracted
  Scan targets: ${TOTAL_FILES} files
```

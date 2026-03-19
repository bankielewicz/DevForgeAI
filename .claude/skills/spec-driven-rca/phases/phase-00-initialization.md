# Phase 00: Initialization

**Purpose:** Validate working directory, extract parameters, detect mode, initialize phase state.
**Applies to:** Both tactical and strategic modes.

---

## Step 00.1: Working Directory Validation [MANDATORY]

### EXECUTE

Verify the current working directory is the project root:

```
Read(file_path="CLAUDE.md")
```

Confirm content contains "DevForgeAI". If Read fails or content does not contain "DevForgeAI", HALT and ask user to navigate to project root.

### VERIFY

- Read succeeded (no error returned)
- Content includes "DevForgeAI" string

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=00 --step=00.1
```

---

## Step 00.2: Load Parameter Extraction Reference [MANDATORY]

### EXECUTE

```
Read(file_path=".claude/skills/spec-driven-rca/references/parameter-extraction.md")
```

This file contains the complete extraction algorithm for context markers in both modes.

### VERIFY

- File content is now in context
- Contains sections for both tactical and strategic marker extraction

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=00 --step=00.2
```

---

## Step 00.3: Detect Mode [MANDATORY]

### EXECUTE

Search conversation context for mode indicators:

**Tactical indicators (any one is sufficient):**
- `**Mode:** tactical` marker present
- `**Fix Attempts:**` marker present (set by dev workflow escalation)
- Context contains phase state from spec-driven-dev (Green/Integration/QA failure)

**Strategic indicators (any one is sufficient):**
- `**Mode:** strategic` marker present
- `**Issue Description:**` marker present (set by /rca command)
- `**Command:** rca` marker present
- No tactical indicators found (strategic is the default)

**Ambiguous (no indicators found):**
```
AskUserQuestion:
    Question: "This skill supports two analysis modes. Which do you need?"
    Header: "RCA Mode"
    Options:
        - label: "Tactical - Quick diagnosis for dev workflow failures"
          description: "Returns fix prescriptions. Use when tests keep failing during /dev."
        - label: "Strategic - Full RCA with 5 Whys analysis"
          description: "Creates self-contained RCA document. Use for framework breakdowns."
    multiSelect: false
```

Set `MODE` variable and determine `ACTIVE_PHASES`:
```
IF MODE == "tactical":
    ACTIVE_PHASES = ["00", "01", "02", "03"]
ELIF MODE == "strategic":
    ACTIVE_PHASES = ["00", "01", "02", "04", "05", "06", "07", "08"]
```

### VERIFY

- MODE is set to either "tactical" or "strategic"
- ACTIVE_PHASES array is populated with correct phase IDs

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=00 --step=00.3
```

---

## Step 00.4: Extract Mode-Specific Parameters [MANDATORY]

### EXECUTE

**For Tactical Mode:**
Extract from conversation context:
```
STORY_ID = extract "**Story ID:**" or "STORY-NNN" pattern
ERROR_MESSAGE = extract "**Error:**" or recent error output
FIX_ATTEMPTS = extract "**Fix Attempts:**" count (integer)
WORKFLOW_PHASE = extract "**Phase:**" (Green | Integration | QA)
FAILING_FILE = extract file path from error output
FAILING_FUNCTION = extract function/test name from error output
```

IF STORY_ID missing: Search for `devforgeai/workflows/*-phase-state.json` to identify active story.
IF ERROR_MESSAGE missing: HALT — cannot diagnose without an error to investigate.

**For Strategic Mode:**
Extract from conversation context:
```
ISSUE_DESCRIPTION = extract "**Issue Description:**" or recent user message
SEVERITY = extract "**Severity:**" (CRITICAL|HIGH|MEDIUM|LOW) or "infer"
AFFECTED_COMPONENT = infer from issue description:
    - Skill name (e.g., "spec-driven-dev") → component_type = "Skill"
    - Command name (e.g., "/dev") → component_type = "Command"
    - Subagent name (e.g., "diagnostic-analyst") → component_type = "Subagent"
    - Context file reference → component_type = "Context File"
    - Workflow/state reference → component_type = "Workflow"
```

IF ISSUE_DESCRIPTION missing:
```
AskUserQuestion:
    Question: "What framework breakdown should I analyze?"
    Header: "RCA Issue"
    Options:
        - "Skill didn't follow intended workflow"
        - "Command violated lean orchestration pattern"
        - "Quality gate was bypassed"
        - "Context file constraint ignored"
    multiSelect: false
```

IF SEVERITY == "infer":
```
Infer from keywords in ISSUE_DESCRIPTION:
    "broken", "blocking", "data loss" → CRITICAL
    "failed", "violation", "bypass" → HIGH
    "improvement", "gap", "unclear" → MEDIUM
    "minor", "cosmetic", "typo" → LOW
```

### VERIFY

- All required parameters extracted (no empty values for mandatory fields)
- MODE-specific parameters are complete

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=00 --step=00.4
```

---

## Step 00.5: Generate Session ID [MANDATORY]

### EXECUTE

**For Tactical Mode:**
```
SESSION_ID = "DIAG-" + STORY_ID
# Example: "DIAG-STORY-127"
```

**For Strategic Mode:**
Generate RCA number by scanning existing RCA files:
```
Glob(pattern="devforgeai/RCA/RCA-*.md")

Extract numbers from filenames: RCA-001 → 1, RCA-009 → 9
highest_number = max(extracted_numbers) or 0
rca_number = highest_number + 1
RCA_NUMBER = format(rca_number, "03d")  # e.g., "031"

SESSION_ID = "RCA-" + RCA_NUMBER
```

Generate RCA title (strategic only):
```
Extract keywords from ISSUE_DESCRIPTION
RCA_TITLE = "{Component} {Problem Type} {Brief Description}"
Length: 3-6 words
Example: "Context File Validation Missing"

slug = RCA_TITLE.lowercase().replace(" ", "-")
```

### VERIFY

- SESSION_ID is a non-empty string matching expected format
- For strategic: RCA_NUMBER does not collide with existing RCA files
- For strategic: RCA_TITLE is 3-6 words

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=00 --step=00.5
```

---

## Step 00.6: Initialize Phase State [MANDATORY]

### EXECUTE

```bash
devforgeai-validate phase-init ${SESSION_ID} --workflow=rca --project-root=.
```

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | New workflow | State file created. Set CURRENT_PHASE = "00". |
| 1 | Existing workflow | Resume from checkpoint. |
| 2 | Invalid session ID | HALT. Verify parameters. |
| 127 | CLI not installed | Continue without enforcement (backward compatibility). |

If resuming (exit code 1):
```
Read(file_path="devforgeai/temp/.rca-checkpoint-${SESSION_ID}.yaml")
```
Extract `current_phase` to determine where to resume.

### VERIFY

- Phase state file exists or backward-compatibility mode active
- CURRENT_PHASE is set

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=00 --step=00.6
```

---

## Step 00.7: Display Initialization Summary [MANDATORY]

### EXECUTE

Display summary for user:

**Tactical Mode:**
```
==============================
RCA INITIALIZATION (TACTICAL)
==============================
Mode: Tactical (dev workflow diagnosis)
Story: {STORY_ID}
Phase: {WORKFLOW_PHASE}
Error: {ERROR_MESSAGE first 100 chars}
Fix Attempts: {FIX_ATTEMPTS}
Session: {SESSION_ID}
Active Phases: 00, 01, 02, 03

Proceeding to Phase 01: Capture...
```

**Strategic Mode:**
```
==============================
RCA INITIALIZATION (STRATEGIC)
==============================
Mode: Strategic (full 5 Whys RCA)
Issue: {ISSUE_DESCRIPTION first 100 chars}
Severity: {SEVERITY}
Component: {AFFECTED_COMPONENT}
RCA Number: RCA-{RCA_NUMBER}
Title: {RCA_TITLE}
Session: {SESSION_ID}
Active Phases: 00, 01, 02, 04, 05, 06, 07, 08

Proceeding to Phase 01: Capture...
```

### VERIFY

- Summary displayed to user with all fields populated

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=00 --step=00.7
```

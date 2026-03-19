# Phase 00: Initialization

**Purpose:** Validate working directory, extract parameters from context markers, normalize Epic ID, and initialize phase state tracking.

**Mode:** ALL (this phase executes for every mode)

---

## Step 0.1: Validate Working Directory

**EXECUTE:**
```
Read(file_path="CLAUDE.md")
```

**VERIFY:**
- File content contains "DevForgeAI"
- If Read fails: HALT — working directory is not the project root

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --phase=00 --step=0.1 --project-root=. 2>&1")
```

---

## Step 0.2: Load Shared Protocols Reference

**EXECUTE:**
```
Read(file_path="src/claude/skills/spec-driven-coverage/references/shared-protocols.md")
```
If Read fails, try fallback path:
```
Read(file_path=".claude/skills/spec-driven-coverage/references/shared-protocols.md")
```

**VERIFY:**
- File content loaded into context
- Content contains "Execute-Verify-Gate"

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --phase=00 --step=0.2 --project-root=. 2>&1")
```

---

## Step 0.3: Load Parameter Extraction Reference

**EXECUTE:**
```
Read(file_path="src/claude/skills/spec-driven-coverage/references/parameter-extraction.md")
```
If Read fails, try fallback path:
```
Read(file_path=".claude/skills/spec-driven-coverage/references/parameter-extraction.md")
```

**VERIFY:**
- File content loaded into context
- Content contains "Context Markers"

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --phase=00 --step=0.3 --project-root=. 2>&1")
```

---

## Step 0.4: Extract Parameters from Context Markers

**EXECUTE:**
Extract the following from conversation context (set by invoking command):

| Parameter | Source | Required | Default |
|-----------|--------|----------|---------|
| EPIC_ID | `**Epic ID:**` marker | Yes | — |
| MODE | `**Mode:**` marker | Yes | — |
| PROMPT_MODE | `**Prompt Mode:**` marker | No | "interactive" |
| SPRINT | `**Sprint:**` marker | create mode only | "Backlog" |
| PRIORITY | `**Priority:**` marker | create mode only | "Medium" |
| POINTS | `**Points:**` marker | create mode only | "5" |
| INDIVIDUAL_PRIORITY | `**Individual Priority:**` marker | create mode only | false |
| INDIVIDUAL_POINTS | `**Individual Points:**` marker | create mode only | false |
| BATCH_TOTAL | `**Batch Total:**` marker | create mode only | — |

**VERIFY:**
- EPIC_ID is not empty (either a specific ID or "all")
- MODE is one of: "validate", "detect", "create"
- If MODE == "create": BATCH_TOTAL is a positive integer

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --phase=00 --step=0.4 --project-root=. 2>&1")
```

---

## Step 0.5: Normalize Epic ID (BR-001)

**EXECUTE:**
```
Read(file_path="src/claude/skills/spec-driven-coverage/references/business-rules.md")
```

Apply BR-001: Epic ID normalization
- Convert to uppercase
- Ensure format matches EPIC-NNN (zero-padded 3 digits)
- If EPIC_ID == "all": skip normalization, use literal "all"

**VERIFY:**
- EPIC_ID matches pattern `^EPIC-[0-9]{3}$` OR equals "all"
- If invalid format: HALT with error message

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --phase=00 --step=0.5 --project-root=. 2>&1")
```

---

## Step 0.6: Verify Epic Files Exist

**EXECUTE:**
```
IF EPIC_ID == "all":
    Glob(pattern="devforgeai/specs/Epics/*.epic.md")
ELSE:
    Glob(pattern="devforgeai/specs/Epics/${EPIC_ID}*.epic.md")
```

**VERIFY:**
- At least one epic file found
- If no files found AND EPIC_ID is specific: HALT with error "Epic not found: ${EPIC_ID}"
- If no files found AND EPIC_ID is "all": Display "No epics found. Run /create-epic to create epics." and RETURN early

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --phase=00 --step=0.6 --project-root=. 2>&1")
```

---

## Step 0.7: Determine Active Phases

**EXECUTE:**
Based on MODE, set the active phases array:

```
SWITCH on MODE:
    "validate": active_phases = ["00", "01", "02", "03"]
    "detect":   active_phases = ["00", "01"]
    "create":   active_phases = ["00", "01", "04", "05"]
```

**VERIFY:**
- active_phases array is populated
- active_phases[0] == "00" (current phase)

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --phase=00 --step=0.7 --project-root=. 2>&1")
```

---

## Phase 00 Completion

**EXECUTE:**
```
Bash(command="devforgeai-validate phase-complete ${IDENTIFIER} --phase=00 --project-root=. 2>&1")
```

**VERIFY:**
- Exit code 0 or 2 (backward compatibility)

**NEXT:** Proceed to Phase 01 (Gap Detection) — required for ALL modes.

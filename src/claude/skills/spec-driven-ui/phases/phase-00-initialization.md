# Phase 00: Initialization

**Purpose:** Validate working directory, extract parameters from context markers, and initialize phase state tracking.

**Mode:** ALL (this phase executes for every invocation)

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
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --workflow=ui --phase=00 --step=0.1 --project-root=. 2>&1")
```

---

## Step 0.2: Load Shared Protocols Reference

**EXECUTE:**
```
Read(file_path="src/claude/skills/spec-driven-ui/references/shared-protocols.md")
```
If Read fails, try fallback path:
```
Read(file_path=".claude/skills/spec-driven-ui/references/shared-protocols.md")
```

**VERIFY:**
- File content loaded into context
- Content contains "Execute-Verify-Record"

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --workflow=ui --phase=00 --step=0.2 --project-root=. 2>&1")
```

---

## Step 0.3: Load Parameter Extraction Reference

**EXECUTE:**
```
Read(file_path="src/claude/skills/spec-driven-ui/references/parameter-extraction.md")
```
If Read fails, try fallback path:
```
Read(file_path=".claude/skills/spec-driven-ui/references/parameter-extraction.md")
```

**VERIFY:**
- File content loaded into context
- Content contains "Mode Detection" or "Context Markers"

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --workflow=ui --phase=00 --step=0.3 --project-root=. 2>&1")
```

---

## Step 0.4: Extract Parameters from Context Markers

**EXECUTE:**
Extract the following from conversation context (set by invoking /create-ui command):

| Parameter | Source | Required | Default |
|-----------|--------|----------|---------|
| MODE | `**Mode:**` marker | Yes | — |
| TARGET | `**Target:**` marker | Yes | — |

Mode detection logic:
- If MODE == "story": TARGET is a STORY-ID (e.g., STORY-042)
- If MODE == "standalone": TARGET is a component description string

Set IDENTIFIER:
- Story mode: IDENTIFIER = STORY_ID (e.g., "STORY-042")
- Standalone mode: IDENTIFIER = "UI-STANDALONE"

**VERIFY:**
- MODE is one of: "story", "standalone"
- TARGET is not empty
- IDENTIFIER is set

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --workflow=ui --phase=00 --step=0.4 --project-root=. 2>&1")
```

---

## Step 0.5: Verify Story File Exists (Story Mode Only)

**EXECUTE:**
```
IF MODE == "story":
    Glob(pattern="devforgeai/specs/Stories/${STORY_ID}*.story.md")
    IF found: Read the story file
    IF not found: HALT with error "Story not found: ${STORY_ID}"
ELSE:
    SKIP — standalone mode does not require a story file
```

**VERIFY:**
- Story mode: Story file found and readable
- Standalone mode: Step marked as skipped (valid)

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --workflow=ui --phase=00 --step=0.5 --project-root=. 2>&1")
```

---

## Phase 00 Completion

**EXECUTE:**
```
Bash(command="devforgeai-validate phase-complete ${IDENTIFIER} --workflow=ui --phase=00 --project-root=. 2>&1")
```

**VERIFY:**
- Exit code 0 or 2 (backward compatibility)

**NEXT:** Proceed to Phase 01 (Context Validation).

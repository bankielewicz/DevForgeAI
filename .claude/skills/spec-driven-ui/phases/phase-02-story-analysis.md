# Phase 02: Story Analysis & Mode Detection

**Purpose:** Extract UI requirements from story acceptance criteria (story mode) or prepare for interactive discovery (standalone mode).

**Pre-Flight:** Verify Phase 01 completed.

---

## Step 2.1: Load Story Analysis Reference

**EXECUTE:**
```
Read(file_path="src/claude/skills/spec-driven-ui/references/story-analysis.md")
```
If Read fails, try fallback path:
```
Read(file_path=".claude/skills/spec-driven-ui/references/story-analysis.md")
```

**VERIFY:**
- File content loaded into context
- Content contains story parsing procedures

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --workflow=ui --phase=02 --step=2.1 --project-root=. 2>&1")
```

---

## Step 2.2: Detect Mode and Branch

**EXECUTE:**
Check MODE variable from Phase 00:

```
IF MODE == "story":
    Display: "Story mode detected. Extracting UI requirements from story."
    Proceed to Step 2.3 (Story Requirements Extraction)
ELIF MODE == "standalone":
    Display: "Standalone mode detected. Loading user-input-guidance.md..."
    Read(file_path="src/claude/skills/spec-driven-ui/references/user-input-guidance.md")
    If Read fails: Read(file_path=".claude/skills/spec-driven-ui/references/user-input-guidance.md")
    Display: "Guidance loaded — applying patterns to UI questions"
    Proceed to Step 2.4 (skip Step 2.3)
```

**VERIFY:**
- MODE is "story" or "standalone"
- If standalone: user-input-guidance.md loaded successfully

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --workflow=ui --phase=02 --step=2.2 --project-root=. 2>&1")
```

---

## Step 2.3: Extract Story UI Requirements (Story Mode Only)

**EXECUTE:**
From the story file loaded in Phase 00 Step 0.5, extract:
- UI components mentioned in Acceptance Criteria (Given/When/Then)
- Technical Specification references to UI elements
- Non-Functional Requirements for UI (performance, accessibility)
- Data fields and interactions described

Build a structured requirements summary:
```
UI_REQUIREMENTS = {
    components: [list of identified components],
    interactions: [user actions described in AC],
    data_fields: [form fields, display fields],
    accessibility: [any accessibility requirements],
    responsive: [any responsive requirements]
}
```

**VERIFY:**
- At least one component identified from story
- If no UI requirements found in story: AskUserQuestion — "No explicit UI requirements found in story. Describe the UI components needed."

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --workflow=ui --phase=02 --step=2.3 --project-root=. 2>&1")
```

---

## Step 2.4: Summarize Requirements for Downstream Phases

**EXECUTE:**
Create a consolidated requirements summary containing:
- Mode (story or standalone)
- Component list (from story extraction or pending user input)
- Data requirements
- Accessibility requirements
- Any constraints from context files (Phase 01)

Display the summary to the user.

**VERIFY:**
- Summary is non-empty
- Summary contains at least: mode and component list (or placeholder for standalone)

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --workflow=ui --phase=02 --step=2.4 --project-root=. 2>&1")
```

---

## Phase 02 Completion

**EXECUTE:**
```
Bash(command="devforgeai-validate phase-complete ${IDENTIFIER} --workflow=ui --phase=02 --project-root=. 2>&1")
```

**VERIFY:**
- Exit code 0 or 2 (backward compatibility)

**NEXT:** Proceed to Phase 03 (Interactive Discovery).

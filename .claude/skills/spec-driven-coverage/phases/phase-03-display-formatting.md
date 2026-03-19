# Phase 03: Display Formatting

**Purpose:** Delegate all display output to the epic-coverage-result-interpreter subagent. Apply shell-safe escaping to gap commands (BR-003).

**Mode:** validate only (skip this phase for detect and create modes)

**Pre-Flight:** Verify Phase 02 completed and display_data is available.

---

## Step 3.1: Verify Phase 02 Completion

**EXECUTE:**
Check that display_data from Phase 02 is available in working memory.

**VERIFY:**
- display_data object exists
- display_data.mode is populated ("single-epic" or "all-epics")
- If display_data is missing: HALT — Phase 02 did not complete correctly

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --phase=03 --step=3.1 --project-root=. 2>&1")
```

---

## Step 3.2: Load Business Rules Reference (BR-003)

**EXECUTE:**
```
Read(file_path="src/claude/skills/spec-driven-coverage/references/business-rules.md")
```
If Read fails, try fallback path:
```
Read(file_path=".claude/skills/spec-driven-coverage/references/business-rules.md")
```

Review BR-003 (Shell-Safe Escaping) before delegating to subagent.

**VERIFY:**
- File content loaded into context
- Content contains "BR-003" and "shell-safe"

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --phase=03 --step=3.2 --project-root=. 2>&1")
```

---

## Step 3.3: Determine Display Template

**EXECUTE:**
```
IF EPIC_ID is a specific ID (not "all"):
    template = "single-epic"
ELSE:
    template = "all-epics"
```

**VERIFY:**
- template is one of "single-epic" or "all-epics"

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --phase=03 --step=3.3 --project-root=. 2>&1")
```

---

## Step 3.4: Delegate to epic-coverage-result-interpreter Subagent

**EXECUTE:**
```
Task(
    subagent_type="epic-coverage-result-interpreter",
    description="Format ${template} coverage display",
    prompt="""
    Generate coverage display using template: ${template}

    Data:
    - Epic ID: ${EPIC_ID}
    - Total features: ${gap_data.total_features}
    - Covered features: ${gap_data.covered_features}
    - Coverage: ${gap_data.coverage_percentage}%
    - Missing features: ${JSON.stringify(gap_data.missing_features)}
    - Report data: ${JSON.stringify(report_data)} (if available)

    Visual indicators:
    - GREEN: 100% coverage
    - YELLOW: 50-99% coverage
    - RED: <50% coverage

    Include actionable gap list with shell-safe /create-story commands (top 10).
    If >10 gaps, show overflow count and batch creation hint.

    Shell-safe escaping (BR-003): Feature descriptions containing quotes,
    backticks, or $ must be escaped in /create-story command suggestions.
    Use single-quote wrapping with interior escaping per POSIX shell conventions.
    """
)
```

**VERIFY:**
- Subagent was invoked (Task call completed)
- Subagent returned display output
- Display output contains visual indicators (coverage percentage visible)

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --phase=03 --step=3.4 --project-root=. 2>&1")
```

---

## Step 3.5: Present Display Output

**EXECUTE:**
Present the subagent's formatted output to the user. The output includes:
- Color-coded coverage indicators per epic
- Per-feature breakdown (covered vs gaps)
- Actionable /create-story commands for top 10 gaps
- Framework-wide coverage percentage (all-epics mode)
- Batch creation hint if >10 gaps

**VERIFY:**
- Display output presented to user
- If PROMPT_MODE == "quiet" or "ci": output is structured data only (no interactive prompts)

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --phase=03 --step=3.5 --project-root=. 2>&1")
```

---

## Phase 03 Completion

**EXECUTE:**
```
Bash(command="devforgeai-validate phase-complete ${IDENTIFIER} --phase=03 --project-root=. 2>&1")
```

**VERIFY:**
- Exit code 0 or 2 (backward compatibility)

**NEXT:** DONE for validate mode. Return gap_data to the invoking command for interactive gap resolution.

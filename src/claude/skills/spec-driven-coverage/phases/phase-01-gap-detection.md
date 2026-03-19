# Phase 01: Gap Detection

**Purpose:** Execute gap detection scripts, parse JSON output, and collect raw coverage data. Handle edge cases (no features, 100% coverage).

**Mode:** ALL (this phase executes for every mode)

**Pre-Flight:** Verify Phase 00 completed before proceeding.

---

## Step 1.1: Load Gap Detector Integration Reference

**EXECUTE:**
```
Read(file_path="src/claude/skills/spec-driven-coverage/references/gap-detector-integration.md")
```
If Read fails, try fallback path:
```
Read(file_path=".claude/skills/spec-driven-coverage/references/gap-detector-integration.md")
```

**VERIFY:**
- File content loaded into context
- Content contains "gap-detector.sh"

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --phase=01 --step=1.1 --project-root=. 2>&1")
```

---

## Step 1.2: Load Business Rules Reference

**EXECUTE:**
```
Read(file_path="src/claude/skills/spec-driven-coverage/references/business-rules.md")
```
If Read fails, try fallback path:
```
Read(file_path=".claude/skills/spec-driven-coverage/references/business-rules.md")
```

**VERIFY:**
- File content loaded into context
- Content contains "BR-002"

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --phase=01 --step=1.2 --project-root=. 2>&1")
```

---

## Step 1.3: Run Gap Detector

**EXECUTE:**
```
IF EPIC_ID == "all":
    Bash(command="devforgeai/traceability/gap-detector.sh 2>&1")
ELSE:
    Bash(command="devforgeai/traceability/gap-detector.sh ${EPIC_ID} 2>&1")
```

**VERIFY:**
- Command executed (exit code 0 or output contains JSON)
- If script not found (exit code 127): HALT with "gap-detector.sh not found at devforgeai/traceability/gap-detector.sh"

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --phase=01 --step=1.3 --project-root=. 2>&1")
```

---

## Step 1.4: Parse JSON Output

**EXECUTE:**
Parse the gap detector output to extract structured data:

```
gap_data = {
    epic_id: EPIC_ID,
    total_features: <integer from output>,
    covered_features: <integer from output>,
    missing_features: [<array of {feature_number, feature_title, feature_description}>],
    coverage_percentage: <float from output>,
    consistency_score: <float if available>,
    story_count: <integer if available>,
    mismatch_count: <integer if available>,
    orphan_count: <integer if available>
}
```

For all-epics mode, parse into an array of per-epic gap_data objects.

**VERIFY:**
- gap_data.total_features is a non-negative integer
- gap_data.coverage_percentage is between 0.0 and 100.0
- gap_data.missing_features is an array (may be empty)

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --phase=01 --step=1.4 --project-root=. 2>&1")
```

---

## Step 1.5: Handle Edge Cases

**EXECUTE:**
Check for early-exit conditions:

```
# Edge Case 1: No features defined in epic
IF gap_data.total_features == 0:
    Display: "No features defined in ${EPIC_ID}"
    Display: "To define features, edit: devforgeai/specs/Epics/${EPIC_ID}*.epic.md"
    Display: "Or run /ideate to generate features from a business idea."
    SET early_exit = true
    SET early_exit_reason = "no_features"

# Edge Case 2: 100% coverage (no gaps)
IF gap_data.missing_features.length == 0 AND gap_data.total_features > 0:
    Display: "${EPIC_ID} has 100% coverage!"
    Display: "All ${gap_data.total_features} features have stories."
    SET early_exit = true
    SET early_exit_reason = "full_coverage"
```

**VERIFY:**
- Edge case logic evaluated
- If early_exit == true AND MODE == "detect": RETURN gap_data immediately
- If early_exit == true AND MODE == "validate": Skip to Phase 03 for display only
- If early_exit == true AND MODE == "create": RETURN with message "No gaps to create stories for"

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --phase=01 --step=1.5 --project-root=. 2>&1")
```

---

## Step 1.6: Apply Coverage Counting Rules (BR-002)

**EXECUTE:**
Apply BR-002: Only stories with status >= "Dev Complete" count toward coverage percentage.

- Stories in Backlog, Architecture, Ready for Dev, or In Development show as "Planned" but do NOT contribute to coverage_percentage
- Stories in Dev Complete, QA In Progress, QA Approved, Releasing, or Released count as covered

Recalculate coverage_percentage using BR-002 rules if the gap detector output includes status data.

**VERIFY:**
- coverage_percentage reflects BR-002 counting rules
- Planned-but-not-complete stories are excluded from numerator

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --phase=01 --step=1.6 --project-root=. 2>&1")
```

---

## Step 1.7: Store Gap Data for Downstream Phases

**EXECUTE:**
Retain gap_data in working memory for use by subsequent phases (02, 03, 04, or 05 depending on mode).

If MODE == "detect":
- RETURN gap_data as structured output
- Skip remaining phases (01 is the last active phase for detect mode)

**VERIFY:**
- gap_data object is populated and accessible
- If MODE == "detect": gap_data returned to caller

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --phase=01 --step=1.7 --project-root=. 2>&1")
```

---

## Phase 01 Completion

**EXECUTE:**
```
Bash(command="devforgeai-validate phase-complete ${IDENTIFIER} --phase=01 --project-root=. 2>&1")
```

**VERIFY:**
- Exit code 0 or 2 (backward compatibility)

**NEXT:**
- If MODE == "validate": Proceed to Phase 02 (Coverage Report)
- If MODE == "detect": DONE — return structured gap data
- If MODE == "create": Proceed to Phase 04 (Batch Story Creation)

# Phase 08: Feedback & Completion

**Purpose:** Invoke feedback hooks, generate completion report, and finalize the UI generation workflow.

**Pre-Flight:** Verify Phase 07 completed.

---

## Reference Loading [MANDATORY]

```
# No required references for this phase. Phase 08 invokes feedback hooks
# via devforgeai-validate (Bash calls — not Reads), displays the completion
# report assembled from session.origin + variables accumulated in Phases
# 01-07, and finalizes the workflow. No skill references, context files,
# memory, or stories are loaded.
```

---

## Step 8.1: Check Feedback Hook Eligibility

**EXECUTE:**
```
Bash(command="devforgeai-validate check-hooks --operation=create-design --status=success 2>&1")
```

**VERIFY:**
- Exit code 0: Hooks are enabled and eligible → proceed to Step 8.2
- Exit code non-zero: Hooks not configured or not eligible → skip to Step 8.3

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} ${WORKFLOW_FLAG} --phase=08 --step=8.1 --project-root=. 2>&1")
```

---

## Step 8.2: Invoke Feedback Hooks (Conditional)

**EXECUTE:**
```
IF hooks eligible (Step 8.1 exit code 0):
    Bash(command="devforgeai-validate invoke-hooks --operation=create-design 2>&1")

    Pass context:
    - ui_type: ${UI_TYPE}
    - technology: ${FRAMEWORK}
    - components: ${COMPONENTS}
    - styling: ${STYLING}
    - story_id: ${STORY_ID} (if story mode)
    - status: ${STATUS}
ELSE:
    Display: "Feedback hooks not configured. Skipping."
```

**VERIFY:**
- Hook invocation completed (success or graceful failure)
- Non-blocking: If hooks fail, log warning and continue

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} ${WORKFLOW_FLAG} --phase=08 --step=8.2 --project-root=. 2>&1")
```

---

## Step 8.3: Generate Completion Report

**EXECUTE:**
Display completion report to user:

```
## UI Generation Complete

**Status:** ${STATUS}
**Mode:** ${MODE}
**UI Type:** ${UI_TYPE}
**Framework:** ${FRAMEWORK}
**Styling:** ${STYLING}
**Theme:** ${THEME}

### Generated Files
- Component: ${OUTPUT_PATH}
- Spec Summary: devforgeai/specs/ui/UI-SPEC-SUMMARY.md

### Components Created
${COMPONENTS list with details}

### Next Steps

```
# Origin-aware routing: send user back to the skill that punted to /create-design
IF session.origin is not null:

  IF session.origin.skill == "ideation":
    Display: "═══ Return to Ideation ═══"
    Display: "design.md created. Your ideation session can now consume it."
    IF session.origin.id:
      Display: "  Resume: /ideate --resume ${session.origin.id}"
    ELSE:
      Display: "  Resume: /ideate (design.md will be auto-detected)"
    Display: ""
    Display: "After ideation, continue with: /create-system-architecture → /create-solution-architecture → /create-story → /dev"

  ELIF session.origin.skill == "architecture":
    Display: "═══ Return to Architecture ═══"
    Display: "design.md created. Continue with epic creation:"
    Display: "  /create-solution-architecture <epic-name>"
    Display: ""
    Display: "Then continue with: /create-story → /dev → /qa"

  ELIF session.origin.skill == "brainstorm":
    Display: "═══ Continue to Ideation ═══"
    Display: "design.md created. Brainstorm is complete. Continue the workflow:"
    Display: "  /ideate (brainstorm + design.md will be auto-detected)"
    Display: ""
    Display: "Then: /create-system-architecture → /create-solution-architecture → /create-story → /dev"

  ELSE:
    Display: "═══ Continue Workflow ═══"
    Display: "Return to: ${session.origin.skill}"

ELSE:
  # No origin — standalone invocation or no punt
  Display: "- Review generated code and design.md"
  Display: "- Install any required dependencies"
  Display: "- Run /create-story to create stories from this spec"
  Display: "- Run /dev to implement the full story (if story mode)"
  Display: "- Run /qa to validate the implementation"

# Visual capture reminder (if screenshots were taken)
IF session.url_validation == true:
  Display: ""
  Display: "Visual Capture: Screenshots saved to devforgeai/specs/ui/visual-capture/"
  Display: "  These will be consumed by /dev, /qa, /create-story, and /create-solution-architecture"
```

If FORMATTER_RESULT contains display template and next_steps, output those as-is (AFTER origin routing above).

**VERIFY:**
- Completion report displayed to user
- Report contains: status, mode, files generated, next steps

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} ${WORKFLOW_FLAG} --phase=08 --step=8.3 --project-root=. 2>&1")
```

---

## Phase 08 Completion

**EXECUTE:**
```
Bash(command="devforgeai-validate validate-design-phase ${IDENTIFIER} ${WORKFLOW_FLAG} --mode=${MODE} --phase=08 --project-root=. 2>&1")
Bash(command="devforgeai-validate phase-complete ${IDENTIFIER} ${WORKFLOW_FLAG} --phase=08 --project-root=. 2>&1")
```

**VERIFY:**
- Exit code 0; any non-zero result blocks completion

**WORKFLOW COMPLETE.** All 9 phases executed successfully.

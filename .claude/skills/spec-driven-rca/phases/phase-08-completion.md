# Phase 08: Completion & Pipeline (Strategic Mode Only)

**Purpose:** Generate completion report, determine next steps, and run recommendation-to-story pipeline.
**Applies to:** Strategic mode only.

---

## Step 08.1: Generate Completion Summary [MANDATORY]

### EXECUTE

```
Create summary:
    rca_number: "RCA-{RCA_NUMBER}"
    rca_title: "{RCA_TITLE}"
    rca_file: "devforgeai/RCA/RCA-{RCA_NUMBER}-{slug}.md"
    severity: "{SEVERITY}"
    root_cause_brief: "{1-2 sentence summary of Why #5}"
    recommendation_counts: {
        CRITICAL: {count},
        HIGH: {count},
        MEDIUM: {count},
        LOW: {count}
    }
    total_recommendations: {count}
```

### VERIFY

- All summary fields populated
- Root cause brief is 1-2 sentences (not a paragraph)

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=08 --step=08.1
```

---

## Step 08.2: Determine Next Steps [MANDATORY]

### EXECUTE

```
IF recommendation_counts.CRITICAL > 0:
    next_steps = "Review CRITICAL recommendations immediately. Create stories for implementation if substantial work (>2 hours)."

ELIF recommendation_counts.HIGH > 0:
    next_steps = "Review HIGH recommendations. Plan implementation in current sprint."

ELIF recommendation_counts.MEDIUM > 0:
    next_steps = "Review MEDIUM recommendations. Add to next sprint backlog."

ELSE:
    next_steps = "Review LOW priority improvements. Implement opportunistically."

Append: next_steps += "\n\nRead complete RCA: {rca_file}"
```

### VERIFY

- Next steps determined based on highest priority recommendations
- RCA file path included in next steps

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=08 --step=08.2
```

---

## Step 08.3: Display Completion Report [MANDATORY]

### EXECUTE

Display formatted report:

```
==============================================
RCA COMPLETE: RCA-{RCA_NUMBER}
==============================================

Title: {RCA_TITLE}
Severity: {SEVERITY}
File: devforgeai/RCA/RCA-{RCA_NUMBER}-{slug}.md

ROOT CAUSE:
{root_cause_brief}

RECOMMENDATIONS:
- CRITICAL: {count} (implement immediately)
- HIGH: {count} (implement this sprint)
- MEDIUM: {count} (next sprint)
- LOW: {count} (backlog)

NEXT STEPS:
{next_steps}

==============================================
```

### VERIFY

- Report displayed to user with all fields populated
- No placeholder text remaining

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=08 --step=08.3
```

---

## Step 08.4: Recommendation-to-Story Pipeline [CONDITIONAL]

### EXECUTE

**Failure Isolation:** This step's failure does NOT invalidate the RCA. The RCA document was already written and validated in Phases 06-07. Wrap all pipeline logic in error handling.

```
TRY:
    Execute pipeline steps below
CATCH any error:
    Display: "WARNING: Recommendation-to-Story Pipeline encountered an error."
    Display: "The RCA document remains valid at: {rca_file}"
    Display: "Error: {error_message}"
    Skip to Step 08.5 (non-blocking)
```

**Filter actionable recommendations:**
```
actionable_recs = [rec for rec in recommendations if rec.priority in ("CRITICAL", "HIGH")]
skipped_recs = [rec for rec in recommendations if rec.priority in ("MEDIUM", "LOW")]

IF len(skipped_recs) > 0:
    Display: "Skipping {count} MEDIUM/LOW recommendations (informational only)"

IF len(actionable_recs) == 0:
    Display: "No CRITICAL/HIGH recommendations to process. Pipeline complete."
    Skip to Step 08.5
```

**For each actionable recommendation:**
```
FOR each rec in actionable_recs:
    Display:
        Priority: {rec.priority}
        ID: {rec.id}
        Title: {rec.title}
        Time: {rec.effort_hours} hours

    AskUserQuestion:
        Question: "What action for {rec.id} ({rec.priority}): {rec.title}?"
        Header: "RCA Pipeline"
        Options:
            - label: "Create story"
              description: "Run /create-stories-from-rca to generate story files"
            - label: "Add to technical debt register"
              description: "Append to devforgeai/technical-debt-register.md"
            - label: "Skip"
              description: "Acknowledged, no action taken"
        multiSelect: false

    IF user_choice == "Create story":
        Display:
            "To create stories from this RCA, run:"
            "  /create-stories-from-rca RCA-{RCA_NUMBER}"

    ELIF user_choice == "Add to technical debt register":
        Read(file_path="devforgeai/technical-debt-register.md")
        # Append entry to end of table
        entry = "| {rec.id} | {rec.priority} | {rec.title} | Source: RCA-{RCA_NUMBER} | Open |"
        Edit(file_path="devforgeai/technical-debt-register.md",
             old_string="{last_table_row}",
             new_string="{last_table_row}\n{entry}")
        Display: "Added to technical debt register: {rec.title}"

    ELIF user_choice == "Skip":
        Display: "Skipped: {rec.id} - {rec.title}"
```

**Pipeline summary:**
```
Display:
    "Recommendation Pipeline Results:"
    "  Stories queued:   {create_count}"
    "  Debt registered: {debt_count}"
    "  Skipped:         {skip_count}"
```

### VERIFY

- Pipeline executed or gracefully handled error
- User was prompted for each actionable recommendation
- Actions executed as selected

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=08 --step=08.4
```

---

## Step 08.5: Final Workflow Completion [MANDATORY]

### EXECUTE

```
Display:
"
RCA Workflow Complete
=====================
Mode: Strategic
Session: {SESSION_ID}
Document: devforgeai/RCA/RCA-{RCA_NUMBER}-{slug}.md
Recommendations: {total_count}
Status: COMPLETE
"
```

### VERIFY

- Completion message displayed
- RCA document file exists at reported path

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=08 --step=08.5
```

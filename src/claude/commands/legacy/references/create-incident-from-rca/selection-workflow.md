# Interactive Selection Workflow (Phases 6-9)

Detailed pseudocode for interactive recommendation selection.

After Phase 1-5 (parsing) returns a `recommendations` array, the user picks which subset to convert into GitHub issues. The output of this phase (`selected_recommendations`) is the input to Phase 10 (the `github-incident-from-rca` skill).

---

## Phase 6: Display Recommendation Summary Table

```
# Display formatted table (readable in 80-char terminal)
IF rca_document.recommendations.length > 0:
    Display: ""
    Display: "┌─────────┬──────────┬────────────────────────────────────┬────────┐"
    Display: "│ REC ID  │ Priority │ Title                              │ Effort │"
    Display: "├─────────┼──────────┼────────────────────────────────────┼────────┤"

    FOR rec in rca_document.recommendations:
        # Truncate title to fit 34 chars
        display_title = rec.title[:34] IF len(rec.title) > 34 ELSE rec.title.ljust(34)
        effort_str = format_effort_estimate(rec.effort_hours)
        Display: "│ ${rec.id.ljust(7)} │ ${rec.priority.ljust(8)} │ ${display_title} │ ${effort_str.rjust(6)} │"

    Display: "└─────────┴──────────┴────────────────────────────────────┴────────┘"
    Display: ""
```

---

## Phase 7: Interactive Selection

```
# Returns selected_recommendations after user selection

# Edge case: No recommendations after filtering
IF rca_document.recommendations.length == 0:
    Display: "No recommendations meet effort threshold. Exiting."
    HALT

# Build options array for AskUserQuestion
options = []

# "All recommendations" option first (recommended)
options.append({
    label: "All recommendations (Recommended)",
    description: "Convert all ${rca_document.recommendations.length} eligible recommendations into GitHub issues"
})

# Individual recommendation options
FOR rec in rca_document.recommendations:
    effort_str = format_effort_estimate(rec.effort_hours)
    options.append({
        label: "${rec.id}: ${rec.title[:30]}",
        description: "Priority: ${rec.priority}, Effort: ${effort_str}"
    })

# "None - cancel" option last
options.append({
    label: "None - cancel",
    description: "Exit without creating issues"
})

# Prompt user with multiSelect: true
AskUserQuestion(
    questions=[{
        question: "Which recommendations to convert into GitHub issues?",
        header: "Select",
        multiSelect: true,
        options: options
    }]
)

# Capture user selection
user_selection = captured from AskUserQuestion response
```

---

## Phase 8: Handle Selection

```
selected_recommendations = []

# Handle "None - cancel"
IF user_selection contains "None - cancel":
    Display: "No recommendations selected. Exiting."
    HALT

# Handle "All recommendations"
IF user_selection contains "All recommendations":
    selected_recommendations = rca_document.recommendations
    Display: "Selected all ${selected_recommendations.length} recommendations"

# Handle individual selections
ELSE:
    FOR selection in user_selection:
        IF selection matches "REC-[0-9]+":
            rec_id = extract REC ID
            rec = find_recommendation_by_id(rec_id)
            IF rec:
                selected_recommendations.append(rec)
            ELSE:
                Display: "Warning: Invalid REC ID '${rec_id}', ignoring"

    # Handle "Other" (custom comma-separated input)
    IF user_selection contains custom text:
        custom_ids = parse comma-separated REC IDs
        FOR rec_id in custom_ids:
            rec = find_recommendation_by_id(rec_id)
            IF rec:
                selected_recommendations.append(rec)
            ELSE:
                Display: "Warning: Invalid REC ID '${rec_id}', ignoring"

# Validate minimum selection
IF selected_recommendations.length == 0:
    Display: "No valid recommendations selected. Please try again."
    GOTO Phase 7  # Re-prompt

Display: "Selected ${selected_recommendations.length} recommendation(s) for GitHub issue creation"
```

---

## Phase 9: Pass to Issue Creation Skill

```
# Selected recommendations passed forward to Phase 10 skill invocation
# No data loss in transformation - all fields complete and intact
# The github-incident-from-rca skill consumes this format directly

batch_input = {
    rca_document: {
        id: rca_document.id,
        title: rca_document.title,
        severity: rca_document.severity
    },
    selected_recommendations: selected_recommendations,
    selection_count: selected_recommendations.length
}

# Each recommendation preserves full metadata for the skill's drafting phase:
# - id (REC-N)              ← used for draft filename, label decisions
# - priority (CRITICAL|HIGH|MEDIUM|LOW)  ← maps to priority:* label
# - title (string)          ← seeds the issue title (skill rewrites to imperative form)
# - description (string)    ← seeds Context, Current behavior, Required behavior
# - effort_hours (integer|null)  ← informational; not used by skill
# - effort_points (integer|null) ← informational; not used by skill
# - success_criteria (array)     ← seeds Acceptance criteria checklist

Display: ""
Display: "Proceeding to GitHub issue drafting via github-incident-from-rca skill (${selection_count} recommendation(s))..."
Display: ""

# Invoke skill (Phase 10)
Skill(command="github-incident-from-rca", args="--batch")
```

---

## Edge Cases Handled

| Edge Case | Behavior |
|-----------|----------|
| Single recommendation | Still display selection prompt (allow cancel) |
| No recommendations after filter | Display "No recommendations meet effort threshold" and HALT |
| User selects "Other" | Parse comma-separated REC IDs from custom input |
| Invalid REC ID in selection | Log warning and ignore invalid entries |
| Empty selection | Re-prompt user for valid selection |
| User cancels | HALT gracefully, no skill invocation |

---

## Difference from /create-stories-from-rca's selection

The selection workflow is structurally identical to the stories version, with two intentional adaptations:

1. **Question wording** — `"Which recommendations to convert into GitHub issues?"` instead of `"to convert to stories?"`. Users reading the prompt should know exactly what artifact will be produced.
2. **All-option label** — `"Convert all N eligible recommendations into GitHub issues"` instead of `"Create stories for..."`. Same clarity reason.

The downstream consumer is different (skill vs skill), but the selection mechanics — multiselect, all/none/individual, custom-other — are identical.

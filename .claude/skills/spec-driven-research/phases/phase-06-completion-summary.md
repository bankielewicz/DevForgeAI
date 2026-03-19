# Phase 06: Completion Summary

## Entry Gate

```bash
source .venv/bin/activate && devforgeai-validate phase-check ${RESEARCH_ID} --workflow=research --from=05 --to=06 --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Proceed to Phase 06 |
| 127 | CLI not installed - proceed without enforcement |
| Other | HALT - Phase 05 not complete |

## Contract

- **PURPOSE:** Validate workflow completion and display comprehensive research summary
- **REQUIRED SUBAGENTS:** none
- **REQUIRED REFERENCES:** none (self-contained)
- **REQUIRED ARTIFACTS:** All checkpoint data from Phases 01-05
- **STEP COUNT:** 2 mandatory steps

---

## Mandatory Steps (2)

### Step 6.1: Workflow Completion Validation

**EXECUTE:**
```
# Read current checkpoint
Read(file_path=f"devforgeai/workflows/{RESEARCH_ID}-phase-state.json")

# Verify all phases completed
completed_phases = checkpoint.progress.phases_completed
expected_phases = ["01", "02", "03", "04", "05"]

missing_phases = [p for p in expected_phases if p not in completed_phases]

IF missing_phases:
  HALT -- f"WORKFLOW INCOMPLETE - Missing phases: {missing_phases}"

# Verify research document exists on disk
research_file_check = Glob(pattern=f"devforgeai/specs/research/{RESEARCH_ID}-*.research.md")
IF not research_file_check:
  HALT -- f"Research document not found on disk for {RESEARCH_ID}"

# Verify index was updated
index_check = Grep(
  pattern=RESEARCH_ID,
  path="devforgeai/specs/research/research-index.md",
  output_mode="count"
)
IF index_check == 0:
  Display: f"WARNING: {RESEARCH_ID} not found in research index"

Display: "Workflow completion validation passed - all 5 phases completed"
```

**VERIFY:**
All 5 phases (01-05) appear in `completed_phases`. Research document exists on disk.

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${RESEARCH_ID} --workflow=research --phase=06 --step=6.1 --project-root=. 2>&1
```
Update checkpoint: `phases["06"].steps_completed.append("6.1")`

---

### Step 6.2: Display Summary

**EXECUTE:**
```
# Gather all data from checkpoint
research_file_path = checkpoint.output.research_file_path
assets_folder = checkpoint.output.assets_folder
epics_linked = checkpoint.output.epics_linked
adr_created = checkpoint.output.adr_created
topic = checkpoint.input.topic
category_code = checkpoint.input.category
questions = checkpoint.input.questions

# Calculate review date
review_date = (today + 180 days).isoformat()

Display: f"""
------------------------------------------------------------
  Research Completed
------------------------------------------------------------

Research Details:
  ID:        {RESEARCH_ID}
  Title:     {topic}
  Category:  {category_code}
  Status:    complete
  Created:   {created_date}
  Review By: {review_date}

Content Summary:
  Research Questions: {len(questions)}
  Key Findings:      {len(findings)}
  Recommendations:   {len(recommendations)}
  Sources:           {len(sources)}

Files Created:
  {research_file_path}
  {assets_folder} (for attachments)

{IF epics_linked:
Related Epics/Stories:
  {', '.join(epics_linked)}
}

{IF adr_created == 'pending':
ADR Creation: Pending - run /create-epic --adr to create
}

Next Steps:
  1. Review research document for accuracy
  2. Add screenshots/diagrams to assets folder if needed
  3. {IF adr_created == 'pending': Create ADR for technology decisions}
  4. Create stories for actionable recommendations if needed
  5. Research will be flagged for review on: {review_date}

Quick Access Commands:
  /research --resume {RESEARCH_ID}                    # Update this research
  /research --search "{topic.split()[0]}"             # Find related research
  /research --list --category {category_code}         # Browse category

------------------------------------------------------------
"""
```

**VERIFY:**
Summary was displayed to user.

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${RESEARCH_ID} --workflow=research --phase=06 --step=6.2 --project-root=. 2>&1
```

---

## Exit Gate

```bash
source .venv/bin/activate && devforgeai-validate phase-complete ${RESEARCH_ID} --workflow=research --phase=06 --checkpoint-passed --project-root=. 2>&1
```

Update checkpoint:
- `phases["06"].status = "completed"`
- `progress.phases_completed.append("06")`
- `progress.current_phase = 7`  (workflow complete)
- `progress.total_steps_completed += 2`
- `status = "completed"`

Write final checkpoint to disk. Verify via `Glob()`.

Display: "Research workflow complete. All 6 phases executed successfully."

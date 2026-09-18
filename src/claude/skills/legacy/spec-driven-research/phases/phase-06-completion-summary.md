# Phase 06: Completion Summary

## Entry Gate

```bash
devforgeai-validate phase-check ${RESEARCH_ID} --workflow=research --from=05 --to=06 --project-root=. 2>&1
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
- **REQUIRED ARTIFACTS:** CLI research phase-state (phases 01-05 via `phase-status`) + the research document
- **STEP COUNT:** 2 mandatory steps

---

## Reference Loading [MANDATORY]

```
# No required references for this phase. Self-contained — validates completion
# from the CLI-managed research state via `phase-status --workflow=research --format=json`,
# verifies disk existence of the research document via Glob, and Grep-counts
# the index. No skill or context references are loaded.
```

---

## Mandatory Steps (2)

### Step 6.1: Workflow Completion Validation

**EXECUTE:**
```
# Validate completion from the CLI-managed research state — the single source of truth.
status_json = run: devforgeai-validate phase-status ${RESEARCH_ID} --workflow=research --project-root=. --format=json
# Parse status_json.phases; require each of phases 01-05 to be present AND
#   status == "completed" AND checkpoint_passed == true.
expected_phases = ["01", "02", "03", "04", "05"]
incomplete = [
  p for p in expected_phases
  if p not in status_json["phases"]
     or status_json["phases"][p]["status"] != "completed"
     or status_json["phases"][p]["checkpoint_passed"] != true
]

IF incomplete:
  HALT -- f"WORKFLOW INCOMPLETE - phases not completed+checkpoint-passed: {incomplete}"

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

Display: "Workflow completion validation passed - all 5 phases completed (status=completed, checkpoint_passed=true)"
```

**VERIFY:**
For each of phases 01-05, the CLI `phase-status --workflow=research --format=json` output reports `status == "completed"` AND `checkpoint_passed == true`. Research document exists on disk.

**RECORD:**
```bash
devforgeai-validate phase-record ${RESEARCH_ID} --workflow=research --phase=06 --step=6.1 --project-root=. 2>&1
```

---

### Step 6.2: Display Summary

**EXECUTE:**
```
# Derive all display data from the research document + filesystem (NOT a hand-maintained checkpoint).
research_file_path = Glob(pattern=f"devforgeai/specs/research/{RESEARCH_ID}-*.research.md")[0]
Read(file_path=research_file_path)   # parse its YAML frontmatter + section content
topic         = frontmatter.title
category_code = frontmatter.category
created_date  = frontmatter.created
review_date   = frontmatter.review_by          # frontmatter already stores created + 180 days
epics_linked  = frontmatter.related_epics + frontmatter.related_stories
assets_folder = f"devforgeai/specs/research/{RESEARCH_ID}/"
# Counts come from the research document body (Research Questions / Key Findings /
# Recommendations sections) and the frontmatter sources_count.
questions       = the Research Questions listed in the document
findings        = the Key Findings listed in the document
recommendations = the Recommendations listed in the document
sources         = frontmatter.sources_count

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

Next Steps:
  1. Review research document for accuracy
  2. Add screenshots/diagrams to assets folder if needed
  3. If this research recommends adopting new technology, create an ADR via /create-system-architecture (referencing {RESEARCH_ID})
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
devforgeai-validate phase-record ${RESEARCH_ID} --workflow=research --phase=06 --step=6.2 --project-root=. 2>&1
```

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${RESEARCH_ID} --workflow=research --phase=06 --checkpoint-passed --project-root=. 2>&1
```

`phase-complete` records phase 06 completion in the CLI-managed research state — no separate checkpoint file is written.

Display: "Research workflow complete. All 6 phases executed successfully."

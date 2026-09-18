# Phase 07: DoD Update

## Entry Gate

```bash
devforgeai-validate phase-check ${STORY_ID} --from=06 --to=07
# Exit 0: proceed | Exit 1: Phase 06 incomplete
```

## Contract

PURPOSE: Update the story file's Definition of Done section, Implementation Notes, and workflow status to reflect completed work.
REQUIRED SUBAGENTS: None (file operations only)
REQUIRED ARTIFACTS: None
STEP COUNT: 2 mandatory steps

**FORMAT CONVENTION:** Keep `## Implementation Notes` as a flat list — avoid `###` subsections — for consistency with the `complete_dod` writer and the `diagnose-dod-failure` check. The validator parser no longer truncates at `###` (fixed via #787), so nested items are not lost; flat list is a convention, not a parser limit. (Reference: `.claude/rules/workflow/commit-failure-recovery.md`)

## Reference Loading [MANDATORY]

```
# No required references for this phase. Self-contained — operates on the
# story file (dynamic-path) via complete-dod CLI; error-recovery Read of
# .claude/rules/workflow/commit-failure-recovery.md sits outside the 4
# declared categories (skill ref / context file / memory / story).
```

---

## Mandatory Steps

### Step 1: Complete DoD (marks items, populates Implementation Notes, validates, updates status)

EXECUTE: Run the complete-dod CLI command which replaces the previous 5 manual steps:
1. Marks all non-deferred DoD `- [ ]` items as `- [x]`
2. Adds items to `## Implementation Notes` as FLAT LIST (no ### subsections)
3. Runs `validate-dod` internally (exit 0 required)
4. Updates `status: In Development` to `status: Dev Complete`
```bash
devforgeai-validate complete-dod --story=${STORY_ID} --story-file=${STORY_FILE} --project-root=${PROJECT_ROOT}
```
VERIFY: Exit code 0 = DoD completed and validated.
```
IF exit code == 1:
  Read(file_path=".claude/rules/workflow/commit-failure-recovery.md")
  # Follow recovery workflow to fix format
  HALT if cannot achieve exit code 0.
IF exit code == 2: HALT — "DoD completion error (file not found or parse error)."
```

### Step 2: Generate TDD Workflow Summary Table

EXECUTE: Generate workflow summary from phase-state.json.
```bash
devforgeai-validate generate-workflow-table --story=${STORY_ID} --project-root=${PROJECT_ROOT}
```
VERIFY: Exit code 0 = table generated. Append to story file Implementation Notes if tables are empty.

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --phase=07 --checkpoint-passed
# Exit 0: proceed to Phase 08 | Exit 1: DoD format invalid
```

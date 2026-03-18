# Phase G10: Completion Summary

## Entry Gate

```bash
devforgeai-validate phase-check ${SESSION_ID} --from=G09 --to=G10 --workflow=doc-gen
# Exit 0: proceed | Exit 1: Phase G09 incomplete
```

## Contract

PURPOSE: Display comprehensive summary report with all updated files, coverage metrics, and next steps. Finalize session.
REQUIRED SUBAGENTS: (none)
REQUIRED ARTIFACTS: Summary report displayed, session finalized
STEP COUNT: 2 mandatory steps

---

## Mandatory Steps

### Step G10.1: Display Completion Summary

EXECUTE: Generate and display the final summary report.
```
Display: ""
Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Display: "  Documentation Generation Complete"
Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Display: ""
Display: "Session: {SESSION_ID}"
Display: "Mode: {$MODE}"
IF $STORY_ID:
    Display: "Story: {$STORY_ID}"
Display: ""

Display: "Updated Sections ({module_name}):"
FOR each doc_type in updated_files:
    Display: "  + {doc_type}: {updated_files[doc_type]} ({word_counts[doc_type]} words)"
FOR each skipped_type in skipped_types:
    Display: "  - {skipped_type}: skipped (no content for this module)"

Display: ""
Display: "Documentation Coverage: {coverage}%"
IF coverage >= 80:
    Display: "  Meets quality gate threshold (>= 80%)"
ELSE:
    Display: "  Below threshold (>= 80% required for release)"

IF $STORY_ID:
    Display: ""
    Display: "Also updated:"
    Display: "  README.md (module blurb)"
    Display: "  CHANGELOG.md ([Unreleased] > Added)"
    Display: "  {story_file} (Change Log table)"

IF $EXPORT_FORMAT != "markdown":
    Display: ""
    Display: "Exported: {$EXPORT_FORMAT} format"

Display: ""
Display: "Next Steps:"
Display: "  - Review generated documentation for accuracy"
IF $STORY_ID:
    Display: "  - Run /qa {$STORY_ID} to validate story"
Display: "  - Update documentation with project-specific details"
Display: "  - Run /document --audit=dryrun to score documentation quality"
Display: ""
Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```
VERIFY: Summary report displayed with all sections (files, coverage, next steps).
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=G10 --step=G10.1 --workflow=doc-gen`

---

### Step G10.2: Finalize Session

EXECUTE: Mark session as complete in checkpoint and validate phase count.
```
# Update checkpoint
checkpoint = Read(file_path="devforgeai/workflows/${SESSION_ID}-checkpoint.json")
checkpoint.current_phase = "COMPLETE"
checkpoint.completed_at = current_timestamp
checkpoint.phases_completed.append("G10")
checkpoint.result = "SUCCESS"

Write(file_path="devforgeai/workflows/${SESSION_ID}-checkpoint.json", content=JSON(checkpoint))

# Validate all phases completed
completed_count = len(checkpoint.phases_completed)
EXPECTED_COUNT = 10  # 01, 02, G03-G10

IF completed_count < EXPECTED_COUNT:
    Display: "WARNING: Only {completed_count}/{EXPECTED_COUNT} phases completed"
ELSE:
    Display: "All {EXPECTED_COUNT} phases completed - Generation workflow passed"
```
VERIFY: Checkpoint file shows result = "SUCCESS" and COMPLETE status.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=G10 --step=G10.2 --workflow=doc-gen`

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --phase=G10 --checkpoint-passed --workflow=doc-gen
```

## Phase Transition Display

```
Display: ""
Display: "Documentation generation workflow complete."
Display: ""
```

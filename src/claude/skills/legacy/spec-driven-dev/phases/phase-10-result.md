# Phase 10: Result Interpretation

## Entry Gate

```bash
devforgeai-validate phase-check ${STORY_ID} --from=09 --to=10
# Exit 0: proceed | Exit 1: Phase 09 incomplete
```

## Contract

PURPOSE: Generate a structured result summary and return it to the invoking command for display.
REQUIRED SUBAGENTS: dev-result-interpreter
REQUIRED ARTIFACTS: None (returns result object)
STEP COUNT: 4 mandatory steps

## Reference Loading [MANDATORY]

```
# No required references for this phase. Self-contained — delegates to
# dev-result-interpreter subagent; no static skill reference, context
# file, memory entry, or story Read in mandatory steps.
```

---

## Mandatory Steps

### Step 0: Append Dev Cycle to Iteration Log (Non-Blocking)

EXECUTE: Record the completed dev cycle in the iteration log. This step is **non-blocking** — if the CLI fails, log a WARNING and continue. Never HALT on iteration log failure.
```bash
devforgeai-validate iteration-log-append-dev ${STORY_ID} \
  --mode=${MODE} \
  --approach=${APPROACH} \
  --commit=${COMMIT_HASH} \
  --tags=${TAGS} \
  --files=${FILES} \
  --project-root=.
```
VERIFY: If exit code != 0, display: "WARNING: Iteration log append-dev failed — continuing workflow."
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=10 --step=0`

---

### Step 1: Invoke Dev Result Interpreter

EXECUTE: Delegate result interpretation to specialist subagent.
```
Task(
  subagent_type="dev-result-interpreter",
  prompt="Interpret development workflow results for ${STORY_ID}.
  Story file: ${STORY_FILE}
  Also read devforgeai/feedback/ai-analysis/${STORY_ID}/consolidated-analysis.json if it exists. Include top 3 findings in the display template under a 'Framework Insights' section. If the file does not exist, omit this section.

  Task:
  1. Read story file and extract:
     - Current status
     - TDD phases completed
     - Test results (passing count, coverage %)
     - DoD completion status
     - Deferred items (if any)

  2. Determine overall result:
     - SUCCESS: status='Dev Complete', all tests passing
     - INCOMPLETE: status='In Development', some work remaining
     - FAILURE: workflow error

  3. Generate display template appropriate for result type

  4. Provide next step recommendations

  5. Check devforgeai/feedback/ai-analysis/aggregated/recommendations-queue.json for HIGH-priority items. If any exist, include in next_steps: 'N HIGH-priority framework improvement recommendations pending. Run /create-incident-from-queue --priority=high to convert them into GitHub issues.'

  Return structured JSON with:
  - status: 'success|incomplete|failure'
  - display.template: '...' (formatted display text)
  - display.next_steps: [...] (actionable recommendations)
  - story_status: '...'
  - tdd_phases_completed: [...]
  - workflow_summary: '...'"
)
```
VERIFY: Task result returned with structured JSON.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=10 --subagent=dev-result-interpreter`

### Step 2: Receive Structured Result

EXECUTE: Parse the dev-result-interpreter output.
```
# Extract:
# - result.status (success/incomplete/failure)
# - result.display.template (formatted display text)
# - result.display.next_steps (array of recommendations)
```
VERIFY: Result contains required fields (status, display.template, display.next_steps).

### Step 2.5: Close Remediation Cycle (Sprint 5, conditional)

This step runs ONLY when `$REMEDIATION_MODE == true AND $REMEDIATION_SOURCE == "qa-recommendations"`. In normal mode, skip to Step 3.

EXECUTE (conditional):
```
IF $REMEDIATION_MODE == true AND $REMEDIATION_SOURCE == "qa-recommendations":
    Display: "Closing remediation cycle ${CURRENT_CYCLE}..."

    # (a) Close the cycle in phase-state.json cycles[] array
    EXECUTE: devforgeai-validate phase-cycle-close \
        --story-id=${STORY_ID} \
        --cycle=${CURRENT_CYCLE} \
        --findings-closed="$(comma-join $CLOSED_REC_IDS)" \
        --completed-phase=10 \
        --project-root=${PROJECT_ROOT} \
        --format=json

    VERIFY: Exit 0 = cycle closed. Capture completed timestamp.
    IF exit 1: HALT with error verbatim.
    IF exit 2: HALT with IO error verbatim.

    # (b) Update qa-recommendations.md to reflect closures (only when >0 closed)
    IF len($CLOSED_REC_IDS) > 0:
        EXECUTE: devforgeai-validate mark-recommendations-closed \
            --story-id=${STORY_ID} \
            --rec-ids="$(comma-join $CLOSED_REC_IDS)" \
            --cycle=${CURRENT_CYCLE} \
            --project-root=${PROJECT_ROOT} \
            --format=json

        VERIFY: Exit 0.
        IF exit 1: HALT with error verbatim.
        IF exit 2: HALT with IO error verbatim.

    Display: ""
    Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    Display: "  Cycle ${CURRENT_CYCLE} closed"
    Display: "  Closed: ${len($CLOSED_REC_IDS)} recommendations"
    Display: "  Failed: ${len($FAILED_REC_IDS)} (remain open for next cycle)"
    Display: ""
    Display: "  Next: Run /qa ${STORY_ID} to validate and regenerate"
    Display: "        qa-recommendations.md (cycle ${CURRENT_CYCLE} + 1)."
    Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=10 --step=2.5 --project-root=${PROJECT_ROOT}`
```

### Step 3: Return Result to Command

EXECUTE: Set the skill's return value for the invoking command to display.
```
# The skill returns result.display.template
# The command (/dev) displays it to the user
# No additional processing — command shows result as-is
```
VERIFY: Result object prepared for return.

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --phase=10 --checkpoint-passed
# Exit 0: workflow complete | Exit 1: result interpretation failed

# After Phase 10 completion:
devforgeai-validate phase-archive ${STORY_ID}
# Moves state file to devforgeai/workflows/completed/
```

## Workflow Complete

All 10 phases completed. The skill returns the structured result to the invoking command.

## Hook-backed OUT-Attestation

This phase has Phase-D dispatch entries in `subagent_out_attestation_registry.json`. When dispatching those named subagents, instruct them to return a `subagent-result-v1` result that includes `coverage_attestation` in the normal response. Phase completion is blocked by `subagent-out-attestation-gate.sh` when the hook-owned ledger line lacks `coverage_attestation_present:true`. This Phase-D path is OUT-attestation-only and does not require `tmp/<WORK_ID>/handoffs/`.

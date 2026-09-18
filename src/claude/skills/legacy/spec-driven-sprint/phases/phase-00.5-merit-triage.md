# Phase 00.5: Merit + Recurrence Triage

## Entry Gate

```bash
devforgeai-validate phase-check ${ISSUE_ID} --workflow=spec-sprint --from=00 --to=00.5 --project-root=${PROJECT_ROOT}
# Exit 0: proceed | Exit != 0: Phase 00 incomplete -> HALT
```

Boundary note: deterministic checks produce structural inputs only. Zero or low recurrence is neutral input and never a basis for `DUPLICATE` or `REJECT`; close-action verdicts require a manual approval gate.

## Contract

PURPOSE: Display recurrence signals, duplicate candidates, ADR-conflict candidates, context contradiction candidates, bug-validity inputs, and enhancement cost vs value inputs before dashboard/materialization work begins.
DELEGATES TO: none.
GATE: The Phase 00.5 verdict set is exactly `["PROCEED", "DUPLICATE", "REJECT", "NEEDS-INFO", "INCONCLUSIVE"]`.

`DUPLICATE` and `REJECT` are close-action verdicts. They require `AskUserQuestion` approval and a grounded closeout/update plan before any outward GitHub action. No issue-close command may run in Phase 00.5.

`NEEDS-INFO` may halt and ask the user for the missing requirement; it is not a close-action mutation.

---

## Mandatory Steps

### Step 1: Count marked recurrence comments

EXECUTE: Count only comments containing the exact marker `<!-- recurrence -->`:

```bash
devforgeai-validate incident-recurrence comment-count ${ISSUE_NUMBER} --repo ${REPO_SLUG} > tmp/${ISSUE_ID}/recurrence-count.json
```

If a fixture was already captured, add `--comments-json tmp/${ISSUE_ID}/comments.json` before the output redirect.
VERIFY: The JSON has `schema == "incident-recurrence-comment-count-v1"` and `zero_never_rejects == true`.

### Step 2: Build deterministic merit-triage inputs

EXECUTE: Build `tmp/${ISSUE_ID}/phase-00.5-merit-triage.json`:

```bash
devforgeai-validate spec-sprint-merit-triage ${ISSUE_ID} \
  --issue-json tmp/${ISSUE_ID}/issue.json \
  --recurrence-json tmp/${ISSUE_ID}/recurrence-count.json \
  --project-root=${PROJECT_ROOT}
```

If a duplicate scan fixture exists, include it:

```bash
devforgeai-validate spec-sprint-merit-triage ${ISSUE_ID} \
  --issue-json tmp/${ISSUE_ID}/issue.json \
  --recurrence-json tmp/${ISSUE_ID}/recurrence-count.json \
  --dup-scan-json tmp/${ISSUE_ID}/dup-scan.json \
  --project-root=${PROJECT_ROOT}
```

VERIFY: The JSON has `schema == "spec-sprint-merit-triage-v1"` and includes these deterministic structural inputs:
- recurrence count and recurrence breadth.
- duplicate candidates from the optional duplicate scan.
- ADR-conflict candidates from deterministic text matching under `devforgeai/specs/adrs/`.
- context contradiction candidates from deterministic text matching under `devforgeai/specs/context/`.
- bug-validity inputs for bug-labeled issues.
- enhancement cost vs value inputs for enhancement-labeled issues.

### Step 3: Separate structural inputs from semantic judgment

EXECUTE: Review `tmp/${ISSUE_ID}/phase-00.5-merit-triage.json`. Its shape is:

```json
{
  "issue_id": "${ISSUE_ID}",
  "allowed_verdicts": ["PROCEED", "DUPLICATE", "REJECT", "NEEDS-INFO", "INCONCLUSIVE"],
  "structural_inputs": {
    "issue_state": "<OPEN|CLOSED|UNKNOWN>",
    "issue_kind": "<bug|enhancement|other>",
    "recurrence_count": 0,
    "recurrence_breadth": 0,
    "zero_never_rejects": true,
    "has_body": true,
    "has_acceptance_criteria_or_clear_request": true,
    "adr_conflict_candidates": [],
    "context_contradiction_candidates": [],
    "duplicate_candidates": [],
    "bug_validity": {"status": "NOT_APPLICABLE", "evidence": []},
    "enhancement_cost_value": {"status": "SUPPORTED", "evidence": []}
  },
  "semantic_judgment": {
    "verdict": "PROCEED",
    "rationale": "<one grounded sentence>"
  },
  "close_action_gate": {
    "required": false,
    "gate": null,
    "issue_mutation_allowed": false
  }
}
```

Structural inputs are deterministic facts. Semantic judgment is a bounded orchestration decision; cite the exact issue text, prior issue, ADR, or context file that supports it. Hooks can verify command execution and artifact shape; they cannot prove semantic readiness.

VERIFY:
- `verdict` is exactly one of `PROCEED`, `DUPLICATE`, `REJECT`, `NEEDS-INFO`, `INCONCLUSIVE`.
- Zero or low recurrence is neutral structural input and cannot determine the verdict by itself.
- `NEEDS-INFO` includes the specific missing requirement in `rationale`.
- `DUPLICATE` cites the exact duplicate issue/PR candidate and has `close_action_gate.required == true`.
- `REJECT` cites the exact invalidity or value/cost evidence and has `close_action_gate.required == true`.

### Step 4: Route the verdict

EXECUTE:
- `PROCEED` or `INCONCLUSIVE`: continue. `INCONCLUSIVE` means Phase 01 must resolve the uncertainty during grounded research.
- `NEEDS-INFO`: HALT and AskUserQuestion for the missing requirement before continuing.
- `DUPLICATE`: HALT and AskUserQuestion with the exact duplicate evidence and proposed issue comment. Continue only after approval for the outward GitHub action.
- `REJECT`: HALT and AskUserQuestion with the exact decline evidence and proposed issue comment. Continue only after approval for the outward GitHub action.

VERIFY: No issue mutation occurred during Phase 00.5 triage.

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${ISSUE_ID} --workflow=spec-sprint --phase=00.5 --checkpoint-passed --project-root=${PROJECT_ROOT}
# Exit 0: proceed to Phase 01 | Exit != 0: HALT
```

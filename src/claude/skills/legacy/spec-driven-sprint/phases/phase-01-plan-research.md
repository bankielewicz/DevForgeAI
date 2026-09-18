# Phase 01: Plan-Mode + Research

## Entry Gate

```bash
devforgeai-validate phase-check ${ISSUE_ID} --workflow=spec-sprint --from=00.5 --to=01 --project-root=${PROJECT_ROOT}
# Exit 0: proceed | Exit != 0: Phase 00.5 incomplete → HALT
```

## Contract

PURPOSE: Enter plan mode, read the issue, produce a GROUNDED fix-surface, decompose into work cards, author the plan file, and get user approval via ExitPlanMode before any worktree mutation.
DELEGATES TO: none (orchestrator research); OPTIONAL `architect-reviewer` (review card decomposition for non-trivial issues — Step 8).
GATE: HALT if the issue is ambiguous or the fix surface is unverifiable. **User approval (ExitPlanMode, Step 9)** must occur before the exit gate.

---

## Mandatory Steps

### Step 1: Enter plan mode

EXECUTE: `EnterPlanMode` (programmatic — this is the command's step, not an assumption). All Phase 01 research and design happen inside plan mode; no working-tree mutation until ExitPlanMode (Step 9) and the worktree (Phase 03).
VERIFY: Plan mode is active.

### Step 2: Read the issue

EXECUTE: `gh issue view ${ISSUE_NUMBER} --repo <org>/<repo> --json number,title,body,labels,state` (the repo detected in Phase 00; the structured `--json` form avoids deprecated-field GraphQL errors the bare form triggers). Capture title, body, and labels from the JSON, plus any linked code references.
VERIFY: Issue fetched (exit 0) → proceed. If `gh` is unavailable or the error says the issue is not found → HALT → AskUserQuestion. Any OTHER non-zero exit (e.g., deprecated-field GraphQL errors) → retry with the structured `--json` form above / a narrower field list before HALTing.

EXECUTE: Extract the source issue acceptance criteria into `tmp/${ISSUE_ID}/source-acs.json` as `{"acceptance_criteria":[{"id":"AC1","text":"..."}]}`. If the issue has no formal AC headings, derive the smallest set of actionable source requests from the issue body/title and mark them `AC1`, `AC2`, ... without inventing scope.
VERIFY: `tmp/${ISSUE_ID}/source-acs.json` exists and every entry has non-empty `id` and `text`. Phase 04 card ACs must reference these ids with `source_refs`; Phase 05 enforces coverage with `verify-source-ac-coverage`.

### Step 3: Ground the fix surface

EXECUTE: For every file/symbol the issue references, `Read`/`Grep` it in the repo to confirm it exists and the fix is feasible. Classify each finding **GROUNDED** (cited file:line), **DERIVED** (one-sentence justification), or **INCONCLUSIVE** (flag — do not guess). See `.claude/rules/core/epistemic-integrity.md`.
VERIFY: At least one GROUNDED fix-surface citation exists. If the fix surface cannot be verified → HALT → AskUserQuestion (do not fabricate a plan).

### Step 3a (conditional): Declare fresh already-fixed closeout

EXECUTE: If Phase 01 research proves the issue is already fixed by a merged PR and no implementation work remains, declare closeout through the CLI instead of fabricating a Phase 04 work card:

```bash
devforgeai-validate phase-set-closeout ${ISSUE_ID} --workflow=spec-sprint --reason=already-fixed --evidence-pr <merged-pr-number-or-url> --repo <org>/<repo> --project-root=${PROJECT_ROOT}
```

Use only a merged GitHub PR as evidence. The command runs `gh pr view`, stores the PR number/title/state/merged timestamp/URL in phase state, records `04.closeout`, and writes `evidence_sha256` over the exact evidence payload. Do not hand-edit `phase_04_mode` or `phase_04_closeout`; Phase 04 completion rejects closeout mode unless the state contains `04.closeout`, merged PR evidence, and a matching evidence hash.
VERIFY: The phase-state file contains `phase_04_mode == "closeout"`, `phase_04_closeout.evidence.state == "MERGED"`, a non-empty `phase_04_closeout.evidence.merged_at`, and `phase_04_closeout.evidence_sha256`. The plan file must name the merged PR and state that Phase 04 will complete through closeout mode, not TDD evidence.

### Step 4: Classify the issue type → branch prefix

EXECUTE: Set `$ISSUE_TYPE` ∈ {`feat`, `fix`, `chore`} from the issue's labels/intent. This drives the Phase 03 branch prefix (`<type>/<issue-slug>`).
VERIFY: `$ISSUE_TYPE` is set.

### Step 5: Draft the Goal

EXECUTE: Draft the sprint **Goal** (one paragraph) that the work cards must serve — grounded in the issue + the fix surface. This becomes the dashboard's Goal section in Phase 03.
VERIFY: The Goal is concrete and maps to the GROUNDED fix surface.

### Step 6: Decompose into work cards

EXECUTE: From the GROUNDED fix surface (Step 3) and Goal (Step 5), author a variable-N list of work cards. Each card carries: mission, files-to-touch, acceptance criteria (testable), and an in-flight verification (the named deterministic signal — exact command + expected exit, and/or the AC list a fresh verifier checks). For CODE cards, the acceptance includes the test that must pass.
VERIFY: Every card maps to the Goal and to a GROUNDED fix-surface citation.

### Step 7: Author the test plan, worktree/branch/PR commands, and HTML-spec outline

EXECUTE: To the plan-mode plan file, add: the test plan (which suite/runner per card), the worktree + branch (`<type>/<issue-slug>`) + PR commands, and the HTML-spec content outline (the GLOBAL fills + one card per work item).
VERIFY: The plan file is self-contained (survives a context clear).

### Step 8 (conditional): Review the decomposition

EXECUTE (non-trivial issues): build the registry-protected Phase 01 handoff for
`architect-reviewer`, then dispatch the review.

```bash
mkdir -p tmp/${ISSUE_ID}
: > tmp/${ISSUE_ID}/spec-sprint-phase01-architect-reviewer-handoff-changed-files.txt

HANDOFF_OUTPUT_ARCHITECT_REVIEWER=$(devforgeai-validate build-subagent-handoff ${ISSUE_ID} \
  --workflow=spec-sprint \
  --phase=01 \
  --subagent=architect-reviewer \
  --changed-files-file=tmp/${ISSUE_ID}/spec-sprint-phase01-architect-reviewer-handoff-changed-files.txt \
  --project-root=${PROJECT_ROOT} 2>&1)
HANDOFF_PATH_ARCHITECT_REVIEWER=$(echo "$HANDOFF_OUTPUT_ARCHITECT_REVIEWER" | jq -r '.handoff_md_path')
```

VERIFY before dispatch:
- `$HANDOFF_PATH_ARCHITECT_REVIEWER` is non-empty and exists.
- `tmp/${ISSUE_ID}/handoffs/phase-01-architect-reviewer-handoff.manifest.json` exists.
- The manifest has `context_pack.coverage_matrix == {}` and `unresolved == []`.

Dispatch:

```
Task(
  subagent_type="architect-reviewer",
  prompt="Handoff: ${HANDOFF_PATH_ARCHITECT_REVIEWER}
    Read the handoff first. Use its context_pack.coverage_matrix and
    role-domain rules as the context source. If a required domain or artifact is
    absent, return H-CONTEXT-MISS and stop.

    Review the work-card decomposition for ${ISSUE_ID}. Verify completeness,
    sequencing, and that every card maps to the grounded fix surface and source
    acceptance criteria. Return findings with severity and exact evidence.
    Include a subagent-result-v1 coverage_attestation with
    context_pack_path='${HANDOFF_PATH_ARCHITECT_REVIEWER}',
    context_pack_consumed=true, and context_miss=[]."
)
```
VERIFY: Findings folded in or explicitly dismissed.
RECORD: `devforgeai-validate phase-record ${ISSUE_ID} --workflow=spec-sprint --phase=01 --subagent=architect-reviewer --project-root=${PROJECT_ROOT}`

### Step 9: ExitPlanMode → user approval

EXECUTE: `ExitPlanMode` presenting the design. The user approves or requests changes.
VERIFY: User approved. If not → revise and re-present (do not proceed unapproved).

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${ISSUE_ID} --workflow=spec-sprint --phase=01 --checkpoint-passed --project-root=${PROJECT_ROOT}
# Runs after user approval (ExitPlanMode). Exit 0: proceed to Phase 03 | Exit != 0: HALT
```

# Phase 05: QA vs Spec (gated completion)

## Entry Gate

```bash
devforgeai-validate phase-check ${ISSUE_ID} --workflow=spec-sprint --from=04 --to=05 --project-root=${PROJECT_ROOT}
# Exit 0: proceed | Exit != 0: Phase 04 incomplete → HALT
```

## Contract

PURPOSE: Validate the implementation against the spec's acceptance criteria with a deterministic test gate AND a disinterested fresh-verifier AC verdict, then complete phase 05 — the one gated boundary of this workflow.
GATE-ENFORCED: `ac-compliance-verifier` (Gate 2, `overall_status=PASS`), `anti-pattern-scanner` (Gate 3, `overall_status∈{PASS,NOT_APPLICABLE}`), `coverage-analyzer` (Gate 4, same). All three verdicts are REQUIRED and sha256-anchored by `spec-sprint-completion-gate.sh` before `phase-complete --phase=05` exits 0.
GATE: **completeness gate** — any AC unmet/INCONCLUSIVE or any Critical/High violation → back-edge to Phase 04. Forward only when every spec AC GROUNDED-passes. The `phase-complete --phase=05` call is hook-enforced by `spec-sprint-completion-gate.sh`.

---

## ⚠ HARD WIRING CONTRACT — emit in EXACTLY this order

`spec-sprint-completion-gate.sh` blocks `phase-complete --phase=05` unless the gate
artifacts (test-result, executable-AC transcript evidence where applicable, source-AC
coverage, AC-verdict, anti-pattern scan, coverage analysis) exist, pass,
AND are sha256-anchored in `.conviction-evidence.jsonl`. Anchoring happens at
`phase-record` time for phase artifacts and at `capture-ac-evidence` time for executable
AC transcripts. **Miss any required anchor — or emit it after `phase-complete` — and the
gate is closed.**
Steps 1→2→2a→3→3-pre→3a→3b→4→5 below are ordered.

## Mandatory Steps

### Step 0: Verify Phase 04 custody baseline

EXECUTE: Before running QA, read `tmp/${ISSUE_ID}/phase-04-commits.json` and verify every work card has Red and Green custody commits, plus Refactor/Integration commits when those subagents were dispatched. Use the recorded SHAs as the QA baseline:
```bash
git -C ${WORKTREE_PATH} diff --name-status
git -C ${WORKTREE_PATH} diff --name-status <segment-commit>..<next-segment-commit>
```
VERIFY: The current worktree has no uncommitted changes before QA starts. If `git diff --name-status` shows a subagent-owned file changed after its recorded commit, HALT and route back through `devforgeai-validate phase-reset ${ISSUE_ID} --workflow=spec-sprint --to=04 --reason=remediation-cycle --project-root=${PROJECT_ROOT}`; re-dispatch the responsible subagent instead of patching files inline.

### Step 1: Run the deterministic test gate (LLM-proof)

EXECUTE:
```bash
devforgeai-validate run-tests ${ISSUE_ID} --phase=05 --record-result --path=${WORKTREE_PATH}/tests/${ISSUE_ID}/ --framework=${TEST_RUNNER} --project-root=${PROJECT_ROOT}
# Writes devforgeai/feedback/ai-analysis/${ISSUE_ID}/phase-05-run-tests.json with
# CLI-computed `passed` (the orchestrator cannot forge a pass for a failing suite).
```

Since #490 anchors all Phase-04 edits in the Phase-03 worktree, the sprint's tests live there under the incident's own number-dir (`${WORKTREE_PATH}/tests/${ISSUE_ID}/`) — using the `$WORKTREE_PATH` and `$ISSUE_ID` markers bound in Phase 03. A `worktrees/<id>/` test path (new site) is sanctioned for `run-tests` without any guard exception (the path contains no `.claude/` segment, so `pre-test-target-guard` quick-exits 0 at its `.claude/` check). Legacy `.claude/worktrees/<id>/` paths remain sanctioned via the gh#451 exception. If a card's Red-phase tests landed in existing suites or `.sh` harnesses (outside the number-dir), the aggregator suite authored in Phase 04 at `${WORKTREE_PATH}/tests/${ISSUE_ID}/` is the sanctioned mechanism for this sprint shape — `run-tests --path` targets that aggregator, which subprocess-runs the external harnesses and asserts their exit codes. Do NOT use the broad `${WORKTREE_PATH}/tests/` or a bare `run-tests` — both silently widen to the whole tests tree (#461) — and do NOT create a main-checkout bridge shim. `${TEST_RUNNER}` is the Phase-00 detected framework persisted by `phase-set-tech-stack` (`phase-00-init.md` Step 2); the flag is explicit because glob-order detection is non-deterministic across checkouts (#428).

VERIFY: Exit 0 AND the artifact's `passed == true`. If tests fail → return to Phase 04 (more TDD); do NOT proceed.

Note: documentation/prose-only sprints still produce a passing test artifact via the content-assertion test authored in Phase 04 Step 3 (see `phase-04-execute.md` Step 3 — Non-CODE card branch). No card type bypasses Gate 1 — a content-assertion test in `${WORKTREE_PATH}/tests/${ISSUE_ID}/` is the sanctioned path for non-code cards.

### Step 2: Anchor the test result (conviction)

EXECUTE:
```bash
devforgeai-validate phase-record ${ISSUE_ID} --workflow=spec-sprint --phase=05 --cli-command=run-tests --project-root=${PROJECT_ROOT}
# conviction-postrecord.sh sha256-anchors phase-05-run-tests.json into .conviction-evidence.jsonl.
```
VERIFY: Exit 0. The test-result artifact is now anchored (Gate 1 of the completion hook).

### Step 2a: Capture executable-AC evidence (for command-execution ACs)

`ac-compliance-verifier` is read-only (it cannot execute commands), so a spec AC whose verification is a command execution has no DIRECT evidence to verify unless a transcript is captured first. Capture it BEFORE the Step 3 dispatch.

EXECUTE: For each spec AC whose verification is a command execution (an exit-code or output assertion), capture the exact command through the CLI:

```bash
devforgeai-validate capture-ac-evidence --story=${ISSUE_ID} --ac=AC<N> --command='<exact AC command>' --expected-command='<exact AC command>' --project-root=${PROJECT_ROOT} --cwd=${WORKTREE_PATH}
# Writes tmp/${ISSUE_ID}/ac<N>-evidence.txt and sha256-anchors it in
# devforgeai/feedback/ai-analysis/${ISSUE_ID}/.conviction-evidence.jsonl.
```

The transcript contains, in order: the echoed exact command, full stdout/stderr, and a final line `exit code: <n>`. `--expected-command` makes command drift a hard error before execution.

**Self-developed `devforgeai-validate` subcommands:** When the AC command is a `devforgeai-validate <subcommand>` implemented in this repository, always capture the transcript through the wrapper by setting the `capture-ac-evidence` command to:

```bash
devforgeai-validate resolve-worktree-subcommand <name> --worktree=${WORKTREE_PATH} [<args>...]
```

This sets `PYTHONPATH` to the worktree's `src/claude/scripts` and invokes `python3 -m devforgeai_cli.cli <name>`. The subcommand's exit code is propagated and used as the transcript's final `exit code: <n>` line. Use the global binary only for commands that are not repo-owned `devforgeai-validate` subcommands.

VERIFY: Each transcript file exists under `tmp/${ISSUE_ID}/`, its anchor entry exists in `.conviction-evidence.jsonl`, the anchor's `executed_command` matches the AC command verbatim, and its final line is `exit code: <n>`. (If the spec has no command-execution ACs, this step is NOT_APPLICABLE — proceed to Step 3.)

### Step 3: Run the fresh-context AC verifier and persist its verdict

EXECUTE: `Task(subagent_type="ac-compliance-verifier", ...)` against the HTML spec's acceptance criteria (a disinterested verifier with no implementation stake). Pass the Step 2a transcript file paths (`tmp/ISSUE-<n>/ac<N>-evidence.txt`) in the verifier's Task prompt and state that a pre-captured transcript the verifier can `Read` qualifies as DIRECT/GROUNDED evidence for that executable AC. `ac-compliance-verifier` is read-only (no Bash tool); the orchestrator writes the verifier's returned substance payload directly to `tmp/${ISSUE_ID}/phase-05-ac-compliance-verifier.json`. The payload must preserve the verifier's top-level `overall_status` and include at least one non-empty substance container (`findings`, `evidence`, or `output`). Every entry in a `findings` container carries a `description` of at least 10 whitespace-delimited words — `_check_payload_content` routes each `findings[]` entry through `_check_word_count` (minimum 10) in `emit_conviction_worklog.py`, so an entry whose `description` is missing, empty, or shorter than 10 words exits 1 with `code=SUBSTANCE_VALIDATION_FAILED` and nothing is written. Entries in `evidence` and the `output` container carry no per-entry word-count requirement. Do not add `subagent_id`, `story_id`, `phase`, or `phase_state_checksum`; `emit-conviction-worklog` injects/computes those fields per Issue #813.

Persist the substance payload through the conviction chain:
```bash
devforgeai-validate emit-conviction-worklog --story ${ISSUE_ID} --phase 05 --subagent ac-compliance-verifier --content-file tmp/${ISSUE_ID}/phase-05-ac-compliance-verifier.json --project-root ${PROJECT_ROOT}
# overall_status ∈ {PASS, PARTIAL, FAIL}; PASS only when every AC GROUNDED-passes.
```
> **Payload contract (Issue #813):** the verdict file `tmp/${ISSUE_ID}/phase-05-ac-compliance-verifier.json` need only carry **substance** — at least one non-empty `findings`, `evidence`, or `output` container. `emit-conviction-worklog` **injects** `subagent_id`, `story_id`, and `phase` from its own `--subagent`/`--story`/`--phase` flags and **computes** `phase_state_checksum` as the sha256 of the resolved phase-state file, so the caller does NOT supply those four identity fields. A payload that explicitly carries one of them with a value that disagrees with the flags (or a `phase_state_checksum` that disagrees with the computed digest) is rejected with exit 1 `code=IDENTITY_MISMATCH` and nothing is written; a missing phase-state file exits 2 `code=PHASE_STATE_NOT_FOUND`. Within a `findings` container, each entry additionally carries a `description` of at least 10 whitespace-delimited words — `_check_payload_content` routes every `findings[]` entry through `_check_word_count` (minimum 10) in `emit_conviction_worklog.py`, so a `description` that is missing, empty, or shorter than 10 words is rejected with exit 1 `code=SUBSTANCE_VALIDATION_FAILED` and nothing is written; `evidence[]` entries and the `output` container carry no per-entry word-count requirement. The same contract applies to the `anti-pattern-scanner` and `coverage-analyzer` emit calls below.

VERIFY: The verdict file exists with `overall_status == PASS`. Route the two non-PASS causes distinctly: **(a) missing-evidence** — PARTIAL/INCONCLUSIVE caused SOLELY by missing execution evidence on executable ACs → capture the missing transcript(s) per Step 2a and re-dispatch the verifier (NO Phase 04 back-edge; the re-dispatched verdict must reach `overall_status == PASS`). The `emit-conviction-worklog` re-dispatch that overwrites `phase-05-ac-compliance-verifier.json` is permitted by `feedback-artifact-write-gate.sh` (ISSUE-579 carve-out: spec-sprint workflow active + filename match → exit 0); no `DEVFORGEAI_ALLOW_OPERATIONAL_EDIT=1` or Bash carve-out is required for this path. **(b) implementation-failure** — any AC failing on content/implementation grounds, or any Critical/High violation → **back-edge to Phase 04**. INCONCLUSIVE never satisfies the gate.

**Testable routing (Issue #819/#888):** ACs with `testable:true` are mechanically backed by Gate 1 (their AC id appears in a test contract's `covered_acs` with a passing `phase-05-run-tests.json`) or a Step 2a transcript captured by `capture-ac-evidence`, ending `exit code: 0`, sha256-anchored, and command-matched — Gate 1.5 (`devforgeai-validate validate-ac-mechanical-backing`) enforces this in `spec-sprint-completion-gate.sh` before `phase-complete --phase=05`. Gate 2 semantic verdict is therefore scoped to ACs with `testable:false` only — the irreducible LLM-verified boundary for genuinely subjective criteria. When all ACs in `ac-list-card*.json` are `testable:false`, Gate 1.5 exits 0 and the full semantic verdict remains the only gate.

**Source-AC routing (Issue #848):** every source issue AC captured in `tmp/${ISSUE_ID}/source-acs.json` must be covered by at least one work-card AC via `source_refs`/`source_ac_ids`, or explicitly listed in an `out_of_scope` entry with a non-empty rationale. Gate 1.6 (`devforgeai-validate verify-source-ac-coverage`) enforces this before `phase-complete --phase=05`.

### Step 3-pre: Classify worktree diff — source-code-changed predicate

EXECUTE:
```bash
devforgeai-validate source-code-changed ${ISSUE_ID} --worktree ${WORKTREE_PATH} --project-root ${PROJECT_ROOT} --format json
# Exits 0; parse source_code_changed from JSON output.
# When source_code_changed=false: NOT_APPLICABLE artifacts written to
#   tmp/${ISSUE_ID}/phase-05-anti-pattern-scanner.json and
#   tmp/${ISSUE_ID}/phase-05-coverage-analyzer.json by the CLI.
```
Parse `source_code_changed` from the JSON output.
VERIFY: Exit 0. Route:
- **`source_code_changed=true`** → proceed to Step 3a (dispatch scanner subagents as today).
- **`source_code_changed=false`** → skip the Task() dispatches in Steps 3a/3b; the CLI has already
  authored the NOT_APPLICABLE artifacts. Run the NOT_APPLICABLE anchor path below, then skip to Step 4.

**NOT_APPLICABLE anchor path (only when `source_code_changed=false`):**
Anchor with `--cli-command`, NOT `--subagent` — no scanner subagent was dispatched on this
branch, so a `--subagent` record would populate `subagents_invoked` with no matching Task() in
the dispatch ledger and `subagent-dispatch-reconcile.sh` would block `phase-complete --phase=05`
("unbacked subagent records"). `--cli-command` records to `cli_commands_invoked` instead — the
same anchoring path the test-result uses (Step 2, `--cli-command=run-tests`) — and
`conviction-postrecord.sh` still resolves the worklog to `phase-05-<name>.json` and sha256-anchors
it, so Gates 3/4 pass. (ISSUE-750 Finding B.)
```bash
devforgeai-validate emit-conviction-worklog --story ${ISSUE_ID} --phase 05 --subagent anti-pattern-scanner --content-file tmp/${ISSUE_ID}/phase-05-anti-pattern-scanner.json --project-root ${PROJECT_ROOT}
devforgeai-validate phase-record ${ISSUE_ID} --workflow=spec-sprint --phase=05 --cli-command=anti-pattern-scanner --project-root=${PROJECT_ROOT}
devforgeai-validate emit-conviction-worklog --story ${ISSUE_ID} --phase 05 --subagent coverage-analyzer --content-file tmp/${ISSUE_ID}/phase-05-coverage-analyzer.json --project-root ${PROJECT_ROOT}
devforgeai-validate phase-record ${ISSUE_ID} --workflow=spec-sprint --phase=05 --cli-command=coverage-analyzer --project-root=${PROJECT_ROOT}
```
VERIFY: Both artifact files exist with `overall_status=NOT_APPLICABLE`. All four CLI calls exit 0. Gates 3/4 of `spec-sprint-completion-gate.sh` will pass (sha256-anchored, correct status) AND `subagent-dispatch-reconcile.sh` does not block (`subagents_invoked` stays empty for the scanners).

### Step 3a: Run anti-pattern scanner, persist its verdict, and anchor (only when source_code_changed=true)

EXECUTE: `Task(subagent_type="anti-pattern-scanner", ...)` — tamper-evident, NOT LLM-proof. Write the scanner's returned substance payload directly to `tmp/${ISSUE_ID}/phase-05-anti-pattern-scanner.json`. The payload must preserve the scanner's top-level `overall_status` and include at least one non-empty substance container (`findings`, `evidence`, or `output`). Do not add `subagent_id`, `story_id`, `phase`, or `phase_state_checksum`; `emit-conviction-worklog` injects/computes those fields per Issue #813. Any `file` value in a `findings[]` entry must be relative to the main checkout project root because `_check_file_realness` resolves it against `--project-root`; for worktree-resident files, write `worktrees/${ISSUE_ID}/...`, not bare paths such as `tests/${ISSUE_ID}/...`. Then persist through the conviction chain:
```bash
devforgeai-validate emit-conviction-worklog --story ${ISSUE_ID} --phase 05 --subagent anti-pattern-scanner --content-file tmp/${ISSUE_ID}/phase-05-anti-pattern-scanner.json --project-root ${PROJECT_ROOT}
# overall_status ∈ {PASS, NOT_APPLICABLE}; NOT_APPLICABLE when no source-code files changed.
```
Then anchor:
```bash
devforgeai-validate phase-record ${ISSUE_ID} --workflow=spec-sprint --phase=05 --subagent=anti-pattern-scanner --project-root=${PROJECT_ROOT}
# conviction-postrecord.sh sha256-anchors phase-05-anti-pattern-scanner.json.
```
VERIFY: Exit 0. The anti-pattern result is now anchored (Gate 3 of the completion hook).

### Step 3b: Run coverage record-result CLI, persist its verdict, and anchor (only when source_code_changed=true)

EXECUTE: Run the coverage record-result CLI — genuinely LLM-proof (Gate 4). The CLI reads the Gate 1 test artifact, applies thresholds from `test-plan.ai.yaml`, and writes the verdict itself — the orchestrator does NOT author the content:
```bash
devforgeai-validate coverage-record-result ${ISSUE_ID} --phase=05 --project-root=${PROJECT_ROOT}
# Writes devforgeai/feedback/ai-analysis/${ISSUE_ID}/phase-05-coverage-analyzer.json
# overall_status ∈ {PASS, FAIL, NOT_APPLICABLE} — CLI-computed from real coverage data.
```
Then persist through the conviction chain:
```bash
devforgeai-validate emit-conviction-worklog --story ${ISSUE_ID} --phase 05 --subagent coverage-analyzer --content-file devforgeai/feedback/ai-analysis/${ISSUE_ID}/phase-05-coverage-analyzer.json --project-root ${PROJECT_ROOT}
```
Then anchor:
```bash
devforgeai-validate phase-record ${ISSUE_ID} --workflow=spec-sprint --phase=05 --cli-command=coverage-record-result --project-root=${PROJECT_ROOT}
# conviction-postrecord.sh sha256-anchors phase-05-coverage-analyzer.json.
```
VERIFY: Exit 0. The coverage result is now anchored (Gate 4 of the completion hook). Unlike Gates 2–3, this artifact was written by the CLI — not by the orchestrator — so the "LLM-proof" label is accurate.

### Step 4: Anchor the AC verdict (conviction)

EXECUTE:
```bash
devforgeai-validate phase-record ${ISSUE_ID} --workflow=spec-sprint --phase=05 --subagent=ac-compliance-verifier --project-root=${PROJECT_ROOT}
# conviction-postrecord.sh sha256-anchors phase-05-ac-compliance-verifier.json.
```
VERIFY: Exit 0. The AC verdict is now anchored (Gate 2 of the completion hook).

### Step 5: Complete phase 05 (hook-gated)

EXECUTE:
```bash
devforgeai-validate phase-complete ${ISSUE_ID} --workflow=spec-sprint --phase=05 --checkpoint-passed --project-root=${PROJECT_ROOT}
```
VERIFY: Exit 0. If `spec-sprint-completion-gate.sh` blocks (exit 2), read its stderr — it names the missing/unanchored artifact — fix the corresponding step above (or return to Phase 04 if tests/ACs do not pass), then retry. **Never bypass the gate.**

---

## The completeness loop

```
04 Execute (TDD) ──► 05 QA ──(all ACs GROUNDED-pass + no Critical/High)──► 06 PR
        ▲                 │
        └─ criterion unmet / INCONCLUSIVE / Critical|High ─┘  (back to 04)
```

3 consecutive failed iterations on the same criterion → HALT/RCA (`diagnostic-analyst`), do not spin.

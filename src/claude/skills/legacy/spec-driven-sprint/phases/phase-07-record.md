# Phase 07: Record + STOP

## Entry Gate

```bash
devforgeai-validate phase-check ${ISSUE_ID} --workflow=spec-sprint --from=06 --to=07 --project-root=${PROJECT_ROOT}
# Exit 0: proceed | Exit != 0: Phase 06 incomplete → HALT
```

## Contract

PURPOSE: Record completion on the dashboard, then STOP — never cascade into unrelated work.
DELEGATES TO: none mandatory; OPTIONAL `framework-analyst` (capture friction, like `/dev` phase-09).
GATE: STOP-AND-ASK (no cascade).

---

## Mandatory Steps

### Step 1: Finalize the dashboard

EXECUTE: Verify the board at `tmp/${ISSUE_ID}/issue-<n>.html` — all work cards should read `done` (rendered automatically by `spec-sprint-board-render.sh` on each `phase-record`/`phase-complete` call). Fill the Phase 06 and Phase 07 completion notes tables manually: Date, Commit, PR, Tests added/total, Coverage, and Review verdict. These are NOT in the phase-state and require LLM annotation. For Phase 07 (record-only — no commit produced), fill the Commit cell with the literal value `no-commit`. The `validate-sprint-closeout` gate accepts this sentinel and does not treat it as a placeholder. Do NOT use `n/a`, `tbd`, or other placeholder values for this cell. For sprints that changed no Python/JavaScript source files, write `"Markdown documentation only — no source code changed"` in the Coverage cell (any non-placeholder prose passes the `validate-sprint-closeout` gate; bare `"N/A"` is rejected).
VERIFY: `devforgeai-validate validate-sprint-closeout ${ISSUE_ID} --project-root=${PROJECT_ROOT}` exits 0 before the Phase 07 completion gate.

### Step 2 (conditional): Capture friction

EXECUTE (optional): `Task(subagent_type="framework-analyst", ...)` to capture workflow friction observations.
VERIFY: Observations recorded.
RECORD: `devforgeai-validate phase-record ${ISSUE_ID} --workflow=spec-sprint --phase=07 --subagent=framework-analyst --project-root=${PROJECT_ROOT}`

### Step 3: Pristine-main hygiene (conditional)

EXECUTE: If a pristine-main watch is in use, `git pull --ff-only` the main checkout's default branch so it stays current with `origin/<default>`. Fast-forward only; never force.
VERIFY: Local default is current or untouched.

### Step 4: STOP-AND-ASK

EXECUTE: Report the outcome (PR link, required-check status, what shipped) and **STOP**. Do not begin another sprint or any follow-up work without explicit user instruction.
VERIFY: Control returned to the user.

---

### Final Step (conditional): End-of-run framework-friction review (#620)

EXECUTE (toggle-gated, default-OFF): read the friction-reporting toggle —
`devforgeai-validate friction-config --get enabled --project-root=${PROJECT_ROOT}`. If it is not
`true`, SKIP this step (friction reporting is opt-in). When `true`, run the verbatim friction
prompt below (`${ID}` is this workflow's id — here `${ISSUE_ID}`). Honest determinism boundary:
the `pre-friction-report-gate.sh` gate forces exactly ONE verdict artifact to exist; it does NOT
make the friction judgment deterministic — that judgment is **NOT-DETERMINISTIC** (the gate can be
satisfied with `{"friction":"none"}`). The deterministic teeth are the toggle, the gate's
force-one-emission, the enforcement-hook auto-append, and the mandatory remote dedup.

```
Role. You are the workflow orchestrator performing the end-of-run framework-friction review for DevForgeAI. Decide whether this run surfaced any framework defect or missing enforcement worth filing, and if so file it correctly and non-redundantly.
Scope. Only friction caused by the framework itself: a skill/phase/subagent that failed to guide a required action without a user reminder (e.g. not being prompted to create a worktree), a gate that fired wrongly or not at all, a phase file that contradicts a hook, prose an LLM predictably skipped, or a CLI/hook defect. Exclude: your own mistakes, the bug this run was fixing, and environment/network issues.
Inputs. (1) devforgeai/feedback/ai-analysis/${ID}/consolidated-analysis.json (captured observations). (2) Your session memory of where the workflow under- or mis-guided you.
Grounding contract. Every candidate must cite verifiable evidence: an exact file:line, the exact command/tool-call + path, and/or an exit code. No claim from memory. Drop any candidate that is not grounded. Use no aspirational language; describe only what IS broken and what WILL change.
Duplicate check (remote, mandatory). For each grounded candidate search open AND closed issues before filing: gh issue list --repo bankielewicz/DevForgeAI --state all --search "<3-5 keywords>" and gh search issues "<phrase>" --repo bankielewicz/DevForgeAI. If any result is the same defect/enhancement, do not file; record its number as the duplicate.
Decision gate. File via /create-incident ONLY when ALL hold: grounded, non-duplicate, scoped to one concrete change, non-aspirational. Otherwise do not file.
Filing. For each qualifying item: /create-incident "<one-sentence observation>" --type=<bug|enhancement> --work="<originating ID> -> <plan path> -> PR #<n>" --related="<chain>". Keep the provenance chain intact end-to-end.
Output (mandatory artifact). Write devforgeai/feedback/ai-analysis/${ID}/friction-summary.json: either {"friction":"filed","issues":[...],"duplicates_skipped":[...]} or {"friction":"none","rationale":"<one sentence>"}. The friction gate requires this artifact; the run cannot complete without it.
Few-shot (file it). "spec-sprint Phase 03 created the worktree but the phase file never told me to set CLAUDE_PROJECT_DIR, so the first gate ran against main (evidence: phase-03-worktree-materialize.md:35; gate exit 2)." -> grounded, scoped: file as bug.
Few-shot (do NOT file). "The board did not auto-update" when that IS the bug this run fixed -> exclude (own-scope). "Tests felt slow" with no file/command/exit evidence -> exclude (ungrounded).
```

VERIFY: `devforgeai/feedback/ai-analysis/${ID}/friction-summary.json` exists with one of the two
shapes — `{"friction":"filed","issues":[...],"duplicates_skipped":[...]}` or
`{"friction":"none","rationale":"..."}`. `duplicates_skipped` records any remote duplicate found by
the mandatory remote dedup probe. The `pre-friction-report-gate.sh` gate reads this artifact at the
final-phase `phase-complete`.

---

## Exit Gate

```bash
devforgeai-validate validate-sprint-closeout ${ISSUE_ID} --project-root=${PROJECT_ROOT}
devforgeai-validate phase-complete ${ISSUE_ID} --workflow=spec-sprint --phase=07 --checkpoint-passed --project-root=${PROJECT_ROOT}
# Exit 0: workflow complete | Exit != 0: HALT
```

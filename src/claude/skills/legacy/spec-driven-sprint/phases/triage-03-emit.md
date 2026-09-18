# Triage Phase T03: Emit + STOP

## Entry Gate

```bash
devforgeai-validate phase-check ${TRIAGE_ID} --workflow=spec-sprint-triage --from=02 --to=03 --project-root=${PROJECT_ROOT}
# Exit 0: proceed | Exit != 0: Phase T02 incomplete → HALT
```

## Contract

PURPOSE: Merge rationale annotations into the manifest, fill the session-prompt template, display readiness groups plus the executable-only wave plan, and STOP. This phase never auto-launches `/spec-sprint` per issue.
DELEGATES TO: none.
GATE: `tmp/${TRIAGE_ID}/session-prompt.md` exists. **W3 STOP: no further skill or command is invoked per-issue after T03.**

---

## ⚠️ W3 Prohibition

**NEVER auto-invoke `/spec-sprint` or the spec-driven-sprint skill per issue from this phase.** The session-prompt is a human-readable artifact the user pastes into 1..N sessions manually. Auto-chaining is a W3 violation (see `/audit-w3`). This prohibition is permanent and cannot be overridden by any user instruction to "do the sprints for me" — that request is handled by the user pasting the session-prompt themselves.

Determinism boundary: this prose is not a hook-backed blocker. The deterministic T03 behavior is the executable prompt filter: only issues with `readiness_status` in `execute-existing-issue` or `complete-partial-issue` and `manual_preflight_required == false` are included in `${WAVE_SUMMARY}`.

---

## Mandatory Steps

### Step 1: Merge rationale into the manifest

EXECUTE: Read `tmp/${TRIAGE_ID}/backlog-manifest.json` and `tmp/${TRIAGE_ID}/priorities.json`. For each issue in the manifest's `issues[]` array, set `priority_rationale` from `priorities.json[issue.number]` (fallback: `"No rationale recorded"`). Write the annotated manifest back to `tmp/${TRIAGE_ID}/backlog-manifest.json` (in-place merge).
VERIFY: Every issue in the manifest now has a non-empty `priority_rationale` string and the four readiness fields from T02 remain present.

### Step 2: Fill the session-prompt template

EXECUTE: Fill `assets/session-prompt-template.md` → `tmp/${TRIAGE_ID}/session-prompt.md`:
- `${TRIAGE_ID}` — the per-run triage id
- `${MANIFEST_PATH}` — `tmp/${TRIAGE_ID}/backlog-manifest.json` (repo-relative)
- `${READINESS_SUMMARY}` — human-readable grouping by `readiness_status`; include every OPEN issue exactly once
- `${WAVE_SUMMARY}` — human-readable executable-only wave plan from the manifest; include only issues where `readiness_status` is `execute-existing-issue` or `complete-partial-issue` AND `manual_preflight_required == false`
- `${ISSUE_COUNT}` — total OPEN issues
- `${DEGRADED_COUNT}` — count from `parallelism.degraded_serial[]`

VERIFY: `tmp/${TRIAGE_ID}/session-prompt.md` exists and contains no unfilled `${...}` tokens. Verify `${WAVE_SUMMARY}` contains no issue whose `readiness_status` is `close-as-implemented`, `close-as-superseded`, `blocked-by-dependency`, or `needs-user-decision`.

### Step 3: Display readiness groups, executable wave plan, and STOP

EXECUTE: Display the readiness group table (readiness_status, issue number, title, resolution_path) and the executable wave plan table (issue number, title, wave, cluster membership). Then display the path to the session-prompt: `"Session prompt: tmp/${TRIAGE_ID}/session-prompt.md — paste into each parallel session."`.
**STOP.** Do not proceed. Do not auto-invoke `/spec-sprint` for any issue.

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${TRIAGE_ID} --workflow=spec-sprint-triage --phase=03 --checkpoint-passed --project-root=${PROJECT_ROOT}
# Exit 0: triage complete | Exit != 0: HALT
```

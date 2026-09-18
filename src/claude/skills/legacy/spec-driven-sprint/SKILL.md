---
name: spec-driven-sprint
description: >
  Drives an ad-hoc, resumable spec-driven sprint from a single GitHub issue with
  structural anti-skip enforcement. Given an issue, it researches the fix surface in
  plan mode, materializes a self-contained resumable HTML spec (work cards + embedded
  AI resumption prompt), creates an isolated worktree off the remote default branch,
  executes each work card (TDD Red-Green-Refactor where there is code), QA-validates
  against the spec's acceptance criteria in an iteration loop, and opens a PR — all
  through the Execute-Verify-Gate pattern at every step. No story file is required.
  Use when turning a GitHub issue into a hook-enforced, resumable sprint, or when the
  user runs /spec-sprint. Distinct from /create-sprint, which plans story sprints from
  an existing backlog; this skill is issue-driven and produces no story artifacts.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - Task
  - EnterPlanMode
  - ExitPlanMode
  - Bash(git:*)
  - Bash(gh:*)
  - Bash(devforgeai-validate:*)
  - Bash(npm:*)
  - Bash(pytest:*)
  - Bash(dotnet:*)
  - Bash(cargo:*)
  - Bash(mvn:*)
  - Bash(gradle:*)
  - Bash(python:*)
model: opus
effort: High
---

# Spec-Driven Sprint

Turn one GitHub issue into a self-contained, **resumable** spec-driven sprint: research the
fix surface, materialize an HTML spec (work cards + embedded AI resumption prompt), branch an
isolated worktree off the remote default, execute each card with TDD where there is code,
QA-validate against the spec's acceptance criteria in an iteration loop, then open a PR.

No story file is produced — this skill is **ad-hoc and issue-driven**, mirroring
`spec-driven-dev`'s Execute-Verify-Gate discipline without `spec-driven-dev`'s story-scoped
artifacts.

**If ambiguous or conflicts detected: HALT and use AskUserQuestion.**

---

## Portability — consumer-safe core + DevForgeAI addendum

This skill runs in **any** repository, not only DevForgeAI's own. Its phase files keep a
**portable core** (generic / runtime-detected: default branch, required check, test runner)
and apply a **DevForgeAI addendum** only when both sentinels are present:

- `devforgeai/specs/context/` (the constitutional context folder), and
- `.github/workflows/python-cli-tests.yml` (the required-check workflow).

When the sentinels are absent, the host-specific addendum mechanics are skipped in favor of
the runtime-detected equivalents (default branch, required check, test runner). The split
rule-set lives in `references/portable-workflow.md` (consumer-safe core) and
`references/devforgeai-addendum.md` (sentinel-gated host mechanics — worktree placement, the
required-check name, coverage/drift gates, dual-path mirror, string hygiene). Never hardcode
host-specific tokens into the consumer-facing core.

---

## Anti-Skip Enforcement Contract

Enforced structurally outside LLM control, not by this prose — by the framework's
deterministic gates wired for the `spec-sprint` workflow: the `devforgeai-validate` phase
gates, the `settings.json`-registered `.claude/hooks/` scripts (`spec-sprint-completion-gate.sh`,
`phase-completion-gate.sh`, `conviction-postrecord.sh`), and the `ISSUE-<n>` phase-state file.
The honest determinism boundary: **CLI-run tests are LLM-proof** (Gate 1: the CLI
executes the suite and signs the result); **CLI-computed coverage is LLM-proof** (Gate 4:
`devforgeai-validate coverage-record-result` reads real coverage data and writes the verdict);
**AC-semantic and anti-pattern verdicts are tamper-evident but NOT LLM-proof** (Gates 2–3:
a Python CLI cannot invoke a Claude `Task()` — the sha256 anchor catches post-hoc edits
but cannot prevent a forged Task() result). Do not claim more.

---

## Delegation Model

This is a **delegating** skill (like `/dev` and `/qa` per `DevForgeAI.md`), NOT inline.
Phases 04–05 reuse the proven `/dev` + `/qa` subagent chain rather than reimplementing
TDD/QA. All delegated subagents ship with the framework (the installer copies
`.claude/agents/`), so the delegation is framework-core — present in every consumer install.
See the **Subagent Delegation Map** below; each phase file specifies the exact `Task()`
invocations and the per-card work-contract marshaling.

---

## Parameter Extraction

| Context Marker | Set By | Description |
|----------------|--------|-------------|
| `$ISSUE_ARG` | /spec-sprint | The issue argument — a URL, `#N` / `N`, or `--backlog <selector>`. |
| `$ISSUE_NUMBER` | Phase 00 | Parsed issue number; the workflow id is `ISSUE-<n>`. (Core route only.) |
| `$ISSUE_ID` | Preamble (before loop) | `ISSUE-<n>` — the workflow id for the state file and every gate call. (Core route.) |
| `$TRIAGE_ID` | Triage T00 | `TRIAGE-YYYYMMDD-HHMMSS` — the per-run id for the triage state file. (Triage route.) |
| `$BACKLOG_SELECTOR` | Triage T00 | Selector string from `--backlog <selector>`. (Triage route.) |
| `$PROJECT_ROOT` | Preamble (before loop) | Repo root (`.`); passed to every gate's `--project-root`. |
| `$ISSUE_TYPE` | Phase 01 | `feat` / `fix` / `chore` — drives the branch prefix. (Core route.) |
| `$DEVFORGEAI_SENTINELS` | Phase 00 | `true` when both sentinels are present → apply the addendum. |
| `$DEFAULT_BRANCH` | Phase 00 | Detected remote default branch (e.g., `main`). |
| `$REQUIRED_CHECK` | Phase 00 | Detected required status check(s) for the PR. |
| `$TEST_RUNNER` | Phase 00 | Detected test runner (npm / pytest / cargo / …). |
| `$BOARD_PATH` | Phase 03 | Canonical board path: `tmp/${ISSUE_ID}/issue-<n>.html`. Fixed — not user-chosen; matches the hook's hardcoded output path. (Core route.) |
| `$WORKTREE_PATH` | Phase 03 | Absolute path of the sprint worktree (e.g. `worktrees/ISSUE-<n>` under the DevForgeAI addendum). On resume, run `devforgeai-validate sprint-resume ${ISSUE_ID} --project-root=${PROJECT_ROOT} --format=json` and bind from the `worktree_path` field. (Core route.) |

**Route selection (before any gate):** if `$ISSUE_ARG` starts with `--backlog`, parse `$BACKLOG_SELECTOR`, generate `$TRIAGE_ID = TRIAGE-$(date -u +%Y%m%d-%H%M%S)`, and route to the **Triage Phase Loop** (T00→T01→T02→T03) instead of the core loop. Otherwise bind `$ISSUE_NUMBER`, `$ISSUE_ID`, and `$PROJECT_ROOT` and route to the **Core Phase Loop** (00→01→03→04→05→06→07). See `references/backlog-triage.md` for the triage route and `references/claim-protocol.md` for the claim/release protocol (Phase 00 Step 5 + Phase 06 Step 2).

**Bind these BEFORE the orchestration loop's first gate (the Phase-00 entry gate references both):**
parse `$ISSUE_ARG` → `$ISSUE_NUMBER` = `<n>` and **`$ISSUE_ID` = `ISSUE-<n>`** (the id for the
phase-state file and every `devforgeai-validate` call; PR-1 made `ISSUE-` a valid id), and set
**`$PROJECT_ROOT` = `.`** (the repo root passed to every gate's `--project-root`). Phase 00 Step 1
re-confirms the parse, but the id and project-root MUST already exist when the loop's first gate runs.
Parameter-extraction detail lives in `phases/phase-00-init.md`.

## Resume Routing (Issue #557)

After binding `$ISSUE_ID` and `$PROJECT_ROOT` and before the orchestration loop, run:

```bash
devforgeai-validate sprint-resume ${ISSUE_ID} --project-root=${PROJECT_ROOT} --format=json
```

- **Exit 0, `next_phase` != `"00"`** → bind `$WORKTREE_PATH` and `$BRANCH` from the JSON
  `worktree_path`/`branch` fields; re-check `$DEVFORGEAI_SENTINELS`; re-detect `$TEST_RUNNER`
  from the state file's `detected_tech_stack`; start the orchestration loop at `next_phase`
  (entry gates still enforce `phase-check --from/--to` order).
- **Exit 1** (no state file) → run a fresh sprint from Phase 00.
- **Exit 3, `worktree_missing: true`** → the checkpoint's `worktree_path` is absent (`None`)
  or points at a directory that no longer exists on disk (worktree pruned, branch deleted, or
  path never resolved). **HALT and AskUserQuestion** with two options:
  (a) **Recreate** — branch a fresh worktree off `origin/<default>` at the checkpoint's
  `$BRANCH` value and resume from `next_phase` (entry gates still run); write the new
  worktree path back to the checkpoint before proceeding.
  (b) **Closeout** — skip directly to Phase 07 (Record + STOP); use when the sprint's work
  already merged and no further code changes are needed.

**Clean-exit note:**
At any phase boundary under context pressure, display the checkpoint's `resume_command` and stop.
The per-phase checkpoint (written by `complete_workflow_phase`) makes abrupt resets lossless —
the next session calls `sprint-resume` and picks up exactly where the previous session stopped.

**Fresh already-fixed closeout (Issue #893):**
When Phase 01 research proves the issue was already fixed by a merged PR before this sprint starts,
use the Phase 01 closeout path, not the worktree-missing resume path and not a fabricated TDD card:
`devforgeai-validate phase-set-closeout ${ISSUE_ID} --workflow=spec-sprint --reason=already-fixed --evidence-pr <merged-pr-number-or-url> --repo <org>/<repo> --project-root=${PROJECT_ROOT}`.
Phase 04 completion accepts closeout mode only when the phase state contains `04.closeout`, merged
PR evidence from `gh pr view`, and a matching `evidence_sha256`.

---

## Workflow Identity

- **Workflow type:** `spec-sprint`
- **Id:** `ISSUE-<n>` (derived from the issue argument)
- **State file:** `devforgeai/workflows/ISSUE-<n>-spec-sprint-phase-state.json`

Phase 00 has no predecessor — its `phase-init` IS the entry gate; skip `phase-check --from=00`.

---

## Phase Orchestration Loop

```
FOR phase_id in [00, 00.5, 01, 03, 04, 05, 06, 07]:

    1. ENTRY GATE — run the phase file's "## Entry Gate" block verbatim.
       (Phase 00 uses `phase-init`; phases 00.5-07 use `phase-check --from={prev} --to={phase_id}`.)
       IF exit != 0: HALT.

    2. LOAD: Read(file_path="phases/{phase_files[phase_id]}") — the phase file is the single
       source of truth for this phase's steps AND its exact gate commands. The gate commands are
       written ONLY in the phase file; do not execute from this loop alone.

    3. EXECUTE: Follow every step in the phase file (EXECUTE-VERIFY-RECORD triplets) — delegate
       to the mapped subagent; VERIFY a named deterministic signal (never "looks done"); RECORD
       the exact phase-record call(s) the phase file emits.

    4. EXIT GATE — run the phase file's "## Exit Gate" block verbatim
       (`phase-complete --phase={phase_id} --checkpoint-passed`). IF exit != 0: HALT.
```

The exact gate commands — `${ISSUE_ID}` + `--project-root=${PROJECT_ROOT}`, and Phase 05's
two-anchor sequence — live ONLY in the phase files' Entry/Exit Gate blocks, the single source of
truth. This loop is the altitude-level shape; read the phase file for the literal CLI.

| Phase | Name | File |
|-------|------|------|
**Core route phases (workflow key: `spec-sprint`, id: `ISSUE-<n>`):**

| Phase | Name | File |
|-------|------|------|
| 00 | Init + Pre-Flight | `phases/phase-00-init.md` |
| 00.5 | Merit + Recurrence Triage (pre-dashboard) | `phases/phase-00.5-merit-triage.md` |
| 01 | Plan-Mode + Research + Design (HTML-spec work cards) | `phases/phase-01-plan-research.md` |
| 03 | Worktree + Materialize HTML | `phases/phase-03-worktree-materialize.md` |
| 04 | Execute (TDD per work card) | `phases/phase-04-execute.md` |
| 05 | QA vs Spec (gated completion) | `phases/phase-05-qa.md` |
| 06 | Commit / Push / PR | `phases/phase-06-pr.md` |
| 07 | Record + STOP | `phases/phase-07-record.md` |

**Triage route phases (workflow key: `spec-sprint-triage`, id: `TRIAGE-YYYYMMDD-HHMMSS`):**

| Phase | Name | File |
|-------|------|------|
| T00 | Init + gh auth + selector validation | `phases/triage-00-init.md` |
| T01 | Fetch + Prioritize issues | `phases/triage-01-fetch-prioritize.md` |
| T02 | Compute overlap + waves (triage-backlog CLI) | `phases/triage-02-overlap.md` |
| T03 | Emit manifest + session-prompt + STOP (W3: never auto-invokes /spec-sprint) | `phases/triage-03-emit.md` |

Each phase's GATE is defined in its phase file's Contract — read the file. The table above is a
manifest of phase→file, not a substitute for the phase file.

---

## The Execute ↔ QA Completeness Loop

Phases 04–05–06 form a completeness loop, not a linear pass: phase 05 back-edges to 04 until
**every** spec acceptance criterion GROUNDED-passes (completeness is the PR gate, not merely
"Critical/High fixed"). The diagram, the back-edge/forward-edge rules, the CI-triage rule, and the
3-attempt loop-bound live in **`phases/phase-05-qa.md`** — read it there.

**The authoritative completion signal is the phase-state file, NOT the HTML.** The HTML
`data-status` is a *view*; every gate reads `ISSUE-<n>-spec-sprint-phase-state.json`. The LLM
cannot edit its way to a PR by writing `done` in the HTML — the gates ignore the HTML.

---

## Subagent Delegation Map (Phase → agents) — DELEGATE, do NOT hand-roll

| Phase | Delegated to | Conditional | Notes |
|-------|-----------|-------------|-------|
| 00 Init + Pre-Flight | `tech-stack-detector`, `git-validator` | — | detector replaces inline detection commands |
| 01 Plan-Mode + Research + Design | — | `architect-reviewer` (review card decomposition for non-trivial issues, Step 8) | |
| 03 Worktree | `git-worktree-manager` | — | discover / idle-detect / max-limit (report-only; orchestrator performs the create + verify) |
| 04 Execute (TDD per card) | `test-automator` (Red), `backend-architect` (Green), `refactoring-specialist` (Refactor), `code-reviewer` (diff), `context-validator` (pre-commit) | `frontend-developer` (UI), `api-designer` (API), `integration-tester` (cross-component) | mirrors `/dev` 02/03/04 |
| 05 QA vs Spec (gated) | `ac-compliance-verifier` (gated AC verdict), `anti-pattern-scanner`, `coverage-analyzer` | `code-quality-auditor`, `security-auditor`, `dead-code-detector` | all three gate-enforced (Gates 2-4); scanner is tamper-evident NOT LLM-proof (Gate 3); coverage is LLM-proof via coverage-record-result CLI (Gate 4) |
| 06 Commit / Push / PR | — | `documentation-writer` (if public API/docs changed) | |
| 07 Record + STOP | — | `framework-analyst` (capture friction) | |
| On failure (3-attempt) | `diagnostic-analyst` (RCA per `diagnosis-before-fix.md`) | — | loop-bound escalation |

Phase-05 has three gate-enforced subagents: `ac-compliance-verifier` (Gate 2, `overall_status=PASS`),
`anti-pattern-scanner` (Gate 3, `overall_status∈{PASS,NOT_APPLICABLE}`), and `coverage-analyzer`
(Gate 4, same) — all sha256-anchored by `spec-sprint-completion-gate.sh` before
`phase-complete --phase=05`. Phase 04's `test-automator`, `backend-architect`,
`frontend-developer`, `api-designer`, `refactoring-specialist`, `integration-tester`,
`code-reviewer`, and `context-validator` dispatches are handoff-path protected by the
registry-driven `subagent-handoff-consumption-gate.sh` when they fire; this gate blocks a protected
dispatch whose prompt omits `tmp/<ISSUE_ID>/handoffs/`. It does not prove that a conditional
subagent was dispatched when a card path skipped it. Delegation-compliance enforcement (a
fabricated-subagent dispatch gate) is tracked by #413. The phase files carry the same honest labels.

**Per-card work-contract marshaling (integration requirement):** the 5 dev subagents consume a
per-invocation work-contract (`test-contract-v1` / `contract-template.yaml`) written to
`tmp/ISSUE-<n>/contracts/`, and `ac-compliance-verifier` verifies against scoped acceptance
criteria. Because this skill is story-file-free, each Phase-04/05 invocation generates the
contract from the work card's AC list via `devforgeai-validate build-test-contract <id> --phase
<NN> --subagent <type> --workflow=spec-sprint --ac-list-file ...`, passing `ISSUE-<n>` as the id —
hand-authoring the YAML is blocked by the contract-schema-validator hook. Step 3 passes each contract path as `Work contract: ${CONTRACT_PATH_<type>}` in the subagent Task() prompt (lean-pointer form, mirroring /dev phase-02:158-163). Documentation-only cards that dispatch no dev subagent in Step 3 generate no contracts (doc-card exemption in Step 1) — this exemption is contract-only; the Phase 05 test gate still requires a content-assertion test authored in Phase 04 Step 3. The phase files specify this marshaling — without the contract the subagents have no input. Each contracted subagent MUST also append its `completion_record` to the contract file when done; `artifact-verification-gate.sh` (BA-018) checks for a populated record at `phase-complete --phase=04` and blocks with an error if it is null — mirror the append instruction and VERIFY in the dispatch prompts, following the pattern in `spec-driven-dev/phases/phase-03-implementation.md`.

**Portable-core language fallback:** `backend-architect`'s framework patterns cover Python /
TypeScript / C# only. For a Go / Rust / Markdown / config-only card → implement inline, then
dispatch `backend-architect` (or the appropriate Green-phase subagent) for post-implementation
verification before calling `phase-record`. Do NOT call `phase-record
--subagent=backend-architect` without a prior `Agent(subagent_type="backend-architect")`
dispatch — the `subagent-dispatch-reconcile.sh` gate will block `phase-complete` with
"unbacked subagent records".

---

## The Resumable HTML Spec

The skill fills `assets/spec-dashboard-template.html` into `tmp/${ISSUE_ID}/issue-<n>.html` — a
self-contained, dark-mode, **30-token** (13 GLOBAL + 17 PER_PHASE) dashboard with an embedded
AI resumption prompt. The fill is mechanical: 13 GLOBAL tokens once, then one `PHASE_NAV` +
`PHASE_CARD` expansion per PHASE_ORDER phase (7 expansions: 00, 01, 03, 04, 05, 06, 07)
(HTML-escape every text slot; set only `data-status`; empties → `—`). The resumption prompt
self-references the spec's own committed path and spells out the board-update mechanism so a
cold session can resume from the first non-done phase.
Phase 00.5 is a pre-dashboard runtime gate and is not rendered as an eighth dashboard phase.

Token contract, fill rules, and the resumption-prompt shape:
`references/resumption-prompt-template.md`.

---

## Reference Files

### Phase Execution (`phases/`)

| File | Phase |
|------|-------|
| `phase-00-init.md` | Init + Pre-Flight |
| `phase-00.5-merit-triage.md` | Merit + Recurrence Triage (pre-dashboard) |
| `phase-01-plan-research.md` | Plan-Mode + Research + Design (HTML-spec work cards) |
| `phase-03-worktree-materialize.md` | Worktree + Materialize HTML |
| `phase-04-execute.md` | Execute (TDD per work card) |
| `phase-05-qa.md` | QA vs Spec (gated completion) |
| `phase-06-pr.md` | Commit / Push / PR |
| `phase-07-record.md` | Record + STOP |

### Supporting References (`references/`)

| File | Purpose |
|------|---------|
| `portable-workflow.md` | Consumer-safe generic / runtime-detected core (zero DevForgeAI tokens) |
| `devforgeai-addendum.md` | DevForgeAI-only mechanics, applied only when both sentinels are present |
| `resumption-prompt-template.md` | The 30 template tokens + the fill-contract rules |

### Assets (`assets/`)

| File | Purpose |
|------|---------|
| `spec-dashboard-template.html` | The fillable dashboard template (30 tokens) |
| `spec-dashboard-example.html` | A filled reference example |

---

## Success Criteria

- The fix surface is GROUNDED (cited files Read/Grep'd), not assumed.
- The HTML spec is materialized with 0 token leak and an accurate work-card decomposition.
- The worktree is branched off the **remote default tip**, never stale local default.
- Every work card reaches `done` only via the spine (test exit 0 AND fresh-verifier
  GROUNDED-pass on every AC) — never by self-flipping the HTML.
- Every spec acceptance criterion GROUNDED-passes before the PR opens.
- The PR's detected required check is green; nothing is bypassed (`--no-verify` is forbidden).
- The skill STOPS-AND-ASKS at phase 07 — no cascade into unrelated work.

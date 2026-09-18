---
description: Run an ad-hoc spec-driven sprint from a GitHub issue (issue → resumable HTML spec → PR)
argument-hint: <issue-url | #number | number | --backlog <selector>>
model: Sonnet
effort: High
allowed-tools: AskUserQuestion, Read, Skill, Bash(git:*)
execution-mode: immediate
---

# /spec-sprint — Ad-Hoc Spec-Driven Sprint

Turn a single GitHub issue into a self-contained, resumable spec-driven sprint: research
the fix surface in plan mode, materialize an HTML spec (work cards + embedded AI resumption
prompt), branch an isolated worktree off the remote default, execute each card with TDD
where there is code, QA-validate against the spec's acceptance criteria, and open a PR.

Distinct from `/create-sprint` (which plans story sprints from an existing backlog) — this
is issue-driven and produces no story file.

You MUST execute the spec-driven-sprint skill, when called upon: Skill(command="spec-driven-sprint")

---

## Phase 0: Parse Arguments

```
ISSUE_ARG = trim($ARGUMENTS)

IF ISSUE_ARG starts with "--backlog":
    # Triage route: pass through to the skill, which routes to the triage phase loop (T00→T01→T02→T03)
    BACKLOG_SELECTOR = parse selector from ISSUE_ARG (the token after "--backlog")
    Display: "**Backlog selector:** ${BACKLOG_SELECTOR}"
ELSE IF ISSUE_ARG empty:
    Display: "Usage: /spec-sprint <issue-url | #number | number>"
    Display: "       /spec-sprint --backlog <selector>"
    Display: "Examples: /spec-sprint #318 | /spec-sprint --backlog 399-430 | /spec-sprint --backlog label:bug"
    HALT
```

The skill's Phase 00 parses `ISSUE_ARG` into `ISSUE-<n>` (core route) or reads the
`--backlog` selector (triage route). Keep this command thin — no business logic here;
all of it lives in the skill's phase files.

---

## Phase 1: Invoke the Skill

```
Display: ""
Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Display: "  DevForgeAI Spec-Driven Sprint"
Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Display: "**Issue:** ${ISSUE_ARG}"

# The skill owns its own plan-mode window — do NOT EnterPlanMode here (a command-level
# wrap would double the plan window and bias the skill toward summarizing instead of
# executing its phase state machine). Phase 01 both researches the fix surface AND
# authors the work-card decomposition inside plan mode, calling ExitPlanMode for your
# approval before the Phase-01 exit gate; phases 03-07 then execute the approved plan.
Skill(command="spec-driven-sprint", args="$ARGUMENTS")
```

---

## Phase 2: Display Results

Display the skill's formatted result directly. No processing, parsing, or template
generation in this command — all business logic is delegated to the skill, and the skill
STOPS-AND-ASKS at its Phase 07 (no cascade).

---

## Resume Behavior (Issue #557)

`/spec-sprint <n>` is also the resume entrypoint for an in-progress sprint. The skill
automatically calls `devforgeai-validate sprint-resume ISSUE-<n>` before entering the
orchestration loop:

- If a checkpoint exists (written after each `phase-complete`), the session binds the
  saved `worktree_path`, `branch`, `ac_status`, and `next_phase` and resumes from the
  first incomplete phase without replaying Phase 00–03 from scratch.
- If no checkpoint or state file exists, the skill runs a fresh sprint from Phase 00.

To manually check resume state without starting a sprint:

```bash
devforgeai-validate sprint-resume ISSUE-<n> --project-root=. --format=json
```

---

## Error Handling

| Error | Resolution |
|-------|------------|
| No issue argument | Usage: `/spec-sprint <issue-url \| #number \| number>` or `/spec-sprint --backlog <selector>` |
| Issue not found / `gh` unauthenticated | The skill HALTs in Phase 01 → authenticate `gh` / verify the issue number |
| Local default branch diverged from origin | The skill HALTs in Phase 00 pre-flight → reconcile before re-running (fast-forward only) |
| phase-05 completion gate blocks | Tests must pass + every acceptance criterion must GROUNDED-pass — return to Phase 04 (more TDD) |
| sprint-resume exits 1 on resume attempt | No state file found → treat as fresh sprint (Phase 00) |

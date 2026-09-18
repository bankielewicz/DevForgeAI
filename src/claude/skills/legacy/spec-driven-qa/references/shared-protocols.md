# Shared QA Protocols

Reusable patterns applied across all QA phases. Load this file once at Phase 1 — it covers pre-flight verification, CLI gates, and task tracking for the entire workflow.

---

## Pre-Flight Verification

Every phase (2-6) must verify the previous phase completed before executing. This prevents phase skipping and ensures sequential integrity.

**Template (replace `{PREV}` and `{CURRENT}` with phase numbers):**

```
devforgeai-validate phase-status {STORY_ID} --workflow=qa --project-root=.

IF phase {PREV} NOT completed in qa-phase-state.json:
    HALT: "Phase {PREV} not verified complete — Phase {CURRENT} cannot execute"
    Exit with code 1 (phase sequencing violation)

Display: "Phase {PREV} verified complete — Phase {CURRENT} preconditions met"
```

**Why this matters:** RCA-022 identified phase skipping as a root cause of STORY-128 failures. Each phase produces artifacts that subsequent phases depend on — skipping corrupts the validation chain.

---

## CLI Gate Protocol

After completing each phase, record completion via the CLI validator. This creates an auditable trail in `qa-phase-state.json`.

**Template (replace `{N}` with two-digit phase number, `{PHASE_NAME}` with phase name):**

```
devforgeai-validate phase-complete {STORY_ID} --workflow=qa --phase={N} --checkpoint-passed --project-root=.

Display: "Phase {N} gate passed | {PHASE_NAME} | {summary_metric}"
```

**Phase number mapping for CLI gates:**

| Phase | CLI `--phase` value |
|-------|-------------------|
| Phase 1: Setup | 01 |
| Phase 2: Validation | 02 |
| Phase 3: Diff Regression | 03 |
| Phase 4: Analysis | 04 |
| Phase 5: Reporting | 05 |
| Phase 6: Cleanup | 06 |

**First call (Phase 1 only):** Before the first gate, initialize phase state:
```
devforgeai-validate phase-init {STORY_ID} --workflow=qa --project-root=.
```

---

## Task Tracking

Use TaskCreate at Phase 1 to create the execution tracker, then TaskUpdate at each phase transition.

**Phase 1 initialization:**
```
TaskCreate(subject="QA Phase 1: Setup", description="Initialize QA environment", activeForm="Running QA Phase 1: Setup")
TaskCreate(subject="QA Phase 2: Validation", description="Tests, coverage, traceability")
TaskCreate(subject="QA Phase 3: Diff Regression", description="Git diff analysis, test integrity")
TaskCreate(subject="QA Phase 4: Analysis", description="Anti-patterns, spec compliance, quality")
TaskCreate(subject="QA Phase 5: Reporting", description="Result determination, report generation")
TaskCreate(subject="QA Phase 6: Cleanup", description="Lock release, hooks, summary")
```

**Phase transitions:** When starting a phase, set its task to `in_progress`. When completing, set to `completed`.

---

## Phase Completion Display

Each phase ends with a standardized completion message:

```
Phase {N} Complete: {Name}
  {metric_1}: {value}
  {metric_2}: {value}
```

The specific metrics vary by phase — see each phase's section in SKILL.md for the display template.

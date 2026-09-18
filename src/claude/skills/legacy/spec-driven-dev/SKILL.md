---
name: spec-driven-dev
description: >
  Implements user stories through spec-driven TDD workflow (Red-Green-Refactor) with
  structural anti-skip enforcement. Replicates all 12 phases of the DevForgeAI development
  workflow using the Execute-Verify-Gate pattern at every step. Designed to prevent token
  optimization bias through lean orchestration, fresh-context subagent delegation, and
  binary CLI gate enforcement. Use when developing features from story specifications,
  building code that must comply with context files, or running TDD workflows.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - Task
  - Bash(git:*)
  - Bash(npm:*)
  - Bash(pytest:*)
  - Bash(dotnet:*)
  - Bash(cargo:*)
  - Bash(mvn:*)
  - Bash(gradle:*)
  - Bash(python:*)
  - Skill
model: opus
effort: High
---

# Spec-Driven Development

Implement user stories using strict TDD (Red-Green-Refactor) while enforcing all 6 context file constraints.

**Context files are THE LAW:** tech-stack.md, source-tree/, dependencies.md, coding-standards.md, architecture-constraints.md, anti-patterns.md

**If ambiguous or conflicts detected: HALT and use AskUserQuestion**

---

## Anti-Skip Enforcement Contract

Enforced structurally outside LLM control, not by this prose — by the framework's deterministic gates wired for this workflow: the `devforgeai-validate` phase gates, the `settings.json`-registered `.claude/hooks/` scripts, and `.claude/hooks/phase-steps-registry.json` (ADR-076).

---

## Parameter Extraction

Extract story ID from conversation context. See `references/parameter-extraction.md` for the extraction algorithm.

## Command Integration

| Context Marker | Set By | Description |
|----------------|--------|-------------|
| `$STORY_ID` | /dev, /resume-dev | Story identifier (STORY-NNN) |
| `$FORCE_FLAG` | /dev | Bypass dependency checks |
| `$REMEDIATION_MODE` | /dev | `--fix` flag or auto-detected from gaps.json |
| `$GAPS_AUTO_DETECTED` | /dev | True if gaps.json auto-detected |
| `$IGNORE_DEBT_FLAG` | /dev | Override technical debt threshold |
| `$RESUME_MODE` | /resume-dev | "manual" or "auto" |
| `$PHASE_NUM` | /resume-dev | Phase number to resume from |
| `$NEXT_ACTION` | dev-preflight | Dispatch enum (STORY-658): `begin-phase-01` / `phase-status-resume` / `phase-cycle-start` / `already-complete` / `halt-ambiguous` / `halt-corrupt-state` |
| `$NEXT_COMMAND` | dev-preflight | Precomputed CLI invocation for the next step (string or null). Used by the `phase-cycle-start` branch. |
| `$NEXT_PHASE_TO_ENTER` | dev-preflight | Phase number CURRENT_PHASE should be set to after dispatch (e.g., "01", "02", existing phase, or null) |
| `$GUIDANCE` | dev-preflight | Human-readable explanation of the chosen `$NEXT_ACTION` (always populated) |

---

## Phase State Initialization & Entry Dispatcher [MANDATORY FIRST]

This block decides whether to start a new workflow, resume an existing one, open a remediation cycle, or halt — based on guidance from `dev-preflight` (or self-bootstrap if invoked outside `/dev`). Full dispatch reference and execution detail: `references/preflight/01.0-entry-dispatcher.md`.

### Step A: Self-bootstrap if `$NEXT_ACTION` is unset

`$NEXT_ACTION` is normally set by the upstream `/dev` command from `dev-preflight` JSON. If unset (e.g., direct skill invocation, `/resume-dev`, or older `/dev` versions), invoke preflight here:

```bash
devforgeai-validate dev-preflight ${STORY_ID} --project-root=. --format=json
```

Parse the JSON result and populate the four context markers:
- `$NEXT_ACTION` ← `result.next_action`
- `$NEXT_COMMAND` ← `result.next_command` (may be null)
- `$NEXT_PHASE_TO_ENTER` ← `result.next_phase_to_enter` (may be null)
- `$GUIDANCE` ← `result.guidance`

Also extract `$REMEDIATION_MODE`, `$REMEDIATION_SOURCE`, `$OPEN_REC_IDS`, `$QA_RECOMMENDATIONS_STATUS`, `$CURRENT_PHASE` from the same payload.

| dev-preflight Exit Code | Meaning | Action |
|-------------------------|---------|--------|
| 0 | New workflow created | Continue to Step B with `$NEXT_ACTION = "begin-phase-01"` |
| 1 | Story not found | HALT — display `result.error` |
| 2 | Existing workflow (resume) | Continue to Step B with `$NEXT_ACTION` from result |
| 3 | Invalid story ID OR corrupt state | If `$NEXT_ACTION == "halt-corrupt-state"`: display guidance + HALT. Else: HALT (invalid format) |
| **4** | **`source_devarch` missing or invalid in story frontmatter (B2 / ADR-099)** | **HALT. Do NOT enter Phase 01. Emit dev-preflight's stderr verbatim to the user; do NOT auto-invoke any migration commands. Wait for user to follow the migration path (see `.claude/rules/workflow/story-lifecycle.md` § DEVARCH Seed Prerequisite) and re-invoke `/dev ${STORY_ID}`.** |
| 127 | CLI not installed | Backward-compat: set `$NEXT_ACTION = "begin-phase-01"` and proceed without enforcement |

### Step B: Dispatch on `$NEXT_ACTION`

| `$NEXT_ACTION` | Action | CURRENT_PHASE |
|----------------|--------|---------------|
| `begin-phase-01` | State already created by `dev-preflight`. Display "Beginning workflow for ${STORY_ID}". Enter Phase Orchestration Loop. | `"01"` |
| `phase-status-resume` | Display "Resuming ${STORY_ID} from phase ${NEXT_PHASE_TO_ENTER}." If `$REMEDIATION_MODE == true` and no open items, display `$GUIDANCE` warning. Enter Phase Orchestration Loop at `$NEXT_PHASE_TO_ENTER`. | `$NEXT_PHASE_TO_ENTER` (existing phase from state) |
| `phase-cycle-start` | **The remediation entry point.** Execute `$NEXT_COMMAND` (precomputed `phase-cycle-start --source=qa-recommendations ...` invocation). Capture `payload.cycle` as `$CURRENT_CYCLE`. Set `$REMEDIATION_MODE=true`, `$REMEDIATION_SOURCE="qa-recommendations"`. The CLI resets top-level `current_phase` to `$NEXT_PHASE_TO_ENTER` (typically `"02"`); read it back from the new state via `phase-status`. Enter Phase Orchestration Loop. | `$NEXT_PHASE_TO_ENTER` (typically `"02"`) |
| `already-complete` | Display `$GUIDANCE`. Do NOT enter the orchestration loop. HALT cleanly (this is not an error — workflow is done). | n/a |
| `halt-ambiguous` | AskUserQuestion: "Story is mid-workflow at phase ${CURRENT_PHASE} with open QA items. Resume the in-progress phase, or open a new remediation cycle?" Branch to `phase-status-resume` or `phase-cycle-start` based on user response. | (depends on user) |
| `halt-corrupt-state` | Display `$GUIDANCE` (from CLI). Do NOT auto-recover. HALT. | n/a |

**Iteration counter:** `iteration_count = 1`, `max_iterations = 5`. If resuming, read from phase-state.json.

**Important — phase-init removal:** This block REPLACES the legacy `phase-init` invocation. `dev-preflight` now creates state when needed (and the dispatcher handles it via `begin-phase-01`). Do NOT separately call `devforgeai-validate phase-init` — that command's "state already exists" failure is the very bug this dispatcher fixes (STORY-658).

---

## Phase Orchestration Loop

```
FOR phase_num in range(CURRENT_PHASE, 11):
    phase_id = format(phase_num)

    1. ENTRY GATE:
       IF phase_id == "01":
         Skip — state already initialized by dev-preflight + the Entry Dispatcher above.
         (STORY-658: legacy phase-init invocation removed; the dispatcher now owns
         state creation/resume decisions.)
       ELSE:
         devforgeai-validate phase-check ${STORY_ID} --from={prev} --to={phase_id}
         IF exit != 0: HALT

    2. LOAD: Read(file_path="phases/{phase_files[phase_id]}")

    3. EXECUTE: Follow every step in the phase file (EXECUTE-VERIFY-GATE triplets)
       - Each step's EXECUTE instruction tells you exactly what to do
       - Each step's VERIFY instruction tells you how to confirm it happened
       - Each step's RECORD instruction tells you what CLI command to call

    4. RECORD: devforgeai-validate phase-record ${STORY_ID} --phase={phase_id} --subagent={name}

    5. EXIT GATE:
       a. AUDIT GATE (precondition — Plan D / ADR-058):
          devforgeai-validate audit-gate ${STORY_ID} --phase={phase_id}
          IF exit != 0: HALT (audit infrastructure failure)
          See references/audit-gate.md for behavior matrix and recovery.
       b. PHASE COMPLETE:
          devforgeai-validate phase-complete ${STORY_ID} --phase={phase_id} --checkpoint-passed
          IF exit != 0: HALT (audit verdict failed OR other gate violation)
```

| Phase | Name | File |
|-------|------|------|
| 01 | Pre-Flight Validation | `phases/phase-01-preflight.md` |
| 02 | Test-First (Red) | `phases/phase-02-test-first.md` |
| 03 | Implementation (Green) | `phases/phase-03-implementation.md` |
| 04 | Refactoring | `phases/phase-04-refactoring.md` |
| 4.5 | AC Verification (Post-Refactor) | `phases/phase-04.5-ac-verification.md` |
| 05 | Integration Testing | `phases/phase-05-integration.md` |
| 5.5 | AC Verification (Post-Integration) | `phases/phase-05.5-ac-verification.md` |
| 06 | Deferral Challenge | `phases/phase-06-deferral.md` |
| 07 | DoD Update | `phases/phase-07-dod-update.md` |
| 08 | Git Workflow | `phases/phase-08-git-workflow.md` |
| 09 | Feedback Hook | `phases/phase-09-feedback.md` |
| 10 | Result Interpretation | `phases/phase-10-result.md` |

---

## Required Subagents Per Phase

| Phase | Required Subagents | Enforcement | Audit (Layer 9) |
|-------|-------------------|-------------|-----------------|
| 01 | git-validator, tech-stack-detector | BLOCKING | — |
| 02 | test-automator | BLOCKING | — |
| 03 | backend-architect OR frontend-developer, context-validator | BLOCKING | single, closed |
| 04 | refactoring-specialist, code-reviewer | BLOCKING | — |
| 4.5 | ac-compliance-verifier | BLOCKING | consensus_when_available, closed |
| 05 | integration-tester | BLOCKING | single, closed |
| 5.5 | ac-compliance-verifier | BLOCKING | consensus_when_available, closed |
| 06 | deferral-validator (if deferrals) | CONDITIONAL | single, open |
| 07 | (none) | N/A | single, closed |
| 08 | (none) | N/A | — |
| 09 | framework-analyst | BLOCKING | — |
| 10 | dev-result-interpreter | BLOCKING | — |

**Audit column**: per-phase audit policy from `audit-policy.yaml`. Format: `mode, fail_mode`. `—` means phase is not audited (e.g., process-glue or no implementation artifacts to verify).

**Deviation Protocol:** Any skip requires explicit user consent via AskUserQuestion. See `references/workflow-deviation-protocol.md`.

---

## Test File Immutability (RCA-046, RCA-047)

After Phase 02, test files are IMMUTABLE until Phase 05. Deterministic enforcement: `.claude/hooks/phase-gate-write.sh` exits 2 on test-file writes during phases 03 / 04 / 4.5 / 5.5 / 06–10. Recovery procedure when the hook fires: see **Phase Regression (Backward Transition)** below.

---

## Remediation Mode

When `$REMEDIATION_MODE == true`, Phases 02-10 execute with inline remediation-specific branches. The narrowed test scope (`$OPEN_REC_IDS`), code-change application (`$OPEN_REC_ENTRIES`), cycle closure, and qa-recommendations.md update are all invoked from within the normal phase files. See `references/qa-remediation-workflow.md` for the cross-phase flow narrative.

`$REMEDIATION_MODE` is set by one of two paths (depending on entry route):

1. **Via dev-preflight + Entry Dispatcher (STORY-658, default):** When `$NEXT_ACTION == "phase-cycle-start"`, the dispatcher executes `$NEXT_COMMAND` which opens a new cycle and sets `$REMEDIATION_MODE=true`. See `references/preflight/01.0-entry-dispatcher.md`.
2. **Via Phase 01 Step 01.9.6 (legacy / mid-workflow):** When entering remediation during a mid-workflow phase (rare), Step 01.9.6 in `references/preflight/01.9-qa-failures.md` opens the cycle. The dispatcher path supersedes this for fresh `/dev --fix` invocations against completed (phase 10) stories.

## Technical Debt Override Banner

If `$DEBT_OVERRIDE_BANNER == true`, display at start of each phase:
```
[DEBT OVERRIDE ACTIVE - Proceeding with elevated debt]
```

---

## State Persistence

**Location:** `devforgeai/workflows/${STORY_ID}-phase-state.json`
**Session Memory:** `.claude/memory/sessions/${STORY_ID}-session.md`
**References:** `references/memory-file-schema.md`, `references/memory-file-operations.md`

---

## Workflow Completion Validation

```
IF completed_count < 10: HALT "WORKFLOW INCOMPLETE - {completed_count}/10 phases"
IF completed_count == 10: "All 10 phases completed - Workflow validation passed"
```

IF iteration_count >= 4: Display "Approaching limit"
IF iteration_count >= max_iterations: HALT "Maximum iterations reached"

---

## Phase Regression (Backward Transition)

When a defect discovered in Phase 03+ requires returning to an earlier phase:

### Supported Backward Transitions

| From Phase | To Phase | Trigger | Authorized By |
|------------|----------|---------|---------------|
| 03 (Green) | 02 (Red) | Test infrastructure defect (not business logic) | test-folder-protection "Return to Phase 02" option |
| 04 (Refactor) | 02 (Red) | Test file needs structural changes | test-folder-protection "Return to Phase 02" option |

### Phase Regression Protocol

1. **User selects "Return to Phase 02"** from test-folder-protection AskUserQuestion
2. **Reset phase state:**
   ```bash
   devforgeai-validate phase-reset ${STORY_ID} --to=02
   ```
3. **Re-invoke test-automator** with context about the defect:
   ```
   Task(
     subagent_type="test-automator",
     prompt="Regenerate test files. Previous tests had defect: {defect_description}. Fix: {fix_description}. Preserve all test assertions and business logic."
   )
   ```
4. **Verify RED state** (tests must still fail for expected business logic reasons)
5. **Re-create red-phase checksum snapshot** (overwrite per BR-005)
6. **Resume forward** from Phase 03

### Constraints

- Phase regression requires explicit user approval (via test-folder-protection AskUserQuestion)
- Only test-automator may write test files during Phase 02 re-entry
- Red-phase snapshot MUST be regenerated after test-automator produces new files
- Phase regression is logged in story Implementation Notes under `### Phase Regressions`
- Maximum 2 regressions per story (prevent infinite loops)

### Fallback When `phase-reset` CLI Not Yet Implemented

If STORY-569 (`phase-reset` CLI command) is not yet implemented, the orchestrator performs the reset manually:

1. Read `devforgeai/workflows/${STORY_ID}-phase-state.json`
2. Edit `current_phase` value from current (e.g., `"03"`) to target (e.g., `"02"`)
3. Add entry to `regressions` array (create array if absent):
   ```json
   {"from": "03", "to": "02", "timestamp": "2026-03-03T00:00:00Z", "reason": "test infrastructure defect"}
   ```
4. Save file
5. Continue with Phase Regression Protocol step 3 (re-invoke test-automator)

---

## Success Criteria

- All tests pass (100% pass rate)
- Coverage meets thresholds (95%/85%/80%)
- Light QA validation passed
- No context file violations
- All AC implemented
- DoD validation passed
- Changes committed
- Story status = "Dev Complete"

---

## Treelint AST-Aware Search Integration

Phases 02-04 invoke Treelint-enabled subagents for semantic code analysis (40-80% token reduction). Automatic fallback to Grep when unavailable.

**Reference:** `references/treelint-integration.md` and `.claude/agents/references/treelint-search-patterns.md`

---

## Reference Files

### Phase Execution (phases/ directory)

| File | Phase |
|------|-------|
| phase-01-preflight.md | Pre-Flight Validation |
| phase-02-test-first.md | Test-First (TDD Red) |
| phase-03-implementation.md | Implementation (TDD Green) |
| phase-04-refactoring.md | Refactoring + Light QA |
| phase-04.5-ac-verification.md | AC Verification (Post-Refactor) |
| phase-05-integration.md | Integration Testing |
| phase-05.5-ac-verification.md | AC Verification (Post-Integration) |
| phase-06-deferral.md | Deferral Challenge |
| phase-07-dod-update.md | DoD Update |
| phase-08-git-workflow.md | Git Workflow |
| phase-09-feedback.md | Feedback Hook |
| phase-10-result.md | Result Interpretation |

### Supporting References (references/ directory)

The references/ tree carries one tier of live documentation plus an archive of supplementary material that no execution path reads.

**Live references (loaded at execution time or cited from a live consumer):**

| File | Loaded by |
|------|-----------|
| `references/ac-verification-workflow.md` | phase-04.5, phase-05.5 (direct `Read()`) |
| `references/ac-checklist-update-workflow.md` | transitive `Read()` |
| `references/technical-debt-register-workflow.md` | phase-06 + transitive `Read()` |
| `references/dod-update-workflow.md` | transitive `Read()` + agent prose |
| `references/dod-validation-checkpoint.md` | transitive `Read()` |
| `references/lock-file-coordination.md` | transitive `Read()` |
| `references/qa-remediation-workflow.md` | transitive `Read()` |
| `references/test-integrity-snapshot.md` | transitive `Read()` (STORY-502) |
| `references/tdd-patterns.md` | agent-side prose pointer (NOT the memory file under `.claude/memory/learning/tdd-patterns.md`) |
| `references/treelint-dependency-query.md` | agent-side prose pointer |
| `references/preflight/01.0-entry-dispatcher.md` | SKILL.md prose pointer (Phase State Initialization) |
| `references/preflight/01.9-qa-failures.md` | SKILL.md prose pointer (Remediation Mode) |
| `references/preflight/_index.md` | agent-side prose pointer |

**Archive:** `references/_archive/` — supplementary historical references absorbed during the spec-driven-dev → spec-driven-dev consolidation (ADR-039, 2026-03-18) that no execution path reads. Preserved in-tree for git history and human reference; safe to consult when context demands; **never `Read()` proactively**.

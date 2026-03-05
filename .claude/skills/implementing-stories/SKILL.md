---
name: implementing-stories
description: Implements user stories through Test-Driven Development (Red-Green-Refactor) while enforcing architectural constraints from six context files. Use when developing features from story specifications, building code that must comply with tech-stack.md and source-tree.md, or running TDD workflows. Automatically invokes architecture skill if context files are missing.
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
model: claude-opus-4-6
---

# Implementing Stories

Implement user stories using strict TDD (Red → Green → Refactor) while enforcing all 6 context file constraints.

**Context files are THE LAW:** tech-stack.md, source-tree.md, dependencies.md, coding-standards.md, architecture-constraints.md, anti-patterns.md

**If ambiguous or conflicts detected → HALT and use AskUserQuestion**

---

## Execution Model

This skill expands inline. After invocation, YOU execute each phase sequentially. Do not wait passively, ask permission, or offer execution options — proceed directly to Phase State Initialization.

### Immediate Execution Checkpoint

**YOU HAVE JUST INVOKED THIS SKILL. EXECUTE PHASE STATE INITIALIZATION NOW.**

**Self-Check (if ANY box is true = VIOLATION):**

```
- [ ] Stopping to ask about token budget
- [ ] Stopping to ask about time constraints
- [ ] Stopping to ask about approach/scope
- [ ] Stopping to offer execution options
- [ ] Waiting passively for results
- [ ] Asking "should I execute this?"
```

**IF any box checked:**

```
EXECUTION MODEL VIOLATION DETECTED

You are stopping to ask for permission instead of executing.

Per CLAUDE.md: "There are no time constraints", "Your context window is plenty big", "Focus on quality"

RECOVERY: Go directly to Phase State Initialization now. Do not ask questions.
```

---

## Parameter Extraction

Extract story ID from conversation context (YAML frontmatter, context markers, or natural language). See `references/parameter-extraction.md` for the extraction algorithm.

---

## Command Integration

This skill is invoked by `/dev` and `/resume-dev` commands. Commands parse arguments and pass structured context markers:

| Context Marker | Set By | Description |
|----------------|--------|-------------|
| `$STORY_ID` | /dev, /resume-dev | Story identifier (STORY-NNN) |
| `$FORCE_FLAG` | /dev | `--force` flag — bypass dependency checks |
| `$REMEDIATION_MODE` | /dev | `--fix` flag or auto-detected from gaps.json |
| `$GAPS_AUTO_DETECTED` | /dev | True if gaps.json was auto-detected |
| `$IGNORE_DEBT_FLAG` | /dev | `--ignore-debt-threshold` flag |
| `$RESUME_MODE` | /resume-dev | "manual" or "auto" |
| `$PHASE_NUM` | /resume-dev | Phase number to resume from (0-7) |

Commands handle only: argument parsing, flag extraction, banner display, result display.
Skill handles all business logic: validation, orchestration, subagent invocation, state management.

---

## Required Subagents Per Phase

| Phase | Required Subagents | Enforcement |
|-------|-------------------|-------------|
| 01 | git-validator, tech-stack-detector | BLOCKING |
| 02 | test-automator | BLOCKING |
| 03 | backend-architect OR frontend-developer, context-validator | BLOCKING |
| 04 | refactoring-specialist, code-reviewer | BLOCKING |
| 4.5 | ac-compliance-verifier | BLOCKING |
| 05 | integration-tester | BLOCKING |
| 5.5 | ac-compliance-verifier | BLOCKING |
| 06 | deferral-validator (if deferrals) | CONDITIONAL |
| 07 | (none — file operations) | N/A |
| 08 | (none — git operations) | N/A |
| 09 | framework-analyst | BLOCKING |
| 10 | dev-result-interpreter | BLOCKING |

BLOCKING = MANDATORY (cannot omit). CONDITIONAL = may skip with documented reason.

**Workflow Deviation Protocol:** Any phase skip, subagent omission, or out-of-sequence execution requires explicit user consent via AskUserQuestion. See `references/workflow-deviation-protocol.md`.

---

## Test File Immutability (RCA-046, RCA-047)

After Phase 02 creates tests, test files are **IMMUTABLE** until Phase 05 (integration-tester only). Any other modification requires returning to Phase 02 and re-invoking test-automator.

**ANTI-RATIONALIZATION:** If test checksums mismatch at any point, HALT immediately. Do not explain away mismatches using environmental factors (line endings, WSL, encoding, git autocrlf, platform differences). The snapshot was computed in the same environment — a mismatch IS test tampering by definition, regardless of the reason.

**Back-to-Red Protocol:** If tests have bugs discovered during Phase 03 or 04:
1. Mark current phase incomplete
2. Return to Phase 02
3. Re-invoke test-automator with bug context
4. Create new test integrity snapshot
5. Resume from Phase 03

**References:** RCA-046, RCA-047, `.claude/rules/workflow/test-folder-protection.md`

---

## Phase Summary

| Phase | Name | Phase File |
|-------|------|------------|
| 01 | Pre-Flight Validation | `phases/phase-01-preflight.md` |
| 02 | Test-First (Red) | `phases/phase-02-test-first.md` |
| 03 | Implementation (Green) | `phases/phase-03-implementation.md` |
| 04 | Refactoring | `phases/phase-04-refactoring.md` |
| 04.5 | AC Verification (Post-Refactor) | `phases/phase-04.5-ac-verification.md` |
| 05 | Integration Testing | `phases/phase-05-integration.md` |
| 05.5 | AC Verification (Post-Integration) | `phases/phase-05.5-ac-verification.md` |
| 06 | Deferral Challenge | `phases/phase-06-deferral.md` |
| 07 | DoD Update | `phases/phase-07-dod-update.md` |
| 08 | Git Workflow | `phases/phase-08-git-workflow.md` |
| 09 | Feedback Hook | `phases/phase-09-feedback.md` |
| 10 | Result Interpretation | `phases/phase-10-result.md` |

---

## Phase State Initialization [MANDATORY FIRST]

```bash
devforgeai-validate phase-init ${STORY_ID} --project-root=.
```

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | New workflow | State file created. Set CURRENT_PHASE = "01". |
| 1 | Existing workflow | Resume. Run `devforgeai-validate phase-status ${STORY_ID}` to get CURRENT_PHASE. |
| 2 | Invalid story ID | HALT. Must match STORY-XXX pattern. |
| 127 | CLI not installed | Continue without enforcement (backward compatibility). |

**Initialize iteration counter:**
```
iteration_count = 1        # TDD cycle iterations (for Phase 06 resumption)
max_iterations = 5         # Maximum before blocking
# If resuming: read iteration_count from phase-state.json
```

---

## Task-Gate Integration Pattern [MANDATORY]

**ENFORCEMENT:** Phase completion status in TaskUpdate is GATED by CLI validation.

**5-Step Gate Enforcement Pattern:**

```
FOR each phase N in [01..10]:

  1. Mark phase "in_progress" at phase start
     TaskUpdate(taskId=phase_N_task_id, status="in_progress")
     Display: "Phase {N}/{10}: {phase_name}"

  2. Execute all phase steps
     Read(file_path="phases/phase-{N}-{name}.md")
     [Execute all steps from phase file]

  3. Call CLI gate: devforgeai-validate phase-complete
     Bash(command="devforgeai-validate phase-complete ${STORY_ID} --phase={N} --checkpoint-passed")

  4. IF gate exit code 0: Mark phase "completed"
     TaskUpdate(taskId=phase_N_task_id, status="completed")
     Display: "✓ Phase {N} complete"
     Proceed to Phase N+1

  5. IF gate exit code != 0: Keep "in_progress", HALT
     Display: "❌ Phase {N} gate failed - see error message"
     HALT (keep phase N as "in_progress")
```

**CRITICAL RULES for TaskUpdate Completion:**

- ❌ **CANNOT** mark phase "completed" without gate exit code 0
- ❌ **CANNOT** start Phase X+1 while Phase X shows "in_progress" or "pending"
- ✅ Phase **MUST** remain "in_progress" until CLI gate passes
- ✅ CLI gate **MUST** be called before TaskUpdate status change
- ✅ **Never** mark completed without gate call - gate failure = HALT
- ✅ Gate failure = HALT (address issues before retry)

---

## Session State Persistence

**Cross-Session Recovery:** Phase state and workflow progress persist to `.claude/memory/sessions/` for recovery after API errors, crashes, or session restarts.

**Capabilities:**
- Resume from last completed phase
- Restore iteration counters and phase variables
- Maintain observation history across sessions
- Backward compatibility with existing workflows

**Reference Files:**
- `references/memory-file-schema.md` - Phase state JSON schema and field definitions
- `references/memory-file-operations.md` - Read/write operations, recovery patterns, error handling

**Location:** `devforgeai/workflows/${STORY_ID}-phase-state.json`

---

## Treelint AST-Aware Search Integration

Phases 02-04 invoke Treelint-enabled subagents for semantic code analysis (40-80% token reduction). Automatic fallback to Grep when unavailable.

**Reference:** `references/treelint-integration.md` and `.claude/agents/references/treelint-search-patterns.md`

---

## Phase Orchestration Loop

Execute phases sequentially, loading each phase file on demand:

```
FOR phase_num in range(CURRENT_PHASE, 11):
    phase_id = f"{phase_num:02d}"

    # 1. Load phase file (progressive loading)
    Read(file_path="phases/{phase_files[phase_id]}")

    # 2. Execute Entry Gate
    devforgeai-validate phase-check ${STORY_ID} --from={prev} --to={phase_id}
    IF exit code != 0: HALT

    # 3. Execute phase workflow (invoke required subagents, validate checkpoint)

    # 4. Capture observations for phases 02-08
    #    See references/observation-capture.md for schema

    # 5. Record subagent invocations
    devforgeai-validate phase-record ${STORY_ID} --phase={phase_id} --subagent={name}

    # 6. Execute Exit Gate
    devforgeai-validate phase-complete ${STORY_ID} --phase={phase_id} --checkpoint-passed
    IF exit code != 0: HALT
```

**Phase file map:**
```python
phase_files = {
    "01": "phase-01-preflight.md",
    "02": "phase-02-test-first.md",
    "03": "phase-03-implementation.md",
    "04": "phase-04-refactoring.md",
    "4.5": "phase-04.5-ac-verification.md",
    "05": "phase-05-integration.md",
    "5.5": "phase-05.5-ac-verification.md",
    "06": "phase-06-deferral.md",
    "07": "phase-07-dod-update.md",
    "08": "phase-08-git-workflow.md",
    "09": "phase-09-feedback.md",
    "10": "phase-10-result.md"
}
```

### Phase Completion Display

After each phase, display:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Phase NN/10: [Phase Name] - Mandatory Steps Completed
  TDD Iteration: X/5 | Observations: N captured
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

IF iteration_count >= 4: Display "⚠️ Approaching limit"
IF iteration_count >= max_iterations: HALT "Maximum iterations reached"

### Remediation Mode

After Phase 01, check `$REMEDIATION_MODE` flag:
```
IF $REMEDIATION_MODE == true:
    Read(file_path="references/qa-remediation-workflow.md")
    SKIP Phases 02-08 → GOTO Phase 09
ELSE:
    Continue with Phase 02
```

### Pre-Phase Planning (Optional)

If `devforgeai/config/pre-phase-planning.yaml` exists and is enabled, execute pre-phase planning before phases 02-05. See `references/pre-phase-planning.md`.

### Technical Debt Override Banner

If `$DEBT_OVERRIDE_BANNER == true` (set in Phase 01 Step 10), display at start of each phase:
```
┌──────────────────────────────────────────────────────────────┐
│ ⚠️  DEBT OVERRIDE ACTIVE - Proceeding with elevated debt     │
└──────────────────────────────────────────────────────────────┘
```

---

## Workflow Completion Validation

Before displaying final result, verify all phases completed:

```
IF completed_count < 10:
    Display: "❌ WORKFLOW INCOMPLETE - Cannot declare completion"
    Display: "Phases completed: {completed_count}/10"
    HALT

IF completed_count == 10:
    Display: "✓ All 10 phases completed - Workflow validation passed"
    Proceed to display result
```

---

## Phase Resumption

When workflow stops incomplete:

1. Check phase state: `devforgeai-validate phase-status STORY-XXX`
2. Load phase file for current phase
3. Execute remaining phases from current to 10
4. Run Workflow Completion Validation

| Scenario | Action |
|----------|--------|
| Phase state exists | Resume from current phase |
| No prior execution evidence | Fresh start |
| Git conflicts | Fresh start after resolving |

---

## Success Criteria

- [ ] All tests pass (100% pass rate)
- [ ] Coverage meets thresholds (95%/85%/80%)
- [ ] Light QA validation passed
- [ ] No context file violations
- [ ] All AC implemented
- [ ] Code follows coding-standards.md
- [ ] No anti-patterns from anti-patterns.md
- [ ] DoD validation passed
- [ ] Changes committed (or file-tracked)
- [ ] Story status = "Dev Complete"

---

## When to Use

**Prerequisites:** Git repo (recommended), 6 context files, story file
**Git modes:** Full workflow (with Git) OR file-based tracking (without Git) — auto-detects
**Invoked by:** `/dev [STORY-ID]`, devforgeai-orchestration, or manual skill call

**Integration:**
- **From:** devforgeai-story-creation (story+AC), designing-systems (context files)
- **To:** devforgeai-qa (validation), devforgeai-release (deployment)
- **Auto-invokes:** designing-systems (if missing), devforgeai-qa (light mode)

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

| File | Purpose |
|------|---------|
| parameter-extraction.md | Story ID extraction algorithm |
| preflight-validation.md | Phase 01 detailed workflow |
| tdd-red-phase.md | Phase 02 detailed workflow |
| test-integrity-snapshot.md | Red-phase test checksum snapshot (STORY-502) |
| tdd-green-phase.md | Phase 03 detailed workflow |
| tdd-refactor-phase.md | Phase 04 detailed workflow |
| ac-verification-workflow.md | AC Verification for Phase 4.5/5.5 |
| ac-checklist-update-workflow.md | AC checklist update procedures |
| integration-testing.md | Phase 05 detailed workflow |
| phase-06-deferral-challenge.md | Phase 06 detailed workflow |
| dod-update-workflow.md | Phase 07 detailed workflow |
| git-workflow-conventions.md | Phase 08 detailed workflow |
| tdd-patterns.md | Comprehensive TDD guidance |
| qa-remediation-workflow.md | Remediation mode workflow |
| resume-detection.md | Resume workflow detection and pre-flight (STORY-459) |
| observation-capture.md | Inline observation schema (STORY-400) |
| workflow-deviation-protocol.md | Deviation consent protocol (RCA-019) |
| pre-phase-planning.md | Optional pre-phase planning (STORY-FEEDBACK-005) |
| phase-transition-validation.md | CLI validation call reference (STORY-153) |
| memory-file-schema.md | Memory file YAML schema (STORY-303) |
| memory-file-operations.md | Memory file read/write operations (STORY-303) |
| ambiguity-protocol.md | When to ask user questions |

---

## Rollback Recovery

1. Check phase: `devforgeai-validate phase-status STORY-XXX`
2. Review phase file for checkpoint requirements
3. Fix blocking issue
4. Re-run `/dev STORY-XXX` — resumes from current phase

**State file:** `devforgeai/workflows/STORY-XXX-phase-state.json`

**CLI reference:** See `references/phase-transition-validation.md` for full CLI command reference and exit codes.

**Change log:** See `MIGRATION-NOTES.md` for version history.

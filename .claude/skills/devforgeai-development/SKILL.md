---
name: devforgeai-development
description: Implement features using Test-Driven Development (TDD) while enforcing architectural constraints from context files. Use when implementing user stories, building features, or writing code that must comply with tech-stack.md, source-tree.md, and dependencies.md. Automatically invokes devforgeai-architecture skill if context files are missing.
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
model: claude-opus-4-5-20251101
---

# DevForgeAI Development Skill

Implement user stories using Test-Driven Development while enforcing architectural constraints to prevent technical debt.

**Phase Enforcement Active:** This skill uses progressive phase loading with CLI validation gates.

---

## Execution Model: This Skill Expands Inline

**After invocation, YOU (Claude) execute these instructions phase by phase.**

**When you invoke this skill:**
1. This SKILL.md content is now in your conversation
2. You execute each phase sequentially via phase files
3. You display results as you work through phases
4. CLI gates block progression if phases incomplete

**Do NOT:**
- Wait passively for skill to "return results"
- Assume skill is executing elsewhere
- Stop workflow after invocation
- Stop to ask about token budget (CLAUDE.md: "context window is plenty big")
- Stop to ask about time constraints (CLAUDE.md: "no time constraints")
- Stop to ask about scope/approach (execute as documented)
- Offer execution options (just execute the workflow)

**CRITICAL:** Skill invocation means "execute now" - not "ask if you should execute"

**Proceed to Phase State Initialization section below and begin execution.**

---

## Immediate Execution Checkpoint

**YOU HAVE JUST INVOKED THIS SKILL. EXECUTE PHASE STATE INITIALIZATION NOW.**

**BEFORE PROCEEDING, VERIFY YOU ARE NOT:**

```
Self-Check (Check boxes if TRUE - any checked = VIOLATION):

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

Per CLAUDE.md:
- "There are no time constraints"
- "Your context window is plenty big"
- "Focus on quality"

RECOVERY: Go directly to Phase 0 now. Do not ask questions.
```

**Reference:** See CLAUDE.md for complete execution model guidance.

---

## Parameter Extraction

This skill extracts the story ID from conversation context (loaded story file YAML frontmatter, context markers, or natural language).

**See `references/parameter-extraction.md` for complete extraction algorithm.**

---

## Workflow Execution Checklist

**After parameter extraction, BEFORE Phase 01, create execution tracker:**

**Initialize iteration counter:**
```
iteration_count = 1  # Track TDD cycle iterations (for Phase 06 resumption)
```

TodoWrite(
  todos=[
    {content: "Execute Phase 01: Pre-Flight Validation", status: "pending", activeForm: "Executing Phase 01 Pre-Flight Validation"},
    {content: "Execute Phase 02: Test-First Design (test-automator)", status: "pending", activeForm: "Executing Phase 02 test-automator"},
    {content: "Execute Phase 02 Step 4: Tech Spec Coverage Validation", status: "pending", activeForm: "Validating Tech Spec Coverage"},
    {content: "Execute Phase 03 Step 1-2: backend-architect OR frontend-developer", status: "pending", activeForm: "Executing backend/frontend architect"},
    {content: "Execute Phase 03 Step 3: context-validator", status: "pending", activeForm: "Validating context constraints"},
    {content: "Execute Phase 04 Step 1-2: refactoring-specialist", status: "pending", activeForm: "Executing refactoring specialist"},
    {content: "Execute Phase 04 Step 3: code-reviewer", status: "pending", activeForm: "Executing code reviewer"},
    {content: "Execute Phase 04 Step 5: Light QA", status: "pending", activeForm: "Executing Light QA validation"},
    {content: "Execute Phase 05: Integration Testing (integration-tester)", status: "pending", activeForm: "Executing integration testing"},
    {content: "Execute Phase 06: Deferral Challenge", status: "pending", activeForm: "Executing deferral challenge"},
    {content: "Execute Phase 07: DoD Update (Bridge)", status: "pending", activeForm: "Updating DoD checkboxes"},
    {content: "Execute Phase 08: Git Workflow", status: "pending", activeForm: "Executing git workflow"},
    {content: "Execute Phase 09: Feedback Hooks", status: "pending", activeForm: "Executing feedback hooks"},
    {content: "Execute Phase 10 Step 10.1: dev-result-interpreter", status: "pending", activeForm: "Interpreting dev results"}
  ]
)

**Usage:** Mark phase "in_progress" when starting, "completed" when checkpoint passes.

---

## Purpose

Implement features following strict TDD workflow (Red → Green → Refactor) while enforcing all 6 context file constraints.

**Context files are THE LAW:** tech-stack.md, source-tree.md, dependencies.md, coding-standards.md, architecture-constraints.md, anti-patterns.md

**If ambiguous or conflicts detected → HALT and use AskUserQuestion**

---

## When to Use This Skill

**Prerequisites:** Git repo (recommended), context files (6), story file

**Git modes:** Full workflow (with Git) OR file-based tracking (without Git) - auto-detects

**Invoked by:** `/dev [STORY-ID]` command, devforgeai-orchestration skill, manual skill call

---

## Phase State Initialization [MANDATORY FIRST]

**Initialize phase tracking before any TDD work:**

```bash
# Initialize state file for this story
devforgeai-validate phase-init ${STORY_ID} --project-root=.
```

**Handle return codes:**
```
IF exit_code == 0:
    # New workflow - state file created
    Display: "✓ Phase state initialized for ${STORY_ID}"
    CURRENT_PHASE = "01"
    GOTO Phase Orchestration Loop

IF exit_code == 1:
    # Existing workflow - resume from current phase
    Display: "📋 Resuming existing workflow for ${STORY_ID}"

    # Get current phase status
    devforgeai-validate phase-status ${STORY_ID}

    # Parse output to determine CURRENT_PHASE
    CURRENT_PHASE = parse from output

    Display: "  Current phase: ${CURRENT_PHASE}"
    GOTO Phase Orchestration Loop (starting at CURRENT_PHASE)

IF exit_code == 2:
    # Invalid story ID
    Display: "❌ Invalid story ID: ${STORY_ID}"
    Display: "  Story ID must match pattern STORY-XXX (e.g., STORY-001)"
    HALT workflow
```

**Backward Compatibility Warning:**
```
IF devforgeai-validate command not found (exit code 127):
    Display: "⚠️  Warning: Phase enforcement CLI not installed"
    Display: "    To enable enforcement, run: pip install devforgeai-validate"
    Display: "    Continuing workflow without enforcement (backward compatibility mode)"
    # Continue workflow without enforcement
```

---

## Phase Orchestration Loop

**Execute phases sequentially, loading each phase file on demand:**

```
FOR phase_num in range(CURRENT_PHASE, 11):
    phase_id = f"{phase_num:02d}"

    # 1. Determine phase file
    phase_files = {
        "01": "phase-01-preflight.md",
        "02": "phase-02-test-first.md",
        "03": "phase-03-implementation.md",
        "04": "phase-04-refactoring.md",
        "05": "phase-05-integration.md",
        "06": "phase-06-deferral.md",
        "07": "phase-07-dod-update.md",
        "08": "phase-08-git-workflow.md",
        "09": "phase-09-feedback.md",
        "10": "phase-10-result.md"
    }

    # 2. Load phase file (progressive loading)
    Read(file_path=f".claude/skills/devforgeai-development/phases/{phase_files[phase_id]}")

    # 3. Execute phase content
    #    - Phase file contains Entry Gate (CLI check)
    #    - Phase file contains workflow steps
    #    - Phase file contains Exit Gate (CLI complete)

    # 4. Entry Gate validates previous phase complete
    #    Entry gate calls: devforgeai-validate phase-check ${STORY_ID} --from={prev} --to={phase_id}
    #    If blocked, workflow HALTs

    # 5. Execute phase workflow (from phase file content)
    #    Each phase has specific subagents to invoke
    #    Update TodoWrite status as phases execute

    # 6. Exit Gate records completion
    #    Exit gate calls: devforgeai-validate phase-complete ${STORY_ID} --phase={phase_id} --checkpoint-passed
    #    If fails, workflow HALTs

    # 7. Record subagent invocations (automatic)
    #    After each Task(), record: devforgeai-validate phase-record ${STORY_ID} --phase={phase_id} --subagent={name}
```

---

## Phase File Structure

Each phase file in `phases/` directory contains:

```markdown
# Phase NN: [Phase Name]

**Entry Gate:**
devforgeai-validate phase-check ${STORY_ID} --from={N-1} --to={N}
# Exit code 0: Proceed
# Exit code 1: Previous phase incomplete - HALT
# Exit code 2: Missing subagents - HALT

---

## Phase Workflow
[Specific phase steps, subagent invocations, validations]

---

## Validation Checkpoint
[Checklist of what must be verified]

---

**Exit Gate:**
devforgeai-validate phase-complete ${STORY_ID} --phase={N} --checkpoint-passed
# Exit code 0: Phase complete, proceed to next
# Exit code 1: Cannot complete - HALT
```

---

## Remediation Mode Decision Point

**After Phase 01 completes, check `$REMEDIATION_MODE` flag:**

```
IF $REMEDIATION_MODE == true:
    # gaps.json exists from previous QA failure
    Display: "🔧 REMEDIATION MODE ACTIVE"

    # Load remediation workflow
    Read(file_path=".claude/skills/devforgeai-development/references/qa-remediation-workflow.md")

    # Execute targeted phases (2R, 3R, 4R, 5R, 6R, 8R)
    # These replace normal Phases 02-08 with targeted versions

    SKIP: Normal TDD Phases 02-08
    GOTO: Phase 09 (Feedback Hook) after remediation

ELSE:
    # Normal TDD workflow
    Continue with Phase 02
```

---

## Required Subagents Per Phase

| Phase | Required Subagents | Enforcement |
|-------|-------------------|-------------|
| 01 | git-validator, tech-stack-detector | BLOCKING |
| 02 | test-automator | BLOCKING |
| 03 | backend-architect OR frontend-developer, context-validator | BLOCKING |
| 04 | refactoring-specialist, code-reviewer | BLOCKING |
| 05 | integration-tester | BLOCKING |
| 06 | deferral-validator (if deferrals) | CONDITIONAL |
| 07 | (none - file operations) | N/A |
| 08 | (none - git operations) | N/A |
| 09 | (none - hook invocation) | N/A |
| 10 | dev-result-interpreter | BLOCKING |

**Note:** Phase files contain subagent invocation templates.

---

## Phase Transition Validation Calls (STORY-153)

**Validation calls are required at every phase transition.** See `devforgeai/config/validation-call-locations.yaml` for the complete mapping.

**Phase-check calls at each transition (9 total):**

| From | To | Command |
|------|-----|---------|
| 01 | 02 | `devforgeai-validate phase-check STORY-XXX --from=01 --to=02` |
| 02 | 03 | `devforgeai-validate phase-check STORY-XXX --from=02 --to=03` |
| 03 | 04 | `devforgeai-validate phase-check STORY-XXX --from=03 --to=04` |
| 04 | 05 | `devforgeai-validate phase-check STORY-XXX --from=04 --to=05` |
| 05 | 06 | `devforgeai-validate phase-check STORY-XXX --from=05 --to=06` |
| 06 | 07 | `devforgeai-validate phase-check STORY-XXX --from=06 --to=07` |
| 07 | 08 | `devforgeai-validate phase-check STORY-XXX --from=07 --to=08` |
| 08 | 09 | `devforgeai-validate phase-check STORY-XXX --from=08 --to=09` |
| 09 | 10 | `devforgeai-validate phase-check STORY-XXX --from=09 --to=10` |

**Complete-phase calls at phase end (10 total):**

Per AC#3, use `devforgeai-validate complete-phase` (alias: `phase-complete`):

| Phase | Command |
|-------|---------|
| 01 | `devforgeai-validate complete-phase STORY-XXX --phase=01 --checkpoint-passed` |
| 02 | `devforgeai-validate complete-phase STORY-XXX --phase=02 --checkpoint-passed` |
| 03 | `devforgeai-validate complete-phase STORY-XXX --phase=03 --checkpoint-passed` |
| 04 | `devforgeai-validate complete-phase STORY-XXX --phase=04 --checkpoint-passed` |
| 05 | `devforgeai-validate complete-phase STORY-XXX --phase=05 --checkpoint-passed` |
| 06 | `devforgeai-validate complete-phase STORY-XXX --phase=06 --checkpoint-passed` |
| 07 | `devforgeai-validate complete-phase STORY-XXX --phase=07 --checkpoint-passed` |
| 08 | `devforgeai-validate complete-phase STORY-XXX --phase=08 --checkpoint-passed` |
| 09 | `devforgeai-validate complete-phase STORY-XXX --phase=09 --checkpoint-passed` |
| 10 | `devforgeai-validate complete-phase STORY-XXX --phase=10 --checkpoint-passed` |

**Record-subagent calls after Task invocations:**

After each `Task(subagent_type="...")` invocation completes:
```bash
devforgeai-validate record-subagent STORY-XXX --phase=NN --subagent=SUBAGENT_NAME
```

**Exit code handling:** Non-zero exit code = HALT workflow (see CLI Commands Reference below for exit codes).

---

## Phase 00: Initialization

Phase state file creation via `devforgeai-validate phase-init` (or `devforgeai-validate init-state` per AC#4).

## Phase 01: Pre-Flight

Context validation, Git status, story loading. Includes RCA-008 user consent checkpoints (Steps 0.1.5-0.1.6) for git operations affecting >10 files. Subagents: git-validator (with enhanced file analysis), tech-stack-detector.

## Phase 02: Test-First (Red)

Write failing tests from acceptance criteria. Subagents: test-automator.

## Phase 03: Implementation (Green)

Implement minimal code to pass tests. Subagents: backend-architect OR frontend-developer, context-validator.

## Phase 04: Refactoring

Improve code quality without changing behavior. Subagents: refactoring-specialist, code-reviewer.

## Phase 05: Integration Testing

Verify cross-component interactions. Subagents: integration-tester.

## Phase 06: Deferral Challenge

Validate any deferred items have proper justification. Subagents: deferral-validator (conditional).

## Phase 07: DoD Update

Update Definition of Done checkboxes in story file.

## Phase 08: Git Workflow

Commit changes with conventional commit message.

## Phase 09: Feedback Hook

Trigger post-dev feedback collection if hooks enabled.

## Phase 10: Result Interpretation

Generate workflow result summary. Subagents: dev-result-interpreter.

---

## Complete Workflow Execution Map

```
START
  ↓
Phase State Initialization (devforgeai-validate phase-init)
  ↓
┌─── RESUME CHECK ───┐
│ IF state exists:   │
│   Resume from      │
│   current_phase    │
└────────────────────┘
  ↓
FOR each phase 01-10:
  ├─ Load phase file (Read)
  ├─ Execute Entry Gate (CLI phase-check)
  │   └─ IF blocked: HALT
  ├─ Execute Phase Workflow
  │   ├─ Invoke required subagents
  │   ├─ Record subagent invocations
  │   └─ Validate checkpoint
  └─ Execute Exit Gate (CLI phase-complete)
      └─ IF fails: HALT
  ↓
Phase 10 Complete → Story Status = "Dev Complete"
  ↓
END
```

---

## Integration Points

**From:** devforgeai-story-creation (story+AC), devforgeai-architecture (context files)
**To:** devforgeai-qa (validation), devforgeai-release (deployment)
**Auto-invokes:** devforgeai-architecture (if missing), devforgeai-qa (light mode), devforgeai-story-creation (deferrals)

---

## Reference Files

Load on-demand during workflow execution:

### Core Workflow (in phases/ directory)
- **phase-01-preflight.md** - Pre-Flight Validation
- **phase-02-test-first.md** - Test-First Design (TDD Red)
- **phase-03-implementation.md** - Implementation (TDD Green)
- **phase-04-refactoring.md** - Refactoring + Light QA
- **phase-05-integration.md** - Integration Testing
- **phase-06-deferral.md** - Deferral Challenge
- **phase-07-dod-update.md** - DoD Update (Bridge)
- **phase-08-git-workflow.md** - Git Workflow
- **phase-09-feedback.md** - Feedback Hook
- **phase-10-result.md** - Result Interpretation

### Supporting References (in references/ directory)
- **parameter-extraction.md** - Story ID extraction
- **preflight-validation.md** - Phase 01 detailed workflow (includes RCA-008 Steps 0.1.5-0.1.6 for user consent)
- **tdd-red-phase.md** - Phase 02 detailed workflow
- **tdd-green-phase.md** - Phase 03 detailed workflow
- **tdd-refactor-phase.md** - Phase 04 detailed workflow
- **integration-testing.md** - Phase 05 detailed workflow
- **phase-06-deferral-challenge.md** - Phase 06 detailed workflow
- **dod-update-workflow.md** - Phase 07 detailed workflow
- **git-workflow-conventions.md** - Phase 08 detailed workflow (includes RCA-008 Git Stash Safety Protocol)
- **tdd-patterns.md** - Comprehensive TDD guidance
- **ambiguity-protocol.md** - When to ask user questions

### Validation Call Configuration (STORY-153)
- **validation-call-locations.yaml** - Phase-to-validation mapping at `devforgeai/config/validation-call-locations.yaml`

### Change Log Integration (STORY-152)
- **changelog-update-guide.md** - Shared reference at `.claude/references/changelog-update-guide.md`

**Changelog Entry Authors by Phase:**
- Phase 02 Red Test-First: `claude/test-automator` for Change Log entries
- Phase 03 Green Implementation: `claude/backend-architect` or `claude/frontend-developer` for changelog
- Phase 04 Refactor: `claude/refactoring-specialist`
- Phase 05 Integration: `claude/integration-tester`
- Phase 07 DoD: `claude/opus`

**Example Edit() for appending changelog entry:**
```python
Edit(
    file_path="devforgeai/specs/Stories/{STORY_ID}.story.md",
    old_string="| {last_entry} |",
    new_string="| {last_entry} |\n| {date} | claude/test-automator | Red (Phase 02) | Tests generated | tests/*.sh |"
)
```

---

## CLI Commands Reference

**Phase State Management:**
```bash
# Initialize state file for story
devforgeai-validate phase-init STORY-XXX --project-root=.

# Check if phase transition is allowed
devforgeai-validate phase-check STORY-XXX --from=01 --to=02

# Mark phase as complete
devforgeai-validate phase-complete STORY-XXX --phase=02 --checkpoint-passed

# Get current phase status
devforgeai-validate phase-status STORY-XXX

# Record subagent invocation
devforgeai-validate phase-record STORY-XXX --phase=02 --subagent=test-automator
```

**Exit Codes:**
| Code | Meaning |
|------|---------|
| 0 | Success / Allowed |
| 1 | State exists (resume) / Previous phase incomplete |
| 2 | Invalid story ID / Missing required subagents |
| 3 | Cannot skip phases |

---

## Success Criteria

This skill succeeds when:

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
- [ ] All 10 phases completed in state file

**The goal: Zero technical debt from wrong assumptions, fully tested features that comply with architectural decisions.**

---

## Rollback Recovery

If workflow fails mid-execution:

1. Check current phase: `devforgeai-validate phase-status STORY-XXX`
2. Review phase file for checkpoint requirements
3. Fix blocking issue
4. Re-run `/dev STORY-XXX` - will resume from current phase

**State file location:** `devforgeai/workflows/STORY-XXX-phase-state.json`

---

## Migration Notes

This skill was refactored from a monolithic 1240-line file to:
- **Thin orchestrator:** ~400 lines (this file)
- **10 phase files:** ~100 lines each
- **CLI enforcement:** phase_state.py module

Backup of original: `SKILL.md.backup-1240-lines`

**Benefits:**
- Progressive loading (load only needed phase)
- CLI enforcement (blocking gates)
- State persistence (resume from any phase)
- Audit trail (subagent invocations recorded)

---

## Change Log

| Date | Change | Reference |
|------|--------|-----------|
| 2025-11-13 | Added RCA-008 git safety enhancements: user consent checkpoint (Step 0.1.5), stash warning workflow (Step 0.1.6), smart stash strategy, git-validator file analysis (Phase 2.5) | RCA-008 |

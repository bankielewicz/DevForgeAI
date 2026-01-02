---
id: STORY-207
title: Integrate TodoWrite with CLI Validation Gates
type: enhancement
epic: EPIC-033
priority: HIGH
points: 2
status: Backlog
created: 2025-01-01
source: RCA-018 REC-2
depends_on: []
---

# STORY-207: Integrate TodoWrite with CLI Validation Gates

## User Story

**As a** DevForgeAI user running the /dev workflow,
**I want** the TodoWrite status updates integrated with CLI validation gates,
**So that** phases can only be marked "completed" after the gate validates phase completion.

## Background

RCA-018 identified that the TodoWrite list is "passive tracking" - Claude can mark phases complete without actually executing mandatory steps. While CLI validation gates now exist (superseding RCA-018 REC-1's inline checkpoints), the TodoWrite updates are not formally integrated with these gates.

**Source RCA:** `devforgeai/RCA/RCA-018-development-skill-phase-completion-skipping.md`

**Current State:**
- CLI gates exist: `devforgeai-validate phase-ready` and `devforgeai-validate phase-complete`
- TodoWrite creates execution tracker at workflow start
- No formal integration between gates and TodoWrite

**Desired State:**
- TodoWrite "completed" status ONLY after CLI gate passes
- TodoWrite "in_progress" status set at phase start
- Clear enforcement pattern documented in SKILL.md

## Acceptance Criteria

### AC-1: TodoWrite Status Tied to CLI Gate

**Given** a phase has a CLI validation gate
**When** Claude attempts to mark the phase "completed" in TodoWrite
**Then** the CLI gate `devforgeai-validate phase-complete` MUST have returned exit code 0

---

### AC-2: Enforcement Pattern Documented in SKILL.md

**Given** the devforgeai-development SKILL.md workflow documentation
**When** Claude reads the TodoWrite usage section
**Then** the text includes explicit enforcement pattern:
```
1. Mark phase "in_progress" at phase start
2. Execute all phase steps
3. Call CLI gate: devforgeai-validate phase-complete
4. IF gate exit code 0: Mark phase "completed"
5. IF gate exit code != 0: Keep "in_progress", HALT
```

---

### AC-3: No Premature Completion Marking

**Given** a phase is being executed
**When** Claude reaches the end of phase steps but hasn't called CLI gate
**Then** the phase MUST remain "in_progress" until gate passes

**Enforcement text in SKILL.md:**
```
**CRITICAL:** CANNOT mark phase "completed" without gate passing.
**CRITICAL:** CANNOT start Phase X+1 while Phase X shows "in_progress".
```

---

### AC-4: Visual Progress Indicator Integration

**Given** the existing "Phase Progress Indicator" display pattern
**When** a phase completes (gate passes)
**Then** display combines gate result with TodoWrite update:
```
devforgeai-validate phase-complete STORY-XXX --phase=03 --checkpoint-passed
Exit code: 0
TodoWrite: Phase 03 marked "completed"
Proceeding to Phase 04...
```

## Technical Specification

### Files to Modify

| File | Change Type | Description |
|------|-------------|-------------|
| `.claude/skills/devforgeai-development/SKILL.md` | Modify | Update TodoWrite usage section with enforcement pattern |

### Location in SKILL.md

Update the "Workflow Execution Checklist" section (around lines 86-110) to add enforcement pattern.

### Pattern Template

```markdown
## Workflow Execution Checklist

**After parameter extraction, BEFORE Phase 01, create execution tracker:**

TodoWrite(
  todos=[
    {content: "Execute Phase 01: Pre-Flight Validation", status: "pending", activeForm: "..."},
    ... (all 10 phases)
  ]
)

---

### TodoWrite-Gate Integration Pattern (MANDATORY)

**ENFORCEMENT:** Phase completion status in TodoWrite is GATED by CLI validation.

```
FOR each phase N in [01..10]:

  # Phase Start
  TodoWrite(mark phase N "in_progress")
  Display: "Phase {N}/{10}: {phase_name}"

  # Execute Phase
  Read(file_path=".claude/skills/devforgeai-development/references/{phase-reference}.md")
  [Execute all steps from reference file]

  # Gate Validation (REQUIRED before marking complete)
  Bash(command="devforgeai-validate phase-complete ${STORY_ID} --phase={N} --checkpoint-passed")

  IF exit_code == 0:
    TodoWrite(mark phase N "completed")
    Display: "✓ Phase {N} complete"
    Proceed to Phase N+1

  IF exit_code != 0:
    Display: "❌ Phase {N} gate failed - see error message"
    HALT (keep phase N as "in_progress")
```

**CRITICAL RULES:**
- ❌ CANNOT mark phase "completed" without gate exit code 0
- ❌ CANNOT start Phase X+1 while Phase X shows "in_progress" or "pending"
- ✅ Gate failure = HALT (address issues before retry)
```

## Definition of Done

### Implementation
- [ ] TodoWrite usage section updated with enforcement pattern
- [ ] Explicit "CANNOT mark complete without gate" language added
- [ ] Visual example of gate + TodoWrite integration added

### Testing
- [ ] Run `/dev STORY-001` and verify gate called before TodoWrite update
- [ ] Verify phase cannot be marked complete if gate fails
- [ ] Verify "in_progress" status maintained during execution

### Documentation
- [ ] Update RCA-018 with implementation status

## Effort Estimate

- **Points:** 2
- **Estimated Hours:** 1-2 hours
  - Update SKILL.md section: 1 hour
  - Testing: 30-60 minutes

## Related

- **RCA:** RCA-018-development-skill-phase-completion-skipping.md
- **Recommendation:** REC-2 (Integrate Todo List with Phase Checkpoints)
- **Supersedes:** Inline checkpoints (now using CLI gates)
- **Related Stories:** STORY-208 (REC-3), STORY-209 (REC-4), STORY-210 (REC-5)

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-01-01 | claude/opus | Story created from RCA-018 REC-2 |

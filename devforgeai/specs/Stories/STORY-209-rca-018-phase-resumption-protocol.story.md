---
id: STORY-209
title: Document Phase Resumption Protocol for Interrupted Workflows
type: documentation
epic: EPIC-033
priority: MEDIUM
points: 1
status: Backlog
created: 2025-01-01
source: RCA-018 REC-4
depends_on:
  - STORY-207
  - STORY-208
---

# STORY-209: Document Phase Resumption Protocol for Interrupted Workflows

## User Story

**As a** DevForgeAI user whose /dev workflow stopped mid-execution,
**I want** a documented resumption protocol,
**So that** I can resume from where I left off without re-executing completed phases.

## Background

RCA-018 identified that when workflows stop mid-execution (as in RCA-013 twice and RCA-018 once), there's no documented procedure for resuming. Users must manually prompt Claude phase-by-phase.

**Source RCA:** `devforgeai/RCA/RCA-018-development-skill-phase-completion-skipping.md`

**Current State:**
- No documented resumption protocol
- Users must manually request phase-by-phase execution
- Claude doesn't have standard pattern for resumption

**Desired State:**
- Clear resumption protocol documented in SKILL.md
- User detection indicators documented
- Claude resumption steps documented
- Resumption validation included

## Acceptance Criteria

### AC-1: User Detection Indicators Documented

**Given** a user suspects workflow stopped incomplete
**When** they consult SKILL.md for indicators
**Then** they find a clear list of detection signs:
- TodoWrite list shows phases as "pending" or "in_progress"
- DoD completion <100% but workflow declared complete
- Story status not updated to expected value
- No git commit of story file

---

### AC-2: User Recovery Command Documented

**Given** a user wants to resume an incomplete workflow
**When** they consult SKILL.md for the command
**Then** they find a template command:
```
Continue /dev workflow for STORY-XXX from Phase Y.
The todo list shows these phases pending: [list]
Resume execution now.
```

---

### AC-3: Claude Resumption Steps Documented

**Given** Claude receives a resumption request
**When** Claude reads the resumption protocol
**Then** Claude finds step-by-step instructions:
1. Check TodoWrite state
2. Identify first pending/in_progress phase
3. Verify previous phases have completion evidence
4. Load phase reference file
5. Execute remaining phases with gates
6. Run final self-check

---

### AC-4: Resumption Validation Checklist

**Given** Claude is about to resume
**When** checking prerequisites
**Then** a validation checklist exists:
- [ ] User confirmed resumption (not fresh /dev)
- [ ] Previous phases have completion evidence
- [ ] No conflicting git changes since last execution
- [ ] Story file exists and is readable

---

### AC-5: Recommendation for Fresh Start vs Resume

**Given** resumption checks identify issues
**When** previous phases lack evidence
**Then** SKILL.md recommends starting fresh:
```
IF any resumption check fails:
  Recommend: "Previous execution state is unclear.
              Start fresh with /dev STORY-XXX for reliable results."
```

## Technical Specification

### Files to Modify

| File | Change Type | Description |
|------|-------------|-------------|
| `.claude/skills/devforgeai-development/SKILL.md` | Modify | Add Phase Resumption Protocol section |

### Location in SKILL.md

Add after "Workflow Completion Self-Check" section:

```markdown
## Workflow Completion Self-Check (MANDATORY)
[existing content]

---

## Phase Resumption Protocol

[new content here]

---

## Final Result Display
[existing content]
```

### Section Template

```markdown
---

## Phase Resumption Protocol

**When workflow stops incomplete (user detects phases still pending):**

### User Detection Indicators

User may notice:
- TodoWrite list shows phases as "pending" or "in_progress"
- DoD completion <100% but workflow declared complete
- Story status not updated (still "Backlog" or "In Development")
- No git commit of story file
- Result display shows "INCOMPLETE" status

### User Recovery Command

User can resume workflow with:
```
Continue /dev workflow for STORY-XXX from Phase Y.
The todo list shows these phases pending: [list phases]
Resume execution now.
```

### Claude Resumption Steps

1. **Check TodoWrite State**
   ```
   Review current todo list
   first_incomplete = first phase with status != "completed"
   ```

2. **Verify Previous Phases**
   ```
   FOR each phase before first_incomplete:
     Check evidence:
       - Phase state marker exists?
       - Expected files/artifacts present?
       - CLI gate previously passed?

     IF evidence missing:
       Display: "⚠️ Phase {N} appears incomplete despite prior execution"
       Ask: "Re-execute Phase {N}? [Y/n]"
   ```

3. **Load Phase Reference**
   ```
   Read(file_path=".claude/skills/devforgeai-development/references/{phase-reference}.md")
   Display: "Resuming workflow from Phase {N}..."
   ```

4. **Execute Remaining Phases**
   ```
   FOR each phase from first_incomplete to Phase 10:
     TodoWrite(mark phase "in_progress")
     Execute ALL steps from phase reference
     Call CLI gate: devforgeai-validate phase-complete
     IF gate passes:
       TodoWrite(mark phase "completed")
       Proceed to next phase
     ELSE:
       HALT with gate error
   ```

5. **Final Validation**
   ```
   Execute Workflow Completion Self-Check
   IF all 10 phases completed:
     Display result
   ELSE:
     Report still-missing phases
   ```

### Resumption Pre-Flight Checklist

Before resuming, verify:
- [ ] User confirmed resumption (not starting fresh /dev)
- [ ] Previous phases have completion evidence (state markers, artifacts)
- [ ] No conflicting git changes since last execution
- [ ] Story file exists and is readable
- [ ] Phase state JSON exists (if using file-based tracking)

**IF any check fails:**
```
Recommend: "Previous execution state is unclear.
            Start fresh with '/dev STORY-XXX' for reliable results.
            Fresh start ensures all phases execute with validation."
```

### Resumption vs Fresh Start Decision

| Scenario | Recommendation |
|----------|----------------|
| Phases 01-05 complete, 06-10 pending | Resume from Phase 06 |
| Phase state markers exist | Resume (state is reliable) |
| No state markers, but artifacts exist | Ask user, then resume or fresh |
| No evidence of prior execution | Fresh start |
| Git conflicts detected | Fresh start after resolving conflicts |

**Purpose:** Enable recovery from premature stopping without requiring complete re-execution of all phases.
```

## Definition of Done

### Implementation
- [ ] User detection indicators documented
- [ ] User recovery command template added
- [ ] Claude resumption steps added
- [ ] Pre-flight checklist added
- [ ] Decision matrix for resume vs fresh start added

### Testing
- [ ] Review documentation for completeness
- [ ] Test resumption scenario manually
- [ ] Verify documentation is discoverable in SKILL.md

### Documentation
- [ ] Update RCA-018 with implementation status

## Effort Estimate

- **Points:** 1
- **Estimated Hours:** 1 hour
  - Write documentation: 45 minutes
  - Review and test: 15 minutes

## Related

- **RCA:** RCA-018-development-skill-phase-completion-skipping.md
- **Recommendation:** REC-4 (Document Phase Resumption Protocol)
- **Dependencies:** STORY-207, STORY-208 (gates and self-check must exist)
- **Related Stories:** STORY-210 (REC-5)

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-01-01 | claude/opus | Story created from RCA-018 REC-4 |

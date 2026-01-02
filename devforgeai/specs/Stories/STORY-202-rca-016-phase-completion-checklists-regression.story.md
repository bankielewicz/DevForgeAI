---
id: STORY-202
title: Re-implement RCA-016 REC-2 Phase Completion Checklists for 5-Phase Structure
type: fix
epic: EPIC-033
priority: HIGH
points: 2
status: Backlog
created: 2025-01-01
source: RCA-016 Regression Record
depends_on:
  - STORY-201
---

# STORY-202: Re-implement RCA-016 REC-2 Phase Completion Checklists for 5-Phase Structure

## User Story

**As a** DevForgeAI user running QA validation,
**I want** phase completion checklists with checkboxes before each phase transition,
**So that** I can verify all mandatory steps were executed before proceeding.

## Background

RCA-016 REC-2 (Phase Completion Checklists) was implemented on 2025-12-01 with:
- Explicit checklists at end of each phase
- Checkbox format for self-verification
- "IF any checkbox unchecked: HALT" instruction

However, a later skill refactoring restructured devforgeai-qa from 7 phases to 5 phases, and the completion checklists were **not preserved** in checkbox format. This story re-implements REC-2 for the current structure.

**Source RCA:** `devforgeai/RCA/RCA-016-qa-skill-phase-skipping-during-deep-validation.md`

**Dependency:** STORY-201 (CHECKPOINT markers) should be implemented first for consistent approach.

## Acceptance Criteria

### AC-1: Completion Checklist Before Phase Marker Write

**Given** a phase is about to write its completion marker
**When** Claude prepares to write the marker
**Then** a completion checklist exists between phase content and marker write

**Phases requiring checklist:**
- Phase 1: After Step 1.4, before Phase 1 Marker Write
- Phase 2: After Step 2.4, before Phase 2 Marker Write
- Phase 3: After Step 3.5, before Phase 3 Marker Write
- Phase 4: After cleanup steps, before Phase 4 Marker Write

---

### AC-2: Checklist Uses Checkbox Format

**Given** a phase completion checklist
**When** Claude reads the checklist
**Then** each item uses checkbox format: `- [ ] Item description`

**Rationale:** Checkbox format enables Claude to mentally check items as completed, matching TodoWrite pattern.

---

### AC-3: Checklist Includes HALT Instruction

**Given** a phase completion checklist
**When** any checkbox would remain unchecked
**Then** the checklist includes: "IF any checkbox unchecked: HALT and complete missing steps before writing phase marker"

---

### AC-4: Phase-Specific Checklist Items

**Given** each phase has unique validation requirements
**When** checklist is defined for a phase
**Then** items are specific to that phase's mandatory steps

**Example (Phase 2: Analysis):**
```markdown
- [ ] Loaded anti-pattern-detection-workflow.md (Step 2.0)
- [ ] Executed anti-pattern-scanner subagent (Step 2.1)
- [ ] Ran parallel validators (Step 2.2) - deep mode only
- [ ] Invoked deferral-validator if deferrals exist (Step 2.3)
- [ ] Analyzed code quality metrics (Step 2.4)
- [ ] Displayed Phase 2 completion summary
```

---

### AC-5: Display Confirmation After Checklist

**Given** Claude completes a phase checklist
**When** all items are verified
**Then** display confirmation: `✓ Phase {N} Complete: {phase_name}`

## Technical Specification

### Files to Modify

| File | Change Type | Description |
|------|-------------|-------------|
| `.claude/skills/devforgeai-qa/SKILL.md` | Modify | Add completion checklists before each Phase Marker Write |

### Checklist Pattern Template

Add before each "Phase X Marker Write" section:

```markdown
### Phase {N} Completion Checklist

**Before writing Phase {N} marker, verify you have:**

- [ ] Loaded reference file(s) (Step {N}.0)
- [ ] Executed Step {N}.1: {step_description}
- [ ] Executed Step {N}.2: {step_description}
- [ ] ... (phase-specific items)
- [ ] Displayed Phase {N} results to user

**IF any checkbox unchecked:** HALT and complete missing steps before Phase {N+1}.

**Display to user:**
```
✓ Phase {N} Complete: {phase_name} | {key_metric}
```
```

### Phase-Specific Checklists

**Phase 1 (Validation) Checklist:**
```markdown
- [ ] Loaded traceability-validation-algorithm.md (Step 1.0)
- [ ] Validated AC-DoD traceability (Step 1.1)
- [ ] Executed test runner (Step 1.2)
- [ ] Analyzed coverage results (Step 1.3)
- [ ] Verified critical threshold (100% pass required)
- [ ] Displayed Phase 1 completion summary
```

**Phase 2 (Analysis) Checklist:**
```markdown
- [ ] Loaded anti-pattern-detection-workflow.md (Step 2.0)
- [ ] Invoked anti-pattern-scanner subagent (Step 2.1)
- [ ] Ran parallel validators (Step 2.2) - deep mode only
- [ ] Executed spec compliance validation (Step 2.3)
- [ ] Analyzed code quality metrics (Step 2.4)
- [ ] Checked blocking violations (CRITICAL/HIGH)
- [ ] Displayed Phase 2 completion summary
```

**Phase 3 (Reporting) Checklist:**
```markdown
- [ ] Loaded qa-result-formatting.md (Step 3.0)
- [ ] Aggregated results from Phases 1-2 (Step 3.1)
- [ ] Invoked qa-result-interpreter subagent (Step 3.2)
- [ ] Generated QA report (Step 3.3)
- [ ] Updated story file if applicable (Step 3.4)
- [ ] Displayed final QA status to user
```

**Phase 4 (Cleanup) Checklist:**
```markdown
- [ ] Released lock file (Step 4.1)
- [ ] Cleaned up temporary files (Step 4.2)
- [ ] Archived session checkpoint (Step 4.3)
- [ ] Displayed cleanup confirmation
```

## Definition of Done

### Implementation
- [ ] Completion checklist added before Phase 1 Marker Write
- [ ] Completion checklist added before Phase 2 Marker Write
- [ ] Completion checklist added before Phase 3 Marker Write
- [ ] Completion checklist added before Phase 4 Marker Write
- [ ] HALT instruction included in each checklist
- [ ] Phase-specific items defined for each checklist

### Testing
- [ ] Run `/qa STORY-001 deep` and verify checklists displayed
- [ ] Verify Claude displays "✓ Phase N Complete" confirmations
- [ ] Verify checklist prevents premature marker writes

### Documentation
- [ ] Update RCA-016 regression record with implementation status

## Effort Estimate

- **Points:** 2
- **Estimated Hours:** 1.5-2 hours
  - Write 4 phase-specific checklists: 1 hour
  - Add HALT instructions: 15 minutes
  - Testing: 30-45 minutes

## Related

- **RCA:** RCA-016-qa-skill-phase-skipping-during-deep-validation.md
- **Original Implementation:** Commit 0d6744f2 (2025-12-01)
- **Dependency:** STORY-201 (REC-1 CHECKPOINT Markers)

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-01-01 | claude/opus | Story created from RCA-016 regression discovery |

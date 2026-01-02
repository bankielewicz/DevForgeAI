---
id: STORY-217
title: Add Pre-Flight HALT Logic to Phases 1-4
type: enhancement
epic: EPIC-033
priority: HIGH
points: 1
status: Backlog
created: 2025-01-01
source: RCA-021 REC-3
depends_on:
  - STORY-216
---

# STORY-217: Add Pre-Flight HALT Logic to Phases 1-4

## User Story

**As a** DevForgeAI user running /qa,
**I want** each phase's pre-flight check to HALT if the previous phase is incomplete,
**So that** Claude cannot jump between phases or skip phase sequencing.

## Background

RCA-021 identified that Phases 1-4 have "Pre-Flight" sections that verify previous phase completed, but these are not enforced. Claude can skip them and jump between phases.

**Source RCA:** `devforgeai/RCA/RCA-021-qa-skill-phases-skipped.md`

**Evidence:**
- SKILL.md lines 129-136: Phase 1 Pre-Flight section
- SKILL.md line 166: Phase 2 Pre-Flight
- SKILL.md line 309: Phase 3 Pre-Flight
- SKILL.md line 409: Phase 4 Pre-Flight
- First /qa execution: Phases 2-4 not properly verified before execution

## Acceptance Criteria

### AC-1: Phase 1 Pre-Flight Has HALT Logic

**Given** the Phase 1 Pre-Flight section
**When** previous phase marker (Phase 0) is NOT found
**Then** HALT with message: "Phase 0 not verified complete. Phase 1 cannot execute."

---

### AC-2: Phase 2 Pre-Flight Has HALT Logic

**Given** the Phase 2 Pre-Flight section
**When** previous phase marker (Phase 1) is NOT found
**Then** HALT with message: "Phase 1 not verified complete. Phase 2 cannot execute."

---

### AC-3: Phase 3 Pre-Flight Has HALT Logic

**Given** the Phase 3 Pre-Flight section
**When** previous phase marker (Phase 2) is NOT found
**Then** HALT with message: "Phase 2 not verified complete. Phase 3 cannot execute."

---

### AC-4: Phase 4 Pre-Flight Has HALT Logic

**Given** the Phase 4 Pre-Flight section
**When** previous phase marker (Phase 3) is NOT found
**Then** HALT with message: "Phase 3 not verified complete. Phase 4 cannot execute."

---

### AC-5: Exact Pattern Per RCA-021

**Given** the RCA-021 recommended implementation (lines 278-292)
**When** updating each phase's Pre-Flight section
**Then** use this pattern:

```markdown
### Pre-Flight: Verify Phase {N-1} Complete

Glob(pattern="devforgeai/qa/reports/{STORY-ID}/.qa-phase-{N-1}.marker")

IF marker file NOT found:
    CRITICAL ERROR: "Phase {N-1} not verified complete"
    HALT: "Phase {N} cannot execute without Phase {N-1} completion"
    Display: "Previous phase (Phase {N-1}) must complete successfully before starting Phase {N}"
    Instruction: "Start workflow from Phase 0. Run setup first."
    Exit: Code 1 (phase sequencing violation)

Display: "✓ Phase {N-1} verified complete - Phase {N} preconditions met"
```

## Technical Specification

### Files to Modify

| File | Change Type | Description |
|------|-------------|-------------|
| `.claude/skills/devforgeai-qa/SKILL.md` | Modify | Update 4 Pre-Flight sections with HALT logic |

### Locations in SKILL.md

Update these existing sections:
1. Phase 1 Pre-Flight (around line 129)
2. Phase 2 Pre-Flight (around line 166)
3. Phase 3 Pre-Flight (around line 309)
4. Phase 4 Pre-Flight (around line 409)

### Example Update (Phase 1)

**Current:**
```markdown
### Pre-Flight: Verify Phase 0 Complete

Glob(pattern="devforgeai/qa/reports/STORY-127/.qa-phase-0.marker")
```

**Updated:**
```markdown
### Pre-Flight: Verify Phase 0 Complete

Glob(pattern="devforgeai/qa/reports/{STORY_ID}/.qa-phase-0.marker")

IF marker file NOT found:
    CRITICAL ERROR: "Phase 0 not verified complete"
    HALT: "Phase 1 cannot execute without Phase 0 completion"
    Display: "Previous phase (Phase 0) must complete successfully before starting Phase 1"
    Instruction: "Start workflow from Phase 0. Run setup first."
    Exit: Code 1 (phase sequencing violation)

Display: "✓ Phase 0 verified complete - Phase 1 preconditions met"
```

## Definition of Done

### Implementation
- [ ] Phase 1 Pre-Flight updated with HALT logic
- [ ] Phase 2 Pre-Flight updated with HALT logic
- [ ] Phase 3 Pre-Flight updated with HALT logic
- [ ] Phase 4 Pre-Flight updated with HALT logic
- [ ] All HALT messages include resolution steps

### Testing
- [ ] Create test: Try to execute Phase 2 without Phase 0/1 complete
- [ ] Verify: HALT message appears
- [ ] Verify: Error message states which phase is missing
- [ ] Fix: Execute from Phase 0
- [ ] Success criteria: Cannot bypass phase sequencing

### Documentation
- [ ] Update RCA-021 Implementation Checklist with status

## Effort Estimate

- **Points:** 1
- **Estimated Hours:** 20 minutes
  - Update 4 Pre-Flight sections: 15 minutes
  - Testing: 5 minutes

## Related

- **RCA:** RCA-021-qa-skill-phases-skipped.md
- **Recommendation:** REC-3 (HIGH - Pre-Flight Verification Enforcement at Phase Boundaries)
- **Dependency:** STORY-216 (REC-2 - Phase 0 enforcement ensures Phase 0 actually completes)
- **Related Stories:** STORY-218 (REC-4), STORY-219 (REC-5)

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-01-01 | claude/opus | Story created from RCA-021 REC-3 |

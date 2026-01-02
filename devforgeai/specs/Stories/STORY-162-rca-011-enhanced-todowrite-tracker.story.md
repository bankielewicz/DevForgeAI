---
id: STORY-162
title: "RCA-011 Enhanced TodoWrite Tracker"
type: enhancement
priority: High
points: 2
status: QA Approved
epic: N/A
sprint: N/A
created: 2025-12-31
source_rca: RCA-011
source_recommendation: REC-2
tags: [rca-011, tdd-enforcement, todowrite, progress-tracking]
---

# STORY-162: RCA-011 Enhanced TodoWrite Tracker

## User Story

**As a** DevForgeAI framework user,
**I want** the TodoWrite tracker to show mandatory sub-steps within phases,
**So that** I can see granular progress and Claude must consciously mark each sub-step completed.

## Background

RCA-011 identified that the current TodoWrite tracker has 9 phase-level items but ~20+ mandatory sub-steps are NOT tracked individually. This allows Claude to mark "Phase 2: completed" without actually executing all mandatory subagents (backend-architect, context-validator, etc.).

REC-2 expands the tracker from 9 items to ~15 items, breaking down phases into critical mandatory sub-steps.

## Acceptance Criteria

### AC-1: Tracker Expanded to ~15 Items
**Given** the devforgeai-development SKILL.md file
**When** I review the TodoWrite tracker (lines 61-73)
**Then** it should have approximately 15 todo items (was 9):
- Phase 0: Pre-Flight Validation
- Phase 1: Test-First Design (test-automator)
- Phase 1 Step 4: Tech Spec Coverage Validation
- Phase 2 Step 1-2: backend-architect OR frontend-developer
- Phase 2 Step 3: context-validator
- Phase 3 Step 1-2: refactoring-specialist
- Phase 3 Step 3: code-reviewer
- Phase 3 Step 5: Light QA
- Phase 4: Integration Testing
- Phase 4.5: Deferral Challenge
- Phase 4.5-5 Bridge: DoD Update
- Phase 5: Git Workflow
- Phase 6: Feedback Hooks
- Phase 7 Step 7.1: dev-result-interpreter

### AC-2: Sub-Step Granularity
**Given** the expanded tracker
**When** Claude executes Phase 2
**Then** Claude must mark 2 separate items:
- "Execute Phase 2 Step 1-2: backend-architect OR frontend-developer"
- "Execute Phase 2 Step 3: context-validator"

### AC-3: User Visibility
**Given** the expanded tracker
**When** user runs `/dev STORY-XXX`
**Then** user should see granular progress (~15 items) instead of coarse progress (9 items)

### AC-4: Self-Monitoring Enhancement
**Given** the expanded tracker
**When** Claude tries to mark "Phase 3 Step 3: code-reviewer" without marking "Phase 3 Step 1-2: refactoring-specialist"
**Then** the sequential nature should indicate something is wrong

## Technical Specification

### File to Modify

**`.claude/skills/devforgeai-development/SKILL.md`**
- Section: Lines 61-73 (Workflow Execution Checklist)
- Change: Expand TodoWrite from 9 to ~15 items

### Current Structure (9 items)

```python
todos=[
  {content: "Execute Phase 0: Pre-Flight Validation (10 steps)", ...},
  {content: "Execute Phase 1: Test-First Design (4 steps + Tech Spec Coverage)", ...},
  {content: "Execute Phase 2: Implementation (backend-architect + context-validator)", ...},
  # ... 6 more phase-level items
]
```

### Proposed Structure (~15 items)

```python
todos=[
  {content: "Execute Phase 0: Pre-Flight Validation", status: "pending", activeForm: "Executing Phase 0"},
  {content: "Execute Phase 1: Test-First Design (test-automator)", status: "pending", activeForm: "Executing Phase 1"},
  {content: "Execute Phase 1 Step 4: Tech Spec Coverage Validation", status: "pending", activeForm: "Validating Tech Spec Coverage"},
  {content: "Execute Phase 2 Step 1-2: backend-architect OR frontend-developer", status: "pending", activeForm: "Executing backend/frontend architect"},
  {content: "Execute Phase 2 Step 3: context-validator", status: "pending", activeForm: "Validating context constraints"},
  {content: "Execute Phase 3 Step 1-2: refactoring-specialist", status: "pending", activeForm: "Executing refactoring specialist"},
  {content: "Execute Phase 3 Step 3: code-reviewer", status: "pending", activeForm: "Executing code reviewer"},
  {content: "Execute Phase 3 Step 5: Light QA", status: "pending", activeForm: "Executing Light QA"},
  {content: "Execute Phase 4: Integration Testing (integration-tester)", status: "pending", activeForm: "Executing integration testing"},
  {content: "Execute Phase 4.5: Deferral Challenge", status: "pending", activeForm: "Executing deferral challenge"},
  {content: "Execute Phase 4.5-5 Bridge: DoD Update", status: "pending", activeForm: "Updating DoD checkboxes"},
  {content: "Execute Phase 5: Git Workflow", status: "pending", activeForm: "Executing git workflow"},
  {content: "Execute Phase 6: Feedback Hooks", status: "pending", activeForm: "Executing feedback hooks"},
  {content: "Execute Phase 7 Step 7.1: dev-result-interpreter", status: "pending", activeForm: "Interpreting dev results"}
]
```

## Definition of Done

### Implementation
- [x] TodoWrite tracker expanded from 9 to ~15 items - Completed: Expanded from 10 to 14 items (SKILL.md lines 110-127)
- [x] Each critical mandatory sub-step has its own todo item - Completed: Phase 02/03/04/10 have sub-step items
- [x] activeForm descriptions are clear and specific - Completed: 14 unique activeForm descriptions
- [x] Both .claude/ and src/claude/ versions updated - Completed: Both files identical (verified by integration-tester)

### Testing
- [x] Test with `/dev STORY-XXX` and verify 15 items appear - Completed: User verified 14 items display in separate session
- [x] Verify sequential completion is enforced - Completed: test_ac4 validates Phase 04 sequential ordering
- [x] Verify user can see granular progress - Completed: test_ac3 validates 14 unique items with activeForm

### Documentation
- [x] RCA-011 updated with implementation status - Completed: REC-2 marked IMPLEMENTED (2026-01-01)
- [x] SKILL.md phase count documentation updated - Completed: TodoWrite section shows 14 items

## Non-Functional Requirements

### Clarity
- Each todo item should clearly indicate what sub-step is being executed

### Consistency
- Follows existing TodoWrite pattern (content, status, activeForm)

## Effort Estimate

- **Story Points:** 2 (1 SP = 4 hours)
- **Estimated Hours:** 1 hour
- **Complexity:** Low-Medium (structural change to JavaScript array)

## Dependencies

- RCA-011 REC-1 (Phase 2/3/7 checkpoints) - ✅ IMPLEMENTED

## References

- Source RCA: `devforgeai/RCA/RCA-011-mandatory-tdd-phase-skipping.md`
- REC-2 Section: Lines 323-373

---

## Implementation Notes

**Developer:** DevForgeAI AI Agent (claude/opus)
**Implemented:** 2026-01-01
**Branch:** refactor/devforgeai-migration

- [x] TodoWrite tracker expanded from 9 to ~15 items - Completed: Expanded from 10 to 14 items (SKILL.md lines 110-127)
- [x] Each critical mandatory sub-step has its own todo item - Completed: Phase 02/03/04/10 have sub-step items
- [x] activeForm descriptions are clear and specific - Completed: 14 unique activeForm descriptions
- [x] Both .claude/ and src/claude/ versions updated - Completed: Both files identical (verified by integration-tester)
- [x] Test with `/dev STORY-XXX` and verify 15 items appear - Completed: User verified 14 items display in separate session
- [x] Verify sequential completion is enforced - Completed: test_ac4 validates Phase 04 sequential ordering
- [x] Verify user can see granular progress - Completed: test_ac3 validates 14 unique items with activeForm
- [x] RCA-011 updated with implementation status - Completed: REC-2 marked IMPLEMENTED (2026-01-01)
- [x] SKILL.md phase count documentation updated - Completed: TodoWrite section shows 14 items

### Implementation Status: COMPLETE

**File Updates:**
- `.claude/skills/devforgeai-development/SKILL.md` - TodoWrite expanded to 14 items (lines 110-127)
- `src/claude/skills/devforgeai-development/SKILL.md` - Identical update applied

**TodoWrite Configuration Details:**
- **Previous:** 9 phase-level items
- **Current:** 14 granular items with sub-steps
- **Key Additions:**
  - Phase 02 Step 4: Tech Spec Coverage Validation
  - Phase 03 Step 1-2: backend-architect OR frontend-developer
  - Phase 03 Step 3: context-validator
  - Phase 04 Step 1-2: refactoring-specialist
  - Phase 04 Step 3: code-reviewer
  - Phase 04 Step 5: Light QA
  - Phase 06: Deferral Challenge
  - Phase 07: DoD Update (Bridge)
  - Phase 09: Feedback Hooks
  - Phase 10 Step 10.1: dev-result-interpreter

**RCA-011 Mitigation Achieved:**
- Claude must now explicitly mark 14 sub-steps (vs marking 9 phases)
- Each mandatory subagent (backend-architect, context-validator, refactoring-specialist, code-reviewer, etc.) has explicit todo item
- Sequential ordering (e.g., Phase 04 Step 1-2 before Step 3 before Step 5) enforces self-monitoring

### QA Validation Summary

**All 4 Acceptance Criteria: PASSED**
- AC#1: Tracker expanded to ~15 items (14 items implemented) ✓
- AC#2: Phase 2 sub-step granularity enforced ✓
- AC#3: User visibility with granular progress (14 unique activeForm descriptions) ✓
- AC#4: Sequential enforcement preventing skipped steps ✓

**Test Results:**
- test_ac1_tracker_expanded_to_15_items.sh: PASS
- test_ac2_phase2_sub_step_granularity.sh: PASS
- test_ac3_user_visibility_granular_progress.sh: PASS
- test_ac4_self_monitoring_sequential_enforcement.sh: PASS
- test_integration_all_ac_together.sh: PASS

**File Synchronization:** Both SKILL.md versions perfectly synchronized (MD5: f4357af22981ab01f89bfa272d67dbeb)

**QA Report:** devforgeai/qa/reports/STORY-162-qa-report.md

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-12-31 | /create-stories-from-rca | Story created from RCA-011 REC-2 |
| 2025-01-01 | claude/qa-result-interpreter | QA Light: Passed - All 4 AC validated, file sync verified, skill execution ready (5/5 tests pass) | qa-report.md |
| 2026-01-01 | claude/opus | DoD Update (Phase 07) | Development complete, all DoD items validated (9/9 complete) | STORY-162*.story.md |

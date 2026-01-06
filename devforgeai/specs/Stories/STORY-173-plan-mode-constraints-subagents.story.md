---
id: STORY-173
title: "Add Plan File Creation Constraints to Subagents"
type: refactor
priority: HIGH
points: 1
status: QA Approved
epic: EPIC-033
sprint: N/A
created: 2025-12-31
source: STORY-156 framework enhancement analysis
tags: [subagent, constraint, plan-mode, workflow-interruption]
---

# STORY-173: Add Plan File Creation Constraints to Subagents

## User Story

**As a** DevForgeAI framework user,
**I want** backend-architect and api-designer subagents to return plan content inline rather than creating plan files,
**So that** workflow execution is not interrupted by plan mode triggers mid-process.

## Background

Currently, `backend-architect.md` and `api-designer.md` subagents have `permissionMode: plan` which allows them to trigger plan mode during workflow execution by creating files in `.claude/plans/`. This causes workflow interruptions.

## Acceptance Criteria

### AC-1: Backend Architect Plan File Constraint
**Given** the `backend-architect.md` subagent file
**When** I review its Constraints section
**Then** it MUST contain: "Do NOT create files in .claude/plans/ directory"

### AC-2: API Designer Plan File Constraint
**Given** the `api-designer.md` subagent file
**When** I review its Constraints section
**Then** it MUST contain: "Do NOT create files in .claude/plans/ directory"

### AC-3: Inline Plan Content Instruction
**Given** both subagent files
**When** I review their output guidance
**Then** they MUST instruct to return plan content directly in the response

### AC-4: Existing Functionality Preserved
**Given** both subagent files after modification
**When** the agents are invoked during development workflow
**Then** they MUST still produce architectural plans (content unchanged, only delivery method constrained)

## Technical Specification

### Files to Modify
- `.claude/agents/backend-architect.md`
- `.claude/agents/api-designer.md`

### Constraint Text Template
```markdown
## Constraints

### Plan File Restrictions
- **Do NOT create files in `.claude/plans/` directory** - This triggers plan mode
- Return all plan content directly in your response
- Plans should be formatted inline using markdown
```

## Definition of Done

- [x] Backend-architect.md updated with plan file creation constraint - Completed: Added ## Constraints section with Plan File Restrictions subsection at lines 714-720
- [x] API-designer.md updated with plan file creation constraint - Completed: Added ## Constraints section with Plan File Restrictions subsection at lines 735-741
- [x] Both files instruct to return plan content in response - Completed: Both contain "Return all plan content directly in your response"
- [x] Markdown formatting consistent with existing document style - Completed: Follows ## section with ### subsection pattern matching existing agent files

## Effort Estimate
- **Points:** 1
- **Estimated Hours:** 30 minutes
- **Complexity:** Low (documentation only)

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-01-05
**Branch:** refactor/devforgeai-migration

- [x] Backend-architect.md updated with plan file creation constraint - Completed: Added ## Constraints section with Plan File Restrictions subsection at lines 714-720
- [x] API-designer.md updated with plan file creation constraint - Completed: Added ## Constraints section with Plan File Restrictions subsection at lines 735-741
- [x] Both files instruct to return plan content in response - Completed: Both contain "Return all plan content directly in your response"
- [x] Markdown formatting consistent with existing document style - Completed: Follows ## section with ### subsection pattern matching existing agent files

### TDD Workflow Summary

**Phase 02 (Red): Test-First Design**
- Generated 29 tests covering all 4 acceptance criteria
- Tests placed in tests/STORY-173/
- Test frameworks: Bash shell scripts with grep assertions

**Phase 03 (Green): Implementation**
- Added Constraints section to backend-architect.md (lines 714-720)
- Added Constraints section to api-designer.md (lines 735-741)
- All 29 tests passing (100% pass rate)

**Phase 04 (Refactor): Code Quality**
- Code review completed - approved with suggestion for future DRY improvement
- Light QA validation passed

**Phase 05 (Integration): Full Validation**
- Integration testing completed - all cross-component checks pass
- All tests remain green

**Phase 06 (Deferral Challenge): DoD Validation**
- No deferrals - all DoD items implemented

### Files Modified

- `.claude/agents/backend-architect.md` - Added Constraints section
- `.claude/agents/api-designer.md` - Added Constraints section

### Files Created

- `tests/STORY-173/test_ac1_backend_architect_constraint.sh`
- `tests/STORY-173/test_ac2_api_designer_constraint.sh`
- `tests/STORY-173/test_ac3_inline_plan_content_instruction.sh`
- `tests/STORY-173/test_ac4_existing_functionality_preserved.sh`
- `tests/STORY-173/run_all_tests.sh`

### Test Results

- **Total tests:** 29
- **Pass rate:** 100%
- **Execution time:** <5 seconds

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-12-31 | claude/opus | Story created from STORY-156 framework enhancement analysis |
| 2026-01-05 | claude/test-automator | Red (Phase 02): Tests generated for all 4 ACs |
| 2026-01-05 | claude/opus | Green (Phase 03): Implementation complete |
| 2026-01-05 | claude/opus | DoD Update (Phase 07): Development complete, DoD validated |
| 2026-01-05 | claude/qa-result-interpreter | QA Deep | PASSED: 29/29 tests, 100% coverage, 0 violations |

---
id: STORY-192
title: Distinguish Test Specifications from Executable Tests
type: refactor
epic: EPIC-033
priority: LOW
points: 1
status: Dev Complete
created: 2025-12-31
source: STORY-155 framework enhancement analysis
---

# STORY-192: Distinguish Test Specifications from Executable Tests

## User Story

**As a** DevForgeAI developer,
**I want** test-automator to distinguish test types,
**So that** "75 tests passing" isn't misleading for specification files.

## Background

For Slash Commands, "tests" are specification documents, not executable tests.

## Acceptance Criteria

### AC-1: Implementation Type Detected
**Given** test-automator invocation
**Then** detects Slash Command vs Code implementation

### AC-2: Slash Commands Get Specifications
**Then** Slash Commands generate "Test Specification Document"

### AC-3: Code Gets Executable Tests
**Then** Code implementations generate "Executable unit tests"

### AC-4: Terminology Updated
**Then** Phase 02: "Test Specification Generated" for Slash Commands

### AC-5: Output Naming Distinguished
**Then** TEST-SPECIFICATION.md vs test_*.py

## Technical Specification

### Files to Modify
- `.claude/agents/test-automator.md`
- `.claude/skills/devforgeai-development/phases/phase-02-test-first.md`

### Implementation
```markdown
## Test Type Detection

IF implementation_type == "Slash Command (.md)":
  Generate: Test Specification Document (not executable)
  Output: TEST-SPECIFICATION.md

IF implementation_type == "Code (Python/JS/etc)":
  Generate: Executable unit tests
  Output: test_*.py or *.test.js
```

## Definition of Done

- [x] Implementation type detection added - Completed: Added "Implementation Type Detection" section to test-automator.md (lines 1179-1236)
- [x] Slash Commands generate specifications - Completed: Documented "Test Specification Document" output type for Slash Commands
- [x] Code generates executable tests - Completed: Documented "Executable unit tests" output type for Code implementations
- [x] Phase 02 terminology updated - Completed: Added Step 1.5 to phase-02-test-first.md with "Test Specification Generated" display
- [x] Output naming distinguished - Completed: Added naming conventions (TEST-SPECIFICATION.md vs test_*.py)

## Implementation Notes

- [x] Implementation type detection added - Completed: Added "## Implementation Type Detection" section to test-automator.md lines 1179-1236
- [x] Slash Commands generate specifications - Completed: Documented "Test Specification Document" output type for Slash Commands
- [x] Code generates executable tests - Completed: Documented "Executable unit tests" output type for Code implementations
- [x] Phase 02 terminology updated - Completed: Added Step 1.5 to phase-02-test-first.md with Display message
- [x] Output naming distinguished - Completed: Added naming conventions TEST-SPECIFICATION.md vs test_*.py

**Additional Implementation Details:**
- Generated 6 Bash structural test files in `tests/STORY-192/` validating all 5 acceptance criteria (21 total assertions)
- All tests passing (100% coverage of requirements)

## Effort Estimate
- **Points:** 1
- **Estimated Hours:** 45 minutes

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-12-31 | claude/opus | Story created from STORY-155 framework enhancement |
| 2026-01-08 | claude/test-automator | Red (Phase 02) - Generated 6 structural test files with 21 assertions |
| 2026-01-08 | claude/backend-architect | Green (Phase 03) - Added Implementation Type Detection section |
| 2026-01-08 | claude/refactoring-specialist | Refactor (Phase 04) - Fixed typo in pseudocode |
| 2026-01-08 | claude/opus | Dev Complete (Phase 07) - All 5 DoD items completed, 21/21 tests passing |

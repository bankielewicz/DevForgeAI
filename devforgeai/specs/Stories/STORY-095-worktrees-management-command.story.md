---
id: STORY-095
title: /worktrees Management Command
epic: EPIC-010
sprint: SPRINT-5
status: QA Approved
points: 5
priority: High
assigned_to: TBD
created: 2025-11-25
format_version: "2.1"
depends_on: ["STORY-091"]
---

# Story: /worktrees Management Command

## Description

**As a** DevForgeAI developer with multiple active worktrees,
**I want** a central command to see all worktrees and their status,
**so that** I can identify stale worktrees for cleanup and resume interrupted work.

**Context:** This is Feature 5 of EPIC-010 (Parallel Story Development). Provides visibility and management for Git worktrees created by /dev.

## Acceptance Criteria

### AC#1: Worktree Table Display

**Given** active worktrees exist
**When** developer runs `/worktrees`
**Then** displays table: Story ID | Path | Age | Size | Status | Last Activity

---

### AC#2: Cleanup Candidate Identification

**Given** worktrees idle >7 days exist
**When** `/worktrees` runs
**Then** identifies cleanup candidates with warning indicator
**And** displays: "⚠️ 2 worktrees idle >7 days"

---

### AC#3: Interactive Actions Menu

**Given** worktree table is displayed
**When** presenting options to developer
**Then** offers:
1. Cleanup all candidates
2. Cleanup selected
3. Inspect worktree
4. Resume development
5. Cancel

---

### AC#4: Safe Cleanup with Status Check

**Given** user selects cleanup
**When** cleanup executes
**Then** verifies story status before deleting
**And** "story-037 status=Released → safe to delete"
**And** "story-041 status=In Development → keep"

---

### AC#5: Execution Time Requirement

**Given** developer runs `/worktrees`
**When** listing and status check runs
**Then** completes in < 5 seconds (including git commands)

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "API"
      name: "/worktrees command"
      endpoint: "/worktrees"
      method: "Slash Command"
      file_path: "src/claude/commands/worktrees.md"
      requirements:
        - id: "CMD-001"
          description: "List all worktrees with status table"
          testable: true
          test_requirement: "Test: /worktrees shows 4 worktrees in table"
          priority: "Critical"
        - id: "CMD-002"
          description: "Identify cleanup candidates"
          testable: true
          test_requirement: "Test: 12-day idle worktree flagged"
          priority: "Critical"
        - id: "CMD-003"
          description: "Provide interactive action menu"
          testable: true
          test_requirement: "Test: 5 options displayed via AskUserQuestion"
          priority: "High"
        - id: "CMD-004"
          description: "Safe cleanup with status verification"
          testable: true
          test_requirement: "Test: In Development worktree not deleted"
          priority: "Critical"

  business_rules:
    - id: "BR-001"
      rule: "Never delete worktrees with status In Development without confirmation"
      trigger: "Cleanup action"
      validation: "Check story status before delete"
      test_requirement: "Test: In Development requires explicit confirmation"
      priority: "Critical"
    - id: "BR-002"
      rule: "Released/QA Approved worktrees safe to delete"
      trigger: "Cleanup action"
      validation: "Status is terminal"
      test_requirement: "Test: Released worktree deleted without extra prompt"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "List and status check"
      metric: "< 5 seconds for up to 20 worktrees"
      test_requirement: "Test: Time /worktrees command"
      priority: "High"
```

---

## Non-Functional Requirements

### Performance
- Worktree listing: < 2 seconds
- Status check: < 3 seconds total
- Full command: < 5 seconds

### Reliability
- Graceful handling of corrupted worktrees
- Error reporting for failed deletions
- Idempotent operations

---

## Edge Cases

1. **No worktrees exist:** Display "No active worktrees found"
2. **Worktree directory missing:** Flag as orphaned, offer repair
3. **Git not available:** Error with resolution steps
4. **All worktrees active:** No cleanup candidates

---

## Dependencies

### Prerequisite Stories
- [x] **STORY-091:** Git Worktree Auto-Management (QA Approved)

---

## Definition of Done

### Implementation
- [x] /worktrees command created (~200 lines) - `.claude/commands/worktrees.md`
- [x] Table display with all columns (Story ID, Path, Age, Size, Status, Last Activity)
- [x] Cleanup candidate detection (>7 days idle)
- [x] Interactive action menu (5 options via AskUserQuestion)
- [x] Safe cleanup with status verification (Released/QA Approved safe, In Development requires confirmation)
- [x] git-worktree-manager subagent integration (via Task tool)

### Quality
- [x] All 5 acceptance criteria pass
- [x] Edge cases handled (no worktrees, corrupted, orphaned, missing git, unknown status)
- [x] Performance < 5 seconds (optimized with cached reads)

### Testing
- [x] Unit tests for table formatting - `tests/worktree/test_worktrees_command.py`
- [x] Integration tests for cleanup workflow
- [ ] Manual testing across platforms (deferred to QA phase)

---

## Workflow Status

- [x] Architecture phase complete
- [x] Development phase complete
- [x] QA phase complete
- [ ] Released

## Workflow History

### 2025-12-17 - Status: QA Approved
**QA Validation PASSED (deep mode)**
- All 27 tests passing (2.44s execution)
- AC-DoD traceability: 100%
- Anti-pattern violations: 0
- Spec compliance: 5/5 ACs validated
- Code quality: All metrics within thresholds
- Report: `devforgeai/qa/reports/STORY-095-qa-report.md`

### 2025-12-17 - Status: Dev Complete
- Implemented /worktrees command with full workflow
- Created 27 unit tests covering all 5 ACs
- Files created:
  - `.claude/commands/worktrees.md` (~200 lines)
  - `tests/worktree/test_worktrees_command.py` (~450 lines)
- TDD phases completed: RED → GREEN → REFACTOR
- All tests passing (27/27)

### 2025-11-27 14:30:00 - Status: Ready for Dev
- Added to SPRINT-5: Parallel Story Development Foundation
- Transitioned from Backlog to Ready for Dev
- Sprint capacity: 45 points
- Priority in sprint: 6 of 7 (High - depends on STORY-091)

---

**Story Template Version:** 2.1
**Created:** 2025-11-25

## Implementation Notes

### Files Created
- `.claude/commands/worktrees.md` - Slash command definition (~200 lines)
- `tests/worktree/test_worktrees_command.py` - Test suite (27 tests, ~450 lines)

### Architecture Decisions
- Leverages existing `git-worktree-manager` subagent from STORY-091
- Uses AskUserQuestion for interactive menu (follows DevForgeAI patterns)
- Safe cleanup logic: Released/QA Approved auto-delete, In Development requires confirmation

### Test Coverage
- AC#1: 4 tests for table display
- AC#2: 4 tests for cleanup candidate identification
- AC#3: 4 tests for action menu
- AC#4: 5 tests for safe cleanup logic
- AC#5: 3 tests for performance requirements
- Edge cases: 4 tests
- Integration: 3 tests

# Plan: STORY-148 Phase State File Module

**Story:** STORY-148 - Phase State File Module
**Epic:** EPIC-031 - Phase Execution Enforcement System
**Status:** 🔄 In Progress
**Created:** 2025-12-25

---

## Overview

Implement `installer/phase_state.py` - a Python module for TDD phase state tracking via JSON files. This is Layer 1 of the 3-Layer Enforcement Architecture that prevents Claude from skipping mandatory TDD phases.

---

## Constitutional Constraints (Read Before Implementation)

### From tech-stack.md (lines 428-445):
- Python 3.10+ required for CLI tools
- Reuses existing `installer/` modules
- Python subprocess invocation pattern

### From source-tree.md (lines 372-401):
- Module location: `installer/phase_state.py`
- Test location: `installer/tests/test_phase_state.py`
- State files: `devforgeai/workflows/STORY-XXX-phase-state.json`
- Archive: `devforgeai/workflows/completed/`

### From dependencies.md (lines 113-136):
- Python stdlib ONLY for core installer modules
- PyYAML 6.0+ available but prefer json (stdlib)
- No external packages for validation

### From architecture-constraints.md:
- Single Responsibility: One module, one purpose (phase state management)
- Atomic writes: temp file + rename pattern
- File locking: fcntl for concurrent write safety

---

## Implementation Plan

### Phase 1: TDD Red Phase (Write Failing Tests First)

**File:** `installer/tests/test_phase_state.py`

**Tests to create:**
1. `test_create_initializes_all_phases` - AC#1
2. `test_read_returns_current_state` - AC#4
3. `test_record_subagent_appends_to_list` - AC#2
4. `test_complete_phase_advances_workflow` - AC#3
5. `test_archive_moves_to_completed` - AC#6
6. `test_validate_rejects_invalid_state` - AC#5
7. `test_concurrent_writes_blocked_by_lock` - AC#7
8. `test_create_is_idempotent` - BR-004
9. `test_phase_transition_ordering` - BR-001
10. `test_subagent_records_immutable` - BR-002
11. `test_archive_rejects_incomplete` - BR-003

**Checkpoint 1:** All tests written, all tests FAIL (Red)

### Phase 2: TDD Green Phase (Minimal Implementation)

**File:** `installer/phase_state.py`

**Implementation order:**
1. PhaseState class with constants (WORKFLOWS_DIR, ARCHIVE_DIR, LOCK_TIMEOUT)
2. `validate_state()` - Structure validation before persistence
3. `create()` - Initialize state file with all 10 phases
4. `read()` - Read current state without modification
5. `record_subagent()` - Append subagent to phase list
6. `complete_phase()` - Mark phase complete, advance current_phase
7. `archive()` - Move completed state to archive directory
8. File locking with fcntl (Unix) / msvcrt (Windows)

**Checkpoint 2:** All tests PASS (Green)

### Phase 3: TDD Refactor Phase

- Reduce code duplication
- Improve error messages
- Add type hints to all public methods
- Add docstrings
- Performance optimization if needed

**Checkpoint 3:** All tests still PASS, code quality improved

### Phase 4: Integration Verification

- Verify directory auto-creation works
- Verify file locking prevents corruption
- Verify atomic writes with temp file pattern

**Checkpoint 4:** Integration verified

### Phase 5: Story Update & Commit

- Update STORY-148 status to "Dev Complete"
- Update Definition of Done checkboxes
- Commit with conventional commit format

**Checkpoint 5:** Story updated, changes committed

---

## Progress Checkpoints

- [ ] Checkpoint 1: Foundation Complete (tests written, all fail)
- [ ] Checkpoint 2: Green Phase Complete (all tests pass)
- [ ] Checkpoint 3: Refactor Complete (code quality verified)
- [ ] Checkpoint 4: Integration Verified
- [ ] Checkpoint 5: Story Updated & Committed

---

## Data Model

### Phase State JSON Schema

```json
{
  "story_id": "STORY-148",
  "workflow_started": "2025-12-25T10:00:00Z",
  "current_phase": "01",
  "phases": {
    "01": {
      "name": "Preflight",
      "status": "pending",
      "started_at": null,
      "completed_at": null,
      "subagents_required": ["tech-stack-detector", "context-validator", "git-validator"],
      "subagents_invoked": [],
      "checkpoint_passed": false
    },
    "02": { ... },
    ...
    "10": { ... }
  },
  "validation_errors": [],
  "blocking_status": false
}
```

### Phase Definitions (10 Phases)

| ID | Name | Required Subagents |
|----|------|-------------------|
| 01 | Preflight | tech-stack-detector, context-validator, git-validator |
| 02 | Red | test-automator |
| 03 | Green | backend-architect |
| 04 | Refactor | refactoring-specialist |
| 05 | Integration | integration-tester |
| 06 | Deferral | deferral-validator |
| 07 | DoD-Update | (none - skill action) |
| 08 | Git | git-validator |
| 09 | Feedback | (none - skill action) |
| 10 | Result | dev-result-interpreter |

---

## Error Handling

| Error Type | Behavior |
|------------|----------|
| State file exists on create() | Return existing state (idempotent) |
| Invalid phase_id | Raise `PhaseNotFoundError` |
| Archive incomplete story | Raise `IncompleteWorkflowError` |
| Corrupted JSON | Raise `StateFileCorruptionError` |
| Missing directories | Auto-create |
| Lock timeout (5s) | Raise `LockTimeoutError` |
| Invalid story_id format | Raise `ValueError` |

---

## Dependencies

- **Upstream:** None (foundation story)
- **Downstream:** STORY-149, STORY-150, STORY-151

---

## Notes

- Use `fcntl.flock()` on Unix, `msvcrt.locking()` on Windows for cross-platform file locking
- Atomic writes via temp file + `os.rename()` pattern
- All timestamps in ISO-8601 UTC format
- Story ID pattern: `STORY-\d{3}` (e.g., STORY-148)

---

## Change Log

| Date | Action | Notes |
|------|--------|-------|
| 2025-12-25 | Plan created | Session recovery - fresh start |

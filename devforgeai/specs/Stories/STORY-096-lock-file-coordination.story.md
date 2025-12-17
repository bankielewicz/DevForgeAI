---
id: STORY-096
title: Lock File Coordination for Critical Operations
epic: EPIC-010
sprint: SPRINT-5
status: Dev Complete
points: 3
priority: High
assigned_to: Claude
created: 2025-11-25
format_version: "2.1"
depends_on: ["STORY-091"]
---

# Story: Lock File Coordination for Critical Operations

## Description

**As a** DevForgeAI developer,
**I want** git commits from parallel stories to be serialized automatically,
**so that** I don't encounter git index lock conflicts or race conditions.

**Context:** This is Feature 6 of EPIC-010 (Parallel Story Development). Lock file coordination prevents race conditions when multiple worktrees commit simultaneously.

## Acceptance Criteria

### AC#1: Lock Acquisition Before Commit

**Given** /dev Phase 5 (git commit) is executing
**When** commit begins
**Then** acquires `.devforgeai/.locks/git-commit.lock` before committing
**And** lock contains PID, story_id, timestamp

---

### AC#2: Wait with Progress Display

**Given** lock is held by another story
**When** second story attempts commit
**Then** waits with progress: "Waiting for git lock (held by STORY-037 PID 12345)... 15s"
**And** updates every 5 seconds

---

### AC#3: Stale Lock Detection

**Given** lock file exists
**And** PID is no longer running (dead process)
**And** lock age > 5 minutes
**When** another story attempts commit
**Then** auto-removes stale lock
**And** logs: "Removed stale lock (PID 12345 not running)"

---

### AC#4: Lock Timeout Prompt

**Given** waiting for lock exceeds 10 minutes
**When** timeout reached
**Then** prompts user:
1. Continue waiting
2. Force acquire lock (risky)
3. Abort

---

### AC#5: Lock Release After Commit

**Given** commit completes (success or failure)
**When** Phase 5 finishes
**Then** `.devforgeai/.locks/git-commit.lock` is removed
**And** next waiting story can proceed

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Service"
      name: "LockManager"
      file_path: "src/claude/skills/devforgeai-development/references/lock-file-coordination.md"
      interface: "Service"
      requirements:
        - id: "SVC-001"
          description: "Acquire lock with PID, story_id, timestamp"
          testable: true
          test_requirement: "Test: Lock file created with correct content"
          priority: "Critical"
        - id: "SVC-002"
          description: "Wait for lock with progress display"
          testable: true
          test_requirement: "Test: Progress updates every 5 seconds"
          priority: "High"
        - id: "SVC-003"
          description: "Detect and remove stale locks"
          testable: true
          test_requirement: "Test: Dead PID lock removed after 5 min"
          priority: "Critical"
        - id: "SVC-004"
          description: "Release lock after operation"
          testable: true
          test_requirement: "Test: Lock file deleted after commit"
          priority: "Critical"

    - type: "DataModel"
      name: "LockFile"
      table: ".devforgeai/.locks/git-commit.lock"
      fields:
        - name: "pid"
          type: "integer"
          constraints: "Required"
          description: "Process ID holding lock"
        - name: "story_id"
          type: "string"
          constraints: "Required"
          description: "Story ID of lock holder"
        - name: "timestamp"
          type: "ISO8601"
          constraints: "Required"
          description: "Lock acquisition time"
        - name: "hostname"
          type: "string"
          constraints: "Optional"
          description: "Machine name for distributed scenarios"

  business_rules:
    - id: "BR-001"
      rule: "Only one commit operation at a time across all worktrees"
      trigger: "Phase 5 git commit"
      validation: "Lock must be acquired before git add/commit"
      test_requirement: "Test: Concurrent commits serialized"
      priority: "Critical"
    - id: "BR-002"
      rule: "Stale locks auto-removed after 5 minutes"
      trigger: "Lock acquisition attempt"
      validation: "Check PID running, check timestamp"
      test_requirement: "Test: 6-minute old lock with dead PID removed"
      priority: "Critical"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Lock acquisition time"
      metric: "< 100ms when no contention"
      test_requirement: "Test: Acquire lock in <100ms"
      priority: "Medium"
    - id: "NFR-002"
      category: "Reliability"
      requirement: "Lock release on process crash"
      metric: "Stale lock detected within 5 minutes"
      test_requirement: "Test: Crashed process lock recoverable"
      priority: "High"
```

---

## Non-Functional Requirements

### Performance
- Lock acquisition: < 100ms (no contention)
- Wait loop overhead: < 10ms per iteration
- Stale detection: < 500ms

### Reliability
- Crash recovery via stale detection
- Atomic lock file writes (temp + rename)
- Guaranteed release on success or failure

### Security
- Lock file permissions: 600 (owner only)
- PID validation prevents spoofing

---

## Edge Cases

1. **Process crashes during commit:** Stale detection cleans up
2. **Multiple machines (same repo):** Hostname helps identify
3. **User interrupts wait:** Lock not acquired, clean exit
4. **Force acquire fails:** Error with recovery steps

---

## Dependencies

### Prerequisite Stories
- [ ] **STORY-091:** Git Worktree Auto-Management (worktrees create concurrent git ops)

---

## Definition of Done

### Implementation
- [x] Lock acquisition logic in Phase 5 Step 5.1
- [x] Wait-with-progress display
- [x] Stale lock detection and removal
- [x] Lock release in Step 5.3
- [x] Timeout prompt implementation

### Quality
- [x] All 5 acceptance criteria pass
- [x] Edge cases handled
- [x] Crash recovery tested

### Testing
- [x] Unit tests for lock operations (45 tests)
- [x] Integration tests for concurrent commits (9 tests)
- [x] Crash simulation tests (via stale lock detection)

---

## Workflow Status

- [x] Architecture phase complete
- [x] Development phase complete
- [ ] QA phase complete
- [ ] Released

## Workflow History

### 2025-11-27 14:30:00 - Status: Ready for Dev
- Added to SPRINT-5: Parallel Story Development Foundation
- Transitioned from Backlog to Ready for Dev
- Sprint capacity: 45 points
- Priority in sprint: 7 of 7 (High - depends on STORY-091)

### 2025-12-17 - Status: Dev Complete
- TDD implementation complete (Red → Green → Refactor)
- 54 tests passing (45 unit + 9 integration)
- Integration with git-workflow-conventions.md complete
- Reference file lock-file-coordination.md created
- SKILL.md Phase 08 updated with lock coordination steps

---

**Story Template Version:** 2.1
**Created:** 2025-11-25

## Implementation Notes

- [x] Lock acquisition logic in Phase 5 Step 5.1 - Completed: GitCommitLock.acquire() in src/lock_file_coordinator.py
- [x] Wait-with-progress display - Completed: progress_callback parameter with 5-second updates
- [x] Stale lock detection and removal - Completed: is_stale() checks PID dead AND age > 5 min
- [x] Lock release in Step 5.3 - Completed: GitCommitLock.release() with try/finally pattern
- [x] Timeout prompt implementation - Completed: AskUserQuestion template in lock-file-coordination.md
- [x] All 5 acceptance criteria pass - Completed: 54 tests verify all AC items
- [x] Edge cases handled - Completed: 5 edge case tests (concurrent, crash, hostname)
- [x] Crash recovery tested - Completed: Stale detection tests verify crash recovery
- [x] Unit tests for lock operations - Completed: 45 unit tests in test_lock_file_coordinator.py
- [x] Integration tests for concurrent commits - Completed: 9 integration tests
- [x] Crash simulation tests - Completed: Stale lock detection tests simulate crash scenarios

Files Created:
- `src/lock_file_coordinator.py` - Core Python lock management module (450 lines)
- `.claude/skills/devforgeai-development/references/lock-file-coordination.md` - Workflow reference (250 lines)
- `tests/lock-coordination/test_lock_file_coordinator.py` - Unit tests (45 tests)
- `tests/lock-coordination/test_lock_integration.py` - Integration tests (9 tests)

Files Modified:
- `.claude/skills/devforgeai-development/references/git-workflow-conventions.md` - Added Step 0.5 Lock Coordination
- `.claude/skills/devforgeai-development/SKILL.md` - Updated Phase 08 references

Key Implementation Details:
- **AC#1:** Lock file contains PID, story_id, timestamp, hostname
- **AC#2:** Progress updates every 5 seconds via callback
- **AC#3:** Stale detection requires PID dead AND age > 5 minutes
- **AC#4:** AskUserQuestion prompt with Continue/Force/Abort options
- **AC#5:** Lock release in try/finally pattern

Test Coverage:
- Lock acquisition: 8 tests (NFR-001 <100ms verified)
- Stale detection: 8 tests (5-minute threshold)
- Wait with progress: 6 tests (5-second updates)
- Timeout handling: 5 tests (10-minute timeout)
- Lock release: 5 tests (idempotent, context manager)
- Content parsing: 5 tests
- Edge cases: 5 tests (concurrent, crash recovery)
- Integration: 9 tests (parallel commits, workflow integration)

---
id: STORY-148
title: Phase State File Module
type: feature
status: Backlog
priority: High
story-points: 3
epic: EPIC-031
sprint: null
created: 2025-12-23
updated: 2025-12-23
assignee: null
depends-on: []
blocks: [STORY-149, STORY-150, STORY-151]
---

## User Story

**As a** development workflow orchestrator,
**I want** to create and manage JSON state files that track TDD phase execution progress,
**So that** the Phase Execution Enforcement System (Layer 1) has a reliable record of which phases have started, which subagents were invoked, and checkpoint validation status for external enforcement.

---

## Acceptance Criteria

### AC#1: Create phase state file at workflow start

**Given** a new `/dev` command is invoked for a story
**When** the `PhaseState.create()` method is called with story_id and workflow metadata
**Then** a new JSON state file is created at `devforgeai/workflows/STORY-XXX-phase-state.json` with initial state containing:
- `story_id`: The provided story identifier
- `workflow_started`: UTC ISO-8601 timestamp
- `current_phase`: "01" (first phase)
- `phases`: Object with all 10 phases initialized with status "pending"
- `validation_errors`: Empty array
- `blocking_status`: false

### AC#2: Record subagent invocation during phase execution

**Given** a state file exists for the current workflow
**When** the `PhaseState.record_subagent()` method is called with phase_id, subagent_name, and timestamp
**Then** the subagent entry is appended to the phase's `subagents_invoked` list, and the method returns success confirmation without modifying other phase data.

### AC#3: Mark phase as complete with checkpoint status

**Given** a phase has all required subagents invoked
**When** the `PhaseState.complete_phase()` method is called with phase_id and checkpoint_passed status
**Then** the phase status is updated to "completed", `completed_at` timestamp is recorded, `checkpoint_passed` flag is set, and `current_phase` advances to the next phase.

### AC#4: Read current phase state without modification

**Given** a state file exists and is valid JSON
**When** the `PhaseState.read()` method is called with story_id
**Then** the method returns the complete current state as a dictionary without modifying the file, preserving all timestamps, phase statuses, and subagent invocations.

### AC#5: Validate state structure before persistence

**Given** a state object is being created or updated
**When** any write operation attempts to persist the state file
**Then** structure validation is performed before write (checking required fields, valid enum values, type correctness), rejecting invalid state with clear error messages (e.g., "Missing required field: current_phase"), and the file is not written if validation fails.

### AC#6: Archive completed state files

**Given** a story workflow reaches "QA Approved" status
**When** the `PhaseState.archive()` method is called with story_id
**Then** the state file is moved from `devforgeai/workflows/STORY-XXX-phase-state.json` to `devforgeai/workflows/completed/STORY-XXX-phase-state.json`, and the original file is removed.

### AC#7: Handle concurrent writes with file locking

**Given** multiple processes attempt to write to the same state file simultaneously
**When** write operations overlap
**Then** file locking prevents corruption by blocking concurrent writes (using Python's fcntl module), ensuring only one write completes at a time with max wait of 5 seconds before timeout.

---

## Technical Specification

```yaml
technical_specification:
  version: "2.0"

  components:
    - type: Module
      name: PhaseState
      file_path: installer/phase_state.py
      description: "Python module for TDD phase state tracking via JSON files"
      dependencies:
        - json (stdlib)
        - pathlib (stdlib)
        - datetime (stdlib)
        - fcntl (stdlib - Unix file locking)
        - logging (stdlib)
        - typing (stdlib)

      methods:
        - name: create
          signature: "create(story_id: str) -> dict"
          description: "Create new phase state file for story"
          test_requirement: "test_create_initializes_all_phases"

        - name: read
          signature: "read(story_id: str) -> dict"
          description: "Read current state without modification"
          test_requirement: "test_read_returns_current_state"

        - name: record_subagent
          signature: "record_subagent(story_id: str, phase_id: str, subagent_name: str) -> bool"
          description: "Record subagent invocation in phase"
          test_requirement: "test_record_subagent_appends_to_list"

        - name: complete_phase
          signature: "complete_phase(story_id: str, phase_id: str, checkpoint_passed: bool) -> bool"
          description: "Mark phase complete and advance current_phase"
          test_requirement: "test_complete_phase_advances_workflow"

        - name: archive
          signature: "archive(story_id: str) -> bool"
          description: "Move completed state to archive directory"
          test_requirement: "test_archive_moves_to_completed"

        - name: validate_state
          signature: "validate_state(state: dict) -> tuple[bool, str]"
          description: "Validate state structure (required fields, types, enums)"
          test_requirement: "test_validate_rejects_invalid_state"

    - type: DataModel
      name: PhaseStateSchema
      file_path: installer/phase_state_schema.json
      description: "JSON schema for phase state validation"
      fields:
        - name: story_id
          type: string
          pattern: "^STORY-\\d{3}$"
          required: true
        - name: workflow_started
          type: string
          format: date-time
          required: true
        - name: current_phase
          type: string
          enum: ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10"]
          required: true
        - name: phases
          type: object
          required: true
          properties:
            status: { enum: ["pending", "in_progress", "completed", "skipped"] }
            started_at: { type: string, format: date-time }
            completed_at: { type: string, format: date-time }
            subagents_required: { type: array, items: { type: string } }
            subagents_invoked: { type: array, items: { type: string } }
            checkpoint_passed: { type: boolean }
        - name: validation_errors
          type: array
          items: { type: string }
          required: true
        - name: blocking_status
          type: boolean
          required: true

    - type: Configuration
      name: PhaseStateConfig
      file_path: installer/phase_state.py
      description: "Configuration constants for phase state module"
      settings:
        - name: WORKFLOWS_DIR
          value: "devforgeai/workflows"
          description: "Directory for active state files"
        - name: ARCHIVE_DIR
          value: "devforgeai/workflows/completed"
          description: "Directory for archived state files"
        - name: LOCK_TIMEOUT
          value: 5
          description: "Max seconds to wait for file lock"
        - name: FILE_PATTERN
          value: "{story_id}-phase-state.json"
          description: "State file naming pattern"

  business_rules:
    - id: BR-001
      description: "Phase transitions must follow strict ordering (01→02→...→10)"
      validation: "current_phase can only increment by 1"
      test_requirement: "test_phase_transition_ordering"

    - id: BR-002
      description: "Subagent invocations are append-only"
      validation: "subagents_invoked list cannot remove entries"
      test_requirement: "test_subagent_records_immutable"

    - id: BR-003
      description: "Archive only when all phases complete or QA Approved"
      validation: "archive() rejects stories with pending phases"
      test_requirement: "test_archive_rejects_incomplete"

    - id: BR-004
      description: "State file creation is idempotent"
      validation: "create() returns existing state if file exists"
      test_requirement: "test_create_is_idempotent"

  non_functional_requirements:
    - category: Performance
      requirement: "State file creation < 50ms including directory creation"
      metric: "p95 latency"
      test_requirement: "test_create_performance"

    - category: Performance
      requirement: "State file read < 20ms for typical files"
      metric: "p95 latency"
      test_requirement: "test_read_performance"

    - category: Reliability
      requirement: "Atomic writes using temp file + rename pattern"
      metric: "No partial writes on crash"
      test_requirement: "test_atomic_write_safety"

    - category: Data Integrity
      requirement: "Structure validation before all writes"
      metric: "0 invalid state files persisted"
      test_requirement: "test_structure_enforcement"
```

---

## Edge Cases

1. **State file already exists:** `create()` returns existing state (idempotent)
2. **Invalid phase_id:** Raise `PhaseNotFoundError` with valid phase list
3. **Archive incomplete story:** Raise `IncompleteWorkflowError`
4. **Corrupted JSON:** Raise `StateFileCorruptionError` with recovery instructions
5. **Missing directories:** Auto-create `devforgeai/workflows/` and `completed/`
6. **Concurrent writes:** File locking with 5-second timeout
7. **Story ID validation:** Must match `STORY-\d{3}` pattern

---

## Definition of Done

### Implementation
- [ ] `installer/phase_state.py` module created with PhaseState class
- [ ] All 6 methods implemented (create, read, record_subagent, complete_phase, archive, validate_schema)
- [ ] JSON schema file created at `installer/phase_state_schema.json`
- [ ] File locking implemented for concurrent write safety
- [ ] Auto-create directories if missing

### Quality
- [ ] Unit test coverage >= 95%
- [ ] All edge cases have tests
- [ ] No anti-pattern violations
- [ ] Code follows PEP 8 style guide
- [ ] Type hints on all public methods

### Testing
- [ ] `test_create_initializes_all_phases` passes
- [ ] `test_read_returns_current_state` passes
- [ ] `test_record_subagent_appends_to_list` passes
- [ ] `test_complete_phase_advances_workflow` passes
- [ ] `test_archive_moves_to_completed` passes
- [ ] `test_validate_rejects_invalid_state` passes
- [ ] `test_concurrent_writes_blocked_by_lock` passes
- [ ] Performance tests meet thresholds

### Documentation
- [ ] Docstrings on all public methods
- [ ] README section for phase_state module (if applicable)

---

## Dependencies

### Upstream (this story depends on)
- None (foundation story)

### Downstream (blocked by this story)
- STORY-149: Phase Validation Script (requires state file to validate)
- STORY-150: Pre-Phase-Transition Hook (requires state file to check)
- STORY-151: Post-Subagent Recording Hook (requires record_subagent method)

---

## Related Documents

| Document | Path |
|----------|------|
| Epic | `devforgeai/specs/Epics/EPIC-031-phase-execution-enforcement.epic.md` |
| Plan | `/home/bryan/.claude/plans/moonlit-meandering-bumblebee.md` |
| RCA-022 | `devforgeai/RCA/RCA-022-mandatory-tdd-phases-skipped.md` |
| Brainstorm | `devforgeai/specs/brainstorms/BRAINSTORM-002-phase-execution-enforcement.brainstorm.md` |

---

## Workflow Status

**Current Status:** Backlog
**Created:** 2025-12-23
**Last Updated:** 2025-12-23

### Status History
| Date | From | To | By | Notes |
|------|------|-----|-----|-------|
| 2025-12-23 | - | Backlog | DevForgeAI | Story created |

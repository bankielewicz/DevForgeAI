---
id: STORY-253
title: Create PhaseState Module in Correct Location
type: feature
epic: None
sprint: Backlog
status: Backlog
points: 8
depends_on: []
priority: Critical
assigned_to: Unassigned
created: 2026-01-12
format_version: "2.5"
source_rca: RCA-001
source_recommendation: REC-1
---

# Story: Create PhaseState Module in Correct Location

## Description

**As a** DevForgeAI framework developer,
**I want** a `PhaseState` class in the `.claude/scripts/devforgeai_cli/` package that manages workflow phase tracking state files,
**so that** the CLI phase commands (`phase-init`, `phase-status`, `phase-record`, `phase-complete`) can enforce sequential phase execution during `/dev` workflow without sys.path manipulation or missing module errors.

## Acceptance Criteria

### AC#1: PhaseState class initialization and path resolution

**Given** a project root directory path
**When** `PhaseState(project_root=Path("/path/to/project"))` is instantiated
**Then** the instance stores the project root and resolves `workflows_dir` to `{project_root}/devforgeai/workflows/`

---

### AC#2: Create new phase state file with complete schema

**Given** a valid story ID (matching pattern `STORY-\d{3}`)
**When** `create(story_id="STORY-001")` is called
**Then** a JSON file is created at `devforgeai/workflows/STORY-001-phase-state.json` containing:
  - `story_id`: "STORY-001"
  - `current_phase`: "01"
  - `workflow_started`: ISO-8601 UTC timestamp
  - `blocking_status`: false
  - `phases`: Object with keys "01" through "10", each containing `status`, `subagents_required`, and `subagents_invoked`
  - `validation_errors`: empty array
  - `observations`: empty array

---

### AC#3: Idempotent state file creation

**Given** a state file already exists for `STORY-001`
**When** `create(story_id="STORY-001")` is called again
**Then** the existing state is returned without modification (no file overwrite)

---

### AC#4: Read existing phase state

**Given** a state file exists for `STORY-001`
**When** `read(story_id="STORY-001")` is called
**Then** the method returns the complete state dictionary parsed from JSON

---

### AC#5: Read returns None for non-existent state

**Given** no state file exists for `STORY-999`
**When** `read(story_id="STORY-999")` is called
**Then** the method returns `None` (not an exception)

---

### AC#6: Complete phase with sequential enforcement

**Given** a state file exists with `current_phase="02"` and phase "01" is completed
**When** `complete_phase(story_id="STORY-001", phase="02", checkpoint_passed=True)` is called
**Then** phase "02" status becomes "completed", `completed_at` timestamp is recorded, `checkpoint_passed` is stored, and `current_phase` advances to "03"

---

### AC#7: Phase transition validation (sequential order only)

**Given** a state file exists with `current_phase="02"`
**When** `complete_phase(story_id="STORY-001", phase="05", checkpoint_passed=True)` is called (attempting to skip phases)
**Then** a `PhaseTransitionError` is raised with message indicating sequential completion required

---

### AC#8: Record subagent invocation

**Given** a state file exists for `STORY-001`
**When** `record_subagent(story_id="STORY-001", phase="02", subagent="test-automator")` is called
**Then** "test-automator" is appended to `phases["02"]["subagents_invoked"]` array and `started_at` timestamp is recorded if not present

---

### AC#9: Add workflow observation

**Given** a state file exists for `STORY-001`
**When** `add_observation(story_id="STORY-001", phase_id="04", category="friction", note="Test took longer than expected", severity="medium")` is called
**Then** an observation object is appended to the `observations` array with unique ID format `obs-{phase_id}-{8-char-uuid}`, phase, category, note, severity, and timestamp

---

### AC#10: Input validation for story ID format

**Given** an invalid story ID "INVALID-ID"
**When** any method is called with this story ID
**Then** a `ValueError` is raised with message: "Invalid story_id: 'INVALID-ID'. Must match pattern STORY-XXX (e.g., STORY-001)"

---

### AC#11: Input validation for phase ID

**Given** an invalid phase ID "15"
**When** `complete_phase()` or `record_subagent()` is called with this phase ID
**Then** a `PhaseNotFoundError` is raised with message indicating valid phases are "01" through "10"

---

### AC#12: State file path helper method

**Given** a PhaseState instance
**When** `_get_state_path(story_id="STORY-001")` is called
**Then** the method returns `Path("{project_root}/devforgeai/workflows/STORY-001-phase-state.json")`

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Service"
      name: "PhaseState"
      file_path: ".claude/scripts/devforgeai_cli/phase_state.py"
      interface: "None (standalone class)"
      lifecycle: "Transient (per-use instantiation)"
      dependencies:
        - "pathlib.Path"
        - "json"
        - "logging"
        - "datetime"
        - "typing"
        - "uuid"
        - "os, tempfile, shutil (atomic writes)"
        - "fcntl (Unix only, conditional import)"
        - "msvcrt (Windows only, conditional import)"
      requirements:
        - id: "SVC-001"
          description: "Initialize with project root and resolve workflows directory path"
          testable: true
          test_requirement: "Test: PhaseState(Path('/project')).workflows_dir == Path('/project/devforgeai/workflows')"
          priority: "Critical"
        - id: "SVC-002"
          description: "Create new phase state file with complete 10-phase schema"
          testable: true
          test_requirement: "Test: create('STORY-001') creates JSON file with all required fields"
          priority: "Critical"
        - id: "SVC-003"
          description: "Return existing state without modification (idempotent create)"
          testable: true
          test_requirement: "Test: Two consecutive create() calls return same state"
          priority: "High"
        - id: "SVC-004"
          description: "Read state from JSON file and return dict, or None if not found"
          testable: true
          test_requirement: "Test: read('STORY-001') returns dict; read('STORY-999') returns None"
          priority: "Critical"
        - id: "SVC-005"
          description: "Validate story ID matches STORY-XXX pattern"
          testable: true
          test_requirement: "Test: Invalid IDs ('INVALID', 'STORY-1') raise ValueError"
          priority: "High"
        - id: "SVC-006"
          description: "Validate phase ID is 01-10"
          testable: true
          test_requirement: "Test: Invalid phase IDs ('0', '11') raise PhaseNotFoundError"
          priority: "High"
        - id: "SVC-007"
          description: "Complete phase only if it's the current phase (sequential enforcement)"
          testable: true
          test_requirement: "Test: Completing phase '05' when current is '02' raises PhaseTransitionError"
          priority: "Critical"
        - id: "SVC-008"
          description: "Advance current_phase after completion (except at phase 10)"
          testable: true
          test_requirement: "Test: After completing '02', current_phase becomes '03'"
          priority: "High"
        - id: "SVC-009"
          description: "Record subagent invocation without duplicates"
          testable: true
          test_requirement: "Test: Recording same subagent twice only adds it once"
          priority: "Medium"
        - id: "SVC-010"
          description: "Add observation with unique ID, timestamp, and validation"
          testable: true
          test_requirement: "Test: add_observation() returns ID matching 'obs-{phase}-{hex}' pattern"
          priority: "Medium"
        - id: "SVC-011"
          description: "Use atomic file writes (temp file + rename)"
          testable: true
          test_requirement: "Test: State file is never partially written"
          priority: "High"
        - id: "SVC-012"
          description: "Use platform-aware file locking with timeout for concurrent access"
          testable: true
          test_requirement: "Test: Concurrent writes don't corrupt file on Unix; last-write-wins on Windows"
          priority: "High"
          platform_notes: |
            Unix (Linux/macOS): Use fcntl.flock() with LOCK_EX | LOCK_NB
            Windows: Use msvcrt.locking() with LK_NBLCK, or accept last-write-wins
            Implementation pattern:
              if os.name == 'posix':
                  import fcntl
                  fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
              elif os.name == 'nt':
                  import msvcrt
                  msvcrt.locking(fd.fileno(), msvcrt.LK_NBLCK, 1)
              else:
                  # Fallback: skip locking (last-write-wins)
        - id: "SVC-013"
          description: "Raise StateFileCorruptionError for malformed JSON"
          testable: true
          test_requirement: "Test: Corrupted JSON triggers exception with recovery message"
          priority: "Medium"
        - id: "SVC-014"
          description: "Create directories automatically if missing"
          testable: true
          test_requirement: "Test: create() on fresh project creates devforgeai/workflows/"
          priority: "Medium"

    - type: "DataModel"
      name: "PhaseStateSchema"
      table: "N/A (JSON file)"
      purpose: "JSON schema for phase state files"
      fields:
        - name: "story_id"
          type: "String"
          constraints: "Required, Pattern: STORY-\\d{3}"
          description: "Story identifier"
          test_requirement: "Test: Validate story_id matches STORY-XXX pattern"
        - name: "current_phase"
          type: "String"
          constraints: "Required, Enum: 01-10"
          description: "Current active phase"
          test_requirement: "Test: current_phase is valid two-digit phase ID"
        - name: "workflow_started"
          type: "DateTime"
          constraints: "Required, ISO-8601 UTC"
          description: "Workflow start timestamp"
          test_requirement: "Test: workflow_started is valid ISO-8601 format with Z suffix"
        - name: "blocking_status"
          type: "Boolean"
          constraints: "Required, Default: false"
          description: "Whether workflow is blocked"
          test_requirement: "Test: blocking_status is boolean"
        - name: "phases"
          type: "Object"
          constraints: "Required, Keys: 01-10"
          description: "Phase status dictionary"
          test_requirement: "Test: phases contains all 10 phase keys"
        - name: "observations"
          type: "Array"
          constraints: "Optional, Default: []"
          description: "Workflow observations"
          test_requirement: "Test: observations is array of observation objects"

  business_rules:
    - id: "BR-001"
      rule: "Phases must be completed sequentially (01 before 02, etc.)"
      trigger: "complete_phase() called"
      validation: "Check current_phase matches requested phase"
      error_handling: "Raise PhaseTransitionError if out of sequence"
      test_requirement: "Test: Skip attempt raises PhaseTransitionError"
      priority: "Critical"
    - id: "BR-002"
      rule: "Subagent recording is idempotent (no duplicates)"
      trigger: "record_subagent() called"
      validation: "Check if subagent already in array"
      error_handling: "Silently skip if duplicate"
      test_requirement: "Test: Duplicate recording doesn't add entry"
      priority: "Medium"
    - id: "BR-003"
      rule: "State file creation is idempotent"
      trigger: "create() called for existing story"
      validation: "Check if file exists"
      error_handling: "Return existing state without modification"
      test_requirement: "Test: Existing file not overwritten"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "State file read latency"
      metric: "< 10ms per read() operation (p99)"
      test_requirement: "Test: 1000 consecutive reads complete in < 10 seconds"
      priority: "High"
    - id: "NFR-002"
      category: "Performance"
      requirement: "State file write latency"
      metric: "< 50ms per create() or complete_phase() operation (p99)"
      test_requirement: "Test: 100 consecutive writes complete in < 5 seconds"
      priority: "High"
    - id: "NFR-003"
      category: "Reliability"
      requirement: "Atomic file writes"
      metric: "0% partial write corruption rate"
      test_requirement: "Test: Simulate crash during write, verify no corruption"
      priority: "Critical"
    - id: "NFR-004"
      category: "Reliability"
      requirement: "File lock timeout"
      metric: "5 second maximum wait, LockTimeoutError if exceeded"
      test_requirement: "Test: Lock held > 5s triggers timeout exception"
      priority: "High"
    - id: "NFR-005"
      category: "Security"
      requirement: "Path traversal prevention"
      metric: "0 successful traversal attempts"
      test_requirement: "Test: story_id '../etc/passwd' raises ValueError"
      priority: "Critical"
    - id: "NFR-006"
      category: "Scalability"
      requirement: "Concurrent workflow support"
      metric: "100+ concurrent story state files"
      test_requirement: "Test: 100 parallel state operations complete without errors"
      priority: "Medium"
    - id: "NFR-007"
      category: "Maintainability"
      requirement: "Test coverage"
      metric: ">= 95% line coverage"
      test_requirement: "Test: Coverage report shows >= 95%"
      priority: "High"
    - id: "NFR-008"
      category: "Compatibility"
      requirement: "Cross-platform support"
      metric: "Works on Windows 10+, macOS 11+, Linux (Ubuntu/Debian/RHEL), WSL 1/2"
      test_requirement: "Test: All operations succeed on each supported platform"
      priority: "Critical"
      notes: |
        Per dependencies.md lines 174-183, all platforms MUST be supported.
        File locking implementation must use platform detection:
        - os.name == 'posix': Use fcntl module
        - os.name == 'nt': Use msvcrt module or skip locking
        No hard dependency on Unix-only modules.
```

## Technical Limitations

```yaml
technical_limitations: []
```

## Non-Functional Requirements

### Performance

**Response Time:**
- State file read: < 10ms (p99)
- State file write: < 50ms (p99)
- Lock acquisition: < 100ms normal, 5s timeout max

**Throughput:**
- Support 100+ concurrent story state files
- 1000 operations/second sustained load

### Security

**Authentication:** N/A (local file access)

**Data Protection:**
- State files contain workflow metadata only (no secrets)
- File permissions: 0644
- Path traversal prevention via input validation

### Reliability

**Error Handling:**
- Custom exception hierarchy for precise error handling
- Atomic writes prevent partial corruption
- File locking prevents concurrent write conflicts

**Retry Logic:**
- Lock acquisition retries for 5 seconds before timeout

### Observability

**Logging:**
- Debug-level logging for all state modifications
- Structured logging with story_id, phase, operation

## Edge Cases

1. **Corrupted JSON state file:** Raise `StateFileCorruptionError` with recovery instructions
2. **Concurrent write protection (platform-aware):**
   - **Unix (Linux/macOS):** Use `fcntl.flock()` with 5-second timeout via polling
   - **Windows:** Use `msvcrt.locking()` if available, otherwise accept last-write-wins semantics
   - **Fallback:** If locking unavailable, log warning and proceed without lock (acceptable for single-user CLI)
3. **Missing workflows directory:** Create automatically with `mkdir(parents=True)`
4. **Duplicate subagent recording:** Idempotent operation (no duplicate)
5. **Phase 10 completion boundary:** Stay at phase "10" (no "11")
6. **Empty observation note:** Raise `ValueError`
7. **Invalid observation category:** Raise `ValueError` with valid options
8. **Invalid observation severity:** Raise `ValueError` with valid options
9. **Atomic file writes:** Use temp file + rename pattern
10. **Empty state file:** Treat as corrupted

## Data Validation Rules

| Field | Validation | Error |
|-------|-----------|-------|
| story_id | Regex: `^STORY-\d{3}$` | ValueError |
| phase_id | Enum: "01" through "10" | PhaseNotFoundError |
| status | Enum: pending, in_progress, completed, skipped | ValueError |
| category | Enum: friction, gap, success, pattern | ValueError |
| severity | Enum: low, medium, high | ValueError |
| timestamps | ISO-8601 UTC with "Z" suffix | ValueError |
| note | Non-empty after trim, max 1000 chars | ValueError |

## Dependencies

### Prerequisite Stories
None - standalone story addressing RCA-001

### Technology Dependencies
- Python standard library only (no external packages)
- Platform-aware imports: `fcntl` (Unix) / `msvcrt` (Windows) for file locking
- Cross-platform requirement per dependencies.md: Windows 10+, macOS 11+, Linux, WSL

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for business logic

**Test File:** `.claude/scripts/devforgeai_cli/tests/test_phase_state.py`

**Test Scenarios:**
1. **Happy Path:** Create, read, complete_phase, record_subagent, add_observation
2. **Edge Cases:** All 10 edge cases documented above
3. **Error Cases:** All validation errors documented

### Integration Tests

**Test Sequence:**
```bash
devforgeai-validate phase-init STORY-TEST --project-root=.
devforgeai-validate phase-status STORY-TEST
devforgeai-validate phase-record STORY-TEST --phase=01 --subagent=git-validator
devforgeai-validate phase-complete STORY-TEST --phase=01 --checkpoint-passed
devforgeai-validate phase-status STORY-TEST
rm devforgeai/workflows/STORY-TEST-phase-state.json
```

## Acceptance Criteria Verification Checklist

### AC#1: PhaseState class initialization
- [ ] __init__ accepts project_root Path - **Phase:** 3 - **Evidence:** test_phase_state.py
- [ ] workflows_dir resolved correctly - **Phase:** 3 - **Evidence:** test_phase_state.py

### AC#2: Create new state file
- [ ] JSON file created at correct path - **Phase:** 3 - **Evidence:** test_phase_state.py
- [ ] All schema fields present - **Phase:** 3 - **Evidence:** test_phase_state.py
- [ ] Phases 01-10 initialized - **Phase:** 3 - **Evidence:** test_phase_state.py

### AC#3: Idempotent creation
- [ ] Existing file not overwritten - **Phase:** 3 - **Evidence:** test_phase_state.py

### AC#4-5: Read operations
- [ ] Existing state returned as dict - **Phase:** 3 - **Evidence:** test_phase_state.py
- [ ] Missing state returns None - **Phase:** 3 - **Evidence:** test_phase_state.py

### AC#6-7: Phase completion
- [ ] Phase status updated - **Phase:** 3 - **Evidence:** test_phase_state.py
- [ ] current_phase advanced - **Phase:** 3 - **Evidence:** test_phase_state.py
- [ ] Sequential enforcement - **Phase:** 3 - **Evidence:** test_phase_state.py

### AC#8-9: Recording operations
- [ ] Subagent recorded - **Phase:** 3 - **Evidence:** test_phase_state.py
- [ ] Observation added with ID - **Phase:** 3 - **Evidence:** test_phase_state.py

### AC#10-12: Validation
- [ ] Story ID validation - **Phase:** 3 - **Evidence:** test_phase_state.py
- [ ] Phase ID validation - **Phase:** 3 - **Evidence:** test_phase_state.py
- [ ] Path helper method - **Phase:** 3 - **Evidence:** test_phase_state.py

---

**Checklist Progress:** 0/15 items complete (0%)

## Definition of Done

### Implementation
- [ ] Module file created: `.claude/scripts/devforgeai_cli/phase_state.py`
- [ ] PhaseState class with all 7 methods
- [ ] Custom exceptions: PhaseStateError, PhaseNotFoundError, StateFileCorruptionError, PhaseTransitionError, LockTimeoutError
- [ ] Input validation for story_id, phase_id, category, severity
- [ ] Atomic file writes (temp + rename)
- [ ] File locking for concurrent access
- [ ] Complete type annotations
- [ ] Docstrings for all public methods

### Quality
- [ ] All 12 acceptance criteria testable
- [ ] All 10 edge cases handled
- [ ] All validation rules enforced
- [ ] NFRs met (performance, reliability, security)
- [ ] Code coverage >= 95%

### Testing
- [ ] Unit tests: 20+ test cases
- [ ] Integration tests: CLI command sequence
- [ ] Edge case tests: All 10 scenarios
- [ ] Performance tests: Latency verification

### Documentation
- [ ] Module docstring with usage examples
- [ ] RCA-001 updated with story link
- [ ] Import updated in phase_commands.py (STORY-254)

## Implementation Notes

**Architecture Decision:**
Place PhaseState in `.claude/scripts/devforgeai_cli/` (same package as consumer `phase_commands.py`) to enable:
1. Simple relative import: `from ..phase_state import PhaseState`
2. Single pip install target
3. No sys.path manipulation
4. No project root pollution with `installer/` directory

**RCA-001 Root Cause Addressed:**
The Phase Execution Enforcement System CLI was created (STORY-148/149) but the underlying PhaseState module was never implemented. This story creates the missing module in the architecturally correct location.

**Related Stories:**
- STORY-254: Update phase_commands.py import
- STORY-255: Add graceful error handling

## Change Log

**Current Status:** Backlog

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-12 12:00 | claude/story-requirements-analyst | Created | Story created from RCA-001 REC-1 | STORY-253.story.md |
| 2026-01-12 13:00 | claude | Updated | Fixed platform compatibility: replaced fcntl-only with platform-aware locking (fcntl/msvcrt) per dependencies.md cross-platform requirement | STORY-253.story.md |

## Notes

**Design Decisions:**
- File-per-story isolation for concurrent workflow support
- Atomic writes for crash safety
- File locking for concurrent access protection
- Idempotent operations for retry safety

**Related ADRs:**
- None (new infrastructure module)

**References:**
- RCA-001: Phase State Module Missing From CLI
- devforgeai/RCA/RCA-001-phase-state-module-missing.md

---

**Story Template Version:** 2.5
**Last Updated:** 2026-01-12

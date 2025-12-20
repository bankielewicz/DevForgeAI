---
id: STORY-120
title: Session Checkpoint Protocol
epic: EPIC-024
sprint: Sprint-8
status: Backlog
points: 8
depends_on: []
priority: Critical
assigned_to: TBD
created: 2025-12-20
format_version: "2.2"
---

# Story: Session Checkpoint Protocol

## Description

**As a** developer,
**I want** TDD progress checkpointed at each phase completion so I can resume after context window fills,
**So that** long development sessions don't lose work when context limits are reached.

This story implements EPIC-024 Feature 1: Create checkpoint files at each TDD phase completion to enable session recovery when context window fills. Checkpoints stored in `devforgeai/sessions/{STORY-ID}/checkpoint.json`.

## Acceptance Criteria

### AC#1: Checkpoint File Written at Phase Completion

**Given** a developer is executing `/dev` workflow,
**When** each phase completes (phases 0-7),
**Then** a checkpoint file is written to `devforgeai/sessions/{STORY-ID}/checkpoint.json` with current phase data.

---

### AC#2: Checkpoint Includes Required Fields

**Given** a checkpoint file is written,
**When** the file is read,
**Then** it contains: story_id, phase number, phase_name, timestamp (ISO 8601), progress_percentage (0-100), dod_completion status (implementation/quality/testing/documentation counts).

---

### AC#3: /resume-dev Auto-Detects from Checkpoint

**Given** a developer runs `/resume-dev STORY-120` without phase number,
**When** checkpoint file exists,
**Then** `/resume-dev` auto-detects the last completed phase and resumes from next phase (no prompting required).

---

### AC#4: Checkpoint Cleaned Up on Story Completion

**Given** a story reaches Released status,
**When** the story workflow completes,
**Then** checkpoint file is deleted (or marked as archived with 7-day retention max).

---

### AC#5: Graceful Handling if Checkpoint Missing/Corrupted

**Given** checkpoint file is missing or corrupted,
**When** `/resume-dev` attempts to read it,
**Then** it falls back to Phase 0 with user warning: "Checkpoint not found. Starting from Phase 0."

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Reference Document"
      name: "session-checkpoint.md"
      file_path: ".claude/skills/devforgeai-development/references/session-checkpoint.md"
      purpose: "Checkpoint protocol documentation for skill implementation"
      required_sections:
        - section: "Checkpoint Format Specification"
          description: "JSON schema, field definitions, examples"
          test_requirement: "Test: Schema matches AC#2 fields"
        - section: "Write Protocol"
          description: "When/where checkpoints written during TDD phases"
          test_requirement: "Test: Checkpoint written after each phase"
        - section: "Read Protocol"
          description: "How /resume-dev reads and resumes from checkpoint"
          test_requirement: "Test: Auto-detection works correctly"
        - section: "Cleanup Protocol"
          description: "When checkpoints deleted, retention policy"
          test_requirement: "Test: Checkpoints cleaned up on story completion"
        - section: "Error Handling"
          description: "Missing/corrupted checkpoint handling"
          test_requirement: "Test: Graceful fallback to Phase 0"

    - type: "Python Module"
      name: "checkpoint.py"
      file_path: "src/claude/scripts/devforgeai_cli/session/checkpoint.py"
      interface: "Python class/functions"
      lifecycle: "Called by devforgeai-development skill during TDD"
      dependencies:
        - "json (stdlib)"
        - "pathlib (stdlib)"
        - "datetime (stdlib)"
      requirements:
        - id: "write_checkpoint"
          description: "Write checkpoint to .devforgeai/sessions/{story_id}/checkpoint.json"
          signature: "def write_checkpoint(story_id: str, phase: int, progress: dict) -> bool"
          test_requirement: "Test: Creates directory if missing, writes valid JSON"
        - id: "read_checkpoint"
          description: "Read checkpoint and return phase/progress data"
          signature: "def read_checkpoint(story_id: str) -> dict or None"
          test_requirement: "Test: Returns valid dict or None if missing"
        - id: "delete_checkpoint"
          description: "Delete checkpoint file"
          signature: "def delete_checkpoint(story_id: str) -> bool"
          test_requirement: "Test: Removes file, handles already-deleted"

    - type: "Skill Reference"
      name: "devforgeai-development SKILL.md modifications"
      file_path: ".claude/skills/devforgeai-development/SKILL.md"
      purpose: "Add checkpoint writes at end of each phase"
      modifications:
        - phase: "Phase 0 (Preflight)"
          action: "Add checkpoint write (initializing phase)"
          test_requirement: "Test: Phase 0 checkpoint written"
        - phase: "Phase 1 (Red)"
          action: "Add checkpoint write after tests generated"
          test_requirement: "Test: Phase 1 checkpoint includes test count"
        - phase: "Phase 2 (Green)"
          action: "Add checkpoint write after implementation"
          test_requirement: "Test: Phase 2 checkpoint includes code written"
        - phase: "Phase 3 (Refactor)"
          action: "Add checkpoint write after refactoring"
          test_requirement: "Test: Phase 3 checkpoint written"
        - phase: "Phases 4-7"
          action: "Add checkpoint write at phase completion"
          test_requirement: "Test: All 8 phases write checkpoints"

    - type: "Command Reference"
      name: "/resume-dev command modifications"
      file_path: ".claude/commands/resume-dev.md"
      purpose: "Add checkpoint reading for auto-detection"
      modifications:
        - section: "Phase 0: Argument Validation"
          action: "Add checkpoint detection before phase number validation"
          logic: "IF no phase number AND checkpoint exists → detect_phase_from_checkpoint()"
          test_requirement: "Test: Auto-detection works when phase omitted"

  data_models:
    - name: "Checkpoint JSON"
      fields:
        - name: "story_id"
          type: "string"
          example: "STORY-120"
          required: true
          validation: "STORY-\\d{3} format"
        - name: "phase"
          type: "integer"
          example: 3
          required: true
          validation: "0-7 range"
        - name: "phase_name"
          type: "string"
          example: "Refactor"
          required: true
          validation: "Red|Green|Refactor|Integration|QA|Release|Complete"
        - name: "timestamp"
          type: "string (ISO 8601)"
          example: "2025-12-20T15:30:00Z"
          required: true
          validation: "Valid ISO timestamp"
        - name: "progress_percentage"
          type: "integer"
          example: 67
          required: true
          validation: "0-100 range"
        - name: "dod_completion"
          type: "object"
          required: true
          fields:
            - name: "implementation"
              type: "array [completed, total]"
              example: "[5, 8]"
            - name: "quality"
              type: "array [completed, total]"
              example: "[2, 6]"
            - name: "testing"
              type: "array [completed, total]"
              example: "[3, 5]"
            - name: "documentation"
              type: "array [completed, total]"
              example: "[1, 4]"
        - name: "last_action"
          type: "string"
          example: "code-reviewer subagent completed"
          required: false
        - name: "next_action"
          type: "string"
          example: "Phase 4: Integration Testing"
          required: true

  directory_structure:
    - path: ".devforgeai/sessions/"
      purpose: "Session checkpoint directory"
      owner: "devforgeai-development skill"
    - path: ".devforgeai/sessions/{STORY-ID}/"
      purpose: "Per-story checkpoint storage"
      files:
        - "checkpoint.json"
      retention: "7 days from last write, or until story Released"
```

## Non-Functional Requirements

| Requirement | Target | Justification |
|-------------|--------|---------------|
| Checkpoint write latency | <100ms | Minimize TDD phase time overhead |
| Checkpoint file size | <10KB | Disk efficient, quick reads |
| Checkpoint directory overhead | <1MB total | Avoid storage bloat across multiple stories |
| Read latency | <50ms | Fast resumption detection |

## Implementation Reference

**Pattern to follow:** Use `src/claude/scripts/devforgeai_cli/validators/dod_validator.py` as architectural pattern for:
- File structure and imports
- Error handling patterns
- JSON parsing with graceful fallbacks
- CLI integration patterns

## Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Checkpoint file bloat over time | Low | Medium | Auto-cleanup on story completion, 7-day max retention |
| Concurrent checkpoint writes (parallel dev) | Low | Low | Use atomic file writes with temp file + rename |
| Corrupted JSON from interrupted write | Low | Medium | Validate JSON on read, fallback to Phase 0 |

## Test Strategy

### Unit Tests
- **Test 1:** write_checkpoint() creates valid JSON
- **Test 2:** write_checkpoint() creates directory if missing
- **Test 3:** read_checkpoint() returns valid dict when present
- **Test 4:** read_checkpoint() returns None when missing
- **Test 5:** read_checkpoint() handles corrupted JSON gracefully
- **Test 6:** delete_checkpoint() removes file successfully
- **Test 7:** delete_checkpoint() doesn't error if file missing

### Integration Tests
- **Test 8:** TDD phase writes checkpoint at completion
- **Test 9:** All 8 phases write valid checkpoints
- **Test 10:** `/resume-dev STORY-120` auto-detects last phase without arg
- **Test 11:** `/resume-dev STORY-120 3` uses explicit phase number (explicit overrides checkpoint)
- **Test 12:** Checkpoint deleted when story reaches Released

### Edge Cases
- **Test 13:** Missing .devforgeai/sessions/ directory is created
- **Test 14:** Corrupted checkpoint.json falls back to Phase 0
- **Test 15:** Concurrent checkpoint writes (if parallel dev) handled safely

## Definition of Done

### Implementation
- [ ] `.claude/skills/devforgeai-development/references/session-checkpoint.md` created with full protocol documentation
- [ ] `src/claude/scripts/devforgeai_cli/session/checkpoint.py` implemented with 3 functions
- [ ] `src/claude/scripts/devforgeai_cli/session/__init__.py` created for package
- [ ] `.claude/skills/devforgeai-development/SKILL.md` modified to write checkpoints at phase completion
- [ ] `.claude/commands/resume-dev.md` modified to read checkpoints for auto-detection

### Quality
- [ ] All unit tests passing (7 tests)
- [ ] All integration tests passing (5 tests)
- [ ] All edge cases handled (3 tests)
- [ ] Code coverage ≥95% for checkpoint.py
- [ ] No Bash used for file operations (Python or native tools only)

### Testing
- [ ] Manual test: Long TDD cycle writes checkpoints progressively
- [ ] Manual test: Context window fill → resume with `/resume-dev STORY-120` → continues from correct phase
- [ ] Manual test: Corrupted checkpoint gracefully falls back

### Documentation
- [ ] session-checkpoint.md complete with examples
- [ ] resume-dev.md updated with checkpoint reading procedure
- [ ] SKILL.md updated with checkpoint write calls
- [ ] Inline comments explain checkpoint protocol

### Release
- [ ] All tests passing
- [ ] Code reviewed for security (file permissions, JSON safety)
- [ ] Documentation reviewed
- [ ] Ready for QA validation

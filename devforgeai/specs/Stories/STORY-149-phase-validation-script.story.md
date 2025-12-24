---
id: STORY-149
title: Phase Completion Validation Script
type: feature
status: Backlog
priority: High
story-points: 3
epic: EPIC-031
sprint: null
created: 2025-12-23
assignee: null
depends-on: [STORY-148]
blocks: [STORY-150, STORY-152]
---

## User Story

**As a** phase enforcement system,
**I want** to validate that previous TDD phases are complete before allowing progression to the next phase,
**So that** the Phase Execution Enforcement System (Layer 2) can BLOCK phase transitions when subagents are skipped or checkpoints fail.

---

## Acceptance Criteria

### AC#1: CLI command validates phase completion

**Given** a story workflow is in progress
**When** `devforgeai-validate phase-check STORY-XXX --from=01 --to=02` is called
**Then** the command validates that phase 01 is complete and returns exit code 0 (proceed), 1 (blocked), or 2 (error).

### AC#2: Validates all required subagents invoked

**Given** phase state file exists for the story
**When** `phase-check` validates phase completion
**Then** it verifies all subagents_required were recorded in subagents_invoked list, rejecting progression if any subagents are missing.

### AC#3: Validates checkpoint passed flag

**Given** a phase has all subagents invoked
**When** `phase-check` validates phase completion
**Then** it checks that checkpoint_passed=true, blocking progression if checkpoint validation failed.

### AC#4: Record subagent invocation command

**Given** a subagent has completed execution
**When** `devforgeai-validate record-subagent STORY-XXX --phase=01 --subagent=git-validator` is called
**Then** the subagent name is appended to the phase's subagents_invoked list in the state file.

### AC#5: Complete phase command marks completion

**Given** all subagents for a phase have been invoked
**When** `devforgeai-validate complete-phase STORY-XXX --phase=01` is called
**Then** the phase status is updated to "completed", completion_timestamp recorded, and exit code 0 returned.

### AC#6: Exit codes enable external enforcement

**Given** validation commands complete
**When** called from hooks or orchestrators
**Then** exit code 0 (proceed), 1 (blocked), or 2 (error) enables external tools to HALT workflows.

---

## Technical Specification

```yaml
technical_specification:
  version: "2.0"

  components:
    - type: API
      name: validate_phase_check
      endpoint: "devforgeai-validate phase-check"
      method: "CLI"
      description: "Validate phase completion before progression"
      parameters:
        - name: story_id
          type: string
          pattern: "STORY-\\d{3}"
          required: true
        - name: from_phase
          type: string
          enum: ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10"]
          required: true
        - name: to_phase
          type: string
          enum: ["02", "03", "04", "05", "06", "07", "08", "09", "10"]
          required: true
      response:
        status_codes:
          - code: 0
            description: "Proceed - previous phase complete"
          - code: 1
            description: "Blocked - previous phase incomplete"
          - code: 2
            description: "Error - state file missing/invalid"
      test_requirement: "test_phase_check_validates_completion"

    - type: API
      name: record_subagent_invocation
      endpoint: "devforgeai-validate record-subagent"
      method: "CLI"
      parameters:
        - name: story_id
          type: string
          pattern: "STORY-\\d{3}"
          required: true
        - name: phase_id
          type: string
          enum: ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10"]
          required: true
        - name: subagent_name
          type: string
          required: true
      response:
        status_codes:
          - code: 0
            description: "Subagent recorded successfully"
          - code: 2
            description: "Error - state file not found"
      test_requirement: "test_record_subagent_appends_entry"

    - type: API
      name: complete_phase
      endpoint: "devforgeai-validate complete-phase"
      method: "CLI"
      parameters:
        - name: story_id
          type: string
          pattern: "STORY-\\d{3}"
          required: true
        - name: phase_id
          type: string
          enum: ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10"]
          required: true
        - name: checkpoint_passed
          type: boolean
          default: true
          required: false
      response:
        status_codes:
          - code: 0
            description: "Phase marked complete"
          - code: 2
            description: "Error - state file not found/invalid"
      test_requirement: "test_complete_phase_marks_completion"

    - type: Module
      name: validate_phase_completion.py
      file_path: installer/validate_phase_completion.py
      description: "Python module implementing phase validation CLI commands"
      dependencies:
        - json (stdlib)
        - argparse (stdlib)
        - pathlib (stdlib)
        - sys (stdlib)
        - installer.phase_state (internal)

  business_rules:
    - id: BR-001
      description: "Exit code 0 allows progression, 1 blocks progression"
      validation: "Return codes strictly enforced for hook integration"
      test_requirement: "test_exit_codes_enable_blocking"

    - id: BR-002
      description: "All required subagents must be recorded before phase complete"
      validation: "missing_subagents check before allowing complete_phase"
      test_requirement: "test_complete_phase_requires_all_subagents"

    - id: BR-003
      description: "Checkpoint must pass before allowing phase complete"
      validation: "checkpoint_passed flag checked before completion"
      test_requirement: "test_complete_phase_requires_checkpoint"

  non_functional_requirements:
    - category: Performance
      requirement: "phase-check command < 30ms (reading state file + validation)"
      metric: "p95 latency"
      test_requirement: "test_phase_check_performance"

    - category: Reliability
      requirement: "All validation errors include specific reason (missing subagent X, checkpoint failed, etc.)"
      metric: "100% of errors have actionable messages"
      test_requirement: "test_error_messages_specific"

    - category: Integration
      requirement: "Exit codes enable hook-based blocking (exit code 1 blocks Task() invocation)"
      metric: "Used by pre-phase-transition hook"
      test_requirement: "test_exit_code_blocking"
```

---

## Edge Cases

1. **Story ID doesn't exist:** Return exit code 2 with "State file not found" message
2. **Incomplete phase validation:** Record subagents succeed, but complete_phase blocked until all subagents recorded
3. **Checkpoint failed:** complete_phase rejects with "checkpoint_passed=false" if not explicitly set to true
4. **Invalid phase IDs:** Return exit code 2 with "Invalid phase ID" message

---

## Definition of Done

### Implementation
- [ ] `installer/validate_phase_completion.py` created with 3 CLI commands
- [ ] `phase-check` command implemented and tested
- [ ] `record-subagent` command implemented and tested
- [ ] `complete-phase` command implemented and tested
- [ ] CLI entry points registered in setup.py

### Quality
- [ ] Unit test coverage >= 95%
- [ ] Exit codes validated (0, 1, 2 only)
- [ ] Error messages are specific and actionable
- [ ] No anti-pattern violations
- [ ] Code follows PEP 8

### Testing
- [ ] test_phase_check_validates_completion passes
- [ ] test_phase_check_blocks_missing_subagents passes
- [ ] test_record_subagent_appends_entry passes
- [ ] test_complete_phase_marks_completion passes
- [ ] test_exit_codes_enable_blocking passes
- [ ] test_error_messages_specific passes

---

## Dependencies

**Upstream:** STORY-148 (requires PhaseState module)
**Downstream:** STORY-150, STORY-152 (hooks and skills use these commands)

---

## Related Documents

| Document | Path |
|----------|------|
| Epic | `devforgeai/specs/Epics/EPIC-031-phase-execution-enforcement.epic.md` |
| Plan | `/home/bryan/.claude/plans/moonlit-meandering-bumblebee.md` |
| Layer 1 Story | `devforgeai/specs/Stories/STORY-148-phase-state-file-module.story.md` |

---

## Workflow Status

**Current Status:** Backlog
**Created:** 2025-12-23

---
id: STORY-153
title: Skill Validation Integration
type: feature
status: Backlog
priority: Medium
story-points: 3
epic: EPIC-031
sprint: null
created: 2025-12-24
updated: 2025-12-24
assignee: null
depends-on: [STORY-150, STORY-151]
blocks: [STORY-154]
---

## User Story

**As a** development workflow orchestrator,
**I want** the devforgeai-development SKILL.md to include validation calls at each phase transition,
**So that** the Phase Execution Enforcement System is actively invoked during TDD workflow execution, ensuring phases cannot be skipped even if Claude attempts to proceed without completing required steps.

---

## Acceptance Criteria

### AC#1: Add validation call before each phase transition

**Given** the devforgeai-development SKILL.md defines 10 TDD phases
**When** each phase begins execution
**Then** the SKILL.md instructs Claude to call `Bash(command="devforgeai-validate phase-check {story_id} {target_phase}")` and HALT if the exit code is non-zero.

### AC#2: Add subagent recording after each subagent invocation

**Given** a phase invokes a subagent using the Task tool
**When** the subagent invocation completes successfully
**Then** the SKILL.md instructs Claude to call `Bash(command="devforgeai-validate record-subagent {story_id} {phase_id} {subagent_name}")` immediately after the Task returns.

### AC#3: Add checkpoint completion call at phase end

**Given** a phase has completed all its required steps
**When** the phase is ready to transition to the next phase
**Then** the SKILL.md instructs Claude to call `Bash(command="devforgeai-validate complete-phase {story_id} {phase_id} --checkpoint-passed")` before proceeding.

### AC#4: Initialize state file at workflow start

**Given** the /dev command begins a new story implementation
**When** Phase 00 (Preflight) starts
**Then** the SKILL.md instructs Claude to call `Bash(command="devforgeai-validate init-state {story_id}")` as the first action, creating the phase state tracking file.

### AC#5: Provide clear error handling for validation failures

**Given** any devforgeai-validate command returns non-zero exit code
**When** Claude processes the command result
**Then** the SKILL.md instructs Claude to:
1. Display the error output to the user
2. HALT with message "Phase enforcement check failed. Complete required steps before proceeding."
3. Do NOT attempt to bypass or continue the workflow

### AC#6: Maintain backward compatibility with existing workflows

**Given** the SKILL.md is updated with validation calls
**When** the devforgeai-validate CLI is not installed (legacy environment)
**Then** the validation calls detect missing CLI and display warning "Phase enforcement not available - CLI not installed. Run: pip install devforgeai-validate" but allow workflow to continue with warning.

---

## Technical Specification

```yaml
technical_specification:
  version: "2.0"

  components:
    - type: SkillModification
      name: devforgeai-development SKILL.md Updates
      file_path: .claude/skills/devforgeai-development/SKILL.md
      description: "Add validation calls at phase transition points"
      modifications:
        - location: "Phase 00: Preflight"
          insertion_point: "After story file validation"
          code: |
            # Initialize phase state tracking
            Bash(command="devforgeai-validate init-state {story_id}")
          test_requirement: "test_init_state_called_at_start"

        - location: "Each phase transition point"
          insertion_point: "Before phase header"
          code: |
            # Validate previous phase complete before proceeding
            result = Bash(command="devforgeai-validate phase-check {story_id} {phase_id}")
            IF result.exit_code != 0:
                Display: result.stderr
                HALT: "Phase enforcement check failed"
          test_requirement: "test_phase_check_blocks_incomplete"

        - location: "After each Task(subagent_type=...) call"
          insertion_point: "Immediately after Task returns"
          code: |
            # Record subagent invocation
            Bash(command="devforgeai-validate record-subagent {story_id} {phase_id} {subagent_type}")
          test_requirement: "test_subagent_recorded_after_task"

        - location: "End of each phase"
          insertion_point: "Before 'Proceed to Phase XX'"
          code: |
            # Mark phase complete with checkpoint
            Bash(command="devforgeai-validate complete-phase {story_id} {phase_id} --checkpoint-passed")
          test_requirement: "test_complete_phase_called"

    - type: Configuration
      name: ValidationCallLocations
      file_path: devforgeai/config/validation-call-locations.yaml
      description: "Mapping of where validation calls are inserted in SKILL.md"
      content:
        phases:
          - id: "00"
            name: "Preflight"
            init_state: true
            phase_check: false  # First phase, no prior check
            subagents: []
            complete_phase: true
          - id: "01"
            name: "Tech Stack Detection"
            phase_check: true
            subagents: ["tech-stack-detector"]
            complete_phase: true
          - id: "02"
            name: "Test Generation (Red)"
            phase_check: true
            subagents: ["test-automator"]
            complete_phase: true
          - id: "03"
            name: "Implementation (Green)"
            phase_check: true
            subagents: ["backend-architect", "frontend-developer"]
            complete_phase: true
          - id: "04"
            name: "Refactoring"
            phase_check: true
            subagents: ["refactoring-specialist"]
            complete_phase: true
          - id: "05"
            name: "Integration Testing"
            phase_check: true
            subagents: ["integration-tester"]
            complete_phase: true
          - id: "06"
            name: "Code Review"
            phase_check: true
            subagents: ["code-reviewer", "security-auditor"]
            complete_phase: true
          - id: "07"
            name: "DoD Update Bridge"
            phase_check: true
            subagents: ["deferral-validator"]
            complete_phase: true
          - id: "08"
            name: "Git Commit"
            phase_check: true
            subagents: []
            complete_phase: true
          - id: "09"
            name: "Feedback Hooks"
            phase_check: true
            subagents: []
            complete_phase: true
          - id: "10"
            name: "Result Interpretation"
            phase_check: true
            subagents: ["dev-result-interpreter"]
            complete_phase: true
      test_requirement: "test_validation_locations_complete"

  business_rules:
    - id: BR-001
      description: "Validation calls are MANDATORY at every phase transition"
      validation: "Every phase except 00 has phase-check call"
      test_requirement: "test_all_phases_have_validation"

    - id: BR-002
      description: "Validation failure HALTS workflow immediately"
      validation: "Non-zero exit → HALT (no continue option)"
      test_requirement: "test_halt_on_validation_failure"

    - id: BR-003
      description: "Subagent recording follows every Task invocation"
      validation: "Every Task(subagent_type=...) followed by record-subagent"
      test_requirement: "test_subagent_recording_coverage"

    - id: BR-004
      description: "Missing CLI triggers warning but allows continuation"
      validation: "CLI not found → warn, continue (backward compatibility)"
      test_requirement: "test_backward_compatibility"

  non_functional_requirements:
    - category: Maintainability
      requirement: "Validation calls use consistent pattern across all phases"
      metric: "100% pattern consistency"
      test_requirement: "test_pattern_consistency"

    - category: Observability
      requirement: "All validation calls logged via CLI audit trail"
      metric: "Full traceability in phase-enforcement.log"
      test_requirement: "test_audit_trail_complete"

    - category: Reliability
      requirement: "Validation call failure blocks workflow (fail-closed)"
      metric: "100% of validation failures result in HALT"
      test_requirement: "test_fail_closed_behavior"
```

---

## Edge Cases

1. **CLI not installed:** Warning message, continue workflow (backward compatibility)
2. **CLI command timeout:** Treat as failure, HALT workflow
3. **Story ID not available:** Extract from story file path in context
4. **Phase ID mismatch:** CLI validates against state file
5. **Concurrent /dev invocations:** Each has separate state file
6. **Skill file has merge conflicts:** Validation during PR review
7. **User tries to skip validation:** Cannot bypass - validation is inline in SKILL.md

---

## Definition of Done

### Implementation
- [ ] SKILL.md updated with init-state call in Phase 00
- [ ] SKILL.md updated with phase-check calls at each phase start
- [ ] SKILL.md updated with record-subagent calls after each Task
- [ ] SKILL.md updated with complete-phase calls at each phase end
- [ ] Error handling with HALT on validation failure
- [ ] Backward compatibility check for missing CLI
- [ ] validation-call-locations.yaml created

### Quality
- [ ] All 10 phases have appropriate validation calls
- [ ] Pattern consistency verified across phases
- [ ] No regression in existing SKILL.md functionality
- [ ] Validation call locations documented

### Testing
- [ ] `test_init_state_called_at_start` passes
- [ ] `test_phase_check_blocks_incomplete` passes
- [ ] `test_subagent_recorded_after_task` passes
- [ ] `test_complete_phase_called` passes
- [ ] `test_all_phases_have_validation` passes
- [ ] `test_halt_on_validation_failure` passes
- [ ] `test_backward_compatibility` passes

### Documentation
- [ ] SKILL.md changes documented in changelog
- [ ] Validation pattern documented for future skill authors
- [ ] Migration notes for existing workflows

---

## Dependencies

### Upstream (this story depends on)
- STORY-150: Pre-Phase-Transition Hook (validation hook infrastructure)
- STORY-151: Post-Subagent Recording Hook (recording hook infrastructure)

### Downstream (blocked by this story)
- STORY-154: Integration Testing (end-to-end validation of enforcement system)

---

## Related Documents

| Document | Path |
|----------|------|
| Epic | `devforgeai/specs/Epics/EPIC-031-phase-execution-enforcement.epic.md` |
| RCA-022 | `devforgeai/RCA/RCA-022-mandatory-tdd-phases-skipped.md` |
| Current SKILL.md | `.claude/skills/devforgeai-development/SKILL.md` |
| STORY-149 | `devforgeai/specs/Stories/STORY-149-phase-validation-script.story.md` |

---

## Workflow Status

**Current Status:** Backlog
**Created:** 2025-12-24
**Last Updated:** 2025-12-24

### Status History
| Date | From | To | By | Notes |
|------|------|-----|-----|-------|
| 2025-12-24 | - | Backlog | DevForgeAI | Story created via /create-missing-stories EPIC-031 |

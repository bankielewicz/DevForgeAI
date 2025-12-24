---
id: STORY-150
title: Pre-Phase-Transition Hook
type: feature
status: Backlog
priority: High
story-points: 2
epic: EPIC-031
sprint: null
created: 2025-12-24
updated: 2025-12-24
assignee: null
depends-on: [STORY-149]
blocks: [STORY-153]
---

## User Story

**As a** development workflow orchestrator,
**I want** a Claude Code hook that validates phase completion before allowing transitions,
**So that** the Phase Execution Enforcement System (Layer 3) can block phase skipping by requiring external validation at each transition point.

---

## Acceptance Criteria

### AC#1: Hook registration in hooks configuration

**Given** the Claude Code environment is configured with hooks support
**When** the hooks.yaml file is loaded at startup
**Then** the pre-phase-transition hook is registered with:
- Event: `pre_tool_call` (triggered before Task tool invocation)
- Filter: Task calls with subagent_type containing phase-related patterns
- Script: `devforgeai/hooks/pre-phase-transition.sh`
- Blocking: true (prevents execution if validation fails)

### AC#2: Validate previous phase completion before transition

**Given** the hook is triggered during a phase transition attempt
**When** the script executes with current story_id and target_phase parameters
**Then** the script reads the phase state file, checks if the previous phase has status "completed" and checkpoint_passed=true, and returns exit code 0 (proceed) if valid or exit code 1 (block) if invalid.

### AC#3: Block transition with descriptive error message

**Given** a phase transition is attempted but the previous phase is incomplete
**When** the validation check fails
**Then** the hook outputs a structured error message containing:
- Which phase is incomplete
- What subagents were expected vs invoked
- Remediation guidance ("Complete phase XX before proceeding")
And the hook returns exit code 1 to block the transition.

### AC#4: Allow first phase without prior validation

**Given** the target phase is "01" (first phase in workflow)
**When** the hook validation runs
**Then** the validation passes automatically (no previous phase to check), and the hook returns exit code 0 to allow the transition.

### AC#5: Handle missing state file gracefully

**Given** a phase transition is attempted but no state file exists for the story
**When** the hook attempts to read the state file
**Then** the hook creates a new state file using `devforgeai-validate init-state {story_id}` before proceeding with validation, ensuring all workflows have proper tracking from first transition.

### AC#6: Log all validation decisions

**Given** any hook execution completes (pass or fail)
**When** the validation result is determined
**Then** the decision is logged to `devforgeai/logs/phase-enforcement.log` with timestamp, story_id, target_phase, decision (allowed/blocked), and reason.

---

## Technical Specification

```yaml
technical_specification:
  version: "2.0"

  components:
    - type: Script
      name: pre-phase-transition.sh
      file_path: devforgeai/hooks/pre-phase-transition.sh
      description: "Bash hook script for pre-phase validation"
      dependencies:
        - devforgeai-validate CLI (STORY-149)
        - jq (JSON parsing)
      inputs:
        - name: CLAUDE_TOOL_NAME
          type: string
          source: environment
          description: "Tool being invoked (Task)"
        - name: CLAUDE_TOOL_INPUT
          type: string
          source: environment
          description: "JSON input to tool (contains subagent_type)"
      outputs:
        - exit_code: 0
          meaning: "Validation passed, proceed with transition"
        - exit_code: 1
          meaning: "Validation failed, block transition"
      test_requirement: "test_hook_blocks_incomplete_phase"

    - type: Configuration
      name: hooks.yaml
      file_path: .claude/hooks.yaml
      description: "Claude Code hooks registration"
      required_entries:
        - event: pre_tool_call
          hooks:
            - name: pre-phase-transition
              script: devforgeai/hooks/pre-phase-transition.sh
              blocking: true
              filter:
                tool: Task
                subagent_type_pattern: ".*-validator|.*-specialist|.*-automator"
      test_requirement: "test_hook_registered_correctly"

    - type: Logging
      name: PhaseEnforcementLog
      file_path: devforgeai/logs/phase-enforcement.log
      description: "Audit trail for all phase transition decisions"
      format: JSON Lines
      fields:
        - name: timestamp
          type: ISO-8601
        - name: story_id
          type: string
        - name: target_phase
          type: string
        - name: decision
          type: enum
          values: ["allowed", "blocked"]
        - name: reason
          type: string
      test_requirement: "test_log_captures_all_decisions"

  business_rules:
    - id: BR-001
      description: "Phase 01 always passes validation (no prior phase)"
      validation: "target_phase == '01' → return 0"
      test_requirement: "test_phase_01_always_allowed"

    - id: BR-002
      description: "All other phases require previous phase completed"
      validation: "phases[N-1].status == 'completed' AND phases[N-1].checkpoint_passed == true"
      test_requirement: "test_requires_previous_phase_complete"

    - id: BR-003
      description: "Missing state file triggers automatic initialization"
      validation: "State file missing → call devforgeai-validate init-state"
      test_requirement: "test_auto_init_on_missing_state"

    - id: BR-004
      description: "Logging is mandatory for all validation decisions"
      validation: "Every hook execution must append to phase-enforcement.log"
      test_requirement: "test_logging_mandatory"

  non_functional_requirements:
    - category: Performance
      requirement: "Hook execution < 100ms to avoid workflow latency"
      metric: "p95 latency"
      test_requirement: "test_hook_performance"

    - category: Reliability
      requirement: "Hook failure defaults to blocking (fail-closed)"
      metric: "100% of failures result in blocked transitions"
      test_requirement: "test_fail_closed_behavior"

    - category: Observability
      requirement: "All decisions logged with sufficient context for debugging"
      metric: "Log entries contain all fields (timestamp, story_id, target_phase, decision, reason)"
      test_requirement: "test_log_completeness"
```

---

## Edge Cases

1. **No state file exists:** Auto-initialize using `devforgeai-validate init-state`
2. **State file corrupted:** Log error, block transition, report corruption
3. **Previous phase has status "skipped":** Treat as valid (skipped phases don't block)
4. **jq not installed:** Error message with installation instructions
5. **Hook script not executable:** Error message with chmod instructions
6. **Concurrent transitions:** File locking in state module handles this (STORY-148)
7. **Story ID extraction fails:** Block transition with parse error message

---

## Definition of Done

### Implementation
- [ ] `devforgeai/hooks/pre-phase-transition.sh` script created
- [ ] Script reads state file and validates previous phase
- [ ] Script outputs structured error messages on failure
- [ ] Script logs all decisions to phase-enforcement.log
- [ ] `.claude/hooks.yaml` updated with hook registration
- [ ] Auto-initialization on missing state file implemented

### Quality
- [ ] Unit test coverage >= 95%
- [ ] All edge cases have tests
- [ ] No anti-pattern violations
- [ ] Script follows Bash best practices (set -euo pipefail)
- [ ] ShellCheck passes with no warnings

### Testing
- [ ] `test_hook_blocks_incomplete_phase` passes
- [ ] `test_hook_registered_correctly` passes
- [ ] `test_phase_01_always_allowed` passes
- [ ] `test_requires_previous_phase_complete` passes
- [ ] `test_auto_init_on_missing_state` passes
- [ ] `test_log_captures_all_decisions` passes
- [ ] `test_hook_performance` meets < 100ms threshold

### Documentation
- [ ] Hook usage documented in script header
- [ ] Error messages include remediation steps
- [ ] Log format documented for parsing

---

## Dependencies

### Upstream (this story depends on)
- STORY-149: Phase Validation Script (provides devforgeai-validate CLI)

### Downstream (blocked by this story)
- STORY-153: Skill Validation Integration (requires hooks in place)

---

## Related Documents

| Document | Path |
|----------|------|
| Epic | `devforgeai/specs/Epics/EPIC-031-phase-execution-enforcement.epic.md` |
| RCA-022 | `devforgeai/RCA/RCA-022-mandatory-tdd-phases-skipped.md` |
| STORY-148 | `devforgeai/specs/Stories/STORY-148-phase-state-file-module.story.md` |
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

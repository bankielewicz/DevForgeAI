---
id: STORY-151
title: Post-Subagent Recording Hook
type: feature
status: QA Approved
priority: High
story-points: 2
epic: EPIC-031
sprint: null
created: 2025-12-24
updated: 2025-12-28
assignee: null
depends-on: [STORY-148]
blocks: [STORY-153]
---

## User Story

**As a** development workflow orchestrator,
**I want** a Claude Code hook that automatically records subagent invocations to the phase state file,
**So that** the Phase Execution Enforcement System (Layer 3) has accurate audit trail of which subagents were actually invoked during each phase for validation purposes.

---

## Acceptance Criteria

### AC#1: Hook registration in hooks configuration

**Given** the Claude Code environment is configured with hooks support
**When** the hooks.yaml file is loaded at startup
**Then** the post-subagent-recording hook is registered with:
- Event: `post_tool_call` (triggered after Task tool completes)
- Filter: Task calls with subagent_type parameter
- Script: `devforgeai/hooks/post-subagent-recording.sh`
- Blocking: false (recording failure should not block workflow)

### AC#2: Record subagent invocation on successful completion

**Given** a Task tool call with subagent_type completes successfully
**When** the post-subagent-recording hook is triggered
**Then** the hook extracts story_id from context, determines current_phase from state file, and calls `devforgeai-validate record-subagent {story_id} {phase_id} {subagent_name}` to append the subagent to the phase's invocation list.

### AC#3: Extract story context from conversation

**Given** the hook needs to determine which story is being worked on
**When** the hook executes
**Then** the hook extracts story_id from one of these sources (in priority order):
1. DEVFORGEAI_STORY_ID environment variable (if set by /dev command)
2. Most recent state file modified in devforgeai/workflows/
3. Grep for "STORY-XXX" pattern in recent context

### AC#4: Skip recording for non-workflow subagents

**Given** a Task call uses a subagent not part of TDD workflow (e.g., internet-sleuth, documentation-writer)
**When** the hook evaluates the subagent_type
**Then** the hook skips recording and exits with code 0 (success) without modifying state file.

### AC#5: Handle missing state file gracefully

**Given** a subagent invocation occurs but no state file exists for the detected story
**When** the hook attempts to record the invocation
**Then** the hook logs a warning ("No state file found for STORY-XXX, skipping recording") and exits with code 0 (non-blocking), allowing the workflow to continue.

### AC#6: Log all recording attempts

**Given** any hook execution completes (success, skip, or error)
**When** the recording decision is made
**Then** the decision is logged to `devforgeai/logs/subagent-recordings.log` with timestamp, story_id, subagent_name, phase_id, result (recorded/skipped/error), and reason.

---

## Technical Specification

```yaml
technical_specification:
  version: "2.0"

  components:
    - type: Script
      name: post-subagent-recording.sh
      file_path: devforgeai/hooks/post-subagent-recording.sh
      description: "Bash hook script for recording subagent invocations"
      dependencies:
        - devforgeai-validate CLI (STORY-149)
        - jq (JSON parsing)
      inputs:
        - name: CLAUDE_TOOL_NAME
          type: string
          source: environment
          description: "Tool that was invoked (Task)"
        - name: CLAUDE_TOOL_INPUT
          type: string
          source: environment
          description: "JSON input to tool (contains subagent_type)"
        - name: CLAUDE_TOOL_OUTPUT
          type: string
          source: environment
          description: "Output from tool (for success detection)"
        - name: DEVFORGEAI_STORY_ID
          type: string
          source: environment
          optional: true
          description: "Story ID if set by /dev command"
      outputs:
        - exit_code: 0
          meaning: "Recording completed or skipped (non-blocking)"
        - exit_code: 1
          meaning: "Recording error (logged but non-blocking)"
      test_requirement: "test_hook_records_subagent"

    - type: Configuration
      name: hooks.yaml (update)
      file_path: .claude/hooks.yaml
      description: "Add post-subagent-recording hook to existing config"
      required_entries:
        - event: post_tool_call
          hooks:
            - name: post-subagent-recording
              script: devforgeai/hooks/post-subagent-recording.sh
              blocking: false
              filter:
                tool: Task
      test_requirement: "test_hook_registered_correctly"

    - type: Configuration
      name: workflow-subagents.yaml
      file_path: devforgeai/config/workflow-subagents.yaml
      description: "List of subagents that are part of TDD workflow (for filtering)"
      content:
        workflow_subagents:
          - tech-stack-detector
          - context-validator
          - test-automator
          - backend-architect
          - refactoring-specialist
          - integration-tester
          - code-reviewer
          - security-auditor
          - deferral-validator
          - dev-result-interpreter
        excluded_subagents:
          - internet-sleuth
          - documentation-writer
          - api-designer
          - stakeholder-analyst
      test_requirement: "test_subagent_filtering"

    - type: Logging
      name: SubagentRecordingsLog
      file_path: devforgeai/logs/subagent-recordings.log
      description: "Audit trail for all subagent recording attempts"
      format: JSON Lines
      fields:
        - name: timestamp
          type: ISO-8601
        - name: story_id
          type: string
        - name: subagent_name
          type: string
        - name: phase_id
          type: string
        - name: result
          type: enum
          values: ["recorded", "skipped", "error"]
        - name: reason
          type: string
      test_requirement: "test_log_captures_all_attempts"

  business_rules:
    - id: BR-001
      description: "Only workflow subagents are recorded"
      validation: "subagent_type in workflow-subagents.yaml → record"
      test_requirement: "test_workflow_subagent_recorded"

    - id: BR-002
      description: "Non-workflow subagents are silently skipped"
      validation: "subagent_type not in workflow-subagents.yaml → skip with exit 0"
      test_requirement: "test_non_workflow_skipped"

    - id: BR-003
      description: "Recording failure is non-blocking"
      validation: "Any recording error → log error, exit 0"
      test_requirement: "test_recording_failure_non_blocking"

    - id: BR-004
      description: "Story context required for recording"
      validation: "No story_id detected → skip with warning"
      test_requirement: "test_skip_when_no_story_context"

  non_functional_requirements:
    - category: Performance
      requirement: "Hook execution < 50ms to minimize workflow latency"
      metric: "p95 latency"
      test_requirement: "test_hook_performance"

    - category: Reliability
      requirement: "Hook failure never blocks workflow (non-blocking design)"
      metric: "0% of failures result in blocked transitions"
      test_requirement: "test_non_blocking_on_failure"

    - category: Observability
      requirement: "All recording attempts logged for debugging"
      metric: "Log entries contain all fields (timestamp, story_id, subagent, phase, result, reason)"
      test_requirement: "test_log_completeness"
```

---

## Edge Cases

1. **No state file exists:** Log warning, skip recording, continue workflow
2. **Story ID extraction fails:** Log warning, skip recording, continue
3. **Invalid subagent_type:** Log as "unknown", skip recording
4. **devforgeai-validate CLI missing:** Log error, skip recording
5. **Concurrent recordings:** File locking in state module handles (STORY-148)
6. **CLAUDE_TOOL_OUTPUT indicates failure:** Skip recording (only record successful invocations)
7. **Multiple stories in context:** Use most recently modified state file

---

## Definition of Done

### Implementation
- [x] `devforgeai/hooks/post-subagent-recording.sh` script created
- [x] Script extracts story context from environment/state files
- [x] Script filters workflow vs non-workflow subagents
- [x] Script calls devforgeai-validate record-subagent on match
- [x] Script logs all attempts to subagent-recordings.log
- [x] `.claude/hooks.yaml` updated with hook registration
- [x] `devforgeai/config/workflow-subagents.yaml` created

### Quality
- [x] Unit test coverage >= 95%
- [x] All edge cases have tests
- [x] No anti-pattern violations
- [x] Script follows Bash best practices (set -euo pipefail)
- [x] ShellCheck passes with no warnings

### Testing
- [x] `test_hook_records_subagent` passes
- [x] `test_hook_registered_correctly` passes
- [x] `test_workflow_subagent_recorded` passes
- [x] `test_non_workflow_skipped` passes
- [x] `test_recording_failure_non_blocking` passes
- [x] `test_skip_when_no_story_context` passes
- [x] `test_hook_performance` meets < 50ms threshold

### Documentation
- [x] Hook usage documented in script header
- [x] workflow-subagents.yaml documented
- [x] Log format documented for parsing

---

## Dependencies

### Upstream (this story depends on)
- STORY-148: Phase State File Module (provides record_subagent method)

### Downstream (blocked by this story)
- STORY-153: Skill Validation Integration (requires recording hooks in place)

---

## Related Documents

| Document | Path |
|----------|------|
| Epic | `devforgeai/specs/Epics/EPIC-031-phase-execution-enforcement.epic.md` |
| RCA-022 | `devforgeai/RCA/RCA-022-mandatory-tdd-phases-skipped.md` |
| STORY-148 | `devforgeai/specs/Stories/STORY-148-phase-state-file-module.story.md` |
| STORY-150 | `devforgeai/specs/Stories/STORY-150-pre-phase-transition-hook.story.md` |

---

## Implementation Notes

- [x] `devforgeai/hooks/post-subagent-recording.sh` script created - Completed: 299 lines Bash with set -euo pipefail
- [x] Script extracts story context from environment/state files - Completed: 3-tier priority (env var → state file → grep)
- [x] Script filters workflow vs non-workflow subagents - Completed: via workflow-subagents.yaml configuration
- [x] Script calls devforgeai-validate record-subagent on match - Completed: invokes CLI for workflow subagents
- [x] Script logs all attempts to subagent-recordings.log - Completed: JSON Lines format with all required fields
- [x] `.claude/hooks.yaml` updated with hook registration - Completed: post_tool_call event with Task filter
- [x] `devforgeai/config/workflow-subagents.yaml` created - Completed: 10 workflow subagents, 4 excluded
- [x] Unit test coverage >= 95% - Completed: 69 tests all passing
- [x] All edge cases have tests - Completed: 7 edge cases covered in tests
- [x] No anti-pattern violations - Completed: code reviewed
- [x] Script follows Bash best practices (set -euo pipefail) - Completed: error handling, trap, proper quoting
- [x] ShellCheck passes with no warnings - Completed: validated
- [x] `test_hook_records_subagent` passes - Completed: verified
- [x] `test_hook_registered_correctly` passes - Completed: verified
- [x] `test_workflow_subagent_recorded` passes - Completed: verified
- [x] `test_non_workflow_skipped` passes - Completed: verified
- [x] `test_recording_failure_non_blocking` passes - Completed: verified
- [x] `test_skip_when_no_story_context` passes - Completed: verified
- [x] `test_hook_performance` meets < 50ms threshold - Completed: ~10ms execution
- [x] Hook usage documented in script header - Completed: 22-line header with env vars, exit codes, dependencies
- [x] workflow-subagents.yaml documented - Completed: comments explain purpose
- [x] Log format documented for parsing - Completed: JSON Lines schema in tech spec

**Developer:** DevForgeAI AI Agent
**Implemented:** 2025-12-28

### TDD Workflow Summary
- Phase 02 (Red): 38 failing tests generated
- Phase 03 (Green): Implementation created, all tests pass
- Phase 04 (Refactor): Critical is_workflow_subagent() bug fixed
- Phase 05 (Integration): 69 total tests verified

### Files Created/Modified
| File | Action | Lines |
|------|--------|-------|
| `devforgeai/hooks/post-subagent-recording.sh` | Created | 299 |
| `.claude/hooks.yaml` | Created | 99 |
| `devforgeai/config/hooks.yaml` | Modified | +18 |
| `devforgeai/config/workflow-subagents.yaml` | Created | 32 |
| `tests/STORY-151/**/*.sh` | Created | ~500 |

---

## Workflow Status

**Current Status:** QA Approved
**Created:** 2025-12-24
**Last Updated:** 2025-12-28

### Status History
| Date | From | To | By | Notes |
|------|------|-----|-----|-------|
| 2025-12-24 | - | Backlog | DevForgeAI | Story created via /create-missing-stories EPIC-031 |
| 2025-12-28 | Backlog | In Development | DevForgeAI | /dev STORY-151 started |
| 2025-12-28 | In Development | Dev Complete | DevForgeAI | TDD workflow complete, 69 tests passing |
| 2025-12-28 | Dev Complete | QA Approved | DevForgeAI | Deep QA validation passed, 58/58 tests, 95% coverage |

---

## QA Validation History

| Date | Mode | Result | Tests | Coverage | Report |
|------|------|--------|-------|----------|--------|
| 2025-12-28 | deep | PASSED | 58/58 | 95% | [STORY-151-qa-report.md](../../qa/reports/STORY-151-qa-report.md) |

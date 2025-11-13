---
id: STORY-029
title: Wire hooks into create-sprint command
epic: EPIC-006
sprint: Sprint-3
status: Backlog
points: 5
priority: High
assigned_to: null
created: 2025-11-12
updated: 2025-11-12
format_version: "2.0"
tags: ["feedback-system", "hook-integration", "command-integration"]
---

# Story: Wire hooks into create-sprint command

## Description

**As a** framework maintainer,
**I want** the `/create-sprint` command to automatically invoke feedback hooks after sprint planning completion,
**so that** I can capture sprint planning insights, configuration decisions, and user preferences to continuously improve the sprint creation workflow and identify pain points in story selection and capacity planning.

## Acceptance Criteria

### 1. [x] Phase N added to /create-sprint command workflow

**Given** a user has successfully completed sprint planning via `/create-sprint` command
**When** the sprint file has been created and stories have been assigned to "Ready for Dev" status
**Then** the command executes Phase N which checks hook availability via `devforgeai check-hooks --operation=create-sprint --status=completed` and invokes hooks if enabled (exit code 0)

---

### 2. [x] Graceful degradation when hooks disabled

**Given** feedback hooks are disabled in `.devforgeai/config/hooks.yaml` (create-sprint: enabled: false)
**When** Phase N executes `devforgeai check-hooks --operation=create-sprint --status=completed`
**Then** the check returns non-zero exit code, hook invocation is skipped, and sprint creation completes successfully without feedback prompts

---

### 3. [x] Hook invocation with sprint context

**Given** feedback hooks are enabled and check-hooks returns success (exit code 0)
**When** Phase N invokes `devforgeai invoke-hooks --operation=create-sprint --sprint-name=${SPRINT_NAME} --story-count=${STORY_COUNT} --capacity=${CAPACITY_POINTS}`
**Then** the feedback system captures sprint planning context (sprint name, story count, total capacity), presents retrospective questions, and logs responses to `.devforgeai/feedback/create-sprint-*.json`

---

### 4. [x] Hook failure does not break sprint creation

**Given** feedback hooks are enabled but hook invocation fails (network error, missing config, Python exception)
**When** `devforgeai invoke-hooks --operation=create-sprint` returns non-zero exit code or throws exception
**Then** the error is logged to `.devforgeai/feedback/logs/hook-errors.log`, user sees warning message "Feedback collection failed (sprint creation succeeded)", and sprint file remains valid with all stories assigned

---

### 5. [x] Sprint creation without story assignment

**Given** user creates a sprint but selects zero stories (empty sprint for future planning)
**When** Phase N executes and `$STORY_COUNT` is 0
**Then** hooks are invoked with `--story-count=0 --capacity=0`, feedback questions adapt to "empty sprint" scenario (e.g., "Why create sprint without stories?"), and responses are logged normally

---

## Edge Cases

1. **Hook check command not found:** If `devforgeai` CLI not installed or not in PATH, `command -v devforgeai` returns non-zero, Phase N skips hook logic silently (logs warning to `.devforgeai/logs/command.log`)

2. **Concurrent sprint creation:** If multiple `/create-sprint` commands run simultaneously (unlikely but possible in CI/CD), hook invocations use unique timestamps in feedback filenames (`create-sprint-YYYY-MM-DD-HH-MM-SS-sprint-N.json`) to prevent file conflicts

3. **User interrupts feedback (Ctrl+C):** If user cancels feedback mid-questionnaire, partial responses are saved with `interrupted: true` flag, skip counter NOT incremented (interruption ≠ explicit skip)

4. **Sprint creation after quota exhaustion:** If feedback quota exhausted (e.g., 5 responses per day), `invoke-hooks` returns exit code 0 but skips questions, logs "Quota exhausted" message, and sprint creation proceeds

5. **Hook invocation timeout:** If feedback system hangs (>3 seconds), Phase N times out hook invocation, logs timeout error, displays "Feedback timed out (non-blocking)" message, and completes sprint creation

---

## Data Validation Rules

1. **Sprint name parameter:** Must match pattern `^Sprint-\d+$` or `^[A-Za-z0-9\s-]+$` (alphanumeric with spaces/hyphens), maximum 100 characters, passed to hooks as `--sprint-name="${SPRINT_NAME}"`

2. **Story count parameter:** Must be non-negative integer (0-999), calculated from story selection phase, passed as `--story-count=${STORY_COUNT}`

3. **Capacity parameter:** Must be non-negative integer (0-9999), sum of story points from selected stories, passed as `--capacity=${CAPACITY_POINTS}`

4. **Operation parameter:** Must be exactly `create-sprint` (hardcoded in Phase N), ensures correct hook configuration loaded

5. **Status parameter:** Must be exactly `completed` for Phase N (indicates successful sprint creation), triggers post-operation retrospective questions

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "Phase N Hook Integration"
      file_path: ".claude/commands/create-sprint.md"
      requirements:
        - id: "COMP-001"
          description: "Add Phase N section to /create-sprint command after Phase 4 (result display) and before completion message"
          testable: true
          test_requirement: "Test: Verify Phase N section exists in create-sprint.md between Phase 4 and final success message using grep"
          priority: "Critical"

        - id: "COMP-002"
          description: "Implement hook check call: devforgeai check-hooks --operation=create-sprint --status=completed"
          testable: true
          test_requirement: "Test: Execute check-hooks command with operation=create-sprint, verify exit code 0 when enabled, 1 when disabled"
          priority: "Critical"

        - id: "COMP-003"
          description: "Implement conditional hook invocation: if check returns 0, call devforgeai invoke-hooks --operation=create-sprint --sprint-name=${SPRINT_NAME} --story-count=${STORY_COUNT} --capacity=${CAPACITY_POINTS}"
          testable: true
          test_requirement: "Test: Mock check-hooks to return 0, verify invoke-hooks called with correct parameters (sprint name, story count, capacity)"
          priority: "Critical"

        - id: "COMP-004"
          description: "Pass sprint context parameters to invoke-hooks: sprint name from user input, story count from selection phase, capacity from story points sum"
          testable: true
          test_requirement: "Test: Create sprint with 5 stories (25 points total), verify invoke-hooks receives --story-count=5 --capacity=25"
          priority: "High"

        - id: "COMP-005"
          description: "Implement graceful degradation: if invoke-hooks fails (non-zero exit or exception), log warning and continue sprint creation without blocking"
          testable: true
          test_requirement: "Test: Mock invoke-hooks to return exit code 1, verify sprint file created successfully and warning logged to command output"
          priority: "Critical"

    - type: "Logging"
      name: "Hook Invocation Logging"
      file_path: ".devforgeai/logs/command.log"
      requirements:
        - id: "COMP-006"
          description: "Log Phase N execution start with timestamp and sprint context"
          testable: true
          test_requirement: "Test: Execute /create-sprint, verify log entry 'Phase N: Checking feedback hooks for operation=create-sprint sprint={name}' exists"
          priority: "Medium"

        - id: "COMP-007"
          description: "Log hook check result (enabled/disabled) for debugging"
          testable: true
          test_requirement: "Test: Run /create-sprint with hooks disabled, verify log entry 'Hook check returned non-zero, skipping invocation' exists"
          priority: "Medium"

        - id: "COMP-008"
          description: "Log hook invocation failures with error message and stack trace"
          testable: true
          test_requirement: "Test: Mock invoke-hooks to throw exception, verify log entry contains 'Hook invocation failed' with exception message"
          priority: "High"

        - id: "COMP-009"
          description: "Log successful hook invocation with feedback session ID"
          testable: true
          test_requirement: "Test: Execute hooks successfully, verify log entry 'Feedback session created: session-id-12345' exists"
          priority: "Low"

  business_rules:
    - id: "BR-001"
      rule: "Phase N must execute AFTER sprint file creation (Phase 4) completes successfully, ensuring hooks only run when sprint creation succeeds"
      test_requirement: "Test: Mock sprint file write failure in Phase 4, verify Phase N never executes (no check-hooks call in logs)"

    - id: "BR-002"
      rule: "Hook failures must NEVER block sprint creation - all hook errors are non-fatal and logged only"
      test_requirement: "Test: Mock all hook operations to fail (check-hooks, invoke-hooks), verify /create-sprint returns exit code 0 and sprint file exists"

    - id: "BR-003"
      rule: "Sprint name parameter must be shell-escaped to prevent command injection (use double quotes: --sprint-name=\"${SPRINT_NAME}\")"
      test_requirement: "Test: Create sprint with name containing shell metacharacters ('Sprint-1; rm -rf /'), verify hook invocation safely escapes parameters and no command injection occurs"

    - id: "BR-004"
      rule: "Empty sprints (zero stories selected) must still invoke hooks with --story-count=0 --capacity=0 to capture 'why create empty sprint' feedback"
      test_requirement: "Test: Create sprint with 0 stories selected, verify invoke-hooks called with --story-count=0 --capacity=0"

    - id: "BR-005"
      rule: "Hook check timeout: if check-hooks doesn't return within 5 seconds, skip hook invocation and log timeout error"
      test_requirement: "Test: Mock check-hooks to hang indefinitely, verify command times out after 5 seconds, logs timeout error, and completes sprint creation"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Hook check execution must complete in under 100ms to avoid noticeable delay in command completion"
      metric: "check-hooks --operation=create-sprint execution time < 100ms (measured via time command)"
      test_requirement: "Test: Execute check-hooks 100 times, calculate average execution time, assert average < 100ms"

    - id: "NFR-002"
      category: "Performance"
      requirement: "Hook invocation (before user interaction) must complete in under 3 seconds to avoid perceived latency"
      metric: "Time from invoke-hooks call to first AskUserQuestion prompt < 3 seconds"
      test_requirement: "Test: Measure timestamp before invoke-hooks and timestamp of first feedback question, assert delta < 3 seconds"

    - id: "NFR-003"
      category: "Performance"
      requirement: "Phase N total overhead must be under 3.5 seconds (check + invocation setup), excluding user response time"
      metric: "Phase N execution time (from start to AskUserQuestion or skip) < 3.5 seconds"
      test_requirement: "Test: Measure Phase N duration from log timestamps (Phase N start to 'Feedback prompt presented' or 'Hooks skipped'), assert < 3.5 seconds"

    - id: "NFR-004"
      category: "Reliability"
      requirement: "Sprint creation success rate must remain 100% regardless of hook status or failures"
      metric: "Sprint file created successfully in 100% of executions, even when hooks disabled/failing"
      test_requirement: "Test: Run /create-sprint 100 times with random hook failures (50% failure rate), verify 100 sprint files created with correct content"

    - id: "NFR-005"
      category: "Reliability"
      requirement: "Hook failure handling must be 100% graceful - errors logged, warnings displayed, execution continues"
      metric: "Zero unhandled exceptions in Phase N (all hook errors caught and logged)"
      test_requirement: "Test: Inject 10 different error scenarios (missing CLI, network error, Python exception, etc.), verify all handled gracefully with logged errors"

    - id: "NFR-006"
      category: "Security"
      requirement: "All sprint parameters passed to hooks must be shell-escaped to prevent command injection"
      metric: "No successful command injection via malicious sprint names or story IDs"
      test_requirement: "Test: Attempt command injection via sprint name ('Sprint; cat /etc/passwd'), verify injection blocked and hook parameters safely escaped"

    - id: "NFR-007"
      category: "Security"
      requirement: "Feedback files must be created with restrictive permissions (mode 0600 - user read/write only)"
      metric: "All files in .devforgeai/feedback/ have permissions -rw------- (600)"
      test_requirement: "Test: Execute hooks, create feedback file, verify file permissions via stat command equal 0600"

    - id: "NFR-008"
      category: "Scalability"
      requirement: "Concurrent sprint creation must support up to 10 simultaneous executions without feedback file conflicts"
      metric: "10 parallel /create-sprint executions complete successfully with unique feedback files"
      test_requirement: "Test: Run 10 /create-sprint commands in parallel (GNU parallel or xargs), verify 10 unique feedback files created (no overwrites)"
```

---

## Dependencies

### Prerequisite Stories

Stories that must complete BEFORE this story can start:

- [x] **STORY-021:** Implement devforgeai check-hooks CLI command
  - **Why:** Phase N requires check-hooks command to determine if feedback should trigger
  - **Status:** Complete

- [x] **STORY-022:** Implement devforgeai invoke-hooks CLI command
  - **Why:** Phase N requires invoke-hooks command to trigger feedback conversations
  - **Status:** Complete

### External Dependencies

None

### Technology Dependencies

None - Uses existing DevForgeAI CLI infrastructure

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for Phase N implementation logic

**Test Scenarios:**
1. **Happy Path:** Hooks enabled, check-hooks returns 0, invoke-hooks succeeds, feedback collected
2. **Edge Cases:**
   - Hooks disabled in config (check-hooks returns 1)
   - Empty sprint (story count = 0, capacity = 0)
   - Sprint name with special characters (shell escaping)
3. **Error Cases:**
   - check-hooks command not found (CLI not installed)
   - invoke-hooks returns non-zero exit code
   - invoke-hooks throws Python exception
   - Hook invocation timeout (>5 seconds)

**Example Test Structure:**
```bash
# Test: Phase N with hooks enabled
./tests/commands/test-create-sprint-hooks-enabled.sh

# Test: Phase N with hooks disabled
./tests/commands/test-create-sprint-hooks-disabled.sh

# Test: Phase N graceful degradation
./tests/commands/test-create-sprint-hook-failures.sh

# Test: Phase N shell escaping
./tests/commands/test-create-sprint-shell-injection.sh

# Test: Phase N concurrent execution
./tests/commands/test-create-sprint-concurrent-hooks.sh
```

---

### Integration Tests

**Coverage Target:** 85%+ for end-to-end sprint creation with hooks

**Test Scenarios:**
1. **End-to-End Sprint Creation with Feedback:** Create sprint → Phase N triggers → Feedback collected → Sprint file valid
2. **Sprint Creation with Hook Failures:** Create sprint → Hook fails → Warning displayed → Sprint file valid
3. **Concurrent Sprint Creation:** 10 parallel sprint creations → All succeed → 10 unique feedback files

**Example Test:**
```bash
#!/bin/bash
# Integration test: Sprint creation with feedback

# Arrange
export DEVFORGEAI_CONFIG_HOOKS_ENABLED=true
export TEST_SPRINT_NAME="Sprint-Integration-Test"

# Act
/create-sprint "$TEST_SPRINT_NAME" < story_selections.txt

# Assert
test -f ".ai_docs/Sprints/$TEST_SPRINT_NAME.md" || exit 1
test -f ".devforgeai/feedback/create-sprint-*.json" || exit 1
grep -q "Feedback session created" .devforgeai/logs/command.log || exit 1

echo "✅ Integration test passed"
```

---

### E2E Tests (If Applicable)

**Coverage Target:** Critical path only (sprint creation with feedback)

**Test Scenarios:**
1. **Critical User Journey:** User runs /create-sprint → Selects stories → Sprint created → Feedback prompt appears → User responds → Feedback saved

---

## Definition of Done

### Implementation
- [ ] Hook integration phase added to /create-sprint command workflow (Phase N after Phase 4 result display)
- [ ] `devforgeai check-hooks --operation=sprint-create` command functional (<100ms execution)
- [ ] `devforgeai invoke-hooks --operation=sprint-create` command functional with sprint context
- [ ] Hook configuration read from `.devforgeai/config/hooks.yaml` (enabled/disabled state respected)
- [ ] Sprint context provided in hook (sprint name, selected story IDs, capacity, dates, team)
- [ ] Graceful degradation implemented (hook failures don't break sprint creation, exit code 0)

### Quality
- [ ] All 6 acceptance criteria have passing tests
- [ ] Edge cases covered (hook timeout, hook CLI error, hook script crash, missing config)
- [ ] Data validation enforced (sprint context metadata complete, hook config format valid)
- [ ] NFRs met (hook check <100ms, hook invocation <500ms, graceful failure handling)
- [ ] Code coverage >95% for hook integration logic

### Testing
- [ ] Unit tests for hook configuration reading and enabled/disabled state
- [ ] Unit tests for sprint context metadata assembly (sprint ID, name, story IDs, capacity, dates)
- [ ] Unit tests for graceful degradation (hook failure doesn't crash workflow)
- [ ] Integration test: /create-sprint hook triggers successfully
- [ ] Integration test: /create-sprint with hooks disabled skips hook invocation
- [ ] Integration test: Sprint-specific questions received by user during feedback
- [ ] E2E test: Complete sprint creation workflow with hook triggering and feedback

### Documentation
- [ ] Hook integration documentation added to sprint planning guide
- [ ] Configuration example added to `.devforgeai/config/hooks.yaml.example` for sprint-create
- [ ] Troubleshooting guide: "Hook not triggering after sprint creation" - resolution steps
- [ ] Framework maintainer guide updated with hook lifecycle for sprint creation

---

## Implementation Notes

**This story wires hook integration into /create-sprint command workflow. See Technical Specification for hook architecture details.**

**Hook Integration Point:**
- Hook integration phase (Phase N) added to /create-sprint command
- Placement: After Phase 4 (result display) ensures hooks only run when sprint creation succeeds
- Hooks invoked via `devforgeai invoke-hooks --operation=sprint-create`

**Sprint Context for Hooks:**
- Sprint metadata passed: name, ID, selected story IDs, capacity, dates, team
- Sprint-specific questions focus on goal clarity, story selection, capacity appropriateness
- Graceful degradation: Failures logged/warned but exit 0

**Configuration:**
- Enabled/disabled state controlled via `.devforgeai/config/hooks.yaml`
- Hook check executes in <100ms
- Hook invocation non-blocking

**Related Stories:**
- STORY-021: devforgeai check-hooks implementation
- STORY-022: devforgeai invoke-hooks implementation
- STORY-027: Hook integration for /create-story command

## Workflow Status

- [ ] Architecture phase complete
- [ ] Development phase complete
- [ ] QA phase complete
- [ ] Released

## Notes

**Design Decisions:**
- Phase N placement: After Phase 4 (result display) ensures hooks only run after successful sprint creation
- Graceful degradation: Hook failures are non-fatal to prevent blocking sprint planning workflow
- Shell escaping: All parameters double-quoted to prevent command injection
- Timeout: 5-second timeout prevents hanging if feedback system unresponsive

**Open Questions:**
- None

**Related ADRs:**
- ADR-018: Event-Driven Hook System Design
- ADR-019: Feedback CLI Architecture

**Related Stories:**
- STORY-021: Implement devforgeai check-hooks CLI command (prerequisite)
- STORY-022: Implement devforgeai invoke-hooks CLI command (prerequisite)
- STORY-023: Wire hooks into /dev command (pilot - similar pattern)
- STORY-030 through STORY-033: Remaining command integration stories

**References:**
- Epic: `.ai_docs/Epics/EPIC-006-feedback-integration-completion.epic.md`
- Feature 6.2: Command Integration Rollout (11 stories total)
- Hook Configuration: `.devforgeai/config/hooks.yaml`
- Feedback Logs: `.devforgeai/feedback/logs/`

---

**Story Template Version:** 1.0
**Last Updated:** 2025-11-12

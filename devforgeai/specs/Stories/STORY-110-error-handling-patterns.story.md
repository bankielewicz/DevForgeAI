---
id: STORY-110
title: Error Handling Patterns for Parallel Orchestration
epic: EPIC-017
sprint: Backlog
status: Backlog
points: 5
depends_on: ["STORY-108"]
priority: Medium
assigned_to: TBD
created: 2025-12-18
format_version: "2.2"
---

# Story: Error Handling Patterns for Parallel Orchestration

## Description

**As a** DevForgeAI Opus orchestrator,
**I want** partial failure recovery, timeout handling, and retry logic patterns for parallel tasks,
**so that** 1 failed subagent doesn't block 5 successful ones and hung tasks are gracefully terminated.

This story implements EPIC-017 Feature 3: Implement partial failure recovery, timeout handling, and retry logic patterns for parallel orchestration.

## Acceptance Criteria

### AC#1: Partial Failure Recovery

**Given** 6 parallel subagents are invoked,
**When** 1 subagent fails and 5 succeed,
**Then** the orchestrator continues with the 5 successful results and logs the failure.

---

### AC#2: Timeout Handling

**Given** a subagent is running,
**When** it exceeds the configured timeout_ms from parallel-orchestration.yaml,
**Then** the task is terminated via KillShell and error is logged with task ID.

---

### AC#3: Retry Logic

**Given** a transient failure occurs (network timeout, rate limit),
**When** retry is enabled in config,
**Then** the task is retried up to max_attempts with exponential backoff.

---

### AC#4: Fallback to Sequential

**Given** parallel execution fails completely (all tasks fail),
**When** fallback_to_sequential is enabled in config,
**Then** tasks are re-executed sequentially with detailed logging.

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Service"
      name: "ParallelErrorHandler"
      file_path: "src/skills/orchestration/parallel-error-handler.py"
      interface: "IParallelErrorHandler"
      lifecycle: "Scoped"
      dependencies:
        - "ParallelConfigLoader"
        - "logging"
      requirements:
        - id: "SVC-001"
          description: "Collect results from parallel tasks, separating successes from failures"
          testable: true
          test_requirement: "Test: 3 success + 2 failure returns PartialResult with both lists"
          priority: "Critical"
        - id: "SVC-002"
          description: "Log failures with task ID, error type, and stack trace"
          testable: true
          test_requirement: "Test: Failed task produces structured log entry"
          priority: "High"
        - id: "SVC-003"
          description: "Determine if partial success is acceptable based on config"
          testable: true
          test_requirement: "Test: min_success_rate=0.5 accepts 3/5 but rejects 2/5"
          priority: "High"

    - type: "Service"
      name: "TimeoutManager"
      file_path: "src/skills/orchestration/timeout-manager.py"
      interface: "ITimeoutManager"
      lifecycle: "Singleton"
      dependencies:
        - "ParallelConfigLoader"
        - "KillShell tool"
      requirements:
        - id: "SVC-004"
          description: "Monitor running task durations against configured timeout"
          testable: true
          test_requirement: "Test: Task running 10s with 5s timeout triggers termination"
          priority: "Critical"
        - id: "SVC-005"
          description: "Invoke KillShell for timed-out background tasks"
          testable: true
          test_requirement: "Test: Timeout triggers KillShell with correct shell_id"
          priority: "Critical"
        - id: "SVC-006"
          description: "Log timeout events with task context"
          testable: true
          test_requirement: "Test: Timeout produces log with task_id, duration, timeout_ms"
          priority: "High"

    - type: "Service"
      name: "RetryHandler"
      file_path: "src/skills/orchestration/retry-handler.py"
      interface: "IRetryHandler"
      lifecycle: "Scoped"
      dependencies:
        - "ParallelConfigLoader"
      requirements:
        - id: "SVC-007"
          description: "Implement exponential backoff between retry attempts"
          testable: true
          test_requirement: "Test: 3 retries with 1000ms base = delays of 1s, 2s, 4s"
          priority: "High"
        - id: "SVC-008"
          description: "Classify errors as transient vs permanent"
          testable: true
          test_requirement: "Test: Rate limit = transient, ValidationError = permanent"
          priority: "High"
        - id: "SVC-009"
          description: "Respect max_attempts from config"
          testable: true
          test_requirement: "Test: max_attempts=3 stops after 3rd failure"
          priority: "Critical"

    - type: "DataModel"
      name: "PartialResult"
      table: "N/A (in-memory)"
      purpose: "Represents outcome of parallel execution with mixed success/failure"
      fields:
        - name: "successes"
          type: "List[TaskResult]"
          constraints: "Required"
          description: "Successfully completed task results"
          test_requirement: "Test: Verify successes list populated"
        - name: "failures"
          type: "List[TaskFailure]"
          constraints: "Required"
          description: "Failed task details with error info"
          test_requirement: "Test: Verify failures list populated"
        - name: "total_tasks"
          type: "Int"
          constraints: "Required, >= 0"
          description: "Total number of tasks attempted"
          test_requirement: "Test: total_tasks = len(successes) + len(failures)"
        - name: "success_rate"
          type: "Float"
          constraints: "Required, 0.0-1.0"
          description: "Percentage of tasks that succeeded"
          test_requirement: "Test: 3/5 success = 0.6 success_rate"

    - type: "DataModel"
      name: "TaskFailure"
      table: "N/A (in-memory)"
      purpose: "Represents a single task failure with diagnostic info"
      fields:
        - name: "task_id"
          type: "String"
          constraints: "Required"
          description: "Unique identifier for the failed task"
          test_requirement: "Test: task_id matches original Task invocation"
        - name: "error_type"
          type: "Enum(Timeout, TransientError, PermanentError, Unknown)"
          constraints: "Required"
          description: "Classification of failure type"
          test_requirement: "Test: error_type correctly classified"
        - name: "error_message"
          type: "String"
          constraints: "Required"
          description: "Human-readable error description"
          test_requirement: "Test: error_message non-empty"
        - name: "retry_count"
          type: "Int"
          constraints: "Required, >= 0"
          description: "Number of retry attempts made"
          test_requirement: "Test: retry_count incremented on each retry"
        - name: "is_retryable"
          type: "Boolean"
          constraints: "Required"
          description: "Whether error type allows retry"
          test_requirement: "Test: Timeout=true, ValidationError=false"

  business_rules:
    - id: "BR-001"
      rule: "Partial success continues workflow if success_rate >= min_success_rate"
      trigger: "After parallel task completion"
      validation: "Compare success_rate against config threshold"
      error_handling: "If below threshold, aggregate failures and raise PartialFailureError"
      test_requirement: "Test: 60% success with 50% threshold continues; 40% fails"
      priority: "Critical"
    - id: "BR-002"
      rule: "Transient errors are retried; permanent errors are not"
      trigger: "On task failure"
      validation: "Error classification lookup"
      error_handling: "Permanent errors added to failures immediately"
      test_requirement: "Test: Rate limit retried, syntax error not retried"
      priority: "High"
    - id: "BR-003"
      rule: "Exponential backoff doubles delay on each retry"
      trigger: "Retry attempt"
      validation: "delay = base_delay_ms * (2 ^ attempt_number)"
      error_handling: "Cap at max_backoff_ms (10 seconds default)"
      test_requirement: "Test: Delays follow exponential pattern with cap"
      priority: "Medium"
    - id: "BR-004"
      rule: "Fallback to sequential only when ALL parallel tasks fail"
      trigger: "success_rate = 0"
      validation: "All tasks in failures list, none in successes"
      error_handling: "Re-queue tasks for sequential execution"
      test_requirement: "Test: 0/5 success triggers sequential fallback"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Reliability"
      requirement: "Error handling must not lose successful results"
      metric: "0% data loss for completed tasks"
      test_requirement: "Test: Verify successes preserved when failures occur"
      priority: "Critical"
    - id: "NFR-002"
      category: "Performance"
      requirement: "Timeout detection latency < 1 second"
      metric: "Task killed within 1s of timeout expiry"
      test_requirement: "Test: Measure time between timeout and KillShell"
      priority: "High"
    - id: "NFR-003"
      category: "Observability"
      requirement: "All failures logged with correlation ID"
      metric: "100% of failures have traceable logs"
      test_requirement: "Test: Each failure produces searchable log entry"
      priority: "High"
```

---

## Non-Functional Requirements (NFRs)

### Reliability

**Error Handling:**
- Successful results never lost due to sibling failures
- All failures logged with full context

**Retry Logic:**
- Transient errors: Retry with exponential backoff
- Permanent errors: Fail immediately

---

### Observability

**Logging:**
- Each failure produces structured log with: task_id, error_type, message, retry_count
- Correlation ID links related parallel tasks

---

## Dependencies

### Prerequisite Stories

- [ ] **STORY-108:** Parallel Configuration Infrastructure
  - **Why:** Provides config for timeout_ms, retry settings, fallback options
  - **Status:** Not Started

### Technology Dependencies

- [ ] **KillShell tool** (Claude Code built-in)
  - **Purpose:** Terminate hung background tasks
  - **Approved:** Yes (built-in)

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for error handling logic

**Test Scenarios:**
1. **Happy Path:** All tasks succeed, empty failures list
2. **Partial Failure:** 3/5 succeed, 2/5 fail with correct classification
3. **Complete Failure:** 0/5 succeed, fallback triggered
4. **Timeout:** Task killed after timeout_ms
5. **Retry Success:** Transient error succeeded on 2nd attempt
6. **Retry Exhaustion:** Max attempts reached, added to failures

---

## Acceptance Criteria Verification Checklist

### AC#1: Partial Failure Recovery

- [ ] Successes collected from parallel results - **Phase:** 3 - **Evidence:** TBD
- [ ] Failures collected separately - **Phase:** 3 - **Evidence:** TBD
- [ ] Workflow continues with successful results - **Phase:** 3 - **Evidence:** TBD
- [ ] Failures logged with context - **Phase:** 3 - **Evidence:** TBD

### AC#2: Timeout Handling

- [ ] Timeout monitoring implemented - **Phase:** 3 - **Evidence:** TBD
- [ ] KillShell invoked on timeout - **Phase:** 3 - **Evidence:** TBD
- [ ] Timeout logged with task_id - **Phase:** 3 - **Evidence:** TBD

### AC#3: Retry Logic

- [ ] Exponential backoff implemented - **Phase:** 3 - **Evidence:** TBD
- [ ] Error classification (transient vs permanent) - **Phase:** 3 - **Evidence:** TBD
- [ ] max_attempts respected - **Phase:** 3 - **Evidence:** TBD

### AC#4: Fallback to Sequential

- [ ] Complete failure detection - **Phase:** 3 - **Evidence:** TBD
- [ ] Sequential re-execution triggered - **Phase:** 3 - **Evidence:** TBD
- [ ] Detailed logging during fallback - **Phase:** 3 - **Evidence:** TBD

---

**Checklist Progress:** 0/14 items complete (0%)

---

## Definition of Done

### Implementation
- [ ] ParallelErrorHandler service implemented
- [ ] TimeoutManager service implemented
- [ ] RetryHandler service implemented
- [ ] PartialResult and TaskFailure data models created

### Quality
- [ ] All 4 acceptance criteria have passing tests
- [ ] Edge cases covered (all fail, all succeed, mixed, timeout)
- [ ] Successful results never lost
- [ ] Code coverage >95% for error handling

### Testing
- [ ] Unit tests for partial failure recovery
- [ ] Unit tests for timeout handling
- [ ] Unit tests for retry logic
- [ ] Integration test for fallback to sequential

### Documentation
- [ ] Error handling patterns documented
- [ ] Retry configuration guide
- [ ] Troubleshooting guide for common failures

---

## Workflow Status

- [ ] Architecture phase complete
- [ ] Development phase complete
- [ ] QA phase complete
- [ ] Released

## Notes

**Design Decisions:**
- Partial failure continues workflow to maximize value from successful tasks
- Exponential backoff prevents thundering herd on transient failures
- Fallback to sequential is last resort when parallel completely fails

**References:**
- EPIC-017: Parallel Task Orchestration for DevForgeAI
- Research: `docs/enhancements/2025-12-04/research/parallel-orchestration-research.md`

---

**Story Template Version:** 2.2
**Last Updated:** 2025-12-18

---
id: STORY-110
title: Error Handling Patterns for Parallel Orchestration
epic: EPIC-017
sprint: Backlog
status: QA Approved ✅
points: 5
depends_on: ["STORY-108"]
priority: Medium
assigned_to: Claude
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
    - type: "Configuration"
      name: "Error Handling Patterns Documentation"
      file_path: ".claude/skills/devforgeai-orchestration/references/error-handling-patterns.md"
      purpose: "Documents error handling patterns for parallel task orchestration"
      required_sections:
        - section: "Partial Failure Recovery Pattern"
          description: "How skills collect results from parallel tasks, separating successes from failures"
          test_requirement: "Test: 3 success + 2 failure scenario handled correctly"
        - section: "Result Aggregation Pattern"
          description: "How to merge successful results while tracking failures"
          test_requirement: "Test: Aggregated result contains both success and failure lists"
        - section: "Failure Logging Pattern"
          description: "Structured logging format for parallel task failures"
          test_requirement: "Test: Failure log contains task_id, error_type, message"

    - type: "Configuration"
      name: "Timeout Handling Documentation"
      file_path: ".claude/skills/devforgeai-orchestration/references/timeout-handling.md"
      purpose: "Documents timeout monitoring and task termination patterns"
      required_sections:
        - section: "Timeout Monitoring Pattern"
          description: "How to track task duration against configured timeout_ms"
          test_requirement: "Test: Task exceeding timeout triggers termination"
        - section: "KillShell Integration"
          description: "How to invoke KillShell tool for timed-out background tasks"
          test_requirement: "Test: KillShell called with correct shell_id"
        - section: "Timeout Logging Pattern"
          description: "Log format for timeout events with task context"
          test_requirement: "Test: Timeout log includes task_id, duration, timeout_ms"

    - type: "Configuration"
      name: "Retry Patterns Documentation"
      file_path: ".claude/skills/devforgeai-orchestration/references/retry-patterns.md"
      purpose: "Documents retry logic patterns for transient failures"
      required_sections:
        - section: "Exponential Backoff Pattern"
          description: "delay = base_delay_ms * (2 ^ attempt_number)"
          test_requirement: "Test: Delays follow exponential pattern"
        - section: "Error Classification"
          description: "How to classify errors as transient vs permanent"
          test_requirement: "Test: Rate limit = transient, ValidationError = permanent"
        - section: "Max Attempts Pattern"
          description: "How to respect max_attempts from config"
          test_requirement: "Test: Retry stops after max_attempts reached"

    - type: "Configuration"
      name: "Sequential Fallback Documentation"
      file_path: ".claude/skills/devforgeai-orchestration/references/sequential-fallback.md"
      purpose: "Documents fallback to sequential execution pattern"
      required_sections:
        - section: "Complete Failure Detection"
          description: "How to detect when all parallel tasks have failed"
          test_requirement: "Test: 0/5 success triggers fallback"
        - section: "Sequential Re-execution Pattern"
          description: "How to re-queue tasks for sequential execution"
          test_requirement: "Test: Tasks execute one-by-one after fallback"
        - section: "Fallback Logging Pattern"
          description: "Detailed logging during sequential fallback"
          test_requirement: "Test: Logs indicate fallback mode activated"

    - type: "DataModel"
      name: "PartialResult"
      table: "N/A (documented pattern, in-memory during execution)"
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
      table: "N/A (documented pattern, in-memory during execution)"
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
      error_handling: "If below threshold, aggregate failures and HALT with error"
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

- [ ] **TaskOutput tool** (Claude Code built-in)
  - **Purpose:** Check background task status
  - **Approved:** Yes (built-in)

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for error handling patterns

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

- [x] Successes collected from parallel results - **Phase:** 3 - **Evidence:** error-handling-patterns.md#Result Aggregation Pattern
- [x] Failures collected separately - **Phase:** 3 - **Evidence:** error-handling-patterns.md#TaskFailure Data Model
- [x] Workflow continues with successful results - **Phase:** 3 - **Evidence:** error-handling-patterns.md#Partial Failure Recovery Pattern (BR-001)
- [x] Failures logged with context - **Phase:** 3 - **Evidence:** error-handling-patterns.md#Failure Logging Pattern

### AC#2: Timeout Handling

- [x] Timeout monitoring pattern documented - **Phase:** 3 - **Evidence:** timeout-handling.md#Timeout Monitoring Pattern
- [x] KillShell integration documented - **Phase:** 3 - **Evidence:** timeout-handling.md#KillShell Integration
- [x] Timeout logged with task_id - **Phase:** 3 - **Evidence:** timeout-handling.md#Timeout Logging Pattern

### AC#3: Retry Logic

- [x] Exponential backoff pattern documented - **Phase:** 3 - **Evidence:** retry-patterns.md#Exponential Backoff Pattern
- [x] Error classification (transient vs permanent) documented - **Phase:** 3 - **Evidence:** retry-patterns.md#Error Classification
- [x] max_attempts pattern documented - **Phase:** 3 - **Evidence:** retry-patterns.md#Max Attempts Pattern

### AC#4: Fallback to Sequential

- [x] Complete failure detection pattern documented - **Phase:** 3 - **Evidence:** sequential-fallback.md#Complete Failure Detection
- [x] Sequential re-execution pattern documented - **Phase:** 3 - **Evidence:** sequential-fallback.md#Sequential Re-execution Pattern
- [x] Detailed logging during fallback documented - **Phase:** 3 - **Evidence:** sequential-fallback.md#Fallback Logging Pattern

---

**Checklist Progress:** 14/14 items complete (100%)

---

## Definition of Done

### Implementation
- [x] `references/error-handling-patterns.md` created
- [x] `references/timeout-handling.md` created
- [x] `references/retry-patterns.md` created
- [x] `references/sequential-fallback.md` created
- [x] PartialResult and TaskFailure data models documented

### Quality
- [x] All 4 acceptance criteria documented with examples
- [x] Edge cases covered (all fail, all succeed, mixed, timeout)
- [x] Successful results never lost
- [x] Test scenarios defined for each pattern

### Testing
- [x] Test scenarios for partial failure recovery
- [x] Test scenarios for timeout handling
- [x] Test scenarios for retry logic
- [x] Test scenarios for fallback to sequential

### Documentation
- [x] Error handling patterns fully documented
- [x] Retry configuration guide
- [x] Troubleshooting guide for common failures

---

## Workflow Status

- [x] Architecture phase complete
- [x] Development phase complete
- [x] QA phase complete
- [ ] Released

## Notes

**Design Decisions:**
- **Framework-compliant:** Documentation patterns in references/, no Python services
- Partial failure continues workflow to maximize value from successful tasks
- Exponential backoff prevents thundering herd on transient failures
- Fallback to sequential is last resort when parallel completely fails
- Per anti-patterns.md: "Framework must be language-agnostic"

**Pattern Example (Partial Failure Recovery):**
```markdown
## Partial Failure Recovery Pattern

When parallel Task() calls complete:

1. Collect all results from TaskOutput
2. Separate into successes[] and failures[]
3. Calculate success_rate = len(successes) / total_tasks
4. If success_rate >= min_success_rate:
   - Continue with successes
   - Log failures with Display
5. Else:
   - HALT with aggregated failure message
```

**References:**
- EPIC-017: Parallel Task Orchestration for DevForgeAI
- Research: `docs/enhancements/2025-12-04/research/parallel-orchestration-research.md`

---

**Story Template Version:** 2.2
**Last Updated:** 2025-12-18
**Context Compliance:** Verified against tech-stack.md, dependencies.md, anti-patterns.md

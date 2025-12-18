---
id: STORY-112
title: Development Skill Refactor for Background Execution
epic: EPIC-017
sprint: Backlog
status: Backlog
points: 8
depends_on: ["STORY-108", "STORY-110"]
priority: Medium
assigned_to: TBD
created: 2025-12-18
format_version: "2.2"
---

# Story: Development Skill Refactor for Background Execution

## Description

**As a** DevForgeAI developer,
**I want** the devforgeai-development skill to run tests in background while implementing code,
**so that** long test runs don't block implementation and TDD cycle time is reduced by 50-80%.

This story implements EPIC-017 Feature 5: Refactor devforgeai-development skill to use background task execution for tests/builds and parallel Phase 0 loading.

## Acceptance Criteria

### AC#1: Background Test Execution

**Given** tests need to run during TDD cycle,
**When** the development skill invokes pytest/npm test,
**Then** tests run in background via `run_in_background=true` while code implementation continues.

---

### AC#2: Parallel Phase 0 Context Loading

**Given** the development skill starts Phase 0,
**When** it needs to load 6 context files,
**Then** all 6 files are read in parallel using a single message with 6 Read tool calls.

---

### AC#3: Background Task Result Retrieval

**Given** tests are running in background,
**When** implementation code is ready,
**Then** the skill retrieves test results via TaskOutput before proceeding to next phase.

---

### AC#4: Long Operation Handling

**Given** a build or test run exceeds 2 minutes,
**When** the operation is background-eligible,
**Then** it runs with `run_in_background=true` and timeout from config.

---

### AC#5: Time Reduction Validation

**Given** a baseline measurement of sequential development,
**When** background execution completes,
**Then** long operations (builds/tests) show 50-80% wall-clock reduction.

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Service"
      name: "BackgroundTaskExecutor"
      file_path: ".claude/skills/devforgeai-development/SKILL.md"
      interface: "Skill Definition"
      lifecycle: "On-demand"
      dependencies:
        - "ParallelConfigLoader"
        - "ParallelErrorHandler"
        - "Bash tool"
        - "TaskOutput tool"
      requirements:
        - id: "SVC-001"
          description: "Execute tests with run_in_background=true"
          testable: true
          test_requirement: "Test: pytest command uses run_in_background parameter"
          priority: "Critical"
        - id: "SVC-002"
          description: "Continue implementation while tests run"
          testable: true
          test_requirement: "Test: Code written after test launch, before test completion"
          priority: "Critical"
        - id: "SVC-003"
          description: "Retrieve background results via TaskOutput"
          testable: true
          test_requirement: "Test: TaskOutput called with correct task_id"
          priority: "Critical"
        - id: "SVC-004"
          description: "Respect timeout_ms from parallel config"
          testable: true
          test_requirement: "Test: Background task uses timeout from config"
          priority: "High"

    - type: "Service"
      name: "ParallelContextLoader"
      file_path: ".claude/skills/devforgeai-development/references/parallel-context.md"
      interface: "Reference Document"
      lifecycle: "N/A"
      dependencies:
        - "Read tool"
      requirements:
        - id: "SVC-005"
          description: "Load 6 context files in single message with parallel Read calls"
          testable: true
          test_requirement: "Test: Phase 0 produces single message with 6 Read tool uses"
          priority: "High"

    - type: "Service"
      name: "BuildOrchestrator"
      file_path: ".claude/skills/devforgeai-development/references/build-orchestrator.md"
      interface: "Reference Document"
      lifecycle: "N/A"
      dependencies:
        - "Bash tool"
      requirements:
        - id: "SVC-006"
          description: "Run builds in background for operations > 2 minutes estimated"
          testable: true
          test_requirement: "Test: dotnet build uses background for large projects"
          priority: "High"
        - id: "SVC-007"
          description: "Keep short operations foreground for simplicity"
          testable: true
          test_requirement: "Test: Quick lint checks run in foreground"
          priority: "Medium"

  business_rules:
    - id: "BR-001"
      rule: "Tests always run in background during TDD Green phase"
      trigger: "TDD Green phase start"
      validation: "Bash tool call includes run_in_background=true"
      error_handling: "If background unavailable, fall back to foreground with warning"
      test_requirement: "Test: Green phase test invocation uses background"
      priority: "Critical"
    - id: "BR-002"
      rule: "Implementation continues while background tests run"
      trigger: "After background test launch"
      validation: "Write/Edit tool calls occur before TaskOutput"
      error_handling: "N/A (normal flow)"
      test_requirement: "Test: Code written between test launch and result retrieval"
      priority: "Critical"
    - id: "BR-003"
      rule: "TaskOutput must block before phase transition"
      trigger: "Before moving to next TDD phase"
      validation: "TaskOutput with block=true called"
      error_handling: "If timeout, use TimeoutManager from STORY-110"
      test_requirement: "Test: Phase transition waits for background completion"
      priority: "Critical"
    - id: "BR-004"
      rule: "Operations < 30 seconds run in foreground"
      trigger: "Command execution"
      validation: "Estimated duration check"
      error_handling: "N/A (foreground is simpler)"
      test_requirement: "Test: Quick commands don't use background"
      priority: "Medium"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "50-80% reduction in perceived test wait time"
      metric: "Work done during test run / total test duration"
      test_requirement: "Test: Measure useful work during background tests"
      priority: "Critical"
    - id: "NFR-002"
      category: "Performance"
      requirement: "Phase 0 loads context in parallel (same as STORY-111)"
      metric: "35-40% reduction from sequential baseline"
      test_requirement: "Test: Time Phase 0 with 6 files"
      priority: "High"
    - id: "NFR-003"
      category: "Reliability"
      requirement: "Background failures detected and handled"
      metric: "0% silent failures"
      test_requirement: "Test: Failed background test triggers error handling"
      priority: "Critical"
    - id: "NFR-004"
      category: "Cost"
      requirement: "Zero additional token consumption"
      metric: "Token count equal to sequential"
      test_requirement: "Test: Compare token usage background vs foreground"
      priority: "High"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Wait Time Reduction:**
- 50-80% reduction in perceived wait time during test runs
- Useful implementation work done while tests execute

**Phase 0:**
- Same 35-40% improvement as STORY-111

### Reliability

**Background Task Handling:**
- All background failures detected
- No silent failures (0% loss rate)

---

## Dependencies

### Prerequisite Stories

- [ ] **STORY-108:** Parallel Configuration Infrastructure
  - **Why:** Provides timeout settings for background tasks
  - **Status:** Not Started

- [ ] **STORY-110:** Error Handling Patterns
  - **Why:** Provides timeout handling and failure recovery
  - **Status:** Not Started

### Technology Dependencies

- [ ] **Bash tool with run_in_background** (Claude Code built-in)
  - **Purpose:** Background command execution
  - **Approved:** Yes (built-in)

- [ ] **TaskOutput tool** (Claude Code built-in)
  - **Purpose:** Retrieve background task results
  - **Approved:** Yes (built-in)

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for background execution logic

**Test Scenarios:**
1. **Happy Path:** Test runs in background, implementation continues, results retrieved
2. **Background Failure:** Test fails, error captured via TaskOutput
3. **Timeout:** Long test killed after timeout_ms
4. **Foreground Fallback:** Short operation runs foreground

### Performance Tests

1. **Baseline Measurement:** Sequential TDD cycle timing
2. **Background Measurement:** Background TDD cycle timing
3. **Work Measurement:** Useful work done during background tests

---

## Acceptance Criteria Verification Checklist

### AC#1: Background Test Execution

- [ ] Bash tool uses run_in_background=true - **Phase:** 3 - **Evidence:** TBD
- [ ] Test starts without blocking - **Phase:** 3 - **Evidence:** TBD
- [ ] Task ID captured for later retrieval - **Phase:** 3 - **Evidence:** TBD

### AC#2: Parallel Phase 0 Context Loading

- [ ] Single message with 6 Read calls - **Phase:** 3 - **Evidence:** TBD
- [ ] All 6 context files loaded - **Phase:** 3 - **Evidence:** TBD

### AC#3: Background Task Result Retrieval

- [ ] TaskOutput called with task_id - **Phase:** 3 - **Evidence:** TBD
- [ ] block=true used for phase transition - **Phase:** 3 - **Evidence:** TBD
- [ ] Results parsed correctly - **Phase:** 3 - **Evidence:** TBD

### AC#4: Long Operation Handling

- [ ] Duration estimation implemented - **Phase:** 3 - **Evidence:** TBD
- [ ] Operations > 2min use background - **Phase:** 3 - **Evidence:** TBD
- [ ] Timeout from config applied - **Phase:** 3 - **Evidence:** TBD

### AC#5: Time Reduction Validation

- [ ] Baseline timing captured - **Phase:** 5 - **Evidence:** TBD
- [ ] Background timing captured - **Phase:** 5 - **Evidence:** TBD
- [ ] 50-80% improvement verified - **Phase:** 5 - **Evidence:** TBD

---

**Checklist Progress:** 0/15 items complete (0%)

---

## Definition of Done

### Implementation
- [ ] Development skill SKILL.md updated with background patterns
- [ ] Background test execution in TDD Green phase
- [ ] Phase 0 uses parallel Read calls
- [ ] TaskOutput integration for result retrieval

### Quality
- [ ] All 5 acceptance criteria have passing tests
- [ ] Edge cases covered (timeout, failure, foreground fallback)
- [ ] NFRs met (50-80% wait reduction, zero extra tokens)
- [ ] Code coverage >95% for background execution

### Testing
- [ ] Unit tests for background test execution
- [ ] Unit tests for TaskOutput integration
- [ ] Unit tests for duration estimation
- [ ] Performance tests with timing validation

### Documentation
- [ ] Background execution patterns documented
- [ ] TaskOutput usage guide
- [ ] Troubleshooting guide for background failures

---

## Workflow Status

- [ ] Architecture phase complete
- [ ] Development phase complete
- [ ] QA phase complete
- [ ] Released

## Notes

**Design Decisions:**
- Background for tests enables productive use of wait time
- Foreground for short ops keeps workflow simple
- TaskOutput blocking ensures phase transitions wait for results

**References:**
- EPIC-017: Parallel Task Orchestration for DevForgeAI
- Research: `docs/enhancements/2025-12-04/research/parallel-orchestration-research.md`
- Claude Code Terminal: Background task documentation

---

**Story Template Version:** 2.2
**Last Updated:** 2025-12-18

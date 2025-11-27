---
id: STORY-092
title: Story-Scoped Test Isolation
epic: EPIC-010
sprint: SPRINT-5
status: Ready for Dev
points: 5
priority: High
assigned_to: TBD
created: 2025-11-25
format_version: "2.1"
depends_on: ["STORY-091"]
---

# Story: Story-Scoped Test Isolation

## Description

**As a** DevForgeAI developer running /qa on multiple stories concurrently,
**I want** test outputs (results, coverage, logs) isolated per story in dedicated directories,
**so that** concurrent QA validations do not overwrite each other's results and I can review and compare results independently.

**Context:** This is Feature 2 of EPIC-010 (Parallel Story Development). Test isolation ensures that concurrent /dev and /qa executions don't corrupt each other's test artifacts.

## Acceptance Criteria

### AC#1: Story-Scoped Test Results Directory Structure

**Given** a developer runs `/dev STORY-037` or `/qa STORY-037`
**When** the test execution phase completes
**Then** all test results are written to `tests/results/STORY-037/` with structure:
- `tests/results/STORY-037/test-results.xml` (JUnit format)
- `tests/results/STORY-037/test-output.log` (console output)
- `tests/results/STORY-037/timestamp.txt` (ISO 8601 execution time)

---

### AC#2: Story-Scoped Coverage Reports

**Given** a developer runs `/qa STORY-038` concurrently with `/qa STORY-037`
**When** coverage collection completes for both stories
**Then** coverage reports are isolated:
- STORY-037: `tests/coverage/STORY-037/coverage.xml`
- STORY-038: `tests/coverage/STORY-038/coverage.xml`
- Neither story's coverage data overwrites the other

---

### AC#3: QA Report Path References

**Given** a QA report is generated for STORY-037
**When** the report references test output paths
**Then** all paths in `.devforgeai/qa/reports/STORY-037-qa-report.md` reference story-scoped directories:
- Test results: `tests/results/STORY-037/`
- Coverage: `tests/coverage/STORY-037/`
- Logs: `tests/logs/STORY-037/`

---

### AC#4: Multi-Language Test Command Generation

**Given** a project uses one of the supported test frameworks
**When** /dev or /qa generates test execution commands
**Then** commands include story-scoped output paths:
- **pytest:** `pytest --junitxml=tests/results/{story_id}/test-results.xml --cov-report=xml:tests/coverage/{story_id}/coverage.xml`
- **jest:** `npm test -- --outputFile=tests/results/{story_id}/test-results.json --coverageDirectory=tests/coverage/{story_id}/`
- **dotnet test:** `dotnet test --results-directory=tests/results/{story_id}/`
- **go test:** `go test ./... -coverprofile=tests/coverage/{story_id}/coverage.out`

---

### AC#5: Configuration File Support

**Given** a project requires customization of test isolation paths
**When** `.devforgeai/config/test-isolation.yaml` exists
**Then** the framework reads configuration for:
- Base results directory (default: `tests/results/`)
- Base coverage directory (default: `tests/coverage/`)
- Cleanup policy (`retain_days: 7`, `max_stories: 10`)

---

### AC#6: Directory Auto-Creation and Validation

**Given** a test execution is initiated for STORY-039
**When** the story-scoped directories do not exist
**Then** the framework:
- Creates `tests/results/STORY-039/` with 755 permissions
- Creates `tests/coverage/STORY-039/` with 755 permissions
- Validates write permissions before test execution
- Halts with error if directory creation fails

---

### AC#7: Concurrent Execution Verification

**Given** two concurrent QA validations are running
**When** both complete within overlapping time windows
**Then**:
- File locking prevents partial writes
- Each story's results are complete and valid
- Coverage files pass schema validation

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "test-isolation.yaml"
      file_path: "src/devforgeai/config/test-isolation.yaml.example"
      purpose: "Configuration for test isolation paths and cleanup"
      required_keys:
        - key: "results_base"
          type: "string"
          default: "tests/results"
          test_requirement: "Test: Config uses tests/results as default"
        - key: "coverage_base"
          type: "string"
          default: "tests/coverage"
          test_requirement: "Test: Config uses tests/coverage as default"
        - key: "cleanup_policy.retain_days"
          type: "integer"
          default: "7"
          test_requirement: "Test: Old results deleted after 7 days"

    - type: "Service"
      name: "TestIsolationService"
      file_path: "src/claude/skills/devforgeai-qa/references/test-isolation-service.md"
      interface: "Service"
      requirements:
        - id: "SVC-001"
          description: "Generate story-scoped paths from story ID"
          testable: true
          test_requirement: "Test: STORY-037 returns tests/results/STORY-037/"
          priority: "Critical"
        - id: "SVC-002"
          description: "Create directories with correct permissions"
          testable: true
          test_requirement: "Test: Directory created with 755 permissions"
          priority: "High"

    - type: "Service"
      name: "TestCommandGenerator"
      file_path: "src/claude/skills/devforgeai-development/references/test-command-generator.md"
      requirements:
        - id: "SVC-003"
          description: "Generate pytest command with story-scoped paths"
          testable: true
          test_requirement: "Test: pytest command includes --junitxml=tests/results/{story_id}/"
          priority: "Critical"
        - id: "SVC-004"
          description: "Generate jest command with story-scoped paths"
          testable: true
          test_requirement: "Test: jest command includes --outputFile=tests/results/{story_id}/"
          priority: "Critical"

  business_rules:
    - id: "BR-001"
      rule: "All test outputs must use story-scoped paths"
      trigger: "Test execution"
      validation: "Check output path contains STORY-NNN"
      test_requirement: "Test: No outputs written to root TestResults/"
      priority: "Critical"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Directory creation time"
      metric: "< 50ms per story including permission validation"
      test_requirement: "Test: Time directory creation"
      priority: "Medium"
```

---

## Non-Functional Requirements

### Performance
- Directory creation: < 50ms per story
- Test command generation: < 10ms overhead
- No measurable impact on test execution time (< 1% overhead)

### Security
- Directory creation uses explicit permissions (no world-writable)
- Path traversal prevention via sanitization
- Configuration file parsing uses safe YAML loader

### Reliability
- Atomic file writes: temp file + rename pattern
- Lock file cleanup: stale locks removed automatically
- Graceful degradation: fall back to default paths with warning

### Scalability
- Support up to 20 concurrent story test executions
- Directory structure scales to 1000+ stories
- Cleanup automation prevents unbounded growth

---

## Edge Cases

1. **Story ID with special characters:** Sanitize invalid directory characters
2. **Disk space exhaustion:** Halt gracefully with error message
3. **Pre-existing results:** Archive previous results before new run
4. **Concurrent writes to same directory:** Use file locking
5. **Missing test framework:** Fail fast with actionable error

---

## Dependencies

### Prerequisite Stories
- [ ] **STORY-091:** Git Worktree Auto-Management (worktrees provide file system isolation)

### Technology Dependencies
- pytest 6.0+, jest 27.0+, dotnet test 6.0+, go test 1.18+

---

## Definition of Done

### Implementation
- [ ] test-isolation.yaml.example config template created
- [ ] TestIsolationService generates story-scoped paths
- [ ] TestCommandGenerator creates correct commands for all frameworks
- [ ] Directory auto-creation with validation
- [ ] QA report references updated paths

### Quality
- [ ] All 7 acceptance criteria have passing tests
- [ ] Edge cases covered
- [ ] NFRs met (< 50ms creation, atomic writes)
- [ ] Code coverage >95%

### Testing
- [ ] Unit tests for path generation
- [ ] Unit tests for each test framework
- [ ] Integration tests for concurrent execution

### Documentation
- [ ] test-isolation-service.md reference created
- [ ] test-isolation.yaml.example documented

---

## Workflow Status

- [ ] Architecture phase complete
- [ ] Development phase complete
- [ ] QA phase complete
- [ ] Released

## Workflow History

### 2025-11-27 14:30:00 - Status: Ready for Dev
- Added to SPRINT-5: Parallel Story Development Foundation
- Transitioned from Backlog to Ready for Dev
- Sprint capacity: 45 points
- Priority in sprint: 3 of 7 (High - depends on STORY-091)

---

**Story Template Version:** 2.1
**Created:** 2025-11-25

## Implementation Notes

No implementation yet - story in planning/backlog phase.

---
id: STORY-093
title: Dependency Graph Enforcement with Transitive Resolution
epic: EPIC-010
sprint: SPRINT-5
status: QA Approved ✅
points: 13
priority: High
assigned_to: TBD
created: 2025-11-25
format_version: "2.1"
depends_on: ["STORY-090"]
---

# Story: Dependency Graph Enforcement with Transitive Resolution

## Description

**As a** DevForgeAI framework user defining story dependencies,
**I want** the framework to enforce dependency order with transitive resolution and block dependent stories when dependencies fail,
**so that** I never develop STORY-038 (Product) before STORY-037 (User) completes and quality is maintained across the dependency chain.

**Context:** This is Feature 3 of EPIC-010 (Parallel Story Development). Dependency enforcement ensures stories execute in correct order and cascade failures prevent invalid builds.

## Acceptance Criteria

### AC#1: Story YAML depends_on Field Support

**Given** a story file with `depends_on: ["STORY-037", "STORY-039"]`
**When** the dependency-graph-analyzer subagent parses the story
**Then** it extracts all dependency IDs into a validated array
**And** each ID matches the pattern `^STORY-\d{3,4}$`
**And** invalid IDs are rejected with error message

---

### AC#2: Dependency Status Validation on /dev Invocation

**Given** STORY-038 has `depends_on: ["STORY-037"]`
**And** STORY-037 status is "In Development"
**When** the user runs `/dev STORY-038`
**Then** /dev blocks execution at Phase 0
**And** displays: "Dependency STORY-037 status is 'In Development'. Required: 'Dev Complete' or 'QA Approved'."

---

### AC#3: Epic-Level Dependency Inheritance

**Given** EPIC-010 defines Feature 2 depends on Feature 1
**And** STORY-038 belongs to Feature 2
**And** STORY-037 belongs to Feature 1
**When** the dependency graph is built for STORY-038
**Then** STORY-037 is included as inherited dependency
**And** inheritance source is logged

---

### AC#4: Transitive Dependency Resolution

**Given** a chain: STORY-040 → STORY-039 → STORY-037
**When** the user runs `/dev STORY-040`
**Then** the subagent resolves full chain: [STORY-037, STORY-039]
**And** validates STORY-037 first, then STORY-039
**And** blocks if ANY dependency fails
**And** displays chain visualization

---

### AC#5: Circular Dependency Detection

**Given** a circular dependency: STORY-037 → STORY-038 → STORY-037
**When** the dependency graph is built
**Then** the cycle is detected using DFS
**And** error shows: "Circular dependency: STORY-037 → STORY-038 → STORY-037"
**And** /dev is blocked for all stories in cycle

---

### AC#6: Force Flag Bypass with Warning

**Given** STORY-038 has unmet dependencies
**When** user runs `/dev STORY-038 --force`
**Then** dependency check is bypassed
**And** warning is logged to `devforgeai/logs/dependency-bypass-{timestamp}.log`
**And** story proceeds to Phase 1

---

### AC#7: Failed Dependency Cascade Blocking

**Given** STORY-038 depends on STORY-037
**And** STORY-037 status is "QA Failed"
**When** user runs `/dev STORY-038`
**Then** execution blocks with: "Dependency STORY-037 has failed QA."
**And** suggests: "Run '/qa STORY-037 deep' to view failures."

---

### AC#8: Multiple Dependency Validation

**Given** STORY-040 depends on STORY-037, STORY-038, STORY-039
**And** statuses vary (approved, in-dev, failed)
**When** user runs `/dev STORY-040`
**Then** all three are checked
**And** all failures reported in single message

---

### AC#9: Dependency Graph Visualization

**Given** complex dependency graph with 5+ stories
**When** visualization is requested
**Then** ASCII tree is generated showing chains and blocked dependencies

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Service"
      name: "dependency-graph-analyzer"
      file_path: "src/claude/agents/dependency-graph-analyzer.md"
      interface: "Subagent"
      dependencies:
        - "Read"
        - "Glob"
        - "Grep"
      requirements:
        - id: "SVC-001"
          description: "Parse depends_on field from story YAML"
          testable: true
          test_requirement: "Test: Extract [STORY-037, STORY-039] from frontmatter"
          priority: "Critical"
        - id: "SVC-002"
          description: "Build directed acyclic graph from dependencies"
          testable: true
          test_requirement: "Test: 5 stories produce correct adjacency list"
          priority: "Critical"
        - id: "SVC-003"
          description: "Detect circular dependencies using DFS"
          testable: true
          test_requirement: "Test: A→B→C→A returns cycle error"
          priority: "Critical"
        - id: "SVC-004"
          description: "Resolve transitive dependencies to flat list"
          testable: true
          test_requirement: "Test: A→B→C returns [C, B] topologically"
          priority: "Critical"
        - id: "SVC-005"
          description: "Validate dependency statuses"
          testable: true
          test_requirement: "Test: 'Dev Complete' passes, 'In Development' blocks"
          priority: "Critical"
        - id: "SVC-006"
          description: "Handle --force bypass with audit logging"
          testable: true
          test_requirement: "Test: --force logs to devforgeai/logs/"
          priority: "High"

  business_rules:
    - id: "BR-001"
      rule: "Dependencies must complete before dependent story can start"
      trigger: "/dev invocation"
      validation: "Check depends_on statuses"
      test_requirement: "Test: Block /dev when dependency incomplete"
      priority: "Critical"
    - id: "BR-002"
      rule: "Circular dependencies are forbidden"
      trigger: "Graph building"
      validation: "DFS cycle detection"
      test_requirement: "Test: Circular chain returns error"
      priority: "Critical"
    - id: "BR-003"
      rule: "QA Failed dependencies block cascade"
      trigger: "Status validation"
      validation: "Reject QA Failed status"
      test_requirement: "Test: Failed dependency blocks all downstream"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Dependency resolution time"
      metric: "< 500ms for 50 stories, 200 edges (p95)"
      test_requirement: "Test: Resolve 50-node graph in <500ms"
      priority: "High"
    - id: "NFR-002"
      category: "Performance"
      requirement: "Single story validation"
      metric: "< 100ms for one story (p99)"
      test_requirement: "Test: Validate single dependency in <100ms"
      priority: "Medium"
```

---

## Non-Functional Requirements

### Performance
- Dependency resolution: < 500ms for 50 stories (p95)
- Single story validation: < 100ms (p99)
- Graph traversal: O(V+E) time complexity
- Memory: < 50MB for 100-story graph

### Security
- Path traversal prevention in story file access
- Input sanitization for STORY-IDs
- Audit logging for --force bypasses

### Reliability
- Error recovery: malformed YAML doesn't crash graph resolution
- Graceful degradation: fall back to story-level dependencies if epic parsing fails
- Timeout: 30 second limit on resolution

---

## Edge Cases

1. **Non-existent dependency reference:** Fail with clear error
2. **Self-dependency:** Treat as circular
3. **Empty depends_on:** Proceed normally
4. **Missing depends_on field:** Treat as empty (v2.1 compatibility)
5. **Deep chain (>10 levels):** Warn but still enforce
6. **Diamond pattern:** Validate shared dependency once
7. **Concurrent /dev on dependent stories:** Block correctly

---

## Dependencies

### Prerequisite Stories
- [ ] **STORY-090:** Story Template v2.2 with depends_on field

### Deliverables
- NEW: dependency-graph-analyzer subagent (~400 lines)

---

## Definition of Done

### Implementation
- [x] dependency-graph-analyzer subagent created
- [x] YAML parsing for depends_on field
- [x] Graph building with adjacency list
- [x] Cycle detection with DFS
- [x] Transitive resolution
- [x] Status validation
- [x] --force bypass with logging
- [x] ASCII visualization

### Quality
- [x] All 9 acceptance criteria have passing tests (67 tests passing)
- [x] Edge cases covered (17 edge case tests + 16 coverage gap remediation tests)
- [x] NFRs met (performance <500ms verified)
- [x] 99% code coverage for analyzer (exceeds 95% threshold)

### Testing
- [x] Unit tests for parsing (8 tests)
- [x] Unit tests for graph algorithms (18 tests)
- [x] Integration tests for /dev blocking (6 tests)

---

## QA Validation History

### 2025-12-16 - Deep QA Validation PASSED ✅

**Validator:** devforgeai-qa (Deep Mode)
**Coverage:** 99% (exceeds 95% threshold)
**Tests:** 67 passed (100% pass rate)
**Violations:** 0 (CRITICAL: 0, HIGH: 0, MEDIUM: 0, LOW: 0)
**Traceability:** 100% (all 9 ACs verified)
**Report:** `devforgeai/qa/reports/STORY-093-qa-report.md`

**Key Metrics:**
- Business Logic Coverage: 99% ✓
- Anti-Pattern Violations: 0 ✓
- Code Quality: Excellent (9 methods, max 36 lines) ✓
- Security: PASS (no vulnerabilities) ✓
- NFRs Met: Performance <500ms verified ✓

---

## Workflow Status

- [x] Architecture phase complete
- [x] Development phase complete
- [x] QA phase complete
- [ ] Released

## Workflow History

### 2025-12-16 - QA Validation Passed (Deep Mode)
- Status: Dev Complete → **QA Approved ✅**
- Coverage: 99% (threshold: 95%) ✓
- Tests: 67/67 passed ✓
- Violations: 0 ✓
- Ready for release (next: `/release STORY-093`)

### 2025-11-27 14:30:00 - Status: Ready for Dev
- Added to SPRINT-5: Parallel Story Development Foundation
- Transitioned from Backlog to Ready for Dev
- Sprint capacity: 45 points
- Priority in sprint: 4 of 7 (High - largest story, 13 points)

---

**Story Template Version:** 2.1
**Created:** 2025-11-25

## Implementation Notes

**Completed:** 2025-12-16

- [x] dependency-graph-analyzer subagent created - Completed: `.claude/agents/dependency-graph-analyzer.md` (400 lines)
- [x] YAML parsing for depends_on field - Completed: `parse_yaml_frontmatter()` in `src/dependency_graph_analyzer.py:62-98`
- [x] Graph building with adjacency list - Completed: `build_dependency_graph()` in `src/dependency_graph_analyzer.py:307-355`
- [x] Cycle detection with DFS - Completed: `detect_cycle()` in `src/dependency_graph_analyzer.py:183-219`
- [x] Transitive resolution - Completed: `resolve_transitive_dependencies()` in `src/dependency_graph_analyzer.py:151-180`
- [x] Status validation - Completed: `validate_dependency_statuses()` in `src/dependency_graph_analyzer.py:222-260`
- [x] --force bypass with logging - Completed: `analyze_dependencies()` lines 410-440 with audit logging
- [x] ASCII visualization - Completed: `generate_visualization()` in `src/dependency_graph_analyzer.py:263-303`
- [x] All 9 acceptance criteria have passing tests - Completed: 51 tests in `tests/dependency-graph/test_dependency_graph_analyzer.py`
- [x] Edge cases covered - Completed: 11 edge case tests (TestEdgeCases class)
- [x] NFRs met - Completed: Performance test verifies <500ms for 50 stories
- [x] 99% code coverage for analyzer - Completed: Verified via `--cov=src.dependency_graph_analyzer` (remediated from 92% to 99% on 2025-12-16)
- [x] Unit tests for parsing - Completed: TestYAMLParsing class (8 tests)
- [x] Unit tests for graph algorithms - Completed: TestGraphBuilding, TestCycleDetection, TestStatusValidation (18 tests)
- [x] Integration tests for /dev blocking - Completed: TestDevBlockingIntegration class (6 tests)

**Implementation Summary:**

Phase 2 (TDD Green) completed with all 51 tests passing:
- `src/dependency_graph_analyzer.py` (462 lines, 9 functions)
- `.claude/agents/dependency-graph-analyzer.md` (subagent definition)
- `tests/dependency-graph/` (test suite + 11 fixtures)

Phase 3 & 4 completed:
- Step 0.2.5 added to `preflight-validation.md`
- `--force` flag added to `dev.md`
- ADR-008 created for test fixture pre-commit exclusion

**Files Created:**
- `src/dependency_graph_analyzer.py`
- `.claude/agents/dependency-graph-analyzer.md`
- `tests/dependency-graph/test_dependency_graph_analyzer.py`
- `tests/dependency-graph/conftest.py`
- `tests/dependency-graph/fixtures/*.story.md` (11 files)
- `devforgeai/specs/adrs/ADR-008-exclude-test-fixtures-from-precommit-validation.md`

**Files Modified:**
- `.claude/skills/devforgeai-development/references/preflight-validation.md`
- `.claude/commands/dev.md`
- `.git/hooks/pre-commit`

**Git Commits:**
- `a993c9c` - Phase 2: TDD Green (implementation + tests)
- `b6a0a4c` - Phases 3 & 4: Integration + --force flag

### Resolved: Coverage Measurement

**Issue:** Coverage tooling initially wasn't collecting data (module path issue)
**Resolution:** Used correct module path `--cov=src.dependency_graph_analyzer`
**Result:** 92% coverage achieved (exceeds 90% target)
**Tests added:** 6 additional edge case tests for YAML parsing and normalize_depends_on

### Resolved: Integration Tests

**Issue:** Integration tests for /dev blocking initially deferred
**Resolution:** Implemented TestDevBlockingIntegration class with 6 tests
**Tests cover:**
- Blocking when dependency status is "In Development"
- Blocking when circular dependency detected
- Proceeding when all dependencies valid
- --force flag bypasses blocking with logging
- Blocking when dependency has "QA Failed" status
- Visualization shown on block

### Bug Fix: Circular Dependency Visualization

**Issue:** `generate_visualization()` caused infinite recursion on circular dependencies
**Resolution:** Added `visited` set parameter to track already visited nodes
**Result:** Visualization now shows `[CIRCULAR]` marker instead of crashing

### Coverage Gap Remediation (2025-12-16)

**Issue:** QA deep validation failed - Business logic coverage 92.16% below 95% threshold
**Gap Analysis:** `devforgeai/qa/reports/STORY-093-gaps.json` identified 5 functions with gaps:
- `build_dependency_graph`: 75.76% (lines 345, 353-356, 363-364, 373)
- `analyze_dependencies`: 89.19% (lines 410, 435-437)
- `resolve_transitive_dependencies`: 90% (lines 163, 170)
- `detect_cycle`: 88.89% (line 200)
- `generate_visualization`: 95.45% (line 303)

**Resolution:** Added 16 tests in `TestCoverageGapRemediation` class:
- 4 tests for `build_dependency_graph` edge cases (None deps, missing files, malformed YAML)
- 3 tests for `analyze_dependencies` edge cases (default path, missing deps blocking)
- 4 tests for `resolve_transitive_dependencies` (empty graph, None graph, not in graph, visited)
- 3 tests for `detect_cycle` (empty graph, not in graph)
- 2 tests for `generate_visualization` (no status in map, partial status map)

**Result:** Coverage improved from 92.16% to 99% (3 lines remaining: 170, 303, 345)

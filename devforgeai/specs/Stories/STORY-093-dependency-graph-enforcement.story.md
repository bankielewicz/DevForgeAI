---
id: STORY-093
title: Dependency Graph Enforcement with Transitive Resolution
epic: EPIC-010
sprint: SPRINT-5
status: Ready for Dev
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
**And** warning is logged to `.devforgeai/logs/dependency-bypass-{timestamp}.log`
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
          test_requirement: "Test: --force logs to .devforgeai/logs/"
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
- [ ] dependency-graph-analyzer subagent created
- [ ] YAML parsing for depends_on field
- [ ] Graph building with adjacency list
- [ ] Cycle detection with DFS
- [ ] Transitive resolution
- [ ] Status validation
- [ ] --force bypass with logging
- [ ] ASCII visualization

### Quality
- [ ] All 9 acceptance criteria have passing tests
- [ ] Edge cases covered
- [ ] NFRs met
- [ ] 90% code coverage for subagent

### Testing
- [ ] Unit tests for parsing
- [ ] Unit tests for graph algorithms
- [ ] Integration tests for /dev blocking

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
- Priority in sprint: 4 of 7 (High - largest story, 13 points)

---

**Story Template Version:** 2.1
**Created:** 2025-11-25

## Implementation Notes

No implementation yet - story in planning/backlog phase.

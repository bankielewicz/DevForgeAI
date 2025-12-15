---
id: STORY-094
title: File Overlap Detection with Hybrid Analysis
epic: EPIC-010
sprint: SPRINT-5
status: Ready for Dev
points: 8
priority: High
assigned_to: TBD
created: 2025-11-25
format_version: "2.1"
depends_on: ["STORY-093"]
---

# Story: File Overlap Detection with Hybrid Analysis

## Description

**As a** DevForgeAI developer working on parallel story implementation,
**I want** automatic detection when two or more concurrent stories will modify overlapping files,
**so that** I can make informed decisions about parallelization safety, avoid merge conflicts, and coordinate with other parallel work streams.

**Context:** This is Feature 4 of EPIC-010 (Parallel Story Development). File overlap detection prevents merge conflicts by warning developers before they commit to conflicting parallel work.

## Acceptance Criteria

### AC#1: Pre-Flight Spec-Based Overlap Detection

**Given** two or more stories exist with status "In Development"
**And** each has `technical_specification` with `file_path` fields
**When** developer runs `/dev STORY-XXX`
**Then** the file-overlap-detector subagent:
- Parses technical_specification YAML
- Extracts all file_path values
- Scans other active stories for overlaps
- Returns analysis within 3 seconds

---

### AC#2: Interactive Overlap Warning Display

**Given** pre-flight detects file overlap
**When** presenting warning to developer
**Then** AskUserQuestion displays:
```
Overlap Detected: 2 files shared with STORY-037
(1) Yes - Proceed
(2) No - Cancel
(3) Review - Show detailed report
```

---

### AC#3: Post-Flight Git-Based Overlap Validation

**Given** developer completed Phase 2 (Implementation)
**And** story is in worktree
**When** Phase 2-3 transition occurs
**Then** the system:
- Runs git diff to find actual changed files
- Compares against spec-declared file_path values
- Detects undeclared modifications
- Detects unused declarations

---

### AC#4: Spec Discrepancy Logging

**Given** post-flight finds discrepancies
**When** discrepancy is detected
**Then** warning is logged:
- Undeclared modifications listed
- Unused declarations listed
- Recommendation to update technical_specification

---

### AC#5: Overlap Report Generation

**Given** overlap detection has completed
**When** analysis is finished
**Then** report is saved to:
`tests/reports/overlap-STORY-{id}-{timestamp}.md`

Including:
- Story ID and timestamp
- Analysis type (pre-flight/post-flight)
- Overlapping files with source stories
- Recommendations

---

### AC#6: Dependency-Aware Filtering

**Given** STORY-XXX has `depends_on: [STORY-YYY]`
**And** they share overlapping files
**When** overlap detection runs
**Then** dependent story overlaps are excluded from warnings
**And** only non-dependent parallel stories trigger warnings

---

### AC#7: Empty or Missing Spec Handling

**Given** a story lacks technical_specification
**Or** components array is empty
**When** overlap detection runs
**Then** warning is logged
**And** spec-based pre-flight is skipped
**And** git-based post-flight still runs

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Service"
      name: "file-overlap-detector"
      file_path: "src/claude/agents/file-overlap-detector.md"
      interface: "Subagent"
      dependencies:
        - "Read"
        - "Bash (git diff)"
        - "Grep"
        - "Glob"
      requirements:
        - id: "SVC-001"
          description: "Parse technical_specification and extract file_path values"
          testable: true
          test_requirement: "Test: 5 components return 5 file_path values in <100ms"
          priority: "Critical"
        - id: "SVC-002"
          description: "Detect overlapping files across active stories"
          testable: true
          test_requirement: "Test: Two stories sharing src/User.cs returns overlap"
          priority: "Critical"
        - id: "SVC-003"
          description: "Execute git diff to identify actual changes"
          testable: true
          test_requirement: "Test: Post-flight identifies modified files in worktree"
          priority: "Critical"
        - id: "SVC-004"
          description: "Generate structured overlap report in Markdown"
          testable: true
          test_requirement: "Test: Report contains all required sections"
          priority: "High"
        - id: "SVC-005"
          description: "Return actionable recommendations"
          testable: true
          test_requirement: "Test: 15 overlapping files returns 'sequential development'"
          priority: "High"

    - type: "Configuration"
      name: "parallel.yaml (overlap section)"
      file_path: "src/devforgeai/config/parallel.yaml.example"
      required_keys:
        - key: "overlap.warning_threshold"
          type: "integer"
          default: "1"
          test_requirement: "Test: Warn if >= 1 file overlaps"
        - key: "overlap.blocking_threshold"
          type: "integer"
          default: "10"
          test_requirement: "Test: Block if >= 10 files overlap"

  business_rules:
    - id: "BR-001"
      rule: "Overlap warnings for non-dependent parallel stories only"
      trigger: "Pre-flight analysis"
      validation: "Filter out depends_on stories"
      test_requirement: "Test: Dependent story overlap not warned"
      priority: "High"
    - id: "BR-002"
      rule: "Post-flight detects spec discrepancies"
      trigger: "Phase 2-3 transition"
      validation: "Compare git diff to spec file_path"
      test_requirement: "Test: Undeclared modification detected"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Pre-flight spec parsing"
      metric: "< 500ms per story (p95)"
      test_requirement: "Test: Parse story spec in <500ms"
      priority: "Medium"
    - id: "NFR-002"
      category: "Performance"
      requirement: "Active story scanning"
      metric: "< 2 seconds for 50 stories (p95)"
      test_requirement: "Test: Scan 50 stories in <2s"
      priority: "Medium"
    - id: "NFR-003"
      category: "Performance"
      requirement: "Total Phase 0 overhead"
      metric: "< 5 seconds added to /dev startup (p95)"
      test_requirement: "Test: Overlap check adds <5s to Phase 0"
      priority: "High"
```

---

## Non-Functional Requirements

### Performance
- Pre-flight parsing: < 500ms per story
- Active story scanning: < 2 seconds for 50 stories
- Git diff execution: < 3 seconds for 1000 files
- Total Phase 0 overhead: < 5 seconds

### Security
- Path traversal prevention in file_path validation
- No privilege escalation
- Report sanitization (paths only, no contents)

### Reliability
- Graceful degradation: fall back to git-only if spec parsing fails
- Idempotency: consistent results on repeated runs
- Atomic report writing

---

## Edge Cases

1. **Circular dependency overlap:** Recommend sequential development
2. **Worktree not available:** Single-branch comparison
3. **Glob pattern in file_path:** Expand before comparison
4. **Story status changes mid-analysis:** Re-scan at post-flight
5. **Large overlap (>20 files):** Paginate and recommend sequential
6. **Git history unavailable:** Spec-only with low confidence
7. **Same file different sections:** Note file-level only

---

## Dependencies

### Prerequisite Stories
- [ ] **STORY-093:** Dependency Graph Enforcement (for dependency-aware filtering)

### Deliverables
- NEW: file-overlap-detector subagent (~350 lines)

---

## Definition of Done

### Implementation
- [ ] file-overlap-detector subagent created
- [ ] Spec parsing for file_path extraction
- [ ] Overlap detection across stories
- [ ] Git diff integration for post-flight
- [ ] Interactive AskUserQuestion prompt
- [ ] Overlap report generation
- [ ] Dependency-aware filtering

### Quality
- [ ] All 7 acceptance criteria have passing tests
- [ ] Edge cases covered
- [ ] NFRs met
- [ ] 90% code coverage

### Testing
- [ ] Unit tests for spec parsing
- [ ] Unit tests for overlap detection
- [ ] Integration tests for pre/post-flight

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
- Priority in sprint: 5 of 7 (High - depends on STORY-093)

---

**Story Template Version:** 2.1
**Created:** 2025-11-25

## Implementation Notes

No implementation yet - story in planning/backlog phase.

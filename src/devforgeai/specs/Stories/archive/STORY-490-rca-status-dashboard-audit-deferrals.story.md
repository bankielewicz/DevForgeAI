---
id: STORY-490
title: RCA Status Dashboard in /audit-deferrals
type: feature
epic: null
sprint: Backlog
status: QA Approved
points: 1
depends_on: []
priority: Low
advisory: false
source_gap: null
source_story: null
source_rca: "RCA-039"
source_recommendation: "REC-6"
assigned_to: DevForgeAI AI Agent
created: 2026-02-22
format_version: "2.9"
---

# Story: RCA Status Dashboard in /audit-deferrals

## Description

**As a** framework maintainer,
**I want** the `/audit-deferrals` command to include an "Open RCAs" section showing count, oldest open RCA, and unimplemented recommendation count,
**so that** stale RCA recommendations are visible during routine auditing and don't silently accumulate.

## Provenance

```xml
<provenance>
  <origin document="RCA-039" section="REC-6">
    <quote>"No visibility into OPEN RCA count or age."</quote>
    <line_reference>RCA-039 lines 309-315</line_reference>
    <quantified_impact>RCA-033 was open for 27 days unnoticed; dashboard would surface this</quantified_impact>
  </origin>
</provenance>
```

## Acceptance Criteria

### AC#1: Open RCAs Section in Output

```xml
<acceptance_criteria id="AC1">
  <given>/audit-deferrals command executes</given>
  <when>the output is displayed</when>
  <then>an "Open RCAs" section appears showing: total open RCA count, oldest open RCA (ID + age in days), total unimplemented CRITICAL/HIGH recommendations across all open RCAs</then>
  <verification>
    <source_files>
      <file hint="command file">src/claude/commands/audit-deferrals.md</file>
    </source_files>
    <test_file>tests/STORY-490/test_ac1_open_rcas_section.sh</test_file>
  </verification>
</acceptance_criteria>
```

### AC#2: RCA Scanning Logic

```xml
<acceptance_criteria id="AC2">
  <given>devforgeai/RCA/ directory contains RCA files with various statuses</given>
  <when>/audit-deferrals scans for open RCAs</when>
  <then>files are scanned for "Status" or "status" field, counted as open when status is not "RESOLVED" or "CLOSED", and unchecked implementation checklist items are counted</then>
  <verification>
    <source_files>
      <file hint="command file">src/claude/commands/audit-deferrals.md</file>
    </source_files>
    <test_file>tests/STORY-490/test_ac2_rca_scanning.sh</test_file>
  </verification>
</acceptance_criteria>
```

### AC#3: Zero Open RCAs Handled

```xml
<acceptance_criteria id="AC3">
  <given>all RCA files have status RESOLVED or CLOSED</given>
  <when>/audit-deferrals executes</when>
  <then>"Open RCAs: 0 — All RCAs resolved ✅" is displayed (no error, no empty section)</then>
  <verification>
    <source_files>
      <file hint="command file">src/claude/commands/audit-deferrals.md</file>
    </source_files>
    <test_file>tests/STORY-490/test_ac3_zero_rcas.sh</test_file>
  </verification>
</acceptance_criteria>
```

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  dual_path_sync:
    note: "Per source-tree.md dual-path architecture, development happens in src/ tree."
    source_paths:
      - "src/claude/commands/audit-deferrals.md"
    operational_paths:
      - ".claude/commands/audit-deferrals.md"
    test_against: "src/"

  components:
    - type: "Configuration"
      name: "rca-dashboard-section"
      file_path: "src/claude/commands/audit-deferrals.md"
      required_keys:
        - key: "Open RCAs section"
          type: "string"
          required: true
          validation: "Section scans devforgeai/RCA/ and displays counts"
          test_requirement: "Test: Grep for 'Open RCAs' in audit-deferrals.md"
```

## Technical Limitations

```yaml
technical_limitations: []
```

## Dependencies

### Prerequisite Stories
- None

## Test Strategy

### Unit Tests
**Coverage Target:** 85%+ (infrastructure layer)

## Acceptance Criteria Verification Checklist

- [x] Open RCAs section in output - **Phase:** 3
- [x] Scanning logic works - **Phase:** 2
- [x] Zero RCAs handled gracefully - **Phase:** 2

**Checklist Progress:** 3/3 items complete (100%)

## Definition of Done

### Implementation
- [x] "Open RCAs" section added to audit-deferrals.md output
- [x] RCA file scanning via Glob + Grep for status
- [x] Count of open RCAs, oldest, and unimplemented CRITICAL/HIGH recs
- [x] Zero-state handled gracefully

### Dual-Path Sync
- [x] File modified in src/claude/commands/ (source of truth)
- [ ] File synced to .claude/commands/ (operational)
- [x] Tests run against src/ tree

### Quality
- [x] All 3 acceptance criteria have passing tests

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|
| Red | ✅ Complete | 17 tests written, all failing initially |
| Green | ✅ Complete | Open RCAs Dashboard section added to audit-deferrals.md |
| Refactor | ✅ Complete | No refactoring needed per review |

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|
| src/claude/commands/audit-deferrals.md | Modified | Added Phase 1.5 (~40 lines) |
| tests/STORY-490/test_ac1_open_rcas_section.sh | Created | 5 tests for AC#1 |
| tests/STORY-490/test_ac2_rca_scanning.sh | Created | 7 tests for AC#2 |
| tests/STORY-490/test_ac3_zero_rcas.sh | Created | 5 tests for AC#3 |
| tests/STORY-490/run_all_tests.sh | Created | Test runner |

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-23

- [x] "Open RCAs" section added to audit-deferrals.md output - Completed: Added Phase 1.5 with Open RCAs Dashboard section
- [x] RCA file scanning via Glob + Grep for status - Completed: Scanning logic uses Glob for discovery and Grep for status field detection
- [x] Count of open RCAs, oldest, and unimplemented CRITICAL/HIGH recs - Completed: Dashboard displays all three metrics
- [x] Zero-state handled gracefully - Completed: Displays "Open RCAs: 0 — All RCAs resolved ✅"
- [x] File modified in src/claude/commands/ (source of truth) - Completed: Changes made to src/ tree
- [x] Tests run against src/ tree - Completed: All 17 tests pass against src/
- [x] All 3 acceptance criteria have passing tests - Completed: 17/17 tests pass across 3 suites

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-22 | /create-stories-from-rca | Created | Story created from RCA-039 REC-6 | STORY-490.story.md |
| 2026-02-23 | .claude/qa-result-interpreter | QA Deep | PASS WITH WARNINGS: 17/17 tests pass, 2 MEDIUM violations | - |

## Notes

**References:**
- [RCA-039](devforgeai/RCA/RCA-039-dual-path-architecture-validation-gap.md) (REC-6)

---

Story Template Version: 2.9
Last Updated: 2026-02-22

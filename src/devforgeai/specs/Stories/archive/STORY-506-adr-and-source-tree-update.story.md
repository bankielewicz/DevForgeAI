---
id: STORY-506
title: ADR-025 Acceptance and Source-Tree Update
type: documentation
epic: EPIC-085
sprint: Sprint-18
status: QA Approved
points: 3
depends_on: []
priority: Medium
advisory: false
source_gap: null
source_story: null
assigned_to: null
created: 2026-02-27
format_version: "2.9"
---

# Story: ADR-025 Acceptance and Source-Tree Update

## Description

**As a** DevForgeAI framework maintainer,
**I want** ADR-025 accepted and the source-tree.md updated to document the QA snapshot directory structure,
**so that** the qa-diff-regression-detection foundation is formally ratified and all downstream EPIC-085 stories have a verified source-tree contract to build against.

## Acceptance Criteria

> **IMPORTANT:** XML acceptance criteria format is REQUIRED for automated verification.

### XML Acceptance Criteria Format

### AC#1: ADR-025 Status Updated from Proposed to Accepted

```xml
<acceptance_criteria id="AC1" implements="COMP-001">
  <given>ADR-025 exists at devforgeai/specs/adrs/ADR-025-qa-diff-regression-detection.md with status: Proposed</given>
  <when>The story is implemented by updating the ADR status field</when>
  <then>The ADR file contains status: Accepted and the acceptance date is recorded, with no other content altered</then>
  <verification>
    <source_files>
      <file hint="ADR file">devforgeai/specs/adrs/ADR-025-qa-diff-regression-detection.md</file>
    </source_files>
  </verification>
</acceptance_criteria>
```

---

### AC#2: source-tree.md Documents devforgeai/qa/snapshots/ Directory

```xml
<acceptance_criteria id="AC2" implements="COMP-002">
  <given>devforgeai/specs/context/source-tree.md exists and does not contain a devforgeai/qa/ section</given>
  <when>The source-tree.md is updated</when>
  <then>source-tree.md contains an entry for devforgeai/qa/snapshots/ describing it as the root snapshot storage directory</then>
  <verification>
    <source_files>
      <file hint="Source tree context file">devforgeai/specs/context/source-tree.md</file>
    </source_files>
  </verification>
</acceptance_criteria>
```

---

### AC#3: source-tree.md Documents {STORY_ID}/ Subdirectory Pattern

```xml
<acceptance_criteria id="AC3" implements="COMP-002">
  <given>devforgeai/qa/snapshots/ has been added to source-tree.md</given>
  <when>A reader inspects the source-tree.md snapshot section</when>
  <then>source-tree.md explicitly documents the {STORY_ID}/ subdirectory pattern with description of per-story isolation purpose</then>
</acceptance_criteria>
```

---

### AC#4: source-tree.md Documents red-phase-checksums.json File

```xml
<acceptance_criteria id="AC4" implements="COMP-002">
  <given>The {STORY_ID}/ subdirectory pattern is documented</given>
  <when>A reader inspects the snapshot section</when>
  <then>source-tree.md documents red-phase-checksums.json as the canonical file within each {STORY_ID}/ directory with its purpose (storing Red-phase test checksums)</then>
</acceptance_criteria>
```

---

### AC#5: ADR-025 Cross-Reference in source-tree.md

```xml
<acceptance_criteria id="AC5" implements="COMP-002">
  <given>source-tree.md has been updated with the snapshot directory structure</given>
  <when>The snapshot section is read</when>
  <then>source-tree.md includes a cross-reference to ADR-025 as the governing decision for this directory structure</then>
</acceptance_criteria>
```

---

### Source Files Guidance

The `<source_files>` element provides hints to the ac-compliance-verifier about where implementation code is located.

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "ADR-025 Status Update"
      file_path: "devforgeai/specs/adrs/ADR-025-qa-diff-regression-detection.md"
      required_keys:
        - key: "status"
          type: "string"
          required: true
          test_requirement: "Test: Read ADR-025; assert status field equals 'Accepted'"
        - key: "acceptance_date"
          type: "string"
          required: true
          test_requirement: "Test: Read ADR-025; assert acceptance date matches ISO 8601 YYYY-MM-DD"

    - type: "Configuration"
      name: "source-tree.md Snapshot Section"
      file_path: "devforgeai/specs/context/source-tree.md"
      required_keys:
        - key: "qa_snapshots_directory"
          type: "string"
          required: true
          test_requirement: "Test: Grep source-tree.md for 'devforgeai/qa/snapshots/'; assert match"
        - key: "story_id_subdirectory"
          type: "string"
          required: true
          test_requirement: "Test: Grep source-tree.md for '{STORY_ID}'; assert match with description"
        - key: "checksums_file"
          type: "string"
          required: true
          test_requirement: "Test: Grep source-tree.md for 'red-phase-checksums.json'; assert match"
        - key: "adr_cross_reference"
          type: "string"
          required: true
          test_requirement: "Test: Grep source-tree.md for 'ADR-025'; assert match within snapshot section"

  business_rules:
    - id: "BR-001"
      rule: "ADR status update must be a targeted field change, not a body rewrite"
      trigger: "When ADR-025 is edited"
      validation: "git diff shows only status and date fields changed"
      error_handling: "If other content changed, revert and retry with targeted Edit"
      test_requirement: "Test: git diff ADR-025 shows only status and date changes"
      priority: "Critical"
    - id: "BR-002"
      rule: "source-tree.md update must match existing notation convention"
      trigger: "When source-tree.md is edited"
      validation: "New entries use same indentation and path notation as existing entries"
      error_handling: "Read nearby entries to infer pattern"
      test_requirement: "Test: New entries use consistent formatting with existing source-tree.md"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Both edits complete quickly"
      metric: "< 5 seconds of wall-clock tool execution time"
      test_requirement: "Test: Total edit time under 5 seconds"
      priority: "Low"
    - id: "NFR-002"
      category: "Reliability"
      requirement: "source-tree.md remains valid after update"
      metric: "No broken headings, unclosed fences, or malformed rows"
      test_requirement: "Test: source-tree.md parseable by devforgeai-validate after update"
      priority: "High"
```

## Technical Limitations

```yaml
technical_limitations: []
```

## Non-Functional Requirements (NFRs)

### Performance

**Edit Time:**
- Both file edits: < 5 seconds total wall-clock time
- No file larger than 500 KB written

### Security

**No Secrets:**
- No credentials or environment-specific values introduced
- {STORY_ID} pattern clearly labeled as substitution token

### Scalability

**Unbounded Story Count:**
- Snapshot directory pattern supports unlimited {STORY_ID}/ subdirectories
- source-tree.md parseable by automated tooling after update

### Reliability

**Idempotent:**
- ADR status update idempotent (second run produces same result)
- source-tree.md remains valid markdown after update
- No partial changes on mid-operation failure

### Observability

**Traceability:**
- ADR-025 cross-reference in source-tree.md enables traceability

## Dependencies

### Prerequisite Stories

None — this is the foundation story for EPIC-085.

### External Dependencies

None.

### Technology Dependencies

None — uses existing Edit tool for file modifications.

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for business logic

**Test Scenarios:**
1. **Happy Path:** ADR status changed to Accepted, source-tree.md updated with snapshot section
2. **Edge Cases:**
   - ADR-025 already Accepted → no change needed (idempotent)
   - source-tree.md already has qa/ entry → reconcile, don't duplicate
   - ADR-025 file missing → HALT
   - source-tree.md format ambiguous → infer from nearby entries
3. **Error Cases:**
   - ADR-025 status is Rejected → HALT and AskUserQuestion

### Integration Tests

**Coverage Target:** 85%+ for application layer

**Test Scenarios:**
1. **Validation:** devforgeai-validate parses source-tree.md after update
2. **Downstream:** STORY-502 can reference devforgeai/qa/snapshots/ in source-tree.md

## Acceptance Criteria Verification Checklist

**Purpose:** Real-time progress tracking during TDD implementation.

### AC#1: ADR-025 Status Updated

- [ ] Status field changed to Accepted - **Phase:** 2 - **Evidence:** ADR-025 file
- [ ] Acceptance date recorded - **Phase:** 2 - **Evidence:** ADR-025 file
- [ ] No other content altered - **Phase:** 2 - **Evidence:** git diff

### AC#2: Snapshot Directory Entry

- [ ] devforgeai/qa/snapshots/ entry in source-tree.md - **Phase:** 2 - **Evidence:** source-tree.md

### AC#3: {STORY_ID}/ Pattern

- [ ] {STORY_ID}/ documented with description - **Phase:** 2 - **Evidence:** source-tree.md

### AC#4: red-phase-checksums.json

- [ ] File entry documented with purpose - **Phase:** 2 - **Evidence:** source-tree.md

### AC#5: ADR-025 Cross-Reference

- [ ] ADR-025 referenced in snapshot section - **Phase:** 2 - **Evidence:** source-tree.md

---

**Checklist Progress:** 0/8 items complete (0%)

---

<!-- IMPLEMENTATION NOTES FORMAT REQUIREMENT (Critical for pre-commit validation):
See: .claude/skills/implementing-stories/references/dod-update-workflow.md for complete details
-->

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-27

- [x] ADR-025 status changed from Proposed to Accepted - Completed: Updated status field in ADR-025-qa-diff-regression-detection.md
- [x] ADR-025 acceptance date recorded (ISO 8601) - Completed: Added **Acceptance Date:** 2026-02-27
- [x] source-tree.md updated with devforgeai/qa/snapshots/ directory - Completed: Added snapshots/ entry under qa/ section
- [x] source-tree.md documents {STORY_ID}/ subdirectory pattern - Completed: Added {STORY_ID}/ with per-story isolation description
- [x] source-tree.md documents red-phase-checksums.json file - Completed: Added entry with SHA-256 checksum purpose
- [x] source-tree.md includes ADR-025 cross-reference - Completed: Added (ADR-025) annotation on snapshots/ line
- [x] All 5 acceptance criteria have passing tests - Completed: 11 tests in tests/STORY-506/test_adr025_acceptance.py all pass
- [x] ADR changes limited to status and date only (verified via diff) - Completed: Only status and date fields modified
- [x] source-tree.md formatting consistent with existing entries - Completed: Used same tree notation pattern
- [x] source-tree.md remains parseable by devforgeai-validate - Completed: Verified valid markdown structure
- [x] Unit tests for ADR status field update - Completed: TestAC1_ADRStatusUpdate (3 tests)
- [x] Unit tests for source-tree.md entry presence - Completed: TestAC2-AC5 (8 tests)
- [x] Unit tests for cross-reference integrity - Completed: TestAC5_ADRCrossReference (2 tests)
- [x] Edge case test for idempotent ADR update - Completed: test_adr025_status_not_proposed verifies idempotency
- [x] ADR-025 rationale preserved - Completed: Only status/date fields changed
- [x] source-tree.md snapshot section clearly describes purpose - Completed: "Red-phase test integrity snapshots"
- [x] Cross-reference enables traceability - Completed: ADR-025 referenced in snapshots/ entry

## Definition of Done

### Implementation
- [x] ADR-025 status changed from Proposed to Accepted
- [x] ADR-025 acceptance date recorded (ISO 8601)
- [x] source-tree.md updated with devforgeai/qa/snapshots/ directory
- [x] source-tree.md documents {STORY_ID}/ subdirectory pattern
- [x] source-tree.md documents red-phase-checksums.json file
- [x] source-tree.md includes ADR-025 cross-reference

### Quality
- [x] All 5 acceptance criteria have passing tests
- [x] ADR changes limited to status and date only (verified via diff)
- [x] source-tree.md formatting consistent with existing entries
- [x] source-tree.md remains parseable by devforgeai-validate

### Testing
- [x] Unit tests for ADR status field update
- [x] Unit tests for source-tree.md entry presence
- [x] Unit tests for cross-reference integrity
- [x] Edge case test for idempotent ADR update

### Documentation
- [x] ADR-025 rationale preserved
- [x] source-tree.md snapshot section clearly describes purpose
- [x] Cross-reference enables traceability

---

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|
| Red | ✅ Complete | 11 tests written, all failing |
| Green | ✅ Complete | ADR-025 status updated, source-tree.md updated, 11/11 pass |
| Refactor | ✅ Complete | No refactoring needed (documentation story) |

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|
| devforgeai/specs/adrs/ADR-025-qa-diff-regression-detection.md | Modified | +1 line (acceptance date), 1 line changed (status) |
| devforgeai/specs/context/source-tree.md | Modified | +3 lines (snapshots directory tree) |
| tests/STORY-506/test_adr025_acceptance.py | Created | 120 lines (11 tests) |

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-27 12:00 | .claude/story-requirements-analyst | Created | Story created from EPIC-085 Feature 6 | STORY-506.story.md |
| 2026-02-27 | /validate-stories | Status Update | Status changed from Backlog to Ready for Dev | STORY-506.story.md |
| 2026-02-27 | .claude/qa-result-interpreter | QA Deep | PASSED: 11/11 tests, 0 violations | STORY-506.story.md |

## Notes

**Design Decisions:**
- ADR-025 already exists as Proposed — this story only changes status to Accepted
- source-tree.md update is minimal: add snapshot directory tree beneath devforgeai/qa/
- {STORY_ID} is a substitution token documented literally (with braces)
- This is the foundation story — all other EPIC-085 stories depend on it

**Related ADRs:**
- [ADR-025: QA Diff Regression Detection](../adrs/ADR-025-qa-diff-regression-detection.md)

**References:**
- EPIC-085: QA Diff Regression Detection and Test Integrity System
- Feature 6: ADR and Source-Tree Update (ADR-025)

---

Story Template Version: 2.9
Last Updated: 2026-02-27

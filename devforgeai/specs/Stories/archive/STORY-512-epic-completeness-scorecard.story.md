---
id: STORY-512
title: Create Epic Completeness Scorecard Display
type: feature
epic: N/A
sprint: Sprint-21
status: QA Approved ✅
points: 2
depends_on: ["STORY-507"]
priority: Low
advisory: false
source_gap: null
source_story: null
assigned_to: Unassigned
created: 2026-02-27
format_version: "2.9"
---

# Story: Create Epic Completeness Scorecard Display

## Description

**As a** DevForgeAI framework user,
**I want** to see a completeness scorecard after epic creation showing which sections are present and populated,
**so that** I can catch gaps before leaving the session without manually auditing the document.

**Source:** RCA-042 REC-6

## Provenance

```xml
<provenance>
  <origin document="RCA-042" section="REC-6">
    <quote>"User had to manually audit the epic to discover it was incomplete. No quick way to assess if an epic is 'ready for story creation.'"</quote>
    <line_reference>lines 284-306</line_reference>
    <quantified_impact>Eliminates need for manual audit of epic completeness</quantified_impact>
  </origin>
</provenance>
```

## Acceptance Criteria

### AC#1: Scorecard Display After Epic Creation

```xml
<acceptance_criteria id="AC1">
  <given>The designing-systems skill epic creation workflow</given>
  <when>An epic is successfully created</when>
  <then>A completeness scorecard is displayed showing each section with ✅ (present and populated), ⚠️ (missing or empty), and an overall score (e.g., "10/13 sections complete")</then>
  <verification>
    <source_files>
      <file hint="Epic creation workflow">.claude/skills/designing-systems/references/artifact-generation.md</file>
    </source_files>
    <test_file>tests/STORY-512/test_ac1_scorecard_display.sh</test_file>
  </verification>
</acceptance_criteria>
```

### AC#2: Decision Context Section Included in Scorecard

```xml
<acceptance_criteria id="AC2">
  <given>The completeness scorecard</given>
  <when>The scorecard sections are inspected</when>
  <then>Decision Context and its key subsections (Design Rationale, Rejected Alternatives) are individually scored</then>
  <verification>
    <source_files>
      <file hint="Epic creation workflow">.claude/skills/designing-systems/references/artifact-generation.md</file>
    </source_files>
    <test_file>tests/STORY-512/test_ac2_decision_context_scored.sh</test_file>
  </verification>
</acceptance_criteria>
```

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "artifact-generation.md"
      file_path: ".claude/skills/designing-systems/references/artifact-generation.md"
      required_keys:
        - key: "Completeness scorecard step"
          type: "markdown"
          required: true
          test_requirement: "Test: Verify scorecard display step exists after epic creation"
```

## Technical Limitations

```yaml
technical_limitations: []
```

## Non-Functional Requirements (NFRs)

### Performance
N/A

### Security
N/A

### Scalability
N/A

### Reliability
N/A

### Observability
N/A

## Dependencies

### Prerequisite Stories
- [ ] **STORY-507:** Add Decision Context Section to Epic Template
  - **Why:** Scorecard includes Decision Context which must exist in template
  - **Status:** Backlog

### External Dependencies
None.

### Technology Dependencies
None.

## Test Strategy

### Unit Tests
**Test Scenarios:**
1. **Happy Path:** Scorecard display step exists in workflow
2. **Decision Context:** Scorecard includes Decision Context subsections

### Integration Tests
N/A

## Acceptance Criteria Verification Checklist

### AC#1: Scorecard Display
- [x] Scorecard step in workflow - **Phase:** 3
- [x] Uses ✅/⚠️ indicators - **Phase:** 3
- [x] Shows overall score - **Phase:** 3

### AC#2: Decision Context Scored
- [x] Design Rationale individually scored - **Phase:** 3
- [x] Rejected Alternatives individually scored - **Phase:** 3

---

**Checklist Progress:** 5/5 items complete (100%)

## Definition of Done

### Implementation
- [x] Completeness scorecard step added to epic creation workflow
- [x] Decision Context subsections individually scored

### Quality
- [x] All 2 acceptance criteria have passing tests

### Testing
- [x] Content verification tests

### Documentation
- [x] RCA-042 updated with STORY-512 link

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-28

- [x] Completeness scorecard step added to epic creation workflow - Completed: Added Step 6.1.7 to artifact-generation.md with scorecard procedure and display format
- [x] Decision Context subsections individually scored - Completed: Design Rationale and Rejected Alternatives scored individually in scorecard
- [x] All 2 acceptance criteria have passing tests - Completed: 9 tests (5 AC#1 + 4 AC#2) all passing
- [x] Content verification tests - Completed: Shell script tests in tests/STORY-512/ verify grep patterns
- [x] RCA-042 updated with STORY-512 link - Completed: Added STORY-512 reference to RCA-042

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|
| Phase 02 (Red) | ✅ Complete | 9 tests written, all failing |
| Phase 03 (Green) | ✅ Complete | Scorecard step implemented, all tests passing |
| Phase 04 (Refactor) | ✅ Complete | Reviewed by refactoring-specialist and code-reviewer |
| Phase 04.5 (AC Verify) | ✅ Complete | Both ACs verified PASS |
| Phase 05 (Integration) | ✅ Complete | Integration tests passed |
| Phase 05.5 (AC Verify) | ✅ Complete | Post-integration AC verification PASS |

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|
| src/claude/skills/designing-systems/references/artifact-generation.md | Modified | +85 lines (Step 6.1.7) |
| tests/STORY-512/test_ac1_scorecard_display.sh | Created | 59 lines |
| tests/STORY-512/test_ac2_decision_context_scored.sh | Created | 57 lines |
| tests/STORY-512/run_all_tests.sh | Created | 31 lines |

---

## Change Log

**Current Status:** Dev Complete

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-27 | /create-stories-from-rca | Created | Story created from RCA-042 REC-6 | STORY-512.story.md |
| 2026-02-28 | DevForgeAI AI Agent | /dev TDD | Implemented scorecard display step | artifact-generation.md, tests/ |

## Notes

**Source RCA:** RCA-042
**Source Recommendation:** REC-6

---

Story Template Version: 2.9
Last Updated: 2026-02-27

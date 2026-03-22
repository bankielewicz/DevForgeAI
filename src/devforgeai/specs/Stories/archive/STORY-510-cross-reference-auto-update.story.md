---
id: STORY-510
title: Add Cross-Reference Auto-Update Step to Epic Creation
type: feature
epic: N/A
sprint: Sprint-21
status: QA Approved
points: 2
depends_on: []
priority: High
advisory: false
source_gap: null
source_story: null
assigned_to: Unassigned
created: 2026-02-27
format_version: "2.9"
---

# Story: Add Cross-Reference Auto-Update Step to Epic Creation

## Description

**As a** DevForgeAI framework user,
**I want** the epic creation workflow to automatically update the source requirements document with actual epic and ADR IDs after creation,
**so that** cross-references remain accurate and no stale "NNN" placeholders persist.

**Source:** RCA-042 REC-4

## Provenance

```xml
<provenance>
  <origin document="RCA-042" section="REC-4">
    <quote>"Requirements doc contained stale references ('ADR-NNN', 'EPIC-NNN') because the epic creation workflow doesn't update the requirements doc with actual IDs after creation."</quote>
    <line_reference>lines 208-241</line_reference>
    <quantified_impact>Stale cross-references cause confusion and broken traceability</quantified_impact>
  </origin>
</provenance>
```

## Acceptance Criteria

### AC#1: Post-Write Cross-Reference Update Step Exists

```xml
<acceptance_criteria id="AC1">
  <given>The epic creation workflow in .claude/skills/designing-systems/references/artifact-generation.md</given>
  <when>The workflow steps are inspected</when>
  <then>A step exists (e.g., Step 6.7.5) that reads the source requirements document and replaces "EPIC-NNN" with the actual EPIC-XXX number and "ADR-NNN" with actual ADR-XXX number</then>
  <verification>
    <source_files>
      <file hint="Artifact generation workflow">.claude/skills/designing-systems/references/artifact-generation.md</file>
    </source_files>
    <test_file>tests/STORY-510/test_ac1_cross_ref_step.sh</test_file>
  </verification>
</acceptance_criteria>
```

### AC#2: STORY-NNN Placeholders Left Intact

```xml
<acceptance_criteria id="AC2">
  <given>The cross-reference update step</given>
  <when>The step instructions are read</when>
  <then>The step explicitly states that "STORY-NNN" placeholders are left as-is (stories not yet created at epic time)</then>
  <verification>
    <source_files>
      <file hint="Artifact generation workflow">.claude/skills/designing-systems/references/artifact-generation.md</file>
    </source_files>
    <test_file>tests/STORY-510/test_ac2_story_placeholder_preserved.sh</test_file>
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
        - key: "Cross-reference update step"
          type: "markdown"
          required: true
          test_requirement: "Test: Verify step exists for EPIC-NNN and ADR-NNN replacement"
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
None.

### External Dependencies
None.

### Technology Dependencies
None.

## Test Strategy

### Unit Tests
**Test Scenarios:**
1. **Happy Path:** Step exists referencing EPIC-NNN and ADR-NNN replacement
2. **Exclusion:** Step explicitly preserves STORY-NNN placeholders

### Integration Tests
N/A

## Acceptance Criteria Verification Checklist

### AC#1: Cross-Reference Step
- [x] Step 6.1.5 exists - **Phase:** 3 - **Evidence:** grep confirmed
- [x] Step references EPIC-NNN → EPIC-XXX replacement - **Phase:** 3
- [x] Step references ADR-NNN → ADR-XXX replacement - **Phase:** 3

### AC#2: STORY-NNN Preserved
- [x] Step explicitly says leave STORY-NNN as-is - **Phase:** 3

---

**Checklist Progress:** 4/4 items complete (100%)

## Definition of Done

### Implementation
- [x] Cross-reference auto-update step added to artifact-generation.md
- [x] Step preserves STORY-NNN placeholders

### Quality
- [x] All 2 acceptance criteria have passing tests

### Testing
- [x] Content verification tests

### Documentation
- [x] RCA-042 updated with STORY-510 link

---

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-28

- [x] Cross-reference auto-update step added to artifact-generation.md - Completed: Added Step 6.1.5 with EPIC-NNN and ADR-NNN replacement procedure
- [x] Step preserves STORY-NNN placeholders - Completed: Explicit section "STORY-NNN Placeholders: Leave As-Is" with rationale
- [x] All 2 acceptance criteria have passing tests - Completed: 6/6 tests pass (4 for AC1, 2 for AC2)
- [x] Content verification tests - Completed: Bash/grep tests in tests/STORY-510/
- [x] RCA-042 updated with STORY-510 link - Completed: Updated RCA-042 Implementation Checklist line 320 to [x]

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|
| Red | ✅ | 6 tests written, all fail |
| Green | ✅ | Step 6.1.5 added, all 6 tests pass |
| Refactor | ✅ | Reviewed by refactoring-specialist and code-reviewer |

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|
| src/claude/skills/designing-systems/references/artifact-generation.md | Modified | +63 |
| .claude/skills/designing-systems/references/artifact-generation.md | Modified (sync) | +63 |
| tests/STORY-510/test_ac1_cross_ref_step.sh | Created | ~40 |
| tests/STORY-510/test_ac2_story_placeholder_preserved.sh | Created | ~25 |

---

## Change Log

**Current Status:** Dev Complete

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-27 | /create-stories-from-rca | Created | Story created from RCA-042 REC-4 | STORY-510.story.md |

## Notes

**Source RCA:** RCA-042
**Source Recommendation:** REC-4

---

Story Template Version: 2.9
Last Updated: 2026-02-27

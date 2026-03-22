---
id: STORY-509
title: Add design_decisions Field to F4 Requirements Schema
type: feature
epic: N/A
sprint: Sprint-21
status: QA Approved
points: 3
depends_on: ["STORY-507"]
priority: High
advisory: false
source_gap: null
source_story: null
assigned_to: Unassigned
created: 2026-02-27
format_version: "2.9"
---

# Story: Add design_decisions Field to F4 Requirements Schema

## Description

**As a** DevForgeAI framework user,
**I want** the F4 requirements schema to include `design_decisions` and `threat_model` fields,
**so that** design rationale, rejected alternatives, and threat models are captured at the point of ideation and flow through the pipeline to epics and stories.

**Source:** RCA-042 REC-3

## Provenance

```xml
<provenance>
  <origin document="RCA-042" section="REC-3">
    <quote>"The F4 schema output by /ideate has no field for design decisions, rejected alternatives, or conversation insights. This means the requirements doc — the primary handoff artifact — cannot carry decision context."</quote>
    <line_reference>lines 170-203</line_reference>
    <quantified_impact>Requirements doc is the primary handoff artifact; missing fields cause context loss at every downstream stage</quantified_impact>
  </origin>
</provenance>
```

## Acceptance Criteria

### AC#1: design_decisions Field Added to F4 Schema

```xml
<acceptance_criteria id="AC1">
  <given>The F4 schema definition in .claude/skills/discovering-requirements/references/artifact-generation.md</given>
  <when>The schema is inspected</when>
  <then>A top-level `design_decisions` section exists with fields: id, decision, rationale, alternatives_rejected (array with name+reason), user_observations, constraints</then>
  <verification>
    <source_files>
      <file hint="F4 schema definition">.claude/skills/discovering-requirements/references/artifact-generation.md</file>
    </source_files>
    <test_file>tests/STORY-509/test_ac1_design_decisions_field.sh</test_file>
  </verification>
</acceptance_criteria>
```

### AC#2: threat_model Field Added to F4 Schema

```xml
<acceptance_criteria id="AC2">
  <given>The F4 schema definition</given>
  <when>The schema is inspected</when>
  <then>A top-level `threat_model` section exists with fields: adversary, in_scope (array), out_of_scope (array)</then>
  <verification>
    <source_files>
      <file hint="F4 schema definition">.claude/skills/discovering-requirements/references/artifact-generation.md</file>
    </source_files>
    <test_file>tests/STORY-509/test_ac2_threat_model_field.sh</test_file>
  </verification>
</acceptance_criteria>
```

### AC#3: Epic Creation Can Extract design_decisions

```xml
<acceptance_criteria id="AC3">
  <given>A requirements document containing design_decisions and threat_model fields</given>
  <when>The designing-systems skill creates an epic from it</when>
  <then>The epic's Decision Context section is populated from the requirements document's design_decisions and threat_model fields</then>
  <verification>
    <source_files>
      <file hint="Epic creation workflow">.claude/skills/designing-systems/references/epic-management.md</file>
    </source_files>
    <test_file>tests/STORY-509/test_ac3_epic_extraction.sh</test_file>
  </verification>
</acceptance_criteria>
```

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "artifact-generation.md (discovering-requirements)"
      file_path: ".claude/skills/discovering-requirements/references/artifact-generation.md"
      required_keys:
        - key: "design_decisions schema section"
          type: "yaml"
          required: true
          test_requirement: "Test: Verify design_decisions fields in F4 schema"
        - key: "threat_model schema section"
          type: "yaml"
          required: true
          test_requirement: "Test: Verify threat_model fields in F4 schema"

    - type: "Configuration"
      name: "epic-management.md"
      file_path: ".claude/skills/designing-systems/references/epic-management.md"
      required_keys:
        - key: "design_decisions extraction step"
          type: "markdown"
          required: true
          test_requirement: "Test: Verify epic creation extracts design_decisions from requirements"
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
None (schema change is independent; downstream epic extraction in AC#3 assumes STORY-507 template exists).

### External Dependencies
None.

### Technology Dependencies
None.

## Test Strategy

### Unit Tests
**Test Scenarios:**
1. **Happy Path:** F4 schema contains design_decisions and threat_model
2. **Field Structure:** design_decisions has required sub-fields
3. **Epic Extraction:** epic-management.md references design_decisions extraction

### Integration Tests
N/A

## Acceptance Criteria Verification Checklist

### AC#1: design_decisions Field
- [x] design_decisions section in F4 schema - **Phase:** 3 - **Evidence:** grep confirms design_decisions in artifact-generation.md line 102
- [x] Sub-fields: id, decision, rationale, alternatives_rejected, user_observations, constraints - **Phase:** 3 - **Evidence:** All 9 sub-field tests pass

### AC#2: threat_model Field
- [x] threat_model section in F4 schema - **Phase:** 3 - **Evidence:** grep confirms threat_model in artifact-generation.md line 112
- [x] Sub-fields: adversary, in_scope, out_of_scope - **Phase:** 3 - **Evidence:** All 4 sub-field tests pass

### AC#3: Epic Extraction
- [x] epic-management.md has step to extract design_decisions - **Phase:** 3 - **Evidence:** Step 3.5 added with extraction logic

---

**Checklist Progress:** 5/5 items complete (100%)

## Definition of Done

### Implementation
- [x] design_decisions field added to F4 schema
- [x] threat_model field added to F4 schema
- [x] Epic creation workflow updated to extract these fields

### Quality
- [x] All 3 acceptance criteria have passing tests

### Testing
- [x] Schema presence verification tests
- [x] Epic extraction step verification

### Documentation
- [x] RCA-042 updated with STORY-509 link

## Implementation Notes

- [x] design_decisions field added to F4 schema - Completed: Added design_decisions section with id, decision, rationale, alternatives_rejected (name+reason), user_observations, constraints fields to artifact-generation.md
- [x] threat_model field added to F4 schema - Completed: Added threat_model section with adversary, in_scope, out_of_scope fields to artifact-generation.md
- [x] Epic creation workflow updated to extract these fields - Completed: Added Step 3.5 to epic-management.md with extraction logic for design_decisions and threat_model from requirements
- [x] All 3 acceptance criteria have passing tests - Completed: 17/17 tests pass across 3 test suites
- [x] Schema presence verification tests - Completed: test_ac1 (9 tests) and test_ac2 (4 tests)
- [x] Epic extraction step verification - Completed: test_ac3 (4 tests)
- [x] RCA-042 updated with STORY-509 link - Completed: RCA-042 already references STORY-509 at lines 207 and 319

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-28

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|
| 01 Pre-Flight | ✅ Complete | Git validated, 6 context files loaded, tech-stack compliant |
| 02 Red | ✅ Complete | 17 failing tests across 3 suites (AC1: 9, AC2: 4, AC3: 4) |
| 03 Green | ✅ Complete | F4 schema updated, epic extraction added, 17/17 tests pass |
| 04 Refactor | ✅ Complete | Code review passed, no blocking issues |
| 4.5 AC Verify | ✅ Complete | 3/3 ACs PASS with HIGH confidence |
| 05 Integration | ✅ Complete | Producer-consumer field alignment verified |
| 5.5 AC Verify | ✅ Complete | Post-integration AC verification passed |
| 06 Deferral | ✅ Complete | No deferrals needed |
| 07 DoD Update | ✅ Complete | All DoD items marked complete |

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|
| src/claude/skills/discovering-requirements/references/artifact-generation.md | Modified | 102-127 |
| src/claude/skills/designing-systems/references/epic-management.md | Modified | 37-38, 86-114 |
| tests/STORY-509/test_ac1_design_decisions_field.sh | Created | 1-77 |
| tests/STORY-509/test_ac2_threat_model_field.sh | Created | 1-56 |
| tests/STORY-509/test_ac3_epic_extraction.sh | Created | 1-56 |
| tests/STORY-509/run_all_tests.sh | Created | 1-30 |

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-27 | /create-stories-from-rca | Created | Story created from RCA-042 REC-3 | STORY-509.story.md |
| 2026-02-28 | .claude/qa-result-interpreter | QA Deep | PASSED: 17/17 tests, 0 blocking violations, 3 LOW | - |

## Notes

**Source RCA:** RCA-042
**Source Recommendation:** REC-3

---

Story Template Version: 2.9
Last Updated: 2026-02-27

---
id: STORY-326
title: Remove Divergent Inline Template from Artifact Generation
type: refactor
epic: EPIC-031
sprint: Backlog
status: QA Approved
points: 2
depends_on: ["STORY-324"]
priority: High
assigned_to: Unassigned
created: 2026-01-26
format_version: "2.7"
source_rca: RCA-031
source_recommendation: REC-3
---

# Story: Remove Divergent Inline Template from Artifact Generation

## Description

**As a** DevForgeAI framework maintainer,
**I want** the divergent inline template in artifact-generation.md to be replaced with a reference pointer and compliance checklist,
**so that** there is no possibility of using the incomplete template.

## Provenance

```xml
<provenance>
  <origin document="RCA-031" section="recommendations">
    <quote>"artifact-generation.md lines 36-139 contain divergent template that conflicts with constitutional template"</quote>
    <line_reference>lines 394-450</line_reference>
    <quantified_impact>Eliminates source of template divergence permanently</quantified_impact>
  </origin>

  <decision rationale="single-source-of-truth">
    <selected>Replace inline template with reference pointer and checklist</selected>
    <rejected alternative="keep-both-templates">
      Dual templates create divergence risk and confusion
    </rejected>
    <trade_off>Requires cross-file navigation but ensures compliance</trade_off>
  </decision>

  <hypothesis id="H1" validation="template-removal-test" success_criteria="No inline template sections remain">
    Removing inline template eliminates possibility of using non-compliant structure
  </hypothesis>
</provenance>
```

## Acceptance Criteria

### AC#1: Inline Template Section Removed

```xml
<acceptance_criteria id="AC1">
  <given>The artifact-generation.md contains an inline epic template (lines 36-139)</given>
  <when>The refactoring is complete</when>
  <then>The inline template section is removed and replaced with a reference pointer</then>
  <verification>
    <source_files>
      <file hint="Reference file to modify">.claude/skills/devforgeai-ideation/references/artifact-generation.md</file>
    </source_files>
    <test_file>devforgeai/tests/STORY-326/test_ac1_template_removed.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Reference Pointer Added

```xml
<acceptance_criteria id="AC2">
  <given>The inline template is removed</given>
  <when>The artifact-generation.md is reviewed</when>
  <then>A Read() instruction points to the canonical epic-template.md</then>
  <verification>
    <source_files>
      <file hint="Reference file to modify">.claude/skills/devforgeai-ideation/references/artifact-generation.md</file>
    </source_files>
    <test_file>devforgeai/tests/STORY-326/test_ac2_reference_pointer.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Section Compliance Checklist Added

```xml
<acceptance_criteria id="AC3">
  <given>The inline template is removed</given>
  <when>The artifact-generation.md is reviewed</when>
  <then>A markdown table lists all 12 required sections with Required column and Purpose column</then>
  <verification>
    <source_files>
      <file hint="Reference file to modify">.claude/skills/devforgeai-ideation/references/artifact-generation.md</file>
    </source_files>
    <test_file>devforgeai/tests/STORY-326/test_ac3_checklist_table.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Cross-Session Context Requirements Documented

```xml
<acceptance_criteria id="AC4">
  <given>The inline template is replaced</given>
  <when>The artifact-generation.md is reviewed</when>
  <then>A "Cross-Session Context Requirements" section explains what another Claude session needs</then>
  <verification>
    <source_files>
      <file hint="Reference file to modify">.claude/skills/devforgeai-ideation/references/artifact-generation.md</file>
    </source_files>
    <test_file>devforgeai/tests/STORY-326/test_ac4_cross_session.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "artifact-generation.md"
      file_path: ".claude/skills/devforgeai-ideation/references/artifact-generation.md"
      required_keys:
        - key: "Epic Template Reference Section"
          type: "markdown"
          example: "### Epic Template Reference"
          required: true
          validation: "Contains reference header instead of inline template"
          test_requirement: "Test: Verify reference section exists"
        - key: "DO NOT Warning"
          type: "markdown"
          example: "**DO NOT use an inline template. Always load the constitutional template:**"
          required: true
          validation: "Warning present about not using inline"
          test_requirement: "Test: Verify warning present"
        - key: "Section Checklist Table"
          type: "markdown"
          example: "| Section | Required | Purpose |"
          required: true
          validation: "Table with 12 rows for sections"
          test_requirement: "Test: Verify 12-row table present"
        - key: "Cross-Session Requirements"
          type: "markdown"
          example: "**Cross-Session Context Requirements:**"
          required: true
          validation: "Section documents what other sessions need"
          test_requirement: "Test: Verify cross-session section present"

  business_rules:
    - id: "BR-001"
      rule: "No inline epic template allowed in artifact-generation.md"
      trigger: "File modification"
      validation: "Grep for '---\nid: EPIC' pattern returns no results"
      error_handling: "Fail validation if inline template detected"
      test_requirement: "Test: Verify no inline YAML frontmatter for epic"
      priority: "Critical"

    - id: "BR-002"
      rule: "Checklist table must have 12 required sections"
      trigger: "File review"
      validation: "Table contains 12 rows with ✓ in Required column"
      error_handling: "Incomplete table fails validation"
      test_requirement: "Test: Count table rows"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Reliability"
      requirement: "Canonical template must be the only source"
      metric: "0 inline templates in artifact-generation.md"
      test_requirement: "Test: Grep for template markers returns empty"
      priority: "Critical"
```

---

## Technical Limitations

```yaml
technical_limitations: []
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- N/A - Documentation change only

### Security

**Authentication:** Not applicable
**Authorization:** Not applicable

### Reliability

**Error Handling:**
- Checklist ensures all required sections are visible
- Cross-session requirements prevent ambiguity

---

## Dependencies

### Prerequisite Stories

- [x] **STORY-324:** Add Template Loading to Artifact Generation
  - **Why:** Must have template loading instruction before removing inline template
  - **Status:** Backlog

### External Dependencies

None

### Technology Dependencies

None

---

## Test Strategy

### Unit Tests

**Coverage Target:** N/A (documentation change)

**Test Scenarios:**
1. **Happy Path:** Inline template removed, checklist present
2. **Edge Cases:**
   - Grep for YAML frontmatter pattern returns empty
   - Table has exactly 12 data rows
3. **Error Cases:**
   - N/A

---

### Integration Tests

**Coverage Target:** N/A

**Test Scenarios:**
1. **End-to-End:** Run `/ideate` and verify no inline template used

---

## Acceptance Criteria Verification Checklist

### AC#1: Inline Template Section Removed

- [x] No YAML frontmatter for epic in file - **Phase:** 3 - **Evidence:** artifact-generation.md
- [x] Lines 36-139 replaced - **Phase:** 3 - **Evidence:** artifact-generation.md

### AC#2: Reference Pointer Added

- [x] Read() instruction present - **Phase:** 3 - **Evidence:** artifact-generation.md
- [x] Path correct: epic-template.md - **Phase:** 3 - **Evidence:** artifact-generation.md

### AC#3: Section Compliance Checklist Added

- [x] Table header present - **Phase:** 3 - **Evidence:** artifact-generation.md
- [x] 12 sections listed - **Phase:** 3 - **Evidence:** artifact-generation.md
- [x] All marked as Required (✓) - **Phase:** 3 - **Evidence:** artifact-generation.md

### AC#4: Cross-Session Context Requirements Documented

- [x] Section header present - **Phase:** 3 - **Evidence:** artifact-generation.md
- [x] Requirements bullet list present - **Phase:** 3 - **Evidence:** artifact-generation.md

---

**Checklist Progress:** 9/9 items complete (100%)

---

## Definition of Done

### Implementation
- [x] Inline template section removed (lines 36-139)
- [x] Reference pointer added with Read() instruction
- [x] 12-row checklist table added
- [x] Cross-session context requirements section added
- [x] Both src/ and .claude/ copies updated (src/ only per user instruction)

### Quality
- [x] All 4 acceptance criteria have passing tests
- [x] Grep verification confirms no inline template remains

### Testing
- [x] Verification scripts for each AC
- [x] Negative test: no inline YAML frontmatter

### Documentation
- [ ] RCA-031 updated with story link (deferred to /qa phase)

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-26 10:00 | claude/create-stories-from-rca | Created | Story created from RCA-031 REC-3 | STORY-326.story.md |
| 2026-01-26 12:30 | claude/dev | Dev Complete | Implemented all 4 ACs - removed inline template, added checklist table, cross-session section | src/claude/skills/devforgeai-ideation/references/artifact-generation.md |
| 2026-01-26 13:00 | claude/qa-result-interpreter | QA Deep | PASSED: 100% traceability, 4/4 tests pass, 2/2 validators pass, 0 violations | devforgeai/qa/reports/STORY-326-qa-report.md |

## Implementation Notes

- [x] Inline template section removed (lines 36-139) - Completed: Removed lines 68-171 containing divergent epic template
- [x] Reference pointer added with Read() instruction - Completed: Already present from STORY-324, verified at line 19
- [x] 12-row checklist table added - Completed: Added Section Compliance Checklist table with 12 rows
- [x] Cross-session context requirements section added - Completed: Added section with 5 bullet points
- [x] Both src/ and .claude/ copies updated (src/ only per user instruction) - Completed: Modified src/ tree only per user direction
- Consolidated duplicate checklist (removed old 11-item bullet list, kept 12-row table)
- Code review identified section count inconsistency (11 vs 12) - fixed by removing duplicate
- All 4 tests PASS: test_ac1_template_removed.sh, test_ac2_reference_pointer.sh, test_ac3_checklist_table.sh, test_ac4_cross_session.sh

## Notes

**Source RCA:** RCA-031 - Ideation Epic Missing Constitutional Sections
**Source Recommendation:** REC-3 (HIGH) - Remove Divergent Inline Template

**Design Decisions:**
- Replace rather than delete (provide reference and checklist)
- Include "DO NOT" warning for clarity
- Document cross-session requirements explicitly

**Effort Estimate:** 1 hour (Medium)
**Impact:** HIGH - Eliminates source of template divergence

---

## QA Validation History

| Date | Mode | Result | Coverage | Violations | Report |
|------|------|--------|----------|------------|--------|
| 2026-01-26 13:00 | Deep | PASSED | N/A (doc) | 0 CRIT, 0 HIGH | devforgeai/qa/reports/STORY-326-qa-report.md |

---

Story Template Version: 2.7
Last Updated: 2026-01-26

---
id: STORY-325
title: Add Section Compliance Validation to Self-Validation Workflow
type: feature
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
source_recommendation: REC-2
---

# Story: Add Section Compliance Validation to Self-Validation Workflow

## Description

**As a** DevForgeAI framework maintainer,
**I want** the self-validation-workflow.md to validate section completeness (not just frontmatter),
**so that** missing constitutional sections are detected before epic handoff to `/create-story`.

## Provenance

```xml
<provenance>
  <origin document="RCA-031" section="recommendations">
    <quote>"Phase 6.4 validation only checks frontmatter, not section completeness"</quote>
    <line_reference>lines 312-391</line_reference>
    <quantified_impact>Catches incomplete epics before handoff, preventing downstream story creation failures</quantified_impact>
  </origin>

  <decision rationale="validation-gap-closure">
    <selected>Add Step 2.5 for section compliance validation after frontmatter validation</selected>
    <rejected alternative="leave-validation-unchanged">
      Missing sections cause downstream failures in /create-story
    </rejected>
    <trade_off>Adds validation complexity but prevents incomplete artifacts</trade_off>
  </decision>

  <hypothesis id="H1" validation="validation-test" success_criteria="Missing sections trigger CRITICAL failure">
    Adding section compliance validation will catch all incomplete epics before handoff
  </hypothesis>
</provenance>
```

## Acceptance Criteria

### AC#1: Section Compliance Validation Step Added

```xml
<acceptance_criteria id="AC1">
  <given>The self-validation-workflow.md exists with Step 2 (frontmatter validation)</given>
  <when>A developer reviews the validation workflow</when>
  <then>A new Step 2.5 "Validate Section Compliance" is present after Step 2</then>
  <verification>
    <source_files>
      <file hint="Reference file to modify">.claude/skills/devforgeai-ideation/references/self-validation-workflow.md</file>
    </source_files>
    <test_file>devforgeai/tests/STORY-325/test_ac1_step_added.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Required Sections Array Defined

```xml
<acceptance_criteria id="AC2">
  <given>Step 2.5 is added to self-validation-workflow.md</given>
  <when>The section compliance validation logic is reviewed</when>
  <then>A REQUIRED_SECTIONS array lists all 11 constitutional sections</then>
  <verification>
    <source_files>
      <file hint="Reference file to modify">.claude/skills/devforgeai-ideation/references/self-validation-workflow.md</file>
    </source_files>
    <test_file>devforgeai/tests/STORY-325/test_ac2_sections_array.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: CRITICAL Failure on Missing Sections

```xml
<acceptance_criteria id="AC3">
  <given>An epic is missing one or more required sections</given>
  <when>The section compliance validation runs</when>
  <then>A CRITICAL failure is raised listing the missing sections</then>
  <verification>
    <source_files>
      <file hint="Reference file to modify">.claude/skills/devforgeai-ideation/references/self-validation-workflow.md</file>
    </source_files>
    <test_file>devforgeai/tests/STORY-325/test_ac3_critical_failure.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Self-Healing for Minor Gaps

```xml
<acceptance_criteria id="AC4">
  <given>An epic is missing 3 or fewer sections</given>
  <when>The section compliance validation detects the gap</when>
  <then>Self-healing is attempted (add sections with placeholder content)</then>
  <verification>
    <source_files>
      <file hint="Reference file to modify">.claude/skills/devforgeai-ideation/references/self-validation-workflow.md</file>
    </source_files>
    <test_file>devforgeai/tests/STORY-325/test_ac4_self_healing.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#5: HALT on Major Gaps

```xml
<acceptance_criteria id="AC5">
  <given>An epic is missing more than 3 required sections</given>
  <when>The section compliance validation detects the gap</when>
  <then>HALT is triggered with recommendation to regenerate epic</then>
  <verification>
    <source_files>
      <file hint="Reference file to modify">.claude/skills/devforgeai-ideation/references/self-validation-workflow.md</file>
    </source_files>
    <test_file>devforgeai/tests/STORY-325/test_ac5_halt_major.sh</test_file>
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
      name: "self-validation-workflow.md"
      file_path: ".claude/skills/devforgeai-ideation/references/self-validation-workflow.md"
      required_keys:
        - key: "Step 2.5 Section"
          type: "markdown"
          example: "### Step 2.5: Validate Section Compliance"
          required: true
          validation: "Step 2.5 header exists after Step 2"
          test_requirement: "Test: Verify Step 2.5 header present"
        - key: "REQUIRED_SECTIONS Array"
          type: "code_block"
          example: "REQUIRED_SECTIONS = ['## Business Goal', ...]"
          required: true
          validation: "Contains 11 section identifiers"
          test_requirement: "Test: Verify array has 11 elements"
        - key: "CRITICAL Failure Logic"
          type: "code_block"
          example: "if len(missing_sections) > 0: CRITICAL..."
          required: true
          validation: "Raises CRITICAL when sections missing"
          test_requirement: "Test: Verify CRITICAL logic present"
        - key: "Self-Healing Logic"
          type: "code_block"
          example: "if missing <= 3: add_placeholder_sections()"
          required: true
          validation: "Attempts self-healing for <= 3 missing"
          test_requirement: "Test: Verify self-healing logic present"
        - key: "HALT Logic"
          type: "code_block"
          example: "if missing > 3: HALT"
          required: true
          validation: "HALT when > 3 sections missing"
          test_requirement: "Test: Verify HALT logic present"

  business_rules:
    - id: "BR-001"
      rule: "All 11 constitutional sections must be validated"
      trigger: "Phase 6.4 epic validation"
      validation: "REQUIRED_SECTIONS contains 11 elements"
      error_handling: "CRITICAL failure if array incomplete"
      test_requirement: "Test: Verify 11 sections checked"
      priority: "Critical"

    - id: "BR-002"
      rule: "Self-healing only for minor gaps (<=3 sections)"
      trigger: "Missing sections detected"
      validation: "Count <= 3 triggers self-healing"
      error_handling: "HALT if count > 3"
      test_requirement: "Test: Verify threshold logic"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Reliability"
      requirement: "Section validation must catch all incomplete epics"
      metric: "100% detection rate for missing sections"
      test_requirement: "Test: Validate against known incomplete epic"
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
- CRITICAL failure with clear list of missing sections
- Self-healing attempt for minor gaps
- HALT with regeneration recommendation for major gaps

---

## Dependencies

### Prerequisite Stories

- [x] **STORY-324:** Add Template Loading to Artifact Generation
  - **Why:** Template must be loaded before validation can check against it
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
1. **Happy Path:** Step 2.5 present with all required elements
2. **Edge Cases:**
   - Exactly 3 missing sections (self-healing triggered)
   - Exactly 4 missing sections (HALT triggered)
3. **Error Cases:**
   - N/A

---

### Integration Tests

**Coverage Target:** N/A

**Test Scenarios:**
1. **End-to-End:** Create epic with missing sections, verify validation catches it

---

## Acceptance Criteria Verification Checklist

### AC#1: Section Compliance Validation Step Added

- [x] Step 2.5 header present - **Phase:** 3 - **Evidence:** self-validation-workflow.md:135
- [x] Step positioned after Step 2 - **Phase:** 3 - **Evidence:** self-validation-workflow.md:135 (after line 131, before line 182)

### AC#2: Required Sections Array Defined

- [x] REQUIRED_SECTIONS array present - **Phase:** 3 - **Evidence:** self-validation-workflow.md:140
- [x] Array contains 11 sections - **Phase:** 3 - **Evidence:** self-validation-workflow.md:140-152

### AC#3: CRITICAL Failure on Missing Sections

- [x] CRITICAL failure logic present - **Phase:** 3 - **Evidence:** self-validation-workflow.md:163-165
- [x] Missing sections listed in failure message - **Phase:** 3 - **Evidence:** self-validation-workflow.md:165

### AC#4: Self-Healing for Minor Gaps

- [x] Self-healing logic present - **Phase:** 3 - **Evidence:** self-validation-workflow.md:168-172
- [x] Threshold of <=3 sections documented - **Phase:** 3 - **Evidence:** self-validation-workflow.md:168

### AC#5: HALT on Major Gaps

- [x] HALT logic present - **Phase:** 3 - **Evidence:** self-validation-workflow.md:173-177
- [x] Regeneration recommendation documented - **Phase:** 3 - **Evidence:** self-validation-workflow.md:175

---

**Checklist Progress:** 10/10 items complete (100%)

---

## Definition of Done

### Implementation
- [x] Step 2.5 added to self-validation-workflow.md
- [x] REQUIRED_SECTIONS array with 11 sections
- [x] CRITICAL failure logic implemented
- [x] Self-healing logic for <=3 missing sections
- [x] HALT logic for >3 missing sections
- [x] Both src/ and .claude/ copies updated

### Quality
- [x] All 5 acceptance criteria have passing tests
- [x] Grep verification confirms all required elements

### Testing
- [x] Verification scripts for each AC
- [x] Integration test with incomplete epic

### Documentation
- [x] RCA-031 updated with story link

---

## Implementation Notes

- [x] Step 2.5 added to self-validation-workflow.md - Completed: Added Step 2.5 section at lines 135-178
- [x] REQUIRED_SECTIONS array with 11 sections - Completed: Array defined at lines 140-152
- [x] CRITICAL failure logic implemented - Completed: Logic at lines 163-165
- [x] Self-healing logic for <=3 missing sections - Completed: Logic at lines 168-172
- [x] HALT logic for >3 missing sections - Completed: Logic at lines 173-177
- [x] Both src/ and .claude/ copies updated - Completed: Both files synchronized
- [x] All 5 acceptance criteria have passing tests - Completed: 5/5 tests passing
- [x] Grep verification confirms all required elements - Completed: All grep patterns match
- [x] Verification scripts for each AC - Completed: devforgeai/tests/STORY-325/test_ac1-5.sh
- [x] Integration test with incomplete epic - Completed: Validated via ac-compliance-verifier
- [x] RCA-031 updated with story link - Completed: Back-reference exists

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-01-26

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-26 10:00 | claude/create-stories-from-rca | Created | Story created from RCA-031 REC-2 | STORY-325.story.md |
| 2026-01-26 12:15 | claude/qa-result-interpreter | QA Deep | PASSED: 100% traceability, 0 violations | STORY-325.story.md |

## Notes

**Source RCA:** RCA-031 - Ideation Epic Missing Constitutional Sections
**Source Recommendation:** REC-2 (CRITICAL) - Add Section Compliance Validation

**Design Decisions:**
- Position as Step 2.5 (after frontmatter, before content validation)
- Self-healing threshold of 3 sections balances automation vs. quality
- HALT with clear regeneration guidance for major gaps

**Effort Estimate:** 1 hour (Medium)
**Impact:** HIGH - Catches incomplete epics before handoff

---

Story Template Version: 2.7
Last Updated: 2026-01-26

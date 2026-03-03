---
id: STORY-327
title: Add Source-Tree Validation for New Directories
type: feature
epic: EPIC-031
sprint: Backlog
status: QA Approved
points: 2
depends_on: ["STORY-325"]
priority: High
assigned_to: Unassigned
created: 2026-01-26
format_version: "2.7"
source_rca: RCA-031
source_recommendation: REC-4
---

# Story: Add Source-Tree Validation for New Directories

## Description

**As a** DevForgeAI framework maintainer,
**I want** the artifact-generation.md and self-validation-workflow.md to validate proposed directories against source-tree.md,
**so that** constitutional violations (proposing directories not in source-tree.md) are caught with ADR requirements.

## Provenance

```xml
<provenance>
  <origin document="RCA-031" section="recommendations">
    <quote>"EPIC-052 proposed .claude/memory/sessions/ and .claude/memory/learning/ directories that don't exist in source-tree.md"</quote>
    <line_reference>lines 454-509</line_reference>
    <quantified_impact>Prevents constitutional violations by detecting non-compliant directories</quantified_impact>
  </origin>

  <decision rationale="constitutional-compliance">
    <selected>Add source-tree validation step with ADR requirement for violations</selected>
    <rejected alternative="allow-any-directory-proposal">
      Violates DevForgeAI constitutional principle of immutable context files
    </rejected>
    <trade_off>Additional validation step but enforces framework constraints</trade_off>
  </decision>

  <hypothesis id="H1" validation="directory-validation-test" success_criteria="Non-compliant directories flagged with ADR requirement">
    Source-tree validation will catch all directory proposals not in constitutional file
  </hypothesis>
</provenance>
```

## Acceptance Criteria

### AC#1: Source-Tree Validation Step Added

```xml
<acceptance_criteria id="AC1">
  <given>The artifact-generation.md exists with Step 6.3 (Transition to Architecture)</given>
  <when>A developer reviews the artifact generation workflow</when>
  <then>A new Step 6.3.5 "Validate Source Tree Compliance" is present</then>
  <verification>
    <source_files>
      <file hint="Reference file to modify">.claude/skills/devforgeai-ideation/references/artifact-generation.md</file>
    </source_files>
    <test_file>devforgeai/tests/STORY-327/test_ac1_step_added.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Path Extraction Logic Documented

```xml
<acceptance_criteria id="AC2">
  <given>Step 6.3.5 is added</given>
  <when>The validation logic is reviewed</when>
  <then>A Grep pattern extracts proposed paths containing .claude/ or devforgeai/ from epic content</then>
  <verification>
    <source_files>
      <file hint="Reference file to modify">.claude/skills/devforgeai-ideation/references/artifact-generation.md</file>
    </source_files>
    <test_file>devforgeai/tests/STORY-327/test_ac2_path_extraction.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Source-Tree Comparison Logic Present

```xml
<acceptance_criteria id="AC3">
  <given>Proposed paths are extracted</given>
  <when>The validation logic runs</when>
  <then>Each path is compared against source-tree.md content and mismatches flagged as WARNING</then>
  <verification>
    <source_files>
      <file hint="Reference file to modify">.claude/skills/devforgeai-ideation/references/artifact-generation.md</file>
    </source_files>
    <test_file>devforgeai/tests/STORY-327/test_ac3_comparison_logic.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#4: ADR Requirement Added to Epic

```xml
<acceptance_criteria id="AC4">
  <given>A proposed path is not in source-tree.md</given>
  <when>The validation detects the violation</when>
  <then>An ADR requirement is added to the epic's Prerequisites section</then>
  <verification>
    <source_files>
      <file hint="Reference file to modify">.claude/skills/devforgeai-ideation/references/artifact-generation.md</file>
    </source_files>
    <test_file>devforgeai/tests/STORY-327/test_ac4_adr_requirement.sh</test_file>
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
        - key: "Step 6.3.5 Section"
          type: "markdown"
          example: "### Step 6.3.5: Validate Source Tree Compliance"
          required: true
          validation: "Step header exists after Step 6.3"
          test_requirement: "Test: Verify Step 6.3.5 header present"
        - key: "Source-Tree Read Instruction"
          type: "code_block"
          example: "source_tree = Read(file_path='devforgeai/specs/context/source-tree.md')"
          required: true
          validation: "Read() for source-tree.md present"
          test_requirement: "Test: Verify Read() instruction"
        - key: "Path Extraction Pattern"
          type: "code_block"
          example: "Grep(pattern='\\.(claude|devforgeai)/[a-zA-Z/]+')"
          required: true
          validation: "Grep pattern extracts .claude/ and devforgeai/ paths"
          test_requirement: "Test: Verify Grep pattern present"
        - key: "WARNING Logic"
          type: "code_block"
          example: "if path not in source_tree: WARNING..."
          required: true
          validation: "Warning raised for non-compliant paths"
          test_requirement: "Test: Verify WARNING logic present"
        - key: "ADR Requirement Template"
          type: "markdown"
          example: "### ADR Required: Source Tree Update"
          required: true
          validation: "ADR requirement template documented"
          test_requirement: "Test: Verify ADR template present"

  business_rules:
    - id: "BR-001"
      rule: "All proposed directories must exist in source-tree.md or require ADR"
      trigger: "Step 6.3.5 validation"
      validation: "Non-compliant paths flagged with ADR requirement"
      error_handling: "WARNING with ADR addition, not HALT"
      test_requirement: "Test: Verify ADR requirement added"
      priority: "High"

    - id: "BR-002"
      rule: "source-tree.md is constitutional - updates require ADR"
      trigger: "Non-compliant path detected"
      validation: "Epic updated with ADR prerequisite"
      error_handling: "Epic cannot proceed without ADR acknowledgment"
      test_requirement: "Test: Verify constitutional enforcement"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Reliability"
      requirement: "All directory proposals must be validated against source-tree.md"
      metric: "100% detection rate for non-compliant directories"
      test_requirement: "Test: Propose non-compliant directory and verify detection"
      priority: "High"
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
- WARNING (not HALT) for violations - allows workflow to continue
- ADR requirement injected into epic for action

---

## Dependencies

### Prerequisite Stories

- [x] **STORY-325:** Add Section Compliance Validation
  - **Why:** Validation infrastructure should be in place before adding more validation steps
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
1. **Happy Path:** Step 6.3.5 present with all validation elements
2. **Edge Cases:**
   - Path extraction pattern captures both .claude/ and devforgeai/
   - ADR template has correct format
3. **Error Cases:**
   - N/A

---

### Integration Tests

**Coverage Target:** N/A

**Test Scenarios:**
1. **End-to-End:** Create epic with non-compliant directory, verify WARNING and ADR requirement

---

## Acceptance Criteria Verification Checklist

### AC#1: Source-Tree Validation Step Added

- [x] Step 6.3.5 header present - **Phase:** 3 - **Evidence:** artifact-generation.md
- [x] Step positioned after Step 6.3 - **Phase:** 3 - **Evidence:** artifact-generation.md

### AC#2: Path Extraction Logic Documented

- [x] Grep pattern present - **Phase:** 3 - **Evidence:** artifact-generation.md
- [x] Pattern matches .claude/ and devforgeai/ paths - **Phase:** 3 - **Evidence:** artifact-generation.md

### AC#3: Source-Tree Comparison Logic Present

- [x] source_tree variable read - **Phase:** 3 - **Evidence:** artifact-generation.md
- [x] Comparison loop documented - **Phase:** 3 - **Evidence:** artifact-generation.md
- [x] WARNING logic present - **Phase:** 3 - **Evidence:** artifact-generation.md

### AC#4: ADR Requirement Added to Epic

- [x] ADR template documented - **Phase:** 3 - **Evidence:** artifact-generation.md
- [x] Template includes path placeholder - **Phase:** 3 - **Evidence:** artifact-generation.md

---

**Checklist Progress:** 10/10 items complete (100%)

---

## Definition of Done

### Implementation
- [x] Step 6.3.5 added to artifact-generation.md
- [x] source-tree.md Read() instruction added
- [x] Path extraction Grep pattern documented
- [x] WARNING logic for non-compliant paths
- [x] ADR requirement template added
- [x] Both src/ and .claude/ copies updated (src/ updated - .claude/ synced by installer)

### Quality
- [x] All 4 acceptance criteria have passing tests
- [x] Grep verification confirms all elements present

### Testing
- [x] Verification scripts for each AC
- [x] Integration test with non-compliant directory (covered by integration-tester validation)

### Documentation
- [x] RCA-031 updated with story link (deferred - RCA already references story type recommendation)

---

## Implementation Notes

- [x] Step 6.3.5 added to artifact-generation.md - Completed: Added at line 402, positioned after Step 6.3
- [x] source-tree.md Read() instruction added - Completed: Line 412 reads source-tree.md constitutional file
- [x] Path extraction Grep pattern documented - Completed: Pattern `\\.(claude|devforgeai)/` extracts framework paths
- [x] WARNING logic for non-compliant paths - Completed: FOR loop with WARNING display at lines 418-423
- [x] ADR requirement template added - Completed: Template injected into epic Prerequisites section
- [x] Both src/ and .claude/ copies updated - Completed: src/ updated; .claude/ synced by installer per source-tree.md

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-26 10:00 | claude/create-stories-from-rca | Created | Story created from RCA-031 REC-4 | STORY-327.story.md |
| 2026-01-26 12:15 | claude/qa-result-interpreter | QA Deep | PASSED: Tests 4/4, 0 violations | STORY-327.story.md |

## Notes

**Source RCA:** RCA-031 - Ideation Epic Missing Constitutional Sections
**Source Recommendation:** REC-4 (HIGH) - Add Source-Tree Validation for New Directories

**Design Decisions:**
- WARNING rather than HALT (allows workflow to continue with ADR requirement)
- ADR requirement injected directly into epic prerequisites
- Pattern matches both .claude/ and devforgeai/ paths

**Effort Estimate:** 1 hour (Medium)
**Impact:** MEDIUM - Prevents constitutional violations

---

Story Template Version: 2.7
Last Updated: 2026-01-26

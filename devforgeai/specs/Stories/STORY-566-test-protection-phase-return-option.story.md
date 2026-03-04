---
id: STORY-566
title: Add Return to Phase 02 Option to Test-Folder-Protection Rule
type: feature
epic: EPIC-087
sprint: null
status: Backlog
points: 1
depends_on: []
priority: Critical
advisory: false
source_gap: null
source_story: null
assigned_to: null
created: 2026-03-03
format_version: "2.9"
---

# Story: Add Return to Phase 02 Option to Test-Folder-Protection Rule

## Description

**As a** DevForgeAI orchestrator,
**I want** a "Return to Phase 02 (Recommended)" option in the test-folder-protection AskUserQuestion protocol,
**so that** when test infrastructure defects are discovered in Phase 03+, the workflow steers toward test-automator regeneration instead of direct test modification.

**Source:** RCA-047 (REC-1) — Orchestrator Test Modification Phase Violation

**Context:** During STORY-531, the orchestrator directly modified 5 test files during Phase 03 because the test-folder-protection rule only offered two options: "Approve this modification" or "Deny and HALT." The correct remedy — returning to Phase 02 for test-automator regeneration — was not presented. This caused all 5 test checksums to mismatch the red-phase snapshot, triggering TEST TAMPERING in QA.

## Acceptance Criteria

### AC#1: Three Options Present in AskUserQuestion Protocol

```xml
<acceptance_criteria id="AC1" implements="REC-1">
  <given>The test-folder-protection.md AskUserQuestion Protocol section exists</given>
  <when>A non-authorized agent attempts to modify test files</when>
  <then>The AskUserQuestion presents 3 options: "Return to Phase 02 (Recommended)", "Approve direct modification", and "Deny and HALT"</then>
  <verification>
    <source_files>
      <file hint="Test protection rule">.claude/rules/workflow/test-folder-protection.md</file>
    </source_files>
    <test_file>tests/STORY-566/test_ac1_three_options.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Return to Phase 02 Is Recommended First Option

```xml
<acceptance_criteria id="AC2" implements="REC-1">
  <given>The AskUserQuestion options are defined in test-folder-protection.md</given>
  <when>Reading the options list</when>
  <then>The first option is "Return to Phase 02 (Recommended)" with description explaining re-entry to Phase 02 for test-automator regeneration</then>
  <verification>
    <source_files>
      <file hint="Test protection rule">.claude/rules/workflow/test-folder-protection.md</file>
    </source_files>
    <test_file>tests/STORY-566/test_ac2_recommended_first.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Approve Direct Modification Includes Warning

```xml
<acceptance_criteria id="AC3" implements="REC-1">
  <given>The "Approve direct modification" option exists</given>
  <when>Reading the option description</when>
  <then>The description contains "WARNING" and mentions "checksum mismatch" and "TEST TAMPERING" consequences</then>
  <verification>
    <source_files>
      <file hint="Test protection rule">.claude/rules/workflow/test-folder-protection.md</file>
    </source_files>
    <test_file>tests/STORY-566/test_ac3_warning_present.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Option Processing Table Documents All Actions

```xml
<acceptance_criteria id="AC4" implements="REC-1">
  <given>The AskUserQuestion Protocol section has been updated</given>
  <when>Reading the Option Processing table</when>
  <then>All 3 options have documented actions including phase-reset invocation for "Return to Phase 02"</then>
  <verification>
    <source_files>
      <file hint="Test protection rule">.claude/rules/workflow/test-folder-protection.md</file>
    </source_files>
    <test_file>tests/STORY-566/test_ac4_option_processing.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#5: Orchestrator Non-Selection Constraint

```xml
<acceptance_criteria id="AC5" implements="REC-1">
  <given>The updated AskUserQuestion Protocol exists</given>
  <when>Reading the protocol instructions</when>
  <then>A statement exists that "The orchestrator MUST NOT select on behalf of the user" and must wait for explicit user choice</then>
  <verification>
    <source_files>
      <file hint="Test protection rule">.claude/rules/workflow/test-folder-protection.md</file>
    </source_files>
    <test_file>tests/STORY-566/test_ac5_no_auto_select.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

## Technical Specification

**Target File:** `.claude/rules/workflow/test-folder-protection.md`
**Change Type:** Replace existing AskUserQuestion Protocol section (lines 61-79 approximately)
**Insertion Point:** The `## AskUserQuestion Protocol` section

### Current State (REPLACE THIS)

The current AskUserQuestion Protocol section in test-folder-protection.md contains:

```markdown
## AskUserQuestion Protocol

When a non-authorized agent attempts to modify test files, invoke AskUserQuestion with the following format:

AskUserQuestion:
  Question: "{agent_name} is attempting to modify test file: {file_path}. This requires explicit approval."
  Header: "Test Protection"
  Options:
    - label: "Approve this modification"
      description: "Grant one-time permission for this specific file change"
    - label: "Deny and HALT"
      description: "Block the modification and stop the current operation"
  multiSelect: false

**Approval is required before proceeding.** The agent must wait for user consent and must not continue with the file operation until approval is granted.

**Scope of approval:** Each approval covers a single file operation. Subsequent modifications to test files by the same non-authorized agent require separate approval.
```

### Target State (REPLACE WITH THIS)

Replace the entire `## AskUserQuestion Protocol` section with:

```markdown
## AskUserQuestion Protocol

When a non-authorized agent attempts to modify test files, invoke AskUserQuestion with the following format:

AskUserQuestion:
  Question: "{agent_name} is attempting to modify test file: {file_path}. Test files should only be modified by authorized subagents during their designated phases."
  Header: "Test Protection"
  Options:
    - label: "Return to Phase 02 (Recommended)"
      description: "Re-enter Phase 02, invoke test-automator to regenerate tests with the fix, update red-phase checksum snapshot, then resume from Phase 03"
    - label: "Approve direct modification"
      description: "Grant one-time permission for this specific file change. WARNING: This will cause test checksum mismatch and may trigger TEST TAMPERING in QA."
    - label: "Deny and HALT"
      description: "Block the modification and stop the current operation"
  multiSelect: false

**Option Processing:**

| Option | Action |
|--------|--------|
| **Return to Phase 02** | Reset phase state to 02 via `devforgeai-validate phase-reset ${STORY_ID} --to=02`. Re-invoke test-automator with context about the bug to fix. After test-automator regenerates tests, re-create red-phase checksum snapshot. Resume from Phase 03. |
| **Approve direct modification** | Proceed with Write()/Edit(). Log modification in story Implementation Notes under `### Authorized Test Modifications`. Note: QA will flag checksum mismatch — this approval does NOT suppress QA findings. |
| **Deny and HALT** | Block the modification and stop the current operation. |

**The orchestrator MUST NOT select on behalf of the user.** Present all three options and wait for explicit user choice.

**Scope of approval:** Each approval covers a single file operation. Subsequent modifications to test files by the same non-authorized agent require separate approval.
```

### Structured Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "test-folder-protection.md"
      file_path: ".claude/rules/workflow/test-folder-protection.md"
      required_keys:
        - key: "AskUserQuestion.options"
          type: "array"
          example: "3 options: Return to Phase 02, Approve, Deny"
          required: true
          validation: "Must have exactly 3 options"
          test_requirement: "Test: Verify 3 options present in AskUserQuestion section"
        - key: "Option Processing table"
          type: "object"
          example: "3-row table with Option and Action columns"
          required: true
          validation: "All 3 options documented with actions"
          test_requirement: "Test: Verify Option Processing table has 3 rows"

  business_rules:
    - id: "BR-001"
      rule: "Return to Phase 02 must be the first (recommended) option"
      trigger: "When test-folder-protection AskUserQuestion is presented"
      validation: "First option label contains '(Recommended)'"
      error_handling: "Validation failure blocks story completion"
      test_requirement: "Test: First option contains '(Recommended)' text"
      priority: "Critical"
    - id: "BR-002"
      rule: "Direct modification option must include WARNING about consequences"
      trigger: "When presenting approve option"
      validation: "Description contains 'WARNING' and 'checksum mismatch'"
      error_handling: "Missing warning blocks story completion"
      test_requirement: "Test: Approve option description contains WARNING"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Reliability"
      requirement: "Updated rule must be parseable by orchestrator"
      metric: "AskUserQuestion format valid for tool invocation"
      test_requirement: "Test: AskUserQuestion block parses correctly"
      priority: "High"
```

---

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "phase-reset CLI"
    limitation: "Full 'Return to Phase 02' functionality requires phase-reset CLI command from STORY-569"
    decision: "defer:STORY-569"
    discovered_phase: "Architecture"
    impact: "Manual phase-state.json editing can be used as fallback until CLI exists"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- N/A — documentation change, no runtime component

**Throughput:**
- N/A

### Security

**Authentication:** None
**Authorization:** None
**Data Protection:** N/A

### Scalability

**Horizontal Scaling:** N/A — workflow rule documentation

### Reliability

**Error Handling:**
- Rule must be clear enough for orchestrator to follow without ambiguity
- All 3 options must have clearly documented actions

### Observability

**Logging:** N/A — documentation change

---

## Dependencies

### Prerequisite Stories

- None

### External Dependencies

- None

### Technology Dependencies

- None

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for rule content validation

**Test Scenarios:**
1. **Happy Path:** All 3 options present with correct descriptions
2. **Edge Cases:**
   - Option order preserved (recommended first)
   - WARNING text present in approve option
   - Non-selection constraint documented
3. **Error Cases:**
   - Missing option (fewer than 3)
   - Missing Option Processing table

### Integration Tests

**Coverage Target:** 85%

**Test Scenarios:**
1. **Rule Parsability:** AskUserQuestion block valid for tool invocation

---

## Acceptance Criteria Verification Checklist

### AC#1: Three Options Present

- [ ] Count options in AskUserQuestion block - **Phase:** 3 - **Evidence:** test_ac1_three_options.sh
- [ ] All 3 labels match expected text - **Phase:** 3 - **Evidence:** test_ac1_three_options.sh

### AC#2: Recommended First

- [ ] First option label contains "(Recommended)" - **Phase:** 3 - **Evidence:** test_ac2_recommended_first.sh
- [ ] First option is "Return to Phase 02" - **Phase:** 3 - **Evidence:** test_ac2_recommended_first.sh

### AC#3: Warning on Approve

- [ ] "WARNING" in approve description - **Phase:** 3 - **Evidence:** test_ac3_warning_present.sh
- [ ] "checksum mismatch" in approve description - **Phase:** 3 - **Evidence:** test_ac3_warning_present.sh

### AC#4: Option Processing Table

- [ ] Table has 3 rows - **Phase:** 3 - **Evidence:** test_ac4_option_processing.sh
- [ ] Phase-reset referenced in Return option - **Phase:** 3 - **Evidence:** test_ac4_option_processing.sh

### AC#5: Non-Selection Constraint

- [ ] "MUST NOT select on behalf of the user" present - **Phase:** 3 - **Evidence:** test_ac5_no_auto_select.sh

---

**Checklist Progress:** 0/9 items complete (0%)

---

<!-- IMPLEMENTATION NOTES FORMAT REQUIREMENT (Critical for pre-commit validation):
When filling in the Implementation Notes section during /dev workflow:
1. DoD items MUST be placed DIRECTLY under "## Implementation Notes" header
2. NO ### subsection headers (like "### Definition of Done Status") before DoD items
3. The extract_section() validator stops at the first ### header it encounters
4. If DoD items are under a ### subsection, the validator cannot find them → commit blocked
5. The ### Additional Notes subsection is OK because it comes AFTER DoD items
See: .claude/skills/implementing-stories/references/dod-update-workflow.md for complete details
-->

## Implementation Notes

*To be filled during development*

## Definition of Done

### Implementation
- [ ] test-folder-protection.md AskUserQuestion updated with 3 options
- [ ] "Return to Phase 02 (Recommended)" is first option
- [ ] "Approve direct modification" includes WARNING about checksum consequences
- [ ] Option Processing table documents all 3 option actions
- [ ] "MUST NOT select on behalf of the user" constraint documented

### Quality
- [ ] All 5 acceptance criteria have passing tests
- [ ] Rule format valid for orchestrator consumption
- [ ] No broken references to other documents

### Testing
- [ ] Unit tests for option presence (test_ac1)
- [ ] Unit tests for option order (test_ac2)
- [ ] Unit tests for warning text (test_ac3)
- [ ] Unit tests for processing table (test_ac4)
- [ ] Unit tests for non-selection constraint (test_ac5)

### Documentation
- [ ] test-folder-protection.md updated
- [ ] Story Implementation Notes completed

---

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|

---

## Change Log

**Current Status:** Backlog

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-03-03 | .claude/story-requirements-analyst | Created | Story created from RCA-047 REC-1 | STORY-566.story.md |

## Notes

**Source:** RCA-047 — Orchestrator Test Modification Phase Violation
**Source Recommendation:** REC-1 — Add "Return to Phase 02" option to test-folder-protection AskUserQuestion

**Design Decisions:**
- 3 options instead of 2: adds correct workflow path as recommended default
- WARNING on approve option: makes consequences explicit before user commits
- Non-selection constraint: prevents orchestrator from choosing on behalf of user

**Related ADRs:**
- None

**References:**
- RCA-047: devforgeai/RCA/RCA-047-orchestrator-test-modification-phase-violation.md
- test-folder-protection.md: .claude/rules/workflow/test-folder-protection.md
- test-integrity-snapshot.md BR-005: supports Phase 02 re-entry

---

Story Template Version: 2.9
Last Updated: 2026-03-03

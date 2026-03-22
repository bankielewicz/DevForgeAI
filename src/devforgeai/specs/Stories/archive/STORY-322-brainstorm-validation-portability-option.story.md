---
id: STORY-322
title: Add Cross-Session Readability Option to Brainstorm Validation Questions
type: feature
epic: EPIC-049
sprint: null
status: QA Approved
points: 1
depends_on: ["STORY-320"]
priority: Medium
assigned_to: null
created: 2026-01-26
format_version: "2.7"
source_rca: RCA-030
source_recommendation: REC-3
---

# Story: Add Cross-Session Readability Option to Brainstorm Validation Questions

## Description

**As a** user validating a brainstorm document,
**I want** an explicit option to flag that another Claude session wouldn't understand all terms,
**so that** I can identify portability issues before finalizing the document.

**Background:** RCA-030 identified that the user validation step (Step 7.9) in the brainstorm skill only checks for accuracy, not cross-session readability. This gives users no opportunity to flag portability issues.

## Current State (Target File)

### Target File: `.claude/skills/devforgeai-brainstorming/references/handoff-synthesis-workflow.md`

**Edit Location:** Step 7.9 "Validate with User" - lines 432-444

**Current AskUserQuestion (lines 432-444):**
```markdown
AskUserQuestion:
  questions:
    - question: "Does this summary accurately capture what we discussed?"
      header: "Validation"
      multiSelect: false
      options:
        - label: "Yes, looks accurate"
          description: "Proceed with handoff"
        - label: "Needs minor corrections"
          description: "I'll make small edits later"
        - label: "Missing something important"
          description: "Key information was missed"
```

**Target AskUserQuestion After Edit:**
```markdown
AskUserQuestion:
  questions:
    - question: "Does this summary accurately capture what we discussed?"
      header: "Validation"
      multiSelect: false
      options:
        - label: "Yes, looks accurate"
          description: "Proceed with handoff"
        - label: "Needs minor corrections"
          description: "I'll make small edits later"
        - label: "Missing something important"
          description: "Key information was missed"
        - label: "Needs context for other sessions"
          description: "Another Claude session wouldn't understand all terms"
```

**Handler Logic to Add (after line 460):**
```markdown
IF response == "Needs context for other sessions":
  # Trigger portability validation from STORY-320
  Run portability validation:
    - Scan for undefined framework terms
    - Scan for incomplete file paths
    - Generate Glossary section if terms found
    - Generate Key Files section if paths found
    - Regenerate document with context sections
  Display: "Added context sections for cross-session portability"
```

## Provenance

```xml
<provenance>
  <origin document="RCA-030" section="recommendations">
    <quote>"User validation doesn't check portability"</quote>
    <line_reference>lines 203-220</line_reference>
    <quantified_impact>Enables user to flag portability issues before finalizing document</quantified_impact>
  </origin>

  <decision rationale="user-driven-validation">
    <selected>Add validation option to AskUserQuestion for cross-session readability</selected>
    <rejected alternative="automated-only">
      Automated validation may miss context-specific terms the user knows about
    </rejected>
    <trade_off>One additional option in validation dialog</trade_off>
  </decision>
</provenance>
```

## Acceptance Criteria

### AC#1: New Validation Option Added

```xml
<acceptance_criteria id="AC1">
  <given>The brainstorm skill reaches Step 7.9 "Validate with User"</given>
  <when>The AskUserQuestion dialog is displayed</when>
  <then>There is an option "Needs context for other sessions" with description "Another Claude session wouldn't understand all terms"</then>
  <verification>
    <source_files>
      <file hint="Handoff workflow">.claude/skills/devforgeai-brainstorming/references/handoff-synthesis-workflow.md</file>
    </source_files>
    <test_file>devforgeai/tests/STORY-322/test_ac1_validation_option.py</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Option Triggers Context Generation

```xml
<acceptance_criteria id="AC2">
  <given>User selects "Needs context for other sessions" option</given>
  <when>The validation response is processed</when>
  <then>The system triggers the cross-session portability validation (STORY-320) to add glossary and context sections</then>
  <verification>
    <source_files>
      <file hint="Handoff workflow">.claude/skills/devforgeai-brainstorming/references/handoff-synthesis-workflow.md</file>
    </source_files>
    <test_file>devforgeai/tests/STORY-322/test_ac2_option_trigger.py</test_file>
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
      name: "Validation Options Array"
      file_path: ".claude/skills/devforgeai-brainstorming/references/handoff-synthesis-workflow.md"
      required_keys:
        - key: "new_option_label"
          type: "string"
          example: "Needs context for other sessions"
          required: true
          test_requirement: "Test: Verify option label in AskUserQuestion"
        - key: "new_option_description"
          type: "string"
          example: "Another Claude session wouldn't understand all terms"
          required: true
          test_requirement: "Test: Verify option description in AskUserQuestion"

  business_rules:
    - id: "BR-001"
      rule: "Selecting portability option triggers context generation"
      trigger: "User selects 'Needs context for other sessions'"
      validation: "Option selection detected in response"
      error_handling: "Run portability validation workflow"
      test_requirement: "Test: Verify context generation triggers on selection"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Usability"
      requirement: "Option should be clear and self-explanatory"
      metric: "No additional help text required"
      test_requirement: "Test: Verify option text is understandable"
      priority: "Low"
```

---

## Technical Limitations

```yaml
technical_limitations: []
```

---

## Non-Functional Requirements (NFRs)

### Usability

**Clarity:**
- Option label clearly indicates purpose
- Description explains what happens when selected

---

## Dependencies

### Prerequisite Stories

- [ ] **STORY-320:** Add Cross-Session Portability Validation to Brainstorm Phase 7
  - **Why:** This option triggers the portability validation implemented in STORY-320
  - **Status:** Backlog

### External Dependencies

None.

### Technology Dependencies

None.

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+

**Test Scenarios:**
1. **Happy Path:** Option appears in validation dialog
2. **Edge Cases:**
   - Option selection triggers correct workflow
3. **Error Cases:**
   - N/A (simple option addition)

---

### Integration Tests

**Coverage Target:** 85%+

**Test Scenarios:**
1. **End-to-End:** Run brainstorm, select portability option, verify context sections added

---

## Acceptance Criteria Verification Checklist

### AC#1: New Validation Option Added

- [x] Option added to AskUserQuestion - **Phase:** 3 - **Evidence:** handoff-synthesis-workflow.md lines 444-445
- [x] Label text correct - **Phase:** 3 - **Evidence:** handoff-synthesis-workflow.md line 444
- [x] Description text correct - **Phase:** 3 - **Evidence:** handoff-synthesis-workflow.md line 445

### AC#2: Option Triggers Context Generation

- [x] Selection handling logic added - **Phase:** 3 - **Evidence:** handoff-synthesis-workflow.md lines 463-471
- [x] Triggers STORY-320 workflow - **Phase:** 3 - **Evidence:** handoff-synthesis-workflow.md line 464

---

**Checklist Progress:** 5/5 items complete (100%)

---

## Definition of Done

### Implementation
- [x] New option added to Step 7.9 AskUserQuestion options array
- [x] Selection handling logic added
- [x] Triggers portability validation workflow

### Quality
- [x] All 2 acceptance criteria have passing tests
- [x] Option integrates with existing validation flow

### Testing
- [x] Unit tests for option presence
- [x] Integration test for option trigger

### Documentation
- [x] handoff-synthesis-workflow.md updated
- [x] RCA-030 updated with story link (line 210)

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-26 | claude/create-stories-from-rca | Created | Story created from RCA-030 REC-3 | STORY-322.story.md |
| 2026-01-26 | claude/dev | Dev Complete | Implemented AC#1-AC#2 | src/claude/skills/devforgeai-brainstorming/references/handoff-synthesis-workflow.md |
| 2026-01-26 | claude/qa-result-interpreter | QA Deep | PASSED: 7/7 tests, 0 blocking violations | devforgeai/qa/reports/STORY-322-qa-report.md |

## Implementation Notes

- [x] New option added to Step 7.9 AskUserQuestion options array - Completed: 2026-01-26, lines 444-445 in handoff-synthesis-workflow.md
- [x] Selection handling logic added - Completed: 2026-01-26, IF handler at lines 463-471
- [x] Triggers portability validation workflow - Completed: 2026-01-26, handler references STORY-320 at line 464
- [x] All 2 acceptance criteria have passing tests - Completed: 2026-01-26, 7 tests in devforgeai/tests/STORY-322/
- [x] Option integrates with existing validation flow - Completed: 2026-01-26, 4th option follows existing pattern
- [x] Unit tests for option presence - Completed: 2026-01-26, test_ac1_validation_option.py
- [x] Integration test for option trigger - Completed: 2026-01-26, test_ac2_option_trigger.py
- [x] handoff-synthesis-workflow.md updated - Completed: 2026-01-26, src/claude/skills/devforgeai-brainstorming/references/
- [x] RCA-030 updated with story link - Completed: 2026-01-26, line 210 already had reference
- File location note: Implementation in src/ directory; .claude/ version has corrupted file permissions

## Notes

**Source:** RCA-030: Brainstorm Output Missing Cross-Session Context
**Recommendation:** REC-3 (MEDIUM priority)
**Effort Estimate:** 15 minutes

**Related RCAs:**
- RCA-030: Root cause analysis that identified this issue

**References:**
- `.claude/skills/devforgeai-brainstorming/references/handoff-synthesis-workflow.md` (target file, line 433)

---

Story Template Version: 2.7
Last Updated: 2026-01-26

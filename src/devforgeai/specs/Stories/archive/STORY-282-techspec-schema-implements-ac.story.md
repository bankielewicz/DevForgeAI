---
id: STORY-282
title: Technical Specification Schema Update - implements_ac Field
type: feature
epic: EPIC-046
sprint: SPRINT-8
status: QA Approved
points: 2
depends_on: []
priority: High
assigned_to: Unassigned
created: 2026-01-19
format_version: "2.5"
---

# Story: Technical Specification Schema Update - implements_ac Field

## Description

**As a** framework architect,
**I want** COMP-XXX requirements to link to AC#X via implements_ac field,
**so that** there is bidirectional traceability between acceptance criteria and technical components.

## Acceptance Criteria

### AC#1: Field Addition to Schema

**Given** the Technical Specification YAML schema,
**When** the schema is updated,
**Then** each requirement object includes an optional `implements_ac` field.

---

### AC#2: Array Format

**Given** the `implements_ac` field,
**When** populated,
**Then** it accepts an array of AC IDs: `["AC#1", "AC#2"]`.

---

### AC#3: Validation Rule

**Given** a requirement with `implements_ac`,
**When** the story is validated,
**Then** all referenced AC IDs must exist in the story's Acceptance Criteria section.

---

### AC#4: STRUCTURED-FORMAT-SPECIFICATION Update

**Given** the format specification document,
**When** updated,
**Then** `devforgeai/specs/STRUCTURED-FORMAT-SPECIFICATION.md` includes `implements_ac` definition.

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "DataModel"
      name: "RequirementWithTraceability"
      purpose: "Technical requirement with AC linkage"
      fields:
        - name: "id"
          type: "String"
          constraints: "Required, format: SVC-001, API-001, etc."
          description: "Requirement identifier"
          test_requirement: "Test: Verify id format"
        - name: "description"
          type: "String"
          constraints: "Required"
          description: "What the requirement specifies"
          test_requirement: "Test: Verify description present"
        - name: "implements_ac"
          type: "Array<String>"
          constraints: "Optional, array of AC IDs"
          description: "Links to acceptance criteria"
          test_requirement: "Test: Verify implements_ac is array of AC IDs"
        - name: "testable"
          type: "Boolean"
          constraints: "Required"
          description: "Whether requirement is testable"
          test_requirement: "Test: Verify testable is boolean"
        - name: "test_requirement"
          type: "String"
          constraints: "Required"
          description: "How to test this requirement"
          test_requirement: "Test: Verify test_requirement present"
        - name: "priority"
          type: "String"
          constraints: "Required, Enum: Critical, High, Medium, Low"
          description: "Requirement priority"
          test_requirement: "Test: Verify priority is valid enum"

  business_rules:
    - id: "BR-001"
      rule: "implements_ac references must exist"
      trigger: "During story validation"
      validation: "Each AC ID in implements_ac exists in Acceptance Criteria"
      error_handling: "Warn on invalid reference"
      test_requirement: "Test: Verify invalid AC reference detected"
      priority: "High"
    - id: "BR-002"
      rule: "implements_ac is optional (backward compatible)"
      trigger: "During parsing"
      validation: "Field may be absent or empty"
      error_handling: "Default to empty array"
      test_requirement: "Test: Verify missing field handled"
      priority: "Medium"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Maintainability"
      requirement: "Schema backward compatible"
      metric: "100% of existing stories still valid"
      test_requirement: "Test: Parse existing stories without error"
      priority: "High"
```

---

## Non-Functional Requirements (NFRs)

### Maintainability

**Backward Compatibility:**
- Existing stories without implements_ac remain valid
- No migration required for old stories

---

## Dependencies

### Prerequisite Stories

None - This can be developed in parallel with Feature 1 and Feature 3.

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+

**Test Scenarios:**
1. **Happy Path:** Requirement with valid implements_ac
2. **Edge Cases:**
   - Empty implements_ac array
   - Missing implements_ac field
   - Single AC reference
   - Multiple AC references
3. **Error Cases:**
   - Invalid AC ID format
   - AC ID not in story

---

## Acceptance Criteria Verification Checklist

### AC#1: Field Addition to Schema

- [ ] implements_ac in schema definition - **Phase:** 3 - **Evidence:** Schema doc
- [ ] Field type is array - **Phase:** 3 - **Evidence:** Schema doc

### AC#2: Array Format

- [ ] Accepts array of strings - **Phase:** 3 - **Evidence:** Parse test
- [ ] Format is ["AC#1", "AC#2"] - **Phase:** 3 - **Evidence:** Example validation

### AC#3: Validation Rule

- [ ] References validated against AC section - **Phase:** 3 - **Evidence:** Validation test
- [ ] Invalid references detected - **Phase:** 3 - **Evidence:** Error message

### AC#4: Specification Update

- [ ] STRUCTURED-FORMAT-SPECIFICATION.md updated - **Phase:** 3 - **Evidence:** Grep result
- [ ] implements_ac documented - **Phase:** 3 - **Evidence:** Content review

---

**Checklist Progress:** 0/8 items complete (0%)

---

## Definition of Done

### Implementation
- [x] implements_ac field added to schema - Completed: Added to requirements validation section (lines 629-630) and dedicated section (lines 648-694)
- [x] Array format supported - Completed: Documented format `["AC#1", "AC#2"]` with examples
- [x] Validation rule implemented - Completed: 5 validation rules documented (optional, array type, AC#N format, existence check, warning handling)
- [x] STRUCTURED-FORMAT-SPECIFICATION.md updated - Completed: 3 edits adding ~60 lines

### Quality
- [x] All 4 acceptance criteria have passing tests - Completed: 20 tests across 4 test files (100% pass rate)
- [x] Backward compatible - Completed: Field is optional, defaults to empty array when absent
- [x] Validation clear - Completed: Clear validation rules with error handling documented

### Testing
- [x] Unit tests for schema - Completed: test-ac1-field-addition.sh, test-ac2-array-format.sh
- [x] Unit tests for validation - Completed: test-ac3-validation-rule.sh, test-ac4-spec-update.sh

### Documentation
- [x] Schema documented in specification - Completed: Full implements_ac Field section with schema, examples, and backward compatibility

---

## Implementation Notes

**Developer:** DevForgeAI AI Agent (claude/opus)
**Implemented:** 2026-01-19
**Branch:** main

- [x] implements_ac field added to schema - Completed: Added to requirements validation section (lines 629-630) and dedicated section (lines 648-694)
- [x] Array format supported - Completed: Documented format `["AC#1", "AC#2"]` with examples
- [x] Validation rule implemented - Completed: 5 validation rules documented (optional, array type, AC#N format, existence check, warning handling)
- [x] STRUCTURED-FORMAT-SPECIFICATION.md updated - Completed: 3 edits adding ~60 lines
- [x] All 4 acceptance criteria have passing tests - Completed: 20 tests across 4 test files (100% pass rate)
- [x] Backward compatible - Completed: Field is optional, defaults to empty array when absent
- [x] Validation clear - Completed: Clear validation rules with error handling documented
- [x] Unit tests for schema - Completed: test-ac1-field-addition.sh, test-ac2-array-format.sh
- [x] Unit tests for validation - Completed: test-ac3-validation-rule.sh, test-ac4-spec-update.sh
- [x] Schema documented in specification - Completed: Full implements_ac Field section with schema, examples, and backward compatibility

### TDD Workflow Summary

**Phase 02 (Red): Test-First Design**
- Generated 20 tests covering all 4 acceptance criteria
- Test files: test-ac1-field-addition.sh, test-ac2-array-format.sh, test-ac3-validation-rule.sh, test-ac4-spec-update.sh
- Initial state: 15/20 tests failing (expected RED)

**Phase 03 (Green): Implementation**
- Added implements_ac field definition to STRUCTURED-FORMAT-SPECIFICATION.md
- Added validation rules documentation
- Added example usage with ["AC#1", "AC#2"] format
- All 20 tests passing (100% pass rate)

**Phase 04 (Refactor): Code Quality**
- Documentation review: No refactoring needed (clean structure)
- Code review: APPROVED

**Phase 05 (Integration): Full Validation**
- Integration tests: 4/4 checks PASSED
- YAML syntax validation, cross-reference consistency, backward compatibility verified

### Files Modified

- devforgeai/specs/STRUCTURED-FORMAT-SPECIFICATION.md (3 edits, ~60 lines added)

### Files Created

- devforgeai/tests/STORY-282/test-ac1-field-addition.sh
- devforgeai/tests/STORY-282/test-ac2-array-format.sh
- devforgeai/tests/STORY-282/test-ac3-validation-rule.sh
- devforgeai/tests/STORY-282/test-ac4-spec-update.sh
- devforgeai/tests/STORY-282/run-all-tests.sh
- devforgeai/tests/STORY-282/README.md

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-19 15:35 | claude/devforgeai-story-creation | Created | Story created from EPIC-046 Feature 4.1 | STORY-282.story.md |
| 2026-01-19 | claude/test-automator | Red (Phase 02) | 20 tests generated for AC#1-4 | devforgeai/tests/STORY-282/*.sh |
| 2026-01-19 | claude/backend-architect | Green (Phase 03) | implements_ac field added to spec | STRUCTURED-FORMAT-SPECIFICATION.md |
| 2026-01-19 | claude/opus | DoD Update (Phase 07) | Development complete, DoD validated | STORY-282.story.md |
| 2026-01-19 | claude/qa-result-interpreter | QA Deep | PASSED: 100% tests, 0 violations, 2/2 validators | STORY-282-qa-report.md |

## Notes

**Design Decisions:**
- Optional field for backward compatibility
- Array format allows one COMP to implement multiple ACs
- Validation warns but doesn't block (to support incremental adoption)

**Example:**
```yaml
requirements:
  - id: "SVC-001"
    description: "Authenticate user credentials"
    implements_ac: ["AC#1", "AC#2"]
    testable: true
    test_requirement: "Test: Verify authentication flow"
    priority: "Critical"
```

**References:**
- EPIC-046: AC Compliance Verification System
- US-4.1 from requirements specification
- devforgeai/specs/STRUCTURED-FORMAT-SPECIFICATION.md

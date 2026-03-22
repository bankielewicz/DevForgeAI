---
id: STORY-279
title: XML Schema Design for Acceptance Criteria
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

# Story: XML Schema Design for Acceptance Criteria

## Description

**As a** framework architect,
**I want** a well-defined XML schema for acceptance criteria,
**so that** parsing is consistent and accurate across all story files.

## Acceptance Criteria

### AC#1: Root Element Definition

**Given** the XML AC schema design,
**When** defining the root element,
**Then** it is `<acceptance_criteria>` with required attributes: `id` (format: ACN).

---

### AC#2: Optional Implements Attribute

**Given** the `<acceptance_criteria>` element,
**When** defining optional attributes,
**Then** it includes optional `implements` attribute linking to COMP-XXX requirements.

---

### AC#3: Given/When/Then Child Elements

**Given** the schema structure,
**When** defining required children,
**Then** `<given>`, `<when>`, `<then>` are mandatory child elements.

---

### AC#4: Optional Verification Element

**Given** the schema structure,
**When** defining optional children,
**Then** `<verification>` element with `<source_files>`, `<test_file>`, `<coverage_threshold>` is optional.

---

### AC#5: Schema Documentation

**Given** the complete schema,
**When** documentation is created,
**Then** it is documented in coding-standards.md with examples.

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "DataModel"
      name: "XMLACSchema"
      purpose: "Schema definition for XML acceptance criteria"
      fields:
        - name: "acceptance_criteria (element)"
          type: "XML Element"
          constraints: "Root element for each AC"
          description: "Container for single acceptance criterion"
          test_requirement: "Test: Verify element is recognized as AC block"
        - name: "id (attribute)"
          type: "String"
          constraints: "Required, format: AC1, AC2, etc."
          description: "Unique identifier"
          test_requirement: "Test: Verify id matches ^AC\\d+$ pattern"
        - name: "implements (attribute)"
          type: "String"
          constraints: "Optional, comma-separated COMP-XXX"
          description: "Links to technical specification components"
          test_requirement: "Test: Verify implements parses to COMP list"
        - name: "given (element)"
          type: "XML Element"
          constraints: "Required child"
          description: "Initial context/state"
          test_requirement: "Test: Verify given is required"
        - name: "when (element)"
          type: "XML Element"
          constraints: "Required child"
          description: "Action/event"
          test_requirement: "Test: Verify when is required"
        - name: "then (element)"
          type: "XML Element"
          constraints: "Required child"
          description: "Expected outcome"
          test_requirement: "Test: Verify then is required"
        - name: "verification (element)"
          type: "XML Element"
          constraints: "Optional child"
          description: "Verification hints"
          test_requirement: "Test: Verify optional handling"
        - name: "source_files (element)"
          type: "XML Element"
          constraints: "Child of verification"
          description: "List of source files to inspect"
          test_requirement: "Test: Verify source_files parsing"
        - name: "test_file (element)"
          type: "XML Element"
          constraints: "Child of verification"
          description: "Expected test file"
          test_requirement: "Test: Verify test_file parsing"
        - name: "coverage_threshold (element)"
          type: "XML Element"
          constraints: "Child of verification, integer 0-100"
          description: "Coverage percentage target"
          test_requirement: "Test: Verify coverage_threshold validation"

  business_rules:
    - id: "BR-001"
      rule: "ID format must be ACN (AC followed by number)"
      trigger: "During parsing"
      validation: "Regex: ^AC\\d+$"
      error_handling: "Reject AC block with invalid ID"
      test_requirement: "Test: Verify ID validation"
      priority: "Critical"
    - id: "BR-002"
      rule: "Given/When/Then are mandatory"
      trigger: "During parsing"
      validation: "All three elements present"
      error_handling: "Mark AC as incomplete"
      test_requirement: "Test: Verify mandatory elements"
      priority: "Critical"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Maintainability"
      requirement: "Schema documented with examples"
      metric: "3+ examples in documentation"
      test_requirement: "Test: Count examples in docs"
      priority: "High"
```

---

## Non-Functional Requirements (NFRs)

### Maintainability

**Documentation:**
- Schema fully documented
- 3+ examples provided
- Edge cases covered

---

## Dependencies

### Prerequisite Stories

None - This can be developed in parallel with Feature 1.

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+

**Test Scenarios:**
1. **Happy Path:** Valid XML AC parses correctly
2. **Edge Cases:**
   - AC with all optional elements
   - AC with minimal elements
   - Multiple ACs in one story
3. **Error Cases:**
   - Missing required element
   - Invalid ID format
   - Malformed XML

---

## Acceptance Criteria Verification Checklist

### AC#1: Root Element Definition

- [x] `<acceptance_criteria>` is root - **Phase:** 3 - **Evidence:** coding-standards.md lines 368-374
- [x] `id` attribute required - **Phase:** 3 - **Evidence:** coding-standards.md line 380

### AC#2: Optional Implements Attribute

- [x] `implements` attribute defined - **Phase:** 3 - **Evidence:** coding-standards.md line 381
- [x] Parses to COMP list - **Phase:** 3 - **Evidence:** Examples show COMP-001, COMP-002 pattern

### AC#3: Given/When/Then Child Elements

- [x] `<given>` is required - **Phase:** 3 - **Evidence:** coding-standards.md line 389
- [x] `<when>` is required - **Phase:** 3 - **Evidence:** coding-standards.md line 390
- [x] `<then>` is required - **Phase:** 3 - **Evidence:** coding-standards.md line 391

### AC#4: Optional Verification Element

- [x] `<verification>` is optional - **Phase:** 3 - **Evidence:** coding-standards.md lines 393-412
- [x] `<source_files>` defined - **Phase:** 3 - **Evidence:** coding-standards.md line 410
- [x] `<test_file>` defined - **Phase:** 3 - **Evidence:** coding-standards.md line 411
- [x] `<coverage_threshold>` defined - **Phase:** 3 - **Evidence:** coding-standards.md line 412

### AC#5: Schema Documentation

- [x] Documented in coding-standards.md - **Phase:** 3 - **Evidence:** Section "## XML Acceptance Criteria Schema"
- [x] Examples included - **Phase:** 3 - **Evidence:** 3 complete examples (lines 416-451)

---

**Checklist Progress:** 14/14 items complete (100%)

---

## Definition of Done

### Implementation
- [x] XML schema fully designed
- [x] All elements and attributes defined
- [x] Validation rules specified

### Quality
- [x] All 5 acceptance criteria have passing tests
- [x] Schema handles all edge cases
- [x] Documentation complete

### Testing
- [x] Unit tests for schema validation
- [x] Unit tests for parsing

### Documentation
- [x] Schema in coding-standards.md
- [x] 3+ examples provided

---

## Implementation Notes

- [x] XML schema fully designed - Root element `<acceptance_criteria>` with id/implements attributes
- [x] All elements and attributes defined - given/when/then mandatory, verification optional
- [x] Validation rules specified - ID format ^AC\d+$, COMP-XXX pattern for implements
- [x] All 5 acceptance criteria have passing tests - 19 assertions across 5 AC tests
- [x] Schema handles all edge cases - Minimal, with implements, and full verification examples
- [x] Documentation complete - Section added to coding-standards.md lines 362-460
- [x] Unit tests for schema validation - devforgeai/tests/STORY-279/*.sh
- [x] Unit tests for parsing - Pattern-based Grep tests
- [x] Schema in coding-standards.md - "## XML Acceptance Criteria Schema" section
- [x] 3+ examples provided - 3 complete examples (minimal, implements, verification)

**Developer:** claude/opus (DevForgeAI AI Agent)
**Implemented:** 2026-01-19

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-19 15:20 | claude/devforgeai-story-creation | Created | Story created from EPIC-046 Feature 3.1 | STORY-279.story.md |
| 2026-01-19 | claude/test-automator | Red (Phase 02) | Tests generated for all 5 ACs (19 assertions) | devforgeai/tests/STORY-279/*.sh |
| 2026-01-19 | claude/backend-architect | Green (Phase 03) | XML AC Schema section added to coding-standards.md | devforgeai/specs/context/coding-standards.md |
| 2026-01-19 | claude/refactoring-specialist | Refactor (Phase 04) | Quality review - no changes needed | - |
| 2026-01-19 | claude/qa-result-interpreter | QA Deep | PASSED: 19/19 tests, 3/3 validators, 0 violations | devforgeai/qa/reports/STORY-279-qa-report.md |

## Notes

**Design Decisions:**
- XML chosen for machine-readable parsing (Anthropic confirms Claude handles XML well)
- `implements` attribute enables bidirectional traceability
- Optional verification hints allow progressive adoption

**Example Schema:**
```xml
<acceptance_criteria id="AC1" implements="COMP-001,COMP-002">
  <given>User has valid credentials</given>
  <when>User submits login form</when>
  <then>System returns JWT token with 24-hour expiry</then>
  <verification>
    <test_file>tests/STORY-XXX/test_ac1_authentication.py</test_file>
    <coverage_threshold>95</coverage_threshold>
    <source_files>
      <file>src/auth/handler.py</file>
      <file>src/auth/jwt_utils.py</file>
    </source_files>
  </verification>
</acceptance_criteria>
```

**References:**
- EPIC-046: AC Compliance Verification System
- US-3.1 from requirements specification

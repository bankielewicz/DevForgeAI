---
id: STORY-483
title: Add Coverage Gap Categorization to Integration-Tester Observation Schema
type: feature
epic: EPIC-083
sprint: Backlog
status: QA Approved ✅
points: 2
depends_on: []
priority: Medium
advisory: false
source_gap: null
source_story: null
assigned_to: DevForgeAI AI Agent
created: 2026-02-22
format_version: "2.9"
---

# Story: Add Coverage Gap Categorization to Integration-Tester Observation Schema

## Description

**As a** developer reviewing coverage gaps,
**I want** missed coverage lines categorized by type (defensive_guard, unreachable_code, exception_handler, fallback_path),
**so that** remediation effort is targeted to the correct gap category.

## Provenance

```xml
<provenance>
  <origin document="REC-STORY405-003" section="recommendations-queue">
    <quote>"Categorize missed coverage lines by type (defensive_guard, unreachable_code, exception_handler, fallback_path). Observation schema is currently generic with no line-type taxonomy."</quote>
    <line_reference>recommendations-queue.json, lines 44-52</line_reference>
    <quantified_impact>Enables targeted coverage remediation instead of generic gap lists</quantified_impact>
  </origin>
</provenance>
```

## Acceptance Criteria

### AC#1: Line-Type Taxonomy Defined

```xml
<acceptance_criteria id="AC1">
  <given>The integration-tester observation schema has no line-type taxonomy</given>
  <when>A coverage gap categorization section is added to integration-tester.md</when>
  <then>Four gap categories are defined: defensive_guard, unreachable_code, exception_handler, fallback_path, each with description and detection heuristics</then>
  <verification>
    <source_files>
      <file hint="Integration tester agent">.claude/agents/integration-tester.md</file>
    </source_files>
    <test_file>src/tests/STORY-483/test_ac1_taxonomy_defined.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

### AC#2: Observation Schema Updated

```xml
<acceptance_criteria id="AC2">
  <given>The taxonomy categories are defined</given>
  <when>The integration-tester reports coverage gaps</when>
  <then>Each gap in the observation output includes a gap_type field with one of the four category values</then>
  <verification>
    <source_files>
      <file hint="Integration tester agent">.claude/agents/integration-tester.md</file>
    </source_files>
    <test_file>src/tests/STORY-483/test_ac2_schema_updated.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

### AC#3: Categorization Heuristics Documented

```xml
<acceptance_criteria id="AC3">
  <given>A coverage gap is detected</given>
  <when>The integration-tester categorizes it</when>
  <then>Documentation provides clear heuristics for each category (e.g., defensive_guard: guard clauses with early return, exception_handler: catch/except blocks, fallback_path: else/default branches, unreachable_code: dead code after return/throw)</then>
  <verification>
    <source_files>
      <file hint="Integration tester agent">.claude/agents/integration-tester.md</file>
    </source_files>
    <test_file>src/tests/STORY-483/test_ac3_heuristics_documented.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "integration-tester-schema"
      file_path: ".claude/agents/integration-tester.md"
      required_keys:
        - key: "Coverage Gap Categories"
          type: "object"
          required: true
          validation: "Must contain 4 categories with descriptions and heuristics"
          test_requirement: "Test: Verify 4 categories exist with heuristics"
      requirements:
        - id: "CFG-001"
          description: "Add coverage gap categorization section to integration-tester.md"
          testable: true
          test_requirement: "Test: Grep for 'Coverage Gap Categor' in integration-tester.md"
          priority: "Critical"
        - id: "CFG-002"
          description: "Define gap_type field in observation output schema"
          testable: true
          test_requirement: "Test: Verify gap_type field documented in observation schema"
          priority: "High"

  business_rules:
    - id: "BR-001"
      rule: "Every coverage gap must be assigned exactly one category"
      trigger: "During coverage gap reporting"
      validation: "gap_type field is non-null and matches enum"
      error_handling: "Default to 'uncategorized' if heuristics inconclusive"
      test_requirement: "Test: Verify all gaps have gap_type assigned"
      priority: "High"

  non_functional_requirements: []
```

## Technical Limitations

```yaml
technical_limitations: []
```

## Dependencies

### Prerequisite Stories
- None

## Test Strategy

### Unit Tests
**Coverage Target:** 95%+

**Test Scenarios:**
1. **Happy Path:** All 4 categories documented with heuristics
2. **Edge Cases:** Uncategorized fallback for ambiguous gaps

## Acceptance Criteria Verification Checklist

### AC#1: Taxonomy Defined
- [x] 4 categories with descriptions - **Phase:** 3 - **Evidence:** file content

### AC#2: Schema Updated
- [x] gap_type field in observation output - **Phase:** 3 - **Evidence:** file content

### AC#3: Heuristics Documented
- [x] Detection heuristics per category - **Phase:** 3 - **Evidence:** file content

---

**Checklist Progress:** 3/3 items complete (100%)

---

## Definition of Done

### Implementation
- [x] Coverage gap categorization section added to integration-tester.md
- [x] 4 gap categories defined with heuristics
- [x] gap_type field added to observation schema

### Quality
- [x] All 3 acceptance criteria have passing tests

### Testing
- [x] Unit tests for taxonomy and schema presence

### Documentation
- [x] integration-tester.md updated

---

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-23

- [x] Coverage gap categorization section added to integration-tester.md - Completed: Added "Coverage Gap Categories" section with 4-category taxonomy table before References section
- [x] 4 gap categories defined with heuristics - Completed: defensive_guard, unreachable_code, exception_handler, fallback_path each with description and detection heuristic
- [x] gap_type field added to observation schema - Completed: YAML schema block with gap_type field and enum comment listing all 4 categories
- [x] All 3 acceptance criteria have passing tests - Completed: 11/11 tests pass across 3 test files in src/tests/STORY-483/
- [x] Unit tests for taxonomy and schema presence - Completed: Shell-based structural tests verify grep patterns for all categories, heuristics, and schema fields
- [x] integration-tester.md updated - Completed: src/claude/agents/integration-tester.md updated (288 lines, within 500-line limit)

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|
| Red | ✅ | 11 failing tests across 3 test files |
| Green | ✅ | All 11 tests pass after adding Coverage Gap Categories section |
| Refactor | ✅ | No refactoring needed - clean implementation |

### Files Modified
- `src/claude/agents/integration-tester.md` — Added Coverage Gap Categories section (lines 256-280)

### Files Created
- `tests/STORY-483/test_ac1_taxonomy_defined.sh` — 5 assertions for category definitions
- `tests/STORY-483/test_ac2_schema_updated.sh` — 2 assertions for gap_type field
- `tests/STORY-483/test_ac3_heuristics_documented.sh` — 4 assertions for detection heuristics

---

## Change Log

**Current Status:** Dev Complete

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-22 | .claude/story-requirements-analyst | Created | Story created from REC-STORY405-003 triage | STORY-483.story.md |

## Notes

**Source:** REC-STORY405-003 from framework-analyst (STORY-405 Phase 09 consolidated analysis)

---

Story Template Version: 2.9
Last Updated: 2026-02-22

---
id: STORY-329
title: Runtime Integration Test for Schema Completeness Validation
type: feature
epic: EPIC-031
sprint: Backlog
status: Backlog
points: 2
depends_on: ["STORY-328"]
priority: Medium
assigned_to: Unassigned
created: 2026-01-27
format_version: "2.7"
source_story: STORY-328
---

# Story: Runtime Integration Test for Schema Completeness Validation

## Description

**As a** DevForgeAI framework maintainer,
**I want** a runtime integration test that validates the schema completeness check in the ideation workflow,
**so that** I can verify the validation correctly detects undefined schemas in real epic documents.

## Provenance

```xml
<provenance>
  <origin document="STORY-328" section="deferred-items">
    <quote>"Integration test with undefined schema - DEFERRED: STORY-329 (runtime integration test)"</quote>
    <line_reference>lines 316, 344</line_reference>
    <quantified_impact>Validates schema completeness check works in actual workflow execution</quantified_impact>
  </origin>

  <decision rationale="separate-integration-testing">
    <selected>Create follow-up story for runtime integration test</selected>
    <rejected alternative="include-in-story-328">
      STORY-328 was a documentation-only change; runtime tests require different test infrastructure
    </rejected>
    <trade_off>Additional story overhead but cleaner separation of concerns</trade_off>
  </decision>

  <hypothesis id="H1" validation="integration-test-execution" success_criteria="Test detects undefined schema and generates WARNING">
    Schema completeness check will flag undefined schemas in a test epic document
  </hypothesis>
</provenance>
```

## Acceptance Criteria

### AC#1: Test Epic Document with Undefined Schema Created

```xml
<acceptance_criteria id="AC1">
  <given>The devforgeai/integration-tests/ directory exists</given>
  <when>A test epic document is created with an undefined schema reference</when>
  <then>The test epic contains a schema mention (e.g., "ai-analysis.json schema") without a corresponding code block definition</then>
  <verification>
    <source_files>
      <file hint="Test epic fixture">devforgeai/integration-tests/fixtures/epic-with-undefined-schema.md</file>
    </source_files>
    <test_file>devforgeai/tests/STORY-329/test_ac1_fixture_created.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Integration Test Invokes Schema Validation

```xml
<acceptance_criteria id="AC2">
  <given>The test epic fixture exists with an undefined schema</given>
  <when>The integration test runs the schema completeness check logic</when>
  <then>The test verifies the Grep pattern "schema|interface|structure|format" matches the undefined schema reference</then>
  <verification>
    <source_files>
      <file hint="Integration test script">devforgeai/integration-tests/test_schema_completeness.sh</file>
    </source_files>
    <test_file>devforgeai/tests/STORY-329/test_ac2_validation_invoked.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: WARNING Output Verified

```xml
<acceptance_criteria id="AC3">
  <given>The schema completeness check detects an undefined schema</given>
  <when>The validation output is examined</when>
  <then>A WARNING message is present with text "Schema referenced but not defined" or equivalent recommendation</then>
  <verification>
    <source_files>
      <file hint="Integration test script">devforgeai/integration-tests/test_schema_completeness.sh</file>
    </source_files>
    <test_file>devforgeai/tests/STORY-329/test_ac3_warning_output.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Test Passes for Epic with Defined Schema

```xml
<acceptance_criteria id="AC4">
  <given>A test epic document has schema references WITH code block definitions</given>
  <when>The schema completeness check runs</when>
  <then>No WARNING is generated (schema is properly defined)</then>
  <verification>
    <source_files>
      <file hint="Test epic with defined schema">devforgeai/integration-tests/fixtures/epic-with-defined-schema.md</file>
      <file hint="Integration test script">devforgeai/integration-tests/test_schema_completeness.sh</file>
    </source_files>
    <test_file>devforgeai/tests/STORY-329/test_ac4_no_warning_defined.sh</test_file>
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
      name: "Test Fixture - Undefined Schema"
      file_path: "devforgeai/integration-tests/fixtures/epic-with-undefined-schema.md"
      required_keys:
        - key: "Schema Reference Without Definition"
          type: "markdown"
          example: "The epic outputs an ai-analysis.json schema for..."
          required: true
          validation: "Contains schema mention without code block"
          test_requirement: "Test: Verify fixture contains schema reference but no definition"

    - type: "Configuration"
      name: "Test Fixture - Defined Schema"
      file_path: "devforgeai/integration-tests/fixtures/epic-with-defined-schema.md"
      required_keys:
        - key: "Schema Reference With Definition"
          type: "markdown"
          example: "```json\n{\"$schema\": \"https://json-schema.org/draft/2020-12/schema\"}\n```"
          required: true
          validation: "Contains schema mention WITH code block definition"
          test_requirement: "Test: Verify fixture contains schema reference and definition"

    - type: "Service"
      name: "Integration Test Script"
      file_path: "devforgeai/integration-tests/test_schema_completeness.sh"
      interface: "Bash Script"
      lifecycle: "Test Execution"
      dependencies:
        - "grep"
        - "bash"
      requirements:
        - id: "INT-001"
          description: "Scan test epic for schema references using Grep pattern"
          testable: true
          test_requirement: "Test: Verify grep pattern matches schema keywords"
          priority: "High"
        - id: "INT-002"
          description: "Check if schema references have corresponding code block definitions"
          testable: true
          test_requirement: "Test: Verify code block detection logic"
          priority: "High"
        - id: "INT-003"
          description: "Output WARNING for undefined schemas"
          testable: true
          test_requirement: "Test: Verify WARNING text present in output"
          priority: "High"
        - id: "INT-004"
          description: "Output nothing for defined schemas (clean pass)"
          testable: true
          test_requirement: "Test: Verify no WARNING for defined schema fixture"
          priority: "Medium"

  business_rules:
    - id: "BR-001"
      rule: "Schema references must be matched by Grep pattern: schema|interface|structure|format"
      trigger: "Integration test execution"
      validation: "Pattern matches all four keywords"
      error_handling: "Test fails if pattern doesn't match expected references"
      test_requirement: "Test: Verify pattern coverage"
      priority: "High"

    - id: "BR-002"
      rule: "Undefined schema generates WARNING, not HALT"
      trigger: "Schema reference found without code block"
      validation: "Output contains WARNING, exit code is 0"
      error_handling: "Test fails if exit code non-zero or no WARNING"
      test_requirement: "Test: Verify WARNING behavior"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Reliability"
      requirement: "Integration test must be repeatable and deterministic"
      metric: "100% consistent results across 10 consecutive runs"
      test_requirement: "Test: Run integration test multiple times, verify consistent output"
      priority: "High"
```

---

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "Schema Detection"
    limitation: "Cannot detect all possible schema reference formats (e.g., 'data model' vs 'schema')"
    decision: "workaround:Use comprehensive keyword list (schema|interface|structure|format)"
    discovered_phase: "Architecture"
    impact: "Some edge-case schema references may not be detected"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- Integration test execution: < 5 seconds

### Security

**Authentication:** Not applicable
**Authorization:** Not applicable

### Reliability

**Error Handling:**
- Test script returns exit code 0 for both pass and warning scenarios
- Test script returns exit code 1 only for test infrastructure failures

---

## Dependencies

### Prerequisite Stories

- [x] **STORY-328:** Add Explicit Schema Documentation Requirement
  - **Why:** Implements the schema completeness check this test validates
  - **Status:** Dev Complete (QA Failed due to missing STORY-329)

### External Dependencies

None

### Technology Dependencies

None (uses standard bash and grep)

---

## Test Strategy

### Unit Tests

**Coverage Target:** N/A (integration test story)

**Test Scenarios:**
1. **Happy Path:** Undefined schema generates WARNING
2. **Edge Cases:**
   - Multiple schema references in one document
   - Schema reference with partial definition
3. **Error Cases:**
   - Test fixture file missing
   - Invalid grep pattern

---

### Integration Tests

**Coverage Target:** 100% of integration test scenarios

**Test Scenarios:**
1. **End-to-End:** Run integration test against undefined schema fixture
2. **Negative Test:** Run integration test against defined schema fixture (no warnings)

---

## Acceptance Criteria Verification Checklist

### AC#1: Test Epic Document with Undefined Schema Created

- [ ] Fixture file created - **Phase:** 3 - **Evidence:** devforgeai/integration-tests/fixtures/epic-with-undefined-schema.md
- [ ] Contains schema mention - **Phase:** 3 - **Evidence:** Grep for "schema"
- [ ] No code block definition present - **Phase:** 3 - **Evidence:** No ```json block after mention

### AC#2: Integration Test Invokes Schema Validation

- [ ] Test script created - **Phase:** 3 - **Evidence:** devforgeai/integration-tests/test_schema_completeness.sh
- [ ] Uses Grep pattern - **Phase:** 3 - **Evidence:** grep -E "schema|interface|structure|format"
- [ ] Validates undefined schema detection - **Phase:** 5 - **Evidence:** Test output

### AC#3: WARNING Output Verified

- [ ] WARNING message generated - **Phase:** 5 - **Evidence:** Test output contains "WARNING"
- [ ] Recommendation text present - **Phase:** 5 - **Evidence:** "Schema referenced but not defined"

### AC#4: Test Passes for Epic with Defined Schema

- [ ] Defined schema fixture created - **Phase:** 3 - **Evidence:** devforgeai/integration-tests/fixtures/epic-with-defined-schema.md
- [ ] No WARNING generated - **Phase:** 5 - **Evidence:** Clean output, exit code 0

---

**Checklist Progress:** 0/10 items complete (0%)

---

## Definition of Done

### Implementation
- [ ] Test fixture with undefined schema created
- [ ] Test fixture with defined schema created
- [ ] Integration test script created
- [ ] Schema detection pattern validated

### Quality
- [ ] All 4 acceptance criteria have passing tests
- [ ] Integration test runs in < 5 seconds
- [ ] Test is deterministic (100% consistent)

### Testing
- [ ] Unit verification scripts for each AC
- [ ] Integration test passes for undefined schema
- [ ] Integration test passes for defined schema

### Documentation
- [ ] STORY-328 deferral resolved (reference STORY-329)

---

## Change Log

**Current Status:** Backlog

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-27 | claude/create-story | Created | Story created as follow-up from STORY-328 deferral | STORY-329.story.md |

## Implementation Notes

(To be populated during development)

## Notes

**Source Story:** STORY-328 - Add Explicit Schema Documentation Requirement
**Deferred Item:** "Integration test with undefined schema - DEFERRED: STORY-329 (runtime integration test)"

**Design Decisions:**
- Use bash script for integration test (aligns with existing test patterns in devforgeai/tests/)
- Create fixtures directory under devforgeai/integration-tests/ for reusable test data
- Test both positive (undefined schema) and negative (defined schema) scenarios

**Open Questions:**
- None

---

Story Template Version: 2.7
Last Updated: 2026-01-27

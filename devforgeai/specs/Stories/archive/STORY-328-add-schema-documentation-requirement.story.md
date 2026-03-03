---
id: STORY-328
title: Add Explicit Schema Documentation Requirement
type: feature
epic: EPIC-031
sprint: Backlog
status: QA Approved
points: 1
depends_on: ["STORY-325"]
priority: Medium
assigned_to: Unassigned
created: 2026-01-26
format_version: "2.7"
source_rca: RCA-031
source_recommendation: REC-5
---

# Story: Add Explicit Schema Documentation Requirement

## Description

**As a** DevForgeAI framework maintainer,
**I want** the self-validation-workflow.md to check that all referenced schemas are explicitly documented,
**so that** another Claude session can implement features without asking "What does this schema look like?"

## Provenance

```xml
<provenance>
  <origin document="RCA-031" section="recommendations">
    <quote>"Epics contained undefined schemas (ai-analysis.json, observation schema) without explicit specification"</quote>
    <line_reference>lines 513-564</line_reference>
    <quantified_impact>Reduces ambiguity in downstream story creation</quantified_impact>
  </origin>

  <decision rationale="cross-session-clarity">
    <selected>Add schema completeness check to validation with recommendation for undefined schemas</selected>
    <rejected alternative="allow-undefined-schemas">
      Undefined schemas cause ambiguity for downstream story creation and implementation
    </rejected>
    <trade_off>Additional validation complexity but reduces handoff friction</trade_off>
  </decision>

  <hypothesis id="H1" validation="schema-validation-test" success_criteria="Undefined schemas trigger WARNING with recommendation">
    Schema completeness check will flag all undefined data structures
  </hypothesis>
</provenance>
```

## Acceptance Criteria

### AC#1: Schema Completeness Check Added to Validation

```xml
<acceptance_criteria id="AC1">
  <given>The self-validation-workflow.md has Step 2.5 (Section Compliance)</given>
  <when>A developer reviews the validation workflow</when>
  <then>A Schema Completeness Check subsection is present within Step 2.5</then>
  <verification>
    <source_files>
      <file hint="Reference file to modify">.claude/skills/devforgeai-ideation/references/self-validation-workflow.md</file>
    </source_files>
    <test_file>devforgeai/tests/STORY-328/test_ac1_check_added.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Schema Reference Detection Pattern Present

```xml
<acceptance_criteria id="AC2">
  <given>The Schema Completeness Check is added</given>
  <when>The detection logic is reviewed</when>
  <then>A Grep pattern searches for schema|interface|structure|format keywords</then>
  <verification>
    <source_files>
      <file hint="Reference file to modify">.claude/skills/devforgeai-ideation/references/self-validation-workflow.md</file>
    </source_files>
    <test_file>devforgeai/tests/STORY-328/test_ac2_detection_pattern.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Warning Generated for Undefined Schema

```xml
<acceptance_criteria id="AC3">
  <given>A schema reference is found without a code block definition</given>
  <when>The Schema Completeness Check runs</when>
  <then>A WARNING is generated with recommendation to add explicit schema definition</then>
  <verification>
    <source_files>
      <file hint="Reference file to modify">.claude/skills/devforgeai-ideation/references/self-validation-workflow.md</file>
    </source_files>
    <test_file>devforgeai/tests/STORY-328/test_ac3_warning_generated.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Cross-Session Context Rule Documented

```xml
<acceptance_criteria id="AC4">
  <given>The Schema Completeness Check is added</given>
  <when>The documentation is reviewed</when>
  <then>A cross-session context rule states: "Another Claude session must be able to implement features without asking 'What does this schema look like?'"</then>
  <verification>
    <source_files>
      <file hint="Reference file to modify">.claude/skills/devforgeai-ideation/references/self-validation-workflow.md</file>
    </source_files>
    <test_file>devforgeai/tests/STORY-328/test_ac4_context_rule.sh</test_file>
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
        - key: "Schema Completeness Check Section"
          type: "markdown"
          example: "### Schema Completeness Check"
          required: true
          validation: "Subsection header exists within Step 2.5"
          test_requirement: "Test: Verify section header present"
        - key: "Schema Detection Pattern"
          type: "code_block"
          example: "Grep(pattern='schema|interface|structure|format')"
          required: true
          validation: "Pattern searches for schema-related keywords"
          test_requirement: "Test: Verify Grep pattern present"
        - key: "Code Block Detection Logic"
          type: "code_block"
          example: "if schema_ref mentions data structure without code block"
          required: true
          validation: "Logic checks for missing code block definitions"
          test_requirement: "Test: Verify code block detection logic"
        - key: "WARNING Output"
          type: "code_block"
          example: "WARNING: Schema referenced but not defined"
          required: true
          validation: "Warning message documented"
          test_requirement: "Test: Verify WARNING text present"
        - key: "Cross-Session Context Rule"
          type: "markdown"
          example: "**Cross-session context rule:** Another Claude session must..."
          required: true
          validation: "Rule explicitly states cross-session requirement"
          test_requirement: "Test: Verify context rule documented"

  business_rules:
    - id: "BR-001"
      rule: "All schema references must have explicit definitions"
      trigger: "Step 2.5 schema completeness check"
      validation: "Schema mention + code block = defined; schema mention only = undefined"
      error_handling: "WARNING with recommendation (not HALT)"
      test_requirement: "Test: Verify undefined schemas flagged"
      priority: "Medium"

    - id: "BR-002"
      rule: "Cross-session clarity is required"
      trigger: "Schema validation"
      validation: "Context rule documented and enforced"
      error_handling: "Recommendation to add explicit definition"
      test_requirement: "Test: Verify recommendation format"
      priority: "Medium"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Reliability"
      requirement: "Schema validation should detect most undefined schemas"
      metric: "80%+ detection rate for schema references"
      test_requirement: "Test: Validate against epic with undefined schemas"
      priority: "Medium"
```

---

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "Schema Detection Pattern"
    limitation: "Keyword-based detection may miss some schema references (e.g., 'data model' vs 'schema')"
    decision: "workaround:Use comprehensive keyword list but accept <100% coverage"
    discovered_phase: "Architecture"
    impact: "Some undefined schemas may not be detected"
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
- WARNING (not HALT) for undefined schemas
- Recommendation includes example JSON schema format

---

## Dependencies

### Prerequisite Stories

- [x] **STORY-325:** Add Section Compliance Validation
  - **Why:** Schema check is a subsection of Step 2.5 validation
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
1. **Happy Path:** Schema completeness check present with all elements
2. **Edge Cases:**
   - Multiple schema keywords in pattern
   - Example JSON schema in recommendation
3. **Error Cases:**
   - N/A

---

### Integration Tests

**Coverage Target:** N/A

**Test Scenarios:**
1. **End-to-End:** Create epic with undefined schema reference, verify WARNING

---

## Acceptance Criteria Verification Checklist

### AC#1: Schema Completeness Check Added to Validation

- [x] Section header present - **Phase:** 3 - **Evidence:** self-validation-workflow.md line 180
- [x] Positioned within Step 2.5 - **Phase:** 3 - **Evidence:** self-validation-workflow.md lines 135, 180, 213

### AC#2: Schema Reference Detection Pattern Present

- [x] Grep pattern documented - **Phase:** 3 - **Evidence:** self-validation-workflow.md line 185
- [x] Pattern includes multiple keywords - **Phase:** 3 - **Evidence:** schema|interface|structure|format

### AC#3: Warning Generated for Undefined Schema

- [x] WARNING logic present - **Phase:** 3 - **Evidence:** self-validation-workflow.md lines 191-193
- [x] Recommendation text documented - **Phase:** 3 - **Evidence:** "Recommend: Add explicit schema definition"
- [x] Example JSON schema in recommendation - **Phase:** 3 - **Evidence:** self-validation-workflow.md lines 198-207

### AC#4: Cross-Session Context Rule Documented

- [x] Context rule text present - **Phase:** 3 - **Evidence:** self-validation-workflow.md line 209
- [x] Rule mentions "another Claude session" - **Phase:** 3 - **Evidence:** "Another Claude session must be able to implement features..."

---

**Checklist Progress:** 10/10 items complete (100%)

---

## Definition of Done

### Implementation
- [x] Schema Completeness Check subsection added
- [x] Detection pattern with schema keywords
- [x] WARNING logic for undefined schemas
- [x] Recommendation with example JSON schema
- [x] Cross-session context rule documented
- [x] Both src/ and .claude/ copies updated

### Quality
- [x] All 4 acceptance criteria have passing tests
- [x] Grep verification confirms all elements present

### Testing
- [x] Verification scripts for each AC
- [ ] Integration test with undefined schema - DEFERRED: STORY-329 (runtime integration test)

### Documentation
- [ ] RCA-031 updated with story link - DEFERRED: User approved: non-blocking

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-26 10:00 | claude/create-stories-from-rca | Created | Story created from RCA-031 REC-5 | STORY-328.story.md |
| 2026-01-27 | claude/dev | Dev Complete | Added Schema Completeness Check subsection to self-validation-workflow.md | .claude/skills/devforgeai-ideation/references/self-validation-workflow.md, devforgeai/tests/STORY-328/*.sh |
| 2026-01-26 | claude/qa | QA Deep | QA Failed: 4/4 AC pass, 1 HIGH violation (STORY-329 not found) | devforgeai/qa/reports/STORY-328-qa-report.md |
| 2026-01-27 | claude/dev | Remediation | Created STORY-329 follow-up story to resolve invalid deferral reference | STORY-329-runtime-integration-test-schema-validation.story.md |
| 2026-01-27 | claude/qa-result-interpreter | QA Deep | PASSED: 4/4 AC pass, 0 violations, all deferrals valid | devforgeai/qa/reports/STORY-328-qa-report.md |

## Implementation Notes

- [x] Schema Completeness Check subsection added - line 180 - Completed: Added subsection header within Step 2.5
- [x] Detection pattern with schema keywords - line 185 - Completed: Grep(pattern="schema|interface|structure|format")
- [x] WARNING logic for undefined schemas - lines 191-193 - Completed: WARNING with recommendation text
- [x] Recommendation with example JSON schema - lines 198-207 - Completed: JSON Schema draft 2020-12 example
- [x] Cross-session context rule documented - line 209 - Completed: Cross-session context rule text added
- [x] All 4 acceptance criteria have passing tests - Completed: 4/4 tests pass
- [x] Grep verification confirms all elements present - Completed: test_ac2 validates pattern
- [x] Verification scripts for each AC - Completed: devforgeai/tests/STORY-328/test_ac*.sh
- [x] Both src/ and .claude/ copies updated - Completed: Both locations synced (backend-architect updated both)
- [ ] Integration test with undefined schema - DEFERRED: STORY-329 (runtime integration test)
- [ ] RCA-031 updated with story link - DEFERRED: Low priority documentation (User approved: non-blocking)

## Notes

**Source RCA:** RCA-031 - Ideation Epic Missing Constitutional Sections
**Source Recommendation:** REC-5 (MEDIUM) - Add Explicit Schema Documentation Requirement

**Design Decisions:**
- WARNING rather than HALT (schema definition is recommended, not mandatory)
- Include example JSON schema in recommendation to guide completion
- Keyword-based detection is pragmatic despite coverage limitations

**Effort Estimate:** 30 minutes (Low)
**Impact:** MEDIUM - Reduces ambiguity

---

Story Template Version: 2.7
Last Updated: 2026-01-26

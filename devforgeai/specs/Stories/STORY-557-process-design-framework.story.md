---
id: STORY-557
title: Process Design Framework
type: feature
epic: EPIC-078
sprint: Sprint-28
status: Ready for Dev
points: 2
depends_on: []
priority: Medium
advisory: false
source_gap: null
source_story: null
assigned_to: null
created: 2026-03-03
format_version: "2.9"
---

# Story: Process Design Framework

## Description

**As a** solo developer launching a business,
**I want** a guided framework for documenting my core business processes,
**so that** I have clear, repeatable workflows for customer onboarding, support, and fulfillment that are adapted to my specific business model and do not require me to learn complex process modeling tools.

## Provenance

```xml
<provenance>
  <origin document="devforgeai/specs/Epics/EPIC-078-operations-launch.epic.md" section="feature-4">
    <quote>"Guide users through defining core business processes (customer onboarding, support, fulfillment)"</quote>
    <line_reference>lines 63-66</line_reference>
    <quantified_impact>3 core processes documented with 5-field template per business model</quantified_impact>
  </origin>
</provenance>
```

## Acceptance Criteria

### AC#1: Model-Specific Processes

```xml
<acceptance_criteria id="AC1" implements="PROC-001">
  <given>a user initiates the process design framework and has identified their business model type</given>
  <when>the framework presents core processes to define</when>
  <then>it covers three universal processes — customer onboarding, customer support, and fulfillment/delivery — with business-model-specific steps</then>
  <verification>
    <source_files>
      <file hint="business-model-specific process templates">src/claude/skills/operating-business/references/process-design-framework.md</file>
    </source_files>
    <test_file>tests/STORY-557/test-ac1-model-specific-processes.md</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Five-Field Template

```xml
<acceptance_criteria id="AC2" implements="PROC-002">
  <given>a user is defining a specific process</given>
  <when>the framework guides them through the process definition</when>
  <then>each process is documented using a 5-field template: Process Name, Trigger, Steps, Owner, and Success Criteria, with the framework prompting the user for each field in sequence</then>
  <verification>
    <source_files>
      <file hint="5-field process template">src/claude/skills/operating-business/references/process-design-framework.md</file>
    </source_files>
    <test_file>tests/STORY-557/test-ac2-five-field-template.md</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Output Format

```xml
<acceptance_criteria id="AC3" implements="PROC-003">
  <given>a user has completed defining one or more processes</given>
  <when>the output is written</when>
  <then>devforgeai/specs/business/operations/core-processes.md is created with each process as an H2 section, all 5 fields as subsections, plus a flow summary line</then>
  <verification>
    <source_files>
      <file hint="output file format">src/claude/skills/operating-business/references/process-design-framework.md</file>
    </source_files>
    <test_file>tests/STORY-557/test-ac3-output-format.md</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Tool Stack Integration

```xml
<acceptance_criteria id="AC4" implements="PROC-004">
  <given>a user is defining process steps involving a tool</given>
  <when>they provide a step that involves a tool or system</when>
  <then>the framework cross-references tool-stack.md (if it exists) and auto-suggests the user's selected tool for that step type</then>
  <verification>
    <source_files>
      <file hint="tool stack cross-reference">src/claude/skills/operating-business/references/process-design-framework.md</file>
    </source_files>
    <test_file>tests/STORY-557/test-ac4-tool-stack-integration.md</test_file>
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
      name: "process-design-framework.md"
      file_path: "src/claude/skills/operating-business/references/process-design-framework.md"
      required_keys:
        - key: "core_processes"
          type: "array"
          example: "[customer onboarding, customer support, fulfillment]"
          required: true
          validation: "All 3 core processes present"
          test_requirement: "Test: Verify all 3 core process templates documented"
        - key: "template_fields"
          type: "array"
          example: "[Name, Trigger, Steps, Owner, Success Criteria]"
          required: true
          validation: "All 5 fields present"
          test_requirement: "Test: Verify 5-field template documented"
        - key: "business_model_variants"
          type: "object"
          example: "{SaaS: trial-to-paid, marketplace: seller+buyer, service: scoping, product: order-to-ship}"
          required: true
          validation: "All 4 model variants present"
          test_requirement: "Test: Verify model-specific process variants for all 4 types"

  business_rules:
    - id: "BR-001"
      rule: "Tool stack cross-reference is advisory, not required"
      trigger: "When process steps mention tools"
      validation: "Suggestion offered if tool-stack.md exists"
      error_handling: "Proceed without suggestions if file missing"
      test_requirement: "Test: Process completes when tool-stack.md absent"
      priority: "Medium"
    - id: "BR-002"
      rule: "Processes saved incrementally"
      trigger: "After each process definition completes"
      validation: "File written after each process, not only at end"
      error_handling: "Session interruption preserves completed processes"
      test_requirement: "Test: Interruption after 2 of 3 processes preserves the 2"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Reference file within size constraints"
      metric: "< 1,000 lines"
      test_requirement: "Test: wc -l process-design-framework.md < 1000"
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
- Framework initialization: < 3 seconds
- Output generation for 3 processes: < 2 seconds
- Tool stack cross-reference: < 1 second

### Security
- No customer PII captured in process documentation

### Scalability
- New business models added via reference file subsection
- New process categories added via reference file extension

### Reliability
- Completes without tool-stack.md (advisory cross-reference)
- Incremental saves after each process definition
- Auto-generated flow summary from numbered steps

### Observability
- Log process definitions completed per session

---

## Dependencies

### Prerequisite Stories
- No blocking prerequisites (STORY-555 optional for tool integration)

### External Dependencies
- None

### Technology Dependencies
- No new packages required

---

## Test Strategy

### Unit Tests
**Coverage Target:** 95%+
1. **Happy Path:** SaaS model, all 3 processes defined with 5 fields each
2. **Edge Cases:** No model, short process (1-2 steps), existing file, digital fulfillment
3. **Error Cases:** Missing output directory

### Integration Tests
**Coverage Target:** 85%+
1. Full process design workflow
2. Tool stack cross-reference integration

---

## Acceptance Criteria Verification Checklist

### AC#1: Model-Specific Processes
- [ ] 3 universal processes covered - **Phase:** 2
- [ ] Model-specific steps included - **Phase:** 2

### AC#2: Five-Field Template
- [ ] All 5 fields prompted sequentially - **Phase:** 2

### AC#3: Output Format
- [ ] H2 headers per process - **Phase:** 2
- [ ] Flow summary line present - **Phase:** 2

### AC#4: Tool Stack Integration
- [ ] Cross-reference works when tool-stack.md exists - **Phase:** 2
- [ ] Graceful when tool-stack.md absent - **Phase:** 2

---

**Checklist Progress:** 0/7 items complete (0%)

---

## Implementation Notes

*To be filled during /dev workflow*

## Definition of Done

### Implementation
- [ ] Reference file process-design-framework.md with 3 core processes and 4 model variants
- [ ] 5-field process template with sequential prompting
- [ ] Output file generation to core-processes.md with flow summary
- [ ] Tool stack cross-reference when available

### Quality
- [ ] All 4 acceptance criteria have passing tests
- [ ] Edge cases covered
- [ ] Reference file < 1,000 lines

### Testing
- [ ] Unit tests for model-specific processes
- [ ] Unit tests for 5-field template
- [ ] Integration tests for tool stack integration

### Documentation
- [ ] Reference file includes usage instructions

---

### TDD Workflow Summary
| Phase | Status | Details |
|-------|--------|---------|

### Files Created/Modified
| File | Action | Lines |
|------|--------|-------|

---

## Change Log

**Current Status:** Ready for Dev

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-03-03 | .claude/story-requirements-analyst | Created | Story created from EPIC-078 Feature 4 | STORY-557.story.md |

## Notes

**Edge Cases:**
1. No business model → default to service model
2. Very short process (1-2 steps) → flag for user review
3. Existing core-processes.md → add/update mode
4. Digital product → simplified fulfillment template

---

Story Template Version: 2.9
Last Updated: 2026-03-03

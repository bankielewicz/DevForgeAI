---
id: STORY-554
title: MVP Launch Checklist
type: feature
epic: EPIC-078
sprint: Sprint-28
status: Ready for Dev
points: 3
depends_on: []
priority: High
advisory: false
source_gap: null
source_story: null
assigned_to: null
created: 2026-03-03
format_version: "2.9"
---

# Story: MVP Launch Checklist

## Description

**As a** solo developer preparing to launch,
**I want** a comprehensive, business-model-aware MVP launch checklist,
**so that** I can systematically complete all legal, financial, marketing, technical, and operational requirements without missing critical steps.

**Example:**
As a SaaS developer ready to go live, I want a launch checklist adapted to SaaS-specific needs (subscription billing, monitoring, trial conversion) so that I can launch with confidence.

## Provenance

```xml
<provenance>
  <origin document="devforgeai/specs/brainstorms/BRAINSTORM-011-business-skills-framework.brainstorm.md" section="operations-launch">
    <quote>"Many aspiring entrepreneurs stall between planning and launching because the operational details feel overwhelming"</quote>
    <line_reference>EPIC-078, line 22</line_reference>
    <quantified_impact>Covers all 5 launch domains: legal, financial, marketing, technical, operations</quantified_impact>
  </origin>
  <decision rationale="comprehensive-checklist-over-minimal">
    <selected>Full 5-domain checklist with business model adaptation</selected>
    <rejected alternative="generic-checklist">Generic checklist lacks model-specific guidance, reducing actionability</rejected>
    <trade_off>Higher complexity (3 pts) for significantly better user experience</trade_off>
  </decision>
  <stakeholder role="Solo Developer" goal="launch-business-without-missing-steps">
    <quote>"Guide DevForgeAI users from business plan complete to business launched"</quote>
    <source>EPIC-078, Business Goal</source>
  </stakeholder>
</provenance>
```

## Acceptance Criteria

Define testable, specific conditions that must be met for story completion. Use XML format with `<acceptance_criteria>` blocks for machine-parseable verification.

> **IMPORTANT:** XML acceptance criteria format is REQUIRED for automated verification by the ac-compliance-verifier subagent. Legacy markdown format (Given/When/Then bullets) is NOT supported by verification tools.

### XML Acceptance Criteria Format

Use the following XML schema for each acceptance criterion.

### AC#1: Business Model Adaptation

```xml
<acceptance_criteria id="AC1" implements="LAUNCH-001">
  <given>a user has completed business planning (EPIC-073 output exists) and their business model type is known (SaaS, marketplace, service, or product)</given>
  <when>the MVP launch checklist skill is invoked</when>
  <then>the checklist adapts its domain sections and specific line items to match the detected business model type, omitting irrelevant items (e.g., inventory management for SaaS) and including model-specific items (e.g., subscription billing setup for SaaS)</then>
  <verification>
    <source_files>
      <file hint="checklist reference with model-specific sections">src/claude/skills/operating-business/references/mvp-launch-checklist.md</file>
    </source_files>
    <test_file>tests/STORY-554/test-ac1-business-model-adaptation.md</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Five Domain Coverage

```xml
<acceptance_criteria id="AC2" implements="LAUNCH-002">
  <given>a user initiates the MVP launch checklist workflow</given>
  <when>the checklist is generated</when>
  <then>it covers all five domains — legal (entity formation, contracts, privacy policy), financial (bank account, payment processing, accounting), marketing (brand assets, social presence, launch announcement), technical (hosting, monitoring, backups, security), and operations (support channel, onboarding flow, fulfillment process) — with a minimum of 3 actionable items per domain</then>
  <verification>
    <source_files>
      <file hint="five-domain checklist structure">src/claude/skills/operating-business/references/mvp-launch-checklist.md</file>
    </source_files>
    <test_file>tests/STORY-554/test-ac2-five-domain-coverage.md</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Output Format Compliance

```xml
<acceptance_criteria id="AC3" implements="LAUNCH-003">
  <given>a checklist has been generated for the user's business model</given>
  <when>the output is written</when>
  <then>the file devforgeai/specs/business/operations/launch-checklist.md is created with GitHub-flavored markdown checkboxes (- [ ] format), grouped by domain with section headers, and each item includes a one-line description of why it matters</then>
  <verification>
    <source_files>
      <file hint="output file path and format specification">src/claude/skills/operating-business/references/mvp-launch-checklist.md</file>
    </source_files>
    <test_file>tests/STORY-554/test-ac3-output-format.md</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Progressive Disclosure and Micro-Task Chunking

```xml
<acceptance_criteria id="AC4" implements="LAUNCH-004">
  <given>a user is working through the checklist and the checklist contains more than 20 items</given>
  <when>the skill presents checklist items</when>
  <then>items are presented in micro-task chunks of 5 to 7 items at a time with adaptive pacing prompts ("Ready for the next section?" before advancing), preventing overwhelm through progressive disclosure</then>
  <verification>
    <source_files>
      <file hint="progressive disclosure and micro-task chunking logic">src/claude/skills/operating-business/references/mvp-launch-checklist.md</file>
    </source_files>
    <test_file>tests/STORY-554/test-ac4-progressive-disclosure.md</test_file>
  </verification>
</acceptance_criteria>
```

---

### Source Files Guidance

The `<source_files>` element provides hints to the ac-compliance-verifier about where implementation code is located.

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "mvp-launch-checklist.md"
      file_path: "src/claude/skills/operating-business/references/mvp-launch-checklist.md"
      required_keys:
        - key: "domains.legal"
          type: "object"
          example: "Entity formation, contracts, privacy policy items"
          required: true
          validation: "Minimum 3 items per domain"
          test_requirement: "Test: Verify legal domain has >= 3 checklist items"
        - key: "domains.financial"
          type: "object"
          example: "Bank account, payment processing, accounting items"
          required: true
          validation: "Minimum 3 items per domain"
          test_requirement: "Test: Verify financial domain has >= 3 checklist items"
        - key: "domains.marketing"
          type: "object"
          example: "Brand assets, social presence, launch announcement"
          required: true
          validation: "Minimum 3 items per domain"
          test_requirement: "Test: Verify marketing domain has >= 3 checklist items"
        - key: "domains.technical"
          type: "object"
          example: "Hosting, monitoring, backups, security"
          required: true
          validation: "Minimum 3 items per domain"
          test_requirement: "Test: Verify technical domain has >= 3 checklist items"
        - key: "domains.operations"
          type: "object"
          example: "Support channel, onboarding flow, fulfillment"
          required: true
          validation: "Minimum 3 items per domain"
          test_requirement: "Test: Verify operations domain has >= 3 checklist items"
        - key: "business_models"
          type: "array"
          example: "[SaaS, marketplace, service, product]"
          required: true
          validation: "All 4 model types present"
          test_requirement: "Test: Verify all 4 business model variants exist"

  business_rules:
    - id: "BR-001"
      rule: "Checklist adapts to business model type from EPIC-073 output"
      trigger: "When business model type is detected in planning artifacts"
      validation: "Model-specific items included, irrelevant items omitted"
      error_handling: "Default to general-purpose checklist if model unknown"
      test_requirement: "Test: SaaS model includes subscription billing, excludes inventory management"
      priority: "High"
    - id: "BR-002"
      rule: "Progressive disclosure presents 5-7 items at a time"
      trigger: "When checklist contains more than 20 items"
      validation: "Items grouped in chunks of 5-7 with pacing prompts"
      error_handling: "Fall back to full list if chunking fails"
      test_requirement: "Test: Checklist with 25 items is presented in 4-5 chunks"
      priority: "Medium"
    - id: "BR-003"
      rule: "Existing checklist is resumed, not regenerated"
      trigger: "When launch-checklist.md already exists with checked items"
      validation: "Only unchecked items presented to user"
      error_handling: "If file corrupted, offer to regenerate"
      test_requirement: "Test: Existing file with 5 checked items shows only remaining unchecked items"
      priority: "Medium"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Checklist generation completes quickly"
      metric: "< 5 seconds from invocation to first output"
      test_requirement: "Test: Measure time from skill invocation to first display output"
      priority: "Medium"
    - id: "NFR-002"
      category: "Performance"
      requirement: "Reference file within size constraints"
      metric: "< 1,000 lines"
      test_requirement: "Test: wc -l mvp-launch-checklist.md < 1000"
      priority: "High"
    - id: "NFR-003"
      category: "Reliability"
      requirement: "Idempotent checklist generation"
      metric: "Same business model produces structurally identical output"
      test_requirement: "Test: Two invocations with same model produce identical domain structure"
      priority: "High"
```

---

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "EPIC-073 Integration"
    limitation: "Business model detection depends on EPIC-073 output which may not exist"
    decision: "workaround:Default to general-purpose checklist when EPIC-073 output missing"
    discovered_phase: "Architecture"
    impact: "Reduced personalization without business plan context"
  - id: TL-002
    component: "User Profile Integration"
    limitation: "EPIC-072 user profile for adaptive pacing may not be available"
    decision: "workaround:Use default micro-task chunking of 5-7 items"
    discovered_phase: "Architecture"
    impact: "Less personalized pacing without cognitive profile"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- Checklist generation: < 5 seconds from invocation to first output
- Output file write: < 1 second

**Throughput:**
- Single user workflow (not concurrent)

---

### Security

**Authentication:**
- None required (local framework tool)

**Data Protection:**
- No credentials, API keys, or financial account numbers captured in output
- No PII beyond what user explicitly provides

---

### Scalability

**Horizontal Scaling:**
- Not applicable (CLI tool)

**Content Scaling:**
- New business model types added via reference file section addition only
- New checklist domains appendable without restructuring

---

### Reliability

**Error Handling:**
- Graceful degradation when business model unknown (default to product model)
- Directory auto-creation if output path missing
- Idempotent generation (same inputs → same structure)

---

### Observability

**Logging:**
- Log business model detection result
- Log checklist item count per domain

---

## Dependencies

### Prerequisite Stories

- No blocking prerequisites (standalone story)

### External Dependencies

- [ ] **EPIC-073 Output (Optional):** Business model type for checklist adaptation
  - **Owner:** DevForgeAI
  - **Status:** Planning
  - **Impact if delayed:** Checklist works with manual model selection

### Technology Dependencies

- No new packages required (Markdown-only skill)

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for business logic

**Test Scenarios:**
1. **Happy Path:** SaaS model generates SaaS-specific checklist with all 5 domains
2. **Edge Cases:**
   - No EPIC-073 output → default general-purpose checklist
   - Hybrid business model → union of relevant items
   - Partially completed checklist → resume with unchecked items only
3. **Error Cases:**
   - Missing output directory → auto-create
   - Corrupted existing checklist → offer regeneration

---

### Integration Tests

**Coverage Target:** 85%+ for application layer

**Test Scenarios:**
1. **End-to-End Workflow:** Full checklist generation from model detection to file output
2. **Progressive Disclosure:** Verify chunked presentation with pacing prompts

---

## Acceptance Criteria Verification Checklist

**Purpose:** Real-time progress tracking during TDD implementation.

### AC#1: Business Model Adaptation

- [ ] SaaS model includes subscription billing items - **Phase:** 2 - **Evidence:** tests/STORY-554/test-ac1-business-model-adaptation.md
- [ ] Marketplace model includes seller/buyer onboarding - **Phase:** 2 - **Evidence:** tests/STORY-554/test-ac1-business-model-adaptation.md
- [ ] Irrelevant items omitted per model type - **Phase:** 2 - **Evidence:** tests/STORY-554/test-ac1-business-model-adaptation.md

### AC#2: Five Domain Coverage

- [ ] Legal domain has >= 3 items - **Phase:** 2 - **Evidence:** tests/STORY-554/test-ac2-five-domain-coverage.md
- [ ] Financial domain has >= 3 items - **Phase:** 2 - **Evidence:** tests/STORY-554/test-ac2-five-domain-coverage.md
- [ ] Marketing domain has >= 3 items - **Phase:** 2 - **Evidence:** tests/STORY-554/test-ac2-five-domain-coverage.md
- [ ] Technical domain has >= 3 items - **Phase:** 2 - **Evidence:** tests/STORY-554/test-ac2-five-domain-coverage.md
- [ ] Operations domain has >= 3 items - **Phase:** 2 - **Evidence:** tests/STORY-554/test-ac2-five-domain-coverage.md

### AC#3: Output Format Compliance

- [ ] Output file uses GitHub-flavored checkboxes - **Phase:** 2 - **Evidence:** tests/STORY-554/test-ac3-output-format.md
- [ ] Items grouped by domain with section headers - **Phase:** 2 - **Evidence:** tests/STORY-554/test-ac3-output-format.md
- [ ] Each item includes one-line description - **Phase:** 2 - **Evidence:** tests/STORY-554/test-ac3-output-format.md

### AC#4: Progressive Disclosure and Micro-Task Chunking

- [ ] Items chunked in groups of 5-7 - **Phase:** 2 - **Evidence:** tests/STORY-554/test-ac4-progressive-disclosure.md
- [ ] Adaptive pacing prompts between chunks - **Phase:** 2 - **Evidence:** tests/STORY-554/test-ac4-progressive-disclosure.md

---

**Checklist Progress:** 0/13 items complete (0%)

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

*To be filled during /dev workflow*

## Definition of Done

### Implementation
- [ ] Reference file mvp-launch-checklist.md created in src/claude/skills/operating-business/references/
- [ ] All 5 domains documented with >= 3 items each
- [ ] Business model adaptation logic for SaaS, marketplace, service, product
- [ ] Progressive disclosure chunking implemented (5-7 items per chunk)
- [ ] Output file generation to devforgeai/specs/business/operations/launch-checklist.md

### Quality
- [ ] All 4 acceptance criteria have passing tests
- [ ] Edge cases covered (no EPIC-073, hybrid model, resume, domain skip)
- [ ] Reference file < 1,000 lines
- [ ] No anti-patterns from anti-patterns.md

### Testing
- [ ] Unit tests for model-specific adaptation
- [ ] Unit tests for 5-domain coverage
- [ ] Unit tests for output format compliance
- [ ] Integration tests for progressive disclosure workflow

### Documentation
- [ ] Reference file includes usage instructions
- [ ] Checklist items include rationale descriptions

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
| 2026-03-03 | .claude/story-requirements-analyst | Created | Story created from EPIC-078 Feature 1 | STORY-554.story.md |

## Notes

**Design Decisions:**
- Checklist uses GitHub-flavored markdown checkboxes for compatibility with all markdown renderers
- Progressive disclosure prevents overwhelm for ADHD users per EPIC-072 adaptive pacing

**Edge Cases:**
1. No EPIC-073 output → default general-purpose checklist
2. Hybrid business models → union of relevant items, deduplicated
3. Partially completed checklist → resume with unchecked items only
4. User skips a domain → mark as pre-existing with timestamp

**References:**
- EPIC-078: Operations & Launch
- EPIC-073: Business Planning & Viability (dependency)
- EPIC-072: Assessment & Coaching Core (optional integration)

---

Story Template Version: 2.9
Last Updated: 2026-03-03

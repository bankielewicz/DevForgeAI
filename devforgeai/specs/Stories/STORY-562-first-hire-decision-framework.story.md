---
id: STORY-562
title: First Hire Decision Framework
type: feature
epic: EPIC-079
sprint: Sprint-29
status: Ready for Dev
points: 3
depends_on: []
priority: Medium
advisory: false
source_gap: null
source_story: null
assigned_to: null
created: 2026-03-03
format_version: "2.9"
---

# Story: First Hire Decision Framework

## Description

**As a** solo entrepreneur evaluating team growth,
**I want** a guided workflow that assesses my readiness to make a first hire based on revenue, time allocation, growth trajectory, and financial runway,
**so that** I receive a data-informed role recommendation with job description outline rather than hiring based on gut instinct.

## Acceptance Criteria

Define testable, specific conditions that must be met for story completion. Use XML format with `<acceptance_criteria>` blocks for machine-parseable verification.

> **IMPORTANT:** XML acceptance criteria format is REQUIRED for automated verification by the ac-compliance-verifier subagent.

### XML Acceptance Criteria Format

Use the following XML schema for each acceptance criterion.

### AC#1: Decision Factor Questionnaire Captures All Four Dimensions

```xml
<acceptance_criteria id="AC1" implements="SVC-001">
  <given>The first-hire decision framework skill is invoked</given>
  <when>The guided workflow executes</when>
  <then>It prompts the user for inputs across all four decision factors: revenue threshold (monthly/annual), percentage of time spent on non-core tasks, growth trajectory (month-over-month revenue trend), and financial runway (months of operating expenses covered), and all four factors are present in the output document</then>
  <verification>
    <source_files>
      <file hint="Skill reference file">src/claude/skills/building-team/references/first-hire-framework.md</file>
    </source_files>
    <test_file>tests/STORY-562/test_ac1_decision_factors.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Role Recommendation Generated from Decision Factor Analysis

```xml
<acceptance_criteria id="AC2" implements="SVC-002,SVC-003">
  <given>The user has provided responses to all four decision factor prompts</given>
  <when>The framework evaluates the inputs against its decision tree</when>
  <then>The output file devforgeai/specs/business/team/first-hire-plan.md contains a recommended first-hire role, a rationale paragraph linking the recommendation to the user's specific inputs, and a job description outline with at least: role title, key responsibilities (minimum 3), required skills, and suggested compensation range methodology</then>
  <verification>
    <source_files>
      <file hint="Skill reference file">src/claude/skills/building-team/references/first-hire-framework.md</file>
    </source_files>
    <test_file>tests/STORY-562/test_ac2_role_recommendation.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Financial Affordability Cross-Reference with EPIC-077 Data

```xml
<acceptance_criteria id="AC3" implements="SVC-004">
  <given>The user has financial model data generated from EPIC-077 (financial planning) skills</given>
  <when>The first-hire framework processes the hiring decision</when>
  <then>The output includes an affordability assessment section that references the user's monthly burn rate and runway, calculates maximum monthly salary budget as no more than 30% of monthly net revenue (or user-configured threshold), and flags a warning if the hire would reduce runway below 6 months</then>
  <verification>
    <source_files>
      <file hint="Skill reference file">src/claude/skills/building-team/references/first-hire-framework.md</file>
    </source_files>
    <test_file>tests/STORY-562/test_ac3_financial_integration.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Skill Reference File Follows DevForgeAI Skill Structure

```xml
<acceptance_criteria id="AC4" implements="SVC-001,SVC-002">
  <given>The first-hire decision framework is implemented as a skill reference file</given>
  <when>The skill file is reviewed against DevForgeAI conventions</when>
  <then>It contains: a decision tree with branching logic for "hire now", "hire soon (3-6 months)", and "not yet ready" outcomes; numbered prompt questions for each decision factor; output template markup for the generated first-hire-plan.md; and integration notes referencing EPIC-077 financial data paths</then>
  <verification>
    <source_files>
      <file hint="Skill reference file">src/claude/skills/building-team/references/first-hire-framework.md</file>
    </source_files>
    <test_file>tests/STORY-562/test_ac4_skill_structure.sh</test_file>
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
    - type: "Service"
      name: "FirstHireDecisionFramework"
      file_path: "src/claude/skills/building-team/references/first-hire-framework.md"
      interface: "Markdown skill reference"
      lifecycle: "Static"
      dependencies:
        - "EPIC-077 financial model output (optional)"
        - "building-team SKILL.md"
      requirements:
        - id: "SVC-001"
          description: "Decision tree with three terminal outcomes: hire now, hire soon (3-6 months), not yet ready"
          testable: true
          test_requirement: "Test: Each outcome is reachable by specific input combinations; verify all 3 paths produce distinct output sections"
          priority: "Critical"
        - id: "SVC-002"
          description: "Four decision factor prompt sections with input validation rules (revenue, time allocation, growth trajectory, runway)"
          testable: true
          test_requirement: "Test: Skill file contains numbered prompts for all 4 factors with explicit validation criteria"
          priority: "Critical"
        - id: "SVC-003"
          description: "Job description outline template with minimum required fields (role title, 3+ responsibilities, skills, compensation methodology)"
          testable: true
          test_requirement: "Test: Output template includes all required placeholders"
          priority: "High"
        - id: "SVC-004"
          description: "EPIC-077 financial data integration with graceful fallback to manual input"
          testable: true
          test_requirement: "Test: Integration notes reference EPIC-077 output paths; fallback flow documented"
          priority: "Medium"

  business_rules:
    - id: "BR-001"
      rule: "Runway < 3 months overrides any hire-now recommendation to stabilize-first"
      trigger: "Financial runway input evaluation"
      validation: "Decision tree must route to not-yet-ready when runway < 3 months"
      error_handling: "Display stabilization warning with freelance alternatives"
      test_requirement: "Test: Input with runway=2 always produces not-yet-ready outcome"
      priority: "Critical"
    - id: "BR-002"
      rule: "Zero-revenue users receive alternative guidance (co-founder/equity-based) instead of salaried-hire recommendation"
      trigger: "Revenue input is $0"
      validation: "No division by zero in percentage calculations"
      error_handling: "Route to alternative paths section"
      test_requirement: "Test: Input with revenue=0 produces alternative-paths output, no math errors"
      priority: "High"
    - id: "BR-003"
      rule: "Maximum salary budget is 30% of monthly net revenue (configurable)"
      trigger: "Affordability calculation"
      validation: "Budget percentage ≤ configured threshold"
      error_handling: "Flag warning if hire reduces runway below 6 months"
      test_requirement: "Test: Affordability section calculates 30% default correctly"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Skill execution completes in under 5 seconds"
      metric: "< 5 seconds end-to-end"
      test_requirement: "Test: Skill file loads and processes within 5 seconds"
      priority: "Medium"
    - id: "NFR-002"
      category: "Reliability"
      requirement: "All four decision factors must complete before document generation"
      metric: "Atomic operation — partial input produces no output"
      test_requirement: "Test: Incomplete inputs do not generate output file"
      priority: "High"
    - id: "NFR-003"
      category: "Scalability"
      requirement: "Skill reference file under 500 lines of Markdown"
      metric: "< 500 lines"
      test_requirement: "Test: wc -l on skill file returns < 500"
      priority: "Medium"
```

---

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "EPIC-077 Financial Integration"
    limitation: "EPIC-077 is in Planning status — financial model output files may not exist"
    decision: "workaround:graceful fallback to manual input prompts"
    discovered_phase: "Architecture"
    impact: "Affordability assessment uses self-reported data instead of validated financial model"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- Skill execution: < 5 seconds end-to-end on standard hardware
- Output file generation: Single write operation (no incremental appends)

**Throughput:**
- N/A (single-user CLI workflow)

---

### Security

**Authentication:** None (local CLI tool)

**Data Protection:**
- No sensitive financial data persisted beyond the output file
- No raw bank account numbers, SSNs, or API keys in output
- File written only to documented output path (`devforgeai/specs/business/team/`)

---

### Scalability

**File Size:**
- Skill reference file: < 500 lines of Markdown
- Output document: < 200 lines per generation

**Extensibility:**
- No external service dependencies — runs entirely offline

---

### Reliability

**Error Handling:**
- All four decision factors must complete before document generation (atomic)
- Missing EPIC-077 data falls back to manual input within 1 retry cycle
- Handles division by zero (zero revenue), negative values (declining growth), boundary values (0%/100%)

---

### Observability

**Logging:**
- Decision tree path taken logged for debugging
- Input validation failures logged with specific factor name

---

## Dependencies

### Prerequisite Stories

- None required (can start immediately)

### External Dependencies

- [ ] **EPIC-077 Financial Planning:** Optional integration for affordability assessment
  - **Owner:** DevForgeAI
  - **Status:** Planning
  - **Impact if delayed:** Framework works with manual input fallback

### Technology Dependencies

- None (Markdown files only)

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for business logic (decision tree paths)

**Test Scenarios:**
1. **Happy Path:** All four inputs provided, hire-now recommendation generated
2. **Edge Cases:**
   - Zero revenue → alternative guidance path
   - 100% non-core time → critical signal + warning
   - Runway < 3 months → override to stabilize-first
   - Revenue > $10M/month → confirmation prompt
3. **Error Cases:**
   - Missing EPIC-077 data → graceful fallback
   - Negative runway → route to not-yet-ready

---

### Integration Tests

**Coverage Target:** 85%+ for application layer

**Test Scenarios:**
1. **End-to-End Skill Flow:** Invoke skill, provide inputs, verify output file generated
2. **EPIC-077 Integration:** Verify affordability section when financial data available

---

## Acceptance Criteria Verification Checklist

**Purpose:** Real-time progress tracking during TDD implementation.

### AC#1: Decision Factor Questionnaire

- [ ] Revenue threshold prompt present - **Phase:** 2 - **Evidence:** src/claude/skills/building-team/references/first-hire-framework.md
- [ ] Time allocation prompt present - **Phase:** 2 - **Evidence:** src/claude/skills/building-team/references/first-hire-framework.md
- [ ] Growth trajectory prompt present - **Phase:** 2 - **Evidence:** src/claude/skills/building-team/references/first-hire-framework.md
- [ ] Financial runway prompt present - **Phase:** 2 - **Evidence:** src/claude/skills/building-team/references/first-hire-framework.md

### AC#2: Role Recommendation

- [ ] Decision tree with 3 outcomes implemented - **Phase:** 2 - **Evidence:** first-hire-framework.md
- [ ] Job description template with required fields - **Phase:** 2 - **Evidence:** first-hire-framework.md
- [ ] Output file template at correct path - **Phase:** 2 - **Evidence:** first-hire-framework.md

### AC#3: Financial Integration

- [ ] EPIC-077 integration notes present - **Phase:** 2 - **Evidence:** first-hire-framework.md
- [ ] Manual fallback flow documented - **Phase:** 2 - **Evidence:** first-hire-framework.md
- [ ] 30% salary budget calculation - **Phase:** 2 - **Evidence:** first-hire-framework.md

### AC#4: Skill Structure Compliance

- [ ] File < 500 lines - **Phase:** 2 - **Evidence:** wc -l first-hire-framework.md
- [ ] DevForgeAI skill conventions followed - **Phase:** 2 - **Evidence:** first-hire-framework.md

---

**Checklist Progress:** 0/11 items complete (0%)

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
- [ ] Skill reference file created at src/claude/skills/building-team/references/first-hire-framework.md
- [ ] Decision tree with 3 outcomes (hire now, hire soon, not yet ready)
- [ ] Four decision factor prompts with validation rules
- [ ] Job description outline template
- [ ] EPIC-077 integration with graceful fallback
- [ ] Output template for devforgeai/specs/business/team/first-hire-plan.md

### Quality
- [ ] All 4 acceptance criteria have passing tests
- [ ] Edge cases covered (zero revenue, 100% non-core, runway < 3 months)
- [ ] Data validation enforced (revenue non-negative, time 0-100%, runway positive)
- [ ] NFRs met (file < 500 lines, execution < 5 seconds)

### Testing
- [ ] Unit tests for decision tree paths
- [ ] Unit tests for input validation
- [ ] Integration test for end-to-end skill flow
- [ ] Integration test for EPIC-077 fallback

### Documentation
- [ ] Skill reference file self-documenting with clear sections
- [ ] Employment law disclaimers included
- [ ] Integration notes for EPIC-077

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
| 2026-03-03 | .claude/story-requirements-analyst | Created | Story created from EPIC-079 Feature 1 | STORY-562.story.md |

## Notes

**Design Decisions:**
- Decision tree uses three terminal outcomes per epic specification
- Financial integration designed as optional with graceful degradation
- 30% salary budget threshold is configurable per BR-003

**Safety Considerations:**
- Employment law guidance is educational only — prominent disclaimers required
- "Consult a professional" triggers at financial thresholds
- No jurisdiction-specific advice — general US guidance with "verify locally" warnings

**Related ADRs:**
- None

---

Story Template Version: 2.9
Last Updated: 2026-03-03

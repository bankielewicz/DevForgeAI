---
id: STORY-553
title: Startup Financial Model Generator
type: feature
epic: EPIC-077
sprint: Sprint-27
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

# Story: Startup Financial Model Generator

## Description

**As a** startup founder or early-stage entrepreneur,
**I want** to generate a 12-month financial projection model with revenue assumptions and cost structure analysis,
**so that** I can visualize my startup's financial trajectory, identify cash flow risks, and make informed planning decisions without requiring external financial modeling tools.

---

## Provenance

```xml
<provenance>
  <origin document="devforgeai/specs/Epics/EPIC-077-financial-planning-modeling.epic.md" section="features">
    <quote>"Startup Financial Model Generator — simple revenue projection model (12-month, assumptions-based), cost structure analysis (fixed vs variable costs), terminal table output format"</quote>
    <line_reference>lines 45-51</line_reference>
    <quantified_impact>First-time entrepreneurs avoid financial modeling due to spreadsheet complexity, leaving them without visibility into financial trajectory</quantified_impact>
  </origin>

  <decision rationale="guided-terminal-tables-over-spreadsheet-export">
    <selected>12-month ASCII table projections with labeled assumptions and uncertainty ranges, written to projections.md</selected>
    <rejected alternative="spreadsheet-file-generation-or-24-month-horizon">
      Spreadsheet export and extended horizons deferred — terminal-first constraint and scope management
    </rejected>
    <trade_off>Users limited to 12-month horizon with ASCII output; complex multi-scenario modeling requires external tools</trade_off>
  </decision>

  <stakeholder role="Startup Founder or Early-Stage Entrepreneur" goal="visualize-financial-trajectory">
    <quote>"Visualize my startup's financial trajectory, identify cash flow risks, and make informed planning decisions"</quote>
    <source>EPIC-077, Feature 1</source>
  </stakeholder>

  <hypothesis id="H1" validation="user-feedback" success_criteria="12-month projection with revenue, costs, and P/L generated correctly for all valid input combinations">
    Guided financial modeling with transparent assumptions makes financial planning accessible to non-finance founders
  </hypothesis>
</provenance>
```

---

## Acceptance Criteria

<acceptance_criteria id="AC1">
  <title>Revenue projection table</title>
  <given>User provides revenue assumptions (initial monthly revenue, growth rate, start month/year)</given>
  <when>The financial model generator runs</when>
  <then>Output displays ASCII table showing Month, Revenue, MoM Growth, Cumulative Revenue for 12 months with assumptions labeled and uncertainty range note</then>
  <verification>
    <source_files>
      <file>src/claude/skills/managing-finances/SKILL.md</file>
      <file>src/claude/skills/managing-finances/references/startup-financial-model.md</file>
    </source_files>
    <test_file>tests/STORY-553/test_ac1_revenue_projection_table.py</test_file>
  </verification>
</acceptance_criteria>

<acceptance_criteria id="AC2">
  <title>Cost structure analysis</title>
  <given>User provides fixed costs and variable costs</given>
  <when>Cost structure phase executes</when>
  <then>Output displays ASCII table showing Cost Category, Type, Monthly Amount/Rate, 12-Month Total with summary row</then>
  <verification>
    <source_files>
      <file>src/claude/skills/managing-finances/SKILL.md</file>
      <file>src/claude/skills/managing-finances/references/startup-financial-model.md</file>
    </source_files>
    <test_file>tests/STORY-553/test_ac2_cost_structure_analysis.py</test_file>
  </verification>
</acceptance_criteria>

<acceptance_criteria id="AC3">
  <title>Combined P/L output with disclaimer</title>
  <given>Both revenue and cost tables generated</given>
  <when>Workflow assembles final output</when>
  <then>Combined P/L table rendered showing Month/Revenue/Costs/Net P&amp;L/Cash Position for 12 months, written to `devforgeai/specs/business/financial/projections.md` with "not financial advice" disclaimer as first line</then>
  <verification>
    <source_files>
      <file>src/claude/skills/managing-finances/SKILL.md</file>
      <file>src/claude/skills/managing-finances/references/startup-financial-model.md</file>
    </source_files>
    <test_file>tests/STORY-553/test_ac3_combined_pl_output.py</test_file>
  </verification>
</acceptance_criteria>

<acceptance_criteria id="AC4">
  <title>Framework constraints met</title>
  <given>SKILL.md exists</given>
  <when>Projection generated</when>
  <then>SKILL.md &lt; 1,000 lines, reference file uses progressive disclosure, no external libraries</then>
  <verification>
    <source_files>
      <file>src/claude/skills/managing-finances/SKILL.md</file>
      <file>src/claude/skills/managing-finances/references/startup-financial-model.md</file>
    </source_files>
    <test_file>tests/STORY-553/test_ac4_framework_constraints.py</test_file>
  </verification>
</acceptance_criteria>

<acceptance_criteria id="AC5">
  <title>Incomplete input handling</title>
  <given>User hasn't provided all required inputs</given>
  <when>Workflow attempts projection</when>
  <then>Skill prompts for missing inputs, halts generation, no partial output written</then>
  <verification>
    <source_files>
      <file>src/claude/skills/managing-finances/SKILL.md</file>
      <file>src/claude/skills/managing-finances/references/startup-financial-model.md</file>
    </source_files>
    <test_file>tests/STORY-553/test_ac5_incomplete_input_handling.py</test_file>
  </verification>
</acceptance_criteria>

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"
  components:
    - type: "Configuration"
      name: "managing-finances skill"
      file_path: "src/claude/skills/managing-finances/SKILL.md"
      required_keys:
        - key: "financial-model-phase"
          type: "string"
          required: true
          test_requirement: "Test: SKILL.md contains financial model phase definition"
    - type: "Configuration"
      name: "startup-financial-model reference"
      file_path: "src/claude/skills/managing-finances/references/startup-financial-model.md"
      required_keys:
        - key: "revenue-projection-methodology"
          type: "string"
          required: true
          test_requirement: "Test: Reference file contains 12-month projection methodology"
        - key: "cost-structure-analysis"
          type: "string"
          required: true
          test_requirement: "Test: Reference file contains cost breakdown logic"
        - key: "ascii-table-templates"
          type: "string"
          required: true
          test_requirement: "Test: Reference file contains ASCII table rendering specs"
  business_rules:
    - id: "BR-001"
      rule: "All financial outputs must include 'not financial advice' disclaimer as first visible line"
      trigger: "Any file write to devforgeai/specs/business/financial/"
      validation: "Grep for disclaimer string in output file"
      error_handling: "Block file write if disclaimer missing"
      test_requirement: "Test: Output file starts with disclaimer"
      priority: "Critical"
    - id: "BR-002"
      rule: "Revenue projections must clearly label all assumptions"
      trigger: "Revenue projection table generation"
      validation: "Check for assumption labels above table"
      error_handling: "Halt if assumptions not labeled"
      test_requirement: "Test: Assumptions section exists above revenue table"
      priority: "High"
    - id: "BR-003"
      rule: "No external libraries for calculations"
      trigger: "Any calculation step"
      validation: "No import statements for math/financial libraries"
      error_handling: "Reject implementation using external libs"
      test_requirement: "Test: No external library references in skill or reference files"
      priority: "Critical"
  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "12-month projection completes in under 2 seconds"
      metric: "< 2000ms execution time"
      test_requirement: "Test: Projection completes within 2s threshold"
      priority: "Medium"
    - id: "NFR-002"
      category: "Security"
      requirement: "NFR-S003 disclaimer present on all financial outputs"
      metric: "100% of output files contain disclaimer"
      test_requirement: "Test: Every output file contains disclaimer string"
      priority: "Critical"
```

---

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "managing-finances skill"
    limitation: "12-month projection only; 24/36 month extension out of scope"
    decision: "descope:EPIC-077"
    discovered_phase: "Architecture"
    impact: "Users limited to 12-month horizon"
```

---

## Non-Functional Requirements

### Performance

| ID | Requirement | Metric | Priority |
|----|-------------|--------|----------|
| NFR-P001 | 12-month projection completes within time threshold | < 2000ms execution time | Medium |
| NFR-P002 | ASCII table rendering is fast | < 500ms table render time | Low |
| NFR-P003 | Output file size is bounded | < 50KB output file | Low |

### Security

| ID | Requirement | Metric | Priority |
|----|-------------|--------|----------|
| NFR-S001 | No use of eval or dynamic code execution | Zero eval calls | Critical |
| NFR-S002 | Output written only to fixed approved path | Output path = devforgeai/specs/business/financial/ | Critical |
| NFR-S003 | Disclaimer present on all financial outputs | 100% of output files contain disclaimer | Critical |
| NFR-S004 | No logging of user-provided financial data | Zero financial data in logs | High |

### Reliability

| ID | Requirement | Metric | Priority |
|----|-------------|--------|----------|
| NFR-R001 | Structured error messages on invalid input | All errors include field name and expected format | High |
| NFR-R002 | Deterministic output for same inputs | Identical inputs produce identical outputs | High |
| NFR-R003 | Numeric precision maintained | All monetary values rounded to 2 decimal places | Medium |

### Scalability

| ID | Requirement | Metric | Priority |
|----|-------------|--------|----------|
| NFR-SC001 | Supports up to 50 cost line items | Cost table handles 50 rows without degradation | Low |
| NFR-SC002 | SKILL.md stays within line limit | SKILL.md < 1,000 lines | Medium |
| NFR-SC003 | Stateless workflow execution | No session state persisted between runs | Medium |

### Observability

| ID | Requirement | Metric | Priority |
|----|-------------|--------|----------|
| NFR-O001 | Phase completion logged to console | Each phase outputs status message | Low |
| NFR-O002 | Input assumptions echoed in output | Assumptions section present in all output files | High |

---

## Edge Cases

| ID | Scenario | Expected Behavior |
|----|----------|-------------------|
| EC-001 | Zero or negative initial revenue | Skill prompts user to confirm and proceeds with 0 as floor; documents as assumption |
| EC-002 | 0% monthly growth rate | Flat revenue line generated; no MoM Growth column shows 0% |
| EC-003 | Variable costs exceed 100% of revenue | Net P&L shows negative for affected months; cash position tracked cumulatively |
| EC-004 | Very high growth rate (> 100% MoM) | Projection computed; uncertainty range note explicitly widened with warning label |
| EC-005 | No cost items provided | Cost structure table omitted; P&L uses revenue-only view with note that costs not provided |

---

## Dependencies

### Prerequisite

- None (first story in EPIC-077)

### External

- None

### Technology

- None (pure Markdown output; no external libraries required)

---

## Test Strategy

### Unit Tests

- Test revenue projection formula: `revenue[n] = revenue[n-1] * (1 + growth_rate)`
- Test cumulative revenue accumulation across 12 months
- Test ASCII table column alignment and header rendering
- Test cost structure table with fixed and variable cost rows
- Test summary row calculation in cost table
- Test P&L assembly: Net P&L = Revenue - Total Costs
- Test cash position running total calculation
- Test disclaimer presence as first line of output file
- Test input validation for missing required fields
- Test input validation for non-numeric inputs
- Test edge cases: zero revenue, 0% growth, costs > 100% revenue, > 100% MoM growth, no costs

### Integration Tests

- Test full workflow from user-provided inputs to output file creation at `devforgeai/specs/business/financial/projections.md`
- Test that partial output is NOT written when inputs are incomplete

---

## AC Verification Checklist

### AC1: Revenue Projection Table
- [ ] (Red) Test: revenue projection table contains 12 rows
- [ ] (Red) Test: table columns are Month, Revenue, MoM Growth, Cumulative Revenue
- [ ] (Red) Test: assumptions section labeled above table
- [ ] (Red) Test: uncertainty range note present
- [ ] (Green) Revenue formula implemented correctly
- [ ] (Green) Table renders with correct alignment

### AC2: Cost Structure Analysis
- [ ] (Red) Test: cost table contains Cost Category, Type, Monthly Amount/Rate, 12-Month Total columns
- [ ] (Red) Test: summary row present at bottom of cost table
- [ ] (Red) Test: fixed and variable cost types correctly labeled
- [ ] (Green) Cost structure table renders with correct totals

### AC3: Combined P/L Output with Disclaimer
- [ ] (Red) Test: output file starts with "not financial advice" disclaimer
- [ ] (Red) Test: P&L table contains Month, Revenue, Costs, Net P&L, Cash Position columns
- [ ] (Red) Test: output written to devforgeai/specs/business/financial/projections.md
- [ ] (Green) P&L assembly combines revenue and cost data correctly
- [ ] (Green) Cash position tracks cumulatively

### AC4: Framework Constraints Met
- [ ] (Red) Test: SKILL.md line count < 1,000
- [ ] (Red) Test: reference file uses progressive disclosure structure
- [ ] (Red) Test: no external library import statements in skill or reference files
- [ ] (Green) SKILL.md phase definition present and within line limit

### AC5: Incomplete Input Handling
- [ ] (Red) Test: missing initial revenue triggers prompt, no output written
- [ ] (Red) Test: missing growth rate triggers prompt, no output written
- [ ] (Red) Test: missing start month/year triggers prompt, no output written
- [ ] (Green) Input validation implemented for all required fields

---

## Implementation Notes

**Developer:** (unassigned)
**Implemented:** (not started)

---

## Definition of Done

### Implementation
- [ ] SKILL.md contains financial model phase definition < 1,000 lines
- [ ] startup-financial-model.md reference file created with progressive disclosure
- [ ] Revenue projection generates 12-month ASCII table
- [ ] Cost structure analysis generates categorized table
- [ ] Combined P/L table generated
- [ ] Output written to devforgeai/specs/business/financial/projections.md
- [ ] "Not financial advice" disclaimer present on all outputs

### Quality
- [ ] All 5 acceptance criteria have passing tests
- [ ] Edge cases covered (zero revenue, 0% growth, costs > 100%, high growth, no costs)
- [ ] Input validation enforced for all numeric inputs
- [ ] NFR-S003 disclaimer compliance verified
- [ ] Code coverage > 95% for calculation logic

### Testing
- [ ] Unit tests for revenue projection formulas
- [ ] Unit tests for cost structure calculations
- [ ] Unit tests for P/L table assembly
- [ ] Unit tests for ASCII table rendering
- [ ] Integration test for full workflow
- [ ] Edge case tests for all 5 documented scenarios

### Documentation
- [ ] SKILL.md phase documentation complete
- [ ] Reference file self-contained with calculation methodology
- [ ] Assumption labeling guide documented

### TDD Workflow Summary

| Phase | Status | Notes |
|-------|--------|-------|
| Phase 01: Pre-Flight | Not Started | |
| Phase 02: Red (Tests) | Not Started | |
| Phase 03: Green (Implementation) | Not Started | |
| Phase 04: Refactor | Not Started | |
| Phase 04.5: AC Verify (Post-Refactor) | Not Started | |
| Phase 05: Integration | Not Started | |
| Phase 05.5: AC Verify (Post-Integration) | Not Started | |
| Phase 06: Deferral Review | Not Started | |
| Phase 07: DoD Update | Not Started | |
| Phase 08: Git Workflow | Not Started | |
| Phase 09: Feedback | Not Started | |
| Phase 10: Result | Not Started | |

### Files Created

| File | Purpose |
|------|---------|
| src/claude/skills/managing-finances/SKILL.md | Skill definition with financial model phase |
| src/claude/skills/managing-finances/references/startup-financial-model.md | Reference file with methodology, templates, and calculation logic |
| tests/STORY-553/test_ac1_revenue_projection_table.py | AC1 unit tests |
| tests/STORY-553/test_ac2_cost_structure_analysis.py | AC2 unit tests |
| tests/STORY-553/test_ac3_combined_pl_output.py | AC3 unit + integration tests |
| tests/STORY-553/test_ac4_framework_constraints.py | AC4 structural tests |
| tests/STORY-553/test_ac5_incomplete_input_handling.py | AC5 validation tests |

---

## Change Log

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-03-03 12:00 | .claude/story-requirements-analyst | Created | Story created from EPIC-077 Feature 1 | STORY-553.story.md |

---

## Notes

- Safety constraint: All financial outputs include "not financial advice" disclaimers (NFR-S003). This is a Critical-priority requirement and blocks QA approval if absent.
- Revenue projections must clearly label assumptions and uncertainty ranges to comply with BR-002.
- No external financial libraries; all calculations use native arithmetic (BR-003).
- Maps to requirement FR-019.
- Output directory `devforgeai/specs/business/financial/` must be created if it does not exist prior to writing projections.md.
- This is the first story in EPIC-077; no prerequisite stories.

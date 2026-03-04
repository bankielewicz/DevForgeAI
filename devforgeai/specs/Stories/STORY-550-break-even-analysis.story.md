---
id: STORY-550
title: Break-Even Analysis
type: feature
epic: EPIC-077
sprint: Sprint-27
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

# Story: Break-Even Analysis

## Description

**As a** business founder or entrepreneur,
**I want** to calculate my break-even point in units and revenue with a visual ASCII chart,
**so that** I understand exactly how much I need to sell to cover all costs before becoming profitable.

## Provenance

```xml
<provenance>
  <origin document="devforgeai/specs/Epics/EPIC-077-financial-planning-modeling.epic.md" section="features">
    <quote>"Break-Even Analysis — calculate units/revenue needed to cover costs, ASCII chart visualization of break-even point"</quote>
    <line_reference>lines 60-65</line_reference>
    <quantified_impact>Founders launch without understanding minimum viable sales volume, risking cash depletion before profitability</quantified_impact>
  </origin>

  <decision rationale="formula-transparency-over-black-box">
    <selected>Show all formulas alongside computed values with ASCII chart visualization within 80-char terminal width</selected>
    <rejected alternative="graphical-chart-or-spreadsheet-export">
      Graphical output rejected — terminal-only constraint; spreadsheet export deferred to future story
    </rejected>
    <trade_off>Chart fidelity limited to ASCII within 80 characters; complex multi-scenario comparison requires multiple invocations</trade_off>
  </decision>

  <stakeholder role="Business Founder or Entrepreneur" goal="understand-sales-volume-for-profitability">
    <quote>"Understand exactly how much I need to sell to cover all costs before becoming profitable"</quote>
    <source>EPIC-077, Feature 3</source>
  </stakeholder>

  <hypothesis id="H1" validation="user-feedback" success_criteria="Break-even calculation produces correct results for all valid input combinations with formula transparency">
    Transparent break-even analysis with visible formulas increases founder confidence in financial planning
  </hypothesis>
</provenance>
```

## Acceptance Criteria

Define testable, specific conditions that must be met for story completion. Use XML format with `<acceptance_criteria>` blocks for machine-parseable verification.

> **IMPORTANT:** XML acceptance criteria format is REQUIRED for automated verification by the ac-compliance-verifier subagent.

### XML Acceptance Criteria Format

### AC#1: Break-Even Calculation with Formulas Shown

```xml
<acceptance_criteria id="AC1" implements="SVC-001">
  <given>A user invokes the break-even analysis phase and provides fixed costs, variable cost per unit, and selling price per unit</given>
  <when>The skill performs the break-even calculation</when>
  <then>The output displays: break-even units (ceil(fixed_costs / (price - variable_cost))), break-even revenue (units * price), contribution margin per unit (price - variable_cost), and contribution margin ratio ((price - variable_cost) / price * 100%), with each formula shown alongside its computed value</then>
  <verification>
    <source_files>
      <file hint="Skill definition">src/claude/skills/managing-finances/SKILL.md</file>
      <file hint="Break-even analysis reference">src/claude/skills/managing-finances/references/break-even-analysis.md</file>
    </source_files>
    <test_file>tests/STORY-550/test_ac1_break_even_calculation.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#2: ASCII Chart with Revenue and Cost Lines

```xml
<acceptance_criteria id="AC2" implements="SVC-002">
  <given>Break-even calculation has been completed successfully</given>
  <when>The skill renders the ASCII chart</when>
  <then>The chart displays a revenue line, a total cost line (fixed + variable), the break-even intersection marked with a distinct symbol (e.g., "X" or "*"), labeled axes (x-axis: Units, y-axis: Amount $), and fits within 80 characters width</then>
  <verification>
    <source_files>
      <file hint="Break-even analysis reference">src/claude/skills/managing-finances/references/break-even-analysis.md</file>
    </source_files>
    <test_file>tests/STORY-550/test_ac2_ascii_chart.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Output Appended to projections.md

```xml
<acceptance_criteria id="AC3" implements="SVC-003">
  <given>Break-even calculation and ASCII chart have been generated</given>
  <when>The skill writes output to disk</when>
  <then>The content is appended to devforgeai/specs/business/financial/projections.md with: a heading ("## Break-Even Analysis"), a timestamp (ISO 8601 format), the calculated results, the ASCII chart, an assumptions section listing the input values used, and a disclaimer noting results are estimates based on provided inputs. If projections.md does not exist, it is created.</then>
  <verification>
    <source_files>
      <file hint="Break-even analysis reference">src/claude/skills/managing-finances/references/break-even-analysis.md</file>
    </source_files>
    <test_file>tests/STORY-550/test_ac3_projections_output.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Error on Invalid Price/Cost Inputs

```xml
<acceptance_criteria id="AC4" implements="SVC-004">
  <given>A user provides a selling price that is less than or equal to the variable cost per unit</given>
  <when>The skill attempts to perform the break-even calculation</when>
  <then>The skill raises a clear error message explaining that selling price must exceed variable cost per unit to have a positive contribution margin, and no output is written to projections.md</then>
  <verification>
    <source_files>
      <file hint="Break-even analysis reference">src/claude/skills/managing-finances/references/break-even-analysis.md</file>
    </source_files>
    <test_file>tests/STORY-550/test_ac4_invalid_input_error.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#5: SKILL.md Size and Progressive Disclosure

```xml
<acceptance_criteria id="AC5" implements="SVC-005">
  <given>The break-even analysis phase has been added to the managing-finances SKILL.md</given>
  <when>The SKILL.md file is measured</when>
  <then>The total line count of SKILL.md remains below 1,000 lines. Detailed calculation methodology, chart rendering specification, and edge case handling are documented in the break-even-analysis.md reference file and referenced from SKILL.md via a progressive disclosure link</then>
  <verification>
    <source_files>
      <file hint="Skill definition">src/claude/skills/managing-finances/SKILL.md</file>
      <file hint="Break-even analysis reference">src/claude/skills/managing-finances/references/break-even-analysis.md</file>
    </source_files>
    <test_file>tests/STORY-550/test_ac5_skill_size_disclosure.py</test_file>
    <coverage_threshold>95</coverage_threshold>
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
      name: "managing-finances-skill"
      file_path: "src/claude/skills/managing-finances/SKILL.md"
      required_keys:
        - key: "break_even_phase"
          type: "object"
          example: "Phase definition with calculation and chart steps"
          required: true
          validation: "Must define break-even phase with reference link to break-even-analysis.md"
          test_requirement: "Test: Verify SKILL.md contains break-even phase definition under 1,000 lines"

    - type: "Configuration"
      name: "break-even-analysis"
      file_path: "src/claude/skills/managing-finances/references/break-even-analysis.md"
      required_keys:
        - key: "calculation_methodology"
          type: "object"
          example: "Formulas for break-even units, revenue, contribution margin, margin ratio"
          required: true
          validation: "Must document all 4 formulas with worked examples"
          test_requirement: "Test: Verify reference contains all 4 formula definitions"
        - key: "chart_rendering_spec"
          type: "object"
          example: "ASCII chart dimensions, axis labels, intersection marker"
          required: true
          validation: "Must specify 80-char width constraint, axis labels, and intersection symbol"
          test_requirement: "Test: Verify chart spec defines 80-char width and labeled axes"
        - key: "edge_case_handling"
          type: "object"
          example: "Zero fixed costs, high break-even, non-integer units, zero variable cost"
          required: true
          validation: "Must document handling for all 6 identified edge cases"
          test_requirement: "Test: Verify edge case documentation covers all 6 scenarios"
        - key: "output_format"
          type: "object"
          example: "projections.md append format with heading, timestamp, results, chart, assumptions, disclaimer"
          required: true
          validation: "Must specify projections.md append format and file creation when missing"
          test_requirement: "Test: Verify output format includes all required sections"

  business_rules:
    - id: "BR-001"
      rule: "Disclaimer must be included in every projections.md output section"
      trigger: "Break-even output written to projections.md"
      validation: "Disclaimer text present in output section"
      error_handling: "HALT if disclaimer omitted from write operation"
      test_requirement: "Test: Verify disclaimer present in projections.md output"
      priority: "Critical"
    - id: "BR-002"
      rule: "All calculation steps must be shown transparently with formula and computed value"
      trigger: "Break-even calculation display"
      validation: "Four formula+value pairs present in output"
      error_handling: "N/A — design constraint"
      test_requirement: "Test: Verify each calculation shows formula and value"
      priority: "High"
    - id: "BR-003"
      rule: "No external libraries — all calculation and chart rendering uses pure Python stdlib"
      trigger: "Any import statement in implementation"
      validation: "No third-party library imports in calculation or chart modules"
      error_handling: "HALT and flag as architecture violation if third-party import detected"
      test_requirement: "Test: Verify no third-party imports in implementation"
      priority: "Critical"
    - id: "BR-004"
      rule: "Selling price must be strictly greater than variable cost per unit"
      trigger: "User-provided price <= variable cost"
      validation: "Error raised before any calculation or file write"
      error_handling: "Display clear error explaining contribution margin must be positive"
      test_requirement: "Test: Verify error raised when price <= variable cost"
      priority: "High"
    - id: "BR-005"
      rule: "Non-integer break-even units are rounded up (ceiling) to the nearest whole unit"
      trigger: "Break-even units calculation produces fractional result"
      validation: "Units value is always a whole number, ceiling of exact division"
      error_handling: "Note rounding applied in output alongside exact fractional value"
      test_requirement: "Test: Verify ceiling rounding applied to fractional unit results"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Break-even calculation completes in under 200ms"
      metric: "< 200ms wall-clock time for calculation logic"
      test_requirement: "Test: Verify calculation executes in under 200ms"
      priority: "High"
    - id: "NFR-002"
      category: "Performance"
      requirement: "ASCII chart rendering completes in under 100ms"
      metric: "< 100ms wall-clock time for chart render"
      test_requirement: "Test: Verify chart rendering executes in under 100ms"
      priority: "High"
    - id: "NFR-003"
      category: "Performance"
      requirement: "projections.md file append operation completes in under 500ms"
      metric: "< 500ms wall-clock time for file append"
      test_requirement: "Test: Verify file append completes in under 500ms"
      priority: "Medium"
    - id: "NFR-S003"
      category: "Compliance"
      requirement: "All financial output must include disclaimer that results are estimates based on user-provided inputs and not professional financial advice"
      metric: "Disclaimer present in every projections.md output section"
      test_requirement: "Test: Verify disclaimer text in every output section"
      priority: "Critical"
```

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "ASCII Chart"
    limitation: "Chart is limited to 80-character terminal width; complex visualizations (multiple scenarios, sensitivity curves) are out of scope for this story"
    decision: "constraint:Single-scenario ASCII chart only; multi-scenario comparison deferred to future story"
    discovered_phase: "Architecture"
    impact: "Users needing multi-scenario comparison must invoke analysis multiple times and compare outputs manually in projections.md"
```

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- **Calculation:** < 200ms for break-even formula computation
- **Chart render:** < 100ms for ASCII chart generation
- **File append:** < 500ms for projections.md write

**Throughput:**
- Single-user CLI tool, no concurrency requirements

**Performance Test:**
- Measure wall-clock time for calculation, chart, and file append operations independently

---

### Security

**Authentication:**
- None (local CLI tool)

**Data Protection:**
- No sensitive data collected; financial inputs are user-provided and stored locally
- Output stored locally in project directory under devforgeai/specs/business/financial/

**Security Testing:**
- [ ] No hardcoded secrets
- [ ] File write uses native Write tool (not Bash echo/redirect)

---

### Scalability

**Horizontal Scaling:**
- Not applicable (CLI tool)

**Database:**
- Not applicable (file-based output)

**Caching:**
- None required

---

### Reliability

**Error Handling:**
- Invalid inputs (price <= variable cost) raise descriptive errors before computation
- Missing projections.md results in file creation, not an error
- Non-integer break-even units are ceiling-rounded with note in output

**Retry Logic:**
- Not applicable (single-pass calculation)

**Monitoring:**
- Log warnings for edge cases (zero fixed costs, high break-even scale, zero variable cost)

---

### Observability

**Logging:**
- Log level: INFO for successful calculation and file write
- Log level: WARN for edge cases (zero costs, ceiling rounding applied, chart scale exceeded)
- Log level: ERROR for invalid price/cost inputs

**Metrics:**
- Calculation execution time
- Chart render execution time
- File append execution time

---

## Dependencies

### Prerequisite Stories

None

### External Dependencies

None

### Technology Dependencies

None — uses Python stdlib (math.ceil) only; no third-party libraries permitted per BR-003

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for business logic

**Test Scenarios:**
1. **Happy Path:** Standard break-even with typical fixed costs, variable cost, and selling price
2. **Edge Cases:**
   - Zero fixed costs (break-even at 0 units)
   - High break-even exceeding default chart scale (auto-scale required)
   - Non-integer break-even units (ceiling rounding applied)
   - Zero variable cost (contribution margin equals selling price)
   - projections.md does not exist (file created on first write)
   - Multiple break-even analyses in same session (each appended as new section)
3. **Error Cases:**
   - Selling price equals variable cost per unit (zero contribution margin — error)
   - Selling price less than variable cost per unit (negative contribution margin — error)
   - Negative selling price (invalid input — error)
   - Negative fixed costs (invalid input — error)

### Integration Tests

**Integration Scenarios:**
1. Full workflow: inputs → calculation → chart → projections.md append
2. Second invocation appends to existing projections.md without overwriting prior sections
3. Error path: invalid inputs halt before any file write

### Test File Locations

```
tests/STORY-550/test_ac1_break_even_calculation.py
tests/STORY-550/test_ac2_ascii_chart.py
tests/STORY-550/test_ac3_projections_output.py
tests/STORY-550/test_ac4_invalid_input_error.py
tests/STORY-550/test_ac5_skill_size_disclosure.py
```

---

## Edge Cases

| Edge Case | Expected Behavior |
|-----------|-------------------|
| Zero fixed costs | Break-even = 0 units, 0 revenue; chart shows lines originating from origin |
| High break-even exceeding chart scale | Chart auto-scales axis to accommodate; note added that scale was adjusted |
| Non-integer break-even units (e.g., 10.3 units) | Display ceiling (11 units) with exact value (10.3) noted |
| Zero variable cost | Contribution margin = selling price; break-even = fixed_costs / selling_price |
| projections.md does not exist | File created with break-even section as first content |
| Multiple analyses in same session | Each analysis appended as a new dated section; prior sections preserved |

---

## Definition of Done

### Implementation
- [ ] Break-even phase added to SKILL.md with total line count remaining below 1,000 lines
- [ ] break-even-analysis.md reference file created with full calculation methodology
- [ ] Break-even formula implementation: units (ceiling), revenue, contribution margin, margin ratio
- [ ] ASCII chart visualization rendering within 80-character terminal width with labeled axes and intersection marker
- [ ] Output appended to projections.md with heading, timestamp, results, chart, assumptions, and disclaimer
- [ ] Error handling for selling price <= variable cost per unit with descriptive message

### Quality
- [ ] All 5 AC passing tests
- [ ] Edge cases covered: zero fixed costs, high break-even, non-integer units, zero variable cost, missing projections.md, multiple sessions
- [ ] NFR-S003 disclaimer compliance verified in every output section
- [ ] Coverage > 95%

### Testing
- [ ] Unit tests for break-even formulas (units, revenue, contribution margin, margin ratio)
- [ ] Unit tests for ASCII chart rendering (dimensions, labels, intersection marker)
- [ ] Unit tests for input validation (price <= variable cost, negative values)
- [ ] Integration test for full workflow (inputs → calculation → chart → file append)
- [ ] Edge case tests for all 6 identified scenarios

### Documentation
- [ ] Reference file (break-even-analysis.md) contains calculation methodology with worked examples
- [ ] Chart rendering specification documented in reference file (80-char width, axis labels, intersection symbol)

---

## Implementation Notes

**Developer:**
**Implemented:**

---

## TDD Workflow

| Phase | Status | Notes |
|-------|--------|-------|
| Phase 01: Pre-Flight | Not Started | |
| Phase 02: Red (Tests) | Not Started | |
| Phase 03: Green (Implementation) | Not Started | |
| Phase 04: Refactor | Not Started | |
| Phase 04.5: AC Verification | Not Started | |
| Phase 05: Integration | Not Started | |
| Phase 05.5: AC Verification | Not Started | |
| Phase 06: Deferral Check | Not Started | |
| Phase 07: DoD Update | Not Started | |
| Phase 08: Git Workflow | Not Started | |
| Phase 09: Feedback | Not Started | |
| Phase 10: Result | Not Started | |

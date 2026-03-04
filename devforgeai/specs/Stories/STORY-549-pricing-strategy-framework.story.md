---
id: STORY-549
title: Pricing Strategy Framework
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

# Story: Pricing Strategy Framework

## Description

**As a** founder or small business owner,
**I want** a guided pricing strategy selection workflow within the managing-finances skill,
**so that** I can choose and document an appropriate pricing model (cost-plus, value-based, or competitive) informed by market research data.

## Provenance

```xml
<provenance>
  <origin document="devforgeai/specs/Epics/EPIC-077-financial-planning-modeling.epic.md" section="features">
    <quote>"Pricing Strategy Framework — guided pricing strategy selection (cost-plus, value-based, competitive) with integration with market research data from EPIC-074 for competitive pricing context"</quote>
    <line_reference>lines 53-58</line_reference>
    <quantified_impact>Founders price products arbitrarily without structured methodology, leading to margin erosion or lost sales</quantified_impact>
  </origin>

  <decision rationale="three-strategy-enumeration-over-single-recommendation">
    <selected>Present all three pricing strategies with guided data collection per strategy and formula-driven output</selected>
    <rejected alternative="single-ai-recommended-price-point">
      Single recommendation rejected — pricing decisions require founder judgment on strategy fit
    </rejected>
    <trade_off>Users must select a strategy and provide inputs rather than receiving a single automated answer</trade_off>
  </decision>

  <stakeholder role="Founder or Small Business Owner" goal="choose-and-document-pricing-model">
    <quote>"Choose and document an appropriate pricing model informed by market research data"</quote>
    <source>EPIC-077, Feature 2</source>
  </stakeholder>

  <hypothesis id="H1" validation="user-feedback" success_criteria="All three pricing strategies produce valid output with disclaimer in 100% of test scenarios">
    Guided pricing strategy selection reduces arbitrary pricing decisions for early-stage founders
  </hypothesis>
</provenance>
```

## Acceptance Criteria

> **IMPORTANT:** XML acceptance criteria format is REQUIRED for automated verification.

### XML Acceptance Criteria Format

### AC#1: Three Pricing Strategies Presented with Mandatory Selection

```xml
<acceptance_criteria id="AC1" implements="SVC-001">
  <given>A founder or small business owner enters the pricing strategy phase of the managing-finances skill</given>
  <when>The workflow begins</when>
  <then>All three pricing strategies (cost-plus, value-based, competitive) are presented with clear descriptions of each approach, and the user must select one strategy before the workflow proceeds to data collection</then>
  <verification>
    <source_files>
      <file hint="Pricing phase entry point">src/claude/skills/managing-finances/SKILL.md</file>
      <file hint="Strategy selection logic">src/claude/skills/managing-finances/references/pricing-strategy-framework.md</file>
    </source_files>
    <test_file>tests/STORY-549/test_ac1_strategy_selection.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Cost-Plus Pricing Collects Inputs, Calculates Price, Displays ASCII Table

```xml
<acceptance_criteria id="AC2" implements="SVC-002">
  <given>A user selects the cost-plus pricing strategy</given>
  <when>The cost-plus workflow executes</when>
  <then>The workflow collects variable cost per unit, fixed cost, expected unit volume, and target margin percentage; calculates Price = (VarCost + FixedCost/Units) × (1 + Margin%); displays the result in an ASCII table showing inputs and calculated price; and includes a "not financial advice" disclaimer prominently in the output</then>
  <verification>
    <source_files>
      <file hint="Cost-plus calculation">src/claude/skills/managing-finances/references/pricing-strategy-framework.md</file>
    </source_files>
    <test_file>tests/STORY-549/test_ac2_cost_plus_calculation.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Competitive Pricing Integrates EPIC-074 Market Research Data

```xml
<acceptance_criteria id="AC3" implements="SVC-003">
  <given>A user selects the competitive pricing strategy and EPIC-074 market research data is available at devforgeai/specs/business/market-research/competitive-landscape.md</given>
  <when>The competitive pricing workflow executes</when>
  <then>The workflow reads and integrates competitor pricing data from the EPIC-074 output file, displays a competitor comparison table with competitor names, their price points, and the user's proposed price, and positions the user's price relative to identified competitors</then>
  <verification>
    <source_files>
      <file hint="Competitive pricing integration">src/claude/skills/managing-finances/references/pricing-strategy-framework.md</file>
    </source_files>
    <test_file>tests/STORY-549/test_ac3_competitive_pricing_integration.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Graceful Degradation When EPIC-074 Market Research Data Unavailable

```xml
<acceptance_criteria id="AC4" implements="BR-003">
  <given>A user selects the competitive pricing strategy and no EPIC-074 market research data file is present or the file is unparseable</given>
  <when>The competitive pricing workflow attempts to read market research data</when>
  <then>The workflow displays a clear message indicating that market research data is unavailable, falls back to a manual entry mode where the user can enter competitor names and price points directly, and continues to completion without error</then>
  <verification>
    <source_files>
      <file hint="Graceful degradation logic">src/claude/skills/managing-finances/references/pricing-strategy-framework.md</file>
    </source_files>
    <test_file>tests/STORY-549/test_ac4_graceful_degradation.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#5: Output Written to pricing-model.md with Required Sections and Disclaimer

```xml
<acceptance_criteria id="AC5" implements="SVC-004">
  <given>A user completes any of the three pricing strategy workflows</given>
  <when>The workflow finalizes</when>
  <then>The output is written atomically to devforgeai/specs/business/financial/pricing-model.md containing: a header with strategy name and date, inputs summary, calculated or selected price point, rationale section, and a prominent "not financial advice" disclaimer; if the file already exists it is overwritten with a backup-safe atomic write</then>
  <verification>
    <source_files>
      <file hint="Output file writer">src/claude/skills/managing-finances/references/pricing-strategy-framework.md</file>
    </source_files>
    <test_file>tests/STORY-549/test_ac5_output_file.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#6: Value-Based Pricing Collects Perceived Value Inputs and Willingness-to-Pay Anchors

```xml
<acceptance_criteria id="AC6" implements="SVC-005">
  <given>A user selects the value-based pricing strategy</given>
  <when>The value-based pricing workflow executes</when>
  <then>The workflow collects perceived value indicators (key benefits, differentiation factors), willingness-to-pay anchors (comparable alternatives, customer segment budget range), and a floor price; uses these inputs to generate a recommended price range with rationale; and includes a "not financial advice" disclaimer in the output</then>
  <verification>
    <source_files>
      <file hint="Value-based pricing logic">src/claude/skills/managing-finances/references/pricing-strategy-framework.md</file>
    </source_files>
    <test_file>tests/STORY-549/test_ac6_value_based_pricing.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### Source Files Guidance

Source files hint the ac-compliance-verifier about implementation locations.

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "managing-finances-skill"
      file_path: "src/claude/skills/managing-finances/SKILL.md"
      interface: "Skill entry point with pricing phase"
      lifecycle: "On-demand"
      dependencies:
        - "pricing-strategy-framework.md reference file"
      requirements:
        - id: "SVC-001"
          description: "Pricing phase entry presenting all three strategies with mandatory selection before proceeding"
          testable: true
          test_requirement: "Test: Strategy selection prompt renders all three options; workflow blocks until selection made"
          priority: "Critical"

    - type: "Configuration"
      name: "pricing-strategy-framework-reference"
      file_path: "src/claude/skills/managing-finances/references/pricing-strategy-framework.md"
      interface: "Progressive disclosure reference with strategy implementations"
      lifecycle: "On-demand"
      dependencies:
        - "managing-finances SKILL.md"
        - "devforgeai/specs/business/market-research/competitive-landscape.md (optional, EPIC-074)"
      requirements:
        - id: "SVC-002"
          description: "Cost-plus calculation: Price = (VarCost + FixedCost/Units) × (1 + Margin%) with ASCII table output"
          testable: true
          test_requirement: "Test: Formula produces correct result for known inputs; ASCII table renders correctly"
          priority: "Critical"
        - id: "SVC-003"
          description: "Competitive pricing reads EPIC-074 output and renders competitor comparison table"
          testable: true
          test_requirement: "Test: Competitor data parsed from file; comparison table rendered with user price positioned"
          priority: "High"
        - id: "SVC-004"
          description: "Output written atomically to devforgeai/specs/business/financial/pricing-model.md with all required sections"
          testable: true
          test_requirement: "Test: File written with correct structure; existing file handled without data loss"
          priority: "Critical"
        - id: "SVC-005"
          description: "Value-based pricing collects perceived value and WTP anchors to generate recommended price range"
          testable: true
          test_requirement: "Test: All required inputs collected; price range generated with rationale"
          priority: "High"

  business_rules:
    - id: "BR-001"
      rule: "All financial outputs must include a 'not financial advice' disclaimer"
      trigger: "Any pricing output generated or written to file"
      validation: "Disclaimer text present in output and in written pricing-model.md"
      error_handling: "Disclaimer absence treated as blocking defect; output suppressed until corrected"
      test_requirement: "Test: Disclaimer present in 100% of outputs across all three strategy paths"
      priority: "Critical"
    - id: "BR-002"
      rule: "Three pricing strategies must be a data-driven enumeration, not hardcoded conditional branches"
      trigger: "Strategy selection phase initialization"
      validation: "Strategy list sourced from enumeration structure in reference file; adding a fourth strategy requires only data change, not code change"
      error_handling: "Structural violation flagged at QA phase"
      test_requirement: "Test: Strategy enumeration structure verifiable; strategy list not hardcoded in SKILL.md"
      priority: "High"
    - id: "BR-003"
      rule: "EPIC-074 market research integration must degrade gracefully when data is unavailable"
      trigger: "Competitive pricing strategy selected"
      validation: "Workflow completes successfully whether or not competitive-landscape.md is present or parseable"
      error_handling: "Missing or unparseable file triggers manual entry fallback; error displayed to user with clear message"
      test_requirement: "Test: Competitive pricing completes with file present; completes with file absent; completes with malformed file"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Prompt cycles and file write within time bounds"
      metric: "Each prompt interaction cycle < 2s; pricing-model.md write completes < 500ms"
      test_requirement: "Test: Timed write operation on pricing-model.md"
      priority: "Medium"
    - id: "NFR-002"
      category: "Security"
      requirement: "Disclaimer present in all outputs; no external network calls; market research file read-only"
      metric: "100% of outputs include disclaimer; zero external HTTP calls; market research file opened read-only"
      test_requirement: "Test: Disclaimer validation on all three strategy outputs; no external call assertions"
      priority: "Critical"
    - id: "NFR-003"
      category: "Reliability"
      requirement: "Atomic writes and graceful fallback on missing market data"
      metric: "pricing-model.md write is atomic (no partial writes on failure); fallback activated on missing or corrupt market data"
      test_requirement: "Test: Simulated write failure leaves no partial file; fallback activates correctly"
      priority: "High"
```

---

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "competitive-pricing-workflow"
    limitation: "Market research integration depends on EPIC-074 outputs at a specific file path; degrades gracefully if file is unavailable or unparseable"
    decision: "workaround:Graceful degradation to manual entry mode when EPIC-074 data is absent"
    discovered_phase: "Architecture"
    impact: "Competitive pricing workflow remains functional without EPIC-074 data, but comparison table is populated from user-entered values rather than automated research"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- Each prompt interaction cycle within the pricing workflow: < 2s
- pricing-model.md file write completion: < 500ms
- ASCII table rendering for cost-plus output: < 100ms
- Competitive landscape file parse (when present): < 300ms

### Security

**Data Protection:**
- No user-entered financial inputs persisted beyond the pricing-model.md output file
- Market research file (competitive-landscape.md) opened read-only at all times
- No external network calls during any pricing strategy workflow
- Disclaimer present in 100% of all generated outputs and written files

### Scalability

**Design:**
- Pricing strategy enumeration supports addition of new strategies with data-only changes (no structural refactoring)
- Reference file under 1,000 lines with progressive disclosure
- Stateless per invocation; no session state maintained between workflow runs

### Reliability

**Error Handling:**
- Atomic write to pricing-model.md: no partial file left on failure
- Graceful degradation on missing, empty, or unparseable competitive-landscape.md
- Zero/negative price result from cost-plus formula triggers warning and blocks file write until user corrects inputs
- Implausible margin percentage (>500%) triggers a confirmation prompt before proceeding

### Observability

**Logging:**
- Log level: INFO for strategy selected, inputs collected, file written
- Log level: WARN for missing market research file, implausible margin, fallback to manual entry
- Structured output with strategy name, input values, and calculated result

---

## Dependencies

### Prerequisite Stories

- [ ] **None blocking** — This story can start immediately
  - **Why:** EPIC-074 market research integration is optional; graceful degradation is built in
  - **Status:** EPIC-074 outputs consumed read-only when present

### External Dependencies

- **EPIC-074 market research outputs** (optional): `devforgeai/specs/business/market-research/competitive-landscape.md`
  - Read-only consumption; absence handled by graceful degradation per AC4

### Technology Dependencies

- None — uses only Markdown and existing DevForgeAI managing-finances skill framework

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for business logic

**Test Scenarios:**
1. **Happy Path — Cost-Plus:** Known inputs produce correct price via formula; ASCII table renders with all columns
2. **Happy Path — Value-Based:** Perceived value and WTP anchors collected; price range generated with rationale
3. **Happy Path — Competitive (with data):** Market research file present and parsed; comparison table rendered
4. **Happy Path — Competitive (without data):** Market research file absent; fallback to manual entry completes without error
5. **Edge Cases:**
   - Multiple strategy selection attempt (only first accepted; workflow does not loop)
   - Zero variable cost input for cost-plus (price still calculated; warning issued)
   - Negative price result from cost-plus (warning displayed; file write blocked)
   - Implausible margin percentage >500% (confirmation prompt before proceeding)
   - pricing-model.md already exists (file overwritten atomically; no data loss)
   - Unparseable market research file (graceful degradation to manual entry)
   - Missing disclaimer in rendered output (treated as blocking defect in test assertion)
6. **Error Cases:**
   - Write failure for pricing-model.md (no partial file; error message displayed)
   - Required input field left blank (workflow re-prompts; does not proceed with empty value)

### Integration Tests

**Coverage Target:** 85%+ for application layer

**Test Scenarios:**
1. **Full Cost-Plus Workflow:** Strategy selection → inputs → calculation → ASCII table → file write → disclaimer verified
2. **Full Value-Based Workflow:** Strategy selection → perceived value inputs → WTP anchors → price range → file write → disclaimer verified
3. **Full Competitive Workflow (data present):** Strategy selection → market data read → comparison table → file write → disclaimer verified
4. **Full Competitive Workflow (data absent):** Strategy selection → fallback message → manual entry → comparison table → file write → disclaimer verified

---

## Acceptance Criteria Verification Checklist

### AC#1: Three Pricing Strategies Presented with Mandatory Selection

- [ ] Cost-plus strategy displayed with description - **Phase:** 2 - **Evidence:** tests/STORY-549/
- [ ] Value-based strategy displayed with description - **Phase:** 2 - **Evidence:** tests/STORY-549/
- [ ] Competitive strategy displayed with description - **Phase:** 2 - **Evidence:** tests/STORY-549/
- [ ] Workflow blocks until user selects one strategy - **Phase:** 2 - **Evidence:** tests/STORY-549/

### AC#2: Cost-Plus Calculation and ASCII Table

- [ ] Variable cost input collected - **Phase:** 2 - **Evidence:** tests/STORY-549/
- [ ] Fixed cost input collected - **Phase:** 2 - **Evidence:** tests/STORY-549/
- [ ] Unit volume input collected - **Phase:** 2 - **Evidence:** tests/STORY-549/
- [ ] Margin percentage input collected - **Phase:** 2 - **Evidence:** tests/STORY-549/
- [ ] Formula Price = (VarCost + FixedCost/Units) × (1 + Margin%) produces correct result - **Phase:** 2 - **Evidence:** tests/STORY-549/
- [ ] ASCII table renders inputs and calculated price - **Phase:** 2 - **Evidence:** tests/STORY-549/
- [ ] Disclaimer present in cost-plus output - **Phase:** 2 - **Evidence:** tests/STORY-549/

### AC#3: Competitive Pricing Integrates EPIC-074 Data

- [ ] competitive-landscape.md read when present - **Phase:** 2 - **Evidence:** tests/STORY-549/
- [ ] Competitor names and price points extracted - **Phase:** 2 - **Evidence:** tests/STORY-549/
- [ ] Comparison table rendered with user price positioned - **Phase:** 2 - **Evidence:** tests/STORY-549/

### AC#4: Graceful Degradation When Market Data Unavailable

- [ ] Clear message when competitive-landscape.md absent - **Phase:** 2 - **Evidence:** tests/STORY-549/
- [ ] Manual entry fallback activates - **Phase:** 2 - **Evidence:** tests/STORY-549/
- [ ] Workflow completes without error on missing file - **Phase:** 2 - **Evidence:** tests/STORY-549/
- [ ] Workflow completes without error on unparseable file - **Phase:** 2 - **Evidence:** tests/STORY-549/

### AC#5: Output Written to pricing-model.md

- [ ] File written to devforgeai/specs/business/financial/pricing-model.md - **Phase:** 2 - **Evidence:** tests/STORY-549/
- [ ] Header with strategy name and date present - **Phase:** 2 - **Evidence:** tests/STORY-549/
- [ ] Inputs summary section present - **Phase:** 2 - **Evidence:** tests/STORY-549/
- [ ] Calculated/selected price point present - **Phase:** 2 - **Evidence:** tests/STORY-549/
- [ ] Rationale section present - **Phase:** 2 - **Evidence:** tests/STORY-549/
- [ ] Disclaimer section present in file - **Phase:** 2 - **Evidence:** tests/STORY-549/
- [ ] Existing file overwritten atomically - **Phase:** 2 - **Evidence:** tests/STORY-549/

### AC#6: Value-Based Pricing Collects Inputs and WTP Anchors

- [ ] Perceived value indicators collected (benefits, differentiation) - **Phase:** 2 - **Evidence:** tests/STORY-549/
- [ ] Willingness-to-pay anchors collected (comparables, budget range) - **Phase:** 2 - **Evidence:** tests/STORY-549/
- [ ] Floor price collected - **Phase:** 2 - **Evidence:** tests/STORY-549/
- [ ] Recommended price range generated with rationale - **Phase:** 2 - **Evidence:** tests/STORY-549/
- [ ] Disclaimer present in value-based output - **Phase:** 2 - **Evidence:** tests/STORY-549/

---

**Checklist Progress:** 0/26 items complete (0%)

---

<!-- IMPLEMENTATION NOTES FORMAT REQUIREMENT -->

## Implementation Notes

*To be filled during /dev workflow*

## Definition of Done

### Implementation
- [ ] Pricing phase added to src/claude/skills/managing-finances/SKILL.md with total file remaining < 1,000 lines
- [ ] pricing-strategy-framework.md reference file created with progressive disclosure and strategy enumeration
- [ ] Cost-plus calculation workflow complete with formula, ASCII table output, and disclaimer
- [ ] Value-based pricing workflow complete with perceived value inputs, WTP anchors, and price range output
- [ ] Competitive pricing workflow complete with EPIC-074 integration and comparison table
- [ ] Graceful degradation implemented for missing or unparseable market research data
- [ ] Output written atomically to devforgeai/specs/business/financial/pricing-model.md with all required sections and disclaimer

### Quality
- [ ] All 6 acceptance criteria have passing tests
- [ ] Edge cases covered (zero/negative price, implausible margin, existing output file, unparseable market data)
- [ ] NFR-002 disclaimer compliance verified across all three strategy paths
- [ ] Code coverage > 95%

### Testing
- [ ] Unit tests for cost-plus formula (test_ac2_cost_plus_calculation.py)
- [ ] Unit tests for value-based pricing logic (test_ac6_value_based_pricing.py)
- [ ] Unit tests for competitive pricing with market data present (test_ac3_competitive_pricing_integration.py)
- [ ] Unit tests for competitive pricing with market data absent (test_ac4_graceful_degradation.py)
- [ ] Integration test for full cost-plus workflow
- [ ] Integration test for full value-based workflow
- [ ] Integration test for full competitive workflow (with and without market data)
- [ ] Edge case tests: zero/negative price, implausible margin, existing pricing-model.md

### Documentation
- [ ] pricing-strategy-framework.md reference file documented with strategy selection guide and progressive disclosure
- [ ] EPIC-074 market data integration path documented in reference file
- [ ] Disclaimer language documented and consistent across all outputs

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
| 2026-03-03 | .claude/story-requirements-analyst | Created | Story created from EPIC-077 Feature 2 | STORY-549-pricing-strategy-framework.story.md |

## Notes

**Design Decisions:**
- Three pricing strategies presented as a data-driven enumeration to support future extensibility without structural refactoring (BR-002)
- EPIC-074 integration is read-only and optional; competitive pricing degrades gracefully to manual entry (TL-001)
- Atomic file writes for pricing-model.md prevent partial output on failure
- Implausible margin (>500%) triggers confirmation rather than silent acceptance to prevent formula errors

**Safety Constraints:**
- "Not financial advice" disclaimer required in 100% of outputs and written files (BR-001)
- Zero or negative calculated price blocks file write until user corrects inputs
- No external network calls during any workflow path

**Maps To:**
- FR-019 (EPIC-077 Feature 2: Pricing Strategy Framework)
- Reads EPIC-074 outputs for competitive pricing context

**Related ADRs:**
- ADR-017: Gerund-Object Naming Convention

**References:**
- EPIC-077: Managing Finances
- EPIC-074: Market Research & Competition (optional integration)

---

Story Template Version: 2.9
Last Updated: 2026-03-03

---
id: STORY-552
title: Funding Options Guide
type: feature
epic: EPIC-077
sprint: Sprint-27
status: Ready for Dev
points: 1
depends_on: []
priority: Medium
advisory: false
source_gap: null
source_story: null
assigned_to: null
created: 2026-03-03
format_version: "2.9"
---

# Story: Funding Options Guide

## Description

**As an** early-stage founder or small business owner,
**I want** a structured decision tree that guides me through funding options based on my business stage, capital needs, and preferences,
**so that** I can identify the most appropriate funding path without requiring prior financial expertise.

## Provenance

```xml
<provenance>
  <origin document="devforgeai/specs/Epics/archive/EPIC-077-funding-financial-planning.epic.md" section="features">
    <quote>"Funding Options Guide — decision tree for funding path selection based on stage, capital need, and equity preference"</quote>
    <line_reference>lines 1-50</line_reference>
    <quantified_impact>Founders waste months pursuing incompatible funding paths due to lack of structured guidance</quantified_impact>
  </origin>

  <decision rationale="educational-guidance-over-prescriptive-advice">
    <selected>Decision tree producing ranked shortlist with rationale and prominent disclaimer</selected>
    <rejected alternative="ai-generated-investor-pitch-or-loan-applications">
      AI-generated funding documents rejected due to liability concern — educational scope only
    </rejected>
    <trade_off>Users receive actionable guidance but must engage licensed professionals for binding financial decisions</trade_off>
  </decision>

  <stakeholder role="Early-Stage Founder" goal="identify-appropriate-funding-path">
    <quote>"Identify most appropriate funding path without prior financial expertise"</quote>
    <source>EPIC-077, Managing Finances feature set</source>
  </stakeholder>

  <hypothesis id="H1" validation="user-feedback" success_criteria="Decision tree produces ranked shortlist in 100% of valid input combinations">
    Structured funding guidance reduces misaligned funding pursuit for early-stage founders
  </hypothesis>
</provenance>
```

## Acceptance Criteria

Define testable, specific conditions that must be met for story completion. Use XML format with `<acceptance_criteria>` blocks for machine-parseable verification.

> **IMPORTANT:** XML acceptance criteria format is REQUIRED for automated verification by the ac-compliance-verifier subagent.

### XML Acceptance Criteria Format

Use the following XML schema for each acceptance criterion.

### AC#1: Decision Tree Produces Ranked Shortlist Based on Inputs

```xml
<acceptance_criteria id="AC1" implements="SVC-001">
  <given>A user has invoked the managing-finances skill and selected the funding options workflow</given>
  <when>The user provides their business stage, capital need amount, and equity preference (willing/unwilling to give equity)</when>
  <then>The system evaluates inputs through the decision tree and produces a ranked shortlist of funding options with rationale for each ranking and a prominent disclaimer stating educational-only scope both at the top and bottom of the output</then>
  <verification>
    <source_files>
      <file hint="Decision tree workflow and funding type definitions">src/claude/skills/managing-finances/references/funding-options-guide.md</file>
    </source_files>
    <test_file>tests/STORY-552/test_ac1_decision_tree_ranked_shortlist.py</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Equity Funding Path Includes Dilution, Control, Timeline, and Referral Trigger

```xml
<acceptance_criteria id="AC2" implements="SVC-001,BR-001">
  <given>The decision tree routes to an equity funding recommendation (VC or angel investment)</given>
  <when>The system produces output for that funding type</when>
  <then>The output includes: (1) dilution explanation showing how equity stake is reduced, (2) board and control implications describing governance impact, (3) typical funding timeline in weeks or months, and (4) a professional referral trigger block naming a financial advisor or attorney as the recommended professional type</then>
  <verification>
    <source_files>
      <file hint="Equity funding branch content">src/claude/skills/managing-finances/references/funding-options-guide.md</file>
    </source_files>
    <test_file>tests/STORY-552/test_ac2_equity_funding_path.py</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Bootstrapping and Grants Path Includes Pros/Cons and Grant Eligibility Signals Without Referral Trigger

```xml
<acceptance_criteria id="AC3" implements="SVC-001,BR-002">
  <given>The decision tree routes to a bootstrapping or grants funding recommendation</given>
  <when>The system produces output for that funding type</when>
  <then>The output includes: (1) a pros/cons list specific to bootstrapping or grants, (2) grant eligibility signals (e.g., industry sector, geography, business age, founder demographics) when the grants branch is selected, and (3) no professional referral trigger block is present — this path is within educational guidance scope</then>
  <verification>
    <source_files>
      <file hint="Bootstrapping and grants branch content">src/claude/skills/managing-finances/references/funding-options-guide.md</file>
    </source_files>
    <test_file>tests/STORY-552/test_ac3_bootstrapping_grants_path.py</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Output Written to funding-strategy.md with Valid Markdown, All 5 Funding Types, Dual Disclaimer, and Source Reference

```xml
<acceptance_criteria id="AC4" implements="SVC-002,NFR-S003">
  <given>The decision tree session is complete and a ranked shortlist has been generated</given>
  <when>The system writes the output artifact</when>
  <then>The file is written to devforgeai/specs/business/financial/funding-strategy.md with: (1) valid Markdown syntax throughout, (2) all 5 funding types documented (Bootstrapping, Grants, Angel Investment, Venture Capital, Debt/Loans), (3) the standard educational disclaimer appearing as the first section and again as the last section of the file, and (4) a reference line citing src/claude/skills/managing-finances/references/funding-options-guide.md as the authoritative source</then>
  <verification>
    <source_files>
      <file hint="Output artifact">devforgeai/specs/business/financial/funding-strategy.md</file>
      <file hint="Reference source">src/claude/skills/managing-finances/references/funding-options-guide.md</file>
    </source_files>
    <test_file>tests/STORY-552/test_ac4_output_artifact.py</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#5: Boundary and Ambiguous Results Show Comparison Table with Explanation

```xml
<acceptance_criteria id="AC5" implements="SVC-003,BR-003">
  <given>The decision tree receives conflicting or ambiguous inputs that produce no clear top-ranked funding option (e.g., high capital need with no equity and no debt preference, unknown grant eligibility, pre-idea stage)</given>
  <when>The system evaluates those boundary inputs</when>
  <then>The system produces a comparison table listing all applicable funding types with scores or suitability ratings across key dimensions, accompanied by a plain-language explanation of why inputs produced ambiguous results and guidance on which inputs to reconsider</then>
  <verification>
    <source_files>
      <file hint="Boundary case handling logic">src/claude/skills/managing-finances/references/funding-options-guide.md</file>
    </source_files>
    <test_file>tests/STORY-552/test_ac5_boundary_ambiguous_results.py</test_file>
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
      name: "managing-finances-funding-options-guide"
      file_path: "src/claude/skills/managing-finances/references/funding-options-guide.md"
      interface: "Decision tree reference file"
      lifecycle: "On-demand"
      dependencies:
        - "managing-finances SKILL.md"
      requirements:
        - id: "SVC-001"
          description: "Decision tree covering all 5 funding types with inputs: business stage, capital need, equity preference"
          testable: true
          test_requirement: "Test: All 5 funding type branches present and reachable from decision tree entry point"
          priority: "Critical"
        - id: "SVC-002"
          description: "Output artifact written to funding-strategy.md with dual disclaimer and source reference"
          testable: true
          test_requirement: "Test: Output file exists at correct path with disclaimer as first and last section and source reference present"
          priority: "Critical"
        - id: "SVC-003"
          description: "Boundary case comparison table produced when inputs are conflicting or ambiguous"
          testable: true
          test_requirement: "Test: Comparison table present in output for each defined boundary scenario"
          priority: "High"

  business_rules:
    - id: "BR-001"
      rule: "Equity funding paths (VC and angel) must always include dilution explanation, board/control implications, timeline, and professional referral trigger"
      trigger: "Decision tree routes to VC or angel investment branch"
      validation: "Output contains all four required elements for equity paths"
      error_handling: "Regenerate equity branch output if any required element is missing"
      test_requirement: "Test: VC and angel branches each independently produce all four required elements"
      priority: "Critical"
    - id: "BR-002"
      rule: "Bootstrapping and grants paths must not include a professional referral trigger block"
      trigger: "Decision tree routes to bootstrapping or grants branch"
      validation: "Output does not contain professional referral trigger language for these paths"
      error_handling: "Remove referral trigger if erroneously included in bootstrapping/grants output"
      test_requirement: "Test: Bootstrapping and grants output verified to be free of referral trigger language"
      priority: "Critical"
    - id: "BR-003"
      rule: "Boundary and ambiguous results must produce a comparison table with suitability ratings and plain-language explanation"
      trigger: "No clear top-ranked funding option can be determined from inputs"
      validation: "Output contains comparison table and explanation paragraph"
      error_handling: "Fall back to full comparison table when boundary condition is detected"
      test_requirement: "Test: Each defined edge case scenario produces comparison table with explanation"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-P001"
      category: "Performance"
      requirement: "Decision tree traversal completes within acceptable time"
      metric: "Full decision tree traversal < 3 seconds end-to-end"
      test_requirement: "Test: Timed execution of decision tree traversal stays under 3 seconds"
      priority: "High"
    - id: "NFR-S001"
      category: "Security"
      requirement: "Output file size bounded to prevent runaway generation"
      metric: "funding-strategy.md output < 150KB"
      test_requirement: "Test: Output file size assertion < 150KB after generation"
      priority: "High"
    - id: "NFR-S002"
      category: "Security"
      requirement: "No personally identifiable information (PII) persisted in output"
      metric: "Output file contains no names, addresses, SSNs, or financial account numbers"
      test_requirement: "Test: PII pattern scan on output returns zero matches"
      priority: "Critical"
    - id: "NFR-S003"
      category: "Compliance"
      requirement: "Educational disclaimer appears as first section and last section of every output artifact"
      metric: "100% of output writes include disclaimer at position 1 and position N (last section)"
      test_requirement: "Test: Output file first section and last section match verbatim disclaimer text"
      priority: "Critical"
```

---

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "managing-finances funding-options-guide reference"
    limitation: "Decision tree covers 5 funding types only: Bootstrapping, Grants, Angel Investment, Venture Capital, Debt/Loans — additional funding types (e.g., crowdfunding, revenue-based financing) are not modelled"
    decision: "workaround:Additional funding types require update to funding-options-guide.md reference file before they can appear in decision tree output"
    discovered_phase: "Architecture"
    impact: "Founders seeking non-standard funding paths will not receive tailored guidance — comparison table fallback applies"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- Decision tree traversal (inputs through ranked shortlist): < 3 seconds end-to-end
- Per-question response: < 500ms per step (p95)

**Throughput:**
- Single-user CLI tool — concurrent user support not required

### Security

**Authentication:**
- None (CLI-local tool)

**Data Protection:**
- No user-provided input is persisted or logged with PII
- No financial account numbers, names, or SSNs in output
- Disclaimer appears as first and last section of every output artifact

**Security Testing:**
- [x] No hardcoded secrets
- [x] Proper input validation (bucketed inputs only — stage, capital tier, equity preference)
- [x] PII pattern exclusion from output

### Scalability

**Design:**
- Stateless per invocation — no shared state between sessions
- Progressive disclosure: funding type details in reference file, not inline in skill
- Reference file architecture supports adding new funding types without skill modification (TL-001 constraint applies)

### Reliability

**Error Handling:**
- All file I/O failures produce specific, human-readable error messages
- Boundary/ambiguous inputs always produce comparison table — no dead ends
- Decision tree reaches terminal state for every valid input combination

### Observability

**Logging:**
- Log level: INFO for session start/end, WARN for boundary condition detected, ERROR for I/O failures
- Structured output with session correlation

---

## Dependencies

### Prerequisite Stories

- [ ] **None** — This story can start immediately
  - **Why:** Standalone reference file creation with no upstream story dependency
  - **Status:** N/A

### External Dependencies

- None

### Technology Dependencies

- None — uses only Markdown and existing DevForgeAI managing-finances skill framework

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for business logic

**Test Scenarios:**
1. **Happy Path:** User provides valid business stage, capital need, and equity preference — receives ranked shortlist with rationale and dual disclaimer
2. **Edge Cases:**
   - Conflicting preferences (high capital need + no equity + no debt) — comparison table produced
   - Unknown grant eligibility — grants branch notes eligibility uncertainty
   - Pre-idea founder (no business stage selected) — boundary comparison table produced
   - Loan path with no credit or collateral signal — debt branch notes limitations
   - Existing funding-strategy.md output file — file is overwritten without error
3. **Error Cases:**
   - Invalid input bucket value for business stage
   - Invalid capital tier input
   - Output path write failure

### Integration Tests

**Coverage Target:** 85%+ for application layer

**Test Scenarios:**
1. **End-to-End Decision Tree Flow:** Complete session from invocation through all 5 funding type branches to output artifact
2. **Professional Referral Coverage:** VC and angel branches both independently trigger referral block
3. **No-Referral Coverage:** Bootstrapping and grants branches verified referral-free
4. **Boundary Coverage:** All defined edge case inputs produce comparison table

---

## Acceptance Criteria Verification Checklist

**Purpose:** Real-time progress tracking during TDD implementation.

**Tracking Mechanisms:**
- **TodoWrite:** Phase-level tracking
- **AC Checklist:** AC sub-item tracking ← YOU ARE HERE
- **Definition of Done:** Official completion record

### AC#1: Decision Tree Produces Ranked Shortlist Based on Inputs

- [ ] Decision tree accepts business stage input - **Phase:** 2 - **Evidence:** tests/STORY-552/
- [ ] Decision tree accepts capital need input - **Phase:** 2 - **Evidence:** tests/STORY-552/
- [ ] Decision tree accepts equity preference input - **Phase:** 2 - **Evidence:** tests/STORY-552/
- [ ] Ranked shortlist produced with rationale - **Phase:** 2 - **Evidence:** tests/STORY-552/
- [ ] Disclaimer present at top of output - **Phase:** 2 - **Evidence:** tests/STORY-552/
- [ ] Disclaimer present at bottom of output - **Phase:** 2 - **Evidence:** tests/STORY-552/

### AC#2: Equity Funding Path Includes Dilution, Control, Timeline, and Referral Trigger

- [ ] Dilution explanation present in VC branch - **Phase:** 2 - **Evidence:** tests/STORY-552/
- [ ] Board/control implications present in VC branch - **Phase:** 2 - **Evidence:** tests/STORY-552/
- [ ] Timeline present in VC branch - **Phase:** 2 - **Evidence:** tests/STORY-552/
- [ ] Professional referral trigger present in VC branch - **Phase:** 2 - **Evidence:** tests/STORY-552/
- [ ] All four elements present in angel investment branch - **Phase:** 2 - **Evidence:** tests/STORY-552/

### AC#3: Bootstrapping and Grants Path Includes Pros/Cons and Grant Eligibility Signals Without Referral Trigger

- [ ] Pros/cons list present in bootstrapping branch - **Phase:** 2 - **Evidence:** tests/STORY-552/
- [ ] Pros/cons list present in grants branch - **Phase:** 2 - **Evidence:** tests/STORY-552/
- [ ] Grant eligibility signals present in grants branch - **Phase:** 2 - **Evidence:** tests/STORY-552/
- [ ] No referral trigger in bootstrapping branch - **Phase:** 2 - **Evidence:** tests/STORY-552/
- [ ] No referral trigger in grants branch - **Phase:** 2 - **Evidence:** tests/STORY-552/

### AC#4: Output Written to funding-strategy.md with Valid Markdown, All 5 Funding Types, Dual Disclaimer, and Source Reference

- [ ] File written to funding-strategy.md - **Phase:** 2 - **Evidence:** tests/STORY-552/
- [ ] Valid Markdown syntax throughout - **Phase:** 2 - **Evidence:** tests/STORY-552/
- [ ] All 5 funding types documented - **Phase:** 2 - **Evidence:** tests/STORY-552/
- [ ] Disclaimer is first section of file - **Phase:** 2 - **Evidence:** tests/STORY-552/
- [ ] Disclaimer is last section of file - **Phase:** 2 - **Evidence:** tests/STORY-552/
- [ ] Source reference line present - **Phase:** 2 - **Evidence:** tests/STORY-552/

### AC#5: Boundary and Ambiguous Results Show Comparison Table with Explanation

- [ ] Conflicting preferences produce comparison table - **Phase:** 2 - **Evidence:** tests/STORY-552/
- [ ] Pre-idea stage produces comparison table - **Phase:** 2 - **Evidence:** tests/STORY-552/
- [ ] Unknown grant eligibility handled gracefully - **Phase:** 2 - **Evidence:** tests/STORY-552/
- [ ] Comparison table includes suitability ratings - **Phase:** 2 - **Evidence:** tests/STORY-552/
- [ ] Plain-language explanation accompanies comparison table - **Phase:** 2 - **Evidence:** tests/STORY-552/

---

**Checklist Progress:** 0/27 items complete (0%)

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
- [ ] funding-options-guide.md reference file created at src/claude/skills/managing-finances/references/funding-options-guide.md
- [ ] Decision tree covers all 5 funding types: Bootstrapping, Grants, Angel Investment, Venture Capital, Debt/Loans
- [ ] Professional referral triggers for complex funding (VC and angel branches)
- [ ] Bootstrapping and grants path without referral triggers
- [ ] Output to funding-strategy.md with dual disclaimer (first and last section)
- [ ] Boundary case comparison table for conflicting/ambiguous inputs

### Quality
- [ ] All 5 AC passing tests
- [ ] Edge cases covered (conflicting preferences, unknown eligibility, pre-idea, no collateral, existing output file)
- [ ] NFR-S003 dual disclaimer compliance verified
- [ ] Coverage > 95%

### Testing
- [ ] Unit tests for decision tree traversal (test_ac1_decision_tree_ranked_shortlist.py)
- [ ] Unit tests for equity funding branch elements (test_ac2_equity_funding_path.py)
- [ ] Unit tests for bootstrapping/grants path and referral absence (test_ac3_bootstrapping_grants_path.py)
- [ ] Integration test for full workflow output artifact (test_ac4_output_artifact.py)
- [ ] Edge case tests for boundary/ambiguous inputs (test_ac5_boundary_ambiguous_results.py)

### Documentation
- [ ] Reference file self-documented with decision tree logic
- [ ] Funding type descriptions complete for all 5 types

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
| 2026-03-03 | opus | Created | Story created for EPIC-077 Funding Options Guide feature | STORY-552-funding-options-guide.story.md |

## Notes

**Design Decisions:**
- Decision inputs kept to three dimensions (business stage, capital need, equity preference) to minimize decision fatigue
- Bucketed inputs (not free-text) for deterministic decision tree traversal
- Equity paths (VC/angel) always trigger professional referral — complexity exceeds educational scope
- Bootstrapping and grants paths intentionally referral-free — within educational guidance scope
- Dual disclaimer (first and last) mirrors legal/compliance skill pattern from STORY-544

**Safety Constraints:**
- Educational guidance ONLY — never prescriptive financial or investment advice
- "Consider" and "may be suitable" language, not "you should invest" language
- Dual disclaimer mandatory on every output artifact (NFR-S003)
- No PII in output (NFR-S002)
- Output bounded to < 150KB (NFR-S001)

**Related ADRs:**
- ADR-017: Gerund-Object Naming Convention

**References:**
- EPIC-077: Managing Finances
- STORY-544: Business Structure Decision Tree (structural pattern reference)
- TL-001: Decision tree covers 5 funding types only

---

Story Template Version: 2.9
Last Updated: 2026-03-03

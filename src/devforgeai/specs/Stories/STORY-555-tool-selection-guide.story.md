---
id: STORY-555
title: Tool Selection Guide
type: feature
epic: EPIC-078
sprint: Sprint-28
status: Ready for Dev
points: 2
depends_on: []
priority: High
advisory: false
source_gap: null
source_story: null
assigned_to: null
created: 2026-03-03
format_version: "2.9"
---

# Story: Tool Selection Guide

## Description

**As a** solo developer selecting tools for my new business,
**I want** a budget-aware guided workflow that compares and recommends tools across CRM, payments, analytics, communication, and project management categories,
**so that** I can build a coherent tool stack that fits my current stage without overspending or choosing tools I will outgrow immediately.

## Provenance

```xml
<provenance>
  <origin document="devforgeai/specs/Epics/EPIC-078-operations-launch.epic.md" section="feature-2">
    <quote>"Guided workflow for selecting business tools: CRM, payment processing, analytics, communication, project management"</quote>
    <line_reference>lines 50-55</line_reference>
    <quantified_impact>Budget-aware recommendations across 5 tool categories with 3 budget tiers</quantified_impact>
  </origin>
</provenance>
```

## Acceptance Criteria

### XML Acceptance Criteria Format

### AC#1: Budget-Aware Recommendations

```xml
<acceptance_criteria id="AC1" implements="TOOLS-001">
  <given>a user initiates the tool selection workflow and provides their monthly budget range (free, under $50, $50-$200, over $200)</given>
  <when>the skill generates tool recommendations</when>
  <then>all recommended tools for each category fall within the specified budget tier, with free-tier options shown first when budget is "free", and each recommendation includes: tool name, pricing for that tier, key features (3-5 bullet points), and a one-line "best for" summary</then>
  <verification>
    <source_files>
      <file hint="budget-tier recommendation tables">src/claude/skills/operating-business/references/tool-selection-guide.md</file>
    </source_files>
    <test_file>tests/STORY-555/test-ac1-budget-aware-recommendations.md</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#2: ASCII Table Format

```xml
<acceptance_criteria id="AC2" implements="TOOLS-002">
  <given>tool recommendations have been generated for any budget tier</given>
  <when>the comparison tables are rendered</when>
  <then>tables are formatted in terminal-compatible ASCII using pipe-and-dash syntax with a maximum column width of 30 characters to prevent line wrapping in 80-character terminals, covering all five categories</then>
  <verification>
    <source_files>
      <file hint="ASCII table format specification">src/claude/skills/operating-business/references/tool-selection-guide.md</file>
    </source_files>
    <test_file>tests/STORY-555/test-ac2-ascii-table-format.md</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Tool Stack Output

```xml
<acceptance_criteria id="AC3" implements="TOOLS-003">
  <given>a user has reviewed recommendations and selected tools for each category</given>
  <when>the tool selection workflow completes</when>
  <then>devforgeai/specs/business/operations/tool-stack.md is created containing: selected tool per category, chosen pricing tier, monthly cost estimate, integration notes, and total estimated monthly cost summary</then>
  <verification>
    <source_files>
      <file hint="output file structure">src/claude/skills/operating-business/references/tool-selection-guide.md</file>
    </source_files>
    <test_file>tests/STORY-555/test-ac3-tool-stack-output.md</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Side-by-Side Comparison

```xml
<acceptance_criteria id="AC4" implements="TOOLS-004">
  <given>a user is evaluating tools in a specific category</given>
  <when>they request a deeper comparison between two specific tools</when>
  <then>the skill presents a side-by-side ASCII comparison table covering: pricing, key features, free trial availability, API access, and known limitations</then>
  <verification>
    <source_files>
      <file hint="side-by-side comparison format">src/claude/skills/operating-business/references/tool-selection-guide.md</file>
    </source_files>
    <test_file>tests/STORY-555/test-ac4-side-by-side-comparison.md</test_file>
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
      name: "tool-selection-guide.md"
      file_path: "src/claude/skills/operating-business/references/tool-selection-guide.md"
      required_keys:
        - key: "categories"
          type: "array"
          example: "[CRM, payment processing, analytics, communication, project management]"
          required: true
          validation: "All 5 categories present"
          test_requirement: "Test: Verify all 5 tool categories documented"
        - key: "budget_tiers"
          type: "array"
          example: "[free, under $50, $50-$200, over $200]"
          required: true
          validation: "All 4 budget tiers present"
          test_requirement: "Test: Verify all 4 budget tiers have recommendations"
        - key: "last_verified"
          type: "string"
          example: "2026-03-03"
          required: true
          validation: "ISO date format"
          test_requirement: "Test: Verify last-verified date exists per tool entry"

  business_rules:
    - id: "BR-001"
      rule: "Recommendations filtered by user's budget tier"
      trigger: "When user provides budget range"
      validation: "All displayed tools within budget tier"
      error_handling: "If no tools at tier, show closest paid options with minimum pricing"
      test_requirement: "Test: Free tier shows only free-tier tools"
      priority: "High"
    - id: "BR-002"
      rule: "ASCII tables fit 80-character terminal width"
      trigger: "When comparison tables rendered"
      validation: "Max column width 30 characters, no line wrapping"
      error_handling: "Truncate long values with ellipsis"
      test_requirement: "Test: No table row exceeds 80 characters"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Reference file within size constraints"
      metric: "< 1,000 lines"
      test_requirement: "Test: wc -l tool-selection-guide.md < 1000"
      priority: "High"
```

---

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "Tool Pricing Data"
    limitation: "Tool pricing may become outdated as vendors change plans"
    decision: "workaround:Include last-verified date per entry and disclaimer to verify current pricing"
    discovered_phase: "Architecture"
    impact: "Users must verify pricing before committing"
```

---

## Non-Functional Requirements (NFRs)

### Performance
- Initial recommendations for all 5 categories: < 10 seconds
- ASCII table rendering: < 1 second per table
- Reference file: < 1,000 lines

### Security
- No payment credentials captured in tool stack output
- Recommendation data sourced only from reference file (no live web requests)

### Scalability
- New tools added by appending entries to reference file
- New categories added via new section without restructuring

### Reliability
- Tables render correctly on 80-character minimum width terminals
- Auto-create output directory if missing
- Versioned "last-verified" date per tool entry

### Observability
- Log category selections and budget tier

---

## Dependencies

### Prerequisite Stories
- No blocking prerequisites

### External Dependencies
- None

### Technology Dependencies
- No new packages required

---

## Test Strategy

### Unit Tests
**Coverage Target:** 95%+
1. **Happy Path:** Full workflow with free tier budget
2. **Edge Cases:** Unknown tool, budget change mid-workflow, category skip, all tools over budget
3. **Error Cases:** Missing output directory

### Integration Tests
**Coverage Target:** 85%+
1. Full tool selection workflow end-to-end
2. ASCII table rendering validation

---

## Acceptance Criteria Verification Checklist

### AC#1: Budget-Aware Recommendations
- [ ] Free tier shows free tools first - **Phase:** 2 - **Evidence:** tests/STORY-555/
- [ ] Each recommendation has name, pricing, features, best-for - **Phase:** 2

### AC#2: ASCII Table Format
- [ ] Pipe-and-dash table syntax used - **Phase:** 2
- [ ] No line exceeds 80 characters - **Phase:** 2

### AC#3: Tool Stack Output
- [ ] tool-stack.md created with all required fields - **Phase:** 2
- [ ] Total monthly cost summary present - **Phase:** 2

### AC#4: Side-by-Side Comparison
- [ ] Two-tool comparison table rendered - **Phase:** 2

---

**Checklist Progress:** 0/7 items complete (0%)

---

<!-- IMPLEMENTATION NOTES FORMAT REQUIREMENT -->

## Implementation Notes

*To be filled during /dev workflow*

## Definition of Done

### Implementation
- [ ] Reference file tool-selection-guide.md created with 5 categories and 4 budget tiers
- [ ] ASCII table rendering with 80-char terminal compatibility
- [ ] Side-by-side comparison capability
- [ ] Output file generation to tool-stack.md with cost summary

### Quality
- [ ] All 4 acceptance criteria have passing tests
- [ ] Edge cases covered
- [ ] Reference file < 1,000 lines

### Testing
- [ ] Unit tests for budget-aware filtering
- [ ] Unit tests for ASCII table format
- [ ] Integration tests for full workflow

### Documentation
- [ ] Reference file includes tool last-verified dates

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
| 2026-03-03 | .claude/story-requirements-analyst | Created | Story created from EPIC-078 Feature 2 | STORY-555.story.md |

## Notes

**Edge Cases:**
1. User's preferred tool not in list → allow manual entry
2. Budget changes mid-workflow → re-run remaining categories at new tier
3. Category not applicable → mark as "not needed"
4. All tools over budget → show closest paid options with minimum pricing

---

Story Template Version: 2.9
Last Updated: 2026-03-03

---
id: STORY-535
title: Market Sizing Guided Workflow
type: feature
epic: EPIC-074
sprint: Sprint-24
status: Ready for Dev
points: 3
depends_on: []
priority: High
advisory: false
source_gap: null
source_story: null
assigned_to: DevForgeAI AI Agent
created: 2026-03-03
format_version: "2.9"
---

# Story: Market Sizing Guided Workflow

## Description

**As a** solo founder or early-stage entrepreneur using DevForgeAI,
**I want** a guided TAM/SAM/SOM market sizing workflow that researches real market data and adapts questions to my business knowledge level,
**so that** I can produce credible, data-backed market size estimates for my business plan without needing a market research background.

## Provenance

```xml
<provenance>
  <origin document="BRAINSTORM-011" section="business-skills-framework">
    <quote>"Enable DevForgeAI users to validate their business ideas through structured market research and competitive analysis before investing significant time and resources."</quote>
    <line_reference>EPIC-074, lines 22-24</line_reference>
    <quantified_impact>Market sizing skill generates TAM/SAM/SOM estimates with cited data sources</quantified_impact>
  </origin>
  <decision rationale="fermi-estimation-with-web-research">
    <selected>Combine internet-sleuth web research with Fermi estimation methodology for market sizing</selected>
    <rejected alternative="manual-only-estimation">
      Pure manual estimation without web research produces lower confidence estimates
    </rejected>
    <trade_off>Depends on internet-sleuth availability; fallback to pure Fermi when unavailable</trade_off>
  </decision>
  <stakeholder role="Entrepreneur" goal="validate-market-size">
    <quote>"Is my market big enough?"</quote>
    <source>EPIC-074, line 24</source>
  </stakeholder>
  <hypothesis id="H1" validation="structural-test" success_criteria="Output contains TAM/SAM/SOM with cited sources">
    Users can produce credible market size estimates using guided workflow
  </hypothesis>
</provenance>
```

## Acceptance Criteria

Define testable, specific conditions that must be met for story completion. Use XML format with `<acceptance_criteria>` blocks for machine-parseable verification.

> **IMPORTANT:** XML acceptance criteria format is REQUIRED for automated verification by the ac-compliance-verifier subagent. Legacy markdown format (Given/When/Then bullets) is NOT supported by verification tools.

### XML Acceptance Criteria Format

Use the following XML schema for each acceptance criterion:

```xml
<acceptance_criteria id="AC1" implements="COMP-XXX,COMP-YYY">
  <given>Initial context or precondition</given>
  <when>Action or event being tested</when>
  <then>Expected outcome or result</then>
  <verification>
    <source_files>
      <file hint="Main implementation">path/to/source.py</file>
    </source_files>
    <test_file>path/to/test.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

### AC#1: TAM/SAM/SOM Output Structure

```xml
<acceptance_criteria id="AC1" implements="SVC-001">
  <given>A user has completed the market sizing workflow</given>
  <when>The workflow writes the output file</when>
  <then>devforgeai/specs/business/market-research/market-sizing.md contains all three tiers (TAM, SAM, SOM) with dollar-value estimates, methodology notes (top-down, bottom-up, or Fermi), data sources cited, and confidence levels (High/Medium/Low) for each tier</then>
  <verification>
    <source_files>
      <file hint="Market sizing skill">src/claude/skills/researching-market/SKILL.md</file>
      <file hint="Methodology reference">src/claude/skills/researching-market/references/market-sizing-methodology.md</file>
    </source_files>
    <test_file>tests/STORY-535/test_ac1_market_sizing_output.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Internet-Sleuth Integration for Market Data

```xml
<acceptance_criteria id="AC2" implements="SVC-002">
  <given>The user provides a target market description (industry, geography, customer segment)</given>
  <when>The workflow needs market data (industry revenue, growth rates, competitor counts)</when>
  <then>The internet-sleuth subagent is invoked to gather external data, and at least 2 external data points are incorporated into the final estimates with source attribution</then>
  <verification>
    <source_files>
      <file hint="Market sizing skill">src/claude/skills/researching-market/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-535/test_ac2_internet_sleuth_integration.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Adaptive Question Depth Based on User Profile

```xml
<acceptance_criteria id="AC3" implements="SVC-003">
  <given>A user profile exists at devforgeai/specs/business/user-profile.md with a business_knowledge field (beginner/intermediate/advanced)</given>
  <when>The workflow starts</when>
  <then>Beginner users receive explanatory context before each question (what TAM/SAM/SOM means, why it matters), intermediate users receive standard prompts, and advanced users receive abbreviated prompts with option to input known figures directly</then>
  <verification>
    <source_files>
      <file hint="Market sizing skill">src/claude/skills/researching-market/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-535/test_ac3_adaptive_questions.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Guided Progressive Disclosure via AskUserQuestion

```xml
<acceptance_criteria id="AC4" implements="SVC-004">
  <given>The workflow is executing</given>
  <when>User input is needed (target market, geographic scope, pricing assumptions, serviceable segment filters)</when>
  <then>The skill uses the AskUserQuestion tool for each interaction with clear options/descriptions, and questions are presented sequentially (not all at once)</then>
  <verification>
    <source_files>
      <file hint="Market sizing skill">src/claude/skills/researching-market/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-535/test_ac4_progressive_disclosure.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#5: Skill File Structure Compliance

```xml
<acceptance_criteria id="AC5" implements="SVC-005">
  <given>The skill is implemented at src/claude/skills/researching-market/</given>
  <when>The skill files are inspected</when>
  <then>The main SKILL.md is under 1,000 lines with YAML frontmatter, market sizing methodology is in references/market-sizing-methodology.md, and Fermi estimation guidance is in references/fermi-estimation.md</then>
  <verification>
    <source_files>
      <file hint="Main skill file">src/claude/skills/researching-market/SKILL.md</file>
      <file hint="Market sizing reference">src/claude/skills/researching-market/references/market-sizing-methodology.md</file>
      <file hint="Fermi estimation reference">src/claude/skills/researching-market/references/fermi-estimation.md</file>
    </source_files>
    <test_file>tests/STORY-535/test_ac5_skill_structure.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### Source Files Guidance

The `<source_files>` element provides hints to the ac-compliance-verifier about where implementation code is located.

**When to Include Source Files:**
- For ACs that modify or create specific files
- When implementation spans multiple files
- When verification needs to locate test coverage targets

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Service"
      name: "MarketSizingWorkflow"
      file_path: "src/claude/skills/researching-market/SKILL.md"
      interface: "Skill"
      lifecycle: "On-demand"
      dependencies:
        - "internet-sleuth subagent"
        - "AskUserQuestion tool"
        - "Read/Write native tools"
      requirements:
        - id: "SVC-001"
          description: "Generate TAM/SAM/SOM output with dollar estimates, methodology, sources, and confidence levels"
          testable: true
          test_requirement: "Test: Output file contains ## TAM, ## SAM, ## SOM sections with dollar values, methodology notes, source citations, and confidence levels"
          priority: "Critical"
        - id: "SVC-002"
          description: "Invoke internet-sleuth subagent for market data gathering with at least 2 external data points"
          testable: true
          test_requirement: "Test: Workflow invokes internet-sleuth and output contains at least 2 cited external data sources"
          priority: "High"
        - id: "SVC-003"
          description: "Adapt question depth based on user profile business_knowledge level (beginner/intermediate/advanced)"
          testable: true
          test_requirement: "Test: Beginner receives explanatory context, intermediate receives standard prompts, advanced receives abbreviated prompts"
          priority: "High"
        - id: "SVC-004"
          description: "Use AskUserQuestion for all user interactions with clear options and sequential presentation"
          testable: true
          test_requirement: "Test: All user inputs collected via AskUserQuestion with descriptive options"
          priority: "High"
        - id: "SVC-005"
          description: "Skill file structure complies with framework constraints (SKILL.md < 1000 lines, references in subdirectory)"
          testable: true
          test_requirement: "Test: SKILL.md line count < 1000, references/market-sizing-methodology.md exists, references/fermi-estimation.md exists"
          priority: "Critical"

    - type: "Configuration"
      name: "market-sizing-output"
      file_path: "devforgeai/specs/business/market-research/market-sizing.md"
      required_keys:
        - key: "TAM"
          type: "object"
          example: "{value: '$2.5B', methodology: 'top-down', confidence: 'Medium', sources: ['...']}"
          required: true
          validation: "Must contain value, methodology, confidence, and sources fields"
          test_requirement: "Test: TAM section has all required fields with valid values"
        - key: "SAM"
          type: "object"
          example: "{value: '$400M', methodology: 'bottom-up', confidence: 'Medium', sources: ['...']}"
          required: true
          validation: "SAM value must be <= TAM value"
          test_requirement: "Test: SAM section exists and SAM <= TAM"
        - key: "SOM"
          type: "object"
          example: "{value: '$50M', methodology: 'Fermi', confidence: 'Low', sources: ['...']}"
          required: true
          validation: "SOM value must be <= SAM value"
          test_requirement: "Test: SOM section exists and SOM <= SAM"

  business_rules:
    - id: "BR-001"
      rule: "TAM >= SAM >= SOM > 0 invariant must hold for all estimates"
      trigger: "After calculation of all three tiers"
      validation: "Compare numeric values after normalization"
      error_handling: "Flag inconsistency and prompt user for correction via AskUserQuestion"
      test_requirement: "Test: Verify constraint enforcement when values violate ordering"
      priority: "Critical"
    - id: "BR-002"
      rule: "All data points must have source attribution (URL, report name, or 'user-provided')"
      trigger: "When incorporating any data point into estimates"
      validation: "Check every figure has non-empty source string"
      error_handling: "Reject unsourced figures and prompt for source"
      test_requirement: "Test: Output file contains no unsourced figures"
      priority: "High"
    - id: "BR-003"
      rule: "Fallback to Fermi estimation when internet-sleuth returns no data"
      trigger: "When internet-sleuth invocation returns empty or error"
      validation: "Check workflow completes with Fermi fallback path"
      error_handling: "Mark confidence as 'Low' and note data limitations"
      test_requirement: "Test: Workflow completes even when internet-sleuth fails"
      priority: "High"
    - id: "BR-004"
      rule: "Default to beginner knowledge level when user profile is missing"
      trigger: "When user profile file does not exist or lacks business_knowledge field"
      validation: "Check default behavior when profile absent"
      error_handling: "Log warning, proceed with beginner-level questions"
      test_requirement: "Test: Missing profile defaults to beginner with logged warning"
      priority: "Medium"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Complete full workflow in under 120 seconds of active processing time"
      metric: "< 120s active processing (excluding user think time)"
      test_requirement: "Test: Measure processing time excluding user input wait"
      priority: "Medium"
    - id: "NFR-002"
      category: "Performance"
      requirement: "Maximum 3 internet-sleuth invocations per workflow run"
      metric: "<= 3 internet-sleuth calls per run"
      test_requirement: "Test: Count internet-sleuth invocations in workflow"
      priority: "High"
    - id: "NFR-003"
      category: "Reliability"
      requirement: "Workflow must complete and produce output even if internet-sleuth fails"
      metric: "100% completion rate with Fermi fallback"
      test_requirement: "Test: Simulate internet-sleuth failure and verify output produced"
      priority: "Critical"
    - id: "NFR-004"
      category: "Security"
      requirement: "No API keys, credentials, or PII in output or skill files"
      metric: "Zero sensitive data in all output files"
      test_requirement: "Test: Scan output for API key patterns, credentials, PII"
      priority: "High"
```

---

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "internet-sleuth subagent"
    limitation: "May not find market data for niche or emerging markets"
    decision: "workaround:Fermi estimation fallback with Low confidence marking"
    discovered_phase: "Architecture"
    impact: "Estimates may be less accurate for obscure markets"
  - id: TL-002
    component: "User profile integration"
    limitation: "EPIC-072 (Assessment & Coaching Core) may not be complete when this story is implemented"
    decision: "workaround:Default to beginner level when profile missing"
    discovered_phase: "Architecture"
    impact: "Adaptive questioning degrades gracefully to beginner defaults"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- Full workflow completion: < 120 seconds active processing (excluding user think time)
- Output file generation: < 2 seconds after final calculation

**Throughput:**
- Maximum 3 internet-sleuth invocations per workflow run
- Single user workflow (not concurrent)

---

### Security

**Authentication:**
- None required (framework-internal skill)

**Data Protection:**
- No API keys or credentials in output files
- No PII in market sizing output
- Internet-sleuth queries contain only market/industry terms, not proprietary data

---

### Scalability

**Horizontal Scaling:**
- Stateless design: Yes (each run is independent)
- Re-runnable for different markets without manual cleanup

**Caching:**
- None (each run produces fresh research)

---

### Reliability

**Error Handling:**
- Fermi fallback when internet-sleuth fails
- Write-on-completion pattern (build in memory, write once at end)
- All AskUserQuestion interactions have cancel option

**Retry Logic:**
- No automatic retries for internet-sleuth (max 3 calls budgeted)

---

### Observability

**Logging:**
- Log confidence levels for each tier
- Log internet-sleuth invocation count and results summary
- Log user profile knowledge level used

---

## Dependencies

### Prerequisite Stories

- [ ] **None:** This is the first story in EPIC-074 sprint 1

### External Dependencies

- [ ] **internet-sleuth subagent:** Existing subagent for web research
  - **Owner:** DevForgeAI framework
  - **Status:** Available
  - **Impact if delayed:** Fermi-only fallback

### Technology Dependencies

- [ ] **None:** Uses existing framework tools (Markdown, native tools)

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for business logic

**Test Scenarios:**
1. **Happy Path:** Complete workflow with internet-sleuth data, user profile present, all tiers generated
2. **Edge Cases:**
   - Missing user profile defaults to beginner
   - Internet-sleuth returns no data, Fermi fallback activates
   - User provides pre-existing market figures
   - Output file already exists, user prompted
   - Extremely broad/narrow market definition warning
3. **Error Cases:**
   - TAM < SAM violation detected and flagged
   - Empty market description rejected
   - Invalid confidence level rejected

---

### Integration Tests

**Coverage Target:** 85%+ for application layer

**Test Scenarios:**
1. **End-to-End Workflow:** Full workflow from user input to file output
2. **Internet-Sleuth Integration:** Verify subagent invocation and data incorporation

---

## Acceptance Criteria Verification Checklist

**Purpose:** Real-time progress tracking during TDD implementation.

### AC#1: TAM/SAM/SOM Output Structure

- [ ] Output file contains ## TAM section with dollar value - **Phase:** 2 - **Evidence:** tests/STORY-535/test_ac1_market_sizing_output.py
- [ ] Output file contains ## SAM section with dollar value - **Phase:** 2 - **Evidence:** tests/STORY-535/test_ac1_market_sizing_output.py
- [ ] Output file contains ## SOM section with dollar value - **Phase:** 2 - **Evidence:** tests/STORY-535/test_ac1_market_sizing_output.py
- [ ] Each tier has methodology notes - **Phase:** 2 - **Evidence:** tests/STORY-535/test_ac1_market_sizing_output.py
- [ ] Each tier has cited data sources - **Phase:** 2 - **Evidence:** tests/STORY-535/test_ac1_market_sizing_output.py
- [ ] Each tier has confidence level (High/Medium/Low) - **Phase:** 2 - **Evidence:** tests/STORY-535/test_ac1_market_sizing_output.py

### AC#2: Internet-Sleuth Integration

- [ ] internet-sleuth subagent is invoked during workflow - **Phase:** 3 - **Evidence:** tests/STORY-535/test_ac2_internet_sleuth_integration.py
- [ ] At least 2 external data points in output - **Phase:** 3 - **Evidence:** tests/STORY-535/test_ac2_internet_sleuth_integration.py
- [ ] Source attribution for external data - **Phase:** 3 - **Evidence:** tests/STORY-535/test_ac2_internet_sleuth_integration.py

### AC#3: Adaptive Question Depth

- [ ] Beginner receives explanatory context - **Phase:** 3 - **Evidence:** tests/STORY-535/test_ac3_adaptive_questions.py
- [ ] Intermediate receives standard prompts - **Phase:** 3 - **Evidence:** tests/STORY-535/test_ac3_adaptive_questions.py
- [ ] Advanced receives abbreviated prompts - **Phase:** 3 - **Evidence:** tests/STORY-535/test_ac3_adaptive_questions.py

### AC#4: Progressive Disclosure via AskUserQuestion

- [ ] All user inputs use AskUserQuestion - **Phase:** 3 - **Evidence:** tests/STORY-535/test_ac4_progressive_disclosure.py
- [ ] Questions presented sequentially - **Phase:** 3 - **Evidence:** tests/STORY-535/test_ac4_progressive_disclosure.py

### AC#5: Skill File Structure Compliance

- [ ] SKILL.md under 1,000 lines - **Phase:** 3 - **Evidence:** tests/STORY-535/test_ac5_skill_structure.py
- [ ] references/market-sizing-methodology.md exists - **Phase:** 3 - **Evidence:** tests/STORY-535/test_ac5_skill_structure.py
- [ ] references/fermi-estimation.md exists - **Phase:** 3 - **Evidence:** tests/STORY-535/test_ac5_skill_structure.py

---

**Checklist Progress:** 0/18 items complete (0%)

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

*To be filled during implementation*

## Definition of Done

### Implementation
- [ ] Create `src/claude/skills/researching-market/SKILL.md` with market sizing workflow
- [ ] Create `src/claude/skills/researching-market/references/market-sizing-methodology.md`
- [ ] Create `src/claude/skills/researching-market/references/fermi-estimation.md`
- [ ] Implement TAM/SAM/SOM calculation with Fermi estimation methodology
- [ ] Implement internet-sleuth subagent invocation for market data
- [ ] Implement adaptive question depth based on user profile
- [ ] Implement output file generation to `devforgeai/specs/business/market-research/market-sizing.md`

### Quality
- [ ] All 5 acceptance criteria have passing tests
- [ ] Edge cases covered (missing profile, no internet data, pre-existing figures, existing output, broad/narrow market)
- [ ] Data validation enforced (TAM>=SAM>=SOM>0, source attribution, confidence levels)
- [ ] NFRs met (120s processing, 3 max internet-sleuth calls, Fermi fallback)
- [ ] SKILL.md under 1,000 lines

### Testing
- [ ] Unit tests for market sizing calculation logic
- [ ] Unit tests for adaptive question depth
- [ ] Unit tests for output file structure validation
- [ ] Integration tests for internet-sleuth workflow
- [ ] Integration tests for end-to-end workflow

### Documentation
- [ ] SKILL.md contains YAML frontmatter and usage instructions
- [ ] Reference files contain methodology documentation
- [ ] Edge case handling documented in skill

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
| 2026-03-03 | .claude/story-requirements-analyst | Created | Story created from EPIC-074 Feature 1 | STORY-535-market-sizing-guided-workflow.story.md |

## Notes

**Design Decisions:**
- Fermi estimation as primary methodology with web research augmentation
- Write-on-completion pattern to prevent partial file corruption
- Default to beginner knowledge level for graceful degradation

**Open Questions:**
- [ ] Exact output markdown template format for market-sizing.md - **Owner:** DevForgeAI - **Due:** Sprint planning

**Related ADRs:**
- None yet

**References:**
- EPIC-074: Market Research & Competition
- BRAINSTORM-011: Business Skills Framework

---

Story Template Version: 2.9
Last Updated: 2026-03-03

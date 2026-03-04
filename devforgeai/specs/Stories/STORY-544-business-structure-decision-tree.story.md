---
id: STORY-544
title: Business Structure Decision Tree
type: feature
epic: EPIC-076
sprint: Sprint-26
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

# Story: Business Structure Decision Tree

## Description

**As a** first-time entrepreneur or small business owner,
**I want** to work through a guided decision tree that evaluates my revenue expectations, partnership structure, liability concerns, and tax preferences,
**so that** I can understand which business entity type (Sole Proprietorship, LLC, S-Corp, or C-Corp) best fits my situation, and know exactly when I need to consult a licensed attorney or CPA before proceeding.

## Provenance

```xml
<provenance>
  <origin document="devforgeai/specs/brainstorms/archive/BRAINSTORM-011-business-skills-framework.brainstorm.md" section="prioritization">
    <quote>"EPIC-E: Legal &amp; Compliance — Business structure and IP protection"</quote>
    <line_reference>lines 333</line_reference>
    <quantified_impact>Entrepreneurs delay legal foundations out of confusion, creating business risk</quantified_impact>
  </origin>

  <decision rationale="educational-guidance-over-document-generation">
    <selected>Decision tree providing educational guidance with professional referral triggers</selected>
    <rejected alternative="ai-generated-legal-documents">
      AI-generated legal documents rejected due to liability concern — explicit Won't Have from BRAINSTORM-011
    </rejected>
    <trade_off>Users get guidance but must engage professionals for binding decisions</trade_off>
  </decision>

  <stakeholder role="Solo Developer" goal="turn-project-into-business">
    <quote>"Turn project into revenue, gain business confidence"</quote>
    <source>BRAINSTORM-011, section 1.2 Stakeholder Goals</source>
  </stakeholder>

  <hypothesis id="H4" validation="user-feedback" success_criteria="Decision tree produces actionable recommendation in 100% of valid input combinations">
    Business structure guidance reduces legal confusion for first-time entrepreneurs
  </hypothesis>
</provenance>
```

## Acceptance Criteria

Define testable, specific conditions that must be met for story completion. Use XML format with `<acceptance_criteria>` blocks for machine-parseable verification.

> **IMPORTANT:** XML acceptance criteria format is REQUIRED for automated verification by the ac-compliance-verifier subagent.

### XML Acceptance Criteria Format

Use the following XML schema for each acceptance criterion.

### AC#1: Decision Tree Guides User Through Entity Selection Factors

```xml
<acceptance_criteria id="AC1" implements="SVC-001">
  <given>A user has invoked the advising-legal skill and selected the business structure workflow</given>
  <when>The decision tree begins</when>
  <then>The system presents sequential questions covering all four decision factors in order: (1) revenue expectations, (2) number of partners/co-founders, (3) liability exposure level, and (4) tax preferences — with each answer narrowing the entity recommendations — and the skill file does not exceed 1,000 lines</then>
  <verification>
    <source_files>
      <file hint="Decision tree workflow">src/claude/skills/advising-legal/references/business-structure-guide.md</file>
    </source_files>
    <test_file>tests/STORY-544/test_ac1_decision_tree_factors.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Entity Recommendations Include Contextual Rationale

```xml
<acceptance_criteria id="AC2" implements="SVC-001,BR-001">
  <given>A user has completed the decision tree input sequence</given>
  <when>The system produces a recommended entity type (Sole Proprietorship, LLC, S-Corp, or C-Corp)</when>
  <then>The output includes: the recommended entity name, a plain-language explanation of why it matches the user's inputs, a comparison of the top two candidates (if scores are within one factor of each other), and a disclaimer header stating educational-only scope</then>
  <verification>
    <source_files>
      <file hint="Entity descriptions and scoring">src/claude/skills/advising-legal/references/business-structure-guide.md</file>
    </source_files>
    <test_file>tests/STORY-544/test_ac2_entity_recommendations.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Professional Referral Triggers Fire for Complex Situations

```xml
<acceptance_criteria id="AC3" implements="BR-002">
  <given>A user's inputs match any of the defined complexity triggers: multi-state operations, international operations, more than one partner/co-founder, S-Corp election timing questions, or C-Corp equity/investor questions</given>
  <when>The decision tree evaluates those inputs</when>
  <then>The system immediately surfaces a "Consult a Professional" block that (a) names the specific complexity detected, (b) explains why it exceeds educational guidance scope, (c) lists the type of professional to contact (attorney, CPA, or both), and (d) halts further recommendation output for that branch</then>
  <verification>
    <source_files>
      <file hint="Complexity trigger definitions">src/claude/skills/advising-legal/references/business-structure-guide.md</file>
    </source_files>
    <test_file>tests/STORY-544/test_ac3_professional_referral_triggers.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Output Artifact Written to Correct Path with Disclaimer Header

```xml
<acceptance_criteria id="AC4" implements="SVC-002,NFR-001">
  <given>The decision tree session is complete and a recommendation has been generated</given>
  <when>The system writes the output artifact</when>
  <then>The file is written to devforgeai/specs/business/legal/business-structure.md, the first three lines of the file are the standard disclaimer header, the file includes the user's decision path as a readable summary, and the reference guide is the sole authoritative source for entity descriptions</then>
  <verification>
    <source_files>
      <file hint="Output artifact">devforgeai/specs/business/legal/business-structure.md</file>
    </source_files>
    <test_file>tests/STORY-544/test_ac4_output_artifact.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#5: Adaptive Pacing Reads User Profile Without Modification

```xml
<acceptance_criteria id="AC5" implements="SVC-003">
  <given>A user profile exists and the advising-legal skill reads it at session start</given>
  <when>The skill accesses the user profile for pacing preferences</when>
  <then>The skill reads the profile in read-only mode (no writes, no mutations), adjusts question verbosity and explanation depth based on detected experience level (beginner/intermediate/advanced), and produces no error if the profile is absent (falls back to default intermediate pacing)</then>
  <verification>
    <source_files>
      <file hint="Profile integration">src/claude/skills/advising-legal/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-544/test_ac5_adaptive_pacing.sh</test_file>
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
      name: "advising-legal-business-structure"
      file_path: "src/claude/skills/advising-legal/references/business-structure-guide.md"
      interface: "Progressive disclosure reference"
      lifecycle: "On-demand"
      dependencies:
        - "advising-legal SKILL.md"
        - "User profile (read-only, optional)"
      requirements:
        - id: "SVC-001"
          description: "Decision tree covering LLC, S-Corp, Sole Proprietorship, C-Corp with four decision factors"
          testable: true
          test_requirement: "Test: All four question branches present and reachable from entry point"
          priority: "Critical"
        - id: "SVC-002"
          description: "Output artifact written to devforgeai/specs/business/legal/business-structure.md with disclaimer header"
          testable: true
          test_requirement: "Test: Output file exists at correct path with disclaimer in first 3 lines"
          priority: "Critical"
        - id: "SVC-003"
          description: "Adaptive pacing reads user profile in read-only mode with graceful fallback"
          testable: true
          test_requirement: "Test: Skill completes successfully with and without user profile present"
          priority: "High"

  business_rules:
    - id: "BR-001"
      rule: "Entity recommendations must include contextual rationale and comparison when scores are close"
      trigger: "Decision tree evaluation produces recommendation"
      validation: "Output contains recommended entity, rationale, and comparison if tie"
      error_handling: "Regenerate recommendation with comparison if missing"
      test_requirement: "Test: Recommendation output contains entity name, rationale, and disclaimer"
      priority: "Critical"
    - id: "BR-002"
      rule: "Professional referral triggers fire for all five complexity conditions: multi-state, international, 2+ partners, S-Corp election, C-Corp equity"
      trigger: "Any complexity indicator detected in user inputs"
      validation: "Referral block fires naming complexity, explaining scope limit, listing professional type"
      error_handling: "Halt further recommendation for that branch"
      test_requirement: "Test: Each of 5 triggers produces referral block — 5 independent test cases"
      priority: "Critical"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Security"
      requirement: "Disclaimer header auto-included in every output artifact"
      metric: "100% of output writes include disclaimer as lines 1-3"
      test_requirement: "Test: Output file lines 1-3 match verbatim disclaimer"
      priority: "Critical"
    - id: "NFR-002"
      category: "Performance"
      requirement: "Decision tree session completes within acceptable time"
      metric: "Full session completion < 30 seconds end-to-end"
      test_requirement: "Test: Timed execution of full decision tree session"
      priority: "High"
    - id: "NFR-003"
      category: "Reliability"
      requirement: "Skill file stays under 1,000 lines with progressive disclosure"
      metric: "wc -l on skill file returns value <= 999"
      test_requirement: "Test: Line count assertion on skill file"
      priority: "High"
```

---

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "advising-legal skill"
    limitation: "Cannot provide jurisdiction-specific legal advice — general US guidance only"
    decision: "workaround:Include 'verify in your state' warnings at every jurisdiction-sensitive point"
    discovered_phase: "Architecture"
    impact: "Users in non-US jurisdictions or specific US states may need additional professional guidance"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- Decision tree question-to-question transition: < 500ms per step (p95)
- Full session completion (all four factors through output artifact): < 30 seconds end-to-end

**Throughput:**
- Single-user CLI tool — concurrent user support not required

### Security

**Authentication:**
- None (CLI-local tool)

**Data Protection:**
- No user-provided input is persisted or logged with PII
- User profile accessed read-only; write attempts must fail
- Disclaimer header present in 100% of output artifacts

**Security Testing:**
- [x] No hardcoded secrets
- [x] Proper input validation (bucketed inputs only)
- [x] Read-only profile enforcement

### Scalability

**Design:**
- Stateless per invocation — no shared state between sessions
- Progressive disclosure: entity descriptions in reference file, not inline in skill
- Reference file architecture supports adding new entity types without skill modification

### Reliability

**Error Handling:**
- All file I/O failures produce specific, human-readable error messages
- Profile absence fallback: 100% uptime regardless of profile presence
- Decision tree reaches terminal state for every valid input combination

### Observability

**Logging:**
- Log level: INFO for session start/end, WARN for profile absence, ERROR for I/O failures
- Structured output with session correlation

---

## Dependencies

### Prerequisite Stories

- [ ] **None** — This story can start immediately
  - **Why:** First story in EPIC-076 feature chain
  - **Status:** N/A

### External Dependencies

- None

### Technology Dependencies

- None — uses only Markdown and existing DevForgeAI framework

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for business logic

**Test Scenarios:**
1. **Happy Path:** User answers all four decision factors, receives entity recommendation with rationale
2. **Edge Cases:**
   - Contradictory inputs (no partners then mentions equity split)
   - Tie score between two entity types
   - Multi-state trigger fires mid-tree
   - Profile absent — fallback to intermediate pacing
   - Output directory does not exist at write time
3. **Error Cases:**
   - Invalid input bucket values
   - Profile file unreadable/malformed
   - Output path write failure

### Integration Tests

**Coverage Target:** 85%+ for application layer

**Test Scenarios:**
1. **End-to-End Decision Tree Flow:** Complete session from invocation to output artifact
2. **Professional Referral Coverage:** All 5 complexity triggers tested independently

---

## Acceptance Criteria Verification Checklist

**Purpose:** Real-time progress tracking during TDD implementation.

**Tracking Mechanisms:**
- **TodoWrite:** Phase-level tracking
- **AC Checklist:** AC sub-item tracking ← YOU ARE HERE
- **Definition of Done:** Official completion record

### AC#1: Decision Tree Guides User Through Entity Selection Factors

- [ ] Decision tree presents revenue expectations question - **Phase:** 2 - **Evidence:** tests/STORY-544/
- [ ] Decision tree presents partners/co-founders question - **Phase:** 2 - **Evidence:** tests/STORY-544/
- [ ] Decision tree presents liability exposure question - **Phase:** 2 - **Evidence:** tests/STORY-544/
- [ ] Decision tree presents tax preferences question - **Phase:** 2 - **Evidence:** tests/STORY-544/
- [ ] Skill file under 1,000 lines - **Phase:** 2 - **Evidence:** wc -l

### AC#2: Entity Recommendations Include Contextual Rationale

- [ ] Recommendation includes entity name - **Phase:** 2 - **Evidence:** tests/STORY-544/
- [ ] Recommendation includes rationale - **Phase:** 2 - **Evidence:** tests/STORY-544/
- [ ] Tie-score comparison shown when applicable - **Phase:** 2 - **Evidence:** tests/STORY-544/
- [ ] Disclaimer header present - **Phase:** 2 - **Evidence:** tests/STORY-544/

### AC#3: Professional Referral Triggers Fire for Complex Situations

- [ ] Multi-state trigger fires - **Phase:** 2 - **Evidence:** tests/STORY-544/
- [ ] International trigger fires - **Phase:** 2 - **Evidence:** tests/STORY-544/
- [ ] 2+ partners trigger fires - **Phase:** 2 - **Evidence:** tests/STORY-544/
- [ ] S-Corp election trigger fires - **Phase:** 2 - **Evidence:** tests/STORY-544/
- [ ] C-Corp equity trigger fires - **Phase:** 2 - **Evidence:** tests/STORY-544/

### AC#4: Output Artifact Written to Correct Path with Disclaimer Header

- [ ] File written to devforgeai/specs/business/legal/business-structure.md - **Phase:** 2 - **Evidence:** tests/STORY-544/
- [ ] Disclaimer in first 3 lines - **Phase:** 2 - **Evidence:** tests/STORY-544/
- [ ] Decision path summary included - **Phase:** 2 - **Evidence:** tests/STORY-544/

### AC#5: Adaptive Pacing Reads User Profile Without Modification

- [ ] Profile read in read-only mode - **Phase:** 2 - **Evidence:** tests/STORY-544/
- [ ] Pacing adjusts to experience level - **Phase:** 2 - **Evidence:** tests/STORY-544/
- [ ] Fallback to intermediate when profile absent - **Phase:** 2 - **Evidence:** tests/STORY-544/

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

*To be filled during /dev workflow*

## Definition of Done

### Implementation
- [ ] Decision tree reference file created at src/claude/skills/advising-legal/references/business-structure-guide.md
- [ ] Decision tree covers all four factors: revenue, partners, liability, tax preferences
- [ ] All four entity types documented: Sole Proprietorship, LLC, S-Corp, C-Corp
- [ ] Professional referral triggers implemented for all 5 complexity conditions
- [ ] Disclaimer header auto-included in every output artifact
- [ ] Output artifact written to devforgeai/specs/business/legal/business-structure.md
- [ ] Adaptive pacing integration with user profile (read-only)

### Quality
- [ ] All 5 acceptance criteria have passing tests
- [ ] Edge cases covered (contradictory inputs, tie scores, mid-tree triggers, missing profile, missing directory)
- [ ] Data validation enforced (bucketed inputs, path validation, disclaimer presence)
- [ ] NFRs met (< 30s session, 1000-line limit, disclaimer 100%)
- [ ] Code coverage > 95% for business logic

### Testing
- [ ] Unit tests for decision tree factor questions
- [ ] Unit tests for entity recommendation with rationale
- [ ] Unit tests for all 5 professional referral triggers
- [ ] Unit tests for disclaimer presence validation
- [ ] Integration tests for end-to-end decision tree flow
- [ ] Integration tests for adaptive pacing with/without profile

### Documentation
- [ ] Reference file includes progressive disclosure structure
- [ ] Entity descriptions sourced from single reference file
- [ ] Disclaimer text sourced from single canonical location

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
| 2026-03-03 12:00 | .claude/story-requirements-analyst | Created | Story created from EPIC-076 Feature 1 | STORY-544-business-structure-decision-tree.story.md |

## Notes

**Design Decisions:**
- Decision factors presented sequentially (not all at once) for guided experience
- Bucketed inputs (not free-text) for reliable scoring
- Professional referral halts branch (does not continue with caveats) for safety
- Disclaimer header enforced as lines 1-3 of every output artifact

**Safety Constraints:**
- Educational guidance ONLY — never prescriptive legal advice
- "Consider" language, not "you should" language
- Every complexity threshold triggers professional referral
- No jurisdiction-specific advice (general US with "verify in your state" warnings)

**Related ADRs:**
- ADR-017: Gerund-Object Naming Convention

**References:**
- EPIC-076: Legal & Compliance
- FR-017: Business Structure Guidance
- BRAINSTORM-011: Business Skills Framework

---

Story Template Version: 2.9
Last Updated: 2026-03-03

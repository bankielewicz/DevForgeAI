---
id: STORY-558
title: Scaling Readiness Assessment
type: feature
epic: EPIC-078
sprint: Sprint-28
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

# Story: Scaling Readiness Assessment

## Description

**As a** recently launched solo developer,
**I want** a structured scaling readiness assessment that evaluates my infrastructure, processes, team capacity, and financial runway,
**so that** I can objectively determine whether my business is ready to scale before committing resources to growth initiatives.

## Provenance

```xml
<provenance>
  <origin document="devforgeai/specs/Epics/EPIC-078-operations-launch.epic.md" section="feature-5">
    <quote>"Post-launch assessment: Is your business ready to scale?"</quote>
    <line_reference>lines 68-72</line_reference>
    <quantified_impact>4-domain assessment with 0-12 composite score and 3 verdicts</quantified_impact>
  </origin>
</provenance>
```

## Acceptance Criteria

### AC#1: Four-Domain Assessment

```xml
<acceptance_criteria id="AC1" implements="SCALE-001">
  <given>a user invokes the scaling readiness assessment after launch</given>
  <when>the assessment runs</when>
  <then>it evaluates readiness across four domains — infrastructure, processes, team, and financial runway — presenting each domain as a scored section from 0 to 3</then>
  <verification>
    <source_files>
      <file hint="four-domain assessment structure">src/claude/skills/operating-business/references/scaling-readiness-assessment.md</file>
    </source_files>
    <test_file>tests/STORY-558/test-ac1-four-domain-assessment.md</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Scoring and Verdicts

```xml
<acceptance_criteria id="AC2" implements="SCALE-002">
  <given>a user has completed the four-domain assessment</given>
  <when>scores are tallied</when>
  <then>the assessment produces a composite readiness score (0-12) mapped to one of three verdicts: "Not Ready (0-4)", "Approaching Ready (5-8)", or "Ready to Scale (9-12)", each with a prioritized list of the top 3 actions to take next</then>
  <verification>
    <source_files>
      <file hint="scoring thresholds and verdicts">src/claude/skills/operating-business/references/scaling-readiness-assessment.md</file>
    </source_files>
    <test_file>tests/STORY-558/test-ac2-scoring-and-verdicts.md</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: When and How to Scale Guidance

```xml
<acceptance_criteria id="AC3" implements="SCALE-003">
  <given>the scaling readiness assessment is complete</given>
  <when>the reference guidance is consulted</when>
  <then>the reference file includes a "When to Scale" section with 5 concrete indicators and a "How to Scale" section with 3 sequenced approaches (process automation first, then tool upgrades, then hiring)</then>
  <verification>
    <source_files>
      <file hint="when-to-scale and how-to-scale sections">src/claude/skills/operating-business/references/scaling-readiness-assessment.md</file>
    </source_files>
    <test_file>tests/STORY-558/test-ac3-when-and-how-to-scale.md</test_file>
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
      name: "scaling-readiness-assessment.md"
      file_path: "src/claude/skills/operating-business/references/scaling-readiness-assessment.md"
      required_keys:
        - key: "domains"
          type: "array"
          example: "[infrastructure, processes, team, financial_runway]"
          required: true
          validation: "All 4 domains present"
          test_requirement: "Test: Verify all 4 assessment domains documented"
        - key: "scoring"
          type: "object"
          example: "{per_domain: 0-3, composite: 0-12, verdicts: 3}"
          required: true
          validation: "Scoring thresholds defined"
          test_requirement: "Test: Verify scoring produces valid verdicts for all score ranges"
        - key: "when_to_scale"
          type: "array"
          example: "5 concrete indicators"
          required: true
          validation: "Exactly 5 indicators"
          test_requirement: "Test: Verify 5 when-to-scale indicators documented"
        - key: "how_to_scale"
          type: "array"
          example: "[process automation, tool upgrades, hiring]"
          required: true
          validation: "3 sequenced approaches"
          test_requirement: "Test: Verify 3 how-to-scale approaches in correct order"

  business_rules:
    - id: "BR-001"
      rule: "Scoring is deterministic — identical answers produce identical scores"
      trigger: "When assessment is scored"
      validation: "No randomness or LLM variance in score calculation"
      error_handling: "N/A — deterministic by design"
      test_requirement: "Test: Same inputs produce same score across multiple runs"
      priority: "Critical"
    - id: "BR-002"
      rule: "Serverless infrastructure auto-scores 3/3"
      trigger: "When user indicates managed/serverless infrastructure"
      validation: "Infrastructure domain scored without further questions"
      error_handling: "N/A"
      test_requirement: "Test: Serverless selection produces infrastructure score of 3"
      priority: "Medium"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Reference file within size constraints"
      metric: "< 1,000 lines"
      test_requirement: "Test: wc -l scaling-readiness-assessment.md < 1000"
      priority: "High"
    - id: "NFR-002"
      category: "Reliability"
      requirement: "Valid verdict for all input combinations"
      metric: "No error state for any score 0-12"
      test_requirement: "Test: All scores 0-12 map to valid verdicts"
      priority: "Critical"
```

---

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "STORY-557 Integration"
    limitation: "Process domain score depends on core-processes.md which may not exist"
    decision: "workaround:Score 0/3 when core-processes.md missing with guidance to complete STORY-557"
    discovered_phase: "Architecture"
    impact: "Reduced accuracy for process domain without prior documentation"
```

---

## Non-Functional Requirements (NFRs)

### Performance
- Assessment initialization: < 2 seconds
- Score calculation and verdict: < 1 second
- Reference file: < 1,000 lines

### Security
- Financial figures used only for scoring, not persisted to output unless explicitly requested
- Assessment output contains scores and verdicts only, no raw financial data

### Scalability
- New domains added via reference file header
- Scoring thresholds externalized to reference file

### Reliability
- Valid verdict for all score combinations (0-12)
- Cross-reference with core-processes.md advisory, not required
- Deterministic scoring (no randomness)

### Observability
- Log assessment scores per domain

---

## Dependencies

### Prerequisite Stories
- No blocking prerequisites (STORY-557 optional for process domain accuracy)

### External Dependencies
- None

### Technology Dependencies
- No new packages required

---

## Test Strategy

### Unit Tests
**Coverage Target:** 95%+
1. **Happy Path:** Full 4-domain assessment producing "Approaching Ready" verdict
2. **Edge Cases:** < 30 days since launch, missing core-processes.md, serverless infra, reassessment
3. **Error Cases:** All domains score 0 → "Not Ready" with remediation

### Integration Tests
**Coverage Target:** 85%+
1. Full assessment workflow end-to-end
2. Cross-reference with core-processes.md

---

## Acceptance Criteria Verification Checklist

### AC#1: Four-Domain Assessment
- [ ] 4 domains evaluated with 0-3 scoring - **Phase:** 2
- [ ] Each domain presented as scored section - **Phase:** 2

### AC#2: Scoring and Verdicts
- [ ] Composite score 0-12 calculated - **Phase:** 2
- [ ] 3 verdicts with top 3 actions each - **Phase:** 2

### AC#3: When and How to Scale
- [ ] 5 concrete indicators documented - **Phase:** 2
- [ ] 3 sequenced approaches documented - **Phase:** 2

---

**Checklist Progress:** 0/6 items complete (0%)

---

## Implementation Notes

*To be filled during /dev workflow*

## Definition of Done

### Implementation
- [ ] Reference file scaling-readiness-assessment.md with 4 domains and scoring
- [ ] Composite score 0-12 with 3 verdict thresholds
- [ ] "When to Scale" section with 5 indicators
- [ ] "How to Scale" section with 3 sequenced approaches

### Quality
- [ ] All 3 acceptance criteria have passing tests
- [ ] Edge cases covered (< 30 days, missing processes, serverless, reassessment)
- [ ] Reference file < 1,000 lines

### Testing
- [ ] Unit tests for 4-domain scoring
- [ ] Unit tests for verdict thresholds
- [ ] Unit tests for deterministic scoring
- [ ] Integration tests for full assessment

### Documentation
- [ ] Reference file includes scoring rubric and indicator definitions

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
| 2026-03-03 | .claude/story-requirements-analyst | Created | Story created from EPIC-078 Feature 5 | STORY-558.story.md |

## Notes

**Edge Cases:**
1. Business < 30 days old → use projections, mark as "(projected)"
2. Missing core-processes.md → process domain scores 0/3
3. Serverless infrastructure → auto-score 3/3
4. Reassessment → load previous scores, update only changed domains

---

Story Template Version: 2.9
Last Updated: 2026-03-03

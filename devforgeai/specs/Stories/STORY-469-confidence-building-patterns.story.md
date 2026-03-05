---
id: STORY-469
title: Confidence-Building Patterns
type: feature
epic: EPIC-072
sprint: Sprint-16
status: QA Approved
points: 3
depends_on: ["STORY-468"]
priority: Medium
advisory: false
source_gap: null
source_story: null
assigned_to: DevForgeAI AI Agent
created: 2026-02-21
format_version: "2.9"
---

# Story: Confidence-Building Patterns

## Description

**As a** user with self-doubt or imposter syndrome,
**I want** the AI to build my confidence through imposter syndrome interventions, momentum tracking, and evidence-based affirmation,
**so that** I believe I can succeed as an entrepreneur.

## Provenance

```xml
<provenance>
  <origin document="BRAINSTORM-011" section="problem-analysis">
    <quote>"Lack of adaptive, personalized business guidance that accounts for neurodivergent cognitive styles and builds confidence through progressive, visible milestones."</quote>
    <line_reference>lines 119</line_reference>
    <quantified_impact>Addresses the psychological gap — the second of three intertwined barriers</quantified_impact>
  </origin>

  <hypothesis id="H2" validation="Compare plans from coached vs uncoached sessions" success_criteria="Plans score higher on viability rubric">
    IF we integrate confidence coaching into business planning, THEN plan quality improves
  </hypothesis>
</provenance>
```

## Acceptance Criteria

### AC#1: Confidence Patterns Reference File

```xml
<acceptance_criteria id="AC1" implements="COMP-001">
  <given>The coaching-entrepreneur skill needs confidence-building capabilities</given>
  <when>The confidence-building-patterns.md reference file is created</when>
  <then>The file exists at src/claude/skills/coaching-entrepreneur/references/confidence-building-patterns.md and contains: imposter syndrome recognition patterns, reframing techniques, evidence-based affirmation templates, and momentum tracking methodology</then>
  <verification>
    <source_files>
      <file hint="Confidence patterns reference">src/claude/skills/coaching-entrepreneur/references/confidence-building-patterns.md</file>
    </source_files>
    <test_file>tests/STORY-469/test_ac1_confidence_patterns.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

### AC#2: Imposter Syndrome Interventions Reference

```xml
<acceptance_criteria id="AC2" implements="COMP-002">
  <given>Users may express imposter syndrome during coaching</given>
  <when>The imposter-syndrome-interventions.md reference file is created</when>
  <then>The file exists at src/claude/skills/coaching-entrepreneur/references/imposter-syndrome-interventions.md and contains: recognition triggers (language patterns indicating imposter syndrome), validation-then-redirect techniques, evidence-based reframing, and the principle "Never dismisses feelings; validates then redirects"</then>
  <verification>
    <source_files>
      <file hint="Imposter syndrome reference">src/claude/skills/coaching-entrepreneur/references/imposter-syndrome-interventions.md</file>
    </source_files>
    <test_file>tests/STORY-469/test_ac2_imposter_syndrome.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

### AC#3: Business-Coach Subagent Integration

```xml
<acceptance_criteria id="AC3" implements="COMP-003">
  <given>The business-coach subagent needs to detect confidence signals</given>
  <when>The subagent is updated to reference confidence patterns</when>
  <then>business-coach.md contains instructions to detect confidence-related language, load the appropriate reference file (confidence-building-patterns.md or imposter-syndrome-interventions.md), and apply the relevant technique</then>
  <verification>
    <source_files>
      <file hint="Updated subagent">src/claude/agents/business-coach.md</file>
    </source_files>
    <test_file>tests/STORY-469/test_ac3_subagent_confidence.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

### AC#4: Evidence-Based Affirmation

```xml
<acceptance_criteria id="AC4">
  <given>A user has completed milestones tracked in the system</given>
  <when>The user expresses doubt during a coaching session</when>
  <then>The coaching system provides evidence-based affirmation using the user's actual progress data (e.g., "You've completed X milestones — that puts you ahead of most aspiring entrepreneurs") rather than generic encouragement</then>
  <verification>
    <source_files>
      <file hint="Evidence-based patterns">src/claude/skills/coaching-entrepreneur/references/confidence-building-patterns.md</file>
    </source_files>
    <test_file>tests/STORY-469/test_ac4_evidence_affirmation.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "confidence-building-patterns.md"
      file_path: "src/claude/skills/coaching-entrepreneur/references/confidence-building-patterns.md"
      required_keys:
        - key: "imposter-syndrome-recognition"
          type: "section"
          required: true
          test_requirement: "Test: Verify section header exists"
        - key: "reframing-techniques"
          type: "section"
          required: true
          test_requirement: "Test: Verify section header exists"
        - key: "evidence-based-affirmation"
          type: "section"
          required: true
          test_requirement: "Test: Verify section header exists"
        - key: "momentum-tracking"
          type: "section"
          required: true
          test_requirement: "Test: Verify section header exists"

    - type: "Configuration"
      name: "imposter-syndrome-interventions.md"
      file_path: "src/claude/skills/coaching-entrepreneur/references/imposter-syndrome-interventions.md"
      required_keys:
        - key: "recognition-triggers"
          type: "section"
          required: true
          test_requirement: "Test: Verify recognition patterns documented"
        - key: "validate-then-redirect"
          type: "section"
          required: true
          test_requirement: "Test: Verify validation-redirect pattern documented"

  business_rules:
    - id: "BR-001"
      rule: "Never dismiss feelings; validate then redirect"
      trigger: "Any user expression of self-doubt or imposter syndrome"
      validation: "Intervention patterns follow validate-first approach"
      error_handling: "If uncertain, default to validation"
      test_requirement: "Test: Verify 'validate' appears before 'redirect' in intervention flow"
      priority: "Critical"

    - id: "BR-002"
      rule: "Affirmations must be evidence-based, not generic"
      trigger: "Confidence intervention"
      validation: "Affirmation templates reference user's actual progress data"
      error_handling: "If no progress data available, use general encouragement with disclaimer"
      test_requirement: "Test: Verify affirmation templates reference milestone/progress data"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Reference files under 1500 lines each"
      metric: "Line count < 1500 per file"
      test_requirement: "Test: wc -l for each reference file < 1500"
      priority: "Medium"
```

## Technical Limitations

```yaml
technical_limitations: []
```

## Dependencies

### Prerequisite Stories
- [ ] **STORY-468:** Emotional State Tracking
  - **Why:** Confidence patterns extend emotional tracking with specific interventions
  - **Status:** Backlog

## Test Strategy

### Unit Tests
**Coverage Target:** 95%+
1. **Happy Path:** Reference files exist with required sections
2. **Edge Cases:** Empty sections, missing patterns
3. **Error Cases:** Reference file missing entirely

## Acceptance Criteria Verification Checklist

### AC#1: Confidence Patterns Reference
- [ ] File exists at correct path - **Phase:** 2
- [ ] Contains 4 required sections - **Phase:** 3

### AC#2: Imposter Syndrome Interventions
- [ ] File exists at correct path - **Phase:** 2
- [ ] Contains recognition triggers - **Phase:** 3
- [ ] Contains validate-then-redirect pattern - **Phase:** 3

### AC#3: Subagent Integration
- [ ] business-coach.md references confidence patterns - **Phase:** 3
- [ ] Detection instructions present - **Phase:** 3

### AC#4: Evidence-Based Affirmation
- [ ] Affirmation templates reference progress data - **Phase:** 3
- [ ] Not generic encouragement - **Phase:** 3

---

**Checklist Progress:** 0/9 items complete (0%)

---

## Definition of Done

### Implementation
- [x] confidence-building-patterns.md created with 4 sections
- [x] imposter-syndrome-interventions.md created with recognition and intervention patterns
- [x] business-coach.md updated with confidence detection instructions
- [x] Evidence-based affirmation templates reference user progress data

### Quality
- [x] All 4 acceptance criteria have passing tests
- [x] "Never dismiss feelings" principle enforced in intervention flow
- [x] Reference files under 1500 lines

### Testing
- [x] Unit tests for confidence patterns (test_ac1)
- [x] Unit tests for imposter syndrome (test_ac2)
- [x] Unit tests for subagent integration (test_ac3)
- [x] Unit tests for evidence affirmation (test_ac4)

### Documentation
- [x] Confidence patterns contain actionable intervention templates
- [x] Imposter syndrome recognition triggers are specific (not vague)

---

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-03-04

- [x] confidence-building-patterns.md created with 4 sections - Completed: Created at src/claude/skills/coaching-entrepreneur/references/confidence-building-patterns.md with Imposter Syndrome Recognition, Reframing Techniques, Evidence-Based Affirmation, and Momentum Tracking sections
- [x] imposter-syndrome-interventions.md created with recognition and intervention patterns - Completed: Created at src/claude/skills/coaching-entrepreneur/references/imposter-syndrome-interventions.md with Recognition Triggers and Validate-Then-Redirect Intervention sections
- [x] business-coach.md updated with confidence detection instructions - Completed: Created at src/claude/agents/business-coach.md with Confidence Detection, Applying Techniques, and Decision Tree sections
- [x] Evidence-based affirmation templates reference user progress data - Completed: Templates use {milestone_count}, {active_weeks}, {completed_count} placeholders referencing actual user data
- [x] All 4 acceptance criteria have passing tests - Completed: 34 tests passing (21 unit + 13 integration)
- [x] "Never dismiss feelings" principle enforced in intervention flow - Completed: Core principle statement at line 5 of interventions file, validate-before-redirect ordering verified
- [x] Reference files under 1500 lines - Completed: confidence-building-patterns.md ~102 lines, imposter-syndrome-interventions.md ~82 lines
- [x] Unit tests for confidence patterns (test_ac1) - Completed: 6 tests in tests/STORY-469/test_ac1_confidence_patterns.py
- [x] Unit tests for imposter syndrome (test_ac2) - Completed: 6 tests in tests/STORY-469/test_ac2_imposter_syndrome.py
- [x] Unit tests for subagent integration (test_ac3) - Completed: 5 tests in tests/STORY-469/test_ac3_subagent_confidence.py
- [x] Unit tests for evidence affirmation (test_ac4) - Completed: 4 tests in tests/STORY-469/test_ac4_evidence_affirmation.py
- [x] Confidence patterns contain actionable intervention templates - Completed: 4 reframing approaches with concrete examples, template affirmations with data placeholders
- [x] Imposter syndrome recognition triggers are specific (not vague) - Completed: 6 verbal triggers, 5 behavioral triggers, 3 severity levels documented

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|
| 01 Pre-Flight | ✅ Complete | Git validated, 6 context files loaded, tech-stack detected |
| 02 Red | ✅ Complete | 21 tests written, all failing (RED confirmed) |
| 03 Green | ✅ Complete | 3 files created, 21/21 tests passing |
| 04 Refactor | ✅ Complete | Cross-references added, naming improved, code review APPROVED |
| 04.5 AC Verify | ✅ Complete | 4/4 ACs PASS |
| 05 Integration | ✅ Complete | 13 integration tests added, 34/34 passing |
| 05.5 AC Verify | ✅ Complete | 4/4 ACs PASS |
| 06 Deferral | ✅ Complete | No deferrals |
| 07 DoD Update | ✅ Complete | All DoD items marked complete |

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|
| src/claude/skills/coaching-entrepreneur/references/confidence-building-patterns.md | Created | ~102 |
| src/claude/skills/coaching-entrepreneur/references/imposter-syndrome-interventions.md | Created | ~82 |
| src/claude/agents/business-coach.md | Created | ~62 |
| tests/STORY-469/test_ac1_confidence_patterns.py | Created | ~130 |
| tests/STORY-469/test_ac2_imposter_syndrome.py | Created | ~130 |
| tests/STORY-469/test_ac3_subagent_confidence.py | Created | ~100 |
| tests/STORY-469/test_ac4_evidence_affirmation.py | Created | ~120 |
| tests/STORY-469/test_integration.py | Created | ~471 |

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-21 | .claude/story-requirements-analyst | Created | Story created from EPIC-072 Feature 5 | STORY-469.story.md |
| 2026-03-04 | .claude/qa-result-interpreter | QA Deep | PASSED: 34/34 tests, 0 violations, 100% traceability | - |

## Notes

**Source Requirements:** FR-005
**Design Decisions:**
- "Validate then redirect" is the core pattern — borrowed from counseling psychology
- Evidence-based affirmation uses actual progress data to be credible, not patronizing

---

Story Template Version: 2.9
Last Updated: 2026-02-21

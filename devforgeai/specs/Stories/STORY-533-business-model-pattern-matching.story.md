---
id: STORY-533
title: Business Model Pattern Matching
type: feature
epic: EPIC-073
sprint: Sprint-23
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

# Story: Business Model Pattern Matching

## Description

**As a** startup founder using the DevForgeAI planning skill,
**I want** automatic detection of my business model type from Lean Canvas data with model-specific guidance and viability scoring,
**so that** I receive relevant frameworks and an objective assessment of business viability before committing development resources.

## Acceptance Criteria

> **IMPORTANT:** XML acceptance criteria format is REQUIRED for automated verification.

### XML Acceptance Criteria Format

### AC#1: Business Model Detection from Lean Canvas

```xml
<acceptance_criteria id="AC1" implements="SVC-001">
  <given>A completed Lean Canvas with populated fields (revenue streams, customer segments, channels, cost structure)</given>
  <when>The business model detection phase executes</when>
  <then>The system identifies one primary business model type from the supported set (SaaS, marketplace, service, product) with a confidence indicator (high/medium/low)</then>
  <verification>
    <source_files>
      <file hint="Business model patterns">src/claude/skills/planning-business/references/business-model-patterns.md</file>
    </source_files>
    <test_file>tests/STORY-533/test_ac1_model_detection.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Model-Specific Reference Loading

```xml
<acceptance_criteria id="AC2" implements="SVC-002">
  <given>A detected business model type</given>
  <when>The detection phase completes</when>
  <then>The system loads the corresponding model-specific guidance from business-model-patterns.md and presents relevant frameworks, metrics, and considerations for that model type</then>
  <verification>
    <source_files>
      <file hint="Business model patterns">src/claude/skills/planning-business/references/business-model-patterns.md</file>
    </source_files>
    <test_file>tests/STORY-533/test_ac2_reference_loading.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Viability Scoring Rubric with Pass/Fail

```xml
<acceptance_criteria id="AC3" implements="SVC-003">
  <given>A detected business model and Lean Canvas data</given>
  <when>The viability scoring phase executes</when>
  <then>The system produces a numerical score (0-100) with a clear PASS (>=70) / FAIL (<50) / BORDERLINE (50-69) outcome and per-dimension breakdowns</then>
  <verification>
    <source_files>
      <file hint="Viability scoring rubric">src/claude/skills/planning-business/references/viability-scoring.md</file>
    </source_files>
    <test_file>tests/STORY-533/test_ac3_viability_scoring.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Financial Guidance Disclaimer

```xml
<acceptance_criteria id="AC4" implements="SVC-004">
  <given>Any viability scoring output</given>
  <when>The score and assessment are presented to the user</when>
  <then>The output includes a clearly visible disclaimer stating that the scoring is directional guidance only and does not constitute financial, investment, or legal advice</then>
  <verification>
    <source_files>
      <file hint="Viability scoring">src/claude/skills/planning-business/references/viability-scoring.md</file>
    </source_files>
    <test_file>tests/STORY-533/test_ac4_disclaimer.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#5: Ambiguous Model Handling

```xml
<acceptance_criteria id="AC5" implements="SVC-005">
  <given>Lean Canvas data that matches multiple business model types with similar confidence (within 0.1)</given>
  <when>The detection phase executes</when>
  <then>The system presents the top candidates ranked by confidence, explains the ambiguity, and uses AskUserQuestion to let the user select the intended model before proceeding</then>
  <verification>
    <source_files>
      <file hint="Business model patterns">src/claude/skills/planning-business/references/business-model-patterns.md</file>
    </source_files>
    <test_file>tests/STORY-533/test_ac5_ambiguous_model.sh</test_file>
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
      name: "business-model-patterns"
      file_path: "src/claude/skills/planning-business/references/business-model-patterns.md"
      required_keys:
        - key: "model_definitions"
          type: "object"
          example: "SaaS, marketplace, service, product pattern definitions"
          required: true
          validation: "Must define 4 model types with detection signals"
          test_requirement: "Test: Verify 4 model type definitions present"
        - key: "detection_signals"
          type: "object"
          example: "Canvas field patterns that indicate each model type"
          required: true
          validation: "Each model type has specific field matching criteria"
          test_requirement: "Test: Verify detection signals for each model type"
        - key: "model_guidance"
          type: "object"
          example: "Frameworks, metrics, and considerations per model"
          required: true
          validation: "Each model has guidance section"
          test_requirement: "Test: Verify guidance exists for each model type"

    - type: "Configuration"
      name: "viability-scoring"
      file_path: "src/claude/skills/planning-business/references/viability-scoring.md"
      required_keys:
        - key: "scoring_rubric"
          type: "object"
          example: "Dimension scores with weights"
          required: true
          validation: "Must define scoring dimensions with numeric weights"
          test_requirement: "Test: Verify scoring dimensions and weights defined"
        - key: "outcome_thresholds"
          type: "object"
          example: "PASS >= 70, BORDERLINE 50-69, FAIL < 50"
          required: true
          validation: "Three outcome levels with numeric thresholds"
          test_requirement: "Test: Verify threshold definitions"
        - key: "disclaimer"
          type: "string"
          example: "This scoring is directional guidance only..."
          required: true
          validation: "Disclaimer text present and non-empty"
          test_requirement: "Test: Verify disclaimer text present"

    - type: "DataModel"
      name: "BusinessModelDetection"
      table: "N/A (in-memory)"
      purpose: "Detection result for business model type"
      fields:
        - name: "model_type"
          type: "Enum"
          constraints: "Required, one of: saas, marketplace, service, product"
          description: "Detected business model type"
          test_requirement: "Test: Verify model_type is valid enum value"
        - name: "confidence"
          type: "Enum"
          constraints: "Required, one of: high, medium, low"
          description: "Detection confidence level"
          test_requirement: "Test: Verify confidence is valid enum value"
        - name: "matching_signals"
          type: "Array"
          constraints: "Required, non-empty"
          description: "Canvas fields that drove the match"
          test_requirement: "Test: Verify matching signals are populated"

    - type: "DataModel"
      name: "ViabilityScore"
      table: "N/A (in-memory)"
      purpose: "Viability assessment result"
      fields:
        - name: "overall_score"
          type: "Int"
          constraints: "Required, range 0-100"
          description: "Overall viability score"
          test_requirement: "Test: Verify score in range 0-100"
        - name: "outcome"
          type: "Enum"
          constraints: "Required, one of: PASS, FAIL, BORDERLINE"
          description: "Binary/ternary outcome"
          test_requirement: "Test: Verify outcome matches threshold rules"
        - name: "dimensions"
          type: "Array"
          constraints: "Required"
          description: "Per-dimension score breakdowns"
          test_requirement: "Test: Verify dimension scores present"

  business_rules:
    - id: "BR-001"
      rule: "Detection uses only Lean Canvas field data as input; no external API calls"
      trigger: "Model detection phase"
      validation: "No external network calls during detection"
      error_handling: "N/A - design constraint"
      test_requirement: "Test: Verify no external API calls in detection"
      priority: "Critical"
    - id: "BR-002"
      rule: "Confidence thresholds: high >= 0.8, medium >= 0.5, low < 0.5"
      trigger: "Confidence calculation"
      validation: "Confidence levels match thresholds"
      error_handling: "Auto-classify based on score"
      test_requirement: "Test: Verify confidence threshold boundaries"
      priority: "High"
    - id: "BR-003"
      rule: "If top two candidates within 0.1 confidence, trigger ambiguity flow"
      trigger: "Multi-model match detection"
      validation: "AskUserQuestion presented for ambiguous matches"
      error_handling: "User selects model via AskUserQuestion"
      test_requirement: "Test: Verify ambiguity detection at 0.1 threshold"
      priority: "High"
    - id: "BR-004"
      rule: "Viability thresholds: PASS >= 70, BORDERLINE 50-69, FAIL < 50"
      trigger: "Score evaluation"
      validation: "Outcome matches score against thresholds"
      error_handling: "Auto-classify"
      test_requirement: "Test: Verify outcome classification at boundary values"
      priority: "Critical"
    - id: "BR-005"
      rule: "Disclaimer text MUST NOT be omitted regardless of score outcome"
      trigger: "Score presentation"
      validation: "Disclaimer present in all outputs"
      error_handling: "HALT if disclaimer missing"
      test_requirement: "Test: Verify disclaimer present in all score outputs"
      priority: "Critical"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Detection and scoring completes within 5 seconds"
      metric: "< 5 seconds (excluding user interaction)"
      test_requirement: "Test: Verify phase completion time"
      priority: "Medium"
    - id: "NFR-002"
      category: "Performance"
      requirement: "Total token consumption under 8K tokens"
      metric: "< 8,000 tokens (including reference loading)"
      test_requirement: "Test: Verify token count"
      priority: "High"
    - id: "NFR-003"
      category: "Maintainability"
      requirement: "Adding new model type requires only reference file changes, no logic changes"
      metric: "Zero code changes for new model addition"
      test_requirement: "Test: Verify extensibility via reference files only"
      priority: "Medium"
```

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "Business Model Detection"
    limitation: "Detection based on text pattern matching of Lean Canvas fields; cannot validate business model accuracy"
    decision: "workaround:Include disclaimer and confidence levels; user confirms selection"
    discovered_phase: "Architecture"
    impact: "Detection is suggestive, not authoritative; user selection overrides"
```

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- **Detection + scoring phase:** < 5 seconds (excluding user interaction)

**Performance Test:**
- Verify token overhead < 8K

---

### Security

**Authentication:**
- None (local CLI tool)

**Data Protection:**
- Business data stored locally
- Disclaimer required on all scoring output

**Security Testing:**
- [ ] No hardcoded secrets
- [ ] Disclaimer text always included

---

### Scalability

- Not applicable (CLI tool)

---

### Reliability

**Error Handling:**
- Missing reference files: HALT with file path
- Incomplete Lean Canvas: Surface missing fields
- All-zero scores: Flag as invalid input

---

### Observability

**Logging:**
- INFO: Detected model type, confidence score, viability outcome
- WARN: Ambiguous match, incomplete canvas fields

---

## Dependencies

### Prerequisite Stories

- [ ] **STORY-531:** Lean Canvas Guided Workflow
  - **Why:** Model detection reads Lean Canvas output
  - **Status:** Not Started

### External Dependencies

None

### Technology Dependencies

None — uses existing Claude Code framework tools

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+

**Test Scenarios:**
1. **Happy Path:** SaaS detection from typical Canvas data
2. **Edge Cases:**
   - Incomplete Canvas (missing fields)
   - Hybrid model (two types similar confidence)
   - All-zero viability scores
3. **Error Cases:**
   - Missing reference files
   - Empty Canvas data

---

### Integration Tests

**Coverage Target:** 85%+

**Test Scenarios:**
1. **Full pipeline:** Lean Canvas → Model detection → Scoring → Display
2. **Ambiguity flow:** User selects from multiple candidates

---

## Acceptance Criteria Verification Checklist

**Purpose:** Real-time progress tracking during TDD implementation.

**Tracking Mechanisms:**
- **TodoWrite:** Phase-level tracking
- **AC Checklist:** AC sub-item tracking ← YOU ARE HERE
- **Definition of Done:** Official completion record

### AC#1: Business Model Detection

- [ ] 4 model type definitions in reference file - **Phase:** 2 - **Evidence:** business-model-patterns.md
- [ ] Detection signals per model type - **Phase:** 2 - **Evidence:** business-model-patterns.md
- [ ] Confidence indicator (high/medium/low) - **Phase:** 1 - **Evidence:** tests/STORY-533/

### AC#2: Model-Specific Reference Loading

- [ ] Guidance loaded for detected model - **Phase:** 2 - **Evidence:** business-model-patterns.md
- [ ] Frameworks and metrics presented - **Phase:** 2 - **Evidence:** business-model-patterns.md

### AC#3: Viability Scoring

- [ ] Scoring rubric with numeric dimensions - **Phase:** 2 - **Evidence:** viability-scoring.md
- [ ] PASS/FAIL/BORDERLINE thresholds - **Phase:** 1 - **Evidence:** tests/STORY-533/
- [ ] Per-dimension breakdowns - **Phase:** 1 - **Evidence:** tests/STORY-533/

### AC#4: Financial Disclaimer

- [ ] Disclaimer text in all scoring output - **Phase:** 2 - **Evidence:** viability-scoring.md

### AC#5: Ambiguous Model Handling

- [ ] Ambiguity detection at 0.1 threshold - **Phase:** 2 - **Evidence:** business-model-patterns.md
- [ ] AskUserQuestion for model selection - **Phase:** 2 - **Evidence:** business-model-patterns.md

---

**Checklist Progress:** 0/11 items complete (0%)

---

<!-- IMPLEMENTATION NOTES FORMAT REQUIREMENT (Critical for pre-commit validation):
When filling in the Implementation Notes section during /dev workflow:
1. DoD items MUST be placed DIRECTLY under "## Implementation Notes" header
2. NO ### subsection headers before DoD items
See: .claude/skills/implementing-stories/references/dod-update-workflow.md for complete details
-->

## Implementation Notes

*To be filled during /dev workflow*

## Definition of Done

### Implementation
- [ ] Reference file created at src/claude/skills/planning-business/references/business-model-patterns.md
- [ ] Reference file created at src/claude/skills/planning-business/references/viability-scoring.md
- [ ] 4 model types defined (SaaS, marketplace, service, product)
- [ ] Detection signals linked to Canvas fields
- [ ] Scoring rubric with numeric dimensions and PASS/FAIL/BORDERLINE thresholds
- [ ] Disclaimer text included in all scoring output

### Quality
- [ ] All 5 acceptance criteria have passing tests
- [ ] Edge cases covered (incomplete canvas, hybrid model, all-zero scores)
- [ ] Disclaimer present in all outputs
- [ ] Token overhead < 8K
- [ ] Code coverage > 95% for business logic

### Testing
- [ ] Unit tests for model detection
- [ ] Unit tests for viability scoring thresholds
- [ ] Integration test for full detection+scoring pipeline
- [ ] Edge case tests for ambiguous models

### Documentation
- [ ] Business model patterns documented
- [ ] Viability scoring rubric documented
- [ ] Adding new model types documented

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
| 2026-03-03 | .claude/story-requirements-analyst | Created | Story created from EPIC-073 Feature 3 | STORY-533-business-model-pattern-matching.story.md |

## Notes

**Design Decisions:**
- 4 model types (SaaS, marketplace, service, product) cover most solo founder scenarios
- Viability scoring is guidance only — disclaimer is mandatory per epic safety requirements
- Ambiguity threshold of 0.1 prevents silent wrong classification
- Model patterns are reference-file driven for extensibility

**Open Questions:**
- [ ] Scoring dimension weights per model type - **Owner:** DevForgeAI - **Due:** Sprint 2

**References:**
- EPIC-073: Business Planning & Viability
- Lean Canvas business model types

---

Story Template Version: 2.9
Last Updated: 2026-03-03

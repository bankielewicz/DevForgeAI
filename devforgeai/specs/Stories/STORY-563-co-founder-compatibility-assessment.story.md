---
id: STORY-563
title: Co-Founder Compatibility Assessment
type: feature
epic: EPIC-079
sprint: Sprint-29
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

# Story: Co-Founder Compatibility Assessment

## Description

**As a** solo founder considering bringing on a co-founder,
**I want** a structured compatibility assessment questionnaire that evaluates complementary skills, values, vision alignment, work style, conflict resolution approaches, and equity expectations,
**so that** I can make an informed partnership decision with a clear understanding of strengths and risk areas before committing.

## Acceptance Criteria

> **IMPORTANT:** XML acceptance criteria format is REQUIRED for automated verification.

### XML Acceptance Criteria Format

### AC#1: Questionnaire Dimensions Cover All Six Evaluation Areas

```xml
<acceptance_criteria id="AC1" implements="SVC-001">
  <given>The co-founder assessment skill file exists at the designated path</given>
  <when>The file content is parsed for questionnaire dimensions</when>
  <then>It contains structured questions for all six dimensions: complementary skills, values alignment, vision alignment, work style compatibility, conflict resolution approach, and equity expectations — with a minimum of 3 questions per dimension (18+ total questions)</then>
  <verification>
    <source_files>
      <file hint="Assessment reference file">src/claude/skills/building-team/references/co-founder-assessment.md</file>
    </source_files>
    <test_file>tests/STORY-563/test_ac1_questionnaire_dimensions.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Scoring Rubric Produces Quantifiable Compatibility Scores

```xml
<acceptance_criteria id="AC2" implements="SVC-002">
  <given>A completed questionnaire with responses for all dimensions</given>
  <when>The scoring rubric is applied</when>
  <then>Each dimension receives a numeric score on a 1-5 scale, an overall compatibility score is computed as a weighted average, and score thresholds are defined (1.0-2.0 = High Risk, 2.1-3.5 = Moderate Concern, 3.6-5.0 = Strong Alignment)</then>
  <verification>
    <source_files>
      <file hint="Assessment reference file">src/claude/skills/building-team/references/co-founder-assessment.md</file>
    </source_files>
    <test_file>tests/STORY-563/test_ac2_scoring_rubric.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Report Template Generates Actionable Output

```xml
<acceptance_criteria id="AC3" implements="SVC-003">
  <given>Scored questionnaire responses across all six dimensions</given>
  <when>The report template is populated</when>
  <then>The output Markdown file contains: a summary table of dimension scores, a strengths section listing dimensions scoring 3.6+, a risk areas section listing dimensions scoring 2.0 or below, and at least one recommended conversation topic per risk area</then>
  <verification>
    <source_files>
      <file hint="Assessment reference file">src/claude/skills/building-team/references/co-founder-assessment.md</file>
    </source_files>
    <test_file>tests/STORY-563/test_ac3_report_template.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Skill File Follows DevForgeAI Skill Reference Format

```xml
<acceptance_criteria id="AC4" implements="SVC-001,SVC-002,SVC-003">
  <given>The skill file is created</given>
  <when>Validated against DevForgeAI skill conventions</when>
  <then>It includes: a structured questionnaire section with numbered questions per dimension, a scoring rubric section with explicit numeric scales, a report template section with placeholder tokens, and guidance text for the interactive workflow</then>
  <verification>
    <source_files>
      <file hint="Assessment reference file">src/claude/skills/building-team/references/co-founder-assessment.md</file>
    </source_files>
    <test_file>tests/STORY-563/test_ac4_skill_format.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### Source Files Guidance

All implementation in a single skill reference Markdown file.

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Service"
      name: "CoFounderCompatibilityAssessment"
      file_path: "src/claude/skills/building-team/references/co-founder-assessment.md"
      interface: "Markdown skill reference"
      lifecycle: "Static"
      dependencies:
        - "building-team SKILL.md"
      requirements:
        - id: "SVC-001"
          description: "Structured questionnaire with 6 dimensions and minimum 3 questions per dimension (18+ total)"
          testable: true
          test_requirement: "Test: Count dimensions = 6, count questions per dimension >= 3"
          priority: "Critical"
        - id: "SVC-002"
          description: "Scoring rubric with 1-5 scale per dimension and defined thresholds (High Risk, Moderate Concern, Strong Alignment)"
          testable: true
          test_requirement: "Test: Scoring section contains 1-5 scale definition and 3 threshold ranges"
          priority: "Critical"
        - id: "SVC-003"
          description: "Report template with summary table, strengths, risk areas, and recommended conversations"
          testable: true
          test_requirement: "Test: Report template contains all 4 required output sections"
          priority: "High"

  business_rules:
    - id: "BR-001"
      rule: "Equity expectations marked 'undecided' score 1.0 with mandatory discussion flag"
      trigger: "Equity dimension response is 'not yet discussed' or 'undecided'"
      validation: "Score is set to 1.0 and flag note is added"
      error_handling: "Display critical pre-partnership discussion warning"
      test_requirement: "Test: Undecided equity response produces score 1.0 with flag"
      priority: "High"
    - id: "BR-002"
      rule: "All dimensions scoring identically produces 'deeper exploration needed' message"
      trigger: "All 6 dimension scores are equal"
      validation: "No empty strengths or risk areas sections"
      error_handling: "Display exploration guidance message"
      test_requirement: "Test: Equal scores across all dimensions produces exploration message"
      priority: "Medium"
    - id: "BR-003"
      rule: "Single-perspective assessments carry lower confidence rating"
      trigger: "Only one party completes the assessment"
      validation: "Report labels perspective type clearly"
      error_handling: "Display reduced confidence warning"
      test_requirement: "Test: Single-perspective report includes confidence warning"
      priority: "Medium"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Skill file < 500 lines of Markdown"
      metric: "< 500 lines"
      test_requirement: "Test: wc -l returns < 500"
      priority: "Medium"
    - id: "NFR-002"
      category: "Reliability"
      requirement: "Partial completion renders correctly for completed dimensions"
      metric: "0 rendering errors on partial data"
      test_requirement: "Test: File with 3/6 dimensions completed produces valid Markdown"
      priority: "High"
    - id: "NFR-003"
      category: "Scalability"
      requirement: "New dimensions can be added without modifying scoring logic"
      metric: "Each dimension is self-contained with its own weight parameter"
      test_requirement: "Test: Adding a 7th dimension section does not break existing scoring"
      priority: "Medium"
```

---

## Technical Limitations

```yaml
technical_limitations: []
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- Questionnaire completion: Estimated 15-25 minutes per participant (documented in guidance)
- File generation: Single write operation

---

### Security

**Data Protection:**
- No personal data collection beyond local Markdown files
- No external API calls or data transmission
- Output written only to `devforgeai/specs/business/team/` directory

---

### Scalability

**Extensibility:**
- New dimensions addable without modifying scoring rubric logic
- Question count per dimension: 3-10 without breaking score calculation

---

### Reliability

**Error Handling:**
- All 6 dimensions render correctly with partial completion
- Report template produces valid Markdown with 0 rendering errors

---

### Observability

**Logging:**
- Score calculation logged per dimension for debugging

---

## Dependencies

### Prerequisite Stories

- None required

### External Dependencies

- None

### Technology Dependencies

- None (Markdown files only)

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for business logic

**Test Scenarios:**
1. **Happy Path:** All 6 dimensions scored, report generated with strengths and risk areas
2. **Edge Cases:**
   - All scores identical (3.0) → exploration message
   - Equity marked undecided → score 1.0 with flag
   - Single-perspective → confidence warning
   - No dimensions below 2.0 or above 3.6 → special handling
3. **Error Cases:**
   - Partial completion (3/6 dimensions)
   - Score out of range validation

---

### Integration Tests

**Coverage Target:** 85%+

**Test Scenarios:**
1. **End-to-End Assessment Flow:** Complete questionnaire, generate report, verify output
2. **Dual-perspective comparison:** Two sets of responses compared

---

## Acceptance Criteria Verification Checklist

### AC#1: Questionnaire Dimensions

- [ ] 6 dimensions present - **Phase:** 2 - **Evidence:** co-founder-assessment.md
- [ ] 3+ questions per dimension - **Phase:** 2 - **Evidence:** co-founder-assessment.md
- [ ] 18+ total questions - **Phase:** 2 - **Evidence:** co-founder-assessment.md

### AC#2: Scoring Rubric

- [ ] 1-5 scale defined - **Phase:** 2 - **Evidence:** co-founder-assessment.md
- [ ] Weighted average formula - **Phase:** 2 - **Evidence:** co-founder-assessment.md
- [ ] 3 threshold ranges defined - **Phase:** 2 - **Evidence:** co-founder-assessment.md

### AC#3: Report Template

- [ ] Summary table section - **Phase:** 2 - **Evidence:** co-founder-assessment.md
- [ ] Strengths section - **Phase:** 2 - **Evidence:** co-founder-assessment.md
- [ ] Risk areas section - **Phase:** 2 - **Evidence:** co-founder-assessment.md
- [ ] Recommended conversations - **Phase:** 2 - **Evidence:** co-founder-assessment.md

### AC#4: Skill Format

- [ ] Numbered questions per dimension - **Phase:** 2 - **Evidence:** co-founder-assessment.md
- [ ] Scoring rubric section - **Phase:** 2 - **Evidence:** co-founder-assessment.md

---

**Checklist Progress:** 0/12 items complete (0%)

---

<!-- IMPLEMENTATION NOTES FORMAT REQUIREMENT (Critical for pre-commit validation):
See: .claude/skills/implementing-stories/references/dod-update-workflow.md for complete details
-->

## Implementation Notes

*To be filled during /dev workflow*

## Definition of Done

### Implementation
- [ ] Skill reference file created at src/claude/skills/building-team/references/co-founder-assessment.md
- [ ] 6 questionnaire dimensions with 3+ questions each
- [ ] Scoring rubric with 1-5 scale and threshold definitions
- [ ] Report template with summary, strengths, risk areas, conversations
- [ ] Guidance text for interactive workflow

### Quality
- [ ] All 4 acceptance criteria have passing tests
- [ ] Edge cases covered (equal scores, undecided equity, single-perspective)
- [ ] Data validation enforced (score range 1-5, dimension count = 6)
- [ ] NFRs met (file < 500 lines)

### Testing
- [ ] Unit tests for scoring rubric
- [ ] Unit tests for edge cases
- [ ] Integration test for end-to-end assessment flow

### Documentation
- [ ] Skill reference file self-documenting
- [ ] "Conversation starter, not verdict" framing included
- [ ] "Consult a business advisor" recommendations included

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
| 2026-03-03 | .claude/story-requirements-analyst | Created | Story created from EPIC-079 Feature 2 | STORY-563.story.md |

## Notes

**Design Decisions:**
- Scoring uses weighted average to allow dimension importance customization
- "Ideal profile" mode supported for founders without a specific candidate
- Report framed as conversation starter, not definitive verdict

**Safety Considerations:**
- Include "consult a business advisor" for equity discussions
- Emphasize that no assessment replaces extended real-world collaboration
- Frame as iterative evaluation tool

---

Story Template Version: 2.9
Last Updated: 2026-03-03

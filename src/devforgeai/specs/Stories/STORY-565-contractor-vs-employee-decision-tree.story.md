---
id: STORY-565
title: Contractor vs Employee Decision Tree
type: feature
epic: EPIC-079
sprint: Sprint-29
status: Ready for Dev
points: 1
depends_on: ["STORY-564"]
priority: Medium
advisory: false
source_gap: null
source_story: null
assigned_to: null
created: 2026-03-03
format_version: "2.9"
---

# Story: Contractor vs Employee Decision Tree

## Description

**As a** first-time entrepreneur building a team,
**I want** a structured decision framework that walks me through contractor vs employee classification,
**so that** I can make informed workforce decisions while understanding when to seek professional legal and tax advice.

## Acceptance Criteria

> **IMPORTANT:** XML acceptance criteria format is REQUIRED for automated verification.

### XML Acceptance Criteria Format

### AC#1: Decision Tree Covers Legal Classification Factors

```xml
<acceptance_criteria id="AC1" implements="SVC-001">
  <given>The contractor-vs-employee.md reference file exists</given>
  <when>A user reads the contractor vs employee decision section</when>
  <then>The file contains at minimum 5 distinct classification factors (e.g., behavioral control, financial control, relationship type, work schedule control, equipment provision) each with a clear contractor indicator and employee indicator</then>
  <verification>
    <source_files>
      <file hint="Decision tree reference">src/claude/skills/building-team/references/contractor-vs-employee.md</file>
    </source_files>
    <test_file>tests/STORY-565/test_ac1_classification_factors.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Cost Comparison Framework with Numeric Structure

```xml
<acceptance_criteria id="AC2" implements="SVC-002">
  <given>The contractor-vs-employee.md reference file exists</given>
  <when>A user reads the cost comparison section</when>
  <then>The file includes a side-by-side comparison table covering at minimum: base compensation, payroll taxes (with approximate percentage ranges), benefits cost, equipment/tools, onboarding cost, and management overhead — for both contractor and employee classifications</then>
  <verification>
    <source_files>
      <file hint="Decision tree reference">src/claude/skills/building-team/references/contractor-vs-employee.md</file>
    </source_files>
    <test_file>tests/STORY-565/test_ac2_cost_comparison.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Professional Consultation Triggers Are Explicit

```xml
<acceptance_criteria id="AC3" implements="SVC-003">
  <given>The contractor-vs-employee.md reference file exists</given>
  <when>A user encounters a complex or high-risk scenario</when>
  <then>The file contains at minimum 3 explicit "consult a professional" trigger conditions (e.g., multi-state workers, misclassification risk, IP-heavy roles) each specifying what type of professional to consult (employment attorney, CPA, HR consultant)</then>
  <verification>
    <source_files>
      <file hint="Decision tree reference">src/claude/skills/building-team/references/contractor-vs-employee.md</file>
    </source_files>
    <test_file>tests/STORY-565/test_ac3_consultation_triggers.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#4: IP Considerations Section Present

```xml
<acceptance_criteria id="AC4" implements="SVC-004">
  <given>The contractor-vs-employee.md reference file exists</given>
  <when>A user reads the IP considerations section</when>
  <then>The file covers work-for-hire doctrine differences between contractors and employees, recommends specific agreement clauses (IP assignment, NDA), and flags jurisdictional variance as a professional-consultation trigger</then>
  <verification>
    <source_files>
      <file hint="Decision tree reference">src/claude/skills/building-team/references/contractor-vs-employee.md</file>
    </source_files>
    <test_file>tests/STORY-565/test_ac4_ip_considerations.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#5: Employment Law Disclaimer Present

```xml
<acceptance_criteria id="AC5" implements="SVC-005">
  <given>The contractor-vs-employee.md reference file exists</given>
  <when>The user reads any section of the file</when>
  <then>The file contains a prominent disclaimer within the first 20 lines stating the content is educational only, not legal advice, and that employment law varies by jurisdiction</then>
  <verification>
    <source_files>
      <file hint="Decision tree reference">src/claude/skills/building-team/references/contractor-vs-employee.md</file>
    </source_files>
    <test_file>tests/STORY-565/test_ac5_disclaimer.sh</test_file>
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
      name: "ContractorVsEmployeeDecisionTree"
      file_path: "src/claude/skills/building-team/references/contractor-vs-employee.md"
      interface: "Markdown skill reference"
      lifecycle: "Static"
      dependencies:
        - "building-team SKILL.md"
      requirements:
        - id: "SVC-001"
          description: "Decision tree with 5+ classification factors, each with contractor and employee indicators"
          testable: true
          test_requirement: "Test: Count classification factors >= 5; each has contractor and employee indicators"
          priority: "Critical"
        - id: "SVC-002"
          description: "Side-by-side cost comparison table covering 6+ cost categories"
          testable: true
          test_requirement: "Test: Cost comparison table contains rows for compensation, taxes, benefits, equipment, onboarding, overhead"
          priority: "High"
        - id: "SVC-003"
          description: "3+ explicit professional consultation triggers with professional type specified"
          testable: true
          test_requirement: "Test: Count 'consult a professional' triggers >= 3; each specifies professional type"
          priority: "Critical"
        - id: "SVC-004"
          description: "IP considerations section covering work-for-hire, agreement clauses, jurisdictional variance"
          testable: true
          test_requirement: "Test: IP section contains work-for-hire, IP assignment, NDA, jurisdictional flag"
          priority: "High"
        - id: "SVC-005"
          description: "Prominent disclaimer within first 20 lines: educational only, not legal advice"
          testable: true
          test_requirement: "Test: Disclaimer appears within first 20 lines of file body"
          priority: "Critical"

  business_rules:
    - id: "BR-001"
      rule: "Decision tree applies to US-based scenarios only; international hiring flagged for specialist consultation"
      trigger: "Cross-border hiring mentioned"
      validation: "US-only scope clearly stated; international callout present"
      error_handling: "Direct to international employment specialist"
      test_requirement: "Test: US-only scope statement present; international callout present"
      priority: "High"
    - id: "BR-002"
      rule: "Contractor-to-employee conversion addressed with misclassification drift warnings"
      trigger: "Hybrid role or evolving relationship"
      validation: "Conversion checklist and warning signs documented"
      error_handling: "Flag for professional review"
      test_requirement: "Test: Conversion section with warning signs and checklist present"
      priority: "Medium"
    - id: "BR-003"
      rule: "Part-time status does not automatically equal contractor classification"
      trigger: "Part-time or fractional role described"
      validation: "Part-time guidance explicitly addresses classification independently"
      error_handling: "Display part-time classification guidance"
      test_requirement: "Test: Part-time section states classification is independent of hours"
      priority: "Medium"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "File size < 30 KB"
      metric: "< 30 KB Markdown text"
      test_requirement: "Test: File size < 30 KB"
      priority: "Medium"
    - id: "NFR-002"
      category: "Reliability"
      requirement: "All internal Markdown links resolve correctly"
      metric: "0 broken internal links"
      test_requirement: "Test: All anchor links resolve within file"
      priority: "High"
    - id: "NFR-003"
      category: "Scalability"
      requirement: "Modular format allows adding classification factors without restructuring"
      metric: "Each factor is self-contained subsection"
      test_requirement: "Test: Each factor is an independent H3 section"
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

**File Size:**
- < 30 KB of Markdown text
- Renders < 2 seconds in standard viewers

---

### Security

**Data Protection:**
- No PII in examples — fictional names and placeholder values only
- No specific legal citations mistakable for current binding law
- General references with "as of [date], verify current status" qualifiers

---

### Scalability

**Extensibility:**
- Modular H2/H3 structure for adding factors or jurisdictional notes
- New factors addable in < 5 minutes of editing

---

### Reliability

**Error Handling:**
- All internal Markdown links resolve correctly (0 broken links)
- Valid Markdown structure

---

### Observability

**Logging:**
- N/A (static reference file)

---

## Dependencies

### Prerequisite Stories

- [ ] **STORY-564:** /build-team Command & Skill Assembly
  - **Why:** Skill infrastructure must exist before adding this reference file
  - **Status:** Backlog

### External Dependencies

- None

### Technology Dependencies

- None (Markdown files only)

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+

**Test Scenarios:**
1. **Happy Path:** All sections present, decision tree complete, disclaimer in first 20 lines
2. **Edge Cases:**
   - International hiring callout present
   - Part-time classification guidance independent of hours
   - Contractor-to-employee conversion checklist
   - Glossary for first-time founders
3. **Error Cases:**
   - Broken internal links detection

---

### Integration Tests

**Coverage Target:** 85%+

**Test Scenarios:**
1. **Skill Integration:** Reference file loaded correctly by building-team SKILL.md
2. **Output Generation:** Decision tree produces workforce-strategy.md output

---

## Acceptance Criteria Verification Checklist

### AC#1: Classification Factors

- [ ] 5+ distinct factors present - **Phase:** 2 - **Evidence:** contractor-vs-employee.md
- [ ] Each factor has contractor indicator - **Phase:** 2 - **Evidence:** contractor-vs-employee.md
- [ ] Each factor has employee indicator - **Phase:** 2 - **Evidence:** contractor-vs-employee.md

### AC#2: Cost Comparison

- [ ] Side-by-side table present - **Phase:** 2 - **Evidence:** contractor-vs-employee.md
- [ ] 6+ cost categories covered - **Phase:** 2 - **Evidence:** contractor-vs-employee.md

### AC#3: Consultation Triggers

- [ ] 3+ trigger conditions - **Phase:** 2 - **Evidence:** contractor-vs-employee.md
- [ ] Professional type specified per trigger - **Phase:** 2 - **Evidence:** contractor-vs-employee.md

### AC#4: IP Considerations

- [ ] Work-for-hire differences covered - **Phase:** 2 - **Evidence:** contractor-vs-employee.md
- [ ] IP assignment and NDA clauses recommended - **Phase:** 2 - **Evidence:** contractor-vs-employee.md

### AC#5: Disclaimer

- [ ] Disclaimer within first 20 lines - **Phase:** 2 - **Evidence:** contractor-vs-employee.md
- [ ] Educational-only framing - **Phase:** 2 - **Evidence:** contractor-vs-employee.md

---

**Checklist Progress:** 0/11 items complete (0%)

---

<!-- IMPLEMENTATION NOTES FORMAT REQUIREMENT -->

## Implementation Notes

*To be filled during /dev workflow*

## Definition of Done

### Implementation
- [ ] Reference file created at src/claude/skills/building-team/references/contractor-vs-employee.md
- [ ] 5+ classification factors with dual indicators
- [ ] Cost comparison table with 6+ categories
- [ ] 3+ professional consultation triggers
- [ ] IP considerations section
- [ ] Disclaimer within first 20 lines

### Quality
- [ ] All 5 acceptance criteria have passing tests
- [ ] Edge cases covered (international, part-time, conversion)
- [ ] All internal links resolve (0 broken)
- [ ] NFRs met (file < 30 KB, valid Markdown)

### Testing
- [ ] Unit tests for structure validation
- [ ] Unit tests for content requirements
- [ ] Integration test for skill reference loading

### Documentation
- [ ] Self-documenting with clear section structure
- [ ] Key terms defined for first-time founders
- [ ] "Consult a professional" triggers prominent

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
| 2026-03-03 | .claude/story-requirements-analyst | Created | Story created from EPIC-079 Feature 4 | STORY-565.story.md |

## Notes

**Design Decisions:**
- Decision tree uses structured format (not prose) for clarity
- US-only scope with international hiring callout
- Conversion path addressed for contractor→employee transitions
- Glossary included for founders unfamiliar with employment terminology

**Safety Considerations:**
- Educational-only framing — never prescriptive language
- "Consult a professional" at every legal threshold
- IRS guidelines referenced generally with "verify current status"
- Misclassification risks prominently warned

---

Story Template Version: 2.9
Last Updated: 2026-03-03

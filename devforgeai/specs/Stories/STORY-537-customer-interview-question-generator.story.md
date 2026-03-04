---
id: STORY-537
title: Customer Interview Question Generator
type: feature
epic: EPIC-074
sprint: Sprint-24
status: Ready for Dev
points: 2
depends_on: ["STORY-535"]
priority: High
advisory: false
source_gap: null
source_story: null
assigned_to: DevForgeAI AI Agent
created: 2026-03-03
format_version: "2.9"
---

# Story: Customer Interview Question Generator

## Description

**As a** startup founder validating business assumptions,
**I want** the `researching-market` skill to generate hypothesis-driven customer interview questions with best practices guidance,
**so that** I can conduct structured interviews that validate or invalidate specific business model assumptions before committing resources.

## Provenance

```xml
<provenance>
  <origin document="BRAINSTORM-011" section="business-skills-framework">
    <quote>"Enable DevForgeAI users to validate their business ideas through structured market research"</quote>
    <line_reference>EPIC-074, lines 57-61</line_reference>
    <quantified_impact>Customer interview generator produces 10-20 hypothesis-aligned questions</quantified_impact>
  </origin>
  <stakeholder role="Entrepreneur" goal="validate-assumptions">
    <quote>"What should I ask potential customers?"</quote>
    <source>EPIC-074, line 24</source>
  </stakeholder>
  <hypothesis id="H1" validation="interview-execution" success_criteria="Users can validate/invalidate at least 1 business assumption per interview session">
    Hypothesis-driven interview questions produce more actionable insights than generic customer discovery questions
  </hypothesis>
</provenance>
```

## Acceptance Criteria

> **IMPORTANT:** XML acceptance criteria format is REQUIRED for automated verification.

### XML Acceptance Criteria Format

```xml
<acceptance_criteria id="AC1" implements="COMP-XXX">
  <given>Initial context or precondition</given>
  <when>Action or event being tested</when>
  <then>Expected outcome or result</then>
</acceptance_criteria>
```

### AC#1: Interview Question Output Structure

```xml
<acceptance_criteria id="AC1" implements="SVC-001">
  <given>The researching-market skill has completed market research phases and identified business hypotheses</given>
  <when>The interview question generation phase executes</when>
  <then>The skill writes devforgeai/specs/business/market-research/customer-interviews.md containing 10-20 questions organized under hypothesis headings, where each hypothesis section contains 2-5 questions</then>
  <verification>
    <source_files>
      <file hint="Skill file">src/claude/skills/researching-market/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-537/test_ac1_question_output.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Best Practices Reference File

```xml
<acceptance_criteria id="AC2" implements="SVC-002">
  <given>The interview question generation phase is invoked</given>
  <when>The skill needs interviewing methodology guidance</when>
  <then>A reference file at src/claude/skills/researching-market/references/customer-interview-guide.md exists containing interviewing best practices (open-ended question techniques, bias avoidance, follow-up patterns), and the skill reads this file during question generation</then>
  <verification>
    <source_files>
      <file hint="Interview guide reference">src/claude/skills/researching-market/references/customer-interview-guide.md</file>
    </source_files>
    <test_file>tests/STORY-537/test_ac2_reference_file.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Hypothesis-Driven Questions

```xml
<acceptance_criteria id="AC3" implements="BR-001">
  <given>Market research has identified specific business assumptions</given>
  <when>Interview questions are generated</when>
  <then>Each question maps to a named hypothesis, avoids leading phrasing, and is open-ended (starts with How, What, Tell me about, Describe, or Walk me through)</then>
  <verification>
    <source_files>
      <file hint="Skill file">src/claude/skills/researching-market/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-537/test_ac3_hypothesis_driven.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Skill Size Compliance

```xml
<acceptance_criteria id="AC4" implements="SVC-003">
  <given>The researching-market skill has existing phases</given>
  <when>The interview question generation phase is added</when>
  <then>The total skill file remains under 1,000 lines with deep documentation delegated to the reference file</then>
  <verification>
    <source_files>
      <file hint="Skill file">src/claude/skills/researching-market/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-537/test_ac4_skill_size.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#5: Parseable Output Structure

```xml
<acceptance_criteria id="AC5" implements="SVC-004">
  <given>The interview question generation phase completes</given>
  <when>customer-interviews.md is written</when>
  <then>The file contains YAML frontmatter (date, hypothesis count, question count), hypothesis sections with ## headers, numbered questions under each, and a Next Steps section</then>
  <verification>
    <source_files>
      <file hint="Skill file">src/claude/skills/researching-market/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-537/test_ac5_output_structure.py</test_file>
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
    - type: "Service"
      name: "InterviewQuestionPhase"
      file_path: "src/claude/skills/researching-market/SKILL.md"
      interface: "Skill Phase"
      lifecycle: "On-demand"
      dependencies:
        - "AskUserQuestion tool"
        - "Read tool (reference file)"
        - "Write tool (output file)"
      requirements:
        - id: "SVC-001"
          description: "Generate 10-20 hypothesis-driven interview questions organized by hypothesis headings"
          testable: true
          test_requirement: "Test: Output contains 10-20 questions across hypothesis sections, 2-5 per hypothesis"
          priority: "Critical"
        - id: "SVC-002"
          description: "Read and apply best practices from customer-interview-guide.md reference file"
          testable: true
          test_requirement: "Test: Generated questions follow open-ended patterns from reference file"
          priority: "High"
        - id: "SVC-003"
          description: "Skill remains under 1,000 lines after phase addition"
          testable: true
          test_requirement: "Test: SKILL.md line count < 1,000"
          priority: "High"
        - id: "SVC-004"
          description: "Output file has YAML frontmatter, hypothesis sections, numbered questions, Next Steps"
          testable: true
          test_requirement: "Test: Output has YAML frontmatter with date/counts, ## hypothesis headers, numbered questions, ## Next Steps"
          priority: "High"

    - type: "Configuration"
      name: "customer-interview-guide"
      file_path: "src/claude/skills/researching-market/references/customer-interview-guide.md"
      required_keys:
        - key: "Open-ended techniques"
          type: "string"
          required: true
          validation: "Section present with question patterns"
          test_requirement: "Test: File contains section on open-ended question techniques"
        - key: "Bias avoidance"
          type: "string"
          required: true
          validation: "Section present with anti-patterns"
          test_requirement: "Test: File contains section on avoiding leading questions"
        - key: "Follow-up patterns"
          type: "string"
          required: true
          validation: "Section present with follow-up examples"
          test_requirement: "Test: File contains section on follow-up question techniques"

  business_rules:
    - id: "BR-001"
      rule: "All questions must be open-ended and map to a named hypothesis"
      trigger: "During question generation"
      validation: "No closed-ended questions (yes/no answerable); each question linked to hypothesis"
      error_handling: "Reject closed-ended questions and regenerate as open-ended"
      test_requirement: "Test: No questions start with Do/Is/Are/Was/Were/Will/Would/Can/Could/Should/Did/Has"
      priority: "Critical"
    - id: "BR-002"
      rule: "Question count must be 10-20 total, 2-5 per hypothesis"
      trigger: "After question generation complete"
      validation: "Count total and per-hypothesis questions"
      error_handling: "< 10 triggers regeneration; > 20 triggers pruning"
      test_requirement: "Test: Total 10-20, each hypothesis has 2-5 questions"
      priority: "High"
    - id: "BR-003"
      rule: "Zero hypotheses triggers HALT with AskUserQuestion"
      trigger: "When no hypotheses identified from prior research"
      validation: "Check hypothesis count before generation"
      error_handling: "HALT and prompt user to articulate at least one assumption"
      test_requirement: "Test: Zero hypotheses triggers AskUserQuestion prompt"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Question generation phase completes in under 30 seconds"
      metric: "< 30s wall clock time"
      test_requirement: "Test: Measure phase execution time"
      priority: "Medium"
    - id: "NFR-002"
      category: "Reliability"
      requirement: "Atomic write - no partial output on failure"
      metric: "Zero partial files on disk after any failure"
      test_requirement: "Test: Simulate mid-generation failure, verify no partial file"
      priority: "High"
    - id: "NFR-003"
      category: "Reliability"
      requirement: "Idempotent - re-running overwrites cleanly"
      metric: "No duplicate content on re-run"
      test_requirement: "Test: Run twice, verify single clean output"
      priority: "Medium"
```

---

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "Hypothesis identification"
    limitation: "Quality of hypotheses depends on prior market research phases"
    decision: "workaround:HALT and prompt user when zero hypotheses found"
    discovered_phase: "Architecture"
    impact: "Question quality is only as good as the hypotheses generated upstream"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- Question generation: < 30 seconds wall clock
- Reference file read: < 500ms
- Output file write: < 1 second

---

### Security

**Data Protection:**
- No customer PII in generated question files
- No hardcoded API keys, tokens, or credentials

---

### Scalability

**Design Limits:**
- Up to 10 hypotheses per session (2-5 questions each, max 20 total)
- Reference file can grow to 500 lines

---

### Reliability

**Error Handling:**
- Atomic write (generate in memory, write once)
- Idempotent execution

---

### Observability

**Logging:**
- Log hypothesis count and question count generated

---

## Dependencies

### Prerequisite Stories

- [ ] **STORY-535:** Market Sizing Guided Workflow
  - **Why:** Creates the researching-market skill that this story extends
  - **Status:** Backlog

### External Dependencies

- [ ] **None**

### Technology Dependencies

- [ ] **None:** Uses existing framework tools

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for business logic

**Test Scenarios:**
1. **Happy Path:** 4 hypotheses, 3 questions each (12 total), all open-ended
2. **Edge Cases:**
   - Zero hypotheses → HALT with AskUserQuestion
   - Single broad hypothesis → split into sub-hypotheses
   - Solution-biased hypothesis → reframed questions
   - Output directory doesn't exist → created
3. **Error Cases:**
   - Closed-ended question rejected
   - < 10 questions triggers regeneration
   - > 20 questions triggers pruning

---

### Integration Tests

**Coverage Target:** 85%+ for application layer

**Test Scenarios:**
1. **Skill Phase Flow:** Verify interview phase integrates with existing skill phases
2. **Reference File Read:** Verify customer-interview-guide.md loaded during generation

---

## Acceptance Criteria Verification Checklist

### AC#1: Interview Question Output

- [ ] Output file created at correct path - **Phase:** 2 - **Evidence:** tests/STORY-537/test_ac1_question_output.py
- [ ] 10-20 questions total - **Phase:** 2 - **Evidence:** tests/STORY-537/test_ac1_question_output.py
- [ ] Questions organized by hypothesis - **Phase:** 2 - **Evidence:** tests/STORY-537/test_ac1_question_output.py
- [ ] 2-5 questions per hypothesis - **Phase:** 2 - **Evidence:** tests/STORY-537/test_ac1_question_output.py

### AC#2: Best Practices Reference

- [ ] Reference file exists at correct path - **Phase:** 2 - **Evidence:** tests/STORY-537/test_ac2_reference_file.py
- [ ] Contains open-ended techniques section - **Phase:** 2 - **Evidence:** tests/STORY-537/test_ac2_reference_file.py
- [ ] Contains bias avoidance section - **Phase:** 2 - **Evidence:** tests/STORY-537/test_ac2_reference_file.py

### AC#3: Hypothesis-Driven Questions

- [ ] Each question maps to a hypothesis - **Phase:** 3 - **Evidence:** tests/STORY-537/test_ac3_hypothesis_driven.py
- [ ] No leading phrasing - **Phase:** 3 - **Evidence:** tests/STORY-537/test_ac3_hypothesis_driven.py
- [ ] All questions open-ended - **Phase:** 3 - **Evidence:** tests/STORY-537/test_ac3_hypothesis_driven.py

### AC#4: Skill Size Compliance

- [ ] SKILL.md under 1,000 lines - **Phase:** 3 - **Evidence:** tests/STORY-537/test_ac4_skill_size.py

### AC#5: Parseable Output

- [ ] YAML frontmatter present - **Phase:** 3 - **Evidence:** tests/STORY-537/test_ac5_output_structure.py
- [ ] ## hypothesis headers present - **Phase:** 3 - **Evidence:** tests/STORY-537/test_ac5_output_structure.py
- [ ] Next Steps section present - **Phase:** 3 - **Evidence:** tests/STORY-537/test_ac5_output_structure.py

---

**Checklist Progress:** 0/14 items complete (0%)

---

<!-- IMPLEMENTATION NOTES FORMAT REQUIREMENT (Critical for pre-commit validation):
When filling in the Implementation Notes section during /dev workflow:
1. DoD items MUST be placed DIRECTLY under "## Implementation Notes" header
2. NO ### subsection headers before DoD items
See: .claude/skills/implementing-stories/references/dod-update-workflow.md for complete details
-->

## Implementation Notes

*To be filled during implementation*

## Definition of Done

### Implementation
- [ ] Add interview question generation phase to `src/claude/skills/researching-market/SKILL.md`
- [ ] Create `src/claude/skills/researching-market/references/customer-interview-guide.md`
- [ ] Implement hypothesis-driven question generation logic
- [ ] Implement open-ended question validation
- [ ] Implement output generation to `devforgeai/specs/business/market-research/customer-interviews.md`

### Quality
- [ ] All 5 acceptance criteria have passing tests
- [ ] Edge cases covered (zero hypotheses, broad hypothesis, solution bias, missing directory)
- [ ] Data validation enforced (10-20 questions, 2-5 per hypothesis, open-ended only)
- [ ] NFRs met (30s generation, atomic write, idempotent)
- [ ] Skill under 1,000 lines

### Testing
- [ ] Unit tests for question count validation
- [ ] Unit tests for open-ended question filtering
- [ ] Unit tests for hypothesis-question mapping
- [ ] Integration tests for skill phase flow
- [ ] Integration tests for reference file loading

### Documentation
- [ ] customer-interview-guide.md contains best practices
- [ ] Phase documented in SKILL.md
- [ ] Edge case handling documented

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
| 2026-03-03 | .claude/story-requirements-analyst | Created | Story created from EPIC-074 Feature 3 | STORY-537-customer-interview-question-generator.story.md |

## Notes

**Design Decisions:**
- Hypothesis-driven over generic question generation for more actionable insights
- Atomic write pattern to prevent partial file corruption
- Reference file for best practices keeps skill under line limit

**References:**
- EPIC-074: Market Research & Competition
- BRAINSTORM-011: Business Skills Framework

---

Story Template Version: 2.9
Last Updated: 2026-03-03

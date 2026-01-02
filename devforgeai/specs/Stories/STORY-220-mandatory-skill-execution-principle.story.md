---
id: STORY-220
title: Document Mandatory Skill Execution Principle
type: documentation
epic: EPIC-031
sprint: null
status: Backlog
points: 1
depends_on: []
priority: High
assigned_to: null
created: 2025-01-01
format_version: "2.5"
source_rca: RCA-022
source_recommendation: REC-4
---

# Story: Document Mandatory Skill Execution Principle

## Description

**As a** DevForgeAI framework user (Claude or future AI agents),
**I want** explicit documentation that skill phases are mandatory protocol (not optional guidelines),
**so that** I understand skills are state machines requiring complete execution of all phases.

**Background:**
RCA-022 root cause analysis identified that Claude treated skill documentation as optional guidance rather than mandatory protocol, leading to skipped phases and subagent invocations during STORY-128. This story implements REC-4 to add explicit clarification to CLAUDE.md about non-negotiable skill execution discipline.

## Acceptance Criteria

### AC#1: New Section in CLAUDE.md

**Given** the CLAUDE.md project instructions file,
**When** this story is complete,
**Then** a new section "CRITICAL: No Deviation from Skill Phases" exists after the "Skill Execution Model" section.

---

### AC#2: Fundamental Principle Documented

**Given** the new CLAUDE.md section,
**When** I read the fundamental principle,
**Then** it explicitly states:
- Skills are NOT guidelines that can be optimized or skipped
- Skills are state machines where EVERY phase MUST execute in order
- EVERY validation checkpoint MUST be verified
- EVERY [MANDATORY] step MUST be completed

---

### AC#3: Examples of Wrong vs Right Behavior

**Given** the new CLAUDE.md section,
**When** I read the examples,
**Then** it includes:
- At least 3 examples of WRONG behavior (with ❌ markers)
- At least 3 examples of RIGHT behavior (with ✅ markers)
- Specific scenarios related to subagent invocations and phase skipping

---

### AC#4: Self-Test Checkpoint

**Given** the new CLAUDE.md section,
**When** I read the self-test checkpoint,
**Then** it provides a clear test to verify skill execution compliance:
- "If you didn't invoke all [MANDATORY] subagents, you skipped required phases. HALT and complete them."

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Documentation"
      name: "Mandatory Execution Principle Section"
      file_path: "CLAUDE.md"
      purpose: "Add explicit clarification about non-negotiable skill execution discipline"
      requirements:
        - id: "DOC-001"
          description: "Add new section 'CRITICAL: No Deviation from Skill Phases' after line 118 in Skill Execution Model"
          testable: true
          test_requirement: "Test: Grep for '## CRITICAL: No Deviation from Skill Phases' in CLAUDE.md"
          priority: "Critical"
        - id: "DOC-002"
          description: "Document fundamental principle that skills are state machines with mandatory phases"
          testable: true
          test_requirement: "Test: Grep for 'Skills are NOT guidelines' in new section"
          priority: "Critical"
        - id: "DOC-003"
          description: "Provide 3+ examples of WRONG behavior with ❌ markers"
          testable: true
          test_requirement: "Test: Count '❌' markers in section >= 3"
          priority: "High"
        - id: "DOC-004"
          description: "Provide 3+ examples of RIGHT behavior with ✅ markers"
          testable: true
          test_requirement: "Test: Count '✅' markers in section >= 3"
          priority: "High"
        - id: "DOC-005"
          description: "Include self-test checkpoint for skill execution verification"
          testable: true
          test_requirement: "Test: Grep for 'Test:.*MANDATORY.*subagents' in section"
          priority: "High"

  business_rules:
    - id: "BR-001"
      rule: "Section must be positioned after 'Skill Execution Model' section for logical flow"
      trigger: "When adding new section to CLAUDE.md"
      validation: "New section appears after line 118 (current Skill Execution Model end)"
      error_handling: "If positioned elsewhere, may not be read in proper context"
      test_requirement: "Test: Verify section position after 'Skill Execution Model'"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Readability"
      requirement: "Section must be clear, actionable, and use bold formatting for emphasis"
      metric: "All key principles use **bold** or ❌/✅ markers for visual clarity"
      test_requirement: "Test: Manual readability review confirms clarity"
      priority: "High"

    - id: "NFR-002"
      category: "Maintainability"
      requirement: "Section under 50 lines to maintain CLAUDE.md readability"
      metric: "< 50 lines added to CLAUDE.md"
      test_requirement: "Test: Line count of new section < 50 lines"
      priority: "Medium"
```

---

## Technical Limitations

None - documentation only.

---

## Non-Functional Requirements

### Readability

**Clarity:**
- Use bold formatting for key principles
- Use ❌/✅ markers for visual distinction
- Examples must be specific and concrete

### Maintainability

**Size Constraint:**
- New section MUST be under 50 lines
- Follow existing CLAUDE.md formatting patterns

---

## Dependencies

### Prerequisite Stories

None - this is a standalone documentation update.

### External Dependencies

None.

### Technology Dependencies

None - documentation only.

---

## Test Strategy

### Unit Tests

**Coverage Target:** 100% verification of documentation patterns

**Test Scenarios:**
1. **Section Exists:** Grep for "## CRITICAL: No Deviation from Skill Phases"
2. **Fundamental Principle Present:** Grep for "Skills are NOT guidelines"
3. **Wrong Behavior Examples:** Count ❌ markers >= 3
4. **Right Behavior Examples:** Count ✅ markers >= 3
5. **Self-Test Checkpoint:** Grep for self-test language

### Integration Tests

**Coverage Target:** Manual verification during next /dev execution

**Test Scenarios:**
1. **Section Visibility:** Verify section loads with CLAUDE.md
2. **Readability:** Verify instructions are clear and actionable
3. **Positioning:** Verify section appears in logical location after Skill Execution Model

---

## Acceptance Criteria Verification Checklist

### AC#1: New Section in CLAUDE.md

- [ ] Section header added: "## CRITICAL: No Deviation from Skill Phases" - **Phase:** 3 - **Evidence:** CLAUDE.md grep
- [ ] Section positioned after "Skill Execution Model" section - **Phase:** 3 - **Evidence:** CLAUDE.md line position

### AC#2: Fundamental Principle Documented

- [ ] States skills are NOT guidelines - **Phase:** 3 - **Evidence:** CLAUDE.md section content
- [ ] States skills are state machines - **Phase:** 3 - **Evidence:** CLAUDE.md section content
- [ ] Lists 4 MUST requirements (phases, checkpoints, mandatory steps, skipping rules) - **Phase:** 3 - **Evidence:** CLAUDE.md section content

### AC#3: Examples of Wrong vs Right Behavior

- [ ] At least 3 WRONG behavior examples with ❌ - **Phase:** 3 - **Evidence:** Count ❌ markers
- [ ] At least 3 RIGHT behavior examples with ✅ - **Phase:** 3 - **Evidence:** Count ✅ markers
- [ ] Examples are specific to subagent/phase scenarios - **Phase:** 3 - **Evidence:** Manual review

### AC#4: Self-Test Checkpoint

- [ ] Self-test checkpoint documented - **Phase:** 3 - **Evidence:** CLAUDE.md section content
- [ ] Test mentions [MANDATORY] subagents - **Phase:** 3 - **Evidence:** CLAUDE.md section content
- [ ] Test includes HALT instruction - **Phase:** 3 - **Evidence:** CLAUDE.md section content

---

**Checklist Progress:** 0/11 items complete (0%)

---

## Definition of Done

### Implementation
- [ ] New section added to CLAUDE.md after line 118
- [ ] Fundamental principle documented with 4 MUST requirements
- [ ] 3+ WRONG behavior examples with ❌ markers
- [ ] 3+ RIGHT behavior examples with ✅ markers
- [ ] Self-test checkpoint included
- [ ] Section under 50 lines
- [ ] Bold formatting for key principles

### Quality
- [ ] All 4 acceptance criteria addressed
- [ ] Examples are specific and actionable
- [ ] Terminology consistent with existing CLAUDE.md
- [ ] Clear visual distinction using markers

### Testing
- [ ] Grep tests for section existence
- [ ] Grep tests for fundamental principle keywords
- [ ] Count tests for ❌/✅ markers
- [ ] Manual readability review

### Documentation
- [ ] Section self-documenting
- [ ] Cross-references to RCA-022 included
- [ ] References to skill execution model

---

## Change Log

**Current Status:** Backlog

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2025-01-01 12:30 | claude/story-requirements-analyst | Created | Story created from RCA-022 REC-4 | STORY-220.story.md |

## Notes

**Source RCA:**
- RCA-022: Mandatory TDD Phases Skipped During STORY-128 Development
- Recommendation: REC-4 (HIGH priority)

**Design Decisions:**
- Position section after "Skill Execution Model" for logical flow
- Use existing CLAUDE.md formatting patterns (bold, markers)
- Keep under 50 lines for maintainability
- Focus on actionable guidance, not abstract philosophy

**Exact Content from RCA-022 REC-4:**
The RCA provides the exact text to add (lines 416-439), which should be used as the implementation template.

**Related RCAs:**
- [RCA-022: Mandatory TDD Phases Skipped](../../RCA/RCA-022-mandatory-tdd-phases-skipped.md)

**References:**
- RCA-022: REC-4 implementation details (lines 399-461)
- CLAUDE.md: Current Skill Execution Model section (lines 104-118)

---

**Story Template Version:** 2.5
**Last Updated:** 2025-01-01

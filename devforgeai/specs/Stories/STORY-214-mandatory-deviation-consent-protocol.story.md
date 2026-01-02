---
id: STORY-214
title: Mandatory Deviation Consent Protocol
type: feature
epic: EPIC-031
sprint: null
status: Backlog
points: 2
depends_on: []
priority: High
assigned_to: null
created: 2025-01-01
format_version: "2.5"
source_rca: RCA-019
source_recommendation: REC-4
---

# Story: Mandatory Deviation Consent Protocol

## Description

**As a** DevForgeAI framework user,
**I want** the development skill to require explicit user consent before any workflow deviation,
**so that** I am always aware when phases are being skipped and can approve or reject deviations.

**Background:**
RCA-019 identified that Claude can rationalize workflow deviations (phase skipping, subagent omission) without user awareness. This story implements REC-4 from RCA-019 to require AskUserQuestion before ANY deviation from the documented TDD workflow.

## Acceptance Criteria

### AC#1: Workflow Deviation Protocol Section

**Given** the devforgeai-development SKILL.md file,
**When** this story is complete,
**Then** a new "Workflow Deviation Protocol" section exists that documents the mandatory consent requirements.

---

### AC#2: AskUserQuestion Enforcement for Phase Skipping

**Given** Claude considers skipping a TDD phase (0-10),
**When** the deviation is considered,
**Then** AskUserQuestion MUST be invoked with:
- Question explaining the specific deviation considered
- Options: "Follow workflow", "Skip with documentation", "User override"
- No deviation occurs without explicit user selection

---

### AC#3: AskUserQuestion Enforcement for Subagent Omission

**Given** Claude considers skipping a required subagent invocation,
**When** the subagent is defined as MANDATORY in the phase file,
**Then** AskUserQuestion MUST be invoked before omitting the subagent invocation.

---

### AC#4: Documentation Requirement for Approved Deviations

**Given** the user selects "Skip with documentation" option,
**When** the deviation is authorized,
**Then** the story file Implementation Notes section MUST be updated with:
- Deviation description
- User authorization timestamp
- Impact assessment

---

### AC#5: RCA Trigger for Documented Deviations

**Given** the user selects "Skip with documentation" option,
**When** the deviation is authorized,
**Then** a recommendation is provided to invoke `/rca` for the deviation reason (optional, not blocking).

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Documentation"
      name: "Workflow Deviation Protocol"
      file_path: ".claude/skills/devforgeai-development/SKILL.md"
      purpose: "Add new section documenting mandatory deviation consent requirements"
      requirements:
        - id: "DOC-001"
          description: "Add 'Workflow Deviation Protocol' section after existing workflow documentation"
          testable: true
          test_requirement: "Test: Grep for '## Workflow Deviation Protocol' in SKILL.md"
          priority: "Critical"
        - id: "DOC-002"
          description: "Document three deviation types: phase skipping, subagent omission, out-of-sequence execution"
          testable: true
          test_requirement: "Test: Grep for deviation type documentation in SKILL.md"
          priority: "High"
        - id: "DOC-003"
          description: "Include AskUserQuestion template with mandatory options"
          testable: true
          test_requirement: "Test: Grep for 'AskUserQuestion' pattern in deviation protocol section"
          priority: "Critical"

    - type: "Documentation"
      name: "Deviation Response Processing"
      file_path: ".claude/skills/devforgeai-development/SKILL.md"
      purpose: "Document how each user response option is processed"
      requirements:
        - id: "DOC-004"
          description: "Document 'Follow workflow' option processing (proceed with required execution)"
          testable: true
          test_requirement: "Test: Grep for 'Follow workflow' processing logic"
          priority: "High"
        - id: "DOC-005"
          description: "Document 'Skip with documentation' option (story file update required)"
          testable: true
          test_requirement: "Test: Grep for story file update requirements in skip option"
          priority: "High"
        - id: "DOC-006"
          description: "Document 'User override' option (timestamp and authorization recording)"
          testable: true
          test_requirement: "Test: Grep for timestamp and authorization requirements"
          priority: "High"

  business_rules:
    - id: "BR-001"
      rule: "All workflow deviations require explicit user consent via AskUserQuestion"
      trigger: "When Claude considers skipping phase, subagent, or modifying phase order"
      validation: "AskUserQuestion must be called before any deviation"
      error_handling: "If AskUserQuestion not called, deviation is forbidden"
      test_requirement: "Test: Verify protocol section mandates AskUserQuestion"
      priority: "Critical"

    - id: "BR-002"
      rule: "Deviation documentation must include timestamp and user authorization"
      trigger: "When user approves deviation via 'Skip with documentation' or 'User override'"
      validation: "Story file Implementation Notes must be updated"
      error_handling: "If story file not updated, deviation is not properly recorded"
      test_requirement: "Test: Verify documentation requirements in protocol"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Compliance"
      requirement: "Protocol aligns with architecture-constraints.md HALT pattern"
      metric: "100% alignment with existing HALT pattern documentation"
      test_requirement: "Test: Verify protocol uses HALT terminology consistent with architecture-constraints.md"
      priority: "High"

    - id: "NFR-002"
      category: "Maintainability"
      requirement: "Protocol section under 100 lines to maintain SKILL.md size constraints"
      metric: "< 100 lines added to SKILL.md"
      test_requirement: "Test: Line count of new section < 100 lines"
      priority: "Medium"
```

---

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "Claude Code Terminal"
    limitation: "No technical enforcement mechanism to prevent Claude from ignoring AskUserQuestion requirement"
    decision: "workaround:Document protocol as MANDATORY with HALT instruction, rely on prompt engineering"
    discovered_phase: "Architecture"
    impact: "Protocol relies on Claude self-discipline to invoke AskUserQuestion; this is a documentation-based enforcement"
```

---

## Non-Functional Requirements

### Compliance

**Architecture Alignment:**
- Protocol MUST use HALT pattern terminology from architecture-constraints.md
- Protocol MUST align with existing error handling patterns

### Maintainability

**Size Constraint:**
- New section MUST be under 100 lines
- MUST follow progressive disclosure pattern (reference files if needed)

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
1. **Protocol Section Exists:** Grep for "## Workflow Deviation Protocol" in SKILL.md
2. **AskUserQuestion Template Present:** Grep for AskUserQuestion pattern
3. **Three Options Documented:** Grep for "Follow workflow", "Skip with documentation", "User override"
4. **Documentation Requirements Present:** Grep for story file update requirements

### Integration Tests

**Coverage Target:** Manual verification during /dev execution

**Test Scenarios:**
1. **Protocol Visibility:** Verify protocol section loads with SKILL.md
2. **Readability:** Verify protocol instructions are clear and actionable

---

## Acceptance Criteria Verification Checklist

### AC#1: Workflow Deviation Protocol Section

- [ ] Protocol section header added to SKILL.md - **Phase:** 3 - **Evidence:** SKILL.md grep
- [ ] Section positioned appropriately in document structure - **Phase:** 3 - **Evidence:** SKILL.md review

### AC#2: AskUserQuestion Enforcement for Phase Skipping

- [ ] AskUserQuestion template documented for phase skipping - **Phase:** 3 - **Evidence:** SKILL.md section
- [ ] Question format specified - **Phase:** 3 - **Evidence:** SKILL.md section
- [ ] Three mandatory options documented - **Phase:** 3 - **Evidence:** SKILL.md section

### AC#3: AskUserQuestion Enforcement for Subagent Omission

- [ ] Subagent omission deviation documented - **Phase:** 3 - **Evidence:** SKILL.md section
- [ ] Mandatory vs optional subagent distinction documented - **Phase:** 3 - **Evidence:** SKILL.md section

### AC#4: Documentation Requirement for Approved Deviations

- [ ] Story file update requirements documented - **Phase:** 3 - **Evidence:** SKILL.md section
- [ ] Timestamp requirement documented - **Phase:** 3 - **Evidence:** SKILL.md section
- [ ] Implementation Notes section usage documented - **Phase:** 3 - **Evidence:** SKILL.md section

### AC#5: RCA Trigger for Documented Deviations

- [ ] RCA recommendation documented for deviations - **Phase:** 3 - **Evidence:** SKILL.md section
- [ ] Optional (not blocking) nature clarified - **Phase:** 3 - **Evidence:** SKILL.md section

---

**Checklist Progress:** 0/12 items complete (0%)

---

## Definition of Done

### Implementation
- [ ] Workflow Deviation Protocol section added to SKILL.md
- [ ] AskUserQuestion template documented with three options
- [ ] Phase skipping deviation flow documented
- [ ] Subagent omission deviation flow documented
- [ ] Documentation requirements for approved deviations specified
- [ ] RCA recommendation for deviations documented
- [ ] Section under 100 lines

### Quality
- [ ] All 5 acceptance criteria addressed in documentation
- [ ] Protocol aligns with architecture-constraints.md HALT pattern
- [ ] Protocol uses consistent terminology
- [ ] Clear, actionable instructions provided

### Testing
- [ ] Grep tests for protocol section existence
- [ ] Grep tests for AskUserQuestion template
- [ ] Grep tests for three option types
- [ ] Manual readability review

### Documentation
- [ ] Protocol section self-documenting
- [ ] References to related RCA (RCA-019) included
- [ ] Cross-references to architecture-constraints.md added

---

## Change Log

**Current Status:** Backlog

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2025-01-01 12:00 | claude/story-requirements-analyst | Created | Story created from RCA-019 REC-4 | STORY-214.story.md |

## Notes

**Source RCA:**
- RCA-019: Development Skill Phase Skipping - Lack of Enforcement Mechanism
- Recommendation: REC-4 (HIGH priority)

**Design Decisions:**
- Documentation-based enforcement chosen (no external tooling required)
- Protocol section kept under 100 lines for maintainability
- Three-option structure provides clear, non-blocking choices

**Related RCAs:**
- [RCA-019: Development Skill Phase Skipping](../../RCA/RCA-019-development-skill-phase-skipping-enforcement.md)

**References:**
- architecture-constraints.md: HALT pattern for gate failures (lines 116-132)
- RCA-019: REC-4 implementation details

---

**Story Template Version:** 2.5
**Last Updated:** 2025-01-01

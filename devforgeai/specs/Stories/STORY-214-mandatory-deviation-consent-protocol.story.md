---
id: STORY-214
title: Mandatory Deviation Consent Protocol
type: feature
epic: EPIC-031
sprint: null
status: Dev Complete
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

- [x] Protocol section header added to SKILL.md - **Phase:** 3 - **Evidence:** SKILL.md grep TEST-001 PASS
- [x] Section positioned appropriately in document structure - **Phase:** 3 - **Evidence:** Lines 206-254, after Purpose, before When to Use

### AC#2: AskUserQuestion Enforcement for Phase Skipping

- [x] AskUserQuestion template documented for phase skipping - **Phase:** 3 - **Evidence:** SKILL.md lines 224-234 TEST-002 PASS
- [x] Question format specified - **Phase:** 3 - **Evidence:** SKILL.md lines 225-233
- [x] Three mandatory options documented - **Phase:** 3 - **Evidence:** TEST-003, TEST-004, TEST-005 PASS

### AC#3: AskUserQuestion Enforcement for Subagent Omission

- [x] Subagent omission deviation documented - **Phase:** 3 - **Evidence:** TEST-007 PASS
- [x] Mandatory vs optional subagent distinction documented - **Phase:** 3 - **Evidence:** SKILL.md line 219, TEST-009 PASS

### AC#4: Documentation Requirement for Approved Deviations

- [x] Story file update requirements documented - **Phase:** 3 - **Evidence:** SKILL.md lines 239-244, TEST-012 PASS
- [x] Timestamp requirement documented - **Phase:** 3 - **Evidence:** SKILL.md line 242-243, TEST-010 PASS
- [x] Implementation Notes section usage documented - **Phase:** 3 - **Evidence:** SKILL.md line 242, TEST-011 PASS

### AC#5: RCA Trigger for Documented Deviations

- [x] RCA recommendation documented for deviations - **Phase:** 3 - **Evidence:** SKILL.md line 245, TEST-013 PASS
- [x] Optional (not blocking) nature clarified - **Phase:** 3 - **Evidence:** SKILL.md line 245 "(Optional - not blocking)", TEST-014 PASS

---

**Checklist Progress:** 12/12 items complete (100%)

---

## Definition of Done

### Implementation
- [x] Workflow Deviation Protocol section added to SKILL.md - Completed: Section at lines 206-254
- [x] AskUserQuestion template documented with three options - Completed: Lines 224-234 with Follow workflow, Skip with documentation, User override
- [x] Phase skipping deviation flow documented - Completed: Deviation Types table, row 1
- [x] Subagent omission deviation flow documented - Completed: Deviation Types table, row 2 + MANDATORY vs OPTIONAL note
- [x] Documentation requirements for approved deviations specified - Completed: Response Processing table with story file update requirements
- [x] RCA recommendation for deviations documented - Completed: Line 245 with /rca command suggestion
- [x] Section under 100 lines - Completed: 49 lines (TEST-016 verifies < 100)

### Quality
- [x] All 5 acceptance criteria addressed in documentation - Completed: AC#1-AC#5 all verified (12/12 checklist items)
- [x] Protocol aligns with architecture-constraints.md HALT pattern - Completed: Line 249 references lines 116-132, TEST-015 PASS
- [x] Protocol uses consistent terminology - Completed: Uses HALT, MANDATORY, AskUserQuestion per architecture-constraints.md
- [x] Clear, actionable instructions provided - Completed: Code block template, response table, enforcement notes

### Testing
- [x] Grep tests for protocol section existence - Completed: TEST-001 PASS
- [x] Grep tests for AskUserQuestion template - Completed: TEST-002 PASS
- [x] Grep tests for three option types - Completed: TEST-003, TEST-004, TEST-005 PASS
- [x] Manual readability review - Completed: code-reviewer approved, refactoring-specialist confirmed "No refactoring required"

### Documentation
- [x] Protocol section self-documenting - Completed: Section includes Purpose, Deviation Types, Consent Protocol, Response Processing, Enforcement Notes
- [x] References to related RCA (RCA-019) included - Completed: Line 208 "(Source: RCA-019 REC-4)"
- [x] Cross-references to architecture-constraints.md added - Completed: Lines 249-251

---

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-01-13
**Branch:** refactor/devforgeai-migration

- [x] Workflow Deviation Protocol section added to SKILL.md - Completed: Section at lines 206-254
- [x] AskUserQuestion template documented with three options - Completed: Lines 224-234 with Follow workflow, Skip with documentation, User override
- [x] Phase skipping deviation flow documented - Completed: Deviation Types table, row 1
- [x] Subagent omission deviation flow documented - Completed: Deviation Types table, row 2 + MANDATORY vs OPTIONAL note
- [x] Documentation requirements for approved deviations specified - Completed: Response Processing table with story file update requirements
- [x] RCA recommendation for deviations documented - Completed: Line 245 with /rca command suggestion
- [x] Section under 100 lines - Completed: 49 lines (TEST-016 verifies < 100)
- [x] All 5 acceptance criteria addressed in documentation - Completed: AC#1-AC#5 all verified (12/12 checklist items)
- [x] Protocol aligns with architecture-constraints.md HALT pattern - Completed: Line 249 references lines 116-132, TEST-015 PASS
- [x] Protocol uses consistent terminology - Completed: Uses HALT, MANDATORY, AskUserQuestion per architecture-constraints.md
- [x] Clear, actionable instructions provided - Completed: Code block template, response table, enforcement notes
- [x] Grep tests for protocol section existence - Completed: TEST-001 PASS
- [x] Grep tests for AskUserQuestion template - Completed: TEST-002 PASS
- [x] Grep tests for three option types - Completed: TEST-003, TEST-004, TEST-005 PASS
- [x] Manual readability review - Completed: code-reviewer approved, refactoring-specialist confirmed "No refactoring required"
- [x] Protocol section self-documenting - Completed: Section includes Purpose, Deviation Types, Consent Protocol, Response Processing, Enforcement Notes
- [x] References to related RCA (RCA-019) included - Completed: Line 208 "(Source: RCA-019 REC-4)"
- [x] Cross-references to architecture-constraints.md added - Completed: Lines 249-251

### TDD Workflow Summary

**Phase 02 (Red): Test-First Design**
- Generated 17 comprehensive tests covering all 5 acceptance criteria
- Tests placed in tests/STORY-214/
- Test framework: Bash shell scripts with grep-based validation
- TEST-SPECIFICATION.md documents test-to-AC mapping

**Phase 03 (Green): Implementation**
- Added Workflow Deviation Protocol section to SKILL.md (lines 206-254)
- Section includes: Deviation Types table, AskUserQuestion template, Response Processing table, Enforcement Notes
- All 17 tests passing (100% pass rate)

**Phase 04 (Refactor): Code Quality**
- refactoring-specialist confirmed "No refactoring required"
- code-reviewer approved with no blocking issues
- Light QA validation passed

**Phase 05 (Integration): Full Validation**
- integration-tester validated: Section positioning, cross-references, frontmatter validity
- All 8 integration tests passed
- Section is 49 lines (well under 100-line NFR limit)

**Phase 06 (Deferral Challenge): DoD Validation**
- No deferred items detected
- All implementation complete
- 18/18 DoD items verified

### Files Modified

- `.claude/skills/devforgeai-development/SKILL.md` - Added Workflow Deviation Protocol section (lines 206-254)

### Files Created

- `tests/STORY-214/TEST-SPECIFICATION.md` - Test specification document
- `tests/STORY-214/test-ac-verification.sh` - Executable test script (17 tests)
- `tests/STORY-214/test-results.log` - Test execution results

### Test Results

- **Total tests:** 17
- **Pass rate:** 100%
- **Coverage:** All 5 ACs covered
- **Execution time:** < 1 second

---

## Change Log

**Current Status:** Dev Complete

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2025-01-01 12:00 | claude/story-requirements-analyst | Created | Story created from RCA-019 REC-4 | STORY-214.story.md |
| 2026-01-13 17:37 | claude/test-automator | Red (Phase 02) | Tests generated (17 tests, 5 ACs) | tests/STORY-214/* |
| 2026-01-13 21:30 | claude/backend-architect | Green (Phase 03) | Workflow Deviation Protocol section implemented | .claude/skills/devforgeai-development/SKILL.md |
| 2026-01-13 22:00 | claude/opus | DoD Update (Phase 07) | Development complete, DoD validated | STORY-214.story.md |

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

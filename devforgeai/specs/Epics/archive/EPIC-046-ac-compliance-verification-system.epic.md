---
id: EPIC-046
title: AC Compliance Verification System
business-value: Eliminate AC compliance gaps escaping to production through automated fresh-context verification
status: Planning
priority: High
complexity-score: 25
architecture-tier: Tier 2
created: 2026-01-19
estimated-points: 34
target-sprints: 2
source-brainstorm: BRAINSTORM-005
source-research: RESEARCH-002
---

# EPIC-046: AC Compliance Verification System

## Business Goal

Achieve **100% acceptance criteria compliance** by automating the manual workaround discovered in BRAINSTORM-005: fresh-context, one-by-one AC verification against actual source code.

**Success Metrics:**
- 0 AC compliance issues escaping to production
- Eliminate manual "separate session AC review" workaround
- All ACs verified with source code evidence before Phase 05 (Integration)

## Problem Statement

**DevForgeAI developers experience AC compliance gaps escaping to production because:**

1. QA relies on test results, not direct source code inspection against AC
2. No fresh-context verification step exists in the workflow
3. Test passing ≠ AC complete (incorrect assumption in original design)

**Root Cause:** Workflow design gap - no independent verification that AC requirements are actually met in source code.

**Evidence:** User's manual workaround (separate session AC review) achieves 100% compliance - this epic codifies that technique into the framework.

## Features

### Feature 1: Verification Subagent Core (P0 - MUST HAVE)

**Description:** Create `ac-compliance-verifier.md` subagent that performs fresh-context, one-by-one AC verification against source code.

**User Stories:**
1. [STORY-269](../Stories/STORY-269-ac-compliance-verifier-subagent-creation.story.md): AC Compliance Verifier Subagent Creation (2 pts)
2. [STORY-270](../Stories/STORY-270-xml-ac-parsing-logic.story.md): XML AC Parsing Logic (3 pts)
3. [STORY-271](../Stories/STORY-271-source-code-inspection-workflow.story.md): Source Code Inspection Workflow (3 pts)
4. [STORY-272](../Stories/STORY-272-coverage-verification-check.story.md): Coverage Verification Check (2 pts)
5. [STORY-273](../Stories/STORY-273-anti-pattern-detection-verification.story.md): Anti-Pattern Detection (2 pts)
6. [STORY-274](../Stories/STORY-274-json-report-generation.story.md): JSON Report Generation (3 pts)

**Estimated Effort:** Medium (15 story points)

### Feature 2: Phase Integration (P0 - MUST HAVE)

**Description:** Add Phase 4.5 and Phase 5.5 insertion points to devforgeai-development SKILL.md with HALT behavior on failure.

**User Stories:**
1. [STORY-275](../Stories/STORY-275-phase-4-5-insertion-point.story.md): Phase 4.5 Insertion Point (2 pts)
2. [STORY-276](../Stories/STORY-276-phase-5-5-insertion-point.story.md): Phase 5.5 Insertion Point (2 pts)
3. [STORY-277](../Stories/STORY-277-halt-behavior-on-verification-failure.story.md): HALT Behavior on Failure (2 pts)
4. [STORY-278](../Stories/STORY-278-phase-documentation-update.story.md): Phase Documentation Update (2 pts)

**Estimated Effort:** Medium (8 story points)

### Feature 3: XML AC Format (P1 - SHOULD HAVE)

**Description:** Update story template to use XML-tagged AC blocks for improved parsing accuracy.

**User Stories:**
1. [STORY-279](../Stories/STORY-279-xml-schema-design-for-ac.story.md): XML Schema Design (2 pts)
2. [STORY-280](../Stories/STORY-280-story-template-xml-ac-update.story.md): Story Template Update for XML AC (3 pts)
3. [STORY-281](../Stories/STORY-281-xml-migration-guide.story.md): XML Migration Guide (3 pts)

**Estimated Effort:** Medium (8 story points)

### Feature 4: AC-TechSpec Traceability (P1 - SHOULD HAVE)

**Description:** Add explicit `implements_ac` linking between Technical Specification COMP-XXX requirements and AC#X acceptance criteria.

**User Stories:**
1. [STORY-282](../Stories/STORY-282-techspec-schema-implements-ac.story.md): Technical Specification Schema Update (2 pts)
2. [STORY-283](../Stories/STORY-283-story-creation-traceability-automation.story.md): Story Creation Automation (2 pts)
3. [STORY-284](../Stories/STORY-284-traceability-validation.story.md): Traceability Validation (1 pt)

**Estimated Effort:** Low (5 story points)

## Requirements Summary

### Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-1 | Verify each AC against source code with fresh context | MUST |
| FR-2 | Support Phase 4.5 AND Phase 5.5 insertion points | MUST |
| FR-3 | Perform source inspection + coverage + anti-pattern detection | MUST |
| FR-4 | Require XML-tagged AC format (strict) | MUST |
| FR-5 | Persist JSON verification report per story | MUST |
| FR-6 | HALT workflow on AC failure with detailed report | MUST |
| FR-7 | Work with story files + source code as primary entities | MUST |
| FR-8 | Standalone subagent (no external integrations) | MUST |
| FR-9 | Support parallel AC verification for larger stories | SHOULD |

### Data Model

**Entities:**
- **Story File:** Existing STORY-XXX.story.md with XML AC blocks
- **Acceptance Criteria:** XML-tagged AC within story file
- **Verification Result:** JSON report with per-AC pass/fail evidence

**Relationships:**
- Story → has many → Acceptance Criteria
- Acceptance Criteria → verified by → Verification Result
- Verification Result → references → Source Files

### Integration Points

1. **devforgeai-development SKILL.md:** Invokes subagent at Phase 4.5 and 5.5
2. **Task() tool:** Standard subagent invocation pattern
3. **Story files:** Read XML AC format
4. **Source files:** Read for verification

### Non-Functional Requirements

**Performance:**
- Verification time: 60-120 seconds acceptable (quality > speed)
- Support parallel AC verification for stories with ≥5 ACs

**Security:**
- Read-only access to source files (no modifications)
- Tools restricted to: Read, Grep, Glob

**Scalability:**
- Handle stories with 1-20 acceptance criteria
- Support parallel verification where ACs are independent

**Availability:**
- Integrated into /dev workflow (always available)

## Architecture Considerations

**Complexity Tier:** Tier 2 - Moderate Application

**Recommended Architecture:**
- Pattern: Single subagent within existing framework
- File: `.claude/agents/ac-compliance-verifier.md`
- Integration: `Task(subagent_type="ac-compliance-verifier")`
- Tools: Read, Grep, Glob (read-only, principle of least privilege)

**Technology Recommendations:**
- Markdown subagent with YAML frontmatter
- JSON report format for verification results
- XML tags within existing markdown story format

## Risks & Mitigations

| Risk | Severity | Probability | Mitigation |
|------|----------|-------------|------------|
| Token overhead increases cost | LOW | 80% | User accepts tradeoff (quality > cost) |
| XML format migration effort | MEDIUM | 60% | Gradual migration, document migration guide |
| Phase 4.5 slows /dev workflow | LOW | 70% | Quality prioritized per user preference |
| Fresh context may miss implementation details | MEDIUM | 20% | Pass story file as context to subagent |
| Breaking existing /dev workflow | MEDIUM | 30% | Implement behind feature flag initially |
| Testing verification accuracy | MEDIUM | 50% | Test retrospectively on STORY-250 through STORY-268 |

## Dependencies

**Prerequisites:**
- None (can start immediately)

**Dependents:**
- Future stories requiring 100% AC compliance
- QA validation improvements

**Feature Dependencies:**
```
Feature 1 (Subagent Core) ─┬─→ Feature 2 (Phase Integration)
                          │
Feature 3 (XML AC Format) ─┴─→ Feature 4 (Traceability)
```

## Implementation Roadmap

| Sprint | Features | Milestone |
|--------|----------|-----------|
| Sprint 1 | F1 + F3 (parallel) | Subagent created, XML format defined |
| Sprint 2 | F2 + F4 (parallel) | Full integration, traceability complete |

## Hypotheses

| ID | Hypothesis | Success Metric | Validation Approach |
|----|------------|----------------|---------------------|
| H1 | XML AC tags improve parsing accuracy | 0 AC misinterpretations | Test on 5 stories |
| H2 | AC-TechSpec traceability eliminates drift | 100% COMP → AC mapping | Template enforcement |
| H3 | Phase 4.5 verification catches gaps | Issues found BEFORE integration | Compare to current state |
| H4 | Phase 5.5 confirmation is safety net | 0 issues in manual review | Eliminate manual workaround |

**Critical Hypothesis:** H3 - If implemented correctly, should eliminate need for manual workaround.

## Next Steps

1. **Sprint Planning:** Run `/create-sprint` to begin Sprint 1
2. **Story Creation:** Run `/create-story` for Feature 1 stories
3. **Development:** Run `/dev STORY-XXX` following TDD workflow

## References

- **BRAINSTORM-005:** 100% Spec Compliance for DevForgeAI
- **RESEARCH-002:** DevForgeAI Spec-Driven Framework Reliability
- **Story Analysis:** STORY-264, STORY-257, STORY-268

## Change Log

| Date | Change |
|------|--------|
| 2026-01-19 | Initial epic created from /ideate command |
| 2026-01-19 | 16 stories created (STORY-269 through STORY-284) via /create-story epic-046 |

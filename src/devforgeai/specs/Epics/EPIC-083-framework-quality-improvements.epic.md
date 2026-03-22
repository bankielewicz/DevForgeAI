---
id: EPIC-083
title: Framework Quality Improvements
status: Planning
start_date: 2026-02-22
target_date: 2026-03-15
total_points: 14
completed_points: 0
created: 2026-02-22
owner: DevForgeAI
tech_lead: DevForgeAI AI Agent
team: DevForgeAI
---

# Epic: Framework Quality Improvements

## Business Goal

Improve DevForgeAI framework quality by implementing AI-generated recommendations from workflow analysis. These improvements address documentation gaps, observation schema enhancements, and workflow validation improvements identified during story development phases.

## Success Metrics

- **Metric 1:** All 7 framework improvement recommendations converted to stories and implemented
- **Metric 2:** Zero recurring observations for addressed areas in subsequent /dev workflows
- **Metric 3:** Reduced QA fix cycles for stories touching affected subagents

**Measurement Plan:**
- Track via recommendations-queue.json (items moved to implemented)
- Monitor framework-analyst outputs for recurring themes
- Review frequency: End of epic

## Scope

### In Scope

1. **Feature 1:** Add constitutional compliance pre-check to requirements elicitation workflow
   - Add Phase N.5 step to /ideate or /create-epic that flags ADR creation as Day 0 prerequisite
   - Verify dependency graphs respect immutability rules before structural changes
   - Source: REC-EPIC081-001

2. **Feature 2:** Resolve subagent reference loading mechanism
   - Decide between orchestration-driven vs opt-in vs auto-load for subagent reference loading
   - Document decision in EPIC-082 context (partially resolved - Approach A recommended)
   - Source: REC-EPIC082-001

3. **Feature 3:** Add test pyramid exception to test-automator documentation
   - Document that pure-logic detector modules are exempt from 70/20/10 test pyramid ratio
   - Applies when no external service boundaries exist
   - Source: REC-STORY405-001

4. **Feature 4:** Add coverage gap categorization to integration-tester observation schema
   - Categorize missed coverage lines by type: defensive_guard, unreachable_code, exception_handler, fallback_path
   - Add line-type taxonomy to observation schema
   - Source: REC-STORY405-003

5. **Feature 5:** Add RED phase baseline assertion to test-automator
   - Flag tests that pass during RED phase as requiring tighter assertions
   - Add anomaly detection and baseline tracking beyond basic warning message
   - Source: REC-STORY408-001

6. **Feature 6:** Accept ADR-012 formally
   - Update ADR-012 status from 'Proposed' to 'Accepted'
   - Add implementation evidence section citing 20+ agents using the pattern
   - Source: REC-EPIC081-002

7. **Feature 7:** Document sibling story pattern reuse protocol
   - Document efficiency pattern from EPIC-064 where test structure/fixture patterns are reused
   - Add protocol to observation-capture.md (batch-sibling-story-session-template.md exists but protocol undocumented)
   - Source: REC-STORY405-002

### Out of Scope

- ❌ New subagent creation (documentation/config changes only)
- ❌ Changes to core TDD workflow phases
- ❌ Breaking changes to existing skill interfaces

## Target Sprints

### Sprint 1: All Features (Single Sprint)
**Goal:** Implement all 7 framework improvements
**Estimated Points:** 14
**Features:** All features (1-7) — each is small (1-2 points, 15-30 min effort)

**Key Deliverables:**
- Updated discovering-requirements SKILL.md with compliance pre-check
- Resolved reference loading decision in EPIC-082
- Updated test-automator.md with pyramid exception
- Updated integration-tester.md with gap categorization
- Updated test-automator RED phase with baseline assertion
- ADR-012 status updated to Accepted
- Updated observation-capture.md with sibling pattern protocol

## User Stories

1. **As a** framework user, **I want** constitutional compliance pre-checks during ideation, **so that** ADR requirements are identified before story creation
2. **As a** framework maintainer, **I want** the reference loading mechanism decided, **so that** EPIC-082 stories have clear implementation guidance
3. **As a** developer, **I want** test pyramid exceptions documented, **so that** pure-logic modules aren't flagged for missing integration tests
4. **As a** developer, **I want** coverage gaps categorized by type, **so that** remediation is targeted to the right gap category
5. **As a** developer, **I want** RED phase baseline assertions, **so that** accidentally passing tests are caught before GREEN phase
6. **As a** framework maintainer, **I want** ADR-012 formally accepted, **so that** its de facto standard status is official
7. **As a** developer, **I want** sibling story reuse patterns documented, **so that** batch workflows are more efficient

## Technical Considerations

### Architecture Impact
- No new services or components — documentation and configuration changes only
- All changes are to existing .md files in .claude/agents/ and .claude/skills/

### Technology Decisions
- No new technologies required
- All changes within existing Markdown documentation

### Security & Compliance
- No security implications (documentation changes only)

### Performance Requirements
- No performance impact (documentation changes only)

## Dependencies

### Internal Dependencies
- [x] **EPIC-082:** Feature 2 references EPIC-082 reference loading decision (exists, in Planning)

### External Dependencies
- None

## Risks & Mitigation

### Risk 1: Feature scope creep during implementation
- **Probability:** Low
- **Impact:** Low
- **Mitigation:** Each feature is narrowly scoped to specific file edits
- **Contingency:** Defer expanded scope to new stories

## Progress Tracking

### Sprint Summary

| Sprint | Status | Points | Stories | Completed | In Progress | Blocked |
|--------|--------|--------|---------|-----------|-------------|---------|
| TBD | Not Started | 14 | 7 | 0 | 0 | 0 |
| **Total** | **0%** | **14** | **7** | **0** | **0** | **0** |

---

**Epic Template Version:** 1.0
**Last Updated:** 2026-02-22

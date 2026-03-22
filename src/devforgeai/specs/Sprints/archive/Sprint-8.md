---
id: SPRINT-8
name: AC Compliance Verification System Implementation
epic: EPIC-046
start_date: 2026-01-20
end_date: 2026-02-02
duration_days: 14
status: Active
total_points: 36
completed_points: 0
stories:
  - STORY-269
  - STORY-270
  - STORY-271
  - STORY-272
  - STORY-273
  - STORY-274
  - STORY-275
  - STORY-276
  - STORY-277
  - STORY-278
  - STORY-279
  - STORY-280
  - STORY-281
  - STORY-282
  - STORY-283
  - STORY-284
created: 2026-01-19 16:00:00
---

# Sprint 8: AC Compliance Verification System Implementation

## Overview

**Duration:** 2026-01-20 to 2026-02-02 (14 days)
**Capacity:** 36 story points
**Epic:** EPIC-046 - AC Compliance Verification System
**Status:** Active

This sprint implements the complete AC Compliance Verification System discovered in BRAINSTORM-005, eliminating the 100% QA miss rate on AC compliance issues by automating fresh-context, one-by-one AC verification against source code.

## Sprint Goals

### Primary Goals

1. **Verification Subagent Core** - Create `ac-compliance-verifier.md` subagent with fresh-context verification technique
2. **Phase Integration** - Add Phase 4.5 and 5.5 to devforgeai-development workflow with HALT behavior
3. **XML AC Format** - Implement machine-readable XML AC format for improved parsing accuracy
4. **AC-TechSpec Traceability** - Establish bidirectional traceability between acceptance criteria and technical components

### Success Metrics

- 0 AC compliance gaps escaping to production (from current 100% miss rate)
- Eliminate manual workaround (separate session AC review)
- 100% verification evidence per AC
- 100% source code inspection per AC

## Stories

### Feature 1: Verification Subagent Core (15 points)

#### STORY-269: AC Compliance Verifier Subagent Creation
- **Points:** 2
- **Priority:** High
- **Epic:** EPIC-046
- **Acceptance Criteria:** 5 criteria
- **Status:** Backlog → Ready for Dev
- **Description:** Create `.claude/agents/ac-compliance-verifier.md` with YAML frontmatter, system prompt, and tool restrictions

#### STORY-270: XML AC Parsing Logic
- **Points:** 3
- **Priority:** High
- **Epic:** EPIC-046
- **Acceptance Criteria:** 5 criteria
- **Status:** Backlog → Ready for Dev
- **Dependencies:** STORY-269
- **Description:** Parse XML-tagged acceptance criteria from story files (Given/When/Then extraction)

#### STORY-271: Source Code Inspection Workflow
- **Points:** 3
- **Priority:** High
- **Epic:** EPIC-046
- **Acceptance Criteria:** 5 criteria
- **Status:** Backlog → Ready for Dev
- **Dependencies:** STORY-270
- **Description:** Read and inspect actual source code files with evidence documentation (file:line:snippet)

#### STORY-272: Coverage Verification Check
- **Points:** 2
- **Priority:** High
- **Epic:** EPIC-046
- **Acceptance Criteria:** 4 criteria
- **Status:** Backlog → Ready for Dev
- **Dependencies:** STORY-271
- **Description:** Verify test coverage exists for each AC following test_ac{N}_* naming convention

#### STORY-273: Anti-Pattern Detection
- **Points:** 2
- **Priority:** High
- **Epic:** EPIC-046
- **Acceptance Criteria:** 4 criteria
- **Status:** Backlog → Ready for Dev
- **Dependencies:** STORY-271
- **Description:** Check for anti-pattern violations using devforgeai/specs/context/anti-patterns.md

#### STORY-274: JSON Report Generation
- **Points:** 3
- **Priority:** High
- **Epic:** EPIC-046
- **Acceptance Criteria:** 6 criteria
- **Status:** Backlog → Ready for Dev
- **Dependencies:** STORY-271, STORY-272, STORY-273
- **Description:** Generate JSON verification report at devforgeai/qa/verification/{STORY-ID}-ac-verification.json

### Feature 2: Phase Integration (8 points)

#### STORY-275: Phase 4.5 Insertion Point
- **Points:** 2
- **Priority:** High
- **Epic:** EPIC-046
- **Acceptance Criteria:** 4 criteria
- **Status:** Backlog → Ready for Dev
- **Dependencies:** STORY-274
- **Description:** Add Phase 4.5 between Phase 04 (Refactor) and Phase 05 (Integration)

#### STORY-276: Phase 5.5 Insertion Point
- **Points:** 2
- **Priority:** High
- **Epic:** EPIC-046
- **Acceptance Criteria:** 4 criteria
- **Status:** Backlog → Ready for Dev
- **Dependencies:** STORY-275
- **Description:** Add Phase 5.5 between Phase 05 (Integration) and Phase 06 (Deferral)

#### STORY-277: HALT Behavior on Failure
- **Points:** 2
- **Priority:** High
- **Epic:** EPIC-046
- **Acceptance Criteria:** 4 criteria
- **Status:** Backlog → Ready for Dev
- **Dependencies:** STORY-275, STORY-276
- **Description:** Workflow HALTs if any AC fails verification with detailed failure report

#### STORY-278: Phase Documentation Update
- **Points:** 2
- **Priority:** High
- **Epic:** EPIC-046
- **Acceptance Criteria:** 4 criteria
- **Status:** Backlog → Ready for Dev
- **Type:** documentation
- **Dependencies:** STORY-275, STORY-276, STORY-277
- **Description:** Update SKILL.md, create references/ac-verification-workflow.md, update coding-standards.md

### Feature 3: XML AC Format (8 points)

#### STORY-279: XML Schema Design
- **Points:** 2
- **Priority:** High
- **Epic:** EPIC-046
- **Acceptance Criteria:** 5 criteria
- **Status:** Backlog → Ready for Dev
- **Description:** Define XML schema with <acceptance_criteria>, <given>, <when>, <then>, <verification>

#### STORY-280: Story Template Update for XML AC
- **Points:** 3
- **Priority:** High
- **Epic:** EPIC-046
- **Acceptance Criteria:** 5 criteria
- **Status:** Backlog → Ready for Dev
- **Dependencies:** STORY-279
- **Description:** Update story-template.md to v2.6 with XML AC format and examples

#### STORY-281: XML Migration Guide
- **Points:** 3
- **Priority:** High
- **Epic:** EPIC-046
- **Acceptance Criteria:** 5 criteria
- **Status:** Backlog → Ready for Dev
- **Type:** documentation
- **Dependencies:** STORY-279, STORY-280
- **Description:** Create docs/guides/ac-xml-migration-guide.md with before/after examples

### Feature 4: AC-TechSpec Traceability (5 points)

#### STORY-282: Technical Specification Schema Update
- **Points:** 2
- **Priority:** High
- **Epic:** EPIC-046
- **Acceptance Criteria:** 4 criteria
- **Status:** Backlog → Ready for Dev
- **Description:** Add implements_ac field to Technical Specification YAML schema

#### STORY-283: Story Creation Automation
- **Points:** 2
- **Priority:** High
- **Epic:** EPIC-046
- **Acceptance Criteria:** 4 criteria
- **Status:** Backlog → Ready for Dev
- **Dependencies:** STORY-282
- **Description:** Auto-generate implements_ac during devforgeai-story-creation execution

#### STORY-284: Traceability Validation
- **Points:** 1
- **Priority:** High
- **Epic:** EPIC-046
- **Acceptance Criteria:** 4 criteria
- **Status:** Backlog → Ready for Dev
- **Dependencies:** STORY-282, STORY-283
- **Description:** Validate AC-COMP linkage, flag orphaned entities in Phase 7 self-validation

## Sprint Metrics

- **Planned Velocity:** 36 points
- **Current Velocity:** 0 points (0%)
- **Stories Planned:** 16
- **Stories Completed:** 0
- **Days Remaining:** 14
- **Burn-down Status:** On track (sprint just started)

## Capacity Analysis

**Capacity:** 36 points for 2-week sprint
- **Status:** Within recommended range (20-40 points) ✅
- **Features:** 4 features (2 P0 MUST HAVE + 2 P1 SHOULD HAVE)
- **Story Size Mix:**
  - 1-point stories: 1 (3%)
  - 2-point stories: 10 (28%)
  - 3-point stories: 5 (42%)
  - Total: Balanced mix ✅

**Risk Assessment:**
- **Dependency Chain:** Feature 1 has linear dependencies (STORY-269 → 270 → 271 → 272/273 → 274)
- **Parallel Tracks:** Features 1, 3, 4 can start in parallel (STORY-269 || STORY-279 || STORY-282)
- **Critical Path:** Feature 1 + Feature 2 (23 points on critical path)

## Daily Progress

### Day 1 (Monday, 2026-01-20)
- Stories in progress: 0
- Points completed: 0
- Notes: Sprint created, all stories transitioned to Ready for Dev

## Development Strategy

### Week 1 (Days 1-7): Foundation + Parallel Tracks

**Parallel Track A:** Feature 1 (Verification Subagent Core)
- Day 1-2: STORY-269 (Subagent file structure)
- Day 3-4: STORY-270 (XML parsing)
- Day 5-7: STORY-271 (Source inspection)

**Parallel Track B:** Feature 3 (XML AC Format)
- Day 1-2: STORY-279 (XML schema design)
- Day 3-5: STORY-280 (Template update)
- Day 6-7: STORY-281 (Migration guide)

**Parallel Track C:** Feature 4 (Traceability)
- Day 1-2: STORY-282 (Schema update)
- Day 3-4: STORY-283 (Auto-generation)
- Day 5: STORY-284 (Validation)

### Week 2 (Days 8-14): Completion + Integration

**Sequential Track:** Feature 1 Completion + Feature 2
- Day 8-9: STORY-272 (Coverage verification) + STORY-273 (Anti-pattern detection)
- Day 10: STORY-274 (JSON report generation)
- Day 11-12: STORY-275 (Phase 4.5) + STORY-276 (Phase 5.5)
- Day 13: STORY-277 (HALT behavior)
- Day 14: STORY-278 (Documentation update)

## Retrospective Notes

*To be filled at sprint end*

### What Went Well
- [To be documented]

### What Could Be Improved
- [To be documented]

### Velocity Analysis
- Planned: 36 points
- Completed: [To be calculated]
- Variance: [+/- points]

### Action Items for Next Sprint
- [To be documented]

## Next Steps

1. ✅ Review sprint goals and story priorities
2. ⏳ Start first stories in parallel:
   - `/dev STORY-269` (Feature 1 foundation)
   - `/dev STORY-279` (Feature 3 schema)
   - `/dev STORY-282` (Feature 4 schema)
3. ⏳ Track progress daily
4. ⏳ Complete sprint with: `/close-sprint`

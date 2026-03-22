---
id: SPRINT-11
name: Treelint Subagent Integration - Final Subagents & Validation
epic: EPIC-057
start_date: 2026-03-01
end_date: 2026-03-07
duration_days: 7
status: Planning
total_points: 10
completed_points: 0
stories:
  - STORY-368
  - STORY-369
created: 2026-02-05
---

# Sprint 11: Treelint Subagent Integration - Final Subagents & Validation

## Overview

**Duration:** 2026-03-01 to 2026-03-07 (7 days)
**Capacity:** 10 story points
**Epic:** EPIC-057 - Treelint Subagent Integration
**Status:** Planning

This sprint completes the Treelint subagent integration initiative by updating the final two subagents: coverage-analyzer and anti-pattern-scanner. This is the closing sprint for EPIC-057.

## Sprint Goals

### Primary Goals

1. **coverage-analyzer Integration** - Enable function-level coverage mapping using Treelint (STORY-368)
2. **anti-pattern-scanner Integration** - Enable AST-level anti-pattern detection using Treelint (STORY-369)
3. **Epic Completion** - Complete all 9 stories in EPIC-057

### Success Metrics

- All 7 target subagents updated with Treelint integration (EPIC-057 complete)
- Token reduction ≥40% measured in controlled workflow tests
- Zero workflow regressions (existing functionality preserved)
- All subagent files comply with progressive disclosure (500-line limit or reference files)

## Stories

### Final Subagent Updates (10 points)

#### STORY-368: Update coverage-analyzer with Treelint AST-Aware Function-Level Coverage Mapping
- **Points:** 5
- **Priority:** Medium
- **Epic:** EPIC-057
- **Dependencies:** STORY-361, STORY-362 (Sprint 9-10)
- **Status:** Backlog → Ready for Dev
- **Description:** Enable function-level coverage mapping, correlating coverage report uncovered line ranges with Treelint function boundaries, JSON parsing, Grep fallback

#### STORY-369: Update anti-pattern-scanner with Treelint AST-Aware Anti-Pattern Detection
- **Points:** 5
- **Priority:** Medium
- **Epic:** EPIC-057
- **Dependencies:** STORY-361, STORY-362 (Sprint 9-10)
- **Status:** Backlog → Ready for Dev
- **Description:** Enable true AST-level anti-pattern detection with god class detection (>20 methods) and long function detection (>50 lines) using class-to-function correlation, mandatory reference file extraction (701-line constraint), JSON parsing, Grep fallback

## Sprint Metrics

- **Planned Velocity:** 10 points
- **Current Velocity:** 0 points (0%)
- **Stories Planned:** 2
- **Stories Completed:** 0
- **Days Remaining:** 7
- **Burn-down Status:** Not started (sprint in Planning)

## Capacity Analysis

**Capacity:** 10 points for 1-week sprint
- **Status:** Light sprint, allows for validation and testing ✅
- **Story Size Mix:**
  - 5-point stories: 2 (100%)
  - Total: Uniform sizing ✅

**Risk Assessment:**
- **Pre-Requisite:** Sprint 9 (STORY-361) and Sprint 10 (STORY-362) must be complete
- **Parallel Tracks:** STORY-368 and STORY-369 are independent — can run fully in parallel
- **Critical Path:** Both stories can start Day 1 (all dependencies in prior sprints)
- **Buffer:** Light capacity allows for epic validation and end-to-end testing

## Development Strategy

### Days 1-5: Parallel Subagent Updates
- `/dev STORY-368` (coverage-analyzer Treelint integration)
- `/dev STORY-369` (anti-pattern-scanner Treelint integration) — fully parallel with STORY-368

### Days 6-7: Epic Validation & Retrospective
- Validate all 9 stories completed and QA approved
- Run end-to-end token reduction measurement
- Update EPIC-057 status to Complete
- Sprint retrospective

## Retrospective Notes

*To be filled at sprint end*

### What Went Well
- [To be documented]

### What Could Be Improved
- [To be documented]

### Velocity Analysis
- Planned: 10 points
- Completed: [To be calculated]
- Variance: [+/- points]

### Action Items for Next Sprint
- [To be documented]

## Next Steps

1. ✅ Review sprint goals and story priorities
2. ⏳ Verify Sprint 9 + Sprint 10 completion (STORY-361, STORY-362 must be done)
3. ⏳ Start parallel: `/dev STORY-368` and `/dev STORY-369`
4. ⏳ After completion, validate epic: EPIC-057 end-to-end
5. ⏳ Track progress daily
6. ⏳ Complete sprint with: `/close-sprint`

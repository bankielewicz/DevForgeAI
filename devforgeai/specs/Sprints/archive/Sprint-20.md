---
id: SPRINT-20
name: Sprint-20
epic: EPIC-085
start_date: 2026-03-27
end_date: 2026-04-10
duration_days: 14
status: Planned
total_points: 5
completed_points: 0
stories:
  - STORY-503
created: 2026-02-27
---

# Sprint 20: QA Diff Regression — Heuristics & Polish

## Overview

**Duration:** 2026-03-27 to 2026-04-10 (14 days)
**Capacity:** 5 story points
**Epic:** QA Diff Regression Detection and Test Integrity System (EPIC-085)
**Status:** Planned

## Sprint Goals

Add heuristic pattern detection for detailed test tampering diagnosis and perform end-to-end validation across the full `/dev` → `/qa` workflow.

1. Implement test tampering heuristic patterns for assertion weakening, test removal, noop substitution, and threshold lowering detection (STORY-503)

## Stories

### Ready for Dev (5 points)

#### STORY-503: Test Tampering Heuristic Patterns
- **Points:** 5
- **Priority:** Medium
- **Epic:** EPIC-085
- **Dependencies:** STORY-501 (Sprint 19), STORY-502 (Sprint 19)
- **Acceptance Criteria:** See story file
- **Status:** Ready for Dev

### In Progress (0 points)

_None_

### Completed (0 points)

_None_

## Dependency Graph

```
[Sprint 19: STORY-501] ──┐
                          ├──> STORY-503 (5 pts, heuristics)
[Sprint 19: STORY-502] ──┘
```

## Execution Order

**Sequential:** STORY-503 requires both STORY-501 (diff detection) and STORY-502 (checksums) to be complete.

1. Verify Sprint 19 stories are complete
2. Start STORY-503
3. End-to-end validation: full `/dev` → `/qa` workflow with heuristic analysis

## Sprint Metrics

- **Planned Velocity:** 5 points
- **Current Velocity:** 0 points (0%)
- **Stories Planned:** 1
- **Stories Completed:** 0
- **Days Remaining:** 14
- **Capacity Status:** Under optimal range (5 pts); acceptable for final heuristics + integration testing sprint

## Priority Distribution

| Priority | Count | Points |
|----------|-------|--------|
| Medium   | 1     | 5      |
| Total    | 1     | 5      |

## Key Deliverables

- `.claude/skills/devforgeai-qa/references/test-tampering-heuristics.md` (new reference)
- Grep pattern library for 4 detection categories
- Integration with diff-regression-detection.md
- End-to-end `/dev` → `/qa` workflow validation

## Daily Progress

_Will be updated during sprint execution._

## Retrospective Notes

_To be filled at sprint end._

## Next Steps

1. Ensure Sprint 19 (STORY-501, STORY-502) is complete before starting
2. Complete STORY-503 with full pattern library
3. Run end-to-end validation across the entire EPIC-085 feature set
4. EPIC-085 complete after Sprint 20 finishes

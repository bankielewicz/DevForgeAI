---
id: SPRINT-19
name: Sprint-19
epic: EPIC-085
start_date: 2026-03-13
end_date: 2026-03-27
duration_days: 14
status: Planned
total_points: 16
completed_points: 0
stories:
  - STORY-502
  - STORY-501
created: 2026-02-27
---

# Sprint 19: QA Diff Regression — Core Detection

## Overview

**Duration:** 2026-03-13 to 2026-03-27 (14 days)
**Capacity:** 16 story points
**Epic:** QA Diff Regression Detection and Test Integrity System (EPIC-085)
**Status:** Planned

## Sprint Goals

Implement the two main detection mechanisms: Red-phase test integrity checksums and git diff regression detection.

1. SHA-256 snapshot creation at Phase 02 and QA verification (STORY-502)
2. Git diff production code regression detection QA phase (STORY-501)

## Stories

### Ready for Dev (16 points)

#### STORY-502: Red-Phase Test Integrity Checksums
- **Points:** 8
- **Priority:** Medium
- **Epic:** EPIC-085
- **Dependencies:** STORY-506 (Sprint 18)
- **Acceptance Criteria:** See story file
- **Status:** Ready for Dev

#### STORY-501: Git Diff Regression Detection QA Phase
- **Points:** 8
- **Priority:** Medium
- **Epic:** EPIC-085
- **Dependencies:** STORY-506 (Sprint 18)
- **Acceptance Criteria:** See story file
- **Status:** Ready for Dev

### In Progress (0 points)

_None_

### Completed (0 points)

_None_

## Dependency Graph

```
[Sprint 18: STORY-506] ──┬──> STORY-502 (8 pts, checksums)
                          |
                          └──> STORY-501 (8 pts, diff detection)
```

## Execution Order

**Parallel start possible:** Both stories depend only on Sprint 18's STORY-506 (not on each other).

1. Start STORY-502 first (per EPIC-085: checksums must exist before QA can verify)
2. STORY-501 can start in parallel (diff detection is independent of checksums)
3. Both must complete before Sprint 20 (STORY-503 depends on both)

## Sprint Metrics

- **Planned Velocity:** 16 points
- **Current Velocity:** 0 points (0%)
- **Stories Planned:** 2
- **Stories Completed:** 0
- **Days Remaining:** 14
- **Capacity Status:** Within optimal range (16 pts)

## Priority Distribution

| Priority | Count | Points |
|----------|-------|--------|
| Medium   | 2     | 16     |
| Total    | 2     | 16     |

## Key Deliverables

- `.claude/skills/implementing-stories/references/test-integrity-snapshot.md` (new reference)
- `devforgeai/qa/snapshots/{STORY_ID}/red-phase-checksums.json` schema and creation logic
- `.claude/skills/devforgeai-qa/references/diff-regression-detection.md` (new reference)
- `devforgeai-qa` SKILL.md updated with new phase between Phase 1 and Phase 2

## Daily Progress

_Will be updated during sprint execution._

## Retrospective Notes

_To be filled at sprint end._

## Next Steps

1. Ensure Sprint 18 (STORY-506) is complete before starting
2. Start STORY-502 and STORY-501 in parallel
3. Sprint 20 begins with heuristic patterns (STORY-503)

---
id: SPRINT-17
name: Sprint-17
epic: EPIC-072
start_date: 2026-03-23
end_date: 2026-04-05
duration_days: 14
status: Planned
total_points: 6
completed_points: 0
stories:
  - STORY-470
  - STORY-471
created: 2026-02-21
---

# Sprint 17: Dashboard & Gamification

## Overview

**Duration:** 2026-03-23 to 2026-04-05 (14 days)
**Capacity:** 6 story points
**Epic:** Assessment & Coaching Core (EPIC-072)
**Status:** Planned

## Sprint Goals

Deliver terminal-compatible gamification (streaks, ASCII progress, celebrations) and the `/my-business` aggregated dashboard with `/coach-me` command — completing the full assessment → coaching → dashboard workflow.

1. Add streak tracking, ASCII progress display, and celebration patterns to coaching skill (STORY-470)
2. Create `/my-business` dashboard and `/coach-me` command with aggregated business view (STORY-471)

## Stories

### Ready for Dev (6 points)

#### STORY-470: Terminal-Compatible Gamification
- **Points:** 3
- **Priority:** Low
- **Epic:** EPIC-072
- **Dependencies:** STORY-467
- **Acceptance Criteria:** See story file
- **Status:** Ready for Dev

#### STORY-471: /my-business Aggregated Dashboard
- **Points:** 3
- **Priority:** Low
- **Epic:** EPIC-072
- **Dependencies:** STORY-470
- **Acceptance Criteria:** See story file
- **Status:** Ready for Dev

### In Progress (0 points)

_None_

### Completed (0 points)

_None_

## Dependency Graph

```
STORY-470 (3 pts, Low, depends on STORY-467)
    |
    +---> STORY-471 (3 pts, Low)
```

## Execution Order

**Sequential:** STORY-470 -> STORY-471

1. Start with STORY-470 (depends on STORY-467 from Sprint 16)
2. After STORY-470, start STORY-471

## Sprint Metrics

- **Planned Velocity:** 6 points
- **Current Velocity:** 0 points (0%)
- **Stories Planned:** 2
- **Stories Completed:** 0
- **Days Remaining:** 14
- **Capacity Status:** Under optimal range (6 pts); acceptable for final polish sprint

## Priority Distribution

| Priority | Count | Points |
|----------|-------|--------|
| Low      | 2     | 6      |
| Total    | 2     | 6      |

## Key Deliverables

- `src/claude/commands/coach-me.md`
- `src/claude/commands/my-business.md`
- ASCII progress visualization patterns
- Celebration event reference file

## Daily Progress

_Will be updated during sprint execution._

## Retrospective Notes

_To be filled at sprint end._

## Next Steps

1. Complete Sprint 16 (prerequisite: STORY-467)
2. Start STORY-470 when Sprint 16 coaching skill is done
3. After STORY-470, complete STORY-471 for full workflow

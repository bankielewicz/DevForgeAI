---
id: SPRINT-14
name: Sprint-14
epic: EPIC-071
start_date: 2026-02-20
end_date: 2026-03-20
duration_days: 28
status: Active
total_points: 77
completed_points: 0
stories:
  - STORY-457
  - STORY-458
  - STORY-459
  - STORY-460
  - STORY-461
  - STORY-462
  - STORY-463
created: 2026-02-20
---

# Sprint 14: Hybrid Command Lean Orchestration Refactoring

## Overview

**Duration:** 2026-02-20 to 2026-03-20 (28 days)
**Capacity:** 77 story points
**Epic:** Hybrid Command Lean Orchestration Refactoring (EPIC-071)
**Status:** Active

## Sprint Goals

Refactor all 20 hybrid command violations to comply with the lean orchestration pattern. Extract business logic from commands into skills and subagents. Achieve zero violations on `/audit-hybrid` and 40-60% token reduction per command invocation.

1. Establish Pattern A precedent with epic coverage pipeline refactoring (STORY-457)
2. Extend existing skills with sprint/triage workflow logic (STORY-458)
3. Protect the critical /dev workflow by extracting resume pre-flight logic (STORY-459)
4. Slim all skill-invoking commands (qa, create-ui, ideate) to lean pattern (STORY-460)
5. Trim documentation-heavy commands via progressive disclosure (STORY-461)
6. Handle special cases: new skill, file deletion, false positives (STORY-462)
7. Complete audit closure with borderline command trimming (STORY-463)

## Stories

### Ready for Dev (77 points)

#### STORY-457: Refactor Epic Coverage Pipeline Commands to Lean Orchestration Pattern
- **Points:** 16
- **Priority:** Critical
- **Epic:** EPIC-071
- **Dependencies:** None
- **Acceptance Criteria:** 7 criteria
- **Status:** Ready for Dev

#### STORY-458: Refactor Sprint and Triage Workflow Commands to Lean Orchestration Pattern
- **Points:** 16
- **Priority:** Critical
- **Epic:** EPIC-071
- **Dependencies:** STORY-457
- **Acceptance Criteria:** 7 criteria
- **Status:** Ready for Dev

#### STORY-459: Extract Resume Dev Pre-Flight Logic into Implementing-Stories Skill
- **Points:** 8
- **Priority:** Critical
- **Epic:** EPIC-071
- **Dependencies:** STORY-457, STORY-458
- **Acceptance Criteria:** 7 criteria
- **Status:** Ready for Dev

#### STORY-460: Slim Skill-Invoking Commands (qa, create-ui, ideate) to Lean Orchestration Pattern
- **Points:** 15
- **Priority:** Critical
- **Epic:** EPIC-071
- **Dependencies:** STORY-457, STORY-458, STORY-459
- **Acceptance Criteria:** 7 criteria
- **Status:** Ready for Dev

#### STORY-461: Trim Documentation-Heavy Commands (create-epic, document, create-agent, rca, insights)
- **Points:** 9
- **Priority:** High
- **Epic:** EPIC-071
- **Dependencies:** STORY-457
- **Acceptance Criteria:** 5 criteria
- **Status:** Ready for Dev

#### STORY-462: Handle Special Cases (audit-w3 skill, dev.backup DELETE, orchestrate/rca-stories trim)
- **Points:** 10
- **Priority:** High
- **Epic:** EPIC-071
- **Dependencies:** STORY-457, STORY-458
- **Acceptance Criteria:** 5 criteria
- **Status:** Ready for Dev

#### STORY-463: Trim Borderline Command (feedback-search) and Confirm False Positive (setup-github-actions)
- **Points:** 3
- **Priority:** High
- **Epic:** EPIC-071
- **Dependencies:** STORY-457
- **Acceptance Criteria:** 5 criteria
- **Status:** Ready for Dev

### In Progress (0 points)

_None_

### Completed (0 points)

_None_

## Dependency Graph

```
STORY-457 (16 pts, Critical, no deps)
    |
    +---> STORY-458 (16 pts, Critical)
    |         |
    |         +---> STORY-459 (8 pts, Critical)
    |         |         |
    |         |         +---> STORY-460 (15 pts, Critical)
    |         |
    |         +---> STORY-462 (10 pts, High)
    |
    +---> STORY-461 (9 pts, High)
    |
    +---> STORY-463 (3 pts, High)
```

## Execution Order

**Sequential Critical Path:** STORY-457 -> STORY-458 -> STORY-459 -> STORY-460

**Parallel after STORY-457:** STORY-461 (9 pts), STORY-463 (3 pts)

**Parallel after STORY-458:** STORY-462 (10 pts)

**Recommended execution plan:**
1. Start with STORY-457 (foundation, no dependencies)
2. After STORY-457 completes, start STORY-458 + STORY-461 + STORY-463 in parallel
3. After STORY-458 completes, start STORY-459 + STORY-462 in parallel
4. After STORY-459 completes, start STORY-460 (final critical path story)

## Sprint Metrics

- **Planned Velocity:** 77 points
- **Current Velocity:** 0 points (0%)
- **Stories Planned:** 7
- **Stories Completed:** 0
- **Days Remaining:** 28
- **Capacity Status:** Over (77 points exceeds 40-point optimal range for 2-week sprint; acceptable for 28-day sprint)

## Priority Distribution

| Priority | Count | Points |
|----------|-------|--------|
| Critical | 4     | 55     |
| High     | 3     | 22     |
| Total    | 7     | 77     |

## Daily Progress

_Will be updated during sprint execution._

## Retrospective Notes

_To be filled at sprint end._

## Next Steps

1. Review sprint stories and dependency graph
2. Start first story: `/dev STORY-457`
3. After STORY-457, parallelize: STORY-458, STORY-461, STORY-463
4. Track progress daily
5. Update story statuses as work progresses

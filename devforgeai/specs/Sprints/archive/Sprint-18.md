---
id: SPRINT-18
name: Sprint-18
epic: EPIC-085
start_date: 2026-02-27
end_date: 2026-03-13
duration_days: 14
status: Planned
total_points: 8
completed_points: 0
stories:
  - STORY-506
  - STORY-504
  - STORY-505
created: 2026-02-27
---

# Sprint 18: QA Diff Regression — Foundation

## Overview

**Duration:** 2026-02-27 to 2026-03-13 (14 days)
**Capacity:** 8 story points
**Epic:** QA Diff Regression Detection and Test Integrity System (EPIC-085)
**Status:** Planned

## Sprint Goals

Establish the foundational rules, ADR, and source-tree updates required before core detection features can be implemented.

1. Accept ADR-025 and update source-tree.md with snapshot directory (STORY-506)
2. Create test folder write protection rule (STORY-504)
3. Create operational safety rules (STORY-505)

## Stories

### Ready for Dev (8 points)

#### STORY-506: ADR-025 Acceptance and Source-Tree Update
- **Points:** 3
- **Priority:** Medium
- **Epic:** EPIC-085
- **Dependencies:** None
- **Acceptance Criteria:** See story file
- **Status:** Ready for Dev

#### STORY-504: Test Folder Write Protection Rule
- **Points:** 3
- **Priority:** Medium
- **Epic:** EPIC-085
- **Dependencies:** STORY-506
- **Acceptance Criteria:** See story file
- **Status:** Ready for Dev

#### STORY-505: Operational Safety Rules
- **Points:** 2
- **Priority:** Medium
- **Epic:** EPIC-085
- **Dependencies:** None
- **Acceptance Criteria:** See story file
- **Status:** Ready for Dev

### In Progress (0 points)

_None_

### Completed (0 points)

_None_

## Dependency Graph

```
STORY-506 (3 pts, no deps) ──┐
    |                         |
    +──> STORY-504 (3 pts)    |
                              |
STORY-505 (2 pts, no deps) ──┘
```

## Execution Order

**Parallel start possible:** STORY-506 and STORY-505 can start in parallel (no shared dependencies).

1. Start with STORY-506 (foundation — ADR + source-tree)
2. STORY-505 can start immediately in parallel
3. After STORY-506 completes, start STORY-504 (depends on STORY-506)

## Sprint Metrics

- **Planned Velocity:** 8 points
- **Current Velocity:** 0 points (0%)
- **Stories Planned:** 3
- **Stories Completed:** 0
- **Days Remaining:** 14
- **Capacity Status:** Under optimal range (8 pts); acceptable for foundation/rules sprint

## Priority Distribution

| Priority | Count | Points |
|----------|-------|--------|
| Medium   | 3     | 8      |
| Total    | 3     | 8      |

## Key Deliverables

- ADR-025 status: Proposed → Accepted
- `devforgeai/specs/context/source-tree.md` updated with `devforgeai/qa/snapshots/` directory
- `.claude/rules/workflow/test-folder-protection.md` (new rule file)
- `.claude/rules/workflow/operational-safety.md` (new rule file)

## Daily Progress

_Will be updated during sprint execution._

## Retrospective Notes

_To be filled at sprint end._

## Next Steps

1. Start STORY-506 and STORY-505 in parallel
2. After STORY-506, complete STORY-504
3. Sprint 19 begins with core detection features (STORY-502, STORY-501)

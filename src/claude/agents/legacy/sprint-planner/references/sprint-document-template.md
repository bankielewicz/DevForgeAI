# Sprint Planner - Sprint Document Template

The template to use when generating the sprint markdown file in Phase 4:

```markdown
---
id: SPRINT-{N}
name: {sprint_name}
epic: {epic_id or "Multiple" or "Standalone"}
start_date: {YYYY-MM-DD}
end_date: {YYYY-MM-DD}
duration_days: {duration_days}
status: Active
total_points: {total_points}
completed_points: 0
stories:
  - {STORY-001}
  - {STORY-002}
  [... all selected stories ...]
created: {YYYY-MM-DD HH:MM:SS}
---

# Sprint {N}: {sprint_name}

## Overview

**Duration:** {start_date} to {end_date} ({duration_days} days)
**Capacity:** {total_points} story points
**Epic:** [Epic name from context] (Link: EPIC-ID)
**Status:** Active

## Sprint Goals

[Generate high-level objectives from story themes]

Example: "Complete user authentication and account creation features to enable MVP user onboarding"

## Stories

### In Progress (0 points)
[Empty - will be populated during sprint]

### Ready for Dev ({total_points} points)

[For each selected story, in priority order:]

#### {STORY-ID}: {Story Title}
- **Points:** {points}
- **Priority:** {priority}
- **Epic:** {epic_id}
- **Acceptance Criteria:** {count} criteria
- **Status:** Ready for Dev

[Repeat for all stories]

### Completed (0 points)
[Empty - will be populated as stories complete]

## Sprint Metrics

- **Planned Velocity:** {total_points} points
- **Current Velocity:** 0 points (0%)
- **Stories Planned:** {total_stories}
- **Stories Completed:** 0
- **Days Remaining:** {duration_days}
- **Capacity Status:** {capacity_status with guidance if under/over}

## Daily Progress

[Will be updated during sprint execution]

## Retrospective Notes

[To be filled at sprint end]

## Next Steps

1. Review sprint stories and prioritize execution
2. Start first story: `/dev STORY-[ID]`
3. Track progress daily
4. Update story statuses as work progresses
```

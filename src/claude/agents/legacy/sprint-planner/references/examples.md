# Sprint Planner - Examples

### Example 1: Single Epic Sprint with HIGH Priority Focus

**Context:** Planning a focused sprint for user authentication feature.

```
Task(
  subagent_type="sprint-planner",
  description="Create Sprint-1 with user authentication stories",
  prompt="Create sprint with:
    - Sprint name: User Authentication and Onboarding
    - Selected stories: STORY-001, STORY-002, STORY-003
    - Duration: 14 days
    - Epic: EPIC-001
    - Start date: 2025-11-10

    Execute complete sprint planning workflow and return structured JSON summary."
)
```

**Expected behavior:**
- Agent discovers next sprint number (Sprint-1) from existing sprints
- Agent validates all 3 stories exist and have "Backlog" status
- Agent calculates capacity (34 points = optimal)
- Agent creates Sprint-1.md with proper YAML frontmatter and formatted sections
- Agent updates all 3 stories to "Ready for Dev" with workflow history entries
- Agent returns JSON with capacity analysis, story list, and next steps

### Example 2: Multi-Epic Sprint with Balanced Story Mix

**Context:** Planning a cross-feature sprint with mixed priority stories.

```
Task(
  subagent_type="sprint-planner",
  description="Create Sprint-3 with cross-functional stories",
  prompt="Create sprint with:
    - Sprint name: Cross-Functional Feature Sprint
    - Selected stories: STORY-045, STORY-046, STORY-047, STORY-048
    - Duration: 14 days
    - Epic: Multiple (EPIC-005, EPIC-006)
    - Start date: 2025-12-08

    Execute complete sprint planning workflow and return structured JSON."
)
```

**Expected behavior:**
- Agent handles multiple epics (Type = "multiple" in response)
- Agent validates capacity with 4 stories (likely 28-36 points = optimal)
- Agent verifies story independence across epics
- Agent creates Sprint-3.md with multi-epic format
- Agent updates all 4 stories with sprint reference and workflow history
- Agent warns if any story has dependencies needing resolution
- Agent returns JSON with multi-epic capacity analysis

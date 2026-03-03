---
name: sprint-command-workflow
description: Extracted sprint planning business logic from create-sprint.md command
---

# Sprint Command Workflow Reference

Business logic for the /create-sprint command, extracted per lean orchestration pattern (STORY-458).

---

## Epic Discovery

When the skill receives sprint context markers, execute epic discovery:

1. Scan for epic files: `Glob(pattern="devforgeai/specs/Epics/*.epic.md")`
2. Read each epic's YAML frontmatter (id, title, status)
3. If no epics found: Set EPIC_ID = "Standalone" mode
4. Return list of available epics for command's user interaction prompt

**Fallback:** If Glob returns no results, proceed in Standalone mode (no epic linkage).

---

## Story Filtering

Filter stories by Backlog status with point extraction:

1. Scan story files: `Glob(pattern="devforgeai/specs/Stories/*.story.md")`
2. For each story file, read YAML frontmatter
3. Filter where `status == "Backlog"`
4. Extract: id, title, points, priority, epic
5. Group stories by epic and sort by priority (Critical > High > Medium > Low)
6. Return structured list for command's story selection prompt

**Empty Backlog handling:**
If no Backlog stories found, return error with resolution:
- Message: "No Stories Available for Sprint"
- Actions: "1. Create stories: /create-story [description]  2. Or move stories back to Backlog status"

---

## Capacity Calculation

Validate sprint capacity with 20-40 point recommended range:

1. Sum points from selected stories: `total_points = SUM(selected_stories.points)`
2. Evaluate capacity:
   - If total_points > 40: Over-capacity (return warning for command)
   - If total_points < 20: Under-capacity (return warning for command)
   - If 20 <= total_points <= 40: Optimal range
3. Capacity status values: "optimal", "over-capacity", "under-capacity"

**Note:** The override/adjustment decision is handled by the command via user prompts. This workflow only calculates and reports.

---

## Sprint Number Auto-Increment

Determine next sprint number:

1. Scan existing sprints: `Glob(pattern="devforgeai/specs/Sprints/Sprint-*.md")`
2. Extract sprint numbers from filenames
3. Calculate: `next_number = max(existing_numbers) + 1`
4. If no sprints exist: `next_number = 1`
5. Sprint filename: `Sprint-{next_number}.md`

---

## Sprint File YAML Generation

Generate sprint file with all required frontmatter fields:

```yaml
---
id: Sprint-{number}
name: "{sprint_name}"
start_date: "{start_date}"
end_date: "{end_date}"
duration_days: {duration}
epic: "{epic_id}"
status: Active
capacity:
  total_points: {total_points}
  story_count: {count}
stories:
  - id: STORY-XXX
    title: "{title}"
    points: {points}
    priority: "{priority}"
created: "{timestamp}"
---

# Sprint-{number}: {sprint_name}

## Sprint Goal

{epic_name} - {story_count} stories ({total_points} points)

## Stories

| ID | Title | Points | Priority | Status |
|----|-------|--------|----------|--------|
| STORY-XXX | {title} | {points} | {priority} | Ready for Dev |

## Timeline

- **Start:** {start_date}
- **End:** {end_date}
- **Duration:** {duration} days
```

Write to: `devforgeai/specs/Sprints/Sprint-{number}.md`

---

## Story Status Updates

Update each selected story from Backlog to Ready for Dev:

1. For each selected story file:
   a. Update YAML frontmatter: `status: Backlog` to `status: Ready for Dev`
   b. Add sprint reference: `sprint: Sprint-{number}`
   c. Add workflow history entry:
      ```
      | {date} | create-sprint | Status Update | Backlog -> Ready for Dev | Sprint-{number} |
      ```

---

## Feedback Hook Integration

Non-blocking feedback collection after sprint creation:

```
# Check hooks enabled
Execute: devforgeai-validate check-hooks --operation=create-sprint --status=success

# Conditional invocation (non-blocking)
IF check-hooks exit == 0:
    Execute: devforgeai-validate invoke-hooks --operation=create-sprint --sprint-name="${SPRINT_NAME}" --story-count=${STORY_COUNT} --capacity=${CAPACITY_POINTS}

    IF invoke-hooks fails:
        Log to: devforgeai/feedback/logs/hook-errors.log
        Display: "Feedback collection failed (sprint creation succeeded)"
```

**Features:**
- Non-blocking (sprint always succeeds)
- Shell-escaped: `"${SPRINT_NAME}"` prevents injection
- Empty sprint: `--story-count=0 --capacity=0` allowed
- **NFR-001:** check-hooks <100ms | **NFR-002:** invoke-hooks <3s | **NFR-003:** Total <3.5s

---

## Error Handling

### Error: No Arguments Provided
Display: "Usage: /create-sprint [sprint-name]" then HALT

### Error: No Epics Found
Display: "No epics found. Creating standalone sprint." then Continue with Standalone mode

### Error: No Backlog Stories
Display: "No stories in Backlog\n\nAction: Create stories first with /create-story" then HALT

### Error: Story Selection Cancelled
Display: "Sprint creation cancelled." then HALT

### Error: Skill Execution Failed
Display: "Sprint Creation Failed\n\nCause: ${error.message}\n\n${error.details}\n\nRecovery: ${error.recovery_steps}" then HALT

---

## Architecture

**Command (<=100 lines - Lean Orchestration):**
- Phase 0: User interaction (epic, stories, metadata via interactive prompts)
- Phase 1: Skill invocation with context markers
- Phase 2: Result display

**Skill (devforgeai-orchestration - Phase 3):**
- Step 1: Extract sprint parameters from conversation
- Step 2: Invoke sprint-planner subagent
- Step 3: Process subagent result
- Step 4: Return formatted summary

**Subagent (sprint-planner):**
- Phase 1: Sprint discovery (next number)
- Phase 2: Story validation (Backlog status)
- Phase 3: Metrics calculation (capacity, dates)
- Phase 4: Document generation (YAML + markdown)
- Phase 5: Story updates (status, references, history)
- Phase 6: Summary report

**Token Efficiency:**
- Before: ~12K tokens in main conversation
- After: ~5K tokens in main conversation
- Savings: 58% reduction

---

## Notes

**Design Philosophy:**
- Commands orchestrate user interaction and delegate to skills
- Skills coordinate workflow phases and invoke subagents
- Subagents execute specialized tasks in isolated contexts
- Reference files provide framework guardrails

**Framework Integration:**
- Respects 11-state workflow (Backlog to Ready for Dev transition)
- Enforces capacity planning (20-40 points for 2-week sprints)
- Maintains workflow history (timestamp, status, actions)
- Links epic hierarchy (epic to sprint to stories)

**When to Use:**
- Starting new 2-week sprint
- Selecting stories for coordinated development
- Planning feature batch for release
- Setting team velocity and capacity goals

**When NOT to Use:**
- For single-story work (use `/dev STORY-ID` directly)
- Mid-sprint (wait for current sprint to complete)
- Without backlog stories (create stories first with `/create-story`)

**Best Practices:**
- Link sprints to epics for traceability
- Balance story points (20-40 ideal for 2-week sprint)
- Prioritize HIGH stories first
- Review sprint goals before starting
- Update sprint progress regularly

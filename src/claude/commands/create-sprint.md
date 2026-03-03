---
description: Create sprint plan with story selection
argument-hint: [sprint-name]
model: opus
allowed-tools: Read, Glob, AskUserQuestion, Skill
---

# /create-sprint - Sprint Planning Command

Create a new sprint with interactive story selection, capacity validation, and automatic story status updates.

## Quick Reference

```bash
/create-sprint "User Authentication Sprint"
/create-sprint
```

**Workflow:** 1) Epic linkage 2) Story selection 3) Sprint metadata 4) Capacity validation (20-40 pts) 5) Create sprint + update statuses

## Command Workflow

### Phase 0: Argument Validation and User Interaction

**Parse sprint name:**
```
SPRINT_NAME = $ARGUMENTS
IF SPRINT_NAME is empty:
    AskUserQuestion: Question: "What is the sprint name or theme?" | Header: "Sprint Name" | Options: ["Sprint [auto-number]", "Custom name"]
```

**Epic discovery:** Glob(pattern="devforgeai/specs/Epics/*.epic.md") → Read frontmatter
AskUserQuestion: "Link this sprint to an epic?" | Header: "Epic" | Options: [each epic, "Multiple epics", "No epic (standalone)"]

**Story selection:** Glob(pattern="devforgeai/specs/Stories/*.story.md") → Filter status=="Backlog"
AskUserQuestion: "Select stories for sprint:" | Header: "Story Selection" | multiSelect: true | Options: [stories by id/title/points/priority]

**Capacity validation (20-40 point range):**
IF selected_points > 40: AskUserQuestion: "Over capacity (${selected_points} pts). Proceed?" | Options: ["Proceed anyway", "Remove lowest priority", "Adjust selection"]
IF selected_points < 20: AskUserQuestion: "Under capacity (${selected_points} pts). Add more?" | Options: ["Proceed anyway", "Add more stories", "Adjust selection"]

**Sprint metadata:**
AskUserQuestion: "Sprint start date?" | Options: ["Today", "Tomorrow", "Next Monday", "Custom"]
AskUserQuestion: "Sprint duration?" | Options: ["2 weeks (standard)", "1 week (short)", "3 weeks (extended)", "Custom"]

**Confirm:** AskUserQuestion: "Create sprint with these parameters?" | Options: ["Yes - create sprint", "No - adjust"]

### Phase 1: Invoke Orchestration Skill

```
**Operation:** plan-sprint
**Sprint Name:** ${SPRINT_NAME}
**Selected Stories:** ${SELECTED_STORY_IDS}
**Duration:** ${DURATION_DAYS} days
**Start Date:** ${START_DATE}
**Epic:** ${EPIC_ID}
```

Skill(command="devforgeai-orchestration")

### Phase 2: Display Results

Display skill result (pre-formatted by skill).

## Lean Orchestration Enforcement

**DO NOT** add business logic to this command:
- ❌ Iteration loops over story files
- ❌ Subagent invocations
- ❌ File write or edit operations
- ❌ Capacity arithmetic or point summation
- ❌ Sprint file generation

All business logic lives in: `.claude/skills/devforgeai-orchestration/references/sprint-command-workflow.md`

## Error Handling

| Error | Display | Action |
|-------|---------|--------|
| No args + user cancels | "Usage: /create-sprint [sprint-name]" | HALT |
| No epics found | "No epics found. Standalone sprint." | Continue |
| No Backlog stories | "No stories in Backlog. Create with /create-story" | HALT |
| Selection cancelled | "Sprint creation cancelled." | HALT |
| Skill failed | "Sprint Creation Failed: ${error}" | HALT |

## Success Criteria

Sprint file created in devforgeai/specs/Sprints/ | Stories updated to "Ready for Dev" | Capacity validated

## Integration

**Prerequisites:** Stories with status=Backlog | **Invokes:** devforgeai-orchestration skill | **Creates:** Sprint file | **Updates:** Story statuses | **Enables:** /dev STORY-ID | **Related:** /create-epic, /create-story, /dev, /orchestrate

## Performance

**Token:** ~5K (command) | **Character:** ≤12K | **Execution:** 3-6 min

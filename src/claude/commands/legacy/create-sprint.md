---
description: Create sprint plan with story selection
argument-hint: [sprint-name] [--epic=EPIC-NNN]
model: opus
allowed-tools: Bash, AskUserQuestion, Skill
---

# /create-sprint - Sprint Planning Command

Create a new sprint with interactive story selection, capacity validation, and automatic story status updates.

## Lean Orchestration Enforcement

**DO NOT (before skill invocation):**
- ❌ DO NOT use Glob to search for sprints, stories, or epics (use CLI instead)
- ❌ DO NOT add business logic (capacity math, file writes, status updates)
- ❌ DO NOT iterate over story files
- ❌ DO NOT invoke subagents directly

**DO (command responsibilities only):**
- ✅ MUST validate via CLI: `devforgeai-validate sprint-preflight`
- ✅ MUST collect user choices (epic, stories, dates) via AskUserQuestion
- ✅ MUST set context markers and invoke skill

## Phase 0: Argument Validation

```
# Single CLI call — replaces all Glob for sprint/story/epic discovery
epic_arg = extract --epic=EPIC-NNN from arguments (or null)
result = Bash(command="devforgeai-validate sprint-preflight ${epic_flag} --project-root=. --format=json 2>&1")

Parse JSON result:
  IF exit 0:
    NEXT_SPRINT = result.next_sprint_id       # "Sprint-38"
    BACKLOG_STORIES = result.backlog_stories   # [{story_id, title, points, priority, depends_on, file}]
    TOTAL_POINTS = result.total_points
    EPIC_ID = result.epic_id                   # null if no --epic
    EPIC_FILE = result.epic_file
  IF exit 1: Display "Epic not found" → HALT
  IF exit 2: Display "Invalid args" → HALT
```

**Sprint name:**
```
AskUserQuestion: "Sprint name?" | Options: ["${NEXT_SPRINT} (auto)", "Custom name"]
```

**Epic linkage (if not already from --epic flag):**
```
IF EPIC_ID is null:
  AskUserQuestion: "Link to epic?" | Options: [epic list from Bash ls, "No epic"]
  IF epic selected: re-run sprint-preflight with --epic to get filtered stories
```

**Story selection:**
```
AskUserQuestion: "Select stories for ${NEXT_SPRINT}:" | multiSelect: true
  Options built from BACKLOG_STORIES (id, title, points, priority, deps)
```

**Capacity validation:**
```
selected_points = sum of selected story points
IF > 40: AskUserQuestion "Over capacity. Proceed?"
IF < 20: AskUserQuestion "Under capacity. Proceed?"
```

**Metadata:**
```
AskUserQuestion: "Start date?" | Options: ["Today", "Tomorrow", "Next Monday", "Custom"]
AskUserQuestion: "Duration?" | Options: ["2 weeks", "1 week", "3 weeks", "Custom"]
```

**Confirm:**
```
AskUserQuestion: "Create sprint?" | Display: sprint_id, stories, points, dates
```

## Phase 1: Invoke Orchestration Skill

```
**Operation:** plan-sprint
**Sprint ID:** ${NEXT_SPRINT}
**Sprint Name:** ${SPRINT_NAME}
**Selected Stories:** ${SELECTED_STORY_IDS}
**Duration:** ${DURATION_DAYS} days
**Start Date:** ${START_DATE}
**Epic:** ${EPIC_ID}
**Total Points:** ${TOTAL_POINTS}
```

Skill(command="spec-driven-lifecycle")

## Phase 2: Display Results

Display skill result (pre-formatted by skill).

## Error Handling

| Error | Action |
|-------|--------|
| No args + user cancels | HALT |
| No Backlog stories | "No stories in Backlog. Run /create-story first." → HALT |
| Skill failed | "Sprint Creation Failed: ${error}" → HALT |

## References

- Skill: `.claude/skills/spec-driven-lifecycle/SKILL.md`
- CLI: `devforgeai-validate sprint-preflight --epic=EPIC-NNN --format=json`

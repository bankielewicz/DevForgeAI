---
description: Triage AI-generated framework improvement recommendations into stories
argument-hint: [--priority=HIGH|MEDIUM|LOW] [--limit=N]
model: opus
allowed-tools: Read, Glob, Skill, AskUserQuestion
---

# /recommendations-triage - Convert Recommendations to Stories

Process AI-generated framework improvement recommendations and convert to user stories.

## Quick Reference

```bash
/recommendations-triage
/recommendations-triage --priority=HIGH
/recommendations-triage --limit=5
/recommendations-triage --priority=HIGH --limit=10
```

## Command Workflow

### Phase 0: Argument Parsing and User Interaction

Parse: PRIORITY_FILTER from --priority= (HIGH|MEDIUM|LOW), LIMIT from --limit= (default: 20)

Read queue and display recommendations, then collect user selection:

AskUserQuestion: "Which recommendations to convert to stories?" | Header: "Select items" | multiSelect: true | Options: [recommendations by title/priority/effort]

AskUserQuestion: "Or select bulk action:" | Header: "Bulk action" | Options: ["All HIGH priority", "Skip - just viewing"]

If "Skip" selected: Display "No stories created." and exit.

### Phase 1: Invoke Feedback Skill

**Feedback Mode:** triage | **Priority Filter:** ${PRIORITY_FILTER} | **Limit:** ${LIMIT} | **Selected Items:** ${SELECTED_IDS}

Skill(command="spec-driven-feedback")

### Phase 2: Display Results

Display skill result (pre-formatted by skill).

## Lean Orchestration Enforcement

**DO NOT** add business logic to this command:
- ❌ Iteration loops over recommendations
- ❌ Subagent invocations
- ❌ File write or edit operations
- ❌ Queue JSON manipulation

All business logic lives in: `src/claude/skills/spec-driven-feedback/phases/phase-03-feedback-execution.md` (triage sub-workflow)
Reference: `.claude/skills/devforgeai-feedback/references/triage-workflow.md`

## Error Handling

| Error | Display | Action |
|-------|---------|--------|
| Queue File Not Found | "Queue not found. Run /dev to generate." | HALT |
| Story Creation Failed | "Failed to create story. Stays in queue." | Continue |
| Queue Write Failed | "Queue not updated. Manual fix needed." | Warn |

## Integration

**Workflow:** /dev Phase 09 → recommendations-triage → /create-story → /dev
**Related:** /DF:feedback, /feedback-search, /dev, /create-story

**Performance:** ~5K tokens (command) + ~90K/story (skill) | <500ms display
**References:** framework-analyst.md, phase-09-feedback.md, recommendations-queue.json, schema.json

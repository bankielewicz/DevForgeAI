---
id: STORY-173
title: "Add Plan File Creation Constraints to Subagents"
type: refactor
priority: HIGH
points: 1
status: Backlog
epic: EPIC-033
sprint: N/A
created: 2025-12-31
source: STORY-156 framework enhancement analysis
tags: [subagent, constraint, plan-mode, workflow-interruption]
---

# STORY-173: Add Plan File Creation Constraints to Subagents

## User Story

**As a** DevForgeAI framework user,
**I want** backend-architect and api-designer subagents to return plan content inline rather than creating plan files,
**So that** workflow execution is not interrupted by plan mode triggers mid-process.

## Background

Currently, `backend-architect.md` and `api-designer.md` subagents have `permissionMode: plan` which allows them to trigger plan mode during workflow execution by creating files in `.claude/plans/`. This causes workflow interruptions.

## Acceptance Criteria

### AC-1: Backend Architect Plan File Constraint
**Given** the `backend-architect.md` subagent file
**When** I review its Constraints section
**Then** it MUST contain: "Do NOT create files in .claude/plans/ directory"

### AC-2: API Designer Plan File Constraint
**Given** the `api-designer.md` subagent file
**When** I review its Constraints section
**Then** it MUST contain: "Do NOT create files in .claude/plans/ directory"

### AC-3: Inline Plan Content Instruction
**Given** both subagent files
**When** I review their output guidance
**Then** they MUST instruct to return plan content directly in the response

### AC-4: Existing Functionality Preserved
**Given** both subagent files after modification
**When** the agents are invoked during development workflow
**Then** they MUST still produce architectural plans (content unchanged, only delivery method constrained)

## Technical Specification

### Files to Modify
- `.claude/agents/backend-architect.md`
- `.claude/agents/api-designer.md`

### Constraint Text Template
```markdown
## Constraints

### Plan File Restrictions
- **Do NOT create files in `.claude/plans/` directory** - This triggers plan mode
- Return all plan content directly in your response
- Plans should be formatted inline using markdown
```

## Definition of Done

- [ ] Backend-architect.md updated with plan file creation constraint
- [ ] API-designer.md updated with plan file creation constraint
- [ ] Both files instruct to return plan content in response
- [ ] Markdown formatting consistent with existing document style

## Effort Estimate
- **Points:** 1
- **Estimated Hours:** 30 minutes
- **Complexity:** Low (documentation only)

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-12-31 | claude/opus | Story created from STORY-156 framework enhancement analysis |

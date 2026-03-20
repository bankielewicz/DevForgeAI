# Parameter Extraction Algorithm

## Purpose
Extract parameters from conversation context for lifecycle skill operation.

## Story Management Mode Parameters
- `$STORY_ID`: Extract from "**Story ID:** STORY-NNN" pattern in conversation
- `$AUTO_RESUME`: Extract from "**Auto-Resume:** Enabled" (default: false)

## Sprint Planning Mode Parameters
- `$SPRINT_NAME`: Extract from "**Sprint Name:** {name}" pattern
- `$SELECTED_STORIES`: Extract from "**Selected Stories:** {ids}" pattern (comma-separated)
- `$DURATION`: Extract from "**Duration:** {days} days" pattern
- `$START_DATE`: Extract from "**Start Date:** {date}" pattern
- `$EPIC_ID`: Extract from "**Epic:** {id}" pattern (optional)

## Audit Deferrals Mode Parameters
- `$AUDIT_MODE`: Extract from "**Mode:** full-audit" (default: "full-audit")

## Extraction Algorithm
1. Search conversation for context markers using Grep patterns
2. First match wins (patterns are unique per marker)
3. Missing required parameters trigger HALT with AskUserQuestion
4. Optional parameters use documented defaults

## Pattern Priority
Sprint markers checked first > Audit markers second > Story markers third > Default
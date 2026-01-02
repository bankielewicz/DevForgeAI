---
id: STORY-174
title: Add Execution-Mode Frontmatter to Execution Commands
type: feature
epic: EPIC-033
priority: HIGH
points: 2
status: Backlog
created: 2025-12-31
source: STORY-156 QA framework enhancement analysis
---

# STORY-174: Add Execution-Mode Frontmatter to Execution Commands

## User Story

**As a** DevForgeAI user,
**I want** execution commands (/qa, /dev, /release) to automatically exit plan mode when invoked,
**So that** I do not need manual intervention when plan mode is active.

## Acceptance Criteria

### AC#1: qa.md Command Has execution-mode Frontmatter
**Given** the qa.md command file
**Then** it contains `execution-mode: immediate` in YAML frontmatter

### AC#2: dev.md Command Has execution-mode Frontmatter
**Given** the dev.md command file
**Then** it contains `execution-mode: immediate` in YAML frontmatter

### AC#3: release.md Command Has execution-mode Frontmatter
**Given** the release.md command file
**Then** it contains `execution-mode: immediate` in YAML frontmatter

### AC#4: Phase 0 Auto-Exits Plan Mode
**Given** execution command invoked with `execution-mode: immediate`
**And** plan mode is currently active
**When** Phase 0 executes
**Then** command auto-exits plan mode using ExitPlanMode tool

### AC#5: User Notification Displayed
**Given** an execution command auto-exits plan mode
**Then** notification displayed: "Note: /{command} is an execution command. Exiting plan mode automatically."

## Technical Specification

### Files to Modify
- `.claude/commands/qa.md`
- `.claude/commands/dev.md`
- `.claude/commands/release.md`

### Implementation
1. Add YAML frontmatter field: `execution-mode: immediate`
2. Add Phase 0 detection logic per command
3. Uses ExitPlanMode tool if plan mode active

## Definition of Done

- [ ] Add `execution-mode: immediate` frontmatter to qa.md
- [ ] Add `execution-mode: immediate` frontmatter to dev.md
- [ ] Add `execution-mode: immediate` frontmatter to release.md
- [ ] Implement Phase 0 plan mode detection in each command
- [ ] Add user notification display logic
- [ ] All 5 acceptance criteria have passing tests

## Effort Estimate
- **Points:** 2
- **Estimated Hours:** 2 hours

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-12-31 | claude/opus | Story created from STORY-156 QA framework enhancement |

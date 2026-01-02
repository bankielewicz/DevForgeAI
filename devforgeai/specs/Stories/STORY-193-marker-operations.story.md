---
id: STORY-193
title: Consolidate Phase Marker Operations Reference File
type: documentation
epic: EPIC-033
priority: LOW
points: 1
status: Backlog
created: 2025-12-31
source: STORY-153 framework enhancement analysis
---

# STORY-193: Consolidate Phase Marker Operations Reference File

## User Story

**As a** DevForgeAI developer,
**I want** marker operations consolidated in one reference,
**So that** marker patterns are consistent.

## Background

Marker operations scattered across skill files with inconsistent patterns.

## Acceptance Criteria

### AC-1: Reference File Created
**Then** marker-operations.md created in devforgeai-qa/references/

### AC-2: Write Pattern Documented
**Then** Write New Marker pattern documented (uses Bash for new files)

### AC-3: Verify Pattern Documented
**Then** Verify Marker Exists pattern documented (uses Glob)

### AC-4: Cleanup Pattern Documented
**Then** Cleanup Markers pattern documented (uses Bash rm)

### AC-5: Write Tool Workaround Documented
**Then** "New files require prior Read" workaround documented

### AC-6: Referenced from SKILL.md
**Then** cross-reference added to main SKILL.md

## Technical Specification

### Files to Create/Modify
- `.claude/skills/devforgeai-qa/references/marker-operations.md` (new)
- `.claude/skills/devforgeai-qa/SKILL.md` (add reference)

### Content
```markdown
# Phase Marker Operations

## Write New Marker
Use native Write tool for new marker files (per tech-stack.md lines 206-207):
Write(file_path="{marker_path}", content="phase: {N}\nstory: {STORY_ID}\ntimestamp: {ISO_TIMESTAMP}")

**Note:** Native tools are required per tech-stack.md - Bash echo/redirect should NOT be used for file operations.

## Verify Marker Exists
Glob(pattern="devforgeai/qa/reports/{STORY_ID}/.qa-phase-{N}.marker")

## Cleanup Markers (QA PASSED only)
# Note: rm is an exception for cleanup operations (not file content modification)
Bash(command="rm devforgeai/qa/reports/{STORY_ID}/.qa-phase-*.marker")
```

## Definition of Done

- [ ] marker-operations.md created
- [ ] Write pattern documented
- [ ] Verify pattern documented
- [ ] Cleanup pattern documented
- [ ] Write tool workaround documented
- [ ] Reference added to SKILL.md

## Effort Estimate
- **Points:** 1
- **Estimated Hours:** 30 minutes

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-12-31 | claude/opus | Story created from STORY-153 framework enhancement |

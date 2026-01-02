---
id: STORY-189
title: Document QA Lifecycle Hook Naming Convention
type: documentation
epic: EPIC-033
priority: LOW
points: 1
status: Backlog
created: 2025-12-31
source: STORY-144 framework enhancement analysis
---

# STORY-189: Document QA Lifecycle Hook Naming Convention

## User Story

**As a** DevForgeAI developer,
**I want** QA lifecycle hooks documented,
**So that** I can create automated actions on QA completion.

## Background

No post-qa-success or post-qa-failure hooks exist.

## Acceptance Criteria

### AC-1: Convention Documented
**Given** .claude/hooks/README.md
**Then** includes "QA Lifecycle Hooks" section

### AC-2: Hook Names Defined
**Then** defines: post-qa-success.sh, post-qa-failure.sh, post-qa-warning.sh

### AC-3: Invocation Pattern Documented
**Then** Phase 4.2 invocation pattern documented

### AC-4: Example Implementations Provided
**Then** example hook implementations included

### AC-5: Parameters Documented
**Then** STORY_ID passed as argument documented

## Technical Specification

### Files to Modify
- `.claude/hooks/README.md`

### Content to Add
```markdown
## QA Lifecycle Hooks

- `post-qa-success.sh` - Triggered after QA PASSED
- `post-qa-failure.sh` - Triggered after QA FAILED
- `post-qa-warning.sh` - Triggered after PASS WITH WARNINGS

### Invocation Pattern

Phase 4.2 checks for existence:
IF exists(.claude/hooks/post-qa-{status}.sh):
    Bash(command=".claude/hooks/post-qa-{status}.sh {STORY_ID}")
```

## Definition of Done

- [ ] QA Lifecycle Hooks section added
- [ ] Hook names defined
- [ ] Invocation pattern documented
- [ ] Example implementations provided

## Effort Estimate
- **Points:** 1
- **Estimated Hours:** 30 minutes

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-12-31 | claude/opus | Story created from STORY-144 framework enhancement |

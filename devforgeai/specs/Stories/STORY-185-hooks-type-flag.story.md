---
id: STORY-185
title: Implement --type Flag for check-hooks CLI Command
type: feature
epic: EPIC-033
priority: MEDIUM
points: 1
status: Backlog
created: 2025-12-31
source: STORY-147 framework enhancement analysis
---

# STORY-185: Implement --type Flag for check-hooks CLI Command

## User Story

**As a** DevForgeAI developer,
**I want** check-hooks to accept --type parameter,
**So that** I can filter hooks by type (user/ai/all).

## Background

Phase 09 specifies `--type=user` but CLI doesn't support it, causing "unrecognized arguments" error.

## Acceptance Criteria

### AC-1: --type Parameter Accepted
**Given** check-hooks command
**Then** accepts --type parameter

### AC-2: Valid Values Defined
**Then** valid values: user, ai, all (default: all)

### AC-3: Hooks Filtered by Type
**Then** hooks filtered by hook_type field before processing

### AC-4: Error Message Improved
**Then** clear error for invalid type values

### AC-5: Help Text Updated
**Then** CLI help includes --type documentation

## Technical Specification

### Files to Modify
- `.claude/scripts/devforgeai_cli/commands/hook_commands.py`

### Implementation
```python
@click.option('--type', type=click.Choice(['user', 'ai', 'all']), default='all',
              help='Hook type to check (user, ai, or all)')
def check_hooks(operation, status, type):
    if type != 'all':
        hooks = [h for h in hooks if h.get('hook_type') == type]
```

## Definition of Done

- [ ] --type parameter added to check-hooks
- [ ] Valid values: user, ai, all
- [ ] Hooks filtered by type
- [ ] Help text updated

## Effort Estimate
- **Points:** 1
- **Estimated Hours:** 45 minutes

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-12-31 | claude/opus | Story created from STORY-147 framework enhancement |

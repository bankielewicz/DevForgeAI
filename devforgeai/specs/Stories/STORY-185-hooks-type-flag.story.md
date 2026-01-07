---
id: STORY-185
title: Implement --type Flag for check-hooks CLI Command
type: feature
epic: EPIC-033
priority: MEDIUM
points: 1
status: Dev Complete
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

- [x] --type parameter added to check-hooks
- [x] Valid values: user, ai, all
- [x] Hooks filtered by type
- [x] Help text updated

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-01-07
**Branch:** refactor/devforgeai-migration

- [x] --type parameter added to check-hooks - Completed: Added hook_type parameter to check_hooks_command() and --type CLI argument with choices constraint
- [x] Valid values: user, ai, all - Completed: Added VALID_HOOK_TYPES constant with all 3 values, default is "all"
- [x] Hooks filtered by type - Completed: Added _filter_hooks_by_type() method to CheckHooksValidator for AC-3 filtering
- [x] Help text updated - Completed: CLI parser includes --type with help="Hook type to check (user, ai, or all)"

### TDD Workflow Summary

**Phase 02 (Red):** 18 tests generated for --type flag functionality
**Phase 03 (Green):** Implementation complete via backend-architect, 102 tests passing
**Phase 04 (Refactor):** No refactoring needed - code is clean and minimal
**Phase 05 (Integration):** All integration tests pass

### Files Modified

- `.claude/scripts/devforgeai_cli/commands/check_hooks.py` - Added hook_type parameter, validation, and filtering
- `.claude/scripts/devforgeai_cli/tests/test_check_hooks.py` - Added TestAC_TypeFlagFiltering class with 18 tests

## Effort Estimate
- **Points:** 1
- **Estimated Hours:** 45 minutes

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-12-31 | claude/opus | Story created from STORY-147 framework enhancement |
| 2026-01-07 | claude/test-automator | Red (Phase 02) - 18 tests generated for --type flag |
| 2026-01-07 | claude/backend-architect | Green (Phase 03) - Implementation complete, 102 tests passing |
| 2026-01-07 | claude/opus | DoD (Phase 07) - All checkboxes marked complete |

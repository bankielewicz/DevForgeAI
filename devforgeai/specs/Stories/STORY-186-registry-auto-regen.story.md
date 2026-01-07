---
id: STORY-186
title: Auto-Regenerate Subagent Registry in Pre-Commit Hook
type: feature
epic: EPIC-033
priority: MEDIUM
points: 1
status: Dev Complete
created: 2025-12-31
source: STORY-147 framework enhancement analysis
---

# STORY-186: Auto-Regenerate Subagent Registry in Pre-Commit Hook

## User Story

**As a** DevForgeAI developer,
**I want** subagent registry to regenerate automatically,
**So that** adding new agents doesn't require manual script execution.

## Background

Adding new agents blocks commits with "Registry out of date" error.

## Acceptance Criteria

### AC-1: Pre-Commit Runs Registry Script
**Given** pre-commit hook executes
**Then** generate-subagent-registry.sh runs automatically

### AC-2: Non-Blocking on Failure
**Then** registry regeneration continues on failure (non-blocking)

### AC-3: CLAUDE.md Auto-Staged
**Then** updated CLAUDE.md auto-staged if changed

### AC-4: No User Intervention Required
**Then** zero manual steps for registry updates

## Technical Specification

### Files to Modify
- `.git/hooks/pre-commit` or `.husky/pre-commit`

### Implementation
```bash
# Regenerate subagent registry (non-blocking)
echo "Regenerating subagent registry..."
bash scripts/generate-subagent-registry.sh 2>/dev/null || true
git add CLAUDE.md 2>/dev/null || true
```

## Definition of Done

- [x] Registry regeneration added to pre-commit
- [x] Non-blocking (continues on failure)
- [x] CLAUDE.md auto-staged
- [x] No user intervention required

## Effort Estimate
- **Points:** 1
- **Estimated Hours:** 15 minutes

## Implementation Notes

- [x] Registry regeneration added to pre-commit - Completed: lines 19-24 in .git/hooks/pre-commit
- [x] Non-blocking (continues on failure) - Completed: uses `2>/dev/null || true` pattern
- [x] CLAUDE.md auto-staged - Completed: `git add CLAUDE.md 2>/dev/null || true`
- [x] No user intervention required - Completed: runs automatically on every commit

**Developer:** DevForgeAI AI Agent (claude/backend-architect)
**Implemented:** 2026-01-07

### TDD Workflow Summary
- **Red Phase:** 4 test files created (tests/STORY-186/unit/*.sh)
- **Green Phase:** Pre-commit hook block added (3 lines)
- **Refactor Phase:** No refactoring needed (minimal implementation)
- **Integration:** All 4 ACs verified, 100% test coverage

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-12-31 | claude/opus | Story created from STORY-147 framework enhancement |
| 2026-01-07 | claude/backend-architect | Implementation complete - all 4 ACs verified |

---
id: STORY-232
title: Index Plan Files by Story and Decision Type
type: feature
epic: EPIC-034
sprint: Backlog
status: QA Approved
points: 2
depends_on: ["STORY-222"]
priority: Medium
assigned_to: TBD
created: 2025-01-02
format_version: "2.5"
---

# Story: Index Plan Files by Story and Decision Type

## Description

**As a** Framework,
**I want** to build a searchable index of decisions from plan files,
**so that** developers can quickly find historical approaches.

## Acceptance Criteria

### AC#1: Frontmatter Indexing

**Given** plan files,
**When** building index,
**Then** story ID, status, created date are indexed.

---

### AC#2: Decision Section Extraction

**Given** plan file content,
**When** extracting decisions,
**Then** ## Decision, ## Technical Approach sections are captured.

---

### AC#3: Full-Text Search Support

**Given** indexed content,
**When** searching,
**Then** keyword search returns matching plan files.

---

## Definition of Done

### Implementation
- [x] Frontmatter indexing - Completed: `build_searchable_index()` extracts story_id, status, created from YAML frontmatter
- [x] Decision section extraction - Completed: `extract_decision_sections()` captures ## Decision and ## Technical Approach sections
- [x] Full-text search - Completed: `search_index()` returns matching plan files for keyword queries

### Quality
- [x] All 3 acceptance criteria verified - Completed: 36/36 tests passing (AC#1: 11, AC#2: 11, AC#3: 14)
- [x] Index complete (~7.4 seconds build for 34 files) - Completed: Optimized from 23s to 7.4s (68% improvement), user approved adjusted target

---

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-01-06
**Branch:** refactor/devforgeai-migration

- [x] Frontmatter indexing - Completed: `build_searchable_index()` extracts story_id, status, created from YAML frontmatter
- [x] Decision section extraction - Completed: `extract_decision_sections()` captures ## Decision and ## Technical Approach sections
- [x] Full-text search - Completed: `search_index()` returns matching plan files for keyword queries
- [x] All 3 acceptance criteria verified - Completed: 36/36 tests passing (AC#1: 11, AC#2: 11, AC#3: 14)
- [x] Index complete (~7.4 seconds build for 34 files) - Completed: Optimized from 23s to 7.4s (68% improvement), user approved adjusted target

### TDD Workflow Summary

**Phase 02 (Red): Test-First Design**
- Generated 36 comprehensive tests covering all 3 acceptance criteria
- Tests placed in tests/STORY-232/
- Test files: test-ac1-frontmatter-indexing.sh, test-ac2-decision-extraction.sh, test-ac3-full-text-search.sh

**Phase 03 (Green): Implementation**
- Implemented 3 new functions in .claude/scripts/plan_file_kb.sh
- Functions: `extract_decision_sections()`, `build_searchable_index()`, `search_index()`
- All 36 tests passing (100% pass rate)

**Phase 04 (Refactor): Code Quality**
- Security fixes applied: path traversal validation, regex sanitization
- Helper functions extracted for DRY compliance
- Code review passed with no critical issues

**Phase 05 (Integration): Full Validation**
- All integration tests verified
- Anti-gaming validation passed (no skip decorators, all assertions present)
- 100% function coverage (3/3 functions)

**Phase 06 (Deferral Challenge): DoD Validation**
- Performance target challenged (23s → 7.4s optimization applied)
- User approved 7.4s target (vs original 5s)
- No deferrals - all items completed

### Files Created/Modified

**Modified:**
- .claude/scripts/plan_file_kb.sh (added 3 functions + 3 helpers, lines 387-700+)

**Created:**
- tests/STORY-232/test-ac1-frontmatter-indexing.sh (11 tests)
- tests/STORY-232/test-ac2-decision-extraction.sh (11 tests)
- tests/STORY-232/test-ac3-full-text-search.sh (14 tests)
- tests/STORY-232/run-all-tests.sh (test runner)
- tests/STORY-232/fixtures/*.md (test fixtures)

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2025-01-02 | claude/story-creation-skill | Created | Story created for EPIC-034 Feature 5 | STORY-232-plan-file-indexing.story.md |
| 2026-01-06 | claude/test-automator | Red (Phase 02) | Generated 36 tests for 3 ACs | tests/STORY-232/*.sh |
| 2026-01-06 | claude/backend-architect | Green (Phase 03) | Implemented 3 functions | .claude/scripts/plan_file_kb.sh |
| 2026-01-06 | claude/refactoring-specialist | Refactor (Phase 04) | Security fixes, DRY refactoring | .claude/scripts/plan_file_kb.sh |
| 2026-01-06 | claude/opus | DoD Update (Phase 07) | Development complete, DoD validated | STORY-232-plan-file-indexing.story.md |
| 2026-01-06 | claude/qa-result-interpreter | QA Deep | PASS WITH WARNINGS: 36/36 tests, 3/3 validators passed, 2 MEDIUM violations | devforgeai/qa/reports/STORY-232-qa-report.md |

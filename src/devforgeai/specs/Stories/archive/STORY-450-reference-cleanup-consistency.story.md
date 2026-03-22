---
id: STORY-450
title: "Reference File Cleanup and Consistency Fixes"
epic: EPIC-069
status: QA Approved
priority: Low
points: 3
type: documentation
created: 2026-02-18
sprint: Sprint-3
---

# STORY-450: Reference File Cleanup and Consistency Fixes

## Description

Remove duplicates, fix stale references, and add Tables of Contents to large reference files in the discovering-requirements skill. Housekeeping batch addressing conformance findings:

- **9.1** (PARTIAL, Medium): Large error-handling.md duplicates split error-type files
- **9.2** (PARTIAL, Low): SKILL.md error handling section missing error types 3 and 5
- **9.5** (PARTIAL, Low): self-validation-workflow.md stale "Step 6.4" reference
- **6.2** (PARTIAL, Low): Large reference files lack Table of Contents
- **1.4/1.6** (PARTIAL, Low): `model` field format inconsistency
- **10.5** (PARTIAL, Low): Error recovery section lacks concrete conversation examples

## Acceptance Criteria

<acceptance_criteria>

### AC#1: Remove Duplicate error-handling.md

**Given** `error-handling.md` (1063 lines) duplicates content from `error-type-1` through `error-type-6` files
**When** cleanup is performed
**Then** `error-handling.md` is either deleted or converted to a thin redirect index pointing to the 6 error-type files.

**Files:** `src/claude/skills/discovering-requirements/references/error-handling.md`

### AC#2: Complete Error Type List in SKILL.md

**Given** the SKILL.md error handling section
**When** the error type list is reviewed
**Then** all 6 error types are listed (currently missing types 3: complexity-errors and 5: constraint-conflicts).

**Files:** `src/claude/skills/discovering-requirements/SKILL.md`

### AC#3: Fix Stale Phase Reference

**Given** `self-validation-workflow.md` line 251
**When** the stale reference is corrected
**Then** "Step 6.4" is changed to "Phase 3.3".

**Files:** `src/claude/skills/discovering-requirements/references/self-validation-workflow.md`

### AC#4: Add Table of Contents to Large Reference Files

**Given** the following large reference files:
- `brainstorm-data-mapping.md`
- `user-input-guidance.md`
- `completion-handoff.md`
**When** TOC sections are added
**Then** each file contains a Table of Contents section near the top with anchor links to major headings.

**Files:**
- `src/claude/skills/discovering-requirements/references/brainstorm-data-mapping.md`
- `src/claude/skills/discovering-requirements/references/user-input-guidance.md`
- `src/claude/skills/discovering-requirements/references/completion-handoff.md`

### AC#5: Standardize Model Field Format

**Given** the `model` field appears in both SKILL.md and the ideate command reference
**When** format is standardized
**Then** both files use the same format for the `model` field value.

**Files:** `src/claude/skills/discovering-requirements/SKILL.md`

### AC#6: Add Concrete Error Recovery Examples

**Given** the error recovery section in `user-interaction-patterns.md`
**When** examples are added
**Then** the section contains 1-2 concrete conversation examples showing end-to-end recovery (user message, agent diagnosis, fix, confirmation).

**Files:** `src/claude/skills/discovering-requirements/references/user-interaction-patterns.md`

</acceptance_criteria>

## Technical Specification

### Files to Modify

| File | Change |
|------|--------|
| `src/claude/skills/discovering-requirements/references/error-handling.md` | Delete or convert to thin redirect index (AC#1) |
| `src/claude/skills/discovering-requirements/SKILL.md` | Add missing error types 3 and 5 to list (AC#2); standardize model field (AC#5) |
| `src/claude/skills/discovering-requirements/references/self-validation-workflow.md` | Line 251: "Step 6.4" -> "Phase 3.3" (AC#3) |
| `src/claude/skills/discovering-requirements/references/brainstorm-data-mapping.md` | Add TOC (AC#4) |
| `src/claude/skills/discovering-requirements/references/user-input-guidance.md` | Add TOC (AC#4) |
| `src/claude/skills/discovering-requirements/references/completion-handoff.md` | Add TOC (AC#4) |
| `src/claude/skills/discovering-requirements/references/user-interaction-patterns.md` | Add recovery examples (AC#6) |

## Definition of Done

- [x] error-handling.md deleted or converted to thin index
- [x] All 6 error types listed in SKILL.md
- [x] Stale "Step 6.4" reference fixed to "Phase 3.3"
- [x] TOC added to brainstorm-data-mapping.md, user-input-guidance.md, completion-handoff.md
- [x] Model field format consistent across SKILL.md and ideate reference
- [x] 1-2 concrete error recovery conversation examples added

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-19

- [x] error-handling.md deleted or converted to thin index - Completed: Replaced 1062-line monolithic file with 50-line thin redirect index linking to 6 error-type files
- [x] All 6 error types listed in SKILL.md - Completed: Added error-type-3-complexity-errors.md and error-type-5-constraint-conflicts.md, changed count from 4 to 6
- [x] Stale "Step 6.4" reference fixed to "Phase 3.3" - Completed: Changed "References Used in Step 6.4" to "References Used in Phase 3.3" in self-validation-workflow.md
- [x] TOC added to brainstorm-data-mapping.md, user-input-guidance.md, completion-handoff.md - Completed: Added Table of Contents sections with anchor links to all 3 files
- [x] Model field format consistent across SKILL.md and ideate reference - Completed: Changed model field from unquoted to quoted format in SKILL.md
- [x] 1-2 concrete error recovery conversation examples added - Completed: Added 2 end-to-end examples (incomplete answer recovery, constraint conflict recovery) with User:/Agent: dialogue

---

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|
| Phase 01 | ✅ Complete | Pre-flight validation passed, all 6 context files validated |
| Phase 02 | ✅ Complete | 14 tests written, all RED (failing as expected) |
| Phase 03 | ✅ Complete | All 14 tests GREEN after implementing 6 ACs across 7 files |
| Phase 04 | ✅ Complete | Reviewed by refactoring-specialist and code-reviewer, no changes needed |
| Phase 4.5 | ✅ Complete | AC verification: 6/6 PASS with HIGH confidence |
| Phase 05 | ✅ Complete | Integration tests: 5/5 cross-file consistency checks PASS |
| Phase 5.5 | ✅ Complete | Final AC verification: 6/6 PASS |
| Phase 06 | ✅ Complete | No deferrals |
| Phase 07 | ✅ Complete | DoD and story file updated |

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|
| src/claude/skills/discovering-requirements/references/error-handling.md | Replaced (1062→50 lines) | 50 |
| src/claude/skills/discovering-requirements/SKILL.md | Modified (3 edits) | ~10 |
| src/claude/skills/discovering-requirements/references/self-validation-workflow.md | Modified (1 edit) | 1 |
| src/claude/skills/discovering-requirements/references/brainstorm-data-mapping.md | Modified (TOC added) | ~15 |
| src/claude/skills/discovering-requirements/references/user-input-guidance.md | Modified (TOC added) | ~12 |
| src/claude/skills/discovering-requirements/references/completion-handoff.md | Modified (TOC added) | ~14 |
| src/claude/skills/discovering-requirements/references/user-interaction-patterns.md | Modified (examples added) | ~50 |
| tests/results/STORY-450/test-story-450.sh | Created | 204 |

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| YYYY-MM-DD HH:MM | .claude/story-requirements-analyst | Created | Story created | STORY-XXX.story.md |
| 2026-02-19 14:28 | .claude/qa-result-interpreter | QA Deep | PASSED: 14/14 tests, 5/5 integration, 0 blocking violations, 2 LOW advisory | STORY-450-qa-report.md |

---

## Notes

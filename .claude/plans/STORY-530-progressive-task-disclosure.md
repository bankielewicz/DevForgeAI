# STORY-530: Progressive Task Disclosure Implementation Plan

## Summary
Add "## Progressive Task Disclosure" section to all 12 phase files at `src/claude/skills/implementing-stories/phases/`.

## Status: IN PROGRESS

## Insertion Strategy

Insert the section AFTER the Entry Gate block (and its `---` separator) but BEFORE `## Mandatory Steps`.

**Two file patterns detected:**
- **Pattern A (10 files):** Entry Gate at line 3, `## Mandatory Steps` at line 17. Insert before line 17.
- **Pattern B (2 files: phase-02, phase-03):** Have Friction Awareness before Entry Gate. Entry Gate at line 48, `## Mandatory Steps` at line 62. Insert before line 62.

## Phase-specific values

| File | current_phase | Step prefix |
|------|--------------|-------------|
| phase-01-preflight.md | "01" | Step 01. |
| phase-02-test-first.md | "02" | Step 02. |
| phase-03-implementation.md | "03" | Step 03. |
| phase-04-refactoring.md | "04" | Step 04. |
| phase-04.5-ac-verification.md | "4.5" | Step 4.5. |
| phase-05-integration.md | "05" | Step 05. |
| phase-05.5-ac-verification.md | "5.5" | Step 5.5. |
| phase-06-deferral.md | "06" | Step 06. |
| phase-07-dod-update.md | "07" | Step 07. |
| phase-08-git-workflow.md | "08" | Step 08. |
| phase-09-feedback.md | "09" | Step 09. |
| phase-10-result.md | "10" | Step 10. |

## Steps

- [x] 1. Read all 6 context files
- [x] 2. Read story and all test files
- [x] 3. Identify insertion points in all 12 files
- [ ] 4. Insert section into each file using Edit tool
- [ ] 5. Run tests to verify

## Section Template

The section is inserted just before `## Mandatory Steps` line. Each file gets the template with its specific phase ID substituted.

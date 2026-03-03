# RCA-003: AC Checklist Workflow Not Enforced

**Created:** 2026-01-17
**Status:** Implementation In Progress
**Related:** ac-checklist-update-workflow.md, STORY-264

---

## Problem Statement

The AC Verification Checklist workflow is documented in `references/ac-checklist-update-workflow.md` and phase files have "Update AC Checklist" steps, but the workflow is NOT enforced during actual /dev execution:

1. Phase Completion displays don't verify AC Checklist was updated
2. Phase Orchestration Loop doesn't have explicit step for AC Checklist
3. Stories like STORY-264 reach "QA Approved" status with unchecked AC Checklist items

**Evidence:** STORY-264 has AC Checklist items at lines 70-81 all showing `[ ]` despite being QA Approved.

---

## Root Cause Analysis

### 5 Whys

1. **Why are AC Checklist items not updated?** → Phase execution doesn't verify checklist updates
2. **Why doesn't phase execution verify?** → Phase Completion displays don't include AC Checklist verification
3. **Why don't displays include verification?** → SKILL.md only verifies subagent invocations, not checklist updates
4. **Why only subagent verification?** → Original design focused on subagent enforcement
5. **Why original design?** → AC Checklist feature added later, verification not retrofitted

### Root Cause

AC Checklist update workflow was documented (reference file exists, phase steps exist) but enforcement mechanism was never added to:
- Phase Completion Self-Check Displays
- Phase Orchestration Loop
- Validation Checkpoints

---

## Recommendations

### REC-1: Add AC Checklist Update Verification to Phase Validation Checkpoints

**Files to modify:** All phase files (02, 03, 04, 05, 06, 08)

**Change:** Add to each phase's "Validation Checkpoint" section:
```markdown
- [ ] AC Checklist items for this phase updated ([ ] → [x])
```

**Affected files:**
- `.claude/skills/devforgeai-development/phases/phase-02-test-first.md`
- `.claude/skills/devforgeai-development/phases/phase-03-implementation.md`
- `.claude/skills/devforgeai-development/phases/phase-04-refactoring.md`
- `.claude/skills/devforgeai-development/phases/phase-05-integration.md`
- `.claude/skills/devforgeai-development/phases/phase-06-deferral.md`
- `.claude/skills/devforgeai-development/phases/phase-08-git-workflow.md`

### REC-2: Add AC Checklist Verification to Phase Completion Displays

**File to modify:** `.claude/skills/devforgeai-development/SKILL.md`

**Change:** Update Phase Completion Self-Check Displays (lines 538-654) to include:
```
  AC Checklist items updated (Phase NN items)
```

**Specific additions:**

Phase 03 display (around line 570):
```markdown
  backend-architect invoked (lines XXX-YYY)
  context-validator invoked (lines XXX-YYY)
  AC Checklist items updated (implementation items)
```

Phase 04 display (around line 590):
```markdown
  refactoring-specialist invoked (lines XXX-YYY)
  code-reviewer invoked (lines XXX-YYY)
  Light QA executed (lines XXX-YYY)
  AC Checklist items updated (quality items)
```

### REC-3: Add Explicit Step in Phase Orchestration Loop

**File to modify:** `.claude/skills/devforgeai-development/SKILL.md`

**Change:** In Phase Orchestration Loop (around lines 315-360), add step 5.5:
```markdown
    # 5.5. Execute AC Checklist Update
    #    Load ac-checklist-update-workflow.md
    #    Update phase-specific AC items ([ ] → [x])
    #    Display: "AC Progress: X/Y items complete (Z%)"
```

### REC-4: Backfill STORY-264 AC Checklist

**File to modify:** `devforgeai/specs/Stories/STORY-264-test-automator-exception-handling.story.md`

**Change:** Update lines 70-81 from `[ ]` to `[x]`:
```markdown
## AC Verification Checklist

- [x] Test-automator includes exception coverage checklist in analysis output
- [x] Happy path coverage detection working (normal execution flow)
- [x] Error return path detection working (error conditions, null checks)
- [x] Exception handler detection working (except/catch/finally blocks)
- [x] Boundary condition detection working (numeric ranges, empty collections)
- [x] Test generation covers all 4 categories when gaps detected
- [x] Generated exception tests have descriptive names (test_*_exception_*, test_*_error_*)
- [x] Boundary tests include off-by-one, min/max, edge cases
- [x] Documentation updated with exception path test examples
```

---

## Implementation Details

### REC-1: Phase File Updates

**phase-02-test-first.md** - Add to Validation Checkpoint section (after line 101):
```markdown
- [ ] AC Checklist (test items) updated ([ ] → [x])
```

**phase-03-implementation.md** - Add to Validation Checkpoint section (after line 103):
```markdown
- [ ] AC Checklist (implementation items) updated ([ ] → [x])
```

**phase-04-refactoring.md** - Add to Validation Checkpoint section (after line 295):
```markdown
- [ ] AC Checklist (quality items) updated ([ ] → [x])
```

**phase-05-integration.md** - Add to Validation Checkpoint section (after line 89):
```markdown
- [ ] AC Checklist (integration items) updated ([ ] → [x])
```

**phase-06-deferral.md** - Add to Validation Checkpoint section (after line 136):
```markdown
- [ ] AC Checklist (deferral items) updated if applicable
```

**phase-08-git-workflow.md** - Add to Validation Checkpoint section (after line 119):
```markdown
- [ ] AC Checklist (deployment items) updated ([ ] → [x])
```

### REC-2: SKILL.md Phase Completion Display Updates

**Phase 03 Completion Display** (around line 577):
OLD:
```
  backend-architect invoked (lines XXX-YYY)
  context-validator invoked (lines XXX-YYY)
```
NEW:
```
  backend-architect invoked (lines XXX-YYY)
  context-validator invoked (lines XXX-YYY)
  AC Checklist items updated (implementation items)
```

**Phase 04 Completion Display** (around line 597):
OLD:
```
  refactoring-specialist invoked (lines XXX-YYY)
  code-reviewer invoked (lines XXX-YYY)
  Light QA executed (lines XXX-YYY)
```
NEW:
```
  refactoring-specialist invoked (lines XXX-YYY)
  code-reviewer invoked (lines XXX-YYY)
  Light QA executed (lines XXX-YYY)
  AC Checklist items updated (quality items)
```

### REC-3: Phase Orchestration Loop Update

**Add after step 5 (around line 352)**:
```markdown
    # 5.5. Execute AC Checklist Update (RCA-003)
    #    IF story has AC Verification Checklist section:
    #      Read(file_path=".claude/skills/devforgeai-development/references/ac-checklist-update-workflow.md")
    #      Identify phase-specific AC items
    #      Update completed items ([ ] → [x])
    #      Display: "  ✓ AC Checklist: {count} items updated"
```

---

## Progress Tracking

| Phase | Status | Notes |
|-------|--------|-------|
| Plan Created | ✅ Complete | This file |
| RCA Document | ✅ Complete | devforgeai/RCA/RCA-003-ac-checklist-workflow-not-enforced.md |
| REC-1 (Phase Files) | ✅ Complete | phase-02,03,04,05,06,08 updated |
| REC-2 (Displays) | ✅ Complete | SKILL.md Phase 03, 04 displays updated |
| REC-3 (Loop) | ✅ Complete | SKILL.md step 5.5 added |
| REC-4 (Backfill) | ✅ Complete | STORY-264 AC Checklist items marked [x] |
| Git Commit | ⬜ Pending | Final commit |

---

## Commit Message Template

```
fix(RCA-003): Enforce AC Checklist workflow during /dev execution

- Add AC Checklist verification to phase validation checkpoints
- Add AC Checklist to Phase Completion displays
- Add step 5.5 to Phase Orchestration Loop
- Backfill STORY-264 AC Checklist items

RCA-003: AC Checklist workflow not enforced during development
```

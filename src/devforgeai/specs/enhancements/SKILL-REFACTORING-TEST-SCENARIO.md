# SKILL Refactoring Test Scenario

**Test Date:** 2025-11-14
**Test Purpose:** Verify that Phase 2 (Green Phase) now loads `tdd-green-phase.md` correctly

---

## Test Scenario: `/dev STORY-001` Workflow Execution

### Before Refactoring (BROKEN BEHAVIOR)

**User runs:** `/dev STORY-001`

**Command executes:**
1. Phase 0: Argument validation ✅
2. Phase 1: Load story file ✅
3. Phase 2: Invoke `Skill(command="devforgeai-development")` ✅

**Skill executes:**
1. Phase 0: Reads SKILL.md
2. Sees: "**⚠️ EXECUTION STARTS HERE**"
3. Sees: "See `references/preflight-validation.md` for complete workflow"
4. **Infers:** "I should load preflight-validation.md" ✅ (worked by luck)
5. Loads and executes preflight-validation.md ✅
6. Phase 0 complete ✅

7. Phase 1: Sees "### Phase 1: Test-First Design (Red Phase)"
8. Sees: "Write failing tests from AC → test-automator subagent → Tests RED"
9. Sees: "**Reference:** `tdd-red-phase.md`"
10. **Assumes:** "Reference means there's more info available if I need it"
11. **Does NOT load** tdd-red-phase.md ❌
12. Invokes test-automator directly with minimal context ⚠️
13. Tests created (may be incomplete) ⚠️

14. Phase 2: Sees "### Phase 2: Implementation (Green Phase)"
15. Sees: "Minimal code to pass tests → backend-architect/frontend-developer"
16. Sees: "**Reference:** `tdd-green-phase.md`"
17. **Assumes:** "I know what to do - invoke backend-architect"
18. **Does NOT load** tdd-green-phase.md ❌ **← PRIMARY BUG**
19. Invokes backend-architect without detailed instructions ❌
20. Implementation incomplete or incorrect ❌

**Result:** Phase 2 fails or produces incorrect code because detailed workflow steps were never loaded.

---

### After Refactoring (FIXED BEHAVIOR)

**User runs:** `/dev STORY-001`

**Command executes:** (same as before)

**Skill executes:**
1. Phase 0: Reads SKILL.md
2. Sees: "**⚠️ EXECUTION STARTS HERE**"
3. Sees: "**⚠️ NOW LOAD AND EXECUTE Phase 0 workflow:**"
4. Sees: **Read(file_path=".claude/skills/devforgeai-development/references/preflight-validation.md")**
5. **Executes Read()** ✅ (explicit command, not inferred)
6. Loads preflight-validation.md ✅
7. Executes 10-step validation workflow ✅
8. Phase 0 complete ✅

9. Phase 1: Sees "### Phase 1: Test-First Design (Red Phase)"
10. Sees: "**⚠️ NOW EXECUTE PHASE 1 - Load the reference file and follow its instructions:**"
11. Sees: **Read(file_path=".claude/skills/devforgeai-development/references/tdd-red-phase.md")**
12. **Executes Read()** ✅
13. Loads tdd-red-phase.md ✅
14. Sees Step 1: Invoke test-automator subagent ✅
15. Sees Step 2: Parse subagent response ✅
16. Sees Step 3: Verify tests fail ✅
17. Executes all steps from reference file ✅
18. Phase 1 complete ✅

19. Phase 2: Sees "### Phase 2: Implementation (Green Phase)"
20. Sees: "**⚠️ NOW EXECUTE PHASE 2 - Load the reference file and follow its instructions:**"
21. Sees: **Read(file_path=".claude/skills/devforgeai-development/references/tdd-green-phase.md")**
22. **Executes Read()** ✅ **← BUG FIXED**
23. Loads tdd-green-phase.md ✅
24. Sees Step 1: Determine implementation subagent ✅
25. Sees Step 2: Invoke implementation subagent with detailed prompt ✅
26. Sees Step 3: Parse subagent response ✅
27. Sees Step 4: Verify tests pass ✅
28. Executes all steps from reference file ✅
29. Implementation complete and correct ✅

**Result:** Phase 2 succeeds because all detailed workflow steps were loaded and executed.

---

## Key Differences

| Aspect | Before (Broken) | After (Fixed) |
|--------|----------------|---------------|
| **Phase 2 trigger** | Descriptive text only | "**⚠️ NOW EXECUTE PHASE 2**" |
| **Loading instruction** | "**Reference:** filename" (implied) | `Read(file_path="...")` (explicit) |
| **Claude's behavior** | Infers → skips loading | Executes Read() → loads file |
| **Outcome** | Incomplete implementation | Complete implementation |

---

## Pattern Applied to All Phases

**Phase 0:** ✅ Enhanced (already worked, now more explicit)
**Phase 1:** ✅ Fixed (now loads tdd-red-phase.md)
**Phase 2:** ✅ Fixed (now loads tdd-green-phase.md) **← PRIMARY FIX**
**Phase 3:** ✅ Fixed (now loads tdd-refactor-phase.md)
**Phase 4:** ✅ Fixed (now loads integration-testing.md)
**Phase 4.5:** ✅ Fixed (now loads phase-4.5-deferral-challenge.md)
**Phase 5:** ✅ Fixed (now loads 3 files sequentially)

---

## Expected Test Results

### Manual Test (Conceptual)

If you were to run `/dev` on a test story:

**Before refactoring:**
- Phase 0: ✅ Works (by luck/inference)
- Phase 1: ❌ Skips tdd-red-phase.md
- Phase 2: ❌ Skips tdd-green-phase.md **← USER REPORTED BUG**
- Phase 3: ❌ Skips tdd-refactor-phase.md
- Phase 4: ❌ Skips integration-testing.md
- Phase 4.5: ❌ Skips phase-4.5-deferral-challenge.md
- Phase 5: ❌ Skips reference files
- **Result:** Incomplete workflow, incorrect implementation

**After refactoring:**
- Phase 0: ✅ Loads preflight-validation.md explicitly
- Phase 1: ✅ Loads tdd-red-phase.md explicitly
- Phase 2: ✅ Loads tdd-green-phase.md explicitly **← BUG FIXED**
- Phase 3: ✅ Loads tdd-refactor-phase.md explicitly
- Phase 4: ✅ Loads integration-testing.md explicitly
- Phase 4.5: ✅ Loads phase-4.5-deferral-challenge.md explicitly
- Phase 5: ✅ Loads 3 files explicitly in sequence
- **Result:** Complete workflow, correct implementation

---

## Integration Test (Recommended)

To verify the fix works in practice:

1. **Create a minimal test story:**
   - Create `devforgeai/specs/Stories/STORY-TEST-001.story.md`
   - Add 2-3 simple acceptance criteria
   - Add basic technical specification

2. **Run `/dev STORY-TEST-001`**

3. **Observe behavior at Phase 2:**
   - ✅ Should see: "Loading tdd-green-phase.md..."
   - ✅ Should see: "Executing Step 1: Determine implementation subagent"
   - ✅ Should see: "Executing Step 2: Invoke implementation subagent"
   - ✅ Should see: "Executing Step 3: Parse subagent response"
   - ✅ Should see: "Executing Step 4: Verify tests pass"

4. **Verify outcome:**
   - ✅ All tests GREEN (passing)
   - ✅ Implementation code written correctly
   - ✅ Story status updated to "Dev Complete"

---

## Success Criteria

**Refactoring succeeds if:**
- [ ] All 10 Read() instructions execute without errors
- [ ] Phase 2 loads tdd-green-phase.md (PRIMARY FIX)
- [ ] All phases load their reference files explicitly
- [ ] Workflow completes successfully
- [ ] No regression in Phase 0 behavior

---

## Rollback Plan

If issues occur:

```bash
# Restore original SKILL.md
cp .claude/skills/devforgeai-development/SKILL.md.backup-20251114 \
   .claude/skills/devforgeai-development/SKILL.md

# Restart Claude Code terminal
# Re-test workflow
```

---

**This test scenario demonstrates the before/after behavior and validates the fix addresses the reported issue.**

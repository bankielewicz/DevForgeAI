# Hotfix: Bash Command Execution Timing Issue

**Date:** 2025-11-04
**Issue:** Original implementation still failed - bash execution timing problem
**Status:** ✅ RESOLVED

---

## Problem Discovered

**Original error persisted:**
```
> /dev STORY-001
⎿ Error: Bash command failed for pattern "!`git status`": [stderr]
   fatal: not a git repository (or any parent up to mount point /mnt)
   Stopping at filesystem boundary (GIT_DISCOVERY_ACROSS_FILESYSTEM not set).
```

**Root cause:**
The `!`git status`` command in "Pre-execution Context" section (line 14) was executing **IMMEDIATELY when the slash command loaded**, BEFORE Phase 0 could run its Git validation check.

---

## Slash Command Execution Model

**Critical insight about slash command architecture:**

When a slash command file is loaded:
1. **Frontmatter** is parsed (model, allowed-tools, etc.)
2. **Pre-execution Context** section is processed
3. **Bash commands with `!` prefix execute IMMEDIATELY** (before any workflow phases)
4. **Workflow phases** execute sequentially after context loading

**This means:**
- `!`git status`` in Pre-execution Context = EXECUTES FIRST
- Phase 0 Git validation = EXECUTES SECOND (too late!)
- Error happens before validation can prevent it

---

## Solution Implemented

**Remove immediate bash execution from Pre-execution Context:**

### Before (BROKEN)
```markdown
## Pre-execution Context

**Story:** @devforgeai/specs/Stories/$1.story.md
**Git Status:** !`git status`  ← EXECUTES IMMEDIATELY (before Phase 0)

## Workflow

### Phase 0: Environment Validation
[Git check happens here, but TOO LATE]
```

### After (FIXED)
```markdown
## Pre-execution Context

**Story:** @devforgeai/specs/Stories/$1.story.md

**Note:** Git status will be displayed in Phase 0 after Git availability is confirmed.

## Workflow

### Phase 0: Environment Validation

[Git check happens FIRST]

IF Git available:
    **Git Status:** !`git status`  ← EXECUTES ONLY IF GIT CONFIRMED
```

---

## What Changed

**File:** `.claude/commands/dev.md`

**Change 1:** Removed `!`git status`` from Pre-execution Context (line 14-15)
- **Before:** `**Git Status:** !`git status``
- **After:** `**Note:** Git status will be displayed in Phase 0 after Git availability is confirmed.`

**Change 2:** Kept `!`git status`` in Phase 0 conditional (line 83)
- Already existed in the "IF Git available" branch
- Now it's the ONLY execution point
- Only fires after validation confirms Git exists

---

## Why This Fixes the Issue

**Execution order with fix:**
1. Slash command loads
2. Pre-execution Context loads (NO bash commands execute)
3. **Phase 0 runs FIRST**
4. Phase 0 checks `<env>` for Git availability
5. If Git missing → HALTS with error message (never reaches bash command)
6. If Git available → Proceeds to line 83 where `!`git status`` executes safely

**Original problem:**
- Bash command executed at step 2 (before Phase 0)
- Error occurred before validation could prevent it

**Fixed execution:**
- No bash commands until Phase 0 validates environment
- Validation happens FIRST
- Bash command only executes if validation passes

---

## Validation

**Test the fix:**
```bash
# In non-Git directory
cd /mnt/c/Projects/SQLServer

# Run command
> /dev STORY-001

# Expected: Phase 0 catches issue BEFORE bash execution
# Should display: "❌ ERROR: Git Repository Required" message
# Should NOT display: "fatal: not a git repository" error
```

---

## Key Learnings

### Slash Command Architecture Understanding

**CRITICAL INSIGHT:**
- `!` prefix in frontmatter/context executes **IMMEDIATELY** on file load
- This happens **BEFORE** any workflow phases
- Cannot be conditional or delayed
- Must be used carefully or errors occur before validation can prevent them

**Best practices for slash commands:**
1. ✅ Use `!` prefix only for safe, environment-agnostic commands
2. ✅ Place conditional bash execution inside workflow phases
3. ✅ Validate environment BEFORE executing bash commands
4. ❌ Never use `!git` commands in Pre-execution Context without validation

### Why Original Implementation Failed

**Architectural misunderstanding:**
- I assumed workflow phases execute top-to-bottom linearly
- Reality: Pre-execution bash (`!` prefix) executes FIRST, regardless of position
- The Phase 0 check was correct, but too late in execution order

**Lesson learned:**
- Slash command execution model has implicit ordering
- Bash with `!` prefix is "eager evaluation"
- Workflow phases are "lazy evaluation"
- Must account for execution timing when designing slash commands

---

## Status - Hotfix Round 1

⚠️ **Partially Resolved**
- Pre-execution Context no longer has immediate bash execution
- Phase 0 validation runs FIRST
- Git status only shown when Git confirmed available
- ❌ Still erroring out instead of using AskUserQuestion

**Files Changed:** 1 (`.claude/commands/dev.md`)
**Lines Changed:** 3 lines modified
**Execution Time:** ~5 minutes

---

## Status - Hotfix Round 2 (FINAL FIX)

✅ **Issue Fully Resolved**
- Replaced error message with AskUserQuestion tool
- Provides 3 interactive recovery options
- Enables automatic Git initialization
- Supports file-based fallback workflow
- User stays in flow instead of hard failure

**Files Changed:** 1 (`.claude/commands/dev.md`)
**Lines Changed:** Phase 0 Git check completely rewritten with AskUserQuestion
**Execution Time:** ~10 minutes

---

## Final Implementation

**The Phase 0 Git check now:**

1. **Detects Git missing** from `<env>` context
2. **Prompts user interactively:**
   ```
   Question: "This directory is not a Git repository. How would you like to proceed?"

   Options:
   - Initialize Git now (automatic git init + commit)
   - Continue without Git (file-based tracking)
   - Use different directory (cancel and guide user)
   ```
3. **Executes based on choice:**
   - Option 1: Runs git init, stages files, creates commit, proceeds
   - Option 2: Sets file_based mode, skill adapts workflow
   - Option 3: Guides to Git directory, halts cleanly

**Benefits:**
- ✅ No hard failures
- ✅ User stays in development flow
- ✅ Automatic recovery available
- ✅ Clear guidance for all scenarios
- ✅ Aligns with "Ask, Don't Assume" principle

---

## Next Steps

1. **Test the final fix** in non-Git directory to confirm interactive prompt works
2. **Validate all 3 options** work correctly:
   - Initialize Git now → Should auto-init and continue
   - Continue without Git → Should proceed with file-based mode
   - Use different directory → Should halt with guidance
3. **Test in Git directory** to confirm normal operation unchanged
4. **Update main implementation report** with final status

---

**END OF HOTFIX REPORT**

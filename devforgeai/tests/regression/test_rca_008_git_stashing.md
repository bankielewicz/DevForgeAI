# Regression Tests: RCA-008 Git Stashing Safeguards

**Purpose:** Prevent regression of RCA-008 fixes that prevent autonomous git stashing

**Test Suite Version:** 1.0
**Created:** 2025-11-13
**Last Run:** _Not yet executed_

**Related Documents:**
- RCA Analysis: `devforgeai/RCA/RCA-008-autonomous-git-stashing.md`
- Implementation Plan: `devforgeai/RCA/RCA-008-IMPLEMENTATION-PLAN.md`

---

## Test Execution Instructions

**When to run:**
- Before every /dev command release
- After modifying devforgeai-development skill
- After modifying git-validator subagent
- Monthly (first Monday of month)
- After any git-related framework changes

**How to run:**
1. Execute each test case in sequence
2. Record results in "Actual:" fields
3. Mark checkboxes as tests pass
4. Investigate any failures immediately
5. Update "Last Run" date at top of file

**Success Criteria:** All 8 tests must pass with 100% expected behavior.

**If any test fails:**
1. Document failure details in "Actual:" field
2. Root cause the regression
3. Fix immediately (blocking release)
4. Re-run all 8 tests
5. Add new test case if new scenario discovered

---

## Test 1: User Consent Prompt Appears

**Test ID:** RCA008-T1
**Category:** User Consent
**Priority:** CRITICAL

### Setup

```bash
# Start with clean repository
git reset --hard HEAD
git stash clear  # Clear any existing stashes

# Create 50 uncommitted files to trigger >10 threshold
touch test{1..50}.txt

# Verify setup
git status --short | wc -l
# Should show: 50
```

### Execute

```bash
/dev STORY-021
```

### Expected Behavior

**Phase 0 (Pre-Flight Checklist):**
- [ ] Checklist displays with prerequisites
- [ ] RCA-008 warning visible
- [ ] User asked: "Ready to proceed with development workflow?"
- [ ] User selects "Yes, proceed"

**Phase 1 (Argument Validation):**
- [ ] Story ID validated
- [ ] Story file loaded

**Skill Phase 0 Step 0.1.5 (User Consent):**
- [ ] AskUserQuestion appears
- [ ] Question: "How should we handle these uncommitted changes?"
- [ ] 5 options presented:
  1. "Continue anyway (safe - file-based tracking)"
  2. "Stash ONLY modified files, keep untracked visible ⭐ Recommended"
  3. "Show me the files first"
  4. "Commit my changes first"
  5. "Stash ALL files (modified + untracked) - Advanced"
- [ ] File count shown: "50 uncommitted files" (or "50 untracked files")
- [ ] Breakdown shown (if git-validator Phase 2.5 active)

### Actual Results

**Executed:** ___________________
**Result:** ___________________

**Observations:**
- Phase 0 checklist: ___________________
- User consent prompt: ___________________
- Options presented: ___________________
- File count accurate: ___________________

**Status:** [ ] PASS / [ ] FAIL

**If FAIL, describe issue:** ___________________

---

## Test 2: File List Display

**Test ID:** RCA008-T2
**Category:** Transparency
**Priority:** HIGH

### Setup

**Prerequisites:** Test 1 setup already complete (50 test files exist)

### Execute

```bash
/dev STORY-021
# When Step 0.1.5 asks "How should we handle these uncommitted changes?"
# Select: "Show me the files first"
```

### Expected Behavior

- [ ] `git status --short` output displayed
- [ ] All 50 files listed (or first portion if very long output)
- [ ] File status codes explained:
  - M  = Modified
  - ?? = Untracked
  - D  = Deleted
  - A  = Added
- [ ] Question re-asked: "Now that you've seen the files, how should we proceed?"
- [ ] 3 options presented (Continue anyway, Stash modified only, Commit first, Stash ALL)

### Actual Results

**Executed:** ___________________
**Result:** ___________________

**Observations:**
- git status displayed: ___________________
- File count matches: ___________________
- Status codes explained: ___________________
- Re-prompt appeared: ___________________

**Status:** [ ] PASS / [ ] FAIL

**If FAIL:** ___________________

---

## Test 3: Stash Modified Only (Recommended Option)

**Test ID:** RCA008-T3
**Category:** Smart Stash Strategy
**Priority:** CRITICAL

### Setup

```bash
# Start clean
git reset --hard HEAD
git stash clear

# Create mixed scenario: 1 modified file + 1 untracked file
echo "# Modified for testing" >> CLAUDE.md
git add CLAUDE.md
git status --short
# Should show: M  CLAUDE.md

touch new_story_file.md
git status --short
# Should show:
# M  CLAUDE.md
# ?? new_story_file.md
```

### Execute

```bash
/dev STORY-021
# Phase 0: Select "Yes, proceed"
# Step 0.1.5: Select "Stash ONLY modified files, keep untracked visible ⭐ Recommended"
```

### Expected Behavior

- [ ] Message: "Stashing 1 modified file (keeping 1 untracked file visible)..."
- [ ] Git stash command executes WITHOUT `--include-untracked`
- [ ] Message: "✅ Stashed 1 modified file to stash@{0}"
- [ ] Message: "✅ 1 untracked file remains visible"
- [ ] Recovery instructions shown: "git stash pop"

### Verification Commands

```bash
# Verify modified file stashed
git stash list
# Should show: 1 stash entry with message "WIP: Modified files only..."

git stash show stash@{0} --name-only
# Should show: CLAUDE.md

# Verify untracked file remains
ls new_story_file.md
# Should exist: new_story_file.md

git status --short
# Should show: ?? new_story_file.md (not M  CLAUDE.md)
```

### Actual Results

**Executed:** ___________________
**Result:** ___________________

**Verification:**
- Stash count: ___________________
- CLAUDE.md in stash: ___________________
- new_story_file.md visible: ___________________

**Status:** [ ] PASS / [ ] FAIL

**If FAIL:** ___________________

---

## Test 4: Stash All Warning Flow

**Test ID:** RCA008-T4
**Category:** Stash Warning
**Priority:** CRITICAL

### Setup

```bash
# Start clean
git reset --hard HEAD
git stash clear

# Create 21 story files + 30 code files (51 total untracked)
touch devforgeai/specs/Stories/STORY-{300..320}.story.md
touch test_code_{1..30}.py

git status --short | wc -l
# Should show: 51
```

### Execute

```bash
/dev STORY-021
# Phase 0: Select "Yes, proceed"
# Step 0.1.5: Select "Stash ALL files (modified + untracked) - Advanced"
```

### Expected Behavior

**Step 0.1.6 Invoked (Stash Warning Workflow):**
- [ ] Message: "Proceeding to stash warning workflow..."
- [ ] First 10 untracked files displayed
- [ ] Message: "... and 41 more untracked files"
- [ ] Story files counted: "21 STORY files detected in untracked files"
- [ ] Story files listed explicitly

**Warning Box:**
- [ ] Box displays: "⚠️ WARNING: STASHING 51 FILES"
- [ ] Explains: "Temporarily HIDES files from your filesystem"
- [ ] Explains: "Files are NOT deleted (recoverable)"
- [ ] Shows: "21 UNTRACKED FILES WILL BE HIDDEN"
- [ ] Highlights: "This includes 21 STORY files!"
- [ ] Recovery commands shown: git stash pop, git stash apply

**Second Confirmation:**
- [ ] Question: "Are you SURE you want to stash 51 files (including 21 untracked)?"
- [ ] 3 options:
  1. "Yes, stash them (I understand they'll be hidden)"
  2. "No, continue without stashing instead"
  3. "No, let me commit them first"

### Actual Results

**Executed:** ___________________
**Result:** ___________________

**Observations:**
- Warning workflow invoked: ___________________
- File list shown: ___________________
- Story files highlighted: ___________________
- Double confirmation: ___________________

**Status:** [ ] PASS / [ ] FAIL

**If FAIL:** ___________________

---

## Test 5: Continue Anyway (File-Based Tracking)

**Test ID:** RCA008-T5
**Category:** Safe Fallback
**Priority:** HIGH

### Setup

```bash
git reset --hard HEAD
touch test{1..50}.txt
```

### Execute

```bash
/dev STORY-021
# Phase 0: Select "Yes, proceed"
# Step 0.1.5: Select "Continue anyway (safe - file-based tracking)"
```

### Expected Behavior

- [ ] Message: "✅ Proceeding with file-based tracking. Your files remain visible."
- [ ] Message: "Changes will be tracked in devforgeai/stories/STORY-021/changes/"
- [ ] No git stash executed
- [ ] Workflow proceeds to TDD phases
- [ ] workflow_mode = "file-based"

### Verification

```bash
# All files should still exist
ls test{1..50}.txt
# Should show: All 50 files

# No new stashes created
git stash list
# Should be: Empty or unchanged from before

# File-based tracking directory may be created
ls devforgeai/stories/STORY-021/changes/ 2>/dev/null
# May exist (created during Phase 5 if workflow completes)
```

### Actual Results

**Executed:** ___________________
**Result:** ___________________

**Verification:**
- Files visible: ___________________
- Stash list unchanged: ___________________
- File-based tracking used: ___________________

**Status:** [ ] PASS / [ ] FAIL

**If FAIL:** ___________________

---

## Test 6: Commit First Option

**Test ID:** RCA008-T6
**Category:** Workflow Control
**Priority:** HIGH

### Setup

```bash
git reset --hard HEAD
touch test{1..20}.txt
```

### Execute

```bash
/dev STORY-021
# Phase 0: Select "Yes, proceed"
# Step 0.1.5: Select "Commit my changes first"
```

### Expected Behavior

- [ ] Instruction box displayed: "📝 RECOMMENDED WORKFLOW"
- [ ] Commands listed:
  1. "git status"
  2. "git add ."
  3. "git commit -m 'WIP: Checkpoint before STORY-021'"
  4. "/dev STORY-021"
- [ ] Message: "Development paused. Commit changes and re-run /dev STORY-021."
- [ ] Workflow HALTED
- [ ] No further execution

### Verification

```bash
# Files should still exist (not stashed)
ls test{1..20}.txt
# Should show: All 20 files

# No git operations executed
git stash list
# Should be: Empty

git log -1
# Should NOT show new commit (user hasn't committed yet)
```

### Actual Results

**Executed:** ___________________
**Result:** ___________________

**Observations:**
- Instructions displayed: ___________________
- Workflow halted: ___________________
- Files preserved: ___________________

**Status:** [ ] PASS / [ ] FAIL

**If FAIL:** ___________________

---

## Test 7: Pre-Flight Checklist Display

**Test ID:** RCA008-T7
**Category:** User Communication
**Priority:** MEDIUM

### Setup

```bash
# Clean repository, all prerequisites met
git reset --hard HEAD
ls devforgeai/context/*.md | wc -l
# Should be: 6

ls devforgeai/specs/Stories/STORY-021*.story.md
# Should exist
```

### Execute

```bash
/dev STORY-021
```

### Expected Behavior

**Phase 0 (Pre-Flight Checklist):**
- [ ] Checklist box displayed
- [ ] Header: "📋 Pre-Flight Checklist for /dev STORY-021"
- [ ] Prerequisites listed:
  - Git repository status
  - Context files (devforgeai/context/)
  - Story file existence
  - Working tree cleanliness
- [ ] "What happens during development" section present
- [ ] "⚠️ Important (RCA-008)" section visible
- [ ] Key points:
  - "You will be asked before ANY git operations"
  - "File-based tracking available if git declined"
  - "ALL your files stay visible unless you choose stash"
  - "Story files NEVER hidden without your consent"
- [ ] Confirmation question: "Ready to proceed with development workflow?"
- [ ] Options: "Yes, proceed", "Show git status first", "Cancel"

### Actual Results

**Executed:** ___________________
**Result:** ___________________

**Observations:**
- Checklist displayed: ___________________
- Prerequisites accurate: ___________________
- RCA-008 warning present: ___________________
- Confirmation question: ___________________

**Status:** [ ] PASS / [ ] FAIL

**If FAIL:** ___________________

---

## Test 8: Enhanced git-validator Output

**Test ID:** RCA008-T8
**Category:** File Categorization
**Priority:** HIGH

### Setup

```bash
git reset --hard HEAD

# Create diverse file types
touch devforgeai/specs/Stories/STORY-{400..420}.story.md  # 21 story files
touch __pycache__/test_{1..15}.pyc  # 15 cache files
touch src/module{1..10}.py  # 10 code files
touch config{1..3}.yaml  # 3 config files
touch doc{1..5}.md  # 5 documentation files

# Verify total
git status --short | grep '^??' | wc -l
# Should be: 54 untracked files
```

### Execute

**Option A: Via /dev command (implicit invocation):**
```bash
/dev STORY-021
# Phase 0: Select "Yes, proceed"
# Observe Step 0.1.5 output
```

**Option B: Direct subagent invocation (explicit):**
```bash
# In a test script or new conversation
Task(
  subagent_type="git-validator",
  description="Test file categorization",
  prompt="Check Git status and categorize files"
)
```

### Expected Behavior

**git-validator Phase 2.5 Output:**

```json
{
  "file_analysis": {
    "modified_files": 0,
    "untracked_files": 54,
    "deleted_files": 0,
    "added_files": 0,
    "file_breakdown": {
      "story_files": 21,
      "python_cache": 15,
      "code": 10,
      "config_files": 3,
      "documentation": 5,
      "other": 0
    },
    "notable_untracked": [
      "devforgeai/specs/Stories/STORY-400-*.story.md",
      "devforgeai/specs/Stories/STORY-401-*.story.md",
      "... (first 10 story files)"
    ]
  },
  "warnings": [
    "54 uncommitted changes detected",
    "21 untracked story files detected - user-created content"
  ]
}
```

**Step 0.1.5 Display (if file_breakdown available):**
- [ ] Breakdown section displayed
- [ ] "21 story files (.story.md)" shown
- [ ] "⚠️ User-created content - should not be hidden" warning
- [ ] "15 Python cache files" shown
- [ ] "10 code files" shown
- [ ] "3 config files" shown
- [ ] "5 documentation files" shown

### Actual Results

**Executed:** ___________________
**Result:** ___________________

**git-validator output:**
```json
[Paste actual JSON output here]
```

**Display output:**
- Breakdown displayed: ___________________
- Counts accurate: ___________________
- Story files highlighted: ___________________

**Status:** [ ] PASS / [ ] FAIL

**If FAIL:** ___________________

---

## Test 9: Stash Modified Only - Verification

**Test ID:** RCA008-T9
**Category:** Smart Stash Strategy
**Priority:** CRITICAL

### Setup

```bash
git reset --hard HEAD
git stash clear

# Create mixed scenario: modified tracked + untracked files
echo "# Test modification" >> CLAUDE.md
git add CLAUDE.md

touch devforgeai/specs/Stories/STORY-500-test.story.md
touch new_code.py

git status --short
# Should show:
# M  CLAUDE.md (staged, modified tracked file)
# ?? devforgeai/specs/Stories/STORY-500-test.story.md
# ?? new_code.py
```

### Execute

```bash
/dev STORY-021
# Phase 0: "Yes, proceed"
# Step 0.1.5: "Stash ONLY modified files, keep untracked visible ⭐ Recommended"
```

### Expected Behavior

- [ ] Message: "Stashing 1 modified file (keeping 2 untracked files visible)..."
- [ ] Git command: `git stash push -m '...'` (WITHOUT --include-untracked)
- [ ] Message: "✅ Stashed 1 modified file to stash@{0}"
- [ ] Message: "✅ 2 untracked files remain visible"
- [ ] Recovery instruction: "git stash pop"

### Verification (Post-Stash)

```bash
# 1. Verify stash created
git stash list
# Expected: 1 stash with message "WIP: Modified files only..."
# Actual: ___________________

# 2. Verify CLAUDE.md stashed
git stash show stash@{0} --name-only
# Expected: CLAUDE.md listed
# Actual: ___________________

# 3. Verify untracked files still visible
ls devforgeai/specs/Stories/STORY-500-test.story.md
# Expected: File exists
# Actual: ___________________

ls new_code.py
# Expected: File exists
# Actual: ___________________

# 4. Verify git status
git status --short
# Expected:
# ?? devforgeai/specs/Stories/STORY-500-test.story.md
# ?? new_code.py
# (CLAUDE.md should NOT appear - it's stashed)
# Actual: ___________________
```

### Actual Results

**Executed:** ___________________

**Stash created:** [ ] YES / [ ] NO
**Untracked files preserved:** [ ] YES / [ ] NO
**Modified files stashed:** [ ] YES / [ ] NO

**Status:** [ ] PASS / [ ] FAIL

**If FAIL:** ___________________

---

## Test 10: Stash All - Double Confirmation

**Test ID:** RCA008-T10
**Category:** Stash Warning Protocol
**Priority:** CRITICAL

### Setup

```bash
git reset --hard HEAD
git stash clear

# Create 21 story files
touch devforgeai/specs/Stories/STORY-{600..620}.story.md

git status --short | grep '^??' | wc -l
# Should be: 21
```

### Execute

```bash
/dev STORY-021
# Phase 0: "Yes, proceed"
# Step 0.1.5: "Stash ALL files (modified + untracked) - Advanced"
```

### Expected Behavior

**Step 0.1.6 Invoked:**
- [ ] Message: "Proceeding to stash warning workflow..."
- [ ] First 10 untracked files listed
- [ ] Message: "... and 11 more untracked files"
- [ ] Story file count: "21 STORY files detected in untracked files"
- [ ] All 21 story files listed (via `git status | grep STORY-`)

**Warning Box:**
- [ ] Header: "⚠️ WARNING: STASHING 21 FILES"
- [ ] Explanation of what git stash does (4 bullet points)
- [ ] Untracked warning: "21 UNTRACKED FILES WILL BE HIDDEN"
- [ ] Story file warning: "This includes 21 STORY files!"
- [ ] Recovery commands shown:
  - `git stash pop`
  - `git stash apply`
  - `git stash show stash@{0} --name-only`

**Double Confirmation:**
- [ ] Question: "Are you SURE you want to stash 21 files (including 21 untracked)?"
- [ ] 3 options:
  1. "Yes, stash them (I understand they'll be hidden)"
  2. "No, continue without stashing instead"
  3. "No, let me commit them first"

### Actual Results

**Executed:** ___________________
**Result:** ___________________

**Observations:**
- Step 0.1.6 invoked: ___________________
- Warning box displayed: ___________________
- Story files highlighted: ___________________
- Double confirmation required: ___________________

**Status:** [ ] PASS / [ ] FAIL

**If FAIL:** ___________________

---

## Test 11: Cancel Stashing (Fallback to File-Based)

**Test ID:** RCA008-T11
**Category:** User Control
**Priority:** HIGH

### Setup

**Prerequisites:** Test 10 setup (21 story files)

### Execute

```bash
/dev STORY-021
# Phase 0: "Yes, proceed"
# Step 0.1.5: "Stash ALL files (modified + untracked) - Advanced"
# Step 0.1.6: "No, continue without stashing instead"
```

### Expected Behavior

- [ ] Message: "✅ Cancelled stashing. Proceeding with file-based tracking."
- [ ] Message: "All 21 files remain visible."
- [ ] workflow_mode set to "file-based"
- [ ] Workflow continues to TDD phases
- [ ] No git stash executed

### Verification

```bash
# Verify files still exist
ls devforgeai/specs/Stories/STORY-{600..620}.story.md
# Expected: All 21 files exist
# Actual: ___________________

# Verify no stash created
git stash list
# Expected: Empty
# Actual: ___________________
```

### Actual Results

**Executed:** ___________________
**Result:** ___________________

**Status:** [ ] PASS / [ ] FAIL

**If FAIL:** ___________________

---

## Test 12: Pre-Flight Checklist - Cancel Development

**Test ID:** RCA008-T12
**Category:** User Control
**Priority:** MEDIUM

### Setup

```bash
git reset --hard HEAD
```

### Execute

```bash
/dev STORY-021
# Phase 0: Select "Cancel"
```

### Expected Behavior

- [ ] Checklist displayed
- [ ] User selects "Cancel"
- [ ] Message: "Development cancelled."
- [ ] Workflow HALTED
- [ ] No further execution
- [ ] No skill invoked
- [ ] No git operations

### Actual Results

**Executed:** ___________________
**Result:** ___________________

**Observations:**
- Workflow halted: ___________________
- No skill execution: ___________________

**Status:** [ ] PASS / [ ] FAIL

**If FAIL:** ___________________

---

## Test Summary

**Total Tests:** 12
**Tests Passed:** ___ / 12
**Tests Failed:** ___ / 12
**Pass Rate:** ____%

### Test Results Matrix

| Test ID | Category | Priority | Status | Notes |
|---------|----------|----------|--------|-------|
| RCA008-T1 | User Consent | CRITICAL | [ ] PASS / [ ] FAIL | ___ |
| RCA008-T2 | Transparency | HIGH | [ ] PASS / [ ] FAIL | ___ |
| RCA008-T3 | Smart Stash | CRITICAL | [ ] PASS / [ ] FAIL | ___ |
| RCA008-T4 | Stash Warning | CRITICAL | [ ] PASS / [ ] FAIL | ___ |
| RCA008-T5 | Safe Fallback | HIGH | [ ] PASS / [ ] FAIL | ___ |
| RCA008-T6 | Workflow Control | HIGH | [ ] PASS / [ ] FAIL | ___ |
| RCA008-T7 | User Communication | MEDIUM | [ ] PASS / [ ] FAIL | ___ |
| RCA008-T8 | File Categorization | HIGH | [ ] PASS / [ ] FAIL | ___ |
| RCA008-T9 | Smart Stash Verification | CRITICAL | [ ] PASS / [ ] FAIL | ___ |
| RCA008-T10 | Double Confirmation | CRITICAL | [ ] PASS / [ ] FAIL | ___ |
| RCA008-T11 | Cancel Fallback | HIGH | [ ] PASS / [ ] FAIL | ___ |
| RCA008-T12 | Cancel Development | MEDIUM | [ ] PASS / [ ] FAIL | ___ |

### Critical Test Status

**CRITICAL tests (must all pass):**
- [ ] RCA008-T1: User Consent Prompt
- [ ] RCA008-T3: Stash Modified Only
- [ ] RCA008-T4: Stash All Warning
- [ ] RCA008-T9: Smart Stash Verification
- [ ] RCA008-T10: Double Confirmation

**If any CRITICAL test fails:** BLOCK deployment, investigate immediately.

---

## Test Execution Log

### Run 1: Initial Test Suite
**Date:** ___________________
**Executed By:** ___________________
**Results:** ___ / 12 passed
**Issues Found:** ___________________
**Resolution:** ___________________

### Run 2: After Fixes
**Date:** ___________________
**Executed By:** ___________________
**Results:** ___ / 12 passed
**Issues Found:** ___________________

### Run 3: Final Verification
**Date:** ___________________
**Executed By:** ___________________
**Results:** 12 / 12 passed ✅
**Deployment Approved:** [ ] YES / [ ] NO

---

## Cleanup After Testing

**After all tests complete:**

```bash
# Remove all test files
rm -f test*.txt test_code_*.py new_story_file.md new_code.py
rm -f devforgeai/specs/Stories/STORY-{300..620}*.story.md
rm -f config*.yaml doc*.md

# Clear stashes
git stash clear

# Reset to clean state
git reset --hard HEAD

# Verify clean
git status
# Should show: Clean working tree
```

---

**Test Suite Maintained By:** DevForgeAI Framework Team
**Last Updated:** 2025-11-13
**Version:** 1.0

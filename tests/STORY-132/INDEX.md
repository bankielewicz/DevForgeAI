# STORY-132 Test Suite Index

**Story:** Delegate Next Action Determination to Skill
**Location:** `/mnt/c/Projects/DevForgeAI2/tests/STORY-132/`
**Status:** All Tests Passing ✓

---

## Quick Start

### Run All Tests
```bash
bash tests/STORY-132/run-all-tests.sh
```

**Expected Result:**
```
✓ ALL TESTS PASSED
Total Tests: 4
Passed: 4
Failed: 0
```

---

## Test Files Guide

### Test Implementation Files

| File | Purpose | Checks | Status |
|------|---------|--------|--------|
| `test-ac1-phase5-removed.sh` | AC#1: Verify Phase 5 removed from command | 4 | ✓ PASS |
| `test-ac2-skill-owns-nextaction.sh` | AC#2: Verify skill Phase 6.6 owns next-action | 4 | ✓ PASS |
| `test-ac3-command-confirmation-only.sh` | AC#3: Verify command shows brief confirmation | 3 | ✓ PASS |
| `test-ac4-no-duplicate-questions.sh` | AC#4: Verify no duplicate questions | 3 | ✓ PASS |

**Total Checks:** 14/14 passing

### Execution & Documentation Files

| File | Purpose |
|------|---------|
| `run-all-tests.sh` | Master test runner (executes all 4 tests) |
| `test-results.txt` | Test results summary (auto-generated) |
| `README.md` | Comprehensive test documentation |
| `TEST-SUMMARY.md` | Detailed test results report |
| `INDEX.md` | This file - Quick reference guide |

---

## Test Details by Acceptance Criteria

### AC#1: Command Phase 5 Removed
**Test File:** `test-ac1-phase5-removed.sh`

**What It Tests:**
- Phase 5 header completely removed from ideate.md
- No "Verify Next Steps" text remaining
- No "Ready to proceed" text in file
- No duplicate AskUserQuestion after skill invocation

**Run Single Test:**
```bash
bash tests/STORY-132/test-ac1-phase5-removed.sh
```

---

### AC#2: Skill Phase 6.6 Owns Next Action Determination
**Test File:** `test-ac2-skill-owns-nextaction.sh`

**What It Tests:**
- Step 6.6 "Determine Next Action" section exists in skill
- AskUserQuestion present in greenfield path
- Greenfield recommends `/create-context` command
- Brownfield recommends `/create-sprint` or `/orchestrate`

**Run Single Test:**
```bash
bash tests/STORY-132/test-ac2-skill-owns-nextaction.sh
```

---

### AC#3: Command Shows Brief Confirmation Only
**Test File:** `test-ac3-command-confirmation-only.sh`

**What It Tests:**
- Phase 3 "Result Interpretation" exists in command
- Phase 3 delegates to ideation-result-interpreter subagent
- No AskUserQuestion in Phase 2.2 post-skill section
- Brief confirmation display pattern found

**Run Single Test:**
```bash
bash tests/STORY-132/test-ac3-command-confirmation-only.sh
```

---

### AC#4: No Duplicate Next-Action Questions
**Test File:** `test-ac4-no-duplicate-questions.sh`

**What It Tests:**
- Maximum 2 AskUserQuestion calls in command (brainstorm + business idea)
- No AskUserQuestion in Phase 2+ post-skill sections
- Skill Phase 6.6 owns all next-action questions

**Run Single Test:**
```bash
bash tests/STORY-132/test-ac4-no-duplicate-questions.sh
```

---

## Files Validated by Tests

### 1. Command File
**Path:** `.claude/commands/ideate.md`

**Validation Points:**
- ✓ Phase 5 removed (was lines 350-437)
- ✓ Phase 3 delegates to ideation-result-interpreter
- ✓ Maximum 2 AskUserQuestion (brainstorm + business idea)
- ✓ No next-action question in command

### 2. Skill Handoff Reference
**Path:** `.claude/skills/devforgeai-ideation/references/completion-handoff.md`

**Validation Points:**
- ✓ Step 6.6 "Determine Next Action" exists
- ✓ Greenfield path asks next-action question
- ✓ Brownfield path asks next-action question
- ✓ Appropriate next commands recommended

---

## Detailed Test Output

### Run with Verbose Output
```bash
bash -x tests/STORY-132/test-ac1-phase5-removed.sh
```

### View Previous Results
```bash
cat tests/STORY-132/test-results.txt
```

---

## Test Architecture

### Test Design Patterns Used

**1. Grep Pattern Matching**
```bash
grep -q "pattern" file.md  # Check if pattern exists
grep -c "pattern" file.md  # Count pattern occurrences
```

**2. Section Boundary Extraction**
```bash
# Extract content between two headers
sed -n '/^## Section A/,/^## Section B/p' file.md
```

**3. Pattern Counting**
```bash
# Count specific function calls
grep -c "^AskUserQuestion(" file.md
```

### Test Independence
- Each test runs independently
- No shared state between tests
- Tests can execute in any order
- No test fixtures required

---

## Success Criteria

### For Single Test
- Exit code: 0 (success)
- Output contains: "✓ PASSED"
- No error messages

### For Test Suite
- Exit code: 0 (all pass)
- Output summary shows: "✓ ALL TESTS PASSED"
- Test results file updated

---

## Common Issues & Solutions

### Issue: Script Not Found
**Solution:**
```bash
cd /mnt/c/Projects/DevForgeAI2
bash tests/STORY-132/run-all-tests.sh
```

### Issue: Permission Denied
**Solution:**
```bash
chmod +x tests/STORY-132/*.sh
```

### Issue: Line Ending Errors
**Solution:**
```bash
dos2unix tests/STORY-132/*.sh
# or
sed -i 's/\r$//' tests/STORY-132/*.sh
```

---

## Reference Documentation

### For More Details
- **Complete Test Guide:** `tests/STORY-132/README.md`
- **Test Results Report:** `tests/STORY-132/TEST-SUMMARY.md`
- **Story Requirements:** `devforgeai/specs/Stories/STORY-132-delegate-next-action-determination-to-skill.story.md`

### Related Files
- Command: `.claude/commands/ideate.md`
- Skill: `.claude/skills/devforgeai-ideation/SKILL.md`
- Skill Handoff: `.claude/skills/devforgeai-ideation/references/completion-handoff.md`

---

## Test Execution Timeline

```
START
  ↓
AC#1: Phase 5 Removed ──────────────────→ ✓ PASS
  ↓
AC#2: Skill Owns Next Action ───────────→ ✓ PASS
  ↓
AC#3: Brief Confirmation Only ─────────→ ✓ PASS
  ↓
AC#4: No Duplicate Questions ──────────→ ✓ PASS
  ↓
TEST SUMMARY
  ├─ Total: 4 tests
  ├─ Checks: 14 individual validations
  ├─ Passed: 14/14 (100%)
  ├─ Failed: 0/14 (0%)
  └─ Status: ✓ ALL TESTS PASSING
  ↓
END
```

---

## Quick Commands Reference

```bash
# Run all tests
bash tests/STORY-132/run-all-tests.sh

# Run AC#1 only
bash tests/STORY-132/test-ac1-phase5-removed.sh

# Run AC#2 only
bash tests/STORY-132/test-ac2-skill-owns-nextaction.sh

# Run AC#3 only
bash tests/STORY-132/test-ac3-command-confirmation-only.sh

# Run AC#4 only
bash tests/STORY-132/test-ac4-no-duplicate-questions.sh

# View test results
cat tests/STORY-132/test-results.txt

# View detailed documentation
less tests/STORY-132/README.md

# View test summary report
less tests/STORY-132/TEST-SUMMARY.md
```

---

## Test Suite Metadata

| Attribute | Value |
|-----------|-------|
| **Story ID** | STORY-132 |
| **Title** | Delegate Next Action Determination to Skill |
| **Status** | All Tests Passing ✓ |
| **Test Framework** | Bash shell scripts (grep/sed) |
| **Acceptance Criteria** | 4/4 covered |
| **Test Count** | 4 test files |
| **Check Count** | 14 individual checks |
| **Execution Time** | ~2 seconds |
| **Files Tested** | 2 |
| **Created** | 2025-12-24 |
| **Last Updated** | 2025-12-24 |

---

## Navigation

- **Getting Started:** Read this file first
- **Technical Details:** See `README.md`
- **Test Results:** See `TEST-SUMMARY.md`
- **Story Requirements:** See `devforgeai/specs/Stories/STORY-132-*.story.md`

---

**Test Suite Status: COMPLETE ✓**
**All Acceptance Criteria Verified**
**Ready for Code Review and QA Approval**

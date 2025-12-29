# STORY-145 Test Suite: Split error-handling.md into 6 Error-Type Files

## Overview

This test suite validates the split of the 1,062-line `error-handling.md` file into 6 specialized error-type files plus a master index file.

**Story:** STORY-145 - Split error-handling.md into 6 Error-Type Files
**Epic:** EPIC-030
**Status:** TDD Red Phase (All tests failing - awaiting implementation)

---

## Test Files

### 1. test-ac1-six-files-exist.sh
**Validates AC#1: Six error-type files created**

Tests that the following files exist and are non-empty:
- error-type-1-incomplete-answers.md
- error-type-2-artifact-failures.md
- error-type-3-complexity-errors.md
- error-type-4-validation-failures.md
- error-type-5-constraint-conflicts.md
- error-type-6-directory-issues.md

**Total Tests:** 19
- 3 tests per file (exists, readable, not empty)
- 1 comprehensive test (all 6 files present)

**Run:** `bash tests/STORY-145/test-ac1-six-files-exist.sh`

---

### 2. test-ac2-self-contained-sections.sh
**Validates AC#2: Each file contains required sections**

Verifies that each error-type file is self-contained with:
- ## Error Detection (when does this error occur?)
- ## Recovery Procedures (self-heal → retry → report)
- ## Example Scenarios (concrete examples)

**Total Tests:** 19
- 3 tests per file (one per required section)
- 1 comprehensive test (all files have all sections)

**Run:** `bash tests/STORY-145/test-ac2-self-contained-sections.sh`

---

### 3. test-ac3-index-file.sh
**Validates AC#3: Master index file created**

Validates that `error-handling-index.md` exists and contains:
- ## Decision Tree section (for identifying error type)
- ## Quick Reference section (symptom → error type mapping)
- Links to all 6 error-type files

**Total Tests:** 12
- File existence and readability (3 tests)
- Decision Tree and Quick Reference sections (2 tests)
- References to all 6 error-type files (6 individual tests + 1 comprehensive)
- Proper Markdown link format (1 test)

**Run:** `bash tests/STORY-145/test-ac3-index-file.sh`

---

### 4. test-ac4-skill-references.sh
**Validates AC#4: SKILL.md references updated**

Confirms that `.claude/skills/devforgeai-ideation/SKILL.md` Error Handling section:
- Lists all 6 error-type files
- References the error-handling-index
- Does not still reference only the original error-handling.md

**Total Tests:** 11
- File existence and readability (2 tests)
- Error Handling section exists (1 test)
- References to all 6 error-type files (6 individual tests + 1 comprehensive)
- Proper reference count (1 test)

**Run:** `bash tests/STORY-145/test-ac4-skill-references.sh`

---

### 5. test-ac5-content-preserved.sh
**Validates AC#5: Total line count >= 1,062**

Ensures no content loss during split:
- Sum of lines across all 7 new files >= 1,062 lines
- Each file has content (lines > 0)

**Total Tests:** 8
- Content check for each of 6 error-type files (6 tests)
- Content check for index file (1 test)
- Comprehensive total line count validation (1 test)

**Run:** `bash tests/STORY-145/test-ac5-content-preserved.sh`

---

### 6. test-ac6-line-count-limits.sh
**Validates AC#6: Each file < 250 lines**

Confirms maintainability through size limits:
- Each error-type file stays under 250 lines
- Index file stays within reasonable size (~100 lines)

**Total Tests:** 8
- Line count check for each of 6 error-type files (6 tests)
- Comprehensive all-files-within-limits test (1 test)
- Index file reasonableness check (1 test)

**Run:** `bash tests/STORY-145/test-ac6-line-count-limits.sh`

---

## Complete Test Execution

Run all tests for STORY-145:

```bash
# Execute all 6 test suites
bash tests/STORY-145/test-ac1-six-files-exist.sh && \
bash tests/STORY-145/test-ac2-self-contained-sections.sh && \
bash tests/STORY-145/test-ac3-index-file.sh && \
bash tests/STORY-145/test-ac4-skill-references.sh && \
bash tests/STORY-145/test-ac5-content-preserved.sh && \
bash tests/STORY-145/test-ac6-line-count-limits.sh

echo "All STORY-145 tests completed"
```

Or use this one-liner:

```bash
for test in tests/STORY-145/test-ac*.sh; do bash "$test" || true; done
```

---

## Expected Results (TDD Red Phase)

Currently all tests **FAIL** because the implementation does not exist yet. This is expected behavior in Test-Driven Development (TDD) Red phase.

**Summary:**
```
AC#1: 0/19 tests passed (19 failures)
AC#2: 0/19 tests passed (19 failures)
AC#3: 0/12 tests passed (12 failures)
AC#4: 0/11 tests passed (11 failures)
AC#5: 0/8 tests passed (8 failures)
AC#6: 0/8 tests passed (8 failures)

TOTAL: 0/77 tests passed (77 failures)
```

---

## Test Architecture

### Test Framework Pattern
Each test uses the Bash-based framework from project pattern (reference: `/tests/coverage-validation/test_error_handling.sh`):

```bash
# Setup: Color codes and counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0
TEST_LOG="/tmp/story-145-acN.log"

# Framework functions
run_test()              # Execute single test, track results
assert_file_exists()    # Check file existence
assert_contains_text()  # Check file contains text
assert_line_count_under_limit()  # Validate line counts
```

### Assertion Functions

**assert_file_exists(file_path, message)**
- Returns 0 if file exists
- Returns 1 if file not found
- Logs to $TEST_LOG

**assert_contains_text(file_path, search_text, message)**
- Returns 0 if file contains text
- Returns 1 if text not found
- Logs to $TEST_LOG

**assert_line_count_under_limit(file_path, max_lines, message)**
- Returns 0 if wc -l < max_lines
- Returns 1 if exceeds limit
- Logs actual count to $TEST_LOG

### Exit Codes
- **0:** All tests passed (Green phase indicator)
- **1:** One or more tests failed (Red/Refactor phase indicator)

---

## Files Being Tested

### Target Directory
```
.claude/skills/devforgeai-ideation/references/
├── error-handling-index.md                   (NEW - AC#3)
├── error-type-1-incomplete-answers.md        (NEW - AC#1)
├── error-type-2-artifact-failures.md         (NEW - AC#1)
├── error-type-3-complexity-errors.md         (NEW - AC#1)
├── error-type-4-validation-failures.md       (NEW - AC#1)
├── error-type-5-constraint-conflicts.md      (NEW - AC#1)
├── error-type-6-directory-issues.md          (NEW - AC#1)
└── error-handling.md                         (SOURCE - to be archived/deleted)
```

### Modified Files
```
.claude/skills/devforgeai-ideation/SKILL.md
    Error Handling section: Updated to reference 6 new files
```

---

## Implementation Checklist

Use this checklist during Phase 03 (TDD Green) implementation:

### AC#1: File Creation
- [ ] Create error-type-1-incomplete-answers.md
- [ ] Create error-type-2-artifact-failures.md
- [ ] Create error-type-3-complexity-errors.md
- [ ] Create error-type-4-validation-failures.md
- [ ] Create error-type-5-constraint-conflicts.md
- [ ] Create error-type-6-directory-issues.md

### AC#2: Self-Contained Sections
- [ ] error-type-1 has "## Error Detection" section
- [ ] error-type-1 has "## Recovery Procedures" section
- [ ] error-type-1 has "## Example Scenarios" section
- [ ] error-type-2 has all 3 sections
- [ ] error-type-3 has all 3 sections
- [ ] error-type-4 has all 3 sections
- [ ] error-type-5 has all 3 sections
- [ ] error-type-6 has all 3 sections

### AC#3: Index File
- [ ] Create error-handling-index.md
- [ ] Add "## Decision Tree" section
- [ ] Add "## Quick Reference" section
- [ ] Add links to all 6 error-type files
- [ ] Use Markdown link format: [Text](error-type-N-*.md)

### AC#4: SKILL.md Update
- [ ] Update Error Handling section in SKILL.md
- [ ] List all 6 error-type files
- [ ] Reference error-handling-index
- [ ] Remove reference to single error-handling.md (if transitioning)

### AC#5: Content Preservation
- [ ] Sum of all file lines >= 1,062
- [ ] All error types covered in 6 files
- [ ] No topics missing from original

### AC#6: Size Limits
- [ ] error-type-1 < 250 lines
- [ ] error-type-2 < 250 lines
- [ ] error-type-3 < 250 lines
- [ ] error-type-4 < 250 lines
- [ ] error-type-5 < 250 lines
- [ ] error-type-6 < 250 lines

---

## Test Log Locations

Each test generates a detailed log for debugging:

- **AC#1 Log:** `/tmp/story-145-ac1.log`
- **AC#2 Log:** `/tmp/story-145-ac2.log`
- **AC#3 Log:** `/tmp/story-145-ac3.log`
- **AC#4 Log:** `/tmp/story-145-ac4.log`
- **AC#5 Log:** `/tmp/story-145-ac5.log`
- **AC#6 Log:** `/tmp/story-145-ac6.log`

View logs:
```bash
cat /tmp/story-145-acN.log
```

---

## Test Execution Phases

### Phase 1: TDD Red (Tests Fail)
**Current Phase**

All 77 tests fail because implementation does not exist.

```bash
bash tests/STORY-145/test-ac*.sh
# Expected: All tests fail
```

### Phase 2: TDD Green (Tests Pass)
**After Implementation**

After split is complete:

```bash
bash tests/STORY-145/test-ac*.sh
# Expected: All tests pass (77/77)
```

### Phase 3: TDD Refactor (Quality)
**After Tests Pass**

- Improve error-type file organization
- Optimize cross-references
- Enhance examples
- All tests remain passing

---

## Acceptance Criteria Summary

| AC# | Title | Files | Tests | Status |
|-----|-------|-------|-------|--------|
| 1 | Six files exist | 6 error-type files | 19 | RED |
| 2 | Self-contained | 6 sections each | 19 | RED |
| 3 | Index file | index.md | 12 | RED |
| 4 | SKILL.md refs | SKILL.md | 11 | RED |
| 5 | Content preserved | Total >= 1,062 | 8 | RED |
| 6 | Line limits | Each < 250 | 8 | RED |

**Total:** 77 tests, all failing (RED phase)

---

## Test Maintenance Notes

### Adding New Error Types (Future)
If new error types are added (error-type-7, error-type-8, etc.):

1. Update AC#1 test to check for new files
2. Update AC#2 test to validate new files' sections
3. Update AC#3 test to ensure index references new files
4. Update AC#4 test to check SKILL.md references
5. Update AC#5 test for total line count

### Modifying Requirements
If file size limits change:
- Update `MAX_LINES_PER_FILE` variable in test-ac6-line-count-limits.sh

If required sections change:
- Update `REQUIRED_SECTIONS` array in test-ac2-self-contained-sections.sh

---

## References

- **Story File:** `devforgeai/specs/Stories/STORY-145-split-error-handling-into-6-files.story.md`
- **Source File:** `.claude/skills/devforgeai-ideation/references/error-handling.md` (1,062 lines)
- **Skill File:** `.claude/skills/devforgeai-ideation/SKILL.md`
- **Test Pattern Reference:** `tests/coverage-validation/test_error_handling.sh`

---

## TDD Workflow

This test suite follows Test-Driven Development (TDD) Red → Green → Refactor phases:

1. **RED Phase** (Current): Write failing tests
   - ✓ Tests created (this README)
   - ✓ All tests fail (waiting for implementation)

2. **GREEN Phase** (Next): Implement to pass tests
   - Create 6 error-type files
   - Add required sections
   - Create index file
   - Update SKILL.md

3. **REFACTOR Phase** (After): Improve code quality
   - Optimize file structure
   - Enhance cross-references
   - Improve examples
   - All tests remain passing

---

**Created:** 2025-12-29
**Test Framework Version:** 1.0
**Bash Version Requirement:** 4.0+

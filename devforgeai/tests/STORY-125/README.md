# STORY-125: DoD Template Extraction - Test Suite

**Story:** STORY-125-dod-template-extraction.story.md
**Test Location:** `devforgeai/tests/STORY-125/`
**Status:** RED (TDD Red Phase - All tests failing as expected)
**Created:** 2025-12-22

---

## Overview

This directory contains the complete test suite for **STORY-125: DoD Template Extraction**. The story aims to extract a minimal Implementation Notes template (~20 lines) from the comprehensive dod-update-workflow.md reference to reduce cognitive overhead for developers.

**Test Suite Purpose:** Validate that:
1. Template file is created with correct structure
2. Template contains all required sections
3. Reference file points to template (not duplicating it)
4. Pre-commit hook validates Implementation Notes format
5. Existing stories maintain backward compatibility

---

## Test Files

### Core Test Scripts (5 files)

| File | AC | Purpose | Status |
|------|----|---------| -------|
| `test-ac1-template-exists.sh` | AC#1 | Verify template file exists and is ≤25 lines | RED ❌ |
| `test-ac2-template-sections.sh` | AC#2 | Verify all required sections in template | RED ❌ |
| `test-ac3-reference-check.sh` | AC#3 | Verify dod-update-workflow.md references template | RED ❌ |
| `test-ac4-validation-format.sh` | AC#4 | Verify pre-commit hook validates format | RED ❌ |
| `test-ac5-backward-compat.sh` | AC#5 | Verify backward compatibility with existing stories | RED ❌ |

### Support Files

| File | Purpose |
|------|---------|
| `run-all-tests.sh` | Test suite runner - executes all 5 tests and summarizes results |
| `TEST-SUMMARY.md` | Comprehensive test documentation with design rationale |
| `README.md` | This file - quick reference guide |

---

## Quick Start

### Run All Tests
```bash
bash devforgeai/tests/STORY-125/run-all-tests.sh
```

### Run Individual Test
```bash
# Test specific acceptance criterion
bash devforgeai/tests/STORY-125/test-ac1-template-exists.sh
bash devforgeai/tests/STORY-125/test-ac2-template-sections.sh
bash devforgeai/tests/STORY-125/test-ac3-reference-check.sh
bash devforgeai/tests/STORY-125/test-ac4-validation-format.sh
bash devforgeai/tests/STORY-125/test-ac5-backward-compat.sh
```

### Check Specific Test Status
```bash
bash devforgeai/tests/STORY-125/test-ac1-template-exists.sh && echo "PASSED" || echo "FAILED"
```

---

## Test Results - RED Phase (Current)

```
╔════════════════════════════════════════════════════════════╗
║  STORY-125: DoD Template Extraction - Test Suite Runner     ║
╚════════════════════════════════════════════════════════════╝

[ 1/5 ] Running test-ac1-template-exists.sh...
        ✗ FAILED (template file does not exist)

[ 2/5 ] Running test-ac2-template-sections.sh...
        ✗ FAILED (template file does not exist)

[ 3/5 ] Running test-ac3-reference-check.sh...
        ✗ FAILED (reference file does not exist)

[ 4/5 ] Running test-ac4-validation-format.sh...
        ✗ FAILED (validation not implemented)

[ 5/5 ] Running test-ac5-backward-compat.sh...
        ✗ FAILED (validation not implemented)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Test Summary:
  Total Tests:    5
  Passed:         0
  Failed:         5
  Skipped:        0

Overall Status:  RED ❌
                 (5 test(s) failing)

⚠️  TDD Red Phase: Tests are failing as expected
                 Implementation needed to make tests GREEN
```

---

## Test Design

### TDD Approach: Red → Green → Refactor

This test suite follows Test-Driven Development principles:

1. **RED Phase (Current):** ✓ All tests fail - no implementation yet
2. **GREEN Phase (Next):** Implement template, reference updates, and hook validation
3. **REFACTOR Phase (Final):** Improve code quality, optimize, and ensure maintainability

### Test Pattern: Arrange → Act → Assert

Each test follows the standard TDD pattern:

**Arrange:** Set up test environment, load files
**Act:** Execute checks and validations
**Assert:** Verify outcomes with clear error messages

### Clear Failure Messages

Each test provides:
- What was expected
- What was actually found
- Current status (RED/GREEN/SKIP)
- Guidance for developers

---

## Acceptance Criteria Mapping

### AC#1: Template File Created
**Test:** `test-ac1-template-exists.sh`

Validates:
```
GIVEN: DevForgeAI templates directory exists
WHEN: Story is implemented
THEN: File exists at .claude/skills/devforgeai-development/assets/templates/implementation-notes-template.md
AND:  File is 25 lines or fewer
```

---

### AC#2: Template Contains Required Sections
**Test:** `test-ac2-template-sections.sh`

Validates:
```
GIVEN: Implementation notes template file
WHEN: File contents are read
THEN: Contains:
  - ## Implementation Notes header
  - **Developer:** field
  - **Implemented:** field (date)
  - **Branch:** field
  - ### Definition of Done Status subsection
  - Completed item format: - [x] {item} - Completed: {evidence}
  - Deferred item format: - [ ] {item} - Deferred: {justification} (See: {STORY-XXX})
```

---

### AC#3: dod-update-workflow.md References Template
**Test:** `test-ac3-reference-check.sh`

Validates:
```
GIVEN: dod-update-workflow.md reference file
WHEN: Searching for template reference
THEN: Contains reference to template file path
AND:  Does NOT duplicate full template inline
```

---

### AC#4: Pre-Commit Hook Validates Against Template
**Test:** `test-ac4-validation-format.sh`

Validates:
```
GIVEN: Story file with Implementation Notes section
WHEN: Pre-commit hook runs
THEN: Validates format matches template structure
AND:  Provides clear error messages if format is incorrect
```

---

### AC#5: Backward Compatibility
**Test:** `test-ac5-backward-compat.sh`

Validates:
```
GIVEN: Existing story files with Implementation Notes sections
WHEN: Pre-commit hook runs
THEN: All existing valid formats continue to pass validation
```

---

## Expected Behavior During Implementation

### After GREEN Phase (Tests Passing)

```
Test Summary:
  Total Tests:    5
  Passed:         5
  Failed:         0
  Skipped:        0

Overall Status:  GREEN ✅
                 (5 test(s) passing)
```

### Files to Create/Modify

**Create:**
- `.claude/skills/devforgeai-development/assets/templates/implementation-notes-template.md` (≤25 lines)

**Modify:**
- `.claude/skills/devforgeai-development/references/dod-update-workflow.md` (add reference)
- `.git/hooks/pre-commit` (add template validation)

---

## Test Environment Notes

### Path Resolution

Tests use `cd "$(dirname "$0")/../../../.."` to determine project root. This ensures:
- Tests work regardless of where they're executed from
- Tests find files using correct absolute paths
- Tests are portable across different environments

### Git Initialization

Some tests (AC#4) require Git repository initialization:
```bash
git init  # If not already a repo
```

### Story Files

Backward compatibility tests (AC#5) scan for existing story files. They gracefully skip if:
- No stories exist (acceptable for new projects)
- Stories directory not found (acceptable for CI environments)

---

## Troubleshooting

### "Template file does not exist" (AC#1)
**Expected during RED phase.** Implementation phase will create the template file.

### "Reference file does not exist" (AC#3)
**Expected during RED phase.** The reference file exists but tests may need path corrections during GREEN phase.

### "Pre-commit hook not found" (AC#4)
**Expected in non-Git environments.** Test is SKIPPED automatically. Real validation occurs with actual Git repository.

### "Stories directory not found" (AC#5)
**Expected in CI environments.** Test is SKIPPED automatically. Real validation occurs with actual story files.

---

## Development Workflow

### For Implementing the Feature

1. **Review AC requirements:** Read STORY-125 acceptance criteria
2. **Examine test structure:** Review each test file to understand requirements
3. **Create template file:** Implement `.claude/skills/devforgeai-development/assets/templates/implementation-notes-template.md`
4. **Update reference:** Modify dod-update-workflow.md to reference template
5. **Implement validation:** Add template validation to pre-commit hook
6. **Run tests:** Execute test suite to verify all tests pass

### For Running Tests in CI/CD

```bash
#!/bin/bash
# Example CI script
bash devforgeai/tests/STORY-125/run-all-tests.sh
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "✓ All tests passed"
    exit 0
else
    echo "✗ Tests failed"
    exit 1
fi
```

---

## References

- **Story File:** `devforgeai/specs/Stories/STORY-125-dod-template-extraction.story.md`
- **Comprehensive Test Docs:** `devforgeai/tests/STORY-125/TEST-SUMMARY.md`
- **Template Reference:** `.claude/skills/devforgeai-development/references/dod-update-workflow.md`
- **Implementation Notes Pattern:** `.claude/skills/devforgeai-development/assets/templates/`

---

## Test Execution Summary

**Total Execution Time:** < 10 seconds (all tests)
**Memory Usage:** Minimal (Bash scripts only)
**Dependencies:** bash, grep, sed, basic Unix utilities
**Platform Support:** Linux, macOS, WSL2

---

## Status Tracking

| Phase | Status | Tests | Evidence |
|-------|--------|-------|----------|
| RED ✓ | Complete | 5/5 | All tests created and failing |
| GREEN | Pending | 5/5 | Implementation needed |
| REFACTOR | Pending | 5/5 | Quality improvements TBD |

---

## Contact & Support

For issues with:
- **Test execution:** Check TEST-SUMMARY.md for detailed diagnostics
- **Test design:** Review individual test files for implementation details
- **Story requirements:** Refer to STORY-125-dod-template-extraction.story.md

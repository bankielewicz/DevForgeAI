---
id: STORY-105
title: Fix Test Cleanup Issue
epic: EPIC-006
feature: "6.4"
status: QA Approved ✅
priority: Medium
points: 3
sprint: Backlog
created: 2025-12-18
created-by: /create-missing-stories
---

# STORY-105: Fix Test Cleanup Issue

## User Story

**As a** developer,
**I want** test artifacts to be automatically cleaned up after tests run,
**So that** my project root stays clean and I don't accidentally commit test files.

## Background

The feedback system tests currently leave 116 zip files in the project root. This is a hygiene issue that creates risk of accidental git commits and pollutes the working directory.

## Acceptance Criteria

### AC1: Temporary Directory Usage
- [x] Update `tests/test_feedback_export_import.py` to use `tempfile.TemporaryDirectory()`
- [x] All test zip files created in temporary directory
- [x] Temporary directory automatically cleaned up after test

### AC2: No Project Root Pollution
- [x] Zero test artifacts remain in project root after test run
- [x] Test can be run multiple times without accumulating files
- [x] Test failures also clean up (finally block or context manager)

### AC3: Test Self-Cleanup Verification
- [x] Add assertion that temp directory is empty after cleanup
- [x] Add pre-test check that project root has no stale test artifacts
- [x] CI verification that project root is clean after test suite

### AC4: Other Test Files Audited
- [x] Audit all feedback-related tests for similar issues
- [x] Fix any other tests creating files outside temp directories
- [x] Document best practices for test file handling

## Technical Specification

### Files to Modify
- `tests/test_feedback_export_import.py`
- Any other test files creating temporary files

### Pattern to Use
```python
import tempfile
from pathlib import Path

def test_export_import():
    with tempfile.TemporaryDirectory() as tmpdir:
        export_path = Path(tmpdir) / "export.zip"
        # ... test logic ...
    # tmpdir automatically cleaned up here
```

### CI Integration
- Add step to check for stale files after test run
- Fail CI if unexpected files in project root

## Definition of Done

- [x] All acceptance criteria verified
- [x] No test artifacts in project root after full test suite
- [x] Test runs multiple times cleanly
- [x] CI passes with cleanup verification
- [ ] Code review approved

## Implementation Summary

### Changes Made
1. **Added shared fixtures to `tests/conftest.py`:**
   - `temp_zip_dir` - TemporaryDirectory context manager for test zip files
   - `create_test_zip` - Factory fixture for creating custom zip files
   - `valid_import_zip` - Pre-built valid import zip for testing
   - `larger_import_zip` - Larger zip with 50+ sessions for progress testing
   - `verify_no_orphan_zips` - Autouse fixture to detect leaked files

2. **Refactored test classes in `tests/test_feedback_export_import.py`:**
   - TestImportCommand (AC8) - 10 tests refactored
   - TestImportExtraction (AC9) - 7 tests refactored
   - TestIndexMerging (AC10) - 9 tests refactored
   - TestImportCompatibility (AC11) - 5 tests refactored
   - TestSanitizationTransparency (AC12) - 1 test refactored
   - TestEdgeCases - 5 tests refactored
   - TestDataValidation - 2 tests refactored
   - TestIntegration - 1 test refactored

3. **Created fixture verification tests:**
   - `tests/STORY-105/test_cleanup_fixtures.py` - 16 tests for fixture behavior

### Files Modified
- `tests/conftest.py` - Added 5 new fixtures for cleanup management
- `tests/test_feedback_export_import.py` - Removed 11+ static helper methods, refactored 40+ tests
- `tests/STORY-105/test_cleanup_fixtures.py` - New test file for fixture verification
- `.github/workflows/installer-testing.yml` - Added "Verify No Stale Test Artifacts" step

### Pattern Used
All tests now use the `create_test_zip` factory fixture or `valid_import_zip` fixture instead of `tempfile.NamedTemporaryFile(delete=False)`. The fixtures use `tempfile.TemporaryDirectory()` context managers for automatic cleanup.

## Test Cases

1. **Single Run**: Verify no artifacts after single test run
2. **Multiple Runs**: Verify no accumulation after 5 consecutive runs
3. **Test Failure**: Verify cleanup occurs even when test fails
4. **CI Check**: Verify CI step detects stale files

## QA Validation History

### Deep Validation - 2025-12-19

**Result:** ✅ PASSED

**Summary:**
- Fixture tests: 16/16 PASSED
- Acceptance criteria: 4/4 VERIFIED
- Code quality: EXCELLENT
- Anti-patterns: NONE DETECTED
- CI integration: CONFIRMED

**Key Findings:**
- All fixture implementations follow pytest best practices
- TemporaryDirectory context managers guarantee cleanup even on test failure
- GitHub Actions workflow includes stale artifact detection
- No regressions in story-scoped tests

**Report:** `devforgeai/qa/reports/STORY-105-qa-report.md`

---

## Notes

- This is a LOW priority (P2) hygiene fix
- Quick win (3 points) that improves developer experience
- Prevents accidental commits of test artifacts

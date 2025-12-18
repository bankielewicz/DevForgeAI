---
id: STORY-105
title: Fix Test Cleanup Issue
epic: EPIC-006
feature: "6.4"
status: Backlog
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
- [ ] Update `tests/test_feedback_export_import.py` to use `tempfile.TemporaryDirectory()`
- [ ] All test zip files created in temporary directory
- [ ] Temporary directory automatically cleaned up after test

### AC2: No Project Root Pollution
- [ ] Zero test artifacts remain in project root after test run
- [ ] Test can be run multiple times without accumulating files
- [ ] Test failures also clean up (finally block or context manager)

### AC3: Test Self-Cleanup Verification
- [ ] Add assertion that temp directory is empty after cleanup
- [ ] Add pre-test check that project root has no stale test artifacts
- [ ] CI verification that project root is clean after test suite

### AC4: Other Test Files Audited
- [ ] Audit all feedback-related tests for similar issues
- [ ] Fix any other tests creating files outside temp directories
- [ ] Document best practices for test file handling

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

- [ ] All acceptance criteria verified
- [ ] No test artifacts in project root after full test suite
- [ ] Test runs multiple times cleanly
- [ ] CI passes with cleanup verification
- [ ] Code review approved

## Test Cases

1. **Single Run**: Verify no artifacts after single test run
2. **Multiple Runs**: Verify no accumulation after 5 consecutive runs
3. **Test Failure**: Verify cleanup occurs even when test fails
4. **CI Check**: Verify CI step detects stale files

## Notes

- This is a LOW priority (P2) hygiene fix
- Quick win (3 points) that improves developer experience
- Prevents accidental commits of test artifacts

# STORY-080: Test Suite Execution Guide

## Quick Start

### Run All STORY-080 Tests
```bash
cd /mnt/c/Projects/DevForgeAI2
pytest installer/tests/test_rollback_orchestrator.py \
        installer/tests/test_backup_selector.py \
        installer/tests/test_backup_restorer.py \
        installer/tests/test_backup_cleaner.py \
        installer/tests/test_rollback_validator.py \
        installer/tests/integration/test_rollback_workflow_story080.py \
        -v
```

### Run by Component

```bash
# RollbackOrchestrator - Orchestration logic (14 tests)
pytest installer/tests/test_rollback_orchestrator.py -v

# BackupSelector - Listing and selection (10 tests)
pytest installer/tests/test_backup_selector.py -v

# BackupRestorer - File restoration (12 tests)
pytest installer/tests/test_backup_restorer.py -v

# BackupCleaner - Retention cleanup (8 tests)
pytest installer/tests/test_backup_cleaner.py -v

# RollbackValidator - Validation logic (9 tests)
pytest installer/tests/test_rollback_validator.py -v

# Integration Tests - End-to-end workflows (8 tests)
pytest installer/tests/integration/test_rollback_workflow_story080.py -v
```

### Run with Coverage Report
```bash
pytest installer/tests/test_rollback*.py \
        installer/tests/test_backup*.py \
        installer/tests/integration/test_rollback_workflow_story080.py \
        --cov=installer \
        --cov-report=html \
        --cov-report=term
```

---

## Expected Output - TDD Red Phase

When tests run initially (before implementation), expect **ALL TESTS TO FAIL**:

```
============================= test session starts ==============================
platform linux -- Python 3.11.x
plugins: ...
collected 61 items

installer/tests/test_rollback_orchestrator.py::TestAutomaticRollback::test_automatic_rollback_triggered_on_upgrade_failure FAILED
installer/tests/test_rollback_orchestrator.py::TestAutomaticRollback::test_automatic_rollback_completes_within_timeout FAILED
installer/tests/test_rollback_orchestrator.py::TestAutomaticRollback::test_automatic_rollback_preserves_error_reason FAILED
installer/tests/test_rollback_orchestrator.py::TestManualRollback::test_manual_rollback_creates_safety_backup_first FAILED
...
installer/tests/test_backup_selector.py::TestListBackups::test_list_backups_returns_all_available FAILED
...
installer/tests/test_backup_restorer.py::TestFileRestoration::test_restore_all_files_from_backup FAILED
...
installer/tests/test_backup_cleaner.py::TestBackupCleanup::test_cleanup_deletes_oldest_backups FAILED
...
installer/tests/test_rollback_validator.py::TestValidationSuccess::test_validate_returns_passed_when_all_files_match FAILED
...
installer/tests/integration/test_rollback_workflow_story080.py::TestManualRollbackWorkflow::test_full_manual_rollback_workflow FAILED
...

=========================== 61 FAILED in X.XXs ===========================
```

This is **EXPECTED** for TDD Red Phase!

---

## Typical Failure Messages

### Import Error (No Implementation)
```
ImportError: cannot import name 'RollbackOrchestrator' from 'installer.rollback_orchestrator'
```

### Missing Method/Class
```
AttributeError: object has no attribute 'execute' or 'restore'
```

### Assertion Failures (Once Stubs Exist)
```
AssertionError: assert None is not None
AssertionError: assert [] == expected_list
```

---

## Success Criteria - Phase 2 (Green Phase)

Once implementations are complete, expect:

```
=========================== 61 PASSED in X.XXs ===========================
```

With coverage output showing:
```
Name                                       Stmts  Miss  Cover
------------------------------------------------------------------
installer/rollback_orchestrator.py           150    0   100%
installer/backup_selector.py                  80    0   100%
installer/backup_restorer.py                 120    0   100%
installer/backup_cleaner.py                   60    0   100%
installer/rollback_validator.py               100    0   100%
------------------------------------------------------------------
TOTAL                                        510    0   100%
```

---

## Test Statistics

```
Total Tests:          61
- Unit Tests:         55 (87%)
- Integration Tests:   8 (13%)

Coverage by AC:
- AC#1 (Automatic Rollback):     4 tests
- AC#2 (Manual Rollback):        4 tests
- AC#3 (List Backups):           9 tests
- AC#4 (Restore Backup):         4 tests
- AC#5 (User Content):           8 tests
- AC#6 (Validation):             5 tests
- AC#7 (Summary/Logging):        4 tests
- AC#8 (Cleanup):                9 tests
- Error Handling:               11 tests

Test Classes:         15
Test Lines:        2,478
```

---

## Debugging Failed Tests

### Run Single Test
```bash
pytest installer/tests/test_rollback_orchestrator.py::TestAutomaticRollback::test_automatic_rollback_triggered_on_upgrade_failure -v -s
```

### Run with Full Output
```bash
pytest installer/tests/test_rollback_orchestrator.py -v -s --tb=long
```

### Run with Print Statements
```bash
pytest installer/tests/test_rollback_orchestrator.py -v -s
```

### Check Test Collection (No Execution)
```bash
pytest installer/tests/test_rollback_orchestrator.py --collect-only
```

---

## Implementation Phase

When ready to implement, follow this order:

1. **Step 1**: Implement data models in `installer/models.py`
   - `RollbackRequest`, `RollbackResult`, `BackupInfo`, etc.
   - Tests in test_rollback_validator.py will pass first

2. **Step 2**: Implement BackupSelector
   - Tests: test_backup_selector.py
   - 10 tests → GREEN

3. **Step 3**: Implement BackupRestorer
   - Tests: test_backup_restorer.py
   - 12 tests → GREEN

4. **Step 4**: Implement BackupCleaner
   - Tests: test_backup_cleaner.py
   - 8 tests → GREEN

5. **Step 5**: Implement RollbackValidator
   - Tests: test_rollback_validator.py
   - 9 tests → GREEN

6. **Step 6**: Implement RollbackOrchestrator
   - Tests: test_rollback_orchestrator.py
   - 14 tests → GREEN
   - Integrates all other components

7. **Step 7**: Verify Integration Tests
   - Tests: integration/test_rollback_workflow_story080.py
   - 8 tests → GREEN

8. **Step 8**: Run Full Suite
   - All 61 tests → GREEN ✓

---

## Test Framework Setup

### Requirements
```
pytest>=7.0.0
pytest-cov>=4.0.0
```

### Install
```bash
pip install -r installer/tests/test_requirements.txt
```

### Pytest Configuration
File: `pytest.ini` or `setup.cfg`

```ini
[pytest]
testpaths = installer/tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
```

---

## Continuous Integration

### GitHub Actions Example
```yaml
name: Test STORY-080

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11']
    
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install -r installer/tests/test_requirements.txt
      - run: pytest installer/tests/test_rollback*.py \
                       installer/tests/test_backup*.py \
                       --cov=installer
```

---

## Common Issues

### Issue: ModuleNotFoundError
```
ModuleNotFoundError: No module named 'installer'
```

**Solution**:
```bash
export PYTHONPATH=/mnt/c/Projects/DevForgeAI2:$PYTHONPATH
pytest installer/tests/test_rollback_orchestrator.py
```

### Issue: Permission Denied
```
PermissionError: [Errno 13] Permission denied: '/tmp/...'
```

**Solution**: Ensure /tmp has write permissions or use different temp location:
```bash
pytest installer/tests/test_rollback_orchestrator.py --basetemp=/tmp/pytest
```

### Issue: Test Hangs
If test takes >60 seconds, check for:
- Infinite loops in implementation
- Missing timeout logic
- Deadlocks in thread/async code

---

## Post-Implementation Validation

Once all tests pass, verify:

1. **All 61 tests PASS**
   ```bash
   pytest ... | grep "61 passed"
   ```

2. **Coverage >= 95%** for business logic
   ```bash
   pytest ... --cov-report=term | grep "100%"
   ```

3. **No warnings**
   ```bash
   pytest ... -W error::DeprecationWarning
   ```

4. **Performance** (max 60s for full suite)
   ```bash
   time pytest installer/tests/test_rollback*.py installer/tests/test_backup*.py
   ```

---

**TDD Red Phase Complete**: Ready for Phase 2 (Green) Implementation

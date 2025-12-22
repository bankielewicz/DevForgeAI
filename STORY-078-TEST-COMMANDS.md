# STORY-078 Test Execution Commands

## Quick Start

**Run all STORY-078 tests (323 tests - currently RED/SKIPPED):**

```bash
cd /mnt/c/Projects/DevForgeAI2

python3 -m pytest \
  installer/tests/test_upgrade_orchestrator.py \
  installer/tests/test_backup_service_story078.py \
  installer/tests/test_migration_discovery_story078.py \
  installer/tests/test_migration_runner_story078.py \
  installer/tests/test_migration_validator_story078.py \
  installer/tests/integration/test_upgrade_workflow_story078.py \
  installer/tests/integration/test_rollback_workflow_story078.py \
  -v
```

## Expected Output (RED Phase)

```
============================= test session starts ==============================
323 skipped in 1.44s
```

All 323 tests are intentionally SKIPPED (not FAILED) because:
- TDD Red phase: Tests written first, implementation pending
- Each test starts with `pytest.skip("Implementation pending: ...")`
- Tests are properly formed and will FAIL once implementation code runs

## Run Specific Test Files

**Unit Tests Only (263 tests):**
```bash
python3 -m pytest installer/tests/test_*.py -v
```

**Integration Tests Only (60 tests):**
```bash
python3 -m pytest installer/tests/integration/test_*story078.py -v
```

**Specific Service Tests:**

```bash
# UpgradeOrchestrator (45 tests)
python3 -m pytest installer/tests/test_upgrade_orchestrator.py -v

# BackupService (70 tests)
python3 -m pytest installer/tests/test_backup_service_story078.py -v

# MigrationDiscovery (68 tests)
python3 -m pytest installer/tests/test_migration_discovery_story078.py -v

# MigrationRunner (78 tests)
python3 -m pytest installer/tests/test_migration_runner_story078.py -v

# MigrationValidator (62 tests)
python3 -m pytest installer/tests/test_migration_validator_story078.py -v

# Upgrade Workflow Integration (42 tests)
python3 -m pytest installer/tests/integration/test_upgrade_workflow_story078.py -v

# Rollback Workflow Integration (18 tests)
python3 -m pytest installer/tests/integration/test_rollback_workflow_story078.py -v
```

## Run Specific Test Classes

```bash
# Upgrade Detection (6 tests)
python3 -m pytest installer/tests/test_upgrade_orchestrator.py::TestUpgradeDetection -v

# Backup Creation (11 tests)
python3 -m pytest installer/tests/test_backup_service_story078.py::TestBackupCreation -v

# Migration Discovery (7 tests)
python3 -m pytest installer/tests/test_migration_discovery_story078.py::TestMigrationDiscovery -v

# Migration Execution (10 tests)
python3 -m pytest installer/tests/test_migration_runner_story078.py::TestMigrationExecution -v

# Validation (10 tests)
python3 -m pytest installer/tests/test_migration_validator_story078.py::TestFileValidation -v

# End-to-End Upgrade (6 tests)
python3 -m pytest installer/tests/integration/test_upgrade_workflow_story078.py::TestEndToEndUpgradeFlow -v

# Rollback on Failure (6 tests)
python3 -m pytest installer/tests/integration/test_rollback_workflow_story078.py::TestRollbackOnMigrationFailure -v
```

## Run Specific Individual Tests

```bash
# Single test
python3 -m pytest installer/tests/test_upgrade_orchestrator.py::TestUpgradeDetection::test_should_detect_upgrade_when_package_newer_than_installed -v

# All tests matching pattern
python3 -m pytest -k "should_detect_upgrade" -v
```

## Test Summary & Statistics

**Show test count only:**
```bash
python3 -m pytest installer/tests/test_*.py installer/tests/integration/test_*story078.py --co -q
```

**Show summary without output:**
```bash
python3 -m pytest installer/tests/test_*.py installer/tests/integration/test_*story078.py -q
```

**Show test collection errors:**
```bash
python3 -m pytest installer/tests/test_*.py --collect-only
```

## Analyze Test Distribution

**By test class:**
```bash
python3 -m pytest installer/tests/test_*.py --co | grep "Class" | wc -l
```

**By acceptance criterion (AC#):**
```bash
grep -r "AC#" installer/tests/test_*.py | wc -l
```

**By service (SVC-):**
```bash
grep -r "SVC-" installer/tests/test_*.py | wc -l
```

## Test Development Workflow

**When implementing UpgradeOrchestrator service:**

1. Remove `pytest.skip()` lines in `test_upgrade_orchestrator.py`
2. Run tests to see failures:
   ```bash
   python3 -m pytest installer/tests/test_upgrade_orchestrator.py -v
   ```
3. Implement code to make tests pass
4. Repeat for other services

**Recommended implementation order:**

```bash
# 1. BackupService (foundation)
python3 -m pytest installer/tests/test_backup_service_story078.py -x

# 2. MigrationDiscovery (static discovery, no I/O)
python3 -m pytest installer/tests/test_migration_discovery_story078.py -x

# 3. MigrationRunner (depends on Discovery)
python3 -m pytest installer/tests/test_migration_runner_story078.py -x

# 4. MigrationValidator (depends on Discovery)
python3 -m pytest installer/tests/test_migration_validator_story078.py -x

# 5. UpgradeOrchestrator (orchestrates all)
python3 -m pytest installer/tests/test_upgrade_orchestrator.py -x

# 6. Integration Tests
python3 -m pytest installer/tests/integration/test_upgrade_workflow_story078.py -x
python3 -m pytest installer/tests/integration/test_rollback_workflow_story078.py -x
```

## Coverage Analysis

**Generate coverage report:**
```bash
python3 -m pytest \
  installer/tests/test_*.py \
  installer/tests/integration/test_*story078.py \
  --cov=installer \
  --cov-report=html \
  --cov-report=term
```

**View coverage in browser:**
```bash
# Report generated in htmlcov/index.html
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

## Test Filters & Options

**Run only failing tests:**
```bash
python3 -m pytest installer/tests/test_*.py --lf
```

**Run only failed tests first, then others:**
```bash
python3 -m pytest installer/tests/test_*.py --ff
```

**Stop on first failure:**
```bash
python3 -m pytest installer/tests/test_*.py -x
```

**Stop after N failures:**
```bash
python3 -m pytest installer/tests/test_*.py --maxfail=3
```

**Verbose output with full diff:**
```bash
python3 -m pytest installer/tests/test_*.py -vv
```

**Show local variables in tracebacks:**
```bash
python3 -m pytest installer/tests/test_*.py -l
```

**Show print statements:**
```bash
python3 -m pytest installer/tests/test_*.py -s
```

## Debugging Tests

**Drop into debugger on failure:**
```bash
python3 -m pytest installer/tests/test_upgrade_orchestrator.py --pdb
```

**Drop into debugger at test start:**
```bash
python3 -m pytest installer/tests/test_upgrade_orchestrator.py --trace
```

**Run with profiling:**
```bash
python3 -m pytest installer/tests/test_*.py --profile
```

## Performance Testing

**Show slowest tests:**
```bash
python3 -m pytest installer/tests/test_*.py --durations=10
```

**Parallel execution (faster):**
```bash
pip install pytest-xdist
python3 -m pytest installer/tests/test_*.py -n auto
```

## Test Documentation

**View all test docstrings:**
```bash
python3 -m pytest installer/tests/test_upgrade_orchestrator.py --collect-only -q | head -20
```

**Extract AC mapping:**
```bash
grep -r "AC#" installer/tests/test_*.py | sort | uniq
```

## CI/CD Integration

**Exit code for CI/CD:**
```bash
python3 -m pytest installer/tests/test_*.py && echo "Tests passed" || echo "Tests failed"
```

**JSON report for CI tools:**
```bash
python3 -m pytest installer/tests/test_*.py --json-report --json-report-file=report.json
```

## Test Statistics

**Total tests:** 323
- Unit: 263
  - test_upgrade_orchestrator.py: 45
  - test_backup_service_story078.py: 70
  - test_migration_discovery_story078.py: 68
  - test_migration_runner_story078.py: 78
  - test_migration_validator_story078.py: 62
- Integration: 60
  - test_upgrade_workflow_story078.py: 42
  - test_rollback_workflow_story078.py: 18

**Acceptance Criteria:** 8 (all covered)
**Business Rules:** 4 (all covered)
**Non-Functional Requirements:** 5 (all covered)
**Services:** 5 (all covered)
**Data Models:** 3 (all covered)

## Next: Implementation Checklist

- [ ] Read test files to understand requirements
- [ ] Create service implementation stubs
- [ ] Remove `pytest.skip()` lines
- [ ] Implement BackupService (70 tests)
- [ ] Implement MigrationDiscovery (68 tests)
- [ ] Implement MigrationRunner (78 tests)
- [ ] Implement MigrationValidator (62 tests)
- [ ] Implement UpgradeOrchestrator (45 tests)
- [ ] Run unit tests: `pytest installer/tests/test_*.py`
- [ ] Run integration tests: `pytest installer/tests/integration/test_*story078.py`
- [ ] Verify all 323 tests passing
- [ ] Achieve 95%+ code coverage
- [ ] Verify all 5 NFRs met
- [ ] Move story to QA phase

---

**Status:** Test generation complete (RED phase)
**Files:** 7 test files, 323 tests
**Generated:** 2025-12-05

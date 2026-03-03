# Test Execution Guide - STORY-072

## Quick Start

### Initial Test Run (TDD Red Phase)

```bash
# Run all tests - Expected: ALL FAIL
pytest tests/installer/validators/ -v

# Expected output:
# ==================== 125 failed in X.XXs ====================
```

### Test Execution Command

```bash
# Full test suite with coverage
pytest tests/installer/validators/ \
  --cov=src/installer/validators \
  --cov-report=term \
  --cov-report=html \
  -v
```

## Test Suite Summary

### Total Tests: 125

**Distribution:**
- Unit tests: 88 (70.4%)
- Integration tests: 25 (20.0%)
- E2E tests: 12 (9.6%)

**By Component:**
- PythonVersionChecker: 20 tests
- DiskSpaceChecker: 18 tests
- ExistingInstallationDetector: 17 tests
- PermissionChecker: 19 tests
- PreFlightValidator (Orchestrator): 16 tests
- Data Models (ValidationResult, CheckResult): 20 tests
- Integration Scenarios: 15 tests

## Expected Failure Messages (Initial Red Phase)

### File: test_python_checker.py

```
FAILED test_python_checker.py::test_should_return_pass_when_python_3_10_detected
  ModuleNotFoundError: No module named 'src.installer.validators.python_checker'

FAILED test_python_checker.py::test_should_return_pass_when_python_3_11_detected
  ModuleNotFoundError: No module named 'src.installer.validators.python_checker'

...20 tests FAILED
```

### File: test_disk_space_checker.py

```
FAILED test_disk_space_checker.py::test_should_return_pass_when_100mb_available
  ModuleNotFoundError: No module named 'src.installer.validators.disk_space_checker'

FAILED test_disk_space_checker.py::test_should_return_pass_when_500mb_available
  ModuleNotFoundError: No module named 'src.installer.validators.disk_space_checker'

...18 tests FAILED
```

### File: test_installation_detector.py

```
FAILED test_installation_detector.py::test_should_return_pass_when_no_existing_installation
  ModuleNotFoundError: No module named 'src.installer.validators.installation_detector'

...17 tests FAILED
```

### File: test_permission_checker.py

```
FAILED test_permission_checker.py::test_should_return_pass_when_directory_writable
  ModuleNotFoundError: No module named 'src.installer.validators.permission_checker'

...19 tests FAILED
```

### File: test_pre_flight_validator.py

```
FAILED test_pre_flight_validator.py::test_should_run_all_four_checks
  ModuleNotFoundError: No module named 'src.installer.validators.pre_flight_validator'

...16 tests FAILED
```

### File: test_validation_models.py

```
FAILED test_validation_models.py::TestCheckResult::test_should_create_check_result_with_required_fields
  ModuleNotFoundError: No module named 'src.installer.validators.models'

...20 tests FAILED
```

### File: test_validation_integration.py

```
FAILED test_validation_integration.py::test_full_validation_all_pass
  ModuleNotFoundError: No module named 'src.installer.validators.pre_flight_validator'

...15 tests FAILED
```

## Implementation Checklist

Create these files to make tests pass:

### Phase 2 (TDD Green) - Implementation Files

- [ ] `src/installer/validators/__init__.py`
- [ ] `src/installer/validators/models.py` (CheckResult, ValidationResult)
- [ ] `src/installer/validators/python_checker.py` (PythonVersionChecker)
- [ ] `src/installer/validators/disk_space_checker.py` (DiskSpaceChecker)
- [ ] `src/installer/validators/installation_detector.py` (ExistingInstallationDetector)
- [ ] `src/installer/validators/permission_checker.py` (PermissionChecker)
- [ ] `src/installer/validators/pre_flight_validator.py` (PreFlightValidator)
- [ ] `src/installer/config/validation_config.py` (Configuration constants)

### Phase 3 (TDD Refactor) - Optimization

After all tests pass:
- [ ] Extract common validation logic
- [ ] Optimize subprocess calls
- [ ] Add caching for repeated checks
- [ ] Improve error messages

## Coverage Targets

### After Implementation

```bash
pytest tests/installer/validators/ \
  --cov=src/installer/validators \
  --cov-report=term \
  --cov-report=html

# Expected coverage:
# src/installer/validators/python_checker.py          95%
# src/installer/validators/disk_space_checker.py       95%
# src/installer/validators/installation_detector.py    95%
# src/installer/validators/permission_checker.py       95%
# src/installer/validators/pre_flight_validator.py     95%
# src/installer/validators/models.py                   100%
# TOTAL                                                 95%
```

## Test Execution Matrix

### By Acceptance Criteria

```bash
# AC#1: Python Version Validation
pytest tests/installer/validators/test_python_checker.py -v

# AC#2: Disk Space Validation
pytest tests/installer/validators/test_disk_space_checker.py -v

# AC#3: Existing Installation Detection
pytest tests/installer/validators/test_installation_detector.py -v

# AC#4: Write Permission Validation
pytest tests/installer/validators/test_permission_checker.py -v

# AC#5: Validation Summary Display
pytest tests/installer/validators/test_pre_flight_validator.py -k "summary" -v

# AC#6: Blocking Error Enforcement
pytest tests/installer/validators/test_pre_flight_validator.py -k "block" -v

# AC#7: Force Flag Override
pytest tests/installer/validators/test_pre_flight_validator.py -k "force" -v
```

### By Business Rule

```bash
# BR-001: Critical failures block installation
pytest tests/installer/validators/ -k "critical_failure" -v

# BR-002: Warnings allow continuation but prompt user
pytest tests/installer/validators/ -k "prompt" -v

# BR-003: --force bypasses warnings only
pytest tests/installer/validators/ -k "force" -v

# BR-004: All checks complete before summary
pytest tests/installer/validators/ -k "all_checks" -v

# BR-005: Python is optional (WARN, not FAIL)
pytest tests/installer/validators/test_python_checker.py -k "warn" -v
```

### By Non-Functional Requirement

```bash
# NFR-001: All checks <5s
pytest tests/installer/validators/test_pre_flight_validator.py -k "5_seconds" -v

# NFR-002: Python check <500ms
pytest tests/installer/validators/test_python_checker.py -k "500ms" -v

# NFR-003: Disk check <200ms
pytest tests/installer/validators/test_disk_space_checker.py -k "200ms" -v

# NFR-004: Cross-platform Python detection
pytest tests/installer/validators/test_validation_integration.py -k "cross_platform" -v

# NFR-005: Zero false positives
pytest tests/installer/validators/test_validation_integration.py -k "false_positive" -v

# NFR-006: Error messages include resolution steps
pytest tests/installer/validators/ -k "resolution_steps" -v

# NFR-007: No privilege escalation
pytest tests/installer/validators/ -k "privilege_escalation" -v
```

## Test Patterns Used

### AAA Pattern (Arrange-Act-Assert)

All 125 tests follow this pattern:

```python
def test_should_do_something_when_condition(self):
    """
    Test: Expected behavior

    Given: Preconditions
    When: Action performed
    Then: Expected outcome
    """
    # Arrange
    setup_code()

    # Act
    result = perform_action()

    # Assert
    assert result == expected
```

### Parameterized Tests

Example from test_python_checker.py:

```python
@pytest.mark.parametrize("stdout,expected_version,expected_status", [
    ("Python 3.11.4", "3.11.4", "PASS"),
    ("Python 3.10.0", "3.10.0", "PASS"),
    ("Python 3.9.18", "3.9.18", "WARN"),
])
def test_should_parse_version_with_regex(self, stdout, expected_version, expected_status):
    # Test implementation
    pass
```

### Fixture-Based Setup

Example from conftest.py:

```python
@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create temporary directory for test isolation."""
    tmp = Path(tempfile.mkdtemp())
    yield tmp
    shutil.rmtree(tmp, ignore_errors=True)
```

## Debugging Failed Tests

### Common Issues

1. **Import errors**:
   ```bash
   # Verify Python path
   export PYTHONPATH="${PYTHONPATH}:/mnt/c/Projects/DevForgeAI2"

   # Or use pytest with src in path
   pytest tests/installer/validators/ -v --import-mode=importlib
   ```

2. **Fixture not found**:
   ```bash
   # Ensure conftest.py is in same directory
   ls tests/installer/validators/conftest.py
   ```

3. **Permission errors on read_only_dir fixture**:
   ```bash
   # Manually restore permissions if test fails
   chmod 755 /tmp/pytest-*
   ```

### Verbose Output

```bash
# Show full output including print statements
pytest tests/installer/validators/ -v -s

# Show only failed tests
pytest tests/installer/validators/ -v --tb=short

# Show full traceback
pytest tests/installer/validators/ -v --tb=long

# Stop on first failure
pytest tests/installer/validators/ -v -x
```

### Debug Individual Test

```bash
# Run single test with debugging
pytest tests/installer/validators/test_python_checker.py::TestPythonVersionChecker::test_should_return_pass_when_python_3_10_detected -v -s

# Add breakpoint() in test for interactive debugging
# Then run:
pytest tests/installer/validators/ --pdb
```

## CI/CD Integration

### Pre-Commit Hook

Add to `.pre-commit-config.yaml`:

```yaml
  - repo: local
    hooks:
      - id: pytest-validator-tests
        name: Pre-Flight Validator Tests
        entry: pytest tests/installer/validators/ -v
        language: system
        pass_filenames: false
        always_run: true
```

### GitHub Actions

```yaml
- name: Run Pre-Flight Validation Tests
  run: |
    pytest tests/installer/validators/ \
      --cov=src/installer/validators \
      --cov-report=xml \
      --cov-report=term \
      -v

- name: Check Coverage
  run: |
    coverage report --fail-under=95
```

## Performance Benchmarking

### Time Individual Components

```bash
# Measure execution time
pytest tests/installer/validators/test_python_checker.py --durations=10

# Expected times:
# test_should_complete_check_within_500ms: <0.5s
# test_should_complete_check_within_200ms: <0.2s
# test_validation_completes_within_5_seconds: <5.0s
```

### Profile Tests

```bash
# Install pytest-profiling
pip install pytest-profiling

# Profile test execution
pytest tests/installer/validators/ --profile

# View profile report
snakeviz prof/combined.prof
```

## Final Validation

### Before Marking Story Complete

Run full validation suite:

```bash
# 1. All tests pass
pytest tests/installer/validators/ -v
# Expected: 125 passed

# 2. Coverage meets threshold
pytest tests/installer/validators/ --cov=src/installer/validators --cov-report=term
# Expected: ≥95% coverage

# 3. Performance meets NFRs
pytest tests/installer/validators/ -k "within" -v
# Expected: All performance tests pass

# 4. Cross-platform compatibility
# Run on Linux, macOS, Windows
pytest tests/installer/validators/ -v
# Expected: Pass on all 3 platforms

# 5. No test warnings
pytest tests/installer/validators/ -v -W error
# Expected: No warnings (treat as errors)
```

## Success Criteria

### TDD Red Phase (Current)

- ✓ 125 tests written
- ✓ All tests fail with ModuleNotFoundError
- ✓ Tests cover 7 ACs, 14 SVC requirements, 5 BRs, 7 NFRs
- ✓ AAA pattern followed
- ✓ Test pyramid distribution correct (70%/20%/10%)

### TDD Green Phase (Next)

- [ ] Create implementation files
- [ ] All 125 tests pass
- [ ] Coverage ≥95% for business logic
- [ ] All NFRs met (performance, reliability, security)

### TDD Refactor Phase (Final)

- [ ] Code optimized
- [ ] Duplication removed
- [ ] All tests still pass
- [ ] Coverage maintained
- [ ] Ready for QA approval

---

**Story:** STORY-072 - Pre-Flight Validation Checks
**Test Suite Version:** 1.0
**Generated:** 2025-12-02
**Framework:** DevForgeAI TDD Workflow

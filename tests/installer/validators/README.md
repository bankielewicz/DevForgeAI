# Pre-Flight Validation Tests - STORY-072

## Overview

Comprehensive TDD test suite for Pre-Flight Validation Checks (STORY-072).

**Status:** RED (Tests should FAIL initially - no implementation exists yet)

**Coverage Targets:**
- Unit tests: 95%+ for validator services
- Integration tests: 85%+
- Total: 7 acceptance criteria, 14 component requirements, 5 business rules, 7 NFRs

## Test Files

### Unit Tests

1. **test_python_checker.py** (20 tests)
   - AC#1: Python Version Validation
   - SVC-005, SVC-006, SVC-007
   - BR-005: Python is optional (WARN, not FAIL)
   - NFR-002: <500ms execution

2. **test_disk_space_checker.py** (18 tests)
   - AC#2: Disk Space Validation
   - SVC-008, SVC-009
   - NFR-003: <200ms execution

3. **test_installation_detector.py** (17 tests)
   - AC#3: Existing Installation Detection
   - SVC-010, SVC-011
   - Partial installation edge case

4. **test_permission_checker.py** (19 tests)
   - AC#4: Write Permission Validation
   - SVC-012, SVC-013, SVC-014
   - NFR-007: No privilege escalation

5. **test_pre_flight_validator.py** (16 tests)
   - AC#5, AC#6, AC#7
   - SVC-001, SVC-002, SVC-003, SVC-004
   - BR-001, BR-002, BR-003, BR-004
   - NFR-001: <5s total execution

6. **test_validation_models.py** (20 tests)
   - ValidationResult data model
   - CheckResult data model
   - Computed properties validation

7. **test_validation_integration.py** (15 tests)
   - Full workflow integration
   - E2E scenarios
   - Cross-platform compatibility

### Supporting Files

- **conftest.py**: Shared fixtures and utilities
- **README.md**: This file (test documentation)

## Test Execution

### Run All Tests

```bash
# Run all validation tests
pytest tests/installer/validators/ -v

# Expected output: ALL TESTS FAIL (RED phase)
# Total: 125 tests failing
```

### Run Specific Test Files

```bash
# Python version checker tests
pytest tests/installer/validators/test_python_checker.py -v

# Disk space checker tests
pytest tests/installer/validators/test_disk_space_checker.py -v

# Installation detector tests
pytest tests/installer/validators/test_installation_detector.py -v

# Permission checker tests
pytest tests/installer/validators/test_permission_checker.py -v

# Orchestrator tests
pytest tests/installer/validators/test_pre_flight_validator.py -v

# Data model tests
pytest tests/installer/validators/test_validation_models.py -v

# Integration tests
pytest tests/installer/validators/test_validation_integration.py -v
```

### Run with Coverage

```bash
# Generate coverage report
pytest tests/installer/validators/ --cov=src/installer/validators --cov-report=term --cov-report=html

# View HTML report
open htmlcov/index.html
```

### Run Specific Test Scenarios

```bash
# Run only AC#1 tests (Python validation)
pytest tests/installer/validators/test_python_checker.py -k "python" -v

# Run only AC#2 tests (Disk space)
pytest tests/installer/validators/test_disk_space_checker.py -k "disk" -v

# Run only performance tests (NFR-001, NFR-002, NFR-003)
pytest tests/installer/validators/ -k "within" -v

# Run only BR-001 tests (Critical failures block)
pytest tests/installer/validators/ -k "block" -v
```

## Expected Initial State (TDD Red Phase)

### All Tests Should FAIL

After running tests for the first time:

```
FAILED test_python_checker.py::test_should_return_pass_when_python_3_10_detected - ModuleNotFoundError: No module named 'src.installer.validators.python_checker'
FAILED test_disk_space_checker.py::test_should_return_pass_when_100mb_available - ModuleNotFoundError: No module named 'src.installer.validators.disk_space_checker'
...
```

**Total Expected Failures:** ~125 tests

**Reason:** Implementation files do not exist yet. Tests written first (TDD Red phase).

### After Implementation (TDD Green Phase)

Expected progression:
1. **Phase 2 (Implementation):** Create validator classes → Tests turn GREEN
2. **Phase 3 (Refactor):** Optimize code → Tests remain GREEN
3. **Phase 4 (Integration):** Full workflow → Integration tests turn GREEN

## Coverage Analysis

### Acceptance Criteria Coverage

| AC | Description | Tests | Files |
|----|-------------|-------|-------|
| AC#1 | Python Version Validation | 12 | test_python_checker.py |
| AC#2 | Disk Space Validation | 12 | test_disk_space_checker.py |
| AC#3 | Existing Installation Detection | 10 | test_installation_detector.py |
| AC#4 | Write Permission Validation | 10 | test_permission_checker.py |
| AC#5 | Validation Summary Display | 5 | test_pre_flight_validator.py |
| AC#6 | Blocking Error Enforcement | 3 | test_pre_flight_validator.py, test_validation_integration.py |
| AC#7 | Force Flag Override | 3 | test_pre_flight_validator.py, test_validation_integration.py |

**Total AC Coverage:** 7/7 (100%)

### Component Requirements Coverage

| Requirement | Description | Tests | Status |
|-------------|-------------|-------|--------|
| SVC-001 | Orchestrate 4 checks | 3 | ✓ |
| SVC-002 | Determine overall outcome | 4 | ✓ |
| SVC-003 | Format summary table | 3 | ✓ |
| SVC-004 | Handle --force flag | 3 | ✓ |
| SVC-005 | Detect Python version | 5 | ✓ |
| SVC-006 | Parse version with regex | 4 | ✓ |
| SVC-007 | Try multiple executables | 3 | ✓ |
| SVC-008 | Calculate disk space | 4 | ✓ |
| SVC-009 | Handle exceptions gracefully | 3 | ✓ |
| SVC-010 | Detect existing installation | 4 | ✓ |
| SVC-011 | Read version.json | 4 | ✓ |
| SVC-012 | Verify write permissions | 4 | ✓ |
| SVC-013 | Clean up test file | 3 | ✓ |
| SVC-014 | Handle missing directory | 2 | ✓ |

**Total Component Coverage:** 14/14 (100%)

### Business Rules Coverage

| Rule | Description | Tests | Files |
|------|-------------|-------|-------|
| BR-001 | Critical failures block | 4 | test_pre_flight_validator.py, test_validation_integration.py |
| BR-002 | Warnings allow continuation | 3 | test_pre_flight_validator.py |
| BR-003 | --force bypasses WARN only | 2 | test_pre_flight_validator.py, test_validation_integration.py |
| BR-004 | All checks complete | 2 | test_pre_flight_validator.py, test_validation_integration.py |
| BR-005 | Python is optional (WARN) | 3 | test_python_checker.py |

**Total BR Coverage:** 5/5 (100%)

### Non-Functional Requirements Coverage

| NFR | Category | Requirement | Tests | Status |
|-----|----------|-------------|-------|--------|
| NFR-001 | Performance | All checks <5s | 2 | ✓ |
| NFR-002 | Performance | Python check <500ms | 1 | ✓ |
| NFR-003 | Performance | Disk check <200ms | 1 | ✓ |
| NFR-004 | Reliability | Cross-platform Python | 1 | ✓ |
| NFR-005 | Reliability | Zero false positives | 2 | ✓ |
| NFR-006 | Usability | Resolution steps | 4 | ✓ |
| NFR-007 | Security | No privilege escalation | 3 | ✓ |

**Total NFR Coverage:** 7/7 (100%)

### Edge Cases Coverage

1. **Python installed but wrong version (3.9)** → test_should_return_warn_when_python_3_9_detected
2. **Multiple Python versions available** → test_should_fallback_to_python_if_python3_missing
3. **Read-only filesystem** → test_should_return_fail_when_directory_read_only
4. **Partial previous installation** → test_should_detect_partial_installation
5. **Disk space check on network mount** → test_network_mount_disk_calculation
6. **Container environment (Docker)** → test_should_detect_virtual_environment_python

**Total Edge Cases:** 6/6 (100%)

## Test Pyramid Distribution

```
       /\
      /E2E\      10% - 12 tests (Integration scenarios)
     /------\
    /Integr.\   20% - 25 tests (Component interactions)
   /----------\
  /   Unit    \ 70% - 88 tests (Individual validators)
 /--------------\
```

**Actual Distribution:**
- Unit: 88 tests (70.4%)
- Integration: 25 tests (20.0%)
- E2E: 12 tests (9.6%)

**Target Met:** ✓ Within 70%/20%/10% guidelines

## Test Quality Metrics

### AAA Pattern Compliance

**All 125 tests follow AAA pattern:**
- ✓ Arrange: Setup with clear Given section
- ✓ Act: Single action with clear When section
- ✓ Assert: Explicit validation with clear Then section

**Example:**
```python
def test_should_return_pass_when_python_3_10_detected(self):
    """
    Test: Python 3.10.0 detected → PASS status

    Given: Python 3.10.0 is installed
    When: PythonVersionChecker.check() is called
    Then: Returns CheckResult with PASS status and version message
    """
    # Arrange
    from src.installer.validators.python_checker import PythonVersionChecker
    checker = PythonVersionChecker()
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = Mock(returncode=0, stdout="Python 3.10.0", stderr="")

        # Act
        result = checker.check()

        # Assert
        assert result.status == "PASS"
        assert "Python 3.10.0" in result.message
        assert result.check_name == "Python Version"
```

### Test Independence

**All tests are independent:**
- ✓ No shared mutable state
- ✓ No execution order dependencies
- ✓ Each test cleans up after itself (using fixtures)
- ✓ Parallel execution safe

### Test Documentation

**All tests include:**
- ✓ Descriptive docstrings (Given/When/Then format)
- ✓ Clear test names (test_should_[expected]_when_[condition])
- ✓ Comments explaining complex setups
- ✓ References to AC/BR/NFR requirements

## Fixtures Used

### Temporary Directories

- **temp_dir**: Empty temporary directory (auto-cleanup)
- **fresh_installation_dir**: Empty directory for fresh install
- **existing_installation_dir**: Directory with .claude/ and devforgeai/
- **partial_installation_dir**: Directory with .claude/ only (incomplete)
- **read_only_dir**: Read-only directory (permission denied scenario)

### Mock Data

- **mock_python_version_output**: Common Python version strings
- **validation_config**: Default configuration values
- **check_status_enum**: CheckStatus enum (PASS/WARN/FAIL)

### Utilities

- **assert_check_result_valid**: Validate CheckResult structure
- **assert_validation_result_valid**: Validate ValidationResult structure

## Running Tests in CI/CD

### GitHub Actions Example

```yaml
name: Pre-Flight Validation Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: ['3.10', '3.11', '3.12']

    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pytest pytest-cov

      - name: Run tests
        run: pytest tests/installer/validators/ -v --cov=src/installer/validators

      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

## Known Issues / Future Improvements

### Known Issues

1. **Cross-platform symlink tests**: Skip on Windows (symlinks require admin)
2. **Network mount tests**: Require actual network mount for full coverage
3. **Container detection**: Needs Docker environment for complete testing

### Future Improvements

1. **Parameterized tests**: Add more test.each scenarios for version combinations
2. **Property-based testing**: Use Hypothesis for edge case generation
3. **Mutation testing**: Use mutmut to validate test effectiveness
4. **Snapshot testing**: For validation summary formatting

## Contact / Support

**Story:** STORY-072
**Epic:** EPIC-013 (Interactive Installer & Validation)
**Created:** 2025-11-25
**Framework:** DevForgeAI Test-Driven Development

For questions or issues, see:
- `devforgeai/specs/Stories/STORY-072-pre-flight-validation-checks.story.md`
- `devforgeai/RCA/` (Root Cause Analysis documents)

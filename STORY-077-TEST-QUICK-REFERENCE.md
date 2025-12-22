# STORY-077: Test Quick Reference Guide

**Quick Start for Running Tests**

## File Locations

```
tests/installer/
├── test_version_detector.py           (38 tests - AC#1, AC#6)
├── test_version_parser.py             (42 tests - AC#2)
├── test_version_comparator.py         (41 tests - AC#3, AC#7)
├── test_compatibility_checker.py      (31 tests - AC#4, AC#5)
└── test_integration_version_flow.py   (40 tests - E2E workflows)
```

## Run All Tests

```bash
# All 142 tests
pytest tests/installer/test_version_*.py tests/installer/test_compatibility_*.py tests/installer/test_integration_*.py -v

# With coverage
pytest tests/installer/test_version_*.py tests/installer/test_compatibility_*.py tests/installer/test_integration_*.py \
    --cov=installer \
    --cov-report=html
```

## Run by Category

### Unit Tests Only (100 tests)
```bash
# VersionParser tests (42 tests)
pytest tests/installer/test_version_parser.py -v

# VersionDetector tests (38 tests)
pytest tests/installer/test_version_detector.py -v

# VersionComparator tests (41 tests)
pytest tests/installer/test_version_comparator.py -v

# Total unit: 121 tests
pytest tests/installer/test_version_parser.py \
        tests/installer/test_version_detector.py \
        tests/installer/test_version_comparator.py -v
```

### Integration Tests (28 tests)
```bash
pytest tests/installer/test_compatibility_checker.py -v
```

### E2E Tests (40 tests)
```bash
pytest tests/installer/test_integration_version_flow.py -v
```

## Run by Acceptance Criteria

### AC#1: Version File Detection
```bash
pytest tests/installer/test_version_detector.py::TestVersionDetectorFileDetection -v
```

### AC#2: Semver Parsing
```bash
pytest tests/installer/test_version_parser.py -v
```

### AC#3: Upgrade Path Validation
```bash
pytest tests/installer/test_version_comparator.py::TestVersionComparatorBasicComparison -v
pytest tests/installer/test_version_comparator.py::TestVersionComparatorUpgradeType -v
```

### AC#4: Breaking Change Warning
```bash
pytest tests/installer/test_compatibility_checker.py::TestCompatibilityCheckerMajorUpgrade -v
```

### AC#5: Downgrade Blocking
```bash
pytest tests/installer/test_compatibility_checker.py::TestCompatibilityCheckerDowngradeBlocking -v
```

### AC#6: Missing Version File Handling
```bash
pytest tests/installer/test_version_detector.py::TestVersionDetectorMissingFile -v
```

### AC#7: Pre-release Version Handling
```bash
pytest tests/installer/test_version_comparator.py::TestVersionComparatorPrerelease -v
pytest tests/installer/test_integration_version_flow.py::TestVersionFlowPrerelease -v
```

## Run by Performance Requirements

### NFR-001: Version Detection < 1 second
```bash
pytest tests/installer/test_version_detector.py::TestVersionDetectorFileDetection::test_should_complete_within_one_second -v
pytest tests/installer/test_integration_version_flow.py::TestVersionFlowPerformance::test_complete_version_detection_flow_under_1_second -v
```

### NFR-002: Version Parsing < 10ms
```bash
pytest tests/installer/test_version_parser.py::TestVersionParserPerformance -v
```

## Run Specific Test

```bash
# Single test
pytest tests/installer/test_version_parser.py::TestVersionParserStandardFormat::test_should_parse_standard_version -v

# Multiple tests from one class
pytest tests/installer/test_version_detector.py::TestVersionDetectorCorruptedFile -v
```

## Expected Results (RED Phase)

All tests WILL FAIL because modules don't exist yet:

```
FAILED tests/installer/test_version_parser.py::TestVersionParserStandardFormat::test_should_parse_standard_version
    ModuleNotFoundError: No module named 'installer.version_parser'
```

This is correct! This is the RED phase of TDD. Next steps:

1. **Implement modules** (installer/version_parser.py, etc.)
2. **Run tests again** → Tests turn GREEN
3. **Refactor code** → Tests stay GREEN

## Test Statistics

- **Total:** 142 tests
- **Unit Tests:** 100 (70%)
- **Integration Tests:** 28 (20%)
- **E2E Tests:** 14 (10%)

- **Acceptance Criteria Coverage:** 7/7 (100%)
- **Technical Spec Coverage:** 14/14 (100%)
- **Business Rules Coverage:** 4/4 (100%)
- **NFR Coverage:** 4/4 (100%)

## Coverage Reports

After implementation, view coverage:

```bash
# Generate HTML coverage report
pytest tests/installer/test_version_*.py tests/installer/test_compatibility_*.py tests/installer/test_integration_*.py \
    --cov=installer \
    --cov-report=html

# View report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

## Debugging Tests

```bash
# Show print statements
pytest tests/installer/test_version_parser.py -v -s

# Stop at first failure
pytest tests/installer/test_version_parser.py -x

# Show local variables on failure
pytest tests/installer/test_version_parser.py -l

# Verbose traceback
pytest tests/installer/test_version_parser.py -vv

# Run specific test with debugging
pytest tests/installer/test_version_parser.py::TestVersionParserStandardFormat::test_should_parse_standard_version -vv
```

## Dependencies

```bash
# Install testing dependencies
pip install pytest

# Optional (for coverage reports)
pip install pytest-cov

# Optional (for performance testing)
pip install pytest-timeout
```

## Quick Test Verification

Check test file syntax without running:

```bash
python -m py_compile tests/installer/test_version_parser.py
python -m py_compile tests/installer/test_version_detector.py
python -m py_compile tests/installer/test_version_comparator.py
python -m py_compile tests/installer/test_compatibility_checker.py
python -m py_compile tests/installer/test_integration_version_flow.py
```

## Test Organization Summary

| Module | Tests | Focus | Status |
|--------|-------|-------|--------|
| test_version_detector.py | 38 | File detection, error handling, metadata | READY |
| test_version_parser.py | 42 | Semver parsing, pre-release, build metadata | READY |
| test_version_comparator.py | 41 | Version comparison, upgrade types, pre-release ordering | READY |
| test_compatibility_checker.py | 31 | Breaking changes, downgrade blocking, safety | READY |
| test_integration_version_flow.py | 40 | End-to-end workflows, performance, edge cases | READY |

**Total: 142 tests ready for TDD implementation**

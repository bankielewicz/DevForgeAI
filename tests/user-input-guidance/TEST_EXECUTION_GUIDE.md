# Test Execution Guide - STORY-059 Validation Test Suite

## Quick Start

Execute all tests (RED phase - all will fail):
```bash
pytest tests/user-input-guidance/ -v
```

Expected result: 118 failing tests (implementation not yet complete)

## Test Suite Overview

- **Total Tests**: 118 (comprehensive coverage)
- **Status**: RED Phase (TDD) - All tests fail until implementation complete
- **Coverage**: 5 acceptance criteria, 3 edge cases, 3 data validation rules, 3 NFR categories
- **Language**: Python (pytest framework)
- **Pattern**: AAA (Arrange-Act-Assert)

## Test Organization

```
tests/user-input-guidance/
├── __init__.py                  # Package marker
├── README.md                    # Test suite documentation
├── TEST_EXECUTION_GUIDE.md      # This file
├── test_infrastructure.py       # AC#1 - Directory structure (20 tests)
├── test_fixtures.py            # Fixture validation (12 tests)
├── test_scripts.py             # AC#2 - Script execution (19 tests)
├── test_measurements.py        # AC#3 & AC#4 - Metrics (23 tests)
├── test_impact_report.py       # AC#5 - Report generation (26 tests)
└── test_edge_cases.py          # Edge cases & DVR (18 tests)
```

## Test Execution Commands

### Run All Tests
```bash
# Basic execution
pytest tests/user-input-guidance/ -v

# With detailed output
pytest tests/user-input-guidance/ -vv

# With output buffering disabled (see print statements)
pytest tests/user-input-guidance/ -v -s

# Generate HTML report
pytest tests/user-input-guidance/ -v --html=tests/user-input-guidance/report.html
```

### Run by Test Module

```bash
# AC#1 - Infrastructure tests
pytest tests/user-input-guidance/test_infrastructure.py -v

# Fixture validation
pytest tests/user-input-guidance/test_fixtures.py -v

# AC#2 - Script execution
pytest tests/user-input-guidance/test_scripts.py -v

# AC#3 & AC#4 - Measurement scripts
pytest tests/user-input-guidance/test_measurements.py -v

# AC#5 - Impact report
pytest tests/user-input-guidance/test_impact_report.py -v

# Edge cases and data validation
pytest tests/user-input-guidance/test_edge_cases.py -v
```

### Run by Test Class

```bash
# Infrastructure directory tests
pytest tests/user-input-guidance/test_infrastructure.py::TestDirectoryStructure -v

# Baseline fixture tests
pytest tests/user-input-guidance/test_infrastructure.py::TestBaselineFixtures -v

# Enhanced fixture tests
pytest tests/user-input-guidance/test_infrastructure.py::TestEnhancedFixtures -v

# Fixture pair matching (DVR1)
pytest tests/user-input-guidance/test_edge_cases.py::TestDVR1FixturePairCompleteness -v

# Token savings measurements
pytest tests/user-input-guidance/test_measurements.py::TestTokenSavingsReportGeneration -v

# Success rate measurements
pytest tests/user-input-guidance/test_measurements.py::TestSuccessRateReportGeneration -v

# Impact report sections
pytest tests/user-input-guidance/test_impact_report.py::TestImpactReportExecutiveSummary -v
```

### Run Specific Tests

```bash
# Single test
pytest tests/user-input-guidance/test_infrastructure.py::TestDirectoryStructure::test_should_have_tests_user_input_guidance_directory -v

# Pattern matching
pytest tests/user-input-guidance/ -k "should_have" -v
pytest tests/user-input-guidance/ -k "fixture" -v
pytest tests/user-input-guidance/ -k "script" -v
```

### Pytest Options

```bash
# Stop on first failure
pytest tests/user-input-guidance/ -v -x

# Show last N test summaries
pytest tests/user-input-guidance/ -v --tb=short

# Exit with code on failure count
pytest tests/user-input-guidance/ -v --maxfail=5

# Quiet mode (summary only)
pytest tests/user-input-guidance/ -q

# Show test durations (slowest first)
pytest tests/user-input-guidance/ -v --durations=10

# Run only failed tests from last run
pytest tests/user-input-guidance/ --lf -v

# Run failed tests first, then others
pytest tests/user-input-guidance/ --ff -v
```

## Expected Output (RED Phase)

### Initial Run - All Tests Fail
```
tests/user-input-guidance/test_infrastructure.py::TestDirectoryStructure::test_should_have_tests_user_input_guidance_directory FAILED
tests/user-input-guidance/test_infrastructure.py::TestDirectoryStructure::test_should_have_fixtures_directory_structure FAILED
tests/user-input-guidance/test_infrastructure.py::TestDirectoryStructure::test_should_have_scripts_directory FAILED
...
tests/user-input-guidance/test_edge_cases.py::TestDVR3StatisticalSignificance::test_should_use_paired_t_test_for_token_savings FAILED

======================== 118 failed in X.XXs ========================
```

### Expected Failure Messages

**AC#1 - Infrastructure**
```
AssertionError: Directory not found: /mnt/c/Projects/DevForgeAI2/tests/user-input-guidance
AssertionError: Baseline fixtures directory not found: .../fixtures/baseline
AssertionError: Expected 10 baseline fixtures, found 0
```

**AC#2 - Script Execution**
```
AssertionError: Baseline test script not found: .../test-story-creation-without-guidance.sh
AssertionError: baseline-results.json is not valid JSON
AssertionError: Expected 10 baseline results, found 0
```

**AC#3 & AC#4 - Measurements**
```
AssertionError: Token savings report not found: .../token-savings-report.md
AssertionError: Success rate report not found: .../success-rate-report.md
AssertionError: Expected 10 baseline results, found 0
```

**AC#5 - Impact Report**
```
AssertionError: Impact report not found: .../USER-INPUT-GUIDANCE-IMPACT-REPORT.md
AssertionError: Impact report missing executive summary section
AssertionError: Impact report missing statistical analysis section
```

## Test Progress Tracking

As implementation progresses, tests will transition from RED to GREEN:

### Phase 1: Infrastructure (Tests 1-32)
When directory structure and fixtures are created:
```bash
pytest tests/user-input-guidance/test_infrastructure.py -v
pytest tests/user-input-guidance/test_fixtures.py -v
# Expected: ~32 tests pass
```

### Phase 2: Script Creation (Tests 33-51)
When test scripts exist and generate output:
```bash
pytest tests/user-input-guidance/test_scripts.py -v
# Expected: ~19 tests pass
```

### Phase 3: Measurement Scripts (Tests 52-74)
When measurement scripts and reports are generated:
```bash
pytest tests/user-input-guidance/test_measurements.py -v
# Expected: ~23 tests pass
```

### Phase 4: Impact Report (Tests 75-100)
When consolidated impact report is created:
```bash
pytest tests/user-input-guidance/test_impact_report.py -v
# Expected: ~26 tests pass
```

### Phase 5: Edge Cases (Tests 101-118)
When all requirements are met with edge case handling:
```bash
pytest tests/user-input-guidance/test_edge_cases.py -v
# Expected: ~18 tests pass
```

### Final State: All GREEN
```bash
pytest tests/user-input-guidance/ -v
# Expected: 118 passed in X.XXs
```

## Requirements-to-Tests Mapping

### Acceptance Criteria Coverage

| AC | Description | Test Module | Tests | Status |
|----|-------------|------------|-------|--------|
| AC#1 | Test Infrastructure | test_infrastructure, test_fixtures | 32 | ✓ |
| AC#2 | Story Creation Validation | test_scripts | 19 | ✓ |
| AC#3 | Token Savings Measurement | test_measurements, test_impact_report | 12 | ✓ |
| AC#4 | Success Rate Measurement | test_measurements, test_impact_report | 13 | ✓ |
| AC#5 | Impact Report Generation | test_impact_report | 26 | ✓ |

### Edge Cases Coverage

| Edge Case | Description | Tests | Status |
|-----------|-------------|-------|--------|
| EC#1 | Fixture Quality Variation | 3 | ✓ |
| EC#2 | Token Counting Methodology | 3 | ✓ |
| EC#3 | Non-Deterministic Generation | 4 | ✓ |

### Data Validation Rules Coverage

| DVR | Description | Tests | Status |
|-----|-------------|-------|--------|
| DVR1 | Fixture Pair Completeness | 2 | ✓ |
| DVR2 | Results JSON Schema | 3 | ✓ |
| DVR3 | Statistical Significance | 3 | ✓ |

### Non-Functional Requirements Coverage

| NFR | Description | Tests | Status |
|-----|-------------|-------|--------|
| NFR-PERF-001 | Performance (<60 min) | 1 | ✓ |
| NFR-REL-001 | Reliability (error handling) | 2 | ✓ |
| NFR-MAINT-001 | Maintainability (stdlib) | 3 | ✓ |

## Test Naming Convention

All tests follow the format: `test_should_[expected]_when_[condition]`

**Examples:**
- `test_should_have_tests_user_input_guidance_directory` → Checks directory exists
- `test_should_validate_baseline_fixtures_not_empty` → Checks content non-empty
- `test_should_have_10_baseline_fixtures` → Checks quantity
- `test_should_generate_token_savings_report_markdown` → Checks report generation
- `test_should_flag_non_significant_results` → Checks validation logic

## Test Structure Pattern (AAA)

Every test follows Arrange-Act-Assert pattern:

```python
def test_should_do_something():
    # ARRANGE: Set up test data and conditions
    test_file = Path("/path/to/expected/file.txt")
    expected_value = 10

    # ACT: Execute the behavior being tested
    file_exists = test_file.exists()
    actual_value = len([...])

    # ASSERT: Verify the outcome
    assert file_exists, f"File not found: {test_file}"
    assert actual_value == expected_value, f"Expected {expected_value}, got {actual_value}"
```

## Troubleshooting

### Tests Not Found
```bash
# Verify pytest can discover tests
pytest tests/user-input-guidance/ --collect-only

# Check Python path
export PYTHONPATH=/mnt/c/Projects/DevForgeAI2:$PYTHONPATH
pytest tests/user-input-guidance/ -v
```

### Import Errors
```bash
# Verify package structure
ls -la tests/user-input-guidance/__init__.py

# Test import directly
python3 -c "from tests.user_input_guidance import test_infrastructure; print('Import successful')"
```

### Pytest Version Issues
```bash
# Check installed version
pytest --version

# Upgrade pytest
pip install --upgrade pytest

# Verify compatibility
python3 -m pytest tests/user-input-guidance/ --version
```

### File Path Issues
```bash
# Verify working directory
pwd  # Should be /mnt/c/Projects/DevForgeAI2

# Check absolute paths in tests
grep -r "Path(" tests/user-input-guidance/test_*.py | head -5
```

## Integration with CI/CD

### GitHub Actions Example
```yaml
name: Run STORY-059 Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.8'
      - run: pip install pytest
      - run: pytest tests/user-input-guidance/ -v --tb=short
```

### Jenkins Example
```groovy
pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                sh '''
                    python3 -m pip install pytest
                    python3 -m pytest tests/user-input-guidance/ -v
                '''
            }
        }
    }
}
```

## Performance Expectations

### Test Execution Times
- **Total Suite**: ~10-30 seconds (all tests are file/content checks, no API calls)
- **Per Module**: ~1-5 seconds
- **Per Test**: ~10-50ms

### System Requirements
- Python 3.8+
- pytest (any recent version)
- No external dependencies
- <100MB disk space

## Next Steps (Implementation)

Once implementation begins:

1. **Create fixtures** → test_infrastructure & test_fixtures pass
2. **Create scripts** → test_scripts passes
3. **Run scripts to generate results** → test_measurements passes
4. **Generate reports** → test_impact_report passes
5. **Validate edge cases** → test_edge_cases passes

When all 118 tests pass: STORY-059 is complete (GREEN phase).

## See Also

- [Test Suite README](./README.md) - Detailed test documentation
- [STORY-059](../../devforgeai/specs/Stories/STORY-059-user-input-guidance-validation.story.md) - Full story spec
- [Test-Automator Documentation](./.claude/skills/test-automator/SKILL.md) - Test generation framework

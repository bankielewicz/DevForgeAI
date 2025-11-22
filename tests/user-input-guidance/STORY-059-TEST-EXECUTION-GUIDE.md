# STORY-059 Test Execution Guide - User Input Guidance Validation & Testing Suite

**Document Version**: 1.0
**Created**: 2025-11-22
**Test Suite Status**: TDD Red Phase (All tests should FAIL before implementation)
**Total Tests**: 108 tests across 3 files

---

## Quick Start

### Run All Tests (Complete Test Suite)

```bash
cd /mnt/c/Projects/DevForgeAI2

# Run all STORY-059 tests
pytest tests/user-input-guidance/test_fixture_structure.py \
        tests/user-input-guidance/test_measurement_scripts.py \
        tests/user-input-guidance/test_edge_cases_and_nfrs.py -v

# Expected Result (RED phase): All 108 tests FAIL
```

### Run Tests by Category

```bash
# Fixture structure tests (AC#1-4) - 30 tests
pytest tests/user-input-guidance/test_fixture_structure.py -v

# Measurement scripts tests (AC#5-8) - 36 tests
pytest tests/user-input-guidance/test_measurement_scripts.py -v

# Edge cases and NFRs - 42 tests
pytest tests/user-input-guidance/test_edge_cases_and_nfrs.py -v
```

### Run Tests by Acceptance Criteria

```bash
# AC#1: Directory Structure (12 tests)
pytest tests/user-input-guidance/test_fixture_structure.py::TestDirectoryStructureCreated -v

# AC#2: Baseline Fixtures (9 tests)
pytest tests/user-input-guidance/test_fixture_structure.py::TestBaselineFixturesStructure -v

# AC#3: Enhanced Fixtures (6 tests)
pytest tests/user-input-guidance/test_fixture_structure.py::TestEnhancedFixturesStructure -v

# AC#4: Expected Improvements (5 tests)
pytest tests/user-input-guidance/test_fixture_structure.py::TestExpectedImprovementsStructure -v

# AC#5: Token Savings Script (9 tests)
pytest tests/user-input-guidance/test_measurement_scripts.py::TestTokenSavingsScript -v

# AC#6: Success Rate Script (7 tests)
pytest tests/user-input-guidance/test_measurement_scripts.py::TestSuccessRateScript -v

# AC#7: Impact Report Script (6 tests)
pytest tests/user-input-guidance/test_measurement_scripts.py::TestImpactReportScript -v

# AC#8: Fixture Validation Script (7 tests)
pytest tests/user-input-guidance/test_measurement_scripts.py::TestFixtureValidationScript -v
```

---

## Test Files Overview

### File 1: test_fixture_structure.py (30 tests)

**Purpose**: Validates directory structure, fixture files, and metadata

**What's Tested**:
- tests/user-input-guidance/ directory hierarchy exists
- File/directory permissions correct (755 dirs, 644 files)
- README.md documentation complete
- 10 baseline fixtures with proper naming and word counts
- 10 enhanced fixtures with improved quality
- 10 expected improvement JSON files with valid schema

**Test Classes**:
1. `TestDirectoryStructureCreated` (12 tests) - Directory structure, permissions, README
2. `TestBaselineFixturesStructure` (9 tests) - 10 baseline fixtures, naming, content quality
3. `TestEnhancedFixturesStructure` (6 tests) - 10 enhanced fixtures, length, guidance
4. `TestExpectedImprovementsStructure` (5 tests) - 10 JSON files, schema, numeric ranges

**Acceptance Criteria Covered**:
- AC#1: Test Directory Structure Created (12 items)
- AC#2: Baseline Test Fixtures Created (13 items)
- AC#3: Enhanced Test Fixtures Created (6 items)
- AC#4: Expected Improvements Documented (5 items)

**Dependencies**: None (tests don't require external libraries)

**Expected in RED phase**: All 30 tests FAIL (fixtures don't exist)

---

### File 2: test_measurement_scripts.py (36 tests)

**Purpose**: Validates measurement scripts and their functionality

**What's Tested**:
- measure-token-savings.py functionality
  - Uses tiktoken cl100k_base encoding
  - Processes 10 baseline/enhanced pairs
  - Generates JSON report with timestamp
  - Calculates aggregate statistics
  - Exits correctly based on 20% threshold
  - Outputs clear success/failure messages

- measure-success-rate.py functionality
  - Analyzes AC testability (Given/When/Then %)
  - Calculates NFR coverage (4 categories)
  - Measures specificity (vague term reduction %)
  - Exits correctly based on 80% threshold
  - Loads expected improvements from JSON

- generate-impact-report.py functionality
  - Loads most recent measurement reports
  - Generates 5 required Markdown sections
  - Includes ASCII visualizations
  - Contains actionable recommendations

- validate-fixtures.py functionality
  - Validates all 30 fixtures
  - Checks baseline word counts, quality issues
  - Checks enhanced length increase, readability
  - Validates expected JSON schema
  - Generates validation report
  - Exits with correct codes (0/1/2)

**Test Classes**:
1. `TestTokenSavingsScript` (9 tests) - Token savings measurement
2. `TestSuccessRateScript` (7 tests) - Success rate measurement
3. `TestImpactReportScript` (6 tests) - Impact report generation
4. `TestFixtureValidationScript` (7 tests) - Fixture validation
5. `TestScriptHelp` (4 tests) - --help flag support
6. `TestScriptUsesLogging` (4 tests) - Logging module usage
7. `TestScriptConfigurableThresholds` (2 tests) - Constants in headers

**Acceptance Criteria Covered**:
- AC#5: Token Savings Measurement Script Functional (9 items)
- AC#6: Success Rate Measurement Script Functional (5 items)
- AC#7: Impact Report Generation Script Functional (6 items)
- AC#8: Fixture Quality Validation Script Functional (7 items)

**Dependencies**:
- tiktoken (for token savings script)
- textstat (optional, for readability checks)

**Expected in RED phase**: All 36 tests FAIL (scripts don't exist)

---

### File 3: test_edge_cases_and_nfrs.py (42 tests)

**Purpose**: Validates edge case handling and non-functional requirements

**What's Tested**:

**Edge Cases**:
1. Tokenization version mismatch (3 tests)
   - Version mismatch detection
   - Graceful handling (warning, not fatal)
   - Disclaimer in JSON report

2. Fixture pairs mismatch (4 tests)
   - Incomplete pair detection
   - Exit code 2 for incomplete pairs
   - Skipped pair warnings
   - Incomplete count in report

3. Expected values too strict/lenient (3 tests)
   - Outlier detection (>20% delta)
   - Recommendations for recalibration
   - Flagging 3+ outlier fixtures

4. Flesch readability unavailable (3 tests)
   - textstat library checking
   - Graceful skip if unavailable
   - Continue with other checks

5. Missing input reports (4 tests)
   - Input report existence checking
   - Exit code 5 for missing reports
   - Guidance on required steps
   - Most recent selection by timestamp

6. Filename format violations (4 tests)
   - Regex-based validation
   - Zero-padded number detection
   - Invalid character detection
   - Remediation guidance

7. Empty or corrupt fixtures (4 tests)
   - Empty file detection
   - UTF-8 encoding validation
   - Whitespace-only detection
   - Specific error messages

8. JSON schema violations (3 tests)
   - JSON syntax validation
   - Required fields checking
   - Numeric range validation

**Non-Functional Requirements**:
- Performance (4 tests)
  - validate-fixtures <5 seconds
  - measure-token-savings <3 seconds
  - measure-success-rate <10 seconds
  - generate-impact-report <2 seconds

- Reliability (4 tests)
  - Pair integrity enforcement
  - Missing library handling
  - Empty fixture handling
  - Missing report handling

- Maintainability (3 tests)
  - Independent script execution
  - Impact report dependencies
  - Threshold constants in headers

- Quality (4 tests)
  - Explicit token threshold (20%)
  - Explicit success threshold (80%)
  - 10 distinct fixture domains
  - Specific recommendations format

- Testability (3 tests)
  - --test flag support
  - Exit code documentation

- Usability (3 tests)
  - --help flag support
  - README.md ≥300 lines
  - Required sections in README
  - Troubleshooting coverage

**Test Classes**:
1. `TestEdgeCaseTokenizationVersionMismatch` (3 tests)
2. `TestEdgeCaseFixturePairsMismatch` (4 tests)
3. `TestEdgeCaseExpectedValuesStrictOrLenient` (3 tests)
4. `TestEdgeCaseFleschReadabilityUnavailable` (3 tests)
5. `TestEdgeCaseReportGenerationMissingInputs` (4 tests)
6. `TestEdgeCaseFixtureFilenameViolations` (4 tests)
7. `TestEdgeCaseEmptyOrCorruptFixtures` (4 tests)
8. `TestEdgeCaseJSONSchemaViolations` (3 tests)
9. `TestPerformanceRequirements` (4 tests)
10. `TestReliabilityRequirements` (4 tests)
11. `TestMaintainabilityRequirements` (3 tests)
12. `TestQualityRequirements` (4 tests)
13. `TestTestabilityRequirements` (3 tests)
14. `TestUsabilityRequirements` (3 tests)

**Story Requirements Covered**:
- All 8 Edge Cases from Technical Specification
- All 18 Non-Functional Requirements

**Expected in RED phase**: Most tests FAIL (edge cases and features not implemented)

---

## Test Execution Workflow

### Step 1: Install Dependencies

```bash
# Core testing
pip install pytest pytest-cov

# Optional but recommended (for measurement scripts)
pip install tiktoken textstat
```

### Step 2: Run All Tests to See Failures (RED Phase)

```bash
cd /mnt/c/Projects/DevForgeAI2

# Run complete test suite
pytest tests/user-input-guidance/test_*.py -v

# Expected: 108 FAILED (all tests failing - this is correct for TDD Red)
```

### Step 3: Implement Features Incrementally (GREEN Phase)

#### 3.1 Create Directory Structure (AC#1)

```bash
# Implement directory structure and README.md
# Then run:
pytest tests/user-input-guidance/test_fixture_structure.py::TestDirectoryStructureCreated -v
# Expected: 12 PASSED
```

#### 3.2 Create Baseline Fixtures (AC#2)

```bash
# Create 10 baseline fixture files with quality issues
# Then run:
pytest tests/user-input-guidance/test_fixture_structure.py::TestBaselineFixturesStructure -v
# Expected: 9 PASSED
```

#### 3.3 Create Enhanced Fixtures (AC#3)

```bash
# Create 10 enhanced fixture files with improvements
# Then run:
pytest tests/user-input-guidance/test_fixture_structure.py::TestEnhancedFixturesStructure -v
# Expected: 6 PASSED
```

#### 3.4 Create Expected Improvements JSON (AC#4)

```bash
# Create 10 expected JSON files with improvement targets
# Then run:
pytest tests/user-input-guidance/test_fixture_structure.py::TestExpectedImprovementsStructure -v
# Expected: 5 PASSED
```

#### 3.5 Implement Measurement Scripts (AC#5-8)

```bash
# Implement all 4 scripts:
# - measure-token-savings.py
# - measure-success-rate.py
# - generate-impact-report.py
# - validate-fixtures.py
# Then run:
pytest tests/user-input-guidance/test_measurement_scripts.py -v
# Expected: 36 PASSED
```

#### 3.6 Add Edge Case Handling (Edge Cases 1-8)

```bash
# Implement error handling for all 8 edge cases
# Then run:
pytest tests/user-input-guidance/test_edge_cases_and_nfrs.py::TestEdgeCaseTokenizationVersionMismatch -v
pytest tests/user-input-guidance/test_edge_cases_and_nfrs.py::TestEdgeCaseFixturePairsMismatch -v
# ... etc for all edge cases
```

#### 3.7 Ensure NFR Compliance (NFR-001 to NFR-018)

```bash
# Implement performance optimizations, logging, help text, README
# Then run:
pytest tests/user-input-guidance/test_edge_cases_and_nfrs.py::TestPerformanceRequirements -v
pytest tests/user-input-guidance/test_edge_cases_and_nfrs.py::TestUsabilityRequirements -v
# ... etc for all NFR tests
```

### Step 4: Run Full Test Suite (All GREEN)

```bash
pytest tests/user-input-guidance/test_*.py -v
# Expected: 108 PASSED
```

---

## Interpreting Test Results

### RED Phase (Expected Initially)

```
FAILED test_fixture_structure.py::TestDirectoryStructureCreated::test_fixture_root_directory_exists
FAILED test_fixture_structure.py::TestBaselineFixturesStructure::test_10_baseline_fixtures_exist
... [more failures]

===== 108 failed in 0.45s =====
```

**This is CORRECT for TDD Red phase.** All tests fail because implementation doesn't exist yet.

### GREEN Phase (After Implementation)

```
PASSED test_fixture_structure.py::TestDirectoryStructureCreated::test_fixture_root_directory_exists
PASSED test_fixture_structure.py::TestBaselineFixturesStructure::test_10_baseline_fixtures_exist
... [more passes]

===== 108 passed in 2.15s =====
```

**This is CORRECT for TDD Green phase.** All tests pass after implementation.

### Partial Progress

```
PASSED test_fixture_structure.py::TestDirectoryStructureCreated (12 tests)
PASSED test_fixture_structure.py::TestBaselineFixturesStructure (9 tests)
FAILED test_fixture_structure.py::TestEnhancedFixturesStructure (6 tests)
... [other failures]

===== 27 passed, 81 failed in 1.23s =====
```

**This is CORRECT during implementation.** Some features done, others not yet.

---

## Test Coverage Summary

### Acceptance Criteria Coverage

| AC | Item Count | Test Count | Coverage |
|-------|-----------|-----------|----------|
| AC#1: Directory Structure | 12 | 12 | 100% |
| AC#2: Baseline Fixtures | 13 | 9 | 69% (covers main items) |
| AC#3: Enhanced Fixtures | 6 | 6 | 100% |
| AC#4: Expected Improvements | 5 | 5 | 100% |
| AC#5: Token Savings Script | 9 | 9 | 100% |
| AC#6: Success Rate Script | 5 | 7 | 100% |
| AC#7: Impact Report Script | 6 | 6 | 100% |
| AC#8: Fixture Validation | 7 | 7 | 100% |
| **TOTAL** | **63** | **61** | **97%** |

### NFR Coverage

18 Non-Functional Requirements covered by 25+ tests across multiple test classes

### Edge Case Coverage

8 Edge Cases covered by 28 tests with specific validation for each scenario

---

## Running Tests with Additional Options

### Verbose Output

```bash
pytest tests/user-input-guidance/test_*.py -v
```

Shows all test names and results

### Quiet Output

```bash
pytest tests/user-input-guidance/test_*.py -q
```

Shows only summary

### Stop on First Failure

```bash
pytest tests/user-input-guidance/test_*.py -x
```

Useful for debugging - stops after first failure

### Show Print Statements

```bash
pytest tests/user-input-guidance/test_*.py -s
```

Shows all print output (usually suppressed)

### Run Specific Test

```bash
pytest tests/user-input-guidance/test_fixture_structure.py::TestDirectoryStructureCreated::test_fixture_root_directory_exists -v
```

Run a single test

### Generate Coverage Report

```bash
pytest tests/user-input-guidance/test_*.py --cov=tests/user-input-guidance --cov-report=html
open htmlcov/index.html
```

HTML coverage report

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'pytest'"

**Solution**:
```bash
pip install pytest
```

### Issue: "No tests found"

**Solution**: Ensure you're in the project root:
```bash
cd /mnt/c/Projects/DevForgeAI2
```

### Issue: Tests fail but shouldn't (before implementation)

**Problem**: Misconfigured test

**Solution**: Review test assertion - it should fail when implementation doesn't exist

### Issue: Tests pass but implementation not done

**Problem**: Test too lenient

**Solution**: Make assertion more specific:
```python
# Too lenient - might pass by accident
assert "tiktoken" in content or "library" in content

# Better - specific requirement
assert "tiktoken" in content and "cl100k_base" in content
```

---

## Implementation Checklist

Use this checklist to track implementation progress:

### Fixtures and Documentation
- [ ] Create tests/user-input-guidance/ directory structure
- [ ] Set permissions (755 dirs, 644 files)
- [ ] Create comprehensive README.md (≥300 lines)
- [ ] Create 10 baseline fixtures (50-200 words, 2-4 issues each)
- [ ] Create 10 enhanced fixtures (30-60% longer, ≥3 guidance principles)
- [ ] Create 10 expected JSON files (valid schema, 0-100% numeric ranges)

### Measurement Scripts
- [ ] Implement measure-token-savings.py
  - [ ] Use tiktoken cl100k_base encoding
  - [ ] Process 10 fixture pairs
  - [ ] Generate JSON with timestamp
  - [ ] Calculate statistics (mean, median, std_dev, min, max)
  - [ ] Exit 0 if ≥20% savings, 1 otherwise
  - [ ] Output success/failure message

- [ ] Implement measure-success-rate.py
  - [ ] Analyze AC testability (Given/When/Then %)
  - [ ] Calculate NFR coverage (4 categories)
  - [ ] Measure specificity (vague term reduction %)
  - [ ] Load expected improvements from JSON
  - [ ] Exit 0 if ≥8/10 fixtures meet expectations, 1 otherwise
  - [ ] Output per-fixture pass/fail with details

- [ ] Implement generate-impact-report.py
  - [ ] Load most recent token-savings and success-rate reports
  - [ ] Generate 5 required Markdown sections
  - [ ] Include ASCII visualizations (Unicode tables, bar charts)
  - [ ] Create actionable recommendations
  - [ ] Exit 5 if input reports missing

- [ ] Implement validate-fixtures.py
  - [ ] Validate all 30 fixtures (baseline, enhanced, expected)
  - [ ] Check baseline word counts (50-200)
  - [ ] Check enhanced length increase (30-60%)
  - [ ] Validate expected JSON schema
  - [ ] Generate validation report (JSON)
  - [ ] Exit 0 (success), 1 (validation failed), 2 (incomplete pairs)

### Features and NFRs
- [ ] Add --help flag support to all 4 scripts
- [ ] Use logging module instead of print statements
- [ ] Define all thresholds as constants in script headers
- [ ] Implement all 8 edge case handlers
- [ ] Optimize performance to meet targets:
  - [ ] validate-fixtures <5 seconds
  - [ ] measure-token-savings <3 seconds
  - [ ] measure-success-rate <10 seconds
  - [ ] generate-impact-report <2 seconds
- [ ] Add --test flag for self-validation
- [ ] Document exit codes in --help and README

---

## Next Steps

1. **Review this guide** - Understand test structure
2. **Run tests** - `pytest tests/user-input-guidance/test_*.py -v` (expect RED)
3. **Implement STORY-059** - Follow acceptance criteria and implementation checklist
4. **Run tests incrementally** - Watch them turn GREEN as features are implemented
5. **Refactor** - Improve code quality while keeping tests GREEN

---

**Test Suite Status**: ✅ Complete and Ready for TDD Red → Green → Refactor

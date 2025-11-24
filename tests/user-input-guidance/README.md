# User Input Guidance Validation Test Suite

Comprehensive test suite for validating the User Input Guidance System's effectiveness through real story creation workflows.

## Test Organization

### 1. Infrastructure Tests (`test_infrastructure.py`)
**AC#1 Coverage**: Tests for test infrastructure establishment

- Directory structure validation (tests/user-input-guidance/)
- Baseline and enhanced fixture existence (10 pairs each)
- Fixture naming convention and sequencing
- Fixture content validation (UTF-8 encoding, size constraints 100-2000 chars)
- Fixture metadata file (fixture-metadata.json)
- Complexity stratification (3 Simple, 4 Medium, 3 Complex)
- Measurement script existence (validate-token-savings.py, measure-success-rate.py)

**Total Tests**: 21

### 2. Fixture Validation Tests (`test_fixtures.py`)
**Supports AC#1, AC#2**: Tests for fixture quality and pairing

- Fixture content validation (non-empty, no placeholders)
- Baseline and enhanced fixture distinctness
- Meaningful enhanced content differences (≥10% length increase)
- Complexity classification accuracy
- Fixture metadata structure and completeness
- Fixture pair matching (DVR1)

**Total Tests**: 11

### 3. Script Execution Tests (`test_scripts.py`)
**AC#2 Coverage**: Tests for story creation script execution

- Script structure and content validation
- Bash shebang verification
- Help flag support (--help, -h)
- Dry-run flag support (--dry-run)
- JSON output structure validation
- Required fields in results JSON (story_id, fixture_name, token_usage, ac_count, nfr_present, incomplete, iterations)
- 10 results per script (baseline and enhanced)
- Token usage metrics capture
- Iteration cycle metrics capture
- AC count metrics capture
- NFR presence flag validation
- Multiple runs per fixture (3 runs per fixture)

**Total Tests**: 15

### 4. Measurement Script Tests (`test_measurements.py`)
**AC#3 and AC#4 Coverage**: Tests for measurement script functionality

#### Token Savings Script (validate-token-savings.py)
- Script existence and content validation
- Help documentation
- Statistical function presence (t-test, scipy, statistics)
- Token savings report generation
- Savings percentage documentation (target ≥9%)
- Statistical significance reporting (p-value <0.05)
- Confidence level documentation
- Token savings chart generation (PNG visualization)

#### Success Rate Script (measure-success-rate.py)
- Script existence and content validation
- Help documentation
- Completeness scoring function
- Success rate report generation
- Baseline incomplete rate documentation (~40%)
- Enhanced incomplete rate documentation (≤13%)
- Reduction percentage documentation (≥67%)
- Iteration metrics documentation (baseline ~2.5, enhanced ≤1.2)
- Per-fixture breakdown in report

#### Dependency Management (NFR-MAINT-001)
- stdlib-only core functionality verification
- matplotlib/scipy as optional visualization

**Total Tests**: 16

### 5. Impact Report Tests (`test_impact_report.py`)
**AC#5 and NFR Coverage**: Tests for consolidated impact report

#### Report Structure
- Report file existence (.devforgeai/specs/enhancements/USER-INPUT-GUIDANCE-IMPACT-REPORT.md)
- Substantial content validation (>1000 characters)

#### Required Sections
- **Executive Summary** (≤500 words with headline metrics)
- **Findings by Business Goal** (incomplete rate, token efficiency, iteration cycles)
- **Evidence Tables** (10 test fixtures with before/after metrics)
- **Statistical Analysis** (confidence intervals, significance testing)
- **Recommendations** (3-5 actionable next steps)
- **Limitations** (sample size, fixture selection bias acknowledgment)
- **Appendix** (raw data tables for reproducibility)

#### Non-Functional Requirements
- **NFR-PERF-001**: Performance documentation (<60 minutes total)
- **NFR-REL-001**: Error handling for partial failures + clear error messages
- **NFR-MAINT-001**: stdlib-only core + simple text fixtures + JSON outputs

**Total Tests**: 23

### 6. Edge Case and Data Validation Tests (`test_edge_cases.py`)
**Edge Cases and DVR Coverage**: Tests for exceptional scenarios

#### Edge Case 1: Fixture Quality Variation
- Complexity stratification verification
- Complexity classification documentation
- Complexity-level analysis in reports

#### Edge Case 2: Token Counting Methodology
- Token counting source documentation (actual vs estimated)
- Variance documentation (±10% if estimated)
- Conversation metadata as source of truth
- Token value validation (reasonable ranges)

#### Edge Case 3: Non-Deterministic Generation
- Multiple runs per fixture (3 runs)
- Median value usage (not mean)
- Standard deviation reporting
- High variance fixture flagging (CV > 25%)

#### Data Validation Rules
- **DVR1**: Fixture pair completeness (baseline-NN.txt ↔ enhanced-NN.txt)
  - Error message validation: "Missing fixture pair: [name] exists but [name] not found"

- **DVR2**: Results JSON schema validation
  - Required fields: story_id, fixture_name, token_usage, ac_count, nfr_present, incomplete, iterations
  - Schema validation in measurement scripts

- **DVR3**: Statistical significance validation
  - P-value calculation and reporting
  - Non-significant result flagging (p ≥ 0.05)
  - Paired t-test usage

**Total Tests**: 22

## Test Execution

### Run All Tests
```bash
pytest tests/user-input-guidance/ -v
```

### Run Specific Test Module
```bash
pytest tests/user-input-guidance/test_infrastructure.py -v
pytest tests/user-input-guidance/test_fixtures.py -v
pytest tests/user-input-guidance/test_scripts.py -v
pytest tests/user-input-guidance/test_measurements.py -v
pytest tests/user-input-guidance/test_impact_report.py -v
pytest tests/user-input-guidance/test_edge_cases.py -v
```

### Run Specific Test Class
```bash
pytest tests/user-input-guidance/test_infrastructure.py::TestDirectoryStructure -v
pytest tests/user-input-guidance/test_edge_cases.py::TestDVR1FixturePairCompleteness -v
```

### Run Specific Test
```bash
pytest tests/user-input-guidance/test_infrastructure.py::TestDirectoryStructure::test_should_have_tests_user_input_guidance_directory -v
```

### Run with Coverage
```bash
pytest tests/user-input-guidance/ --cov=tests.user_input_guidance --cov-report=html
```

### Run with Output Details
```bash
pytest tests/user-input-guidance/ -v -s  # Shows print statements
pytest tests/user-input-guidance/ -vv    # Very verbose output
```

## Test Status: RED PHASE

All tests are designed to **FAIL** until implementation is complete. This follows Test-Driven Development (TDD) Red-Green-Refactor cycle:

- **RED Phase** (Current): All tests fail - validates test correctly checks requirements
- **GREEN Phase** (Next): Implementation created - tests pass
- **REFACTOR Phase** (Final): Code improved - tests stay green

## Story Requirements Coverage

| Requirement | Test Module | Test Count | Status |
|------------|------------|-----------|--------|
| **AC#1: Infrastructure** | test_infrastructure, test_fixtures | 32 | ✓ |
| **AC#2: Story Creation** | test_scripts | 15 | ✓ |
| **AC#3: Token Savings** | test_measurements, test_impact_report | 12 | ✓ |
| **AC#4: Success Rate** | test_measurements, test_impact_report | 13 | ✓ |
| **AC#5: Impact Report** | test_impact_report | 23 | ✓ |
| **Edge Case 1** | test_edge_cases | 3 | ✓ |
| **Edge Case 2** | test_edge_cases | 3 | ✓ |
| **Edge Case 3** | test_edge_cases | 4 | ✓ |
| **DVR1** | test_edge_cases | 2 | ✓ |
| **DVR2** | test_edge_cases | 3 | ✓ |
| **DVR3** | test_edge_cases | 3 | ✓ |
| **NFR-PERF** | test_impact_report | 1 | ✓ |
| **NFR-REL** | test_impact_report | 2 | ✓ |
| **NFR-MAINT** | test_measurements, test_impact_report | 3 | ✓ |

**Total Test Coverage: 99 tests across 5 acceptance criteria, 3 edge cases, 3 data validation rules, and 3 NFR categories**

## Expected Test Results (RED Phase)

When running the full test suite initially, expect:

```
FAILED tests/user-input-guidance/test_infrastructure.py::TestDirectoryStructure::test_should_have_tests_user_input_guidance_directory
FAILED tests/user-input-guidance/test_infrastructure.py::TestFixtureMetadata::test_should_have_fixture_metadata_file
FAILED tests/user-input-guidance/test_scripts.py::TestScriptOutputRequirements::test_should_generate_baseline_results_json_structure
... (99 failures total)

======================== 99 failed in X.XXs ========================
```

All failures are expected until implementation creates:
1. Test fixtures (10 baseline, 10 enhanced)
2. Test scripts (2 shell scripts)
3. Measurement scripts (2 Python scripts)
4. Results JSON files
5. Impact report

## Test Naming Convention

All tests follow the pattern: `test_should_[expected_behavior]_when_[condition]`

**Examples:**
- `test_should_have_tests_user_input_guidance_directory` - Directory structure
- `test_should_validate_baseline_fixtures_not_empty` - Content validation
- `test_should_have_10_baseline_fixtures` - Quantity check
- `test_should_generate_token_savings_report_markdown` - Output generation
- `test_should_calculate_p_value` - Statistical validation

## AAA Pattern (Arrange, Act, Assert)

Every test follows the Arrange-Act-Assert pattern:

```python
def test_should_do_something():
    # Arrange: Set up test preconditions
    expected_file = Path("/path/to/expected/file.txt")

    # Act: Execute the behavior being tested
    file_exists = expected_file.exists() and expected_file.is_file()

    # Assert: Verify the outcome
    assert file_exists, f"File not found: {expected_file}"
```

## Traceability

Each test is traceable to story requirements:

| Story Section | Test Modules | Coverage |
|---------------|--------------|----------|
| Acceptance Criteria | test_infrastructure through test_impact_report | 99 tests |
| Technical Specification | test_infrastructure through test_edge_cases | 99 tests |
| Edge Cases | test_edge_cases | 10 tests |
| Data Validation Rules | test_edge_cases | 8 tests |
| Non-Functional Requirements | test_measurements, test_impact_report | 6 tests |

## Dependencies

- **Python**: 3.8+
- **pytest**: Latest version
- **Standard Library**: pathlib, json, os, sys (used in implementation)

## Implementation Checklist

When implementing STORY-059, ensure:

- [ ] Create `tests/user-input-guidance/` directory structure
- [ ] Create 10 baseline fixtures in `fixtures/baseline/`
- [ ] Create 10 enhanced fixtures in `fixtures/enhanced/`
- [ ] Create `fixture-metadata.json` with complexity stratification
- [ ] Create `scripts/test-story-creation-without-guidance.sh`
- [ ] Create `scripts/test-story-creation-with-guidance.sh`
- [ ] Create `scripts/validate-token-savings.py` with statistical analysis
- [ ] Create `scripts/measure-success-rate.py` with completeness scoring
- [ ] Generate `baseline-results.json` from test execution
- [ ] Generate `enhanced-results.json` from test execution
- [ ] Generate `token-savings-report.md` with metrics
- [ ] Generate `success-rate-report.md` with breakdown
- [ ] Generate `.devforgeai/specs/enhancements/USER-INPUT-GUIDANCE-IMPACT-REPORT.md`

Once all artifacts exist, all 99 tests will pass (GREEN phase).

## See Also

- [STORY-059](../../.ai_docs/Stories/STORY-059-user-input-guidance-validation.story.md) - Full story specification
- [EPIC-011](../../.ai_docs/Epics/EPIC-011.epic.md) - User Input Guidance System epic
- [Test-Automator Skill](./.claude/skills/test-automator/) - Test generation framework

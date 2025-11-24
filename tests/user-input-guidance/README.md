# User Input Guidance Validation Test Suite

## Overview

This directory contains the complete test suite for **STORY-059: User Input Guidance Validation & Testing Suite**.

The test suite validates the user input guidance system through:
- **260+ pytest test functions** across 8 acceptance criteria
- **TDD Red-Green-Refactor cycle** integration
- **Comprehensive fixtures** (baseline, enhanced, expected improvements)
- **Measurement scripts** (token savings, success rate, impact reporting, validation)

## Directory Structure

```
tests/user-input-guidance/
├── fixtures/                    # Test data
│   ├── baseline/               # 10 baseline feature descriptions (50-200 words)
│   ├── enhanced/               # 10 enhanced descriptions (30-60% longer, Flesch ≥60)
│   └── expected/               # 10 expected improvements (JSON schema)
├── scripts/                     # Measurement and validation scripts
│   ├── measure-token-savings.py        # Token efficiency analysis
│   ├── measure-success-rate.py         # Quality metric analysis
│   ├── generate-impact-report.py       # Comprehensive reporting
│   └── validate-fixtures.py            # Fixture quality validation
├── reports/                     # Generated reports (created during test execution)
├── test_ac1_directory_structure.py     # AC#1: 35 tests
├── test_ac2_baseline_fixtures.py       # AC#2: 45 tests
├── test_ac3_enhanced_fixtures.py       # AC#3: 50 tests
├── test_ac4_expected_improvements.py   # AC#4: 40 tests
├── test_ac5_token_savings_script.py    # AC#5: 35 tests
├── test_ac6_to_ac8_measurement_scripts.py # AC#6-8: 55 tests
├── conftest.py                 # Shared pytest fixtures
├── README.md                    # This file
└── TEST_SUITE_SUMMARY.md       # Detailed test documentation
```

## Test Suite Purpose and Organization

### Purpose
This test suite validates a user input guidance system that helps improve software requirements. The system takes baseline requirements (50-200 words with typical quality issues) and demonstrates how guidance principles produce enhanced versions (30-60% longer with 3-5 quality improvements). The suite measures token savings, success rates, and business impact.

### Test Organization
Tests are organized by acceptance criteria (AC#1-AC#8):
- **AC#1**: Directory structure validation (35 tests)
- **AC#2**: Baseline fixtures validation (45 tests)
- **AC#3**: Enhanced fixtures validation (50 tests)
- **AC#4**: Expected improvements JSON files (40 tests)
- **AC#5**: Token savings measurement script (35 tests)
- **AC#6-AC#8**: Success rate, impact report, validation scripts (55 tests)

### Expected Outcomes
The test suite expects:
1. **Directory Structure**: 6 directories (baseline, enhanced, expected, scripts, reports) with README.md
2. **Baseline Fixtures**: 10 natural language descriptions (50-200 words) with quality issues
3. **Enhanced Fixtures**: 10 improved versions (30-60% longer) with 3-5 guidance principles applied
4. **Measurement Scripts**: 4 Python scripts that run in sequence and exit with code 0 on success
5. **Report Generation**: JSON reports from measurement scripts with consistent field structures
6. **Token Savings**: Mean token savings ≥20% from guidance application
7. **Success Rate**: ≥8 of 10 fixtures meeting quality improvement targets

## Running Tests

### Quick Start
```bash
cd /mnt/c/Projects/DevForgeAI2

# Run all tests with verbose output
pytest tests/user-input-guidance/ -v

# Run specific AC tests
pytest tests/user-input-guidance/test_ac1_directory_structure.py -v
pytest tests/user-input-guidance/test_ac2_baseline_fixtures.py -v
```

### By Category
```bash
# Run tests by acceptance criteria
pytest tests/user-input-guidance/ -k "ac1" -v
pytest tests/user-input-guidance/ -k "ac2" -v
pytest tests/user-input-guidance/ -k "ac3" -v
pytest tests/user-input-guidance/ -k "ac4" -v
pytest tests/user-input-guidance/ -k "ac5" -v
pytest tests/user-input-guidance/ -k "ac6 or ac7 or ac8" -v

# Run by test type
pytest tests/user-input-guidance/ -m "not edge_case" -v  # Skip edge cases
pytest tests/user-input-guidance/ -m "integration" -v    # Integration tests only
pytest tests/user-input-guidance/ -m "nfr" -v           # NFR tests only
```

### With Coverage Analysis
```bash
pytest tests/user-input-guidance/ --cov --cov-report=html
open htmlcov/index.html  # View coverage report
```

### Verbose Debugging
```bash
# Show print output and detailed tracebacks
pytest tests/user-input-guidance/ -v -s --tb=long

# Stop on first failure
pytest tests/user-input-guidance/ -x

# Run last failed tests
pytest tests/user-input-guidance/ --lf -v
```

## Test Acceptance Criteria

### AC#1: Test Directory Structure Created (35 tests)
**Status**: FAILING (TDD Red phase)

Validates:
- All 7 required directories exist
- Proper file permissions (755 for dirs, 644 for files)
- README.md with required sections
- .gitkeep file in reports/

**Test File**: `test_ac1_directory_structure.py`

### AC#2: Baseline Test Fixtures (45 tests)
**Status**: FAILING (TDD Red phase)

Validates:
- 10 baseline fixtures (one per domain)
- Naming: baseline-[NN]-[category].txt (NN=01-10)
- Word count: 50-200 words
- 2-4 quality issues per fixture
- Natural language content
- 10 unique domains covered

**Domains**:
1. CRUD operations (user management)
2. Authentication (login/signup)
3. API integration (third-party)
4. Data processing (ETL/batch)
5. UI components (dashboard/forms)
6. Reporting (analytics)
7. Background jobs (workers)
8. Search functionality
9. File uploads
10. Notifications

**Test File**: `test_ac2_baseline_fixtures.py`

### AC#3: Enhanced Test Fixtures (50 tests)
**Status**: FAILING (TDD Red phase)

Validates:
- 10 enhanced fixtures (baseline + guidance improvements)
- Naming: enhanced-[NN]-[category].txt
- 30-60% length increase over baseline
- Flesch Reading Ease ≥60
- 3-5 guidance principles applied
- Same domain as baseline

**Guidance Principles**:
- Specific scope (clear boundaries)
- Measurable criteria (numeric targets)
- Clear AC (Given/When/Then format)
- Explicit constraints (tech/compliance)
- NFR requirements (perf/security/scalability)

**Test File**: `test_ac3_enhanced_fixtures.py`

### AC#4: Expected Improvements (40 tests)
**Status**: FAILING (TDD Red phase)

Validates:
- 10 JSON files with expected improvements
- Required schema fields
- Evidence-based numeric ranges
- Baseline issues documentation
- Improvement predictions

**Schema**:
```json
{
  "fixture_id": "01",
  "category": "crud-operations",
  "baseline_issues": ["issue1", "issue2", ...],
  "expected_improvements": {
    "token_savings": 15-35,
    "ac_completeness": 70-95,
    "nfr_coverage": 50-100,
    "specificity_score": 60-90
  },
  "rationale": "Evidence-based explanation..."
}
```

**Test File**: `test_ac4_expected_improvements.py`

### AC#5: Token Savings Script (35 tests)
**Status**: FAILING (TDD Red phase)

Validates:
- `measure-token-savings.py` functionality
- Uses tiktoken (cl100k_base encoding)
- Loads 10 baseline/enhanced pairs
- Calculates savings % per pair
- Generates JSON report with statistics
- Exit code: 0 if ≥20% mean savings, 1 otherwise

**Report Fields**:
- Per-fixture: baseline_tokens, enhanced_tokens, savings_percentage
- Aggregate: mean_savings, median_savings, std_dev, min_savings, max_savings
- Hypothesis validation: passed (true/false)

**Test File**: `test_ac5_token_savings_script.py`

### AC#6: Success Rate Script (16 tests, part of combined file)
**Status**: FAILING (TDD Red phase)

Validates:
- `measure-success-rate.py` functionality
- Analyzes AC testability (Given/When/Then format)
- Analyzes NFR coverage (4 categories)
- Analyzes specificity (vague term reduction)
- Loads expected improvements for comparison
- Exit code: 0 if ≥8 of 10 fixtures meet expectations

**Test File**: `test_ac6_to_ac8_measurement_scripts.py`

### AC#7: Impact Report Script (18 tests, part of combined file)
**Status**: FAILING (TDD Red phase)

Validates:
- `generate-impact-report.py` functionality
- Loads latest token-savings and success-rate reports
- Generates Markdown report with 5 sections:
  1. Executive Summary (hypothesis + evidence)
  2. Token Efficiency (statistics + table)
  3. Quality Improvements (metric scores)
  4. Fixture Analysis (actual vs expected)
  5. Recommendations (specific, actionable)
- Includes ASCII visualizations
- DevForgeAI standards compliance (evidence-based)

**Test File**: `test_ac6_to_ac8_measurement_scripts.py`

### AC#8: Validation Script (21 tests, part of combined file)
**Status**: FAILING (TDD Red phase)

Validates:
- `validate-fixtures.py` functionality
- Validates all 30 fixtures:
  - Baseline: word count (50-200), issues (≥2), readability (≥50)
  - Enhanced: length increase (30-60%), readability (≥60), principles (≥3)
  - Expected: JSON schema, numeric ranges (0-100), evidence-based
- Generates JSON validation report
- Exit codes: 0 (pass), 1 (fail), 2 (incomplete pairs)

**Test File**: `test_ac6_to_ac8_measurement_scripts.py`

## Quality Metrics

### Fixture Quality Thresholds
| Metric | Baseline | Enhanced |
|--------|----------|----------|
| Word count | 50-200 | 30-60% increase |
| Quality issues | 2-4 per fixture | 3-5 principles |
| Flesch Reading Ease | ≥50 | ≥60 |

### Script Quality Thresholds
| Metric | Threshold | Purpose |
|--------|-----------|---------|
| Token savings | ≥20% mean | Cost reduction validation |
| Success rate | ≥8 of 10 fixtures | Quality improvement validation |
| Execution time | <5s (validate), <3s (token), <10s (success), <2s (report) | Performance |

### Numeric Ranges (Expected Improvements)
| Metric | Range |
|--------|-------|
| token_savings | 15-35% |
| ac_completeness | 70-95% |
| nfr_coverage | 50-100% |
| specificity_score | 60-90% |

## Test Fixtures Structure

### Baseline Fixtures (`fixtures/baseline/`)
- **Purpose**: Represent typical user input with quality issues
- **Format**: Plain text, natural language
- **Naming**: baseline-01-crud-operations.txt through baseline-10-notifications.txt
- **Content**: 50-200 words, 2-4 quality issues (vague requirements, missing AC, omitted NFRs)

### Enhanced Fixtures (`fixtures/enhanced/`)
- **Purpose**: Demonstrate guidance improvements
- **Format**: Plain text, natural language with structured AC/NFRs
- **Naming**: enhanced-01-crud-operations.txt through enhanced-10-notifications.txt
- **Content**: 30-60% longer than baseline, ≥60 Flesch score, 3-5 guidance principles

### Expected Improvements (`fixtures/expected/`)
- **Purpose**: Define validation criteria
- **Format**: JSON with schema validation
- **Naming**: expected-01-crud-operations.json through expected-10-notifications.json
- **Content**: fixture_id, category, baseline_issues array, expected_improvements object, rationale string

## Dependencies

### Required Python Packages
```
pytest>=7.0.0
pathlib (stdlib)
```

### Optional Packages for Full Functionality
```
tiktoken>=0.5.0          # For token savings measurement
textstat>=0.7.0          # For Flesch Reading Ease calculation
```

## Methodology

### Measurement Approach

**Token Savings Calculation:**
- Uses tiktoken library with Claude's cl100k_base encoding
- Counts all tokens in baseline and enhanced fixtures
- Calculates percentage savings as: (baseline_tokens - enhanced_tokens) / baseline_tokens × 100
- Aggregates across all 10 fixtures using mean, median, standard deviation
- Hypothesis validation: Mean savings must be ≥20% to demonstrate effectiveness
- Report includes per-fixture breakdowns and summary statistics

**Success Rate Measurement:**
- Analyzes acceptance criteria testability (Given/When/Then format presence)
- Counts NFR coverage across 4 categories: Performance, Security, Scalability, Compliance
- Measures specificity improvement by counting reductions in vague terms (fast, good, better, easy, simple, etc.)
- Compares actual metrics against expected improvements defined in expected/ JSON files
- Success rate: percentage of fixtures meeting or exceeding expected targets
- Threshold for passing: ≥8 of 10 fixtures meet expectations

**Enhanced Fixture Quality Validation:**
- Length increase: Measures word count ratio (enhanced_words / baseline_words)
- Target range: 30-60% increase ensures sufficient detail without verbosity
- Flesch Reading Ease: Calculated using textstat library
  - Formula: 206.835 - 1.015(words/sentences) - 84.6(syllables/words)
  - Target ≥60: Ensures readability for broad audience
  - Baseline ≥50: Maintains baseline readability
- Guidance principles: Detection of 5 key improvements
  1. Specific scope (presence of boundaries, explicit constraints, clear domain)
  2. Measurable criteria (numeric targets: <Xms, YK users, Z%)
  3. Clear AC structure (Given/When/Then format or equivalent)
  4. Explicit constraints (technology choices, integration requirements)
  5. Non-functional requirements (performance, security, scalability targets)

**Report Generation:**
- Combines token-savings and success-rate reports
- Produces Markdown output with 5 sections:
  1. Executive Summary: Hypothesis validation with evidence
  2. Token Efficiency: Statistics, distribution, visual table
  3. Quality Improvements: Metric scores and comparisons
  4. Fixture Analysis: Per-fixture actual vs. expected
  5. Recommendations: Specific, evidence-based, actionable
- Includes ASCII bar charts for visual interpretation

### Data Flow

```
Baseline Fixtures (50-200 words)
         ↓
    [Guidance Applied]
         ↓
Enhanced Fixtures (30-60% longer)
         ↓
┌────────┴────────┐
│                 │
[Token Count]  [Quality Analysis]
│                 │
├─ baseline_tokens ├─ AC testability
├─ enhanced_tokens ├─ NFR coverage
└─ savings_pct  └─ Specificity
         ↓                ↓
    [measure-token-savings.py] [measure-success-rate.py]
         ↓                ↓
    token-savings-*.json success-rate-*.json
         ↓                ↓
         └────────┬────────┘
                  ↓
     [generate-impact-report.py]
                  ↓
          impact-report-*.md

```

### Validation Strategy

**Fixture-Level Validation (validate-fixtures.py):**
- Baseline fixtures:
  - Word count: 50-200 words (realistic user input)
  - Quality issues: ≥2 detectable issues (vague terms, missing AC, omitted NFRs)
  - Readability: Flesch ≥50 (comprehensible)
- Enhanced fixtures:
  - Length increase: 30-60% (sufficient detail, no padding)
  - Readability: Flesch ≥60 (improved clarity)
  - Guidance principles: ≥3 of 5 applied (measurable improvement)
- Expected fixtures:
  - JSON schema validation
  - Numeric ranges: 0-100% valid percentages
  - Evidence-based: Rationale field explains improvements

**Integration-Level Validation:**
- Complete pipeline execution (all 10 fixtures)
- Report generation with proper formatting
- Exit codes reflect pass/fail status
- Error handling for edge cases (missing pairs, malformed data)

## Interpretation

### Understanding Token Savings Results

**Mean Savings ≥20%:**
- Hypothesis VALIDATED: Guidance effectively reduces token usage
- Recommendation: Framework improvements justified
- Business impact: Lower API costs, faster processing

**Mean Savings 10-20%:**
- Hypothesis MARGINAL: Modest improvement, but below threshold
- Recommendation: Review guidance principles, improve conciseness
- Action items: Refine enhanced fixture writing for tighter language

**Mean Savings <10%:**
- Hypothesis FAILED: Guidance increases complexity
- Recommendation: Fundamental changes needed to approach
- Root cause analysis: Check if enhanced fixtures are truly improved or just longer

**Standard Deviation Interpretation:**
- Std dev <10%: Consistent improvement across all domains
- Std dev 10-20%: Variable effectiveness by domain (some features benefit more)
- Std dev >20%: Inconsistent results (some fixtures much better, some worse)
  - Action: Identify outlier domains for targeted improvement

### Understanding Quality Metrics

**AC Completeness (70-95% target):**
- Measures coverage of Given/When/Then acceptance criteria
- 70%: Baseline with some implicit criteria
- 80%: Explicit Given/When/Then for key scenarios
- 95%: Comprehensive edge case coverage
- Interpretation: Higher completeness = fewer ambiguous acceptance criteria

**NFR Coverage (50-100% in 25% increments):**
- Tracks explicit non-functional requirements
- 50%: 1-2 categories mentioned (performance OR security)
- 75%: 3 categories with basic targets
- 100%: All 4 categories (performance, security, scalability, compliance) with numeric targets

**Specificity Score (60-90% target):**
- Measures reduction of vague terminology
- Tracks elimination of: "fast", "good", "better", "easy", "simple", "scalable", "reliable"
- 60%: Basic improvement, vague terms reduced
- 75%: Significant improvement, most terms clarified with metrics
- 90%: Comprehensive specificity, all quantities explicit with units/ranges

### Reading the Impact Report

**Executive Summary Section:**
- Hypothesis statement: What we're testing
- Result: PASSED/FAILED with evidence
- Key metric: Mean token savings percentage
- Recommendation: Framework adoption status

**Token Efficiency Table:**
- fixture_id: Fixture number 01-10
- category: Feature domain (CRUD, auth, API, etc.)
- baseline_tokens: Original token count
- enhanced_tokens: Improved version token count
- savings_percentage: (baseline - enhanced) / baseline × 100
- interpretation: Mark rows >20% as green, <20% as yellow, negative as red

**Quality Improvements Table:**
- Shows per-fixture scores: AC completeness, NFR coverage, specificity
- Expected vs. actual comparison
- Metrics meeting targets highlighted

**Recommendations Section:**
- Addresses specific failure modes if any
- Suggests domain-specific improvements
- Identifies best practices from high-performing fixtures
- Actionable next steps

### Troubleshooting Interpretation Issues

**Q: Token savings looks low. Why?**
A: Check if enhanced fixtures truly add detail (structure, AC, NFRs) or just verbosity. Quality gains should offset length increase.

**Q: Why is one domain much worse than others?**
A: May indicate domain-specific complexity. API integration might benefit less from guidance than UI components. Consider domain-aware thresholds.

**Q: Should we always aim for 60% length increase?**
A: No. The 30-60% range is a guideline. Some domains may need 20% (tight requirements) or 70% (complex integrations). Focus on quality over quantity.

**Q: How do I interpret negative token savings?**
A: Means enhanced fixture is longer but token usage decreased (e.g., more concise explanations of complex topics). Still valid if quality improved.

## Test Execution Workflow

### Phase 1: Red (Tests Failing)
1. All 260+ tests created and FAILING
2. No implementation code exists
3. Tests define specification

### Phase 2: Green (Tests Passing)
1. Implementation code created
2. Tests pass one by one
3. Target: 100% pass rate

### Phase 3: Refactor
1. Code quality improvements
2. Maintain all tests passing
3. Optimize performance

## Key Test Patterns

### AAA Pattern (Arrange, Act, Assert)
```python
def test_should_validate_word_count(self):
    # Arrange
    expected_min = 50
    content = "..." # fixture content

    # Act
    word_count = len(content.split())

    # Assert
    assert word_count >= expected_min
```

### Fixture-Based Dependencies
```python
@pytest.fixture
def baseline_dir(self):
    return Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/baseline")

def test_should_exist(self, baseline_dir):
    assert baseline_dir.is_dir()
```

### Descriptive Test Names
```
test_should_create_10_baseline_fixtures
test_fixture_word_count_should_be_50_to_200_words
test_enhanced_should_be_30_to_60_percent_longer
```

## Troubleshooting

### Tests Fail with "FileNotFoundError"
**Cause**: Missing fixture files
**Solution**: Implement AC#1-4 to create directory structure and fixtures

### Tests Skip with "textstat library not found"
**Cause**: Optional dependency missing
**Solution**: Install textstat for enhanced fixture readability validation
```bash
pip install textstat
```

### Tests Skip with "tiktoken library not found"
**Cause**: Optional dependency missing
**Solution**: Install tiktoken for token savings calculation
```bash
pip install tiktoken
```

### Test Takes Longer Than Expected
**Cause**: Performance requirements not being met
**Solution**: Review NFR requirements and optimize script implementation

## Contributing

When adding new tests:
1. Follow AAA pattern (Arrange, Act, Assert)
2. Use descriptive test names
3. Add docstring explaining what is being tested
4. Group related tests in test classes
5. Use fixtures for shared setup
6. Include both happy path and edge case tests

## References

- **STORY-059**: /mnt/c/Projects/DevForgeAI2/.ai_docs/Stories/STORY-059-validation-testing-suite.story.md
- **Test Suite Summary**: TEST_SUITE_SUMMARY.md
- **Effective Prompting Guide**: `.ai_docs/research/effective-prompting-guide.md`
- **User Input Guidance**: `.ai_docs/research/user-input-guidance.md`

## Status

**Current Phase**: Red (Tests Failing) - TDD Phase 1
**Last Updated**: 2025-01-22
**Total Tests**: 260+
**Pass Rate**: 0% (awaiting implementation)

See TEST_SUITE_SUMMARY.md for detailed test inventory and AC-by-AC breakdown.

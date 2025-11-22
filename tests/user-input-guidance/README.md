# User Input Guidance Validation & Testing Suite (STORY-059)

## Purpose

This comprehensive test suite validates the effectiveness of the **user input guidance system** for DevForgeAI. The guidance system provides structured recommendations to help users write clearer, more actionable feature descriptions and requirements. This suite measures whether the guidance achieves its primary objectives:

1. **Reduce token consumption** - More concise, less redundant specifications
2. **Improve acceptance criteria quality** - Clear, testable acceptance criteria (Given/When/Then)
3. **Increase NFR coverage** - Explicit non-functional requirements (performance, security, reliability, scalability)
4. **Improve specificity** - Replace vague terms ("fast", "good", "better") with measurable metrics

The test suite provides evidence-based validation that guidance improves specification quality through automated measurement and human-interpretable reporting.

## Test Suite Organization

### Fixture Descriptions

The test suite contains three parallel sets of 10 fixtures each, organized by domain and purpose:

#### Baseline Fixtures (10 files)
Located in: `tests/user-input-guidance/fixtures/baseline/`

These represent typical user input quality **without** guidance application. Each baseline fixture exhibits 2-4 common quality issues:
- **Vague language** ("fast", "good", "better", "optimize", "improve") without metrics
- **Missing success criteria** - No Given/When/Then structure, no testable outcomes
- **Ambiguous acceptance criteria** - Unclear what constitutes completion or success
- **Omitted non-functional requirements** - No explicit performance, security, reliability, or scalability targets

Baseline fixtures are **realistic** based on actual user patterns observed in DevForgeAI usage.

**Files (10 domains):**
1. baseline-01-crud-operations.txt - User account CRUD operations
2. baseline-02-authentication.txt - Login/signup/password recovery  
3. baseline-03-api-integration.txt - Third-party API integration
4. baseline-04-data-processing.txt - ETL and data pipelines
5. baseline-05-ui-components.txt - Dashboard and responsive design
6. baseline-06-reporting.txt - Analytics and report generation
7. baseline-07-background-jobs.txt - Asynchronous job processing
8. baseline-08-search-functionality.txt - Full-text search and filtering
9. baseline-09-file-uploads.txt - File handling and uploads
10. baseline-10-notifications.txt - Email, SMS, and webhook notifications

#### Enhanced Fixtures (10 files)  
Located in: `tests/user-input-guidance/fixtures/enhanced/`

These represent the **same requirements** rewritten following user input guidance principles. Enhanced fixtures demonstrate how guidance improves specification quality while preserving original scope.

**Improvements applied (3-5 per fixture):**
- **Specific scope** - Clear boundaries, concrete names
- **Measurable success criteria** - Specific numbers (e.g., <100ms, 10K users)
- **Clear acceptance criteria** - Given/When/Then format
- **Explicit constraints** - Technology, compliance requirements
- **Non-functional requirements** - All 4 NFR categories (Performance, Security, Reliability, Scalability)

#### Expected Improvements (10 JSON files)
Located in: `tests/user-input-guidance/fixtures/expected/`

These define the **expected improvements** from applying guidance, used as validation targets.

**JSON Schema:**
```json
{
  "fixture_id": "01",
  "category": "crud-operations",
  "baseline_issues": ["vague scope", "missing criteria"],
  "expected_improvements": {
    "token_savings": 28.0,
    "ac_completeness": 85.0,
    "nfr_coverage": 75.0,
    "specificity_score": 78.0
  },
  "rationale": "Guidance clarifies scope, adds Given/When/Then AC, specifies performance <500ms, security TLS 1.2+, scalability 100K users. Token reduction from removing hedging language and replacing vague terms with metrics."
}
```

## Measurement Scripts

All scripts are located in: `tests/user-input-guidance/scripts/`

### 1. measure-token-savings.py

**Purpose:** Quantify token efficiency improvements using Claude's tokenizer.

**Usage:**
```bash
python scripts/measure-token-savings.py
python scripts/measure-token-savings.py --help
python scripts/measure-token-savings.py --test
```

**Functionality:**
- Load all 10 baseline/enhanced fixture pairs
- Calculate token counts using tiktoken (cl100k_base encoding)
- Compute savings: (baseline_tokens - enhanced_tokens) / baseline_tokens * 100
- Generate JSON report with per-fixture and aggregate statistics

**Output:** `reports/token-savings-YYYY-MM-DD-HH-MM-SS.json`

**Exit Codes:**
- `0` - Success: Mean savings ≥20%
- `1` - Failure: Mean savings <20%  
- `3` - Missing library: tiktoken not installed
- `4` - Invalid input: Fixture files missing

**Output Messages:**
- Success: "✅ Token savings hypothesis VALIDATED: Mean savings 25.3% (target ≥20%)"
- Failure: "❌ Token savings hypothesis FAILED: Mean savings 18.5% (target ≥20%)"

### 2. measure-success-rate.py

**Purpose:** Evaluate acceptance criteria completeness and requirement quality.

**Usage:**
```bash
python scripts/measure-success-rate.py
python scripts/measure-success-rate.py --help
python scripts/measure-success-rate.py --test
```

**Functionality:**
- Load all 10 baseline/enhanced fixture pairs
- Analyze 3 quality metrics:
  1. **AC Testability** - % using Given/When/Then format
  2. **NFR Coverage** - % of 4 categories (performance, security, reliability, scalability)
  3. **Specificity** - % reduction in vague terms
- Compare actual vs expected values from expected/*.json files

**Output:** `reports/success-rate-YYYY-MM-DD-HH-MM-SS.json`

**Exit Codes:**
- `0` - Success: ≥8 of 10 fixtures meet expectations
- `1` - Failure: <8 of 10 fixtures meet expectations
- `5` - Missing dependencies: expected/*.json files not found

**Per-Fixture Output Example:**
```
Fixture 01 (crud-operations):
  AC testability: 85% (expected 85%) ✅
  NFR coverage: 75% (expected 75%) ✅
  Specificity: 78% (expected 78%) ✅
  → PASS (3/3 metrics met)
```

### 3. generate-impact-report.py

**Purpose:** Generate comprehensive Markdown report from measurement results.

**Usage:**
```bash
python scripts/generate-impact-report.py
python scripts/generate-impact-report.py --help
```

**Functionality:**
- Load most recent token-savings and success-rate JSON reports
- Generate Markdown report with 5 required sections
- Include ASCII visualizations using Unicode box-drawing characters
- Provide actionable recommendations

**Output:** `reports/impact-report-YYYY-MM-DD-HH-MM-SS.md`

**Required Report Sections:**
1. **Executive Summary** - Overall pass/fail, 3-5 key findings, recommendation
2. **Token Efficiency** - Mean/median/std dev savings, per-fixture table
3. **Quality Improvements** - AC testability, NFR coverage, specificity scores
4. **Fixture Analysis** - Per-fixture comparison (actual vs expected)
5. **Recommendations** - Actionable improvements if metrics below expectations

**Exit Codes:**
- `0` - Success: Report generated
- `5` - Missing dependencies: Measurement reports not found

### 4. validate-fixtures.py

**Purpose:** Validate all 30 fixtures against quality rules.

**Usage:**
```bash
python scripts/validate-fixtures.py
python scripts/validate-fixtures.py --help
python scripts/validate-fixtures.py --test
```

**Validation Rules:**

**Baseline Fixtures:**
- Word count: 50-200 words
- Quality issues: ≥2 detected
- Readability: Flesch ≥50 (when textstat available)
- Language: Natural sentences (not bullets, not code)

**Enhanced Fixtures:**
- Length: 30-60% longer than baseline
- Readability: Flesch ≥60
- Principles: ≥3 guidance principles applied
- Preservation: Same domain as baseline

**Expected Files:**
- Valid JSON with required fields
- Numeric ranges: All values 0-100%
- Evidence-based rationale

**Output:** `reports/fixture-validation-YYYY-MM-DD-HH-MM-SS.json`

**Exit Codes:**
- `0` - Success: All 30 fixtures pass
- `1` - Failure: Any fixtures fail
- `2` - Incomplete pairs: Missing baseline, enhanced, or expected
- `3` - Missing library: textstat not installed
- `4` - Invalid input: Fixture directories not found

## Measurement Methodology

### Token Calculation
- **Library:** tiktoken (Claude's official tokenizer)
- **Encoding:** cl100k_base (same as Claude Sonnet 4.5)
- **Formula:** (baseline_tokens - enhanced_tokens) / baseline_tokens * 100

### AC Testability
- **Definition:** % of requirements using Given/When/Then format
- **Calculation:** (Given/When/Then blocks / total requirement statements) * 100
- **Range:** 0-100%

### NFR Coverage
- **Categories:** Performance, Security, Reliability, Scalability
- **Calculation:** (count of mentioned categories / 4) * 100
- **Granularity:** 0%, 25%, 50%, 75%, 100%

### Specificity Scoring
- **Vague terms:** fast, good, better, optimize, improve, easy, simple
- **Calculation:** ((baseline_vague_count - enhanced_vague_count) / baseline_vague_count) * 100
- **Range:** 0-100%

### Readability (Optional)
- **Library:** textstat (optional dependency)
- **Metric:** Flesch Reading Ease (0-100)
- **Baseline Target:** ≥50
- **Enhanced Target:** ≥60

## Interpretation Guide

### Token Savings
**Note:** Enhanced may be LONGER in tokens (more detailed), but CLEARER and MORE TESTABLE.
- **Positive savings (15-35%):** Guidance reduces redundancy while clarifying
- **Negative savings (-60%):** Expected when adding structure and detail
- **Focus:** Clarity and completeness, not mere token reduction

### AC Testability
- **Baseline:** <30% (vague language, no structure)
- **Enhanced:** 80-95% (Given/When/Then format, testable)
- **Interpretation:** Clear, verifiable acceptance criteria

### NFR Coverage
- **Baseline:** 25-50% (1-2 categories vaguely mentioned)
- **Enhanced:** 75-100% (all 4 categories with specific targets)
- **0%** = No NFR discussion
- **25%** = 1 category mentioned
- **50%** = 2 categories mentioned
- **75%** = 3 categories with targets
- **100%** = All 4 with measurable targets

### Specificity
- **Baseline:** 8-15 vague terms
- **Enhanced:** 1-4 vague terms
- **Improvement:** 60-90% reduction
- **Examples:**
  - "fast" → "<500ms p95 latency"
  - "good" → "≥80% success rate"
  - "better" → "+30% improvement"
  - "optimize" → "10,000 records/second"

## Performance Benchmarks

Scripts must complete within:
- measure-token-savings.py: <3 seconds
- measure-success-rate.py: <10 seconds  
- generate-impact-report.py: <2 seconds
- validate-fixtures.py: <5 seconds

## Running the Test Suite

### Manual Execution
```bash
# Validate fixtures
python scripts/validate-fixtures.py

# Measure token efficiency
python scripts/measure-token-savings.py

# Evaluate quality improvements
python scripts/measure-success-rate.py

# Generate final report
python scripts/generate-impact-report.py
```

### With Pytest
```bash
pytest tests/user-input-guidance/test_fixture_structure.py
pytest tests/user-input-guidance/test_measurement_scripts.py
pytest tests/user-input-guidance/test_edge_cases_and_nfrs.py
```

## Dependencies

### Required
- Python 3.9+
- tiktoken >=0.5.1
- pytest >=7.0

### Optional
- textstat >=0.7.0 (for Flesch Reading Ease)

### Installation
```bash
pip install -r requirements.txt
```

## References

- **Guidance Documents:**
  - effective-prompting-guide.md
  - user-input-guidance.md

- **Related Stories:**
  - STORY-052 through STORY-058: Guidance implementation
  - STORY-059: Validation testing suite

---

**Last Updated:** 2025-01-20
**Fixtures:** 30 (10 baseline + 10 enhanced + 10 expected)
**Test Coverage:** Directory structure, fixtures, measurement scripts, edge cases, NFRs

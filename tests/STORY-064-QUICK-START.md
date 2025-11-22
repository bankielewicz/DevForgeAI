# STORY-064 Test Suite - Quick Start Guide

## Overview

Test suite for STORY-064: devforgeai-story-creation Integration Validation and Test Execution

- **Total Tests**: 45
- **Pass Rate**: 100% (45/45 passing)
- **Execution Time**: ~1.2 seconds
- **Status**: All tests passing (infrastructure in place from STORY-056)

---

## Running Tests

### All Tests
```bash
cd /mnt/c/Projects/DevForgeAI2
python3 -m pytest tests/unit/test_story_064_unit_suite.py \
  tests/integration/test_story_064_integration_suite.py \
  tests/regression/test_story_064_regression_suite.py \
  tests/performance/test_story_064_performance_suite.py -v
```

### By Suite
```bash
# Unit tests (15 tests)
pytest tests/unit/test_story_064_unit_suite.py -v

# Integration tests (12 tests)
pytest tests/integration/test_story_064_integration_suite.py -v

# Regression tests (10 tests)
pytest tests/regression/test_story_064_regression_suite.py -v

# Performance tests (8 tests)
pytest tests/performance/test_story_064_performance_suite.py -v
```

### By Marker
```bash
# Only unit tests
pytest -m unit -v

# Only acceptance criteria tests
pytest -m acceptance_criteria -v

# Only performance tests
pytest -m performance -v
```

---

## Test Files

### Location: `/mnt/c/Projects/DevForgeAI2/tests/`

| Suite | File | Tests | Classes |
|-------|------|-------|---------|
| Unit | `unit/test_story_064_unit_suite.py` | 15 | TestFixtures, TestDataValidationRules |
| Integration | `integration/test_story_064_integration_suite.py` | 12 | TestSkillIntegration, TestCICDIntegration, TestCrossReferences, TestProductionValidation |
| Regression | `regression/test_story_064_regression_suite.py` | 10 | TestBackwardCompatibility, TestProductionScenarios |
| Performance | `performance/test_story_064_performance_suite.py` | 8 | TestGuidanceLoadingPerformance, TestQuestionGenerationPerformance |

---

## Test Fixtures

Location: `/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/`

1. **simple-feature.md** - CRUD operation (straightforward)
2. **moderate-feature.md** - Multi-component integration
3. **complex-feature.md** - Cross-cutting concerns (real-time notifications)
4. **ambiguous-feature.md** - Vague requirements (intentional)
5. **edge-case-feature.md** - Resource exhaustion handling (boundary conditions)

---

## Acceptance Criteria Coverage

| AC | Coverage | Tests |
|----|----------|-------|
| AC-1 | Test Suite Execution (45 tests, 95%+ pass rate) | All 45 tests |
| AC-2 | Test Fixtures (5 feature descriptions) | UT01-05, IT03 |
| AC-3 | Data Validation Rules (8 rules) | UT06-15 |
| AC-4 | CI/CD Integration | IT04-06 |
| AC-5 | Cross-References | IT07-09 |
| AC-6 | Production Validation | IT10-12, REG06-10 |

---

## CI/CD Pipeline

**File**: `.devforgeai/ci/story-creation-test-pipeline.yml`

**Features**:
- Triggers on story-creation SKILL.md commits
- Runs all 4 test suites (unit → [integration, regression, performance])
- Blocks merge on any test failure
- Provides aggregated results

**Pipeline Jobs**:
1. unit-tests (15 tests)
2. integration-tests (12 tests, after unit)
3. regression-tests (10 tests, after unit)
4. performance-tests (8 tests, after unit)
5. test-summary (aggregates results)
6. merge-gate (blocks if failures)

---

## Key Test Classes

### Unit Tests (UT01-UT15)
- **TestFixtures** - Validates 5 fixture files exist with correct content
- **TestDataValidationRules** - Validates 8 data rules with assertions

### Integration Tests (IT01-IT12)
- **TestSkillIntegration** - Guidance loading in SKILL.md, pattern documentation
- **TestCICDIntegration** - Pipeline configuration, trigger conditions
- **TestCrossReferences** - Bidirectional guidance navigation
- **TestProductionValidation** - /create-story command integration

### Regression Tests (REG01-REG10)
- **TestBackwardCompatibility** - Works without guidance, no circular dependencies
- **TestProductionScenarios** - Pattern usage in epic, priority, points selection

### Performance Tests (PERF01-PERF08)
- **TestGuidanceLoadingPerformance** - Load time <2s, file size <50KB
- **TestQuestionGenerationPerformance** - Epic/priority/points generation fast

---

## Data Validation Rules (8)

| Rule | Test | Validation |
|------|------|-----------|
| 1 | UT06 | Guidance file location and path |
| 2 | UT07 | Pattern extraction methodology |
| 3 | UT08 | Pattern-to-question mapping |
| 4 | UT09 | Token measurement (<50KB) |
| 5 | UT10 | Batch mode caching strategy |
| 6 | UT11 | Conditional loading logic |
| 7 | UT12 | Pattern name normalization |
| 8 | UT13 | Backward compatibility |

---

## Test Status Summary

```
Unit Tests (UT01-UT15)          15/15 PASS ✓
Integration Tests (IT01-IT12)   12/12 PASS ✓
Regression Tests (REG01-REG10)  10/10 PASS ✓
Performance Tests (PERF01-08)    8/8  PASS ✓
────────────────────────────────────────────
TOTAL                           45/45 PASS ✓

Pass Rate: 100% (exceeds 95% target)
Execution Time: 1.18 seconds
```

---

## Expected Test Behavior

All tests currently PASS because:
1. STORY-056 implementation complete (infrastructure in place)
2. Test fixtures created (5 files with correct format)
3. Integration guide exists (pattern-to-question mapping)
4. CI/CD pipeline configured (GitHub Actions YAML)
5. Cross-references documented (bidirectional navigation)

Tests will FAIL if:
1. Fixtures are removed or renamed
2. Integration guide content deleted
3. SKILL.md guidance loading removed
4. Cross-reference links broken

---

## Integration with Story Workflow

**AC-1: Test Suite Execution Complete**
- All 45 tests must pass (95%+ minimum, achieved 100%)
- Tests verify correct test suite exists and passes

**AC-2: Test Fixtures Created**
- 5 feature descriptions in tests/user-input-guidance/fixtures/
- Unit tests (UT01-05) validate fixture existence and format

**AC-3: Data Validation Rules Enforced**
- 8 validation rules with ≥1 test assertion each
- Unit tests (UT06-15) validate each rule is tested

**AC-4: CI/CD Integration Configured**
- Pipeline configuration in .devforgeai/ci/
- Integration tests (IT04-06) validate pipeline setup

**AC-5: Cross-Reference Added**
- Integration points section in ideation guidance
- Integration tests (IT07-09) validate cross-references

**AC-6: Production Validation**
- /create-story command tested
- Integration tests (IT10-12) verify production readiness

---

## Troubleshooting

### Test fails: "fixture not found"
```
Check: tests/user-input-guidance/fixtures/
Ensure all 5 .md files exist with correct names
```

### Test fails: "integration guide not found"
```
Check: src/claude/skills/devforgeai-story-creation/references/user-input-integration-guide.md
Ensure file exists with pattern documentation
```

### Test fails: "SKILL.md guidance loading missing"
```
Check: src/claude/skills/devforgeai-story-creation/SKILL.md
Ensure Phase 1 Step 0 documents guidance loading
```

### Test fails: "pipeline configuration missing"
```
Check: .devforgeai/ci/story-creation-test-pipeline.yml
Ensure file exists with trigger conditions and job definitions
```

---

## Next Steps

1. **Review Test Results**: All 45 tests passing (100%)
2. **Verify Infrastructure**: Fixtures, integration guide, SKILL.md all present
3. **CI/CD Validation**: Confirm pipeline triggers correctly on commits
4. **Production Testing**: Execute /create-story with sample feature descriptions
5. **Update Story**: Mark AC items complete once validation complete

---

## References

- **Full Summary**: STORY-064-TEST-GENERATION-SUMMARY.md
- **Story File**: .ai_docs/Stories/STORY-064-story-creation-integration-validation.story.md
- **Story-056 Implementation**: .ai_docs/Stories/STORY-056-devforgeai-story-creation-integration.story.md
- **Ideation Integration**: .ai_docs/Stories/STORY-055-devforgeai-ideation-integration.story.md

---

**Generated**: 2025-01-21
**Status**: COMPLETE - Ready for Green Phase (Production Validation)

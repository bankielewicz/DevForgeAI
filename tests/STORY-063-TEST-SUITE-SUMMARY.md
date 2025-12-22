# STORY-063: code-quality-auditor Test Suite Summary

## Test-Driven Development (TDD) - RED PHASE

**Status:** All tests written BEFORE implementation (Red phase)
**Expected Result:** All tests should FAIL initially
**Next Steps:** Implement code-quality-auditor subagent (Green phase)

---

## Test Coverage Overview

### Unit Tests
**File:** `tests/unit/subagents/test_code_quality_auditor.py`
**Test Count:** 20+ tests across 6 test classes
**Coverage Target:** 95% business logic

#### Test Classes

1. **TestSubagentSpecification** (AC1)
   - `test_subagent_file_exists_in_src` - Validates file creation
   - `test_yaml_frontmatter_complete` - Validates YAML structure
   - `test_eight_phase_workflow_documented` - Validates 8 phases
   - `test_three_metrics_documented` - Validates 3 metrics

2. **TestComplexityAnalysis** (AC2)
   - `test_detects_extreme_complexity_critical` - Complexity 28 → CRITICAL
   - `test_complexity_warning_does_not_block` - Complexity 18 → WARNING
   - `test_language_specific_tool_mapping` - Tool mappings

3. **TestDuplicationDetection** (AC3)
   - `test_detects_extreme_duplication_critical` - 27% duplication → CRITICAL
   - `test_duplication_percentage_calculation` - Calculation accuracy

4. **TestMaintainabilityIndex** (AC4)
   - `test_detects_low_maintainability_critical` - MI 35 → CRITICAL
   - `test_mi_scale_interpretation` - MI scale (0-100)

5. **TestBusinessImpactExplanations** (AC5)
   - `test_complexity_business_impact_quantified` - Quantified impact
   - `test_duplication_business_impact_quantified` - Quantified impact
   - `test_maintainability_business_impact_quantified` - Quantified impact

6. **TestRefactoringPatternRecommendations** (AC6)
   - `test_complexity_refactoring_pattern_specific` - Extract Method
   - `test_duplication_refactoring_pattern_specific` - Extract to Utility

7. **TestExtremeViolationsOnly** (AC9)
   - `test_acceptable_metrics_no_violations` - No noise
   - `test_positive_feedback_for_excellent_quality` - ✅ feedback

8. **TestErrorHandlingMissingTools** (AC10)
   - `test_tool_not_available_returns_failure` - Tool missing
   - `test_no_source_files_returns_failure` - Files missing
   - `test_tool_execution_failed_returns_stderr` - Execution error

9. **TestEdgeCases**
   - `test_multiple_violations_same_file` - Edge Case 2
   - `test_generated_code_excluded` - Edge Case 4

---

### Integration Tests
**File:** `tests/integration/test_code_quality_auditor_integration.py`
**Test Count:** 10+ tests across 4 test classes
**Coverage Target:** 85% application layer

#### Test Classes

1. **TestQASkillIntegration** (AC7)
   - `test_qa_skill_invokes_code_quality_auditor` - End-to-end integration
   - `test_qa_skill_continues_after_successful_analysis` - Continue on success
   - `test_qa_skill_halts_on_analysis_failure` - HALT on failure

2. **TestPromptTemplate** (AC8)
   - `test_prompt_template_file_exists` - File exists
   - `test_prompt_template_includes_code_quality_auditor` - Template 3 documented
   - `test_prompt_template_documents_token_savings` - 70% savings

3. **TestEndToEndWorkflow**
   - `test_complete_workflow_with_violations` - QA blocked
   - `test_complete_workflow_no_violations` - QA approved

4. **TestPerformance**
   - `test_analysis_completes_within_60_seconds` - <60s for large projects

---

### Test Fixtures
**File:** `tests/fixtures/code_quality_fixtures.py`
**Purpose:** Provide deterministic test data

#### Fixtures Provided

1. **Sample Code:**
   - `PYTHON_EXTREME_COMPLEXITY` - Complexity 28 function
   - `CSHARP_EXTREME_COMPLEXITY` - Complexity 28 function
   - `CODE_WITH_DUPLICATION` - 27% duplication
   - `PYTHON_LOW_MAINTAINABILITY` - MI 35.2 file

2. **Mock Tool Outputs:**
   - `MOCK_RADON_COMPLEXITY_OUTPUT` - radon cc JSON
   - `MOCK_RADON_MI_OUTPUT` - radon mi JSON
   - `MOCK_JSCPD_DUPLICATION_OUTPUT` - jscpd JSON

3. **Expected Results:**
   - `EXPECTED_COMPLEXITY_VIOLATION` - Full violation structure
   - `EXPECTED_DUPLICATION_VIOLATION` - Full violation structure
   - `EXPECTED_MAINTAINABILITY_VIOLATION` - Full violation structure

4. **Utility Functions:**
   - `create_test_source_file()` - Create test files
   - `create_test_context_files()` - Create context files

---

## Test Execution

### Running All Tests
```bash
# Run all STORY-063 tests
pytest tests/unit/subagents/test_code_quality_auditor.py \
       tests/integration/test_code_quality_auditor_integration.py \
       -v --tb=short

# Expected result (RED PHASE): All tests FAIL
# Reason: code-quality-auditor subagent not yet implemented
```

### Running Unit Tests Only
```bash
pytest tests/unit/subagents/test_code_quality_auditor.py -v
```

### Running Integration Tests Only
```bash
pytest tests/integration/test_code_quality_auditor_integration.py -v
```

### Running with Coverage Analysis
```bash
pytest tests/unit/subagents/test_code_quality_auditor.py \
       tests/integration/test_code_quality_auditor_integration.py \
       --cov=src/claude/agents/code_quality_auditor \
       --cov-report=term \
       --cov-report=html
```

---

## Coverage Targets

### Business Logic (95% target)
**Code-quality-auditor core logic:**
- Metric calculations (complexity, duplication, MI)
- Threshold validation (CRITICAL >20, >25%, <40)
- Business impact generation
- Refactoring pattern generation
- Violation aggregation

### Application Layer (85% target)
**Integration with devforgeai-qa skill:**
- Task() invocation
- Context file loading
- Result parsing
- blocks_qa state management
- Error handling

### Infrastructure Layer (80% target)
**Tool execution and parsing:**
- radon, eslint, jscpd invocation
- JSON parsing
- File I/O
- Error handling

---

## Expected Test Failures (RED PHASE)

### Unit Test Failures (Expected)
```
FAILED test_subagent_file_exists_in_src - AssertionError: Subagent file not found
FAILED test_yaml_frontmatter_complete - FileNotFoundError: code-quality-auditor.md
FAILED test_eight_phase_workflow_documented - FileNotFoundError
FAILED test_three_metrics_documented - FileNotFoundError
FAILED test_detects_extreme_complexity_critical - NotImplementedError
FAILED test_detects_extreme_duplication_critical - NotImplementedError
FAILED test_detects_low_maintainability_critical - NotImplementedError
... (all tests expected to fail)
```

### Integration Test Failures (Expected)
```
FAILED test_qa_skill_invokes_code_quality_auditor - SubagentNotFoundError
FAILED test_prompt_template_file_exists - FileNotFoundError
FAILED test_complete_workflow_with_violations - NotImplementedError
... (all tests expected to fail)
```

---

## Acceptance Criteria Test Mapping

### AC1: Subagent Specification (4 tests)
- ✅ `test_subagent_file_exists_in_src`
- ✅ `test_yaml_frontmatter_complete`
- ✅ `test_eight_phase_workflow_documented`
- ✅ `test_three_metrics_documented`

### AC2: Cyclomatic Complexity (3 tests)
- ✅ `test_detects_extreme_complexity_critical`
- ✅ `test_complexity_warning_does_not_block`
- ✅ `test_language_specific_tool_mapping`

### AC3: Code Duplication (2 tests)
- ✅ `test_detects_extreme_duplication_critical`
- ✅ `test_duplication_percentage_calculation`

### AC4: Maintainability Index (2 tests)
- ✅ `test_detects_low_maintainability_critical`
- ✅ `test_mi_scale_interpretation`

### AC5: Business Impact (3 tests)
- ✅ `test_complexity_business_impact_quantified`
- ✅ `test_duplication_business_impact_quantified`
- ✅ `test_maintainability_business_impact_quantified`

### AC6: Refactoring Patterns (2 tests)
- ✅ `test_complexity_refactoring_pattern_specific`
- ✅ `test_duplication_refactoring_pattern_specific`

### AC7: QA Integration (3 tests)
- ✅ `test_qa_skill_invokes_code_quality_auditor`
- ✅ `test_qa_skill_continues_after_successful_analysis`
- ✅ `test_qa_skill_halts_on_analysis_failure`

### AC8: Prompt Template (3 tests)
- ✅ `test_prompt_template_file_exists`
- ✅ `test_prompt_template_includes_code_quality_auditor`
- ✅ `test_prompt_template_documents_token_savings`

### AC9: Extreme Violations Only (2 tests)
- ✅ `test_acceptable_metrics_no_violations`
- ✅ `test_positive_feedback_for_excellent_quality`

### AC10: Error Handling (3 tests)
- ✅ `test_tool_not_available_returns_failure`
- ✅ `test_no_source_files_returns_failure`
- ✅ `test_tool_execution_failed_returns_stderr`

**Total AC Coverage:** 10/10 acceptance criteria (100%)

---

## Test Data Scenarios

### Scenario 1: Extreme Complexity (CRITICAL)
**Input:** Function with complexity 28
**Expected Output:**
- `blocks_qa = True`
- Severity: CRITICAL
- Business Impact: "40% higher defect rate..."
- Refactoring Pattern: "Extract Method: Split into 5 methods..."

### Scenario 2: Extreme Duplication (CRITICAL)
**Input:** 27% code duplication
**Expected Output:**
- `blocks_qa = True`
- Severity: CRITICAL
- Business Impact: "Changes in 2+ places..."
- Refactoring Pattern: "Extract to Shared Utility Class..."

### Scenario 3: Low Maintainability (CRITICAL)
**Input:** MI 35.2 file
**Expected Output:**
- `blocks_qa = True`
- Severity: CRITICAL
- Business Impact: "50% slower modifications..."
- Refactoring Pattern: "Simplify logic and extract methods..."

### Scenario 4: Acceptable Quality (No violations)
**Input:** Complexity 12, Duplication 15%, MI 65
**Expected Output:**
- `blocks_qa = False`
- No violations
- Positive feedback: "✅ EXCELLENT: All metrics meet thresholds"

### Scenario 5: Tool Not Available (Error)
**Input:** radon not installed
**Expected Output:**
- `status = "failure"`
- `blocks_qa = True`
- Error: "radon not installed"
- Remediation: "pip install radon"

---

## Next Steps (GREEN PHASE)

After tests written (current state - RED PHASE):

1. **Implement code-quality-auditor subagent:**
   - Create `src/claude/agents/code-quality-auditor.md`
   - Implement 8-phase workflow
   - Add language-specific tooling
   - Add business impact explanations
   - Add refactoring patterns

2. **Create prompt template:**
   - Add Template 3 to `src/claude/skills/devforgeai-qa/references/subagent-prompt-templates.md`
   - Document invocation pattern
   - Document response parsing

3. **Run tests (GREEN PHASE):**
   ```bash
   pytest tests/unit/subagents/test_code_quality_auditor.py -v
   # Expected: All tests PASS
   ```

4. **Validate coverage:**
   ```bash
   pytest --cov=src/claude/agents/code_quality_auditor \
          --cov-report=term \
          --cov-fail-under=95
   # Expected: ≥95% coverage
   ```

5. **REFACTOR PHASE:**
   - Improve code quality
   - Optimize performance
   - Enhance error messages
   - Keep tests green

---

## Success Criteria

### Definition of Done Validation

- [x] **Test Generation:**
  - 20+ unit tests created (4 minimum requirement)
  - 10+ integration tests created (1 minimum requirement)
  - Test fixtures created
  - All acceptance criteria covered

- [ ] **Test Execution (After Implementation):**
  - All tests PASS (currently FAIL - expected)
  - Coverage ≥95% business logic
  - Coverage ≥85% application layer
  - Performance <60s for large projects

- [x] **Test Quality:**
  - AAA pattern (Arrange, Act, Assert)
  - Descriptive test names
  - No shared mutable state
  - Independent test execution

---

## Token Budget Analysis

### Test File Sizes
- `test_code_quality_auditor.py`: ~650 lines (~20K tokens)
- `test_code_quality_auditor_integration.py`: ~450 lines (~14K tokens)
- `code_quality_fixtures.py`: ~550 lines (~16K tokens)
- **Total:** ~1,650 lines (~50K tokens)

### Token Efficiency
- Progressive disclosure: Fixtures separate from tests
- Reusable fixtures: 9 fixtures for 30+ tests
- Mocked dependencies: No external API calls
- Deterministic data: Known input/output pairs

---

## Files Created

### Test Files
1. `/mnt/c/Projects/DevForgeAI2/tests/unit/subagents/test_code_quality_auditor.py`
   - Unit tests (20+ tests)
   - 9 test classes
   - 650 lines

2. `/mnt/c/Projects/DevForgeAI2/tests/integration/test_code_quality_auditor_integration.py`
   - Integration tests (10+ tests)
   - 4 test classes
   - 450 lines

3. `/mnt/c/Projects/DevForgeAI2/tests/fixtures/code_quality_fixtures.py`
   - Test fixtures and sample data
   - 9 fixtures
   - 2 utility functions
   - 550 lines

4. `/mnt/c/Projects/DevForgeAI2/tests/STORY-063-TEST-SUITE-SUMMARY.md`
   - This summary document
   - Test execution guide
   - Coverage targets
   - Success criteria

---

## Related Documentation

- **Story:** `devforgeai/specs/Stories/STORY-063-code-quality-auditor-subagent.story.md`
- **Subagent (to be created):** `src/claude/agents/code-quality-auditor.md`
- **Prompt Template (to be created):** `src/claude/skills/devforgeai-qa/references/subagent-prompt-templates.md`
- **Test Automation Skill:** `.claude/skills/test-automator/SKILL.md`
- **QA Skill:** `.claude/skills/devforgeai-qa/SKILL.md`

---

**Test Suite Status:** ✅ COMPLETE (RED PHASE)
**Implementation Status:** ⏳ PENDING (GREEN PHASE)
**Date Created:** 2025-11-24
**Story:** STORY-063
**Test Coverage:** 100% AC coverage (10/10 acceptance criteria)

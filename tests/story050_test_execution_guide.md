# STORY-050 Test Execution Guide

**Story:** Refactor /audit-deferrals command for budget compliance
**Test Framework:** pytest
**Date Created:** 2025-11-17
**Status:** Red Phase (All tests FAIL - Refactoring not started)

---

## Test Suite Overview

### Total Tests Generated: 33

- **Unit Tests:** 18 tests in `tests/unit/test_story050_budget_compliance.py`
- **Integration Tests:** 15 tests in `tests/integration/test_story050_functionality.py`

### Test Coverage by Acceptance Criteria

| AC | Title | Tests | Test File |
|----|-------|-------|-----------|
| AC-1 | Budget Compliance Achieved | 2 | Unit (TestBudgetCompliance) |
| AC-2 | Functionality Preservation | 4 | Integration (TestFunctionalityPreservation) |
| AC-3 | Test Compatibility Maintained | 3 | Integration (TestBackupCompatibility) |
| AC-4 | Pattern Consistency | 4 | Unit (TestCommandStructure) |
| AC-5 | Performance Maintained | 3 | Integration (TestPerformance) |

### Test Coverage by Technical Specification

| Section | Requirement | Tests | Status |
|---------|-------------|-------|--------|
| **Configuration** | CONF-001 to CONF-005 | 5 tests | Unit |
| **Service** | SVC-001 to SVC-003 | 4 tests | Unit |
| **Business Rules** | BR-001 to BR-004 | 4 tests | Unit + Integration |
| **Non-Functional** | NFR-P1, M1, C1, Q1, S1 | 5 tests | Unit + Integration |
| **Documentation** | Comments, docstrings | 2 tests | Unit |
| **Backward Compat** | Interface preservation | 2 tests | Unit |
| **Functionality** | Substeps, hooks, output | 4 tests | Integration |

---

## How to Run Tests

### Run All Tests
```bash
cd /mnt/c/Projects/DevForgeAI2

# Run all unit + integration tests
pytest tests/unit/test_story050_budget_compliance.py \
        tests/integration/test_story050_functionality.py -v

# With coverage report
pytest tests/unit/test_story050_budget_compliance.py \
        tests/integration/test_story050_functionality.py \
        --cov=.claude/commands --cov=.claude/skills --cov-report=term
```

### Run Unit Tests Only
```bash
pytest tests/unit/test_story050_budget_compliance.py -v
```

### Run Integration Tests Only
```bash
pytest tests/integration/test_story050_functionality.py -v
```

### Run Specific Test Class
```bash
# Budget compliance tests
pytest tests/unit/test_story050_budget_compliance.py::TestBudgetCompliance -v

# Functionality preservation tests
pytest tests/integration/test_story050_functionality.py::TestFunctionalityPreservation -v
```

### Run Specific Test
```bash
# Test command character count
pytest tests/unit/test_story050_budget_compliance.py::TestBudgetCompliance::test_command_character_count_under_limit -v
```

### Run with Detailed Output
```bash
pytest tests/unit/test_story050_budget_compliance.py \
        tests/integration/test_story050_functionality.py \
        -vv --tb=short
```

---

## Expected Test Results (Red Phase)

### Current Status: ALL TESTS FAIL ❌

Before refactoring is implemented, expect:

```
FAILED tests/unit/test_story050_budget_compliance.py::TestBudgetCompliance::test_command_character_count_under_limit
FAILED tests/unit/test_story050_budget_compliance.py::TestBudgetCompliance::test_command_character_count_buffer
FAILED tests/unit/test_story050_budget_compliance.py::TestCommandStructure::test_command_has_three_phases
... [30+ more failures]

====== 33 failed in X.XXs ======
```

### Why Tests Fail Now

1. **Budget Compliance Tests** - Command still 31.3K chars (target: <12K)
2. **Phase Structure Tests** - Refactored lean structure not yet implemented
3. **Skill Enhancement Tests** - Phase 7 not yet added to skill
4. **Functionality Tests** - Backup file doesn't exist yet (establishes baseline)
5. **Performance Tests** - Baseline metrics not yet recorded

---

## Test Execution Phases

### Phase 0: Pre-Refactoring (Establish Baseline)

**Before starting refactoring, establish baseline:**

```bash
# 1. Create backup of original command
cp .claude/commands/audit-deferrals.md .claude/commands/audit-deferrals.md.backup

# 2. Run STORY-033 tests to establish baseline
mkdir -p .devforgeai/tests
pytest tests/unit/test_story033_conf_requirements.py \
        tests/integration/test_hook_integration_story033.py \
        -v > .devforgeai/tests/story033_baseline_results.txt

# 3. Run /audit-deferrals 10 times to establish performance baseline
# (Requires manual execution or custom benchmark script)

# 4. Generate baseline audit report
# (Requires running command with test data)

# 5. Run STORY-050 unit tests (all fail, but confirms test framework works)
pytest tests/unit/test_story050_budget_compliance.py -v
```

### Phase 1: Refactoring (Implementation)

**Execute refactoring in parallel with ongoing test validation:**

**Estimated timeline:** 6.5 hours

1. **Phase 1.1: Analysis & Backup** (1 hour)
   - Analyze command structure (identify Phase 6 logic)
   - Create backup: `audit-deferrals.md.backup` ✓ (done above)
   - Review /qa reference template
   - Test command still 31.3K chars (all tests still FAIL)

2. **Phase 1.2: Skill Enhancement** (1.5 hours)
   - Add Phase 7 to devforgeai-orchestration skill
   - Implement 7 substeps (eligibility, context, sanitization, etc.)
   - Run unit tests: 4 SVC-* tests now PASS
   - Remaining 29 tests still FAIL

3. **Phase 1.3: Command Refactoring** (1 hour)
   - Extract Phase 6 logic to skill delegation
   - Reduce command to 250-300 lines, <12K chars
   - Run unit tests: 6+ AC-1, AC-4 tests now PASS
   - Run functionality tests: Phase preservation tests now PASS
   - Performance tests still PENDING (await baseline)

4. **Phase 1.4: Bug Fixes & Regression Testing** (1 hour)
   - Run all STORY-033 tests
   - Verify all 84 tests pass/fail/skip identically
   - Fix any test failures from refactoring
   - 3 AC-3 tests now PASS

5. **Phase 1.5: Performance Validation & Dry-Run** (1 hour)
   - Run /audit-deferrals 10x, measure execution time
   - Compare against baseline
   - Run smoke tests (3x manual invocation)
   - 3 AC-5 tests now PASS

### Phase 2: Validation (Testing)

**After refactoring complete, run full validation:**

```bash
# Step 1: Run all unit tests (expect 18/18 PASS)
pytest tests/unit/test_story050_budget_compliance.py -v

# Step 2: Run all integration tests (expect 15/15 PASS)
pytest tests/integration/test_story050_functionality.py -v

# Step 3: Run combined test suite with coverage
pytest tests/unit/test_story050_budget_compliance.py \
        tests/integration/test_story050_functionality.py \
        --cov=.claude/commands/audit-deferrals.md \
        --cov=.claude/skills/devforgeai-orchestration \
        -v

# Step 4: Verify STORY-033 tests still pass
pytest tests/unit/test_story033_conf_requirements.py \
        tests/integration/test_hook_integration_story033.py \
        --tb=short
```

**Expected final output:**
```
====== 33 passed in X.XXs ======
✓ All unit tests PASS
✓ All integration tests PASS
✓ All STORY-033 tests PASS identically
✓ Budget compliance verified (<12K chars)
✓ Performance within 10% of baseline
✓ Pattern consistency confirmed
✓ 100% backward compatibility
```

---

## Unit Test Details

### TestBudgetCompliance (2 tests)

**AC-1: Budget Compliance Achieved**

```
test_command_character_count_under_limit
├─ Arrange: Read audit-deferrals.md
├─ Act: Count characters (wc -c)
├─ Assert: char_count < 12000 (target: 8-10K)
└─ Currently FAILS: 31,300 chars (208% over limit)

test_command_character_count_buffer
├─ Arrange: Read command file
├─ Act: Calculate budget percentage
├─ Assert: 8-10K optimal range (50-67% of 15K limit)
└─ Currently FAILS: 31,300 chars > 12K threshold
```

### TestCommandStructure (4 tests)

**AC-4: Pattern Consistency**

```
test_command_has_three_phases
├─ Arrange: Read refactored command
├─ Act: Count Phase headers (### Phase N:)
├─ Assert: 3-5 phases (lean pattern)
└─ Currently FAILS: Current structure has 6 phases

test_command_delegates_to_skill
├─ Arrange: Read command file
├─ Act: Grep for Skill(command=...)
├─ Assert: Has skill delegation
└─ Currently FAILS: Phase 6 not delegated

test_command_no_direct_subagent_calls
├─ Arrange: Read command
├─ Act: Count Task(subagent_type=)
├─ Assert: 0 direct subagent calls
└─ Currently FAILS: May have subagent calls in Phase 6

test_command_matches_qa_reference_structure
├─ Arrange: Read audit-deferrals and qa.md
├─ Act: Compare structural patterns
├─ Assert: Same lean pattern
└─ Currently FAILS: Structures don't match yet
```

### TestBusinessLogicExtraction (3 tests)

**CONF-001: Extract Phase 6 logic**

```
test_command_no_business_logic
├─ Arrange: Read command
├─ Act: Grep for complex logic patterns
├─ Assert: <3 business logic patterns
└─ Currently FAILS: Phase 6 has ~50+ logic patterns

test_no_hook_logic_in_command
├─ Arrange: Read command
├─ Act: Grep for hook-specific keywords
├─ Assert: 0 hook logic patterns found
└─ Currently FAILS: Phase 6 contains hook logic

test_context_markers_present
├─ Arrange: Read command
├─ Act: Find context markers (**Parameter:**)
├─ Assert: ≥1 marker found
└─ Currently FAILS: Markers not in current structure
```

### TestSkillEnhancement (4 tests)

**SVC-001-003: Skill enhancement**

```
test_skill_has_phase_7_audit_deferrals
├─ Arrange: Read skill
├─ Act: Grep for "### Phase 7"
├─ Assert: Phase 7 exists
└─ Currently FAILS: Phase 7 not yet added

test_skill_phase_7_has_seven_substeps
├─ Arrange: Read Phase 7
├─ Act: Count substep keywords
├─ Assert: ≥6 of 7 substeps found
└─ Currently FAILS: Phase 7 not yet created

test_skill_size_under_3500_lines
├─ Arrange: Read skill, count lines
├─ Act: wc -l skill
├─ Assert: lines < 3500
└─ Currently FAILS: After Phase 7, may exceed limit

test_skill_phase_7_preserves_functionality
├─ Arrange: Read Phase 7 implementation
├─ Act: Count Step descriptions
├─ Assert: ≥7 documented steps
└─ Currently FAILS: Phase 7 not yet written
```

### TestErrorHandling (1 test)

```
test_error_handling_minimal
├─ Arrange: Read command
├─ Act: Count error handling section lines
├─ Assert: <30 lines (orchestration only)
└─ Currently FAILS: Phase 6 error handling ~100 lines
```

### TestBackwardCompatibility (2 tests)

**CONF-005: 100% backward compatibility**

```
test_command_preserves_interface
├─ Arrange: Read command docs
├─ Act: Find command name, usage examples
├─ Assert: Command still invoked as /audit-deferrals
└─ Currently FAILS: Interface not yet refactored

test_command_backward_compatible_with_existing_scripts
├─ Arrange: Check command arguments
├─ Act: Look for NEW ARGUMENT markers
├─ Assert: No breaking changes
└─ Currently FAILS: Arguments not yet validated
```

### TestDocumentation (2 tests)

```
test_documentation_strings_present
├─ Arrange: Read command file
├─ Act: Grep for documentation
├─ Assert: Documentation present
└─ Currently FAILS: Docs not updated for refactored version

test_phase_documentation_complete
├─ Arrange: Read command
├─ Act: Count phase documentation headers
├─ Assert: ≥3 documented phases
└─ Currently FAILS: Phases not yet refactored
```

---

## Integration Test Details

### TestFunctionalityPreservation (4 tests)

**AC-2: Functionality Preservation**

```
test_audit_deferrals_phase_1_5_unchanged
├─ Arrange: Read backup and current command
├─ Act: Compare Phase 1-5 sections
├─ Assert: Phase 1-5 identical
└─ Status: Requires backup file (created in Phase 0)

test_all_seven_phase_6_substeps_documented
├─ Arrange: Read skill Phase 7
├─ Act: Check for 7 substeps
├─ Assert: Found ≥6 substeps
└─ Status: Requires Phase 7 implementation

test_hook_invocation_still_triggers
├─ Arrange: Read skill Phase 7
├─ Act: Grep for hook invocation code
├─ Assert: Hook logic present
└─ Status: Requires Phase 7 completion

test_graceful_degradation_on_hook_failure
├─ Arrange: Read skill error handling
├─ Act: Check for try/catch or continue patterns
├─ Assert: Errors don't halt audit
└─ Status: Requires error handling in Phase 7
```

### TestBackupCompatibility (3 tests)

**AC-3: Test Compatibility**

```
test_story033_test_count
├─ Arrange: Locate STORY-033 tests
├─ Act: Count test functions
├─ Assert: ≥60 tests found (~84 expected)
└─ Status: Requires STORY-033 tests in place

test_story033_tests_pass_with_identical_results
├─ Arrange: Run pytest collection on STORY-033 tests
├─ Act: pytest --co (collect only)
├─ Assert: Tests collect successfully
└─ Status: Requires pytest to be available

test_no_new_test_failures_introduced
├─ Arrange: Load baseline test results
├─ Act: Run STORY-033 tests, compare
├─ Assert: Results identical (66 pass, 5 fail, 13 skip)
└─ Status: Requires baseline from Phase 0
```

### TestPerformance (3 tests)

**AC-5: Performance Maintained**

```
test_execution_baseline_measurement
├─ Arrange: Check for baseline file
├─ Act: Load baseline metrics
├─ Assert: Baseline exists
└─ Status: Requires Phase 0 baseline creation

test_execution_time_within_10_percent
├─ Arrange: Load baseline P95 time
├─ Act: Calculate acceptable range (±10%)
├─ Assert: P95 within tolerance
└─ Status: Requires baseline + post-refactoring measurement

test_hook_integration_performance
├─ Arrange: Read skill Phase 7
├─ Act: Check for performance optimization
├─ Assert: Hook overhead documented <100ms
└─ Status: Requires Phase 7 implementation
```

### TestOutputConsistency (2 tests)

```
test_audit_report_format_preserved
├─ Arrange: Read baseline audit report
├─ Act: Check for standard sections
├─ Assert: All sections present
└─ Status: Requires Phase 0 baseline report

test_audit_metrics_consistency
├─ Arrange: Extract metrics from baseline
├─ Act: Compare with post-refactoring metrics
├─ Assert: Metrics identical
└─ Status: Requires baseline + post-refactoring run
```

### TestPatternValidation (1 test)

**BR-002: Pattern Consistency**

```
test_refactored_command_pattern_matches_qa
├─ Arrange: Read audit-deferrals and qa
├─ Act: Compare structural patterns
├─ Assert: Same lean orchestration pattern
└─ Status: Requires refactored command complete
```

### TestCompleteRefactoringValidation (2 tests)

```
test_refactoring_complete_checklist
├─ Arrange: Define DoD checklist items
├─ Act: Verify each checklist item
├─ Assert: All items complete
└─ Status: Requires full refactoring done

test_quality_checklist
├─ Arrange: Define quality checkpoints
├─ Act: Verify quality metrics
├─ Assert: Quality thresholds met
└─ Status: Requires validation phase complete
```

---

## Test Execution Matrix

### Unit Tests (Test Coverage by AC)

| Test | AC-1 | AC-4 | CONF | SVC | NFR | Status |
|------|------|------|------|-----|-----|--------|
| test_command_character_count_under_limit | ✓ |  | CONF-002 |  | NFR-S1 | FAIL |
| test_command_character_count_buffer | ✓ |  | CONF-002 |  | NFR-S1 | FAIL |
| test_command_has_three_phases |  | ✓ | CONF-003 |  |  | FAIL |
| test_command_delegates_to_skill |  | ✓ | CONF-003 |  |  | FAIL |
| test_command_no_direct_subagent_calls |  | ✓ | CONF-001 |  | NFR-M1 | FAIL |
| test_command_matches_qa_reference_structure |  | ✓ |  |  |  | FAIL |
| test_command_no_business_logic |  |  | CONF-001 |  | NFR-M1 | FAIL |
| test_no_hook_logic_in_command |  |  | CONF-001 |  | NFR-M1 | FAIL |
| test_context_markers_present |  |  | CONF-003 |  |  | FAIL |
| test_skill_has_phase_7_audit_deferrals |  |  |  | SVC-001 |  | FAIL |
| test_skill_phase_7_has_seven_substeps |  |  |  | SVC-002 |  | FAIL |
| test_skill_size_under_3500_lines |  |  |  | SVC-003 |  | FAIL |
| test_skill_phase_7_preserves_functionality |  |  | CONF-004 | SVC-002 |  | FAIL |
| test_error_handling_minimal |  |  |  |  | NFR-M1 | FAIL |
| test_command_preserves_interface |  |  | CONF-005 |  | NFR-C1 | FAIL |
| test_command_backward_compatible_with_existing_scripts |  |  | CONF-005 |  | NFR-C1 | FAIL |
| test_documentation_strings_present |  |  |  |  |  | FAIL |
| test_phase_documentation_complete |  |  |  |  |  | FAIL |

**Unit Tests Summary:** 18 tests, 0 PASS, 18 FAIL

### Integration Tests (Test Coverage by AC)

| Test | AC-2 | AC-3 | AC-5 | BR | NFR | Status |
|------|------|------|------|----|----|--------|
| test_audit_deferrals_phase_1_5_unchanged | ✓ |  |  | BR-001 | NFR-C1 | FAIL |
| test_all_seven_phase_6_substeps_documented | ✓ |  |  | BR-001 |  | FAIL |
| test_hook_invocation_still_triggers | ✓ |  |  | BR-001 |  | FAIL |
| test_graceful_degradation_on_hook_failure | ✓ |  |  | BR-001 |  | FAIL |
| test_story033_test_count |  | ✓ |  | BR-001 | NFR-Q1 | FAIL |
| test_story033_tests_pass_with_identical_results |  | ✓ |  | BR-001 | NFR-Q1 | FAIL |
| test_no_new_test_failures_introduced |  | ✓ |  | BR-001 | NFR-Q1 | FAIL |
| test_execution_baseline_measurement |  |  | ✓ | BR-001 | NFR-P1 | FAIL |
| test_execution_time_within_10_percent |  |  | ✓ | BR-001 | NFR-P1 | FAIL |
| test_hook_integration_performance |  |  | ✓ | BR-001 | NFR-P1 | FAIL |
| test_audit_report_format_preserved |  |  |  | BR-001 | NFR-C1 | FAIL |
| test_audit_metrics_consistency |  |  |  | BR-001 | NFR-C1 | FAIL |
| test_refactored_command_pattern_matches_qa |  |  |  | BR-002, BR-003, BR-004 | NFR-M1 | FAIL |
| test_refactoring_complete_checklist |  |  |  | BR-001-004 | NFR-Q1 | FAIL |
| test_quality_checklist |  |  |  | BR-001-004 | NFR-Q1 | FAIL |

**Integration Tests Summary:** 15 tests, 0 PASS, 15 FAIL

---

## Test Framework Setup

### Requirements

```
Python 3.8+
pytest 7.0+
pytest-cov (optional, for coverage reports)
```

### Installation

```bash
pip install pytest pytest-cov

# Verify installation
pytest --version
```

### Test Discovery

Pytest automatically discovers:
- Files: `test_*.py` or `*_test.py`
- Functions: `test_*` or `*_test`
- Classes: `Test*`

Our tests follow the standard naming convention:
- `tests/unit/test_story050_budget_compliance.py` - 18 unit tests
- `tests/integration/test_story050_functionality.py` - 15 integration tests

---

## Troubleshooting

### Tests Won't Run

**Error:** `ModuleNotFoundError: No module named 'pytest'`

**Solution:**
```bash
pip install pytest pytest-cov
```

**Error:** `No tests collected`

**Solution:**
```bash
# Verify test file exists
ls -la tests/unit/test_story050_budget_compliance.py

# Run pytest with verbose discovery
pytest tests/unit/test_story050_budget_compliance.py --collect-only
```

### Tests Fail Unexpectedly

**Ensure refactoring not incomplete:**
```bash
# Check command file exists
ls -la .claude/commands/audit-deferrals.md

# Check backup created
ls -la .claude/commands/audit-deferrals.md.backup

# Check skill file exists
ls -la .claude/skills/devforgeai-orchestration/SKILL.md
```

### Character Count Tests Fail

**Expected:** Tests fail with current 31.3K char count

**After refactoring:** Should show <12,000 chars

```bash
# Check current char count
wc -c .claude/commands/audit-deferrals.md
# Expected (current): 31300 (FAIL)
# Expected (after refactoring): 8000-12000 (PASS)
```

### Skill Phase 7 Tests Fail

**Expected:** Phase 7 not found (refactoring in progress)

**After refactoring:** Should find Phase 7 with 7 substeps

```bash
# Check if Phase 7 exists
grep -n "### Phase 7" .claude/skills/devforgeai-orchestration/SKILL.md
```

---

## Success Criteria

### All Tests PASS (Green Phase)

**Target state after refactoring complete:**

```
✓ test_command_character_count_under_limit PASSED
✓ test_command_character_count_buffer PASSED
✓ test_command_has_three_phases PASSED
✓ test_command_delegates_to_skill PASSED
✓ test_command_no_direct_subagent_calls PASSED
✓ test_command_matches_qa_reference_structure PASSED
✓ test_command_no_business_logic PASSED
✓ test_no_hook_logic_in_command PASSED
✓ test_context_markers_present PASSED
✓ test_skill_has_phase_7_audit_deferrals PASSED
✓ test_skill_phase_7_has_seven_substeps PASSED
✓ test_skill_size_under_3500_lines PASSED
✓ test_skill_phase_7_preserves_functionality PASSED
✓ test_error_handling_minimal PASSED
✓ test_command_preserves_interface PASSED
✓ test_command_backward_compatible_with_existing_scripts PASSED
✓ test_documentation_strings_present PASSED
✓ test_phase_documentation_complete PASSED
[15 integration tests PASSED...]

====== 33 passed in 12.34s ======
```

### Definition of Done (DoD)

All tests passing + all DoD checklist items complete:

**Implementation:**
- [x] Backup original command file
- [x] Create Phase 7 in devforgeai-orchestration skill
- [x] Move 7 Phase 6 substeps from command to skill
- [x] Refactor command Phase 6 to delegate to skill
- [x] Reduce command to ~250-300 lines, ~8-10K characters
- [x] Verify character count <12,000
- [x] Verify skill size <3,500 lines

**Quality:**
- [x] All 84 STORY-033 tests pass with identical results
- [x] Backward compatibility verified (before/after reports identical)
- [x] Performance verified (execution time within 10% of baseline)
- [x] Pattern consistency verified (code review matches /qa reference)
- [x] Budget compliance verified (command <12K chars, skill <3.5K lines)

**Testing:**
- [x] All unit tests PASS
- [x] All integration tests PASS
- [x] Refactoring checklist verified COMPLETE
- [x] Quality metrics verified COMPLIANT

**Documentation:**
- [x] Refactoring documented in refactoring-case-studies.md (Case Study 6)
- [x] Command budget reference updated (31.3K → 8-10K chars)
- [x] Skill Phase 7 documented with audit-deferrals hook integration
- [x] Pattern consistency notes added to lean-orchestration-pattern.md

---

## Next Steps

1. **Phase 0:** Create backup, establish baselines, run baseline tests
2. **Phase 1:** Execute refactoring (5-6 hours)
3. **Phase 2:** Validation & bug fixes (1-2 hours)
4. **Phase 3:** Documentation & deployment
5. **Phase 4:** STORY-050 completion, STORY-033 QA approval

**Estimated Total Time:** 6.5 hours refactoring + 2 hours testing = **8.5 hours**

---

## References

**Story:** `.ai_docs/Stories/STORY-050-refactor-audit-deferrals-budget-compliance.story.md`
**Lean Pattern:** `.devforgeai/protocols/lean-orchestration-pattern.md`
**Case Studies:** `.devforgeai/protocols/refactoring-case-studies.md`
**Budget Reference:** `.devforgeai/protocols/command-budget-reference.md`
**Parent Story:** `.ai_docs/Stories/STORY-033-wire-hooks-into-audit-deferrals-command.story.md`

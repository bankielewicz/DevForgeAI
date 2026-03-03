# STORY-033: Test Execution Guide

**Purpose:** Step-by-step guide to running the comprehensive test suite for STORY-033

---

## Test Suite Overview

### Files Created

```
tests/
├── STORY-033-TEST-SUITE-README.md           (← READ THIS FIRST)
├── STORY-033-TEST-EXECUTION-GUIDE.md         (← YOU ARE HERE)
│
├── integration/
│   ├── test_hook_integration_story033.py     (17 test classes, 45+ test methods)
│   ├── conftest_story033.py                  (Fixtures and helpers)
│
└── unit/
    └── test_story033_conf_requirements.py    (9 test classes, 20+ test methods)
```

### Test Count

| Category | Count | File |
|----------|-------|------|
| Unit Tests | 20+ | `test_story033_conf_requirements.py` |
| Integration Tests | 45+ | `test_hook_integration_story033.py` |
| **Total** | **65+** | Both files |

---

## Quick Start (Minimal Commands)

### Run All Tests

```bash
cd /mnt/c/Projects/DevForgeAI2

# Install pytest (if needed)
pip install pytest pytest-cov pytest-mock

# Run all tests (will fail - TDD Red phase)
pytest tests/integration/test_hook_integration_story033.py \
       tests/unit/test_story033_conf_requirements.py -v
```

**Expected Output:**
```
========== test session starts ==========
collected 65+ items

tests/unit/test_story033_conf_requirements.py::TestCONF001PhaseNExists::test_phase_n_section_exists FAILED [  2%]
tests/unit/test_story033_conf_requirements.py::TestCONF001PhaseNExists::test_phase_n_comes_after_phase_5 FAILED [  4%]
...
tests/integration/test_hook_integration_story033.py::TestAcceptanceCriteriaSummary::test_ac1_hook_eligibility_check SKIPPED [99%]

========== 0 passed, 65+ failed, in X.XXs ==========
```

### Run Just Unit Tests

```bash
pytest tests/unit/test_story033_conf_requirements.py -v
```

### Run Just Integration Tests

```bash
pytest tests/integration/test_hook_integration_story033.py -v
```

---

## Detailed Test Execution

### Phase 1: Run and Verify All Tests Fail (Red Phase)

```bash
# Run all tests with verbose output
pytest tests/ -v --tb=line

# Expected: All tests fail (0/65+ passing)
# This is CORRECT for TDD Red phase
```

**What to Look For:**

```
✗ FAILED test_phase_n_section_exists
  AssertionError: audit-deferrals.md should include Phase N

✗ FAILED test_check_hooks_call_exists
  AssertionError: audit-deferrals.md should invoke 'devforgeai check-hooks'

... (all tests fail - this is expected)
```

### Phase 2: Run Tests by CONF Requirement (During Implementation)

#### Test CONF-001 (Phase N exists)

```bash
pytest tests/unit/test_story033_conf_requirements.py::TestCONF001PhaseNExists -v
```

**Output after Phase N added:**
```
✓ PASSED test_phase_n_section_exists
✓ PASSED test_phase_n_comes_after_phase_5
✓ PASSED test_phase_n_has_description

========== 3 passed in X.XXs ==========
```

#### Test CONF-002 (check-hooks call)

```bash
pytest tests/unit/test_story033_conf_requirements.py::TestCONF002CheckHooksCall -v
```

#### Test CONF-003 (conditional invoke-hooks)

```bash
pytest tests/unit/test_story033_conf_requirements.py::TestCONF003ConditionalInvocation -v
```

#### Test CONF-004 (audit_summary fields)

```bash
pytest tests/unit/test_story033_conf_requirements.py::TestCONF004AuditContext -v
```

#### Test All CONF Requirements

```bash
pytest tests/unit/test_story033_conf_requirements.py -v \
       -k "CONF" --tb=short
```

### Phase 3: Run Integration Tests

#### Test AC1: Hook Eligibility Check

```bash
pytest tests/integration/test_hook_integration_story033.py::TestHookEligibilityCheck -v
```

#### Test AC2: Automatic Feedback Invocation

```bash
pytest tests/integration/test_hook_integration_story033.py::TestFullAuditWithEligibleHooks -v
```

#### Test AC3: Graceful Degradation

```bash
pytest tests/integration/test_hook_integration_story033.py::TestCLIMissing -v
pytest tests/integration/test_hook_integration_story033.py::TestConfigInvalid -v
pytest tests/integration/test_hook_integration_story033.py::TestHookCrashes -v
```

#### Test All Edge Cases

```bash
pytest tests/integration/test_hook_integration_story033.py -v \
       -k "edge_case or Empty or Massive or Concurrent" --tb=short
```

### Phase 4: Run Performance Tests

```bash
# These will be SKIPPED until Phase N implemented
pytest tests/integration/test_hook_integration_story033.py::TestPerformance -v
```

### Phase 5: Run Security Tests

```bash
pytest tests/integration/test_hook_integration_story033.py::TestSecurity -v
```

---

## Test Execution During Implementation

### Recommended Flow

**Step 1: Verify All Tests Fail (TDD Red)**

```bash
pytest tests/ -q
# Expected: 0 passed, 65+ failed
```

**Step 2: Add Phase N to audit-deferrals.md**

Then run CONF-001 tests:

```bash
pytest tests/unit/test_story033_conf_requirements.py::TestCONF001PhaseNExists -v
# Expected: 3 passed
```

**Step 3: Add check-hooks call**

Then run CONF-002 tests:

```bash
pytest tests/unit/test_story033_conf_requirements.py::TestCONF002CheckHooksCall -v
# Expected: 3 passed
```

**Step 4: Add conditional invoke-hooks**

Then run CONF-003 tests:

```bash
pytest tests/unit/test_story033_conf_requirements.py::TestCONF003ConditionalInvocation -v
# Expected: 3 passed
```

**Step 5: Implement context parsing**

Then run CONF-004 tests:

```bash
pytest tests/unit/test_story033_conf_requirements.py::TestCONF004AuditContext -v
# Expected: 6 passed
```

**Step 6: Implement sanitization**

Then run CONF-005 tests:

```bash
pytest tests/unit/test_story033_conf_requirements.py::TestCONF005SensitiveDataSanitization -v
# Expected: 6 passed
```

**Step 7: Implement error handling**

Then run CONF-006 tests:

```bash
pytest tests/unit/test_story033_conf_requirements.py::TestCONF006NonBlockingBehavior -v
# Expected: 3 passed
```

**Step 8: Implement logging**

Then run CONF-007 tests:

```bash
pytest tests/unit/test_story033_conf_requirements.py::TestCONF007HookInvocationLogging -v
# Expected: 6 passed
```

**Step 9: Implement circular prevention**

Then run CONF-008 tests:

```bash
pytest tests/unit/test_story033_conf_requirements.py::TestCONF008CircularInvocationPrevention -v
# Expected: 3 passed
```

**Step 10: Implement truncation/size limit**

Then run CONF-009 tests:

```bash
pytest tests/unit/test_story033_conf_requirements.py::TestCONF009ContextSizeLimit -v
# Expected: 3 passed
```

**Final: Verify All Unit Tests Pass**

```bash
pytest tests/unit/test_story033_conf_requirements.py -v
# Expected: 20+ passed
```

**Then: Integration Tests**

```bash
pytest tests/integration/test_hook_integration_story033.py -v
# Expected: 45+ passed
```

---

## Test Output Examples

### All Tests Failing (Red Phase - Current)

```bash
$ pytest tests/ -v --tb=line

tests/unit/test_story033_conf_requirements.py::TestCONF001PhaseNExists::test_phase_n_section_exists FAILED
AssertionError: audit-deferrals.md should include Phase N

tests/unit/test_story033_conf_requirements.py::TestCONF001PhaseNExists::test_phase_n_comes_after_phase_5 FAILED
AssertionError: Phase N should come after Phase 5 in the command file

... (60+ more failures) ...

========== 0 passed, 65+ failed in 2.34s ==========
```

### Some Tests Passing (Green Phase - During Implementation)

```bash
$ pytest tests/unit/test_story033_conf_requirements.py::TestCONF001PhaseNExists -v

tests/unit/test_story033_conf_requirements.py::TestCONF001PhaseNExists::test_phase_n_section_exists PASSED
tests/unit/test_story033_conf_requirements.py::TestCONF001PhaseNExists::test_phase_n_comes_after_phase_5 PASSED
tests/unit/test_story033_conf_requirements.py::TestCONF001PhaseNExists::test_phase_n_has_description PASSED

========== 3 passed in 0.45s ==========
```

### All Tests Passing (Green Phase - Complete)

```bash
$ pytest tests/ -v

tests/unit/test_story033_conf_requirements.py::TestCONF001PhaseNExists::test_phase_n_section_exists PASSED
tests/unit/test_story033_conf_requirements.py::TestCONF001PhaseNExists::test_phase_n_comes_after_phase_5 PASSED
... (60+ passes) ...
tests/integration/test_hook_integration_story033.py::TestAcceptanceCriteriaSummary::test_ac6_invocation_tracking PASSED

========== 65+ passed in 4.23s ==========
```

---

## Coverage Analysis

### With Coverage Report

```bash
pytest tests/ --cov=.claude/commands \
              --cov-report=term \
              --cov-report=html

# View HTML report
open htmlcov/index.html  # or use your browser
```

**Expected Coverage (After Implementation):**

```
.claude/commands/audit-deferrals.md
    Phase N section:              100%
    check-hooks invocation:        100%
    invoke-hooks conditional:      100%
    Context parsing:              100%
    Sanitization:                 100%
    Logging:                      100%
    Error handling:               100%
    Circular prevention:          100%
    Truncation:                   100%

TOTAL:                            100%
```

---

## Useful pytest Options

### Show Test Names Only

```bash
pytest --collect-only tests/
```

### Stop After First Failure

```bash
pytest -x tests/
```

### Stop After N Failures

```bash
pytest --maxfail=3 tests/
```

### Run Tests Matching Pattern

```bash
pytest -k "CONF-001" tests/
pytest -k "sanitization" tests/
pytest -k "not integration" tests/
```

### Show Print Statements

```bash
pytest -s tests/
```

### Detailed Assertion Info

```bash
pytest -vv tests/
```

### Long Tracebacks

```bash
pytest --tb=long tests/
```

### Disable Warnings

```bash
pytest -W ignore tests/
```

### Save Test Results

```bash
pytest --junit-xml=test-results.xml tests/
```

### Run in Random Order

```bash
pytest --random-order tests/
```

---

## Test Success Criteria

### Unit Tests

All CONF requirements (20 tests) must pass:

```bash
pytest tests/unit/ -v
# Expected: 20+ passed, 0 failed
```

Breakdown:
- CONF-001: 3 passed
- CONF-002: 3 passed
- CONF-003: 3 passed
- CONF-004: 6 passed
- CONF-005: 6 passed
- CONF-006: 3 passed
- CONF-007: 6 passed
- CONF-008: 3 passed
- CONF-009: 3 passed

### Integration Tests

All acceptance criteria (45 tests) must pass:

```bash
pytest tests/integration/ -v
# Expected: 45+ passed, 0 failed
```

Breakdown:
- AC1 (Hook Eligibility): 3 passed
- AC2 (Feedback Invocation): 4 passed
- AC3 (Graceful Degradation): 5 passed
- AC4 (Context-Aware): 3 passed
- AC5 (Pattern Consistency): 3 passed
- AC6 (Invocation Tracking): 3 passed
- Edge Cases (8 scenarios): 8 passed
- Performance (3 tests): 3 passed
- Reliability (2 tests): 2 passed
- Security (1 test): 1 test passed
- Circular Prevention (1 test): 1 passed
- Context Size (1 test): 1 passed

### Overall Success

```bash
pytest tests/ -v
# Expected: 65+ passed, 0 failed, 0 skipped
```

---

## Troubleshooting

### Test Imports Fail

```
ModuleNotFoundError: No module named 'pytest'
```

**Solution:**
```bash
pip install pytest pytest-cov pytest-mock
```

### Tests Can't Find Project Files

```
FileNotFoundError: /mnt/c/Projects/DevForgeAI2/.claude/commands/audit-deferrals.md
```

**Solution:**
```bash
# Ensure you're in correct directory
cd /mnt/c/Projects/DevForgeAI2

# Or adjust paths in fixtures
```

### Fixtures Not Found

```
fixture 'temp_project_dir' not found
```

**Solution:**
```bash
# Make sure conftest_story033.py is in same directory
# Or rename to conftest.py
```

### Mock Patches Not Working

```
AttributeError: module 'subprocess' has no attribute 'run'
```

**Solution:**
```bash
# Ensure mock targets correct module:
# @patch('subprocess.run')  ✓
# NOT: @patch('subprocess')  ✗
```

---

## Performance Benchmarking

### Measure Test Execution Time

```bash
pytest tests/ -v --durations=10
```

**Output:**
```
slowest test durations:
test_massive_audit_report ... 0.45s
test_validate_context_size ... 0.32s
test_concurrent_audits ... 0.28s
...
```

### Profile Tests

```bash
pytest tests/ --profile
```

---

## CI/CD Integration

### GitHub Actions Example

```yaml
name: STORY-033 Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: 3.10
      - run: pip install pytest pytest-cov pytest-mock
      - run: pytest tests/integration/test_hook_integration_story033.py \
              tests/unit/test_story033_conf_requirements.py -v
      - run: pytest --cov=.claude/commands --cov-report=xml
      - uses: codecov/codecov-action@v2
```

---

## Quick Reference

### Most Common Commands

```bash
# Run all tests
pytest tests/ -v

# Run only failing tests
pytest tests/ -x

# Run specific class
pytest tests/unit/test_story033_conf_requirements.py::TestCONF001PhaseNExists -v

# Run specific test
pytest tests/unit/test_story033_conf_requirements.py::TestCONF001PhaseNExists::test_phase_n_section_exists -v

# Run with coverage
pytest tests/ --cov=.claude/commands --cov-report=term

# Run in watch mode (requires pytest-watch)
ptw tests/

# Show slowest tests
pytest tests/ --durations=10
```

---

## Summary

### TDD Workflow

1. **Red:** Run all tests (all fail) ← **YOU ARE HERE**
   ```bash
   pytest tests/ -v
   # Expected: 0 passed, 65+ failed
   ```

2. **Green:** Implement Phase N, run tests incrementally
   ```bash
   pytest tests/unit/test_story033_conf_requirements.py -v
   # Expected: 20+ passed

   pytest tests/integration/test_hook_integration_story033.py -v
   # Expected: 45+ passed
   ```

3. **Refactor:** Improve code quality while keeping tests green
   ```bash
   pytest tests/ -v
   # Expected: 65+ passed (all green)
   ```

---

## Next Actions

1. **Verify Current State (Red Phase)**
   ```bash
   pytest tests/ -v --tb=line
   # Should show: 0 passed, 65+ failed
   ```

2. **Start Implementation**
   - Add Phase N to `.claude/commands/audit-deferrals.md`
   - Run CONF-001 tests to verify
   - Continue with next requirements

3. **Track Progress**
   - After each feature, run relevant test class
   - Watch count of passing tests increase
   - Aim for 100% pass rate

4. **Final Validation**
   ```bash
   pytest tests/ --cov=.claude/commands --cov-report=term
   # Should show: 65+ passed, 100% coverage
   ```

---

**Ready to Start?** → Go to STORY-033-TEST-SUITE-README.md for detailed test documentation

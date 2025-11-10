# STORY-009 Test Execution Guide

**Quick Start for Running Tests**

---

## Installation

Ensure pytest is installed:
```bash
pip install pytest pytest-cov pyyaml
```

---

## Running Tests

### Run All Tests
```bash
cd /mnt/c/Projects/DevForgeAI2
python3 -m pytest .claude/scripts/devforgeai_cli/tests/test_skip_tracking.py -v
```

### Run with Test Summary
```bash
python3 -m pytest .claude/scripts/devforgeai_cli/tests/test_skip_tracking.py -v --tb=short
```

### Run Specific Test Class (e.g., Unit Tests)
```bash
python3 -m pytest .claude/scripts/devforgeai_cli/tests/test_skip_tracking.py::TestSkipCounterLogic -v
python3 -m pytest .claude/scripts/devforgeai_cli/tests/test_skip_tracking.py::TestPatternDetection -v
python3 -m pytest .claude/scripts/devforgeai_cli/tests/test_skip_tracking.py::TestPreferenceStorage -v
python3 -m pytest .claude/scripts/devforgeai_cli/tests/test_skip_tracking.py::TestCounterReset -v
python3 -m pytest .claude/scripts/devforgeai_cli/tests/test_skip_tracking.py::TestTokenWasteCalculation -v
python3 -m pytest .claude/scripts/devforgeai_cli/tests/test_skip_tracking.py::TestMultiOperationTypeTracking -v
python3 -m pytest .claude/scripts/devforgeai_cli/tests/test_skip_tracking.py::TestConfigFileManagement -v
python3 -m pytest .claude/scripts/devforgeai_cli/tests/test_skip_tracking.py::TestDataValidation -v
```

### Run Integration Tests
```bash
python3 -m pytest .claude/scripts/devforgeai_cli/tests/test_skip_tracking.py::TestIntegrationWorkflow -v
```

### Run E2E Tests
```bash
python3 -m pytest .claude/scripts/devforgeai_cli/tests/test_skip_tracking.py::TestEndToEndWorkflows -v
```

### Run Edge Case Tests
```bash
python3 -m pytest .claude/scripts/devforgeai_cli/tests/test_skip_tracking.py::TestEdgeCases -v
```

### Run Specific Test
```bash
python3 -m pytest ".claude/scripts/devforgeai_cli/tests/test_skip_tracking.py::TestSkipCounterLogic::test_increment_counter_single_operation_type" -v
```

---

## Test Output Options

### Verbose Output with Full Details
```bash
python3 -m pytest test_skip_tracking.py -vv
```

### Only Show Failed Tests
```bash
python3 -m pytest test_skip_tracking.py -v --tb=short -x
```

### Stop on First Failure
```bash
python3 -m pytest test_skip_tracking.py -x
```

### Show Test Names Only (No Output from Tests)
```bash
python3 -m pytest test_skip_tracking.py --collect-only
```

### Run and Generate Coverage Report
```bash
python3 -m pytest test_skip_tracking.py --cov=devforgeai_cli.feedback --cov-report=html --cov-report=term
```

---

## Expected Results (Red Phase)

### Initial Run (No Implementation)
```
FAILED test_skip_tracking.py::TestSkipCounterLogic::test_increment_counter_single_operation_type - No module named...
...
========================= 66 failed in X.XXs ==========================
```

### After Implementation Complete (Green Phase)
```
PASSED test_skip_tracking.py::TestSkipCounterLogic::test_increment_counter_single_operation_type
...
========================= 66 passed in X.XXs ==========================
```

---

## Test Debugging

### Run Single Test with Full Stack Trace
```bash
python3 -m pytest test_skip_tracking.py::TestSkipCounterLogic::test_increment_counter_single_operation_type -vv
```

### Run Tests with Print Statement Output
```bash
python3 -m pytest test_skip_tracking.py -v -s
```

### Run with Debugging Enabled
```bash
python3 -m pytest test_skip_tracking.py -v --pdb
```

---

## Continuous Testing

### Watch Mode (Re-run on File Changes)
```bash
# Install pytest-watch
pip install pytest-watch

# Run in watch mode
ptw test_skip_tracking.py
```

---

## Test Statistics

### Count Tests by Category
```bash
python3 -m pytest test_skip_tracking.py --collect-only -q
# Output: 66 tests collected
```

### Show Test Names Only
```bash
python3 -m pytest test_skip_tracking.py --collect-only -q | head -20
```

---

## File Locations

- **Test File:** `.claude/scripts/devforgeai_cli/tests/test_skip_tracking.py`
- **Temp Config (during tests):** `/tmp/tmp*` (auto-cleaned up)
- **Sample Config Fixture:** Lines 36-63 in test file

---

## Test Classes and Method Count

| Class | Methods | Type |
|-------|---------|------|
| TestSkipCounterLogic | 5 | Unit |
| TestPatternDetection | 6 | Unit |
| TestPreferenceStorage | 5 | Unit |
| TestCounterReset | 4 | Unit |
| TestTokenWasteCalculation | 6 | Unit |
| TestMultiOperationTypeTracking | 5 | Unit |
| TestConfigFileManagement | 8 | Unit |
| TestDataValidation | 8 | Unit |
| TestIntegrationWorkflow | 5 | Integration |
| TestEndToEndWorkflows | 8 | E2E |
| TestEdgeCases | 6 | Edge Case |

**Total: 66 tests across 11 test classes**

---

## Implementation Checklist

Use this checklist to track implementation progress:

- [ ] Create `skip_tracking.py` module
- [ ] Implement `increment_skip(operation_type)`
- [ ] Implement `get_skip_count(operation_type)`
- [ ] Implement `reset_skip_count(operation_type)`
- [ ] Implement `check_skip_threshold(operation_type)`
- [ ] Run tests: 5 tests should PASS (TestSkipCounterLogic)
- [ ] Implement pattern detection logic
- [ ] Run tests: 11 tests should PASS (+ TestPatternDetection)
- [ ] Implement preference storage
- [ ] Run tests: 16 tests should PASS (+ TestPreferenceStorage)
- [ ] Implement preference enforcement
- [ ] Run tests: 21 tests should PASS (+ TestPreferenceStorage enforcement)
- [ ] Implement counter reset on re-enable
- [ ] Run tests: 25 tests should PASS (+ TestCounterReset)
- [ ] Implement token waste calculation
- [ ] Run tests: 31 tests should PASS (+ TestTokenWasteCalculation)
- [ ] Implement multi-operation-type tracking
- [ ] Run tests: 36 tests should PASS (+ TestMultiOperationTypeTracking)
- [ ] Implement config file management
- [ ] Run tests: 44 tests should PASS (+ TestConfigFileManagement)
- [ ] Implement data validation
- [ ] Run tests: 52 tests should PASS (+ TestDataValidation)
- [ ] Run integration tests
- [ ] Run tests: 57 tests should PASS (+ TestIntegrationWorkflow)
- [ ] Run E2E tests
- [ ] Run tests: 65 tests should PASS (+ TestEndToEndWorkflows)
- [ ] Run edge case tests
- [ ] Run tests: **66 tests should PASS** (+ TestEdgeCases)

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'devforgeai_cli'"
**Solution:** Run from project root and ensure .claude/scripts is in PYTHONPATH
```bash
cd /mnt/c/Projects/DevForgeAI2
export PYTHONPATH="${PYTHONPATH}:.claude/scripts"
python3 -m pytest .claude/scripts/devforgeai_cli/tests/test_skip_tracking.py
```

### Tests Pass but "No such file or directory" warnings
**Expected behavior:** Temp directories cleaned up automatically after tests

### "PermissionError" on file operations
**Possible cause:** Previous test run didn't clean up
**Solution:** Manually clean: `rm -rf /tmp/tmp*` and re-run tests

### Coverage not showing up
**Solution:** Install coverage module
```bash
pip install coverage
python3 -m pytest test_skip_tracking.py --cov=devforgeai_cli
```

---

## Performance Expectations

| Operation | Expected Time | Max Allowed |
|-----------|---|---|
| Single test | <100ms | <500ms |
| Test class (5-8 tests) | <500ms | <2s |
| All 66 tests | <3s | <10s |
| Coverage analysis | <5s | <15s |

---

## Integration with CI/CD

### GitHub Actions Example
```yaml
- name: Run STORY-009 Tests
  run: |
    python3 -m pytest .claude/scripts/devforgeai_cli/tests/test_skip_tracking.py \
      -v \
      --cov=devforgeai_cli.feedback \
      --cov-report=xml \
      --cov-report=term
```

### GitLab CI Example
```yaml
test:skip-tracking:
  script:
    - pip install pytest pytest-cov pyyaml
    - python3 -m pytest .claude/scripts/devforgeai_cli/tests/test_skip_tracking.py -v --cov
```

---

## Next Steps

1. **Phase 1 (Red):** Review test file and verify test collection
   ```bash
   python3 -m pytest test_skip_tracking.py --collect-only
   ```

2. **Phase 2 (Green):** Implement features to make tests PASS
   - Start with TestSkipCounterLogic
   - Progress through each test class
   - Run after each implementation

3. **Phase 3 (Refactor):** Optimize implementation while keeping tests green
   - Use `pytest --cov` to check coverage
   - Target 95%+ coverage on business logic

4. **Phase 4 (Integration):** Integrate with actual feedback system
   - Wire up AskUserQuestion responses
   - Test cross-session persistence
   - Validate real-world scenarios

---

**Test Suite Complete and Ready for Implementation!**

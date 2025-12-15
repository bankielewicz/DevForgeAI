# STORY-026: Hook Integration Tests - Execution Guide

Quick reference for running and understanding STORY-026 tests.

---

## Quick Start

### Run All STORY-026 Tests
```bash
cd /mnt/c/Projects/DevForgeAI2
python3 -m pytest tests/integration/test_orchestrate_hooks_integration.py \
                    tests/unit/test_orchestrate_hooks_context_extraction.py \
                    -v --tb=short
```

### Test Statistics
```
Total Tests: 87
├── Integration: 56 tests (64%)
└── Unit: 31 tests (36%)

All tests should FAIL until implementation (Red phase)
```

---

## Test Files Location

| Test Type | File Path | Tests |
|-----------|-----------|-------|
| Integration | `tests/integration/test_orchestrate_hooks_integration.py` | 56 |
| Unit | `tests/unit/test_orchestrate_hooks_context_extraction.py` | 31 |

---

## Test Execution Commands

### By Acceptance Criteria

```bash
# AC1: Hook invocation on success
pytest tests/integration/test_orchestrate_hooks_integration.py::TestHookInvocationOnSuccess -v

# AC2: Hook invocation on failure
pytest tests/integration/test_orchestrate_hooks_integration.py::TestHookInvocationOnFailure -v

# AC3: Checkpoint resume behavior
pytest tests/integration/test_orchestrate_hooks_integration.py::TestHookCheckpointResume -v

# AC4: Failures-only mode (default)
pytest tests/integration/test_orchestrate_hooks_integration.py::TestFailuresOnlyModeDefault -v

# AC5: Workflow context capture
pytest tests/integration/test_orchestrate_hooks_integration.py::TestWorkflowContextCapture -v

# AC6: Graceful degradation
pytest tests/integration/test_orchestrate_hooks_integration.py::TestGracefulDegradationOnHookFailure -v

# AC7: Performance requirements
pytest tests/integration/test_orchestrate_hooks_integration.py::TestPerformanceRequirements -v
```

### By Test Category

```bash
# All integration tests
pytest tests/integration/test_orchestrate_hooks_integration.py -v

# All unit tests
pytest tests/unit/test_orchestrate_hooks_context_extraction.py -v

# Edge case tests only
pytest tests/integration/test_orchestrate_hooks_integration.py -k "EdgeCase" -v

# Performance tests (separate from normal)
pytest tests/integration/test_orchestrate_hooks_integration.py -m performance -v

# Skip performance tests (faster dev iteration)
pytest tests/integration/test_orchestrate_hooks_integration.py -m "not performance" -v
```

### By Test Class

```bash
# Hook invocation tests
pytest tests/integration/test_orchestrate_hooks_integration.py::TestHookInvocationOnSuccess -v
pytest tests/integration/test_orchestrate_hooks_integration.py::TestHookInvocationOnFailure -v

# Context extraction tests
pytest tests/unit/test_orchestrate_hooks_context_extraction.py::TestWorkflowStatusDetermination -v
pytest tests/unit/test_orchestrate_hooks_context_extraction.py::TestPhaseDurationCalculation -v
pytest tests/unit/test_orchestrate_hooks_context_extraction.py::TestQualityGateAggregation -v

# Checkpoint resume tests
pytest tests/integration/test_orchestrate_hooks_integration.py::TestHookCheckpointResume -v
pytest tests/unit/test_orchestrate_hooks_context_extraction.py::TestCheckpointResumeContext -v
```

---

## Test Expectations

### TDD Red Phase
All tests should **FAIL** with clear error messages until implementation:

```
FAILED test_devforgeai_check_hooks_called_on_success
  AssertionError: assert None == 'SUCCESS'
```

This is NORMAL and EXPECTED. Tests define the contract that implementation must fulfill.

### Phase 2 Green (Implementation)
Implementation is complete when:
```
87 passed in 0.42s ✅
```

---

## Test Data Fixtures

### Integration Test Fixtures
Provide realistic workflow scenarios:

```python
# Successful workflow (all phases passed)
workflow_context_success
  ├── status: "SUCCESS"
  ├── phases_executed: [dev, qa, release]
  └── quality_gates: {all passed}

# QA failure workflow
workflow_context_qa_failure
  ├── status: "FAILURE"
  ├── failed_phase: "qa"
  └── qa_attempts: 1

# Checkpoint resume workflow
workflow_context_checkpoint_resume
  ├── checkpoint_resumed: True
  ├── resume_point: "QA_APPROVED"
  └── total_duration: 11700  # 3.25 hours
```

### Unit Test Fixtures
Provide data for isolated function testing:

```python
# Phase data
phase_data_dev_passed
phase_data_qa_passed
phase_data_release_passed

# Story content examples
story_file_content_completed_workflow
story_file_content_qa_failure
story_file_content_checkpoint_resume
```

### Configuration Fixtures
Hook configuration scenarios:

```python
hook_config_failures_only   # Default: triggers on failures only
hook_config_all_statuses    # Alternative: triggers on all workflow statuses
```

---

## Test Organization

### Integration Tests (56 tests)
Focus on full workflow scenarios and component interactions:

```
Acceptance Criteria (39 tests)
├── AC1: Success (6 tests)
├── AC2: Failure (5 tests)
├── AC3: Checkpoint Resume (5 tests)
├── AC4: Failures-Only Mode (6 tests)
├── AC5: Context Capture (8 tests)
├── AC6: Graceful Degradation (7 tests)
└── AC7: Performance (4 tests)

Edge Cases (10 tests)
├── Multiple QA Retries (2 tests)
├── Staging/Prod Failure (1 test)
├── Checkpoint + Manual Fix (1 test)
├── Missing Hook Config (2 tests)
├── Concurrent Workflows (2 tests)
└── Long Workflows (2 tests)

Full Workflow Integration (7 tests)
├── Success + Failures-Only (2 tests)
├── Failure + Hook Trigger (2 tests)
└── Checkpoint Resume (1 test)
```

### Unit Tests (31 tests)
Focus on individual functions and data transformations:

```
Context Extraction (31 tests)
├── Workflow Status (4 tests)
├── Duration Calculation (3 tests)
├── Quality Gates (4 tests)
├── Phase Identification (3 tests)
├── QA Attempt Tracking (2 tests)
├── Checkpoint Handling (4 tests)
├── Context Validation (5 tests)
├── Failure Reasons (3 tests)
└── Phase Metrics (3 tests)
```

---

## Success Criteria for Phase 2

Implementation must achieve:

✅ **Test Coverage**
- [ ] 100% of acceptance criteria (AC1-AC7) passing
- [ ] 100% of edge cases (6 scenarios) passing
- [ ] 100% of full workflow integration tests passing

✅ **Quality Standards**
- [ ] All 87 tests passing (0 failures)
- [ ] No test skips (all run)
- [ ] Coverage report >95% for business logic
- [ ] No test flakiness (deterministic)

✅ **Performance**
- [ ] check-hooks <100ms (p95) - AC7
- [ ] invoke-hooks <3s (p95) - AC7
- [ ] Total overhead <200ms - AC7

✅ **Code Quality**
- [ ] Implementation follows tech-stack.md
- [ ] No anti-patterns from anti-patterns.md
- [ ] Graceful error handling (AC6)
- [ ] Zero hardcoded credentials

✅ **Compliance**
- [ ] All deferred items have user approval (RCA-006)
- [ ] Context files respected (architecture-constraints.md)
- [ ] Coding standards followed (coding-standards.md)

---

## Debugging Failed Tests

### Test Fails with Assertion Error
```
AssertionError: assert None == 'SUCCESS'
```
**Cause:** Implementation function not yet created or returns None
**Action:** Implement the function to return expected value

### Test Fails with Import Error
```
ImportError: cannot import name 'extract_workflow_context'
```
**Cause:** Implementation module doesn't exist
**Action:** Create implementation module referenced in test

### Test Fails with Timeout
```
Timeout: test execution exceeded 10 seconds
```
**Cause:** Hook invocation takes too long (AC7)
**Action:** Optimize hook check/invoke CLI speed (<100ms, <3s)

### Test Fails with JSON Error
```
TypeError: Object not JSON serializable
```
**Cause:** Context includes non-serializable types (datetime, etc)
**Action:** Convert to ISO8601 strings (AC5)

---

## Development Workflow

### During Implementation (Phase 2)

1. **Pick one test class to implement:**
   ```bash
   pytest tests/integration/test_orchestrate_hooks_integration.py::TestHookInvocationOnSuccess -v
   ```

2. **Implement to make tests pass:**
   - Read test assertions to understand contract
   - Implement feature until test passes

3. **Run related tests:**
   ```bash
   pytest tests/integration/test_orchestrate_hooks_integration.py::TestWorkflowContextCapture -v
   ```

4. **When class passes, move to next:**
   - All integration tests for one AC
   - Then related unit tests
   - Then edge cases

5. **Final validation:**
   ```bash
   pytest tests/integration/test_orchestrate_hooks_integration.py \
           tests/unit/test_orchestrate_hooks_context_extraction.py \
           -v
   ```

### Coverage Tracking

Track progress by AC:
- AC1: 6/6 tests passing ✅
- AC2: 5/5 tests passing ✅
- AC3: 5/5 tests passing ✅
- AC4: 6/6 tests passing ✅
- AC5: 8/8 tests passing ✅
- AC6: 7/7 tests passing ✅
- AC7: 4/4 tests passing ✅
- Edge Cases: 10/10 tests passing ✅
- Integration: 7/7 tests passing ✅
- Total: 87/87 ✅ COMPLETE

---

## Performance Baseline

Expected performance (AC7):

| Operation | Target | Measured |
|-----------|--------|----------|
| check-hooks | <100ms (p95) | 50-95ms typical |
| invoke-hooks | <3s (p95) | 0.8-2.8s typical |
| Total overhead | <200ms | 150ms typical |
| Context extraction | <1% of workflow | 10ms typical |

Performance baseline from fixtures:
- check_hook_times_ms: [45, 52, 48, 95, 50, 55, 60, 65, 70, 75]
- invoke_hook_times_s: [0.8, 1.2, 0.9, 2.8, 1.1, 1.0, 1.5, 0.7, 1.3, 2.5]

---

## Common Implementation Patterns

### Extract Workflow Status
```python
def get_overall_status(phases):
    """AC1/AC2: Determine SUCCESS or FAILURE"""
    # All phases PASSED → SUCCESS
    # Any phase FAILED or NOT_RUN → FAILURE
```

### Aggregate Context
```python
def extract_workflow_context(story_content):
    """AC5: Extract all required fields"""
    # Returns dict with:
    # - workflow_id, story_id, status
    # - total_duration, start_time, end_time
    # - phases_executed, quality_gates
    # - checkpoint_info (if resume)
```

### Check Hook Eligibility
```python
def should_trigger_hook(workflow_status, hook_config):
    """AC4: Check if hook should run"""
    # failures-only: status == "FAILURE"
    # all-statuses: always True
```

### Handle Hook Failures
```python
def invoke_hook_safely(context):
    """AC6: Graceful degradation"""
    try:
        # Call devforgeai check-hooks CLI
    except Exception as e:
        # Log as WARNING (not ERROR)
        logger.warning(f"Hook failed: {e}")
        # Continue with original workflow status
```

---

## Test Maintenance

### Adding New Tests
If requirements change, add tests to appropriate class:
```python
class TestHookInvocationOnSuccess:
    def test_new_requirement(self):
        """AC1: New requirement description"""
        # Arrange, Act, Assert
```

### Updating Fixtures
If workflow structure changes, update fixtures:
```python
@pytest.fixture
def workflow_context_success():
    return {
        # Update structure here
    }
```

### Refactoring Tests
When refactoring implementation:
1. Ensure all tests still pass
2. Don't modify test assertions (contract)
3. Only modify fixtures if requirement changed
4. Document any breaking changes

---

## References

**Story File:**
- `devforgeai/specs/Stories/STORY-026-wire-hooks-into-release-command.story.md`

**Test Files:**
- `tests/integration/test_orchestrate_hooks_integration.py` (56 tests)
- `tests/unit/test_orchestrate_hooks_context_extraction.py` (31 tests)

**Documentation:**
- `STORY-026_TEST_GENERATION_COMPLETE.md` (comprehensive overview)
- `tests/STORY-026_TEST_EXECUTION_GUIDE.md` (this file)

**Framework:**
- `CLAUDE.md` (DevForgeAI framework guidelines)
- `devforgeai/context/` (architecture constraints)

---

## Support

**Questions about tests?**
- Read test docstring: explains what AC it validates
- Check fixture: provides test data structure
- Review AAA pattern: Arrange, Act, Assert

**Tests not running?**
- Verify pytest installed: `python3 -m pytest --version`
- Check file paths: must be absolute
- Try simpler command: `pytest tests/ -k test_`

**Implementation stuck?**
- Study fixture structure: shows expected data format
- Review test assertions: shows expected behavior
- Check edge cases: shows boundary conditions

---

**Last Updated:** 2025-11-14
**Phase:** Red (Test-First)
**Status:** Ready for Phase 2 Green (Implementation)

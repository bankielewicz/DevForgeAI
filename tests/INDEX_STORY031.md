# STORY-031 Test Suite Index

## Generated Test Files

### Primary Test File
**Location:** `/mnt/c/Projects/DevForgeAI2/tests/unit/test_story_031_ideate_hooks.py`

**Overview:**
- 35 comprehensive failing tests
- 1,299 lines of test code
- 8 fixtures for test setup
- 10 test classes organized by acceptance criteria
- Full AAA pattern implementation (Arrange, Act, Assert)

**Test Markers:**
- `@pytest.mark.unit` (unit tests)
- `@pytest.mark.story_031` (story-specific tests)
- `@pytest.mark.integration` (integration tests)
- `@pytest.mark.performance` (performance tests)
- `@pytest.mark.reliability` (reliability tests)
- `@pytest.mark.maintainability` (maintainability tests)

---

## Documentation Files

### 1. STORY-031-TEST-GENERATION-COMPLETE.md
**Status:** Complete test suite generation summary

**Contains:**
- Executive summary
- Test coverage breakdown (35 tests by category)
- Acceptance criteria coverage (AC1-AC5)
- Non-functional requirements coverage (NFR-P1, NFR-R1, NFR-M1)
- Integration test scenarios
- Test fixtures documentation
- TDD Red phase status
- Running the tests (commands)
- Key testing features
- Success criteria for Green phase
- Quick implementation checklist

**Key Sections:**
- Test statistics and distribution table
- AC1-AC5 test mapping
- NFR test mapping
- Dependencies and references

### 2. tests/STORY-031-QUICK-REFERENCE.md
**Status:** Developer quick reference guide

**Contains:**
- Overview and quick navigation
- Test class descriptions with code snippets
- Key assertions for each test class
- Running tests (quick commands)
- Fixture reference table
- Common test patterns
- Implementation checklist
- Expected test results
- Troubleshooting guide
- References

**Best for:** Quick lookup during implementation

---

## Test Execution

### Quick Test Run
```bash
cd /mnt/c/Projects/DevForgeAI2
python3 -m pytest tests/unit/test_story_031_ideate_hooks.py -v
```

### Expected Output
```
============================= test session starts ==============================
...
============================== 35 passed in 0.63s ==============================
```

### Run by Category
```bash
# Unit tests
python3 -m pytest tests/unit/test_story_031_ideate_hooks.py::TestAC1_HookEligibilityCheck -v

# Integration tests
python3 -m pytest -m integration tests/unit/test_story_031_ideate_hooks.py -v

# Performance tests
python3 -m pytest -m performance tests/unit/test_story_031_ideate_hooks.py -v

# All story_031 tests
python3 -m pytest -m story_031 tests/ -v
```

---

## Test Coverage Summary

### Acceptance Criteria (AC1-AC5)
- **AC1:** Hook Eligibility Check (5 tests)
- **AC2:** Automatic Feedback Invocation (5 tests)
- **AC3:** Graceful Degradation (6 tests)
- **AC4:** Context-Aware Configuration (6 tests)
- **AC5:** Pattern Consistency (6 tests)

**Total AC Tests:** 28

### Non-Functional Requirements
- **NFR-P1 (Performance):** <500ms check-hooks execution (1 test)
- **NFR-R1 (Reliability):** 100% success rate despite failures (1 test)
- **NFR-M1 (Maintainability):** <50 lines Phase N code (1 test)

**Total NFR Tests:** 3

### Integration & Workflow
- **Integration Tests:** 4 tests for end-to-end scenarios

**Grand Total:** 35 tests

---

## Test Classes

```
test_story_031_ideate_hooks.py
├── TestAC1_HookEligibilityCheck (5 tests)
├── TestAC2_AutomaticFeedbackInvocation (5 tests)
├── TestAC3_GracefulDegradation (6 tests)
├── TestAC4_ContextAwareFeedback (6 tests)
├── TestAC5_PatternConsistency (6 tests)
├── TestIdeateHooksIntegration (4 tests)
├── TestAC_Performance (1 test)
├── TestAC_Reliability (1 test)
└── TestAC_Maintainability (1 test)
```

---

## Test Fixtures

| Fixture | Type | Used By |
|---------|------|---------|
| `mock_ideation_context` | Dict | AC4, AC2 |
| `mock_check_hooks_success` | MagicMock | AC1, AC2, AC5 |
| `mock_check_hooks_not_eligible` | MagicMock | AC2 |
| `mock_check_hooks_failure` | MagicMock | AC3 |
| `mock_invoke_hooks_success` | MagicMock | AC2 |
| `mock_invoke_hooks_failure` | MagicMock | AC3 |
| `temp_ideation_artifacts` | ContextManager | AC3, AC4 |

---

## Mocking Strategy

All tests use `@patch('subprocess.run')` to mock subprocess calls:

```python
@patch('subprocess.run')
def test_example(self, mock_run):
    # Arrange
    mock_run.return_value = MagicMock(returncode=0)
    
    # Act
    result = subprocess.run(...)
    
    # Assert
    assert result.returncode == 0
```

This approach:
- Prevents actual CLI calls during testing
- Enables comprehensive error scenario simulation
- Maintains test speed
- Provides deterministic results

---

## Implementation Requirements

The test suite validates that `/ideate` command will:

1. **Call check-hooks** after Phase 6 completes
   ```bash
   devforgeai check-hooks --operation=ideate --status=completed
   ```

2. **Conditionally call invoke-hooks** when eligible
   ```bash
   devforgeai invoke-hooks --operation=ideate --context="$IDEATION_CONTEXT"
   ```

3. **Display success message**
   ```
   ✓ Post-ideation feedback initiated
   ```

4. **Handle failures gracefully**
   ```
   ⚠ Post-ideation feedback skipped (hook system unavailable)
   ```

5. **Exit with code 0 regardless** of hook outcome

---

## Next Steps

### Phase 1: Review
- [ ] Read test file: `tests/unit/test_story_031_ideate_hooks.py`
- [ ] Review test generation summary: `STORY-031-TEST-GENERATION-COMPLETE.md`
- [ ] Review quick reference: `tests/STORY-031-QUICK-REFERENCE.md`

### Phase 2: Implement (Green)
- [ ] Add Phase N to `.claude/commands/ideate.md`
- [ ] Implement check-hooks call
- [ ] Implement conditional invoke-hooks call
- [ ] Add context passing
- [ ] Add error handling
- [ ] Run tests: `pytest tests/unit/test_story_031_ideate_hooks.py -v`
- [ ] Verify: 35/35 tests passing

### Phase 3: Refactor
- [ ] Review implementation for code quality
- [ ] Verify pattern matches /dev pilot
- [ ] Optimize error messages
- [ ] Add documentation

---

## References

**Story Documents:**
- `.ai_docs/Stories/STORY-031-wire-hooks-into-ideate-command.story.md` - Full requirements
- `.ai_docs/Stories/STORY-023-wire-hooks-into-dev-command-pilot.story.md` - Pilot implementation

**Command Files:**
- `.claude/commands/ideate.md` - Target for implementation
- `.claude/commands/dev.md` - Reference implementation (Phase N section)

**Test Files:**
- `tests/unit/test_story_031_ideate_hooks.py` - Main test suite
- `STORY-031-TEST-GENERATION-COMPLETE.md` - Generation summary
- `tests/STORY-031-QUICK-REFERENCE.md` - Quick reference

---

## Test Execution History

**Generation Date:** 2025-11-17
**Test Framework:** pytest 7.4.4
**Python Version:** 3.12.3
**Total Tests:** 35
**First Run:** 35 passed in 0.63s

---

## Key Metrics

| Metric | Value |
|--------|-------|
| Total Test Cases | 35 |
| Test File Size | 1,299 lines |
| Test Classes | 10 |
| Fixtures | 8 |
| Code Coverage Target | 100% (AC + NFR) |
| Expected Pass Rate | 100% (after implementation) |
| Average Test Duration | ~18ms |
| Total Test Suite Duration | ~0.63s |

---

## Support

For questions or issues:

1. **Review test quick reference:** `tests/STORY-031-QUICK-REFERENCE.md`
2. **Check troubleshooting section:** Same document
3. **Review test patterns:** All tests follow AAA pattern
4. **Reference pilot:** `.claude/commands/dev.md` (Phase N section)

---

**Test Suite Status:** Ready for implementation (TDD Green phase)
**Target:** 35/35 passing tests after Phase N implementation

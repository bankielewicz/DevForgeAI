# STORY-030 Test Suite - Quick Reference

## Running the Tests

### Run All Tests
```bash
pytest tests/integration/test_create_context_hooks_integration.py \
       tests/unit/test_create_context_hook_eligibility.py \
       tests/unit/test_create_context_hook_invocation.py \
       tests/unit/test_create_context_hooks_error_handling.py -v
```

### Run Individual Test Files
```bash
# Integration tests
pytest tests/integration/test_create_context_hooks_integration.py -v

# Unit tests - Eligibility
pytest tests/unit/test_create_context_hook_eligibility.py -v

# Unit tests - Invocation
pytest tests/unit/test_create_context_hook_invocation.py -v

# Unit tests - Error handling
pytest tests/unit/test_create_context_hooks_error_handling.py -v
```

### Run Specific Test Class
```bash
pytest tests/integration/test_create_context_hooks_integration.py::TestHookEligibilityCheck -v
pytest tests/unit/test_create_context_hook_invocation.py::TestConditionalInvokeHooksLogic -v
```

### Run Single Test
```bash
pytest tests/integration/test_create_context_hooks_integration.py::TestHookEligibilityCheck::test_check_hooks_exit_code_zero_means_eligible -v
```

---

## Test Organization

### File Structure
```
tests/
├── integration/
│   └── test_create_context_hooks_integration.py  (27 tests)
├── unit/
│   ├── test_create_context_hook_eligibility.py   (15 tests)
│   ├── test_create_context_hook_invocation.py    (18 tests)
│   └── test_create_context_hooks_error_handling.py (29 tests)
├── STORY-030-test-suite-summary.md
└── STORY-030-quick-reference.md
```

### Test Classes by Acceptance Criteria

**AC1 (Hook Eligibility Check)**
- `TestHookEligibilityCheck` (integration)
- `TestCheckHooksArgumentValidation` (unit)
- `TestCheckHooksExitCodeInterpretation` (unit)
- `TestCheckHooksErrorDetection` (unit)

**AC2 (Automatic Hook Invocation When Eligible)**
- `TestHookInvocationLogic` (integration)
- `TestConditionalInvokeHooksLogic` (unit)
- `TestInvokeHooksArgumentValidation` (unit)
- `TestFeedbackConversationCompletion` (unit)
- `TestFeedbackMetadataCapture` (unit)

**AC3 (Graceful Degradation on Hook Failures)**
- `TestCreateContextWithHooksIntegration` (integration - multiple scenarios)
- `TestGracefulDegradationOnErrors` (unit)
- `TestWarningMessageFormatting` (unit)
- `TestErrorTypeHandling` (unit)
- `TestNonBlockingErrorHandling` (unit)
- `TestErrorLogging` (unit)
- `TestCommandSuccessDespiteFailures` (unit)

**AC4 (Hook Skip When Not Eligible)**
- `TestHookEligibilityCheck` (integration)
- `TestSkipMessageDisplay` (unit)
- `TestSkipOverheadPerformance` (unit)

**AC5 (Integration with Existing Command Flow)**
- `TestCreateContextWithHooksIntegration` (integration)
- `TestCreateContextHooksIntegration` (integration)
- `TestCreateContextHooksPatternConsistency` (integration)

---

## Test Status

### Current Status: RED (All Failing)
```
✗ 65 failing tests
  → Implementation not started
  → All tests currently FAIL (expected for TDD Red phase)
```

### Expected After Implementation: GREEN
```
✓ 65 passing tests
  → Hook eligibility check implemented
  → Hook invocation conditional logic implemented
  → Error handling implemented
  → All acceptance criteria satisfied
```

---

## Key Test Cases by Requirement

### Must Pass (Critical Implementation)
1. `test_check_hooks_command_called_with_correct_arguments` - Command structure
2. `test_check_hooks_exit_code_zero_means_eligible` - Exit code interpretation
3. `test_invoke_hooks_called_when_check_hooks_returns_zero` - Conditional invocation
4. `test_invoke_hooks_NOT_called_when_check_hooks_returns_one` - Skip logic
5. `test_command_continues_when_check_hooks_fails` - Graceful degradation
6. `test_warning_message_format_matches_spec` - Error message format

### High Priority (Core Features)
- Hook eligibility check tests (5 tests)
- Hook invocation logic tests (4 tests)
- Error handling tests (12 tests)
- Backward compatibility tests (1 test)

### Medium Priority (Non-Functional Requirements)
- Performance tests (4 tests)
- Usability tests (8 tests)
- Reliability tests (6 tests)

### Nice to Have (Edge Cases)
- CLI missing scenario
- Config file corrupted scenario
- User interrupt (Ctrl+C) scenario
- Rate limiting scenario

---

## Expected Test Failures (Red Phase)

When running tests in Red phase, expect failures like:

```
FAILED test_check_hooks_command_called_with_correct_arguments
  → subprocess.run not mocked correctly (Phase N not implemented)

FAILED test_context_files_created_when_hooks_eligible
  → Phase N not in /create-context command yet

FAILED test_command_returns_zero_despite_hook_failure
  → Error handling not implemented

FAILED test_warning_message_format_matches_spec
  → Warning message not shown (Phase N not added)
```

All failures are EXPECTED at this point.

---

## Implementation Checklist (for developer)

### Phase N Structure in .claude/commands/create-context.md
- [ ] Add "Phase N: Invoke Hooks" section after Phase 4
- [ ] Include check-hooks command call
- [ ] Include exit code conditional logic
- [ ] Include invoke-hooks call for exit code 0
- [ ] Include error handling (graceful degradation)
- [ ] Include warning message on errors

### Implementation Requirements (from tests)
- [ ] check-hooks called with --operation=create-context --status=completed
- [ ] Exit code 0 triggers invoke-hooks call
- [ ] Exit code 1 skips invoke-hooks (silent, <100ms)
- [ ] Error codes treated as skip
- [ ] Hook failures don't prevent file creation
- [ ] Warning message: "Optional feedback system unavailable, continuing..."
- [ ] All 6 context files created regardless of hook state
- [ ] Return code 0 (success) always

### Pattern Reference (STORY-023 /dev pilot)
Compare implementation to `/dev` Phase 6 from STORY-023:
- Same check-hooks structure
- Same conditional logic
- Same error handling pattern
- Same non-blocking behavior

---

## Debugging Tips

### When Tests Fail

1. **Check if subprocess.run is mocked correctly**
   ```python
   # Verify mock in test fixture
   @patch('subprocess.run')
   def test_something(self, mock_run):
       mock_run.return_value = MagicMock(returncode=0)
   ```

2. **Verify exit codes are being checked**
   ```python
   # Should check: if result.returncode == 0
   result = subprocess.run(["devforgeai", "check-hooks"])
   if result.returncode == 0:  # MUST check this
       invoke_result = subprocess.run(["devforgeai", "invoke-hooks"])
   ```

3. **Ensure context files created in Phase 4**
   - Files must exist BEFORE Phase N
   - Phase N executes AFTER Phase 4
   - All 6 files required

4. **Check warning message format**
   - Exact format: "Optional feedback system unavailable, continuing..."
   - Must include "Optional"
   - Must include "continuing"
   - <50 words
   - No scary language

### Common Issues

**Issue:** Tests can't find subprocess.run
- **Solution:** Import subprocess and use @patch decorator

**Issue:** Exit codes not being interpreted
- **Solution:** Implement `if result.returncode == 0` check

**Issue:** Context files not showing as created
- **Solution:** Ensure Phase 4 completes before Phase N

**Issue:** Error messages not matching spec
- **Solution:** Use exact message format from tests

---

## Test Dependencies

### Files Required
```
.claude/commands/create-context.md - Command with Phase N
.devforgeai/context/*.md - 6 context files created in Phase 4
devforgeai CLI - Mock available (subprocess.run mocked)
```

### No External Dependencies
- Tests are isolated (no network calls)
- No actual hooks system needed (mocked)
- No real CLI required (mocked)
- All dependencies injected via fixtures

---

## Verification Steps

### Step 1: Run All Tests (should all fail)
```bash
pytest tests/integration/test_create_context_hooks_integration.py \
       tests/unit/test_create_context_hook_eligibility.py \
       tests/unit/test_create_context_hook_invocation.py \
       tests/unit/test_create_context_hooks_error_handling.py -v
```

Expected: 65 FAILED, 0 PASSED

### Step 2: Implement Phase N in command

### Step 3: Run tests incrementally
```bash
# Step 1: AC1 tests (eligibility)
pytest tests/unit/test_create_context_hook_eligibility.py -v

# Step 2: AC2/AC4 tests (invocation logic)
pytest tests/unit/test_create_context_hook_invocation.py -v

# Step 3: AC3 tests (error handling)
pytest tests/unit/test_create_context_hooks_error_handling.py -v

# Step 4: Integration tests (full workflow)
pytest tests/integration/test_create_context_hooks_integration.py -v
```

### Step 4: Final verification
```bash
# All tests should pass
pytest tests/integration/test_create_context_hooks_integration.py \
       tests/unit/test_create_context_hook_eligibility.py \
       tests/unit/test_create_context_hook_invocation.py \
       tests/unit/test_create_context_hooks_error_handling.py -v

# Expected: 65 PASSED, 0 FAILED
```

---

## Coverage Goals

After implementation, verify coverage:
```bash
pytest tests/integration/test_create_context_hooks_integration.py \
       tests/unit/test_create_context_hook_eligibility.py \
       tests/unit/test_create_context_hook_invocation.py \
       tests/unit/test_create_context_hooks_error_handling.py \
       --cov=.claude/commands/create-context.md \
       --cov-report=html
```

**Target:** 100% coverage of Phase N

---

## Questions and Answers

**Q: Why are all tests failing initially?**
A: TDD Red phase - tests are written before implementation. This is intentional.

**Q: Should I modify the tests?**
A: No. Tests define the requirements. Implementation must pass tests as written.

**Q: What if a test seems wrong?**
A: Review the acceptance criteria in STORY-030. Tests match AC exactly. Verify AC is correct before changing test.

**Q: How do I know if implementation is complete?**
A: All 65 tests pass. Run: `pytest -v` and verify 65 PASSED.

**Q: Can I run tests in different order?**
A: Yes, but recommend: AC1 → AC2 → AC3 → AC4 → AC5 (logical progression)

---

## Success Criteria

Implementation is complete when:

- [x] All 65 tests pass (100% pass rate)
- [x] Phase N added to /create-context.md command
- [x] check-hooks called with correct arguments
- [x] Exit codes properly interpreted (0, 1)
- [x] invoke-hooks conditionally called
- [x] Context files created regardless of hook state
- [x] Errors handled gracefully (non-blocking)
- [x] Warning message matches specification
- [x] Pattern consistent with /dev pilot (STORY-023)
- [x] Backward compatibility verified

---

**Total Tests:** 65
**Test Files:** 4
**Acceptance Criteria:** 5
**Non-Functional Requirements:** 3
**Edge Cases:** 6

**Framework:** pytest
**Pattern:** AAA (Arrange, Act, Assert)
**Status:** RED (All failing - ready for implementation)

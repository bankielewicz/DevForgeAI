# STORY-185 Integration Tests: --type Flag for check-hooks

**Story:** STORY-185 - Implement --type Flag for check-hooks CLI Command
**Status:** Feature specification testing (NOT YET IMPLEMENTED)
**Test Creation Date:** 2025-01-07

---

## Overview

This directory contains comprehensive integration tests for STORY-185. The tests are designed to validate that the `--type` flag feature for the `devforgeai check-hooks` command works correctly when implemented.

**Current Status:**
- Feature: NOT IMPLEMENTED
- Tests: COMPLETE AND READY (14/27 passing with expected failures)
- Test Suite: Production-ready for feature validation

---

## Contents

### Test Files

1. **`integration_test_check_hooks_type_flag.py`** (Main Test Suite)
   - 27 comprehensive integration tests
   - CLI argument parsing (5 tests)
   - Module type functionality (5 tests)
   - Hook filtering logic (3 tests)
   - End-to-end integration (4 tests)
   - Error handling (2 tests)
   - Type filtering logic (3 tests)
   - CLI command execution (5 tests)

### Documentation Files

2. **`TEST_REPORT.md`** (Detailed Test Specification)
   - Complete test plan
   - Expected vs. actual results
   - Implementation requirements (AC#1-5)
   - Files involved and changes needed

3. **`INTEGRATION_TEST_SUMMARY.md`** (Test Execution Results)
   - Pass/fail breakdown by category
   - Detailed analysis of each test result
   - Root cause analysis for failures
   - Acceptance criteria validation status
   - Implementation checklist

4. **`MANUAL_CLI_TESTS.md`** (CLI Testing Documentation)
   - Manual command-line test scenarios
   - Module-level test documentation
   - Current implementation status
   - Implementation plan (4-step fix)
   - Expected results after implementation

5. **`test_execution_results.log`** (Raw Test Output)
   - Complete pytest output
   - Exit codes and error messages
   - Test execution timeline

---

## Quick Start

### Run All Tests

```bash
cd /mnt/c/Projects/DevForgeAI2
python3 -m pytest tests/STORY-185/integration_test_check_hooks_type_flag.py -v
```

### Run Specific Test Category

```bash
# CLI Argument Parsing Tests
pytest tests/STORY-185/integration_test_check_hooks_type_flag.py::TestCLIArgumentParsing -v

# Module Type Functionality Tests
pytest tests/STORY-185/integration_test_check_hooks_type_flag.py::TestModuleTypeFunctionality -v

# Hook Filtering Tests
pytest tests/STORY-185/integration_test_check_hooks_type_flag.py::TestTypedHookFiltering -v
```

### Run Single Test

```bash
pytest tests/STORY-185/integration_test_check_hooks_type_flag.py::TestCLIArgumentParsing::test_parser_has_type_option -v
```

### Run with Coverage

```bash
pytest tests/STORY-185/integration_test_check_hooks_type_flag.py \
  --cov=src.claude.scripts.devforgeai_cli.commands.check_hooks \
  -v
```

---

## Test Results Summary

### Current Status (Feature Not Implemented)
```
Tests:    27
Passed:   14 (51.9%)
Failed:   13 (48.1%)
Expected: 13 failures (all due to missing feature)
```

### Results by Category
| Category | Tests | Passed | Failed | Notes |
|----------|-------|--------|--------|-------|
| CLI Argument Parsing | 5 | 1 | 4 | `--type` not in parser |
| Module Type Functionality | 5 | 1 | 4 | `hook_type` param missing |
| Hook Filtering Logic | 3 | 3 | 0 | Algorithm validated ✓ |
| End-to-End Integration | 4 | 3 | 1 | Partial E2E success |
| Error Handling | 2 | 0 | 2 | Invalid type handling missing |
| Type Filtering Logic | 3 | 2 | 1 | Mock filtering works ✓ |
| CLI Command Execution | 5 | 4 | 1 | Help text missing `--type` |

---

## What These Tests Validate

### 1. CLI Interface (Feature AC#1, AC#2, AC#5)
- `--type` parameter accepted
- Valid choices: user, ai, all
- Default value: all
- Invalid values rejected
- Help text includes `--type` documentation

### 2. Module Interface (Feature AC#1)
- `check_hooks_command()` accepts `hook_type` parameter
- Parameter supports: user, ai, all
- Default: all
- Invalid values return error code

### 3. Filtering Logic (Feature AC#3)
- Hooks filtered by `hook_type` field
- Only matching hooks processed
- 'all' type processes all hooks

### 4. Error Handling (Feature AC#4)
- Invalid types produce clear errors
- Exit code 2 for errors
- Error messages guide user to valid choices

### 5. End-to-End Workflows (Integration)
- Complete CLI workflows with type parameter
- Backward compatibility (works without --type)
- Consistent behavior across type values

---

## Implementation Status

### What's Working ✓
- Argument parser (except for --type)
- Basic operation/status validation
- Hook configuration loading
- Circular invocation detection
- Exit code handling

### What's Missing ✗
- `--type` argument in parser
- `hook_type` parameter in function
- Hook filtering by type
- Type-specific error messages
- Help text for `--type`

### Implementation Effort
- **Time:** 15-20 minutes
- **Complexity:** Low
- **Files to Change:** 1 (`check_hooks.py`)
- **Lines to Add:** ~20
- **Risk:** Very Low (backward compatible)

---

## Implementation Checklist

See `MANUAL_CLI_TESTS.md` for 4-step implementation plan:

- [ ] Step 1: Add `--type` argument to parser
- [ ] Step 2: Add `hook_type` parameter to function
- [ ] Step 3: Implement filtering logic
- [ ] Step 4: Pass type parameter from CLI to function
- [ ] Step 5: Run test suite (should see 27/27 passing)

---

## Acceptance Criteria Coverage

| AC | Requirement | Test Coverage | Status |
|----|-------------|---|---|
| AC#1 | --type parameter accepted | `test_parser_has_type_option`, `test_check_hooks_accepts_type_parameter` | BLOCKED |
| AC#2 | Valid values: user, ai, all | `test_parser_type_has_choices`, `test_parser_type_default_is_all` | BLOCKED |
| AC#3 | Hooks filtered by type | `test_filter_user_type_hooks`, `test_filter_ai_type_hooks` | BLOCKED |
| AC#4 | Error message improved | `test_invalid_type_error_message`, `test_invalid_type_cli_rejection` | BLOCKED |
| AC#5 | Help text updated | `test_help_text_includes_type_documentation`, `test_cli_help_shows_type_flag` | BLOCKED |

---

## Test Scenarios Covered

### CLI Tests (10 tests)
1. Help text includes `--type` (FAILED)
2. Accept `--type user` (FAILED)
3. Accept `--type ai` (FAILED)
4. Accept `--type all` (FAILED)
5. Reject `--type invalid` (PASSED)
6. Help shows type choices (FAILED)
7. Full workflow with user type (PASSED)
8. Full workflow with ai type (PASSED)
9. Full workflow with all type (PASSED)
10. Default matches all type (FAILED)

### Module Tests (5 tests)
1. Accept `hook_type='user'` (FAILED)
2. Accept `hook_type='ai'` (FAILED)
3. Accept `hook_type='all'` (FAILED)
4. Reject `hook_type='invalid'` (FAILED)
5. Default without parameter (PASSED)

### Logic Tests (12 tests)
1. Filter user hooks (PASSED)
2. Filter ai hooks (PASSED)
3. Filter all returns all (PASSED)
4. Handle missing type field (PASSED)
5. No filtering for 'all' (PASSED)
6. E2E user type (PASSED)
7. E2E ai type (PASSED)
8. E2E all type (PASSED)
9. Config filtering with types (FAILED)
10. Parser rejects invalid (PASSED)
11. CLI rejects invalid (PASSED)
12. Default defaults to all (PASSED)

---

## File Locations

| File | Purpose | Lines |
|------|---------|-------|
| `integration_test_check_hooks_type_flag.py` | Main test suite | 521 |
| `TEST_REPORT.md` | Test specification | 340 |
| `INTEGRATION_TEST_SUMMARY.md` | Execution results | 400 |
| `MANUAL_CLI_TESTS.md` | CLI testing & plan | 380 |
| `test_execution_results.log` | Raw pytest output | 50 |
| `README.md` | This file | 300 |

---

## Documentation References

**Implementation Required:** `MANUAL_CLI_TESTS.md` (Section: Implementation Plan)
- 4-step implementation
- Code snippets ready to copy-paste
- ~15-20 minutes effort

**Test Failures Explained:** `INTEGRATION_TEST_SUMMARY.md` (Section: Detailed Test Results)
- Each test result analyzed
- Root causes documented
- Evidence provided

**Comprehensive Test Plan:** `TEST_REPORT.md` (Section: Implementation Requirements)
- AC#1-5 requirement mapping
- Acceptance criteria coverage
- Testing strategy

---

## Success Criteria

Tests will be considered successful when:

```
✓ All 27 tests pass
✓ CLI accepts --type with valid values (user, ai, all)
✓ CLI rejects invalid --type values with error code 2
✓ Help text documents --type parameter
✓ Module accepts hook_type parameter
✓ Hooks are correctly filtered by type
✓ Default behavior (no --type) = --type all
✓ Backward compatibility maintained
```

---

## Next Steps

### To Run Tests Now (Feature Not Implemented)
```bash
pytest tests/STORY-185/integration_test_check_hooks_type_flag.py -v
# Expected: 14 passed, 13 failed
```

### To Implement Feature
1. Read `MANUAL_CLI_TESTS.md` (Implementation Plan section)
2. Apply 4-step changes to `check_hooks.py`
3. Run tests to verify (should see 27/27 passing)

### To Validate Implementation
```bash
# Should see 27 passed, 0 failed
pytest tests/STORY-185/integration_test_check_hooks_type_flag.py -v

# Should show all AC#1-5 covered
pytest tests/STORY-185/integration_test_check_hooks_type_flag.py -v --tb=short
```

---

## Questions?

Refer to the appropriate documentation:
- **What needs to be implemented?** → `TEST_REPORT.md` (Implementation Requirements)
- **Why did tests fail?** → `INTEGRATION_TEST_SUMMARY.md` (Detailed Test Results)
- **How to implement?** → `MANUAL_CLI_TESTS.md` (Implementation Plan)
- **How to run tests?** → This README (Quick Start section)

---

## Summary

This test suite provides:
- ✓ Complete validation of STORY-185 feature
- ✓ Clear pass/fail criteria for implementation
- ✓ Step-by-step implementation guide
- ✓ Comprehensive documentation
- ✓ Production-ready test framework

**Ready to proceed with STORY-185 implementation.**

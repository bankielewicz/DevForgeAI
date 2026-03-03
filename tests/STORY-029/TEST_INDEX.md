# STORY-029 Test Suite Index

**Generated:** 2025-11-16
**Story:** Wire hooks into create-sprint command
**Test Coverage:** 100% (5 ACs, 5 edge cases, 8 NFRs, E2E)

---

## Directory Structure

```
tests/STORY-029/
├── README.md                           # Quick start guide
├── TEST_SUMMARY.md                     # Comprehensive test documentation
├── TEST_INDEX.md                       # This file
├── run_all_tests.sh                    # Master test runner
│
├── unit/                               # Unit tests (AC1-5)
│   ├── test_phase_n_hook_check.sh             # AC1 - Phase N added to workflow
│   ├── test_graceful_degradation.sh           # AC2 - Hooks disabled handling
│   ├── test_hook_invocation_with_context.sh   # AC3 - Sprint context parameters
│   ├── test_hook_failure_resilience.sh        # AC4 - Failure doesn't break sprint
│   └── test_empty_sprint_handling.sh          # AC5 - Zero stories selected
│
├── edge-cases/                         # Edge case tests
│   ├── test_shell_injection.sh                # E1 - Shell injection prevention
│   └── test_concurrent_execution.sh           # E2 - Concurrent sprint creation
│
├── performance/                        # Performance tests (NFRs)
│   └── test_nfr_performance.sh                # NFR-001, NFR-002, NFR-003
│
└── integration/                        # Integration tests
    └── test_end_to_end_sprint_creation.sh     # E2E workflow validation
```

---

## Test Files Overview

### Unit Tests (5 files, 32 test cases)

**1. test_phase_n_hook_check.sh** (5 tests)
- Validates Phase N section exists
- Checks check-hooks command invocation
- Verifies Phase N placement after Phase 4
- Validates command parameters
- Ensures conditional execution

**2. test_graceful_degradation.sh** (5 tests)
- check-hooks exit code when disabled
- Hook invocation skipped
- Sprint creation succeeds
- No feedback prompts
- Disabled status logged

**3. test_hook_invocation_with_context.sh** (7 tests)
- --sprint-name parameter
- --story-count parameter
- --capacity parameter
- --operation=create-sprint parameter
- Feedback file creation
- Context variables defined
- Shell escaping validation

**4. test_hook_failure_resilience.sh** (8 tests)
- Error handling present
- Hook failures logged
- User warning message
- Sprint file valid
- Story statuses preserved
- Non-zero exit handled
- Python exceptions handled
- Graceful degradation documented

**5. test_empty_sprint_handling.sh** (7 tests)
- STORY_COUNT=0 handling
- invoke-hooks with --story-count=0
- invoke-hooks with --capacity=0
- Feedback adapts to empty sprint
- Empty sprint file valid
- Zero story count validation
- Zero capacity validation

### Edge Case Tests (2 files, 13 test cases)

**6. test_shell_injection.sh** (7 tests)
- Shell metacharacters escaped
- Semicolon injection prevented
- Backtick substitution prevented
- $() substitution prevented
- Pipe injection prevented
- Null byte injection handled
- BR-003 compliance

**7. test_concurrent_execution.sh** (6 tests)
- Unique feedback filenames
- Concurrent invocations don't conflict
- File locking present
- NFR-008 compliance
- Sprint numbering race condition
- Feedback file overwrites prevented

### Performance Tests (1 file, 5 test cases)

**8. test_nfr_performance.sh** (5 tests)
- NFR-001: check-hooks < 100ms
- NFR-002: invoke-hooks < 3s
- NFR-003: Phase N overhead < 3.5s
- Phase N overhead acceptable
- Performance NFRs documented

### Integration Tests (1 file, 8 test cases)

**9. test_end_to_end_sprint_creation.sh** (8 tests)
- Sprint file created
- Stories updated to Ready for Dev
- Phase N executes after sprint
- Hooks invoked with context
- Feedback file created
- Workflow resilient to failures
- Exit code 0 despite failures
- Workflow history complete

---

## Test Coverage Matrix

| Requirement | Test File(s) | Test Count | Status |
|-------------|--------------|-----------|--------|
| **AC1** - Phase N added | test_phase_n_hook_check.sh | 5 | ❌ FAIL (Red) |
| **AC2** - Graceful degradation | test_graceful_degradation.sh | 5 | ❌ FAIL (Red) |
| **AC3** - Sprint context | test_hook_invocation_with_context.sh | 7 | ❌ FAIL (Red) |
| **AC4** - Hook failure resilience | test_hook_failure_resilience.sh | 8 | ❌ FAIL (Red) |
| **AC5** - Empty sprint | test_empty_sprint_handling.sh | 7 | ❌ FAIL (Red) |
| **E1** - Shell injection | test_shell_injection.sh | 7 | ❌ FAIL (Red) |
| **E2** - Concurrent execution | test_concurrent_execution.sh | 6 | ✅ PASS |
| **NFR-001** - Performance | test_nfr_performance.sh | 1 | ✅ PASS |
| **NFR-002** - Performance | test_nfr_performance.sh | 1 | ✅ PASS |
| **NFR-003** - Performance | test_nfr_performance.sh | 1 | ✅ PASS |
| **E2E** - Integration | test_end_to_end_sprint_creation.sh | 8 | ❌ FAIL (Red) |

**Coverage:** 100% (all requirements have tests)

---

## Test Execution Commands

### Run All Tests

```bash
cd /mnt/c/Projects/DevForgeAI2/tests/STORY-029
bash run_all_tests.sh
```

**Expected output (Red phase):**
```
Total:  9 test files
Passed: 1 (test_concurrent_execution)
Failed: 8 (awaiting Phase N implementation)
```

### Run By Category

```bash
# Unit tests only
for f in unit/*.sh; do bash "$f"; done

# Edge case tests only
for f in edge-cases/*.sh; do bash "$f"; done

# Performance tests only
bash performance/test_nfr_performance.sh

# Integration tests only
bash integration/test_end_to_end_sprint_creation.sh
```

### Run Individual Test

```bash
# Specific test file
bash unit/test_phase_n_hook_check.sh

# With detailed output
bash unit/test_phase_n_hook_check.sh 2>&1 | less
```

---

## Test Results Interpretation

### Current Results (Red Phase)

```
TOTAL TESTS: 58 test cases
PASS: 15 (26% - mostly performance and validation tests)
FAIL: 43 (74% - awaiting Phase N implementation)
```

**Expected failures:**
- Phase N section not found (all structural tests)
- check-hooks not invoked (all hook check tests)
- invoke-hooks not invoked (all hook invocation tests)
- Sprint context not passed (all parameter tests)
- Error handling missing (all failure resilience tests)

**Passing tests (expected):**
- Concurrent execution (infrastructure already supports)
- Performance measurements (hook CLI meets targets)
- Validation checks (data validation correct)
- Sprint creation logic (existing workflow intact)

### After Implementation (Green Phase)

**Expected results:**
```
TOTAL TESTS: 58 test cases
PASS: 58 (100% - all tests pass)
FAIL: 0
```

**Critical tests that must pass:**
1. Phase N section exists
2. check-hooks invoked with correct parameters
3. invoke-hooks invoked with sprint context
4. Hook failures don't break sprint creation
5. Sprint name shell-escaped (security)
6. Empty sprint handling (edge case)
7. All performance targets met
8. End-to-end workflow complete

---

## Implementation Checklist

Track implementation progress:

### Phase N Structure
- [ ] Section added: `### Phase N: Feedback Hook Integration`
- [ ] Placed after Phase 4 (Display Results)
- [ ] Hook check: `devforgeai check-hooks --operation=create-sprint --status=completed`
- [ ] Conditional invocation: `if check returns 0`
- [ ] Hook invoke: `devforgeai invoke-hooks --operation=create-sprint ...`

### Sprint Context
- [ ] SPRINT_NAME variable defined
- [ ] STORY_COUNT calculated (from selection)
- [ ] CAPACITY_POINTS calculated (sum of story points)
- [ ] All 3 parameters passed to invoke-hooks

### Error Handling
- [ ] Hook failures caught (try-catch or `|| true`)
- [ ] Errors logged to `devforgeai/feedback/logs/hook-errors.log`
- [ ] User warning displayed
- [ ] Sprint creation succeeds regardless

### Security
- [ ] Sprint name double-quoted: `--sprint-name="${SPRINT_NAME}"`
- [ ] Tested with malicious names
- [ ] No command injection possible

### Testing
- [ ] All 58 tests pass
- [ ] Manual smoke test complete
- [ ] Performance targets met

---

## Quick Reference

### Most Important Tests (Run First)

```bash
# 1. Structural validation
bash unit/test_phase_n_hook_check.sh

# 2. Hook invocation
bash unit/test_hook_invocation_with_context.sh

# 3. Failure resilience
bash unit/test_hook_failure_resilience.sh

# 4. Security
bash edge-cases/test_shell_injection.sh

# 5. Integration
bash integration/test_end_to_end_sprint_creation.sh
```

### Common Test Patterns

**Grep for implementation:**
```bash
grep "Phase N" .claude/commands/create-sprint.md
grep "check-hooks" .claude/commands/create-sprint.md
grep "invoke-hooks" .claude/commands/create-sprint.md
```

**Verify parameters:**
```bash
grep "sprint-name" .claude/commands/create-sprint.md
grep "story-count" .claude/commands/create-sprint.md
grep "capacity" .claude/commands/create-sprint.md
```

**Check error handling:**
```bash
grep -A 10 "invoke-hooks" .claude/commands/create-sprint.md | grep "|| true\|error\|fail"
```

---

## Test Maintenance Log

| Date | Change | Reason | Files Modified |
|------|--------|--------|----------------|
| 2025-11-16 | Initial test suite created | STORY-029 TDD Red phase | All test files |
| - | - | - | - |

---

## Related Documentation

- **README.md** - Quick start guide and troubleshooting
- **TEST_SUMMARY.md** - Comprehensive test documentation
- **Story** - `devforgeai/specs/Stories/STORY-029-wire-hooks-into-create-sprint-command.story.md`
- **Implementation Target** - `.claude/commands/create-sprint.md`

---

## Contact

**Questions or Issues:**
- See `TEST_SUMMARY.md` for detailed test documentation
- See `README.md` for troubleshooting
- Review story file for requirements clarification

---

**Last Updated:** 2025-11-16
**Test Suite Version:** 1.0
**Framework:** DevForgeAI TDD Workflow

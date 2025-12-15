# STORY-033: Wire Hooks into /audit-deferrals Command - Test Suite

**Status:** All tests FAILING (TDD Red phase - tests written before implementation)

**Purpose:** Comprehensive test suite for STORY-033 requirements covering:
- Hook eligibility checking and conditional invocation
- Audit context passing with 5 metadata fields
- Graceful degradation on hook failures
- Sensitive data sanitization
- Logging and audit trails
- Performance benchmarks
- Pattern consistency with /dev pilot (STORY-023)

---

## Test Structure

### File Organization

```
tests/
├── STORY-033-TEST-SUITE-README.md (this file)
├── integration/
│   ├── test_hook_integration_story033.py    (15-20 integration tests)
│   ├── conftest_story033.py                 (fixtures and helpers)
│
└── unit/
    └── test_story033_conf_requirements.py   (9 CONF unit tests)
```

### Test Count Summary

| Category | Count | Focus |
|----------|-------|-------|
| **Unit Tests** | 20+ | CONF-001 through CONF-009 requirements |
| **Integration Tests** | 12+ | Full workflow with different scenarios |
| **Performance Tests** | 3 | Latency and overhead benchmarks |
| **Edge Case Tests** | 8 | CLI missing, config invalid, etc. |
| **Acceptance Criteria** | 6 | AC1-AC6 validation |
| **Total** | **50+** | Complete STORY-033 coverage |

---

## Quick Start

### Run All Tests

```bash
# All tests (will fail until Phase N implemented)
pytest tests/integration/test_hook_integration_story033.py \
       tests/unit/test_story033_conf_requirements.py -v

# Just integration tests
pytest tests/integration/test_hook_integration_story033.py -v

# Just unit tests
pytest tests/unit/test_story033_conf_requirements.py -v

# Specific test class
pytest tests/unit/test_story033_conf_requirements.py::TestCONF001PhaseNExists -v

# Show detailed output
pytest -v --tb=long
```

### Run with Coverage

```bash
pytest tests/ --cov=.claude/commands --cov=tests \
       --cov-report=term --cov-report=html
```

---

## Test Categories & Coverage

### 1. Unit Tests (20 tests in `test_story033_conf_requirements.py`)

#### CONF-001: Phase N Exists After Phase 5
- ✗ Phase N section exists in audit-deferrals.md
- ✗ Phase N comes after Phase 5 in document order
- ✗ Phase N has clear description of hook integration

#### CONF-002: check-hooks Call with Correct Arguments
- ✗ check-hooks call exists in Phase N
- ✗ Argument: --operation=audit-deferrals
- ✗ Argument: --status=completed

#### CONF-003: Conditional invoke-hooks Invocation
- ✗ invoke-hooks call exists in Phase N
- ✗ Conditional logic based on check-hooks exit code
- ✗ invoke-hooks has --operation=audit-deferrals

#### CONF-004: audit_summary with 5 Metadata Fields
- ✗ resolvable_count field present
- ✗ valid_count field present
- ✗ invalid_count field present
- ✗ oldest_age field present (in days)
- ✗ circular_chains field present (array of STORY-IDs)
- ✗ All 5 fields present together

#### CONF-005: Sensitive Data Sanitization
- ✗ api_key=secret → api_key=[REDACTED]
- ✗ password=pass → password=[REDACTED]
- ✗ token=token → token=[REDACTED]
- ✗ secret=val → secret=[REDACTED]
- ✗ Multiple patterns in one string
- ✗ 100% redaction rate (zero false negatives)

#### CONF-006: Non-Blocking Behavior
- ✗ Command succeeds even if check-hooks fails
- ✗ Hook failures log warnings (non-blocking)
- ✗ Audit report created despite hook failure

#### CONF-007: Hook Invocation Logging
- ✗ Log file created at .devforgeai/feedback/logs/hook-invocations.log
- ✗ Log entry has timestamp (ISO format)
- ✗ Log entry has operation name
- ✗ Log entry has status
- ✗ Log entry has outcome
- ✗ Log entries are structured JSON (one per line)

#### CONF-008: Circular Invocation Prevention
- ✗ Guard checks parent_operation == "audit-deferrals"
- ✗ Circular prevention logs warning
- ✗ No infinite loop possible

#### CONF-009: Context Size and Truncation
- ✗ Deferrals > 100 truncated to top 20 by priority
- ✗ Context size ≤ 50KB enforced
- ✗ Full report remains on disk

### 2. Integration Tests (12+ tests in `test_hook_integration_story033.py`)

#### AC1: Hook Eligibility Check
- ✗ After audit Phase 5, invoke check-hooks
- ✗ Capture eligibility result (true/false)
- ✗ Proceed to invocation only if eligible=true

#### AC2: Automatic Feedback Invocation with Context
- ✗ When eligible=true, invoke invoke-hooks
- ✗ Pass audit context with all 5 metadata fields
- ✗ Context matches expected format

#### AC3: Graceful Degradation
- ✗ CLI missing → warning logged, command succeeds
- ✗ Config invalid → warning logged, command succeeds
- ✗ Hook crashes → error logged, command succeeds
- ✗ Exit code 0 in all failure scenarios
- ✗ Audit report created despite failures

#### AC4: Context-Aware Feedback
- ✗ Questions reference audit findings
- ✗ operation_metadata includes audit_summary
- ✗ Context size ≤ 50KB

#### AC5: Pilot Pattern Consistency (vs STORY-023)
- ✗ Phase N structure matches /dev Phase 6
- ✗ check-hooks → conditional invoke-hooks flow
- ✗ Same error handling patterns
- ✗ Same logging approach

#### AC6: Invocation Tracking
- ✗ All invocations logged to hook-invocations.log
- ✗ Timestamp, operation, status, outcome recorded
- ✗ Failures include error details
- ✗ Successful invocations include session_id

#### Edge Cases (8 scenarios)
- ✗ No deferrals (empty audit)
- ✗ 150 deferrals (truncation to 20)
- ✗ Circular invocation prevention
- ✗ Concurrent audits (unique filenames)
- ✗ Very old deferrals (>365 days)
- ✗ User interrupts feedback (Ctrl+C)
- ✗ CLI not installed
- ✗ Config invalid/missing

### 3. Performance Tests (3 tests)

#### NFR-P1: Check-hooks Latency
- ✗ Must complete in <100ms (95th percentile)
- ✗ Measure 20 runs, verify p95 < 100ms

#### NFR-P2: Context Extraction
- ✗ Must complete in <300ms (95th percentile)
- ✗ JSON parsing + metadata building
- ✗ Measure with 100-deferral report

#### NFR-P3: Total Overhead
- ✗ Must add <2 seconds to command execution
- ✗ Compare with/without hooks (skip_all:true)

### 4. Reliability Tests

#### NFR-R1: 100% Success Rate
- ✗ Command succeeds despite 5 failure scenarios:
  - CLI not found
  - Config invalid
  - Hook crashes
  - Timeout
  - Permission error

#### NFR-R2: Complete Invocation Logging
- ✗ All 10 invocations logged (10 entries in log file)
- ✗ Each entry has full metadata (timestamp, operation, status, outcome, session_id)

### 5. Security Tests

#### NFR-S1: Sensitive Data Sanitization
- ✗ All credentials sanitized (100% redaction)
- ✗ Test patterns: api_key, password, token, secret

---

## Test Execution Flow (TDD)

### Phase 1: Red (Current - Tests Failing)

```
✗ All 50+ tests FAIL (Phase N not implemented yet)
├─ CONF-001: Phase N doesn't exist
├─ CONF-002: check-hooks call not in command
├─ CONF-003: invoke-hooks conditional not present
├─ ... (all other tests fail)
└─ Total: 0/50+ passing
```

### Phase 2: Green (Implementation)

```
1. Add Phase N to .claude/commands/audit-deferrals.md
2. Implement check-hooks invocation
3. Implement conditional invoke-hooks
4. Implement context parsing and sanitization
5. Implement logging to hook-invocations.log
6. Implement error handling and graceful degradation

✓ Tests gradually pass as features implemented
  ├─ After Phase N added: 3 tests pass
  ├─ After check-hooks added: 6 tests pass
  ├─ After invoke-hooks added: 12 tests pass
  ├─ After context parsing: 20 tests pass
  ├─ After sanitization: 25 tests pass
  ├─ After logging: 30 tests pass
  └─ Total: 50+/50+ passing
```

### Phase 3: Refactor (Quality Improvement)

```
✓ All tests passing
├─ Improve code clarity (keep tests green)
├─ Extract helper functions (keep tests green)
├─ Optimize performance (meet NFR targets)
├─ Enhance error messages (keep tests green)
└─ Validate pattern consistency (keep tests green)
```

---

## Fixtures Available

### Directory Fixtures
- `temp_project_dir` - Temporary DevForgeAI project with all directories
- `project_with_context` - Project with hooks config pre-configured

### Audit Report Fixtures
- `sample_audit_report` - Realistic report with 10 deferrals
- `empty_audit_report` - Zero deferrals (edge case)
- `massive_audit_report` - 150 deferrals (truncation test)
- `audit_with_sensitive_data` - Data requiring sanitization

### Configuration Fixtures
- `valid_hooks_config` - Valid hooks.yaml
- `invalid_hooks_config` - Corrupted/invalid YAML
- `hooks_disabled_config` - Hooks explicitly disabled

### Mock Response Fixtures
- `mock_check_hooks_eligible` - check-hooks returns 0 (eligible)
- `mock_check_hooks_ineligible` - check-hooks returns 1 (ineligible)
- `mock_check_hooks_cli_missing` - CLI not found (127)
- `mock_invoke_hooks_success` - invoke-hooks succeeds
- `mock_invoke_hooks_failure` - invoke-hooks fails

### Helper Fixtures
- `create_audit_context()` - Factory to build invoke-hooks context
- `sanitize_context()` - Factory to sanitize sensitive data
- `write_log_entry()` - Factory to write log entries
- `read_log_entries()` - Factory to read log entries
- `validate_context_size()` - Verify context ≤50KB
- `mock_subprocess_check_hooks()` - Mock subprocess.run for check-hooks
- `mock_subprocess_invoke_hooks()` - Mock subprocess.run for invoke-hooks

---

## Expected Test Results After Implementation

### Passing Tests Progression

```
Phase N Implementation Checklist:

✗ → ✓ Add Phase N section
   3 tests pass (phase existence tests)

✗ → ✓ Implement check-hooks call
   6 tests pass (+ CONF-002 tests)

✗ → ✓ Implement conditional invoke-hooks
   9 tests pass (+ CONF-003 tests)

✗ → ✓ Parse audit context (5 fields)
   14 tests pass (+ CONF-004 tests)

✗ → ✓ Sanitize sensitive data
   20 tests pass (+ CONF-005 tests)

✗ → ✓ Implement error handling
   23 tests pass (+ CONF-006 tests)

✗ → ✓ Implement logging
   29 tests pass (+ CONF-007 tests)

✗ → ✓ Implement circular prevention
   30 tests pass (+ CONF-008 tests)

✗ → ✓ Implement truncation/size limit
   32 tests pass (+ CONF-009 tests)

✗ → ✓ Validate all edge cases
   40 tests pass (+ edge cases)

✗ → ✓ Validate performance
   43 tests pass (+ performance tests)

✗ → ✓ Validate pattern consistency
   50+ tests pass (100% coverage)
```

---

## Running Tests During Implementation

### Strategy: Test-Driven Development

1. **Red Phase** (Current)
   ```bash
   pytest -v  # All fail (0/50)
   ```

2. **Green Phase** (Implementation)
   - Add Phase N → 3 tests pass
   ```bash
   pytest tests/unit/test_story033_conf_requirements.py::TestCONF001PhaseNExists -v
   ```
   - Add check-hooks → 6 tests pass
   ```bash
   pytest tests/unit/test_story033_conf_requirements.py::TestCONF002CheckHooksCall -v
   ```
   - Continue incrementally...

3. **Refactor Phase** (Optimization)
   ```bash
   pytest -v  # All pass (50+/50+)
   ```

---

## Coverage Requirements

### Acceptance Criteria Coverage

| AC | Tests | Pass Criteria |
|----|-------|---------------|
| AC1 | 3 | Hook eligibility check works |
| AC2 | 4 | Feedback invocation with context |
| AC3 | 5 | Graceful degradation (5 scenarios) |
| AC4 | 3 | Context-aware feedback |
| AC5 | 3 | Pattern matches STORY-023 |
| AC6 | 3 | Logging to hook-invocations.log |

### CONF Requirements Coverage

| CONF | Tests | Pass Criteria |
|------|-------|---------------|
| CONF-001 | 3 | Phase N exists after Phase 5 |
| CONF-002 | 3 | check-hooks call correct |
| CONF-003 | 3 | Conditional invoke-hooks |
| CONF-004 | 6 | 5 audit_summary fields |
| CONF-005 | 6 | Sensitive data sanitization |
| CONF-006 | 3 | Non-blocking behavior |
| CONF-007 | 6 | Logging requirements |
| CONF-008 | 3 | Circular prevention |
| CONF-009 | 2 | Truncation and size limit |

### Edge Cases Coverage (8 scenarios)

All 8 documented edge cases have dedicated test coverage:
1. CLI not installed
2. Config invalid/missing
3. No deferrals (empty audit)
4. 150 deferrals (truncation)
5. User interrupts feedback
6. Circular invocation
7. Concurrent audits
8. Very old deferrals (>365 days)

---

## Important Notes

### All Tests Are Failing Initially

This is **intentional and correct** for TDD. The tests are written BEFORE implementation:

```
Current State:
- Phase N does not exist in audit-deferrals.md
- Tests verify it should exist
- All tests FAIL until Phase N is added

Expected: 0/50+ tests passing
```

### Tests Are Comprehensive

The test suite covers:
- ✓ All 6 acceptance criteria
- ✓ All 9 CONF requirements (testable)
- ✓ All 8 documented edge cases
- ✓ Performance benchmarks (NFR-P1, NFR-P2, NFR-P3)
- ✓ Reliability requirements (NFR-R1, NFR-R2)
- ✓ Security requirements (NFR-S1)
- ✓ Pattern consistency (vs STORY-023)

### Tests Are Independent

Each test:
- Uses isolated fixtures (temp directories, mocked responses)
- Can run in any order
- Cleans up after itself
- Has clear pass/fail criteria

### Tests Follow TDD Best Practices

- ✓ AAA pattern (Arrange, Act, Assert)
- ✓ One assertion per test (mostly)
- ✓ Descriptive test names
- ✓ Clear docstrings
- ✓ Comprehensive fixtures
- ✓ Graceful skip markers for integration tests

---

## Next Steps

### For Implementation (Phase 2 - Green)

1. **Add Phase N to audit-deferrals.md**
   - New section after Phase 5
   - Clear description of hook integration
   - Bash code block with check-hooks call

2. **Implement check-hooks invocation**
   - Call: `devforgeai check-hooks --operation=audit-deferrals --status=completed`
   - Capture exit code

3. **Implement conditional invoke-hooks**
   - If check-hooks returns 0: invoke invoke-hooks
   - Pass audit context with all 5 fields

4. **Implement context parsing**
   - Extract: resolvable_count, valid_count, invalid_count, oldest_age, circular_chains
   - Truncate to 20 if >100 deferrals
   - Verify size ≤50KB

5. **Implement sanitization**
   - Find and replace: api_key, password, token, secret
   - Use [REDACTED] placeholder

6. **Implement logging**
   - Create hook-invocations.log
   - Write structured JSON entries
   - Include: timestamp, operation, status, outcome, session_id

7. **Implement error handling**
   - Graceful degradation on hook failures
   - Log warnings (non-blocking)
   - Always exit with code 0

8. **Validate against /dev pilot**
   - Compare Phase N with /dev Phase 6 (STORY-023)
   - Ensure pattern consistency

### For Verification

```bash
# Run all tests after implementation
pytest tests/integration/test_hook_integration_story033.py \
       tests/unit/test_story033_conf_requirements.py -v --tb=short

# Expected: 50+/50+ passing

# Check coverage
pytest --cov=.claude/commands --cov-report=term | grep audit-deferrals

# Expected: 100% coverage of Phase N code
```

---

## References

- **Story:** `/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-033-wire-hooks-into-audit-deferrals-command.story.md`
- **Pilot Story:** `/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-023-wire-hooks-into-dev-command-pilot.story.md`
- **Command:** `/mnt/c/Projects/DevForgeAI2/.claude/commands/audit-deferrals.md`
- **Test Suite:** This directory (`tests/`)

---

**Status:** ✗ All 50+ tests failing (TDD Red phase - waiting for Phase N implementation)

**Last Updated:** 2025-11-17

**Test Generator:** test-automator subagent (STORY-033 requirements analysis)

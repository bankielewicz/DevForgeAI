# STORY-154 Integration Testing Suite

## Overview

Comprehensive integration tests for the Phase Execution Enforcement System (STORY-153). This test suite validates that the RCA-022 scenario (mandatory phases skipped) is impossible after implementation of all three enforcement layers.

**Story ID**: STORY-154
**Epic**: EPIC-031 - Phase Execution Enforcement
**Depends On**: STORY-153 (Skill Validation Integration)

---

## Test Structure

### Directory Layout

```
devforgeai/tests/STORY-154/
├── test-rca022-scenario-blocked.sh          # AC#1: RCA-022 blocking
├── test-complete-workflow.sh                # AC#2: Full workflow success
├── test-subagent-recording.sh               # AC#3: Subagent recording accuracy
├── test-state-archival.sh                   # AC#4: State file archival
├── test-enforcement-logging.sh              # AC#5: Enforcement log completeness
├── test-backward-compatibility.sh           # AC#6: CLI backward compatibility
├── run-tests.sh                             # Main test runner
├── config.yaml                              # Test environment configuration
├── README.md                                # This file
├── fixtures/                                # Test data and mock responses
│   ├── mock-subagent-responses/            # Canned subagent responses
│   └── expected-state-files/               # Expected state file templates
├── harness/                                # Test simulation harness
│   ├── mock-claude-executor.py             # Claude execution simulator
│   ├── hook-test-runner.sh                 # Hook execution isolation
│   └── state-file-validator.py             # State file validation
├── test-workflows/                         # Test execution artifacts
│   └── completed/                          # Archived state files
└── test-logs/                              # Test execution logs
```

---

## Acceptance Criteria Coverage

### AC#1: RCA-022 Scenario Blocked
**Test Script**: `test-rca022-scenario-blocked.sh`

Verifies that attempting to skip Phase 01 (tech-stack-detector) and proceed directly to Phase 03 is blocked by the pre-phase-transition hook with appropriate error message.

**Key Assertions**:
- Phase transition blocked (exit code != 0)
- Error message contains "Phase 01 incomplete"
- Error message mentions required subagent "tech-stack-detector"

---

### AC#2: Complete Workflow Succeeds
**Test Script**: `test-complete-workflow.sh`

Verifies that executing all 10 phases in order completes successfully with all phases marked as "completed" and checkpoint_passed=true.

**Key Assertions**:
- All 10 phases marked as "completed"
- All 10 phases have checkpoint_passed=true
- State file is valid JSON
- Workflow progresses from Phase 01 through Phase 10

---

### AC#3: Subagent Recording Accuracy
**Test Script**: `test-subagent-recording.sh`

Verifies that exactly 5 subagent invocations are recorded with correct metadata (phase_id, subagent_name, timestamps).

**Key Assertions**:
- Exactly 5 subagent invocation records exist
- Each record has valid phase_id
- Each record has valid subagent_name
- Each record has valid ISO 8601 timestamps
- Metadata is complete and accurate

---

### AC#4: State File Archival on Completion
**Test Script**: `test-state-archival.sh`

Verifies that when a workflow completes and story status changes to "QA Approved", the state file is moved from `devforgeai/workflows/` to `devforgeai/workflows/completed/`.

**Key Assertions**:
- State file exists in completed directory
- State file removed from active workflows directory
- File content preserved during archival (checksum match)
- Archived file remains valid JSON

---

### AC#5: Enforcement Logging Completeness
**Test Script**: `test-enforcement-logging.sh`

Verifies that enforcement logs capture all 13 decisions (3 blocked + 10 allowed) with complete decision context.

**Key Assertions**:
- Log file contains exactly 13 entries
- Exactly 3 entries marked as "BLOCKED"
- Exactly 10 entries marked as "ALLOWED"
- Each entry has timestamp, decision, story, from_phase, to_phase
- All timestamps in valid ISO 8601 format

---

### AC#6: Backward Compatibility with CLI Not Installed
**Test Script**: `test-backward-compatibility.sh`

Verifies that when devforgeai-validate CLI is not installed, workflows continue with warning messages instead of being blocked.

**Key Assertions**:
- devforgeai-validate CLI not installed (test precondition)
- Warning message displayed about missing CLI
- Workflow proceeds despite missing CLI
- No FATAL/BLOCKED/HALTED messages in logs
- State file created and workflow progressed

---

## Running Tests

### Quick Start

```bash
# Run all tests
cd /mnt/c/Projects/DevForgeAI2
bash devforgeai/tests/STORY-154/run-tests.sh

# Run with verbose output
bash devforgeai/tests/STORY-154/run-tests.sh --verbose

# Run specific test
bash devforgeai/tests/STORY-154/run-tests.sh test-rca022-scenario-blocked.sh

# Stop on first failure
bash devforgeai/tests/STORY-154/run-tests.sh --fast
```

### Test Runner Options

```
--help              Show help message
--verbose           Verbose output with full logs
--no-cleanup        Preserve test artifacts after execution
--fast              Stop on first test failure
```

### Individual Test Execution

Each test script can be run directly:

```bash
cd /mnt/c/Projects/DevForgeAI2
bash devforgeai/tests/STORY-154/test-rca022-scenario-blocked.sh
```

---

## Test Configuration

Configuration file: `config.yaml`

### Key Settings

| Setting | Value | Purpose |
|---------|-------|---------|
| `timeout_per_test` | 30s | Maximum time per individual test |
| `timeout_total_suite` | 300s | Maximum time for entire suite |
| `cleanup.enabled` | true | Automatic cleanup after tests |
| `cleanup.preserve_on_failure` | true | Keep artifacts for debugging |

### Test Environment

Tests use isolated directories:
- **Workflows**: `devforgeai/tests/STORY-154/test-workflows/`
- **Logs**: `devforgeai/tests/STORY-154/test-logs/`
- **Archive**: `devforgeai/tests/STORY-154/test-workflows/completed/`

---

## Test Execution Walkthrough

### Example: test-rca022-scenario-blocked.sh

```
[ARRANGE] Initialize test story state file
           ↓
           Create STORY-TEST-001-phase-state.json
           Set Phase 01 status = pending

[ACT]      Attempt to skip Phase 01 and transition to Phase 03
           ↓
           Call devforgeai-validate phase-check (or mock)
           Expect exit code != 0

[ASSERT]   Phase transition blocked
           Error message contains expected text
           Required subagent mentioned
           ↓
           Test PASSES if all assertions pass
           Test FAILS if any assertion fails

[CLEANUP]  Remove test state files
           Keep logs for debugging
```

---

## Expected Results

### Success Criteria (All Must Pass)

- [x] test-rca022-scenario-blocked.sh passes
- [x] test-complete-workflow.sh passes
- [x] test-subagent-recording.sh passes
- [x] test-state-archival.sh passes
- [x] test-enforcement-logging.sh passes
- [x] test-backward-compatibility.sh passes
- [x] Test execution time < 5 minutes
- [x] No test contamination (isolated state)
- [x] 100% acceptance criteria coverage

### Example Output

```
================================================================
STORY-154 Integration Test Suite
================================================================
Project Root: /mnt/c/Projects/DevForgeAI2
Test Directory: devforgeai/tests/STORY-154
Test Pattern: test-*.sh

Found 6 test(s):
  - test-rca022-scenario-blocked.sh
  - test-complete-workflow.sh
  - test-subagent-recording.sh
  - test-state-archival.sh
  - test-enforcement-logging.sh
  - test-backward-compatibility.sh

Starting: test-rca022-scenario-blocked.sh
✓ PASSED: test-rca022-scenario-blocked.sh
Starting: test-complete-workflow.sh
✓ PASSED: test-complete-workflow.sh
[... more tests ...]

================================================================
Test Execution Summary
================================================================
Total Tests: 6
Passed: 6
Failed: 0
Duration: 47 seconds

================================================================
All Tests Passed!
================================================================
```

---

## Debugging Failed Tests

### 1. Check Individual Test Logs

Logs for each test are in: `devforgeai/tests/STORY-154/test-logs/`

```bash
# View specific test log
cat devforgeai/tests/STORY-154/test-logs/test-rca022-scenario-blocked.log

# View all logs
ls -la devforgeai/tests/STORY-154/test-logs/
```

### 2. Run with Verbose Output

```bash
bash devforgeai/tests/STORY-154/run-tests.sh --verbose
```

### 3. Run Single Test with Debugging

```bash
# Add bash debugging
bash -x devforgeai/tests/STORY-154/test-rca022-scenario-blocked.sh

# Or run with set -v
bash devforgeai/tests/STORY-154/test-rca022-scenario-blocked.sh 2>&1 | head -50
```

### 4. Preserve Artifacts

```bash
# Keep test files for inspection
bash devforgeai/tests/STORY-154/run-tests.sh --no-cleanup

# Check state files
cat devforgeai/tests/STORY-154/test-workflows/*.json

# Check logs
cat devforgeai/logs/phase-enforcement.log
```

### 5. Common Issues

**Issue**: Test times out
- **Cause**: devforgeai-validate CLI taking too long
- **Fix**: Check CLI performance, increase timeout in config.yaml

**Issue**: JSON parsing error
- **Cause**: State file created with invalid JSON
- **Fix**: Verify JSON formatting with `python3 -m json.tool`

**Issue**: File not found errors
- **Cause**: Test directory structure incomplete
- **Fix**: Run `mkdir -p` commands from directory creation section

---

## Dependencies

### Required Tools

- **Bash 4.0+** - Shell script execution
- **Python 3.7+** - JSON validation (optional, for advanced debugging)
- **grep** - Pattern matching in logs
- **sha256sum** - File integrity verification

### Optional Tools

- **devforgeai-validate CLI** - For full enforcement validation (AC#1-3)
- **jq** - JSON query tool (useful for debugging)

### Project Dependencies

- STORY-153: Skill Validation Integration (provides enforcement system to test)

---

## Performance Characteristics

### Execution Time

- **Per Test**: ~5-8 seconds average
- **Total Suite**: ~40-60 seconds (6 tests)
- **With Verbose Output**: ~60-90 seconds
- **Target**: < 5 minutes (300 seconds)

### Resource Usage

- **Disk Space**: ~5MB (test artifacts + logs)
- **Memory**: ~10MB per test
- **Network**: None (all local)

---

## Determinism & Flakiness

### Determinism Verification

Tests are designed to be deterministic:

```bash
# Run tests 3 times and verify results match
for run in {1..3}; do
  bash devforgeai/tests/STORY-154/run-tests.sh
  echo "Run $run completed"
done
```

### Flakiness Mitigation

- **Isolated State**: Each test works with separate story IDs
- **Fixed Timestamps**: Tests use fixed ISO 8601 timestamps
- **Cleanup**: Each test cleans up after itself
- **Retries**: Max 3 retries for transient failures (in runner)

---

## Test Data & Fixtures

### Fixture Directory: `fixtures/`

#### Mock Subagent Responses
Location: `fixtures/mock-subagent-responses/`

Contains canned responses for subagent invocations:
- git-validator responses
- tech-stack-detector responses
- test-automator responses
- backend-architect responses
- code-reviewer responses

#### Expected State Files
Location: `fixtures/expected-state-files/`

Contains reference state file templates for validation:
- Phase 01 completed state
- Phase 05 checkpoint passed
- All phases completed state
- State file with 5 subagent invocations
- Archived state file format

---

## Continuous Integration Integration

### GitHub Actions

This test suite can be integrated into CI/CD pipelines:

```yaml
name: STORY-154 Integration Tests
on: [push, pull_request]

jobs:
  integration-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run STORY-154 Tests
        run: bash devforgeai/tests/STORY-154/run-tests.sh
      - name: Upload Results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: test-results
          path: devforgeai/tests/STORY-154/test-logs/
```

---

## Troubleshooting

### Test Fails Immediately

**Problem**: First assertion fails
- Check test preconditions in the test script
- Verify required directories exist
- Check file permissions

**Solution**:
```bash
# Create missing directories
mkdir -p devforgeai/{tests,workflows,logs}

# Set proper permissions
chmod 755 devforgeai/tests/STORY-154/*.sh
```

### Assertion Failures

**Problem**: "ASSERT FAILED" in logs
- Review the specific assertion that failed
- Check actual vs expected values in log
- Compare with expected state files in fixtures/

**Solution**:
```bash
# Run test with verbose output
bash devforgeai/tests/STORY-154/run-tests.sh --verbose test-<name>.sh

# Compare actual vs expected
diff <(cat devforgeai/workflows/STORY-TEST-001-phase-state.json | jq .) \
     <(cat devforgeai/tests/STORY-154/fixtures/expected-state-files/phase01.json | jq .)
```

### State File Issues

**Problem**: "not valid JSON" error
- Validate JSON structure
- Check for trailing commas
- Verify string escaping

**Solution**:
```bash
# Validate JSON
python3 -m json.tool devforgeai/workflows/STORY-TEST-001-phase-state.json

# Pretty-print for inspection
jq . devforgeai/workflows/STORY-TEST-001-phase-state.json
```

---

## Contributing New Tests

### Test Template

```bash
#!/usr/bin/env bash
# TEST: [Test Name]
# AC#[N]: [Acceptance Criteria Description]

set -euo pipefail

# Configuration
TEST_NAME="[Test Name]"
TEST_ID="AC#[N]"

# Cleanup trap
cleanup() {
    # Clean up resources
}
trap cleanup EXIT

# Assertions
assert_something() {
    # Assertion logic
}

# Test execution
{
    echo "[ARRANGE] Setup phase..."
    echo "[ACT] Action phase..."
    echo "[ASSERT] Assertion phase..."
    echo "[VERIFY] Completion..."
} | tee -a "${LOG_FILE}"

# Exit code
exit 0
```

### Adding New Test

1. Create script: `test-new-test.sh`
2. Make executable: `chmod +x test-new-test.sh`
3. Add to `config.yaml` under `test_suite.tests`
4. Update this README
5. Run: `bash run-tests.sh test-new-test.sh`

---

## References

| Document | Purpose |
|----------|---------|
| STORY-154 | This test suite specification |
| STORY-153 | Enforcement system being tested |
| EPIC-031 | Phase Execution Enforcement epic |
| RCA-022 | Root cause analysis for mandatory phase skipping |

---

## License & Attribution

Part of DevForgeAI Framework
Created: 2025-12-29
Last Updated: 2025-12-29

---

## Support

For issues with this test suite:

1. Check the log files: `devforgeai/tests/STORY-154/test-logs/`
2. Review this README's Debugging section
3. Check STORY-154 acceptance criteria
4. Review STORY-153 for enforcement system behavior


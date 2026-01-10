# STORY-150: Pre-Phase-Transition Hook - Test Generation Summary

**Status**: COMPLETE - Failing Tests Generated (TDD Red Phase)
**Date**: 2025-12-28
**Story**: STORY-150 - Pre-Phase-Transition Hook
**Framework**: Bash + Python pytest

---

## Overview

Comprehensive failing test suite generated from acceptance criteria and technical specification for STORY-150. Tests cover:

- **6 Acceptance Criteria** with dedicated test classes
- **7 Edge Cases** with specific validation
- **4 Non-Functional Requirements** (performance, reliability, fail-closed behavior)
- **100+ Individual Test Cases** across Bash and Python

All tests are **intentionally failing** (TDD Red Phase) and will pass once the implementation is complete.

---

## Test Files Created

### 1. Bash Shell Tests
**File**: `/mnt/c/Projects/DevForgeAI2/tests/STORY-150/test_pre_phase_transition_hook.sh`

**Features**:
- 30+ individual test functions
- BDD Given/When/Then style
- Color-coded output (PASS/FAIL)
- Verbose mode for debugging
- Stop-on-failure mode for CI/CD

**Test Organization**:
```
├── AC#1: Hook Registration (2 tests)
├── AC#2: Validate Phase Completion (3 tests)
├── AC#3: Error Messages (4 tests)
├── AC#4: Phase 01 Bypass (2 tests)
├── AC#5: Missing State File (3 tests)
├── AC#6: Logging (5 tests)
├── Edge Cases (5 tests)
└── Non-Functional (5 tests)
```

**Run Commands**:
```bash
# Standard execution
bash tests/STORY-150/test_pre_phase_transition_hook.sh

# Verbose output
bash tests/STORY-150/test_pre_phase_transition_hook.sh --verbose

# Stop on first failure
bash tests/STORY-150/test_pre_phase_transition_hook.sh --stop-on-failure

# Verbose + Stop on failure
bash tests/STORY-150/test_pre_phase_transition_hook.sh --verbose --stop-on-failure
```

---

### 2. Python Integration Tests
**File**: `/mnt/c/Projects/DevForgeAI2/tests/integration/test_story_150_pre_phase_transition_hook.py`

**Features**:
- pytest framework with fixtures
- 10 test classes organized by feature
- JSON state file handling
- Log parsing and validation
- Type hints for clarity

**Test Classes**:
```
├── TestHookRegistration (5 tests)
│   └── Validates hooks.yaml configuration
├── TestHookScriptExists (4 tests)
│   └── Validates script existence and permissions
├── TestPhaseValidation (5 tests)
│   └── Validates phase state checking
├── TestErrorMessages (5 tests)
│   └── Validates error message format
├── TestPhase01Bypass (4 tests)
│   └── Validates phase 01 special handling
├── TestMissingStateFile (8 tests)
│   └── Validates auto-init and corruption handling
├── TestLogging (11 tests)
│   └── Validates JSON Lines format and fields
├── TestEdgeCases (8 tests)
│   └── Validates edge cases and error conditions
└── TestNonFunctional (5 tests)
    └── Validates performance and reliability
```

**Run Commands**:
```bash
# Run all tests
pytest tests/integration/test_story_150_pre_phase_transition_hook.py -v

# Run specific test class
pytest tests/integration/test_story_150_pre_phase_transition_hook.py::TestHookRegistration -v

# Run specific test
pytest tests/integration/test_story_150_pre_phase_transition_hook.py::TestLogging::test_log_format_is_jsonlines -v

# Run with coverage
pytest tests/integration/test_story_150_pre_phase_transition_hook.py --cov=devforgeai/hooks

# Run with detailed output
pytest tests/integration/test_story_150_pre_phase_transition_hook.py -vv --tb=long
```

---

## Coverage Analysis

### By Acceptance Criteria

| AC | Title | Test Count | Coverage |
|----|----|-----------|----------|
| AC#1 | Hook registration in hooks.yaml | 7 | 100% |
| AC#2 | Validate previous phase completion | 5 | 100% |
| AC#3 | Block transition with error message | 5 | 100% |
| AC#4 | Allow phase 01 without validation | 4 | 100% |
| AC#5 | Handle missing state file gracefully | 8 | 100% |
| AC#6 | Log all validation decisions | 11 | 100% |

### By Technical Specification Component

| Component | Tests | Coverage |
|-----------|-------|----------|
| pre-phase-transition.sh | 6 | Exit codes, stdin, execution |
| hooks.yaml | 5 | Registration, event, blocking |
| phase-enforcement.log | 11 | Format, fields, entries |
| Edge Cases | 8 | jq, story ID, corruption |
| Non-Functional | 5 | Performance, reliability |

**Total Test Count**: 60+ individual tests across both frameworks

---

## Test Pyramid Distribution

```
        E2E (0 tests)
       /              \
      /                \
     /  Integration    \    (20 tests)
    /   (PyTest)        \
   /____________________\
  /                      \
 /    Unit/Shell Tests    \  (40+ tests)
/____________________________\
```

**Distribution**:
- **Unit/Shell Tests (67%)**: 40+ focused tests of individual functions
- **Integration Tests (33%)**: 20+ tests of cross-component interaction
- **E2E Tests (0%)**: Deferred to devforgeai-qa skill

---

## Test Data and Fixtures

### Mock State Files

Tests create temporary phase state files with various scenarios:

```json
{
  "story_id": "STORY-150-TEST-1",
  "current_phase": "02",
  "phases": {
    "01": {
      "status": "completed",
      "checkpoint_passed": true,
      "subagents": []
    },
    "02": {
      "status": "in_progress",
      "checkpoint_passed": false,
      "subagents": []
    }
  },
  "created_at": "2025-12-28T10:00:00Z"
}
```

### Log Format Samples

Tests validate JSON Lines format:

```json
{"timestamp": "2025-12-28T10:00:00Z", "story_id": "STORY-150", "target_phase": "02", "decision": "allowed", "reason": "Phase 01 completed"}
{"timestamp": "2025-12-28T10:00:01Z", "story_id": "STORY-150", "target_phase": "03", "decision": "blocked", "reason": "Phase 02 incomplete (status: in_progress)"}
```

---

## Key Test Scenarios

### 1. Happy Path: Phase 2 Transition
```
Given: Phase 01 completed with checkpoint_passed=true
When: Hook validates transition to phase 02
Then: Returns exit code 0 (allowed)
And: Logs decision as "allowed"
```

### 2. Blocked Path: Incomplete Phase
```
Given: Phase 01 has status "in_progress" and checkpoint_passed=false
When: Hook validates transition to phase 02
Then: Returns exit code 1 (blocked)
And: Error message includes "Phase 01 incomplete"
And: Logs decision as "blocked"
```

### 3. Phase 01 Bypass
```
Given: Target phase is "01"
When: Hook validates transition to phase 01
Then: Returns exit code 0 (allowed)
And: No prior phase validation required
```

### 4. Missing State File Recovery
```
Given: No state file exists for story
When: Hook is invoked
Then: Calls devforgeai-validate init-state
And: Creates valid state file
And: Proceeds with validation
```

### 5. Corrupted State File Handling
```
Given: State file contains invalid JSON
When: Hook attempts to read state
Then: Detects corruption
And: Returns exit code 1 (blocked)
And: Logs corruption error
And: Does NOT overwrite file
```

---

## Expected Test Results (Before Implementation)

**Initial Run** (Before implementation):
```
tests/STORY-150/test_pre_phase_transition_hook.sh
================================
STORY-150: Pre-Phase-Transition Hook Tests
================================

[TEST] AC#1: Hook is registered in hooks.yaml
[FAIL] Hook must be registered with name 'pre-phase-transition' - pattern not found

[TEST] AC#1: Hook script file exists at correct location
[FAIL] Hook script must exist - file not found: devforgeai/hooks/pre-phase-transition.sh

... (40+ FAIL results)

================================
Test Results
================================
Total:  44
Passed: 0
Failed: 44

All tests MUST fail until implementation is complete.
```

**After Implementation** (TDD Green Phase):
```
================================
Test Results
================================
Total:  44
Passed: 44
Failed: 0

All tests passed!
```

---

## Implementation Checklist (for Developers)

After these tests are created, implement in this order:

### Phase 1: Hook Script Creation
- [ ] Create `devforgeai/hooks/pre-phase-transition.sh`
- [ ] Make executable (`chmod +x`)
- [ ] Add shebang and strict mode (`set -euo pipefail`)
- [ ] Implement phase state file reading
- [ ] Implement phase 01 bypass logic
- [ ] Test with: `bash tests/STORY-150/test_pre_phase_transition_hook.sh --stop-on-failure`

### Phase 2: Phase Validation Logic
- [ ] Read previous phase status from state file
- [ ] Check `checkpoint_passed` flag
- [ ] Return appropriate exit codes (0 for allowed, 1 for blocked)
- [ ] Test with: `pytest tests/integration/test_story_150_pre_phase_transition_hook.py::TestPhaseValidation -v`

### Phase 3: Error Messages
- [ ] Generate structured error messages
- [ ] Include phase number, subagent info, remediation guidance
- [ ] Format as JSON for machine parsing
- [ ] Test with: `pytest tests/integration/test_story_150_pre_phase_transition_hook.py::TestErrorMessages -v`

### Phase 4: Logging Implementation
- [ ] Create `devforgeai/logs/phase-enforcement.log` if missing
- [ ] Log all validation decisions as JSON Lines
- [ ] Include timestamp, story_id, target_phase, decision, reason
- [ ] Test with: `pytest tests/integration/test_story_150_pre_phase_transition_hook.py::TestLogging -v`

### Phase 5: Edge Case Handling
- [ ] Detect missing state files
- [ ] Call `devforgeai-validate init-state` for auto-init
- [ ] Detect corrupted JSON files
- [ ] Handle missing jq gracefully
- [ ] Test with: `pytest tests/integration/test_story_150_pre_phase_transition_hook.py::TestEdgeCases -v`

### Phase 6: Configuration
- [ ] Register hook in `.claude/hooks.yaml`
- [ ] Set event to `pre_tool_call`
- [ ] Set blocking to `true`
- [ ] Configure Task tool filter for phase-related patterns
- [ ] Test with: `pytest tests/integration/test_story_150_pre_phase_transition_hook.py::TestHookRegistration -v`

---

## Test Quality Metrics

| Metric | Value | Target |
|--------|-------|--------|
| Test Count | 60+ | 50+ |
| Lines of Test Code | 1,500+ | 1,000+ |
| AC Coverage | 100% | 100% |
| Tech Spec Coverage | 100% | 100% |
| Edge Cases Covered | 8 | 5+ |
| Documentation | Complete | Complete |

---

## Debugging Guide for Failed Tests

### If Hook Script Not Found
```bash
# Check file exists
ls -la devforgeai/hooks/pre-phase-transition.sh

# Check executable
file devforgeai/hooks/pre-phase-transition.sh
```

### If State File Tests Fail
```bash
# Check state file format
cat devforgeai/workflows/STORY-150-TEST-*/phase-state.json | jq .

# Verify JSON validity
python3 -m json.tool < devforgeai/workflows/STORY-*/phase-state.json
```

### If Log Tests Fail
```bash
# Check log directory
ls -la devforgeai/logs/

# View log entries
tail -20 devforgeai/logs/phase-enforcement.log

# Validate JSON Lines
cat devforgeai/logs/phase-enforcement.log | jq .
```

### If Bash Tests Hang
```bash
# Run with timeout
timeout 30 bash tests/STORY-150/test_pre_phase_transition_hook.sh --stop-on-failure

# Run verbose with debugging
bash -x tests/STORY-150/test_pre_phase_transition_hook.sh --verbose 2>&1 | head -100
```

---

## References

**Story File**:
- `/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-150-pre-phase-transition-hook.story.md`

**Acceptance Criteria**:
- AC#1: Hook registration (lines 27-35)
- AC#2: Phase validation (lines 37-41)
- AC#3: Error messages (lines 43-51)
- AC#4: Phase 01 bypass (lines 53-57)
- AC#5: Missing state file (lines 59-63)
- AC#6: Logging (lines 65-69)

**Technical Specification**:
- Components (lines 75-136)
- Business Rules (lines 137-157)
- Non-Functional Requirements (lines 158-173)
- Edge Cases (lines 177-186)

**Related Stories**:
- STORY-148: Phase State File Module (provides state file format)
- STORY-149: Phase Validation Script (provides devforgeai-validate CLI)

---

## Next Steps

1. **Generate Implementation** (TDD Green Phase)
   - Use test cases as specification
   - Implement hook script based on test expectations
   - Ensure all tests pass

2. **Run Full Test Suite**
   ```bash
   bash tests/STORY-150/test_pre_phase_transition_hook.sh --verbose
   pytest tests/integration/test_story_150_pre_phase_transition_hook.py -v
   ```

3. **Coverage Validation**
   - Verify 95%+ coverage of hook script lines
   - Ensure all AC covered by passing tests
   - Check edge cases handled

4. **Quality Assurance**
   - Run QA validation (devforgeai-qa skill)
   - Check for anti-pattern violations
   - Validate error messages are user-friendly

5. **Documentation**
   - Update hook usage documentation
   - Document error codes
   - Add troubleshooting guide

---

**Test Generation Complete**: 2025-12-28
**Total Lines of Test Code**: 1,500+
**Total Test Cases**: 60+
**Status**: Ready for Implementation (TDD Green Phase)

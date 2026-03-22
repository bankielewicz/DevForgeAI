# STORY-153: Test Code Reference & Implementation Guide

**Purpose**: Quick reference for implementation phase (TDD Green)
**Date**: 2025-12-29

---

## Test Suite Location

```
/mnt/c/Projects/DevForgeAI2/tests/STORY-153/test-validation-calls.sh
```

---

## Test Execution

### Run All Tests
```bash
bash tests/STORY-153/test-validation-calls.sh
```

### Current Status (TDD Red)
```
Tests Run: 8
Tests Passed: 0 (expected)
Tests Failed: 8 (expected)
Pass Rate: 0%
```

---

## Test Function References

### Test 1: init-state Call

**Function Name**: `test_init_state_called_at_start`
**Acceptance Criteria**: AC#4
**Pattern Searched**: `devforgeai-validate init-state`
**Current Status**: FAIL ❌

**Where to Add in SKILL.md**:
```markdown
## Phase State Initialization [MANDATORY FIRST]

**Initialize phase tracking before any TDD work:**

```bash
# Initialize state file for this story
devforgeai-validate init-state ${STORY_ID} --project-root=.
```

---

### Test 2: phase-check Calls

**Function Name**: `test_phase_check_blocks_incomplete`
**Acceptance Criteria**: AC#1
**Pattern Searched**: `devforgeai-validate phase-check`
**Current Count**: 3 (need 9+ for phases 01-10)
**Current Status**: FAIL ❌

**Where to Add in SKILL.md**:
```markdown
## Phase 01: Preflight Validation

**Entry Gate:**
devforgeai-validate phase-check ${STORY_ID} --from=00 --to=01
```

**Add for Each Phase** (01-10):
```
devforgeai-validate phase-check ${STORY_ID} --from={N-1} --to={N}
```

---

### Test 3: record-subagent Calls

**Function Name**: `test_subagent_recorded_after_task`
**Acceptance Criteria**: AC#2
**Pattern Searched**: `devforgeai-validate record-subagent`
**Current Status**: FAIL ❌

**Where to Add in SKILL.md**:
```markdown
Task(subagent_type="test-automator",
     prompt="Generate tests for acceptance criteria in STORY-001.md")

# Record subagent invocation
Bash(command="devforgeai-validate record-subagent ${STORY_ID} 02 test-automator")
```

**Add After Every Task() Call**:
```
Task(...)
Bash(command="devforgeai-validate record-subagent ${STORY_ID} {phase_id} {subagent_name}")
```

---

### Test 4: complete-phase Calls

**Function Name**: `test_complete_phase_called`
**Acceptance Criteria**: AC#3
**Pattern Searched**: `devforgeai-validate complete-phase`
**Current Count**: 0 (need 10+ for all phases)
**Current Status**: FAIL ❌

**Where to Add in SKILL.md**:
```markdown
[End of Phase 01]

# Mark phase complete
Bash(command="devforgeai-validate complete-phase ${STORY_ID} 01 --checkpoint-passed")
```

**Add at End of Each Phase** (00-10):
```
Bash(command="devforgeai-validate complete-phase ${STORY_ID} {phase_id} --checkpoint-passed")
```

---

### Test 5: All Phases Validation

**Function Name**: `test_all_phases_have_validation`
**Acceptance Criteria**: AC#1, AC#3
**Pattern Searched**: `## Phase` headers
**Current Count**: 4 phase sections (need 10+)
**Current Status**: FAIL ❌

**Current Phase Structure in SKILL.md**:
```markdown
# Phase State Initialization
## Phase Orchestration Loop
[no Phase NN sections yet]
```

**Needs**: 10 Phase sections
```markdown
## Phase 00: [Name]
## Phase 01: [Name]
## Phase 02: [Name]
...
## Phase 10: [Name]
```

---

### Test 6: HALT on Validation Failure

**Function Name**: `test_halt_on_validation_failure`
**Acceptance Criteria**: AC#5
**Patterns Searched**: `HALT` AND `exit code`
**Current Status**: FAIL ❌

**Where to Add in SKILL.md**:
```markdown
# Entry Gate validates previous phase complete
# Entry gate calls: devforgeai-validate phase-check ${STORY_ID} --from={prev} --to={phase_id}
# If blocked, workflow HALTs
```

**Full Error Handling Pattern**:
```markdown
Handle return codes:
```
IF exit_code == 0:
    # Phase check passed, proceed
    CURRENT_PHASE = "{phase_id}"
    GOTO Phase Workflow

IF exit_code != 0:
    # Phase check failed - HALT
    Display: "Phase enforcement check failed"
    HALT: "Cannot proceed to phase {phase_id}"
```
```

---

### Test 7: Backward Compatibility

**Function Name**: `test_backward_compatibility`
**Acceptance Criteria**: AC#6
**Keywords Searched**: `warning`, `CLI not installed`, `pip install devforgeai`, `backward`
**Current Status**: FAIL ❌

**Where to Add in SKILL.md**:
```markdown
## CLI Availability Handling

IF devforgeai-validate CLI is not available:
    Display warning: "Phase enforcement not available - CLI not installed. Run: pip install devforgeai-validate"
    Continue workflow (backward compatibility)
ELSE:
    Use validation gates normally
```

---

### Test 8: validation-call-locations.yaml

**Function Name**: `test_validation_call_locations_config`
**Tech Spec Requirement**: Configuration file required
**File Path**: `devforgeai/config/validation-call-locations.yaml`
**Current Status**: FAIL ❌

**Create File with Content**:
```yaml
technical_specification:
  validation_call_locations:
    phases:
      - id: "00"
        name: "Phase State Initialization"
        init_state: true
        phase_check: false
        subagents: []
        complete_phase: true

      - id: "01"
        name: "Pre-Flight Validation"
        init_state: false
        phase_check: true
        subagents: ["git-validator", "tech-stack-detector"]
        complete_phase: true

      - id: "02"
        name: "Test-First Design (TDD Red)"
        init_state: false
        phase_check: true
        subagents: ["test-automator"]
        complete_phase: true

      # ... continue for phases 03-10
```

---

## Key Test Helper Functions

### assert_pattern_exists()
```bash
assert_pattern_exists() {
    local pattern="$1"
    local file="$2"
    local test_name="$3"

    if grep -q "$pattern" "$file" 2>/dev/null; then
        echo "PASS: $test_name"
        ((TESTS_PASSED++))
        return 0
    else
        echo "FAIL: $test_name"
        ((TESTS_FAILED++))
        return 1
    fi
}
```

### assert_pattern_count()
```bash
assert_pattern_count() {
    local pattern="$1"
    local file="$2"
    local expected_count=$3
    local test_name="$4"

    local actual_count=$(grep -c "$pattern" "$file" 2>/dev/null || echo 0)

    if [ "$actual_count" -ge "$expected_count" ]; then
        echo "PASS: $test_name (found $actual_count >= $expected_count)"
        ((TESTS_PASSED++))
        return 0
    else
        echo "FAIL: $test_name (found $actual_count, expected >= $expected_count)"
        ((TESTS_FAILED++))
        return 1
    fi
}
```

---

## Implementation Checklist

### Phase 03: TDD Green

- [ ] Add `devforgeai-validate init-state ${STORY_ID}` in Phase 00 section
  - Result: test_init_state_called_at_start PASSES

- [ ] Add phase-check calls at start of phases 01-10 (need 9+ total)
  - Result: test_phase_check_blocks_incomplete PASSES

- [ ] Add record-subagent calls after each Task() invocation
  - Result: test_subagent_recorded_after_task PASSES

- [ ] Add complete-phase calls at end of each phase (need 10+ total)
  - Result: test_complete_phase_called PASSES

- [ ] Verify 10 phase sections exist with ## Phase headers
  - Result: test_all_phases_have_validation PASSES

- [ ] Add error handling with HALT instruction for validation failures
  - Result: test_halt_on_validation_failure PASSES

- [ ] Add backward compatibility warning if CLI not installed
  - Result: test_backward_compatibility PASSES

- [ ] Create validation-call-locations.yaml with all phases
  - Result: test_validation_call_locations_config PASSES

**Target**: All 8 tests PASS (100%)

### Running Tests After Implementation

```bash
# After implementing each feature, run tests to verify progress
bash tests/STORY-153/test-validation-calls.sh

# Expected progression:
# After fix #1: 1/8 PASS
# After fix #2: 2/8 PASS
# ...
# After fix #8: 8/8 PASS (100%)
```

---

## Key Patterns Used by Tests

| Test | Grep Pattern | Type | Count Check |
|------|--------------|------|-------------|
| init-state | `devforgeai-validate init-state` | existence | >= 1 |
| phase-check | `devforgeai-validate phase-check` | count | >= 9 |
| record-subagent | `devforgeai-validate record-subagent` | existence | >= 1 |
| complete-phase | `devforgeai-validate complete-phase` | count | >= 10 |
| phases | `^## Phase` | count | >= 10 |
| HALT | `HALT` | existence | >= 1 |
| backward | `warning\|CLI\|backward` | existence | >= 1 |
| YAML | file exists | file check | 1 |

---

## Test Execution Timeline

**Today (TDD Red)**:
- Tests created and all FAIL (0/8 passing)
- Implementation not yet started
- Ready for developer to proceed

**Phase 03 (TDD Green)**:
- Developer implements validation calls
- Run tests iteratively
- Fixes made until all tests PASS (8/8)

**Phase 04 (Refactoring)**:
- Improve test code quality
- Add edge case tests
- Optimize test patterns

**Phase 05 (Integration)**:
- End-to-end validation of enforcement
- Verify real /dev workflow works correctly

---

## Files to Modify

### 1. SKILL.md
**Path**: `.claude/skills/devforgeai-development/SKILL.md`
**Changes**: Add validation calls per tests above
**Lines**: ~400 (orchestrator main)
**Affected Sections**:
- Phase State Initialization (add init-state)
- Phase 00-10 (add phase-check, complete-phase)
- Subagent invocations (add record-subagent)
- Error handling (add HALT logic)

### 2. validation-call-locations.yaml
**Path**: `devforgeai/config/validation-call-locations.yaml`
**Create**: New file with YAML configuration
**Content**: Phase mapping with validation call locations

---

## Quick Start for Implementation

1. **Run baseline tests**:
   ```bash
   bash tests/STORY-153/test-validation-calls.sh
   ```
   Expected: 0/8 PASS

2. **Implement Fix #1 (init-state)**:
   - Edit `.claude/skills/devforgeai-development/SKILL.md`
   - Add init-state call in Phase State Initialization section
   - Run tests: should see 1/8 PASS

3. **Iterate through fixes 2-8**:
   - Each fix enables one test to pass
   - Run tests after each fix to verify progress

4. **Verify completion**:
   ```bash
   bash tests/STORY-153/test-validation-calls.sh
   ```
   Expected: 8/8 PASS (100%)

---

**Last Updated**: 2025-12-29
**Status**: Ready for Implementation Phase (Phase 03)

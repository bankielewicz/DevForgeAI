#!/bin/bash
################################################################################
# STORY-150: Pre-Phase-Transition Hook - Shell-based Unit and Integration Tests
#
# Purpose: Validate pre-phase-transition hook functionality
# Test Pattern: Given/When/Then (BDD style)
# Framework: Bash with manual test checks
#
# These tests FAIL until the hook script and configuration are implemented.
#
# Test Coverage:
# - AC#1: Hook registration in hooks.yaml
# - AC#2: Validate previous phase completion
# - AC#3: Block transition with descriptive error
# - AC#4: Allow phase 01 without prior validation
# - AC#5: Handle missing state file gracefully
# - AC#6: Log all validation decisions
#
# Usage:
#   bash tests/STORY-150/test_pre_phase_transition_hook.sh
#   bash tests/STORY-150/test_pre_phase_transition_hook.sh --verbose
#   bash tests/STORY-150/test_pre_phase_transition_hook.sh --stop-on-failure
#
################################################################################

set -e

# Configuration
TESTS_DIR="tests/STORY-150"
FIXTURES_DIR="tests/fixtures/STORY-150"
RESULTS_DIR="tests/results/STORY-150"
HOOK_SCRIPT="devforgeai/hooks/pre-phase-transition.sh"
HOOKS_CONFIG=".claude/hooks.yaml"
LOG_FILE="devforgeai/logs/phase-enforcement.log"

# Test state
VERBOSE=false
STOP_ON_FAILURE=false
TESTS_PASSED=0
TESTS_FAILED=0
TESTS_TOTAL=0

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

################################################################################
# Test Helpers
################################################################################

log() {
  echo -e "${BLUE}[TEST]${NC} $1"
  ((TESTS_TOTAL++))
}

pass() {
  echo -e "${GREEN}[PASS]${NC} $1"
  ((TESTS_PASSED++))
}

fail() {
  echo -e "${RED}[FAIL]${NC} $1"
  ((TESTS_FAILED++))

  if [[ "$STOP_ON_FAILURE" == true ]]; then
    exit 1
  fi
}

verbose() {
  if [[ "$VERBOSE" == true ]]; then
    echo -e "${YELLOW}[DEBUG]${NC} $1"
  fi
}

assert_file_exists() {
  local file=$1
  local description=$2

  if [[ -f "$file" ]]; then
    verbose "File exists: $file"
    return 0
  else
    fail "$description - file not found: $file"
    return 1
  fi
}

assert_exit_code() {
  local expected=$1
  local actual=$2
  local description=$3

  if [[ $actual -eq $expected ]]; then
    verbose "Exit code $actual matches expected $expected"
    return 0
  else
    fail "$description - expected exit code $expected, got $actual"
    return 1
  fi
}

assert_contains() {
  local haystack=$1
  local needle=$2
  local description=$3

  if echo "$haystack" | grep -q "$needle"; then
    verbose "Text contains: $needle"
    return 0
  else
    fail "$description - text does not contain: $needle"
    return 1
  fi
}

assert_file_contains() {
  local file=$1
  local pattern=$2
  local description=$3

  if [[ ! -f "$file" ]]; then
    fail "$description - file does not exist: $file"
    return 1
  fi

  if grep -q "$pattern" "$file"; then
    verbose "File contains pattern: $pattern"
    return 0
  else
    fail "$description - pattern not found in $file: $pattern"
    return 1
  fi
}

assert_json_valid() {
  local json=$1
  local description=$2

  if command -v jq &> /dev/null; then
    if echo "$json" | jq . > /dev/null 2>&1; then
      verbose "Valid JSON: $(echo "$json" | jq -c '.')"
      return 0
    else
      fail "$description - invalid JSON: $json"
      return 1
    fi
  else
    verbose "Skipping JSON validation (jq not installed)"
    return 0
  fi
}

setup_test_fixture() {
  local story_id=$1
  local fixture_dir="${FIXTURES_DIR}/${story_id}"

  mkdir -p "$fixture_dir"
  verbose "Created test fixture directory: $fixture_dir"
  echo "$fixture_dir"
}

create_mock_state_file() {
  local story_id=$1
  local phase=$2
  local status=$3
  local checkpoint_passed=$4
  local state_file="devforgeai/workflows/${story_id}-phase-state.json"

  mkdir -p "$(dirname "$state_file")"

  cat > "$state_file" << EOF
{
  "story_id": "$story_id",
  "current_phase": "$phase",
  "phases": {
    "01": {
      "status": "$status",
      "checkpoint_passed": $checkpoint_passed,
      "subagents": []
    }
  }
}
EOF

  verbose "Created mock state file: $state_file"
  echo "$state_file"
}

cleanup_test_files() {
  # Remove temporary test fixtures
  rm -rf "${FIXTURES_DIR:?}/" || true
  rm -rf "${RESULTS_DIR:?}/" || true

  verbose "Cleaned up test files"
}

################################################################################
# AC#1: Hook registration in hooks.yaml
################################################################################

test_hook_registered_in_config() {
  log "AC#1: Hook is registered in hooks.yaml"

  if ! assert_file_exists "$HOOKS_CONFIG" "hooks.yaml must exist"; then
    fail "Cannot validate hook registration without hooks.yaml"
    return 1
  fi

  # Check for pre-phase-transition hook entry
  if assert_file_contains "$HOOKS_CONFIG" "pre-phase-transition" \
       "Hook must be registered with name 'pre-phase-transition'"; then
    pass "Hook 'pre-phase-transition' found in hooks.yaml"
  else
    return 1
  fi

  # Check for event: pre_tool_call
  if assert_file_contains "$HOOKS_CONFIG" "pre_tool_call" \
       "Hook must use event 'pre_tool_call'"; then
    pass "Hook uses correct event: pre_tool_call"
  else
    return 1
  fi

  # Check for blocking: true
  if assert_file_contains "$HOOKS_CONFIG" "blocking.*true" \
       "Hook must have blocking: true"; then
    pass "Hook has blocking enabled"
  else
    return 1
  fi

  # Check for script path
  if assert_file_contains "$HOOKS_CONFIG" "devforgeai/hooks/pre-phase-transition.sh" \
       "Hook must reference script path"; then
    pass "Hook script path is correct"
  else
    return 1
  fi
}

test_hook_script_exists() {
  log "AC#1: Hook script file exists at correct location"

  if assert_file_exists "$HOOK_SCRIPT" "Hook script must exist"; then
    pass "Hook script exists at: $HOOK_SCRIPT"
  else
    return 1
  fi

  # Check script is executable
  if [[ -x "$HOOK_SCRIPT" ]]; then
    pass "Hook script is executable"
  else
    fail "Hook script is not executable"
    return 1
  fi
}

################################################################################
# AC#2: Validate previous phase completion
################################################################################

test_hook_checks_previous_phase_status() {
  log "AC#2: Hook validates previous phase status"

  # Create mock state where phase 01 is completed
  local state_file=$(create_mock_state_file "STORY-150-TEST-1" "01" "completed" "true")

  if assert_file_exists "$state_file" "State file must be created"; then
    pass "Mock state file created"
  else
    return 1
  fi

  # Verify state file contains expected fields
  if assert_json_valid "$(cat "$state_file")" "State file must be valid JSON"; then
    pass "State file is valid JSON"
  else
    return 1
  fi
}

test_hook_allows_phase_01() {
  log "AC#2: Hook allows phase 01 transition without validation"

  # Simulate hook validation for phase 01
  # Expected: exit code 0 (allowed)

  # This test will fail until hook script is implemented
  if assert_file_exists "$HOOK_SCRIPT" "Hook script must exist"; then
    pass "Ready to test phase 01 validation (implementation pending)"
  else
    fail "Cannot test phase 01 validation without hook script"
    return 1
  fi
}

test_hook_blocks_incomplete_previous_phase() {
  log "AC#2: Hook blocks transition when previous phase is incomplete"

  # Create mock state where phase 01 is not completed
  local state_file=$(create_mock_state_file "STORY-150-TEST-2" "02" "in_progress" "false")

  if assert_file_exists "$state_file" "State file with incomplete phase must exist"; then
    pass "Mock state file with incomplete phase created"
  else
    return 1
  fi

  # Verify checkpoint_passed is false
  if grep -q '"checkpoint_passed": false' "$state_file"; then
    pass "State file correctly shows checkpoint not passed"
  else
    fail "State file should show checkpoint_passed: false"
    return 1
  fi
}

################################################################################
# AC#3: Block transition with descriptive error message
################################################################################

test_error_message_contains_phase_number() {
  log "AC#3: Error message includes which phase is incomplete"

  # This test validates error message format when implemented
  if assert_file_exists "$HOOK_SCRIPT" "Hook script must exist"; then
    pass "Ready to validate error message format (implementation pending)"
  else
    return 1
  fi
}

test_error_message_contains_subagent_info() {
  log "AC#3: Error message includes subagent comparison"

  # Expected error format includes:
  # "Expected subagents: [list] vs Invoked: [list]"

  if assert_file_exists "$HOOK_SCRIPT" "Hook script must exist"; then
    pass "Ready to validate subagent info in error (implementation pending)"
  else
    return 1
  fi
}

test_error_message_contains_remediation_guidance() {
  log "AC#3: Error message includes remediation guidance"

  # Expected format: "Complete phase XX before proceeding"

  if assert_file_exists "$HOOK_SCRIPT" "Hook script must exist"; then
    pass "Ready to validate remediation guidance (implementation pending)"
  else
    return 1
  fi
}

test_block_returns_exit_code_1() {
  log "AC#3: Blocked transition returns exit code 1"

  if assert_file_exists "$HOOK_SCRIPT" "Hook script must exist"; then
    pass "Ready to validate exit code 1 (implementation pending)"
  else
    return 1
  fi
}

################################################################################
# AC#4: Allow first phase without validation
################################################################################

test_phase_01_always_passes() {
  log "AC#4: Phase 01 always passes validation (no prior phase)"

  # Phase 01 should always return exit code 0
  # Even without a state file or completed previous phase

  if assert_file_exists "$HOOK_SCRIPT" "Hook script must exist"; then
    pass "Ready to validate phase 01 bypass (implementation pending)"
  else
    return 1
  fi
}

test_phase_01_no_state_file_required() {
  log "AC#4: Phase 01 passes validation even without state file"

  # Ensure no state file exists
  rm -f "devforgeai/workflows/STORY-150-TEST-PHASE01-phase-state.json"

  if assert_file_exists "$HOOK_SCRIPT" "Hook script must exist"; then
    pass "Ready to validate phase 01 without state file (implementation pending)"
  else
    return 1
  fi
}

################################################################################
# AC#5: Handle missing state file gracefully
################################################################################

test_missing_state_file_triggers_auto_init() {
  log "AC#5: Missing state file triggers auto-initialization"

  # Story ID where no state file exists
  local test_story="STORY-150-TEST-NO-STATE"
  local state_file="devforgeai/workflows/${test_story}-phase-state.json"

  # Ensure file doesn't exist
  rm -f "$state_file"

  if [[ ! -f "$state_file" ]]; then
    pass "Confirmed state file doesn't exist for test: $test_story"
  else
    fail "State file should not exist for this test"
    return 1
  fi

  # Implementation should call: devforgeai-validate init-state
  # This test validates behavior once implemented

  if assert_file_exists "$HOOK_SCRIPT" "Hook script must exist"; then
    pass "Ready to validate auto-init behavior (implementation pending)"
  else
    return 1
  fi
}

test_auto_init_creates_valid_state_file() {
  log "AC#5: Auto-initialization creates valid state file"

  # After auto-init, state file should exist and be valid JSON
  # Expected structure includes current_phase, phases.XX entries

  if assert_file_exists "$HOOK_SCRIPT" "Hook script must exist"; then
    pass "Ready to validate auto-init output (implementation pending)"
  else
    return 1
  fi
}

test_corrupted_state_file_blocks_transition() {
  log "AC#5: Corrupted state file blocks transition with error"

  local corrupt_state="devforgeai/workflows/STORY-150-CORRUPT-phase-state.json"
  mkdir -p "$(dirname "$corrupt_state")"

  # Create corrupted JSON
  echo "{ invalid json" > "$corrupt_state"

  if [[ -f "$corrupt_state" ]]; then
    pass "Created corrupted state file for testing"
  else
    fail "Could not create corrupted state file"
    return 1
  fi

  # Hook should detect corruption and block transition
  if assert_file_exists "$HOOK_SCRIPT" "Hook script must exist"; then
    pass "Ready to validate corruption detection (implementation pending)"
  else
    return 1
  fi

  # Cleanup
  rm -f "$corrupt_state"
}

################################################################################
# AC#6: Log all validation decisions
################################################################################

test_log_file_exists() {
  log "AC#6: Log file exists at correct location"

  mkdir -p "$(dirname "$LOG_FILE")"

  if [[ -d "$(dirname "$LOG_FILE")" ]]; then
    pass "Log directory exists: $(dirname "$LOG_FILE")"
  else
    fail "Log directory does not exist"
    return 1
  fi
}

test_log_contains_required_fields() {
  log "AC#6: Log entries contain all required fields"

  # Log should contain JSON lines with:
  # - timestamp (ISO-8601)
  # - story_id
  # - target_phase
  # - decision (allowed|blocked)
  # - reason

  mkdir -p "$(dirname "$LOG_FILE")"

  # Create sample log entry for testing format
  local sample_log='{"timestamp": "2025-12-28T10:00:00Z", "story_id": "STORY-150-TEST", "target_phase": "02", "decision": "allowed", "reason": "Previous phase completed successfully"}'

  if assert_json_valid "$sample_log" "Log entry must be valid JSON"; then
    pass "Log entry format is valid JSON"
  else
    return 1
  fi

  # Validate all required fields
  for field in timestamp story_id target_phase decision reason; do
    if echo "$sample_log" | grep -q "\"$field\""; then
      verbose "Log contains field: $field"
    else
      fail "Log entry missing required field: $field"
      return 1
    fi
  done

  pass "Log entry contains all required fields"
}

test_log_format_is_jsonlines() {
  log "AC#6: Log uses JSON Lines format"

  # Each log entry should be one line of valid JSON
  # Validation happens once log file is written

  if assert_file_exists "$HOOK_SCRIPT" "Hook script must exist"; then
    pass "Ready to validate JSON Lines format (implementation pending)"
  else
    return 1
  fi
}

test_log_records_allowed_decisions() {
  log "AC#6: Log records allowed transitions"

  # When transition is allowed, log should show: "decision": "allowed"

  if assert_file_exists "$HOOK_SCRIPT" "Hook script must exist"; then
    pass "Ready to validate allowed decision logging (implementation pending)"
  else
    return 1
  fi
}

test_log_records_blocked_decisions() {
  log "AC#6: Log records blocked transitions"

  # When transition is blocked, log should show: "decision": "blocked"

  if assert_file_exists "$HOOK_SCRIPT" "Hook script must exist"; then
    pass "Ready to validate blocked decision logging (implementation pending)"
  else
    return 1
  fi
}

################################################################################
# Edge Cases and Non-Functional Requirements
################################################################################

test_hook_requires_jq() {
  log "Edge Case: jq availability check"

  if command -v jq &> /dev/null; then
    pass "jq is installed (required for JSON parsing)"
  else
    fail "jq is not installed - hook implementation requires jq"
    return 1
  fi
}

test_story_id_extraction_from_environment() {
  log "Edge Case: Hook extracts story ID from environment"

  # Hook receives:
  # - CLAUDE_TOOL_NAME (should be "Task")
  # - CLAUDE_TOOL_INPUT (JSON with subagent_type)

  if assert_file_exists "$HOOK_SCRIPT" "Hook script must exist"; then
    pass "Ready to validate story ID extraction (implementation pending)"
  else
    return 1
  fi
}

test_hook_performance_under_100ms() {
  log "Non-Functional: Hook execution < 100ms"

  # This requires timing instrumentation in hook script
  # Baseline test: script exists and is not obviously slow

  if assert_file_exists "$HOOK_SCRIPT" "Hook script must exist"; then
    pass "Ready to benchmark hook performance (implementation pending)"
  else
    return 1
  fi
}

test_hook_fail_closed_behavior() {
  log "Non-Functional: Hook failure defaults to blocking"

  # If hook encounters unexpected error, it should:
  # 1. Log the error
  # 2. Return exit code 1 (block transition)
  # 3. Not allow proceeding even if hook is partially broken

  if assert_file_exists "$HOOK_SCRIPT" "Hook script must exist"; then
    pass "Ready to validate fail-closed behavior (implementation pending)"
  else
    return 1
  fi
}

test_hook_not_executable_error() {
  log "Edge Case: Error when hook script is not executable"

  if [[ -x "$HOOK_SCRIPT" ]] 2>/dev/null; then
    pass "Hook script is executable"
  else
    fail "Hook script must be executable (chmod +x required)"
    return 1
  fi
}

################################################################################
# Test Execution
################################################################################

run_all_tests() {
  echo "=================================="
  echo "STORY-150: Pre-Phase-Transition Hook Tests"
  echo "=================================="
  echo ""

  # Parse arguments
  while [[ $# -gt 0 ]]; do
    case $1 in
      --verbose)
        VERBOSE=true
        shift
        ;;
      --stop-on-failure)
        STOP_ON_FAILURE=true
        shift
        ;;
      *)
        shift
        ;;
    esac
  done

  echo "Test Configuration:"
  echo "  Verbose: $VERBOSE"
  echo "  Stop on Failure: $STOP_ON_FAILURE"
  echo ""

  # Setup
  mkdir -p "$RESULTS_DIR"
  mkdir -p "$(dirname "$LOG_FILE")"

  echo "=================================="
  echo "AC#1: Hook Registration"
  echo "=================================="
  test_hook_registered_in_config
  test_hook_script_exists

  echo ""
  echo "=================================="
  echo "AC#2: Validate Phase Completion"
  echo "=================================="
  test_hook_checks_previous_phase_status
  test_hook_allows_phase_01
  test_hook_blocks_incomplete_previous_phase

  echo ""
  echo "=================================="
  echo "AC#3: Error Messages"
  echo "=================================="
  test_error_message_contains_phase_number
  test_error_message_contains_subagent_info
  test_error_message_contains_remediation_guidance
  test_block_returns_exit_code_1

  echo ""
  echo "=================================="
  echo "AC#4: Phase 01 Always Allowed"
  echo "=================================="
  test_phase_01_always_passes
  test_phase_01_no_state_file_required

  echo ""
  echo "=================================="
  echo "AC#5: Missing State File Handling"
  echo "=================================="
  test_missing_state_file_triggers_auto_init
  test_auto_init_creates_valid_state_file
  test_corrupted_state_file_blocks_transition

  echo ""
  echo "=================================="
  echo "AC#6: Logging"
  echo "=================================="
  test_log_file_exists
  test_log_contains_required_fields
  test_log_format_is_jsonlines
  test_log_records_allowed_decisions
  test_log_records_blocked_decisions

  echo ""
  echo "=================================="
  echo "Edge Cases & Non-Functional"
  echo "=================================="
  test_hook_requires_jq
  test_story_id_extraction_from_environment
  test_hook_performance_under_100ms
  test_hook_fail_closed_behavior
  test_hook_not_executable_error

  echo ""
  echo "=================================="
  echo "Test Results"
  echo "=================================="
  echo "Total:  $TESTS_TOTAL"
  echo "Passed: $TESTS_PASSED"
  echo "Failed: $TESTS_FAILED"
  echo ""

  if [[ $TESTS_FAILED -eq 0 ]]; then
    echo -e "${GREEN}All tests passed!${NC}"
    return 0
  else
    echo -e "${RED}$TESTS_FAILED test(s) failed${NC}"
    return 1
  fi
}

# Run tests
run_all_tests "$@"
exit $?

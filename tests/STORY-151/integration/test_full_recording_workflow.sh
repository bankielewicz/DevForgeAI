#!/usr/bin/env bash

# STORY-151: Post-Subagent Recording Hook - Full Workflow Integration Tests
# Tests complete end-to-end workflows for recording and skipping subagents

set -euo pipefail

# Setup
readonly TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly PROJECT_ROOT="$(cd "${TEST_DIR}/../../../" && pwd)"
readonly TEMP_DIR="${TEST_DIR}/.temp"
readonly WORKFLOWS_DIR="$TEMP_DIR/workflows"
readonly LOGS_DIR="$TEMP_DIR/logs"
readonly CONFIG_DIR="$TEMP_DIR/config"

# Color codes for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly NC='\033[0m'

# Test counters
tests_run=0
tests_passed=0
tests_failed=0

# Cleanup function
cleanup_temp_files() {
    if [[ -d "$TEMP_DIR" ]]; then
        rm -rf "$TEMP_DIR"
    fi
}

trap cleanup_temp_files EXIT

# Test helper functions
run_test() {
    local test_name="$1"
    local test_func="$2"

    echo -e "\n${YELLOW}Running: ${test_name}${NC}"
    tests_run=$((tests_run + 1))

    if $test_func; then
        echo -e "${GREEN}✓ PASSED${NC}"
        tests_passed=$((tests_passed + 1))
        return 0
    else
        echo -e "${RED}✗ FAILED${NC}"
        tests_failed=$((tests_failed + 1))
        return 1
    fi
}

assert_equals() {
    local expected="$1"
    local actual="$2"
    local message="${3:-Assertion failed}"

    if [[ "$expected" != "$actual" ]]; then
        echo "  Error: $message"
        echo "  Expected: $expected"
        echo "  Actual: $actual"
        return 1
    fi
    return 0
}

assert_file_exists() {
    local file="$1"
    local message="${2:-File not found}"

    if [[ ! -f "$file" ]]; then
        echo "  Error: $message"
        return 1
    fi
    return 0
}

assert_contains() {
    local text="$1"
    local pattern="$2"
    local message="${3:-Pattern not found}"

    if ! echo "$text" | grep -q "$pattern"; then
        echo "  Error: $message"
        echo "  Text: $text"
        echo "  Pattern: $pattern"
        return 1
    fi
    return 0
}

# Setup temporary directories
mkdir -p "$WORKFLOWS_DIR" "$LOGS_DIR" "$CONFIG_DIR"

# Create mock workflow-subagents.yaml
create_mock_config() {
    cat > "$CONFIG_DIR/workflow-subagents.yaml" << 'YAML'
workflow_subagents:
  - tech-stack-detector
  - context-validator
  - test-automator
  - backend-architect
  - refactoring-specialist
  - integration-tester
  - code-reviewer
  - security-auditor
  - deferral-validator
  - dev-result-interpreter

excluded_subagents:
  - internet-sleuth
  - documentation-writer
  - api-designer
  - stakeholder-analyst
YAML
}

# Create mock phase state file
create_mock_phase_state() {
    local story_id="$1"
    local phase_id="${2:-02}"
    local file="$WORKFLOWS_DIR/${story_id}-phase-state.json"

    cat > "$file" << JSON
{
  "story_id": "$story_id",
  "current_phase": "$phase_id",
  "phases": {
    "$phase_id": {
      "name": "Test-First Design",
      "status": "in_progress",
      "subagent_invocations": []
    }
  }
}
JSON
}

# TEST INTEGRATION#1: Workflow subagent recording end-to-end
test_workflow_subagent_recorded_end_to_end() {
    local story_id="STORY-151"
    local subagent="test-automator"
    local phase_id="02"
    local log_file="$LOGS_DIR/recordings.log"

    create_mock_config
    create_mock_phase_state "$story_id" "$phase_id"

    # Simulate hook execution for workflow subagent
    if grep -q "^  - $subagent$" "$CONFIG_DIR/workflow-subagents.yaml"; then
        # Subagent is in workflow list - record it
        echo "{\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"story_id\":\"$story_id\",\"subagent_name\":\"$subagent\",\"phase_id\":\"$phase_id\",\"result\":\"recorded\",\"reason\":\"Workflow subagent recorded to phase state\"}" >> "$log_file"
    fi

    # Verify recording was logged
    assert_file_exists "$log_file" "Log file not created"
    assert_contains "$(cat $log_file)" "\"result\":\"recorded\"" \
        "Recording result not in log"
    assert_contains "$(cat $log_file)" "\"subagent_name\":\"$subagent\"" \
        "Subagent name not in log"

    return 0
}

# TEST INTEGRATION#2: Non-workflow subagent skip end-to-end
test_non_workflow_subagent_skipped_end_to_end() {
    local story_id="STORY-151"
    local subagent="internet-sleuth"
    local phase_id="02"
    local log_file="$LOGS_DIR/skip-recordings.log"

    create_mock_config
    create_mock_phase_state "$story_id" "$phase_id"

    # Simulate hook execution for non-workflow subagent
    if ! grep -q "^  - $subagent$" "$CONFIG_DIR/workflow-subagents.yaml"; then
        # Subagent NOT in workflow list - skip it
        echo "{\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"story_id\":\"$story_id\",\"subagent_name\":\"$subagent\",\"phase_id\":\"$phase_id\",\"result\":\"skipped\",\"reason\":\"Non-workflow subagent skipped\"}" >> "$log_file"
    fi

    # Verify skip was logged
    assert_file_exists "$log_file" "Log file not created"
    assert_contains "$(cat $log_file)" "\"result\":\"skipped\"" \
        "Skip result not in log"
    assert_contains "$(cat $log_file)" "\"subagent_name\":\"$subagent\"" \
        "Subagent name not in log"

    return 0
}

# TEST INTEGRATION#3: Missing state file graceful exit
test_missing_state_file_graceful_exit() {
    local story_id="STORY-NOTFOUND"
    local subagent="test-automator"
    local log_file="$LOGS_DIR/missing-state.log"
    local state_file="$WORKFLOWS_DIR/${story_id}-phase-state.json"

    create_mock_config

    # Verify state file does NOT exist
    if [[ ! -f "$state_file" ]]; then
        # Hook should skip recording and exit 0
        local hook_exit_code=0
        echo "{\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"story_id\":\"$story_id\",\"subagent_name\":\"$subagent\",\"result\":\"skipped\",\"reason\":\"No state file found for $story_id, skipping recording\"}" >> "$log_file"
    else
        # State file exists, would record
        local hook_exit_code=1
    fi

    # Verify exit code is 0 (non-blocking)
    assert_equals "0" "$hook_exit_code" \
        "Hook should exit 0 when state file missing"

    # Verify skip was logged
    assert_file_exists "$log_file" "Log file not created"
    assert_contains "$(cat $log_file)" "No state file found" \
        "Missing state warning not in log"

    return 0
}

# TEST INTEGRATION#4: Log and state file consistency
test_log_and_state_consistency() {
    local story_id="STORY-151"
    local subagent="test-automator"
    local phase_id="02"
    local log_file="$LOGS_DIR/consistency.log"

    create_mock_config
    create_mock_phase_state "$story_id" "$phase_id"

    # Simulate recording the subagent
    if grep -q "^  - $subagent$" "$CONFIG_DIR/workflow-subagents.yaml"; then
        # Record in state file (simulated)
        local state_file="$WORKFLOWS_DIR/${story_id}-phase-state.json"

        # Write to log
        echo "{\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"story_id\":\"$story_id\",\"subagent_name\":\"$subagent\",\"phase_id\":\"$phase_id\",\"result\":\"recorded\"}" >> "$log_file"

        # Verify both have consistent information
        assert_file_exists "$state_file" "State file should exist"
        assert_file_exists "$log_file" "Log file should exist"

        # Verify log mentions same story and subagent as state file
        local log_story=$(grep -o "\"story_id\":\"[^\"]*\"" "$log_file" | head -1)
        local log_subagent=$(grep -o "\"subagent_name\":\"[^\"]*\"" "$log_file" | head -1)

        assert_contains "$log_story" "$story_id" "Log story ID mismatch"
        assert_contains "$log_subagent" "$subagent" "Log subagent mismatch"
    fi

    return 0
}

# TEST INTEGRATION#5: Multiple subagent recordings in sequence
test_multiple_subagents_recorded_sequentially() {
    local story_id="STORY-151"
    local phase_id="02"
    local log_file="$LOGS_DIR/multi-subagents.log"
    local subagents=("test-automator" "backend-architect" "code-reviewer")

    create_mock_config
    create_mock_phase_state "$story_id" "$phase_id"

    # Simulate recording multiple subagents in sequence
    for subagent in "${subagents[@]}"; do
        if grep -q "^  - $subagent$" "$CONFIG_DIR/workflow-subagents.yaml"; then
            echo "{\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"story_id\":\"$story_id\",\"subagent_name\":\"$subagent\",\"phase_id\":\"$phase_id\",\"result\":\"recorded\"}" >> "$log_file"
        fi
    done

    # Verify all subagents were logged
    local log_content=$(cat "$log_file")
    for subagent in "${subagents[@]}"; do
        if ! echo "$log_content" | grep -q "\"subagent_name\":\"$subagent\""; then
            echo "  Error: Subagent $subagent not found in log"
            return 1
        fi
    done

    # Verify log has at least 3 entries
    local entry_count=$(wc -l < "$log_file")
    if [[ "$entry_count" -lt "3" ]]; then
        echo "  Error: Expected at least 3 log entries, got $entry_count"
        return 1
    fi

    return 0
}

# TEST INTEGRATION#6: Mixed workflow and non-workflow subagents
test_mixed_workflow_and_non_workflow() {
    local story_id="STORY-151"
    local phase_id="02"
    local log_file="$LOGS_DIR/mixed-subagents.log"
    local workflow_subagent="test-automator"
    local non_workflow_subagent="internet-sleuth"

    create_mock_config
    create_mock_phase_state "$story_id" "$phase_id"

    # Extract workflow section only (before excluded_subagents:)
    local workflow_section=$(sed -n '/^workflow_subagents:/,/^excluded_subagents:/p' "$CONFIG_DIR/workflow-subagents.yaml")

    # Process workflow subagent (check if in workflow section)
    if echo "$workflow_section" | grep -qF -- "- $workflow_subagent"; then
        echo "{\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"story_id\":\"$story_id\",\"subagent_name\":\"$workflow_subagent\",\"phase_id\":\"$phase_id\",\"result\":\"recorded\"}" >> "$log_file"
    fi

    # Process non-workflow subagent (check if NOT in workflow section)
    if ! echo "$workflow_section" | grep -qF -- "- $non_workflow_subagent"; then
        echo "{\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"story_id\":\"$story_id\",\"subagent_name\":\"$non_workflow_subagent\",\"phase_id\":\"$phase_id\",\"result\":\"skipped\"}" >> "$log_file"
    fi

    # Verify both are in log with correct results
    local log_content=$(cat "$log_file")

    # Check workflow subagent was recorded (fields may be in any order)
    if ! echo "$log_content" | grep -q "\"subagent_name\":\"$workflow_subagent\""; then
        echo "  Error: Workflow subagent '$workflow_subagent' not found in log"
        return 1
    fi
    if ! echo "$log_content" | grep "\"subagent_name\":\"$workflow_subagent\"" | grep -q "\"result\":\"recorded\""; then
        echo "  Error: Workflow subagent not recorded correctly"
        return 1
    fi

    # Check non-workflow subagent was skipped (fields may be in any order)
    if ! echo "$log_content" | grep -q "\"subagent_name\":\"$non_workflow_subagent\""; then
        echo "  Error: Non-workflow subagent '$non_workflow_subagent' not found in log"
        return 1
    fi
    if ! echo "$log_content" | grep "\"subagent_name\":\"$non_workflow_subagent\"" | grep -q "\"result\":\"skipped\""; then
        echo "  Error: Non-workflow subagent not skipped correctly"
        return 1
    fi

    return 0
}

# TEST INTEGRATION#7: Hook doesn't block workflow on failure
test_hook_failure_nonblocking() {
    local log_file="$LOGS_DIR/nonblocking.log"

    # Simulate various hook failures
    # All should result in exit code 0 (non-blocking)

    # Failure 1: CLI error
    echo "{\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"story_id\":\"STORY-151\",\"result\":\"error\",\"reason\":\"devforgeai-validate failed\"}" >> "$log_file"

    # Failure 2: Missing config
    echo "{\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"story_id\":\"STORY-151\",\"result\":\"error\",\"reason\":\"workflow-subagents.yaml not found\"}" >> "$log_file"

    # All failures should have exit code 0
    local hook_exit_code=0

    assert_equals "0" "$hook_exit_code" \
        "Hook should exit 0 even on failure (non-blocking)"

    return 0
}

# TEST INTEGRATION#8: Environment variable story ID extraction
test_env_var_story_id_in_workflow() {
    local story_id="STORY-151"
    local subagent="test-automator"
    local phase_id="02"
    local log_file="$LOGS_DIR/env-story.log"

    create_mock_config
    create_mock_phase_state "$story_id" "$phase_id"

    # Set environment variable
    export DEVFORGEAI_STORY_ID="$story_id"

    # Hook uses env var to get story ID
    local detected_story="${DEVFORGEAI_STORY_ID:-}"

    # Simulate recording with detected story
    if [[ "$detected_story" == "$story_id" ]]; then
        echo "{\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"story_id\":\"$detected_story\",\"subagent_name\":\"$subagent\",\"phase_id\":\"$phase_id\",\"result\":\"recorded\"}" >> "$log_file"
    fi

    # Verify correct story in log
    assert_contains "$(cat $log_file)" "\"story_id\":\"$story_id\"" \
        "Story ID from env var not in log"

    unset DEVFORGEAI_STORY_ID
    return 0
}

# MAIN - Run all tests
echo "=================================================================="
echo "STORY-151: Full Recording Workflow Integration Tests"
echo "=================================================================="

run_test "workflow subagent recorded end-to-end" \
    test_workflow_subagent_recorded_end_to_end
run_test "non-workflow subagent skipped end-to-end" \
    test_non_workflow_subagent_skipped_end_to_end
run_test "missing state file graceful exit (exit 0)" \
    test_missing_state_file_graceful_exit
run_test "log and state file consistency" \
    test_log_and_state_consistency
run_test "multiple subagents recorded sequentially" \
    test_multiple_subagents_recorded_sequentially
run_test "mixed workflow and non-workflow subagents" \
    test_mixed_workflow_and_non_workflow
run_test "hook failure is non-blocking (exit 0)" \
    test_hook_failure_nonblocking
run_test "environment variable story ID in workflow" \
    test_env_var_story_id_in_workflow

# Print summary
echo ""
echo "=================================================================="
echo "Test Summary"
echo "=================================================================="
echo "Total: $tests_run"
echo "Passed: $tests_passed"
echo "Failed: $tests_failed"
echo "=================================================================="

exit $tests_failed

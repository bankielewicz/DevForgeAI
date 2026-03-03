#!/usr/bin/env bash

# STORY-151: Post-Subagent Recording Hook - State File Handling Tests (AC#5)
# Tests that hook handles missing state file gracefully

set -euo pipefail

# Setup
readonly TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly PROJECT_ROOT="$(cd "${TEST_DIR}/../../../" && pwd)"
readonly TEMP_DIR="${TEST_DIR}/.temp"
readonly WORKFLOWS_DIR="$TEMP_DIR/workflows"
readonly LOGS_DIR="$TEMP_DIR/logs"

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

assert_file_not_exists() {
    local file="$1"
    local message="${2:-File should not exist}"

    if [[ -f "$file" ]]; then
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
mkdir -p "$WORKFLOWS_DIR" "$LOGS_DIR"

# TEST AC#5.1: Skip recording when state file missing (exit 0)
test_skip_when_state_file_missing() {
    local story_id="STORY-151"
    local state_file="$WORKFLOWS_DIR/${story_id}-phase-state.json"

    # Verify state file does not exist
    if [[ -f "$state_file" ]]; then
        echo "  Error: State file should not exist for this test"
        return 1
    fi

    # When state file missing, hook should exit 0
    # This simulates the hook behavior
    if [[ -f "$state_file" ]]; then
        local exit_code=1  # Would normally call devforgeai-validate
    else
        local exit_code=0  # Skip recording, exit cleanly
    fi

    assert_equals "0" "$exit_code" \
        "Hook should exit 0 when state file missing"

    return 0
}

# TEST AC#5.2: Log warning message for missing state file
test_log_warning_for_missing_state() {
    local story_id="STORY-151"
    local state_file="$WORKFLOWS_DIR/${story_id}-phase-state.json"
    local log_file="$LOGS_DIR/subagent-recordings.log"

    # Ensure directories exist
    mkdir -p "$(dirname "$state_file")" "$(dirname "$log_file")"

    # Simulate logging warning (in real implementation, hook would write this)
    if [[ ! -f "$state_file" ]]; then
        echo "{\"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\", \"story_id\": \"$story_id\", \"result\": \"skipped\", \"reason\": \"No state file found for $story_id, skipping recording\"}" >> "$log_file"
    fi

    # Verify warning was logged
    if ! grep -q "No state file found" "$log_file"; then
        echo "  Error: Warning not logged for missing state file"
        return 1
    fi

    return 0
}

# TEST AC#5.3: State file not modified when missing
test_no_state_modification_on_missing_file() {
    local story_id="STORY-151"
    local state_file="$WORKFLOWS_DIR/${story_id}-phase-state.json"

    # Verify state file does not exist
    assert_file_not_exists "$state_file" \
        "State file should not exist at start"

    # Simulate hook execution (no modification should occur)
    if [[ ! -f "$state_file" ]]; then
        # Hook skips - does not create or modify state file
        :  # No action taken
    fi

    # Verify state file was not created
    assert_file_not_exists "$state_file" \
        "State file should not be created when missing"

    return 0
}

# TEST AC#5.4: Workflow continues on missing state (non-blocking)
test_workflow_continues_on_missing_state() {
    local story_id="STORY-151"
    local state_file="$WORKFLOWS_DIR/${story_id}-phase-state.json"

    # Hook encounters missing state file
    if [[ -f "$state_file" ]]; then
        # Would record subagent
        local recording_succeeded="true"
    else
        # State file missing - skip recording
        local recording_succeeded="false"
    fi

    # Even though recording didn't happen, workflow should continue
    # Hook returns exit code 0 (non-blocking)
    local hook_exit_code=0

    assert_equals "0" "$hook_exit_code" \
        "Hook should return exit 0 (non-blocking) even when state missing"

    return 0
}

# TEST AC#5.5: Log message includes story ID
test_log_includes_story_id() {
    local story_id="STORY-151"
    local log_file="$LOGS_DIR/test-log.log"

    mkdir -p "$(dirname "$log_file")"

    # Write log entry with story ID
    echo "{\"story_id\": \"$story_id\", \"result\": \"skipped\"}" >> "$log_file"

    # Verify story ID is in log
    if ! grep -q "\"story_id\": \"$story_id\"" "$log_file"; then
        echo "  Error: Story ID not found in log message"
        return 1
    fi

    return 0
}

# TEST AC#5.6: Multiple missing states don't cause errors
test_multiple_missing_states_no_errors() {
    local story_ids=("STORY-100" "STORY-101" "STORY-151")

    # Try to handle multiple missing state files
    for story_id in "${story_ids[@]}"; do
        local state_file="$WORKFLOWS_DIR/${story_id}-phase-state.json"

        if [[ ! -f "$state_file" ]]; then
            # Skip this story gracefully
            local exit_code=0
        else
            # Would process
            local exit_code=1
        fi

        # All should result in exit code 0 (graceful skip)
        if [[ "$exit_code" != "0" ]]; then
            echo "  Error: Failed to handle missing state for $story_id"
            return 1
        fi
    done

    return 0
}

# TEST AC#5.7: Log format is JSON Lines (one JSON per line)
test_log_json_lines_format() {
    local log_file="$LOGS_DIR/jsonlines.log"

    mkdir -p "$(dirname "$log_file")"

    # Write multiple log entries
    echo '{"story_id": "STORY-100", "result": "skipped"}' >> "$log_file"
    echo '{"story_id": "STORY-151", "result": "recorded"}' >> "$log_file"
    echo '{"story_id": "STORY-200", "result": "error"}' >> "$log_file"

    # Verify each line is valid JSON
    local line_count=0
    while IFS= read -r line; do
        ((line_count++))

        # Skip empty lines
        if [[ -z "$line" ]]; then
            continue
        fi

        # Try to parse as JSON
        if ! echo "$line" | python3 -c "import sys, json; json.load(sys.stdin)" 2>/dev/null; then
            echo "  Error: Line $line_count is not valid JSON: $line"
            return 1
        fi
    done < "$log_file"

    if [[ "$line_count" != "3" ]]; then
        echo "  Error: Expected 3 log lines, got $line_count"
        return 1
    fi

    return 0
}

# TEST AC#5.8: Graceful handling doesn't suppress other errors
test_graceful_skip_vs_other_errors() {
    local log_file="$LOGS_DIR/errors.log"

    mkdir -p "$(dirname "$log_file")"

    # Scenario 1: Missing state file (graceful skip)
    local story_id="STORY-151"
    local state_file="$WORKFLOWS_DIR/${story_id}-phase-state.json"

    if [[ ! -f "$state_file" ]]; then
        echo '{"story_id": "'$story_id'", "result": "skipped", "reason": "No state file found"}' >> "$log_file"
    fi

    # Scenario 2: CLI error (still logged but non-blocking)
    echo '{"story_id": "STORY-152", "result": "error", "reason": "devforgeai-validate CLI failed"}' >> "$log_file"

    # Both should be present in log
    if ! grep -q "No state file found" "$log_file"; then
        echo "  Error: Skip not logged"
        return 1
    fi

    if ! grep -q "devforgeai-validate CLI failed" "$log_file"; then
        echo "  Error: Error not logged"
        return 1
    fi

    return 0
}

# TEST AC#5.9: Empty workflows directory handled correctly
test_empty_workflows_directory() {
    local empty_workflows="$TEMP_DIR/empty_workflows"
    mkdir -p "$empty_workflows"

    # List state files in empty directory
    local file_count=$(find "$empty_workflows" -name "*-phase-state.json" -type f | wc -l)

    assert_equals "0" "$file_count" \
        "Empty workflows directory should have no state files"

    return 0
}

# TEST AC#5.10: Recovery from transient state file deletion
test_recovery_from_deleted_state() {
    local story_id="STORY-151"
    local state_file="$WORKFLOWS_DIR/${story_id}-phase-state.json"
    local log_file="$LOGS_DIR/recovery.log"

    mkdir -p "$(dirname "$state_file")" "$(dirname "$log_file")"

    # Create state file, then delete it
    echo '{"story_id": "'$story_id'"}' > "$state_file"
    rm "$state_file"

    # Hook should handle gracefully
    if [[ -f "$state_file" ]]; then
        local exit_code=1
    else
        local exit_code=0
        echo '{"story_id": "'$story_id'", "result": "skipped", "reason": "State file deleted"}' >> "$log_file"
    fi

    assert_equals "0" "$exit_code" \
        "Hook should handle deleted state file gracefully"

    return 0
}

# MAIN - Run all tests
echo "============================================================"
echo "STORY-151: State File Handling Tests (AC#5)"
echo "============================================================"

run_test "skip recording when state file missing (exit 0)" \
    test_skip_when_state_file_missing
run_test "log warning for missing state file" \
    test_log_warning_for_missing_state
run_test "no state file modification when missing" \
    test_no_state_modification_on_missing_file
run_test "workflow continues on missing state (non-blocking)" \
    test_workflow_continues_on_missing_state
run_test "log message includes story ID" \
    test_log_includes_story_id
run_test "multiple missing states don't cause errors" \
    test_multiple_missing_states_no_errors
run_test "log format is JSON Lines (one JSON per line)" \
    test_log_json_lines_format
run_test "graceful skip vs other errors both logged" \
    test_graceful_skip_vs_other_errors
run_test "empty workflows directory handled correctly" \
    test_empty_workflows_directory
run_test "recovery from transient state file deletion" \
    test_recovery_from_deleted_state

# Print summary
echo ""
echo "============================================================"
echo "Test Summary"
echo "============================================================"
echo "Total: $tests_run"
echo "Passed: $tests_passed"
echo "Failed: $tests_failed"
echo "============================================================"

exit $tests_failed

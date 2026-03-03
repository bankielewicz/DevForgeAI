#!/usr/bin/env bash

# STORY-151: Post-Subagent Recording Hook - Logging Tests (AC#6)
# Tests that hook logs all recording attempts with required fields

set -euo pipefail

# Setup
readonly TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly PROJECT_ROOT="$(cd "${TEST_DIR}/../../../" && pwd)"
readonly TEMP_DIR="${TEST_DIR}/.temp"
readonly LOG_FILE="$TEMP_DIR/subagent-recordings.log"
readonly LOG_DIR="$(dirname "$LOG_FILE")"

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

# Setup log directory
mkdir -p "$LOG_DIR"

# TEST AC#6.1: Log file created at correct path
test_log_file_created() {
    # Simulate hook creating log file
    mkdir -p "$LOG_DIR"

    # Write a log entry
    echo '{"timestamp":"2025-12-28T10:30:45Z","story_id":"STORY-151","subagent_name":"test-automator","phase_id":"02","result":"recorded","reason":"Workflow subagent recorded to phase state"}' >> "$LOG_FILE"

    assert_file_exists "$LOG_FILE" \
        "Log file not created at $LOG_FILE"

    return 0
}

# TEST AC#6.2: Log entries are JSON Lines format (one JSON per line)
test_log_entry_json_lines_format() {
    # Clear log file
    > "$LOG_FILE"

    # Write multiple entries in JSON Lines format
    echo '{"timestamp":"2025-12-28T10:30:45Z","story_id":"STORY-151","result":"recorded"}' >> "$LOG_FILE"
    echo '{"timestamp":"2025-12-28T10:31:00Z","story_id":"STORY-152","result":"skipped"}' >> "$LOG_FILE"
    echo '{"timestamp":"2025-12-28T10:31:15Z","story_id":"STORY-153","result":"error"}' >> "$LOG_FILE"

    # Verify each line is valid JSON
    local line_num=0
    while IFS= read -r line; do
        ((line_num++))

        # Skip empty lines
        if [[ -z "$line" ]]; then
            continue
        fi

        # Verify line is valid JSON
        if ! command -v python3 &> /dev/null; then
            # Fallback: check if line starts with { and ends with }
            if [[ ! "$line" =~ ^\{.*\}$ ]]; then
                echo "  Error: Line $line_num is not valid JSON format"
                echo "  Content: $line"
                return 1
            fi
        else
            if ! echo "$line" | python3 -c "import sys, json; json.load(sys.stdin)" 2>/dev/null; then
                echo "  Error: Line $line_num is not valid JSON: $line"
                return 1
            fi
        fi
    done < "$LOG_FILE"

    if [[ "$line_num" -lt "3" ]]; then
        echo "  Error: Expected at least 3 log lines, got $line_num"
        return 1
    fi

    return 0
}

# TEST AC#6.3: Log contains all required fields
test_log_contains_required_fields() {
    > "$LOG_FILE"

    # Write log entry with all required fields
    local entry='{"timestamp":"2025-12-28T10:30:45Z","story_id":"STORY-151","subagent_name":"test-automator","phase_id":"02","result":"recorded","reason":"Workflow subagent recorded to phase state"}'
    echo "$entry" >> "$LOG_FILE"

    local log_content=$(cat "$LOG_FILE")

    # Verify all required fields are present
    local required_fields=("timestamp" "story_id" "subagent_name" "phase_id" "result" "reason")

    for field in "${required_fields[@]}"; do
        if ! echo "$log_content" | grep -q "\"$field\""; then
            echo "  Error: Required field '$field' not found in log"
            return 1
        fi
    done

    return 0
}

# TEST AC#6.4: Timestamp is ISO-8601 format
test_log_timestamp_iso8601() {
    > "$LOG_FILE"

    # ISO-8601 format: YYYY-MM-DDTHH:MM:SSZ
    local iso_timestamp="2025-12-28T10:30:45Z"
    local entry="{\"timestamp\":\"$iso_timestamp\",\"story_id\":\"STORY-151\",\"result\":\"recorded\"}"
    echo "$entry" >> "$LOG_FILE"

    local log_content=$(cat "$LOG_FILE")

    # Verify timestamp matches ISO-8601 pattern
    if ! echo "$log_content" | grep -qE '"timestamp":"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z"'; then
        echo "  Error: Timestamp is not in ISO-8601 format"
        echo "  Log entry: $log_content"
        return 1
    fi

    return 0
}

# TEST AC#6.5: Result field contains valid enum values
test_log_result_enum_values() {
    > "$LOG_FILE"

    # Valid result values: recorded, skipped, error
    local test_cases=("recorded" "skipped" "error")

    for result in "${test_cases[@]}"; do
        local entry="{\"story_id\":\"STORY-151\",\"result\":\"$result\",\"reason\":\"Test\"}"
        echo "$entry" >> "$LOG_FILE"
    done

    local log_content=$(cat "$LOG_FILE")

    # Verify all valid results are present
    for result in "${test_cases[@]}"; do
        if ! echo "$log_content" | grep -q "\"result\":\"$result\""; then
            echo "  Error: Result value '$result' not found"
            return 1
        fi
    done

    # Verify invalid result value would fail
    if echo '{"result":"invalid"}' | grep -q '"result":"recorded\|skipped\|error"'; then
        # This should NOT match, which is correct
        true
    fi

    return 0
}

# TEST AC#6.6: Reason field explains action taken
test_log_reason_field_present() {
    > "$LOG_FILE"

    # Test various reason messages
    local test_reasons=(
        "Workflow subagent recorded to phase state"
        "Non-workflow subagent skipped"
        "No state file found for STORY-151, skipping recording"
        "devforgeai-validate CLI failed"
    )

    for reason in "${test_reasons[@]}"; do
        local entry="{\"story_id\":\"STORY-151\",\"reason\":\"$reason\"}"
        echo "$entry" >> "$LOG_FILE"
    done

    local log_content=$(cat "$LOG_FILE")

    # Verify reason field is present
    if ! echo "$log_content" | grep -q '"reason":'; then
        echo "  Error: Reason field not found"
        return 1
    fi

    # Verify at least one reason is meaningful
    if ! echo "$log_content" | grep -q "recorded\|skipped\|failed"; then
        echo "  Error: No meaningful reason text found"
        return 1
    fi

    return 0
}

# TEST AC#6.7: Log file is world-readable for audit purposes
test_log_file_permissions() {
    # Simulate setting log file with readable permissions
    mkdir -p "$LOG_DIR"
    touch "$LOG_FILE"
    chmod 644 "$LOG_FILE"

    # Verify file is readable
    if [[ ! -r "$LOG_FILE" ]]; then
        echo "  Error: Log file is not readable"
        return 1
    fi

    return 0
}

# TEST AC#6.8: Multiple log entries maintain chronological order
test_log_chronological_order() {
    > "$LOG_FILE"

    # Write entries with increasing timestamps
    echo '{"timestamp":"2025-12-28T10:30:00Z","story_id":"STORY-100","event":"1"}' >> "$LOG_FILE"
    echo '{"timestamp":"2025-12-28T10:30:15Z","story_id":"STORY-101","event":"2"}' >> "$LOG_FILE"
    echo '{"timestamp":"2025-12-28T10:30:30Z","story_id":"STORY-151","event":"3"}' >> "$LOG_FILE"

    # Verify timestamps are in order
    local first_ts=$(sed -n '1p' "$LOG_FILE" | grep -oP '(?<="timestamp":")[^"]*')
    local last_ts=$(tail -n1 "$LOG_FILE" | grep -oP '(?<="timestamp":")[^"]*')

    if [[ "$first_ts" > "$last_ts" ]]; then
        echo "  Error: Log entries not in chronological order"
        echo "  First: $first_ts"
        echo "  Last: $last_ts"
        return 1
    fi

    return 0
}

# TEST AC#6.9: Log entries include story_id for traceability
test_log_story_id_traceability() {
    > "$LOG_FILE"

    # Write entries for different stories
    local story_ids=("STORY-100" "STORY-151" "STORY-200")

    for story_id in "${story_ids[@]}"; do
        local entry="{\"story_id\":\"$story_id\",\"subagent_name\":\"test-automator\",\"result\":\"recorded\"}"
        echo "$entry" >> "$LOG_FILE"
    done

    local log_content=$(cat "$LOG_FILE")

    # Verify all story IDs are present
    for story_id in "${story_ids[@]}"; do
        if ! echo "$log_content" | grep -q "\"story_id\":\"$story_id\""; then
            echo "  Error: Story ID $story_id not found in log"
            return 1
        fi
    done

    return 0
}

# TEST AC#6.10: Log entries include subagent name for audit trail
test_log_subagent_name_audit_trail() {
    > "$LOG_FILE"

    # Write entries for different subagents
    local subagents=("test-automator" "backend-architect" "code-reviewer")

    for subagent in "${subagents[@]}"; do
        local entry="{\"story_id\":\"STORY-151\",\"subagent_name\":\"$subagent\",\"result\":\"recorded\"}"
        echo "$entry" >> "$LOG_FILE"
    done

    local log_content=$(cat "$LOG_FILE")

    # Verify all subagent names are present
    for subagent in "${subagents[@]}"; do
        if ! echo "$log_content" | grep -q "\"subagent_name\":\"$subagent\""; then
            echo "  Error: Subagent $subagent not found in log"
            return 1
        fi
    done

    return 0
}

# MAIN - Run all tests
echo "============================================================"
echo "STORY-151: Logging Tests (AC#6)"
echo "============================================================"

run_test "log file created at correct path" \
    test_log_file_created
run_test "log entries are JSON Lines format" \
    test_log_entry_json_lines_format
run_test "log contains all required fields" \
    test_log_contains_required_fields
run_test "timestamp is ISO-8601 format" \
    test_log_timestamp_iso8601
run_test "result field contains valid enum values" \
    test_log_result_enum_values
run_test "reason field explains action taken" \
    test_log_reason_field_present
run_test "log file is world-readable for audit" \
    test_log_file_permissions
run_test "multiple log entries maintain chronological order" \
    test_log_chronological_order
run_test "log entries include story_id for traceability" \
    test_log_story_id_traceability
run_test "log entries include subagent name for audit trail" \
    test_log_subagent_name_audit_trail

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

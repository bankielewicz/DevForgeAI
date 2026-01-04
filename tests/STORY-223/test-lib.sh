#!/bin/bash
#
# Shared Test Library for STORY-223 Tests
# Centralizes common assertion functions and utilities for session catalog tests
#
# Usage: source tests/STORY-223/test-lib.sh
#

# ============================================================================
# Color Constants
# ============================================================================
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly NC='\033[0m'  # No Color

# ============================================================================
# Test Counters (Global)
# ============================================================================
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# ============================================================================
# Constants
# ============================================================================
readonly SESSION_MINER_FILE="/mnt/c/Projects/DevForgeAI2/.claude/agents/session-miner.md"
readonly PLANS_DIR="/mnt/c/Projects/DevForgeAI2/.claude/plans"
readonly STORIES_DIR="/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories"

# ============================================================================
# Assertion: assert_equal(expected, actual, message)
# Compares expected with actual value. Increments test counter.
# ============================================================================
assert_equal() {
    local expected="$1"
    local actual="$2"
    local message="${3:-Assertion failed}"

    TESTS_RUN=$((TESTS_RUN + 1))

    if [[ "$expected" == "$actual" ]]; then
        echo -e "${GREEN}PASS${NC} $message"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAIL${NC} $message"
        echo "  Expected: $expected"
        echo "  Actual: $actual"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

# ============================================================================
# Assertion: assert_not_empty(value, message)
# Verifies value is not empty string.
# ============================================================================
assert_not_empty() {
    local value="$1"
    local message="${2:-Assertion failed}"

    TESTS_RUN=$((TESTS_RUN + 1))

    if [[ -n "$value" ]]; then
        echo -e "${GREEN}PASS${NC} $message"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAIL${NC} $message"
        echo "  Value is empty"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

# ============================================================================
# Assertion: assert_file_exists(file, message)
# Verifies file exists at given path.
# ============================================================================
assert_file_exists() {
    local file="$1"
    local message="${2:-File should exist: $file}"

    TESTS_RUN=$((TESTS_RUN + 1))

    if [[ -f "$file" ]]; then
        echo -e "${GREEN}PASS${NC} $message"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAIL${NC} $message"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

# ============================================================================
# Assertion: assert_contains(haystack, needle, message)
# Verifies needle string exists in haystack (supports regex).
# ============================================================================
assert_contains() {
    local haystack="$1"
    local needle="$2"
    local message="${3:-String should contain value}"

    TESTS_RUN=$((TESTS_RUN + 1))

    if echo "$haystack" | grep -q "$needle"; then
        echo -e "${GREEN}PASS${NC} $message"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAIL${NC} $message"
        echo "  Looking for: $needle"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

# ============================================================================
# Assertion: assert_json_has_field(json_string, field_name, message)
# Verifies JSON contains specified field.
# ============================================================================
assert_json_has_field() {
    local json_string="$1"
    local field_name="$2"
    local message="${3:-JSON should contain field: $field_name}"

    TESTS_RUN=$((TESTS_RUN + 1))

    if echo "$json_string" | grep -q "\"$field_name\""; then
        echo -e "${GREEN}PASS${NC} $message"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAIL${NC} $message"
        echo "  Looking for field: $field_name"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

# ============================================================================
# Assertion: assert_array_length(json_array, expected_length, message)
# Verifies JSON array has expected number of elements.
# ============================================================================
assert_array_length() {
    local json_array="$1"
    local expected_length="$2"
    local message="${3:-Array should have $expected_length elements}"

    TESTS_RUN=$((TESTS_RUN + 1))

    # Count array elements by counting commas + 1 (simplified)
    local actual_length
    actual_length=$(echo "$json_array" | grep -o '"' | wc -l)
    actual_length=$((actual_length / 2))  # Each string has 2 quotes

    if [[ "$actual_length" -ge "$expected_length" ]]; then
        echo -e "${GREEN}PASS${NC} $message"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAIL${NC} $message"
        echo "  Expected: >= $expected_length elements"
        echo "  Actual: $actual_length elements"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

# ============================================================================
# Assertion: assert_directory_exists(dir, message)
# Verifies directory exists at given path.
# ============================================================================
assert_directory_exists() {
    local dir="$1"
    local message="${2:-Directory should exist: $dir}"

    TESTS_RUN=$((TESTS_RUN + 1))

    if [[ -d "$dir" ]]; then
        echo -e "${GREEN}PASS${NC} $message"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAIL${NC} $message"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

# ============================================================================
# Assertion: assert_function_exists(function_name, message)
# Verifies a bash function is defined.
# ============================================================================
assert_function_exists() {
    local function_name="$1"
    local message="${2:-Function should exist: $function_name}"

    TESTS_RUN=$((TESTS_RUN + 1))

    if declare -f "$function_name" &> /dev/null; then
        echo -e "${GREEN}PASS${NC} $message"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAIL${NC} $message"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

# ============================================================================
# Helper: create_test_session_dir(base_dir)
# Creates a temporary directory with mock session data structure
# Returns: path to temp directory
# ============================================================================
create_test_session_dir() {
    local base_dir="${1:-/tmp/test-story-223-$$}"
    mkdir -p "$base_dir/plans"
    mkdir -p "$base_dir/sessions"
    mkdir -p "$base_dir/artifacts"
    echo "$base_dir"
}

# ============================================================================
# Helper: create_mock_plan_file(plan_dir, plan_id, story_refs)
# Creates a mock plan file with specified story references
# ============================================================================
create_mock_plan_file() {
    local plan_dir="$1"
    local plan_id="$2"
    local story_refs="$3"  # Comma-separated: "STORY-100,STORY-101"

    cat > "$plan_dir/$plan_id.md" << EOF
---
id: $plan_id
status: approved
created: 2025-01-02
author: claude/test
related_stories:
$(for story in $(echo "$story_refs" | tr ',' '\n'); do echo "  - $story"; done)
---

# Test Plan: $plan_id

This is a mock plan file for testing purposes.
EOF
}

# ============================================================================
# Helper: create_mock_session_file(session_dir, session_id, parent_uuid)
# Creates a mock session file with parentUuid reference
# ============================================================================
create_mock_session_file() {
    local session_dir="$1"
    local session_id="$2"
    local parent_uuid="${3:-}"  # Optional parent UUID

    local parent_line=""
    if [[ -n "$parent_uuid" ]]; then
        parent_line="\"parentUuid\": \"$parent_uuid\","
    fi

    cat > "$session_dir/$session_id.json" << EOF
{
  "uuid": "$session_id",
  $parent_line
  "timestamp": "2025-01-02T10:00:00Z",
  "command": "/dev STORY-223",
  "status": "success"
}
EOF
}

# ============================================================================
# Helper: print_test_summary(suite_name)
# Prints formatted test results summary
# ============================================================================
print_test_summary() {
    local suite_name="${1:-Test Results}"

    echo "========================================================================"
    echo "$suite_name"
    echo "========================================================================"
    echo "Tests run:    $TESTS_RUN"
    echo "Tests passed: $TESTS_PASSED"
    echo "Tests failed: $TESTS_FAILED"
    echo ""
}

# ============================================================================
# Helper: exit_with_result()
# Prints final PASSED/FAILED message and exits with appropriate code
# ============================================================================
exit_with_result() {
    if [[ $TESTS_FAILED -gt 0 ]]; then
        echo -e "${RED}RESULT: FAILED${NC}"
        exit 1
    else
        echo -e "${GREEN}RESULT: PASSED${NC}"
        exit 0
    fi
}

# ============================================================================
# Helper: reset_test_counters()
# Resets test counters for starting new test run
# ============================================================================
reset_test_counters() {
    TESTS_RUN=0
    TESTS_PASSED=0
    TESTS_FAILED=0
}

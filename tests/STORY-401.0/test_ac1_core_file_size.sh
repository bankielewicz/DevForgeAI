#!/bin/bash
# Test AC#1: Core File Size Compliance
# STORY-401: Extract Anti-Pattern-Scanner to Reference Files
#
# Validates:
# - Core file src/claude/agents/anti-pattern-scanner.md contains <= 300 lines (target)
# - Core file absolutely <= 500 lines (max)
#
# Expected: FAIL initially (TDD Red phase - file currently has 703 lines)

# Configuration
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
CORE_FILE="$PROJECT_ROOT/src/claude/agents/anti-pattern-scanner.md"
TARGET_LINES=300
MAX_LINES=500

# Test tracking
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Test helper functions
pass_test() {
    local test_name="$1"
    TESTS_PASSED=$((TESTS_PASSED + 1))
    echo "[PASS] $test_name"
}

fail_test() {
    local test_name="$1"
    local message="$2"
    TESTS_FAILED=$((TESTS_FAILED + 1))
    echo "[FAIL] $test_name: $message"
}

run_test() {
    local test_name="$1"
    TESTS_RUN=$((TESTS_RUN + 1))
    shift
    "$@"
}

# -----------------------------------------------------------------------------
# Test 1: Core file exists
# -----------------------------------------------------------------------------
test_core_file_exists() {
    local test_name="Core file exists"
    if [ -f "$CORE_FILE" ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "File not found: $CORE_FILE"
    fi
}

# -----------------------------------------------------------------------------
# Test 2: Core file line count <= 300 (target)
# -----------------------------------------------------------------------------
test_core_file_target_lines() {
    local test_name="Core file line count <= $TARGET_LINES (target)"

    if [ ! -f "$CORE_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    local line_count
    line_count=$(wc -l < "$CORE_FILE")

    if [ "$line_count" -le "$TARGET_LINES" ]; then
        pass_test "$test_name (actual: $line_count lines)"
    else
        fail_test "$test_name" "File has $line_count lines (target: $TARGET_LINES)"
    fi
}

# -----------------------------------------------------------------------------
# Test 3: Core file line count <= 500 (absolute max)
# -----------------------------------------------------------------------------
test_core_file_max_lines() {
    local test_name="Core file line count <= $MAX_LINES (absolute max)"

    if [ ! -f "$CORE_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    local line_count
    line_count=$(wc -l < "$CORE_FILE")

    if [ "$line_count" -le "$MAX_LINES" ]; then
        pass_test "$test_name (actual: $line_count lines)"
    else
        fail_test "$test_name" "File has $line_count lines (max allowed: $MAX_LINES)"
    fi
}

# -----------------------------------------------------------------------------
# Main test execution
# -----------------------------------------------------------------------------
echo "=============================================="
echo "STORY-401 AC#1: Core File Size Compliance"
echo "=============================================="
echo "Target file: $CORE_FILE"
echo "Target lines: $TARGET_LINES | Max lines: $MAX_LINES"
echo "----------------------------------------------"
echo ""

run_test "1" test_core_file_exists
run_test "2" test_core_file_target_lines
run_test "3" test_core_file_max_lines

echo ""
echo "=============================================="
echo "Test Summary: $TESTS_PASSED/$TESTS_RUN passed"
echo "=============================================="

if [ "$TESTS_FAILED" -gt 0 ]; then
    echo "Status: FAILED ($TESTS_FAILED failures)"
    exit 1
else
    echo "Status: PASSED"
    exit 0
fi

#!/bin/bash
# Test AC#5: File follows Markdown documentation style standards
# STORY-406: Create Batch Sibling Story Session Template
#
# Validates:
# - File is between 200-400 lines
# - File is under 20,000 characters (single Read() load)
# - Uses imperative verbs (not narrative prose)
#
# Expected: FAIL initially (TDD Red phase - file does not exist yet)

# Configuration
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TARGET_FILE="$PROJECT_ROOT/src/claude/memory/batch-sibling-story-session-template.md"

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
# Test 1: File is between 200-400 lines
# -----------------------------------------------------------------------------
test_line_count() {
    local test_name="File is between 200-400 lines"
    if [ ! -f "$TARGET_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    local line_count
    line_count=$(wc -l < "$TARGET_FILE")
    if [ "$line_count" -ge 200 ] && [ "$line_count" -le 400 ]; then
        pass_test "$test_name ($line_count lines)"
    else
        fail_test "$test_name" "Expected 200-400 lines, found $line_count"
    fi
}

# -----------------------------------------------------------------------------
# Test 2: File is under 20,000 characters (single Read() load)
# -----------------------------------------------------------------------------
test_character_count() {
    local test_name="File is under 20,000 characters"
    if [ ! -f "$TARGET_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    local char_count
    char_count=$(wc -c < "$TARGET_FILE")
    if [ "$char_count" -le 20000 ]; then
        pass_test "$test_name ($char_count characters)"
    else
        fail_test "$test_name" "Expected <= 20,000 characters, found $char_count"
    fi
}

# -----------------------------------------------------------------------------
# Test 3: File under 500 lines (non-functional requirement)
# -----------------------------------------------------------------------------
test_under_500_lines() {
    local test_name="File is under 500 lines (NFR: single Read() load)"
    if [ ! -f "$TARGET_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    local line_count
    line_count=$(wc -l < "$TARGET_FILE")
    if [ "$line_count" -lt 500 ]; then
        pass_test "$test_name ($line_count lines)"
    else
        fail_test "$test_name" "Expected < 500 lines, found $line_count"
    fi
}

# -----------------------------------------------------------------------------
# Test 4: No narrative prose style (forbidden per coding-standards.md)
# -----------------------------------------------------------------------------
test_no_narrative_prose() {
    local test_name="No narrative prose style (direct instructions only)"
    if [ ! -f "$TARGET_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    # Check for forbidden prose patterns: "The system should...", "It will then..."
    # These indicate narrative style rather than direct instruction style
    local prose_count
    prose_count=$(grep -ciE '(The system should|It will then|This will|One should|You might want to consider)' "$TARGET_FILE")
    if [ "$prose_count" -eq 0 ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Found $prose_count narrative prose patterns (forbidden per coding-standards.md)"
    fi
}

# -----------------------------------------------------------------------------
# Test 5: Minimum 3+ recommended batch size mentioned
# -----------------------------------------------------------------------------
test_batch_size_recommendation() {
    local test_name="Batch size recommendation (3+ stories) is documented"
    if [ ! -f "$TARGET_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    if grep -qE '3\+|three or more|3 or more|at least 3' "$TARGET_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No batch size recommendation (3+ stories) found"
    fi
}

# -----------------------------------------------------------------------------
# Main test execution
# -----------------------------------------------------------------------------
echo "=============================================="
echo "STORY-406 AC#5: Markdown Style Standards"
echo "=============================================="
echo "Target file: $TARGET_FILE"
echo "----------------------------------------------"
echo ""

run_test "1" test_line_count
run_test "2" test_character_count
run_test "3" test_under_500_lines
run_test "4" test_no_narrative_prose
run_test "5" test_batch_size_recommendation

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

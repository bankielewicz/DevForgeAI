#!/bin/bash
# Test AC#3: Template references EPIC-057 as proof of concept
# STORY-406: Create Batch Sibling Story Session Template
#
# Validates:
# - EPIC-057 is referenced in the file
# - STORY-366 through STORY-370 are all referenced
# - Progressive efficiency gains data is present
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
# Test 1: EPIC-057 is referenced
# -----------------------------------------------------------------------------
test_epic057_referenced() {
    local test_name="EPIC-057 is referenced"
    if [ ! -f "$TARGET_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    if grep -q 'EPIC-057' "$TARGET_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "'EPIC-057' not found in file"
    fi
}

# -----------------------------------------------------------------------------
# Test 2: STORY-366 is referenced
# -----------------------------------------------------------------------------
test_story366_referenced() {
    local test_name="STORY-366 is referenced"
    if [ ! -f "$TARGET_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    if grep -q 'STORY-366' "$TARGET_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "'STORY-366' not found in file"
    fi
}

# -----------------------------------------------------------------------------
# Test 3: STORY-367 is referenced
# -----------------------------------------------------------------------------
test_story367_referenced() {
    local test_name="STORY-367 is referenced"
    if [ ! -f "$TARGET_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    if grep -q 'STORY-367' "$TARGET_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "'STORY-367' not found in file"
    fi
}

# -----------------------------------------------------------------------------
# Test 4: STORY-368 is referenced
# -----------------------------------------------------------------------------
test_story368_referenced() {
    local test_name="STORY-368 is referenced"
    if [ ! -f "$TARGET_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    if grep -q 'STORY-368' "$TARGET_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "'STORY-368' not found in file"
    fi
}

# -----------------------------------------------------------------------------
# Test 5: STORY-369 is referenced
# -----------------------------------------------------------------------------
test_story369_referenced() {
    local test_name="STORY-369 is referenced"
    if [ ! -f "$TARGET_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    if grep -q 'STORY-369' "$TARGET_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "'STORY-369' not found in file"
    fi
}

# -----------------------------------------------------------------------------
# Test 6: STORY-370 is referenced
# -----------------------------------------------------------------------------
test_story370_referenced() {
    local test_name="STORY-370 is referenced"
    if [ ! -f "$TARGET_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    if grep -q 'STORY-370' "$TARGET_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "'STORY-370' not found in file"
    fi
}

# -----------------------------------------------------------------------------
# Test 7: Progressive efficiency gains data present
# -----------------------------------------------------------------------------
test_efficiency_gains_data() {
    local test_name="Progressive efficiency gains data present"
    if [ ! -f "$TARGET_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    # Check for percentage references indicating efficiency data (e.g., 35%, 40%, reduction)
    if grep -qiE '(35|40)%|efficiency|time reduction' "$TARGET_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No efficiency gains data (e.g., '35%', '40%', 'time reduction') found"
    fi
}

# -----------------------------------------------------------------------------
# Main test execution
# -----------------------------------------------------------------------------
echo "=============================================="
echo "STORY-406 AC#3: EPIC-057 References"
echo "=============================================="
echo "Target file: $TARGET_FILE"
echo "----------------------------------------------"
echo ""

run_test "1" test_epic057_referenced
run_test "2" test_story366_referenced
run_test "3" test_story367_referenced
run_test "4" test_story368_referenced
run_test "5" test_story369_referenced
run_test "6" test_story370_referenced
run_test "7" test_efficiency_gains_data

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

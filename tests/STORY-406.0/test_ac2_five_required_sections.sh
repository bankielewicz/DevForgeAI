#!/bin/bash
# Test AC#2: Template contains all five required sections
# STORY-406: Create Batch Sibling Story Session Template
#
# Validates:
# - Section 1: Epic Context Loading Instructions
# - Section 2: Shared Pattern Recognition
# - Section 3: Incremental Observation Capture
# - Section 4: Batch Coordination Instructions
# - Section 5: Proof of Concept
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
# Test 1: Section - Epic Context Loading Instructions
# -----------------------------------------------------------------------------
test_section_epic_context() {
    local test_name="Section present: Epic Context Loading Instructions"
    if [ ! -f "$TARGET_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    if grep -qi 'Epic Context Loading' "$TARGET_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Heading containing 'Epic Context Loading' not found"
    fi
}

# -----------------------------------------------------------------------------
# Test 2: Section - Shared Pattern Recognition
# -----------------------------------------------------------------------------
test_section_shared_pattern() {
    local test_name="Section present: Shared Pattern Recognition"
    if [ ! -f "$TARGET_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    if grep -qi 'Shared Pattern Recognition' "$TARGET_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Heading containing 'Shared Pattern Recognition' not found"
    fi
}

# -----------------------------------------------------------------------------
# Test 3: Section - Incremental Observation Capture
# -----------------------------------------------------------------------------
test_section_observation_capture() {
    local test_name="Section present: Incremental Observation Capture"
    if [ ! -f "$TARGET_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    if grep -qi 'Incremental Observation Capture' "$TARGET_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Heading containing 'Incremental Observation Capture' not found"
    fi
}

# -----------------------------------------------------------------------------
# Test 4: Section - Batch Coordination Instructions
# -----------------------------------------------------------------------------
test_section_batch_coordination() {
    local test_name="Section present: Batch Coordination Instructions"
    if [ ! -f "$TARGET_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    if grep -qi 'Batch Coordination' "$TARGET_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Heading containing 'Batch Coordination' not found"
    fi
}

# -----------------------------------------------------------------------------
# Test 5: Section - Proof of Concept
# -----------------------------------------------------------------------------
test_section_proof_of_concept() {
    local test_name="Section present: Proof of Concept"
    if [ ! -f "$TARGET_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    if grep -qi 'Proof of Concept' "$TARGET_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Heading containing 'Proof of Concept' not found"
    fi
}

# -----------------------------------------------------------------------------
# Test 6: All five sections are H2 headings (## level)
# -----------------------------------------------------------------------------
test_sections_are_h2() {
    local test_name="All five sections use ## heading level"
    if [ ! -f "$TARGET_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    local h2_count
    h2_count=$(grep -cE '^## ' "$TARGET_FILE")
    if [ "$h2_count" -ge 5 ]; then
        pass_test "$test_name ($h2_count H2 headings found)"
    else
        fail_test "$test_name" "Expected at least 5 H2 headings, found $h2_count"
    fi
}

# -----------------------------------------------------------------------------
# Main test execution
# -----------------------------------------------------------------------------
echo "=============================================="
echo "STORY-406 AC#2: Five Required Sections"
echo "=============================================="
echo "Target file: $TARGET_FILE"
echo "----------------------------------------------"
echo ""

run_test "1" test_section_epic_context
run_test "2" test_section_shared_pattern
run_test "3" test_section_observation_capture
run_test "4" test_section_batch_coordination
run_test "5" test_section_proof_of_concept
run_test "6" test_sections_are_h2

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

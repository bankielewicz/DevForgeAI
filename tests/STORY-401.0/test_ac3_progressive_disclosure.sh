#!/bin/bash
# Test AC#3: Progressive Disclosure Read() Instructions in Core File
# STORY-401: Extract Anti-Pattern-Scanner to Reference Files
#
# Validates:
# - Core file contains exactly 2 Read(file_path= instructions
# - Read instructions point to integration-testing-guide.md
# - Read instructions point to metrics-reference.md
#
# Expected: FAIL initially (TDD Red phase - no Read() instructions in current file)

# Configuration
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
CORE_FILE="$PROJECT_ROOT/src/claude/agents/anti-pattern-scanner.md"
EXPECTED_READ_COUNT=2

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
# Test 1: Core file contains Read(file_path= instructions
# -----------------------------------------------------------------------------
test_read_instructions_exist() {
    local test_name="Core file contains Read(file_path= instructions"

    if [ ! -f "$CORE_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    local read_count
    read_count=$(grep -c 'Read(file_path=' "$CORE_FILE")

    if [ "$read_count" -gt 0 ]; then
        pass_test "$test_name (found $read_count)"
    else
        fail_test "$test_name" "No Read(file_path= instructions found"
    fi
}

# -----------------------------------------------------------------------------
# Test 2: Exactly 2 Read() instructions pointing to anti-pattern-scanner/references/
# Note: We count only Read() instructions pointing to the NEW reference files,
# not pre-existing references like phase5-treelint-detection.md
# -----------------------------------------------------------------------------
test_exact_read_count() {
    local test_name="Exactly $EXPECTED_READ_COUNT Read() pointing to anti-pattern-scanner/references/"

    if [ ! -f "$CORE_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    local read_count
    read_count=$(grep -c 'Read(file_path=.*anti-pattern-scanner/references/' "$CORE_FILE")

    if [ "$read_count" -eq "$EXPECTED_READ_COUNT" ]; then
        pass_test "$test_name (found $read_count)"
    else
        fail_test "$test_name" "Found $read_count Read() instructions (expected $EXPECTED_READ_COUNT)"
    fi
}

# -----------------------------------------------------------------------------
# Test 3: Read() instruction references integration-testing-guide.md
# -----------------------------------------------------------------------------
test_read_integration_testing_guide() {
    local test_name="Read() references integration-testing-guide.md"

    if [ ! -f "$CORE_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    if grep -q 'Read(file_path=.*integration-testing-guide\.md' "$CORE_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No Read() instruction pointing to integration-testing-guide.md"
    fi
}

# -----------------------------------------------------------------------------
# Test 4: Read() instruction references metrics-reference.md
# -----------------------------------------------------------------------------
test_read_metrics_reference() {
    local test_name="Read() references metrics-reference.md"

    if [ ! -f "$CORE_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    if grep -q 'Read(file_path=.*metrics-reference\.md' "$CORE_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No Read() instruction pointing to metrics-reference.md"
    fi
}

# -----------------------------------------------------------------------------
# Main test execution
# -----------------------------------------------------------------------------
echo "=============================================="
echo "STORY-401 AC#3: Progressive Disclosure Read()"
echo "=============================================="
echo "Target file: $CORE_FILE"
echo "Expected Read() count: $EXPECTED_READ_COUNT"
echo "----------------------------------------------"
echo ""

run_test "1" test_read_instructions_exist
run_test "2" test_exact_read_count
run_test "3" test_read_integration_testing_guide
run_test "4" test_read_metrics_reference

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

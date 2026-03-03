#!/bin/bash

# STORY-170 Integration Test: All Acceptance Criteria Together
# Validates that all AC components work together as a cohesive feature
#
# This test SHOULD FAIL initially (Red phase - TDD)
# Runs after all individual AC tests pass

set -e

SKILL_FILE=".claude/skills/devforgeai-development/SKILL.md"

echo "TEST: STORY-170 Integration - Visual Iteration Counter"
echo "======================================================="
echo ""

# Track failures
FAILURES=0
TESTS_RUN=0

run_test() {
    local test_name="$1"
    local test_script="$2"

    TESTS_RUN=$((TESTS_RUN + 1))
    echo "Running: $test_name"

    if bash "$test_script" > /dev/null 2>&1; then
        echo "  [PASS] $test_name"
    else
        echo "  [FAIL] $test_name"
        FAILURES=$((FAILURES + 1))
    fi
}

# Check if SKILL.md exists first
if [ ! -f "$SKILL_FILE" ]; then
    echo "FAIL: $SKILL_FILE does not exist"
    exit 1
fi

echo "Checking that all AC components integrate correctly..."
echo ""

# Test 1: Run individual AC tests
echo "--- Individual AC Tests ---"
TEST_DIR="tests/STORY-170"

run_test "AC-1: Iteration Counter in Phase Headers" "$TEST_DIR/test_ac1_iteration_counter_in_phase_headers.sh"
run_test "AC-2: Counter Increments on Resumption" "$TEST_DIR/test_ac2_counter_increments_on_resumption.sh"
run_test "AC-3: Warning at High Iterations" "$TEST_DIR/test_ac3_warning_at_high_iterations.sh"
run_test "AC-4: Counter Persists Across Session" "$TEST_DIR/test_ac4_counter_persists_across_session.sh"

echo ""
echo "--- Integration Checks ---"

# Test 2: Verify iteration lifecycle is complete
# Should have: init (1) -> display -> increment -> persist -> resume
TESTS_RUN=$((TESTS_RUN + 1))
echo "Checking iteration lifecycle completeness..."

LIFECYCLE_SCORE=0
LIFECYCLE_ITEMS="initialization display increment persist resume warning"

for item in $LIFECYCLE_ITEMS; do
    if grep -qi "$item" "$SKILL_FILE" 2>/dev/null; then
        LIFECYCLE_SCORE=$((LIFECYCLE_SCORE + 1))
    fi
done

if [ "$LIFECYCLE_SCORE" -ge 5 ]; then
    echo "  [PASS] Iteration lifecycle appears complete ($LIFECYCLE_SCORE/6 items found)"
else
    echo "  [FAIL] Iteration lifecycle incomplete ($LIFECYCLE_SCORE/6 items found)"
    FAILURES=$((FAILURES + 1))
fi

# Test 3: Verify iteration counter is integrated with phase display template
TESTS_RUN=$((TESTS_RUN + 1))
echo "Checking iteration-phase display integration..."

# Extract phase display template and check for iteration
PHASE_TEMPLATE=$(grep -A10 "Phase NN/10:" "$SKILL_FILE" 2>/dev/null | head -15 || true)

if echo "$PHASE_TEMPLATE" | grep -q "Iteration"; then
    echo "  [PASS] Iteration counter integrated with phase display template"
else
    echo "  [FAIL] Iteration counter not found in phase display template"
    FAILURES=$((FAILURES + 1))
fi

# Test 4: Verify max iterations constant (5) is used consistently
TESTS_RUN=$((TESTS_RUN + 1))
echo "Checking max iterations consistency..."

MAX_5_COUNT=$(grep -o "/5" "$SKILL_FILE" 2>/dev/null | wc -l || echo "0")

if [ "$MAX_5_COUNT" -ge 2 ]; then
    echo "  [PASS] Max iterations (5) used consistently ($MAX_5_COUNT occurrences)"
else
    echo "  [FAIL] Max iterations (5) not used consistently (found $MAX_5_COUNT occurrences)"
    FAILURES=$((FAILURES + 1))
fi

# Test 5: Verify warning threshold (4) and display are connected
TESTS_RUN=$((TESTS_RUN + 1))
echo "Checking warning threshold integration..."

WARNING_SECTION=$(grep -B5 -A5 "Approaching limit" "$SKILL_FILE" 2>/dev/null || true)

if echo "$WARNING_SECTION" | grep -qE "[>=].*4|4.*[>=]"; then
    echo "  [PASS] Warning threshold (4) connected to display logic"
else
    echo "  [FAIL] Warning threshold not properly connected to display"
    FAILURES=$((FAILURES + 1))
fi

# Test 6: Verify persistence and resume are linked
TESTS_RUN=$((TESTS_RUN + 1))
echo "Checking persistence-resume integration..."

if grep -q "phase-state" "$SKILL_FILE" && grep -q "iteration_count" "$SKILL_FILE"; then
    echo "  [PASS] Persistence mechanism (phase-state.json) references iteration_count"
else
    echo "  [FAIL] Persistence and iteration_count not properly linked"
    FAILURES=$((FAILURES + 1))
fi

echo ""
echo "======================================================="
echo "INTEGRATION TEST SUMMARY"
echo "======================================================="
echo ""
echo "Tests Run: $TESTS_RUN"
echo "Passed:    $((TESTS_RUN - FAILURES))"
echo "Failed:    $FAILURES"
echo ""

if [ "$FAILURES" -eq 0 ]; then
    echo "RESULT: ALL TESTS PASSED"
    exit 0
else
    echo "RESULT: $FAILURES TEST(S) FAILED"
    exit 1
fi

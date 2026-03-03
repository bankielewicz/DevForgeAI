#!/bin/bash
# Test AC#5: Summary Statistics Reflect Filter
# STORY-347: Add --blocking-only Filter to review-qa-reports
#
# Validates:
# - Total count reflects filtered results
# - Footer shows hidden gap count
# - Filter active message displayed
#
# Expected: FAIL initially (TDD Red phase)

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
SKILL_FILE="$PROJECT_ROOT/.claude/skills/devforgeai-qa-remediation/SKILL.md"

TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

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
    TESTS_RUN=$((TESTS_RUN + 1))
}

echo "=============================================="
echo "STORY-347 AC#5: Summary Statistics Reflect Filter"
echo "=============================================="
echo "Target file: $SKILL_FILE"
echo "----------------------------------------------"
echo ""

# Test 5.1: Total count shows filtered count
run_test
if grep -qiE 'total.*filtered|filtered.*count|count.*after.*filter' "$SKILL_FILE"; then
    pass_test "Total shows filtered count"
else
    fail_test "Total shows filtered count" "Summary should show filtered count, not raw total"
fi

# Test 5.2: Hidden gap count documented
run_test
if grep -qiE 'hidden.*count|gaps.*hidden|\$HIDDEN_COUNT|hidden_count' "$SKILL_FILE"; then
    pass_test "Hidden gap count documented"
else
    fail_test "Hidden gap count documented" "Should track count of hidden/filtered gaps"
fi

# Test 5.3: Filter active message documented
run_test
if grep -qiE 'filter.*active|--blocking-only.*active|filter.*message' "$SKILL_FILE"; then
    pass_test "Filter active message documented"
else
    fail_test "Filter active message documented" "Should show message when filter is active"
fi

# Test 5.4: Footer message format (X advisory gaps hidden)
run_test
if grep -qiE 'advisory.*gaps.*hidden|hidden.*advisory|N.*gaps.*hidden' "$SKILL_FILE"; then
    pass_test "Footer message format documented"
else
    fail_test "Footer message format documented" "Should show 'X advisory gaps hidden' in footer"
fi

# Test 5.5: Final summary includes filter status
run_test
if grep -A 30 'Final Summary' "$SKILL_FILE" | grep -qiE 'blocking.only|filter.*status|advisory.*hidden'; then
    pass_test "Final summary includes filter status"
else
    fail_test "Final summary includes filter status" "Final summary should reflect filter state"
fi

echo ""
echo "=============================================="
echo "Test Summary: $TESTS_PASSED/$TESTS_RUN passed"
echo "=============================================="

if [ "$TESTS_FAILED" -gt 0 ]; then
    echo "Status: FAILED ($TESTS_FAILED failures)"
    echo ""
    echo "TDD Red Phase: Expected failures - implementation not complete"
    exit 1
else
    echo "Status: PASSED"
    exit 0
fi

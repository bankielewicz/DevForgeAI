#!/bin/bash
# Test AC#4: Flag Combines with --min-severity
# STORY-347: Add --blocking-only Filter to review-qa-reports
#
# Validates:
# - AND logic applied (not OR)
# - Both filters respected simultaneously
#
# Expected: FAIL initially (TDD Red phase)

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
COMMAND_FILE="$PROJECT_ROOT/.claude/commands/review-qa-reports.md"
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
echo "STORY-347 AC#4: Flag Combines with --min-severity"
echo "=============================================="
echo "Target files:"
echo "  - $COMMAND_FILE"
echo "  - $SKILL_FILE"
echo "----------------------------------------------"
echo ""

# Test 4.1: Combined usage example exists
run_test
if grep -qE -- '--blocking-only.*--min-severity|--min-severity.*--blocking-only' "$COMMAND_FILE"; then
    pass_test "Combined usage example exists"
else
    fail_test "Combined usage example exists" "Should have example with both flags"
fi

# Test 4.2: AND logic documented (not OR)
run_test
if grep -qiE 'AND.*logic|both.*filter|combine.*AND|AND-combined|intersection' "$SKILL_FILE" || \
   grep -qiE 'BOTH.*blocking.*AND.*severity|AND.*not.*OR' "$COMMAND_FILE"; then
    pass_test "AND logic documented"
else
    fail_test "AND logic documented" "Should document filters use AND logic, not OR"
fi

# Test 4.3: Filter combination in Phase 03
run_test
if grep -A 80 'Phase 03:' "$SKILL_FILE" | grep -qiE 'blocking.only.*min.severity|min.severity.*blocking.only|both.*filter'; then
    pass_test "Filter combination in Phase 03"
else
    fail_test "Filter combination in Phase 03" "Phase 03 should handle combined filters"
fi

# Test 4.4: Example shows expected behavior
run_test
if grep -qiE -- '--blocking-only --min-severity HIGH' "$COMMAND_FILE"; then
    pass_test "HIGH severity + blocking example"
else
    fail_test "HIGH severity + blocking example" "Should show example: --blocking-only --min-severity HIGH"
fi

# Test 4.5: Both conditions must be met (documented)
run_test
if grep -qiE 'both.*condition|both.*must|severity.*>=.*HIGH.*AND.*blocking' "$SKILL_FILE" || \
   grep -qiE 'blocking:.*true.*AND|BOTH.*blocking.*AND' "$COMMAND_FILE"; then
    pass_test "Both conditions required documented"
else
    fail_test "Both conditions required documented" "Should document that both conditions must be met"
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

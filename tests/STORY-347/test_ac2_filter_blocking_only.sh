#!/bin/bash
# Test AC#2: Blocking-Only Filter Applied to Gap Display
# STORY-347: Add --blocking-only Filter to review-qa-reports
#
# Validates:
# - Filter logic documented in skill Phase 03
# - Only blocking: true gaps displayed when flag set
# - Advisory gaps excluded from table
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
echo "STORY-347 AC#2: Blocking-Only Filter Applied"
echo "=============================================="
echo "Target file: $SKILL_FILE"
echo "----------------------------------------------"
echo ""

# Test 2.1: Filter logic documented in Phase 03 section
run_test
if grep -A 50 'Phase 03:' "$SKILL_FILE" | grep -qiE 'blocking.only|filter.*blocking'; then
    pass_test "Filter logic in Phase 03"
else
    fail_test "Filter logic in Phase 03" "Phase 03 should document --blocking-only filter logic"
fi

# Test 2.2: Filter condition documented (blocking === true)
run_test
if grep -qiE 'blocking.*===.*true|blocking.*==.*true|blocking.*:.*true' "$SKILL_FILE" && \
   grep -qiE 'filter|when.*--blocking-only' "$SKILL_FILE"; then
    pass_test "Filter condition documented"
else
    fail_test "Filter condition documented" "Should document filtering to blocking: true gaps"
fi

# Test 2.3: Advisory gap exclusion mentioned
run_test
if grep -qiE 'advisory.*exclu|blocking.*false.*exclu|filter.*out.*advisory' "$SKILL_FILE"; then
    pass_test "Advisory gap exclusion documented"
else
    fail_test "Advisory gap exclusion documented" "Should mention advisory gaps are excluded"
fi

# Test 2.4: $BLOCKING_ONLY variable in argument parsing
run_test
if grep -qE '\$BLOCKING_ONLY|\$blocking_only|blocking_only' "$SKILL_FILE"; then
    pass_test "BLOCKING_ONLY variable defined"
else
    fail_test "BLOCKING_ONLY variable defined" "Should have $BLOCKING_ONLY variable in argument parsing"
fi

# Test 2.5: Conditional filter application logic
run_test
if grep -qiE 'if.*blocking.only|when.*blocking.only|IF.*\$BLOCKING_ONLY' "$SKILL_FILE"; then
    pass_test "Conditional filter logic present"
else
    fail_test "Conditional filter logic present" "Should have IF $BLOCKING_ONLY conditional"
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

#!/bin/bash
# Test AC#3: Gap Count Summary Includes Blocking Breakdown
# STORY-346: Update review-qa-reports Default to Show All Gaps
#
# Validates:
# - Summary shows "Blocking Gaps: X"
# - Summary shows "Advisory Gaps: Y"
# - Summary shows "Total Gaps: Z"
# - Documentation indicates Total = Blocking + Advisory
#
# Expected: FAIL initially (TDD Red phase - breakdown not implemented)

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
echo "STORY-346 AC#3: Gap Count Summary Includes Blocking Breakdown"
echo "=============================================="
echo "Target file: $SKILL_FILE"
echo "----------------------------------------------"
echo ""

# Test 3.1: Skill file exists
run_test
if [ -f "$SKILL_FILE" ]; then
    pass_test "Skill file exists"
else
    fail_test "Skill file exists" "File not found: $SKILL_FILE"
    exit 1
fi

# Test 3.2: "Blocking Gaps" count in summary section
run_test
if grep -qE 'Blocking Gaps:' "$SKILL_FILE"; then
    pass_test "Blocking Gaps count label present"
else
    fail_test "Blocking Gaps count label present" "Summary should include 'Blocking Gaps: X'"
fi

# Test 3.3: "Advisory Gaps" count in summary section
run_test
if grep -qE 'Advisory Gaps:' "$SKILL_FILE"; then
    pass_test "Advisory Gaps count label present"
else
    fail_test "Advisory Gaps count label present" "Summary should include 'Advisory Gaps: Y'"
fi

# Test 3.4: "Total Gaps" count exists (backward compatibility)
run_test
if grep -qE 'Total Gaps' "$SKILL_FILE"; then
    pass_test "Total Gaps count label present"
else
    fail_test "Total Gaps count label present" "Summary should include 'Total Gaps: Z'"
fi

# Test 3.5: Summary display includes breakdown in Final Summary section
run_test
# Check the Final Summary section specifically for the breakdown
if grep -A 20 '## Final Summary' "$SKILL_FILE" | grep -qE 'Blocking|Advisory'; then
    pass_test "Final Summary section includes blocking breakdown"
else
    fail_test "Final Summary section includes blocking breakdown" "Final Summary should show blocking/advisory counts"
fi

# Test 3.6: Count validation rule documented (Total = Blocking + Advisory)
run_test
if grep -qE 'Total.*=.*Blocking.*Advisory|Blocking.*\+.*Advisory.*Total' "$SKILL_FILE"; then
    pass_test "Count validation rule documented"
else
    fail_test "Count validation rule documented" "Should document that Total = Blocking + Advisory"
fi

echo ""
echo "=============================================="
echo "Test Summary: $TESTS_PASSED/$TESTS_RUN passed"
echo "=============================================="

if [ "$TESTS_FAILED" -gt 0 ]; then
    echo "Status: FAILED ($TESTS_FAILED failures)"
    echo ""
    echo "TDD Red Phase: Expected failures - breakdown summary not implemented"
    exit 1
else
    echo "Status: PASSED"
    exit 0
fi

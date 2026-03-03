#!/bin/bash
# Test AC#2: Visual Distinction Between Blocking and Advisory Gaps
# STORY-346: Update review-qa-reports Default to Show All Gaps
#
# Validates:
# - Status column added to gap summary table
# - Red indicator (red circle) for blocking: true gaps
# - Yellow indicator (yellow circle) for blocking: false gaps
#
# Expected: FAIL initially (TDD Red phase - Status column not yet added)

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
echo "STORY-346 AC#2: Visual Distinction Between Blocking and Advisory"
echo "=============================================="
echo "Target file: $SKILL_FILE"
echo "----------------------------------------------"
echo ""

# Test 2.1: Skill file exists
run_test
if [ -f "$SKILL_FILE" ]; then
    pass_test "Skill file exists"
else
    fail_test "Skill file exists" "File not found: $SKILL_FILE"
    exit 1
fi

# Test 2.2: Status column in gap summary table header
run_test
# Looking for table header with Status column
if grep -qE '\|\s*Status\s*\|' "$SKILL_FILE"; then
    pass_test "Status column present in table header"
else
    fail_test "Status column present in table header" "Table should include | Status | column"
    echo "  Current table headers in Phase 04 display:"
    grep -E '^\|\s*#\s*\|.*\|$' "$SKILL_FILE" | head -2
fi

# Test 2.3: Red indicator documented for blocking gaps
run_test
# The red circle emoji should be documented for blocking: true
if grep -q "red" "$SKILL_FILE" && grep -q "blocking.*true" "$SKILL_FILE"; then
    pass_test "Red indicator concept documented for blocking gaps"
else
    fail_test "Red indicator documented for blocking gaps" "Should document red indicator for blocking: true gaps"
fi

# Test 2.4: Yellow indicator documented for advisory gaps
run_test
# The yellow circle emoji should be documented for blocking: false
if grep -q "yellow" "$SKILL_FILE" && grep -q "blocking.*false" "$SKILL_FILE"; then
    pass_test "Yellow indicator concept documented for advisory gaps"
else
    fail_test "Yellow indicator documented for advisory gaps" "Should document yellow indicator for blocking: false gaps"
fi

# Test 2.5: Visual indicator assignment logic documented
run_test
# Check for indicator assignment rule documentation
if grep -qE 'indicator|visual.*distinction|Status.*column' "$SKILL_FILE"; then
    pass_test "Visual indicator logic referenced in skill"
else
    fail_test "Visual indicator logic referenced" "Skill should document how indicators are assigned"
fi

echo ""
echo "=============================================="
echo "Test Summary: $TESTS_PASSED/$TESTS_RUN passed"
echo "=============================================="

if [ "$TESTS_FAILED" -gt 0 ]; then
    echo "Status: FAILED ($TESTS_FAILED failures)"
    echo ""
    echo "TDD Red Phase: Expected failures - Status column not implemented"
    exit 1
else
    echo "Status: PASSED"
    exit 0
fi

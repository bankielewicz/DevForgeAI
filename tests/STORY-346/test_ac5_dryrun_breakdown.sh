#!/bin/bash
# Test AC#5: Dry-Run Mode Displays Blocking Breakdown
# STORY-346: Update review-qa-reports Default to Show All Gaps
#
# Validates:
# - Dry-run output shows blocking gap count
# - Dry-run output shows advisory gap count
# - Format: "Would process X blocking gaps and Y advisory gaps"
#
# Expected: FAIL initially (TDD Red phase - dry-run breakdown not implemented)

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
SKILL_FILE="$PROJECT_ROOT/.claude/skills/devforgeai-qa-remediation/SKILL.md"
COMMAND_FILE="$PROJECT_ROOT/.claude/commands/review-qa-reports.md"

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
echo "STORY-346 AC#5: Dry-Run Mode Displays Blocking Breakdown"
echo "=============================================="
echo "Target file: $SKILL_FILE"
echo "----------------------------------------------"
echo ""

# Test 5.1: Skill file exists
run_test
if [ -f "$SKILL_FILE" ]; then
    pass_test "Skill file exists"
else
    fail_test "Skill file exists" "File not found: $SKILL_FILE"
    exit 1
fi

# Test 5.2: Dry-run mode section exists
run_test
if grep -qE 'Dry-Run|dry-run|DRY_RUN' "$SKILL_FILE"; then
    pass_test "Dry-run mode section exists"
else
    fail_test "Dry-run mode section exists" "Skill should document dry-run mode"
fi

# Test 5.3: Dry-run shows blocking gap count
run_test
if grep -A 10 -iE 'dry.?run' "$SKILL_FILE" | grep -qE 'blocking.*gap|X.*blocking'; then
    pass_test "Dry-run shows blocking gap count"
else
    fail_test "Dry-run shows blocking gap count" "Dry-run output should include blocking gap count"
fi

# Test 5.4: Dry-run shows advisory gap count
run_test
if grep -A 10 -iE 'dry.?run' "$SKILL_FILE" | grep -qE 'advisory.*gap|Y.*advisory'; then
    pass_test "Dry-run shows advisory gap count"
else
    fail_test "Dry-run shows advisory gap count" "Dry-run output should include advisory gap count"
fi

# Test 5.5: Dry-run output format matches specification
run_test
# Looking for: "Would process X blocking gaps and Y advisory gaps"
if grep -qE 'Would process.*blocking.*gaps.*and.*advisory.*gaps' "$SKILL_FILE"; then
    pass_test "Dry-run output format matches specification"
else
    fail_test "Dry-run output format matches specification" "Should show 'Would process X blocking gaps and Y advisory gaps'"
    echo "  Looking for format: 'Would process X blocking gaps and Y advisory gaps'"
fi

# Test 5.6: Dry-run section in Step 4.2
run_test
if grep -qE 'Step 4\.2.*Dry-Run|Handle Dry-Run Mode' "$SKILL_FILE"; then
    pass_test "Dry-run handling documented in Step 4.2"
else
    fail_test "Dry-run handling documented in Step 4.2" "Step 4.2 should handle dry-run mode"
fi

echo ""
echo "=============================================="
echo "Test Summary: $TESTS_PASSED/$TESTS_RUN passed"
echo "=============================================="

if [ "$TESTS_FAILED" -gt 0 ]; then
    echo "Status: FAILED ($TESTS_FAILED failures)"
    echo ""
    echo "TDD Red Phase: Expected failures - dry-run breakdown not implemented"
    exit 1
else
    echo "Status: PASSED"
    exit 0
fi

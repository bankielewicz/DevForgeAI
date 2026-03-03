#!/bin/bash
# Test AC#3: Default Behavior Unchanged (Shows All)
# STORY-347: Add --blocking-only Filter to review-qa-reports
#
# Validates:
# - Without --blocking-only flag, all gaps displayed
# - STORY-346 behavior preserved (default shows all)
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
echo "STORY-347 AC#3: Default Behavior Unchanged"
echo "=============================================="
echo "Target files:"
echo "  - $COMMAND_FILE"
echo "  - $SKILL_FILE"
echo "----------------------------------------------"
echo ""

# Test 3.1: Default --blocking-only is false (not filtering by default)
run_test
if grep -qE '\|\s*`--blocking-only`.*\|\s*false\s*\|' "$COMMAND_FILE"; then
    pass_test "Default is false in argument table"
else
    fail_test "Default is false in argument table" "Default should be false to show all gaps"
fi

# Test 3.2: Without flag, all gaps displayed (documented)
run_test
if grep -qiE 'without.*--blocking-only.*all|default.*all.*gaps|shows.*all.*by.*default' "$COMMAND_FILE" || \
   grep -qiE 'without.*flag.*all' "$SKILL_FILE"; then
    pass_test "Default shows all gaps documented"
else
    fail_test "Default shows all gaps documented" "Should document that default shows all gaps"
fi

# Test 3.3: STORY-346 behavior preserved (min-severity LOW default)
run_test
if grep -qE '\|\s*`--min-severity`.*\|\s*`LOW`\s*\|' "$COMMAND_FILE"; then
    pass_test "STORY-346 min-severity LOW preserved"
else
    fail_test "STORY-346 min-severity LOW preserved" "min-severity default should remain LOW (STORY-346)"
fi

# Test 3.4: No breaking changes to existing behavior
run_test
# Check that blocking_only defaults to false in skill argument parsing
if grep -A 10 'Argument.*Variable.*Default' "$SKILL_FILE" | grep -qiE 'blocking.only.*false'; then
    pass_test "Skill defaults blocking_only to false"
else
    fail_test "Skill defaults blocking_only to false" "Should default to false for backward compatibility"
fi

# Test 3.5: Usage example shows flag is optional
run_test
if grep -qE '# (Review|Show).*all.*gaps' "$COMMAND_FILE" && \
   ! grep -qE '# Review all gaps.*--blocking-only' "$COMMAND_FILE"; then
    pass_test "Usage examples show flag is optional"
else
    fail_test "Usage examples show flag is optional" "Should have example without --blocking-only"
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

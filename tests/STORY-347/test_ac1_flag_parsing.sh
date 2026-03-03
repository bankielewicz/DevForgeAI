#!/bin/bash
# Test AC#1: Flag Recognized and Parsed
# STORY-347: Add --blocking-only Filter to review-qa-reports
#
# Validates:
# - --blocking-only flag added to argument table in command file
# - Flag parsed as boolean (no value required)
# - Default is false when absent
#
# Expected: FAIL initially (TDD Red phase)

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
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
echo "STORY-347 AC#1: Flag Recognized and Parsed"
echo "=============================================="
echo "Target file: $COMMAND_FILE"
echo "----------------------------------------------"
echo ""

# Test 1.1: --blocking-only flag exists in argument table
run_test
if grep -qE '\|\s*`--blocking-only`\s*\|' "$COMMAND_FILE"; then
    pass_test "Flag exists in argument table"
else
    fail_test "Flag exists in argument table" "Expected: | \`--blocking-only\` | in argument table"
fi

# Test 1.2: Flag is documented as boolean type (flag or boolean flag)
run_test
if grep -qE '\|\s*`--blocking-only`.*\|\s*(flag|boolean)\s*\|' "$COMMAND_FILE" || \
   grep -A 2 '`--blocking-only`' "$COMMAND_FILE" | grep -qiE 'boolean|flag'; then
    pass_test "Flag documented as boolean type"
else
    fail_test "Flag documented as boolean type" "Should be documented as boolean flag"
fi

# Test 1.3: Default value is false
run_test
if grep -qE '\|\s*`--blocking-only`.*\|\s*false\s*\|' "$COMMAND_FILE" || \
   grep -A 2 '`--blocking-only`' "$COMMAND_FILE" | grep -qiE 'false|default.*false'; then
    pass_test "Default value is false"
else
    fail_test "Default value is false" "Default should be false when flag absent"
fi

# Test 1.4: Flag appears in argument-hint YAML frontmatter
run_test
if grep -qE 'argument-hint:.*--blocking-only' "$COMMAND_FILE"; then
    pass_test "Flag in argument-hint frontmatter"
else
    fail_test "Flag in argument-hint frontmatter" "argument-hint should include --blocking-only"
fi

# Test 1.5: Flag has description explaining its purpose
run_test
if grep -A 3 '`--blocking-only`' "$COMMAND_FILE" | grep -qiE 'block|filter|only.*blocking'; then
    pass_test "Flag has descriptive purpose"
else
    fail_test "Flag has descriptive purpose" "Description should explain filtering to blocking gaps"
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

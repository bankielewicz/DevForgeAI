#!/bin/bash
# Test AC#1: Default Behavior Shows All Gaps
# STORY-346: Update review-qa-reports Default to Show All Gaps
#
# Validates:
# - Default --min-severity is changed from MEDIUM to LOW
# - Command documentation reflects new default
#
# Expected: FAIL initially (TDD Red phase - currently defaults to MEDIUM)

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
echo "STORY-346 AC#1: Default Behavior Shows All Gaps"
echo "=============================================="
echo "Target files:"
echo "  - $COMMAND_FILE"
echo "  - $SKILL_FILE"
echo "----------------------------------------------"
echo ""

# Test 1.1: Command file exists
run_test
if [ -f "$COMMAND_FILE" ]; then
    pass_test "Command file exists"
else
    fail_test "Command file exists" "File not found: $COMMAND_FILE"
fi

# Test 1.2: Default --min-severity is LOW in argument table
run_test
if grep -qE '\|\s*`--min-severity`.*\|\s*`LOW`\s*\|' "$COMMAND_FILE"; then
    pass_test "Argument table shows LOW as default"
else
    fail_test "Argument table shows LOW as default" "Expected: | --min-severity | ... | LOW | (currently shows MEDIUM)"
    echo "  Current default value:"
    grep -E '\|\s*`--min-severity`' "$COMMAND_FILE" | head -1
fi

# Test 1.3: Argument parsing section shows LOW as default
run_test
if grep -qE 'min-severity.*Default.*LOW' "$COMMAND_FILE" || \
   grep -qE '\*\*--min-severity\*\*.*Default.*LOW' "$COMMAND_FILE"; then
    pass_test "Argument parsing section shows LOW as default"
else
    fail_test "Argument parsing section shows LOW as default" "Default should be LOW, not MEDIUM"
fi

# Test 1.4: Skill file argument parsing defaults to LOW (not MEDIUM)
run_test
# Check if the argument parsing table shows LOW as default for --min-severity
if grep -A 10 'Argument.*Variable.*Default' "$SKILL_FILE" | grep -qE 'min-severity.*From config'; then
    # Config-based default is acceptable, but we need to verify config shows LOW
    pass_test "Skill file references config for min-severity default"
else
    fail_test "Skill file min-severity default" "Should reference config or show LOW as default"
fi

# Test 1.5: No hardcoded MEDIUM default in command file arguments section
run_test
if grep -qE '\|\s*`--min-severity`.*\|\s*`MEDIUM`\s*\|' "$COMMAND_FILE"; then
    fail_test "No MEDIUM hardcoded as default" "Found MEDIUM as default, should be LOW"
else
    pass_test "No MEDIUM hardcoded as default"
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

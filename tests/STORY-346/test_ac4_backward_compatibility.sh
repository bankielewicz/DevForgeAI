#!/bin/bash
# Test AC#4: Backward Compatibility with Existing Workflows
# STORY-346: Update review-qa-reports Default to Show All Gaps
#
# Validates:
# - Missing blocking field defaults to true (blocking)
# - Existing --min-severity flag continues to work
# - Legacy gaps.json parsing documented
#
# Expected: FAIL initially (TDD Red phase - backward compatibility not documented)

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
echo "STORY-346 AC#4: Backward Compatibility with Existing Workflows"
echo "=============================================="
echo "Target files:"
echo "  - $COMMAND_FILE"
echo "  - $SKILL_FILE"
echo "----------------------------------------------"
echo ""

# Test 4.1: Files exist
run_test
if [ -f "$COMMAND_FILE" ] && [ -f "$SKILL_FILE" ]; then
    pass_test "Required files exist"
else
    fail_test "Required files exist" "Missing command or skill file"
    exit 1
fi

# Test 4.2: Default blocking: true documented for missing field
run_test
if grep -qE 'missing.*blocking.*default.*true|blocking.*field.*missing.*true|default.*true.*blocking' "$SKILL_FILE"; then
    pass_test "Missing blocking field defaults to true documented in skill"
else
    fail_test "Missing blocking field defaults to true" "Skill should document default blocking: true for legacy files"
fi

# Test 4.3: Command file documents backward compatibility
run_test
if grep -qE 'Backward Compatibility|backward compatible|legacy' "$COMMAND_FILE"; then
    pass_test "Backward compatibility mentioned in command"
else
    fail_test "Backward compatibility mentioned in command" "Command should document backward compatibility"
fi

# Test 4.4: Existing --min-severity flag preserved
run_test
# Verify the --min-severity argument is still documented
if grep -qE '\-\-min-severity.*CRITICAL.*HIGH.*MEDIUM.*LOW' "$COMMAND_FILE"; then
    pass_test "Existing --min-severity flag preserved"
else
    fail_test "Existing --min-severity flag preserved" "Original severity filtering should remain"
fi

# Test 4.5: Skill documents legacy gap parsing behavior
run_test
if grep -qE 'Optional.*default.*true|without.*blocking.*field.*parse' "$SKILL_FILE"; then
    pass_test "Legacy gap parsing behavior documented"
else
    fail_test "Legacy gap parsing behavior documented" "Skill should document how legacy gaps without blocking field are handled"
fi

# Test 4.6: Error-free parsing of missing blocking field guaranteed
run_test
if grep -qE 'parse successfully|error-free|without errors' "$SKILL_FILE"; then
    pass_test "Error-free parsing guarantee documented"
else
    fail_test "Error-free parsing guarantee documented" "Should guarantee legacy files parse without errors"
fi

echo ""
echo "=============================================="
echo "Test Summary: $TESTS_PASSED/$TESTS_RUN passed"
echo "=============================================="

if [ "$TESTS_FAILED" -gt 0 ]; then
    echo "Status: FAILED ($TESTS_FAILED failures)"
    echo ""
    echo "TDD Red Phase: Expected failures - backward compatibility not fully documented"
    exit 1
else
    echo "Status: PASSED"
    exit 0
fi

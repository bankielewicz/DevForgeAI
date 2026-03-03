#!/bin/bash
###############################################################################
# Test Suite: STORY-177 - AC#3: History Entry After Verification
# Purpose: Verify Status History entry appended ONLY AFTER verification succeeds
# TDD Phase: RED (tests should FAIL until implementation)
###############################################################################

set -euo pipefail

QA_SKILL_FILE=".claude/skills/devforgeai-qa/SKILL.md"
TEST_COUNT=0
PASS_COUNT=0
FAIL_COUNT=0

pass_test() {
    PASS_COUNT=$((PASS_COUNT + 1))
    echo "  PASS: $1"
}

fail_test() {
    FAIL_COUNT=$((FAIL_COUNT + 1))
    echo "  FAIL: $1"
}

test_case() {
    TEST_COUNT=$((TEST_COUNT + 1))
    echo ""
    echo "Test $TEST_COUNT: $1"
}

header() {
    echo ""
    echo "================================================================"
    echo "$1"
    echo "================================================================"
}

echo "STORY-177 AC#3: History Entry After Verification"
echo "Target: $QA_SKILL_FILE"

# Check file exists
if [ ! -f "$QA_SKILL_FILE" ]; then
    echo ""
    echo "ERROR: QA skill file does not exist: $QA_SKILL_FILE"
    echo "All tests will FAIL."
    exit 1
fi

header "AC#3: Conditional History Append Validation"

test_case "History append is conditional on verification success"
# Look for conditional logic: IF verification succeeds THEN append history
if grep -qE "IF.*verif.*THEN.*history|IF.*succeed.*THEN.*append|only.*after.*verification" "$QA_SKILL_FILE" 2>/dev/null || \
   grep -qE "verification.*succeed.*history|ONLY.*AFTER.*verification" "$QA_SKILL_FILE" 2>/dev/null; then
    pass_test "Found conditional history append based on verification"
else
    fail_test "Missing conditional logic for history append after verification"
fi

test_case "Protocol explicitly states 'ONLY AFTER' verification"
if grep -qiE "only.*after.*verif|append.*only.*if.*verif|history.*only.*after" "$QA_SKILL_FILE" 2>/dev/null; then
    pass_test "Found 'ONLY AFTER verification' constraint"
else
    fail_test "Missing explicit 'ONLY AFTER verification' language"
fi

test_case "History append skipped if verification fails"
# Look for explicit skip/abort logic when verification fails
if grep -qE "IF.*fail.*skip.*history|IF.*fail.*no.*history|verification.*fail.*abort" "$QA_SKILL_FILE" 2>/dev/null || \
   grep -qE "do.*not.*append.*if.*fail|skip.*history.*on.*fail" "$QA_SKILL_FILE" 2>/dev/null; then
    pass_test "Found skip-on-failure logic for history append"
else
    fail_test "Missing skip logic when verification fails"
fi

test_case "Sequence documented: Edit YAML -> Verify -> Edit History"
# Check for explicit 3-step sequence documentation
if grep -qE "(1|step.*1).*yaml.*(2|step.*2).*verify.*(3|step.*3).*history" "$QA_SKILL_FILE" 2>/dev/null || \
   grep -qE "Edit.*status.*Grep.*verify.*Edit.*history|yaml.*first.*verify.*then.*history" "$QA_SKILL_FILE" 2>/dev/null; then
    pass_test "Found 3-step sequence documentation"
else
    fail_test "Missing explicit 3-step sequence (YAML -> Verify -> History)"
fi

test_case "History entry references Change Log table"
# Verify the history entry goes into the Change Log table
if grep -qE "Change.*Log.*entry|changelog.*append|append.*Change.*Log" "$QA_SKILL_FILE" 2>/dev/null; then
    pass_test "Found Change Log table reference for history entry"
else
    fail_test "Missing Change Log table reference for history entry"
fi

header "Summary"
echo ""
echo "Total Tests: $TEST_COUNT"
echo "Passed: $PASS_COUNT"
echo "Failed: $FAIL_COUNT"
echo ""

if [ $FAIL_COUNT -gt 0 ]; then
    echo "STATUS: RED PHASE - Tests failing as expected (TDD)"
    exit 1
else
    echo "STATUS: GREEN PHASE - All tests passing"
    exit 0
fi

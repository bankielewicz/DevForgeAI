#!/bin/bash
###############################################################################
# Test Suite: STORY-177 - AC#5: Rollback on Failure
# Purpose: Verify rollback restores original value, no history append on failure
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

echo "STORY-177 AC#5: Rollback on Failure"
echo "Target: $QA_SKILL_FILE"

# Check file exists
if [ ! -f "$QA_SKILL_FILE" ]; then
    echo ""
    echo "ERROR: QA skill file does not exist: $QA_SKILL_FILE"
    echo "All tests will FAIL."
    exit 1
fi

header "AC#5: Rollback Mechanism Validation"

test_case "Rollback mechanism documented"
# Look for rollback documentation
if grep -qiE "rollback.*mechanism|rollback.*on.*fail|restore.*original" "$QA_SKILL_FILE" 2>/dev/null; then
    pass_test "Found rollback mechanism documentation"
else
    fail_test "Missing rollback mechanism documentation"
fi

test_case "Original status value captured before Edit"
# Check for capturing original value before modification
if grep -qE "original.*status|capture.*current.*status|read.*current.*status|save.*original" "$QA_SKILL_FILE" 2>/dev/null || \
   grep -qE "store.*original|backup.*status|current.*status.*before" "$QA_SKILL_FILE" 2>/dev/null; then
    pass_test "Found original status capture step"
else
    fail_test "Missing step to capture original status value"
fi

test_case "Rollback restores original status on verification failure"
# Check for restore logic when verification fails
if grep -qE "IF.*verif.*fail.*restore|IF.*fail.*rollback|restore.*original.*if.*fail" "$QA_SKILL_FILE" 2>/dev/null || \
   grep -qE "rollback.*Edit.*original|Edit.*restore.*original" "$QA_SKILL_FILE" 2>/dev/null; then
    pass_test "Found rollback-on-failure logic"
else
    fail_test "Missing restore logic for verification failure"
fi

test_case "No history append on rollback"
# Check that history is not appended if rollback occurs
if grep -qE "no.*history.*append.*rollback|skip.*history.*on.*fail|rollback.*no.*history" "$QA_SKILL_FILE" 2>/dev/null || \
   grep -qE "history.*not.*append.*fail|abort.*history.*if.*fail" "$QA_SKILL_FILE" 2>/dev/null; then
    pass_test "Found no-history-on-rollback constraint"
else
    fail_test "Missing constraint: no history append on rollback"
fi

test_case "Rollback uses Edit to restore original value"
# Check for Edit command usage in rollback
if grep -qE "Edit.*rollback|Edit.*restore.*original|rollback.*Edit\(" "$QA_SKILL_FILE" 2>/dev/null; then
    pass_test "Found Edit-based rollback mechanism"
else
    fail_test "Missing Edit-based rollback implementation"
fi

test_case "Error handling/HALT on rollback scenario"
# Check for error handling when rollback occurs
if grep -qE "HALT.*rollback|rollback.*HALT|fail.*manual.*intervention" "$QA_SKILL_FILE" 2>/dev/null || \
   grep -qE "error.*rollback|rollback.*error.*handling" "$QA_SKILL_FILE" 2>/dev/null; then
    pass_test "Found error handling for rollback scenario"
else
    fail_test "Missing error handling when rollback is triggered"
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

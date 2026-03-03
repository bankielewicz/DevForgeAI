#!/bin/bash
###############################################################################
# Test Suite: STORY-177 - AC#4: Single Edit Sequence
# Purpose: Verify both updates in single Edit sequence when possible
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

echo "STORY-177 AC#4: Single Edit Sequence"
echo "Target: $QA_SKILL_FILE"

# Check file exists
if [ ! -f "$QA_SKILL_FILE" ]; then
    echo ""
    echo "ERROR: QA skill file does not exist: $QA_SKILL_FILE"
    echo "All tests will FAIL."
    exit 1
fi

header "AC#4: Single Edit Sequence Validation"

test_case "Single Edit sequence option documented"
# Look for documentation about combining edits when possible
if grep -qE "single.*Edit.*sequence|combine.*edit|atomic.*edit|one.*edit.*both" "$QA_SKILL_FILE" 2>/dev/null; then
    pass_test "Found single Edit sequence documentation"
else
    fail_test "Missing single Edit sequence option documentation"
fi

test_case "Conditions for single Edit sequence specified"
# Check for 'when possible' or conditions under which single edit applies
if grep -qE "when.*possible.*single|if.*both.*single|combine.*when" "$QA_SKILL_FILE" 2>/dev/null || \
   grep -qE "single.*edit.*when|possible.*combine.*edit" "$QA_SKILL_FILE" 2>/dev/null; then
    pass_test "Found conditions for single Edit sequence"
else
    fail_test "Missing conditions specification for single Edit sequence"
fi

test_case "Edit tool usage pattern includes both status and history"
# Check for Edit pattern that could update both
if grep -qE "Edit.*status.*history|new_string.*status.*changelog|Edit.*old_string.*new_string" "$QA_SKILL_FILE" 2>/dev/null; then
    pass_test "Found Edit pattern for combined update"
else
    fail_test "Missing Edit pattern that combines status and history update"
fi

test_case "Fallback to separate edits documented"
# Check for fallback when single edit isn't possible
if grep -qE "fallback.*separate|if.*not.*possible.*separate|two.*edit.*fallback" "$QA_SKILL_FILE" 2>/dev/null || \
   grep -qE "separate.*edit.*when|cannot.*combine" "$QA_SKILL_FILE" 2>/dev/null; then
    pass_test "Found fallback to separate edits documentation"
else
    fail_test "Missing fallback documentation for when single edit not possible"
fi

test_case "Optimization rationale documented (token efficiency)"
# Check for rationale about why single edit is preferred
if grep -qE "token.*effic|reduc.*edit|optim.*edit|fewer.*edit" "$QA_SKILL_FILE" 2>/dev/null || \
   grep -qE "single.*edit.*efficient|minimize.*edit" "$QA_SKILL_FILE" 2>/dev/null; then
    pass_test "Found optimization rationale for single Edit"
else
    fail_test "Missing optimization rationale for single Edit sequence"
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

#!/bin/bash
###############################################################################
# Test Suite: STORY-177 - AC#1: YAML Frontmatter Updated First
# Purpose: Verify QA skill updates YAML frontmatter status field FIRST
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

echo "STORY-177 AC#1: YAML Frontmatter Updated First"
echo "Target: $QA_SKILL_FILE"

# Check file exists
if [ ! -f "$QA_SKILL_FILE" ]; then
    echo ""
    echo "ERROR: QA skill file does not exist: $QA_SKILL_FILE"
    echo "All tests will FAIL."
    exit 1
fi

header "AC#1: YAML Frontmatter Update Order Validation"

test_case "Atomic Update Protocol section exists"
if grep -qiE "atomic.*update.*protocol|atomic.*status.*update" "$QA_SKILL_FILE" 2>/dev/null; then
    pass_test "Found Atomic Update Protocol reference"
else
    fail_test "Missing Atomic Update Protocol documentation"
fi

test_case "Protocol specifies YAML frontmatter updated FIRST"
# Look for explicit ordering that YAML is updated first
if grep -qE "(step.?1|first).*(yaml|frontmatter|status)" "$QA_SKILL_FILE" 2>/dev/null || \
   grep -qE "(yaml|frontmatter).*(first|step.?1)" "$QA_SKILL_FILE" 2>/dev/null; then
    pass_test "Found explicit YAML-first ordering"
else
    fail_test "Missing explicit YAML-first ordering specification"
fi

test_case "Edit command for YAML status precedes history append"
# Check that Edit for status: field comes before Edit for history/changelog
step34_content=$(sed -n '/### Step 3.4/,/### Step 3.5/p' "$QA_SKILL_FILE" 2>/dev/null || echo "")

if echo "$step34_content" | grep -qn 'old_string="status:' 2>/dev/null; then
    status_line=$(echo "$step34_content" | grep -n 'old_string="status:' 2>/dev/null | head -1 | cut -d: -f1)

    if echo "$step34_content" | grep -qn 'Change.*Log\|changelog\|history' 2>/dev/null; then
        history_line=$(echo "$step34_content" | grep -n 'Change.*Log\|changelog\|history' 2>/dev/null | head -1 | cut -d: -f1)

        if [ -n "$status_line" ] && [ -n "$history_line" ] && [ "$status_line" -lt "$history_line" ]; then
            pass_test "Status Edit precedes history append in Step 3.4"
        else
            fail_test "Status Edit does not precede history append (or order unclear)"
        fi
    else
        fail_test "Cannot verify order - history append not found in Step 3.4"
    fi
else
    fail_test "Cannot verify order - status Edit not found in Step 3.4"
fi

test_case "Protocol documents order explicitly (YAML first, then history)"
if grep -qE "(1|first).*status.*(2|then|after).*history" "$QA_SKILL_FILE" 2>/dev/null || \
   grep -qE "status.*before.*history|yaml.*before.*changelog" "$QA_SKILL_FILE" 2>/dev/null; then
    pass_test "Found explicit order documentation (YAML first, history second)"
else
    fail_test "Missing explicit order documentation for YAML-first protocol"
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

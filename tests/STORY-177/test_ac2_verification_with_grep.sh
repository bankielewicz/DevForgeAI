#!/bin/bash
###############################################################################
# Test Suite: STORY-177 - AC#2: Verification with Grep
# Purpose: Verify Grep verification confirms new status before proceeding
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

echo "STORY-177 AC#2: Verification with Grep"
echo "Target: $QA_SKILL_FILE"

# Check file exists
if [ ! -f "$QA_SKILL_FILE" ]; then
    echo ""
    echo "ERROR: QA skill file does not exist: $QA_SKILL_FILE"
    echo "All tests will FAIL."
    exit 1
fi

header "AC#2: Grep Verification Validation"

test_case "Grep verification step exists after YAML update"
# Look for Grep command after status update
if grep -qE "Grep.*status|grep.*verify|verify.*grep" "$QA_SKILL_FILE" 2>/dev/null; then
    pass_test "Found Grep verification reference"
else
    fail_test "Missing Grep verification after YAML update"
fi

test_case "Verification confirms new status value"
# Check for verification that checks the new status value
if grep -qE "Grep.*pattern.*status.*QA\s*(Approved|Failed)|verify.*new.*status" "$QA_SKILL_FILE" 2>/dev/null || \
   grep -qE "Grep.*QA Approved|Grep.*QA Failed" "$QA_SKILL_FILE" 2>/dev/null; then
    pass_test "Found verification of new status value"
else
    fail_test "Missing verification of new status value in YAML frontmatter"
fi

test_case "Verification step occurs BEFORE history append"
# Extract Step 3.4 and check order: status update -> grep verify -> history append
step34_content=$(sed -n '/### Step 3.4/,/### Step 3.5/p' "$QA_SKILL_FILE" 2>/dev/null || echo "")

# Look for sequence: Edit status -> Grep verify -> Edit history
if echo "$step34_content" | grep -qE "Grep\(|grep\(" 2>/dev/null; then
    grep_line=$(echo "$step34_content" | grep -nE "Grep\(|grep\(" 2>/dev/null | head -1 | cut -d: -f1)

    # Check if history append comes after grep
    if echo "$step34_content" | grep -qn "Change.*Log\|Append.*changelog\|history.*entry" 2>/dev/null; then
        history_line=$(echo "$step34_content" | grep -n "Change.*Log\|Append.*changelog\|history.*entry" 2>/dev/null | head -1 | cut -d: -f1)

        if [ -n "$grep_line" ] && [ -n "$history_line" ] && [ "$grep_line" -lt "$history_line" ]; then
            pass_test "Grep verification precedes history append"
        else
            fail_test "Grep verification does not precede history append"
        fi
    else
        fail_test "Cannot verify order - history append not found"
    fi
else
    fail_test "Grep verification step not found in Step 3.4"
fi

test_case "Verification is documented as MANDATORY"
if grep -qE "MANDATORY.*verify|verify.*MANDATORY|Verify.*\(MANDATORY\)" "$QA_SKILL_FILE" 2>/dev/null; then
    pass_test "Found MANDATORY verification documentation"
else
    fail_test "Verification step not documented as MANDATORY"
fi

test_case "Verification pattern matches YAML frontmatter status format"
# Check for pattern that matches ^status: <value>
if grep -qE "pattern.*\^status:|status:.*pattern|\^status:" "$QA_SKILL_FILE" 2>/dev/null || \
   grep -qE "Grep.*status:.*QA|verify.*status:.*QA" "$QA_SKILL_FILE" 2>/dev/null; then
    pass_test "Found YAML-specific status pattern"
else
    fail_test "Missing YAML frontmatter status pattern for verification"
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

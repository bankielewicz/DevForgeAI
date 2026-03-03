#!/bin/bash
###############################################################################
# Test Suite: STORY-177 - AC#6: Protocol Documented
# Purpose: Verify protocol is documented in Step 3.4 of SKILL.md
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

echo "STORY-177 AC#6: Protocol Documented"
echo "Target: $QA_SKILL_FILE"

# Check file exists
if [ ! -f "$QA_SKILL_FILE" ]; then
    echo ""
    echo "ERROR: QA skill file does not exist: $QA_SKILL_FILE"
    echo "All tests will FAIL."
    exit 1
fi

header "AC#6: Step 3.4 Protocol Documentation Validation"

test_case "Step 3.4 section exists"
if grep -q "### Step 3.4" "$QA_SKILL_FILE" 2>/dev/null; then
    pass_test "Found Step 3.4 section header"
else
    fail_test "Missing Step 3.4 section header"
fi

test_case "Atomic Update Protocol title in Step 3.4"
# Extract Step 3.4 content and check for atomic protocol title
step34_content=$(sed -n '/### Step 3.4/,/### Step 3.5/p' "$QA_SKILL_FILE" 2>/dev/null || echo "")

if echo "$step34_content" | grep -qiE "atomic.*update.*protocol|atomic.*status.*update" 2>/dev/null; then
    pass_test "Found Atomic Update Protocol title in Step 3.4"
else
    fail_test "Missing Atomic Update Protocol title in Step 3.4"
fi

test_case "Protocol documents 5-step sequence"
# Check for the 5 steps of the atomic update protocol
step_count=0

# Step 1: Read current status
if echo "$step34_content" | grep -qE "(1|step.?1).*read.*status|read.*current.*status" 2>/dev/null; then
    step_count=$((step_count + 1))
fi

# Step 2: Edit YAML frontmatter
if echo "$step34_content" | grep -qE "(2|step.?2).*edit.*yaml|edit.*frontmatter.*status" 2>/dev/null; then
    step_count=$((step_count + 1))
fi

# Step 3: Grep verify
if echo "$step34_content" | grep -qE "(3|step.?3).*grep.*verify|verify.*new.*status" 2>/dev/null; then
    step_count=$((step_count + 1))
fi

# Step 4: Edit append history
if echo "$step34_content" | grep -qE "(4|step.?4).*append.*history|edit.*append.*history" 2>/dev/null; then
    step_count=$((step_count + 1))
fi

# Step 5: Rollback
if echo "$step34_content" | grep -qE "(5|step.?5).*rollback|rollback.*restore" 2>/dev/null; then
    step_count=$((step_count + 1))
fi

if [ $step_count -ge 4 ]; then
    pass_test "Found at least 4/5 protocol steps documented"
else
    fail_test "Only $step_count/5 protocol steps documented (need at least 4)"
fi

test_case "Protocol includes numbered sequence or code block"
# Check for numbered list or code block with protocol
if echo "$step34_content" | grep -qE "^[0-9]+\.|^\`\`\`" 2>/dev/null || \
   echo "$step34_content" | grep -qE "Step 1:|Step 2:|Step 3:" 2>/dev/null; then
    pass_test "Found numbered sequence or code block in protocol"
else
    fail_test "Missing numbered sequence or code block for protocol steps"
fi

test_case "Protocol references story STORY-177"
if grep -q "STORY-177" "$QA_SKILL_FILE" 2>/dev/null; then
    pass_test "Found STORY-177 reference in SKILL.md"
else
    fail_test "Missing STORY-177 reference (traceability)"
fi

test_case "Validation checkpoint includes atomic update verification"
# Check for validation checkpoint mentioning atomic update
if grep -qE "Validation.*Checkpoint.*atomic|atomic.*update.*Validation" "$QA_SKILL_FILE" 2>/dev/null || \
   echo "$step34_content" | grep -qE "\[.*\].*status.*update|\[.*\].*verif" 2>/dev/null; then
    pass_test "Found atomic update in validation checkpoint"
else
    fail_test "Missing atomic update in validation checkpoint"
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

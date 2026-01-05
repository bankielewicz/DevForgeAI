#!/bin/bash

################################################################################
# Test: AC#1 - Recovery Action Identification
#
# Story: STORY-230 - Track Error Recovery Patterns
#
# Validates: session-miner can identify 4 recovery action types:
#   - retry: Same command executed again after error
#   - manual-fix: Different command to fix issue, then original retried
#   - skip: Different command/story executed without addressing error
#   - escalate: User interaction (AskUserQuestion) to get human input
#
# Test Approach: Check session-miner.md for Error Recovery Patterns section
# Expected: FAIL initially (section does not exist yet - TDD Red phase)
################################################################################

SESSION_MINER_FILE="/mnt/c/Projects/DevForgeAI2/src/claude/agents/session-miner.md"
TEST_NAME="AC#1 - Recovery Action Detection"

# Arrange: Verify file exists
if [ ! -f "$SESSION_MINER_FILE" ]; then
    echo "FAIL: [$TEST_NAME] File not found: $SESSION_MINER_FILE"
    exit 1
fi

echo "Testing: $TEST_NAME"
echo "File: $SESSION_MINER_FILE"
echo "---"

################################################################################
# Test 1: Error Recovery Patterns section exists
################################################################################
SECTION_HEADER=$(grep -n "Error Recovery Patterns" "$SESSION_MINER_FILE" | head -1)

if [ -z "$SECTION_HEADER" ]; then
    echo "FAIL: [$TEST_NAME] 'Error Recovery Patterns' section not found"
    echo "  Expected: ## Error Recovery Patterns (STORY-230) section header"
    echo "  Actual: Section does not exist"
    exit 1
fi

echo "PASS: Error Recovery Patterns section found at line $(echo $SECTION_HEADER | cut -d: -f1)"

################################################################################
# Test 2: RecoveryEntry data model defined
################################################################################
RECOVERY_ENTRY=$(grep -n "RecoveryEntry" "$SESSION_MINER_FILE")

if [ -z "$RECOVERY_ENTRY" ]; then
    echo "FAIL: [$TEST_NAME] RecoveryEntry data model not defined"
    echo "  Expected: Data Model: RecoveryEntry section"
    echo "  Actual: RecoveryEntry not found in file"
    exit 1
fi

echo "PASS: RecoveryEntry data model found"

################################################################################
# Test 3: All 4 recovery action types documented
################################################################################
RECOVERY_ACTIONS=("retry" "manual-fix" "skip" "escalate")
MISSING_ACTIONS=()

for action in "${RECOVERY_ACTIONS[@]}"; do
    # Case-insensitive search for each recovery action type
    ACTION_FOUND=$(grep -i "$action" "$SESSION_MINER_FILE" | grep -i "recovery\|action")
    if [ -z "$ACTION_FOUND" ]; then
        MISSING_ACTIONS+=("$action")
    fi
done

if [ ${#MISSING_ACTIONS[@]} -gt 0 ]; then
    echo "FAIL: [$TEST_NAME] Missing recovery action types: ${MISSING_ACTIONS[*]}"
    echo "  Expected: All 4 types documented (retry, manual-fix, skip, escalate)"
    echo "  Missing: ${MISSING_ACTIONS[*]}"
    exit 1
fi

echo "PASS: All 4 recovery action types documented"

################################################################################
# Test 4: Recovery action classification algorithm defined
################################################################################
CLASSIFICATION_ALGO=$(grep -n "classify_recovery_action\|Recovery Action Classification\|Classification Algorithm" "$SESSION_MINER_FILE")

if [ -z "$CLASSIFICATION_ALGO" ]; then
    echo "FAIL: [$TEST_NAME] Recovery action classification algorithm not defined"
    echo "  Expected: FUNCTION classify_recovery_action or Classification Algorithm section"
    echo "  Actual: No classification algorithm found"
    exit 1
fi

echo "PASS: Recovery action classification algorithm found"

################################################################################
# Test 5: Recovery action detection workflow defined
################################################################################
DETECTION_WORKFLOW=$(grep -n "AC#1\|Recovery Action Identification\|recovery_action.*type\|action_type" "$SESSION_MINER_FILE")

if [ -z "$DETECTION_WORKFLOW" ]; then
    echo "FAIL: [$TEST_NAME] AC#1 Recovery Action Identification workflow not defined"
    echo "  Expected: ### AC#1: Recovery Action Identification section"
    echo "  Actual: No workflow section found"
    exit 1
fi

echo "PASS: Recovery action identification workflow found"

################################################################################
# All assertions passed
################################################################################
echo "---"
echo "PASS: [$TEST_NAME] All 5 assertions passed"
echo "  1. Error Recovery Patterns section exists"
echo "  2. RecoveryEntry data model defined"
echo "  3. All 4 recovery action types documented"
echo "  4. Classification algorithm defined"
echo "  5. AC#1 workflow section exists"
exit 0

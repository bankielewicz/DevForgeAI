#!/bin/bash

################################################################################
# Test: AC#2 - Recovery Success Tracking
#
# Story: STORY-230 - Track Error Recovery Patterns
#
# Validates: session-miner tracks recovery success rates:
#   - Success rate calculation formula defined
#   - Per-action success rate aggregation
#   - Overall recovery success metrics
#
# Test Approach: Check session-miner.md for success rate calculation workflow
# Expected: FAIL initially (section does not exist yet - TDD Red phase)
################################################################################

SESSION_MINER_FILE="/mnt/c/Projects/DevForgeAI2/src/claude/agents/session-miner.md"
TEST_NAME="AC#2 - Recovery Success Tracking"

# Arrange: Verify file exists
if [ ! -f "$SESSION_MINER_FILE" ]; then
    echo "FAIL: [$TEST_NAME] File not found: $SESSION_MINER_FILE"
    exit 1
fi

echo "Testing: $TEST_NAME"
echo "File: $SESSION_MINER_FILE"
echo "---"

################################################################################
# Test 1: AC#2 section exists in session-miner.md
################################################################################
AC2_SECTION=$(grep -n "AC#2\|Recovery Success Tracking\|Success Rate Tracking" "$SESSION_MINER_FILE")

if [ -z "$AC2_SECTION" ]; then
    echo "FAIL: [$TEST_NAME] AC#2 Recovery Success Tracking section not found"
    echo "  Expected: ### AC#2: Recovery Success Tracking section"
    echo "  Actual: Section does not exist"
    exit 1
fi

echo "PASS: AC#2 Recovery Success Tracking section found"

################################################################################
# Test 2: Success rate calculation formula defined
################################################################################
SUCCESS_FORMULA=$(grep -n "success_rate\|success rate.*=\|successful.*attempts\|recovery_success" "$SESSION_MINER_FILE")

if [ -z "$SUCCESS_FORMULA" ]; then
    echo "FAIL: [$TEST_NAME] Success rate calculation formula not defined"
    echo "  Expected: success_rate = successful_recoveries / total_attempts"
    echo "  Actual: No formula found"
    exit 1
fi

echo "PASS: Success rate calculation formula found"

################################################################################
# Test 3: Per-action success rate aggregation defined
################################################################################
PER_ACTION_RATE=$(grep -n "per.*action\|action.*rate\|rate.*by.*action\|action_success_rates" "$SESSION_MINER_FILE")

if [ -z "$PER_ACTION_RATE" ]; then
    echo "FAIL: [$TEST_NAME] Per-action success rate aggregation not defined"
    echo "  Expected: Success rate calculated for each action type (retry, manual-fix, skip, escalate)"
    echo "  Actual: No per-action aggregation found"
    exit 1
fi

echo "PASS: Per-action success rate aggregation found"

################################################################################
# Test 4: RecoveryEntry includes success tracking fields
################################################################################
RECOVERY_SUCCESS_FIELDS=$(grep -A 30 "RecoveryEntry" "$SESSION_MINER_FILE" | grep -i "success\|successful\|recovered")

if [ -z "$RECOVERY_SUCCESS_FIELDS" ]; then
    echo "FAIL: [$TEST_NAME] RecoveryEntry missing success tracking fields"
    echo "  Expected: Fields like 'recovery_successful', 'next_attempt_succeeded', or 'recovered'"
    echo "  Actual: No success tracking fields in RecoveryEntry"
    exit 1
fi

echo "PASS: RecoveryEntry includes success tracking fields"

################################################################################
# Test 5: Success determination logic defined
################################################################################
SUCCESS_LOGIC=$(grep -n "next.*attempt\|subsequent.*command\|recovery.*success.*when\|FUNCTION.*determine.*success" "$SESSION_MINER_FILE")

if [ -z "$SUCCESS_LOGIC" ]; then
    echo "FAIL: [$TEST_NAME] Success determination logic not defined"
    echo "  Expected: Logic for determining if recovery action succeeded (next attempt succeeded)"
    echo "  Actual: No success determination logic found"
    exit 1
fi

echo "PASS: Success determination logic found"

################################################################################
# Test 6: Recovery metrics output structure defined
################################################################################
METRICS_OUTPUT=$(grep -n "recovery_metrics\|RecoveryMetrics\|success_rate.*output\|recovery.*report" "$SESSION_MINER_FILE")

if [ -z "$METRICS_OUTPUT" ]; then
    echo "FAIL: [$TEST_NAME] Recovery metrics output structure not defined"
    echo "  Expected: Output structure showing success rates and recovery metrics"
    echo "  Actual: No metrics output structure found"
    exit 1
fi

echo "PASS: Recovery metrics output structure found"

################################################################################
# All assertions passed
################################################################################
echo "---"
echo "PASS: [$TEST_NAME] All 6 assertions passed"
echo "  1. AC#2 Recovery Success Tracking section exists"
echo "  2. Success rate calculation formula defined"
echo "  3. Per-action success rate aggregation defined"
echo "  4. RecoveryEntry includes success tracking fields"
echo "  5. Success determination logic defined"
echo "  6. Recovery metrics output structure defined"
exit 0

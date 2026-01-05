#!/bin/bash

################################################################################
# Test: AC#3 - Best Recovery Per Error Type
#
# Story: STORY-230 - Track Error Recovery Patterns
#
# Validates: session-miner correlates recovery patterns with error categories:
#   - Error category to recovery action mapping
#   - Most effective recovery action per error category
#   - Effectiveness ranking based on success rates
#
# Test Approach: Check session-miner.md for error-recovery correlation section
# Expected: FAIL initially (section does not exist yet - TDD Red phase)
################################################################################

SESSION_MINER_FILE="/mnt/c/Projects/DevForgeAI2/src/claude/agents/session-miner.md"
TEST_NAME="AC#3 - Best Recovery Per Error Type"

# Arrange: Verify file exists
if [ ! -f "$SESSION_MINER_FILE" ]; then
    echo "FAIL: [$TEST_NAME] File not found: $SESSION_MINER_FILE"
    exit 1
fi

echo "Testing: $TEST_NAME"
echo "File: $SESSION_MINER_FILE"
echo "---"

################################################################################
# Test 1: AC#3 section exists in session-miner.md
################################################################################
AC3_SECTION=$(grep -n "AC#3\|Best Recovery.*Error\|Error.*Recovery.*Correlation\|Recovery.*Error.*Type" "$SESSION_MINER_FILE")

if [ -z "$AC3_SECTION" ]; then
    echo "FAIL: [$TEST_NAME] AC#3 Best Recovery Per Error Type section not found"
    echo "  Expected: ### AC#3: Best Recovery Per Error Type section"
    echo "  Actual: Section does not exist"
    exit 1
fi

echo "PASS: AC#3 Best Recovery Per Error Type section found"

################################################################################
# Test 2: Error category to recovery action correlation defined
################################################################################
CORRELATION=$(grep -n "error.*category.*recovery\|category.*action.*correlation\|correlate.*error.*recovery\|error_recovery_correlation" "$SESSION_MINER_FILE")

if [ -z "$CORRELATION" ]; then
    echo "FAIL: [$TEST_NAME] Error-recovery correlation not defined"
    echo "  Expected: Mapping between error categories (api, timeout, validation, etc.) and recovery actions"
    echo "  Actual: No correlation mapping found"
    exit 1
fi

echo "PASS: Error-recovery correlation defined"

################################################################################
# Test 3: Error categories from STORY-229 referenced
################################################################################
# STORY-229 defined 6 error categories: api, validation, timeout, context-overflow, file-not-found, other
ERROR_CATEGORIES=("api" "timeout" "validation" "file-not-found" "context-overflow" "other")
FOUND_CATEGORIES=0

for category in "${ERROR_CATEGORIES[@]}"; do
    CATEGORY_FOUND=$(grep -i "$category" "$SESSION_MINER_FILE" | grep -i "error\|category")
    if [ -n "$CATEGORY_FOUND" ]; then
        FOUND_CATEGORIES=$((FOUND_CATEGORIES + 1))
    fi
done

# At least 4 of 6 categories should be referenced in error-recovery context
if [ $FOUND_CATEGORIES -lt 4 ]; then
    echo "FAIL: [$TEST_NAME] Insufficient error categories referenced"
    echo "  Expected: At least 4 of 6 error categories (api, timeout, validation, file-not-found, context-overflow, other)"
    echo "  Actual: Found $FOUND_CATEGORIES categories"
    exit 1
fi

echo "PASS: Error categories from STORY-229 referenced ($FOUND_CATEGORIES/6)"

################################################################################
# Test 4: Best recovery action determination logic defined
################################################################################
BEST_RECOVERY=$(grep -n "best.*recovery\|most.*effective\|recommended.*action\|optimal.*recovery\|effectiveness.*ranking" "$SESSION_MINER_FILE")

if [ -z "$BEST_RECOVERY" ]; then
    echo "FAIL: [$TEST_NAME] Best recovery action determination logic not defined"
    echo "  Expected: Logic for identifying most effective recovery action per error category"
    echo "  Actual: No best recovery determination found"
    exit 1
fi

echo "PASS: Best recovery action determination logic found"

################################################################################
# Test 5: Effectiveness ranking based on success rates
################################################################################
EFFECTIVENESS_RANKING=$(grep -n "rank.*effectiveness\|effectiveness.*score\|success.*rate.*rank\|recovery.*effectiveness\|sort.*success" "$SESSION_MINER_FILE")

if [ -z "$EFFECTIVENESS_RANKING" ]; then
    echo "FAIL: [$TEST_NAME] Effectiveness ranking not defined"
    echo "  Expected: Ranking of recovery actions by success rate per error category"
    echo "  Actual: No effectiveness ranking found"
    exit 1
fi

echo "PASS: Effectiveness ranking based on success rates found"

################################################################################
# Test 6: Error-Recovery correlation output structure defined
################################################################################
CORRELATION_OUTPUT=$(grep -n "error_recovery_recommendations\|best_actions_by_category\|correlation.*output\|recovery.*recommendations" "$SESSION_MINER_FILE")

if [ -z "$CORRELATION_OUTPUT" ]; then
    echo "FAIL: [$TEST_NAME] Error-recovery correlation output structure not defined"
    echo "  Expected: Output showing best recovery action per error category with success rates"
    echo "  Actual: No correlation output structure found"
    exit 1
fi

echo "PASS: Error-recovery correlation output structure found"

################################################################################
# Test 7: Integration with Error Categorization (STORY-229)
################################################################################
STORY_229_INTEGRATION=$(grep -n "STORY-229\|Error Categorization\|ErrorEntry\|error.*category" "$SESSION_MINER_FILE")

if [ -z "$STORY_229_INTEGRATION" ]; then
    echo "FAIL: [$TEST_NAME] Integration with STORY-229 Error Categorization not found"
    echo "  Expected: Reference to STORY-229 or ErrorEntry from Error Categorization"
    echo "  Actual: No STORY-229 integration found"
    exit 1
fi

echo "PASS: Integration with STORY-229 Error Categorization found"

################################################################################
# All assertions passed
################################################################################
echo "---"
echo "PASS: [$TEST_NAME] All 7 assertions passed"
echo "  1. AC#3 Best Recovery Per Error Type section exists"
echo "  2. Error-recovery correlation defined"
echo "  3. Error categories from STORY-229 referenced"
echo "  4. Best recovery action determination logic defined"
echo "  5. Effectiveness ranking based on success rates"
echo "  6. Error-recovery correlation output structure defined"
echo "  7. Integration with STORY-229 Error Categorization"
exit 0

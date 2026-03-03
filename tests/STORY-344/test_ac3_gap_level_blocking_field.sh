#!/bin/bash
# Test AC#3: Gap-level blocking: boolean field in each gap entry
# Story: STORY-344 - Extend gaps.json Schema with Blocking Field
# Expected: FAIL (RED phase - blocking field not in gap entries)

set -e

TARGET_FILE=".claude/skills/devforgeai-qa/references/report-generation.md"

echo "=== AC#3 Test: Gap-level blocking Field ==="
echo "Target: $TARGET_FILE"
echo ""

# Test 3.1: Check for blocking field in coverage_gaps schema
echo "Test 3.1: Checking for 'blocking' field in gap entry schema..."
if grep -B 5 -A 15 "coverage_gaps" "$TARGET_FILE" | grep -E "\"blocking\":\s*(true|false)" > /dev/null 2>&1; then
    echo "PASS: 'blocking' field found in coverage_gaps schema"
    RESULT_3_1=0
else
    echo "FAIL: 'blocking' field NOT found in coverage_gaps schema"
    RESULT_3_1=1
fi

# Test 3.2: Check for blocking field in anti_pattern_violations schema
echo ""
echo "Test 3.2: Checking for 'blocking' in anti_pattern_violations schema..."
if grep -B 5 -A 15 "anti_pattern_violations" "$TARGET_FILE" | grep -E "\"blocking\":\s*(true|false)" > /dev/null 2>&1; then
    echo "PASS: 'blocking' field found in anti_pattern_violations schema"
    RESULT_3_2=0
else
    echo "FAIL: 'blocking' field NOT found in anti_pattern_violations schema"
    RESULT_3_2=1
fi

# Test 3.3: Check for CRITICAL/HIGH = blocking: true documentation
echo ""
echo "Test 3.3: Checking CRITICAL/HIGH = blocking: true rule..."
if grep -iE "CRITICAL.*blocking.*true|HIGH.*blocking.*true|blocking.*true.*CRITICAL|blocking.*true.*HIGH" "$TARGET_FILE" > /dev/null 2>&1; then
    echo "PASS: CRITICAL/HIGH = blocking: true rule documented"
    RESULT_3_3=0
else
    echo "FAIL: CRITICAL/HIGH = blocking: true rule NOT documented"
    RESULT_3_3=1
fi

# Test 3.4: Check for MEDIUM/LOW can be blocking: false documentation
echo ""
echo "Test 3.4: Checking MEDIUM/LOW = blocking: false rule..."
if grep -iE "MEDIUM.*blocking.*false|LOW.*blocking.*false|blocking.*false.*MEDIUM|blocking.*false.*LOW" "$TARGET_FILE" > /dev/null 2>&1; then
    echo "PASS: MEDIUM/LOW = blocking: false rule documented"
    RESULT_3_4=0
else
    echo "FAIL: MEDIUM/LOW = blocking: false rule NOT documented"
    RESULT_3_4=1
fi

# Test 3.5: Check for blocking field in JSON example
echo ""
echo "Test 3.5: Checking for 'blocking' in JSON example..."
if grep -A 50 '```json' "$TARGET_FILE" | grep -E "\"blocking\":" > /dev/null 2>&1; then
    echo "PASS: 'blocking' field found in JSON example"
    RESULT_3_5=0
else
    echo "FAIL: 'blocking' field NOT in JSON example"
    RESULT_3_5=1
fi

echo ""
echo "=== AC#3 Summary ==="
TOTAL_PASS=$((5 - RESULT_3_1 - RESULT_3_2 - RESULT_3_3 - RESULT_3_4 - RESULT_3_5))
echo "Tests passed: $TOTAL_PASS/5"

if [ $RESULT_3_1 -ne 0 ] || [ $RESULT_3_2 -ne 0 ] || [ $RESULT_3_3 -ne 0 ] || [ $RESULT_3_4 -ne 0 ] || [ $RESULT_3_5 -ne 0 ]; then
    echo "STATUS: FAIL (expected in RED phase)"
    exit 1
else
    echo "STATUS: PASS"
    exit 0
fi

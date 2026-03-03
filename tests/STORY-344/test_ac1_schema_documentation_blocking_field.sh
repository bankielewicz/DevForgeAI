#!/bin/bash
# Test AC#1: Schema documentation includes blocking: boolean field
# Story: STORY-344 - Extend gaps.json Schema with Blocking Field
# Expected: FAIL (RED phase - field not yet documented)

set -e

TARGET_FILE=".claude/skills/devforgeai-qa/references/report-generation.md"

echo "=== AC#1 Test: Schema Documentation - blocking field ==="
echo "Target: $TARGET_FILE"
echo ""

# Test 1.1: Check for 'blocking: boolean' or 'blocking": true/false' in schema documentation
echo "Test 1.1: Checking for 'blocking' field documentation..."
if grep -E "\"blocking\":\s*(true|false)|blocking:\s*boolean|blocking:\s*(true|false)" "$TARGET_FILE" > /dev/null 2>&1; then
    echo "PASS: 'blocking' field found in schema documentation"
    RESULT_1_1=0
else
    echo "FAIL: 'blocking' field NOT found in schema documentation"
    RESULT_1_1=1
fi

# Test 1.2: Check for blocking field default behavior documentation
echo ""
echo "Test 1.2: Checking for default behavior documentation (blocking: true)..."
if grep -iE "default.*blocking.*true|blocking.*default.*true" "$TARGET_FILE" > /dev/null 2>&1; then
    echo "PASS: Default blocking behavior documented"
    RESULT_1_2=0
else
    echo "FAIL: Default blocking behavior NOT documented"
    RESULT_1_2=1
fi

# Test 1.3: Check for qa_result enum documentation in schema
echo ""
echo "Test 1.3: Checking for qa_result enum values (FAILED/PASS WITH WARNINGS/PASSED)..."
if grep -E "qa_result.*FAILED.*PASS WITH WARNINGS.*PASSED|\"qa_result\".*enum" "$TARGET_FILE" > /dev/null 2>&1; then
    echo "PASS: qa_result enum documented with all values"
    RESULT_1_3=0
else
    echo "FAIL: qa_result enum NOT fully documented"
    RESULT_1_3=1
fi

echo ""
echo "=== AC#1 Summary ==="
TOTAL_PASS=$((3 - RESULT_1_1 - RESULT_1_2 - RESULT_1_3))
echo "Tests passed: $TOTAL_PASS/3"

if [ $RESULT_1_1 -ne 0 ] || [ $RESULT_1_2 -ne 0 ] || [ $RESULT_1_3 -ne 0 ]; then
    echo "STATUS: FAIL (expected in RED phase)"
    exit 1
else
    echo "STATUS: PASS"
    exit 0
fi

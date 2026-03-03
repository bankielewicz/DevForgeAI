#!/bin/bash
# Test AC#2: Root-level qa_result field added to gaps.json schema
# Story: STORY-344 - Extend gaps.json Schema with Blocking Field
# Expected: FAIL (RED phase - field not fully documented)

set -e

TARGET_FILE_1=".claude/skills/devforgeai-qa/references/report-generation.md"
TARGET_FILE_2=".claude/skills/devforgeai-qa/references/deep-validation-workflow.md"

echo "=== AC#2 Test: Root-level qa_result Field ==="
echo "Target 1: $TARGET_FILE_1"
echo "Target 2: $TARGET_FILE_2"
echo ""

# Test 2.1: Check for qa_result at root level in report-generation.md schema
echo "Test 2.1: Checking qa_result at root level in report-generation.md..."
if grep -E "\"qa_result\":\s*\"(FAILED|PASSED|PASS WITH WARNINGS)\"" "$TARGET_FILE_1" > /dev/null 2>&1; then
    echo "PASS: qa_result field found at root level in report-generation.md"
    RESULT_2_1=0
else
    echo "FAIL: qa_result field NOT at root level or missing in report-generation.md"
    RESULT_2_1=1
fi

# Test 2.2: Check for qa_result enum values documentation
echo ""
echo "Test 2.2: Checking qa_result enum values are documented..."
ENUM_COUNT=$(grep -oE "(FAILED|PASS WITH WARNINGS|PASSED)" "$TARGET_FILE_1" | sort -u | wc -l)
if [ "$ENUM_COUNT" -ge 3 ]; then
    echo "PASS: All 3 qa_result enum values found"
    RESULT_2_2=0
else
    echo "FAIL: Not all qa_result enum values documented (found $ENUM_COUNT/3)"
    RESULT_2_2=1
fi

# Test 2.3: Check for qa_result field in deep-validation-workflow.md
echo ""
echo "Test 2.3: Checking qa_result documentation in deep-validation-workflow.md..."
if grep -E "qa_result.*FAILED|qa_result.*PASSED|\"qa_result\"" "$TARGET_FILE_2" > /dev/null 2>&1; then
    echo "PASS: qa_result field referenced in deep-validation-workflow.md"
    RESULT_2_3=0
else
    echo "FAIL: qa_result field NOT referenced in deep-validation-workflow.md"
    RESULT_2_3=1
fi

# Test 2.4: Verify qa_result is part of the gaps.json schema section
echo ""
echo "Test 2.4: Checking qa_result is in gaps.json schema section..."
if grep -A 20 "gaps.json Schema" "$TARGET_FILE_1" | grep -E "qa_result" > /dev/null 2>&1; then
    echo "PASS: qa_result is in gaps.json Schema section"
    RESULT_2_4=0
else
    echo "FAIL: qa_result NOT in gaps.json Schema section"
    RESULT_2_4=1
fi

echo ""
echo "=== AC#2 Summary ==="
TOTAL_PASS=$((4 - RESULT_2_1 - RESULT_2_2 - RESULT_2_3 - RESULT_2_4))
echo "Tests passed: $TOTAL_PASS/4"

if [ $RESULT_2_1 -ne 0 ] || [ $RESULT_2_2 -ne 0 ] || [ $RESULT_2_3 -ne 0 ] || [ $RESULT_2_4 -ne 0 ]; then
    echo "STATUS: FAIL (expected in RED phase)"
    exit 1
else
    echo "STATUS: PASS"
    exit 0
fi

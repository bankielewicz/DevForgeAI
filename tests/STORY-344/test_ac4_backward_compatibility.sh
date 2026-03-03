#!/bin/bash
# Test AC#4: Backward Compatibility - missing blocking field defaults to true
# Story: STORY-344 - Extend gaps.json Schema with Blocking Field
# Expected: FAIL (RED phase - backward compatibility not documented)

set -e

TARGET_FILE_1=".claude/skills/devforgeai-qa-remediation/SKILL.md"
TARGET_FILE_2=".claude/commands/review-qa-reports.md"

echo "=== AC#4 Test: Backward Compatibility ==="
echo "Target 1: $TARGET_FILE_1"
echo "Target 2: $TARGET_FILE_2"
echo ""

# Test 4.1: Check for default blocking behavior documentation in qa-remediation SKILL.md
echo "Test 4.1: Checking default blocking behavior in qa-remediation SKILL.md..."
if grep -iE "missing.*blocking.*default.*true|blocking.*not.*present.*assume.*true|default.*blocking.*true" "$TARGET_FILE_1" > /dev/null 2>&1; then
    echo "PASS: Default blocking behavior documented in qa-remediation SKILL.md"
    RESULT_4_1=0
else
    echo "FAIL: Default blocking behavior NOT documented in qa-remediation SKILL.md"
    RESULT_4_1=1
fi

# Test 4.2: Check for backward compatibility statement in qa-remediation SKILL.md
echo ""
echo "Test 4.2: Checking backward compatibility statement in qa-remediation SKILL.md..."
if grep -iE "backward.*compat.*blocking|existing.*gaps.*json.*parse|legacy.*gaps" "$TARGET_FILE_1" > /dev/null 2>&1; then
    echo "PASS: Backward compatibility statement found"
    RESULT_4_2=0
else
    echo "FAIL: Backward compatibility statement NOT found"
    RESULT_4_2=1
fi

# Test 4.3: Check for blocking field handling in review-qa-reports.md
echo ""
echo "Test 4.3: Checking blocking field reference in review-qa-reports.md..."
if grep -iE "blocking|severity.*filter" "$TARGET_FILE_2" > /dev/null 2>&1; then
    echo "PASS: blocking/severity handling referenced in review-qa-reports.md"
    RESULT_4_3=0
else
    echo "FAIL: blocking/severity handling NOT referenced in review-qa-reports.md"
    RESULT_4_3=1
fi

# Test 4.4: Check for error-free parsing documentation
echo ""
echo "Test 4.4: Checking error-free parsing documentation..."
if grep -iE "existing.*gaps.*json.*error|parse.*without.*error|backward.*compat.*error" "$TARGET_FILE_1" > /dev/null 2>&1; then
    echo "PASS: Error-free parsing documentation found"
    RESULT_4_4=0
else
    echo "FAIL: Error-free parsing documentation NOT found"
    RESULT_4_4=1
fi

echo ""
echo "=== AC#4 Summary ==="
TOTAL_PASS=$((4 - RESULT_4_1 - RESULT_4_2 - RESULT_4_3 - RESULT_4_4))
echo "Tests passed: $TOTAL_PASS/4"

if [ $RESULT_4_1 -ne 0 ] || [ $RESULT_4_2 -ne 0 ] || [ $RESULT_4_3 -ne 0 ] || [ $RESULT_4_4 -ne 0 ]; then
    echo "STATUS: FAIL (expected in RED phase)"
    exit 1
else
    echo "STATUS: PASS"
    exit 0
fi

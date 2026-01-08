#!/bin/bash
# STORY-191 AC-4: Context Hint Uses Section Header
# Tests that section header (not line numbers) is specified

# set -e  # Disabled: ((VAR++)) returns 1 when VAR=0
TARGET="/mnt/c/Projects/DevForgeAI2/devforgeai/specs/context/coding-standards.md"
PASS=0
FAIL=0

echo "=== STORY-191 AC-4: Section Header Hint ==="

# Test 1: Section header mentioned for context hint
if grep -qE "actual section header" "$TARGET"; then
    echo "PASS: Section header specified for context hint"
    ((PASS++))
else
    echo "FAIL: Missing 'actual section header' specification"
    ((FAIL++))
fi

# Test 2: Not line numbers (negative test - line numbers should NOT be required)
if grep -qE "not line numbers" "$TARGET" || ! grep -qE "lines [0-9]+-[0-9]+" "$TARGET"; then
    echo "PASS: Line numbers not required for context hints"
    ((PASS++))
else
    echo "FAIL: Should specify section headers, not line numbers"
    ((FAIL++))
fi

echo ""
echo "Results: $PASS passed, $FAIL failed"
exit $FAIL

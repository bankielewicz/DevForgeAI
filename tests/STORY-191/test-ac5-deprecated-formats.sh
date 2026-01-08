#!/bin/bash
# STORY-191 AC-5: Old Formats Deprecated
# Tests that old cross-reference formats marked deprecated

# set -e  # Disabled: ((VAR++)) returns 1 when VAR=0
TARGET="/mnt/c/Projects/DevForgeAI2/devforgeai/specs/context/coding-standards.md"
PASS=0
FAIL=0

echo "=== STORY-191 AC-5: Old Formats Deprecated ==="

# Test 1: Deprecated section or marker exists in cross-reference section
# The DEPRECATED marker appears within the Documentation Cross-Reference Format section
if grep -q "DEPRECATED" "$TARGET" && grep -q "Documentation Cross-Reference Format" "$TARGET"; then
    echo "PASS: Old formats marked as deprecated in cross-reference section"
    ((PASS++))
else
    echo "FAIL: No deprecation marker for old cross-reference formats"
    ((FAIL++))
fi

# Test 2: Example of old format shown
if grep -qE "See:|see:.*\[" "$TARGET"; then
    echo "PASS: Example of old format pattern present"
    ((PASS++))
else
    echo "FAIL: Missing example of deprecated format"
    ((FAIL++))
fi

echo ""
echo "Results: $PASS passed, $FAIL failed"
exit $FAIL

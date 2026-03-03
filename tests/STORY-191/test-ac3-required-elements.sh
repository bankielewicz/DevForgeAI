#!/bin/bash
# STORY-191 AC-3: Required Elements Documented
# Tests intro phrase, markdown link, context hint elements

# set -e  # Disabled: ((VAR++)) returns 1 when VAR=0
TARGET="/mnt/c/Projects/DevForgeAI2/devforgeai/specs/context/coding-standards.md"
PASS=0
FAIL=0

echo "=== STORY-191 AC-3: Required Elements ==="

# Test 1: Introductory phrase element
if grep -qE "Introductory phrase" "$TARGET"; then
    echo "PASS: Introductory phrase element documented"
    ((PASS++))
else
    echo "FAIL: Missing 'Introductory phrase' element"
    ((FAIL++))
fi

# Test 2: Markdown link element
if grep -qE "Markdown link" "$TARGET"; then
    echo "PASS: Markdown link element documented"
    ((PASS++))
else
    echo "FAIL: Missing 'Markdown link' element"
    ((FAIL++))
fi

# Test 3: Context hint element
if grep -qE "Context hint" "$TARGET"; then
    echo "PASS: Context hint element documented"
    ((PASS++))
else
    echo "FAIL: Missing 'Context hint' element"
    ((FAIL++))
fi

echo ""
echo "Results: $PASS passed, $FAIL failed"
exit $FAIL

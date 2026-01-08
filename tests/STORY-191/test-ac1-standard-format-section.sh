#!/bin/bash
# STORY-191 AC-1: Standard Format Section Defined
# Tests that coding-standards.md contains cross-reference format section

TARGET="/mnt/c/Projects/DevForgeAI2/devforgeai/specs/context/coding-standards.md"
PASS=0
FAIL=0

echo "=== STORY-191 AC-1: Standard Format Section ==="

# Test 1: Section header exists
if grep -qE "^## Documentation Cross-Reference Format" "$TARGET"; then
    echo "PASS: Cross-reference format section header exists"
    ((PASS++))
else
    echo "FAIL: Missing '## Documentation Cross-Reference Format' section"
    ((FAIL++))
fi

# Test 2: Section marked as LOCKED
if grep -qE "Cross-Reference Format.*LOCKED" "$TARGET"; then
    echo "PASS: Section marked as LOCKED"
    ((PASS++))
else
    echo "FAIL: Section not marked as LOCKED"
    ((FAIL++))
fi

echo ""
echo "Results: $PASS passed, $FAIL failed"
exit $FAIL

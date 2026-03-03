#!/bin/bash
# STORY-191 AC-2: Format Specification
# Tests format: `For full details, see: [filename.md](filename.md) (Section Name)`

# set -e  # Disabled: ((VAR++)) returns 1 when VAR=0
TARGET="/mnt/c/Projects/DevForgeAI2/devforgeai/specs/context/coding-standards.md"
PASS=0
FAIL=0

echo "=== STORY-191 AC-2: Format Specification ==="

# Test 1: Standard format pattern documented
if grep -qE "For full details, see:" "$TARGET"; then
    echo "PASS: Standard intro phrase documented"
    ((PASS++))
else
    echo "FAIL: Missing 'For full details, see:' pattern"
    ((FAIL++))
fi

# Test 2: Markdown link pattern shown
if grep -qE "\[filename\.md\]\(filename\.md\)" "$TARGET"; then
    echo "PASS: Markdown link pattern documented"
    ((PASS++))
else
    echo "FAIL: Missing markdown link pattern [filename.md](filename.md)"
    ((FAIL++))
fi

# Test 3: Section name parentheses pattern
if grep -qE "\(Section Name\)" "$TARGET"; then
    echo "PASS: Section name hint pattern documented"
    ((PASS++))
else
    echo "FAIL: Missing (Section Name) pattern"
    ((FAIL++))
fi

echo ""
echo "Results: $PASS passed, $FAIL failed"
exit $FAIL

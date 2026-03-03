#!/bin/bash
# STORY-357 AC#5: source-tree.md Version and Metadata Updated
# TDD Red Phase - These tests MUST FAIL before implementation
#
# Business Rules Tested:
#   BR-001: LOCKED status marker must remain unchanged
#   BR-002: Existing tree diagram entries must not be modified (only additions)

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

SOURCE_TREE="$PROJECT_ROOT/devforgeai/specs/context/source-tree.md"

echo "=== AC#5: Version and Metadata Updated ==="
echo "Target file: $SOURCE_TREE"
echo ""

PASS=0
FAIL=0
TOTAL=7

# Test 5.1: Version incremented to 3.6
echo -n "Test 5.1: Version incremented to 3.6... "
if grep -qE '^[*]*Version[*]*:.*3\.6' "$SOURCE_TREE" 2>/dev/null; then
    echo "PASS"
    PASS=$((PASS + 1))
else
    echo "FAIL - Version is not 3.6 (current version likely still 3.5)"
    FAIL=$((FAIL + 1))
fi

# Test 5.2: Version line changelog note includes ADR-013
echo -n "Test 5.2: Version changelog note includes ADR-013... "
if grep -iE '^[*]*Version[*]*:.*ADR-013' "$SOURCE_TREE" 2>/dev/null; then
    echo "PASS"
    PASS=$((PASS + 1))
else
    echo "FAIL - Version line does not reference ADR-013"
    FAIL=$((FAIL + 1))
fi

# Test 5.3: Version line changelog note includes STORY-357
echo -n "Test 5.3: Version changelog note includes STORY-357... "
if grep -iE '^[*]*Version[*]*:.*STORY-357' "$SOURCE_TREE" 2>/dev/null; then
    echo "PASS"
    PASS=$((PASS + 1))
else
    echo "FAIL - Version line does not reference STORY-357"
    FAIL=$((FAIL + 1))
fi

# Test 5.4: Version changelog note mentions .treelint/
echo -n "Test 5.4: Version changelog note mentions .treelint/... "
if grep -iE '^[*]*Version[*]*:.*\.treelint' "$SOURCE_TREE" 2>/dev/null; then
    echo "PASS"
    PASS=$((PASS + 1))
else
    echo "FAIL - Version line does not mention .treelint/"
    FAIL=$((FAIL + 1))
fi

# Test 5.5: Last Updated date has been changed (not 2026-02-02)
echo -n "Test 5.5: Last Updated date changed from 2026-02-02... "
LAST_UPDATED=$(grep -E '^\*\*Last Updated\*\*:' "$SOURCE_TREE" 2>/dev/null | head -1)
if echo "$LAST_UPDATED" | grep -qv '2026-02-02'; then
    echo "PASS"
    PASS=$((PASS + 1))
else
    echo "FAIL - Last Updated date still shows 2026-02-02"
    FAIL=$((FAIL + 1))
fi

# Test 5.6: BR-001 - LOCKED status marker preserved
echo -n "Test 5.6: BR-001 - LOCKED status marker preserved... "
if grep -qE '^\*\*Status\*\*:.*LOCKED' "$SOURCE_TREE" 2>/dev/null; then
    echo "PASS"
    PASS=$((PASS + 1))
else
    echo "FAIL - LOCKED status marker missing or modified"
    FAIL=$((FAIL + 1))
fi

# Test 5.7: BR-002 - Existing root entries still present (spot check)
echo -n "Test 5.7: BR-002 - Existing root entries unchanged (.github/, .claude/, devforgeai/)... "
HAS_GITHUB=$(grep -c '\.github/' "$SOURCE_TREE" 2>/dev/null)
HAS_CLAUDE=$(grep -c '\.claude/' "$SOURCE_TREE" 2>/dev/null)
HAS_DEVFORGEAI=$(grep -c 'devforgeai/' "$SOURCE_TREE" 2>/dev/null)
HAS_SRC=$(grep -c 'src/' "$SOURCE_TREE" 2>/dev/null)
HAS_TESTS=$(grep -c 'tests/' "$SOURCE_TREE" 2>/dev/null)
if [ "$HAS_GITHUB" -gt 0 ] && [ "$HAS_CLAUDE" -gt 0 ] && [ "$HAS_DEVFORGEAI" -gt 0 ] && [ "$HAS_SRC" -gt 0 ] && [ "$HAS_TESTS" -gt 0 ]; then
    echo "PASS"
    PASS=$((PASS + 1))
else
    echo "FAIL - Existing root entries appear modified or missing"
    FAIL=$((FAIL + 1))
fi

echo ""
echo "=== AC#5 Results: $PASS/$TOTAL tests passed, $FAIL failed ==="
exit $FAIL

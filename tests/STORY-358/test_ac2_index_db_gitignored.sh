#!/bin/bash
# STORY-358 AC#2: index.db Documented as GITIGNORED with Rationale
# TDD Red Phase - These tests MUST FAIL before implementation
#
# Validates: index.db is marked GITIGNORED with rationale mentioning
# "regenerable" and "size concern" in the gitignore pattern section.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

SOURCE_TREE="$PROJECT_ROOT/devforgeai/specs/context/source-tree.md"

echo "=== AC#2: index.db Documented as GITIGNORED ==="
echo "Target file: $SOURCE_TREE"
echo ""

PASS=0
FAIL=0
TOTAL=4

# Locate the gitignore pattern section start line
GITIGNORE_SECTION_LINE=$(grep -niE '(##|###).*gitignore.*pattern' "$SOURCE_TREE" 2>/dev/null | head -1 | cut -d: -f1)

# Extract the gitignore section content (up to 50 lines from heading)
if [ -n "$GITIGNORE_SECTION_LINE" ]; then
    SECTION_CONTENT=$(tail -n +"$GITIGNORE_SECTION_LINE" "$SOURCE_TREE" 2>/dev/null | head -50)
else
    SECTION_CONTENT=""
fi

# Test 2.1: index.db has GITIGNORED recommendation in the section
echo -n "Test 2.1: index.db marked as GITIGNORED... "
if echo "$SECTION_CONTENT" | grep -qi 'index\.db' && echo "$SECTION_CONTENT" | grep -qi 'GITIGNORED'; then
    # Verify both appear on same line or in close proximity (table row)
    if echo "$SECTION_CONTENT" | grep -iE 'index\.db.*GITIGNORED|GITIGNORED.*index\.db' >/dev/null 2>&1; then
        echo "PASS"
        PASS=$((PASS + 1))
    else
        echo "FAIL - index.db and GITIGNORED not on same entry"
        FAIL=$((FAIL + 1))
    fi
else
    echo "FAIL - index.db with GITIGNORED not found in gitignore pattern section"
    FAIL=$((FAIL + 1))
fi

# Test 2.2: Rationale mentions "regenerable" (key AC keyword)
echo -n "Test 2.2: Rationale mentions regenerable... "
if echo "$SECTION_CONTENT" | grep -qi 'regenerable'; then
    echo "PASS"
    PASS=$((PASS + 1))
else
    echo "FAIL - Rationale does not mention 'regenerable'"
    FAIL=$((FAIL + 1))
fi

# Test 2.3: Rationale mentions size concern (large, size, grow)
echo -n "Test 2.3: Rationale mentions size concern... "
if echo "$SECTION_CONTENT" | grep -iE '(large|size|grow)' >/dev/null 2>&1; then
    echo "PASS"
    PASS=$((PASS + 1))
else
    echo "FAIL - Rationale does not mention size concern (large/size/grow)"
    FAIL=$((FAIL + 1))
fi

# Test 2.4: Rationale has at least 2 sentences (contains at least one period followed by text)
echo -n "Test 2.4: Rationale has minimum 2 sentences... "
# Extract lines mentioning index.db from section and count sentence-ending periods
INDEX_RATIONALE=$(echo "$SECTION_CONTENT" | grep -iA2 'index\.db')
PERIOD_COUNT=$(echo "$INDEX_RATIONALE" | grep -o '\.' | wc -l)
if [ "$PERIOD_COUNT" -ge 2 ]; then
    echo "PASS (found $PERIOD_COUNT periods)"
    PASS=$((PASS + 1))
else
    echo "FAIL - Rationale has fewer than 2 sentences (found $PERIOD_COUNT periods)"
    FAIL=$((FAIL + 1))
fi

echo ""
echo "=== AC#2 Results: $PASS/$TOTAL tests passed, $FAIL failed ==="
exit $FAIL

#!/bin/bash
# STORY-357 AC#2: index.db Documented as Gitignored SQLite Index
# TDD Red Phase - These tests MUST FAIL before implementation

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

SOURCE_TREE="$PROJECT_ROOT/devforgeai/specs/context/source-tree.md"

echo "=== AC#2: index.db Documented as Gitignored SQLite Index ==="
echo "Target file: $SOURCE_TREE"
echo ""

PASS=0
FAIL=0
TOTAL=4

# Test 2.1: index.db entry exists in tree diagram
echo -n "Test 2.1: index.db entry exists in tree diagram... "
if grep -qE '(├──|└──).*index\.db' "$SOURCE_TREE" 2>/dev/null; then
    echo "PASS"
    PASS=$((PASS + 1))
else
    echo "FAIL - index.db entry not found in tree diagram"
    FAIL=$((FAIL + 1))
fi

# Test 2.2: index.db comment mentions "gitignored" or "gitignore"
echo -n "Test 2.2: index.db comment mentions gitignored... "
if grep -iE 'index\.db.*#.*gitignore' "$SOURCE_TREE" 2>/dev/null; then
    echo "PASS"
    PASS=$((PASS + 1))
else
    echo "FAIL - index.db line does not mention gitignored"
    FAIL=$((FAIL + 1))
fi

# Test 2.3: index.db comment mentions "SQLite" or "AST index"
echo -n "Test 2.3: index.db comment mentions SQLite or AST index... "
if grep -iE 'index\.db.*#.*(SQLite|AST.index)' "$SOURCE_TREE" 2>/dev/null; then
    echo "PASS"
    PASS=$((PASS + 1))
else
    echo "FAIL - index.db line does not mention SQLite or AST index"
    FAIL=$((FAIL + 1))
fi

# Test 2.4: index.db is a child of .treelint/ (positioned after .treelint/ line)
echo -n "Test 2.4: index.db is a child of .treelint/ directory... "
TREELINT_LINE=$(grep -n '\.treelint/' "$SOURCE_TREE" 2>/dev/null | head -1 | cut -d: -f1)
INDEX_LINE=$(grep -n 'index\.db' "$SOURCE_TREE" 2>/dev/null | head -1 | cut -d: -f1)
if [ -n "$TREELINT_LINE" ] && [ -n "$INDEX_LINE" ]; then
    DIFF=$((INDEX_LINE - TREELINT_LINE))
    # Child should be within 4 lines of parent (parent + up to 3 children)
    if [ "$DIFF" -gt 0 ] && [ "$DIFF" -le 4 ]; then
        echo "PASS"
        PASS=$((PASS + 1))
    else
        echo "FAIL - index.db not positioned as immediate child of .treelint/"
        FAIL=$((FAIL + 1))
    fi
else
    echo "FAIL - Could not find .treelint/ or index.db lines"
    FAIL=$((FAIL + 1))
fi

echo ""
echo "=== AC#2 Results: $PASS/$TOTAL tests passed, $FAIL failed ==="
exit $FAIL

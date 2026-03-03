#!/bin/bash
# STORY-357 AC#1: .treelint/ Directory Added to Framework Directory Structure
# TDD Red Phase - These tests MUST FAIL before implementation

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

SOURCE_TREE="$PROJECT_ROOT/devforgeai/specs/context/source-tree.md"

echo "=== AC#1: .treelint/ Directory in Framework Directory Structure ==="
echo "Target file: $SOURCE_TREE"
echo ""

PASS=0
FAIL=0
TOTAL=6

# Test 1.1: .treelint/ entry exists in tree diagram
echo -n "Test 1.1: .treelint/ entry exists in tree diagram... "
if grep -q '\.treelint/' "$SOURCE_TREE" 2>/dev/null; then
    echo "PASS"
    PASS=$((PASS + 1))
else
    echo "FAIL - .treelint/ entry not found in source-tree.md"
    FAIL=$((FAIL + 1))
fi

# Test 1.2: .treelint/ entry is at project root level (uses root-level tree connector)
echo -n "Test 1.2: .treelint/ is at project root level (alongside .github/, .claude/)... "
if grep -qE '^[│├└].*\.treelint/' "$SOURCE_TREE" 2>/dev/null; then
    echo "PASS"
    PASS=$((PASS + 1))
else
    echo "FAIL - .treelint/ not at root level in tree diagram"
    FAIL=$((FAIL + 1))
fi

# Test 1.3: .treelint/ entry has comment referencing ADR-013
echo -n "Test 1.3: .treelint/ comment references ADR-013... "
if grep -E '\.treelint/' "$SOURCE_TREE" 2>/dev/null | grep -q 'ADR-013'; then
    echo "PASS"
    PASS=$((PASS + 1))
else
    echo "FAIL - .treelint/ line does not reference ADR-013"
    FAIL=$((FAIL + 1))
fi

# Test 1.4: index.db listed as child of .treelint/
echo -n "Test 1.4: index.db listed as child file... "
if grep -qE '(├──|└──).*index\.db' "$SOURCE_TREE" 2>/dev/null; then
    # Verify it appears after .treelint/ and before next root entry
    TREELINT_LINE=$(grep -n '\.treelint/' "$SOURCE_TREE" 2>/dev/null | head -1 | cut -d: -f1)
    INDEX_LINE=$(grep -n 'index\.db' "$SOURCE_TREE" 2>/dev/null | head -1 | cut -d: -f1)
    if [ -n "$TREELINT_LINE" ] && [ -n "$INDEX_LINE" ] && [ "$INDEX_LINE" -gt "$TREELINT_LINE" ]; then
        echo "PASS"
        PASS=$((PASS + 1))
    else
        echo "FAIL - index.db not positioned as child of .treelint/"
        FAIL=$((FAIL + 1))
    fi
else
    echo "FAIL - index.db not found in tree diagram"
    FAIL=$((FAIL + 1))
fi

# Test 1.5: config.toml listed as child of .treelint/
echo -n "Test 1.5: config.toml listed as child file... "
if grep -qE '(├──|└──).*config\.toml' "$SOURCE_TREE" 2>/dev/null; then
    TREELINT_LINE=$(grep -n '\.treelint/' "$SOURCE_TREE" 2>/dev/null | head -1 | cut -d: -f1)
    CONFIG_LINE=$(grep -n 'config\.toml' "$SOURCE_TREE" 2>/dev/null | head -1 | cut -d: -f1)
    if [ -n "$TREELINT_LINE" ] && [ -n "$CONFIG_LINE" ] && [ "$CONFIG_LINE" -gt "$TREELINT_LINE" ]; then
        echo "PASS"
        PASS=$((PASS + 1))
    else
        echo "FAIL - config.toml not positioned as child of .treelint/"
        FAIL=$((FAIL + 1))
    fi
else
    echo "FAIL - config.toml not found in tree diagram"
    FAIL=$((FAIL + 1))
fi

# Test 1.6: daemon.sock listed as child of .treelint/
echo -n "Test 1.6: daemon.sock listed as child file... "
if grep -qE '(├──|└──).*daemon\.sock' "$SOURCE_TREE" 2>/dev/null; then
    TREELINT_LINE=$(grep -n '\.treelint/' "$SOURCE_TREE" 2>/dev/null | head -1 | cut -d: -f1)
    DAEMON_LINE=$(grep -n 'daemon\.sock' "$SOURCE_TREE" 2>/dev/null | head -1 | cut -d: -f1)
    if [ -n "$TREELINT_LINE" ] && [ -n "$DAEMON_LINE" ] && [ "$DAEMON_LINE" -gt "$TREELINT_LINE" ]; then
        echo "PASS"
        PASS=$((PASS + 1))
    else
        echo "FAIL - daemon.sock not positioned as child of .treelint/"
        FAIL=$((FAIL + 1))
    fi
else
    echo "FAIL - daemon.sock not found in tree diagram"
    FAIL=$((FAIL + 1))
fi

echo ""
echo "=== AC#1 Results: $PASS/$TOTAL tests passed, $FAIL failed ==="
exit $FAIL

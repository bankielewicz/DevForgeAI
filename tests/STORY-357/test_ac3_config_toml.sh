#!/bin/bash
# STORY-357 AC#3: config.toml Documented as Optional-Commit Project Configuration
# TDD Red Phase - These tests MUST FAIL before implementation

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

SOURCE_TREE="$PROJECT_ROOT/devforgeai/specs/context/source-tree.md"

echo "=== AC#3: config.toml Documented as Optional-Commit Configuration ==="
echo "Target file: $SOURCE_TREE"
echo ""

PASS=0
FAIL=0
TOTAL=4

# Test 3.1: config.toml entry exists in tree diagram
echo -n "Test 3.1: config.toml entry exists in tree diagram... "
if grep -qE '(├──|└──).*config\.toml' "$SOURCE_TREE" 2>/dev/null; then
    echo "PASS"
    PASS=$((PASS + 1))
else
    echo "FAIL - config.toml entry not found in tree diagram"
    FAIL=$((FAIL + 1))
fi

# Test 3.2: config.toml comment mentions "optional" (optional commit, optional to commit)
echo -n "Test 3.2: config.toml comment mentions optional commit... "
if grep -iE 'config\.toml.*#.*optional' "$SOURCE_TREE" 2>/dev/null; then
    echo "PASS"
    PASS=$((PASS + 1))
else
    echo "FAIL - config.toml line does not mention optional commit"
    FAIL=$((FAIL + 1))
fi

# Test 3.3: config.toml mentions configuration purpose (config, configuration, settings)
echo -n "Test 3.3: config.toml comment describes configuration purpose... "
if grep -iE 'config\.toml.*#.*(config|configuration|settings|project)' "$SOURCE_TREE" 2>/dev/null; then
    echo "PASS"
    PASS=$((PASS + 1))
else
    echo "FAIL - config.toml line does not describe configuration purpose"
    FAIL=$((FAIL + 1))
fi

# Test 3.4: config.toml is a child of .treelint/ (positioned after .treelint/ line)
echo -n "Test 3.4: config.toml is a child of .treelint/ directory... "
TREELINT_LINE=$(grep -n '\.treelint/' "$SOURCE_TREE" 2>/dev/null | head -1 | cut -d: -f1)
CONFIG_LINE=$(grep -n 'config\.toml' "$SOURCE_TREE" 2>/dev/null | head -1 | cut -d: -f1)
if [ -n "$TREELINT_LINE" ] && [ -n "$CONFIG_LINE" ]; then
    DIFF=$((CONFIG_LINE - TREELINT_LINE))
    # Child should be within 4 lines of parent
    if [ "$DIFF" -gt 0 ] && [ "$DIFF" -le 4 ]; then
        echo "PASS"
        PASS=$((PASS + 1))
    else
        echo "FAIL - config.toml not positioned as immediate child of .treelint/"
        FAIL=$((FAIL + 1))
    fi
else
    echo "FAIL - Could not find .treelint/ or config.toml lines"
    FAIL=$((FAIL + 1))
fi

echo ""
echo "=== AC#3 Results: $PASS/$TOTAL tests passed, $FAIL failed ==="
exit $FAIL

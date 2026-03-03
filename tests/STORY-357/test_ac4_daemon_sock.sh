#!/bin/bash
# STORY-357 AC#4: daemon.sock Documented as Gitignored Ephemeral IPC Socket
# TDD Red Phase - These tests MUST FAIL before implementation

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

SOURCE_TREE="$PROJECT_ROOT/devforgeai/specs/context/source-tree.md"

echo "=== AC#4: daemon.sock Documented as Gitignored Ephemeral IPC Socket ==="
echo "Target file: $SOURCE_TREE"
echo ""

PASS=0
FAIL=0
TOTAL=5

# Test 4.1: daemon.sock entry exists in tree diagram
echo -n "Test 4.1: daemon.sock entry exists in tree diagram... "
if grep -qE '(├──|└──).*daemon\.sock' "$SOURCE_TREE" 2>/dev/null; then
    echo "PASS"
    PASS=$((PASS + 1))
else
    echo "FAIL - daemon.sock entry not found in tree diagram"
    FAIL=$((FAIL + 1))
fi

# Test 4.2: daemon.sock comment mentions "gitignored" or "gitignore"
echo -n "Test 4.2: daemon.sock comment mentions gitignored... "
if grep -iE 'daemon\.sock.*#.*gitignore' "$SOURCE_TREE" 2>/dev/null; then
    echo "PASS"
    PASS=$((PASS + 1))
else
    echo "FAIL - daemon.sock line does not mention gitignored"
    FAIL=$((FAIL + 1))
fi

# Test 4.3: daemon.sock comment mentions "ephemeral"
echo -n "Test 4.3: daemon.sock comment mentions ephemeral... "
if grep -iE 'daemon\.sock.*#.*ephemeral' "$SOURCE_TREE" 2>/dev/null; then
    echo "PASS"
    PASS=$((PASS + 1))
else
    echo "FAIL - daemon.sock line does not mention ephemeral"
    FAIL=$((FAIL + 1))
fi

# Test 4.4: daemon.sock comment mentions "IPC" or "socket"
echo -n "Test 4.4: daemon.sock comment mentions IPC or socket... "
if grep -iE 'daemon\.sock.*#.*(IPC|socket)' "$SOURCE_TREE" 2>/dev/null; then
    echo "PASS"
    PASS=$((PASS + 1))
else
    echo "FAIL - daemon.sock line does not mention IPC or socket"
    FAIL=$((FAIL + 1))
fi

# Test 4.5: daemon.sock is a child of .treelint/ (positioned after .treelint/ line)
echo -n "Test 4.5: daemon.sock is a child of .treelint/ directory... "
TREELINT_LINE=$(grep -n '\.treelint/' "$SOURCE_TREE" 2>/dev/null | head -1 | cut -d: -f1)
DAEMON_LINE=$(grep -n 'daemon\.sock' "$SOURCE_TREE" 2>/dev/null | head -1 | cut -d: -f1)
if [ -n "$TREELINT_LINE" ] && [ -n "$DAEMON_LINE" ]; then
    DIFF=$((DAEMON_LINE - TREELINT_LINE))
    # Child should be within 4 lines of parent
    if [ "$DIFF" -gt 0 ] && [ "$DIFF" -le 4 ]; then
        echo "PASS"
        PASS=$((PASS + 1))
    else
        echo "FAIL - daemon.sock not positioned as immediate child of .treelint/"
        FAIL=$((FAIL + 1))
    fi
else
    echo "FAIL - Could not find .treelint/ or daemon.sock lines"
    FAIL=$((FAIL + 1))
fi

echo ""
echo "=== AC#4 Results: $PASS/$TOTAL tests passed, $FAIL failed ==="
exit $FAIL

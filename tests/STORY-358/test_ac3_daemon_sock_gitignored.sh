#!/bin/bash
# STORY-358 AC#3: daemon.sock Documented as GITIGNORED with Rationale
# TDD Red Phase - These tests MUST FAIL before implementation
#
# Validates: daemon.sock is marked GITIGNORED with rationale mentioning
# "ephemeral" and "runtime/IPC socket" in the gitignore pattern section.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

SOURCE_TREE="$PROJECT_ROOT/devforgeai/specs/context/source-tree.md"

echo "=== AC#3: daemon.sock Documented as GITIGNORED ==="
echo "Target file: $SOURCE_TREE"
echo ""

PASS=0
FAIL=0
TOTAL=4

# Locate the gitignore pattern section start line
GITIGNORE_SECTION_LINE=$(grep -niE '(##|###).*gitignore.*pattern' "$SOURCE_TREE" 2>/dev/null | head -1 | cut -d: -f1)

if [ -n "$GITIGNORE_SECTION_LINE" ]; then
    SECTION_CONTENT=$(tail -n +"$GITIGNORE_SECTION_LINE" "$SOURCE_TREE" 2>/dev/null | head -50)
else
    SECTION_CONTENT=""
fi

# Test 3.1: daemon.sock has GITIGNORED recommendation in the section
echo -n "Test 3.1: daemon.sock marked as GITIGNORED... "
if echo "$SECTION_CONTENT" | grep -iE 'daemon\.sock.*GITIGNORED|GITIGNORED.*daemon\.sock' >/dev/null 2>&1; then
    echo "PASS"
    PASS=$((PASS + 1))
else
    echo "FAIL - daemon.sock with GITIGNORED not found in gitignore pattern section"
    FAIL=$((FAIL + 1))
fi

# Test 3.2: Rationale mentions "ephemeral" (key AC keyword)
echo -n "Test 3.2: Rationale mentions ephemeral... "
if echo "$SECTION_CONTENT" | grep -qi 'ephemeral'; then
    echo "PASS"
    PASS=$((PASS + 1))
else
    echo "FAIL - Rationale does not mention 'ephemeral'"
    FAIL=$((FAIL + 1))
fi

# Test 3.3: Rationale mentions runtime or IPC socket
echo -n "Test 3.3: Rationale mentions runtime or IPC socket... "
if echo "$SECTION_CONTENT" | grep -iE '(runtime|IPC.*socket|Unix.*socket)' >/dev/null 2>&1; then
    echo "PASS"
    PASS=$((PASS + 1))
else
    echo "FAIL - Rationale does not mention runtime/IPC socket"
    FAIL=$((FAIL + 1))
fi

# Test 3.4: Rationale has at least 2 sentences
echo -n "Test 3.4: Rationale has minimum 2 sentences... "
DAEMON_RATIONALE=$(echo "$SECTION_CONTENT" | grep -iA2 'daemon\.sock')
PERIOD_COUNT=$(echo "$DAEMON_RATIONALE" | grep -o '\.' | wc -l)
if [ "$PERIOD_COUNT" -ge 2 ]; then
    echo "PASS (found $PERIOD_COUNT periods)"
    PASS=$((PASS + 1))
else
    echo "FAIL - Rationale has fewer than 2 sentences (found $PERIOD_COUNT periods)"
    FAIL=$((FAIL + 1))
fi

echo ""
echo "=== AC#3 Results: $PASS/$TOTAL tests passed, $FAIL failed ==="
exit $FAIL

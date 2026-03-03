#!/bin/bash
# STORY-333 AC#6: Operational Copy Synchronization
# Tests that src/ and .claude/ copies are identical
# TDD Red Phase: These tests FAIL until implementation complete

set -e
SRC_CORE="src/claude/agents/test-automator.md"
OPS_CORE=".claude/agents/test-automator.md"
SRC_REFS="src/claude/agents/test-automator/references"
OPS_REFS=".claude/agents/test-automator/references"

echo "=== AC#6: Operational Copy Synchronization ==="

# Test 1: Both core files exist
echo -n "Test 1: Both core files exist... "
if [ ! -f "$SRC_CORE" ]; then
    echo "FAIL (missing: $SRC_CORE)"
    exit 1
fi
if [ ! -f "$OPS_CORE" ]; then
    echo "FAIL (missing: $OPS_CORE)"
    exit 1
fi
echo "PASS"

# Test 2: Core files are identical
echo -n "Test 2: Core files identical... "
if ! diff -q "$SRC_CORE" "$OPS_CORE" > /dev/null 2>&1; then
    echo "FAIL (files differ)"
    exit 1
fi
echo "PASS"

# Test 3: Both reference directories exist
echo -n "Test 3: Both reference directories exist... "
if [ ! -d "$SRC_REFS" ]; then
    echo "FAIL (missing: $SRC_REFS)"
    exit 1
fi
if [ ! -d "$OPS_REFS" ]; then
    echo "FAIL (missing: $OPS_REFS)"
    exit 1
fi
echo "PASS"

# Test 4: Reference directories have same file count
echo -n "Test 4: Same reference file count... "
SRC_COUNT=$(find "$SRC_REFS" -maxdepth 1 -name "*.md" -type f | wc -l)
OPS_COUNT=$(find "$OPS_REFS" -maxdepth 1 -name "*.md" -type f | wc -l)
if [ "$SRC_COUNT" -ne "$OPS_COUNT" ]; then
    echo "FAIL (src=$SRC_COUNT, ops=$OPS_COUNT)"
    exit 1
fi
echo "PASS ($SRC_COUNT files each)"

# Test 5: Reference files are identical
echo -n "Test 5: Reference files identical... "
DIFF_OUTPUT=$(diff -rq "$SRC_REFS" "$OPS_REFS" 2>&1 || true)
if [ -n "$DIFF_OUTPUT" ]; then
    echo "FAIL"
    echo "$DIFF_OUTPUT"
    exit 1
fi
echo "PASS"

echo ""
echo "AC#6: All tests PASSED"

#!/bin/bash
# STORY-333 AC#4: Reference Loading Pattern Implementation
# Tests that core file has Reference Loading section with Read() calls
# TDD Red Phase: These tests FAIL until implementation complete

set -e
CORE_FILE="src/claude/agents/test-automator.md"

echo "=== AC#4: Reference Loading Pattern ==="

# Test 1: Reference Loading section exists
echo -n "Test 1: Reference Loading section exists... "
if ! grep -qE "^## Reference Loading" "$CORE_FILE"; then
    echo "FAIL"
    exit 1
fi
echo "PASS"

# Test 2: Read() calls present (minimum 6 for 6 reference files)
echo -n "Test 2: Read() calls for references (>=6)... "
READ_COUNT=$(grep -cE 'Read\(file_path.*test-automator/references/' "$CORE_FILE" || echo "0")
if [ "$READ_COUNT" -lt 6 ]; then
    echo "FAIL (found $READ_COUNT, need >=6)"
    exit 1
fi
echo "PASS ($READ_COUNT calls)"

# Test 3: Conditional loading documented (when to load each)
echo -n "Test 3: Conditional loading instructions... "
CONDITIONALS=("framework-patterns" "remediation-mode" "exception-path" "technical-specification" "common-patterns" "coverage-optimization")
MISSING=""
for COND in "${CONDITIONALS[@]}"; do
    if ! grep -qE "$COND" "$CORE_FILE"; then
        MISSING="$MISSING $COND"
    fi
done
if [ -n "$MISSING" ]; then
    echo "FAIL (missing:$MISSING)"
    exit 1
fi
echo "PASS"

# Test 4: Reference paths are correct format
echo -n "Test 4: Reference paths format correct... "
if ! grep -qE 'src/claude/agents/test-automator/references/[a-z-]+\.md' "$CORE_FILE"; then
    echo "FAIL (no valid reference paths)"
    exit 1
fi
echo "PASS"

echo ""
echo "AC#4: All tests PASSED"

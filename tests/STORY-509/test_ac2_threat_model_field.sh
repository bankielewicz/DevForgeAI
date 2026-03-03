#!/bin/bash
# Test: AC#2 - threat_model Field Added to F4 Schema
# Story: STORY-509
# Generated: 2026-02-28

PASSED=0
FAILED=0

TARGET_FILE="src/claude/skills/discovering-requirements/references/artifact-generation.md"

run_test() {
    local name="$1"
    local result="$2"
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        PASSED=$((PASSED + 1))
    else
        echo "  FAIL: $name"
        FAILED=$((FAILED + 1))
    fi
}

echo "=== AC#2: threat_model Field in F4 Schema ==="
echo "Target: $TARGET_FILE"
echo ""

if [ ! -f "$TARGET_FILE" ]; then
    echo "  FAIL: Target file does not exist: $TARGET_FILE"
    echo "Results: 0 passed, 1 failed"
    exit 1
fi

# Test 1: threat_model top-level section exists
grep -qi "threat_model" "$TARGET_FILE" 2>/dev/null; run_test "threat_model section exists in F4 schema" $?

# Test 2: adversary field
grep -A 20 -i "threat_model" "$TARGET_FILE" 2>/dev/null | grep -qi "\badversary\b" 2>/dev/null; run_test "threat_model has 'adversary' field" $?

# Test 3: in_scope field
grep -A 20 -i "threat_model" "$TARGET_FILE" 2>/dev/null | grep -qi "in_scope" 2>/dev/null; run_test "threat_model has 'in_scope' field" $?

# Test 4: out_of_scope field
grep -A 20 -i "threat_model" "$TARGET_FILE" 2>/dev/null | grep -qi "out_of_scope" 2>/dev/null; run_test "threat_model has 'out_of_scope' field" $?

# Summary
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1

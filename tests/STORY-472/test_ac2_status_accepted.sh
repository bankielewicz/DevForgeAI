#!/bin/bash
# Test: AC#2 - ADR Status Is Accepted
# Story: STORY-472
# Generated: 2026-02-23

PASSED=0
FAILED=0

run_test() {
    local name="$1"
    local result="$2"
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        ((PASSED++))
    else
        echo "  FAIL: $name"
        ((FAILED++))
    fi
}

echo "=== AC#2: ADR Status Is Accepted ==="

# === Arrange ===
TARGET_FILE="devforgeai/specs/adrs/ADR-021-configuration-layer-alignment-protocol.md"

# === Act & Assert ===

# Test 1: Status field is exactly "Accepted"
grep -q "^[*]*Status[*]*:.*Accepted" "$TARGET_FILE" 2>/dev/null
run_test "Status field value is exactly Accepted" $?

# Test 2: Status is NOT Draft
grep -q "^[*]*Status[*]*:.*Draft" "$TARGET_FILE" 2>/dev/null
DRAFT_FOUND=$?
[ "$DRAFT_FOUND" -ne 0 ]
run_test "Status is not Draft" $?

# Test 3: Status is NOT Proposed
grep -q "^[*]*Status[*]*:.*Proposed" "$TARGET_FILE" 2>/dev/null
PROPOSED_FOUND=$?
[ "$PROPOSED_FOUND" -ne 0 ]
run_test "Status is not Proposed" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1

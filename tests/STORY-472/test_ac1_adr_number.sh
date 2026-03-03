#!/bin/bash
# Test: AC#1 - ADR Number Assignment
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

echo "=== AC#1: ADR Number Assignment ==="

# === Arrange ===
TARGET_FILE="devforgeai/specs/adrs/ADR-021-configuration-layer-alignment-protocol.md"

# === Act & Assert ===

# Test 1: ADR file exists at correct path
test -f "$TARGET_FILE"
run_test "ADR-021 file exists at devforgeai/specs/adrs/ADR-021-configuration-layer-alignment-protocol.md" $?

# Test 2: Document header contains "ADR-021"
grep -q "ADR-021" "$TARGET_FILE" 2>/dev/null
run_test "Document header contains ADR-021" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1

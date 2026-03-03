#!/bin/bash
# Test: AC#7 - References Section Links to Source Materials
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

echo "=== AC#7: References Section Links to Source Materials ==="

# === Arrange ===
TARGET_FILE="devforgeai/specs/adrs/ADR-021-configuration-layer-alignment-protocol.md"

# === Act & Assert ===

# Test 1: References section exists
grep -q "^## References" "$TARGET_FILE" 2>/dev/null
run_test "References section header exists" $?

# Test 2: ENH-CLAP-001 referenced
grep -q "ENH-CLAP-001" "$TARGET_FILE" 2>/dev/null
run_test "ENH-CLAP-001 referenced" $?

# Test 3: Requirements specification referenced
grep -qi "requirements.*spec\|clap.*requirements\|configuration-layer-alignment-requirements" "$TARGET_FILE" 2>/dev/null
run_test "CLAP requirements specification referenced" $?

# Test 4: EPIC-081 referenced
grep -q "EPIC-081" "$TARGET_FILE" 2>/dev/null
run_test "EPIC-081 referenced" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1

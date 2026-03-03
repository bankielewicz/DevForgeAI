#!/bin/bash
# Test: AC#3 - Context Section Explains Validation Gap
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

echo "=== AC#3: Context Section Explains Validation Gap ==="

# === Arrange ===
TARGET_FILE="devforgeai/specs/adrs/ADR-021-configuration-layer-alignment-protocol.md"

# === Act & Assert ===

# Test 1: Context section exists
grep -q "^## Context" "$TARGET_FILE" 2>/dev/null
run_test "Context section header exists" $?

# Test 2: Context mentions cross-layer or validation gap
grep -qi "cross-layer\|validation gap\|no.*cross.*check" "$TARGET_FILE" 2>/dev/null
run_test "Context explains cross-layer validation gap" $?

# Test 3: Context lists existing validators
grep -qi "context-validator" "$TARGET_FILE" 2>/dev/null
run_test "Context mentions existing context-validator" $?

# Test 4: Context references ENH-CLAP-001
grep -q "ENH-CLAP-001" "$TARGET_FILE" 2>/dev/null
run_test "Context references ENH-CLAP-001" $?

# Test 5: Context references GPUXtend evidence
grep -qi "GPUXtend" "$TARGET_FILE" 2>/dev/null
run_test "Context references GPUXtend evidence" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1

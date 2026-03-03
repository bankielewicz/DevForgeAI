#!/bin/bash
# Test: AC#5 - Rationale Explains SRP Boundary
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

echo "=== AC#5: Rationale Explains SRP Boundary ==="

# === Arrange ===
TARGET_FILE="devforgeai/specs/adrs/ADR-021-configuration-layer-alignment-protocol.md"

# === Act & Assert ===

# Test 1: Rationale section exists
grep -q "^## Rationale" "$TARGET_FILE" 2>/dev/null
run_test "Rationale section header exists" $?

# Test 2: SRP or Single Responsibility Principle mentioned
grep -qi "Single Responsibility\|SRP" "$TARGET_FILE" 2>/dev/null
run_test "Single Responsibility Principle referenced" $?

# Test 3: alignment-auditor vs context-validator separation explained
grep -qi "alignment-auditor.*context-validator\|context-validator.*alignment-auditor" "$TARGET_FILE" 2>/dev/null
run_test "alignment-auditor vs context-validator separation explained" $?

# Test 4: Model requirements mentioned (haiku vs opus)
grep -qi "haiku.*opus\|opus.*haiku\|model.*requirement" "$TARGET_FILE" 2>/dev/null
run_test "Different model requirements documented (haiku vs opus)" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1

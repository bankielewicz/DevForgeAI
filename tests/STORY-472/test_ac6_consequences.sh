#!/bin/bash
# Test: AC#6 - Consequences Section Documents Trigger Points and Exclusions
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

echo "=== AC#6: Consequences Section Documents Trigger Points and Exclusions ==="

# === Arrange ===
TARGET_FILE="devforgeai/specs/adrs/ADR-021-configuration-layer-alignment-protocol.md"

# === Act & Assert ===

# Test 1: Consequences section exists
grep -q "^## Consequences" "$TARGET_FILE" 2>/dev/null
run_test "Consequences section header exists" $?

# Test 2: Trigger - after /create-context
grep -qi "create-context" "$TARGET_FILE" 2>/dev/null
run_test "Trigger point: after /create-context documented" $?

# Test 3: Trigger - on-demand via /audit-alignment
grep -qi "audit-alignment" "$TARGET_FILE" 2>/dev/null
run_test "Trigger point: on-demand via /audit-alignment documented" $?

# Test 4: Trigger - after ADR acceptance
grep -qi "after ADR\|ADR acceptance" "$TARGET_FILE" 2>/dev/null
run_test "Trigger point: after ADR acceptance documented" $?

# Test 5: Exclusion - not during /dev
grep -qi "not.*during.*/dev\|exclud.*/dev\|/dev.*not\|/dev.*exclud" "$TARGET_FILE" 2>/dev/null
run_test "Exclusion: not during /dev documented" $?

# Test 6: Exclusion - not during /qa
grep -qi "not.*during.*/qa\|exclud.*/qa\|/qa.*not\|/qa.*exclud" "$TARGET_FILE" 2>/dev/null
run_test "Exclusion: not during /qa documented" $?

# Test 7: Mutability rules - never auto-modify context files
grep -qi "never.*auto.*modif\|immutab\|Critical Rule.*4\|not.*modify.*context" "$TARGET_FILE" 2>/dev/null
run_test "Mutability rule: never auto-modify context files" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1

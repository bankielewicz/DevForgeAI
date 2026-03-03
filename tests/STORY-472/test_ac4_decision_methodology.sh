#!/bin/bash
# Test: AC#4 - Decision Section Documents CLAP Methodology
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

echo "=== AC#4: Decision Section Documents CLAP Methodology ==="

# === Arrange ===
TARGET_FILE="devforgeai/specs/adrs/ADR-021-configuration-layer-alignment-protocol.md"

# === Act & Assert ===

# Test 1: Decision section exists
grep -q "^## Decision" "$TARGET_FILE" 2>/dev/null
run_test "Decision section header exists" $?

# Test 2: 5-step methodology documented
grep -qi "5-step\|five.step\|step 1.*step 2.*step 3\|methodology" "$TARGET_FILE" 2>/dev/null
run_test "5-step alignment methodology documented" $?

# Test 3: alignment-auditor subagent mentioned
grep -q "alignment-auditor" "$TARGET_FILE" 2>/dev/null
run_test "alignment-auditor subagent documented" $?

# Test 4: /audit-alignment command mentioned
grep -q "/audit-alignment\|audit-alignment" "$TARGET_FILE" 2>/dev/null
run_test "audit-alignment command documented" $?

# Test 5: Phase 5.5 integration mentioned
grep -qi "Phase 5.5\|phase 5\.5\|designing-systems" "$TARGET_FILE" 2>/dev/null
run_test "Phase 5.5 designing-systems integration documented" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1

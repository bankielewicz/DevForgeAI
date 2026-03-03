#!/bin/bash
# Test: AC#2 - ADR Created for Decision
# Story: STORY-481
# Generated: 2026-02-23
# Description: Verifies that an ADR file exists documenting the subagent reference loading
#              mechanism decision, including alternatives and consequences.

# === Test Configuration ===
PASSED=0
FAILED=0

ADR_DIR="/mnt/c/Projects/DevForgeAI2/devforgeai/specs/adrs"
# ADR-022 is the next available number after ADR-021
EXPECTED_ADR_FILE="$ADR_DIR/ADR-022-subagent-reference-loading.md"

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

echo "=== AC#2: ADR Created for Decision ==="
echo "Expected ADR: $EXPECTED_ADR_FILE"
echo ""

# === Arrange ===
# Verify ADR directory exists
if [ ! -d "$ADR_DIR" ]; then
    echo "  ERROR: ADR directory does not exist: $ADR_DIR"
    echo "Results: 0 passed, 1 failed (ADR directory missing)"
    exit 1
fi

# === Act & Assert ===

# Test 1: ADR file must exist at expected path ADR-022
[ -f "$EXPECTED_ADR_FILE" ]
run_test "ADR-022-subagent-reference-loading.md file exists" $?

# Test 2: ADR file must reference EPIC-082 (this decision is scoped to EPIC-082)
if [ -f "$EXPECTED_ADR_FILE" ]; then
    grep -q "EPIC-082" "$EXPECTED_ADR_FILE"
    run_test "ADR references EPIC-082 (decision scope)" $?
else
    echo "  FAIL: ADR references EPIC-082 (decision scope) - file missing"
    ((FAILED++))
fi

# Test 3: ADR must document all 3 alternatives (orchestration-driven, opt-in, auto-load)
if [ -f "$EXPECTED_ADR_FILE" ]; then
    grep -q "orchestration-driven" "$EXPECTED_ADR_FILE"
    run_test "ADR documents orchestration-driven alternative" $?
else
    echo "  FAIL: ADR documents orchestration-driven alternative - file missing"
    ((FAILED++))
fi

if [ -f "$EXPECTED_ADR_FILE" ]; then
    grep -q "opt-in" "$EXPECTED_ADR_FILE"
    run_test "ADR documents opt-in alternative" $?
else
    echo "  FAIL: ADR documents opt-in alternative - file missing"
    ((FAILED++))
fi

if [ -f "$EXPECTED_ADR_FILE" ]; then
    grep -q "auto-load" "$EXPECTED_ADR_FILE"
    run_test "ADR documents auto-load alternative" $?
else
    echo "  FAIL: ADR documents auto-load alternative - file missing"
    ((FAILED++))
fi

# Test 4: ADR must have a Consequences section
if [ -f "$EXPECTED_ADR_FILE" ]; then
    grep -q "## Consequences" "$EXPECTED_ADR_FILE"
    run_test "ADR contains '## Consequences' section" $?
else
    echo "  FAIL: ADR contains '## Consequences' section - file missing"
    ((FAILED++))
fi

# Test 5: ADR must have a Decision section
if [ -f "$EXPECTED_ADR_FILE" ]; then
    grep -q "## Decision" "$EXPECTED_ADR_FILE"
    run_test "ADR contains '## Decision' section" $?
else
    echo "  FAIL: ADR contains '## Decision' section - file missing"
    ((FAILED++))
fi

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1

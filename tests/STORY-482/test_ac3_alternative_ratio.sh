#!/bin/bash

# Test: AC#3 - Alternative Ratio Provided
# Story: STORY-482
# Generated: 2026-02-23
#
# This test verifies that documentation specifies an alternative ratio
# (e.g., 95/5/0 unit/integration/e2e) for pure-logic modules.

# === Test Configuration ===
PASSED=0
FAILED=0
TARGET_FILE=".claude/agents/test-automator.md"

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

echo "Testing AC#3: Alternative Ratio Provided"
echo "=========================================="

# === Arrange ===
if [ ! -f "$TARGET_FILE" ]; then
    echo "ERROR: Target file not found: $TARGET_FILE"
    exit 1
fi

# === Act & Assert ===

# Test 1: Alternative ratio mentioned in exception section
grep -A 50 "^## Test Pyramid Exceptions" "$TARGET_FILE" | grep -q -E "[0-9]+/[0-9]+/[0-9]+"
run_test "Alternative ratio specified (ratio format: XX/XX/XX)" $?

# Test 2: Ratio components mentioned (unit, integration, E2E)
grep -A 50 "^## Test Pyramid Exceptions" "$TARGET_FILE" | grep -q -E "unit|integration|e2e|end-to-end"
run_test "Ratio components labeled (unit/integration/E2E)" $?

# Test 3: Document distinguishes from default 70/20/10
grep -A 50 "^## Test Pyramid Exceptions" "$TARGET_FILE" | grep -q -i "alternative\|instead.*70\|instead.*standard"
run_test "Documentation distinguishes alternative from standard 70/20/10" $?

# Test 4: Example ratio with high unit test percentage
grep -A 50 "^## Test Pyramid Exceptions" "$TARGET_FILE" | grep -q -E "9[0-9]/[0-9]+/[0-9]+"
run_test "Alternative ratio shows high unit test percentage (90%+)" $?

# Test 5: Documentation mentions "pure-logic" in context of alternative ratio
grep -A 50 "^## Test Pyramid Exceptions" "$TARGET_FILE" | grep -q -i "pure"
run_test "Alternative ratio tied to pure-logic modules" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1

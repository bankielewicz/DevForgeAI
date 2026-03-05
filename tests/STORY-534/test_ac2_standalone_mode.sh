#!/bin/bash
# Test: AC#2 - Standalone Mode Detection
# Story: STORY-534
# Generated: 2026-03-04
#
# Verifies the command file contains standalone mode logic:
# - Operates without context directory
# - Prompts user for business idea via AskUserQuestion
# - Labels this as standalone mode

# === Test Configuration ===
PASSED=0
FAILED=0
TARGET_FILE="src/claude/commands/business-plan.md"

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

echo "=== AC#2: Standalone Mode Detection ==="
echo ""

# === Arrange ===
if [ ! -f "$TARGET_FILE" ]; then
    echo "  FAIL: Target file does not exist: $TARGET_FILE"
    echo ""
    echo "Results: 0 passed, 1 failed (file missing - expected in RED phase)"
    exit 1
fi

# === Act & Assert ===

# Test 1: Command references standalone mode
grep -qiE "standalone.mode|standalone" "$TARGET_FILE"
run_test "References standalone mode" $?

# Test 2: Command handles missing context directory scenario
grep -qiE "(no|without|missing|absent).*(context|devforgeai)" "$TARGET_FILE"
run_test "Handles missing context directory scenario" $?

# Test 3: Command uses AskUserQuestion to prompt for business idea
grep -qiE "AskUserQuestion.*business.idea|business.idea.*AskUserQuestion|prompt.*business.idea" "$TARGET_FILE"
run_test "Uses AskUserQuestion for business idea input" $?

# Test 4: Command collects business idea description from user
grep -qiE "business.idea|idea.description|describe.*business" "$TARGET_FILE"
run_test "Collects business idea description" $?

# Test 5: Command distinguishes standalone from project mode
grep -qiE "IF.*(context|devforgeai).*exist|ELSE.*standalone|mode.detection" "$TARGET_FILE"
run_test "Contains mode detection branching logic" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1

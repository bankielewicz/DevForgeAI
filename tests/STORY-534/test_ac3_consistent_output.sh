#!/bin/bash
# Test: AC#3 - Consistent Output Format
# Story: STORY-534
# Generated: 2026-03-04
#
# Verifies the command produces the same output structure regardless of mode:
# - Both modes invoke planning-business skill
# - Output sections are consistent across modes
# - Shared output template or format specification

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

echo "=== AC#3: Consistent Output Format ==="
echo ""

# === Arrange ===
if [ ! -f "$TARGET_FILE" ]; then
    echo "  FAIL: Target file does not exist: $TARGET_FILE"
    echo ""
    echo "Results: 0 passed, 1 failed (file missing - expected in RED phase)"
    exit 1
fi

# === Act & Assert ===

# Test 1: Command invokes planning-business skill
grep -qiE "planning-business" "$TARGET_FILE"
run_test "Invokes planning-business skill" $?

# Test 2: Both modes produce same output structure
grep -qiE "consistent|same.*(output|format|structure)|output.*format|regardless.*mode" "$TARGET_FILE"
run_test "Specifies consistent output across modes" $?

# Test 3: Command references planning-business skill in project-anchored mode
grep -qiE "project.*planning-business|anchored.*planning-business" "$TARGET_FILE"
run_test "Uses planning-business in project-anchored mode" $?

# Test 4: Command references planning-business skill in standalone mode
grep -qiE "standalone.*planning-business|planning-business.*standalone" "$TARGET_FILE"
run_test "Uses planning-business in standalone mode" $?

# Test 5: Output sections include business model or viability content
grep -qiE "business.model|viability|revenue|market|output.*section" "$TARGET_FILE"
run_test "Output includes business model analysis sections" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1

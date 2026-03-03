#!/bin/bash
# Test: AC#5 - Graceful skip when source-tree.md has no "Dual-Location Architecture" section
# Story: STORY-487
# Generated: 2026-02-23
# RED PHASE: These tests FAIL until the function is implemented.
#
# Validates:
#   - Function checks for "Dual-Location Architecture" section in source-tree.md
#   - When section is absent, function returns empty violations list (graceful skip)
#   - No error/halt when section is missing

PASSED=0
FAILED=0

TARGET_FILE="/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-story-creation/references/context-validation.md"

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

echo "=== AC#5: Graceful skip when source-tree.md has no Dual-Location Architecture section ==="
echo "Target: $TARGET_FILE"
echo ""

# Extract the validate_dual_path function section
LINE_FUNC_START=$(grep -n "validate_dual_path" "$TARGET_FILE" | head -1 | cut -d: -f1)
LINE_CUSTODY=$(grep -n "Custody Chain Validation Functions" "$TARGET_FILE" | head -1 | cut -d: -f1)

if [ -z "$LINE_FUNC_START" ] || [ -z "$LINE_CUSTODY" ]; then
    echo "  FAIL: validate_dual_path function section not found - cannot extract function content"
    ((FAILED+=4))
    echo ""
    echo "Results: $PASSED passed, $FAILED failed"
    exit 1
fi

FUNC_CONTENT=$(sed -n "${LINE_FUNC_START},${LINE_CUSTODY}p" "$TARGET_FILE" 2>/dev/null)

# Test 1: Function checks for "Dual-Location Architecture" section in source-tree.md
echo "$FUNC_CONTENT" | grep -q "Dual-Location Architecture"
run_test "Function checks for 'Dual-Location Architecture' section" $?

# Test 2: Function reads source-tree.md
echo "$FUNC_CONTENT" | grep -q "source-tree.md"
run_test "Function reads source-tree.md" $?

# Test 3: Function has early return / graceful skip when section absent
# Pattern: IF section not found -> return [] or RETURN empty
echo "$FUNC_CONTENT" | grep -qiE 'not found.*return|RETURN \[\]|return \[\]|skip.*validation|IF.*NOT.*Dual-Location|no.*Dual-Location'
run_test "Function documents graceful skip when Dual-Location Architecture section absent" $?

# Test 4: Empty violations list is the documented return for graceful skip
echo "$FUNC_CONTENT" | grep -qE 'violations = \[\]|\[\].*violations|empty.*violations|violations.*empty'
run_test "Function returns empty violations list for graceful skip case" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1

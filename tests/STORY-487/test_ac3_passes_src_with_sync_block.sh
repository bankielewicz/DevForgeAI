#!/bin/bash
# Test: AC#3 - Function passes stories with src/ paths and dual_path_sync block
# Story: STORY-487
# Generated: 2026-02-23
# RED PHASE: These tests FAIL until the function is implemented.
#
# Validates:
#   - validate_dual_path() documents happy-path logic for src/ paths
#   - Function explicitly returns zero violations when dual_path_sync block present
#   - src/ path pattern is recognized as valid (does not trigger violation)

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

echo "=== AC#3: Function passes stories with src/ paths and dual_path_sync block ==="
echo "Target: $TARGET_FILE"
echo ""

# Test 1: Function logic references src/ path pattern
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

# Test 1: Function references src/ path as valid/pass condition
echo "$FUNC_CONTENT" | grep -qE 'src/'
run_test "Function body references src/ path pattern" $?

# Test 2: Function documents zero violations return for compliant stories
echo "$FUNC_CONTENT" | grep -qE 'violations.*\[\]|zero violations|no violations|violations = \[\]'
run_test "Function documents zero violations return for compliant stories" $?

# Test 3: dual_path_sync presence is a pass condition (not just detected as missing)
# The function should check IF dual_path_sync IS present → pass
echo "$FUNC_CONTENT" | grep -qE 'dual_path_sync.*present|has.*dual_path_sync|dual_path_sync.*found|IF.*dual_path_sync'
run_test "Function documents dual_path_sync presence as pass condition" $?

# Test 4: Return statement exists for the no-violation case
echo "$FUNC_CONTENT" | grep -qiE 'return violations|RETURN violations'
run_test "Function has explicit return violations statement" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1

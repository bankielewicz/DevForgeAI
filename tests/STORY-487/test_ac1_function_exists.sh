#!/bin/bash
# Test: AC#1 - validate_dual_path() function exists in correct position
# Story: STORY-487
# Generated: 2026-02-23
# RED PHASE: These tests FAIL until the function is implemented.
#
# Validates:
#   - validate_dual_path() function header exists in context-validation.md
#   - It appears AFTER validate_anti_patterns section
#   - It appears BEFORE "Custody Chain Validation Functions" section

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

echo "=== AC#1: validate_dual_path() function exists in correct position ==="
echo "Target: $TARGET_FILE"
echo ""

# Test 1: Function header exists at all
grep -q "validate_dual_path" "$TARGET_FILE"
run_test "validate_dual_path appears in context-validation.md" $?

# Test 2: Function is defined as a numbered section (### 7. validate_dual_path)
grep -qE "^### [0-9]+\. validate_dual_path" "$TARGET_FILE"
run_test "validate_dual_path defined as numbered section heading" $?

# Test 3: validate_anti_patterns appears BEFORE validate_dual_path
# Extract line numbers and compare
LINE_ANTI=$(grep -n "validate_anti_patterns" "$TARGET_FILE" | head -1 | cut -d: -f1)
LINE_DUAL=$(grep -n "validate_dual_path" "$TARGET_FILE" | head -1 | cut -d: -f1)

if [ -n "$LINE_ANTI" ] && [ -n "$LINE_DUAL" ] && [ "$LINE_ANTI" -lt "$LINE_DUAL" ]; then
    run_test "validate_dual_path appears AFTER validate_anti_patterns" 0
else
    run_test "validate_dual_path appears AFTER validate_anti_patterns" 1
fi

# Test 4: validate_dual_path appears BEFORE "Custody Chain Validation Functions"
LINE_CUSTODY=$(grep -n "Custody Chain Validation Functions" "$TARGET_FILE" | head -1 | cut -d: -f1)

if [ -n "$LINE_DUAL" ] && [ -n "$LINE_CUSTODY" ] && [ "$LINE_DUAL" -lt "$LINE_CUSTODY" ]; then
    run_test "validate_dual_path appears BEFORE Custody Chain Validation Functions" 0
else
    run_test "validate_dual_path appears BEFORE Custody Chain Validation Functions" 1
fi

# Test 5: Function is numbered as 7th validation function
grep -qE "^### 7\. validate_dual_path" "$TARGET_FILE"
run_test "validate_dual_path is the 7th validation function (### 7.)" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1

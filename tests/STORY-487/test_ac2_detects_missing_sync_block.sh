#!/bin/bash
# Test: AC#2 - Function detects .claude/ paths without dual_path_sync block
# Story: STORY-487
# Generated: 2026-02-23
# RED PHASE: These tests FAIL until the function is implemented.
#
# Validates:
#   - validate_dual_path() documents detection of .claude/ paths missing dual_path_sync
#   - MISSING_DUAL_PATH_SYNC violation type is defined in the function
#   - Function logic references checking for dual_path_sync block presence

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

echo "=== AC#2: Function detects .claude/ paths without dual_path_sync block ==="
echo "Target: $TARGET_FILE"
echo ""

# Test 1: MISSING_DUAL_PATH_SYNC violation type appears in function
grep -q "MISSING_DUAL_PATH_SYNC" "$TARGET_FILE"
run_test "MISSING_DUAL_PATH_SYNC violation type defined" $?

# Test 2: Function checks for .claude/ path pattern
grep -q '\.claude/' "$TARGET_FILE"
run_test "Function references .claude/ path pattern for detection" $?

# Test 3: Function checks for dual_path_sync block
grep -q "dual_path_sync" "$TARGET_FILE"
run_test "Function references dual_path_sync block check" $?

# Test 4: MISSING_DUAL_PATH_SYNC appears within the validate_dual_path function section
# (Not in some other section)
LINE_FUNC_START=$(grep -n "validate_dual_path" "$TARGET_FILE" | head -1 | cut -d: -f1)
LINE_VIOLATION=$(grep -n "MISSING_DUAL_PATH_SYNC" "$TARGET_FILE" | head -1 | cut -d: -f1)
LINE_CUSTODY=$(grep -n "Custody Chain Validation Functions" "$TARGET_FILE" | head -1 | cut -d: -f1)

if [ -n "$LINE_FUNC_START" ] && [ -n "$LINE_VIOLATION" ] && [ -n "$LINE_CUSTODY" ] \
   && [ "$LINE_VIOLATION" -gt "$LINE_FUNC_START" ] && [ "$LINE_VIOLATION" -lt "$LINE_CUSTODY" ]; then
    run_test "MISSING_DUAL_PATH_SYNC violation defined within validate_dual_path section" 0
else
    run_test "MISSING_DUAL_PATH_SYNC violation defined within validate_dual_path section" 1
fi

# Test 5: Function severity is defined (should be HIGH or CRITICAL for missing sync)
# Check within the validate_dual_path function block
LINE_FUNC_END="${LINE_CUSTODY:-9999}"
if [ -n "$LINE_FUNC_START" ]; then
    FUNC_CONTENT=$(sed -n "${LINE_FUNC_START},${LINE_FUNC_END}p" "$TARGET_FILE" 2>/dev/null)
    echo "$FUNC_CONTENT" | grep -qE '"severity".*"(HIGH|CRITICAL)"'
    run_test "MISSING_DUAL_PATH_SYNC violation has severity of HIGH or CRITICAL" $?
else
    run_test "MISSING_DUAL_PATH_SYNC violation has severity of HIGH or CRITICAL" 1
fi

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1

#!/bin/bash
# Test: AC#6 - /validate-stories Phase 2 invokes validate_dual_path() as 7th check
# Story: STORY-487
# Generated: 2026-02-23
# RED PHASE: These tests FAIL until the function is implemented.
#
# Validates:
#   - validate_dual_path() is called in Phase 2 of validate-stories.md
#   - It appears as the 7th validation call (after the existing 6)
#   - It is gated by context_status check (consistent with other validators)

PASSED=0
FAILED=0

TARGET_FILE="/mnt/c/Projects/DevForgeAI2/src/claude/commands/validate-stories.md"

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

echo "=== AC#6: /validate-stories Phase 2 invokes validate_dual_path() as 7th check ==="
echo "Target: $TARGET_FILE"
echo ""

# Test 1: validate_dual_path appears anywhere in validate-stories.md
grep -q "validate_dual_path" "$TARGET_FILE"
run_test "validate_dual_path referenced in validate-stories.md" $?

# Test 2: validate_dual_path appears in the Phase 2 section
LINE_PHASE2=$(grep -n "Phase 2: Context Validation" "$TARGET_FILE" | head -1 | cut -d: -f1)
LINE_PHASE3=$(grep -n "^### Phase 3" "$TARGET_FILE" | head -1 | cut -d: -f1)
LINE_DUAL=$(grep -n "validate_dual_path" "$TARGET_FILE" | head -1 | cut -d: -f1)

if [ -n "$LINE_PHASE2" ] && [ -n "$LINE_DUAL" ] && [ "$LINE_DUAL" -gt "$LINE_PHASE2" ]; then
    # Check it's before Phase 3 if Phase 3 exists
    if [ -n "$LINE_PHASE3" ]; then
        if [ "$LINE_DUAL" -lt "$LINE_PHASE3" ]; then
            run_test "validate_dual_path invoked within Phase 2 section" 0
        else
            run_test "validate_dual_path invoked within Phase 2 section" 1
        fi
    else
        run_test "validate_dual_path invoked within Phase 2 section" 0
    fi
else
    run_test "validate_dual_path invoked within Phase 2 section" 1
fi

# Test 3: validate_dual_path call appears AFTER all 6 existing validate_* calls
# The 6th existing call is validate_anti_patterns (line 231 in original)
LINE_ANTI_CALL=$(grep -n "validate_anti_patterns" "$TARGET_FILE" | tail -1 | cut -d: -f1)

if [ -n "$LINE_ANTI_CALL" ] && [ -n "$LINE_DUAL" ] && [ "$LINE_DUAL" -gt "$LINE_ANTI_CALL" ]; then
    run_test "validate_dual_path call appears AFTER validate_anti_patterns call" 0
else
    run_test "validate_dual_path call appears AFTER validate_anti_patterns call" 1
fi

# Test 4: Invocation follows the same pattern as other validators
# Pattern: violations.extend(validate_dual_path(...))
grep -qE "violations\.extend\(validate_dual_path" "$TARGET_FILE"
run_test "validate_dual_path invoked with violations.extend() pattern" $?

# Test 5: Invocation is gated by context_status check (consistent pattern)
# Pattern: IF context_status.source_tree: violations.extend(validate_dual_path
# (dual path validation requires source-tree.md to be present)
grep -qE "context_status.*validate_dual_path|IF.*context_status.*\n.*validate_dual_path" "$TARGET_FILE"
if [ $? -ne 0 ]; then
    # Try multiline: the context_status gate may be on the line before
    LINE_DUAL_CALL=$(grep -n "validate_dual_path" "$TARGET_FILE" | head -1 | cut -d: -f1)
    if [ -n "$LINE_DUAL_CALL" ]; then
        PREV_LINE=$((LINE_DUAL_CALL - 1))
        CONTEXT_CHECK=$(sed -n "${PREV_LINE}p" "$TARGET_FILE")
        echo "$CONTEXT_CHECK" | grep -qE "context_status|IF.*source_tree"
        run_test "validate_dual_path gated by context_status check" $?
    else
        run_test "validate_dual_path gated by context_status check" 1
    fi
else
    run_test "validate_dual_path gated by context_status check" 0
fi

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1

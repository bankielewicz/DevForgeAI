#!/bin/bash
# Test: AC#4 - Function exempts non-dual-path files
# Story: STORY-487
# Generated: 2026-02-23
# RED PHASE: These tests FAIL until the function is implemented.
#
# Validates:
#   - devforgeai/specs/ paths are explicitly exempted
#   - CLAUDE.md is explicitly exempted
#   - tests/ paths are explicitly exempted
#   - Exemptions return zero violations

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

echo "=== AC#4: Function exempts non-dual-path files ==="
echo "Target: $TARGET_FILE"
echo ""

# Extract the validate_dual_path function section
LINE_FUNC_START=$(grep -n "validate_dual_path" "$TARGET_FILE" | head -1 | cut -d: -f1)
LINE_CUSTODY=$(grep -n "Custody Chain Validation Functions" "$TARGET_FILE" | head -1 | cut -d: -f1)

if [ -z "$LINE_FUNC_START" ] || [ -z "$LINE_CUSTODY" ]; then
    echo "  FAIL: validate_dual_path function section not found - cannot extract function content"
    ((FAILED+=5))
    echo ""
    echo "Results: $PASSED passed, $FAILED failed"
    exit 1
fi

FUNC_CONTENT=$(sed -n "${LINE_FUNC_START},${LINE_CUSTODY}p" "$TARGET_FILE" 2>/dev/null)

# Test 1: devforgeai/specs/ is listed as an exempted path
echo "$FUNC_CONTENT" | grep -qE 'devforgeai/specs/'
run_test "devforgeai/specs/ path listed as exemption in function" $?

# Test 2: CLAUDE.md is listed as an exempted file
echo "$FUNC_CONTENT" | grep -q 'CLAUDE\.md'
run_test "CLAUDE.md listed as exemption in function" $?

# Test 3: tests/ is listed as an exempted path
echo "$FUNC_CONTENT" | grep -qE 'tests/'
run_test "tests/ path listed as exemption in function" $?

# Test 4: Exemptions use skip/continue/exempt pattern (not violations)
echo "$FUNC_CONTENT" | grep -qiE 'skip|exempt|SKIP|continue|ignore'
run_test "Function uses skip/exempt pattern for exempted paths" $?

# Test 5: Exempt paths do not trigger MISSING_DUAL_PATH_SYNC
# The exemption check should appear BEFORE the violation append
LINE_EXEMPT=$(echo "$FUNC_CONTENT" | grep -n "devforgeai/specs/" | head -1 | cut -d: -f1)
LINE_VIOLATION=$(echo "$FUNC_CONTENT" | grep -n "MISSING_DUAL_PATH_SYNC" | head -1 | cut -d: -f1)

if [ -n "$LINE_EXEMPT" ] && [ -n "$LINE_VIOLATION" ] && [ "$LINE_EXEMPT" -lt "$LINE_VIOLATION" ]; then
    run_test "Exemption check appears BEFORE violation append" 0
else
    run_test "Exemption check appears BEFORE violation append" 1
fi

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1

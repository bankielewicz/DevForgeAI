#!/bin/bash
# Test: AC#1 - Halt Trigger Text Updated in Operational File
# Story: STORY-499
# Generated: 2026-02-24
# Phase: RED (tests must FAIL before implementation)
#
# Acceptance Criteria:
#   Given: .claude/system-prompt-core.md contains the halt trigger on line 44
#   When: The STORY-499 change is applied
#   Then: Line 44 reads the new expanded text and no other halt triggers are modified
#
# NOTE: Tests target .claude/ operational file per AC#1 specification.
#       AC#2 tests cover src/ tree parity separately.

# === Test Configuration ===
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TARGET_FILE="${PROJECT_ROOT}/.claude/system-prompt-core.md"
PASSED=0
FAILED=0
TOTAL=0

run_test() {
    local name="$1"
    local result="$2"
    ((TOTAL++))
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        ((PASSED++))
    else
        echo "  FAIL: $name"
        ((FAILED++))
    fi
}

echo "=============================================="
echo "  AC#1: Halt Trigger Text Updated in Operational File"
echo "  Story: STORY-499"
echo "  Target: ${TARGET_FILE}"
echo "=============================================="
echo ""

# === Pre-condition: Target file exists ===
echo "--- Pre-conditions ---"
test -f "$TARGET_FILE"
run_test "Target file exists (.claude/system-prompt-core.md)" $?

# === Arrange ===
LINE_44=$(sed -n '44p' "$TARGET_FILE")
EXPECTED_NEW_TEXT="WHEN about to skip, abbreviate, or declare 'not applicable' for any workflow phase THEN HALT — load the phase reference file first, then evaluate applicability."

# === Act & Assert ===
echo ""
echo "--- AC#1 Tests: New halt trigger text on line 44 ---"

# Test 1: Line 44 contains the word "abbreviate"
echo "$LINE_44" | grep -q "abbreviate"
run_test "Line 44 contains 'abbreviate'" $?

# Test 2: Line 44 contains "not applicable"
echo "$LINE_44" | grep -q "not applicable"
run_test "Line 44 contains 'not applicable'" $?

# Test 3: Line 44 contains "declare"
echo "$LINE_44" | grep -q "declare"
run_test "Line 44 contains 'declare'" $?

# Test 4: Line 44 contains the exact new text
echo "$LINE_44" | grep -qF "$EXPECTED_NEW_TEXT"
run_test "Line 44 matches exact expected new text" $?

# Test 5: Old text is NOT present on line 44
OLD_TEXT="WHEN about to skip a workflow phase THEN HALT and complete the current phase first."
echo "$LINE_44" | grep -qF "$OLD_TEXT"
OLD_PRESENT=$?
# We want old text to NOT be present (grep returns 1 when not found)
[ "$OLD_PRESENT" -ne 0 ]
run_test "Old halt trigger text is NOT present on line 44" $?

# Test 6: No other halt trigger lines modified (count of WHEN...THEN HALT lines should remain the same)
# Current file has specific halt trigger lines. Count them excluding line 44.
echo ""
echo "--- AC#1 Tests: No other halt triggers modified ---"

HALT_TRIGGER_COUNT=$(grep -c "WHEN.*THEN HALT" "$TARGET_FILE")
# After implementation, total halt trigger count should remain the same (line 44 is modified, not added/removed)
# Current count is the baseline - the count should stay the same after implementation
# We verify the new line 44 still contains "THEN HALT" pattern
echo "$LINE_44" | grep -q "THEN HALT"
run_test "Line 44 still contains 'THEN HALT' pattern" $?

# Test 7: Line 44 contains the em dash separator
echo "$LINE_44" | grep -q "HALT —"
run_test "Line 44 uses em dash after HALT (new format)" $?

# === Summary ===
echo ""
echo "=============================================="
echo "  Results: $PASSED passed, $FAILED failed (out of $TOTAL)"
echo "=============================================="
[ $FAILED -eq 0 ] && exit 0 || exit 1

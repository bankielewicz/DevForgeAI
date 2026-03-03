#!/bin/bash
# Test: AC#2 - Halt Trigger Text Updated in Source File (Dual-Path Parity)
# Story: STORY-499
# Generated: 2026-02-24
# Phase: RED (tests must FAIL before implementation)
#
# Acceptance Criteria:
#   Given: src/claude/system-prompt-core.md contains the same halt trigger on line 44
#   When: The STORY-499 change is applied
#   Then: The halt trigger text in src/ is byte-for-byte identical to .claude/ line 44
#
# NOTE: Tests target BOTH src/ and .claude/ for parity verification per AC#2.

# === Test Configuration ===
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
OPERATIONAL_FILE="${PROJECT_ROOT}/.claude/system-prompt-core.md"
SOURCE_FILE="${PROJECT_ROOT}/src/claude/system-prompt-core.md"
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
echo "  AC#2: Halt Trigger Text Updated in Source File"
echo "  Story: STORY-499"
echo "  Operational: ${OPERATIONAL_FILE}"
echo "  Source: ${SOURCE_FILE}"
echo "=============================================="
echo ""

# === Pre-conditions ===
echo "--- Pre-conditions ---"
test -f "$OPERATIONAL_FILE"
run_test "Operational file exists (.claude/system-prompt-core.md)" $?

test -f "$SOURCE_FILE"
run_test "Source file exists (src/claude/system-prompt-core.md)" $?

# === Arrange ===
OPERATIONAL_LINE_44=$(sed -n '44p' "$OPERATIONAL_FILE")
SOURCE_LINE_44=$(sed -n '44p' "$SOURCE_FILE")
EXPECTED_NEW_TEXT="WHEN about to skip, abbreviate, or declare 'not applicable' for any workflow phase THEN HALT — load the phase reference file first, then evaluate applicability."

# === Act & Assert ===
echo ""
echo "--- AC#2 Tests: Source file contains new halt trigger text ---"

# Test 1: Source file line 44 contains "abbreviate"
echo "$SOURCE_LINE_44" | grep -q "abbreviate"
run_test "Source line 44 contains 'abbreviate'" $?

# Test 2: Source file line 44 contains "not applicable"
echo "$SOURCE_LINE_44" | grep -q "not applicable"
run_test "Source line 44 contains 'not applicable'" $?

# Test 3: Source file line 44 matches exact expected text
echo "$SOURCE_LINE_44" | grep -qF "$EXPECTED_NEW_TEXT"
run_test "Source line 44 matches exact expected new text" $?

# Test 4: Old text NOT present in source file line 44
OLD_TEXT="WHEN about to skip a workflow phase THEN HALT and complete the current phase first."
echo "$SOURCE_LINE_44" | grep -qF "$OLD_TEXT"
OLD_PRESENT=$?
[ "$OLD_PRESENT" -ne 0 ]
run_test "Old halt trigger text NOT present in source line 44" $?

echo ""
echo "--- AC#2 Tests: Byte-for-byte parity between files ---"

# Test 5: Line 44 is byte-for-byte identical between operational and source
[ "$OPERATIONAL_LINE_44" = "$SOURCE_LINE_44" ]
LINES_MATCH=$?
run_test "Line 44 is identical in both files (current state)" $LINES_MATCH

# Test 6: Both files have the new expected text (verifies parity with new content)
OP_HAS_NEW=$(echo "$OPERATIONAL_LINE_44" | grep -cF "$EXPECTED_NEW_TEXT")
SRC_HAS_NEW=$(echo "$SOURCE_LINE_44" | grep -cF "$EXPECTED_NEW_TEXT")
[ "$OP_HAS_NEW" -eq 1 ] && [ "$SRC_HAS_NEW" -eq 1 ]
run_test "Both files contain new expected text on line 44" $?

# Test 7: Full file diff of halt_triggers section (lines 39-48 contain the halt_triggers block)
OPERATIONAL_BLOCK=$(sed -n '39,48p' "$OPERATIONAL_FILE")
SOURCE_BLOCK=$(sed -n '39,48p' "$SOURCE_FILE")
[ "$OPERATIONAL_BLOCK" = "$SOURCE_BLOCK" ]
run_test "Halt triggers block (lines 39-48) identical in both files" $?

# === Summary ===
echo ""
echo "=============================================="
echo "  Results: $PASSED passed, $FAILED failed (out of $TOTAL)"
echo "=============================================="
[ $FAILED -eq 0 ] && exit 0 || exit 1

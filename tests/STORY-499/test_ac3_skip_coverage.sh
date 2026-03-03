#!/bin/bash
# Test: AC#3 - Original Skip Coverage Preserved
# Story: STORY-499
# Generated: 2026-02-24
# Phase: RED (tests must FAIL before implementation)
#
# Acceptance Criteria:
#   Given: The updated halt trigger text
#   When: The text is inspected
#   Then: The word "skip" is still present (backward compatibility)
#         AND three bypass patterns present: skip, abbreviate, not applicable
#
# NOTE: Tests both src/ and .claude/ files. The src/ file is the canonical
#       source per CLAUDE.md testing rules.

# === Test Configuration ===
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
SRC_FILE="${PROJECT_ROOT}/src/claude/system-prompt-core.md"
OP_FILE="${PROJECT_ROOT}/.claude/system-prompt-core.md"
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
echo "  AC#3: Original Skip Coverage Preserved"
echo "  Story: STORY-499"
echo "  Source: ${SRC_FILE}"
echo "=============================================="
echo ""

# === Arrange ===
SRC_LINE_44=$(sed -n '44p' "$SRC_FILE")
OP_LINE_44=$(sed -n '44p' "$OP_FILE")

# === Act & Assert ===
echo "--- AC#3 Tests: Backward compatibility (skip still present) ---"

# Test 1: Word "skip" is present in src/ line 44 (backward compatibility)
echo "$SRC_LINE_44" | grep -q "skip"
run_test "Word 'skip' present in src/ line 44 (backward compat)" $?

# Test 2: Word "skip" is present in .claude/ line 44
echo "$OP_LINE_44" | grep -q "skip"
run_test "Word 'skip' present in .claude/ line 44 (backward compat)" $?

echo ""
echo "--- AC#3 Tests: Three bypass patterns present ---"

# Test 3: Pattern 1 - "skip" present in new trigger text
echo "$SRC_LINE_44" | grep -q "skip"
SKIP_PRESENT=$?
run_test "Bypass pattern 1: 'skip' present" $SKIP_PRESENT

# Test 4: Pattern 2 - "abbreviate" present in new trigger text
echo "$SRC_LINE_44" | grep -q "abbreviate"
ABBREVIATE_PRESENT=$?
run_test "Bypass pattern 2: 'abbreviate' present" $ABBREVIATE_PRESENT

# Test 5: Pattern 3 - "not applicable" present in new trigger text
echo "$SRC_LINE_44" | grep -q "not applicable"
NA_PRESENT=$?
run_test "Bypass pattern 3: 'not applicable' present" $NA_PRESENT

# Test 6: All three patterns present simultaneously
[ "$SKIP_PRESENT" -eq 0 ] && [ "$ABBREVIATE_PRESENT" -eq 0 ] && [ "$NA_PRESENT" -eq 0 ]
run_test "All three bypass patterns present simultaneously" $?

# Test 7: The three patterns appear in a comma-separated list format
# Expected: "skip, abbreviate, or declare 'not applicable'"
echo "$SRC_LINE_44" | grep -q "skip, abbreviate, or declare"
run_test "Three patterns in comma-separated format ('skip, abbreviate, or declare')" $?

echo ""
echo "--- AC#3 Tests: No regression (halt trigger count unchanged) ---"

# Test 8: Total halt trigger count in src/ file unchanged
# Current file has exactly 5 WHEN...THEN lines in halt_triggers block (lines 42-47)
SRC_HALT_COUNT=$(grep -c "^WHEN.*THEN" "$SRC_FILE")
[ "$SRC_HALT_COUNT" -ge 5 ]
run_test "Source file has at least 5 halt trigger lines (no triggers removed)" $?

# === Summary ===
echo ""
echo "=============================================="
echo "  Results: $PASSED passed, $FAILED failed (out of $TOTAL)"
echo "=============================================="
[ $FAILED -eq 0 ] && exit 0 || exit 1

#!/bin/bash
# Test: AC#4 - Prescriptive Action Includes Reference File Loading
# Story: STORY-499
# Generated: 2026-02-24
# Phase: RED (tests must FAIL before implementation)
#
# Acceptance Criteria:
#   Given: The updated halt trigger fires
#   When: An LLM executor encounters the halt
#   Then: The trigger text prescribes loading the phase reference file
#         before evaluating applicability (not just halting)
#
# NOTE: Tests both src/ and .claude/ files for completeness.

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
echo "  AC#4: Prescriptive Action Includes Reference File Loading"
echo "  Story: STORY-499"
echo "  Source: ${SRC_FILE}"
echo "=============================================="
echo ""

# === Arrange ===
SRC_LINE_44=$(sed -n '44p' "$SRC_FILE")
OP_LINE_44=$(sed -n '44p' "$OP_FILE")

# === Act & Assert ===
echo "--- AC#4 Tests: Prescriptive action in source file ---"

# Test 1: Source line 44 contains "load the phase reference file first"
echo "$SRC_LINE_44" | grep -q "load the phase reference file first"
run_test "Source line 44 contains 'load the phase reference file first'" $?

# Test 2: Source line 44 contains "evaluate applicability"
echo "$SRC_LINE_44" | grep -q "evaluate applicability"
run_test "Source line 44 contains 'evaluate applicability'" $?

# Test 3: Source line 44 prescribes loading BEFORE evaluating (order check)
# The text should read "load...first, then evaluate" - checking the sequencing
echo "$SRC_LINE_44" | grep -q "load the phase reference file first, then evaluate applicability"
run_test "Source line 44 prescribes load-then-evaluate sequence" $?

# Test 4: Source line 44 does NOT just say "HALT and complete" (old prescriptive action)
echo "$SRC_LINE_44" | grep -q "HALT and complete the current phase first"
OLD_ACTION_PRESENT=$?
[ "$OLD_ACTION_PRESENT" -ne 0 ]
run_test "Old prescriptive action ('HALT and complete') NOT present in source" $?

echo ""
echo "--- AC#4 Tests: Prescriptive action in operational file ---"

# Test 5: Operational line 44 contains "load the phase reference file first"
echo "$OP_LINE_44" | grep -q "load the phase reference file first"
run_test "Operational line 44 contains 'load the phase reference file first'" $?

# Test 6: Operational line 44 contains "evaluate applicability"
echo "$OP_LINE_44" | grep -q "evaluate applicability"
run_test "Operational line 44 contains 'evaluate applicability'" $?

# Test 7: Operational line 44 prescribes load-then-evaluate sequence
echo "$OP_LINE_44" | grep -q "load the phase reference file first, then evaluate applicability"
run_test "Operational line 44 prescribes load-then-evaluate sequence" $?

# Test 8: The new action replaces a simple halt with a two-step procedure
# Verify the trigger contains both "HALT" and "load" (two-step: halt then load)
echo "$SRC_LINE_44" | grep -q "HALT" && echo "$SRC_LINE_44" | grep -q "load"
run_test "Trigger contains both HALT and load (two-step procedure)" $?

# === Summary ===
echo ""
echo "=============================================="
echo "  Results: $PASSED passed, $FAILED failed (out of $TOTAL)"
echo "=============================================="
[ $FAILED -eq 0 ] && exit 0 || exit 1

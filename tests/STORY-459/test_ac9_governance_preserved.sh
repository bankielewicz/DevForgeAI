#!/bin/bash
# Test: AC#9 - Governance, integration, and architecture documentation preserved
# Story: STORY-459
# Generated: 2026-02-20
# Phase: TDD Red (tests MUST fail before implementation)
#
# Validates:
# - Integration with implementing-stories section preserved (3 skill changes + 3 no-changes)
# - Integration Pattern (REC-1 automatic + REC-2 manual paths) preserved
# - Success Indicators (7 items + UX before/after) preserved

set -uo pipefail

# === Test Configuration ===
PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
COMMAND_FILE="${PROJECT_ROOT}/src/claude/commands/resume-dev.md"
REFERENCE_FILE="${PROJECT_ROOT}/src/claude/skills/implementing-stories/references/resume-detection.md"
PASSED=0
FAILED=0
TOTAL=0

# Combined content from both files for preservation checks
get_combined_content() {
    local content=""
    if [ -f "$COMMAND_FILE" ]; then
        content=$(cat "$COMMAND_FILE")
    fi
    if [ -f "$REFERENCE_FILE" ]; then
        content="${content}$(cat "$REFERENCE_FILE")"
    fi
    echo "$content"
}

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

echo "=========================================="
echo "  AC#9: Governance Preservation Tests"
echo "  Story: STORY-459"
echo "=========================================="
echo ""

# --- Pre-condition: Command file exists ---
if [ ! -f "$COMMAND_FILE" ]; then
    echo "  FATAL: Command file not found: $COMMAND_FILE"
    exit 1
fi

COMBINED=$(get_combined_content)

# === Integration with implementing-stories ===

# Test 1: Integration with implementing-stories section exists
echo "$COMBINED" | grep -q -i -E '(Integration with implementing-stories|Integration.*Skill)'
run_test "Integration with implementing-stories section preserved" $?

# Test 2: Parameter Extraction skill change mentioned
echo "$COMBINED" | grep -q -i "Parameter Extraction"
run_test "Skill change: Parameter Extraction documented" $?

# Test 3: Phase skip logic skill change mentioned
echo "$COMBINED" | grep -q -i -E '(Phase.*skip|skip.*Phase|GOTO Phase)'
run_test "Skill change: Phase skip / GOTO Phase logic documented" $?

# === Integration Pattern ===

# Test 4: REC-1 (automatic path) preserved
echo "$COMBINED" | grep -q "REC-1"
run_test "Integration Pattern: REC-1 (automatic path) preserved" $?

# Test 5: REC-2 (manual path) preserved
echo "$COMBINED" | grep -q "REC-2"
run_test "Integration Pattern: REC-2 (manual path) preserved" $?

# Test 6: Integration Pattern section with workflow diagram
echo "$COMBINED" | grep -q -i "Integration Pattern"
run_test "Integration Pattern section preserved" $?

# === Success Indicators ===

# Test 7: Success Indicators section exists
echo "$COMBINED" | grep -q -i "Success Indicators"
run_test "Success Indicators section preserved" $?

# Test 8: UX before/after narrative exists
echo "$COMBINED" | grep -q -i -E '(UX.*before|before.*after|Before.*UX|After.*UX)'
run_test "Success Indicators: UX before/after narrative preserved" $?

# === Summary ===
echo ""
echo "=========================================="
echo "  Results: $PASSED passed, $FAILED failed out of $TOTAL tests"
echo "=========================================="
[ "$FAILED" -eq 0 ] && exit 0 || exit 1

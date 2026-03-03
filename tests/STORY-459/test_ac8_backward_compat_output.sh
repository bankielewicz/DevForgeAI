#!/bin/bash
# Test: AC#8 - Backward-compatible output for all command modes and display formats
# Story: STORY-459
# Generated: 2026-02-20
# Phase: TDD Red (tests MUST fail before implementation)
#
# Validates that ALL original content is preserved across command + reference:
# - 4 Use Cases preserved (Fix Test Failures, Complete Documentation, Auto-Detect, Second Run)
# - 3 error types preserved (story complete, not started, invalid phase)
# - 2 Examples preserved (manual mode, auto-detect mode)
# - Comparison table (/dev vs /resume-dev)
# - Related Commands, Integration Pattern, Success Indicators

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
echo "  AC#8: Backward-Compatible Output Tests"
echo "  Story: STORY-459"
echo "=========================================="
echo ""

# --- Pre-condition: Command file exists ---
if [ ! -f "$COMMAND_FILE" ]; then
    echo "  FATAL: Command file not found: $COMMAND_FILE"
    exit 1
fi

COMBINED=$(get_combined_content)

# === Use Cases (4 required) ===

# Test 1: Fix Test Failures use case
echo "$COMBINED" | grep -q -i "Fix Test Failures"
run_test "Use Case: 'Fix Test Failures' preserved" $?

# Test 2: Complete Documentation use case
echo "$COMBINED" | grep -q -i "Complete Documentation"
run_test "Use Case: 'Complete Documentation' preserved" $?

# Test 3: Auto-Detect use case
echo "$COMBINED" | grep -q -i "Auto-Detect"
run_test "Use Case: 'Auto-Detect' preserved" $?

# Test 4: Second Run use case
echo "$COMBINED" | grep -q -i "Second Run"
run_test "Use Case: 'Second Run' preserved" $?

# === Error Types (3 required) ===

# Test 5: Story complete error
echo "$COMBINED" | grep -q -i -E '(story.*complete|already.*complete|100%.*complete)'
run_test "Error type: story complete error preserved" $?

# Test 6: Story not started error
echo "$COMBINED" | grep -q -i -E '(not.*started|never.*started|Backlog)'
run_test "Error type: story not started error preserved" $?

# Test 7: Invalid phase error
echo "$COMBINED" | grep -q -i -E '(invalid.*phase|phase.*invalid|valid.*range)'
run_test "Error type: invalid phase error preserved" $?

# === Examples (2 required) ===

# Test 8: Manual mode example with terminal output
echo "$COMBINED" | grep -q -E '/resume-dev.*STORY-[0-9]+.*[0-9]'
run_test "Example: manual mode example preserved" $?

# Test 9: Auto-detect mode example
echo "$COMBINED" | grep -q -E '/resume-dev.*STORY-[0-9]+[^0-9]'
run_test "Example: auto-detect mode example preserved" $?

# === Structural Content ===

# Test 10: Comparison table (/dev vs /resume-dev)
echo "$COMBINED" | grep -q -i -E '(/dev.*vs.*resume|resume.*vs.*/dev|Comparison)'
run_test "Comparison table (/dev vs /resume-dev) preserved" $?

# Test 11: Related Commands section
echo "$COMBINED" | grep -q -i "Related Commands"
run_test "Related Commands section preserved" $?

# Test 12: Integration Pattern section
echo "$COMBINED" | grep -q -i "Integration Pattern"
run_test "Integration Pattern section preserved" $?

# Test 13: Success Indicators section
echo "$COMBINED" | grep -q -i "Success Indicators"
run_test "Success Indicators section preserved" $?

# === Summary ===
echo ""
echo "=========================================="
echo "  Results: $PASSED passed, $FAILED failed out of $TOTAL tests"
echo "=========================================="
[ "$FAILED" -eq 0 ] && exit 0 || exit 1

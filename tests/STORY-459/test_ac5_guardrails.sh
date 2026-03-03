#!/bin/bash
# Test: AC#5 - Lean Orchestration Enforcement section added
# Story: STORY-459
# Generated: 2026-02-20
# Phase: TDD Red (tests MUST fail before implementation)
#
# Validates:
# - resume-dev.md contains "Lean Orchestration Enforcement" section
# - resume-dev.md has >=4 "DO NOT" items in that section
# - Specific DO NOT items verified: tech-stack-detector, DoD parsing,
#   checkpoint reading, resume phase determination

set -uo pipefail

# === Test Configuration ===
PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
COMMAND_FILE="${PROJECT_ROOT}/src/claude/commands/resume-dev.md"
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

echo "=========================================="
echo "  AC#5: Lean Orchestration Guardrails Tests"
echo "  Story: STORY-459"
echo "=========================================="
echo ""

# --- Pre-condition: File exists ---
if [ ! -f "$COMMAND_FILE" ]; then
    echo "  FATAL: Target file not found: $COMMAND_FILE"
    exit 1
fi

# === Test 1: resume-dev.md contains "Lean Orchestration Enforcement" section ===
grep -q "Lean Orchestration Enforcement" "$COMMAND_FILE"
run_test "resume-dev.md contains 'Lean Orchestration Enforcement' section" $?

# === Test 2: At least 4 "DO NOT" items exist in the file ===
# Count lines containing "DO NOT" (case sensitive, as guardrails use uppercase)
DO_NOT_COUNT=$(grep -c "DO NOT" "$COMMAND_FILE" || true)
echo "  [INFO] DO NOT item count: $DO_NOT_COUNT"
test "$DO_NOT_COUNT" -ge 4
run_test "resume-dev.md has >=4 'DO NOT' items (found: $DO_NOT_COUNT)" $?

# === Test 3: DO NOT run tech-stack-detector in command ===
grep -q "DO NOT.*tech-stack-detector" "$COMMAND_FILE"
run_test "Contains 'DO NOT run tech-stack-detector in command'" $?

# === Test 4: DO NOT parse DoD sections in command ===
grep -q "DO NOT.*DoD" "$COMMAND_FILE"
run_test "Contains 'DO NOT parse DoD sections in command'" $?

# === Test 5: DO NOT read checkpoint files in command ===
grep -q "DO NOT.*checkpoint" "$COMMAND_FILE"
run_test "Contains 'DO NOT read checkpoint files in command'" $?

# === Test 6: DO NOT determine resume phase in command ===
grep -q "DO NOT.*resume.*phase\|DO NOT.*phase.*determin" "$COMMAND_FILE"
run_test "Contains 'DO NOT determine resume phase in command'" $?

# === Summary ===
echo ""
echo "=========================================="
echo "  Results: $PASSED passed, $FAILED failed out of $TOTAL tests"
echo "=========================================="
[ "$FAILED" -eq 0 ] && exit 0 || exit 1

#!/bin/bash
# Test: AC#5 - Validation Gate Specificity
# Story: STORY-532
# Generated: 2026-03-04
# Validates: milestone-generator.md specifies concrete binary pass/fail validation gates

set -euo pipefail

# === Test Configuration ===
PASSED=0
FAILED=0
TARGET_FILE="src/claude/skills/planning-business/references/milestone-generator.md"
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TARGET_PATH="${PROJECT_ROOT}/${TARGET_FILE}"

run_test() {
    local name="$1"
    local result="$2"
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        PASSED=$((PASSED + 1))
    else
        echo "  FAIL: $name"
        FAILED=$((FAILED + 1))
    fi
}

echo "=== AC#5: Validation Gate Specificity ==="
echo "Target: ${TARGET_FILE}"
echo ""

# --- Test 1: Source file exists ---
test_result=0
[ -f "$TARGET_PATH" ] || test_result=1
run_test "test_milestone_generator_file_exists_returns_true" $test_result

# --- Test 2: Validation gates are defined ---
test_result=0
if [ -f "$TARGET_PATH" ]; then
    grep -qi 'validation_gate' "$TARGET_PATH" 2>/dev/null || test_result=1
else
    test_result=1
fi
run_test "test_validation_gate_field_defined" $test_result

# --- Test 3: Gates described as binary/pass-fail ---
test_result=0
if [ -f "$TARGET_PATH" ]; then
    grep -qiE '(binary|pass.?fail|concrete|verifiable|measurable|done.?not.?done)' "$TARGET_PATH" 2>/dev/null || test_result=1
else
    test_result=1
fi
run_test "test_gates_described_as_binary_pass_fail" $test_result

# --- Test 4: Vague language explicitly prohibited ---
test_result=0
if [ -f "$TARGET_PATH" ]; then
    grep -qiE '(feels ready|good enough|vague|subjective)' "$TARGET_PATH" 2>/dev/null || test_result=1
else
    test_result=1
fi
run_test "test_vague_language_explicitly_prohibited" $test_result

# --- Test 5: At least 10 concrete validation gates present (one per milestone) ---
test_result=0
if [ -f "$TARGET_PATH" ]; then
    gate_count=$(grep -ci 'validation_gate' "$TARGET_PATH" 2>/dev/null || echo "0")
    [ "$gate_count" -ge 10 ] || test_result=1
else
    test_result=1
fi
run_test "test_at_least_10_validation_gates_present" $test_result

# --- Test 6: No vague gates in actual milestone definitions ---
# Checks that the file does NOT contain vague validation gate values
test_result=0
if [ -f "$TARGET_PATH" ]; then
    # If file exists, check that no validation_gate line contains vague terms
    vague_gates=$(grep -iE 'validation_gate.*:.*( feels | good enough | ready enough | probably )' "$TARGET_PATH" 2>/dev/null | wc -l || true)
    [ "$vague_gates" -eq 0 ] || test_result=1
    # But file must exist first - if no file, fail
    [ -f "$TARGET_PATH" ] || test_result=1
else
    test_result=1
fi
run_test "test_no_vague_validation_gate_values_in_milestones" $test_result

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed out of $((PASSED + FAILED)) tests"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1

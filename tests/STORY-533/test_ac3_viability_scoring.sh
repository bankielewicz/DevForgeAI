#!/bin/bash
# Test: AC#3 - Viability Scoring Rubric with Pass/Fail
# Story: STORY-533
# Generated: 2026-03-04

# === Test Configuration ===
PASSED=0
FAILED=0
TARGET_FILE="src/claude/skills/planning-business/references/viability-scoring.md"

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

echo "=== AC#3: Viability Scoring Rubric ==="
echo ""

# --- Act & Assert ---

# Test 1: File exists
test -f "$TARGET_FILE"
run_test "test_should_exist_when_viability_scoring_file_created" $?

# Test 2: Scoring rubric section present
grep -qi "scoring rubric\|rubric" "$TARGET_FILE" 2>/dev/null
run_test "test_should_contain_scoring_rubric_when_rubric_defined" $?

# Test 3: Numeric dimensions with weights
grep -qi "weight" "$TARGET_FILE" 2>/dev/null
run_test "test_should_contain_weights_when_scoring_dimensions_defined" $?

# Test 4: PASS threshold >= 70
grep -q "70" "$TARGET_FILE" 2>/dev/null && grep -qi "PASS" "$TARGET_FILE" 2>/dev/null
run_test "test_should_define_pass_threshold_at_70_when_thresholds_defined" $?

# Test 5: BORDERLINE threshold 50-69
grep -q "50" "$TARGET_FILE" 2>/dev/null && grep -qi "BORDERLINE" "$TARGET_FILE" 2>/dev/null
run_test "test_should_define_borderline_threshold_50_69_when_thresholds_defined" $?

# Test 6: FAIL threshold < 50
grep -qi "FAIL" "$TARGET_FILE" 2>/dev/null && grep -q "50" "$TARGET_FILE" 2>/dev/null
run_test "test_should_define_fail_threshold_below_50_when_thresholds_defined" $?

# Test 7: Per-dimension breakdowns present
grep -qi "dimension" "$TARGET_FILE" 2>/dev/null
run_test "test_should_contain_dimension_breakdowns_when_scoring_detailed" $?

# Test 8: At least 3 scoring dimensions defined
DIMENSION_COUNT=$(grep -ci "dimension\|score.*:" "$TARGET_FILE" 2>/dev/null || echo 0)
[ "$DIMENSION_COUNT" -ge 3 ]
run_test "test_should_have_at_least_3_dimensions_when_rubric_complete" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed out of $((PASSED + FAILED)) tests"
[ $FAILED -eq 0 ] && exit 0 || exit 1

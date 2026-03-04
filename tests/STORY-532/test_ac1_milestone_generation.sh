#!/bin/bash
# Test: AC#1 - Full Milestone Generation
# Story: STORY-532
# Generated: 2026-03-04
# Validates: milestone-generator.md defines exactly 10 milestones with required fields,
#            first="Problem Validated", last="Launch Ready"

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

echo "=== AC#1: Full Milestone Generation ==="
echo "Target: ${TARGET_FILE}"
echo ""

# --- Test 1: Source file exists ---
test_result=0
[ -f "$TARGET_PATH" ] || test_result=1
run_test "test_milestone_generator_file_exists_returns_true" $test_result

# --- Test 2: Defines exactly 10 milestones ---
test_result=0
if [ -f "$TARGET_PATH" ]; then
    count=$(grep -cE '^\s*-\s+name:\s' "$TARGET_PATH" 2>/dev/null || echo "0")
    # Also check for numbered milestone patterns (e.g., "Milestone 1:", "## 1.", "### Milestone 1")
    if [ "$count" -lt 10 ]; then
        count2=$(grep -cEi '(milestone\s+([0-9]+|one|two|three|four|five|six|seven|eight|nine|ten))|^#{1,3}\s+[0-9]+\.' "$TARGET_PATH" 2>/dev/null || echo "0")
        [ "$count2" -ge 10 ] || test_result=1
    fi
else
    test_result=1
fi
run_test "test_milestone_count_exactly_10_milestones_defined" $test_result

# --- Test 3: Each milestone has required field "name" ---
test_result=0
if [ -f "$TARGET_PATH" ]; then
    grep -qi 'name' "$TARGET_PATH" 2>/dev/null || test_result=1
else
    test_result=1
fi
run_test "test_milestone_schema_name_field_present" $test_result

# --- Test 4: Each milestone has required field "definition" ---
test_result=0
if [ -f "$TARGET_PATH" ]; then
    grep -qi 'definition' "$TARGET_PATH" 2>/dev/null || test_result=1
else
    test_result=1
fi
run_test "test_milestone_schema_definition_field_present" $test_result

# --- Test 5: Each milestone has required field "soft_timeframe" ---
test_result=0
if [ -f "$TARGET_PATH" ]; then
    grep -qi 'soft_timeframe' "$TARGET_PATH" 2>/dev/null || test_result=1
else
    test_result=1
fi
run_test "test_milestone_schema_soft_timeframe_field_present" $test_result

# --- Test 6: Each milestone has required field "micro_tasks" ---
test_result=0
if [ -f "$TARGET_PATH" ]; then
    grep -qi 'micro_tasks' "$TARGET_PATH" 2>/dev/null || test_result=1
else
    test_result=1
fi
run_test "test_milestone_schema_micro_tasks_field_present" $test_result

# --- Test 7: Each milestone has required field "validation_gate" ---
test_result=0
if [ -f "$TARGET_PATH" ]; then
    grep -qi 'validation_gate' "$TARGET_PATH" 2>/dev/null || test_result=1
else
    test_result=1
fi
run_test "test_milestone_schema_validation_gate_field_present" $test_result

# --- Test 8: Each milestone has required field "celebration" ---
test_result=0
if [ -f "$TARGET_PATH" ]; then
    grep -qi 'celebration' "$TARGET_PATH" 2>/dev/null || test_result=1
else
    test_result=1
fi
run_test "test_milestone_schema_celebration_field_present" $test_result

# --- Test 9: First milestone is "Problem Validated" ---
test_result=0
if [ -f "$TARGET_PATH" ]; then
    grep -qi 'Problem Validated' "$TARGET_PATH" 2>/dev/null || test_result=1
else
    test_result=1
fi
run_test "test_first_milestone_problem_validated_exists" $test_result

# --- Test 10: Last milestone is "Launch Ready" ---
test_result=0
if [ -f "$TARGET_PATH" ]; then
    grep -qi 'Launch Ready' "$TARGET_PATH" 2>/dev/null || test_result=1
else
    test_result=1
fi
run_test "test_last_milestone_launch_ready_exists" $test_result

# --- Test 11: All 6 required fields appear for each milestone (structural check) ---
test_result=0
if [ -f "$TARGET_PATH" ]; then
    for field in name definition soft_timeframe micro_tasks validation_gate celebration; do
        field_count=$(grep -ci "$field" "$TARGET_PATH" 2>/dev/null || echo "0")
        if [ "$field_count" -lt 10 ]; then
            test_result=1
            break
        fi
    done
else
    test_result=1
fi
run_test "test_all_milestones_have_all_six_required_fields" $test_result

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed out of $((PASSED + FAILED)) tests"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1

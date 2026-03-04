#!/bin/bash
# Test: AC#2 - Soft Timeframe Guard Rails
# Story: STORY-532
# Generated: 2026-03-04
# Validates: milestone-generator.md specifies guard rails (min 7 days, 180-day recalibration trigger)

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

echo "=== AC#2: Soft Timeframe Guard Rails ==="
echo "Target: ${TARGET_FILE}"
echo ""

# --- Test 1: Source file exists ---
test_result=0
[ -f "$TARGET_PATH" ] || test_result=1
run_test "test_milestone_generator_file_exists_returns_true" $test_result

# --- Test 2: Guard rails section exists ---
test_result=0
if [ -f "$TARGET_PATH" ]; then
    grep -qiE '(guard.?rail|timeframe.*(constraint|rule|limit)|constraint.*timeframe)' "$TARGET_PATH" 2>/dev/null || test_result=1
else
    test_result=1
fi
run_test "test_guard_rails_section_defined" $test_result

# --- Test 3: Minimum 7 days per milestone documented ---
test_result=0
if [ -f "$TARGET_PATH" ]; then
    grep -qE '(min.*7\s*day|7\s*day.*min|min_days.*7|minimum.*7)' "$TARGET_PATH" 2>/dev/null || test_result=1
else
    test_result=1
fi
run_test "test_minimum_7_days_per_milestone_specified" $test_result

# --- Test 4: No milestone min_days < 7 rule stated ---
test_result=0
if [ -f "$TARGET_PATH" ]; then
    grep -qiE '(no.*milestone.*(less|fewer|under|below).*7|min_days.*(>=|greater|least).*7|clamp.*7)' "$TARGET_PATH" 2>/dev/null || test_result=1
else
    test_result=1
fi
run_test "test_no_milestone_below_7_days_rule_present" $test_result

# --- Test 5: 180-day total duration reference ---
test_result=0
if [ -f "$TARGET_PATH" ]; then
    grep -qE '180' "$TARGET_PATH" 2>/dev/null || test_result=1
else
    test_result=1
fi
run_test "test_180_day_total_duration_referenced" $test_result

# --- Test 6: Recalibration trigger documented ---
test_result=0
if [ -f "$TARGET_PATH" ]; then
    grep -qi 'recalibration_trigger' "$TARGET_PATH" 2>/dev/null || test_result=1
else
    test_result=1
fi
run_test "test_recalibration_trigger_field_documented" $test_result

# --- Test 7: Recalibration fires when exceeding 180 days ---
test_result=0
if [ -f "$TARGET_PATH" ]; then
    grep -qiE '(exceed.*180.*recalibrat|recalibrat.*180|180.*trigger|total.*180.*true)' "$TARGET_PATH" 2>/dev/null || test_result=1
else
    test_result=1
fi
run_test "test_recalibration_trigger_fires_at_180_days" $test_result

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed out of $((PASSED + FAILED)) tests"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1

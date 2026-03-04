#!/bin/bash
# Test: AC#3 - Missing User Profile Handling
# Story: STORY-532
# Generated: 2026-03-04
# Validates: milestone-generator.md includes error handling for missing user-profile.yaml

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

echo "=== AC#3: Missing User Profile Handling ==="
echo "Target: ${TARGET_FILE}"
echo ""

# --- Test 1: Source file exists ---
test_result=0
[ -f "$TARGET_PATH" ] || test_result=1
run_test "test_milestone_generator_file_exists_returns_true" $test_result

# --- Test 2: References user-profile.yaml ---
test_result=0
if [ -f "$TARGET_PATH" ]; then
    grep -q 'user-profile.yaml' "$TARGET_PATH" 2>/dev/null || test_result=1
else
    test_result=1
fi
run_test "test_user_profile_yaml_referenced" $test_result

# --- Test 3: HALT behavior documented for missing profile ---
test_result=0
if [ -f "$TARGET_PATH" ]; then
    grep -qiE '(halt|stop|abort|error).*miss' "$TARGET_PATH" 2>/dev/null || \
    grep -qiE 'miss.*(halt|stop|abort|error)' "$TARGET_PATH" 2>/dev/null || test_result=1
else
    test_result=1
fi
run_test "test_halt_on_missing_profile_documented" $test_result

# --- Test 4: Specific error message present ---
test_result=0
if [ -f "$TARGET_PATH" ]; then
    grep -qi 'User profile not found' "$TARGET_PATH" 2>/dev/null || test_result=1
else
    test_result=1
fi
run_test "test_error_message_user_profile_not_found_present" $test_result

# --- Test 5: Instruction to run user-profile phase first ---
test_result=0
if [ -f "$TARGET_PATH" ]; then
    grep -qi 'user-profile phase first' "$TARGET_PATH" 2>/dev/null || test_result=1
else
    test_result=1
fi
run_test "test_instruction_run_user_profile_phase_first" $test_result

# --- Test 6: No milestones.yaml created on missing profile ---
test_result=0
if [ -f "$TARGET_PATH" ]; then
    grep -qiE '(no.*milestones.*creat|not.*creat.*milestones|milestones.*not.*overwr)' "$TARGET_PATH" 2>/dev/null || test_result=1
else
    test_result=1
fi
run_test "test_no_milestones_created_on_missing_profile" $test_result

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed out of $((PASSED + FAILED)) tests"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1

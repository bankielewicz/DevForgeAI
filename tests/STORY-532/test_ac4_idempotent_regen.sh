#!/bin/bash
# Test: AC#4 - Idempotent Re-generation
# Story: STORY-532
# Generated: 2026-03-04
# Validates: milestone-generator.md includes backup mechanism (milestones.yaml.bak) before overwrite

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

echo "=== AC#4: Idempotent Re-generation ==="
echo "Target: ${TARGET_FILE}"
echo ""

# --- Test 1: Source file exists ---
test_result=0
[ -f "$TARGET_PATH" ] || test_result=1
run_test "test_milestone_generator_file_exists_returns_true" $test_result

# --- Test 2: Backup mechanism documented ---
test_result=0
if [ -f "$TARGET_PATH" ]; then
    grep -qi 'backup' "$TARGET_PATH" 2>/dev/null || test_result=1
else
    test_result=1
fi
run_test "test_backup_mechanism_documented" $test_result

# --- Test 3: milestones.yaml.bak filename specified ---
test_result=0
if [ -f "$TARGET_PATH" ]; then
    grep -q 'milestones.yaml.bak' "$TARGET_PATH" 2>/dev/null || test_result=1
else
    test_result=1
fi
run_test "test_backup_filename_milestones_yaml_bak_specified" $test_result

# --- Test 4: Overwrite behavior documented ---
test_result=0
if [ -f "$TARGET_PATH" ]; then
    grep -qiE '(overwrit|replace|regenerat|re-generat|idempoten)' "$TARGET_PATH" 2>/dev/null || test_result=1
else
    test_result=1
fi
run_test "test_overwrite_behavior_documented" $test_result

# --- Test 5: Backup happens before overwrite (order specified) ---
test_result=0
if [ -f "$TARGET_PATH" ]; then
    grep -qiE '(backup.*before.*overwrit|preserve.*previous|copy.*bak.*before|backup.*prior)' "$TARGET_PATH" 2>/dev/null || test_result=1
else
    test_result=1
fi
run_test "test_backup_before_overwrite_order_specified" $test_result

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed out of $((PASSED + FAILED)) tests"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1

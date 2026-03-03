#!/bin/bash
# Test: AC#2 - Test Removal and Skip Decorator Detection
# Story: STORY-503
# Generated: 2026-02-27

# === Test Configuration ===
PASSED=0
FAILED=0
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TARGET_FILE="${PROJECT_ROOT}/src/claude/skills/devforgeai-qa/references/test-tampering-heuristics.md"

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

echo "=== AC#2: Test Removal and Skip Decorator Detection ==="

# === Test 1: Contains test_removal_skip_patterns section ===
grep -q -i "test.removal.skip.pattern" "$TARGET_FILE" 2>/dev/null
run_test "Contains test_removal_skip_patterns section" $?

# === Test 2: Documents deleted test functions detection ===
grep -q -i "deleted.*test.*function" "$TARGET_FILE" 2>/dev/null
run_test "Documents deleted test functions detection" $?

# === Test 3: Documents .skip suffix detection ===
grep -q "\.skip" "$TARGET_FILE" 2>/dev/null
run_test "Documents .skip suffix detection" $?

# === Test 4: Documents .xfail suffix detection ===
grep -q "\.xfail\|xfail" "$TARGET_FILE" 2>/dev/null
run_test "Documents .xfail suffix detection" $?

# === Test 5: Documents @unittest.skip decorator ===
grep -q "@unittest\.skip\|unittest\.skip" "$TARGET_FILE" 2>/dev/null
run_test "Documents @unittest.skip decorator detection" $?

# === Test 6: Documents @pytest.mark.skip decorator ===
grep -q "@pytest\.mark\.skip\|pytest\.mark\.skip" "$TARGET_FILE" 2>/dev/null
run_test "Documents @pytest.mark.skip decorator detection" $?

# === Test 7: All marked CRITICAL severity ===
grep -i "test.removal.skip" "$TARGET_FILE" 2>/dev/null | grep -q -i "critical"
run_test "Test removal/skip patterns marked CRITICAL severity" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1

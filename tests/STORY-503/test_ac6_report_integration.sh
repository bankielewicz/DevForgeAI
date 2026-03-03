#!/bin/bash
# Test: AC#6 - Findings Integrated into Diff Regression Report
# Story: STORY-503
# Generated: 2026-02-27

# === Test Configuration ===
PASSED=0
FAILED=0
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TARGET_FILE="${PROJECT_ROOT}/src/claude/skills/devforgeai-qa/references/test-tampering-heuristics.md"
INTEGRATION_FILE="${PROJECT_ROOT}/src/claude/skills/devforgeai-qa/references/diff-regression-detection.md"

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

echo "=== AC#6: Report Integration ==="

# === Test 1: Documents tampering_patterns array format ===
grep -q -i "tampering.patterns" "$TARGET_FILE" 2>/dev/null
run_test "Documents tampering_patterns array format" $?

# === Test 2: Documents file field in findings ===
grep -q -i "\"file\"\|file.*path" "$TARGET_FILE" 2>/dev/null
run_test "Documents file field in findings" $?

# === Test 3: Documents line field in findings ===
grep -q -i "\"line\"\|line.*number" "$TARGET_FILE" 2>/dev/null
run_test "Documents line field in findings" $?

# === Test 4: Documents type field with pattern types ===
grep -q -i "assertion_weakening\|test_removal_skip\|test_body_noop\|threshold_lowering" "$TARGET_FILE" 2>/dev/null
run_test "Documents type field with pattern type values" $?

# === Test 5: Documents before/after fields ===
grep -q -i "\"before\"\|\"after\"\|before.*content\|after.*content" "$TARGET_FILE" 2>/dev/null
run_test "Documents before/after fields in findings" $?

# === Test 6: Documents overall_verdict FAIL behavior ===
grep -q -i "overall.verdict.*FAIL\|verdict.*FAIL" "$TARGET_FILE" 2>/dev/null
run_test "Documents overall_verdict FAIL when patterns found" $?

# === Test 7: diff-regression-detection.md references test-tampering-heuristics ===
grep -q -i "test.tampering.heuristic" "$INTEGRATION_FILE" 2>/dev/null
run_test "diff-regression-detection.md references test-tampering-heuristics.md" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1

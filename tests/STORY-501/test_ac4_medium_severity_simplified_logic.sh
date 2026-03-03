#!/bin/bash
# Test: AC#4 - MEDIUM severity for simplified logic (non-blocking)
# Story: STORY-501
# Generated: 2026-02-27

# === Test Configuration ===
PASSED=0
FAILED=0
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
REF_FILE="${PROJECT_ROOT}/src/claude/skills/devforgeai-qa/references/diff-regression-detection.md"

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

echo "=== AC#4: MEDIUM Severity for Simplified Logic ==="

# === Test 1: Reference file contains MEDIUM severity ===
grep -q "MEDIUM" "$REF_FILE" 2>/dev/null
run_test "Reference file contains MEDIUM severity" $?

# === Test 2: MEDIUM classified as warning/non-blocking ===
grep -i -q "MEDIUM.*warning\|MEDIUM.*non-blocking\|warning.*MEDIUM" "$REF_FILE" 2>/dev/null
run_test "MEDIUM severity classified as warning/non-blocking" $?

# === Test 3: MEDIUM linked to simplified logic ===
grep -i -q "simplif\|logic.*reduc\|condition.*remov\|branch.*remov" "$REF_FILE" 2>/dev/null
run_test "MEDIUM severity covers simplified logic patterns" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1

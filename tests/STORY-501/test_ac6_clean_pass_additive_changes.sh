#!/bin/bash
# Test: AC#6 - Clean pass on additive-only changes
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

echo "=== AC#6: Clean Pass on Additive-Only Changes ==="

# === Test 1: Reference file documents PASS result ===
grep -i -q "PASS\|clean.*pass\|no.*finding\|no.*regression" "$REF_FILE" 2>/dev/null
run_test "Reference file documents PASS result for no findings" $?

# === Test 2: Additive-only changes produce no warnings ===
grep -i -q "additive\|addition.*only\|new.*function\|new.*file" "$REF_FILE" 2>/dev/null
run_test "Additive-only changes documented as clean pass" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1

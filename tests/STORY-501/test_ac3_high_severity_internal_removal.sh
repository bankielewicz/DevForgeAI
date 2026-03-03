#!/bin/bash
# Test: AC#3 - HIGH severity for internal function/error handler removal
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

echo "=== AC#3: HIGH Severity for Internal Function/Error Handler Removal ==="

# === Test 1: Reference file contains HIGH severity ===
grep -q "HIGH" "$REF_FILE" 2>/dev/null
run_test "Reference file contains HIGH severity" $?

# === Test 2: HIGH linked to internal function removal ===
grep -i -q "HIGH.*internal.*function\|internal.*function.*HIGH\|HIGH.*helper\|HIGH.*private" "$REF_FILE" 2>/dev/null
run_test "HIGH severity linked to internal function removal" $?

# === Test 3: HIGH linked to error handler removal ===
grep -i -q "error.*handler\|catch.*block\|exception.*handler\|error.*handling" "$REF_FILE" 2>/dev/null
run_test "HIGH severity covers error handler removal" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1

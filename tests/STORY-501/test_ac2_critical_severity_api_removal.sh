#!/bin/bash
# Test: AC#2 - CRITICAL severity for public API removal
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

echo "=== AC#2: CRITICAL Severity for Public API Removal ==="

# === Test 1: Reference file contains CRITICAL severity ===
grep -q "CRITICAL" "$REF_FILE" 2>/dev/null
run_test "Reference file contains CRITICAL severity" $?

# === Test 2: CRITICAL linked to public API removal ===
grep -i -q "CRITICAL.*public.*API\|public.*API.*CRITICAL" "$REF_FILE" 2>/dev/null
run_test "CRITICAL severity linked to public API removal" $?

# === Test 3: Blocking message pattern present ===
grep -i -q "block\|BLOCKING\|blocks.*QA\|blocks.*progression" "$REF_FILE" 2>/dev/null
run_test "Blocking message pattern present for CRITICAL" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1

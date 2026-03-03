#!/bin/bash
# Test: AC#5 - Function signature change detection
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

echo "=== AC#5: Function Signature Change Detection ==="

# === Test 1: Reference file contains signature change patterns ===
grep -i -q "signature.*change\|parameter.*change\|argument.*change\|signature.*modif" "$REF_FILE" 2>/dev/null
run_test "Reference file contains signature change detection patterns" $?

# === Test 2: Detection covers parameter additions/removals ===
grep -i -q "parameter.*remov\|parameter.*add\|argument.*remov\|argument.*add" "$REF_FILE" 2>/dev/null
run_test "Detection covers parameter additions/removals" $?

# === Test 3: Detection covers return type changes ===
grep -i -q "return.*type\|return.*change\|output.*type" "$REF_FILE" 2>/dev/null
run_test "Detection covers return type changes" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1

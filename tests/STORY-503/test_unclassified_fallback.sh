#!/bin/bash
# Test: BR-003 - Unclassified Modification Fallback
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

echo "=== BR-003: Unclassified Modification Fallback ==="

# === Test 1: Contains unclassified_fallback section ===
grep -q -i "unclassified.fallback" "$TARGET_FILE" 2>/dev/null
run_test "Contains unclassified_fallback section" $?

# === Test 2: Documents unclassified_modification finding type ===
grep -q -i "unclassified.modification" "$TARGET_FILE" 2>/dev/null
run_test "Documents unclassified_modification finding type" $?

# === Test 3: Unclassified modifications are CRITICAL ===
grep -i "unclassified" "$TARGET_FILE" 2>/dev/null | grep -q -i "critical"
run_test "Unclassified modifications produce CRITICAL findings" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
